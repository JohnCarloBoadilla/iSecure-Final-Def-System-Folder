import cv2
import numpy as np
import os

def convert_to_png(image_path):
    if not image_path.lower().endswith('.png'):
        img = cv2.imread(image_path)
        if img is not None:
            png_path = os.path.splitext(image_path)[0] + '.png'
            cv2.imwrite(png_path, img)
            print(f"Converted {image_path} to {png_path}")
            return png_path
        else:
            raise FileNotFoundError(f"Image not found: {image_path}")
    else:
        return image_path

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def preprocess_image(image_path, output_path="preprocessed.png", do_deskew=True):
    # Convert to PNG if not already PNG
    image_path = convert_to_png(image_path)

    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Disable deskew to prevent unwanted rotations for landscape images
    # if do_deskew:
    #     img = deskew(img)

    # Ensure the image is in landscape orientation
    if img.shape[1] < img.shape[0]:  # width < height, portrait
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 3)

    # Resize to fixed size to ensure consistent ROI coordinates
    resized = cv2.resize(denoised, (1988, 1262))

    cv2.imwrite(output_path, resized)
    print(f"Preprocessed image saved to {output_path} ({resized.shape[1]}x{resized.shape[0]} px)")

    return resized

if __name__ == "__main__":
    test_img = "sample_id .png"
    preprocess_image(test_img)