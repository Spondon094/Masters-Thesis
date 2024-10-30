
"""
Module for computing optical flow between consecutive slices.
"""

import numpy as np
import cv2
import multiprocessing as mp

def compute_optical_flows(nifti_data):
    """
    Computes TV-L1 optical flow between consecutive slices in the NIFTI dataset.
    
    Args:
        nifti_data (list): List containing NIFTI data arrays for each time step.
    
    Returns:
        list: A list of optical flow results between consecutive time steps.
    """
    optical_flow = cv2.optflow.DualTVL1OpticalFlow_create()
    time_steps = len(nifti_data)
    slices_per_time_step = nifti_data[0].shape[2]
    
    # Prepare pairs of slices between consecutive time steps
    slice_pairs = [(nifti_data[t][:, :, z], nifti_data[t + 1][:, :, z]) 
                   for t in range(time_steps - 1) for z in range(slices_per_time_step)]
    
    def compute_flow(slice_pair):
        return optical_flow.calc(slice_pair[0].astype(np.float32), slice_pair[1].astype(np.float32), None)
    
    with mp.Pool(mp.cpu_count()) as pool:
        flows = pool.map(compute_flow, slice_pairs)
    
    return flows
