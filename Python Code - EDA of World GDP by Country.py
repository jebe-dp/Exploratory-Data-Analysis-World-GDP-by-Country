#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("C:/Users/Jebe Dela Peña/Downloads/GDP.csv")


# In[2]:


#UNDERSTANDING THE DATA

df.head()


# In[3]:


df.tail()


# In[4]:


df.shape


# In[5]:


df.columns


# In[6]:


df.nunique()


# In[7]:


df['2022'].unique()


# In[8]:


# DATA CLEANING

# Identify columns with missing values
df.isnull().sum()


# In[9]:


# Identify and remove duplicate rows
df = df.drop_duplicates()


# In[10]:


# Drop rows where all values in year columns are missing
years = [str(year) for year in range(1960, 2023)]

df = df.dropna(subset=years, how='all')


# In[12]:


# Remove all non-country entries (Continents and Other Classifications)
col_to_remove = ['World','Africa Eastern and Southern', 'Africa Western and Central', 'Arab World', 'Central Europe and the Baltics', 
                'Channel Islands', 'Caribbean small states', 'East Asia & Pacific (excluding high income)', 'Early-demographic dividend', 
                'East Asia & Pacific', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia', 'Arab Rep.', 'Euro area', 
                'European Union', 'Fragile and conflict affected situations', 'High income', 'Heavily indebted poor countries (HIPC)', 
                'IBRD only', 'IDA & IBRD total', 'IDA total', 'IDA blend', 'IDA only', 'Not classified', 'Latin America & Caribbean (excluding high income)', 
                'Latin America & Caribbean', 'Least developed countries: UN classification', 'Low income', 'Lower middle income', 'Low & middle income', 
                'Late-demographic dividend', 'Middle East & North Africa', 'Middle income', 'Middle East & North Africa (excluding high income)', 
                'North America', 'OECD members', 'Other small states', 'Pre-demographic dividend', 'West Bank and Gaza', 'Pacific island small states', 
                'Post-demographic dividend', 'South Asia', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'Small states', 
                'East Asia & Pacific (IDA & IBRD countries)', 'Europe & Central Asia (IDA & IBRD countries)', 'Latin America & the Caribbean (IDA & IBRD countries)',  
                'Middle East & North Africa (IDA & IBRD countries)', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa (IDA & IBRD countries)','Upper middle income'] 

df_countries = df[~df['Country'].isin(col_to_remove)]


# In[13]:


# DATA VISUALIZATION

# 1 - Global GDP over the years

# Calculate global GDP by summing GDP values across all countries for each year
global_gdp = df_countries.loc[:, '1960':'2022'].sum()

# Extract years and global GDP values
years = global_gdp.index.astype(int)
gdp_values = global_gdp.values / 1_000_000_000  # Convert GDP to billions for better readability

# Create a line chart for global GDP growth by year
plt.figure(figsize=(12, 6))
plt.plot(years, gdp_values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.title('Global GDP (1960-2022)')
plt.xlabel('Year')
plt.ylabel('Global GDP (in Billions USD)')
plt.grid(True)

# Show only a subset of years on the x-axis (every 5 years, for example)
subset_years = years[::5]  # Every 5 years
plt.xticks(subset_years, rotation=45)  # Rotate labels for better visibility

plt.tight_layout()
plt.show()


# In[16]:


# 2 - Annual Growth Rate of Global GDP

# Calculate Annual Growth Rate (AGR) of Global GDP
agr_values = []
years = df_countries.columns[2:]  # Assuming the columns start from the third column
for i in range(1, len(years)):
    gdp_current_year = df_countries[years[i]].sum()
    gdp_previous_year = df_countries[years[i - 1]].sum()
    agr = ((gdp_current_year - gdp_previous_year) / gdp_previous_year) * 100
    agr_values.append(agr)

# Create a line chart for Annual Growth Rate of Global GDP
plt.figure(figsize=(12, 6))
plt.plot(years[1:], agr_values, marker='o', color='green', linestyle='-', linewidth=2, markersize=8)
plt.title('Annual Growth Rate of Global GDP (1961-2022)')
plt.xlabel('Year')
plt.ylabel('Annual Growth Rate (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()



# In[63]:


# 3 - Top 5 Countries with Highest GDP for the last 5 years

# Select the top 5 countries with the highest GDP for the last 5 years (2018-2022)
top_countries = df_countries.nlargest(5, '2022')

# Extract years from the columns of the DataFrame
years = [str(year) for year in range(2018, 2023)]

# Extract country names and GDP values for the last 5 years
country_names = top_countries['Country']
gdp_values = top_countries[years].values / 1_000_000_000  # Convert GDP to billions

# Set the bar width for the chart
bar_width = 0.15

# Set the positions of bars on X-axis for better visibility
r1 = list(range(len(years)))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]
r5 = [x + bar_width for x in r4]

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(r1, gdp_values[0], color='b', width=bar_width, edgecolor='grey', label=country_names.iloc[0])
plt.bar(r2, gdp_values[1], color='g', width=bar_width, edgecolor='grey', label=country_names.iloc[1])
plt.bar(r3, gdp_values[2], color='r', width=bar_width, edgecolor='grey', label=country_names.iloc[2])
plt.bar(r4, gdp_values[3], color='c', width=bar_width, edgecolor='grey', label=country_names.iloc[3])
plt.bar(r5, gdp_values[4], color='m', width=bar_width, edgecolor='grey', label=country_names.iloc[4])

# Customize the plot
plt.xlabel('Year', fontweight='bold', fontsize=15)
plt.ylabel('GDP (in Billions USD)', fontweight='bold', fontsize=15)
plt.xticks([r + 2 * bar_width for r in range(len(years))], years)
plt.title('Top 5 Countries with Highest GDP (2018-2022)', fontweight='bold', fontsize=15)
plt.legend(loc='upper left', bbox_to_anchor=(1,1))

# Show the plot
plt.tight_layout()  # Ensures the legend fits within the plot area
plt.show()




# In[102]:


# 4 - GDP Distribution in 2022 - Top 10 Countries, Philippines and the entire world

year = '2022'
top_countries_2022 = df_countries.nlargest(10, year)  # Top 10 countries (GDP in 2022)

# Add the GDP data of the Philippines
ph_gdp = df_countries.loc[df_countries['Country'] == 'Philippines', year].values[0]
philippines_df = pd.DataFrame({'Country': ['Philippines'], year: [ph_gdp]})
top_countries_2022 = pd.concat([top_countries_2022, philippines_df], ignore_index=True)

# Calculate the total GDP of other countries (excluding top 10 and Philippines)
other_countries_gdp = df_countries[year].sum() - top_countries_2022[year].sum()

# Create a list of GDP values (in billions USD) including top 10 countries, Philippines, and "Other Countries"
gdp_values = list(top_countries_2022[year] / 1_000_000_000) + [other_countries_gdp / 1_000_000_000]

# Create a list of country names including top 10 countries, Philippines, and "Other Countries"
countries = list(top_countries_2022['Country']) + ['Other Countries']

# Define colors for each segment
colors = ['#1f77b4', '#2ca02c','#aec7e8', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ff9896','#ff7f0e']

plt.figure(figsize=(10, 10))
plt.pie(gdp_values, labels=countries, autopct='%1.1f%%', startangle=140, colors=colors)

# Add legends with country names
plt.legend(countries, loc='upper left')

plt.title(f'GDP Distribution in {year}')
plt.show()



# In[88]:


# 5 - Philippines Annual Growth Rate of GDP (1960-2022)

# Calculate Annual Growth Rate (AGR) of GDP for the Philippines
agr_values_philippines = []
years = df.columns[2:]  # Assuming the GDP data starts from the third column
for i in range(len(years)):
    gdp_current_year = df[df['Country'] == 'Philippines'][years[i]].values[0]
    if i > 0:
        gdp_previous_year = df[df['Country'] == 'Philippines'][years[i - 1]].values[0]
        agr = ((gdp_current_year - gdp_previous_year) / gdp_previous_year) * 100
        agr_values_philippines.append(agr)
    else:
        # For the first year (1960), set AGR to 0 as there is no previous year for comparison
        agr_values_philippines.append(0)

# Create a line chart for Annual Growth Rate of GDP in the Philippines including year 1960
plt.figure(figsize=(12, 6))
plt.plot(years, agr_values_philippines, marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
plt.title('Annual Growth Rate of GDP in the Philippines (1960-2022)')
plt.xlabel('Year')
plt.ylabel('Annual Growth Rate (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()



# In[93]:


# 6 - Annual Growth Rate of GDP in the Philippines each President's term

# Define the years corresponding to each president's term
president_terms = {
    'Macapagal': (1960, 1965),
    'Marcos': (1965, 1986),
    'Aquino Sr.': (1986, 1992),
    'Ramos': (1992, 1998),
    'Estrada': (1998, 2001),
    'Arroyo': (2001, 2010),
    'Aquino': (2010, 2016),
    'Duterte': (2016, 2022)
}

# Calculate Annual Growth Rate (AGR) of GDP for the Philippines including year 1960
agr_values_philippines = []
years = df.columns[2:]  # Assuming the GDP data starts from the third column
for i in range(len(years)):
    gdp_current_year = df[df['Country'] == 'Philippines'][years[i]].values[0]
    if i > 0:
        gdp_previous_year = df[df['Country'] == 'Philippines'][years[i - 1]].values[0]
        agr = ((gdp_current_year - gdp_previous_year) / gdp_previous_year) * 100
        agr_values_philippines.append(agr)
    else:
        # For the first year (1960), set AGR to 0 as there is no previous year for comparison
        agr_values_philippines.append(0)

# Extract the years for x-axis labels
years = list(range(1960, 2023))

# Create a bar chart for Annual Growth Rate of GDP in the Philippines with president's terms highlighted
plt.figure(figsize=(12, 6))
plt.bar(years, agr_values_philippines, color='gray', label='Annual Growth Rate')
plt.xlabel('Year')
plt.ylabel('Annual Growth Rate (%)')

# Highlight each president's term with different colors and add legends
for president, (start_year, end_year) in president_terms.items():
    plt.bar(range(start_year, end_year + 1), 
            agr_values_philippines[start_year - 1960:end_year - 1960 + 1], 
            label=f'{president} ({start_year}-{end_year})')

plt.title('Annual Growth Rate of GDP in the Philippines with President\'s Terms Highlighted')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()


# In[ ]:




