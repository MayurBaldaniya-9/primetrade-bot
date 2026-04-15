import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger
from dotenv import load_dotenv

load_dotenv()

class BinanceClientWrapper:
    def __init__(self, api_key=None, api_secret=None):
        """
        Initialize the Binance Client with Testnet credentials
        """
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_SECRET_KEY')
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key or API Secret is missing. Ensure BINANCE_API_KEY and BINANCE_SECRET_KEY are set in the .env file.")
            raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be set")

        try:
            # Sync server time once
            # We must use a direct request to avoid signing errors during initialization
            import requests
            import time
            resp = requests.get('https://testnet.binance.vision/api/v3/time')
            server_time = resp.json()['serverTime']
            local_time = int(time.time() * 1000)
            
            # Standard setup
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            self.client.timestamp_offset = server_time - local_time
            
            # Use specific Testnet URLs to be safe
            self.client.API_URL = 'https://testnet.binance.vision/api'
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi/v1'
            
            # Crucial: Enable automatic time sync
            self.client.REQUEST_PARAMS = {'timeout': 10}
            
            logger.info(f"Successfully initialized Binance Client (Testnet). Time Offset: {self.client.timestamp_offset}ms")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {str(e)}")
            raise

    def place_futures_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place a futures order on USDT-M Testnet
        """
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }
            
            if order_type.upper() == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Till Cancelled is standard for Limit
            
            logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}...")
            
            # Use USDT-M Futures endpoint
            response = self.client.futures_create_order(**params)
            
            logger.debug(f"Order Response: {response}")
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise

    def place_spot_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place a spot order on Testnet
        """
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }
            
            if order_type.upper() == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                params['price'] = price
                params['timeInForce'] = 'GTC'
            
            logger.info(f"Placing SPOT {order_type} {side} order for {quantity} {symbol}...")
            
            # Use Spot endpoint
            response = self.client.create_order(**params)
            
            logger.debug(f"Spot Order Response: {response}")
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise
