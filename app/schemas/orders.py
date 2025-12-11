from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Annotated

from schemas.base import ValidatedCamelCaseSchema, CamelCaseSchema


class OrderId(BaseModel):
    id: int


class OrderProductIn(ValidatedCamelCaseSchema):
    comment: str
    quantity: int
    initial_price: Annotated[Decimal, Field(ge=0, lt=10000000, decimal_places=3)]


class OrderCustomerInfo(CamelCaseSchema):
    id: int


class OrderCreate(ValidatedCamelCaseSchema):
    customer: OrderCustomerInfo
    items: list[OrderProductIn]
    number: str

class OrderCreatedResponse(BaseModel):
    id: int
    success: bool
    order: OrderId

class OrderResponse(OrderCreate, OrderId):
    pass


class PaymentCreate(ValidatedCamelCaseSchema):
    order: OrderId
    amount: Annotated[Decimal, Field(ge=0, lt=10000000, decimal_places=3)]
    type: str = "cash"
    comment: str | None = None


class PaymentCreatedResponse(BaseModel):
    id: int
    success: bool
