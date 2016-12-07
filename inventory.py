class Inventory(object):
    """This class maintains an inventory of products with quantities

    """

    def __init__(self):
        self.entries = {}
        self.back_order = {}

    def add(self, name, quantity):
        self.entries[name] = quantity

    def lookup(self, name):
        return self.entries[name]

    def fulfill_order(self, name, quantity):
        if self.entries[name] == 0:
            self.back_order[name] = quantity
            # create back order
        elif self.entries[name] >= quantity:
            self.entries[name] -= quantity
        else:
            # fulfill partial
            self.back_order[name] = abs(self.entries[name] - quantity)
            self.entries[name] = 0

    def lookup_back_order(self, name):
        return self.back_order[name]
