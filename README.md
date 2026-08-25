# Car Object Detection from Scratch 🚗

A YOLO-style car object detection system built from scratch with PyTorch, developed to understand the internal mechanics of object detection rather than relying on an off-the-shelf YOLO implementation.

## Project Overview

The goal of this project was not only to train a detector, but to build and investigate the complete detection pipeline:

**Image → Model → Grid Predictions → Bounding Boxes → Confidence → NMS → Detection → Video**

The final model uses a **320×320 input** and a **20×20 prediction grid**, with cell-relative coordinates for object centers and directly normalized width/height predictions.

## What Was Built

The project includes:

* Custom V8 detection model built with PyTorch
* Custom target encoding and decoding
* 20×20 grid-based object detection
* Custom localization and confidence loss
* Controlled training and optimizer validation
* Confidence and localization diagnostics
* IoU-based confidence calibration
* NMS and duplicate-detection analysis
* True validation and unseen-test evaluation
* Temporal stability analysis for video detection
* Real-video inference and visualization

## Key Finding

A major finding during development was that the model could often produce good bounding-box candidates, while its confidence scores did not rank those candidates correctly.

This led to controlled experiments with localization-aware confidence targets. The best candidate improved unseen-test performance without changing the localization channels or model architecture.

## Final Evaluation

Using the validation-selected operating point for the final B_IOU model:

* **Precision:** 0.68
* **Recall:** 0.71
* **F1:** 0.70

The final system was also evaluated on a real **665-frame, 1920×1080 video**.

## Development Approach

Rather than repeatedly changing the model blindly, the project followed a controlled workflow:

**Problem → Hypothesis → Diagnostic Audit → Controlled Experiment → Validation → Unseen Test → Visualization → Final Video**

This helped isolate issues in geometry, decoding, confidence ranking, localization, duplicate suppression, and temporal stability before making model decisions.

## Repository Structure

```text
Object-Detection-from-Scratch/
│
├── data/
│   ├── dataset/
│   └── raw/
│
├── notebooks/
│   └── 01_data_preparation.ipynb
│
├── models/
│
├── src/
│
└── README.md
```

## Technologies

* Python
* PyTorch
* OpenCV
* NumPy
* Pillow
* Jupyter Notebook

## Final Result

The project demonstrates an end-to-end car detection pipeline developed from scratch, from dataset preparation and model design to diagnostic analysis, unseen-test evaluation, and real-video inference.

## GitHub

https://github.com/AzerQasimzade/Object-Detection-from-Scratch.git
