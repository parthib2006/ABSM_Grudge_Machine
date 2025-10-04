# abs_model_experiment.py
import numpy as np
import pandas as pd
from math import exp, sin, tanh
from scipy import integrate, stats

# --- Activation functions ---
def linear(x): return x
def polynomial(x): return x**3 - 0.5*x**2 + 0.2*x  # example cubic polynomial
def relu(x): return x if x > 0 else 0
def sine(x): return sin(x)
def gaussian(x, sigma=1.0): return np.exp(-x**2 / (2 * sigma**2))
def tanh_fn(x): return tanh(x)

# Map names to functions
FUNCTIONS = {
    "Linear": linear,
    "Polynomial": polynomial,
    "ReLU": relu,
    "Sine": sine,
    "Gaussian": gaussian,
    "Tanh": tanh_fn
}

# --- x0 values (20) ---
x_values = [1, 2, 5, -1, -2, -5, 0.5, 0.25, -0.75, 3.1416, 1.4142, -2.7183,
            100, -100, 0.0001, -0.0001, 10, -10, 7, -7]

# --- Offsets experiment choices ---
# You can run multiple experiments with different (n0,n1) pairs
offset_sets = [
    (0.0, 0.0),      # baseline
    (0.2, -0.1)      # small offsets
]

rows = []
for (n0, n1) in offset_sets:
    n_prime = (n0 + n1) / 2.0
    experiment_label = f"n0={n0},n1={n1}"
    for fname, f in FUNCTIONS.items():
        for x0 in x_values:
            # compute x1 = f(x0)
            # gaussian signature: gaussian(x) defined above
            if fname == "Gaussian":
                x1 = gaussian(x0, sigma=1.0)
            else:
                x1 = f(x0)
            # define integrand P(x) -- we will use same function as "P"
            def P(x):
                if fname == "Gaussian":
                    return gaussian(x, sigma=1.0)
                return f(x)
            # numeric integral Q from x0 to x1
            # handle case where x0 == x1 -> integral zero
            try:
                Q_val = integrate.quad(P, x0, x1, limit=100)[0] if x0 != x1 else 0.0
            except Exception as e:
                Q_val = np.nan  # record NaN if integration fails
            n_val = n_prime + Q_val
            # compute deviation D = n*x1 + n0 - (n*x0 + n1)
            D_val = n_val * x1 + n0 - (n_val * x0 + n1)
            rows.append({
                "experiment": experiment_label,
                "x0": x0,
                "function": fname,
                "x1": x1,
                "n0": n0,
                "n1": n1,
                "n_prime": n_prime,
                "Q": Q_val,
                "n": n_val,
                "D": D_val,
                "abs_D": abs(D_val)
            })

df = pd.DataFrame(rows)

# Save full dataset
df.to_csv("absm_results.csv", index=False)

# --- Summary per function per experiment ---
summary = df.groupby(["experiment", "function"]).agg(
    count=("D","count"),
    mean_D=("D","mean"),
    std_D=("D","std"),
    mean_abs_D=("abs_D","mean")
).reset_index()
print("\nSummary (mean D, std D) per function and experiment:\n")
print(summary.to_string(index=False))

# --- Run one-sample t-test (mean(D) vs 0) per function per experiment ---
print("\nOne-sample t-test results (H0: mean(D) != 0) -- p-value shown\n")
ttest_results = []
for (exp_label, fname), group in df.groupby(["experiment", "function"]):
    Dvals = group["D"].dropna().values
    if len(Dvals) >= 2 and not np.isnan(Dvals).any():
        t_stat, p_val = stats.ttest_1samp(Dvals, 0.0, nan_policy='omit')
    else:
        t_stat, p_val = np.nan, np.nan
    ttest_results.append({
        "experiment": exp_label,
        "function": fname,
        "n_samples": len(Dvals),
        "t_stat": t_stat,
        "p_value": p_val,
        "mean_D": np.mean(Dvals) if len(Dvals)>0 else np.nan
    })

ttest_df = pd.DataFrame(ttest_results)
print(ttest_df.to_string(index=False))

# Save t-test results
ttest_df.to_csv("absm_ttest_results.csv", index=False)

print("\nFiles saved: absm_results.csv, absm_ttest_results.csv")