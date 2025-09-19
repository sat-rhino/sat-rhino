from PIL import Image
import sys
import os

def patchify_image(image_path, annotation_path, output_dir, patch_size=(256, 256), overlap=0):
    """
    Patchify an image into smaller parts and create corresponding text annotations.

    Args:
        image_path (str): Path to the input image.
        annotation_path (str): Path to the text file containing the annotations.
        output_dir (str): Directory to save the image patches and annotations.
        patch_size (tuple): Size of each patch (width, height).
        overlap (int): Number of pixels to overlap between patches (default is 0).
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
    patch_id = 0

    for top in range(0, img_height, patch_height - overlap):
        for left in range(0, img_width, patch_width - overlap):
            # Define the bounding box for the patch
            box = (left, top, min(left + patch_width, img_width), min(top + patch_height, img_height))

            # Create the patch
            patch = image.crop(box)
            patch_name = f"patch_{patch_id}.png"  # Save as PNG
            patch_path = os.path.join(output_dir, patch_name)
            patch.save(patch_path, "PNG")  # Specify PNG format to preserve quality

            # Create the corresponding annotation file
            annotation_name = f"patch_{patch_id}.txt"
            annotation_path = os.path.join(output_dir, annotation_name)

            with open(annotation_path, 'w') as patch_annotation_file:
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

if __name__ == "__main__":
    image_path = str(sys.argv[1])  # Replace with the path to your large TIFF image
    annotation_path = str(sys.argv[2])  # Replace with the path to your annotation file
    output_dir = "."  # Replace with the directory where patches will be saved

    patchify_image(image_path, annotation_path, output_dir)
