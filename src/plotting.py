import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

def plot_acquisition_times(acquisition_times):
    acquisition_order = list(range(len(acquisition_times)))
    plt.figure(figsize=(12, 6))
    plt.plot(acquisition_order, acquisition_times, marker='o')
    plt.title('Acquisition Times Over Sequence', fontsize = 20)
    plt.xlabel('Acquisition Order', fontsize = 18)
    plt.ylabel('Time (milliseconds)' , fontsize = 18)
    plt.grid(True)
    plt.show()

def plot_singular_values(S):
    plt.plot(S, 'o-')
    plt.title('Singular Values over Time Step', fontsize = 16)
    plt.xlabel('Time Steps', fontsize = 14)
    plt.ylabel('Singular Value', fontsize = 14)
    plt.show()

def plot_temporal_patterns(U, time_differences, num_patterns=10):
    plt.figure(figsize=(15, 10))
    for i in range(num_patterns):
        plt.plot(time_differences, U[:, i], label=f'Pattern {i+1}')
    plt.title('Magnitude of Temporal Patterns Over Time Differences', fontsize = 20)
    plt.xlabel('Time Differences (milliseconds)', fontsize = 16)
    plt.ylabel('Magnitude', fontsize = 16)
    plt.legend()
    plt.show()

def smooth_and_plot_patterns(U_averaged_noised, time_differences, S):
    

    x = np.array(time_differences)
    plt.figure(figsize=(10, 6))
    for i in range(0,8):
        #y = U_averaged_noised[:, i] * S[i]
        y = U_averaged_noised[i, :] * S[i]
        #y = U_averaged_noised[i, :] #* S[i]

        cubic_interpolation_model = interp1d(x, y, kind="cubic")
        X_smooth = np.linspace(x.min(), x.max(), 5000)
        Y_smooth = cubic_interpolation_model(X_smooth)
        plt.plot(X_smooth, Y_smooth, label=f'Pattern {i+1}')
    plt.title('Smooth Curves Using Cubic Interpolation for All Patterns', fontsize = 18)
    plt.xlabel('Time Differences (milliseconds)', fontsize = 16)
    plt.ylabel('Magnitude', fontsize = 16)
    plt.legend(loc='upper right')
    plt.show()
    
# if __name__ == '__main__':
    
