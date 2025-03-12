import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
    WEIGHT_IN_GRAMS_COLUMN,
)
from scripts.files import REMAINING_DAYS_WEIGHT_PNG, WEIGHT_CHANGE_PNG, WEIGHT_PNG

COLOR_WEIGHT_7D_AVERAGE = "#1f77b4"
COLOR_WEIGHT_14D_AVERAGE = "#ff7f0e"
COLOR_RED = "#d62728"
COLOR_MISC = "#9467bd"


def plot_figures(
    df_daily: pd.DataFrame, df: pd.DataFrame, remaining_days_weight: pd.Series
) -> None:
    # pylint: disable=too-many-locals, too-many-statements
    last_two_rows = df.tail(2)
    df = df.drop(df.tail(1).index)

    plot_weight(
        df=df,
        targets_df=last_two_rows.tail(1),
    )
    plot_remaining_days_weight(
        remaining_days_weight, df_daily=df_daily, last_two_rows=last_two_rows
    )
    plot_weekly_change(df)


def plot_weight(
    df: pd.DataFrame,
    targets_df: pd.DataFrame,
) -> None:

    is_gaining_weight = (df["target_weight_change_14d"] > 0).any()
    va_position_14d = "top" if is_gaining_weight else "bottom"
    va_position_14d_offset = -100 if is_gaining_weight else 100
    va_position_7d = "bottom" if is_gaining_weight else "top"
    va_position_7d_offset = 100 if is_gaining_weight else -100

    # pylint: disable=too-many-locals, too-many-statements
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))

    # First plot all 14d data
    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_14d_weekly",
        marker="o",
        ax=ax,
        label="14d Weekly",
        color=COLOR_WEIGHT_14D_AVERAGE,
    )
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_14d_weekly"]):
        ax.text(
            x_val,
            y_val + va_position_14d_offset,
            y_val,
            ha="center",
            va=va_position_14d,
            color=COLOR_WEIGHT_14D_AVERAGE,
        )

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_7d_weekly",
        marker="o",
        ax=ax,
        label="7d Weekly",
        color=COLOR_WEIGHT_7D_AVERAGE,
    )
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_7d_weekly"]):
        ax.text(
            x_val,
            y_val + va_position_7d_offset,
            y_val,
            ha="center",
            va=va_position_7d,
            color=COLOR_WEIGHT_7D_AVERAGE,
        )

    # Plot only the last 2 values of each column
    sns.scatterplot(
        data=targets_df,
        x=DATE_COLUMN,
        y="target_weight_14d",
        color=COLOR_WEIGHT_14D_AVERAGE,
        ax=ax,
        label="Target Weekly 14d",
        marker="x",
    )
    for x_val, y_val in zip(targets_df[DATE_COLUMN], targets_df["target_weight_14d"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_14D_AVERAGE,
            style="italic",
        )

    sns.scatterplot(
        data=targets_df,
        x=DATE_COLUMN,
        y="target_weight_7d",
        color=COLOR_WEIGHT_7D_AVERAGE,
        ax=ax,
        label="Target Weekly 7d",
        marker="x",
    )
    for x_val, y_val in zip(targets_df[DATE_COLUMN], targets_df["target_weight_7d"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_7D_AVERAGE,
            style="italic",
        )

    # save the plot
    fig.tight_layout()
    fig.savefig(WEIGHT_PNG)


def plot_remaining_days_weight(
    remaining_days_weight: pd.Series,
    df_daily: pd.DataFrame,
    last_two_rows: pd.DataFrame,
) -> None:
    # pylint: disable=too-many-locals
    df_raw_data_14_days = (
        df_daily[df_daily[WEIGHT_IN_GRAMS_COLUMN] != 0][
            [DATE_COLUMN, WEIGHT_IN_GRAMS_COLUMN]
        ]
        .tail(14)
        .copy()
    )

    df_daily_14_days = (
        df_daily[df_daily[WEIGHT_IN_GRAMS_7D_COLUMN] != 0][
            [DATE_COLUMN, WEIGHT_IN_GRAMS_7D_COLUMN]
        ]
        .tail(14)
        .copy()
    )

    df_daily_14d_14_days = (
        df_daily[df_daily[WEIGHT_IN_GRAMS_14D_COLUMN] != 0][
            [DATE_COLUMN, WEIGHT_IN_GRAMS_14D_COLUMN]
        ]
        .tail(14)
        .copy()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot 7d average for the last 14 days

    sns.lineplot(
        data=df_daily_14_days,
        x=DATE_COLUMN,
        y=WEIGHT_IN_GRAMS_7D_COLUMN,
        marker="o",
        ax=ax,
        label="7d Weight Average",
        color=COLOR_WEIGHT_7D_AVERAGE,
    )
    df_14d_last = df_daily_14_days.tail(1)
    for x_val, y_val in zip(
        df_14d_last[DATE_COLUMN], df_14d_last[WEIGHT_IN_GRAMS_7D_COLUMN]
    ):
        ax.text(
            x_val, y_val, y_val, ha="center", va="bottom", color=COLOR_WEIGHT_7D_AVERAGE
        )

    # PLot the 14d average for the last 14 days
    sns.lineplot(
        data=df_daily_14d_14_days,
        x=DATE_COLUMN,
        y="weight_in_grams_14d",
        marker="o",
        ax=ax,
        label="14d Weight Average",
        color=COLOR_WEIGHT_14D_AVERAGE,
    )
    df_14d_14d_last = df_daily_14d_14_days.tail(1)
    for x_val, y_val in zip(
        df_14d_14d_last[DATE_COLUMN], df_14d_14d_last[WEIGHT_IN_GRAMS_14D_COLUMN]
    ):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_14D_AVERAGE,
        )

    # plot the raw data for the last 14 days
    sns.lineplot(
        data=df_raw_data_14_days,
        x=DATE_COLUMN,
        y=WEIGHT_IN_GRAMS_COLUMN,
        marker="o",
        ax=ax,
        label="Daily Weight",
        color=COLOR_MISC,
    )

    # add the latest value as text -> current day weight
    df_raw_data_last = df_raw_data_14_days.tail(1)
    for x_val, y_val in zip(
        df_raw_data_last[DATE_COLUMN], df_raw_data_last[WEIGHT_IN_GRAMS_COLUMN]
    ):
        ax.text(
            x_val, y_val, y_val, ha="center", va="bottom", color=COLOR_WEIGHT_7D_AVERAGE
        )
        break

    # plot the remaining days weight
    sns.lineplot(
        data=remaining_days_weight,
        marker="o",
        ax=ax,
        label="Remaining Days Weight",
        color=COLOR_RED,
    )
    # add the values
    for x_val, y_val in zip(remaining_days_weight.index, remaining_days_weight.values):
        # round y to full integer / grams
        y_val = round(y_val)
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_RED,
        )

    # add target weight 7d
    last_row = last_two_rows.tail(1)
    sns.scatterplot(
        data=last_row,
        x=DATE_COLUMN,
        y="target_weight_7d",
        color=COLOR_WEIGHT_7D_AVERAGE,
        ax=ax,
        label="7d Target Weekly",
        marker="x",
    )
    for x_val, y_val in zip(last_row[DATE_COLUMN], last_row["target_weight_7d"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_7D_AVERAGE,
            style="italic",
        )

    # add target weight 14d
    sns.scatterplot(
        data=last_row,
        x=DATE_COLUMN,
        y="target_weight_14d",
        color=COLOR_WEIGHT_14D_AVERAGE,
        ax=ax,
        label="14d Target Weekly",
        marker="x",
    )
    for x_val, y_val in zip(last_row[DATE_COLUMN], last_row["target_weight_14d"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_14D_AVERAGE,
            style="italic",
        )
    # add the title
    ax.set_title("Detailed Weight and Remaining Days Weight")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight in Grams")
    ax.legend()

    fig.tight_layout()
    fig.savefig(REMAINING_DAYS_WEIGHT_PNG)


def plot_weekly_change(df: pd.DataFrame) -> None:
    # pylint: disable=too-many-locals, too-many-statements

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_14d_weekly_change",
        marker="o",
        ax=ax,
        label="14d Weekly Change",
        color=COLOR_WEIGHT_14D_AVERAGE,
    )
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_14d_weekly_change"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_14D_AVERAGE,
        )

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_7d_weekly_change",
        marker="o",
        ax=ax,
        label="7d Weekly Change",
        color=COLOR_WEIGHT_7D_AVERAGE,
    )
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_7d_weekly_change"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=COLOR_WEIGHT_7D_AVERAGE,
        )

    # add line plot for target weekly change (column target_weight_change)
    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="target_weight_change_14d",
        marker="o",
        ax=ax,
        label="Target Weekly Change",
        color=COLOR_RED,
    )
    for x_val, y_val in zip(df[DATE_COLUMN], df["target_weight_change_14d"]):
        ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=COLOR_RED)

    # save the plot
    fig.tight_layout()
    fig.savefig(WEIGHT_CHANGE_PNG)
