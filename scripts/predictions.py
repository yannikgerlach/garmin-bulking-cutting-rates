import numpy as np
import pandas as pd

from scripts.columns import (
    DATE_COLUMN,
    WEIGHT_IN_GRAMS_7D_COLUMN,
    WEIGHT_IN_GRAMS_COLUMN,
)
from scripts.files import DAILY_DATA_FILE, WEEKLY_DATA_FILE


class DailyWeightForecaster:
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self._df_daily = None
        self._df_weekly = None

    def calculate(self) -> pd.DataFrame:
        if self._df_daily is None or self._df_weekly is None:
            self._load_daily_weekly_data()

        target_this_week = self._df_weekly.tail(1)
        target_this_week_weight = target_this_week["target_weight_7d"].values[0]

        remaining_days_this_week = self._get_remaining_days_this_week(
            target_this_week=target_this_week
        )
        passed_days_this_week = 7 - remaining_days_this_week

        raw_data_weight_first_days = self._df_daily[WEIGHT_IN_GRAMS_COLUMN].tail(
            passed_days_this_week
        )

        # method max(3, passed_days_this_week)
        if passed_days_this_week < 3:
            number_of_days_to_look_back = 3
            interpolation_method = "quadratic"
        else:
            number_of_days_to_look_back = passed_days_this_week
            interpolation_method = "barycentric"

        last_7d_weights = (
            self._df_daily[WEIGHT_IN_GRAMS_COLUMN]
            .tail(number_of_days_to_look_back)
            .values.tolist()
        )
        # how many days to look back
        number_of_last_weeks_days = max(
            0, number_of_days_to_look_back - passed_days_this_week
        )
        raw_weight_last_days = last_7d_weights[:number_of_last_weeks_days]
        target_weight_sum_with_last_days = target_this_week_weight * 7 + sum(
            raw_weight_last_days
        )

        # interpolate using pandas on the sums
        interpolate_df = pd.DataFrame()
        interpolate_df["weight"] = (
            np.cumsum(last_7d_weights).tolist()
            + (remaining_days_this_week - 1) * [np.nan]
            + [float(target_weight_sum_with_last_days)]
        )
        remaining_days_weight = (
            interpolate_df["weight"]
            .interpolate(method=interpolation_method)
            .diff()
            .tail(remaining_days_this_week)
        )

        remaining_days_weight = remaining_days_weight.reset_index(drop=True)

        self._add_date_to_remaining_days_weight(
            remaining_days_weight=remaining_days_weight,
        )

        self._check_correctness(
            target_this_week_weight=target_this_week_weight,
            remaining_days_weight=remaining_days_weight,
            raw_data_weight_first_days=raw_data_weight_first_days,
        )

        return remaining_days_weight

    def _load_daily_weekly_data(self):
        self._df_daily = pd.read_csv(DAILY_DATA_FILE)
        self._df_daily[DATE_COLUMN] = pd.to_datetime(self._df_daily[DATE_COLUMN])

        self._df_weekly = pd.read_csv(WEEKLY_DATA_FILE)
        self._df_weekly[DATE_COLUMN] = pd.to_datetime(self._df_weekly[DATE_COLUMN])

    def _get_remaining_days_this_week(self, target_this_week: pd.DataFrame) -> int:
        assert self._df_daily is not None

        target_this_week_day = target_this_week[DATE_COLUMN].values[0]
        most_recent_reading_date = self._df_daily[DATE_COLUMN].max()
        return (target_this_week_day - most_recent_reading_date).days

    def _add_date_to_remaining_days_weight(
        self, remaining_days_weight: pd.DataFrame
    ) -> None:
        """
        Add the dates to the remaining days weight values.
        """
        remaining_days_this_week = len(remaining_days_weight)

        df_7d_last = (
            self._df_daily[self._df_daily[WEIGHT_IN_GRAMS_7D_COLUMN] != 0][
                [DATE_COLUMN, WEIGHT_IN_GRAMS_7D_COLUMN]
            ]
            .tail(1)
            .copy()
        )

        remaining_days_weight.index = df_7d_last[DATE_COLUMN].values[
            0
        ] + pd.to_timedelta(np.arange(1, remaining_days_this_week + 1), unit="D")

    def _check_correctness(
        self, target_this_week_weight, remaining_days_weight, raw_data_weight_first_days
    ):
        """
        Check correctness of the calculation by comparing the average
        of the targeted weights with the target weight for this week.
        """
        targeted_weights_this_week = (
            raw_data_weight_first_days.values.tolist()
            + remaining_days_weight.values.tolist()
        )
        average_targeted_weight_this_week = (
            np.mean(targeted_weights_this_week).round().astype(int)
        )
        if average_targeted_weight_this_week == target_this_week_weight:
            print("Correctly calculated the target weight for this week")
        else:
            print(
                "Error in calculating the target weight for this week: ",
                average_targeted_weight_this_week,
                target_this_week_weight,
            )
