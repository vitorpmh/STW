import cv2 as cv
from tqdm import tqdm
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '.'))
from main.utils import mediapipe_vitor as mpv


output_path = os.path.join('data/images/all_cropped_skin_only_images')
os.makedirs(output_path, exist_ok=True)
for i in range(1,11):
    os.makedirs(os.path.join(output_path, f"{i}"), exist_ok=True)
input_path = 'data/OpenData/'
log = open('data/images/log_skin_only.txt','w')

paths = []
def process_image(path, label, new_token):
    path_2_save = (output_path 
                   + f'/{label}/' 
                   + new_token 
                   + '_' 
                   + path.split('/')[-1])
    
    # if the path exists with png or other just rewrite it into jpg
    if os.path.exists(path_2_save) and not path_2_save.lower().endswith('.jpg'):
        cv.imwrite(p := path_2_save.rsplit('.', 1)[0] + '.jpg', cv.imread(path_2_save))
        os.remove(path_2_save) 
        paths.append(p)
        return
    # replace extension with jpg
    path_2_save = path_2_save.rsplit('.', 1)[0] + '.jpg'
    paths.append(path_2_save)
    if not os.path.exists(path_2_save):

        
        try:
            img = cv.imread(path)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = mpv.show_or_remove_roi(
                img, [mpv.FACE], [mpv.R_EYE, mpv.L_EYE, mpv.MOUTH], crop=True)

            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            cv.imwrite(path_2_save, img)
            log.write(f"Processed: {path}\n")
        except:
            log.write(f"Failed to process: {path}\n")
            pass
    else:
        log.write(f"Already processed: {path}\n")


def copy_image(df):
    for path, label, new_token in tqdm(df[['paths','class','new_tokens']].values):
        log.write(f"Processing: {path}\n")
        path = os.path.join(input_path, path)
        process_image(path, label, new_token)


if __name__ == "__main__":
    anotations = pd.read_csv(
        'data/splits/updated_annotations.csv',
        dtype = {
            'tokens': str,
            'new_tokens': str
        })
    

    copy_image(anotations)
    anotations_face_only = anotations.copy(deep=True)
    anotations_face_only.insert(1,'paths_face_only',paths)
    anotations_face_only.to_csv('data/splits/anotations_face_only.csv',index=False)

