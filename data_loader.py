import json
import pathlib

import pandas as pd

from file_settings import accounting_dir


def concat_filepath(filename: str, default_dir: pathlib = accounting_dir):
    return default_dir / filename


def load_money_manager_data(file_name: str):
    filepath = concat_filepath(file_name, default_dir=accounting_dir)
    df_data = pd.read_csv(filepath)
    print(df_data.shape)

    return df_data


def load_ahorro_data(file_name: str):
    filepath = concat_filepath(file_name, default_dir=accounting_dir)

    with open(filepath, 'r', encoding='utf8') as data_input:
        data = json.load(data_input)
    return data


if __name__ == '__main__':
    # name = '2023-01-01-2024-01-01.csv'
    # load_money_manager_data(name)

    name = 'Ahorro_Backup_20190522144210.json'
    data_json = load_ahorro_data(name)

    print(data_json)
