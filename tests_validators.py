import unittest
from unittest.mock import MagicMock, patch
from bot.validators import validate_input

class TestValidators(unittest.TestCase):
    def test_valid_input_market(self):
        self.assertTrue(validate_input("BTCUSDT", "BUY", "MARKET", 0.001))

    def test_valid_input_limit(self):
        self.assertTrue(validate_input("BTCUSDT", "SELL", "LIMIT", 0.001, 60000))

    def test_invalid_side(self):
        with self.assertRaises(ValueError):
            validate_input("BTCUSDT", "HOLD", "MARKET", 0.001)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            validate_input("BTCUSDT", "BUY", "MARKET", "not-a-number")
        with self.assertRaises(ValueError):
            validate_input("BTCUSDT", "BUY", "MARKET", -1)

    def test_missing_price_for_limit(self):
        with self.assertRaises(ValueError):
            validate_input("BTCUSDT", "BUY", "LIMIT", 0.001)

if __name__ == "__main__":
    unittest.main()
