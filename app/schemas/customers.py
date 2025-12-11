from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from schemas.base import FormattedDatetime, CamelCaseSchema, ValidatedCamelCaseSchema


class CustomerId(BaseModel):
    internal_id: int


class CustomerPhone(BaseModel):
    number: str | None = None


class CustomerFilter(CamelCaseSchema):
    name: str | None = None
    email: EmailStr | None = None
    date_from: FormattedDatetime | None = None
    date_to: FormattedDatetime | None = None

    limit: Annotated[
        int,
        Field(
            default=20,
            description="Количество элементов (20/50/100)",
            ge=1,
            json_schema_extra={"enum": [20, 50, 100]},
        ),
    ]

    page: Annotated[
        int,
        Field(
            default=1,
            description="Номер страницы (>=1)",
            ge=1,
        ),
    ]


class CustomerBase(BaseModel):
    first_name: str
    last_name: str | None = None
    patronymic: str | None = None
    email: EmailStr | None = None
    phones: list[CustomerPhone] | None = None
    subscribed: Annotated[
        bool,
        Field(
            default=False,
            description="Статус подписки на маркетинговые рассылки писем",
        ),
    ]
    site: Annotated[
        str,
        Field(
            description="Символьный код магазина",
        ),
    ]


class CustomerResponse(CustomerId, CustomerBase):
    pass


class CustomerCreate(CustomerBase, ValidatedCamelCaseSchema):
    pass


class CustomerCreatedResponse(CustomerId):
    success: bool
