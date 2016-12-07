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
        self.inventory.fulfill_order("A", 1)
        self.assertEqual(4, self.inventory.lookup("A"))

    def test_reduce_inventory_for_a_partial_satisfy_order(self):
        self.inventory.add("A", 5)
        self.inventory.fulfill_order("A", 6)
        self.assertEqual(0, self.inventory.lookup("A"))

    def test_reduce_inventory_to_zero(self):
        self.inventory.add("A", 5)
        self.inventory.fulfill_order("A", 5)
        self.assertEqual(0, self.inventory.lookup("A"))