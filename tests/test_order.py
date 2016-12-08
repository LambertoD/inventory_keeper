import unittest
from product_orders import ProductOrder


class Order(unittest.TestCase):

    # def test_create_product_order_with_class_method(self):
    #     header = "1"
    #     order_lines = [('A', 1), ('B', 1), ('C', 1), ('D', 1)]
    #     order = ProductOrder.create_with_items(header, order_lines)

    def test_create_product_order(self):
        header = "2"
        order_lines = 'A:1,B:2,C:3,D:4,E:5'
        order = ProductOrder(header, order_lines)
        # expected_order = {
        #     'Header': '1',
        #     'Lines': [
        #         {'A': '1'},
        #         {'B': '2'},
        #         {'C': '3'},
        #         {'D': '4'},
        #         {'E': '5'}
        #     ]
        # }
        self.assertEqual('2', order.get_id())
        self.assertEqual(5, len(order.order_details()))
        self.assertIn({'A': 1}, order.order_details())
        self.assertIn({'B': 2}, order.order_details())
        self.assertIn({'C': 3}, order.order_details())
        self.assertIn({'D': 4}, order.order_details())
        self.assertIn({'E': 5}, order.order_details())

    def test_create_product_with_qty_greater_than_5(self):
        header = "3"
        order_lines = 'A:6'
        with self.assertRaises(ValueError):
            ProductOrder(header, order_lines)

    def test_create_product_with_qty_less_than_1(self):
        header = "3"
        order_lines = 'A:1,B:0'
        with self.assertRaises(ValueError):
            ProductOrder(header, order_lines)
