
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
