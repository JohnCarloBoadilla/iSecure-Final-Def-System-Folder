import cv2
import pytesseract
import os
import difflib
from address_corrections import address_corrections
import preprocess

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load Philippine locations from separate files
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

# Preprocess the image
image = preprocess.preprocess_image('sample_id.png')

# Load raw image for comparison
raw_image_path = 'sample_id.png'  # Adjust if needed
raw_image = cv2.imread(raw_image_path)
if raw_image is None:
    raise FileNotFoundError(f"Raw image not found at {raw_image_path}")

# Flag to enable raw image fallback
use_raw_fallback = False

# Define ROIs for ID fields
fields = {
    "ID Number": (80, 320, 750, 120),
    "Last Name": (885, 465, 590, 100),
    "Given Name": (890, 630, 650, 80),
    "Middle Name": (890, 830, 590, 85),
    "Date of Birth": (890, 960, 700, 100),
    "Address": (90, 1080, 1330, 150)
}

# Draw ROIs on the image for visualization
image_with_rois = image.copy()
for field, (x, y, w, h) in fields.items():
    cv2.rectangle(image_with_rois, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image_with_rois, field, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Save the image with ROIs
cv2.imwrite('preprocessed_with_rois.png', image_with_rois)
print("Image with ROIs saved as 'preprocessed_with_rois.png'")

# Function to run OCR on a ROI
def ocr_read(roi, psm=6):
    # Convert to grayscale if needed
    if len(roi.shape) == 3:
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    else:
        gray = roi

    # Run Tesseract OCR with config for better text extraction
    config = f'--psm {psm}'
    text = pytesseract.image_to_string(gray, lang="eng", config=config).strip()
    return text

# Function to choose the better text between preprocessed and raw OCR results
def choose_better_text(text1, text2, field):
    # Heuristic: choose the one with more alphanumeric characters
    alnum1 = sum(c.isalnum() for c in text1)
    alnum2 = sum(c.isalnum() for c in text2)
    if alnum1 > alnum2:
        return text1
    elif alnum2 > alnum1:
        return text2
    else:
        return text1  # default to preprocessed

# Clear old debug ROIs
for file in os.listdir("debug_rois"):
    if file.endswith("_gray.png"):
        os.remove(os.path.join("debug_rois", file))

# Extract text from each field
extracted = {}
for field, (x, y, w, h) in fields.items():
    roi = image[y:y+h, x:x+w]
    print(f"Processing field: {field}, ROI shape: {roi.shape}")
    # Save debug ROI
    if len(roi.shape) == 3:
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    else:
        gray_roi = roi
    cv2.imwrite(f"debug_rois/{field.replace(' ', '_')}_gray.png", gray_roi)
    # Use PSM 8 for ID Number and names (single word), PSM 7 for other single-line fields, PSM 6 for multi-line address
    if field == "ID Number" or field in ["Last Name", "Given Name", "Middle Name"]:
        psm = 8
    elif field == "Address":
        psm = 6
    else:
        psm = 7
    text = ocr_read(roi, psm=psm)
    if use_raw_fallback:
        raw_roi = raw_image[y:y+h, x:x+w]
        raw_text = ocr_read(raw_roi, psm=psm)
        text = choose_better_text(text, raw_text, field)
    # Remove non-alphabetic characters from last name field except spaces
    if field == "Last Name":
        text = ''.join(c for c in text if c.isalpha() or c.isspace()).strip()
    extracted[field] = text

# Split Address into components and autocorrect subdivision, city, province
if "Address" in extracted:
    address_text = extracted["Address"].upper()

    # Apply corrections from the imported dict
    for old, new in address_corrections.items():
        address_text = address_text.replace(old, new)

    # Clean the address: remove non-alnum except space and comma
    cleaned = ''.join(c if c.isalnum() or c.isspace() or c == ',' else ' ' for c in address_text.upper())
    # Split by comma
    parts = [p.strip() for p in cleaned.split(',') if p.strip()]
    if len(parts) >= 2:
        house_street = parts[0]
        location = ' '.join(parts[1:])
        location_words = location.split()
        if len(location_words) >= 3:
            # Assume province is last, municipality is second last, barangay is the rest
            province = location_words[-1]
            municipality = location_words[-2]
            barangay = ' '.join(location_words[:-2])
            # Autocorrect using separate dictionaries
            barangay = autocorrect_text(barangay, barangays)
            municipality = autocorrect_text(municipality, municipalities)
            province = autocorrect_text(province, provinces)
            extracted["Address"] = f"{house_street}, {barangay}, {municipality}, {province}"
        else:
            extracted["Address"] = autocorrect_text(cleaned, philippine_locations)
    else:
        extracted["Address"] = autocorrect_text(cleaned, philippine_locations)

# Autocorrect Date of Birth
if "Date of Birth" in extracted:
    dob_text = extracted["Date of Birth"]
    # Clean and autocorrect words in DOB
    dob_words = dob_text.upper().split()
    corrected_dob_words = []
    months = {"JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"}
    for word in dob_words:
        if word.isalpha():
            if word in months:
                corrected_dob_words.append(word)
            else:
                # Try autocorrect with months list
                matches = difflib.get_close_matches(word, months, n=1, cutoff=0.6)
                if matches:
                    corrected_dob_words.append(matches[0])
                else:
                    corrected_dob_words.append(word)
        else:
            corrected_dob_words.append(word)
    extracted["Date of Birth"] = ' '.join(corrected_dob_words)

# Show results
print("\n=== Extracted ID Fields ===")
for field, text in extracted.items():
    print(f"{field}: {text}")
