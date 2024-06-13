import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt
import re

model = load_model('numbers/models/handwritten_model.h5')

# Create output directory if it does not exist
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to sanitize file names
def sanitize_filename(filename):
    # Replace consecutive non-alphanumeric characters with a single underscore
    return re.sub(r'\W+', '_', filename).strip('_')

# Function to preprocess and extract digits from an image
def ocr(image_path):
    # Load image
    base_image = cv2.imread(image_path)
    if base_image is None:
        print(f"Warning: The image at path {image_path} could not be loaded.")
        return []

    # Define the coordinates of the region of interest (ROI)
    roi_y, roi_h = 500, 1200  # Example coordinates; adjust as needed

    # Ensure ROI is within image bounds
    if roi_y + roi_h > base_image.shape[0]:
        print(f"Warning: ROI out of bounds for image {image_path}")
        return []

    # Crop the ROI from the image
    roi = base_image[roi_y:roi_y + roi_h]

    # Check if ROI is valid
    if roi.size == 0:
        print(f"Warning: The ROI for image {image_path} is empty.")
        return []

    # Resize the ROI to double its original size
    zoomed_roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    image = zoomed_roi.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

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
                if 50 <= w <= 100 and 50 <= h <= 100:  # Ensure the box size is within the specified range
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.2:  # Filter based on a stricter aspect ratio for squares
                        bounding_boxes.append((x, y, w, h))

    print(f"Detected {len(bounding_boxes)} bounding boxes before filtering.")

    # Remove boxes that are inside other boxes
    def is_inside(box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        return x1 > x2 and y1 > y2 and (x1 + w1) < (x2 + w2) and (y1 + h1) < (y2 + h2)

    filtered_boxes = []
    for box in bounding_boxes:
        if not any(is_inside(box, other) for other in bounding_boxes):
            filtered_boxes.append(box)

    print(f"Detected {len(filtered_boxes)} bounding boxes after filtering.")

    # Sort bounding_boxes by y first (top to bottom), then by x (left to right)
    filtered_boxes.sort(key=lambda b: (b[1], b[0]))

    # Draw the filtered bounding boxes on the original image
    for (x, y, w, h) in filtered_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with all detected boxes using matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Boxes')
    plt.axis('off')
    plt.show()

    # Set to store processed coordinates to avoid duplicates
    processed_coordinates = set()

    # List to store individual predictions
    predictions = []

    def process_box(x, y, w, h):
        # Crop the detected square region
        cropped_image = image[y:y + h, x:x + w]

        # Ensure the cropped image is C-contiguous
        cropped_image_contiguous = np.ascontiguousarray(cropped_image)

        # Resize the cropped image to the input size expected by the model
        resized_image = cv2.resize(cropped_image_contiguous, (150, 150))
        resized_image = resized_image.astype('float32') / 255
        resized_image = np.expand_dims(resized_image, axis=0)

        # Make prediction
        prediction = model.predict(resized_image)
        predicted_index = np.argmax(prediction)

        # Map indices 10 and 11 to 0, otherwise use predicted index
        if predicted_index in [10, 11]:
            predicted_label = 0
        else:
            predicted_label = predicted_index

        # Append prediction to the list
        predictions.append(predicted_label)

        # Print the coordinates and the prediction
        print(f'Coordinates: (x: {x}, y: {y}, w: {w}, h: {h}) - Predicted Number: {predicted_label}')

    # Process boxes from top left to bottom right, avoiding duplicates using coordinates as unique value
    current_y = filtered_boxes[0][1] if filtered_boxes else 0
    row_boxes = []
    for (x, y, w, h) in filtered_boxes:
        if (x, y) not in processed_coordinates:
            if abs(y - current_y) > 5:
                # Process the previous row
                for box in sorted(row_boxes, key=lambda b: b[0]):
                    process_box(*box)
                row_boxes = []
                current_y = y
            row_boxes.append((x, y, w, h))
            processed_coordinates.add((x, y))

    # Process the last row
    for box in sorted(row_boxes, key=lambda b: b[0]):
        process_box(*box)

    # Group every 3 numbers together and concatenate them
    grouped_predictions = [int(''.join(map(str, predictions[i:i + 3]))) for i in range(0, len(predictions), 3)]

    # Print grouped predictions
    print(f'Grouped Predictions: {grouped_predictions}')

    print('---------------------------------------------processing complete----------------------------------')

    return grouped_predictions

# Function to process a single image
def process_image(image_path):
    grouped_predictions = ocr(image_path)
    # Ensure the output directory exists
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Define the mapping of predictions to categories
    categories = {
        "Jumlah pemilih dalam DPT": grouped_predictions[0:3],
        "Jumlah pengguna hak pilih dalam DPT": grouped_predictions[3:6],
        "Jumlah pengguna hak pilih dalam DPTb": grouped_predictions[6:9],
        "Jumlah pengguna hak pilih dalam DPK": grouped_predictions[9:12],
        "Jumlah pengguna hak pilih (B.1 + B.2 + B.3)": grouped_predictions[12:15],
        "Jumlah surat suara yang diterima, termasuk surat suara cadangan 2% dari DPT": grouped_predictions[15] if len(grouped_predictions) > 15 else None,
        "Jumlah surat suara yang digunakan": grouped_predictions[16] if len(grouped_predictions) > 16 else None,
        "Jumlah surat suara yang dikembalikan oleh pemilih (karena rusak atau keliru coblos)": grouped_predictions[17] if len(grouped_predictions) > 17 else None,
        "Jumlah surat suara yang tidak digunakan/tidak terpakai, termasuk sisa surat suara cadangan": grouped_predictions[18] if len(grouped_predictions) > 18 else None,
        "Jumlah seluruh pemilih disabilitas yang menggunakan hak pilih": grouped_predictions[19:22] if len(grouped_predictions) > 19 else None,
    }

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(categories.items()), columns=['Category', 'Value'])

    # Extract the base name of the image file without extension
    base_name = os.path.basename(image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]

    # Sanitize the file name
    sanitized_file_name = sanitize_filename(file_name_without_ext)

    # Specify the path for the CSV file
    output_csv_path = os.path.join(output_dir, f'lembar_1_{sanitized_file_name}.csv')

    # Export the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)

    # Print the DataFrame
    print(f'{output_csv_path} done')

    # Provide the output CSV path
    print(f'CSV file saved at: {output_csv_path}')

# Example usage
image_path = "lembar_1/['PILPRES', 'Hitung Suara', 'DKI JAKARTA', 'ADM. KEP. SERIBU', 'KEPULAUAN SERIBU SELATAN.', 'PULAU PARI', 'TPS 005', 'TPS 005', '']_image_1.jpg"  # Replace with the path to your image
process_image(image_path)
