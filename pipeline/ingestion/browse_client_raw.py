# ingestion_raw/browse_client_raw.py

import aiohttp
import asyncio
import json
from typing import List, Dict, Optional


EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# ------------------------------------------------------------
# GLOBAL RATE LIMITER
# ------------------------------------------------------------
RATE_LIMIT = asyncio.Semaphore(3)
MAX_RETRIES = 5


class EbayBrowseClientRaw:
    """
    RAW Browse API client.
    - No normalization
    - No domain defaults
    - No LEGO-specific logic
    - Returns untouched Browse API items
    - Handles pagination, concurrency, and retry/backoff
    """

    def __init__(self, token: str):
        self.token = token

    # ------------------------------------------------------------
    # Internal request with retry/backoff
    # ------------------------------------------------------------
    async def _request(self, session, params):
        for attempt in range(MAX_RETRIES):
            async with RATE_LIMIT:
                async with session.get(
                    EBAY_API_URL,
                    params=params,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
                    },
                ) as resp:

                    text = await resp.text()

                    # Throttled → retry with backoff
                    if resp.status == 429:
                        await asyncio.sleep(2 ** attempt)
                        continue

                    # Other errors
                    if resp.status >= 400:
                        raise RuntimeError(f"eBay API error {resp.status}: {text}")

                    return json.loads(text)

        raise RuntimeError("Exceeded retry attempts due to repeated 429 throttling")

    # ------------------------------------------------------------
    # Public fetch method (pagination only, returns raw items)
    # ------------------------------------------------------------
    async def fetch(
        self,
        query: Optional[str] = "",
        filters: Optional[str] = "",
        category_id: Optional[str] = "",
        limit: int = 200,
        max_pages: int = 1,
        offset: int = 0,
    ) -> List[Dict]:

        results: List[Dict] = []

        async with aiohttp.ClientSession() as session:
            current_offset = offset

            for _ in range(max_pages):
                params = {
                    "q": query or "",
                    "filter": filters or "",
                    "limit": str(limit),
                    "offset": str(current_offset),
                    "category_ids": category_id or "",
                }

                data = await self._request(session, params)
                items = data.get("itemSummaries", [])

                if not items:
                    break

                # Append raw items exactly as returned by eBay
                results.extend(items)

                current_offset += limit

        return results
