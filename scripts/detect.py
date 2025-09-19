from ultralytics import YOLO

model = YOLO('/fs/nexus-scratch/apalnitk/ylo/pure/runs/detect/yolo_x_ele_all-real3/weights/best.pt')

model.val(data='/fs/nexus-scratch/apalnitk/ylo/pure/data.yaml', batch=256)
