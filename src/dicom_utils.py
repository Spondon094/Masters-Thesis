import os, sys
import datetime
import pydicom

def load_dicom_files(path):
    """
    Load all DICOM files from the specified directory.

    Parameters:
    path (str): The directory path where DICOM files are stored.

    Returns:
    list: List of DICOM datasets.
    """
    dicom_files = [f for f in os.listdir(path) if f.endswith('.dcm')]
    dicom_datasets = [pydicom.dcmread(os.path.join(path, f)) for f in dicom_files]
    return dicom_datasets

def calculate_time_differences(acquisition_times):
    """
    Calculate time differences from the initial acquisition time.

    Parameters:
    acquisition_times (list): List of acquisition times in milliseconds.

    Returns:
    list: Time differences in milliseconds.
    """
    initial_value = acquisition_times[0]
    time_differences = [time - initial_value for time in acquisition_times]
    return time_differences


def convert_to_milliseconds(acquisition_time_str):
    """
    Convert DICOM Acquisition DateTime to milliseconds.

    Parameters:
    acquisition_time_str (str): Acquisition DateTime string in the format YYYYMMDDHHMMSS.FFFFFF.

    Returns:
    float: Time in milliseconds.
    """
    time_str = acquisition_time_str[8:20]
    acquisition_time = datetime.datetime.strptime(time_str, '%H%M%S.%f')
    total_milliseconds = (acquisition_time.hour * 3600 + acquisition_time.minute * 60 + acquisition_time.second) * 1000 + acquisition_time.microsecond / 1000
    return total_milliseconds

def sort_datasets_by_time(dicom_datasets):
    """
    Sort DICOM datasets by Acquisition DateTime.

    Parameters:
    dicom_datasets (list): List of DICOM datasets.

    Returns:
    list: Sorted list of tuples (dataset, milliseconds).
    """
    datasets_with_time = []
    for ds in dicom_datasets:
        if 'AcquisitionDateTime' in ds:
            millis = convert_to_milliseconds(ds.AcquisitionDateTime)
            datasets_with_time.append((ds, millis))
        else:
            print("Acquisition DateTime not found in the dataset.")
    sorted_datasets = sorted(datasets_with_time, key=lambda x: x[1])
    return sorted_datasets

def group_volumes_by_time(sorted_datasets):
    """
    Group DICOM slices by acquisition time points.

    Parameters:
    sorted_datasets (list): Sorted list of tuples (dataset, milliseconds).

    Returns:
    dict: Dictionary with time points as keys and list of pixel arrays as values.
    """
    from collections import defaultdict
    volumes_by_time = defaultdict(list)
    for ds, _ in sorted_datasets:
        time_point = ds.get('AcquisitionDateTime', 'DefaultTime')
        volumes_by_time[time_point].append(ds.pixel_array)
    return volumes_by_time

def create_4d_volumes(volumes_by_time):
    """
    Create 4D volumes from grouped DICOM slices.

    Parameters:
    volumes_by_time (dict): Dictionary with time points as keys and list of pixel arrays as values.

    Returns:
    dict: Dictionary with time points as keys and 4D volumes as values.
    """
    import numpy as np
    volumes_4d = {time_point: np.stack(slices) for time_point, slices in volumes_by_time.items()}
    return volumes_4d
