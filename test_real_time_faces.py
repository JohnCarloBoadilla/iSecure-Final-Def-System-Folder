import requests
import cv2
import numpy as np

# Create a simple test image with a face-like rectangle (since we don't have a real image)
img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.rectangle(img, (200, 150), (440, 330), (255, 255, 255), -1)  # White rectangle as fake face

# Save as JPEG
cv2.imwrite('test.jpg', img)

# Test the API
url = 'http://localhost:8000/real_time_compare/faces'
files = {'file': open('test.jpg', 'rb')}
data = {'selfie_path': 'test'}

response = requests.post(url, files=files, data=data)
print('Status Code:', response.status_code)
print('Response:', response.json())
