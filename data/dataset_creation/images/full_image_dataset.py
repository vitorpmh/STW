import ctypes
import pandas as pd
import os
import cv2 as cv
import mediapipe as mp
from PIL import Image
from tqdm import tqdm

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Function to crop faces from a single image and save them
def crop_faces_single_image(input_image_path, output_folder, image_new_token, expansion, standard_size, return_img=False, face_detection=None):
    """
    Crop faces from a single image and save them
    :param input_image_path: Path to the input image
    :param output_folder: Path to the output folder
    :param image_new_token: New token for the image
    :param expansion: Expansion factor for the bounding box
    :param standard_size: Standard size for the cropped face
    :param return_img: If True, returns the cropped face as an BGR image 
    :param face_detection: MediaPipe Face Detection object

    """
    # Read the image
    image = cv.imread(input_image_path)
    if image is None:
        return
    # Convert image to RGB
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)
    # Check if faces are detected
    if results.detections:
        for i, detection in enumerate(results.detections):
            
            # Save the cropped face
            if not return_img:
                face_filename = f"{os.path.splitext(os.path.basename(input_image_path))[0]}_face_{i+1}.jpg"
                face_filepath = os.path.join(output_folder, image_new_token + face_filename)
                if os.path.exists(face_filepath):
                    continue
            # Get bounding box
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            # Extend the square defined by x,y,w,h to a bigger square but only in the topwise direction
            if w>h:
                factor = int(w*expansion)
                y_start = max(0, (y - (w-h) - factor))
                y_end = y+h
                x_start = max(0,int(x - factor/2))
                x_end = int(x+w + factor/2)
                cropped_face = image[y_start:y_end, x_start:x_end]
            else:
                factor = int(h*expansion)
                y_start = max(0,int(y - factor))
                y_end = y+h
                x_start = max(0, int(x - (h-w)/2 - factor/2))
                x_end = max(0, int(x + w + (h-w)/2 + factor/2))
                cropped_face = image[y_start:y_end, x_start:x_end]



            if cropped_face.shape[0] != cropped_face.shape[1]:
                height, width, _ = cropped_face.shape
    
                square_size = max(height, width)
                
                pad_top = (square_size - height) // 2
                pad_bottom = square_size - height - pad_top
                pad_left = (square_size - width) // 2
                pad_right = square_size - width - pad_left
                
                cropped_face = cv.copyMakeBorder(
                    cropped_face,
                    pad_top, pad_bottom, pad_left, pad_right,
                    borderType=cv.BORDER_REFLECT
                )
            else:
                pass
            
            cropped_face = cv.resize(cropped_face, (standard_size, standard_size))
            if return_img:
                return cropped_face
            else:
                cv.imwrite(face_filepath, cropped_face)
    else:
        pass
    return

########################3
# This is a single run for all the images
########################3

df = pd.read_csv('data/splits/updated_annotations.csv')
input_folder = 'data/OpenData'
output_folder = 'data/images/all_cropped_images_by_class'
log = open('data/images/log_full_image.txt','w')
os.makedirs(output_folder, exist_ok=True)
for i in range(1,11):
    os.makedirs(output_folder + f"/{i}", exist_ok=True)
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    for i in tqdm(range(len(df)), desc="Processing images", unit="image", ncols=100,total=len(df)):
        sample = df.iloc[i]
        input_image_path = os.path.join(input_folder, sample.paths)
        # check if input exists otherwise pass
        if os.path.exists(input_image_path):
            image_new_token = sample.new_tokens
            
            # check if output image already exists
            output_image_path = os.path.join(output_folder,str(sample['class']))
            if not os.path.exists(os.path.join(output_image_path, image_new_token + os.path.basename(input_image_path))):  
                try:
                    crop_faces_single_image(
                        input_image_path, 
                        os.path.join(output_folder,str(sample['class'])),
                        image_new_token,
                        expansion=0.33,
                        standard_size=300,
                        face_detection=face_detection
                    )
                    log.write(f"Processed: {input_image_path}\n")
                except Exception as e:
                    log.write(f"Failed to process: {input_image_path}\n")
                    log.write(f"Error: {e}\n")
            else:
                log.write(f"Already processed: {input_image_path}\n")
        else:
            log.write(f"File not found: {input_image_path}\n")
            