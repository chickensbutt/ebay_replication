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

# Step 4
daily_rev = (
	df.groupby(["date", "search_stays_on"], as_index = False)["revenue"]
	.mean()
	.sort_values("date")
)

control_rev = daily_rev[daily_rev["search_stays_on"] == 1]
treat_rev = daily_rev[daily_rev["search_stays_on"] == 0]

plt.figure()
plt.plot(control_rev["date"], control_rev["revenue"], label = "Control (search stays on)")
plt.plot(treat_rev["date"], treat_rev["revenue"], label = "Treatment (search goes off")
plt.axvline(pd.Timestamp("2012-05-22"), linestyle = "--")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Average Revenue Over Time: Control vs Treatment")
plt.legend()
plt.xticks(fontsize = 0, rotation = 45)
plt.tight_layout()
plt.savefig("output/figures/figure_5_2.png", dpi=300)
plt.close()

# Step 5
daily_log = (
	df.groupby(["date", "search_stays_on"], as_index = False)["log_revenue"]
	.mean()
	.sort_values("date")
)


daily_log_pivot = daily_log.pivot(index = "date", columns = "search_stays_on", values = "log_revenue")

daily_log_pivot["log_diff"] = daily_log_pivot[1] - daily_log_pivot[0]

plt.figure()
plt.plot(daily_log_pivot.index, daily_log_pivot["log_diff"])
plt.axvline(pd.Timestamp("2022-05-22"), linestyle = "--")
plt.xlabel("Date")
plt.ylabel("log(rev_control) - log(rev_treat)")
plt.title("Log Revenue Gap Over Time (Control - Treatment)")
plt.xlim(daily_log_pivot.index.min(), daily_log_pivot.index.max())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.xticks(rotation=45, fontsize=8)
plt.tight_layout()
plt.savefig("output/figures/figure_5_3.png", dpi=300)
plt.close()
