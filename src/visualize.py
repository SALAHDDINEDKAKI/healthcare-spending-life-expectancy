import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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

# Snapshot year: 2019 — full country coverage, no COVID distortion
snapshot = df_clean[df_clean['year'] == 2019]

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(snapshot['health_expenditure'], snapshot['life_expectancy'], alpha=0.6)
ax.set_xscale('log')
ax.set_xlabel('Health expenditure per capita, PPP ($, log scale)')
ax.set_ylabel('Life expectancy at birth (years)')
ax.set_title('Healthcare Spending vs. Life Expectancy (2019)')

# Highlight the US
us = snapshot[snapshot['country'] == 'United States']
if not us.empty:
    ax.scatter(us['health_expenditure'], us['life_expectancy'], color='red', s=80, zorder=5)
    ax.annotate('United States', (us['health_expenditure'].values[0], us['life_expectancy'].values[0]),
                xytext=(10, -10), textcoords='offset points')

plt.tight_layout()
plt.savefig(Path(__file__).resolve().parent.parent / "images" / "spending_vs_life_expectancy_2019.png", dpi=150)
plt.show()

# Time trend: a few countries over the full range
countries_to_track = ['United States', 'Germany', 'Japan', 'United Kingdom']
trend_data = df_clean[df_clean['country'].isin(countries_to_track)]

fig2, ax2 = plt.subplots(figsize=(10, 6))
for country in countries_to_track:
    subset = trend_data[trend_data['country'] == country]
    ax2.plot(subset['year'], subset['life_expectancy'], marker='o', markersize=3, label=country)

ax2.set_xlabel('Year')
ax2.set_ylabel('Life expectancy at birth (years)')
ax2.set_title('Life Expectancy Over Time: US vs. Peer Countries')
ax2.legend()
plt.tight_layout()
plt.savefig(Path(__file__).resolve().parent.parent / "images" / "life_expectancy_trend.png", dpi=150)
plt.show()