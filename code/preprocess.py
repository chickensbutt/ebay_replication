# Step 1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data
df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# Step 2
treated = df[df["search_stays_on"] == 0].copy()
untreated = df[df["search_stays_on"] == 1].copy()

treated_pivot = (
	treated.pivot_table(
		index = "dma",
		columns = "treatment_period",
		values = "log_revenue",
		aggfunc = "mean"
	)
	.rename(columns={0: "log_revenue_pre", 1: "log_revenue_post"})
	.reset_index()
)
treated_pivot["log_revenue_diff"] = (
	treated_pivot["log_revenue_post"] - treated_pivot["log_revenue_pre"]
)

untreated_pivot = (
	untreated.pivot_table(
		index = "dma",
		columns = "treatment_period",
		values = "log_revenue",
		aggfunc = "mean",
	)
	.rename(columns={0: "log_revenue_pre", 1: "log_revenue_post"})
	.reset_index()
)
untreated_pivot["log_revenue_diff"] = (
	untreated_pivot["log_revenue_post"] - untreated_pivot["log_revenue_pre"]
)

treated_pivot.to_csv("temp/treated_pivot.csv", index = False)
untreated_pivot.to_csv("temp/untreated_pivot.csv", index = False)

# Step 3
treated_dmas = treated["dma"].nunique()
untreated_dmas = untreated["dma"].nunique()
date_min = df["date"].min().date()
date_max = df["date"].max().date()

print(f"Treated DMAs: {treated_dmas}")
print(f"Untreated DMAs: {untreated_dmas}")
print(f"Date range: {date_min} to {date_max}")

# Step  4
daily_rev = (
	df.groupby(["date", "search_stays_on"], as_index = False)["revenue"]
	.mean()
	.sort_values("date")
)

control_rev = daily_rev[daily_rev["search_stays_on"] == 1]
treat_rev = daily_rev[daily_rev["search_stays_on"] == 0]

fig, ax = plt.subplots(figsize=(9,3))

ax.plot(control_rev["date"], control_rev["revenue"], linewidth=1.5)
ax.plot(treat_rev["date"], treat_rev["revenue"], linewidth=1.5)

ax.axvline(pd.Timestamp("2012-05-22"), linestyle="--", linewidth=1)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

ax.set_xlabel("")
ax.set_ylabel("revenue")

ax.text(control_rev["date"].iloc[-1], control_rev["revenue"].iloc[-1],
	"control\n(search stays on)", va="center", ha="left")
ax.text(treat_rev["date"].iloc[-1], treat_rev["revenue"].iloc[-1],
	"treatment\n(search goes off)", va="center", ha="left")
ax.set_xlim(df["date"].min(), df["date"].max() + pd.Timedelta(days=5))

fig.tight_layout()
fig.savefig("output/figures/figure_5_2.png", dpi=300)
plt.close(fig)

# Step 5
daily_rev = (
	df.groupby(["date", "search_stays_on"], as_index=False)["revenue"]
	.sum()
	.sort_values("date")
)

daily_pivot = daily_rev.pivot(
	index = "date",
	columns="search_stays_on",
	values="revenue"
)

daily_pivot["log_diff"] = np.log(daily_pivot[1]) - np.log(daily_pivot[0])

plt.figure(figsize=(9,3))
plt.plot(daily_pivot.index, daily_pivot["log_diff"], linewidth=1.5)
plt.axvline(pd.Timestamp("2012-05-22"), linestyle = "--", linewidth=1)

plt.xlabel("")
plt.ylabel("log(rev_control) - log(rev_treat)")
plt.title("Log Revenue Gap Over Time (Control - Treatment)")

plt.tight_layout()
plt.savefig("output/figures/figure_5_3.png", dpi=300)
plt.close()
