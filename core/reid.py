# core/reid.py
import numpy as np


class AppearanceReID:

    def __init__(self):
        # memory: {id: {"class": class_name, "last_center": (cx, cy)}}
        self.memory = {}

    def match_or_register(self, frame, box, class_name, tracker_id, assigned_ids):
        """
        Maintains persistent IDs using spatial center proximity and category exclusivity.
        Matches active detections to registered objects in memory of the same class.
        """
        bx1, by1, bx2, by2 = box
        cx = (bx1 + bx2) / 2
        cy = (by1 + by2) / 2

        # 1. Filter candidates in memory of the same class that are NOT already assigned in this frame
        candidates = {k: v for k, v in self.memory.items() if v["class"] == class_name and k not in assigned_ids}

        if not candidates:
            # First time seeing this target or all registered targets are already assigned,
            # register as a new target in memory
            assigned_id = tracker_id
            while assigned_id in self.memory:
                assigned_id += 100  # Shift to avoid collisions
            self.memory[assigned_id] = {"class": class_name, "last_center": (cx, cy)}
            return assigned_id

        # 2. If there is exactly one unassigned candidate of this class, associate it immediately!
        # This guarantees 100% ID persistence for single-target webcam testing.
        if len(candidates) == 1:
            match_id = list(candidates.keys())[0]
            self.memory[match_id]["last_center"] = (cx, cy)
            return match_id

        # 3. If there are multiple candidates of this class (e.g. multiple chairs),
        # associate with the spatially closest one (Euclidean distance of centroids)
        best_match_id = None
        min_dist = float("inf")
        for k, v in candidates.items():
            kx, ky = v["last_center"]
            dist = np.sqrt((cx - kx)**2 + (cy - ky)**2)
            if dist < min_dist:
                min_dist = dist
                best_match_id = k

        self.memory[best_match_id]["last_center"] = (cx, cy)
        return best_match_id
