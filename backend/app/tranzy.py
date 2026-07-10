import httpx

from .config import settings


class TranzyClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.tranzy_base_url,
            headers={
                "X-API-KEY": settings.tranzy_api_key,
                "X-Agency-Id": str(settings.tranzy_agency_id),
                "Accept": "application/json",
            },
            timeout=15.0,
        )

    async def get_vehicles(self) -> list[dict]:
        resp = await self._client.get("/vehicles")
        resp.raise_for_status()
        return resp.json()

    async def get_routes(self) -> list[dict]:
        resp = await self._client.get("/routes")
        resp.raise_for_status()
        return resp.json()

    async def aclose(self) -> None:
        await self._client.aclose()

    def __repr__(self):
        return f"TranzyClient()"

    def __str__(self):
        return "Tranzy client used for HTTP request to OpenData API"