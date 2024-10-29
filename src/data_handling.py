import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, IntSlider
import os
import nibabel as nib

def calculate_time_differences(acquisition_times):
    initial_value = acquisition_times[0]
    time_differences = [time - initial_value for time in acquisition_times]
    return time_differences

def sort_slices_into_4d_volumes(sorted_datasets):
    volumes_by_time = defaultdict(list)
    for ds, _ in sorted_datasets:
        time_point = ds.get('AcquisitionDateTime', 'DefaultTime')
        volumes_by_time[time_point].append(ds.pixel_array)
    volumes_4d = {time_point: np.stack(slices) for time_point, slices in volumes_by_time.items()}
    return volumes_4d

def display_3d_volume(volumes_4d):

    first_volume_key = next(iter(volumes_4d))
    first_volume = volumes_4d[first_volume_key]
    frame_max = first_volume.shape[0] - 1
    slice_max = first_volume.shape[2] - 1

    def display_slice(frame_index, slice_index):
        volume = volumes_4d[first_volume_key]
        if volume.ndim == 4 and frame_index < volume.shape[0] and slice_index < volume.shape[1]:
            specific_slice = volume[frame_index, slice_index, :, :]
            plt.imshow(specific_slice, cmap='gray')
            plt.title(f"Frame {frame_index}, Slice {slice_index}")
            plt.axis('off')
            plt.show()
        else:
            print("Invalid frame or slice index.")

    interact(display_slice, frame_index=IntSlider(min=0, max=frame_max, step=1, value=0), slice_index=IntSlider(min=0, max=slice_max, step=1, value=0))

def flatten_volumes(volumes_4d):
    flattened_volumes = []
    for time_point, volume_3d in volumes_4d.items():
        for frame_index in range(volume_3d.shape[0]):
            flattened_volume = volume_3d[frame_index].flatten()
            flattened_volumes.append(flattened_volume)
    return flattened_volumes

def perform_svd(matrix_for_svd):
    U, S, VT = np.linalg.svd(matrix_for_svd, full_matrices=False)
    return U, S, VT

def save_3d_volumes_as_nifti(VT, output_directory="nifti_com1/"):
    

    z_dim = 60   
    x_dim = 128  
    y_dim = 128  

    os.makedirs(output_directory, exist_ok=True)
    num_components = VT.shape[0]
    for i in range(num_components):
        component_3d = VT[i].reshape((z_dim, x_dim, y_dim))
        nifti_img = nib.Nifti1Image(component_3d, np.eye(4))
        filename = f"C{i}_3D.nii.gz"
        nib.save(nifti_img, os.path.join(output_directory, filename))
        print(f"Saved component {i} as NIFTI file: {filename}")
