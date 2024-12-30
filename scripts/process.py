import json

from scripts.process_weight_data import process_weight_data


data = json.load(open("weight_raw.json"))
df = process_weight_data(data)
df.to_csv("weight.csv")
