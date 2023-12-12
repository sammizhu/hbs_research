import pandas as pd

# Read both CSV files into DataFrames
df_a = pd.read_csv('direct_match.csv')
df_b = pd.read_csv('fuzzy_match.csv')

# Find rows in File B that are not in File A
differences = pd.merge(df_b, df_a, indicator=True, how='left').loc[lambda x: x['_merge'] == 'left_only']

# Drop the '_merge' column
differences = differences.drop(columns=['_merge'])

# Write the differences into a new CSV file called 'differences.csv'
differences.to_csv('differences.csv', index=False)
