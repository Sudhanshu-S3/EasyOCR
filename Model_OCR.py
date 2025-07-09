import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from PIL import Image
plt.style.use('ggplot')

# Load CSV
csv_file = 'test.csv'
df = pd.read_csv(csv_file)

# Prepare image file names
img_fns = []
for j in range(135000):
    img_fns.append(f'Resource\\downloaded_images\\image_{j}.jpg')

# Create a 7x7 grid of subplots
fig, axs = plt.subplots(5, 5, figsize=(1000, 1000))
axs = axs.flatten()

# Limit the number of images to the number of subplots (max 49)
num_images_to_show = min(len(img_fns), len(axs))

# Iterate over the images and plot them
for id, i in enumerate(tqdm(img_fns[:num_images_to_show])):
    # Ensure correct path splitting using os.path
    image_id = os.path.basename(i).split('.')[0].split('_')[-1]
    
    # Read and display the image
    axs[id].imshow(plt.imread(i))
    axs[id].axis('off')
    
    # Check for annotations in the CSV file
    n_annot = len(df.query('index == @image_id'))
    axs[id].set_title(f'{image_id} (Annotations: {n_annot})')

# Turn off axes for any unused subplots
for id in range(num_images_to_show, len(axs)):
    axs[id].axis('off')

# Show the plot if needed (commented out if not used)
# plt.show()

# OCR Reading using easyocr
reader = easyocr.Reader(['en'])

results = []
for img in tqdm(img_fns[:num_images_to_show]):  # Limit to the number of images shown
    result = reader.readtext(img)
    
    # Extract the image ID
    img_id = os.path.basename(img).split('.')[0].split('_')[-1]
    
    # Concatenate detected text
    concatenated_text = ' '.join([res[1] for res in result])
    
    # Add results to the list
    results.append({'img_id': img_id, 'text': concatenated_text})

# Save the OCR results to CSV
img_df = pd.DataFrame(results)
img_df.to_csv('text_new.csv', index=False)
