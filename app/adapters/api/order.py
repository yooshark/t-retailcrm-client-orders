from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter
from schemas.orders import PaymentCreate, OrderCreate, OrderResponse, PaymentCreatedResponse, \
    OrderCreatedResponse
from application.orders_service import OrdersService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/by-customer/{customer_id}", response_model=list[OrderResponse])
@inject
async def get_orders(customer_id:int, service: Injected[OrdersService]):
    return await service.get_orders_by_customer({'customerId': customer_id})



@router.post("/", response_model=OrderCreatedResponse)
@inject
async def create_order(data: OrderCreate, service: Injected[OrdersService]):
    return await service.create_order(data.model_dump(by_alias=True))


@router.post("/payments", response_model=PaymentCreatedResponse)
@inject
async def create_payment(data: PaymentCreate, service: Injected[OrdersService]):
    return await service.create_payment(data.model_dump(exclude_none=True, by_alias=True))
