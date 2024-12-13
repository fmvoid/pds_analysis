#!/bin/bash

# Inputs
SUBJECTS=(sub-030P)  # Add more subjects to this array if needed
BIDS_DIR=/Users/fdjim/Desktop/PDS_FULL  # Path to your BIDS dataset
AFNI_CODE_DIR=/Users/fdjim/Desktop/PDS_CODE  # Path to store AFNI working directories
VENT_TEMPLATE=/Users/fdjim/Desktop/PDS_CODE/ventricle_mask/template_ventricle_3mm+tlrc
nthreads=10  # Number of threads for parallel processing

# Loop through subjects
for SUB in "${SUBJECTS[@]}"; do
    echo "Processing subject: $SUB"

    # Set subject-specific directories
    OUTPUT_DIR=${BIDS_DIR}/derivatives/afni_${SUB}  # Output directory in the derivatives folder
    WORK_DIR=${AFNI_CODE_DIR}/tmp/workflow_${SUB}/work  # Working directory

    # Create necessary directories if they don't exist
    mkdir -p $OUTPUT_DIR $WORK_DIR

    # Find subject's anatomical and functional data in BIDS format
    ANAT_FILE=$(find $BIDS_DIR/$SUB/anat -name "*_T1w.nii" | head -n 1)  # Anatomical scan
    FUNC_FILES=$(find $BIDS_DIR/$SUB/func -name "*_bold.nii")  # Functional runs (BOLD data)

    if [ -z "$ANAT_FILE" ] || [ -z "$FUNC_FILES" ]; then
        echo "Error: Could not find anatomical or functional data for $SUB"
        continue
    fi

    # Run afni_proc.py for the current subject
    afni_proc.py \
        -subj_id $SUB \
        -blocks despike tshift align tlrc volreg blur mask scale regress \
        -radial_correlate_blocks tcat volreg regress \
        -copy_anat $ANAT_FILE \
        -anat_has_skull yes \
        -dsets $FUNC_FILES \
        -tcat_remove_first_trs 2 \
        -align_unifize_epi local \
        -align_opts_aea -cost lpc+ZZ -giant_move -check_flip \
        -tlrc_base MNI152_2009_template_SSW.nii.gz \
        -tlrc_NL_warp \
        -volreg_align_to MIN_OUTLIER \
        -volreg_align_e2a \
        -volreg_tlrc_warp \
        -volreg_warp_dxyz 3 \
        -blur_size 4 \
        -mask_segment_anat yes \
        -mask_segment_erode yes \
        -mask_import Tvent ${VENT_TEMPLATE} \
        -mask_intersect Svent CSFe Tvent \
        -mask_epi_anat yes \
        -regress_apply_mot_types demean deriv \
        -regress_motion_per_run \
        -regress_anaticor_fast \
        -regress_ROI_PC Svent 3 \
        -regress_ROI_PC_per_run Svent \
        -regress_censor_motion 0.2 \
        -regress_censor_outliers 0.05 \
        -regress_make_corr_vols WMe Svent \
        -regress_est_blur_epits \
        -regress_est_blur_errts \
        -regress_run_clustsim yes \
        -html_review_style pythonic \
        -bash \
        -execute

    echo "Finished processing subject: $SUB"
done

echo "All subjects processed"