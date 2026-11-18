import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "life-expectancy-vs-healthcare-expenditure.csv"
df = pd.read_csv(DATA_PATH)

print(df.shape)
print(df.columns.tolist())

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

# Remove implausible values (data artifacts, not real countries in crisis)
df_clean = df_clean[df_clean['life_expectancy'] >= 30].copy()

print(df_clean['year'].min(), '-', df_clean['year'].max())
print(df_clean.shape)
print(df_clean['country'].nunique(), 'countries')