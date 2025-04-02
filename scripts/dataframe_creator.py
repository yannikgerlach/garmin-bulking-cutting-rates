import json
from abc import abstractmethod
from typing import Protocol

import pandas as pd

from scripts.columns import DATE_COLUMN, WEIGHT_IN_GRAMS_COLUMN
from scripts.files import RAW_DATA_FILE


class WeightDataFrameCreator(Protocol):
    # pylint: disable=too-few-public-methods
    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        """
        Return a DataFrame with daily weight measurements.

        Returns:
        pd.DataFrame
            A DataFrame containing daily weight data where:
            - DATE_COLUMN is used as the datetime index
            - WEIGHT_IN_GRAMS_COLUMN contains integer weight values in grams
            - Data includes exactly one row per day with no missing values
        """


class GarminWeightDataFrameCreator(WeightDataFrameCreator):
    # pylint: disable=too-few-public-methods
    """
    Takes the weight of the first weight measurement of each day and rounds it to the nearest integer.
    Loads the raw data from a local JSON file.

    This function expects a dictionary containing a "dailyWeightSummaries" key, where each item includes:
     - "summaryDate": A string representing the date.
     - "allWeightMetrics": A list of dictionaries with a "weight" key, specifying weight in grams.
    """

    def get_dataframe(self) -> pd.DataFrame:
        data = self._load_data()
        daily_weights = [
            (d["summaryDate"], round(d["allWeightMetrics"][0]["weight"]))
            for d in data["dailyWeightSummaries"]
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

    def _load_data(self) -> dict:
        with open(RAW_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
