import cvxpy as cp
import numpy as np

def apply_ls_decomposition(data_matrix, lambda_val, max_iters=50):
    """
    Apply Low-Rank and Sparse decomposition on the data matrix.

    Parameters:
    data_matrix (np.ndarray): The data matrix to decompose.
    lambda_val (float): Regularization parameter for the sparse component.
    max_iters (int): Maximum number of iterations.

    Returns:
    tuple: Low-rank component and sparse component matrices.
    """
    L = cp.Variable(data_matrix.shape)
    S = cp.Variable(data_matrix.shape)
    
    objective = cp.Minimize(cp.normNuc(L) + lambda_val * cp.norm1(S))
    constraints = [L + S == data_matrix]
    
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.SCS, verbose=False, max_iters=max_iters)
    
    return L.value, S.value

def create_matrix_structure(volume_4d, z_range=None):
    """
    Create a dictionary structure to store the L and S matrices for each slice in the volume.

    Parameters:
    volume_4d (dict): Dictionary with time points as keys and 4D volumes as values.
    z_range (range, optional): Range of z values to include.

    Returns:
    dict: Dictionary structure for storing matrices.
    """
    if z_range is None:
        z_range = range(volume_4d[next(iter(volume_4d))].shape[1])
    
    return {z: {x: [] for x in range(volume_4d[next(iter(volume_4d))].shape[2])} for z in z_range}

def get_M_matrices(volume_4d, z_range=None):
    """
    Create M matrices for each slice in the volume.

    Parameters:
    volume_4d (dict): Dictionary with time points as keys and 4D volumes as values.
    z_range (range, optional): Range of z values to include.

    Returns:
    dict: Dictionary of M matrices.
    """
    M = create_matrix_structure(volume_4d, z_range)
    for _, volume_3d in volume_4d.items():
        volume_3d = np.squeeze(volume_3d, axis=0)
        for z in (range(volume_3d.shape[0]) if z_range is None else z_range):
            slice_matrix = volume_3d[z, :, :]
            for x in range(slice_matrix.shape[0]):
                M[z][x].append(np.array(slice_matrix[x, :]))
    
    for key in M.keys():
        for key2 in M[key].keys():
            M[key][key2] = np.array(M[key][key2]).T
    return M

def apply_ls_on_whole_volume(volume_4d, lambda_val=0.25, max_iters=5, z_range=None):
    """
    Apply Low-Rank and Sparse decomposition on the whole volume.

    Parameters:
    volume_4d (dict): Dictionary with time points as keys and 4D volumes as values.
    lambda_val (float): Regularization parameter for the sparse component.
    max_iters (int): Maximum number of iterations.
    z_range (range, optional): Range of z values to include.

    Returns:
    tuple: Low-rank and sparse component matrices.
    """
    M = get_M_matrices(volume_4d, z_range)
    L = create_matrix_structure(volume_4d, z_range)
    S = create_matrix_structure(volume_4d, z_range)
    for key in M.keys():
        for key2 in M[key].keys():
            local_L, local_S = apply_ls_decomposition(M[key][key2], lambda_val, max_iters)
            L[key][key2] = local_L
            S[key][key2] = local_S
    return L, S
