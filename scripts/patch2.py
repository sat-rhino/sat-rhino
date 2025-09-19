from PIL import Image
from tqdm import tqdm
import sys
import os

# Increase the max image pixels to handle large images safely
Image.MAX_IMAGE_PIXELS = None  # Set to None to disable the limit or set a larger specific number

def patchify_image(image_path, annotation_path, output_dir, patch_size=(256, 256), overlap=0, start_patch_id=0):
    """
    Patchify an image into smaller parts and create corresponding text annotations.

    Args:
        image_path (str): Path to the input image.
        annotation_path (str): Path to the text file containing the annotations.
        output_dir (str): Directory to save the image patches and annotations.
        patch_size (tuple): Size of each patch (width, height).
        overlap (int): Number of pixels to overlap between patches (default is 0).
        start_patch_id (int): Starting index for naming patches to avoid conflicts.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the image
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Read the annotations
    with open(annotation_path, 'r') as file:
        annotations = file.readlines()

    # Process the image and create patches
    patch_width, patch_height = patch_size
    patch_id = start_patch_id

    for top in range(0, img_height, patch_height - overlap):
        for left in range(0, img_width, patch_width - overlap):
            # Define the bounding box for the patch
            box = (left, top, min(left + patch_width, img_width), min(top + patch_height, img_height))

            base_name = os.path.splitext(os.path.basename(image_path))[0]

            # Create a subdirectory named after the image file in the output directory
            image_output_dir = os.path.join(output_dir, base_name)
            os.makedirs(image_output_dir, exist_ok=True)


            # Create the patch
            patch = image.crop(box)
            patch_name = f"patch_{patch_id}{base_name}.png"  # Save as PNG
            patch_path = os.path.join(output_dir, base_name, patch_name)

            patch.save(patch_path, "PNG")  # Specify PNG format to preserve quality

            # Create the corresponding annotation file
            annotation_name = f"patch_{patch_id}{base_name}.txt"
            annotation_patch_path = os.path.join(output_dir, base_name, annotation_name)

            with open(annotation_patch_path, 'w') as patch_annotation_file:
                for annotation in annotations:
                    # Parse the annotation (assuming the format is: label x_center y_center width height)
                    label, x_center, y_center, width, height = annotation.split()
                    x_center, y_center, width, height = map(float, [x_center, y_center, width, height])

                    # Convert to absolute coordinates
                    x_center_abs = x_center * img_width
                    y_center_abs = y_center * img_height
                    width_abs = width * img_width
                    height_abs = height * img_height

                    # Check if the annotation is within the patch
                    if (left <= x_center_abs < left + patch_width) and (top <= y_center_abs < top + patch_height):
                        # Adjust coordinates relative to the patch
                        x_center_patch = (x_center_abs - left) / patch_width
                        y_center_patch = (y_center_abs - top) / patch_height
                        width_patch = width_abs / patch_width
                        height_patch = height_abs / patch_height

                        # Write the adjusted annotation to the patch's annotation file
                        patch_annotation_file.write(f"{label} {x_center_patch} {y_center_patch} {width_patch} {height_patch}\n")

            patch_id += 1

    return 0  # Return the last used patch_id to avoid naming conflicts

def process_multiple_images(image_annotation_pairs, base_output_dir, patch_size=(256, 256), overlap=0):
    """
    Process multiple image and annotation pairs.

    Args:
        image_annotation_pairs (list): List of tuples containing (image_path, annotation_path).
        base_output_dir (str): Base directory to save the image patches and annotations.
        patch_size (tuple): Size of each patch (width, height).
        overlap (int): Number of pixels to overlap between patches.
    """
    patch_id = 0  # Initialize patch_id to avoid conflicts

    for image_path, annotation_path in tqdm(image_annotation_pairs, desc="Processing image-annotation pairs"):
        # Use the same output directory for all patches
        patch_id = patchify_image(image_path, annotation_path, base_output_dir, patch_size, overlap, start_patch_id=patch_id)

if __name__ == "__main__":
    # List of (image_path, annotation_path) tuples
    image_annotation_pairs = [
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2014/01_12_2014subset1.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2014/01_12_2014subset1.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2014/subset2_01_12_2014.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2014/subset2_01_12_2014.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/10_02_2016_subset1.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/10_02_2016_subset1.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/10_02_2016_subset2.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/10_02_2016_subset2.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/16Jan29_Subset1.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/16Jan29_Subset1.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/16Jan29_Subset2.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2016/16Jan29_Subset2.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2017/17NOV22.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 1/2017/17NOV22.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18JAN11.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18JAN11.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18MAR27.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18MAR27added.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18OCT08.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2018/18OCT08Added.txt'),
        ('/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2019/19JAN20.tif', '/fs/nexus-scratch/apalnitk/ylo/Elephants/Part 2/2019/19JAN20Added.txt')
    ]

    base_output_dir = "labels"  # Replace with the base directory where patches will be saved
    process_multiple_images(image_annotation_pairs, base_output_dir)

