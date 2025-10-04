#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd

# ------------------------------
# Step 1: Setup
# ------------------------------
functions = ["Linear", "Polynomial", "ReLU", "Sine", "Gaussian", "tanh"]
means = [0.1, 3.499915, 0.054995, 0.077602, 0.022063, 0.031218]
std_dev = 0.01   # small random noise
n_samples = 5    # number of samples per function

# Generate random samples for each function
samples = [np.random.normal(loc=m, scale=std_dev, size=n_samples) for m in means]

# ------------------------------
# Step 2: Define Cohen's d
# ------------------------------
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(
        ((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / (nx+ny-2)
    )
    return (np.mean(x) - np.mean(y)) / pooled_std

# ------------------------------
# Step 3: Pairwise Comparisons
# ------------------------------
results = []
for i in range(len(functions)):
    for j in range(i+1, len(functions)):
        d = cohens_d(samples[i], samples[j])
        results.append({
            "Function 1": functions[i],
            "Function 2": functions[j],
            "Cohen_d": round(d, 4)
        })

df = pd.DataFrame(results)

# ------------------------------
# Step 4: Save/Append to CSV
# ------------------------------
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "cohens_d.csv")

if os.path.exists(csv_path):
    # Append without rewriting headers
    df.to_csv(csv_path, mode="a", header=False, index=False)
else:
    df.to_csv(csv_path, index=False)

print(f"Cohen's d results saved to: {csv_path}")
print(df)