
"""
Module for loading NIFTI data files and preparing them for optical flow analysis.
"""

import os
import nibabel as nib

def load_nifti_files(nifti_folder):
    """
    Loads NIFTI files from a specified folder.

    Args:
        nifti_folder (str): Path to the folder containing NIFTI files.

    Returns:
        list: List of NIFTI data arrays, each representing a time step.
    """
    nifti_files = sorted([f for f in os.listdir(nifti_folder) if f.endswith('.nii.gz')])
    nifti_data = []

    for nifti_file in nifti_files:
        file_path = os.path.join(nifti_folder, nifti_file)
        img = nib.load(file_path)
        nifti_data.append(img.get_fdata())
    
    return nifti_data
