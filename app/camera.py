import threading
import cv2
from app.services.face_recog.face_service import recognize_face_from_frame
from app.services.vehicle_recog.vehicle_services import detect_vehicle_plate, detect_vehicle_color
from io import BytesIO
from fastapi import UploadFile

class Camera:
    def __init__(self, camera_type="webcam", source=0):
        self.source = source
        self.cap = None
        self.running = False
        self.frame = None
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        if not self.running:
            self.cap = cv2.VideoCapture(self.source)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # 16:9 aspect ratio for landscape
            self.running = True
            # Start thread to continuously read frames
            self.thread = threading.Thread(target=self._update_frame, daemon=True)
            self.thread.start()

    def _update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                self.frame = None

    def read_frame(self):
        if not self.running:
            self.start()
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def recognize_face(self):
        frame = self.read_frame()
        if frame is not None:
            return recognize_face_from_frame(frame)
        return {"recognized": False}

    def recognize_vehicle(self):
        frame = self.read_frame()
        if frame is None:
            return {"plate_number": "", "color": (0, 0, 0)}
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            return {"plate_number": "", "color": (0, 0, 0)}
        img_bytes = buffer.tobytes()
        file_like = BytesIO(img_bytes)
        upload_file = UploadFile(filename="frame.jpg", file=file_like)
        plate = detect_vehicle_plate(upload_file)
        upload_file.file.seek(0)
        color = detect_vehicle_color(upload_file)
        return {"plate_number": plate, "color": color}

    def stop(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
            if self.thread:
                self.thread.join(timeout=1.0)
