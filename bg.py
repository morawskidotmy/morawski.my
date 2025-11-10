import os
import random
import shutil
import time

# Define the directory containing background images
bg_folder = './bg'

# Define the path to the output file
output_file = './bg.jpg'

def change_background_image():
    # List all files in the bg folder
    images = [f for f in os.listdir(bg_folder) if os.path.isfile(os.path.join(bg_folder, f))]
    
    # Select a random image
    if images:
        selected_image = random.choice(images)
        # Construct full path for the selected image
        selected_image_path = os.path.join(bg_folder, selected_image)
        
        # Copy the selected image to the output file location
        shutil.copy(selected_image_path, output_file)
        print(f'Background image changed to: {selected_image}')

def main():
    while True:
        change_background_image()
        # Wait for 1 hour (3600 seconds)
        time.sleep(3600)

if __name__ == '__main__':
    main()
