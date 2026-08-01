# config/config.py
import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model Path (yolov8m is medium/highly accurate, yolov8s is standard, yolov8n is fast/lightweight)
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8m.pt")
# MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8s.pt")
# MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8n.pt")

# Video Source (0 for webcam, or path to video file)
VIDEO_SOURCE = 0

# Confidence Threshold (Lowered to 0.35 to detect background and partially occluded objects like chairs/backpacks)
CONFIDENCE_THRESHOLD = 0.35

# Classes of Interest (includes all COCO classes except train [6])
CLASSES_OF_INTEREST = [i for i in range(80) if i not in [6]]

# Outputs
OUTPUT_VIDEO = os.path.join(BASE_DIR, "outputs", "tracked_output.mp4")
DATABASE_PATH = os.path.join(BASE_DIR, "database", "tracking.db")

# Display
WINDOW_NAME = "Surveillance Analytics"