from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.services.face_recog.face_service import recognize_face, compare_faces, real_time_compare_faces
from app.services.vehicle_recog.vehicle_services import detect_vehicle_plate
from app.services.ocr.ocr_services import extract_id_info
from app.config import camera
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

@app.post("/recognize/face")
async def recognize_face_endpoint(file: UploadFile = File(...)):
    try:
        result = await asyncio.get_event_loop().run_in_executor(executor, recognize_face, file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare/faces")
async def compare_faces_endpoint(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        result = await asyncio.get_event_loop().run_in_executor(executor, compare_faces, file1, file2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/real_time_compare/faces")
async def real_time_compare_faces_endpoint(file: UploadFile = File(...), selfie_path: str = ""):
    try:
        frame_bytes = await file.read()
        from app.services.face_recog.face_service import real_time_compare_faces
        result = await asyncio.get_event_loop().run_in_executor(executor, real_time_compare_faces, frame_bytes, selfie_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/camera/recognize_face")
def recognize_face_endpoint():
    try:
        result = camera.recognize_face()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/camera/recognize_vehicle")
def recognize_vehicle_endpoint():
    try:
        result = camera.recognize_vehicle()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
