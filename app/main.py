import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import os
from app.db import get_db_connection
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np
import time

app = FastAPI(title="iSecure Recognition API")

# ThreadPool for CPU-heavy tasks
executor = ThreadPoolExecutor(max_workers=4)

# Allow PHP frontend (Apache) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
def shutdown_event():
    # Properly release the camera resource on shutdown
    camera.stop()

@app.post("/recognize/vehicle")
async def recognize_vehicle(file: UploadFile = File(...)):
    try:
        plate = await asyncio.get_event_loop().run_in_executor(executor, detect_vehicle_plate, file)
        return {"plate_number": plate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr/id")
async def ocr_id(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = await asyncio.get_event_loop().run_in_executor(executor, extract_id_info, contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "API running"}

@app.get("/camera/frame")
def get_camera_frame():
    def generate():
        while True:
            frame = camera.read_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)  # Adjust frame rate, e.g., 10 fps
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/camera/single_frame")
def get_single_frame():
    frame = camera.read_frame()
    if frame is not None:
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            return Response(content=buffer.tobytes(), media_type='image/jpeg')
    # Fallback blank frame
    blank = cv2.zeros((480, 640, 3), dtype=np.uint8)
    ret, buffer = cv2.imencode('.jpg', blank)
    return Response(content=buffer.tobytes(), media_type='image/jpeg')

@app.get("/camera/recognize_vehicle")
def recognize_vehicle_endpoint():
    try:
        result = camera.recognize_vehicle()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register/face")
async def register_face_endpoint(file: UploadFile = File(...), session_token: str = ""):
    if not session_token:
        raise HTTPException(status_code=400, detail="Session token is required.")

    upload_dir = "public/uploads/selfies"
    os.makedirs(upload_dir, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"{session_token}.{file_extension}"
    file_path = os.path.join(upload_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        db_connection = get_db_connection()
        try:
            with db_connection.cursor() as cursor:
                sql = "UPDATE visitor_sessions SET selfie_photo_path = %s WHERE user_token = %s"
                cursor.execute(sql, (file_path, session_token))
            db_connection.commit()
        finally:
            db_connection.close()

        return {"message": "Face registered successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register face: {str(e)}")
