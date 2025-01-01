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
    
# add target weight for each week (column target_weight) as points (without lines)
sns.scatterplot(data=df, x="date", y="target_weight", color="red", ax=ax, label="Target Weekly")
for x_val, y_val in zip(df["date"], df["target_weight"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color="red")

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
    
# add line plot for target weekly change (column target_weight_change)
sns.lineplot(data=df, x="date", y="target_weight_change", marker='o', ax=ax, label="Target Weekly Change", color="red")
line_target = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["target_weight_change"]):
    ax.text(x_val, y_val, y_val, ha="center", va="bottom", color=line_target.get_color())

# save the plot
fig.savefig("weight_change.png")
