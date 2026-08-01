import time

class FPSCounter:

    def __init__(self):
        self.prev_time = time.time()

    def get_fps(self):

        current_time = time.time()

        elapsed = current_time - self.prev_time

        self.prev_time = current_time

        if elapsed == 0:
            return 0

        return int(1 / elapsed)