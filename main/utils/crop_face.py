import os
import cv2 as cv
import mediapipe as mp




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
        # print(f"Failed to read image: {input_image_path}")
        # log.write(f"Failed to read image: {input_image_path}\n") 
        return
    # Convert image to RGB
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)
    # Check if faces are detected
    if results.detections:
        for i, detection in enumerate(results.detections):
            # if i> 0: log.write(f"More than one face detected in: {input_image_path}\n")
            
            # Save the cropped face
            if return_img == None:
                face_filename = f"{os.path.splitext(os.path.basename(input_image_path))[0]}_face_{i+1}.jpg"
                face_filepath = os.path.join(output_folder, image_new_token + face_filename)
                if os.path.exists(face_filepath):
                    # log.write(f"Face {i+1} already exists: {face_filepath}\n")
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
                # print('w>h',y_end-y_start,x_end-x_start)
            else:
                factor = int(h*expansion)
                y_start = max(0,int(y - factor))
                y_end = y+h
                x_start = max(0, int(x - (h-w)/2 - factor/2))
                x_end = max(0, int(x + w + (h-w)/2 + factor/2))
                cropped_face = image[y_start:y_end, x_start:x_end]
                # print('w<h',y_end-y_start,x_end-x_start)



            if cropped_face.shape[0] != cropped_face.shape[1]:
                # print('not equal sides',cropped_face.shape)
                # log.write(f"Cropped face sides are not equal. Cropped face shape: {cropped_face.shape}\n")
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
                # print('now sides are equal',cropped_face.shape)
                # log.write(f"Face {i+1} - Cropped now are equal. Cropped face shape: {cropped_face.shape}\n")
            else:
                pass
                # log.write(f"Face {i+1} - Sides are equal. Cropped face shape: {cropped_face.shape}\n")
                # print('sides are equal',cropped_face.shape)
            
            # resize to standard size
            cropped_face = cv.resize(cropped_face, (standard_size, standard_size))
            # print('after resize',cropped_face.shape)
            if return_img:
                return cropped_face
            else:
                cv.imwrite(face_filepath, cropped_face)
            # log.write(f"Saved cropped Face {i+1}: {face_filepath}\n")
    else:
        # log.write(f"No face detected in: {input_image_path}\n")
        # print(f"No face detected in: {input_image_path}")
        pass
    return