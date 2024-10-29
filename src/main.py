import sys
import os
import numpy as np
from dicom_handling import extract_acquisition_times, load_dicom_files, convert_to_milliseconds
from data_handling import (calculate_time_differences, sort_slices_into_4d_volumes, 
                           display_3d_volume, flatten_volumes, perform_svd, save_3d_volumes_as_nifti)
from plotting import plot_acquisition_times, plot_singular_values, plot_temporal_patterns, smooth_and_plot_patterns

# Main code execution
path = '../data/'  # Adjust this to the directory where your DICOM files are located
dicom_datasets = load_dicom_files(path)  # Load all DICOM files
datasets_with_time = extract_acquisition_times(dicom_datasets)  # Extract acquisition times
sorted_datasets = sorted(datasets_with_time, key=lambda x: x[1])  # Sort datasets by acquisition time

# Display acquisition times for debugging purposes
for ds, millis in sorted_datasets:
    print(f"Acquisition Time: {ds.AcquisitionDateTime}, Milliseconds: {millis}")

# Get the list of acquisition times
acquisition_times = [millis for _, millis in sorted_datasets]
plot_acquisition_times(acquisition_times)  # Plot the acquisition times

# Calculate time differences between acquisitions
time_differences = calculate_time_differences(acquisition_times)

# Sort slices into 4D volumes
volumes_4d = sort_slices_into_4d_volumes(sorted_datasets)
display_3d_volume(volumes_4d)  # Optionally display a 3D volume for verification

# Flatten the volumes to prepare for SVD (i.e., convert the 4D volumes into a 2D matrix)
flattened_volumes = flatten_volumes(volumes_4d)
matrix_for_svd = np.vstack(flattened_volumes)  # Stack the volumes to create a matrix

# Perform Singular Value Decomposition (SVD)
U, S, VT = perform_svd(matrix_for_svd)

# Plot the singular values
plot_singular_values(S)

# Plot the temporal patterns (left-singular vectors in U matrix)
plot_temporal_patterns(U, time_differences)

# Threshold to retain significant singular values
threshold = 0.01  # Define a threshold (you can adjust this value based on your data)
significant_singular_values = S[S > threshold]  # Retain singular values above the threshold

print(f"Number of significant singular values retained: {len(significant_singular_values)}")

# Retain only the significant components based on the threshold
retained_U = U[:, :len(significant_singular_values)]
retained_S = S[:len(significant_singular_values)]
retained_VT = VT[:len(significant_singular_values), :]

# Averaging and noise addition for the U matrix to smooth temporal patterns
U_averaged_noised = np.zeros_like(U)
for i in range(0, U.shape[0], 3):
    avg = np.mean(U[i:i+3], axis=0)
    noise = np.random.normal(0, 0.0005, avg.shape)
    avg_noised = avg + noise
    U_averaged_noised[i:i+3] = np.tile(avg_noised, (3, 1))

# Smooth and plot the modified temporal patterns
smooth_and_plot_patterns(U_averaged_noised, time_differences, significant_singular_values)

# Save the 3D volumes (after applying SVD) as NIfTI files
save_3d_volumes_as_nifti(retained_VT)
