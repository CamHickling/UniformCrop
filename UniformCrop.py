import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import os

# given an image, find the bounding box of the non-transparent part of the image for an left page
def find_non_white_bounding_boxL(image_path, min_width=10, min_height=10):
    # change these values to match the desired width and height of the image for left pages
    totalWidth = 2083 
    totalHeight = 3415

    #First, get or create an image number
    #in this case, the image number is the 4th element of the split string
    #ex. "PR2751_A1_1623_0025_L.tif"
    #so we will take this "0025"
    image_num = image_path.split("_")[3]

    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to separate non-white part
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get bounding box for each contour
    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
    
    # Filter out bounding boxes with minimum height and width
    bounding_boxes = [(x, y, w, h) for x, y, w, h in bounding_boxes if w >= min_width and h >= min_height]
    
    # Print bounding box coordinates
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        print(f"before adjusting: bounding box {image_num}: (x={x}, y={y}), (width={w}, height={h})")

    # Expand each bounding box to fit exact pixel dimensions
    for i, (x, y, w, h) in enumerate(bounding_boxes):

        #adjust X and Width
        #for right pages we'd like this box to be aligned with the left edge of the page
        X = int(2453 - totalWidth)
        W = int(totalWidth)

        #adjust Y and Height
        #we'd also like the box to be centered vertically
        deltaHeight = totalHeight - h 
        Y = int(y - deltaHeight/2)
        H = int(h + deltaHeight)

        bounding_boxes[i] = (X, Y, W+X, H+Y)
        print(f"after adjusting:  bounding box {image_num}: (x={X}, y={Y}), (width={W}, height={H})")
    
    # Draw bounding box on original image
    for x, y, w, h in bounding_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the result
    #!!! comment out the following 3 lines to avoid displaying the image when batching !!!
    cv2.imshow('Bounding Box', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return bounding_boxes[0]

# process all left page image in the input folder and save the resized images in the output folder
def process_imagesL(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):

        # Don't worry about this line, it's just to skip macOS metadata files
        if filename.startswith("._"):
            continue  # Skip macOS metadata files

        # Only process left page images
        # The image is a left page if it ends with "_l.png" or "_l.png"
        # change these string in the ends with function to match the naming convention of all your left page images
        if filename.lower().endswith(("_l.png", "_l.png")):
            print(filename)

            # Find the bounding box of the non-white part of the image and crop it
            image_path = os.path.join(input_folder, filename)
            bounding_box = find_non_white_bounding_boxL(image_path)
            img = Image.open(image_path)
            cropped_img = img.crop(bounding_box)

            # Resize and save the resized image, ensuring it's also a PNG
            resized_img = cropped_img.resize(target_size)
            resized_png_output_path = os.path.join(output_folder, f"{filename.rsplit('.', 1)[0]}.png")
            resized_img.save(resized_png_output_path, "PNG")
            print(f"Resized {filename} and saved as {resized_png_output_path}\n")
    
# given an image, find the bounding box of the non-transparent part of the image for a right page
def find_non_white_bounding_boxR(image_path, min_width=10, min_height=10):
    # change these values to match the desired width and height of the image for right pages
    totalWidth = int(1936/5)
    totalHeight = int(3351/5)

    #First, get or create an image number
    #in this case, the image number is the 4th element of the split string
    #ex. "PR2751_A1_1623_0026_R.tif"
    #so we will take this "0026"
    image_num = image_path.split("_")[3]

    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to separate non-white part
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get bounding box for each contour
    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
    
    # Filter out bounding boxes with minimum height and width
    bounding_boxes = [(x, y, w, h) for x, y, w, h in bounding_boxes if w >= min_width and h >= min_height]
    
    # Print bounding box coordinates
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        print(f"before adjusting: bounding box {image_num}: (x={x}, y={y}), (width={w}, height={h})")

    # Expand each bounding box to fit exact pixel dimensions
    for i, (x, y, w, h) in enumerate(bounding_boxes):

        #adjust X and Width
        #for right pages we'd like this box to be aligned with the left edge of the page
        X = int(0)
        W = int(totalWidth)

        #adjust Y and Height
        #we'd also like the box to be centered vertically
        deltaHeight = totalHeight - h 
        Y = int(y - deltaHeight/2)
        H = int(h + deltaHeight)
        H -= 70

        bounding_boxes[i] = (X, Y, W+X, H+Y)
        print(f"after adjusting:  bounding box {image_num}: (x={X}, y={Y}), (width={W}, height={H})")

    # Draw bounding box on original image
    for x, y, w, h in bounding_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the result
    #!!! comment out the following 3 lines to avoid displaying the image when batching !!!
    cv2.imshow('Bounding Box', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return bounding_boxes[0]

# Function to process images
def process_imagesR(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):

        # Don't worry about this line, it's just to skip macOS metadata files
        if filename.startswith("._"):
            continue  # Skip macOS metadata files

        # Only process right page images
        # The image is a right page if it ends with "_r.png" or "_r.png"
        # change these string in the ends with function to match the naming convention of all your right page images
        if filename.lower().endswith(("_r.png", "_r.png")):
            print(filename)

            # Find the bounding box of the non-white part of the image and crop it
            image_path = os.path.join(input_folder, filename)
            bounding_box = find_non_white_bounding_boxR(image_path)
            img = Image.open(image_path)
            cropped_img = img.crop(bounding_box)
            
            # Resize and save the resized image, ensuring it's also a PNG
            resized_img = cropped_img.resize(target_size)
            resized_png_output_path = os.path.join(output_folder, f"{filename.rsplit('.', 1)[0]}.png")
            resized_img.save(resized_png_output_path, "PNG")
            print(f"Resized {filename} and saved as {resized_png_output_path}\n")


    
# Set input and output folders as well as desired width and height for the images
# put all of your photos to be processed in a folder labeled "input"
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
out = os.path.join(desktop, 'output')
os.makedirs(out)

desired_widthR = 1936
desired_heightR = 3351
desired_widthL = 2083
desired_heightL = 3415

# Set target size (width, height)
target_sizeR = (desired_widthR, desired_heightR)
target_sizeL = (desired_widthL, desired_heightL)

# Process images
process_imagesL(input_folder, output_folder, target_sizeL)
process_imagesR(input_folder, output_folder, target_sizeR)