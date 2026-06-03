import aiohttp
from typing import List, Dict

EBAY_BROWSE_BASE = "https://api.ebay.com/buy/browse/v1/item_summary/search"

class EbaySoldClient:
    def __init__(self, token: str):
        self.token = token

    async def fetch_sold(self, query: str, limit: int = 50, max_pages: int = 1) -> List[Dict]:
        """
        Fetch sold/ended items via Browse API using filters.
        NOTE: This uses 'filter=buyingOptions:{AUCTION}|{FIXED_PRICE}' and 'item_filters' style
        depending on how your app is set up. Adjust to your actual sold endpoint/filters.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        items: List[Dict] = []
        offset = 0

        async with aiohttp.ClientSession(headers=headers) as session:
            for _ in range(max_pages):
                params = {
                    "q": query,
                    "limit": str(limit),
                    "offset": str(offset),
                    # You may need to adjust this to your real sold/completed filter
                    "filter": "itemEndDate:[..NOW]"
                }
                async with session.get(EBAY_BROWSE_BASE, params=params) as resp:
                    data = await resp.json()
                    batch = data.get("itemSummaries", [])
                    if not batch:
                        break
                    items.extend(batch)
                    offset += len(batch)

        return items
