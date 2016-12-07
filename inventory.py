class Inventory(object):

    def __init__(self):
        self.entries = {}

    def add(self, name, quantity):
        self.entries[name] = quantity

    def lookup(self, name):
        return self.entries[name]

    def fulfill_order(self, name, quantity):
        if self.entries[name] == 0:
            pass
            # create back order
        elif self.entries[name] >= quantity:
            self.entries[name] -= quantity
        else:
            # fulfill partial
            self.entries[name] = 0
            back_order = abs(self.entries[name] - quantity)
