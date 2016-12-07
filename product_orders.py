class ProductOrder(object):
    """This class creates instances of Orders

        Orders follow the following structure:
            'Header': '1',
            'Lines': [
                {'A': '1'},
                {'B': '2'},
                {'C': '3'},
                {'D': '4'},
                {'E': '5'}
            ]
        }
        Header represents unique identifier for the order.
        Lines represent a list of 1 to 5 units of a product 'A', 'B',
        'C', 'D', or 'E'.
        Each order should have at least a demand for 1 product.
        A demand for a product can be from 1 to 5 units.
        A demand for a product cannot be 0 or greater than 5

        Create an order by providing a string value for the header id and
            providing a string of colon delimited Product:Qty values.
            Example:  ProductOrder("1", "A:1,B:2,C:3,D:4,E:5")
    """

    MIN_ORDER = 1
    MAX_ORDER = 5

    @classmethod
    def create_empty(cls, header):
        return cls(header, order_lines=None)

    @classmethod
    def create_with_items(cls, header, items):
        return cls(header, order_lines=list(items))

    @staticmethod
    def extract_line_details(lines):
        product_orders = lines.split(',')
        order_details = []
        for item in product_orders:
            if int(item[-1]) > ProductOrder.MAX_ORDER or \
               int(item[-1]) < ProductOrder.MIN_ORDER:
                raise ValueError("Order quantity cannot exceed 5")
            else:
                order_details.append({item[0]: int(item[-1])})

        # return [{p[0]: int(p[-1])} for p in product_orders]
        return order_details

    def __init__(self, header, order_lines):
        order_lines = ProductOrder.extract_line_details(order_lines)
        self.order_entries = {}
        self.order_entries['Header'] = header
        self.order_entries['Lines'] = order_lines

    def get_id(self):
        return self.order_entries['Header']

    def order_details(self):
        return self.order_entries['Lines']
