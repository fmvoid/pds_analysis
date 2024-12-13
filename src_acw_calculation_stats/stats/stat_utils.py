# src/processing_utils.py

import pandas as pd
import numpy as np
from scipy import stats
import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pingouin as pg

def calculate_descriptive_statistics(csv_file_path, acw_type, output_folder, subjects_to_remove=None):
    """
    Calculate descriptive statistics for a given ACW measure from a CSV file and save results.
    
    Parameters:
    csv_file_path (str): Path to the CSV file containing ACW results
    acw_type (str): Type of ACW to analyze ('Mean_ACW_0', 'Mean_ACW_50', or 'Mean_ACW_Nadir')
    output_folder (str): Path to the folder where the results will be saved
    subjects_to_remove (list): Optional list of subject IDs to remove for outlier correction
    
    Returns:
    pandas.DataFrame: Dataframe containing descriptive statistics for each region
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Remove specified subjects if any
    if subjects_to_remove:
        df = df[~df.iloc[:, 0].isin(subjects_to_remove)]
    
    # Group by region and calculate statistics
    stats_df = df.groupby(df.columns[1])[acw_type].agg([
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', lambda x: np.std(x, ddof=1)),
        ('variance', lambda x: np.var(x, ddof=1)),
        ('iqr', stats.iqr),
        ('min', 'min'),
        ('max', 'max')
    ])
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Generate output file name
    input_file_name = os.path.basename(csv_file_path)
    output_file_name = f"stats_{acw_type}_{input_file_name}"
    if subjects_to_remove:
        output_file_name = f"stats_{acw_type}_outliers_removed_{input_file_name}"
    output_path = os.path.join(output_folder, output_file_name)
    
    # Save results to CSV
    stats_df.to_csv(output_path)
    
    print(f"Statistics saved to: {output_path}")
    
    return stats_df

def check_normality(csv_file_path, acw_type, output_folder, subjects_to_remove=None):
    """
    Check normality of ACW values for each region using Shapiro-Wilk test and Q-Q plots.
    
    Parameters:
    csv_file_path (str): Path to the CSV file containing ACW results
    acw_type (str): Type of ACW to analyze ('Mean_ACW_0', 'Mean_ACW_50', or 'Mean_ACW_Nadir')
    output_folder (str): Path to the folder where the results will be saved
    subjects_to_remove (list): Optional list of subject IDs to remove for outlier correction
    
    Returns:
    pandas.DataFrame: Dataframe containing Shapiro-Wilk test results for each region
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    input_file_name = os.path.basename(csv_file_path)
    
    # Remove specified subjects if any
    if subjects_to_remove:
        df = df[~df.iloc[:, 0].isin(subjects_to_remove)]
    
    # Extract group name from the group header or input file name
    if 'Group' in df.columns:
        group_name = df['Group'].iloc[0]
    elif 'HC' in input_file_name:
        group_name = 'HC'
    elif 'MDD' in input_file_name:
        group_name = 'MDD'
    elif 'SZ' in input_file_name:
        group_name = 'SZ'
    else:
        raise ValueError("Unable to determine group name from the group header or input file name")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize dictionary to store Shapiro-Wilk test results
    shapiro_results = {}
    
    # Perform Shapiro-Wilk test and create Q-Q plots for each region
    for region in df[df.columns[1]].unique():
        region_data = df[df[df.columns[1]] == region][acw_type]
        
        # Perform Shapiro-Wilk test
        statistic, p_value = stats.shapiro(region_data)
        shapiro_results[region] = {'statistic': statistic, 'p_value': p_value}
        
        # Create Q-Q plot
        fig, ax = plt.subplots(figsize=(8, 6))
        stats.probplot(region_data, dist="norm", plot=ax)
        ax.set_title(f"Q-Q Plot for {region} - {acw_type} ({group_name})")
        
        # Save Q-Q plot
        plot_filename = f"qq_plot_{region}_{acw_type}_{group_name}.png"
        if subjects_to_remove:
            plot_filename = f"qq_plot_{region}_{acw_type}_{group_name}_outliers_removed.png"
        plt.savefig(os.path.join(output_folder, plot_filename))
        plt.close()
    
    # Create DataFrame from Shapiro-Wilk test results
    shapiro_df = pd.DataFrame.from_dict(shapiro_results, orient='index')
    shapiro_df.columns = ['Shapiro_statistic', 'Shapiro_p_value']
    
    # Save Shapiro-Wilk test results
    output_file_name = f"shapiro_test_{acw_type}_{group_name}.csv"
    if subjects_to_remove:
        output_file_name = f"shapiro_test_{acw_type}_{group_name}_outliers_removed.csv"
    output_path = os.path.join(output_folder, output_file_name)
    shapiro_df.to_csv(output_path)
    
    print(f"Shapiro-Wilk test results saved to: {output_path}")
    print(f"Q-Q plots saved in: {output_folder}")
    
    return shapiro_df

def perform_two_way_welch_anova(data, acw_type, output_folder, subjects_to_remove=None):
    """
    Perform a two-way Welch's ANOVA for group and region effects on ACW values using Pingouin.
    
    Parameters:
    data (pandas.DataFrame or str): DataFrame in long format or path to a CSV file in long format
    acw_type (str): Type of ACW to analyze ('Mean_ACW_0', 'Mean_ACW_50', or 'Mean_ACW_Nadir')
    output_folder (str): Path to the folder where the results will be saved
    subjects_to_remove (list): Optional list of subject IDs to remove for outlier correction
    
    Returns:
    pandas.DataFrame: Dataframe containing Welch's ANOVA results
    pandas.DataFrame: Combined DataFrame used for analysis
    """
    if isinstance(data, str):
        # It's a path to a CSV file
        combined_df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        # It's already a DataFrame
        combined_df = data.copy()
    else:
        print("Error: Invalid input format. Please provide either a DataFrame or a path to a CSV file.")
        return None, None

    # Remove specified subjects if any
    if subjects_to_remove:
        combined_df = combined_df[~combined_df.iloc[:, 0].isin(subjects_to_remove)]

    # Ensure required columns are present
    required_columns = ['Group', acw_type]
    if not all(col in combined_df.columns for col in required_columns):
        print(f"Error: The data must contain 'Group' and '{acw_type}' columns.")
        return None, None

    # Extract region column (assuming it's the second column)
    region_col = combined_df.columns[1]
    
    # Get unique regions
    regions = combined_df[region_col].unique()
    
    # Initialize results list
    results = []
    
    # Perform Welch's ANOVA for each region
    for region in regions:
        region_data = combined_df[combined_df[region_col] == region]
        
        # Perform Welch's ANOVA using Pingouin
        aov = pg.welch_anova(dv=acw_type, between='Group', data=region_data)
        
        # Add region information to the results
        aov['Region'] = region
        
        results.append(aov)
    
    # Combine all results
    results_df = pd.concat(results, ignore_index=True)
    
    # Reorder columns for better readability
    results_df = results_df[['Region', 'Source', 'ddof1', 'ddof2', 'F', 'p-unc', 'np2']]
    
    # Save the results to the output folder
    os.makedirs(output_folder, exist_ok=True)
    result_file_name = f"welch_anova_{acw_type}.csv"
    output_path = os.path.join(output_folder, result_file_name)
    
    # Save the Welch's ANOVA results as CSV
    results_df.to_csv(output_path, index=False)
    
    # Print results to terminal
    print(f"\nWelch's ANOVA results for {acw_type}:")
    print(results_df.to_string(index=False))
    print(f"\nWelch's ANOVA results saved to: {output_path}")
    
    return results_df, combined_df

def calculate_acw_ratio(csv_file_path, acw_type, output_folder, region1, region2, subjects_to_remove=None):
    """
    For a given ACW measure, calculate the ACW ratio between two brain regions for each subject.

    Parameters:
    csv_file_path (str): Path to the CSV file containing ACW results
    acw_type (str): Type of ACW to analyze ('Mean_ACW_0', 'Mean_ACW_50', or 'Mean_ACW_Nadir')
    output_folder (str): Path to the folder where the results will be saved
    region1 (str): Name of the first brain region
    region2 (str): Name of the second brain region
    subjects_to_remove (list): Optional list of subject IDs to remove for outlier correction
    
    Returns:
    pandas.DataFrame: Dataframe containing ACW ratio between region1 and region2
    """
    print(f"Debug: csv_file_path = {csv_file_path}")
    print(f"Debug: acw_type = {acw_type}")
    print(f"Debug: region1 = {region1}")
    print(f"Debug: region2 = {region2}")
    print(f"Debug: output_folder = {output_folder}")

    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Remove specified subjects if any
    if subjects_to_remove:
        df = df[~df.iloc[:, 0].isin(subjects_to_remove)]
    
    # Filter data for region1 and region2
    region1_data = df[(df['Region'] == region1) & (df['ACW_Type'] == acw_type)]
    region2_data = df[(df['Region'] == region2) & (df['ACW_Type'] == acw_type)]
    
    # Merge the data for both regions
    merged_data = pd.merge(region1_data, region2_data, on=['Subject', 'Group'], suffixes=('_region1', '_region2'))
    
    # Calculate the ACW ratio
    merged_data['ACW_Ratio'] = merged_data['ACW_Value_region1'] / merged_data['ACW_Value_region2']
    
    # Keep only necessary columns
    df = merged_data[['Subject', 'Group', 'ACW_Ratio']]
    
    # Save the results to the output folder
    print(f"Debug: About to create directory: {output_folder}")
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f'acw_ratio_{region1}_{region2}_{acw_type}.csv')
    print(f"Debug: Attempting to save file: {output_file}")
    df.to_csv(output_file, index=False)
    
    print(f"ACW ratio between {region1} and {region2} for {acw_type} saved to: {output_file}")
    
    return df

def perform_one_way_welch_anova(csv_file_path, acw_ratio_column, output_folder):
    """
    Perform a one-way Welch's ANOVA for group effects on ACW ratio values using Pingouin.
    
    Parameters:
    csv_file_path (str): Path to the CSV file containing ACW ratio results
    acw_ratio_column (str): Name of the column containing ACW ratio values (e.g., 'ACW_Ratio')
    output_folder (str): Path to the folder where the results will be saved
    
    Returns:
    pandas.DataFrame: Dataframe containing Welch's ANOVA results
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Ensure required columns are present
    required_columns = ['Group', acw_ratio_column]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: The data must contain 'Group' and '{acw_ratio_column}' columns.")
        return None
    
    # Perform Welch's ANOVA using Pingouin
    aov = pg.welch_anova(dv=acw_ratio_column, between='Group', data=df)
    
    # Save the results to the output folder
    os.makedirs(output_folder, exist_ok=True)
    result_file_name = f"welch_anova_{acw_ratio_column}.csv"
    output_path = os.path.join(output_folder, result_file_name)
    
    # Save the Welch's ANOVA results as CSV
    aov.to_csv(output_path, index=False)
    
    # Print results to terminal
    print(f"\nWelch's ANOVA results for {acw_ratio_column}:")
    print(aov.to_string(index=False))
    print(f"\nWelch's ANOVA results saved to: {output_path}")
    
    return aov
