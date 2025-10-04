# ABSM – Adaptive Basis Selection Model

🚀 ABSM is a novel model proposed to compare and analyze different mathematical basis functions 
(Linear, Polynomial, Sine, Gaussian, Tanh, ReLU, etc.) for performance consistency and deviation 
analysis in machine learning applications.

This repository contains:
- 📂 Source code implementations in multiple languages (Python, C, C++, Java, JavaScript).
- 📊 Experimental results and statistical tests (Cohen’s d, deviation analysis, etc.).
- 📑 Documentation and research paper draft.

---

## 📁 Repository Structure

```
ABSM/
├── documentation/ # Documentation
│ ├── ABSM_Report.pdf
| |___ ABSM_Paper.pdf
| |___ ABSM_Data.xlsx
|
├── data/ # Dataset
│ └── raw_inputs.csv
| |__ processed_outputs.csv
|
├── src/ # Source code
|_main/
│ ├── Python/
│ │ └── main.py
│ ├── C++/
│ │ └── main.cpp
│ ├── C/
│ │ └── main.c
│ ├── Java/
│ │ └── Main.java
│ └── JavaScript/
│ └── main.js
|
|_test/
| |__ttest_absm.py
| |__tukey_hsd.py
| |__polynomial_compare.py
| |__two_way_anova.py
| |__absm_data.py
| |__cohen_d.py
|
├── results/ # Output, csv, figures
│ └── absm/
| |__ anova_absm/
| | |__absm_results.csv
| |
| |__ cohen_d_absm/
| | |__cohen_d.csv
| |
| |__ polynomial_ABSM/
| | |__polynomial_D_raw.csv
| | |__polynomial_friedman.csv
| | |__polynomial_pairwise_paired.csv
| | |__polynomial_summary.csv
| |
| |__ttest_absm/
| | |__ttest_table.csv
| |
| |__tukey_hsd_ABSM/
| | |__tukey_hsd.csv
| |
| |__plot/
| | |__plotting.py
| | |__absm/
| | | |__absm_abs_diff.png
| | | |__absm_data.png
| | | |__absm_offset_difference.png
| | |
| | |__anova/
| | | |__anova_results.png
| | |
| | |__cohen_d/
| | | |__cohen_d_results.png
| | |
| | |__t_test/
| | | |__ttest_results.png
| | |
| | |__tukey_hsd/
| | | |__tukey_hsd_absm.png
| | |
| | |__polynomial/
| | | |__plots_Polynomial_ttest/
| | | |__plots_Polynomial_Summary/
| | | |__plots_Polynomial_friedman/
| | | |__plots_Polynomial_D/
| |
| |__NOTES.md
|
├── requirements.txt # Python dependencies
├── LICENSE # License
└── README.md # This file
```

## ⚙️ Installation
```bash
pip install -r requirements.txt
```

## 📖 References
[List of references in IEEE style]

[1] GitHub, “GitHub: Where the world builds software.” [Online]. 
Available: https://github.com 
[2] C. R. Harris, K. J. Millman, S. J. van der Walt, et al., “Array 
programming with NumPy,” Nature, vol. 585, no. 7825, pp. 357–362, 
2020. [Online]. Available: https://numpy.org 
[3] P. Virtanen, R. Gommers, T. E. Oliphant, et al., “SciPy 1.0: 
Fundamental algorithms for scientific computing in Python,” Nature 
Methods, vol. 17, pp. 261–272, 2020. [Online]. Available: 
https://scipy.org 
[4] J. D. Hunter, “Matplotlib: A 2D graphics environment,” 
Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, 2007. 
[Online]. Available: https://matplotlib.org 
[5] “Statsmodels: Statistics in Python — Statsmodels 0.14.0 
Documentation,” Statsmodels Developers, 2023. [Online]. Available: 
https://www.statsmodels.org 
[6] “draw.io – Flowchart Maker & Online Diagram Software,” 
Google / diagrams.net, 2025. [Online]. Available: 
https://app.diagrams.net 
 
