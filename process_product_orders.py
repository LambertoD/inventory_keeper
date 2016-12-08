#! /usr/bin/env python

import argparse
import csv
import sys
from inventory import Inventory
from product_orders import ProductOrder
import pytest

# ====
# MAIN
# ====
PRODUCTS = "ABCDE"


def main():
    parser = argparse.ArgumentParser(
        description='Execute run inventory workflow')

    parser.add_argument('-i', '--input-path', required=True,
                        dest='input_path', metavar='PATH', action='store',
                        help='Path of input file to use with test')

    parser.add_argument('-q', '--inventory-qty',
                        dest='inventory_qty', type=int, action='store',
                        help='Setting for initial inventory quantity, '
                             'default is 100')

    # COLLECT COMMAND LINE ARGUMENTS
    cl_args = parser.parse_args()
    csv_input_file = cl_args.input_path

    # SET INITIAL INVENTORY WITH EACH PRODUCT QUANTITY EQUAL TO 100
    qty_per_product = cl_args.inventory_qty if cl_args else 100
    inventory = Inventory()
    for product in PRODUCTS:
        inventory.add(product, qty_per_product)
    # Test example inventory with uneven quantities
    # inventory.add('A', 2)
    # inventory.add('B', 3)
    # inventory.add('C', 1)
    # inventory.add('D', 0)
    # inventory.add('E', 0)

    # READ IN CSV FILE OF ORDERS AND CONVERT TO A DICT OBJECT
    file_rows = []
    with open(csv_input_file, 'rU') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            file_rows.append(row)

    # TRANSFORM EACH RECORD INTO A PRODUCT ORDER OBJECT
    order_history = []
    for index, csv_row in enumerate(file_rows):
        header = csv_row['Header']
        lines = csv_row['Lines']
        order_lines = lines.replace('"', '')
        try:
            order = ProductOrder(header, order_lines)
            inventory_depleted, order_status = process_order(order, inventory)
            if not inventory_depleted:
                order_history.append(order_status)
            else:
                break

        except ValueError as e:
            print(e)

    print_order_history(order_history)


def process_order(order, inventory):
    inventory_exhausted = False
    header = order.get_id()
    details = order.order_details()
    products = list(PRODUCTS)
    print_order_part1 = '{}: '.format(header)
    print_order_part2 = format_order_line(products, header, details)
    orders_fulfilled = {}
    back_orders_for_order = {}
    for item in order.order_details():
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
