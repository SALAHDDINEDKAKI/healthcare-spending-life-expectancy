import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "life-expectancy-vs-healthcare-expenditure.csv"
df = pd.read_csv(DATA_PATH)

df = df.rename(columns={
    'Entity': 'country',
    'Code': 'code',
    'Year': 'year',
    'Life expectancy at birth': 'life_expectancy',
    'Health expenditure per capita, PPP': 'health_expenditure',
    'Population': 'population',
    'World region according to OWID': 'owid_region'
})
df = df[df['code'].notna() & (~df['code'].str.startswith('OWID_'))].copy()
df_clean = df.dropna(subset=['life_expectancy', 'health_expenditure']).copy()

# How many countries have data per year? (picks our "snapshot" year)
coverage = df_clean.groupby('year')['country'].nunique()
print(coverage.tail(10))

# Basic stats
print(df_clean[['life_expectancy', 'health_expenditure']].describe())

# Overall correlation
corr = df_clean['life_expectancy'].corr(df_clean['health_expenditure'])
print(f"\nCorrelation: {corr:.3f}")

print(df_clean[df_clean['life_expectancy'] < 30][['country', 'year', 'life_expectancy']])