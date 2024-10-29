import os
from processing.frequency_extraction import extract_breathing_frequency_wavelet
from processing.visualization import visualize_and_save_components_wavelet, load_and_visualize_components_wavelet
from processing.loading import load_breathing_frequency_wavelet

# Directory configurations
nifti_directory = 'output/nifti_S_full'
save_directory_breathing = 'output/processed_breathing_data'
os.makedirs(save_directory_breathing, exist_ok=True)

# Load files
nifti_files = sorted([os.path.join(nifti_directory, f) for f in os.listdir(nifti_directory) if f.endswith('.nii.gz')])

# Extract, visualize, and save components
breathing_freq = extract_breathing_frequency_wavelet(nifti_files, save_directory_breathing)
visualize_and_save_components_wavelet(nifti_files, breathing_freq, save_directory_breathing)
loaded_breathing_freq = load_breathing_frequency_wavelet(save_directory_breathing)
load_and_visualize_components_wavelet(nifti_files, save_directory_breathing)