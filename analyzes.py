from typing import Optional

import numpy as np
import pandas as pd

"""
Each class represents one report
"""


class EventTypeAnalysis:
    def __init__(self, df: pd.DataFrame):

        df = df.groupby(["user_session"])["event_type"].apply(set).reset_index()
        df["has_cart"] = df["event_type"].apply(lambda x: "cart" in x)
        df["has_view"] = df["event_type"].apply(lambda x: "view" in x)
        df["has_purchase"] = df["event_type"].apply(lambda x: "purchase" in x)

        self.LABEL = "Анализ совершённых событий"
        self.report = pd.DataFrame(
            columns=[self.LABEL],
            index=[
                "Количество сессий",
                "Просмотры",
                "Добавлений в карзину",
                "Покупок",
                "% просмотров",
                "% добавлений в карзину",
                "% покупок"
                ])
        self.total_sessions = len(df)

        self.views = df["has_view"].sum()
        self.carts = df["has_cart"].sum()
        self.purchases = df["has_purchase"].sum()

        self.view_percentage = round(self.views / self.total_sessions, 3)
        self.cart_percentage = round(self.carts / self.total_sessions, 3)
        self.purchases_percentage = round(self.purchases / self.total_sessions, 3)

    def make_report(self):
        self.report.loc["Количество сессий", self.LABEL] = self.total_sessions
        self.report.loc["Просмотры", self.LABEL] = self.views
        self.report.loc["Добавлений в карзину", self.LABEL] = self.carts
        self.report.loc["Покупок", self.LABEL] = self.purchases
        self.report.loc["% просмотров", self.LABEL] = self.view_percentage
        self.report.loc["% добавлений в карзину", self.LABEL] = self.cart_percentage
        self.report.loc["% покупок", self.LABEL] = self.purchases_percentage


class CategoryCodeRatingAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.LABEL = "Рейтинг категорий товаров"
        self.report: pd.DataFrame = df

    def make_report(self):
        purchases_df = self.report[self.report["event_type"] == "purchase"]
        self.report = purchases_df.groupby("category_code")["product_id"].count().sort_values(ascending=False).reset_index()
        self.report.columns = ["Категория товара", "Количество совершенных покупок"]


class TimeBeforePurchaseAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.LABEL = "Время перед покупкой"
        self.report: pd.DataFrame = df

    @staticmethod
    def calc_time_diffs(session_df):

        first_view = session_df[session_df["event_type"] == "view"]["event_time"].min()
        purchase = session_df[session_df["event_type"] == "purchase"]["event_time"].min()

        result = {
            "price": np.nan,
            "total_seconds": np.nan
        }

        if pd.notna(first_view) and pd.notna(purchase) and purchase >= first_view:
            result["price"] = session_df[session_df["event_type"] == "purchase"]["price"].min()
            result["total_seconds"] = (purchase - first_view).total_seconds()
        return pd.Series(result)

    def make_report(self):
        session_time_sorted_df = self.report.sort_values(["user_session", "event_time"])

        self.report = session_time_sorted_df.groupby('user_session').apply(TimeBeforePurchaseAnalysis.calc_time_diffs).reset_index().dropna()
        self.report.sort_values("price", inplace=True)


def make_reports(df, start, end):
    # 1
    event_type_analysis = EventTypeAnalysis(df)
    event_type_analysis.make_report()

    # 2
    category_code_rating = CategoryCodeRatingAnalysis(df)
    category_code_rating.make_report()

    # 3
    time_before_puchase = TimeBeforePurchaseAnalysis(df)
    time_before_puchase.make_report()
    # dump all reports
    with pd.ExcelWriter(f"output/{start} - {end}.xlsx") as writer:
        event_type_analysis.report.to_excel(writer,
                                            sheet_name=event_type_analysis.LABEL,)

        category_code_rating.report.to_excel(writer,
                                             sheet_name=category_code_rating.LABEL,
                                             index=False)

        time_before_puchase.report.to_excel(writer,
                                            sheet_name=time_before_puchase.LABEL,
                                            index=False)
