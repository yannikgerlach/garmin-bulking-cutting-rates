import os

import pandas as pd

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
    WEIGHT_IN_GRAMS_COLUMN,
)


def add_moving_average_and_change(df: pd.DataFrame, column: str, window: int) -> None:
    """
    Add a rolling mean and compute weekly changes in the rolling mean for the specified column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing time-series data, indexed by date.
    column : str
        The column name in the DataFrame on which to compute the moving average.
    window : int
        The size of the rolling window (in days) used for computing the moving average.

    Notes
    -----
    This function adds the following columns to the input DataFrame:
    - ``{column}_{window}d``: Rolling mean over the specified window.
    - ``{column}_{window}d_weekly``: Weekly resampled value of the rolling mean (using the last observed).
    - ``{column}_{window}d_weekly_change``: Difference in the weekly rolling mean over a 7-week period.

    The DataFrame is modified in-place, and no value is returned.
    """
    df[f"{column}_{window}d"] = df[column].rolling(window=window).mean()
    df[f"{column}_{window}d_weekly"] = df[f"{column}_{window}d"].resample("W").last()
    df[f"{column}_{window}d_weekly_change"] = df[f"{column}_{window}d_weekly"].diff(
        periods=7
    )


def create_weight_data_frame(data: dict) -> pd.DataFrame:
    data_weight = data["dailyWeightSummaries"]
    daily_weights = [
        (d["summaryDate"], round(d["allWeightMetrics"][0]["weight"]))
        for d in data_weight
    ]
    df = pd.DataFrame(daily_weights, columns=[DATE_COLUMN, WEIGHT_IN_GRAMS_COLUMN])

    # fill in missing dates
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
    df.set_index(DATE_COLUMN, inplace=True)
    df = df.resample("D").asfreq()
    df[WEIGHT_IN_GRAMS_COLUMN] = (
        df[WEIGHT_IN_GRAMS_COLUMN].interpolate(method="linear").round().astype(int)
    )

    return df


def process_weight_data(data: dict) -> pd.DataFrame:
    """
    Processes daily weight data and returns a DataFrame of interpolated weights with moving averages.

    This function expects a dictionary containing a "dailyWeightSummaries" key, where each item includes:
     - "summaryDate": A string representing the date.
     - "allWeightMetrics": A list of dictionaries with a "weight" key, specifying weight in grams.

    Steps:
    1. Extracts and rounds daily weight data.
    2. Resamples daily dates and interpolates missing weights.
    3. Adds 7-day and 14-day moving averages and their weekly changes.
    4. Removes the original weight columns, retaining only entries with non-null 14-day weekly changes.

    Args:
        data (dict): A dictionary containing Garmin daily weight summaries.

    Returns:
        pd.DataFrame: A DataFrame indexed by date with integer weight changes and averages for analysis.
    """
    df = create_weight_data_frame(data)

    add_moving_average_and_change(df=df, column=WEIGHT_IN_GRAMS_COLUMN, window=7)
    add_moving_average_and_change(df=df, column=WEIGHT_IN_GRAMS_COLUMN, window=14)

    return df


def filter_df_to_weekly_changes(df: pd.DataFrame) -> pd.DataFrame:
    # remove weight in grams columns
    df = df.drop(
        columns=[
            WEIGHT_IN_GRAMS_COLUMN,
            WEIGHT_IN_GRAMS_7D_COLUMN,
            WEIGHT_IN_GRAMS_14D_COLUMN,
        ]
    )

    # only show the rows where the weekly change is not null
    df = df[df["weight_in_grams_14d_weekly_change"].notnull()]

    return df.round().astype(int)


def add_target_weight_change(df: pd.DataFrame, window: int) -> pd.DataFrame:
    column = f"weight_in_grams_{window}d_weekly"
    target_weight_change_column = f"target_weight_change_{window}d"
    target_weight_column = f"target_weight_{window}d"

    weekly_change_percentage = float(
        os.getenv("TARGET_WEEKLY_CHANGE_PERCENTAGE", "0.0")
    )
    df_without_last_row = df.iloc[:-1]
    df[target_weight_change_column] = (
        (df_without_last_row[column] * weekly_change_percentage).round().astype(int)
    )

    first_value = df[column].iloc[0]
    df[target_weight_column] = (
        (df_without_last_row[column] + df[target_weight_change_column])
        .shift(1)
        .fillna(value=first_value)
        .round()
        .astype(int)
    )

    return df
