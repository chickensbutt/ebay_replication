# did_analysis.py
# Computes the difference-in-differences estimate for the eBay paid search experiment.
# Method: Compare pre-post log revenue changes between treatment and control DMAs. 
# Reference: Blake et al. (2014), Taddy Ch. 5

import pandas as pd
import numpy as np

# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

r1 = np.mean(treated_pivot['log_revenue_diff'])
r0 = np.mean(untreated_pivot['log_revenue_diff'])

gam = r1 - r0

se = np.sqrt(np.var(treated_pivot['log_revenue_diff'], ddof=1)/len(treated_pivot) + np.var(untreated_pivot['log_revenue_diff'], ddof=1)/len(untreated_pivot))

ci = [gam - 1.96*se, gam + 1.96*se]

gamma_hat = gam
ci_lower, ci_upper = ci[0], ci[1]

print("Difference-in-Differences Estimate")
print("----------------------------------")
print("----------------------------------")
print(f"Gamma hat: {gam:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
 & Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open('output/tables/did_table.tex', 'w') as f:
	f.write(latex)
