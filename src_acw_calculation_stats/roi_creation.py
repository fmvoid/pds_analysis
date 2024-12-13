from nilearn import datasets, image, plotting
from nilearn.maskers import MultiNiftiLabelsMasker
import matplotlib.pyplot as plt

def fetch_aal_atlas():
    """
    Fetches the AAL atlas and returns the labels, indices, and atlas.

    Returns:
        labels (list): The labels associated with the AAL atlas.
        indices (list): The indices associated with the AAL atlas.
        atlas (nibabel.nifti1.Nifti1Image): The AAL atlas image.
    """
    atlas = datasets.fetch_atlas_aal()
    labels = atlas['labels']
    indices = atlas['indices']
    atlas_img = atlas['maps']
    return labels, indices, atlas_img


def create_label_to_pseudo_index(labels):
    """
    Creates a dictionary to map labels to pseudo-indices. Due to the nature of the AAL atlas, the original indices are 
    not appropriate for indexing into the time series data. This function creates a mapping from labels to pseudo-indices
    that can be used to index into the extracted time series data.
    
    Note that this list will have 116 elements because the 'Background' label is not included.

    Parameters:
        labels (list): The labels associated with the AAL atlas.

    Returns:
        label_to_pseudo_index (dict): A dictionary mapping labels to pseudo-indices.
    """
    label_to_pseudo_index = {label: idx for idx, label in enumerate(labels)}
    return label_to_pseudo_index

def get_pseudo_index(label_to_pseudo_index, labels):
    """
    Retrieves the pseudo-indices for a given list of labels.

    Parameters:
        label_to_pseudo_index (dict): A dictionary mapping labels to pseudo-indices.
        labels (list): The list of labels for which the pseudo-indices will be retrieved.

    Returns:
        pseudo_indices (list): The list of pseudo-indices corresponding to the given labels.
    """
    pseudo_indices = [label_to_pseudo_index[label] for label in labels]
    return pseudo_indices

def create_masker(atlas_filename, smoothing_fwhm=2, high_pass=0.01, low_pass=0.24, t_r=2, standardize=True):
    """
    Creates an instance of the masker object with the specified parameters.

    Parameters:
        atlas_filename (str): The filename of the atlas image.
        smoothing_fwhm (float): The full width at half maximum (FWHM) value for spatial smoothing.
        high_pass (float): The high-pass filter cutoff frequency.
        low_pass (float): The low-pass filter cutoff frequency.
        t_r (float): The repetition time (TR) of the fMRI data.
        standardize (bool): Whether to standardize the time series data.

    Returns:
        masker (NiftiLabelsMasker): The masker object.
    """
    masker = MultiNiftiLabelsMasker(labels_img=atlas_filename, smoothing_fwhm=smoothing_fwhm, high_pass=high_pass, low_pass=low_pass, t_r=t_r, standardize=standardize)
    print('Masker object created.')
    return masker

def extract_timeseries(masker, fmri_files, regressors):
    """
    Extracts the time series data from fMRI data using a masker object.

    Parameters:
        masker (MultiNiftiLabelsMasker): The masker object.
        fmri_files (str or list): The filename(s) of the fMRI data for multiple subjects.
        regressors (pandas.DataFrame, optional): The confounds dataframe.

    Returns:
        time_series_list (list): The extracted time series data for each subject.
    """
    time_series_list = masker.fit_transform(fmri_files, confounds=regressors)
    
    return time_series_list

def extract_timeseries_for_roi(
    timeseries_list,
    pseudo_idx_auditory,
    pseudo_idx_visual,
    pseudo_idx_motor,
    pseudo_idx_dmn,
    pseudo_idx_fpn,
    pseudo_idx_salience,
    pseudo_idx_limbic,
    subjects,
    group_name
):
    """
    Extracts time series data for voxels in unimodal and transmodal brain regions.

    Parameters:
        timeseries_list (list): List of time series data for each subject
        pseudo_idx_auditory (list): Indices for auditory cortex voxels
        pseudo_idx_visual (list): Indices for visual cortex voxels  
        pseudo_idx_motor (list): Indices for motor cortex voxels
        pseudo_idx_dmn (list): Indices for default mode network voxels
        pseudo_idx_fpn (list): Indices for frontoparietal network voxels
        pseudo_idx_salience (list): Indices for salience network voxels
        pseudo_idx_limbic (list): Indices for limbic system voxels
        subjects (list): List of subject IDs
        group_name (str): Name of the subject group (e.g. "HC", "MDD", "SZ")

    Returns:
        dict: Dictionary containing time series data for each subject and region.
              Structure is {subject_id: {'region': timeseries_array}} where regions are
              'auditory', 'visual', 'motor', 'dmn', 'fpn', 'salience', and 'limbic'.
    """
    time_series_dict = {}
    for i, ts in enumerate(timeseries_list):
        subject = subjects[i]
        auditory_timeseries = ts[:, pseudo_idx_auditory]
        visual_timeseries = ts[:, pseudo_idx_visual]
        motor_timeseries = ts[:, pseudo_idx_motor]
        dmn_timeseries = ts[:, pseudo_idx_dmn]
        fpn_timeseries = ts[:, pseudo_idx_fpn]
        salience_timeseries = ts[:, pseudo_idx_salience]
        limbic_timeseries = ts[:, pseudo_idx_limbic]
        time_series_dict[subject] = {
            'auditory': auditory_timeseries,
            'visual': visual_timeseries,
            'motor': motor_timeseries,
            'dmn': dmn_timeseries,
            'fpn': fpn_timeseries,
            'salience': salience_timeseries,
            'limbic': limbic_timeseries
        }
        print(f'Time series for {subject} ({group_name}): auditory shape {auditory_timeseries.shape}, '
              f'visual shape {visual_timeseries.shape}, motor shape {motor_timeseries.shape}, '
              f'dmn shape {dmn_timeseries.shape}, fpn shape {fpn_timeseries.shape}, '
              f'salience shape {salience_timeseries.shape}, limbic shape {limbic_timeseries.shape}')
    return time_series_dict
