import cv2
import pytesseract

# Function to preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding or other preprocessing techniques as needed
    return gray

# Function to extract squares from contours
def extract_squares(contours, image):
    square_rois = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            square_rois.append(image[y:y+h, x:x+w])
    return square_rois

# Read the image
image = cv2.imread("lembar_1/['PILPRES', 'Hitung Suara', 'DKI JAKARTA', 'ADM. KEP. SERIBU', 'KEPULAUAN SERIBU SELATAN.', 'PULAU PARI', 'TPS 004', 'TPS 004', '']_image_1.jpg")

# Preprocessing
preprocessed_image = preprocess_image(image)

# Contour detection
contours, _ = cv2.findContours(preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Square identification
square_contours = [contour for contour in contours if cv2.contourArea(contour) > 1000]

# Extracting ROIs
square_rois = extract_squares(square_contours, image)

# OCR (Optical Character Recognition)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\prata\Tesseract_OCR\tesseract.exe' # Path to Tesseract executable
for roi in square_rois:
    text = pytesseract.image_to_string(roi, config='--psm 6')  # PSM 6 assumes a single uniform block of text
    print("Number inside square:", text)

# Display the results or save them to a file
