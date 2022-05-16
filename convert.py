import csv
from glob import escape
from typing import List
import os


INTEGER_TYPE = 0
FLOAT_TYPE = 1
VARCHAR_TYPE = 2

class TypeConversion:
    def __init__(self):
        self.integers = {}
        self.strings = {}
        self.floats = {}

    def convert_integer(self, i):
        if i != '':
            i = int(i)
        if i not in self.integers:
            self.integers[i] = len(self.integers) + 1  # + 1, since FROSTT spare tensors are one-indexed
        return self.integers[i]

    def convert_string(self, s: str):
        if s not in self.strings:
            self.strings[s] = len(self.strings) + 1
        return self.strings[s]

    def convert_float(self, f: float):
        if f != '':
            f = float(f)
        if f not in self.floats:
            self.floats[f] = len(self.floats) + 1
        return self.floats[f]

def get_rows(csv_file_name: str, row_types: List[int]):
    tc = TypeConversion()
    with open(csv_file_name, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', escapechar='\\', quotechar='"', doublequote=False, quoting=csv.QUOTE_MINIMAL)
        for i, row in enumerate(reader):
            output_row = []
            for value, value_type in zip(row, row_types):
                try:
                    if value_type == INTEGER_TYPE:
                        output_value = tc.convert_integer(value)
                    elif value_type == FLOAT_TYPE:
                        output_value = tc.convert_string(value)
                    elif value_type == VARCHAR_TYPE:
                        output_value = tc.convert_string(value)
                except ValueError:
                    print(row)
                    print(f'failed to parse row {i} in {csv_file_name}')
                output_row.append(output_value)
            yield output_row

def convert_csv(csv_file_name: str, row_types: List[int], output_file_name: str, has_unique_rows: bool=True):
    if has_unique_rows:
        with open(output_file_name, mode='w') as output_file:
            for output_row in get_rows(csv_file_name, row_types):
                output_row.append(1)
                output_file.write(' '.join(str(v) for v in output_row))
                output_file.write('\n')
    else:
        row_freq = {}
        row_order = []
        for output_row in get_rows(csv_file_name, row_types):
            output_tup = tuple(output_row)
            if output_tup not in row_freq:
                row_freq[output_tup] = 1
                row_order.append(output_tup)
            else:
                row_freq[output_tup] += 1
        with open(output_file_name, mode='w') as output_file:
            for output_tup in row_order:
                output_row = list(output_tup)
                output_row.append(row_freq[output_tup])
                output_file.write(' '.join(str(v) for v in output_row))
                output_file.write('\n')

def parse_imdb_schema(schema_path: str):
    with open(schema_path, mode='r') as schema_file:
        schema = {}
        curr_table_name = None
        curr_row_types = []
        for line in schema_file.readlines():
            if line.startswith('CREATE TABLE'):
                if curr_table_name:
                    schema[curr_table_name] = curr_row_types
                curr_table_name = line.split()[2]
                curr_row_types = []
            elif 'character varying' in line:
                curr_row_types.append(VARCHAR_TYPE)
            elif 'integer' in line:
                curr_row_types.append(INTEGER_TYPE)
            elif line == ');\n' or not line.split():
                pass
            else:
                raise Exception(f'failed to parse line:\n{line}')
        if curr_table_name:
            schema[curr_table_name] = curr_row_types
        return schema

def generate_imdb_tensors(imdb_dir: str, output_dir: str, tables=None):
    schema_path = os.path.join(imdb_dir, 'schematext.sql')
    schema = parse_imdb_schema(schema_path)
    for table_name, row_types in schema.items():
        if tables and table_name in tables:
            csv_file_name = os.path.join(imdb_dir, table_name + '.csv')
            output_file_name = os.path.join(output_dir, table_name + '.tns')
            print(f'generating {output_file_name}')
            convert_csv(csv_file_name, row_types, output_file_name, True)

generate_imdb_tensors('imdb', 'imdb_tns', {'title'})