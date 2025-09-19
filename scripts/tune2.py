from ultralytics import YOLO

# Load your YOLO model (using a pretrained weight or a config file)
model = YOLO("yolov12x.pt")

data="/fs/nexus-scratch/apalnitk/ylo/pure/data.yaml",  # Path to your dataset config
result_grid = model.tune(data=data, use_ray=True)
