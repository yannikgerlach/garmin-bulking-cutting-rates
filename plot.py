import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("weight.csv")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly", marker='o', ax=ax, label="14d Weekly")
line_14d = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_14d_weekly"]):
    ax.text(x_val, y_val, f"{y_val:.1f}", ha="center", va="bottom", color=line_14d.get_color())

sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly", marker='o', ax=ax, label="7d Weekly")
line_7d = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_7d_weekly"]):
    ax.text(x_val, y_val, f"{y_val:.1f}", ha="center", va="bottom", color=line_7d.get_color())

# save the plot
fig.savefig("weight.png")

# plot the weekly change separately

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly_change", marker='o', ax=ax, label="7d Weekly Change")
line_7d_change = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_7d_weekly_change"]):
    ax.text(x_val, y_val, f"{y_val:.1f}", ha="center", va="bottom", color=line_7d_change.get_color())

sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly_change", marker='o', ax=ax, label="14d Weekly Change")
line_14d_change = ax.lines[-1]
for x_val, y_val in zip(df["date"], df["weight_in_grams_14d_weekly_change"]):
    ax.text(x_val, y_val, f"{y_val:.1f}", ha="center", va="bottom", color=line_14d_change.get_color())

# save the plot
fig.savefig("weight_change.png")
