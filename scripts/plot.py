import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

df = pd.read_csv("weight.csv")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly", marker='o', ax=ax, label="14d Weekly")
line_14d = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_14d_weekly"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_14d.get_color())

sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly", marker='o', ax=ax, label="7d Weekly")
line_7d = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_7d_weekly"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_7d.get_color())

# save the plot
fig.savefig("weight.png")

# plot the weekly change separately

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly_change", marker='o', ax=ax, label="14d Weekly Change")
line_14d_change = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_14d_weekly_change"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_14d_change.get_color())

sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly_change", marker='o', ax=ax, label="7d Weekly Change")
line_7d_change = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_7d_weekly_change"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_7d_change.get_color())
    
# add horizontal line at optimal weekly rate (load from environment variable, TARGET_WEEKLY_CHANGE_IN_GRAMS)
target_weekly_change = int(os.getenv("TARGET_WEEKLY_CHANGE_IN_GRAMS", 0))
ax.axhline(y=target_weekly_change, color='r', linestyle='--', label="Target Weekly Change")
# add text
ax.text(df["date"].iloc[-1], target_weekly_change, target_weekly_change, ha="left", va="bottom", color="r")

# save the plot
fig.savefig("weight_change.png")
