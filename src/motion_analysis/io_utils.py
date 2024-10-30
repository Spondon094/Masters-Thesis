"""
Utility functions for loading, saving, and processing NIFTI files and CSV outputs.
"""

import os
import nibabel as nib
import pandas as pd

def load_nifti_data(file_path):
    """
    Loads NIFTI data from a given file path.

    Parameters:
        file_path (str): Path to the NIFTI file.

    Returns:
        numpy.ndarray: Loaded data array.
    """
    nifti_img = nib.load(file_path)
    return nifti_img.get_fdata()

def save_nifti_data(data, output_folder, filename):
    """
    Saves NIFTI data to the specified output folder.

    Parameters:
        data (numpy.ndarray): Image data to save.
        output_folder (str): Folder to save the data in.
        filename (str): Name for the output NIFTI file.
    """
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    nifti_img = nib.Nifti1Image(data, affine=np.eye(4))
    nib.save(nifti_img, output_path)

def save_csv(folder, filename, data_list):
    """
    Saves a list of data to a CSV file.

    Parameters:
        folder (str): Folder to save the CSV.
        filename (str): Name for the CSV file.
        data_list (list): List of data to save in the CSV file.
    """
    os.makedirs(folder, exist_ok=True)
    data_df = pd.DataFrame(data_list, columns=['Value'])
    output_path = os.path.join(folder, filename)
    data_df.to_csv(output_path, index=False)