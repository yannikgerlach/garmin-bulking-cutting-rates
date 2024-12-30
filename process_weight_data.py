import pandas as pd
import json

data = json.load(open("weight_raw.json"))

data_weight = data["dailyWeightSummaries"]
daily_weights = [(d["summaryDate"], round(d["allWeightMetrics"][0]["weight"])) for d in data_weight]
df = pd.DataFrame(daily_weights, columns=["date", "weight_in_grams"])

# fill in missing dates
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df = df.resample("D").asfreq()
df["weight_in_grams"] = df["weight_in_grams"].interpolate(method="pad").astype(int)


def add_moving_average_and_change(df: pd.DataFrame, column: str, window: int):
    df[f"{column}_{window}d"] = df[column].rolling(window=window).mean()
    df[f"{column}_{window}d_weekly"] = df[f"{column}_{window}d"].resample("W").last()
    df[f"{column}_{window}d_weekly_change"] = df[f"{column}_{window}d_weekly"].diff(periods=7)
    
    
add_moving_average_and_change(df=df, column="weight_in_grams", window=7)
add_moving_average_and_change(df=df, column="weight_in_grams", window=14)

# remove weight in grams columns
df = df.drop(columns=["weight_in_grams", "weight_in_grams_7d", "weight_in_grams_14d"])

# only show the rows where the weekly change is not null
df = df[df["weight_in_grams_14d_weekly_change"].notnull()]
df = df.astype(int)

df.to_csv("weight.csv")
