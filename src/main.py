"""
Main script for conducting motion analysis on 3D NIFTI files.

This script loads a series of NIFTI files, applies B-spline nonlinear warping, calculates the motion
magnitude in millimeters (mm), and stores the results in CSV files. It also generates a comparative
plot of original and warped motion values.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from motion_analysis.bspline_warp import apply_bspline_warping
from motion_analysis.motion_calc import calculate_motion_magnitude
from motion_analysis.io_utils import load_nifti_data, save_nifti_data, save_csv

# Directory setup
ls_nifti_folder = 'output/nifti_S_full'
nonlinear_warped_folder = 'output/nonlinear_warped_nifti'
csv_output_folder = 'output/nonlinear_motion_values'
os.makedirs(nonlinear_warped_folder, exist_ok=True)
os.makedirs(csv_output_folder, exist_ok=True)

# NIFTI filenames for processing
nifti_filenames = [
    'C2_3D_S.nii.gz', 'C5_3D_S.nii.gz', 'C8_3D_S.nii.gz', # Continue with the list...
]

# Spacing metadata
pixel_spacing = [3.125, 3.125]  # X and Y pixel spacing
slice_thickness = 3.1           # Z-axis slice thickness

# Motion values lists
original_motion_values = []
nonlinear_warped_motion_values = []

# Loop through NIFTI files to calculate motion
for i in range(len(nifti_filenames)):
    moving_file = os.path.join(ls_nifti_folder, nifti_filenames[i])
    original_motion = calculate_motion_magnitude(moving_file, pixel_spacing, slice_thickness)
    original_motion_values.append(original_motion)

    # Only warp after the first time step
    if i > 0:
        reference_file = os.path.join(ls_nifti_folder, nifti_filenames[i - 1])
        warped_data = apply_bspline_warping(moving_file, reference_file)
        save_nifti_data(warped_data, nonlinear_warped_folder, nifti_filenames[i])

        warped_motion = calculate_motion_magnitude(warped_data, pixel_spacing, slice_thickness)
        nonlinear_warped_motion_values.append(warped_motion)
    else:
        nonlinear_warped_motion_values.append(None)  # First time step has no warping

# Save motion values
save_csv(csv_output_folder, 'original_motion_values_mm.csv', original_motion_values)
save_csv(csv_output_folder, 'nonlinear_warped_motion_values_mm.csv', nonlinear_warped_motion_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(original_motion_values, label='Original Motion (mm)', marker='o')
plt.plot(nonlinear_warped_motion_values, label='Warped Motion (mm)', marker='x')
plt.xlabel('Time Step')
plt.ylabel('Motion Magnitude (mm)')
plt.title('Motion Comparison (Original vs. Nonlinear Warped)')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(csv_output_folder, 'motion_comparison_plot.png'))
plt.show()