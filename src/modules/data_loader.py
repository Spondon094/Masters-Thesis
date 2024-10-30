
"""
Module for loading NIFTI data.
"""

import nibabel as nib
import os

def load_nifti_data(nifti_folder):
    """
    Loads all NIFTI files from a specified folder and returns the data as a list.
    
    Args:
        nifti_folder (str): Path to the folder containing NIFTI files.
    
    Returns:
        tuple: A tuple containing:
            - nifti_data (list): A list with NIFTI image data for each time step.
            - time_steps (int): Number of time steps.
            - slices_per_time_step (int): Number of slices per time step.
    """
    nifti_files = sorted([f for f in os.listdir(nifti_folder) if f.endswith('.nii.gz')])
    nifti_data = [nib.load(os.path.join(nifti_folder, file)).get_fdata() for file in nifti_files]
    
    time_steps = len(nifti_data)
    slices_per_time_step = nifti_data[0].shape[2] if nifti_data else 0
    
    return nifti_data, time_steps, slices_per_time_step
