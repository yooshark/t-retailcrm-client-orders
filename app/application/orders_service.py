from typing import Any

import httpx
from fastapi import HTTPException

from application.base import RetailCRMBaseService


class OrdersService(RetailCRMBaseService):
    ORDERS_PATH = "orders"
    ORDERS_ADD_PATH = "orders/create"
    ORDERS_LINK_PAYMENT_PATH = "orders/payments/create"

    async def get_orders_by_customer(
        self, filters: dict[str, int]
    ) -> list[dict[str, Any]]:
        try:
            resp = await self.client.get(
                path=await self.set_filters(self.ORDERS_PATH, filters)
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())
        result = []
        for o in resp.get("orders", []):
            items = []
            for it in o.get("items", []):
                items.append(
                    {
                        "comment": it.get("comment"),
                        "quantity": it.get("quantity", 1),
                        "initial_price": it.get("initialPrice", 0.0),
                    }
                )
            result.append(
                {
                    "id": o.get("id"),
                    "number": o.get("number") or "",
                    "customer": {"id": o.get("customer", {})["id"]},
                    "items": items,
                    "site": o.get("site"),
                }
            )
        return result

    async def create_order(self, data: dict[str, Any]) -> dict[str, Any]:
        site = data.pop("site", None)
        form_data = await self.build_form_data(**{"site": site}, **{"order": data})
        try:
            resp = await self.client.post(self.ORDERS_ADD_PATH, data=form_data)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())

        return {
            "id": resp["id"],
            "success": resp["success"],
            "order": {"id": resp.get("order", {}).get("id")},
        }

    async def create_payment(self, data: dict) -> dict[str, int | bool]:
        site = data.pop("site", None)
        form_data = await self.build_form_data(**{"site": site}, **{"payment": data})
        try:
            resp = await self.client.post(self.ORDERS_LINK_PAYMENT_PATH, data=form_data)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())
        return {"id": resp["id"], "success": resp["success"]}
