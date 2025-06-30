import httpx


class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org"
    COVERS_URL = "https://covers.openlibrary.org"

    async def search_book(self, title: str) -> dict | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.BASE_URL}/search.json", params={"q": title})
            if resp.status_code == 200:
                data = resp.json()
                for doc in data.get("docs", []):
                    if doc.get("title", "").lower() == title.lower():
                        return doc

    async def get_description(self, olid: str) -> dict | None:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"{self.BASE_URL}/{olid}.json")
            response.raise_for_status()
            return response.json()

    def get_cover_url(self, cover_id: int, size: str = "L") -> str:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
