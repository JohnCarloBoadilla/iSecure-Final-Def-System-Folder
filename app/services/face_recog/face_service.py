import face_recognition
import numpy as np
import json
from fastapi import UploadFile
from app.db import get_db_connection
import cv2
import os



def get_all_visitors_encodings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name as name, selfie_photo_path FROM visitors WHERE selfie_photo_path IS NOT NULL")
    visitors = cursor.fetchall()
    conn.close()

    encodings_list = []
    for v in visitors:
        path = v["selfie_photo_path"]
        if path and os.path.exists(path):
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                encodings_list.append({"id": v["id"], "name": v["name"], "face_encoding": encodings[0]})
    return encodings_list

def get_all_personnels_encodings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name as name, selfie_photo_path FROM personnels WHERE selfie_photo_path IS NOT NULL")
    personnels = cursor.fetchall()
    conn.close()

    encodings_list = []
    for p in personnels:
        path = p["selfie_photo_path"]
        if path and os.path.exists(path):
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                encodings_list.append({"id": p["id"], "name": p["name"], "face_encoding": encodings[0]})
    return encodings_list

def update_visitor_time_in(visitor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE visitors SET time_in = NOW() WHERE id = %s", (visitor_id,))
    conn.commit()
    conn.close()

def update_personnel_time_in(personnel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE personnels SET time_in = NOW() WHERE id = %s", (personnel_id,))
    conn.commit()
    conn.close()

def recognize_face_from_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    uploaded_encodings = face_recognition.face_encodings(rgb_frame)
    
    if not uploaded_encodings:
        return {"recognized": False}
    
    uploaded_encoding = uploaded_encodings[0]
    visitors = get_all_visitors_encodings()
    personnels = get_all_personnels_encodings()

    for visitor in visitors:
        known_encoding = np.array(visitor["face_encoding"])
        match = face_recognition.compare_faces([known_encoding], uploaded_encoding, tolerance=0.5)
        if match[0]:
            update_visitor_time_in(visitor["id"])
            return {"recognized": True, "type": "visitor", "id": visitor["id"], "name": visitor["name"]}

    for personnel in personnels:
        known_encoding = np.array(personnel["face_encoding"])
        match = face_recognition.compare_faces([known_encoding], uploaded_encoding, tolerance=0.5)
        if match[0]:
            update_personnel_time_in(personnel["id"])
            return {"recognized": True, "type": "personnel", "id": personnel["id"], "name": personnel["name"]}

    return {"recognized": False}

def recognize_face(file: UploadFile):
    image = face_recognition.load_image_file(file.file)
    uploaded_encodings = face_recognition.face_encodings(image)

    if not uploaded_encodings:
        return {"recognized": False}

    uploaded_encoding = uploaded_encodings[0]
    visitors = get_all_visitors_encodings()
    personnels = get_all_personnels_encodings()

    for visitor in visitors:
        known_encoding = np.array(visitor["face_encoding"])
        match = face_recognition.compare_faces([known_encoding], uploaded_encoding, tolerance=0.5)
        if match[0]:
            update_visitor_time_in(visitor["id"])
            return {"recognized": True, "type": "visitor", "id": visitor["id"], "name": visitor["name"]}

    for personnel in personnels:
        known_encoding = np.array(personnel["face_encoding"])
        match = face_recognition.compare_faces([known_encoding], uploaded_encoding, tolerance=0.5)
        if match[0]:
            update_personnel_time_in(personnel["id"])
            return {"recognized": True, "type": "personnel", "id": personnel["id"], "name": personnel["name"]}

    return {"recognized": False}

def compare_faces(file1: UploadFile, file2: UploadFile):
    image1 = face_recognition.load_image_file(file1.file)
    image2 = face_recognition.load_image_file(file2.file)

    encodings1 = face_recognition.face_encodings(image1)
    encodings2 = face_recognition.face_encodings(image2)

    if not encodings1 or not encodings2:
        return {"match": False, "message": "No face detected in one or both images"}

    encoding1 = encodings1[0]
    encoding2 = encodings2[0]

    match = face_recognition.compare_faces([encoding1], encoding2, tolerance=0.5)
    return {"match": bool(match[0]), "message": "Faces match" if match[0] else "Faces do not match"}

def real_time_compare_faces(frame_bytes: bytes, selfie_path: str):
    try:
        import os
        from PIL import Image
        import io

        # Load frame image from bytes
        frame_image = Image.open(io.BytesIO(frame_bytes)).convert("RGB")
        frame_np = np.array(frame_image)

        # Detect face locations and encodings in frame
        frame_face_locations = face_recognition.face_locations(frame_np)
        frame_face_encodings = face_recognition.face_encodings(frame_np, frame_face_locations)

        if not frame_face_encodings:
            return {"match": False, "message": "No face detected in camera frame", "boxes": []}

        # Load selfie image from file path
        if not os.path.exists(selfie_path):
            return {"match": False, "message": "Selfie image not found", "boxes": []}

        selfie_image = face_recognition.load_image_file(selfie_path)
        selfie_encodings = face_recognition.face_encodings(selfie_image)

        if not selfie_encodings:
            return {"match": False, "message": "No face detected in selfie image", "boxes": []}

        selfie_encoding = selfie_encodings[0]

        # Compare each face in frame to selfie encoding
        boxes = []
        match_found = False
        for (top, right, bottom, left), face_encoding in zip(frame_face_locations, frame_face_encodings):
            matches = face_recognition.compare_faces([selfie_encoding], face_encoding, tolerance=0.4)
            face_distance = face_recognition.face_distance([selfie_encoding], face_encoding)[0]
            confidence = max(0, 1 - face_distance)  # Confidence score between 0 and 1

            if matches[0]:
                match_found = True
                boxes.append({"top": top, "right": right, "bottom": bottom, "left": left, "match": True, "confidence": confidence})
            else:
                boxes.append({"top": top, "right": right, "bottom": bottom, "left": left, "match": False, "confidence": confidence})

        return {"match": match_found, "message": "Face comparison completed", "boxes": boxes}
    except Exception as e:
        print(f"Error in real_time_compare_faces: {str(e)}")
        return {"match": False, "message": f"Error: {str(e)}", "boxes": []}
