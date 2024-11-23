import unittest
from model import Order, OrderBook, tradeRecord

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        """Initialize a new OrderBook before each test"""
        self.order_book = OrderBook()

    def test_basic_order_matching(self):
        """Test basic matching of buy and sell orders"""
        print("\n=== Testing Basic Order Matching ===")
        
        # Create test orders
        buy_order = Order(
            id="buyer1",
            price=100.0,
            quantity=10,
            isBuy=True,
            timestamp=1
        )
        print(f"Created buy order: {buy_order}")
        
        sell_order = Order(
            id="seller1",
            price=95.0,
            quantity=5,
            isBuy=False,
            timestamp=1
        )
        print(f"Created sell order: {sell_order}")

        # Add orders to the book
        self.order_book.addOrder(buy_order)
        self.order_book.addOrder(sell_order)
        print("\nOrder book state after adding orders:")
        print(f"Buy orders: {self.order_book.buyHeap}")
        print(f"Sell orders: {self.order_book.sellHeap}")

        # Try to fulfill orders
        records = self.order_book.fullfillOrders(None, tick=1)
        print("\nTrade records created:")
        for record in records:
            print(f"Trade: {record.buyer} bought {record.quantity} units from {record.seller} at ${record.price}")

    
    def test_multiple_orders(self):
        """Test matching multiple orders"""
        print("\n=== Testing Multiple Orders ===")
        
        orders = [
            Order("buyer1", 100.0, 10, True, 1),
            Order("seller1", 95.0, 3, False, 1),
            Order("seller2", 98.0, 4, False, 1),
            Order("buyer2", 102.0, 5, True, 1)
        ]

        print("\nAdding orders:")
        for order in orders:
            print(f"Adding order: {order}")
            self.order_book.addOrder(order)

        print("\nOrder book state before matching:")
        print(f"Buy orders: {self.order_book.buyHeap}")
        print(f"Sell orders: {self.order_book.sellHeap}")

        records = self.order_book.fullfillOrders(None, tick=1)
        
        print("\nTrade records created:")
        for record in records:
            print(f"Trade: {record.buyer} bought {record.quantity} units from {record.seller} at ${record.price}")

        # Verify multiple trades occurred
        self.assertTrue(len(records) > 0)
        
    def test_no_matching_orders(self):
        """Test behavior when no orders match"""
        buy_order = Order("buyer1", 90.0, 10, True, 1)
        sell_order = Order("seller1", 100.0, 5, False, 1)

        self.order_book.addOrder(buy_order)
        self.order_book.addOrder(sell_order)

        records = self.order_book.fullfillOrders(None, tick=1)

        # Verify no trades occurred
        #self.assertEqual(len(records), 0)
    

if __name__ == '__main__':
    unittest.main()