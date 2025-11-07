import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, Response, stream_with_context, abort
import os
from app.db import get_db_connection
from app.config import set_camera_source, camera_facial, camera_vehicle
from app.services.face_recog.authentication_service import authenticate_face
from app.services.vehicle_recog.license_plate_ocr_scanner import detect_vehicle_plate
from app.services.ocr.ocr_service import extract_id_info
from flask_cors import CORS
import asyncio
import cv2
import numpy as np
import time
import tempfile
import json

app = Flask(__name__)

# Allow PHP frontend (Apache) to access this API
CORS(app, resources={r"/*": {"origins": "*"}})



@app.route("/recognize/vehicle", methods=["POST"])
def recognize_vehicle():
    try:
        if 'file' not in request.files:
            abort(400, description="No file part")
        file = request.files['file']
        if file.filename == '':
            abort(400, description="No selected file")
        
        # Read the file content directly
        contents = file.read()
        plate = detect_vehicle_plate(contents)
        return jsonify({"plate_number": plate})
    except Exception as e:
        abort(500, description=str(e))

@app.route("/ocr/id", methods=["POST"])
def ocr_id():
    try:
        if 'file' not in request.files:
            abort(400, description="No file part")
        file = request.files['file']
        if file.filename == '':
            abort(400, description="No selected file")
        
        contents = file.read()
        result = extract_id_info(contents)
        return jsonify(result)
    except Exception as e:
        abort(500, description=str(e))

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API running"})

@app.route("/camera/facial/frame", methods=["GET"])
def get_camera_facial_frame():
    def generate_facial():
        while True:
            frame = camera_facial.read_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
    return Response(stream_with_context(generate_facial()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/camera/vehicle/frame", methods=["GET"])
def get_camera_vehicle_frame():
    def generate_vehicle():
        while True:
            frame = camera_vehicle.read_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
    return Response(stream_with_context(generate_vehicle()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/camera/facial/single_frame", methods=["GET"])
def get_single_facial_frame():
    frame = camera_facial.read_frame()
    if frame is not None:
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            return Response(buffer.tobytes(), mimetype='image/jpeg')
    blank = cv2.zeros((480, 640, 3), dtype=np.uint8)
    ret, buffer = cv2.imencode('.jpg', blank)
    return Response(buffer.tobytes(), mimetype='image/jpeg')

@app.route("/camera/recognize_vehicle", methods=["GET"])
def recognize_vehicle_endpoint():
    try:
        frame = camera_vehicle.read_frame()
        if frame is None:
            return jsonify({"error": "Could not get frame from vehicle camera"}), 500
        
        # The rest of the recognition logic would go here
        # For now, just returning a success message
        return jsonify({"message": "Vehicle recognition triggered with vehicle camera."})
    except Exception as e:
        abort(500, description=str(e))

@app.route("/camera/source", methods=["POST"])
def set_camera_source_endpoint():
    try:
        data = request.get_json()
        camera_type = data.get('camera_type')
        source = data.get('source')
        if not all([camera_type, source]):
            abort(400, description="`camera_type` and `source` are required.")
        
        set_camera_source(camera_type, source)
        return jsonify({"message": f"{camera_type.capitalize()} camera source set to {source}"})
    except Exception as e:
        abort(500, description=str(e))

@app.route("/authenticate/face", methods=["POST"])
def authenticate_face_endpoint():
    try:
        if 'file' not in request.files:
            abort(400, description="No file part")
        file = request.files['file']
        if file.filename == '':
            abort(400, description="No selected file")

        # Save the uploaded frame to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_frame:
            content = file.read()
            temp_frame.write(content)
            temp_frame_path = temp_frame.name
        
        # Run authentication
        result = authenticate_face(temp_frame_path)
        
        # Clean up the temporary file
        os.unlink(temp_frame_path)
        
        return jsonify(result)
    except Exception as e:
        # Clean up in case of an error
        if 'temp_frame_path' in locals() and os.path.exists(temp_frame_path):
            os.unlink(temp_frame_path)
        abort(500, description=str(e))

@app.route("/register/face", methods=["POST"])
def register_face_endpoint():
    session_token = request.form.get('session_token')
    if not session_token:
        abort(400, description="Session token is required.")

    if 'file' not in request.files:
        abort(400, description="No file part")
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No selected file")

    upload_dir = "public/uploads/selfies"
    os.makedirs(upload_dir, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"{session_token}.{file_extension}"
    file_path = os.path.join(upload_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            content = file.read()
            buffer.write(content)
        
        db_connection = get_db_connection()
        try:
            with db_connection.cursor() as cursor:
                sql = "UPDATE visitor_sessions SET selfie_photo_path = %s WHERE user_token = %s"
                cursor.execute(sql, (file_path, session_token))
            db_connection.commit()
        finally:
            db_connection.close()

        return jsonify({"message": "Face registered successfully", "file_path": file_path})
    except Exception as e:
        abort(500, description=f"Failed to register face: {str(e)}")

@app.route("/camera/recognize_and_compare_plate", methods=["POST"])
def recognize_and_compare_plate():
    try:
        data = request.get_json()
        expected_plate = data.get('expected_plate_number')
        if not expected_plate:
            abort(400, description="Expected plate number is required.")

        frame = camera_vehicle.read_frame()
        if frame is None:
            abort(500, description="Could not capture frame from vehicle camera.")

        # Save the captured frame for auditing
        output_dir = "ID' Data for ocr/"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}_capture.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            abort(500, description="Could not encode frame.")
        
        image_bytes = buffer.tobytes()
        recognized_plate = detect_vehicle_plate(image_bytes)

        # --- New: Save the recognized data to a JSON file ---
        json_output_folder = "License Plate Data/"
        os.makedirs(json_output_folder, exist_ok=True)

        plate_data = {
            "id_type": "philippine_license_plate",
            "license_plate_number": recognized_plate if recognized_plate else "Not found",
            "vehicle_type": "Not found"  # This isn't provided by the current service
        }

        base_name = os.path.splitext(filename)[0]
        json_filename = f"{base_name}.json"
        json_path = os.path.join(json_output_folder, json_filename)

        with open(json_path, 'w') as f:
            json.dump(plate_data, f, indent=4)
        # --- End new logic ---

        if recognized_plate is None:
            return jsonify({
                "match": False,
                "recognized_plate": "Not found",
                "message": "Could not detect a license plate."
            })

        match = (recognized_plate.strip().upper() == expected_plate.strip().upper())
        
        return jsonify({
            "match": match,
            "recognized_plate": recognized_plate
        })

    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
