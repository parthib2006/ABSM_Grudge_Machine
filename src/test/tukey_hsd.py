import numpy as np
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Example data: Replace with your actual D values
functions = ["Linear", "Polynomial", "ReLU", "Sine", "Gaussian", "tanh"]
offsets = ["Zero", "NonZero"]

# Random demo data (replace with actual D values)
np.random.seed(0)
data = {f: {o: np.random.normal(loc=np.random.rand(), scale=0.01, size=5) for o in offsets} for f in functions}

# Prepare long-format DataFrame
records = []
for f in functions:
    for o in offsets:
        for val in data[f][o]:
            records.append([f + "_" + o, val])  # Group by function + offset
df = pd.DataFrame(records, columns=["Group", "Value"])

# Run Tukey's HSD
tukey = pairwise_tukeyhsd(endog=df["Value"], groups=df["Group"], alpha=0.05)

# Convert results to DataFrame
tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])

# Save to CSV
tukey_df.to_csv("results/tukey_hsd_results.csv", index=False)

print("Tukey HSD results saved to 'results/tukey_hsd_results.csv'")
print(tukey_df)