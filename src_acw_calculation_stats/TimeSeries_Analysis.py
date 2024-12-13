import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import acf
from antropy import lziv_complexity
from pyentrp import entropy as ent

"""
A class for fMRI time-series analysis.
Included a measurements often used in the Northoff lab.
"""

class TimeSeriesAnalysis:
    """
    The class includes functions for fMRI time-series analysis
    """
    def __init__(self):
        """
        Initialize time-series
        """

    def ip_f(self, ts, method, order):
        """
        Function computing interpolation on a time-series
        ts = timeseries
        method = interpolation method
        order = order of interpolation
        """
        df = pd.DataFrame(data=ts)
        df.replace(0, np.nan, inplace=True) # Replace 0 by nan
        ip = (df.interpolate(method=method, order=order, limit=3,
                             limit_direction=None) # Interpolate
              .fillna(df.interpolate(method="spline", order=1, limit=3,
                                     limit_direction="both"))) # Extrapolate
        ip = ip[0].values.tolist() # df to list
        return ip
    
    def smooth(self, data, window_len, window):
        """
        Function for smoothing time-series
        data = time-series
        window_len = smoothing window length
        window = window type
        """
        s = np.r_[2*data[0] - data[window_len-1::-1],
                  data,2*data[-1]-data[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=np.ones(window_len,'d')
        else:  
            w=eval('np.'+window+'(window_len)')
            y=np.convolve(w/w.sum(),s,mode='same')
            return y[window_len:-window_len+1]
    
    def sliding_windows(self, ts, ws):
        """
        Function computing sliding windows (step increase = 1)
        ts = time-series
        ws = window size
        """
        list_windows = []
        if len(ts) <= ws:
            return ts
        for i in range(len(ts) - ws + 1):
            sw = ts[i:i+ws]
            list_windows.append(sw)
        return list_windows
        
    def ple_f(self, ideal_frequency, power_spectrum):
        """
        Function computing the power-law exponent
        """
        ple = stats.linregress(np.log(ideal_frequency), np.log(power_spectrum))
        return ple[0]
    
    def median_f(self, freq, power):
        """
        Function computing the median frequency
        """
        cum_sum = np.cumsum(power)
        med_freq = freq[np.argmax(cum_sum >= cum_sum[-1] / 2)]
        return med_freq

    def mean_f(freq, power):
        """
        Function computing the mean frequency
        """
        mean_f = np.sum(freq*power) / np.sum(power)
        return mean_f
        
    def acw_f(self, ts, sr, fast=True):
        """
        Function computing the autocorrelation window
        acw = autocorrelation function
        acw_50 = autocorrelation at or below r = 0.5
        acw_0 = autocorrelation at or below r = 0
        acw_nadir = autocorrelation at or below first nadir
        ts = timeseries
        sr = sampling rate (in seconds)
        """
        sr = 1/sr # Sampling rate (s to Hz)
        acw = acf(ts, nlags=len(ts)-1, qstat=False, alpha=None, fft=fast)
        lags = np.arange(0, len(ts), 1)
        acw_50 = np.argmax(acw <= 0.5) / sr
        acw_0 = np.argmax(acw <= 0) / sr
        deriv = np.sign(np.diff(acw))
        acw_nadir = np.where(deriv == 1)[0][0] / sr
        return acw, lags, acw_50, acw_0, acw_nadir
    
    def sampen_f(self, ts, m, r):
        """
        Function computing the Sample Entropy
        m = embedding dimension
        r = similarity criterion (effectively a noise threshold)
        Recommended settings (Wang et al. 2014)
            embedding dimension = 3
            r = 0.6
            tau = 1 (1 is default)
        ts = time-series
        """
        sd = np.std(ts)
        sampen = ent.sample_entropy(ts, m, sd*r)[-1]
        return sampen
    
    def lzc_f(self, ts):
        """
        Function computing the Lempel-Ziv complexity
        ts = time-series
        """
        threshold = np.median(ts)
        ts[ts >= threshold] = 1.0
        ts[ts < threshold] = 0.0
        lzc = lziv_complexity(ts, normalize=True)
        return lzc
