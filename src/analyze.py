import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "life-expectancy-vs-healthcare-expenditure.csv"
df = pd.read_csv(DATA_PATH)

df = df.rename(columns={
    'Entity': 'country', 'Code': 'code', 'Year': 'year',
    'Life expectancy at birth': 'life_expectancy',
    'Health expenditure per capita, PPP': 'health_expenditure',
    'Population': 'population',
    'World region according to OWID': 'owid_region'
})
df = df[df['code'].notna() & (~df['code'].str.startswith('OWID_'))].copy()
df_clean = df.dropna(subset=['life_expectancy', 'health_expenditure']).copy()
df_clean = df_clean[df_clean['life_expectancy'] >= 30].copy()

snapshot = df_clean[df_clean['year'] == 2019].copy()

# Log-transform spending — this is the key move for "diminishing returns"
snapshot['log_expenditure'] = np.log10(snapshot['health_expenditure'])

# Regression: life expectancy explained by log(spending)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    snapshot['log_expenditure'], snapshot['life_expectancy']
)

print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.6f}")
print(f"Slope: {slope:.3f}  (life expectancy gain per 10x increase in spending)")

# Plot with regression line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(snapshot['health_expenditure'], snapshot['life_expectancy'], alpha=0.6)
ax.set_xscale('log')

x_line = np.linspace(snapshot['log_expenditure'].min(), snapshot['log_expenditure'].max(), 100)
y_line = slope * x_line + intercept
ax.plot(10**x_line, y_line, color='darkorange', linewidth=2, label=f'Fit (R²={r_value**2:.2f})')

ax.set_xlabel('Health expenditure per capita, PPP ($, log scale)')
ax.set_ylabel('Life expectancy at birth (years)')
ax.set_title('Diminishing Returns: Spending vs. Life Expectancy (2019)')
ax.legend()
plt.tight_layout()
plt.savefig(Path(__file__).resolve().parent.parent / "images" / "diminishing_returns.png", dpi=150)
plt.show()