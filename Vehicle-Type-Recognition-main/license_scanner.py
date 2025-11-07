from mindee import ClientV2, InferenceParameters, PathInput
import json
import os
import glob

# Find the first image file in the folder
folder_path = "ID' Data for ocr/"
image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png"))

if not image_files:
    print("No image files found in the folder.")
    exit(1)

# Use the first image file found
input_path = image_files[0]

# API credentials
api_key = "md_wSasrvkkiuFg06GG7bY1X8TI0PxHAEZD"
model_id = "f538247d-0f42-4491-bd0c-3fdd2898ad5f"

# Init a new client
mindee_client = ClientV2(api_key)

# Set inference parameters
params = InferenceParameters(
    # ID of the model, required.
    model_id=model_id,

    # Options: set to `True` or `False` to override defaults

    # Enhance extraction accuracy with Retrieval-Augmented Generation.
    rag=None,
    # Extract the full text content from the document as strings.
    raw_text=None,
    # Calculate bounding box polygons for all fields.
    polygon=None,
    # Boost the precision and accuracy of all extractions.
    # Calculate confidence scores for all fields.
    confidence=None,
)

# Load a file from disk
input_source = PathInput(input_path)

# Send for processing using polling
response = mindee_client.enqueue_and_get_inference(
    input_source, params
)

# Access the result fields
fields: dict = response.inference.result.fields

# Print only the license plate number and vehicle type
print(f":license_plate_number: {fields['license_plate_number'].value}")
print(f":vehicle_type: {fields['vehicle_type'].value}")

# Convert fields to a serializable dictionary
serializable_fields = {}
for key, field in fields.items():
    serializable_fields[key] = {
        'value': field.value,
        'confidence': field.confidence if hasattr(field, 'confidence') else None,
        'polygon': field.polygon if hasattr(field, 'polygon') else None,
        'raw_text': field.raw_text if hasattr(field, 'raw_text') else None
    }

# Save the extracted fields to a JSON file in "License Plate Data/" directory
output_dir = "License Plate Data/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, "scanned_license.json")
with open(output_file, 'w') as f:
    json.dump(serializable_fields, f, indent=4)

print(f"Extracted fields saved to {output_file}")
