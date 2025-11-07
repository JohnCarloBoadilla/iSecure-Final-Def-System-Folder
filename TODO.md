# FastAPI to Flask Conversion Plan

## Objective
Convert the existing FastAPI application (`app/main.py`) to a Flask application, maintaining equivalent functionality.

## Steps

1.  **Analyze `app/main.py` for FastAPI constructs:** (Completed)
    *   Identified all `fastapi` imports, `FastAPI` instance creation, route decorators (`@app.get`, `@app.post`), `HTTPException`, `StreamingResponse`, `CORSMiddleware`, `UploadFile`, `File`, and `Depends`.
    *   Noted the usage of `async`/`await` and `asyncio.get_event_loop().run_in_executor` for background tasks.

2.  **Replace FastAPI with Flask:** (Completed)
    *   Changed `from fastapi import ...` to `from flask import Flask, request, jsonify, Response, stream_with_context, abort`.
    *   Initialized `app = Flask(__name__)`.

3.  **Convert Route Decorators:** (Completed)
    *   Replaced `@app.get("/path")` with `@app.route("/path", methods=["GET"])`.
    *   Replaced `@app.post("/path")` with `@app.route("/path", methods=["POST"])`.

4.  **Handle Request Data:** (Completed)
    *   For `UploadFile` and `File(...)`: Used `request.files['file']` to access uploaded files. Read content with `.read()`.
    *   For path parameters: Flask automatically handles these in the route function arguments.
    *   For query parameters: Used `request.args.get('param_name')`.
    *   For JSON body: Used `request.get_json()`.

5.  **Implement CORS:** (Completed)
    *   Installed `flask-cors` (via `requirements.txt`).
    *   Imported `CORS` from `flask_cors`.
    *   Initialized `CORS(app, resources={r"/*": {"origins": "*"}})`.

6.  **Adapt Error Handling:** (Completed)
    *   Replaced `HTTPException(status_code, detail)` with `abort(status_code)` and `jsonify({"detail": message})`.

7.  **Convert Streaming Response:** (Completed)
    *   Replaced `StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')` with Flask's `Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')`.
    *   Ensured the `generate` function yields byte strings.

8.  **Manage Background Tasks:** (Completed)
    *   Removed `ThreadPoolExecutor` and `asyncio.get_event_loop().run_in_executor`. Direct calls are now used.

9.  **Update `app.on_event("shutdown")`:** (Completed)
    *   Removed FastAPI shutdown event handler. Camera resource management will need to be handled differently if required.

10. **Review `app/utils/security.py`:** (Completed)
    *   Refactored `verify_token` to use manual token extraction from `request.headers`.
    *   Removed `HTTPBearer` and `HTTPAuthorizationCredentials`.

11. **Testing:**
    *   Run the Flask application using: `set FLASK_APP=app/main.py` and `flask run --host=localhost --port=8000`.
    *   Test all endpoints (`/`, `/recognize/vehicle`, `/ocr/id`, `/camera/frame`, `/camera/single_frame`, `/camera/recognize_vehicle`, `/camera/source`, `/authenticate/face`, `/register/face`) to ensure they function correctly.
    *   Verify file uploads, streaming, and error handling.
    *   **Note:** The `php/routes/process_recognition.php` file was updated to call `/authenticate/face` instead of the non-existent `/recognize/face` endpoint.