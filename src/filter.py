from scipy.signal import butter, filtfilt

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Applies a bandpass Butterworth filter to the data along the specified axis.

    Parameters:
    data (numpy.ndarray): The input data to be filtered.
    lowcut (float): The lower bound of the frequency to allow.
    highcut (float): The upper bound of the frequency to allow.
    fs (float): The sampling rate of the data.
    order (int, optional): The order of the Butterworth filter (default is 5).

    Returns:
    numpy.ndarray: The filtered data.
    """
    nyquist = 0.5 * fs
    low_normalized = lowcut / nyquist
    high_normalized = highcut / nyquist

    # Adjust frequency values if they are out of bounds
    if low_normalized <= 0:
        low_normalized = 1e-6
    if high_normalized >= 1:
        high_normalized = 1 - 1e-6

    b, a = butter(order, [low_normalized, high_normalized], btype='band')
    return filtfilt(b, a, data, axis=2)