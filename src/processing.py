import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import pywt
from skimage.metrics import structural_similarity as ssim

def visualize_and_save_components_wavelet(nifti_files, breathing_freq, save_directory_breathing):
    """
    Performs wavelet decomposition on NIfTI files to isolate and visualize breathing and non-breathing components.

    Parameters:
    nifti_files (list): List of NIfTI files to be processed.
    breathing_freq (float): The calculated breathing frequency.
    save_directory_breathing (str): Directory to save the decomposed components.

    Returns:
    None
    """
    for i, nifti_file in enumerate(nifti_files):
        S_nifti = nib.load(nifti_file)
        S_data = S_nifti.get_fdata()

        # Perform Wavelet Transform
        coeffs = pywt.wavedec(S_data, 'db4', level=3, axis=2)
        S_periodic = pywt.waverec(coeffs[:2], 'db4', axis=2)
        S_non_periodic = S_data - np.pad(S_periodic, ((0, 0), (0, 0), (0, S_data.shape[2] - S_periodic.shape[2])), 'constant')

        # Save the decomposed components
        np.save(os.path.join(save_directory_breathing, f'S_periodic_wavelet_{i}.npy'), S_periodic)
        np.save(os.path.join(save_directory_breathing, f'S_non_periodic_wavelet_{i}.npy'), S_non_periodic)

        # Visualization
        plt.figure()
        plt.subplot(1, 3, 1)
        plt.imshow(S_data.mean(axis=2), cmap='gray')
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(S_periodic.mean(axis=2), cmap='gray')
        plt.title('Breathing Motion')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(S_non_periodic.mean(axis=2), cmap='gray')
        plt.title('Non-Periodic Motion')
        plt.axis('off')
        plt.show()

        # Calculate and display SSIM for quality assessment
        ssim_periodic = ssim(S_data.mean(axis=2), S_periodic.mean(axis=2), data_range=S_data.mean(axis=2).max() - S_data.mean(axis=2).min())
        ssim_non_periodic = ssim(S_data.mean(axis=2), S_non_periodic.mean(axis=2), data_range=S_data.mean(axis=2).max() - S_data.mean(axis=2).min())
        
        print(f"Image {i}:")
        print(f"SSIM Original: 1.0")
        print(f"SSIM Periodic: {ssim_periodic}")
        print(f"SSIM Non-Periodic: {ssim_non_periodic}")

def load_and_visualize_components_wavelet(nifti_files, save_directory_breathing):
    """
    Loads and visualizes previously saved wavelet components for NIfTI files.

    Parameters:
    nifti_files (list): List of NIfTI files to be processed.
    save_directory_breathing (str): Directory where the decomposed components are saved.

    Returns:
    None
    """
    for i, nifti_file in enumerate(nifti_files):
        S_nifti = nib.load(nifti_file)
        S_data = S_nifti.get_fdata()

        # Load periodic and non-periodic components
        S_periodic = np.load(os.path.join(save_directory_breathing, f'S_periodic_wavelet_{i}.npy'))
        S_non_periodic = np.load(os.path.join(save_directory_breathing, f'S_non_periodic_wavelet_{i}.npy'))

        # Visualization
        plt.figure()
        plt.subplot(1, 3, 1)
        plt.imshow(S_data.mean(axis=2), cmap='gray')
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(S_periodic.mean(axis=2), cmap='gray')
        plt.title('Breathing Motion')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(S_non_periodic.mean(axis=2), cmap='gray')
        plt.title('Non-Periodic Motion')
        plt.axis('off')
        plt.show()

        # Calculate and display SSIM for quality assessment
        ssim_periodic = ssim(S_data.mean(axis=2), S_periodic.mean(axis=2), data_range=S_data.mean(axis=2).max() - S_data.mean(axis=2).min())
        ssim_non_periodic = ssim(S_data.mean(axis=2), S_non_periodic.mean(axis=2), data_range=S_data.mean(axis=2).max() - S_data.mean(axis=2).min())

        print(f"Image {i}:")
        print(f"SSIM Original: 1.0")
        print(f"SSIM Periodic: {ssim_periodic}")
        print(f"SSIM Non-Periodic: {ssim_non_periodic}")