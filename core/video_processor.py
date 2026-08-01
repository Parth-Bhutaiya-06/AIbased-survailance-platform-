import cv2


class VideoProcessor:

    def __init__(self, source):
        # On Windows, DirectShow (CAP_DSHOW) opens the webcam instantly (under 0.5 seconds)
        if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
            self.cap = cv2.VideoCapture(int(source), cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(source)

    def read_frame(self):

        success, frame = self.cap.read()

        return success, frame

    def release(self):

        self.cap.release()