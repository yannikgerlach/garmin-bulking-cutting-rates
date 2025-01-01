import json
import pandas as pd
from scripts.process_weight_data import add_target_weight_change, process_weight_data


data = json.load(open("weight_raw.json"))

df = process_weight_data(data)

df = pd.concat([df, pd.DataFrame(index=pd.date_range(df.index[-1] + pd.DateOffset(days=1), periods=1, freq="W", name="date"))])

df = add_target_weight_change(df, window=14)
df = add_target_weight_change(df, window=7)

df = df.fillna(0).astype("int")

df.to_csv("weight.csv")
