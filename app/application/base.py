import json
from decimal import Decimal
from typing import Any

from infrastructure.retailcrm_client import RetailCRMClient
from urllib.parse import urlencode

from multidimensional_urlencode import urlencode as query_builder


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


class RetailCRMBaseService:
    def __init__(self, client: RetailCRMClient):
        self.client = client

    @staticmethod
    async def join_form_parts(*args) -> str:
        return "&".join([*args])

    @staticmethod
    async def param_encode(key: str | None, dictionary: dict[str, Any]) -> str:
        if key is None:
            return urlencode(dictionary)
        return urlencode({key: json.dumps(dictionary, cls=DecimalEncoder)})

    @staticmethod
    async def set_filters(path: str, filters: dict[str, Any]) -> str:
        if not filters:
            return path

        filter_params = {
            "limit": filters.pop("limit", 20),
            "page": filters.pop("page", 1),
        }
        filter_params |= {f"filter[{k}]": v for k, v in filters.items()}
        return f"{path}?{query_builder(filter_params)}"

    async def build_form_data(self, **kwargs: dict[str, Any]) -> str:
        parts = []
        for k, v in kwargs.items():
            if isinstance(v, dict):
                encoded = await self.param_encode(k, v)
            else:
                encoded = await self.param_encode(None, {k: v})
            parts.append(encoded)
        return await self.join_form_parts(*parts)
