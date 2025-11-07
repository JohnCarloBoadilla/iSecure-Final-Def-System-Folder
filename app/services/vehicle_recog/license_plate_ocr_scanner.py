import argparse
import json
import os
import re
import time
from mindee import ClientV2, InferenceParameters, PathInput
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("watchdog library is required for automatic scanning. Install it with: pip install watchdog")
    exit(1)

class ImageHandler(FileSystemEventHandler):
    def __init__(self, api_key, model_id, plate_type, output_folder):
        self.api_key = api_key
        self.model_id = model_id
        self.plate_type = plate_type
        self.output_folder = output_folder
        self.image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            filename = os.path.basename(filepath)
            if filename.lower().endswith(self.image_extensions):
                print(f"New image detected: {filename}")
                # Wait a bit to ensure the file is fully written
                time.sleep(1)
                if os.path.exists(filepath):
                    try:
                        plate_number, vehicle_type = process_image(filepath, self.api_key, self.model_id, self.plate_type)
                        print_output(filename, plate_number, vehicle_type)
                        save_json(filename, plate_number, vehicle_type, self.output_folder)
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")
                        print_output(filename, None, None)
                        save_json(filename, None, None, self.output_folder)
                else:
                    print(f"File {filename} not found after waiting.")

def extract_license_plate_number(text, plate_type):
    """
    Extract license plate number using regex based on Philippine plate formats.
    Old format: 3 letters + 3 numbers (e.g., ABC123)
    New format: 3 letters + 4 numbers (e.g., ABC1234)
    """
    if plate_type == 'old':
        pattern = r'\b[A-Z]{3}\d{3}\b'
    elif plate_type == 'new':
        pattern = r'\b[A-Z]{3}\d{4}\b'
    else:
        # If not specified, try both
        pattern = r'\b[A-Z]{3}\d{3,4}\b'

    match = re.search(pattern, text.upper())
    return match.group(0) if match else None

def process_image(image_path, api_key, model_id, plate_type):
    """
    Process a single image using Mindee API and extract license plate data.
    """
    # Init a new client
    mindee_client = ClientV2(api_key)

    # Set inference parameters
    params = InferenceParameters(
        model_id=model_id,
        rag=None,
        raw_text=True,  # Extract full text
        polygon=None,
        confidence=None,
    )

    # Load a file from disk
    input_source = PathInput(image_path)

    # Send for processing using polling
    response = mindee_client.enqueue_and_get_inference(input_source, params)

    # Extract fields from raw text
    raw_text = str(response.inference)
    plate_number = None
    vehicle_type = None

    match = re.search(r':license_plate_number:\s*([^\n]+)', raw_text)
    if match:
        plate_number = match.group(1).strip()

    match = re.search(r':vehicle_type:\s*([^\n]+)', raw_text)
    if match:
        vehicle_type = match.group(1).strip()

    return plate_number, vehicle_type

def print_output(filename, plate_number, vehicle_type):
    """
    Print the output for a file.
    """
    print(f"File: {filename}")
    print(":license_plate_number:", plate_number if plate_number else "Not found")
    print(":vehicle_type:", vehicle_type if vehicle_type else "Not found")
    print("-" * 50)

def save_json(filename, plate_number, vehicle_type, output_folder):
    """
    Save the extracted data to a JSON file.
    """
    data = {
        "id_type": "philippine_license_plate",
        "license_plate_number": plate_number if plate_number else "Not found",
        "vehicle_type": vehicle_type if vehicle_type else "Not found"
    }

    base_name = os.path.splitext(filename)[0]
    json_filename = f"{base_name}.json"
    json_path = os.path.join(output_folder, json_filename)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="License Plate OCR Scanner using Mindee API")
    parser.add_argument('--folder', type=str, default="ID' Data for ocr/", help='Folder containing images to process')
    parser.add_argument('--plate_type', type=str, choices=['old', 'new'], default='new', help='Type of Philippine license plate (old: 3 letters + 3 numbers, new: 3 letters + 4 numbers)')
    parser.add_argument('--api_key', type=str, required=True, help='Mindee API key')
    parser.add_argument('--model_id', type=str, default="3fe18303-4899-4ed5-b32d-2dfb4f6f1d37", help='Mindee model ID')
    parser.add_argument('--watch', action='store_true', help='Watch the folder for new images and process them automatically')

    args = parser.parse_args()

    folder = args.folder
    plate_type = args.plate_type
    api_key = args.api_key
    model_id = args.model_id
    watch = args.watch

    output_folder = "License Plate Data/"
    os.makedirs(output_folder, exist_ok=True)

    # Supported image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    if watch:
        # Watch mode: monitor the folder for new files
        event_handler = ImageHandler(api_key, model_id, plate_type, output_folder)
        observer = Observer()
        observer.schedule(event_handler, folder, recursive=False)
        observer.start()
        print(f"Watching folder: {folder}")
        print("Press Ctrl+C to stop watching.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        # Batch mode: process existing files
        # List all image files in the folder
        image_files = [f for f in os.listdir(folder) if f.lower().endswith(image_extensions)]

        if not image_files:
            print(f"No image files found in {folder}")
            return

        for image_file in image_files:
            image_path = os.path.join(folder, image_file)
            print(f"Processing {image_file}...")

            try:
                plate_number, vehicle_type = process_image(image_path, api_key, model_id, plate_type)
                print_output(image_file, plate_number, vehicle_type)
                save_json(image_file, plate_number, vehicle_type, output_folder)
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")
                print_output(image_file, None, None)
                save_json(image_file, None, None, output_folder)

if __name__ == '__main__':
    main()
