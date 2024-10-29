import sys
import os
from dicom_utils import load_dicom_files, sort_datasets_by_time, group_volumes_by_time, create_4d_volumes,calculate_time_differences
from plot_utils import plot_acquisition_times, interactive_slice_viewer
from decomposition_utils import apply_ls_on_whole_volume
from nifti_utils import export_to_csv, import_from_csv, save_as_nifti

# directory containing the SVD module to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main():
    path = '../data/'
    dicom_datasets = load_dicom_files(path)
    sorted_datasets = sort_datasets_by_time(dicom_datasets)
    plot_acquisition_times(sorted_datasets)
    
    acquisition_times = [millis for _, millis in sorted_datasets]
    time_differences = calculate_time_differences(acquisition_times)
    print(time_differences)
    
    volumes_by_time = group_volumes_by_time(sorted_datasets)
    volumes_4d = create_4d_volumes(volumes_by_time)
    
    interactive_slice_viewer(volumes_4d)
    
    z_range = range(0, 5)
    L, S = apply_ls_on_whole_volume(volumes_4d, lambda_val=0.25, max_iters=1, z_range=z_range)
    
    output_directory_L1 = "output_L1"
    output_directory_S1 = "output_S1"
    export_to_csv(L, output_directory_L1)
    export_to_csv(S, output_directory_S1)
    
    L_imported = import_from_csv(output_directory_L1, z_range=range(0, z_range[-1]+1))
    S_imported = import_from_csv(output_directory_S1, z_range=range(0, z_range[-1]+1))
    
    t_dim = len(volumes_4d)
    z_dim = len(L.keys())
    x_dim = len(L[list(L.keys())[-1]].keys())
    y_dim = L[list(L.keys())[-1]][0].shape[0]
    
    save_as_nifti(L_imported, "output/nifti_L_full", t_dim, x_dim, y_dim, z_dim)
    save_as_nifti(S_imported, "output/nifti_S_full", t_dim, x_dim, y_dim, z_dim)

#if __name__ == "__main__":
   # main()
