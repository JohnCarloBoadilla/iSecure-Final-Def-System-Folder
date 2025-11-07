# Live Vehicle Plate Recognition and Comparison Plan

## Objective
Implement a live vehicle recognition system that allows personnel to verify a vehicle's license plate against the information provided in a visitation request.

## High-Level Workflow

1.  A visitor submits a visitation request, including their vehicle's license plate number.
2.  When the vehicle arrives, a security person opens a verification interface.
3.  This interface shows the expected license plate number.
4.  The personnel points a camera at the vehicle's license plate.
5.  The system performs live OCR on the camera feed, recognizes the plate, and compares it to the expected plate number.
6.  The system displays a clear "Match" or "No Match" status to the personnel.

## TODO Items

### Backend (Flask App)

1.  **Create a New Endpoint (`/camera/recognize_and_compare_plate`):**
    *   This endpoint will not take an image upload. Instead, it will trigger the camera to capture a single frame.
    *   It should accept the `expected_plate_number` as a parameter (e.g., in a POST request body).
    *   It will call the `detect_vehicle_plate` function using the captured frame's bytes.
    *   It will compare the recognized plate number with the `expected_plate_number`.
    *   It will return a JSON response, e.g., `{"match": true, "recognized_plate": "ABC1234"}` or `{"match": false, "recognized_plate": "XYZ7890"}`.

2.  **Refine `detect_vehicle_plate` Function:**
    *   Ensure the function in `license_plate_ocr_scanner.py` is robust and handles cases where no plate is found gracefully (returns `None`).
    *   Make sure the Mindee API key is loaded from a secure configuration, not hardcoded.

### Frontend (PHP/JavaScript)

1.  **Identify the Verification Page:**
    *   Locate the PHP page where personnel view the details of an expected visitor or vehicle (e.g., a "pendings" or "visitor details" page).

2.  **Add "Verify Vehicle" Button:**
    *   On this page, next to the displayed license plate number, add a "Verify Vehicle" button.

3.  **Create Camera Verification Modal:**
    *   Clicking the button will open a modal window.
    *   The modal will display the live camera feed (using the `/camera/frame` endpoint).
    *   The modal will have a "Scan Plate" or "Verify Now" button.

4.  **Implement JavaScript Logic:**
    *   When the "Verify Now" button is clicked:
        *   The script will get the `expected_plate_number` from the main page.
        *   It will make a POST request to the new `/camera/recognize_and_compare_plate` endpoint, sending the `expected_plate_number`.
        *   It will handle the JSON response from the backend.
        *   It will display a clear success ("✅ Match") or failure ("❌ No Match: Found XYZ7890") message to the user within the modal or on the main page.
        *   It should also handle potential errors (e.g., API failure, no plate detected).