class Inventory(object):
    """This class maintains an inventory of products with quantities

    It maintains state for a product inventory and a back-order inventory.

    """

    def __init__(self):
        self.entries = {}
        self.back_order = {}
        self.back_order_status = {}

    def add(self, name, quantity):
        self.entries[name] = quantity

    def lookup(self, name):
        return self.entries[name]

    def fulfill_order(self, name, quantity):
        if self.entries[name] == 0:
            # create back order
            self.back_order_status[name] = True
            if name in self.back_order:
                self.back_order[name] += quantity
            else:
                self.back_order[name] = quantity
            return 0
        elif self.entries[name] >= quantity:
            self.entries[name] -= quantity
            return quantity
        else:
            # fulfill partial
            self.back_order_status[name] = True
            self.back_order[name] = abs(self.entries[name] - quantity)
            fulfilled_order = self.entries[name]
            self.entries[name] = 0
            return fulfilled_order

    def lookup_back_order(self, name):
        if name in self.back_order:
            return self.back_order[name]
        else:
            return 0

    def has_back_order(self, name):
        if name in self.back_order_status:
            return self.back_order_status[name]
        return False
