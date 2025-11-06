
class DummyCamera:
    def read_frame(self):
        return None
    def stop(self):
        pass
    def recognize_face(self):
        return {"message": "Camera not configured."}
    def recognize_vehicle(self):
        return {"message": "Camera not configured."}

camera = DummyCamera()

# New variable to hold the active camera source ('webcam' or a CCTV URL)
active_camera_source = 'webcam'

def set_camera_source(source):
    """Sets the active camera source."""
    global active_camera_source
    active_camera_source = source
