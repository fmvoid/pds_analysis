import pandas as pd
from acw_plot import acw_plot


# Prepare the data
data_hc = pd.read_csv('analysis_codebase/results/mean_acw_results_HC.csv', header=0, names=['Subject', 'Region', 'ACW_50', 'ACW_0', 'ACW_Nadir'])
data_mdd = pd.read_csv('analysis_codebase/results/mean_acw_results_MDD.csv', header=0, names=['Subject', 'Region', 'ACW_50', 'ACW_0', 'ACW_Nadir'])
data_sz = pd.read_csv('analysis_codebase/results/mean_acw_results_SZ.csv', header=0, names=['Subject', 'Region', 'ACW_50', 'ACW_0', 'ACW_Nadir'])
# Add a 'Group' column to each dataframe
data_hc['Group'] = 'HC'
data_mdd['Group'] = 'MDD'
data_sz['Group'] = 'SZ'
# Combine all dataframes into one
combined_data = pd.concat([data_hc, data_mdd, data_sz], ignore_index=True)
# Melt the dataframe to long format
long_data = pd.melt(combined_data, id_vars=['Subject', 'Region', 'Group'], 
                    var_name='ACW_Type', value_name='ACW_Value')
# Save the combined long format dataframe
long_data.to_csv('analysis_codebase/results/combined_acw_results.csv', index=False)

# Plotting
