# polynomial_compare_run.py
import numpy as np
import pandas as pd
from scipy import stats

# ----- INPUTS -----
# primary (same) 20 inputs you used earlier:
x_same = np.array([-10, -7, -5, -2, -1, -0.75, -0.25, -0.0001, 0, 0.25,
                   0.5, 1, 2, 3.1416, 7, 10, 50, 100, -50, -100], dtype=float)

# extra random reproducible set
np.random.seed(2025)
x_rand = np.round(np.random.uniform(-200, 200, 20), 6)

# choose which sets to run
datasets = {"same": x_same, "random_extra": x_rand}

# ----- POLYNOMIALS -----
def quadratic(x, a=1, b=0, c=0):   # ax^2 + bx + c
    return a*x**2 + b*x + c

def cubic(x, a=1, b=0, c=0, d=0): # ax^3 + bx^2 + cx + d
    return a*x**3 + b*x**2 + c*x + d

def quartic(x, a=1, b=0, c=0, d=0, e=0): # ax^4 + ...
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

polys = {"Quadratic": quadratic, "Cubic": cubic, "Quartic": quartic}

# offsets to test
offsets = [0.0, 0.1]

# ----- COLLECT RAW DATA -----
rows = []
for ds_name, xvals in datasets.items():
    for fname, f in polys.items():
        for offset in offsets:
            for x in xvals:
                y0 = f(x)
                y1 = f(x + offset)
                D = y1 - y0
                rows.append({"dataset": ds_name, "Function": fname, "Offset": offset, "x0": x, "y0": y0, "y1": y1, "D": D})
df = pd.DataFrame(rows)

# Save raw for appendix
df.to_csv("polynomial_D_raw.csv", index=False)

# ----- SUMMARY (mean/std) -----
summary = df.groupby(["dataset","Function","Offset"])["D"].agg(["mean","std","count"]).reset_index()
summary.to_csv("polynomial_summary.csv", index=False)

# ----- PAIRED TESTS: For each dataset, compare functions (repeated measures) -----
# Example: one-way repeated-like ANOVA using scipy: we can do a simple F-test across paired samples
# For simplicity: do Friedman test (non-parametric) across the three polys for each offset within each dataset
from scipy.stats import friedmanchisquare

friedman_results = []
for ds_name, xvals in datasets.items():
    for offset in offsets:
        # build arrays: each column is D for a polynomial across same x values (paired)
        quad_D = df[(df.dataset==ds_name) & (df.Function=="Quadratic") & (df.Offset==offset)]["D"].values
        cubic_D = df[(df.dataset==ds_name) & (df.Function=="Cubic") & (df.Offset==offset)]["D"].values
        quart_D = df[(df.dataset==ds_name) & (df.Function=="Quartic") & (df.Offset==offset)]["D"].values
        # if distributions length > 0 and equal
        if len(quad_D)>1:
            stat, p = friedmanchisquare(quad_D, cubic_D, quart_D)
        else:
            stat, p = np.nan, np.nan
        friedman_results.append({"dataset": ds_name, "offset": offset, "friedman_stat": stat, "p_value": p})
friedman_df = pd.DataFrame(friedman_results)
friedman_df.to_csv("polynomial_friedman.csv", index=False)

# ----- pairwise paired t-tests between polynomials for each dataset/offset (with Bonferroni) -----
pairs = [("Quadratic","Cubic"), ("Quadratic","Quartic"), ("Cubic","Quartic")]
pairwise_rows = []
for ds_name in datasets.keys():
    for offset in offsets:
        for (a,b) in pairs:
            Da = df[(df.dataset==ds_name)&(df.Function==a)&(df.Offset==offset)]["D"].values
            Db = df[(df.dataset==ds_name)&(df.Function==b)&(df.Offset==offset)]["D"].values
            # paired t-test (same x0 ordering)
            t_stat, p_val = stats.ttest_rel(Da, Db)
            pairwise_rows.append({"dataset": ds_name, "offset": offset, "pair": f"{a} vs {b}", "t_stat": t_stat, "p_value": p_val})
pairwise_df = pd.DataFrame(pairwise_rows)
# Bonferroni correction for 3 comparisons: multiply p by 3
pairwise_df["p_bonf"] = np.minimum(pairwise_df["p_value"]*3, 1.0)
pairwise_df.to_csv("polynomial_pairwise_paired_ttests.csv", index=False)

print("Done. Files saved: polynomial_D_raw.csv, polynomial_summary.csv, polynomial_friedman.csv, polynomial_pairwise_paired_ttests.csv")