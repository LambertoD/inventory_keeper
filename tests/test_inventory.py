import unittest
from inventory import Inventory


class InventoryTest(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        # self.order = Order()

    def tearDown(self):
        pass

    def test_create_inventory(self):
        for char in "ABCDE":
            self.inventory.add(char, 100)
        for char in "ABCDE":
            self.assertEqual(100, self.inventory.lookup(char))

    def test_lookup_inventory_by_product(self):
        self.inventory.add("A", 5)
        self.assertEqual(5, self.inventory.lookup("A"))

    def test_invalid_product_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.inventory.lookup("Z")

    def test_reduce_inventory_for_a_satisfiable_order(self):
        self.inventory.add("A", 5)
        orders_fulfilled = self.inventory.fulfill_order("A", 1)
        self.assertEqual(1, orders_fulfilled)
        self.assertEqual(4, self.inventory.lookup("A"))

    def test_reduce_inventory_to_zero(self):
        self.inventory.add("A", 5)
        orders_fulfilled = self.inventory.fulfill_order("A", 5)
        self.assertEqual(5, orders_fulfilled)
        self.assertEqual(0, self.inventory.lookup("A"))

    def test_back_order_inventory_with_0_qty(self):
        self.inventory.add("A", 0)
        orders_fulfilled = self.inventory.fulfill_order("A", 5)
        self.assertEqual(0, orders_fulfilled)
        self.assertEqual(5, self.inventory.lookup_back_order("A"))

    def test_back_order_for_product_with_good_inventory(self):
        self.inventory.add("A", 0)
        self.assertEqual(0, self.inventory.lookup_back_order("B"))
        self.assertFalse(self.inventory.has_back_order("B"))

    def test_back_orders_for_multiple_orders_exhausting_product(self):
        self.inventory.add("A", 5)
        order1 = self.inventory.fulfill_order("A", 5)
        self.assertEqual(5, order1)
        self.assertEqual(0, self.inventory.lookup_back_order("A"))
        order2 = self.inventory.fulfill_order("A", 1)
        self.assertEqual(0, order2)
        self.assertEqual(1, self.inventory.lookup_back_order("A"))
        order3 = self.inventory.fulfill_order("A", 5)
        self.assertEqual(0, order3)
        self.assertEqual(6, self.inventory.lookup_back_order("A"))
        order4 = self.inventory.fulfill_order("A", 1)
        self.assertEqual(0, order4)
        self.assertEqual(7, self.inventory.lookup_back_order("A"))

    def test_back_order_status(self):
        self.inventory.add("A", 3)
        order1 = self.inventory.fulfill_order("A", 2)
        self.assertEqual(2, order1)
        self.assertFalse(self.inventory.has_back_order("A"))
        order2 = self.inventory.fulfill_order("A", 2)
        self.assertEqual(1, order2)
        self.assertTrue(self.inventory.has_back_order("A"))

    def test_reduce_inventory_for_a_partial_satisfy_order(self):
        self.inventory.add("A", 3)
        orders_fulfilled = self.inventory.fulfill_order("A", 5)
        self.assertEqual(3, orders_fulfilled)
        self.assertEqual(0, self.inventory.lookup("A"))
        self.assertEqual(2, self.inventory.lookup_back_order("A"))
