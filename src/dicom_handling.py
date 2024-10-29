import os
import datetime
import pydicom
import random

def load_dicom_files(path):
    dicom_files = [f for f in os.listdir(path) if f.endswith('.dcm')]
    dicom_datasets = [pydicom.dcmread(os.path.join(path, f)) for f in dicom_files]
    return dicom_datasets

def convert_to_milliseconds(acquisition_time_str):
    time_str = acquisition_time_str[8:20]
    acquisition_time = datetime.datetime.strptime(time_str, '%H%M%S.%f')
    total_milliseconds = (acquisition_time.hour * 3600 + acquisition_time.minute * 60 + acquisition_time.second) * 1000 + acquisition_time.microsecond / 1000
    return total_milliseconds

def extract_acquisition_times(dicom_datasets):
    datasets_with_time = []
    for ds in dicom_datasets:
        if 'AcquisitionDateTime' in ds:
            millis = convert_to_milliseconds(ds.AcquisitionDateTime)
            datasets_with_time.append((ds, millis))
        else:
            print("Acquisition DateTime not found in the dataset.")
    return datasets_with_time

if __name__ == "__main__":
    path = '../data/'
    dicom_datasets = load_dicom_files(path)
    datasets_with_time = extract_acquisition_times(dicom_datasets)
    print(type(datasets_with_time))
    print(datasets_with_time[0])
