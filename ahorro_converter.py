from data_loader import load_ahorro_data
import pandas as pd
from IPython.display import display
from file_settings import output_dir


def get_ahorro_categories(category_list: list):
    print(len(category_list))

    category_mapping = {item['_id']: item['default_name'] for item in category_list}

    print(category_mapping)
    print(len(category_mapping))

    return category_mapping


def convert_ahorro_data(data: dict):
    real_data = data['tables']
    # print(real_data)
    data_dict = {item['tableName']: item['items'] for item in real_data}

    # print(data_dict)

    category_mapping = get_ahorro_categories(data_dict['category'])

    df_expense = pd.DataFrame.from_dict(data_dict['expense'])
    df_income = pd.DataFrame.from_dict(data_dict['income'])

    df_expense['type'] = df_expense['category_id'].map(category_mapping)
    df_income['type'] = df_income['category_id'].map(category_mapping)


    display(df_expense)
    display(df_income)


def save_data(file_name: str):
    output_dir

def main(file_name: str):
    data = load_ahorro_data(file_name)
    convert_ahorro_data(data)


if __name__ == '__main__':
    name = 'Ahorro_Backup_20190522144210.json'
    main(name)
