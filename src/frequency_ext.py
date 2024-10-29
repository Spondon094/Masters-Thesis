import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.signal import detrend
from .filter import bandpass_filter

def extract_breathing_frequency_wavelet(nifti_files, save_directory_breathing):
    """
    Extracts the breathing frequency from the NIfTI files using FFT-based frequency analysis.

    Parameters:
    nifti_files (list): List of NIfTI files to be processed.
    save_directory_breathing (str): Directory to save the extracted frequency.

    Returns:
    float: Estimated breathing frequency in Hz.
    """
    for nifti_file in nifti_files:
        S_nifti = nib.load(nifti_file)
        S_data = S_nifti.get_fdata()

        # Detrend data along the time axis
        S_data = detrend(S_data, axis=2)

        # Define filter parameters
        fs = 1 / 3.0  # Sampling rate of 1 sample every 3 seconds
        lowcut, highcut = 0.15, 0.5  # Frequency band in Hz

        # Apply bandpass filter to isolate breathing frequency
        S_data_filtered = bandpass_filter(S_data, lowcut=lowcut, highcut=highcut, fs=fs)

        # Perform FFT and calculate the magnitude
        S_fft = np.fft.fft(S_data_filtered, axis=2)
        S_fft_magnitude = np.abs(S_fft)
        freqs = np.fft.fftfreq(S_fft.shape[2], d=3.0)

        # Plot the frequency spectrum
        plt.figure()
        plt.plot(freqs, S_fft_magnitude.mean(axis=(0, 1)))
        plt.title('Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
        plt.show()

        # Find the peak frequency corresponding to breathing
        breathing_freq_index = np.argmax(S_fft_magnitude.mean(axis=(0, 1)))
        breathing_freq = freqs[breathing_freq_index]
        print(f'Breathing frequency: {breathing_freq} Hz')

        # Save the breathing frequency
        np.save(os.path.join(save_directory_breathing, 'breathing_frequency.npy'), breathing_freq)
        return breathing_freq