import os
from ultralytics import YOLO


class ObjectTracker:

    def __init__(self, model_path):
        self.model = YOLO(model_path)
        # Load the custom tracker configuration file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tracker_config = os.path.join(base_dir, "config", "custom_tracker.yaml")
        if not os.path.exists(self.tracker_config):
            self.tracker_config = "bytetrack.yaml"

    def track(self, frame, conf=0.5, classes=None):

        results = self.model.track(
            frame,
            persist=True,
            tracker=self.tracker_config,
            verbose=False,
            conf=conf,
            classes=classes
        )

        return results