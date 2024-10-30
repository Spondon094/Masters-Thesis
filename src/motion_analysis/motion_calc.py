"""
Calculates the motion magnitude in millimeters.

This module computes motion by taking into account voxel dimensions from metadata.
"""

import numpy as np
import nibabel as nib

def calculate_motion_magnitude(nifti_file, pixel_spacing, slice_thickness):
    """
    Calculates the motion magnitude in millimeters from a NIFTI file.

    Parameters:
        nifti_file (str): Path to the NIFTI file.
        pixel_spacing (list): Pixel spacing in X and Y directions.
        slice_thickness (float): Slice thickness in Z direction.

    Returns:
        float: Calculated motion magnitude in millimeters.
    """
    nifti_img = nib.load(nifti_file)
    nifti_data = nifti_img.get_fdata()
    
    voxel_volume = np.prod([*pixel_spacing, slice_thickness])
    motion_magnitude = np.linalg.norm(nifti_data) * voxel_volume
    
    return motion_magnitude