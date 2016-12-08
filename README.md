# Inventory Keeper

Inventory Keeper is a Python project that processes a stream of orders and maintains an inventory of products.

### Features:

* Initialize inventory
* Generate a stream of orders to fulfill against the inventory (Use CSV file)
* Create a back-order data structure to list orders that cannot be fulfilled
* Print a summary of order activity by order received. List the order number, the quantities of product inventory, the quantities of order fulfilled, and the quantities of the back-order if any


## Run tests:
`$ python3 -m unittest -v`

## Execute Process Order CLI command
There are 2 client programs that can be run.  They differ in the format of the input file used.   Input is generated through spreadsheet table saved as CSV file.

### CLI client 1: `process_product_orders_joined_lines_csv.py`
#### Requires input in the following format:

Input File is a CSV format file with 2 columns, where 1st column is Header containing IDs, 2nd row is Lines which contains string of key:value pairs separated by commas where key is product and value is quantity

| Header   | Lines               |
| :------: |:-------------:      |
| 1        | A:1,B:1,C:1,D:1,E:1 |
| 2        | A:1,C:1             |
| 3        | E:5                 |

Run client 1 where:

"-i" is the path to the input csv file and
"q" is the initial quantity value for each product in inventory:

`$ python process_product_orders_joined_lines_csv.py \
   -i data/order_sample1.csv -q 5`

To display arguments used by process_product_orders_joined_lines_csv:
`$ python process_product_orders_joined_lines_csv.py -h`

### CLI client 2: `process_product_orders.py`

#### Requires CSV input in the following format:

Header column contains ID, Lines column is blank, Product:A thru Product:E contain quanties for each product

| Header  | Lines | Product:A | Product:B | Product:C | Product:D | Product:E |
| :------:|:----: |:----:     |:----:     |:----:     |:----:     |:----:     |
| 1       |       | 1         |           |    1      |           |           |
| 2       |       |           |           |           |           |     5     |
| 3       |       |           |           |           |     4     |           |
| 5       |       |           |    3      |           |           |          |

This client requires 2 steps to generate the processed order report.

Step 1: Convert CSV to a stream file

`$ python convert_csv_to_stream.py -i data/order_products_in_columns1.csv -o data/stream_file.txt`

Step 2: Run cli to generate inventory report

`$ python process_product_orders.py -i data/stream_file.txt -q 5`

"-i" is the path to the input csv file and

"q" is the initial quantity value for each product in inventory:
