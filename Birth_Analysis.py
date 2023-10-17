# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from a CSV file into a Pandas DataFrame
births = pd.read_csv("births.csv")

# Display the first few rows of the DataFrame
print(births.head())

# Data Cleaning:
# Fill missing values in the 'day' column with zeros and convert it to integers
births['day'].fillna(0, inplace=True)
births['day'] = births['day'].astype(int)

# Create a 'decade' column to represent birth decades
births['decade'] = 10 * (births['year'] // 10)

# Create a pivot table summarizing total births by gender for each decade
birth_decade = births.pivot_table('births', index='decade', columns='gender', aggfunc='sum')

# Data Visualization:
# Set Seaborn style
sns.set()

# Create a line plot to show total births per year for each gender
birth_decade.plot()
plt.ylabel("Total births per year")
plt.show()

# Calculate quartiles and define a range for valid birth counts
quartiles = np.percentile(births['births'], [25, 50, 75])
mu = quartiles[1]
sig = 0.74 * (quartiles[2] - quartiles[0])

# Filter the DataFrame to keep only valid birth counts
births = births.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
births['day'] = births['day'].astype(int)

# Set the index of the DataFrame to a datetime format
births.index = pd.to_datetime(10000 * births.year +
                              100 * births.month +
                              births.day, format='%Y%m%d')

# Add a 'dayofweek' column to represent the day of the week for each birth date
births['dayofweek'] = births.index.dayofweek

# Create a pivot table showing the mean births by day of the week for each decade and visualize it
births.pivot_table('births', index='dayofweek', columns='decade', aggfunc='mean').plot()
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.ylabel('Mean births by day')
plt.show()

# Create a pivot table summarizing births by month and day and convert the index to datetime
births_month = births.pivot_table('births', [births.index.month, births.index.day])
births_month.index = [pd.datetime(2012, month, day) for (month, day) in births_month.index]

# Visualize the births by month and day
fig, ax = plt.subplots(figsize=(12, 4))
births_month.plot(ax=ax)
plt.show()
