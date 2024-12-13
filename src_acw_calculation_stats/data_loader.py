import nibabel as nib
from nilearn import datasets
import nibabel as nib
import pandas as pd

def load_fmri_data(data_dir, subjects, task):
    """
    Load fMRI data from a specified directory for a given list of subjects and task.

    Parameters:
    - data_dir (str): The directory path where the fMRI data is located.
    - subjects (list): List of subject identifiers.
    - task (str): The task identifier.

    Returns:
    - fmri_imgs (list): List of loaded fMRI data as Nifti1Image objects.
    """
    fmri_imgs = []

    for subject in subjects:
        # Construct data file path
        fmri_file = f'{data_dir}/{subject}/func/{subject}_task-{task}_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz'

        # Load the fMRI data using nibabel
        fmri_img = nib.load(fmri_file)

        # Print the shape of the loaded fMRI data
        print('Shape of fMRI data for subject', subject, ':', fmri_img.shape)

        fmri_imgs.append(fmri_img)

    return fmri_imgs
    
def load_regressors(data_dir, subjects, task):
    """
    Load and process regressors for multiple subjects.

    Args:
    - data_dir (str): Path to the root of the BIDS dataset.
    - subjects (list): List of subject IDs.
    - task (str): Name of the task.

    Returns:
    - regressors (list): List of arrays of regressor values for each subject.
    """
    regressors = []

    for subject_id in subjects:
        regressor_file_path = f'{data_dir}/{subject_id}/func/{subject_id}_task-{task}_desc-confounds_timeseries.tsv'

        regressor_df = pd.read_csv(regressor_file_path, delimiter='\t')
        desired_regressors = [
            "csf",
            "white_matter",
            "framewise_displacement",
            "trans_x",
            "trans_y",
            "trans_z",
            "rot_x",
            "rot_y",
            "rot_z",
            "a_comp_cor_00",
            "a_comp_cor_01",
            "a_comp_cor_02",
            "a_comp_cor_03",
            # "a_comp_cor_04",
            "cosine00",
            "cosine01"
        ]
        
        regressors.append(regressor_df[desired_regressors].fillna(0).to_numpy())

    return regressors
