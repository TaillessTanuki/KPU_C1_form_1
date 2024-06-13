import os
from PIL import Image


def delete_small_images(folder_path, min_width=50, min_height=50):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Open an image file
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                # Check if the image is smaller than the specified dimensions
                if width < min_width or height < min_height:
                    img.close()
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Could not process {file_path}: {e}")


# Define the folder path
folder_path = 'extracted_digits'

# Call the function
delete_small_images(folder_path)
