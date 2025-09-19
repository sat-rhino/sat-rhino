import yaml
from ultralytics import YOLO
import wandb

# Load YOLOv12x model
model = YOLO("yolov12x.pt")

# Path to your YAML file containing hyperparameters
hyperparameters_path = '/fs/nexus-scratch/apalnitk/ylo/pure/big.yaml'

# Load hyperparameters from YAML file
with open(hyperparameters_path, 'r') as file:
    yaml_hyperparameters = yaml.safe_load(file)

# Define default hyperparameters directly in the train method
default_hyperparameters = {
    'data': "/fs/nexus-scratch/apalnitk/ylo/pure/pure.yaml",  # Your data config file
    'epochs': 50,             # Total number of training epochs
    'imgsz': 512,             # Target image size
    'name': 'yolo_small_obj', # Name for this training run
    'batch': 8,               # Lower per-GPU batch size
    'device': 0,              # Use GPU device 0
    'augment': True,          # Enable augmentation
    'multi_scale': True,      # Enable multi-scale training
    'amp': True,              # Enable mixed precision training
}

# Merge YAML hyperparameters with default hyperparameters
# YAML hyperparameters take precedence over default ones
merged_hyperparameters = {**default_hyperparameters, **yaml_hyperparameters}

# Save data.yaml to wandb as an artifact
wandb.init()
data_artifact = wandb.Artifact("data_yaml", type="dataset")
data_artifact.add_file(default_hyperparameters['data'])
data_artifact.add_file(hyperparameters_path)
wandb.log_artifact(data_artifact)

merged_hyperparameters['epochs'] = 100
# Train the model with the merged hyperparameters
model.train(**merged_hyperparameters)

wandb.finish()
