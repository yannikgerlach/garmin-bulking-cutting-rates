import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("weight.csv")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly", ax=ax)
sns.lineplot(data=df, x="date", y="weight_in_grams_14d_weekly_change", ax=ax)
sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly", ax=ax)
sns.lineplot(data=df, x="date", y="weight_in_grams_7d_weekly_change", ax=ax)

plt.show()
