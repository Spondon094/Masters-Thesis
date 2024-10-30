"""
Main script to compute and visualize optical flow from a sequence of NIFTI images.
"""

from modules.data_loader import load_nifti_data
from modules.optical_flow import compute_optical_flows
from modules.save_results import save_optical_flow_data, save_mean_flow_per_time_step
from modules.visualize_flow import visualize_and_save_flows, plot_smoothed_mean_magnitudes

def main():
    """
    Main function to execute the full pipeline: load data, compute optical flow, save results,
    and visualize output.
    """
    # Step 1: Load NIFTI data
    nifti_folder = 'output/nonlinear_warped_nifti'
    nifti_data, time_steps, slices_per_time_step = load_nifti_data(nifti_folder)
    print(f"Loaded {time_steps} time steps with {slices_per_time_step} slices per time step.")
    
    # Step 2: Compute optical flow
    flows = compute_optical_flows(nifti_data)
    
    # Step 3: Save optical flow results
    save_optical_flow_data(flows, 'output/flows.pkl')
    save_mean_flow_per_time_step(flows, slices_per_time_step, time_steps, 'output/mean_flow_magnitudes_per_time_step.csv')
    
    # Step 4: Visualize optical flow and save images
    visualize_and_save_flows(flows, nifti_data, 'output/flow_visualizations')
    
    # Step 5: Plot smoothed mean flow magnitude over time steps
    plot_smoothed_mean_magnitudes('output/mean_flow_magnitudes_per_time_step.csv', 'output/flow_plots')

if __name__ == "__main__":
    main()