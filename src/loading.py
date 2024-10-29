import os
import numpy as np

def load_breathing_frequency_wavelet(save_directory_breathing):
    """
    Loads the saved breathing frequency from a file.

    Parameters:
    save_directory_breathing (str): Directory where the breathing frequency file is saved.

    Returns:
    float: The loaded breathing frequency.
    """
    breathing_freq_path = os.path.join(save_directory_breathing, 'breathing_frequency.npy')
    breathing_freq = np.load(breathing_freq_path)
    print(f'Loaded Breathing frequency: {breathing_freq} Hz')
    return breathing_freq