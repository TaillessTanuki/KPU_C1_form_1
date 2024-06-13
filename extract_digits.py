import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory if it does not exist
output_folder = "extracted_digits"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to preprocess and extract digits from an image
def extract_digits(image_path, output_folder):
    # Load image
    base_image = cv2.imread(image_path)
    if base_image is None:
        print(f"Warning: The image at path {image_path} could not be loaded.")
        return [], None

    # Define the coordinates of the region of interest (ROI)
    roi_y, roi_h = 500, 1000  # Example coordinates; adjust as needed

    # Ensure ROI is within image bounds
    if roi_y + roi_h > base_image.shape[0]:
        print(f"Warning: ROI out of bounds for image {image_path}")
        return [], None

    # Crop the ROI from the image
    roi = base_image[roi_y:roi_y + roi_h]

    # Check if ROI is valid
    if roi.size == 0:
        print(f"Warning: The ROI for image {image_path} is empty.")
        return [], None

    # Resize the ROI to double its original size
    zoomed_roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    image = zoomed_roi.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)

    # Dilate the image to connect edges
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=2)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # Apply edge detection
    edges = cv2.Canny(eroded, 30, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours based on area and shape
    min_area = 300  # Adjust this threshold as needed
    filtered_contours = []

    # List to store bounding boxes and cropped images
    bounding_boxes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # Check if the approximated contour has 4 vertices (square/rectangle)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h
                if 0.8 <= aspect_ratio <= 1.2:  # Filter based on a stricter aspect ratio for squares
                    bounding_boxes.append((x, y, w, h))

    # Sort bounding boxes from top to bottom, then left to right
    bounding_boxes.sort(key=lambda b: (b[1], b[0]))

    # List to store cropped images without duplicates
    cropped_images = []

    # Draw contours on the original image
    result = image.copy()
    for (x, y, w, h) in bounding_boxes:
        # Crop the detected square region
        cropped_image = image[y:y+h, x:x+w]
        # Check if this cropped image is already in the list to avoid duplicates
        if not any(np.array_equal(cropped_image, img) for img in cropped_images):
            cropped_images.append(cropped_image)
            # Draw the bounding box on the result image
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Save individual cropped images
    for i, cropped_image in enumerate(cropped_images):
        output_filename = os.path.join(output_folder, f'{filename}cropped_square_{i}.png')
        cv2.imwrite(output_filename, cropped_image)

    return cropped_images, result

# Path to the input folder
input_folder = "lembar_1"

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image_path = os.path.join(input_folder, filename)
        cropped_images, result_image = extract_digits(image_path, output_folder)
        print(f'{filename} downloaded')

print("Processing completed.")
