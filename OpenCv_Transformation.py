# -*- coding: utf-8 -*-
"""Balaji_kesavan_CV_assignment3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_ajw4XL4FkoDsqspes7bQz2FLcH5FCxF

Task 1: Rotation Implementation
1. Implement a function to perform rotation on a given image by a specified angle (in degrees).
2. Apply the rotation function to a set of images with varying rotation angles (e.g., 30°, 60°, -45°) and visualize the results.
3. Compare the results of your rotation implementation with a built-in rotation function from a popular image processing library (e.g., OpenCV). Discuss any differences or similarities observed.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Custom function to rotate an image by a specified angle.
Uses affine transformation to manually perform rotation.
"""

def custom_rotate(image, angle):

    # Get image dimensions and calculate the center
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    # Convert the angle from degrees to radians
    angle_rad = np.radians(angle)

    # Calculate the rotation matrix elements
    cos = np.cos(angle_rad)
    sin = np.sin(angle_rad)

    # Create the rotation matrix
    rotation_matrix = np.array([
        [cos, -sin, (1 - cos) * center[0] + sin * center[1]],
        [sin, cos, (1 - sin) * center[1] - cos * center[0]]
    ])

    # Apply affine transformation using the calculated matrix
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image

    """
    Uses OpenCV's built-in rotation function to rotate an image by a specified angle.
    """
def opencv_rotate(image, angle):

    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    # Get rotation matrix from OpenCV and apply it
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image

    """
    Applies custom and OpenCV rotations for specified angles and displays the results.
    """
def visualize_rotation(image, angles):

    fig, axs = plt.subplots(len(angles), 3, figsize=(10, 10))
    fig.suptitle("Rotation Comparison: Custom vs. OpenCV")

    for i, angle in enumerate(angles):
        custom_rotated = custom_rotate(image, angle)
        opencv_rotated = opencv_rotate(image, angle)

        # Display original image, custom rotated image, and OpenCV rotated image
        axs[i, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axs[i, 0].set_title(f"Original - {angle}°")

        axs[i, 1].imshow(cv2.cvtColor(custom_rotated, cv2.COLOR_BGR2RGB))
        axs[i, 1].set_title(f"Custom Rotation - {angle}°")

        axs[i, 2].imshow(cv2.cvtColor(opencv_rotated, cv2.COLOR_BGR2RGB))
        axs[i, 2].set_title(f"OpenCV Rotation - {angle}°")

        for ax in axs[i]:
            ax.axis('off')

    plt.show()

image_path = '/content/cv/tree.jpg'
image = cv2.imread(image_path)

#angles for test rotation
angles = [30, 60, -45]

#rotation results
visualize_rotation(image, angles)

"""Task 2: Transformation Matrix Calculation
1. Implement a function to calculate the transformation matrix for a given translation (dx, dy) and scaling factors (sx, sy).
2. Apply the transformation matrix to a set of images along with the translation and scaling parameters.
3. Visualize and compare the transformed images with the original ones.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
    Calculates a transformation matrix for a given translation (dx, dy) and scaling factors (sx, sy).
    Returns a 2x3 affine transformation matrix.
"""
def calculate_transformation_matrix(dx, dy, sx, sy):

    transformation_matrix = np.array([
        [sx, 0, dx],
        [0, sy, dy]
    ], dtype=np.float32)

    return transformation_matrix

    """
    Applies a transformation matrix to an image with specified translation and scaling parameters.
    """
def apply_transformation(image, dx, dy, sx, sy):

    # Get image dimensions
    (h, w) = image.shape[:2]

    # Calculate transformation matrix
    transformation_matrix = calculate_transformation_matrix(dx, dy, sx, sy)

    # Apply the transformation to the image
    transformed_image = cv2.warpAffine(image, transformation_matrix, (w, h))

    return transformed_image

    """
    Applies transformations to an image with various translation and scaling parameters,
    and display the original and transformed images side by side.
    """
def visualize_transformation(image, transformations):

    fig, axs = plt.subplots(1, len(transformations) + 1, figsize=(15, 5))
    fig.suptitle("Transformation Comparison: Translation & Scaling")

    # Display original image
    axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original")
    axs[0].axis('off')

    # Apply each transformation and display results
    for i, (dx, dy, sx, sy) in enumerate(transformations):
        transformed_image = apply_transformation(image, dx, dy, sx, sy)

        axs[i + 1].imshow(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
        axs[i + 1].set_title(f"dx={dx}, dy={dy}\nsx={sx}, sy={sy}")
        axs[i + 1].axis('off')

    plt.show()

image_path = '/content/cv/tree.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    raise FileNotFoundError(f"Image file not found at specified path: {image_path}")


# Transformations with different translation and scaling parameters
transformations = [
    (50, 30, 1.2, 1.2),  # Translation right and down, scaling up
    (-30, -50, 0.8, 0.8),  # Translation left and up, scaling down
    (20, -20, 1.0, 1.5)    # Translation right and up, anisotropic scaling
]

# Transformation results
visualize_transformation(image, transformations)

"""Task 3: Combining Transformations
1. Implement a function that combines multiple transformations (e.g., rotation followed by translation).
2. Apply the combined transformation to a set of images and visualize the results.
3. Discuss the order of applying transformations and its impact on the final outcome.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
    A combined transformation matrix with scaling, rotation, and translation is calculated
    Parameters:
        dx, dy: Translation offsets
        angle: Rotation angle in degrees
        sx, sy: Scaling factors (default is no scaling)
    Returns:
        A 2x3 affine transformation matrix combining scaling, rotation, and translation.
"""
def calculate_combined_transformation(dx, dy, angle, sx=1, sy=1):

    # Rotation matrix
    angle_rad = np.radians(angle)
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
    rotation_matrix = np.array([
        [cos_a * sx, -sin_a * sy, 0],
        [sin_a * sx, cos_a * sy, 0]
    ], dtype=np.float32)

    # Translation matrix
    transformation_matrix = rotation_matrix.copy()
    transformation_matrix[0, 2] = dx
    transformation_matrix[1, 2] = dy

    return transformation_matrix

    """
    Combined transformation (rotation followed by translation) to an image is applied
    """
def apply_combined_transformation(image, dx, dy, angle, sx=1, sy=1):

    # Get image dimensions
    (h, w) = image.shape[:2]

    # Calculate the combined transformation matrix
    transformation_matrix = calculate_combined_transformation(dx, dy, angle, sx, sy)

    # Apply the transformation matrix to the image
    transformed_image = cv2.warpAffine(image, transformation_matrix, (w, h))
    return transformed_image

    """
    Combined transformations to an image with various parameters and display the results is applied
    """
def visualize_combined_transformations(image, transformations):

    fig, axs = plt.subplots(1, len(transformations) + 1, figsize=(15, 5))
    fig.suptitle("Combined Transformation: Rotation & Translation")

    # Display the original image
    axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original")
    axs[0].axis('off')

    # Apply each transformation and display results
    for i, (dx, dy, angle, sx, sy) in enumerate(transformations):
        transformed_image = apply_combined_transformation(image, dx, dy, angle, sx, sy)

        axs[i + 1].imshow(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
        axs[i + 1].set_title(f"dx={dx}, dy={dy}\nangle={angle}°, sx={sx}, sy={sy}")
        axs[i + 1].axis('off')

    plt.show()


image_path = '/content/cv/tree.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    raise FileNotFoundError(f"Image file not found in the path: {image_path}")

# Transformations with different parameters
transformations = [
    (50, 30, 45, 1, 1),       # Translate right & down, rotate 45°
    (-30, -50, -30, 1.2, 1.2), # Translate left & up, rotate -30°, scale up
    (20, 40, 90, 0.8, 1)      # Translate right & down, rotate 90°, scale down on x-axis
]

# Combined transformations visualization
visualize_combined_transformations(image, transformations)