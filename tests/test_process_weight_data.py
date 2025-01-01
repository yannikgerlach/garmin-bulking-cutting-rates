import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from scripts.process_weight_data import add_moving_average_and_change
from scripts.process_weight_data import add_moving_average_and_change, process_weight_data
from scripts.process_weight_data import add_moving_average_and_change, process_weight_data, add_target_weight_change
import os

class TestAddMovingAverageAndChange(unittest.TestCase):
    def setUp(self):
        data = {
            "date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
            "weight_in_grams": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
        }
        self.df = pd.DataFrame(data)
        self.df.set_index("date", inplace=True)

    def test_add_moving_average_and_change_7d(self):
        expected_df = self.df.copy()
        expected_df["weight_in_grams_7d"] = expected_df["weight_in_grams"].rolling(window=7).mean()
        expected_df["weight_in_grams_7d_weekly"] = expected_df["weight_in_grams_7d"].resample("W").last()
        expected_df["weight_in_grams_7d_weekly_change"] = expected_df["weight_in_grams_7d_weekly"].diff(periods=7)

        add_moving_average_and_change(self.df, "weight_in_grams", 7)
        assert_frame_equal(self.df, expected_df)

    def test_add_moving_average_and_change_14d(self):
        expected_df = self.df.copy()
        expected_df["weight_in_grams_14d"] = expected_df["weight_in_grams"].rolling(window=14).mean()
        expected_df["weight_in_grams_14d_weekly"] = expected_df["weight_in_grams_14d"].resample("W").last()
        expected_df["weight_in_grams_14d_weekly_change"] = expected_df["weight_in_grams_14d_weekly"].diff(periods=7)

        add_moving_average_and_change(self.df, "weight_in_grams", 14)
        assert_frame_equal(self.df, expected_df)

class TestProcessWeightData(unittest.TestCase):
    def test_process_weight_data(self):
        data = {
            "dailyWeightSummaries": [
                {"summaryDate": "2023-01-01", "allWeightMetrics": [{"weight": 70}]},
                {"summaryDate": "2023-01-02", "allWeightMetrics": [{"weight": 71}]},
                {"summaryDate": "2023-01-03", "allWeightMetrics": [{"weight": 72}]},
                {"summaryDate": "2023-01-04", "allWeightMetrics": [{"weight": 73}]},
                {"summaryDate": "2023-01-05", "allWeightMetrics": [{"weight": 74}]},
                {"summaryDate": "2023-01-06", "allWeightMetrics": [{"weight": 75}]},
                {"summaryDate": "2023-01-07", "allWeightMetrics": [{"weight": 76}]},
                {"summaryDate": "2023-01-08", "allWeightMetrics": [{"weight": 77}]},
                {"summaryDate": "2023-01-09", "allWeightMetrics": [{"weight": 78}]},
                {"summaryDate": "2023-01-10", "allWeightMetrics": [{"weight": 79}]},
                {"summaryDate": "2023-01-11", "allWeightMetrics": [{"weight": 80}]},
                {"summaryDate": "2023-01-12", "allWeightMetrics": [{"weight": 81}]},
                {"summaryDate": "2023-01-13", "allWeightMetrics": [{"weight": 82}]},
                {"summaryDate": "2023-01-14", "allWeightMetrics": [{"weight": 83}]},
                {"summaryDate": "2023-01-15", "allWeightMetrics": [{"weight": 84}]},
                {"summaryDate": "2023-01-16", "allWeightMetrics": [{"weight": 85}]},
                {"summaryDate": "2023-01-17", "allWeightMetrics": [{"weight": 86}]},
                {"summaryDate": "2023-01-18", "allWeightMetrics": [{"weight": 87}]},
                {"summaryDate": "2023-01-19", "allWeightMetrics": [{"weight": 88}]},
                {"summaryDate": "2023-01-20", "allWeightMetrics": [{"weight": 89}]},
                {"summaryDate": "2023-01-21", "allWeightMetrics": [{"weight": 90}]},
                {"summaryDate": "2023-01-22", "allWeightMetrics": [{"weight": 91}]},
                {"summaryDate": "2023-01-23", "allWeightMetrics": [{"weight": 92}]},
                {"summaryDate": "2023-01-24", "allWeightMetrics": [{"weight": 93}]},
                {"summaryDate": "2023-01-25", "allWeightMetrics": [{"weight": 94}]},
                {"summaryDate": "2023-01-26", "allWeightMetrics": [{"weight": 95}]},
                {"summaryDate": "2023-01-27", "allWeightMetrics": [{"weight": 96}]},
                {"summaryDate": "2023-01-28", "allWeightMetrics": [{"weight": 97}]},
                {"summaryDate": "2023-01-29", "allWeightMetrics": [{"weight": 98}]},
                {"summaryDate": "2023-01-30", "allWeightMetrics": [{"weight": 99}]}
            ]
        }

        # data only becomes meaningful after 14 days
        expected_data = {
            "weight_in_grams_7d_weekly": [88, 95],
            "weight_in_grams_7d_weekly_change": [7, 7],
            "weight_in_grams_14d_weekly": [84, 91],
            "weight_in_grams_14d_weekly_change": [7, 7]
        }
        expected_df = pd.DataFrame(expected_data, index=pd.to_datetime(["2023-01-22", "2023-01-29"])).astype("int64")

        result_df = process_weight_data(data)
        assert_frame_equal(result_df, expected_df, check_freq=False, check_names=False)

class TestAddTargetWeightChange(unittest.TestCase):
    def setUp(self):
        data = {
            "date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
            "weight_in_grams_14d_weekly": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
        }
        self.df = pd.DataFrame(data)
        self.df.set_index("date", inplace=True)

    def test_add_target_weight_change(self):
        os.environ["TARGET_WEEKLY_CHANGE_PERCENTAGE"] = "0.05"  # 5% change
        
        expected_target_weight_change = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5] 
        expected_target_weight = [70, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103]

        assert "target_weight_change" not in self.df.columns
        assert "target_weight" not in self.df.columns
        
        result_df = add_target_weight_change(self.df)
        
        assert "target_weight_change" in result_df.columns
        assert "target_weight" in result_df.columns
        
        assert result_df["target_weight_change"].tolist() == expected_target_weight_change
        assert result_df["target_weight"].tolist() == expected_target_weight
