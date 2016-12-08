# Inventory Keeper

Inventory Keeper is a Python project that processes a stream of orders and maintains an inventory of products.

Features:
---------
* Initialize inventory
* Generate a stream of orders to fulfill against the inventory (Use CSV file)
* Create a back-order data structure to list orders that cannot be fulfilled
* Print a summary of order activity by order received. List the order number, the quantities of product inventory, the quantities of order fulfilled, and the quantities of the back-order if any


Run tests:
`$ python3 -m unittest -v`

Run process_product_orders where "-i" is location of input csv file and
"q" is the initial quantity value for each product in inventory:
`$ python process_product_orders.py -i data/order_sample1.csv -q 5`

To display arguments used by process_product_orders:
`$ python process_product_orders.py -h`
