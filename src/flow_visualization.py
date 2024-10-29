"""
Module for visualizing optical flow in 3D and plotting mean flow magnitudes over time.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import cv2
from scipy.ndimage import gaussian_filter1d

def draw_flow_3d(flows, output_folder, filename='3d_farneback_optical_flow.png', step=5):
    """
    Generates a 3D visualization of optical flow over time steps.

    Args:
        flows (list): List of optical flow data arrays.
        output_folder (str): Folder to save the visualization.
        filename (str): Name of the output image file.
        step (int): Sampling step size for visualization.

    Saves:
        PNG file with 3D flow visualization.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    z_vals = np.arange(0, len(flows), step)
    y_vals, x_vals = np.mgrid[0:flows[0].shape[0]:step, 0:flows[0].shape[1]:step]

    for t, flow in enumerate(flows[::step]):
        u = flow[::step, ::step, 0]
        v = flow[::step, ::step, 1]
        w = np.ones_like(u) * t
        ax.quiver(x_vals, y_vals, w, u, v, np.zeros_like(w), length=0.1, normalize=True, color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Time')
    plt.title('3D Optical Flow Visualization (Farneback)')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=300)
    plt.show()

def plot_mean_flow_magnitudes(mean_flow_magnitude, output_folder, filename='smoothed_mean_flow_magnitude_plot.png'):
    """
    Plots and saves the smoothed mean flow magnitudes over time steps.

    Args:
        mean_flow_magnitude (list): List of mean flow magnitudes.
        output_folder (str): Folder to save the plot.
        filename (str): Name of the output image file.
    """
    smoothed_data = gaussian_filter1d(mean_flow_magnitude, sigma=1)
    output_path = os.path.join(output_folder, filename)

    plt.plot(smoothed_data, label='Smoothed Data (Gaussian)')
    plt.xlabel('Time Step')
    plt.ylabel('Mean Flow Magnitude')
    plt.title('Smoothed Mean Flow Magnitude Over Time Steps (Gaussian)')
    plt.grid(True)
    plt.tight_layout()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.savefig(output_path, dpi=300)
    plt.show()