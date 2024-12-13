#!/bin/bash

# Inputs
SUBJECTS=sub-030P
BIDS_DIR=/Users/fdjim/Desktop/PDS_FULL
nthreads=10
mem=16 #gb
container=docker #docker or singularity

# Convert virtual memory from gb to mb
mem=`echo "${mem//[!0-9]/}"`
mem_mb=`echo $(((mem*1000)-5000))`

export TEMPLATEFLOW_HOME=$HOME/.cache/templateflow
export FS_LICENSE=/Users/fdjim/Desktop/Research/PDS_GN/derivatives/license.txt

# Loop through subjects
for SUB in "${SUBJECTS[@]}"; do
    echo "Processing subject: $SUB"
    # Set subject-specific directories
    OUTPUT_DIR=/Users/fdjim/Desktop/PDS_CODE/tmp/workflow_${SUB}/derivatives 
    WORK_DIR=/Users/fdjim/Desktop/PDS_CODE/tmp/workflow_${SUB}/work

    # Run fmriprep
    if [ $container == singularity ]; then
        unset PYTHONPATH; singularity run -B $HOME/.cache/templateflow:/opt/templateflow $HOME/fmriprep.simg \
            $BIDS_DIR $OUTPUT_DIR \
            participant \
            --participant-label $SUB \
            --skip-bids-validation \
            --md-only-boilerplate \
            --fs-license-file $FREESURFER_HOME/license.txt \
            --fs-no-reconall \
            --output-spaces MNI152NLin2009cAsym:res-2 \
            --nthreads $nthreads \
            --stop-on-first-crash \
            --mem_mb $mem_mb \
            -w $HOME
    else
        fmriprep-docker $BIDS_DIR $OUTPUT_DIR \
            participant \
            --participant-label $SUB \
            --skip-bids-validation \
            --md-only-boilerplate \
            --fs-license-file /Users/fdjim/Desktop/Research/FreeSurfer/license.txt \
            --fs-no-reconall \
            --output-spaces MNI152NLin2009cAsym:res-2 \
            --nthreads $nthreads \
            --stop-on-first-crash \
            --mem_mb $mem_mb \
            -w $WORK_DIR
    fi

    echo "Finished processing subject: $SUB"
done

echo "All subjects processed"