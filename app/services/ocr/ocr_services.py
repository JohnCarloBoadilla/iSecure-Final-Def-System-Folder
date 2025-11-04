import cv2
import numpy as np
import pytesseract
import os
import tempfile
from .preprocess import preprocess_image
from .address_corrections import address_corrections
import difflib

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load Philippine locations from separate files if they exist
def load_locations(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(line.strip().upper() for line in f if line.strip())
    except FileNotFoundError:
        return set()

provinces = load_locations('province.txt')
municipalities = load_locations('municipality.txt')
barangays = load_locations('barangay.txt')
philippine_locations = barangays | municipalities | provinces

def autocorrect_text(text, word_list):
    words = text.upper().split()
    corrected_words = []
    for word in words:
        if word.isalpha():
            matches = difflib.get_close_matches(word, word_list, n=1, cutoff=0.5)
            if matches:
                corrected_words.append(matches[0])
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)

def extract_id_info(image_bytes):
    try:
        # Save image bytes to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_path = temp_file.name

        try:
            # Preprocess the image
            preprocessed = preprocess_image(temp_path)

            # Define ROIs for ID fields
            fields = {
                "ID Number": (80, 320, 750, 120),
                "Last Name": (885, 465, 590, 100),
                "Given Name": (890, 630, 650, 80),
                "Middle Name": (890, 830, 590, 85),
                "Date of Birth": (890, 960, 700, 100),
                "Address": (90, 1080, 1330, 150)
            }

            # Function to run OCR on a ROI
            def ocr_read(roi, psm=6):
                try:
                    if len(roi.shape) == 3:
                        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    else:
                        gray = roi
                    config = f'--psm {psm}'
                    text = pytesseract.image_to_string(gray, lang="eng", config=config).strip()
                    return text
                except Exception as e:
                    print(f"OCR error: {e}")
                    return ""

            # Extract text from each field
            extracted = {}
            for field, (x, y, w, h) in fields.items():
                try:
                    roi = preprocessed[y:y+h, x:x+w]
                    if roi.size == 0:
                        text = ""
                    else:
                        if field == "ID Number" or field in ["Last Name", "Given Name", "Middle Name"]:
                            psm = 8
                        elif field == "Address":
                            psm = 6
                        else:
                            psm = 7
                        text = ocr_read(roi, psm=psm)
                        if field == "Last Name":
                            text = ''.join(c for c in text if c.isalpha() or c.isspace()).strip()
                except Exception as e:
                    print(f"Error extracting {field}: {e}")
                    text = ""
                extracted[field] = text

            # Process Address
            if "Address" in extracted:
                try:
                    address_text = extracted["Address"].upper()
                    for old, new in address_corrections.items():
                        address_text = address_text.replace(old, new)
                    cleaned = ''.join(c if c.isalnum() or c.isspace() or c == ',' else ' ' for c in address_text.upper())
                    parts = [p.strip() for p in cleaned.split(',') if p.strip()]
                    if len(parts) >= 2:
                        house_street = parts[0]
                        location = ' '.join(parts[1:])
                        location_words = location.split()
                        if len(location_words) >= 3:
                            province = location_words[-1]
                            municipality = location_words[-2]
                            barangay = ' '.join(location_words[:-2])
                            barangay = autocorrect_text(barangay, barangays)
                            municipality = autocorrect_text(municipality, municipalities)
                            province = autocorrect_text(province, provinces)
                            extracted["Address"] = f"{house_street}, {barangay}, {municipality}, {province}"
                        else:
                            extracted["Address"] = autocorrect_text(cleaned, philippine_locations)
                    else:
                        extracted["Address"] = autocorrect_text(cleaned, philippine_locations)
                except Exception as e:
                    print(f"Error processing address: {e}")

            # Autocorrect Date of Birth
            if "Date of Birth" in extracted:
                try:
                    dob_text = extracted["Date of Birth"]
                    dob_words = dob_text.upper().split()
                    corrected_dob_words = []
                    months = {"JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"}
                    for word in dob_words:
                        if word.isalpha():
                            if word in months:
                                corrected_dob_words.append(word)
                            else:
                                matches = difflib.get_close_matches(word, months, n=1, cutoff=0.6)
                                if matches:
                                    corrected_dob_words.append(matches[0])
                                else:
                                    corrected_dob_words.append(word)
                        else:
                            corrected_dob_words.append(word)
                    extracted["Date of Birth"] = ' '.join(corrected_dob_words)
                except Exception as e:
                    print(f"Error processing DOB: {e}")

            return extracted
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
    except Exception as e:
        print(f"Error in extract_id_info: {e}")
        return {}
