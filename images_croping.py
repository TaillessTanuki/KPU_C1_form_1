import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import pytesseract



def crop_images(input_folder, output_folder, x, y, w, h):
    """
    Crop images in the input folder using the specified coordinates and save the cropped regions in the output folder.

    Args:
    - input_folder (str): Path to the folder containing input images.
    - output_folder (str): Path to the folder where cropped images will be saved.
    - x, y, w, h (int): Coordinates of the region of interest (ROI) to be cropped.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            # Read the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            # Crop the ROI from the image
            roi = image[y:y + h, x:x + w]

            # Save the cropped ROI as a new JPG file
            output_filename = os.path.splitext(filename)[0] + '_cropped.jpg'
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, roi)

            print(f"Image '{filename}' cropped and saved as '{output_filename}'")


# Define the coordinates of the region of interest (ROI)
x, y, w, h = 100, 500, 1000, 1000  # Example coordinates; adjust as needed

# Call the function to crop images in the "lembar_1" folder and save them in the "cropped_images" folder
crop_images('testroom_2/original_images', 'testroom_2/cropped_images', x, y, w, h)