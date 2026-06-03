# ingestion_raw/finding_client_raw.py

import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from pathlib import Path
import json
import hashlib
import random
import time


FINDING_URL = "https://svcs.ebay.com/services/search/FindingService/v1"

# Ultra-safe: only ONE request at a time
RATE_LIMIT = asyncio.Semaphore(1)

# Max retries per request
MAX_RETRIES = 5

# Global cooldown between ANY requests (ultra-safe)
GLOBAL_COOLDOWN_SECONDS = 12  # 10–15 seconds is ideal


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


CACHE_DIR = project_root() / "cache" / "finding"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_key(params: Dict) -> Path:
    key = json.dumps(params, sort_keys=True)
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{h}.xml"


class EbayFindingClientRaw:
    """
    Ultra-safe Finding API client.
    - Absolute paths
    - Aggressive caching
    - Global cooldowns
    - RateLimiter detection
    - Long backoff
    - Debug visibility
    """

    def __init__(self, app_id: str):
        self.app_id = app_id
        self._last_request_time = 0

    async def _global_cooldown(self):
        """
        Ensures at least GLOBAL_COOLDOWN_SECONDS between ANY requests.
        """
        now = time.time()
        elapsed = now - self._last_request_time

        if elapsed < GLOBAL_COOLDOWN_SECONDS:
            wait = GLOBAL_COOLDOWN_SECONDS - elapsed + random.uniform(0.5, 1.5)
            print(f"[GLOBAL COOLDOWN] Sleeping {wait:.1f}s...")
            await asyncio.sleep(wait)

        self._last_request_time = time.time()

    async def _request(self, session: aiohttp.ClientSession, params: Dict) -> str:
        cache_path = _cache_key(params)

        # Serve from cache
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8")

        headers = {"User-Agent": "Mozilla/5.0"}

        for attempt in range(MAX_RETRIES):

            # Enforce global cooldown
            await self._global_cooldown()

            async with RATE_LIMIT:
                async with session.get(FINDING_URL, params=params, headers=headers) as resp:
                    text = await resp.text()

                    print("\n========== FINDING API REQUEST ==========")
                    print("DEBUG APP_ID:", repr(self.app_id))
                    print("DEBUG PARAMS:", json.dumps(params, indent=2))
                    print("DEBUG STATUS:", resp.status)
                    print("DEBUG RESPONSE (first 300 chars):")
                    print(text[:300])
                    print("=========================================\n")

                    # RateLimiter (500 with specific XML)
                    if resp.status == 500 and "RateLimiter" in text:
                        cooldown = 15 + random.uniform(3, 6)
                        print(f"[RATE LIMIT] Cooling down for {cooldown:.1f}s...")
                        await asyncio.sleep(cooldown)
                        continue

                    # Retry on server errors
                    if resp.status >= 500:
                        cooldown = 8 + random.uniform(1, 3)
                        print(f"[SERVER ERROR] Retrying in {cooldown:.1f}s...")
                        await asyncio.sleep(cooldown)
                        continue

                    # Retry on 429
                    if resp.status == 429:
                        cooldown = 10 + random.uniform(2, 4)
                        print(f"[429 RATE LIMIT] Retrying in {cooldown:.1f}s...")
                        await asyncio.sleep(cooldown)
                        continue

                    # Hard fail
                    if resp.status >= 400:
                        raise RuntimeError(f"Finding API error {resp.status}: {text}")

                    # Success → cache
                    cache_path.write_text(text, encoding="utf-8")
                    return text

        raise RuntimeError("Exceeded retry attempts for Finding API")

    def _parse_xml(self, xml_text: str) -> List[Dict]:
        root = ET.fromstring(xml_text)
        ns = {"ns": "http://www.ebay.com/marketplace/search/v1/services"}

        ack = root.find(".//ns:ack", ns)
        if ack is not None and ack.text != "Success":
            return []

        items: List[Dict] = []

        for item in root.findall(".//ns:item", ns):
            raw: Dict = {}

            for child in item:
                tag = child.tag.split("}")[-1]

                if list(child):
                    child_dict: Dict = {}
                    for sub in child:
                        sub_tag = sub.tag.split("}")[-1]

                        if list(sub):
                            sub_dict = {
                                s2.tag.split("}")[-1]: s2.text
                                for s2 in sub
                            }
                            child_dict[sub_tag] = sub_dict
                        else:
                            child_dict[sub_tag] = sub.text

                    raw[tag] = child_dict
                else:
                    raw[tag] = child.text

            items.append(raw)

        return items

    async def fetch(
        self,
        query: str,
        category_id: Optional[str] = None,
        limit: int = 100,
        max_pages: int = 1,
        sold_only: bool = True,
    ) -> List[Dict]:

        results: List[Dict] = []

        async with aiohttp.ClientSession() as session:
            for page in range(1, max_pages + 1):

                params: Dict[str, str] = {
                    "OPERATION-NAME": "findCompletedItems",
                    "SERVICE-VERSION": "1.13.0",
                    "SECURITY-APPNAME": self.app_id,
                    "RESPONSE-DATA-FORMAT": "XML",
                    "REST-PAYLOAD": "true",
                    "keywords": query,
                    "paginationInput.entriesPerPage": str(limit),
                    "paginationInput.pageNumber": str(page),
                }

                if category_id:
                    params["categoryId"] = category_id

                if sold_only:
                    params["itemFilter(0).name"] = "SoldItemsOnly"
                    params["itemFilter(0).value"] = "true"

                xml_text = await self._request(session, params)
                items = self._parse_xml(xml_text)

                if not items:
                    break

                results.extend(items)

                # Ultra-safe: cooldown between pages
                await asyncio.sleep(5 + random.uniform(1, 3))

        return results
