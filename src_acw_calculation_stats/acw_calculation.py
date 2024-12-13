from TimeSeries_Analysis import TimeSeriesAnalysis
import numpy as np
tsa = TimeSeriesAnalysis()

def calculate_acw(timeseries_dict):
    """
    Calculate the ACW and autocorrelation function for each time series in the given input.
    """
    acw_results = {}
    autocorr_results = {}
    for subject_id, regions in timeseries_dict.items():
        print(f'Calculating ACW for subject {subject_id}...')
        acw_results[subject_id] = {}
        autocorr_results[subject_id] = {}
        for region, timeseries_list in regions.items():
            print(f'Calculating ACW for region {region}...')
            acw_results[subject_id][region] = {}
            autocorr_results[subject_id][region] = {}
            for i, timeseries in enumerate(timeseries_list.T):
                acw_output = tsa.acw_f(ts=timeseries, sr=2, fast=True)
                acw_50, acw_0, acw_nadir = acw_output[2], acw_output[3], acw_output[4]
                autocorr = acw_output[0]  # Assuming the autocorrelation function is the first output
                acw_results[subject_id][region].setdefault('ACW_50', []).append(acw_50)
                acw_results[subject_id][region].setdefault('ACW_0', []).append(acw_0)
                acw_results[subject_id][region].setdefault('ACW_Nadir', []).append(acw_nadir)
                autocorr_results[subject_id][region].setdefault('Autocorr', []).append(autocorr)
    return acw_results, autocorr_results

def compute_mean_acw(acw_results):
    """
    Compute the mean ACW for each kind of ACW in the given ACW results.
    """
    mean_acw = {}
    for subject_id, regions in acw_results.items():
        mean_acw[subject_id] = {}
        for region, acw_values in regions.items():
            mean_acw[subject_id][region] = {
                'Mean_ACW_50': np.mean(acw_values['ACW_50']),
                'Mean_ACW_0': np.mean(acw_values['ACW_0']),
                'Mean_ACW_Nadir': np.mean(acw_values['ACW_Nadir'])
            }
    return mean_acw

def compute_mean_autocorr(autocorr_results):
    """
    Compute the mean ACF for each kind of ACF in the given ACF results.
    Averages over columns to get one average value per time point.
    """
    mean_autocorr = {}
    for subject_id, regions in autocorr_results.items():
        mean_autocorr[subject_id] = {}
        for region, autocorr_values in regions.items():
            # Convert list of autocorrelation arrays to a 2D numpy array
            autocorr_array = np.array(autocorr_values['Autocorr'])
            # Compute mean across columns (axis=0)
            mean_autocorr[subject_id][region] = {
                'Mean_Autocorr': np.mean(autocorr_array, axis=0)
            }
    return mean_autocorr