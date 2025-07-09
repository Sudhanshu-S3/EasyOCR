import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image


def remove_side_white_padding_cv2(image_path, output_path=None, border_color=(255, 255, 255)):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_value = 240 if border_color == (255, 255, 255) else np.mean(border_color)
    _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)
    row_sum = np.sum(thresh, axis=1)
    col_sum = np.sum(thresh, axis=0)
    top, bottom = np.where(row_sum > 0)[0][[0, -1]]
    left, right = np.where(col_sum > 0)[0][[0, -1]]
    cropped_image = image[top:bottom+1, left:right+1]
    if output_path:
        cv2.imwrite(output_path, cropped_image)
    return cropped_image


def denoise_image(image):

    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    return denoised_image


def upscale_image_pillow(image, scale_factor=1.25):
    # Convert OpenCV image (BGR) to PIL image (RGB)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Calculate new dimensions
    width, height = pil_image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Resize the image using LANCZOS resampling
    upscaled_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    
    # Convert back to OpenCV image (BGR)
    return cv2.cvtColor(np.array(upscaled_image), cv2.COLOR_RGB2BGR)


output_folder = 'processed_img'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

img_fns=[]
for j in range(1000):
    img_fns.append('Resource\\1000_images\\image_'+str(j)+'.jpg')

# Process each image
for img_path in img_fns:
    try:
        # 1. Load Image
        image = cv2.imread(img_path)
        if image is None:
            print(f"Error: Could not load image at: {img_path}")
            continue

        cropped_image = remove_side_white_padding_cv2(img_path)

        #  Denoise Image
        denoised_image = denoise_image(image)

        # Upscale image
        upscale_image = upscale_image_pillow(image)

        #  Save to Output Folder
        image_name = os.path.basename(img_path)
        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, upscale_image)

        print(f"Processed: {image_name}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

