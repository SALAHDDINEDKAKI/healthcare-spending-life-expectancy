import pandas as pd

url = "https://ourworldindata.org/grapher/life-expectancy-vs-healthcare-expenditure.csv?v=1&csvType=full&useColumnShortNames=true"
df = pd.read_csv(url, storage_options={'User-Agent': 'Mozilla/5.0'})

print(df.shape)
print(df.columns.tolist())

# --- new code below ---
df = df.rename(columns={
    'entity': 'country',
    'life_expectancy__sex_all__age_0__variant_estimates': 'life_expectancy',
    'sh_xpd_chex_pp_cd': 'health_expenditure',
    'population_historical': 'population'
})

df = df[df['code'].notna() & (~df['code'].str.startswith('OWID_'))].copy()

df_clean = df.dropna(subset=['life_expectancy', 'health_expenditure']).copy()

print(df_clean['year'].min(), '-', df_clean['year'].max())
print(df_clean.shape)
print(df_clean['country'].nunique(), 'countries')