import os
import csv
import numpy as np
import nibabel as nib

from decomposition_utils import create_matrix_structure

def export_to_csv(data, output_directory):
    """
    Export matrices to CSV files.

    Parameters:
    data (dict): Dictionary of matrices.
    output_directory (str): Directory to save CSV files.
    """
    os.makedirs(output_directory, exist_ok=True)
    for z in data.keys():
        for x in data[z].keys():
            filename = f"{output_directory}/slice_z{z}_x{x}.csv"
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data[z][x])
    print(f"Data exported to {output_directory}")

def import_from_csv(output_directory, z_range=None):
    """
    Import matrices from CSV files.

    Parameters:
    output_directory (str): Directory to load CSV files from.
    z_range (range, optional): Range of z values to include.

    Returns:
    dict: Dictionary of matrices.
    """
    data = create_matrix_structure(volumes_4d, z_range=z_range)
    for z in data.keys():
        for x in data[z].keys():
            filename = f"{output_directory}/slice_z{z}_x{x}.csv"
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                data[z][x] = [list(map(float, row)) for row in reader]
    return data

def save_as_nifti(data, output_directory, t_dim, x_dim, y_dim, z_dim):
    """
    Save matrices as NIFTI files.

    Parameters:
    data (dict): Dictionary of matrices.
    output_directory (str): Directory to save NIFTI files.
    t_dim (int): Time dimension.
    x_dim (int): X dimension.
    y_dim (int): Y dimension.
    z_dim (int): Z dimension.
    """
    os.makedirs(output_directory, exist_ok=True)
    for t in range(t_dim):
        component_3d_L = np.zeros((z_dim, x_dim, y_dim))
        component_3d_S = np.zeros((z_dim, x_dim, y_dim))
        for z in range(z_dim):
            for x in range(x_dim):
                if x in data[z]:
                    component_3d_L[z, x, :] = np.array(data[z][x])[:, t]
                    component_3d_S[z, x, :] = np.array(data[z][x])[:, t]
                else:
                    print(f"Missing data for z={z}, x={x}")

        nifti_img_L = nib.Nifti1Image(component_3d_L, np.eye(4))
        filename_L = f"C{t}_3D_L.nii.gz"
        nib.save(nifti_img_L, os.path.join(output_directory, filename_L))
        
        nifti_img_S = nib.Nifti1Image(component_3d_S, np.eye(4))
        filename_S = f"C{t}_3D_S.nii.gz"
        nib.save(nifti_img_S, os.path.join(output_directory, filename_S))
        
        print(f"Saved component {t} as NIFTI file: {filename_L}")
        print(f"Saved component {t} as NIFTI file: {filename_S}")
