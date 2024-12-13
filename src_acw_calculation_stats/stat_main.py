# Statistics
from analysis_codebase.src.stats.stat_utils import calculate_acw_statistics, check_normality, perform_two_way_welch_anova, perform_post_hoc_tests

hc_data_path = 'analysis_codebase/results/results_1/mean_acw_results_HC.csv'
mdd_data_path = 'analysis_codebase/results/results_1/mean_acw_results_MDD.csv'
sz_data_path = 'analysis_codebase/results/results_1/mean_acw_results_SZ.csv'

output_folder_desc_stats = 'analysis_codebase/results/acw_statistics'
acw_measure = 'Mean_ACW_0' # Mean_ACW_0, Mean_ACW_Nadir
# Calculate statistics for each group and ACW measure
for group, data_path in [('HC', hc_data_path), ('MDD', mdd_data_path), ('SZ', sz_data_path)]:
    for acw_measure in [acw_measure]:
        if group == 'HC':
            stats = calculate_acw_statistics(data_path, acw_measure, output_folder_desc_stats, subjects_to_remove=['sub-005C'])
        elif group == 'MDD':
            stats = calculate_acw_statistics(data_path, acw_measure, output_folder_desc_stats, subjects_to_remove=['sub-004P', 'sub-035P', 'sub-051P'])
        print(f"Statistics for {group} - {acw_measure}:")
        print(stats)
        print("\n")

# Check for Normality
output_folder_normality = 'analysis_codebase/results/normality_tests'

for group, data_path in [('HC', hc_data_path), ('MDD', mdd_data_path), ('SZ', sz_data_path)]:
    if group == 'HC':
        normality_results = check_normality(data_path, acw_measure, output_folder_normality, subjects_to_remove=['sub-005C'])
    elif group == 'MDD':
        normality_results = check_normality(data_path, acw_measure, output_folder_normality, subjects_to_remove=['sub-004P', 'sub-035P', 'sub-051P'])
    else:
        normality_results = check_normality(data_path, acw_measure, output_folder_normality)
    print(f"Normality test results for {group} - {acw_measure}:")
    print(normality_results)
    print("\n")

# Perform Welch's ANOVA
output_folder_anova = 'analysis_codebase/results/welch_anova'
csv_files = {
    'HC': hc_data_path,
    'MDD': mdd_data_path,
    'SZ': sz_data_path
}
anova_results, combined_df = perform_two_way_welch_anova(csv_files, acw_measure, output_folder_anova)

# Perform post-hoc tests
output_folder_post_hoc = 'analysis_codebase/results/post_hoc'
post_hoc_results = perform_post_hoc_tests(anova_results, combined_df, acw_measure, output_folder_post_hoc)

