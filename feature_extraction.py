import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import pytesseract


def crop_images(input_folder, output_folder):
    # Iterate through all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            # Read the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Threshold the image to obtain binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilate = cv2.dilate(binary, kernal, iterations=1)

            # Find Contours
            cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                if h > 25 and w > 25:
                    if h < 50 and w < 50:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

            # Save the cropped ROI as a new JPG file
            output_filename = os.path.splitext(filename)[0] + '_cropped.jpg'
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, image)

            print(f"Image '{filename}' cropped and saved as '{output_filename}'")


# Call the function to crop images in the "lembar_1" folder and save them in the "cropped_images" folder
crop_images('testroom/croped_images', 'testroom/temp_images/3rd_attempt')
