from datetime import datetime
import os


class TrackingLogger:

    def __init__(self, log_file_path=None):
        self.log_file_path = log_file_path
        if self.log_file_path:
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def get_timestamp(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def _write_to_file(self, formatted_msg):
        if self.log_file_path:
            try:
                with open(self.log_file_path, "a") as f:
                    f.write(formatted_msg + "\n")
            except Exception as e:
                print(f"[ERROR] Failed to write to log file: {e}")

    def info(self, message):
        timestamp = self.get_timestamp()
        formatted_msg = f"[{timestamp}] [INFO] {message}"
        print(formatted_msg)
        self._write_to_file(formatted_msg)

    def warning(self, message):
        timestamp = self.get_timestamp()
        formatted_msg = f"[{timestamp}] [WARNING] {message}"
        print(formatted_msg)
        self._write_to_file(formatted_msg)

    def error(self, message):
        timestamp = self.get_timestamp()
        formatted_msg = f"[{timestamp}] [ERROR] {message}"
        print(formatted_msg)
        self._write_to_file(formatted_msg)