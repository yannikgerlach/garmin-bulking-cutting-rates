import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
)
from scripts.files import (
    DAILY_DATA_FILE,
    WEEKLY_DATA_FILE,
    WEIGHT_CHANGE_PNG,
    WEIGHT_PNG,
)


def plot_figures():
    df_daily = pd.read_csv(DAILY_DATA_FILE)
    df_daily[DATE_COLUMN] = pd.to_datetime(df_daily[DATE_COLUMN])

    df = pd.read_csv(WEEKLY_DATA_FILE)
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

    last_two_rows = df.tail(2)
    df = df.drop(df.tail(1).index)

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
    
    target_this_week = last_two_rows.tail(1)
    target_this_week_weight = target_this_week["target_weight_7d"].values[0]
    target_this_week_day = target_this_week[DATE_COLUMN].values[0]
    most_recent_reading_date = df_daily[DATE_COLUMN].max()
    remaining_days_this_week = (target_this_week_day - most_recent_reading_date).days
    
    # we now have 7 - remaining_days_this_week days of data
    # at the end of the week the average should be the target weight
    # so we need to calculate the average of the remaining days
    # TODO: NEEDS TO BE ON RAW DATA
    raw_data_weight_first_days = df_daily["weight_in_grams"].tail(7 - remaining_days_this_week)
    
    # the average of raw_data_weight_first_days + some values needs to be target_this_week_weight
    # we want to find out the values needed to add to raw_data_weight_first_days to get target_this_week_weight
    # we can do this by calculating the average of raw_data_weight_first_days and then adding the difference
    # between the target_this_week_weight and the average to each value in raw_data_weight_first_days
    average_weight = raw_data_weight_first_days.mean()
    difference = target_this_week_weight - average_weight
    # find the reamining raw weight data (remaining_days_this_week) to get to the desired target weight
    
    target_weight_sum = target_this_week_weight * 7 - sum(raw_data_weight_first_days)
    target_weight_per_day = target_weight_sum / remaining_days_this_week
    
    # now we want to distribute the weight unevenly over the remaining days
    # so that it increases over time (or decreases) to reach the target weight
    
    # assume we want to gain weight
    average_weight_days_so_far = raw_data_weight_first_days.mean() # that's the minimum weight
    
    difference_needed_per_day = target_weight_per_day - average_weight_days_so_far
    
    full_target_weight_sum = sum(raw_data_weight_first_days) + target_weight_sum
    
    # interpolate using pandas on the sums
    interpolate_df = pd.DataFrame()
    interpolate_df["weight"] = np.cumsum(raw_data_weight_first_days).values.tolist() + (remaining_days_this_week - 1) * [np.nan] + [float(full_target_weight_sum)]
    remaining_days_weight = interpolate_df['weight'].interpolate(method="quadratic").diff().tail(remaining_days_this_week)
    

    # Plot each series
    df_7d_last = df_7d.tail(1)
    df_14d_last = df_14d.tail(1)

    line_7d = sns.lineplot(
        data=df_7d,
        x=DATE_COLUMN,
        y=WEIGHT_IN_GRAMS_7D_COLUMN,
        marker="o",
        ax=ax,
        label="7d",
    )
    color_7d = line_7d.get_lines()[-1].get_color()
    for x_val, y_val in zip(df_7d_last[DATE_COLUMN], df_7d_last[WEIGHT_IN_GRAMS_7D_COLUMN]):
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
        ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_14d.get_color())

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
        ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_7d.get_color())

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
    for x_val, y_val in zip(last_two_rows[DATE_COLUMN], last_two_rows["target_weight_14d"]):
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
    for x_val, y_val in zip(last_two_rows[DATE_COLUMN], last_two_rows["target_weight_7d"]):
        ax.text(
            x_val,
            y_val,
            y_val,
            ha="center",
            va="bottom",
            color=line_7d.get_color(),
            style="italic",
        )


    # save the plot
    fig.savefig(WEIGHT_PNG)

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
            x_val, y_val, y_val, ha="center", va="bottom", color=line_14d_change.get_color()
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
            x_val, y_val, y_val, ha="center", va="bottom", color=line_7d_change.get_color()
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


if __name__ == "__main__":
    plot_figures()
