import unittest
from unittest.mock import patch, MagicMock
from stock_price_server import get_stock_price, compare_stocks, get_stock_history


class TestStockPriceServer(unittest.TestCase):

    @patch("stock_price_server.yf.Ticker")
    def test_get_stock_price_success(self, mock_ticker):
        # Set up mock to simulate successful price retrieval
        mock_ticker_instance = MagicMock()
        mock_data = MagicMock()
        mock_data.empty = False
        mock_data.__getitem__.return_value.iloc.__getitem__.return_value = 150.25
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance

        # Test the function
        price = get_stock_price("AAPL")
        self.assertEqual(price, 150.25)

    @patch("stock_price_server.yf.Ticker")
    def test_get_stock_price_empty_data(self, mock_ticker):
        # Set up mock to simulate empty data with fallback
        mock_ticker_instance = MagicMock()
        mock_data = MagicMock()
        mock_data.empty = True
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker_instance.info = {"regularMarketPrice": 151.50}
        mock_ticker.return_value = mock_ticker_instance

        # Test the function
        price = get_stock_price("AAPL")
        self.assertEqual(price, 151.50)

    @patch("stock_price_server.get_stock_price")
    def test_compare_stocks(self, mock_get_stock_price):
        # Set up return values for the two calls to get_stock_price
        mock_get_stock_price.side_effect = [150.25, 200.50]

        # Test comparison
        result = compare_stocks("AAPL", "GOOG")
        self.assertIn("AAPL ($150.25) is lower than GOOG ($200.50)", result)

    @patch("stock_price_server.yf.Ticker")
    def test_get_stock_history(self, mock_ticker):
        # Set up mock for historical data
        mock_ticker_instance = MagicMock()
        mock_data = MagicMock()
        mock_data.empty = False
        mock_data.to_csv.return_value = "Date,Open,High,Low,Close,Volume\n2023-04-16,150.25,152.30,149.80,151.20,12345678"
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance

        # Test the function
        csv_data = get_stock_history("AAPL")
        self.assertIn("Date,Open,High,Low,Close,Volume", csv_data)
        self.assertIn("151.20", csv_data)


if __name__ == "__main__":
    unittest.main()
