import json
from typing import Any
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from application.base import RetailCRMBaseService


class CustomersService(RetailCRMBaseService):
    CUSTOMERS_PATH = 'customers'
    CUSTOMER_ADD_PATH = 'customers/create'

    async def get_customers(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        try:
            resp = await self.client.get(path=await self.set_filters(self.CUSTOMERS_PATH, filters))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())
        result = []
        for c in resp.get("customers", []):
            phones = [{'number': p.get("number")} for p in c.get("phones", [])] if c.get("phones") else None
            result.append({
                'internal_id': c.get("id"),
                'site': c.get("site"),
                'first_name': c.get("firstName") or c.get("name") or "",
                'last_name': c.get("lastName"),
                'patronymic': c.get("patronymic"),
                'email': c.get("email"),
                'phones': phones,
            })
        return result

    async def create_customer(self, data: dict[str, Any]):
        site = data.pop('site', None)
        customer_data = await self.param_encode('customer', data)
        site_data = await self.param_encode(None, {'site': site})
        form_data = await self.join_form_parts(site_data, customer_data)
        try:
            resp = await self.client.post(self.CUSTOMER_ADD_PATH, data=form_data)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())
        return {'internal_id': resp['id'], 'success': resp['success']}
