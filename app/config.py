import os
from dotenv import load_dotenv
from app.camera import Camera

# Load environment variables
load_dotenv()

# Camera config
camera = Camera(camera_type="webcam", source=0)
# To switch: camera = Camera(camera_type="ip", source="rtsp://192.168.1.10/stream")

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# MySQL config
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "isecure")