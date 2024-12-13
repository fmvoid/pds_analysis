"""
This script performs fMRI data analysis for a study comparing healthy controls (HC),
major depressive disorder (MDD), and schizophrenia (SZ) patients. It processes fMRI
data for multiple subjects, extracts time series data for various brain regions
(auditory, visual, motor cortices, DMN, FPN, salience network, and limbic system),
and calculates autocorrelation window (ACW) and autocorrelation function (ACF) for
each group. The script loads data, applies preprocessing steps, extracts region-
specific time series, computes ACW and ACF, and saves both individual and mean
results to CSV files for further analysis and comparison between groups.

To fix:
- Separate the data processing from the ACW and ACF calculation
- Change the bandpassing parameters to 0.008 and 0.24
"""


from data_loader import load_fmri_data, load_regressors
from roi_creation import fetch_aal_atlas, create_label_to_pseudo_index, get_pseudo_index, create_masker, extract_timeseries, extract_timeseries_for_roi
from region_lists import auditory_cortex_regions, visual_cortex_regions, motor_cortex_regions, dmn_regions, fpn_regions, salience_network_regions, limbic_system_regions
from acw_calculation import calculate_acw, compute_mean_acw, compute_mean_autocorr
from TimeSeries_Analysis import TimeSeriesAnalysis
import pandas as pd
import numpy as np

tsa = TimeSeriesAnalysis()

# Load empricial fMRI data and regressors
data_dir = '/Users/fdjim/Desktop/PDS_FULL/derivatives/fmriprep'
subjects = [
    "sub-003P", "sub-004P", "sub-005C", "sub-005P", "sub-006C",
    "sub-007C", "sub-007P", "sub-008P", "sub-009C", "sub-010P",
    "sub-013C", "sub-014C", "sub-014P", "sub-015C", "sub-015P",
    "sub-016C", "sub-016P", "sub-017C", "sub-018C", "sub-018P",
    "sub-019C", "sub-019P", "sub-020C", "sub-020P", "sub-021C",
    "sub-023P", "sub-024C", "sub-024P", "sub-025C", "sub-026C",
    "sub-027C", "sub-028C", "sub-029C", "sub-030C", "sub-030P",
    "sub-031C", "sub-031P", "sub-032P", "sub-033P", "sub-035P",
    "sub-037P", "sub-039P", "sub-041P", "sub-042P", "sub-043P",
    "sub-045P", "sub-046P", "sub-047P", "sub-048P", "sub-049P",
    "sub-050P", "sub-051P", "sub-052P", "sub-055P", "sub-056P",
    "sub-061P", "sub-066P", "sub-067P", "sub-069P", "sub-071P",
    "sub-075P"
]

# Split the subjects into groups for the analysis
diagnosis_df = pd.read_csv('/Users/fdjim/Desktop/PDS_FULL/participants.tsv', sep='\t')
# Create a dictionary mapping subject IDs to diagnosis
diagnosis_dict = dict(zip(diagnosis_df['participant_id'], diagnosis_df['dx']))
# Split subjects into groups based on diagnosis
subjects_hc = []
subjects_mdd = []
subjects_sz = []
for subject in subjects:
    if subject in diagnosis_dict:
        if diagnosis_dict[subject] == 'hc':
            subjects_hc.append(subject)
        elif diagnosis_dict[subject] == 'mdd':
            subjects_mdd.append(subject)
        elif diagnosis_dict[subject] == 'sz':
            subjects_sz.append(subject)
    else:
        print(f"Warning: Subject {subject} not found in diagnosis file")
print(f"HC: {subjects_hc}")
print(f"MDD: {subjects_mdd}")
print(f"SZ: {subjects_sz}")

# Fetch atlas and create label to pseudo-index mapping
labels_aal, indices_aal, aal_img = fetch_aal_atlas()
pseudo_idx_aal = create_label_to_pseudo_index(labels_aal)
pseudo_idx_auditory = get_pseudo_index(pseudo_idx_aal, auditory_cortex_regions)
pseudo_idx_visual = get_pseudo_index(pseudo_idx_aal, visual_cortex_regions)
pseudo_idx_motor = get_pseudo_index(pseudo_idx_aal, motor_cortex_regions)
pseudo_idx_dmn = get_pseudo_index(pseudo_idx_aal, dmn_regions)
pseudo_idx_fpn = get_pseudo_index(pseudo_idx_aal, fpn_regions)
pseudo_idx_salience = get_pseudo_index(pseudo_idx_aal, salience_network_regions)
pseudo_idx_limbic = get_pseudo_index(pseudo_idx_aal, limbic_system_regions)
# Create masker object, bandpass filter and smooth the data
masker = create_masker(aal_img, smoothing_fwhm=2, high_pass=0.01, low_pass=0.24, 
                       t_r=2, standardize=True)

ts_hc = []
ts_mdd = []
ts_sz = []
task = 'pds'
for group in [subjects_hc, subjects_mdd, subjects_sz]:
    fmri_imgs = load_fmri_data(data_dir, group, task)
    regressors = load_regressors(data_dir, group, task)
    # Extract time series data
    ts_group = extract_timeseries(masker, fmri_imgs, regressors)
    if group == subjects_hc:
        ts_hc.extend(ts_group)
    elif group == subjects_mdd:
        ts_mdd.extend(ts_group)
    elif group == subjects_sz:
        ts_sz.extend(ts_group)

print(f"HC time series: {len(ts_hc)}")
print(f"MDD time series: {len(ts_mdd)}")
print(f"SZ time series: {len(ts_sz)}")

# Process each group independently
time_series_dict_hc = extract_timeseries_for_roi(
    ts_hc,
    pseudo_idx_auditory,
    pseudo_idx_visual,
    pseudo_idx_motor,
    pseudo_idx_dmn,
    pseudo_idx_fpn,
    pseudo_idx_salience,
    pseudo_idx_limbic,
    subjects_hc,
    "HC"
)

time_series_dict_mdd = extract_timeseries_for_roi(
    ts_mdd,
    pseudo_idx_auditory,
    pseudo_idx_visual,
    pseudo_idx_motor,
    pseudo_idx_dmn,
    pseudo_idx_fpn,
    pseudo_idx_salience,
    pseudo_idx_limbic,
    subjects_mdd,
    "MDD"
)

time_series_dict_sz = extract_timeseries_for_roi(
    ts_sz,
    pseudo_idx_auditory,
    pseudo_idx_visual,
    pseudo_idx_motor,
    pseudo_idx_dmn,
    pseudo_idx_fpn,
    pseudo_idx_salience,
    pseudo_idx_limbic,
    subjects_sz,
    "SZ"
)

# Calculate ACW results for each group
acw_results_hc = calculate_acw(time_series_dict_hc)[0]
acw_results_mdd = calculate_acw(time_series_dict_mdd)[0]
acw_results_sz = calculate_acw(time_series_dict_sz)[0]

# Calculate ACF results for each group
acf_results_hc = calculate_acw(time_series_dict_hc)[1]
acf_results_mdd = calculate_acw(time_series_dict_mdd)[1]
acf_results_sz = calculate_acw(time_series_dict_sz)[1]

# Save ACW results to CSV for each group
for group_name, acw_results in [("HC", acw_results_hc), ("MDD", acw_results_mdd), ("SZ", acw_results_sz)]:
    acw_results_df = pd.DataFrame.from_dict({(i, j): acw_results[i][j] 
                                            for i in acw_results.keys() 
                                            for j in acw_results[i].keys()},
                                            orient='index')
    acw_results_df.to_csv(f'/Users/fdjim/Desktop/PDS_CODE/analysis_codebase/results/acw_results_{group_name}.csv')

# Save ACF results to CSV for each group
for group_name, acf_results in [("HC", acf_results_hc), ("MDD", acf_results_mdd), ("SZ", acf_results_sz)]:
    acf_results_df = pd.DataFrame.from_dict({(i, j): acf_results[i][j] 
                                            for i in acf_results.keys() 
                                            for j in acf_results[i].keys()},
                                            orient='index')
    acf_results_df.to_csv(f'/Users/fdjim/Desktop/PDS_CODE/analysis_codebase/results/acf_results_{group_name}.csv')

# Calculate mean ACW results for each group
mean_acw_results_hc = compute_mean_acw(acw_results_hc)
mean_acw_results_mdd = compute_mean_acw(acw_results_mdd)
mean_acw_results_sz = compute_mean_acw(acw_results_sz)

# Calculate mean ACF results for each group
mean_acf_results_hc = compute_mean_autocorr(acf_results_hc)
mean_acf_results_mdd = compute_mean_autocorr(acf_results_mdd)
mean_acf_results_sz = compute_mean_autocorr(acf_results_sz)

# Save mean ACW results to CSV for each group
for group_name, mean_acw_results in [("HC", mean_acw_results_hc), ("MDD", mean_acw_results_mdd), ("SZ", mean_acw_results_sz)]:
    mean_acw_results_df = pd.DataFrame.from_dict({(i, j): mean_acw_results[i][j] 
                                                for i in mean_acw_results.keys() 
                                                for j in mean_acw_results[i].keys()},
                                                orient='index')
    mean_acw_results_df.to_csv(f'/Users/fdjim/Desktop/PDS_CODE/analysis_codebase/results/mean_acw_results_{group_name}.csv')
    print(f'Saved mean ACW results for {group_name} to CSV file!')

# Print mean ACW results for each group
print("Healthy Control Mean ACW:")
print(pd.DataFrame(mean_acw_results_hc))
print("\nMDD Mean ACW:")
print(pd.DataFrame(mean_acw_results_mdd))
print("\nSZ Mean ACW:")
print(pd.DataFrame(mean_acw_results_sz))
