import json

from scripts.process_weight_data import add_target_weight_change, process_weight_data


data = json.load(open("weight_raw.json"))

df = process_weight_data(data)
df = add_target_weight_change(df)

df.to_csv("weight.csv")
