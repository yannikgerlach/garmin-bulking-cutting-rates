import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
)
from scripts.files import WEIGHT_CHANGE_PNG, WEIGHT_PNG


def plot_figures(
    df_daily: pd.DataFrame, df: pd.DataFrame, remaining_days_weight: pd.Series
) -> None:
    # pylint: disable=too-many-locals, too-many-statements
    last_two_rows = df.tail(2)
    df = df.drop(df.tail(1).index)

    plot_weight(
        df_daily=df_daily,
        df=df,
        remaining_days_weight=remaining_days_weight,
        last_two_rows=last_two_rows,
    )
    plot_weekly_change(df)


def plot_weight(
    df_daily: pd.DataFrame,
    df: pd.DataFrame,
    remaining_days_weight: pd.Series,
    last_two_rows: pd.DataFrame,
) -> None:
    # pylint: disable=too-many-locals, too-many-statements
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))

    # plot weight_in_grams_7d (removing zeros)
    # Create separate dataframes for 7d and 14d data, remove zeros
    df_7d = (
        df_daily[df_daily[WEIGHT_IN_GRAMS_7D_COLUMN] != 0][
            [DATE_COLUMN, WEIGHT_IN_GRAMS_7D_COLUMN]
        ]
        .tail(7)
        .copy()
    )
    df_14d = (
        df_daily[df_daily[WEIGHT_IN_GRAMS_14D_COLUMN] != 0][
            [DATE_COLUMN, WEIGHT_IN_GRAMS_14D_COLUMN]
        ]
        .tail(7)
        .copy()
    )

    # Plot each series
    df_7d_last = df_7d.tail(1)

    line_7d = sns.lineplot(
        data=df_7d,
        x=DATE_COLUMN,
        y=WEIGHT_IN_GRAMS_7D_COLUMN,
        marker="o",
        ax=ax,
        label="7d",
    )
    color_7d = line_7d.get_lines()[-1].get_color()
    for x_val, y_val in zip(
        df_7d_last[DATE_COLUMN], df_7d_last[WEIGHT_IN_GRAMS_7D_COLUMN]
    ):
        ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=color_7d)

    line_14d = sns.lineplot(
        data=df_14d,
        x=DATE_COLUMN,
        y=WEIGHT_IN_GRAMS_14D_COLUMN,
        marker="o",
        ax=ax,
        label="14d",
    )

    # First plot all 14d data
    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_14d_weekly",
        marker="o",
        ax=ax,
        label="14d Weekly",
    )
    line_14d = ax.lines[-1]
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_14d_weekly"]):
        ax.text(
            x_val, y_val, y_val, ha="center", va="bottom", color=line_14d.get_color()
        )

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_7d_weekly",
        marker="o",
        ax=ax,
        label="7d Weekly",
    )
    line_7d = ax.lines[-1]
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_7d_weekly"]):
        ax.text(
            x_val, y_val, y_val, ha="center", va="bottom", color=line_7d.get_color()
        )

    # Plot only the last 2 values of each column
    sns.scatterplot(
        data=last_two_rows,
        x=DATE_COLUMN,
        y="target_weight_14d",
        color=line_14d.get_color(),
        ax=ax,
        label="Target Weekly 14d",
        marker="x",
    )
    for x_val, y_val in zip(
        last_two_rows[DATE_COLUMN], last_two_rows["target_weight_14d"]
    ):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=line_14d.get_color(),
            style="italic",
        )

    sns.scatterplot(
        data=last_two_rows,
        x=DATE_COLUMN,
        y="target_weight_7d",
        color=line_7d.get_color(),
        ax=ax,
        label="Target Weekly 7d",
        marker="x",
    )
    for x_val, y_val in zip(
        last_two_rows[DATE_COLUMN], last_two_rows["target_weight_7d"]
    ):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=line_7d.get_color(),
            style="italic",
        )

    sns.lineplot(
        data=remaining_days_weight,
        marker="o",
        ax=ax,
        label="Remaining Days",
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
            color=color_7d,
        )

    # save the plot
    fig.savefig(WEIGHT_PNG)


def plot_weekly_change(df: pd.DataFrame) -> None:
    # pylint: disable=too-many-locals, too-many-statements
    # plot the weekly change separately

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_14d_weekly_change",
        marker="o",
        ax=ax,
        label="14d Weekly Change",
    )
    line_14d_change = ax.lines[-1]
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_14d_weekly_change"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=line_14d_change.get_color(),
        )

    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="weight_in_grams_7d_weekly_change",
        marker="o",
        ax=ax,
        label="7d Weekly Change",
    )
    line_7d_change = ax.lines[-1]
    for x_val, y_val in zip(df[DATE_COLUMN], df["weight_in_grams_7d_weekly_change"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=line_7d_change.get_color(),
        )

    # add line plot for target weekly change (column target_weight_change)
    sns.lineplot(
        data=df,
        x=DATE_COLUMN,
        y="target_weight_change_14d",
        marker="o",
        ax=ax,
        label="Target Weekly Change",
        color="red",
    )
    line_target = ax.lines[-1]
    for x_val, y_val in zip(df[DATE_COLUMN], df["target_weight_change_14d"]):
        ax.text(
            x_val, y_val, y_val, ha="center", va="bottom", color=line_target.get_color()
        )

    # save the plot
    fig.savefig(WEIGHT_CHANGE_PNG)
