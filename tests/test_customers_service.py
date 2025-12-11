from unittest import mock

from app.application.customers_service import CustomersService


class TestCustomersService:
    @mock.patch(
        "infrastructure.retailcrm_client.RetailCRMClient.get",
        new_callable=mock.AsyncMock,
    )
    async def test_it_calls_client_on_get_customers(self, mock_get):
        mock_get.return_value = {"customers": []}

        client = mock.Mock()
        client.get = mock_get

        service = CustomersService(client)

        await service.get_customers({"name": "John"})

        mock_get.assert_called_once()

    @mock.patch(
        "infrastructure.retailcrm_client.RetailCRMClient.post",
        new_callable=mock.AsyncMock,
    )
    async def test_it_calls_client_on_create_customer(self, mock_post):
        mock_post.return_value = {"id": 1, "success": True}

        client = mock.Mock()
        client.post = mock_post

        service = CustomersService(client)

        payload = {"firstName": "Alice", "site": "main"}

        await service.create_customer(payload)

        mock_post.assert_called_once()
