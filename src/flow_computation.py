"""
Module for computing optical flow using Farneback's method and saving results.
"""

import cv2
import numpy as np
import pickle
import multiprocessing as mp

def compute_optical_flow_farneback(slice_pair):
    """
    Computes optical flow between two image slices using Farneback's method.

    Args:
        slice_pair (tuple): Pair of consecutive image slices (slice_t, slice_t1).

    Returns:
        ndarray: Optical flow data between the slices.
    """
    slice_t, slice_t1 = slice_pair
    flow = cv2.calcOpticalFlowFarneback(slice_t.astype(np.float32), slice_t1.astype(np.float32), None, 
                                        0.5, 3, 15, 3, 5, 1.2, 0)
    return flow

def parallel_compute_flow(slice_pairs):
    """
    Uses multiprocessing to parallelize optical flow computation across slice pairs.

    Args:
        slice_pairs (list): List of slice pairs to compute optical flow.

    Returns:
        list: List of computed flow data for each slice pair.
    """
    with mp.Pool(mp.cpu_count()) as pool:
        flows = pool.map(compute_optical_flow_farneback, slice_pairs)
    return flows

def save_flow_data(flows, output_path):
    """
    Saves computed flow data to a file using pickle.

    Args:
        flows (list): List of computed flow data.
        output_path (str): Path to save the pickle file.
    """
    with open(output_path, 'wb') as f:
        pickle.dump(flows, f)