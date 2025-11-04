import cv2
import pytesseract
from fastapi import UploadFile
import numpy as np

def detect_vehicle_plate(file: UploadFile):
    img_array = np.frombuffer(file.file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plate_text = pytesseract.image_to_string(gray)
    file.file.seek(0)
    return plate_text.strip()


def detect_vehicle_color(file: UploadFile):
    img_array = np.frombuffer(file.file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 3
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    counts = np.bincount(labels.flatten())
    dominant = centers[np.argmax(counts)]
    color = tuple(int(c) for c in dominant)
    file.file.seek(0)
    return color


