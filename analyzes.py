from typing import Optional

import pandas as pd

from globals import date


class EventTypeAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.LABEL = "Анализ совершённых событий пользователями"
        self.report: Optional[pd.DataFrame] = None
        self.total_sessions = len(df)

        self.views = df["has_view"].sum()
        self.carts = df["has_cart"].sum()
        self.purchases = df["has_purchase"].sum()

        self.view_percentage = round(self.views / self.total_sessions, 3)
        self.cart_percentage = round(self.carts / self.total_sessions, 3)
        self.purchases_percentage = round(self.purchases / self.total_sessions, 3)

    def make_report(self) -> pd.DataFrame:
        self.report = pd.DataFrame(
            columns=[self.LABEL],
            index=[
                "Колличество сессий",
                "Просмотры",
                "Добавлений в карзину",
                "Покупок",
                "% просмотров",
                "% добавлений в карзину",
                "% покупок"
                ])
        self.df.loc["Колличество сессий", self.LABEL] = self.total_sessions
        self.df.loc["Просмотры", self.LABEL] = self.views
        self.df.loc["Добавлений в карзину", self.LABEL] = self.carts
        self.df.loc["Покупок", self.LABEL] = self.purchases
        self.df.loc["% просмотров", self.LABEL] = self.view_percentage
        self.df.loc["% добавлений в карзину", self.LABEL] = self.cart_percentage
        self.df.loc["% покупок", self.LABEL] = self.purchases_percentage

    def dump_report(self):
        with pd.ExcelWriter(f"{date['start']} - {date['end']}.xlsx") as writer:
            self.report.to_excel(writer, sheet_name=self.LABEL)


def event_type_report(df):
    event_type_df = df.groupby(["user_session"])["event_type"].apply(set).reset_index()
    event_type_df["has_view"] = event_type_df["event_type"].apply(lambda x: "view" in x)
    event_type_df["has_cart"] = event_type_df["event_type"].apply(lambda x: "cart" in x)
    event_type_df["has_purchase"] = event_type_df["event_type"].apply(lambda x: "purchase" in x)

    event_type_analysis = EventTypeAnalysis(event_type_df)
    event_type_analysis.make_report()
    event_type_analysis.dump_report()


class CategoryCodeRating:
    def __init__(self, df):
        self.LABEL = "Рейтинг категорий товаров по покупке"
        self.df: pd.DataFrame = df
        self.report: Optional[pd.DataFrame] = None

    def make_report(self):
        purchases_df = self.df[self.df["event_type"] == "purchase"]
        self.report = purchases_df.groupby("category_code")["product_id"].count().sort_values(ascending=False).reset_index()
        self.report.columns = ["Категория товара", "Колличество совершенных покупок"]

    def dump_report(self):
        with pd.ExcelWriter(f"{date['start']} - {date['end']}.xlsx") as writer:
            self.report.to_excel(writer, sheet_name=self.LABEL)


def category_code_rating(df):
    category_code_rating_analysis = CategoryCodeRating(df)
    category_code_rating_analysis.dump_report()