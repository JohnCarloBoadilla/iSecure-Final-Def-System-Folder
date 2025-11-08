import cv2
import numpy as np
from deepface import DeepFace
import json
import os
import sys
import argparse

# --- Constants ---
MODEL = "Facenet512"
DETECTOR_BACKEND = "mtcnn"
THRESHOLD = 0.4
# Get the absolute path to the project root, assuming this script is in app/services/face_recog/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DB_FILE = os.path.join(project_root, "app", "services", "face_recog", "visitors.json")

# --- Database Functions ---
def load_database():
    if not os.path.exists(os.path.dirname(DB_FILE)):
        os.makedirs(os.path.dirname(DB_FILE))
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    data[k] = np.array(v)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_database(db):
    data = {k: v.tolist() for k, v in db.items()}
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Core Functions ---
def register_visitor(visitor_id, frame_path):
    try:
        if not os.path.exists(frame_path):
            return False, f"Image path does not exist: {frame_path}"

        results = DeepFace.represent(
            img_path=frame_path,
            model_name=MODEL,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True
        )
        
        embedding = np.array(results[0]['embedding'])
        db = load_database()
        db[visitor_id] = embedding
        save_database(db)
        
        return True, f"Visitor {visitor_id} registered successfully."
        
    except Exception as e:
        if "Face could not be detected" in str(e):
            return False, "Registration failed: No face could be detected."
        return False, f"Registration error: {str(e)}"

def authenticate_visitor(frame_path):
    try:
        if not os.path.exists(frame_path):
            return False, f"Image path does not exist: {frame_path}"

        results = DeepFace.represent(
            img_path=frame_path,
            model_name=MODEL,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True
        )
        embedding = np.array(results[0]['embedding'])

        db = load_database()
        if not db:
            return False, "No registered visitors in the database."

        min_dist = float('inf')
        best_id = None
        for vid, emb in db.items():
            cos_sim = np.dot(emb, embedding) / (np.linalg.norm(emb) * np.linalg.norm(embedding))
            dist = 1 - cos_sim
            if dist < min_dist:
                min_dist = dist
                best_id = vid

        if min_dist < THRESHOLD:
            return True, f"Authenticated as {best_id}"
        else:
            return False, f"Rejected (Closest match: {best_id}, Distance: {min_dist:.3f})"
            
    except Exception as e:
        if "Face could not be detected" in str(e):
            return False, "Authentication failed: No face could be detected."
        return False, f"Authentication error: {str(e)}"

# --- Command-Line Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Registration and Authentication CLI")
    parser.add_argument("mode", choices=['register', 'authenticate'], help="The mode to run the script in.")
    parser.add_argument("--id", required=True, help="The visitor ID.")
    parser.add_argument("--image", required=True, help="The absolute path to the image file.")

    args = parser.parse_args()
    
    response = {}

    if args.mode == 'register':
        success, message = register_visitor(args.id, args.image)
        response['success'] = success
        response['message'] = message
    
    elif args.mode == 'authenticate':
        success, message = authenticate_visitor(args.image)
        response['success'] = success
        response['message'] = message
        if success:
            # In case of successful auth, the message is "Authenticated as {id}"
            # We can parse the ID out if needed, but for now the message is sufficient.
            response['visitor_id'] = message.split(" ")[2]

    print(json.dumps(response))

