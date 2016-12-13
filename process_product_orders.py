#! /usr/bin/env python

import argparse
import logging
import pickle
import sys
from inventory import Inventory
from product_orders import ProductOrder

# ====
# MAIN
# ====
PRODUCTS = "ABCDE"


def main():
    parser = argparse.ArgumentParser(
        description='Execute run inventory workflow')

    parser.add_argument('-i', '--input-path', required=True,
                        dest='input_path', metavar='PATH', action='store',
                        help='Path of input stream file to use with test')

    parser.add_argument('-q', '--inventory-qty',
                        dest='inventory_qty', type=int, action='store',
                        help='Setting for initial inventory quantity, '
                             'default is 100')

    # SETUP LOGGING
    logging.basicConfig(filename='log/inventory_keeper.log',
                        filemode='w', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s | %(message)s')
    logging.info('\n%s\nSTART Order Processing Session\n%s' %
                 ('-' * 108, '-' * 108))
    # COLLECT COMMAND LINE ARGUMENTS
    cl_args = parser.parse_args()
    csv_input_file = cl_args.input_path

    # SET INITIAL INVENTORY WITH EACH PRODUCT QUANTITY EQUAL TO 100
    qty_per_product = cl_args.inventory_qty if cl_args.inventory_qty else 100
    inventory = Inventory()
    for product in PRODUCTS:
        inventory.add(product, qty_per_product)
    # Test example inventory with uneven quantities
    # inventory.add('A', 2)
    # inventory.add('B', 3)
    # inventory.add('C', 1)
    # inventory.add('D', 0)
    # inventory.add('E', 0)

    with open(csv_input_file, 'rb') as handle:
        input_stream = pickle.load(handle)

    # TRANSFORM EACH RECORD INTO A PRODUCT ORDER OBJECT
    order_history = []
    for index, csv_row in enumerate(input_stream):
        logging.info('Processing Order: {}'.format(csv_row))
        header = csv_row['Header']
        lines = csv_row['Lines']

        # format order_lines as 'A:1,B:2,C:3,D:4,E:5'
        order_list = \
            ["{}:{}".format(x['Product'], x['Quantity']) for x in lines]
        order_lines = ','.join(order_list)
        try:
            order = ProductOrder(header, order_lines)
            inventory_depleted, order_status = process_order(order, inventory)
            if not inventory_depleted:
                order_history.append(order_status)
            else:
                break

        except ValueError as e:
            error_msg = "Error occured during execution: %s\n%s\n" \
                % (e.__class__.__name__, e.message)
            logging.error(error_msg)
            message = "\n*** WARNING: Order \'{0}\' with items \'{}\' was" \
                "not processed".format(order.get_id(), order.order_details())
            logging.error(message)

    print_order_history(order_history)

    logging.info('\n%s\nEND Order Processing Session\n%s' %
                 ('-' * 108, '-' * 108))


def process_order(order, inventory):
    inventory_exhausted = False
    header = order.get_id()
    details = order.order_details()
    products = list(PRODUCTS)
    print_order_part1 = '{}: '.format(header)
    print_order_part2 = format_order_line(products, header, details)
    orders_fulfilled = {}
    back_orders_for_order = {}
    for item in details:
        product = list(item.keys())[0]
        quantity = list(item.values())[0]
        if inventory_has_products(inventory):
            # message = "Order Processed"
            qty_fulfilled = inventory.fulfill_order(product, quantity)
            orders_fulfilled[product] = qty_fulfilled
            if inventory.has_back_order(product):
                back_orders_for_order[product] = quantity - qty_fulfilled
            else:
                back_orders_for_order[product] = 0
        else:
            # message = "Inventory Exhausted. Can't process more orders"
            orders_fulfilled[product] = 0
            inventory_exhausted = True
            logging.info('\n%s Inventory Exhausted.  Stop processing '
                         'more orders%s' %
                         ('>' * 10, '<' * 10))

    print_order_part3 = format_order_line(products, header, orders_fulfilled)
    # back_orders = get_back_orders(products, inventory)
    print_order_part4 = format_order_line(products, header,
                                          back_orders_for_order)
    order_status = \
        "{} {}::{}::{}".format(print_order_part1, print_order_part2,
                               print_order_part3, print_order_part4)
    return (inventory_exhausted, order_status)


def inventory_has_products(inventory):
    total_quantity = 0
    for product in PRODUCTS:
        total_quantity += inventory.lookup(product)
    # print("current inventory: {}".format(inventory.entries))
    # print(total_quantity)
    return total_quantity != 0


def format_order_line(products, header, details):
    order = {}
    for product in products:
        if isinstance(details, list):
            product_value = [x[product] for x in details if product in x]
            if product_value:
                order[product] = product_value[0]
            else:
                order[product] = 0
        else:
            if product in details:
                order[product] = details[product]
            else:
                order[product] = 0
    return "{},{},{},{},{}".format(order['A'], order['B'],
                                   order['C'], order['D'], order['E'])


def get_back_orders(products, inventory):
    back_order = {}
    for product in products:
        back_order[product] = inventory.lookup_back_order(product)
    return back_order


def print_order_history(order_history):
    for item in order_history:
        print(item)

if __name__ == "__main__":
    exit_code = main()
    print("\nAll Done")
    sys.exit(exit_code)
