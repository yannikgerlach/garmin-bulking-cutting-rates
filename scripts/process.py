import json
import pandas as pd
from scripts.process_weight_data import add_target_weight_change, filter_df_to_weekly_changes, process_weight_data


data = json.load(open("weight_raw.json"))

df = process_weight_data(data)
df_weekly = filter_df_to_weekly_changes(df)

df_weekly = pd.concat([df_weekly, pd.DataFrame(index=pd.date_range(df_weekly.index[-1] + pd.DateOffset(days=1), periods=1, freq="W", name="date"))])

df_weekly = add_target_weight_change(df_weekly, window=14)
df_weekly = add_target_weight_change(df_weekly, window=7)

df_weekly = df_weekly.fillna(0).astype("int")
df_weekly.to_csv("weight.csv")

df = df.fillna(0).astype("int")
# only keep "weight_in_grams", "weight_in_grams_7d", "weight_in_grams_14d" columns
df = df[["weight_in_grams", "weight_in_grams_7d", "weight_in_grams_14d"]]
df.to_csv("weight_daily.csv")


