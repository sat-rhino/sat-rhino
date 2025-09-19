import yaml
from ultralytics import YOLO

# Load YOLOv12x model
model = YOLO("yolov12x.pt")

# Path to your dataset config
data_path = "/fs/nexus-scratch/apalnitk/ylo/pure/data.yaml"

# Tune hyperparameters on COCO8 for 30 epochs,
# with reduced space usage by disabling saving and plotting.
model.tune(
    data=data_path,
    epochs=300,
    iterations=300,
    batch=6,
    imgsz=640,
    optimizer="AdamW",
    save=False,    # Do not save intermediate models to disk
    plots=False,   # Do not generate plots
    verbose=False  # Optional: Reduce logging output
)

