from aioinject import Injected

from application.customers_service import CustomersService
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends
from schemas.customers import CustomerFilter, CustomerResponse, CustomerCreate, CustomerCreatedResponse

router = APIRouter(
    prefix='/customers',
    tags=['Customers'],
)


@router.get('/', response_model=list[CustomerResponse])
@inject
async def get_customers(service: Injected[CustomersService], filters: CustomerFilter = Depends()):
    return await service.get_customers(filters.model_dump(exclude_none=True, by_alias=True))


@router.post('/', response_model=CustomerCreatedResponse)
@inject
async def create_customer(data: CustomerCreate, service: Injected[CustomersService]):
    return await service.create_customer(data.model_dump(exclude_none=True, by_alias=True))
