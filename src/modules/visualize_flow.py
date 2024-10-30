"""
Module for visualizing optical flow and plotting flow magnitudes over time steps.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import os

def draw_flow(slice_img, flow, step=16):
    """
    Draws optical flow vectors on a slice image.
    
    Args:
        slice_img (ndarray): Image slice.
        flow (ndarray): Optical flow data.
        step (int): Step size for sampling flow vectors.
    
    Returns:
        ndarray: Visualization with flow vectors overlaid.
    """
    h, w = slice_img.shape
    y, x = np.mgrid[step//2:h:step, step//2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    
    vis = cv2.cvtColor(slice_img.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    for (x1, y1), (x2, y2) in lines:
        cv2.arrowedLine(vis, (x1, y1), (x2, y2), (0, 255, 0), 1, cv2.LINE_AA)
    return vis

def visualize_and_save_flows(flows, nifti_data, output_dir, resize_factor=2):
    """
    Visualizes and saves optical flow results.
    """
    os.makedirs(output_dir, exist_ok=True)
    for i, (flow, slice_img) in enumerate(zip(flows, [nifti_data[t][:, :, 0] for t in range(len(nifti_data) - 1)])):
        vis = draw_flow(slice_img, flow)
        resized_vis = cv2.resize(vis, (int(vis.shape[1] * resize_factor), int(vis.shape[0] * resize_factor)))
        cv2.imwrite(f"{output_dir}/flow_{i:03d}.png", resized_vis)
    print(f"Flow visualizations saved in {output_dir}")

def plot_smoothed_mean_magnitudes(mean_flow_csv, output_dir, sigma=1):
    """
    Plots and saves smoothed mean flow magnitude over time steps.
    
    Args:
        mean_flow_csv (str): Path to mean flow magnitude CSV file.
        output_dir (str): Directory to save plot.
        sigma (float): Smoothing parameter for Gaussian filter.
    """
    os.makedirs(output_dir, exist_ok=True)
    data = np.loadtxt(mean_flow_csv, delimiter=',')
    smoothed_data = gaussian_filter1d(data, sigma=sigma)
    
    plt.plot(smoothed_data, label='Smoothed Data (Gaussian)')
    plt.xlabel('Time Step')
    plt.ylabel('Mean Flow Magnitude')
    plt.title('Smoothed Mean Flow Magnitude Over Time Steps')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/smoothed_mean_flow_magnitude_plot.png", dpi=300)
    plt.show()
    print(f"Plot saved in {output_dir}")