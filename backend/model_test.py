import unittest
from model import Order, OrderBook, tradeRecord, GameOrderBook

class TestGameOrderBook(unittest.TestCase):
    def setUp(self):
        """Initialize GameOrderBook with test securities"""
        self.securities = ["AAPL", "GOOGL", "MSFT"]
        self.game_order_book = GameOrderBook(self.securities)
        
    def test_market_maker_initialization(self):
        """Test market maker creation and updates"""
        print("\n=== Testing Market Maker Initialization ===")
        
        security_prices = {
            "AAPL": 100.0,
            "GOOGL": 2800.0,
            "MSFT": 300.0
        }
        
        self.game_order_book.update_market_maker_orders(security_prices, 1)
        
        # Verify market makers exist with correct prices
        for security, price in security_prices.items():
            market_order = self.game_order_book.orderBooks[security].market_order
            self.assertIsNotNone(market_order)
            self.assertEqual(market_order.id, "MARKET_MAKER")
            self.assertEqual(market_order.price, price * 1.05)  # 5% premium

    def test_basic_order_matching(self):
        """Test matching orders across multiple securities"""
        print("\n=== Testing Basic Order Matching ===")
        
        # Initialize market makers
        self.game_order_book.update_market_maker_orders({
            "AAPL": 100.0,
            "GOOGL": 2800.0,
            "MSFT": 300.0
        }, 1)
        
        # Create test orders for different securities
        orders = [
            Order("buyer1", "AAPL", 100.0, 10, True, 1),
            Order("seller1", "AAPL", 95.0, 5, False, 1),
            Order("buyer2", "GOOGL", 2900.0, 3, True, 1),
            Order("seller2", "GOOGL", 2850.0, 2, False, 1)
        ]
        
        # Add all orders
        self.game_order_book.addOrder(orders)
        
        # Try to fulfill orders
        records = self.game_order_book.fullfillOrders(1)
        
        # Verify trades occurred for both securities
        self.assertTrue("AAPL" in records)
        self.assertTrue("GOOGL" in records)
        self.assertTrue(len(records["AAPL"]) > 0)
        self.assertTrue(len(records["GOOGL"]) > 0)

    def test_market_maker_trading(self):
        """Test trading with market makers when no other sellers available"""
        print("\n=== Testing Market Maker Trading ===")
        
        # Setup market makers
        self.game_order_book.update_market_maker_orders({
            "AAPL": 100.0,
            "GOOGL": 2800.0
        }, 1)
        
        # Create buy orders above market maker prices
        orders = [
            Order("buyer1", "AAPL", 110.0, 5, True, 1),  # Above AAPL market maker
            Order("buyer2", "GOOGL", 3000.0, 3, True, 1)  # Above GOOGL market maker
        ]
        
        self.game_order_book.addOrder(orders)
        records = self.game_order_book.fullfillOrders(1)
        
        # Verify trades with market makers
        for security in ["AAPL", "GOOGL"]:
            self.assertTrue(security in records)
            self.assertTrue(len(records[security]) > 0)
            self.assertEqual(records[security][0].seller, "MARKET_MAKER")

    def test_mixed_trading(self):
        """Test mix of regular trading and market maker trading"""
        print("\n=== Testing Mixed Trading Scenarios ===")
        
        # Setup market makers
        self.game_order_book.update_market_maker_orders({
            "AAPL": 100.0,
            "GOOGL": 2800.0
        }, 1)
        
        # Create mix of orders
        orders = [
            # AAPL orders - should match with each other
            Order("seller1", "AAPL", 95.0, 5, False, 1),
            Order("buyer1", "AAPL", 98.0, 5, True, 1),
            
            # GOOGL orders - should match with market maker
            Order("buyer2", "GOOGL", 3000.0, 3, True, 1)
        ]
        
        self.game_order_book.addOrder(orders)
        records = self.game_order_book.fullfillOrders(1)
        
        # Verify AAPL trade between regular orders
        self.assertTrue(len(records["AAPL"]) > 0)
        self.assertEqual(records["AAPL"][0].seller, "seller1")
        self.assertEqual(records["AAPL"][0].buyer, "buyer1")
        
        # Verify GOOGL trade with market maker
        self.assertTrue(len(records["GOOGL"]) > 0)
        self.assertEqual(records["GOOGL"][0].seller, "MARKET_MAKER")

    def test_market_maker_price_updates(self):
        """Test market maker price updates"""
        print("\n=== Testing Market Maker Price Updates ===")
        
        # Initial market maker setup
        initial_prices = {"AAPL": 100.0}
        self.game_order_book.update_market_maker_orders(initial_prices, 1)
        
        # Verify initial price
        initial_mm_price = self.game_order_book.orderBooks["AAPL"].market_order.price
        self.assertEqual(initial_mm_price, 105.0)  # 5% premium
        
        # Update price
        new_prices = {"AAPL": 120.0}
        self.game_order_book.update_market_maker_orders(new_prices, 2)
        
        # Verify price update
        new_mm_price = self.game_order_book.orderBooks["AAPL"].market_order.price
        self.assertEqual(new_mm_price, 126.0)  # 5% premium on new price

if __name__ == '__main__':
    unittest.main()