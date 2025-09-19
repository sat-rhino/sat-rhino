# import zipfile
# import os
#
# # Assuming the uploaded file name is 'dataset.zip'
# zip_file_name = 'dataset 3.zip'
#
# # Extract the file
# with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
#     zip_ref.extractall('extracted_files')
#
# # Verify the extraction
# print(os.listdir('extracted_files'))

import os
from ultralytics import YOLO
#model = YOLOv10(f'/fs/nexus-scratch/zeorymer/yolov10/runs/detect/yolo_large_run1_ultralyticsnew2/weights/best.pt')

# Load YOLOv10n model from scratch
model = YOLO("yolov12x.pt")
#!yolo task=detect mode=predict conf=0.25 save=True
#model =  YOLOv10(f'yolov10l_best.pt')
#source=frame_0090.png

model.train(
    data="/fs/nexus-scratch/apalnitk/ylo/pure/whale.yaml",  # Your data config file
    epochs=100,             # Fewer epochs to start—monitor for early stopping
    imgsz=512,               # Reduced resolution to help with memory
    name='yolo_small_obj',   # Name for this training run
    batch=8,                 # Lower per-GPU batch size
    save_period=50,
    device=0,
    augment=True,
    multi_scale=True,        # You can set this to False if needed
    amp=True                 # Enable mixed precision training
)

"""
model.train(
    data="/fs/nexus-scratch/apalnitk/ylo/pure/data.yaml",  # your dataset config file
    epochs=2500,             # fewer epochs to start—monitor validation metrics for early stopping
    imgsz=512,               # increased resolution for better small object representation
    name='yolov11_small_obj_setup2',  # unique name for this run
    batch=8,                 # lower batch size to avoid OOM
    lr0=0.0005,              # lower starting learning rate for more gradual weight updates
    optimizer='SGD',         # SGD with momentum works well; consider experimenting with Adam if needed
    momentum=0.9,            # standard momentum value
    weight_decay=0.0005,     # standard weight decay
    save_period=50,          # save checkpoints every 50 epochs
    device=0,                # select your GPU device
    augment=True,            # enable data augmentation for robustness
    multi_scale=True,        # use multi-scale training; ensure that your scale range doesn’t drop too low
    amp=True                 # enable Automatic Mixed Precision for reduced memory usage
)
"""

#yolo_command = f"yolo task=detect mode=predict conf=0.5 save=True model=yolov10l_best.pt" #source=/fs/nexus-scratch/zeorymer/yolov10/GX010065.MP4"
#model.train(data="./datasets/all-real-dataset/data.yaml", epochs=300, imgsz=640)
#os.system(yolo_command)
