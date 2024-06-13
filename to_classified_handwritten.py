import os
import shutil
import pickle
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

# Define paths
to_classify_dir = 'numbers/to_classify'  # Directory with images to classify
sorted_folder = 'numbers/sorted'  # Destination folder for sorted images
model_path = 'numbers/models/handwritten_model.h5'
class_indices_path = 'numbers/models/class_indices.pkl'

# Load the model
model = load_model(model_path)

# Load class indices
with open(class_indices_path, 'rb') as f:
    class_indices = pickle.load(f)
class_labels = {v: k for k, v in class_indices.items()}


# Function to classify and move images
def classify_and_move(image_path, model, target_folder):
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_label = class_labels[predicted_class]

    target_class_folder = os.path.join(target_folder, predicted_label)
    if not os.path.exists(target_class_folder):
        os.makedirs(target_class_folder)

    shutil.move(image_path, os.path.join(target_class_folder, os.path.basename(image_path)))


# Classify and move all images in the to_classify_dir
for filename in os.listdir(to_classify_dir):
    file_path = os.path.join(to_classify_dir, filename)
    if os.path.isfile(file_path):
        classify_and_move(file_path, model, sorted_folder)
print("All images classified and moved.")
