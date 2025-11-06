# Feature Plan: Facial Authentication

## 1. Information Gathered
- **Objective:** Authenticate visitors using their registered facial data.
- **Primary Logic Source:** The `authenticate_visitor` function in `face_authenticator.py` will be adapted for this feature.
- **Camera Source:** The system must support switching between a live CCTV feed and the local webcam.
- **UI Integration:** The functionality will be located in a "Facial" tab within the `visitors.php` page.
- **Feedback Mechanism:** Upon successful or failed authentication, a notification should be displayed with the result.

## 2. Plan

### Backend (Python/FastAPI)
- **Modify `app/config.py`:** Add a mechanism to manage the active camera source (e.g., a variable to hold 'webcam' or 'cctv_url').
- **Modify `app/main.py`:**
    - Create a new endpoint, `/camera/source`, that allows the frontend to set the active camera source ('webcam' or a specific CCTV stream URL).
    - Create a new endpoint, `/authenticate/face`, that accepts an image (a frame from the video feed). This endpoint will perform the core authentication logic.
- **Create `app/services/face_recog/authentication_service.py`:**
    - Develop a new function `authenticate_face(frame)`.
    - This function will:
        1. Fetch the `selfie_photo_path` and names of all visitors currently marked as 'Inside' from the database.
        2. Use the `deepface` library to compare the face in the provided `frame` against each of the fetched selfie photos.
        3. If a match is found with a high confidence score, return the visitor's name.
        4. If no match is found, return "Unknown" or an error message.

### Frontend (PHP/JavaScript)
- **Modify `php/routes/visitors.php`:**
    - Add a new "Facial" or "Authentication" tab to the user interface.
    - Inside this tab, create the following UI elements:
        - A video player element to display the camera feed.
        - A dropdown or toggle switch to select the camera source ("Webcam" vs. "CCTV").
        - An "Authenticate" button to trigger the process.
- **Modify `scripts/visitors.js` (or create a new script):**
    - Implement JavaScript to handle the camera source selection. When changed, it should call the `/camera/source` endpoint on the backend.
    - Write a function to stream the selected camera feed to the video player. For "Webcam", use `navigator.mediaDevices.getUserMedia`. For "CCTV", use the `/camera/frame` endpoint.
    - When the "Authenticate" button is clicked, capture a frame from the video feed, send it to the `/authenticate/face` endpoint.
    - On receiving a response, use a JavaScript notification library or a simple `alert()` to display the visitor's name or "Unknown visitor".

## 3. Dependent Files to Edit
- `app/config.py`
- `app/main.py`
- `app/services/face_recog/authentication_service.py` (New file)
- `php/routes/visitors.php`
- `scripts/visitors.js`

## 4. Follow-up Steps
- **Testing:**
    - Test the camera source switching functionality.
    - Test the authentication with known and unknown faces.
    - Ensure notifications display correctly and promptly.
- **Refinement:** Adjust the confidence threshold for face matching in `authentication_service.py` to balance security and usability.
