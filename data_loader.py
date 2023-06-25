import pathlib

import pandas

from file_settings import accounting_dir


def concat_filepath(filename: str, default_dir: pathlib = accounting_dir):
    return default_dir / filename


def load_money_manager_data(file_name: str):
    filepath = concat_filepath(file_name, default_dir=accounting_dir)
    df_data = pandas.read_csv(filepath)
    print(df_data.shape)

    return df_data


if __name__ == '__main__':
    name = '2023-01-01-2024-01-01.csv'
    load_money_manager_data(name)
