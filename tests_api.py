import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.place_order")
    def test_place_order_success(self, mock_place_order):
        mock_place_order.return_value = {
            "orderId": 123,
            "status": "FILLED",
            "symbol": "BTCUSDT",
            "type": "MARKET",
            "side": "BUY",
            "origQty": "0.001",
            "executedQty": "0.001",
            "avgPrice": "62000",
        }

        response = self.client.post(
            "/api/orders",
            json={
                "market": "FUTURES",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
                "quantity": 0.001,
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["orderId"], 123)

    def test_place_order_validation_error(self):
        response = self.client.post(
            "/api/orders",
            json={
                "market": "FUTURES",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "LIMIT",
                "quantity": 0.001,
            },
        )

        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertEqual(body["error"]["message"], "Order validation failed")

    def test_place_order_payload_error(self):
        response = self.client.post(
            "/api/orders",
            json={
                "market": "FUTURES",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
            },
        )

        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertEqual(body["error"]["message"], "Invalid request payload")


if __name__ == "__main__":
    unittest.main()
