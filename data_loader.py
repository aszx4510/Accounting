
import pathlib

import pandas

from file_settings import accounting_dir

file_name = '2023-01-01-2024-01-01.csv'

file_path = accounting_dir / file_name

print(file_path)

data = pandas.read_csv(file_path)

print(data.shape)
