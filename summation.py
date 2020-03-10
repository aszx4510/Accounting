
import json


def load_data(data_path):
    with open(data_path, 'r', encoding='utf8') as data_input:
        data = json.load(data_input)
    return data


def main():
    data_path = 'data/Ahorro_Backup_20190522144210.json'
    data = load_data(data_path)
    print(data)


if __name__ == '__main__':
    main()
