# main.py
import cv2
import os
import time
import threading
import numpy as np
from config.config import *

from core.tracker import ObjectTracker
from core.video_processor import VideoProcessor
from core.performance import FPSCounter
from core.counter import ObjectCounter
from core.logger import TrackingLogger
from core.reid import AppearanceReID
from database.database import DatabaseManager

# Get dynamic project root directory from config
PROJECT_ROOT = BASE_DIR

# Initialize core components
tracker = ObjectTracker(MODEL_PATH)
video = VideoProcessor(VIDEO_SOURCE)
fps_counter = FPSCounter()
db_manager = DatabaseManager(DATABASE_PATH)
counter = ObjectCounter()
reid_handler = AppearanceReID()

# Initialize file logger targeting reports/event_log.txt
log_file = os.path.join(PROJECT_ROOT, "reports", "event_log.txt")
logger = TrackingLogger(log_file_path=log_file)

logger.info("Initializing Asynchronous Surveillance AI Platform...")
logger.info(f"Loaded YOLOv8 model from: {MODEL_PATH}")
logger.info(f"Database path set to: {DATABASE_PATH}")

# Setup video writer (always output at 640x480 for standardized CPU-resized files)
width, height = 640, 480
fps_val = video.cap.get(cv2.CAP_PROP_FPS)

# Fallback for webcam or unreadable video properties
if fps_val <= 0 or fps_val > 100:
    fps_val = 20.0

os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out_writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps_val, (width, height))
logger.info(f"Saving tracked output video to: {OUTPUT_VIDEO}")

def get_color(obj_id):
    """
    Generates a deterministic color based on the object ID to keep box colors consistent.
    """
    np.random.seed(obj_id & 0xFFFF)
    color = tuple(int(x) for x in np.random.randint(40, 230, size=3))
    return color

# Global variables for thread synchronization
frame_to_process = None
last_results = None
thread_lock = threading.Lock()
running = True

def tracking_thread_fn(tracker_obj, conf, classes):
    """
    Background worker thread running heavy YOLOv8 tracking inference asynchronously.
    """
    global frame_to_process, last_results, running
    
    while running:
        frame_copy = None
        with thread_lock:
            if frame_to_process is not None:
                frame_copy = frame_to_process.copy()
                frame_to_process = None  # Consume frame
        
        if frame_copy is not None:
            # Run heavy ML tracking in the background
            results = tracker_obj.track(frame_copy, conf=conf, classes=classes)
            with thread_lock:
                last_results = results
        else:
            # Small sleep to prevent CPU spinning when idle
            time.sleep(0.005)

# Start background tracking thread
tracking_thread = threading.Thread(
    target=tracking_thread_fn,
    args=(tracker, CONFIDENCE_THRESHOLD, CLASSES_OF_INTEREST),
    daemon=True
)
tracking_thread.start()

# Tracking event memory to avoid duplicate logs in rapid frames for same ID
logged_ids = set()

# Bounding box cache for UI rendering
current_boxes = []
current_ids = []
current_clss = []

while True:
    # Read frame
    success, frame = video.read_frame()

    if not success:
        logger.info("Finished processing video stream or source disconnected.")
        break

    # Resize frame to standard 640x480 to significantly boost CPU processing
    frame = cv2.resize(frame, (640, 480))

    # Send the current frame to the background thread for asynchronous tracking
    with thread_lock:
        frame_to_process = frame.copy()

    # Retrieve and process tracking updates if the background thread has finished
    with thread_lock:
        if last_results is not None:
            results = last_results
            last_results = None  # Consume the result

            if results[0].boxes is not None:
                if results[0].boxes.id is not None:
                    boxes = results[0].boxes.xyxy.cpu().numpy()
                    ids = results[0].boxes.id.int().cpu().tolist()
                    clss = results[0].boxes.cls.int().cpu().tolist()

                    assigned_ids = set()
                    temp_boxes = []
                    temp_ids = []
                    temp_clss = []

                    # Process detections and match with persistent Re-ID memory
                    for box, tracker_id, cls_id in zip(boxes, ids, clss):
                        class_name = tracker.model.names[cls_id]

                        # Match or Register with our custom Re-ID module using assigned_ids filter
                        persistent_id = reid_handler.match_or_register(frame, box, class_name, tracker_id, assigned_ids)
                        assigned_ids.add(persistent_id)

                        temp_boxes.append(box)
                        temp_ids.append(persistent_id)
                        temp_clss.append(cls_id)

                        # Update unique object counter
                        counter.update(persistent_id)

                        # Insert raw logging data into database for analytics dashboard
                        db_manager.insert_log(
                            timestamp=logger.get_timestamp(),
                            object_id=persistent_id,
                            object_class=class_name,
                            is_intrusion=0
                        )

                        # File/Console logger updates (log once per ID to prevent log bloat)
                        if persistent_id not in logged_ids:
                            logger.info(f"New object detected - ID: {persistent_id}, Class: {class_name}")
                            logged_ids.add(persistent_id)

                    # Update active boxes cache
                    current_boxes = temp_boxes
                    current_ids = temp_ids
                    current_clss = temp_clss
                else:
                    # Reset active boxes cache if YOLO found nothing
                    current_boxes = []
                    current_ids = []
                    current_clss = []

    # Draw active bounding boxes on the current raw frame
    annotated_frame = frame.copy()
    for box, persistent_id, cls_id in zip(current_boxes, current_ids, current_clss):
        class_name = tracker.model.names[cls_id]
        x1, y1, x2, y2 = map(int, box)
        color = get_color(persistent_id)

        # Draw box border
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

        # Draw custom label tag
        label_text = f"ID {persistent_id}: {class_name}"
        (lbl_w, lbl_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(annotated_frame, (x1, y1 - lbl_h - 10), (x1 + lbl_w + 5, y1), color, -1)
        cv2.putText(
            annotated_frame,
            label_text,
            (x1 + 3, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    # Calculate UI Display FPS
    fps = fps_counter.get_fps()

    # Create semi-transparent overlay for telemetry HUD
    hud_overlay = annotated_frame.copy()
    cv2.rectangle(hud_overlay, (10, 10), (330, 90), (0, 0, 0), -1)
    cv2.addWeighted(hud_overlay, 0.6, annotated_frame, 0.4, 0, annotated_frame)

    # Render telemetry text on HUD
    cv2.putText(
        annotated_frame,
        f"FPS: {fps}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )
    cv2.putText(
        annotated_frame,
        f"Total Unique Objects: {counter.get_count()}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 0),
        2,
        cv2.LINE_AA
    )

    # Write frame to output video file
    out_writer.write(annotated_frame)

    # Show live window output (will skip if running in headless environment)
    try:
        cv2.imshow(WINDOW_NAME, annotated_frame)
    except cv2.error:
        pass

    # Quit on 'q' (waitKey(10) caps maximum FPS at 100 to ensure smooth, natural video display)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        logger.info("Application manual exit triggered.")
        break

# Cleanup
running = False
tracking_thread.join(timeout=1.0)
video.release()
out_writer.release()
cv2.destroyAllWindows()
logger.info("Surveillance components shut down successfully.")