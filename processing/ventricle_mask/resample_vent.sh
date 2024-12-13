# Set up variables
ventricle_mask_path="/Users/fdjim/Desktop/PDS_CODE/ventricle_mask/aparc.a2009s+aseg_REN_vent.nii.gz"
output_path="/Users/fdjim/Desktop/PDS_CODE/ventricle_mask"

3dresample -dxyz 3 3 3 -inset ${ventricle_mask_path} \
            -prefix ${output_path}/template_ventricle_3mm \

3drefit -space MNI -view tlrc  ${output_path}/template_ventricle_3mm+orig