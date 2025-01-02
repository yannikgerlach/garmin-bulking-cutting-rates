import json

import pandas as pd

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_14D_COLUMN,
    WEIGHT_IN_GRAMS_COLUMN,
)
from scripts.files import DAILY_DATA_FILE, RAW_DATA_FILE, WEEKLY_DATA_FILE
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

    return df_weekly.fillna(0).astype("int")


def process_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(0).astype("int")
    return df[
        [WEIGHT_IN_GRAMS_COLUMN, WEIGHT_IN_GRAMS_7D_COLUMN, WEIGHT_IN_GRAMS_14D_COLUMN]
    ]


with open(RAW_DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
    df_weight_data = process_weight_data(data)

    df_daily_data = process_daily_data(df_weight_data)
    df_daily_data.to_csv(DAILY_DATA_FILE)

    df_weekly_data = process_weekly_data(df_weight_data)
    df_weekly_data.to_csv(WEEKLY_DATA_FILE)
