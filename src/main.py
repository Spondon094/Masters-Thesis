"""
Main script for loading data, computing optical flow, and visualizing results.
"""

import os
from data_loader import load_nifti_files
from flow_computation import parallel_compute_flow, save_flow_data
from flow_visualization import draw_flow_3d, plot_mean_flow_magnitudes
import numpy as np

def main():
    # Define folder paths
    nifti_folder = 'output/nifti_S_full'
    flow_output_path = 'output/flows_farneback.pkl'
    output_folder_visuals = 'output/flow_visualizations_farneback'

    # Load NIFTI data
    nifti_data = load_nifti_files(nifti_folder)

    # Prepare slice pairs
    slice_pairs = [(nifti_data[t][:, :, z], nifti_data[t + 1][:, :, z]) 
                   for t in range(len(nifti_data) - 1) for z in range(nifti_data[0].shape[2])]

    # Compute optical flows in parallel
    flows = parallel_compute_flow(slice_pairs)

    # Save flow data
    save_flow_data(flows, flow_output_path)

    # Calculate and visualize mean flow magnitudes
    flow_magnitudes = [np.linalg.norm(flow, axis=2) for flow in flows]
    mean_flow_magnitudes = [np.mean(mag) for mag in flow_magnitudes]

    # Plot the smoothed mean flow magnitudes
    plot_mean_flow_magnitudes(mean_flow_magnitudes, output_folder_visuals)

    # Draw 3D visualization of the flow
    draw_flow_3d(flows, output_folder_visuals)

if __name__ == "__main__":
    main()