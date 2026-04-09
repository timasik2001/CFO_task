import sys

import pandas as pd

import utils
import help
import analyzes


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
    start, end = utils.process_date_input()
    df = utils.set_time_intervals(initial_df, start, end)
    analyzes.make_reports(df, start, end)


if __name__ == "__main__":
    main()
