from mindee import ClientV2, InferenceParameters, PathInput
from app.config import MINDEE_API_KEY

def detect_vehicle_plate(image_bytes: bytes) -> str:
    """
    Detects a vehicle license plate from an image using the Mindee API.
    
    Args:
        image_bytes: The byte content of the image file.
        
    Returns:
        The license plate number as a string, or None if not found.
    """
    try:
        mindee_client = ClientV2(api_key=MINDEE_API_KEY)
        
        # Create a PathInput from the image bytes
        input_doc = PathInput(raw_bytes=image_bytes, filename="plate.jpg")
        
        # Parse the document
        result = mindee_client.parse(
            endpoint_name="license_plate",
            input_doc=input_doc
        )
        
        # Extract the license plate number
        if result.document and result.document.inference.prediction.license_plates:
            plate = result.document.inference.prediction.license_plates[0].value
            return plate
        return None
    except Exception as e:
        print(f"Error during Mindee OCR: {e}")
        return None
