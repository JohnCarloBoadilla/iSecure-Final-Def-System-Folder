import cv2

for i in range(5):  # test camera indices 0-4
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} works!")
        cap.release()
    else:
        print(f"Camera {i} failed")