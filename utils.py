import pandas as pd

"""
Utility functions
"""


def set_time_intervals(df, start, end) -> pd.DataFrame:
    # возможно требует рефактора, не нашёл другого решения т.к коструктор
    # Timestamp не принимает аргумент format для даты
    start = list(map(int, start.split(".")))
    end = list(map(int, end.split(".")))
    start_ts = pd.Timestamp(day=start[0],
                            month=start[1],
                            year=start[2],
                            tz="UTC")
    end_ts = pd.Timestamp(day=end[0],
                          month=end[1],
                          year=end[2],
                          tz="UTC") + pd.Timedelta(days=1)
    time_mask = (start_ts <= df["event_time"]) & (end_ts > df["event_time"])
    return df[time_mask]


def process_date_input():
    date = input("Введите 2 даты в формате dd.mm.YYYY\n"
                 "Первая дата - начало отчёта, "
                 "вторая - конец.\n").split()
    if len(date) == 1:
        start = date[0]
        end = input()
    elif len(date) == 2:
        start = date[0]
        end = date[1]
    return start, end
