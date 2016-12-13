#! /usr/bin/env python

import argparse
import sys
import csv
import pickle

# ====
# MAIN
# ====
PRODUCTS = "ABCDE"


def main():
    parser = argparse.ArgumentParser(
        description='Execute convert csv file to stream file')

    parser.add_argument('-i', '--input-path', required=True,
                        dest='input_path', metavar='PATH', action='store',
                        help='Path of input CSV file')

    parser.add_argument('-o', '--output-path', required=True,
                        dest='output_path', metavar='PATH', action='store',
                        help='Path of output file to use with test')

    # COLLECT COMMAND LINE ARGUMENTS
    cl_args = parser.parse_args()
    csv_input_file = cl_args.input_path
    stream_output_file = cl_args.output_path

    # READ IN CSV FILE OF ORDERS AND CONVERT TO A DICT OBJECT
    file_rows = []
    with open(csv_input_file, 'rU') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            file_rows.append(row)

    # TRANSFORM EACH RECORD INTO A PRODUCT ORDER OBJECT
    stream_rows = []
    for index, csv_row in enumerate(file_rows):
        stream = {}
        stream['Header'] = csv_row['Header']
        stream['Lines'] = []
        if csv_row['Product:A'] and int(csv_row['Product:A']) > 0:
            stream['Lines'].append({"Product": "A",
                                    "Quantity": csv_row['Product:A']})
        if csv_row['Product:B'] and int(csv_row['Product:B']) > 0:
            stream['Lines'].append({"Product": "B",
                                    "Quantity": csv_row['Product:B']})
        if csv_row['Product:C'] and int(csv_row['Product:C']) > 0:
            stream['Lines'].append({"Product": "C",
                                    "Quantity": csv_row['Product:C']})
        if csv_row['Product:D'] and int(csv_row['Product:D']) > 0:
            stream['Lines'].append({"Product": "D",
                                    "Quantity": csv_row['Product:D']})
        if csv_row['Product:E'] and int(csv_row['Product:E']) > 0:
            stream['Lines'].append({"Product": "E",
                                    "Quantity": csv_row['Product:E']})
        stream_rows.append(stream)

    with open(stream_output_file, 'wb') as handle:
        pickle.dump(stream_rows, handle)


if __name__ == "__main__":
    exit_code = main()
    print("\nAll Done")
    sys.exit(exit_code)
