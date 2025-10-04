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

# Example synthetic data (replace with your actual values if available)
np.random.seed(0)
data = {f: {o: np.random.randn(20) for o in offsets} for f in functions}

# Convert to long DataFrame
records = []
for f in functions:
    for o in offsets:
        for val in data[f][o]:
            records.append([f, o, val])
df = pd.DataFrame(records, columns=["Function", "Offset", "Value"])

# ------------------------------
# Step 2: Two-way ANOVA (manual calculation)
# ------------------------------
grand_mean = df["Value"].mean()

# Factor A (Function)
ss_func = sum([
    len(df[df["Function"]==f]) * (df[df["Function"]==f]["Value"].mean() - grand_mean)**2
    for f in functions
])

# Factor B (Offset)
ss_offset = sum([
    len(df[df["Offset"]==o]) * (df[df["Offset"]==o]["Value"].mean() - grand_mean)**2
    for o in offsets
])

# Interaction
ss_interaction = 0
for f in functions:
    for o in offsets:
        cell = df[(df["Function"]==f) & (df["Offset"]==o)]
        ss_interaction += len(cell) * (
            (cell["Value"].mean() - df[df["Function"]==f]["Value"].mean()
             - df[df["Offset"]==o]["Value"].mean() + grand_mean) ** 2
        )

# Within-group (residual)
ss_within = sum((df["Value"] - df.groupby(["Function","Offset"])["Value"].transform("mean"))**2)

# Degrees of freedom
df_func = len(functions)-1
df_offset = len(offsets)-1
df_inter = df_func * df_offset
df_within = len(df)- (len(functions)*len(offsets))

# Mean squares
ms_func = ss_func/df_func
ms_offset = ss_offset/df_offset
ms_inter = ss_interaction/df_inter
ms_within = ss_within/df_within

# F values
F_func = ms_func/ms_within
F_offset = ms_offset/ms_within
F_inter = ms_inter/ms_within

# p-values
p_func = 1-stats.f.cdf(F_func, df_func, df_within)
p_offset = 1-stats.f.cdf(F_offset, df_offset, df_within)
p_inter = 1-stats.f.cdf(F_inter, df_inter, df_within)

# ------------------------------
# Step 3: Build Results Table
# ------------------------------
anova_table = pd.DataFrame([
    ["Function Effect", F_func, p_func],
    ["Offset Effect",   F_offset, p_offset],
    ["Interaction",     F_inter, p_inter]
], columns=["Effect", "F_value", "p_value"])

# ------------------------------
# Step 4: Save Results
# ------------------------------
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "anova_results.csv")

# Save / Append to CSV
if os.path.exists(csv_path):
    anova_table.to_csv(csv_path, mode="a", header=False, index=False)
else:
    anova_table.to_csv(csv_path, index=False)

# ------------------------------
# Step 5: Print
# ------------------------------
print("\n Two-way ANOVA Results:")
print(anova_table.to_string(index=False))
print(f"\n Results saved to: {csv_path}")