from unittest import mock

from app.application.orders_service import OrdersService


class TestOrdersService:
    @mock.patch(
        "infrastructure.retailcrm_client.RetailCRMClient.get",
        new_callable=mock.AsyncMock,
    )
    async def test_it_calls_client_on_get_orders(self, mock_get):
        mock_get.return_value = {"orders": []}

        client = mock.Mock()
        client.get = mock_get

        service = OrdersService(client)

        await service.get_orders_by_customer({"customerId": 10})

        mock_get.assert_called_once()

    @mock.patch(
        "infrastructure.retailcrm_client.RetailCRMClient.post",
        new_callable=mock.AsyncMock,
    )
    async def test_it_calls_client_on_create_order(self, mock_post):
        mock_post.return_value = {"id": 99, "success": True, "order": {"id": 99}}

        client = mock.Mock()
        client.post = mock_post

        service = OrdersService(client)

        data = {
            "customer": {"id": 10},
            "items": [{"comment": "Test", "quantity": 1, "initialPrice": 10}],
            "number": "A-001",
        }

        await service.create_order(data)

        mock_post.assert_called_once()

    @mock.patch(
        "infrastructure.retailcrm_client.RetailCRMClient.post",
        new_callable=mock.AsyncMock,
    )
    async def test_it_calls_client_on_create_payment(self, mock_post):
        mock_post.return_value = {"id": 500, "success": True}

        client = mock.Mock()
        client.post = mock_post

        service = OrdersService(client)

        payload = {"order": {"id": 99}, "amount": 200}

        await service.create_payment(payload)

        mock_post.assert_called_once()
