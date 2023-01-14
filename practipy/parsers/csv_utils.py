import csv


def parse_csv_row(row_string: str):
    """
    Parse a string containing one row of CSV data
    """
    values = list(csv.reader([row_string]))
    return values[0] if values else None
