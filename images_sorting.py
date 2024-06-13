import os
import shutil


def divide_images_into_folders(source_dir, dest_dirs):
    # Iterate through each image file in the source directory
    print('Sorting begins')

    for filename in os.listdir(source_dir):
        print(f'filename: {filename}')
        if filename.endswith('1.jpg'):
            dest_dir = dest_dirs["image_1"]
        elif filename.endswith('2.jpg'):
            dest_dir = dest_dirs["image_2"]
        elif filename.endswith('3.jpg'):
            dest_dir = dest_dirs["image_3"]
        else:
            # Skip files that don't match the expected pattern
            continue

        # Move the image file to the corresponding destination folder
        shutil.move(os.path.join(source_dir, filename), os.path.join(dest_dir, filename))

if __name__ == "__main__":
    # Source directory containing the images
    source_directory = "images"

    # Destination directories for each category
    destination_directories = {
        "image_1": "lembar_1",
        "image_2": "lembar_2",
        "image_3": "lembar_3"
    }

    # Create destination folders if they don't exist
    for dest_dir in destination_directories.values():
        os.makedirs(dest_dir, exist_ok=True)

    # Divide images into folders based on their names
    divide_images_into_folders(source_directory, destination_directories)