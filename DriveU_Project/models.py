import cv2
import numpy as np
import requests
from DriveU_Project.images import get_image_urls


def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        return None


def calculate_image_metrics(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    laplacian_var = round(laplacian_var)

    # Calculate noise
    mean = np.mean(gray)
    stddev = np.std(gray)
    noise = stddev / mean * 100
    noise = round(noise)

    # Calculate contrast
    contrast = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 2].std()
    contrast = round(contrast)
    # Calculate saturation
    saturation = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1].std()
    saturation = round(saturation)

    # Calculate brightness
    brightness = np.mean(gray)
    brightness = round(brightness)

    return laplacian_var, noise, contrast, saturation, brightness


def is_photo_clear(laplacian_var, noise, contrast, saturation, brightness):
    # Define thresholds for clarity assessment
    laplacian_var_threshold = list(range(20, 17000))  # Provided value
    noise_threshold = list(range(20, 140))
    contrast_threshold = list(range(25, 100))
    saturation_threshold = list(range(8, 110))  # Provided value
    brightness_threshold = list(range(30, 200))

    # Check if the image meets the clarity criteria
    if (laplacian_var in laplacian_var_threshold and
            noise in noise_threshold and
            contrast in contrast_threshold and
            saturation in saturation_threshold and
            brightness in brightness_threshold):
        return True
    else:
        return False


def process_images(image_urls):
    newlist = []

    for idx, image_url in enumerate(image_urls):
        print(f"Processing Image {idx + 1}: {image_url}")
        image = load_image_from_url(image_url)

        print(image)
        if image is not None:
            laplacian_var, noise, contrast, saturation, brightness = calculate_image_metrics(
                image)

            print(f"Laplacian Variance: {laplacian_var}")
            print(f"Noise: {noise}")
            print(f"Contrast: {contrast}")
            print(f"Saturation: {saturation}")
            print(f"Brightness: {brightness}")

            # Check if the image is clear
            is_clear = is_photo_clear(laplacian_var, noise, contrast, saturation, brightness)
            print("Is the image clear?", is_clear)
            obj = {
                "url": image_url,
                "is_clear": is_clear,
                "laplacian_variance": round(laplacian_var),
                "noise": round(noise),
                "contrast": round(contrast),
                "saturation": round(saturation),
                "brightness": round(brightness)
            }
            newlist.append(obj)
        else:
            print(f"Failed to load the image from URL: {image_url}")
        print()

    return newlist


image_urls = get_image_urls()
process_images(image_urls)
