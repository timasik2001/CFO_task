import sys

import pandas as pd

import utils
import help
import analyzes
from globals import date


def main():
    if "--help" in sys.argv:
        help.help()
        return
    if len(sys.argv) == 1:
        print("Не хватает пути/до/excel, \n"
              "воспользуйтесь командой python main.py --help")
        return
    excel_file_path = sys.argv[1]
    print("Открываем excel, может занять несколько минут...")
    initial_df = pd.read_excel(excel_file_path, parse_dates=["event_time"])
    date["start"], date["end"] = utils.process_date_input()
    df = utils.set_time_intervals(initial_df)
    # 1 Анализ соверённых событий пользователями
    analyzes.event_type_report(df)
    # 2 Рейтинг категорий товаров по покупке
    analyzes.category_code_rating(df)


if __name__ == "__main__":
    main()
