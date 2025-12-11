from fastapi import APIRouter
from adapters.api.customers import router as customers_router
from adapters.api.order import router as orders_router

api_router = APIRouter(prefix='/api')
api_router.include_router(customers_router)
api_router.include_router(orders_router)
