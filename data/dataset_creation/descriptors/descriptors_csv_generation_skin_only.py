import os
import pandas as pd
import numpy as np
import cv2 as cv
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from descriptors import *

main_path = "/store/vitorpmatias/TESE/TESE/"

# Load dataset
annotated_data_face_only = pd.read_csv(
    os.path.join(main_path, "dissertation/dataset/anotations_face_only.csv")
)

# Read images and classes
images_path_cls = annotated_data_face_only[['paths_face_only', 'class']].values


for bins in [8, 16, 32, 64, 128]:

    # Sample an image to get column names
    sample_img_path = images_path_cls[0, 0]
    sample_img = cv.imread(sample_img_path)
    sample_features, _ = descriptors_generator(sample_img,bins=bins)
    columns_names = list(sample_features.keys()) + ['class', 'paths']

    # Worker function for multiprocessing
    def process_image(data):
        img_path, cls = data
        input_img = cv.imread(img_path)
        if input_img is None:
            return None  # Skip if the image is not loaded

        features_dict, _ = descriptors_generator(input_img,bins)
        features_dict['paths'] = img_path
        features_dict['class'] = cls
        return features_dict

    # Process images in parallel
    with ProcessPoolExecutor(max_workers=20) as executor:
        results = list(
            tqdm(
                executor.map(process_image, 
                             images_path_cls), 
                             total=len(images_path_cls)))

    # Filter out any None values (failed image loads)
    results = [res for res in results if res is not None]

    # Convert to DataFrame
    descriptors_df = pd.DataFrame(results, columns=columns_names)

    # Save CSV
    output_path = os.path.join(main_path, 
        f"dissertation/CCVmodel/descriptors/descriptors_skin_only_{bins}.csv")
    descriptors_df.to_csv(output_path, index=False)

    print(f"CSV saved to {output_path}")
