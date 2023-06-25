
import json

from file_settings import accounting_dir


def load_data(data_path):
    with open(data_path, 'r', encoding='utf8') as data_input:
        data = json.load(data_input)
    return data


def main():
    file_name = 'Ahorro_Backup_20190522144210.json'
    data_path = accounting_dir / file_name
    data = load_data(data_path)
    print(data)


if __name__ == '__main__':
    main()
