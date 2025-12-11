import aioinject
from aioinject.ext.fastapi import FastAPIExtension

from application.customers_service import CustomersService
from application.orders_service import OrdersService
from core import settings
from core.server import new_server
from infrastructure.retailcrm_client import RetailCRMClient


def new_container() -> aioinject.Container:
    container = aioinject.Container(extensions=[FastAPIExtension()])
    container.register(
        aioinject.Singleton(settings.AppSettings.new),
        aioinject.Singleton(settings.RetailCRMSettings.new),
        aioinject.Singleton(RetailCRMClient),
        aioinject.Singleton(CustomersService),
        aioinject.Singleton(OrdersService),
        aioinject.Singleton(new_server),
    )

    return container


container: aioinject.Container = new_container()
