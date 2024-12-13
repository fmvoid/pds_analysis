import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for the plot
plt.style.use('seaborn')
sns.set_palette("deep")

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(20, 10))

# Create the boxplot
sns.boxplot(x='Region', y='ACW_Value', hue='Group', data=long_data, ax=ax, 
            width=0.6, fliersize=0)

# Add individual data points
sns.stripplot(x='Region', y='ACW_Value', hue='Group', data=long_data, ax=ax,
              dodge=True, alpha=0.6, jitter=0.2, size=4)

# Customize the plot
plt.title('ACW Distribution Across Regions and Groups', fontsize=16)
plt.xlabel('Brain Region', fontsize=14)
plt.ylabel('Autocorrelation Window (ACW)', fontsize=14)
plt.legend(title='Group', title_fontsize='13', fontsize='12')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()