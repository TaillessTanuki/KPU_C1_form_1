import cv2
import numpy as np
import re
import base64
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from io import BytesIO
from PIL import Image

model = load_model('numbers/models/handwritten_model.h5')

def sanitize_filename(filename):
    return re.sub(r'\W+', '_', filename).strip('_')


def show_image_matplotlib(title, img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.title(title)
    plt.axis('off')
    plt.show()


def decode_base64_image(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def show_detected_boxes_lembar_2(base64_str):
    base_image = decode_base64_image(base64_str)
    if base_image is None:
        print("Warning: The image could not be decoded.")
        return [], None

    roi_y = base_image.shape[0] // 6
    roi_h = base_image.shape[0] - roi_y
    roi_x = (base_image.shape[1] * 3) // 4
    roi_w = base_image.shape[1] - roi_x

    if roi_y + roi_h > base_image.shape[0] or roi_x + roi_w > base_image.shape[1]:
        print("Warning: ROI out of bounds for the image")
        return [], None

    roi = base_image[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    if roi.size == 0:
        print("Warning: The ROI for the image is empty.")
        return [], None

    zoomed_roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    image = zoomed_roi.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=2)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    edges = cv2.Canny(eroded, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 300
    bounding_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                if 50 <= w <= 100 and 50 <= h <= 100:
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        bounding_boxes.append((x, y, w, h))

    print(f"Detected {len(bounding_boxes)} bounding boxes before filtering.")

    def is_inside(box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        return x1 > x2 and y1 > y2 and (x1 + w1) < (x2 + w2) and (y1 + h1) < (y2 + h2)

    filtered_boxes = [box for box in bounding_boxes if not any(is_inside(box, other) for other in bounding_boxes)]
    print(f"Detected {len(filtered_boxes)} bounding boxes after filtering.")
    filtered_boxes.sort(key=lambda b: (b[1], b[0]))

    for (x, y, w, h) in filtered_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    show_image_matplotlib('Detected Boxes', image)
    return filtered_boxes, image


def predict_numbers_lembar_2(filtered_boxes, image):
    processed_coordinates = set()
    predictions = []

    def process_box(x, y, w, h):
        cropped_image = image[y:y + h, x:x + w]
        cropped_image_contiguous = np.ascontiguousarray(cropped_image)
        resized_image = cv2.resize(cropped_image_contiguous, (150, 150))
        resized_image = resized_image.astype('float32') / 255
        resized_image = np.expand_dims(resized_image, axis=0)
        prediction = model.predict(resized_image)
        predicted_number = np.argmax(prediction)
        if predicted_number in [10, 11]:
            predicted_number = 0
        print(f'Coordinates: (x: {x}, y: {y}, w: {w}, h: {h}) - Predicted Number: {predicted_number}')
        predictions.append(predicted_number)

    current_y = filtered_boxes[0][1] if filtered_boxes else 0
    row_boxes = []
    for (x, y, w, h) in filtered_boxes:
        if (x, y) not in processed_coordinates:
            if abs(y - current_y) > 5:
                for box in sorted(row_boxes, key=lambda b: b[0]):
                    process_box(*box)
                row_boxes = []
                current_y = y
            row_boxes.append((x, y, w, h))
            processed_coordinates.add((x, y))

    for box in sorted(row_boxes, key=lambda b: b[0]):
        process_box(*box)

    grouped_predictions = [int(''.join(map(str, predictions[i:i + 3]))) for i in range(0, len(predictions), 3)]
    print(f'Grouped Predictions: {grouped_predictions}')
    print('---------------------------------------------processing complete----------------------------------')
    return grouped_predictions


if __name__ == '__main__':
    # Replace with your base64 image string

    filtered_boxes, processed_image = show_detected_boxes_lembar_2(base64_image_str)

    if filtered_boxes:
        user_input = input("Apakah anda ingin melanjutkan proses ini? (y/t): ")
        if user_input.lower() == 'y':
            grouped_predictions = predict_numbers_lembar_2(filtered_boxes, processed_image)
            print(grouped_predictions)
        else:
            print("Process terminated by the user.")
    else:
        print("No boxes to process.")