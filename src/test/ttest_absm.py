#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
from scipy import stats

# ------------------------------
# Step 1: Setup
# ------------------------------
functions = ["Linear", "Polynomial", "ReLU", "Sine", "Gaussian", "tanh"]
offsets = ["Zero", "NonZero"]

# Example synthetic data (replace with your real D values if available)
np.random.seed(42)
data = {f: {
            "Zero": np.random.normal(loc=0, scale=0.01, size=20),
            "NonZero": np.random.normal(loc=np.random.rand()*3, scale=0.05, size=20)
         } for f in functions}

# ------------------------------
# Step 2: Perform Paired T-tests
# ------------------------------
results = []
for f in functions:
    group1 = data[f]["Zero"]
    group2 = data[f]["NonZero"]

    # t-test
    t_stat, p_val = stats.ttest_rel(group1, group2)

    # mean difference
    mean_diff = np.mean(group2) - np.mean(group1)

    results.append([f, mean_diff, t_stat, p_val])

# ------------------------------
# Step 3: Build Results Table
# ------------------------------
ttest_table = pd.DataFrame(
    results, 
    columns=["Function", "Mean_Difference", "t_stat", "p_value"]
)

# Round for readability
ttest_table["Mean_Difference"] = ttest_table["Mean_Difference"].round(6)
ttest_table["t_stat"] = ttest_table["t_stat"].round(6)
ttest_table["p_value"] = ttest_table["p_value"].apply(lambda x: f"{x:.2e}")

# ------------------------------
# Step 4: Save Results
# ------------------------------
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "ttest_results.csv")

# Save / Append to CSV
if os.path.exists(csv_path):
    ttest_table.to_csv(csv_path, mode="a", header=False, index=False)
else:
    ttest_table.to_csv(csv_path, index=False)

# ------------------------------
# Step 5: Print Results
# ------------------------------
print("\nPaired T-Test Results (Zero vs NonZero Offset):")
print(ttest_table.to_string(index=False))
print(f"\nResults saved to: {csv_path}")