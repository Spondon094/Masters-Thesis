"""
Applies B-spline nonlinear warping to align moving images with a reference image.

The B-spline warping method helps achieve smooth and flexible deformations.
"""

import SimpleITK as sitk
import numpy as np

def apply_bspline_warping(moving_file, reference_file):
    """
    Applies B-spline nonlinear warping to align the moving image to the reference image.

    Parameters:
        moving_file (str): Path to the moving NIFTI file.
        reference_file (str): Path to the reference NIFTI file.

    Returns:
        numpy.ndarray: Warped image array.
    """
    # Load images using SimpleITK
    reference_img = sitk.ReadImage(reference_file)
    moving_img = sitk.ReadImage(moving_file)

    # Initialize transformation parameters
    grid_physical_spacing = [50.0, 50.0, 50.0]
    image_size = moving_img.GetSize()
    image_physical_size = [sz * spc for sz, spc in zip(image_size, moving_img.GetSpacing())]
    mesh_size = [int(sz / spc + 0.5) for sz, spc in zip(image_physical_size, grid_physical_spacing)]

    transform = sitk.BSplineTransformInitializer(reference_img, mesh_size)
    registration = sitk.ImageRegistrationMethod()
    registration.SetMetricAsMeanSquares()
    registration.SetOptimizerAsLBFGSB()
    registration.SetInitialTransform(transform, inPlace=False)
    registration.SetInterpolator(sitk.sitkLinear)

    # Execute the transformation
    final_transform = registration.Execute(reference_img, moving_img)
    warped_img = sitk.Resample(moving_img, reference_img, final_transform, sitk.sitkLinear, 0.0, moving_img.GetPixelID())
    
    return sitk.GetArrayFromImage(warped_img)