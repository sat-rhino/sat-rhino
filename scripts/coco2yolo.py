import json
import os

# Load COCO annotations
with open('annotations_coco_512_02.json') as f:
    coco_data = json.load(f)

# Create directories for YOLO format
os.makedirs('./train_yolo/images', exist_ok=True)
os.makedirs('./train_yolo/labels', exist_ok=True)
os.makedirs('./valid_yolo/images', exist_ok=True)
os.makedirs('./valid_yolo/labels', exist_ok=True)
os.makedirs('./test_yolo/images', exist_ok=True)
os.makedirs('./test_yolo/labels', exist_ok=True)

def convert_bbox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    return (x * dw, y * dh, w * dw, h * dh)

# Loop through images and annotations
for img in coco_data['images']:
    img_filename = img['file_name']
    img_id = img['id']
    img_width = img['width']
    img_height = img['height']

    # Copy images to YOLO directory
    src_img_path = f"./annotations_coco_images_512_02/{img_filename}"
    dest_img_path = f"./train_yolo/images/{img_filename}"
    os.system(f"cp {src_img_path} {dest_img_path}")

    # Create label file in YOLO format
    label_filename = os.path.splitext(img_filename)[0] + '.txt'
    label_file_path = f"./train_yolo/labels/{label_filename}"
    
    with open(label_file_path, 'w') as label_file:
        for ann in coco_data['annotations']:
            if ann['image_id'] == img_id:
                bbox = ann['bbox']  # COCO format: [x_min, y_min, width, height]
                category_id = ann['category_id']
                bbox_converted = convert_bbox((img_width, img_height), bbox)
                label_file.write(f"{category_id} {' '.join(map(str, bbox_converted))}\n")

print("Conversion complete.")
