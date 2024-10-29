import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from ipywidgets import interact, IntSlider

def plot_acquisition_times(sorted_datasets):
    """
    Plot acquisition times over sequence.

    Parameters:
    sorted_datasets (list): Sorted list of tuples (dataset, milliseconds).
    """
    acquisition_order = list(range(len(sorted_datasets)))
    acquisition_times = [millis for _, millis in sorted_datasets]
    
    plt.figure(figsize=(12, 6))
    plt.plot(acquisition_order, acquisition_times, marker='o')
    plt.title('Acquisition Times Over Sequence')
    plt.xlabel('Acquisition Order')
    plt.ylabel('Time (milliseconds)')
    plt.grid(True)
    plt.show()

def display_slice(volume_4d, first_volume_key, frame_index, slice_index):
    """
    Display a specific slice from the 4D volume.

    Parameters:
    volume_4d (dict): Dictionary with time points as keys and 4D volumes as values.
    first_volume_key (str): Key of the first volume to be displayed.
    frame_index (int): Frame index of the slice to display.
    slice_index (int): Slice index to display.
    """
    volume = volume_4d[first_volume_key]
    if volume.ndim == 4:
        if frame_index < volume.shape[0] and slice_index < volume.shape[1]:
            specific_slice = volume[frame_index, slice_index, :, :]
            plt.imshow(specific_slice, cmap='gray')
            plt.title(f"Frame {frame_index}, Slice {slice_index}")
            plt.axis('off')
            plt.show()
        else:
            print("Invalid frame or slice index.")
    else:
        print("Volume is not 4D.")

def interactive_slice_viewer(volume_4d):
    """
    Create an interactive slice viewer for the 4D volume.

    Parameters:
    volume_4d (dict): Dictionary with time points as keys and 4D volumes as values.
    """
    first_volume_key = next(iter(volume_4d))
    first_volume = volume_4d[first_volume_key]
    frame_max = first_volume.shape[0] - 1
    slice_max = first_volume.shape[2] - 1
    
    interact(display_slice, volume_4d=widgets.fixed(volume_4d),
             first_volume_key=widgets.fixed(first_volume_key),
             frame_index=IntSlider(min=0, max=frame_max, step=1, value=0),
             slice_index=IntSlider(min=0, max=slice_max, step=1, value=0))


# if __name__ == '__main__':