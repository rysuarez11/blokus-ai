import os
from PIL import Image

def extract_images(image_path):
    # Construct the absolute path to the file
    absolute_path = os.path.join(os.path.dirname(__file__), image_path)
    print("Resolved Path:", absolute_path)  # Debugging statement
    image = Image.open(absolute_path)
    return image
