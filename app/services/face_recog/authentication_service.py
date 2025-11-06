from deepface import DeepFace
import cv2
import numpy as np
from app.db import get_db_connection
import os

def authenticate_face(frame):
    """
    Authenticates a face by comparing it against the selfies of all visitors currently 'Inside'.
    """
    db_connection = get_db_connection()
    try:
        with db_connection.cursor() as cursor:
            # Fetch the selfie paths and names of all visitors with 'Inside' status
            sql = "SELECT selfie_photo_path, first_name, last_name FROM visitors WHERE status = 'Inside'"
            cursor.execute(sql)
            inside_visitors = cursor.fetchall()
    finally:
        db_connection.close()

    if not inside_visitors:
        return {"authenticated": False, "message": "No visitors are currently inside."}

    for visitor in inside_visitors:
        selfie_path = visitor['selfie_photo_path']
        full_name = f"{visitor['first_name']} {visitor['last_name']}"

        # Ensure the selfie file exists
        if not os.path.exists(selfie_path):
            continue

        try:
            # Use DeepFace to verify the face in the frame against the visitor's selfie
            result = DeepFace.verify(img1_path=frame, img2_path=selfie_path, model_name="Facenet512", detector_backend="mtcnn")
            
            if result['verified']:
                return {"authenticated": True, "visitor_name": full_name}
        except Exception as e:
            # This can happen if no face is detected in the frame
            print(f"DeepFace error: {e}")
            continue

    return {"authenticated": False, "message": "Unknown visitor."}
