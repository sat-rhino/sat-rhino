# Rhinoceros Detection

This is the official repository for the paper ``Automated Rhinoceros Detection in Satellite Imagery using Deep Learning'' *Scienticic Reports*. The repository contains scripts and configuration files for training and evaluating a YOLOv12 object detection model to detect rhinoceroses in satellite imagery, including a pipeline for generating synthetic training data using Blender. 

## Repository Structure and Usage

### Key Directories:

*   `scripts/`: Contains the core Python scripts for data processing, synthetic data generation, model training, and evaluation.
*   `sets/`: Holds YAML configuration files defining the datasets (training, validation, test splits) used by the YOLO model. These files specify image paths and class information.
*   `hyperparams/`: Contains YAML files specifying hyperparameters for YOLO model training (e.g., learning rate, batch size, optimizer).

### Core Scripts (`scripts/`):

*   `sim.py`: Uses the [Blender Python API](https://pypi.org/project/bpy/) (`bpy`) to generate synthetic satellite images of rhinoceroses. It sets up a 3D scene, places rhino models randomly on a textured plane, configures lighting and camera, and renders images with corresponding labels. This is used to augment the training data as described in the paper.
*   `patch.py`: Implements the image tiling strategy mentioned in the paper. It takes large satellite images (e.g., TIFFs) and corresponding annotation files (YOLO format) and divides them into smaller, overlapping patches suitable for model training (e.g., 512x512 pixels). It adjusts annotation coordinates for each patch.
*   `coco2yolo.py` (or `script.py`): Converts object detection annotations from COCO JSON format to the YOLO `.txt` format required for training. It reads a COCO file, converts bounding box coordinates, and creates individual label files for each image, organizing them into the necessary directory structure.
*   `yolo_run.py`: Executes the YOLOv12 model training process using the `ultralytics` library. It loads a base model, applies hyperparameters from a specified `.yaml` file (e.g., `hyperparams/best_hyp.yaml`), uses a dataset configuration from `sets/`, and runs the training loop with defined settings (epochs, image size, augmentation, etc.).
*   `detect.py`: Performs model evaluation. It loads a trained YOLO model checkpoint (`best.pt`) and runs the validation (`model.val()`) method on a specified dataset configuration (`sets/data.yaml`) to calculate performance metrics like mAP.
*   `tune.py`: Implements hyperparameter tuning for the YOLO model using the `ultralytics` library's `model.tune()` function. It searches for optimal hyperparameters based on performance on the specified dataset.

### Configuration Files:

*   `sets/*.yaml` (e.g., `data.yaml`, `data_synth.yaml`, `pure.yaml`): Define dataset configurations for YOLO. They specify paths to train, validation, and test image sets, the number of classes, and class names. Different files might represent different data mixes (e.g., real only, synthetic only, combined).
*   `hyperparams/*.yaml` (e.g., `best_hyp.yaml`): Define specific hyperparameters used during training (learning rate, optimizer, batch size, etc.), often derived from the tuning process (`tune.py`).

### Other Scripts:

The `scripts/` directory may contain other utility scripts, experimental code, or duplicates (e.g., `patch2.py`, `tune2.py`, `yolo_example_copy.py`). The core functionality is captured by the scripts listed above. 

### Google Drive For Blender Sim and Backgrounds

To access the full simulation in Blender along with the backgrounds, go HERE: https://drive.google.com/drive/folders/131eGJ5P7uJMqY3SAge9DGGt4Ew7bsrtA?usp=drive_link
