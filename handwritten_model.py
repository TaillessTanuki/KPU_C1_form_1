import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import random

# Set random seed for reproducibility
random_state = 42
np.random.seed(random_state)
tf.random.set_seed(random_state)
random.seed(random_state)

# Define paths
train_dir = 'numbers/training_set'
test_dir = 'numbers/test_set'
model_path = 'numbers/models/handwritten_model.h5'
class_indices_path = 'numbers/models/class_indices.pkl'


# Function to load images and labels from a directory
def load_images_and_labels(directory):
    images = []
    labels = []
    class_names = sorted(os.listdir(directory))
    class_indices = {class_name: idx for idx, class_name in enumerate(class_names)}

    for class_name in class_names:
        class_dir = os.path.join(directory, class_name)
        if os.path.isdir(class_dir):
            for filename in os.listdir(class_dir):
                file_path = os.path.join(class_dir, filename)
                if os.path.isfile(file_path):
                    img = load_img(file_path, target_size=(150, 150))
                    img_array = img_to_array(img) / 255.0
                    images.append(img_array)
                    labels.append(class_indices[class_name])

    images = np.array(images)
    labels = tf.keras.utils.to_categorical(labels, num_classes=len(class_names))

    return images, labels, class_indices


# Load training and test data
train_images, train_labels, class_indices = load_images_and_labels(train_dir)
test_images, test_labels, _ = load_images_and_labels(test_dir)

print(f"Total training images: {train_images.shape[0]}")
print(f"Total test images: {test_images.shape[0]}")

# Save class indices
with open(class_indices_path, 'wb') as f:
    pickle.dump(class_indices, f)

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),  # Increased number of filters
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(256, activation='relu'),  # Increased number of neurons
    Dense(len(class_indices), activation='softmax')  # Update number of classes
])

# Define the optimizer with adjustable learning rate
learning_rate = 0.001  # Adjust learning rate
optimizer = Adam(learning_rate=learning_rate)

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Define EarlyStopping callback to stop training when accuracy reaches 0.75
early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=5, verbose=1, mode='max', baseline=0.75,
                               restore_best_weights=True)

# Train the model without batching
history = model.fit(
    train_images, train_labels,
    validation_data=(test_images, test_labels),
    epochs=20,  # Set a high number of epochs
    callbacks=[early_stopping]
)

# Save the model
model.save(model_path)
print(f"Model saved at {model_path}")

# Plot training & validation accuracy values
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')

plt.show()
