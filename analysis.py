from datetime import date
import os
import pandas as pd

import garminconnect


garmin = garminconnect.Garmin(os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD"))
garmin.login()

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)


startdate = date(2024, 11, 1)
startdate = startdate.isoformat()

enddate = date.today()
enddate = enddate.isoformat()

data = garmin.get_weigh_ins(startdate, enddate)
assert data is not None

data_weight = data["dailyWeightSummaries"]
daily_weights = [(d["summaryDate"], d["allWeightMetrics"][0]["weight"]) for d in data_weight]
df = pd.DataFrame(daily_weights, columns=["date", "weight_in_grams"])

# fill in missing dates
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df = df.resample("D").asfreq()
df["weight_in_grams"] = df["weight_in_grams"].interpolate(method="pad")


def add_moving_average_and_change(df: pd.DataFrame, column: str, window: int):
    df[f"{column}_{window}d"] = df[column].rolling(window=window).mean().round(0)
    df[f"{column}_{window}d_weekly"] = df[f"{column}_{window}d"].resample("W").last()
    df[f"{column}_{window}d_weekly_change"] = df[f"{column}_{window}d_weekly"].diff(periods=7).round(0)
    
    
add_moving_average_and_change(df=df, column="weight_in_grams", window=7)
add_moving_average_and_change(df=df, column="weight_in_grams", window=14)

# remove weight in grams columns
df = df.drop(columns=["weight_in_grams", "weight_in_grams_7d", "weight_in_grams_14d"])

# only show the rows where the weekly change is not null
df = df[df["weight_in_grams_14d_weekly_change"].notnull()]
print(df)

df.to_csv("weight.csv")
