from IPython.display import display

from data_loader import load_money_manager_data


def main():
    file_name = '2023-01-01-2024-01-01.csv'
    df_data = load_money_manager_data(file_name)
    display(df_data)


if __name__ == '__main__':
    main()
