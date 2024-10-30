"""
Module for saving optical flow results and computed magnitudes.
"""

import pickle
import numpy as np

def save_optical_flow_data(flows, output_path):
    """
    Saves computed optical flow data to a file.
    
    Args:
        flows (list): List of optical flow results.
        output_path (str): Path where the file will be saved.
    """
    with open(output_path, 'wb') as f:
        pickle.dump(flows, f)
    print(f"Optical flow data saved to {output_path}")

def save_mean_flow_per_time_step(flows, slices_per_time_step, time_steps, output_path):
    """
    Computes and saves mean flow magnitude per time step to a CSV file.
    
    Args:
        flows (list): List of optical flow results.
        slices_per_time_step (int): Number of slices per time step.
        time_steps (int): Number of time steps.
        output_path (str): Path to the CSV output file.
    """
    flow_magnitudes = [np.linalg.norm(flow, axis=2) for flow in flows]
    mean_flow_magnitude = [np.mean(magnitude) for magnitude in flow_magnitudes][:time_steps * slices_per_time_step]
    
    # Group magnitudes by time step
    mean_per_time_step = [np.mean(mean_flow_magnitude[i * slices_per_time_step:(i + 1) * slices_per_time_step])
                          for i in range(time_steps)]
    
    np.savetxt(output_path, mean_per_time_step, delimiter=",")
    print(f"Mean flow magnitudes per time step saved to {output_path}")