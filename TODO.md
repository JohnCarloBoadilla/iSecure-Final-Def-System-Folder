# FastAPI to Flask Conversion Plan

## Objective
Convert the existing FastAPI application (`app/main.py`) to a Flask application, maintaining equivalent functionality.

## Steps

1.  **Analyze `app/main.py` for FastAPI constructs:**
    *   Identify all `fastapi` imports, `FastAPI` instance creation, route decorators (`@app.get`, `@app.post`), `HTTPException`, `StreamingResponse`, `CORSMiddleware`, `UploadFile`, `File`, and `Depends`.
    *   Note the usage of `async`/`await` and `asyncio.get_event_loop().run_in_executor` for background tasks.

2.  **Replace FastAPI with Flask:**
    *   Change `from fastapi import ...` to `from flask import Flask, request, jsonify, Response, stream_with_context, abort`.
    *   Initialize `app = Flask(__name__)`.

3.  **Convert Route Decorators:**
    *   Replace `@app.get("/path")` with `@app.route("/path", methods=["GET"])`.
    *   Replace `@app.post("/path")` with `@app.route("/path", methods=["POST"])`.

4.  **Handle Request Data:**
    *   For `UploadFile` and `File(...)`: Use `request.files['file']` to access uploaded files. Read content with `.read()`.
    *   For path parameters: Flask automatically handles these in the route function arguments.
    *   For query parameters: Use `request.args.get('param_name')`.
    *   For JSON body: Use `request.get_json()`.

5.  **Implement CORS:**
    *   Install `flask-cors`: `pip install flask-cors`.
    *   Import `CORS` from `flask_cors`.
    *   Initialize `CORS(app, resources={r"/*": {"origins": "*"}})`.

6.  **Adapt Error Handling:**
    *   Replace `HTTPException(status_code, detail)` with `abort(status_code)` and return `jsonify({"detail": message})` or a custom error handler.

7.  **Convert Streaming Response:**
    *   Replace `StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')` with Flask's `Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')`.
    *   Ensure the `generate` function yields byte strings.

8.  **Manage Background Tasks:**
    *   Remove `ThreadPoolExecutor` and `asyncio.get_event_loop().run_in_executor`. Flask is synchronous. For CPU-bound tasks, consider using `threading.Thread` or `multiprocessing.Process` if truly necessary, but for simple file reads/writes, direct calls are usually sufficient.

9.  **Update `app.on_event("shutdown")`:**
    *   Replace with Flask's `app.teardown_appcontext` or `app.before_first_request` if camera initialization needs to be moved. For shutdown, a simple `atexit` registration might be suitable if the camera object is globally accessible.

10. **Review `app/utils/security.py`:**
    *   The `verify_token` function uses `Depends(security)`. This will need to be refactored to a custom decorator or manual token extraction from `request.headers`.
    *   `HTTPBearer` and `HTTPAuthorizationCredentials` are FastAPI-specific and will be removed.

11. **Testing:**
    *   Run the Flask application.
    *   Test all endpoints (`/`, `/recognize/vehicle`, `/ocr/id`, `/camera/frame`, `/camera/single_frame`, `/camera/recognize_vehicle`, `/camera/source`, `/authenticate/face`, `/register/face`) to ensure they function correctly.
    *   Verify file uploads, streaming, and error handling.