import yaml
from ultralytics import YOLO

# Load YOLOv12x model
model = YOLO("yolov12x.pt")

# Path to your YAML file
hyperparameters_path = '/fs/nexus-scratch/apalnitk/ylo/pure/best_hyp.yaml'

# Load hyperparameters from YAML file
with open(hyperparameters_path, 'r') as file:
    hyperparameters = yaml.safe_load(file)

# Update model overrides with the loaded hyperparameters
model.overrides.update(hyperparameters)

# Train the model with your hyperparameters
model.train(
    data="/fs/nexus-scratch/apalnitk/ylo/pure/data.yaml",  # Your data config file
    epochs=50,             # Total number of training epochs
    imgsz=512,             # Target image size
    name='yolo_small_obj', # Name for this training run
    batch=8,               # Lower per-GPU batch size
    device=0,              # Use GPU device 0
    augment=True,          # Enable augmentation
    multi_scale=True,      # Enable multi-scale training
    amp=True,              # Enable mixed precision training
)

