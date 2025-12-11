from typing import Any

import httpx
from core.settings import RetailCRMSettings


class RetailCRMClient:

    def __init__(self, cfg: RetailCRMSettings):
        self.base_url = cfg.base_url
        self.api_key = cfg.API_KEY
        self.version = cfg.API_VERSION
        self._timeout = cfg.HTTP_TIMEOUT
        self.base_api = f'{self.base_url.rstrip('/')}/api/v{str(self.version)}'
        self.headers = {"X-API-KEY": self.api_key}


    async def _request(self, method: str, path: str, data: str | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout, headers=self.headers) as client:
            r = await client.request(method, f'{self.base_api}/{path}', data=data)
            r.raise_for_status()
            return r.json()

    async def get(self, path: str) -> dict[str, Any]:
        return await self._request("GET", path)

    async def post(self, path: str, data: str | None = None) -> dict[str, Any]:
        print(data)
        self.headers = self.headers | {"Content-Type": "application/x-www-form-urlencoded"}
        return await self._request("POST", path, data=data)
