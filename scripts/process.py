import json

import pandas as pd

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
    WEIGHT_IN_GRAMS_COLUMN,
)
from scripts.files import RAW_DATA_FILE
from scripts.plot import plot_figures
from scripts.predictions import DailyWeightForecaster
from scripts.process_weight_data import (
    add_target_weight_change,
    filter_df_to_weekly_changes,
    process_weight_data,
)


def process_weekly_data(df: pd.DataFrame) -> pd.DataFrame:
    df_weekly = filter_df_to_weekly_changes(df)

    df_weekly = pd.concat(
        [
            df_weekly,
            pd.DataFrame(
                index=pd.date_range(
                    df_weekly.index[-1] + pd.DateOffset(days=1),
                    periods=1,
                    freq="W",
                    name=DATE_COLUMN,
                )
            ),
        ]
    )

    df_weekly = add_target_weight_change(df_weekly, window=14)
    df_weekly = add_target_weight_change(df_weekly, window=7)

    df_weekly = df_weekly.fillna(0).astype("int")
    df_weekly = df_weekly.reset_index()
    df_weekly[DATE_COLUMN] = pd.to_datetime(df_weekly[DATE_COLUMN])
    return df_weekly


def process_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(0).astype("int")
    df = df[
        [WEIGHT_IN_GRAMS_COLUMN, WEIGHT_IN_GRAMS_7D_COLUMN, WEIGHT_IN_GRAMS_14D_COLUMN]
    ]
    df = df.reset_index()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
    return df


def process():
    with open(RAW_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    df_weight_data = process_weight_data(data)
    df_daily_data = process_daily_data(df_weight_data.copy())
    df_weekly_data = process_weekly_data(df_weight_data.copy())

    print("weight today", df_daily_data[WEIGHT_IN_GRAMS_COLUMN].iloc[-1])

    daily_weight_forecaster = DailyWeightForecaster(
        df_daily=df_daily_data.copy(), df_weekly=df_weekly_data.copy()
    )
    remaining_days_weight = daily_weight_forecaster.calculate()

    print(remaining_days_weight.to_string())
    print("target weight this week", df_weekly_data["target_weight_7d"].iloc[-1])

    plot_figures(
        df_daily=df_daily_data.copy(),
        df=df_weekly_data.copy(),
        remaining_days_weight=remaining_days_weight.copy(),
    )


if __name__ == "__main__":
    process()
