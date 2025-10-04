import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("absm_results.csv")

# Unique functions
functions = df['function'].unique()

# Plot x0 vs x1 for each function
plt.figure(figsize=(12,6))
for f in functions:
    subset = df[df['function'] == f]
    plt.plot(subset['x0'], subset['x1'], marker='o', label=f)
plt.xlabel('x0 (Input)')
plt.ylabel('x1 (Output)')
plt.title('ABSM: x0 vs x1 for each Activation Function')
plt.legend()
plt.grid(True)
plt.savefig("absm_data")
plt.show()