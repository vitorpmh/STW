import os
import numpy as np
import cv2 as cv
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt



# aplica o detetor de landmarks.... (parecido com mediapipe2 .....)
mp_face_mesh = mp.solutions.face_mesh # type: ignore
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

L_EYE = [243, 112, 26, 22, 23, 24, 110, 25,
        130, 247, 30, 29, 27, 28, 56, 190, 243]
R_EYE = [463, 341, 256, 252, 253, 254, 339, 255,
        359, 467, 260, 259, 257, 258, 286, 414, 463]
MOUTH = [61, 185,  40,  39,  37,  0, 267, 269, 270, 409,
         291, 375, 321, 405, 314, 17,  84, 181,  91, 146, 61]
NOSE = [2,  97,  98, 129, 209, 198, 174, 122,   6,
        351, 399, 420, 429, 279, 331, 358, 327, 326, 2]
FACE = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400,
        377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109, 10]
L_EYEBROW = [55, 222, 52, 53, 46, 156, 139, 71, 63, 105, 66, 107, 55]
R_EYEBROW = [285,  442, 282, 283, 276, 353, 383, 300, 293, 334, 296, 336, 285]

FACE_WITHOUT_BEARD= [6, 122, 245, 26, 22, 23, 24, 110, 25, 226, 35, 143, 34, 127, 227, 234, 123, 205, 203, 218, 1, 438, 423, 425, 352, 454, 447, 356, 264, 372, 265, 255, 339, 254, 253, 252, 256, 465, 351, 6]
ALL_REGIONS_DICT = {
    'leye'                  : L_EYE,
    'reye'                  : R_EYE,
    'mouth'                 : MOUTH,
    'nose'                  : NOSE,
    'face'                  : FACE,
    'leyebrow'              : L_EYEBROW,
    'reyebrow'              : R_EYEBROW,
    'face_without_beard'    : FACE_WITHOUT_BEARD,
}
# def get_paths():
#     try:
#         return os.listdir('/home/vitor/Documents/MinhaVidaPessoal/Mestrado/TESE/imagens')
#     except:
#         return os.listdir('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/imagens')

# paths = get_paths()

# def get_img(index,paths):
#     try:
#         img = cv.imread('/home/vitor/Documents/MinhaVidaPessoal/Mestrado/TESE/imagens/'+paths[index])
#     except:
#         img = cv.imread('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/imagens'+paths[index])
#     img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
#     return img




"""
Função para imprimir uma região de interesse baseado nos indices dos landmarks.
"""
def show_region_of_interest(roi, info, img):
    color = (0, 255, 255)
    thickness = 1
    for i in range(len(roi)-1):
        idx_s = roi[i]
        idx_e = roi[i+1]
        start_point = (info[idx_s][3], info[idx_s][4])
        end_point   = (info[idx_e][3], info[idx_e][4])
        cv.line(img, start_point, end_point, color, thickness)
    return img


"""
Função para segmentar uma região de interesse baseado nos indices dos landmarks.
"""
# def region_of_interest_segmentation(roi, info, img):
    
#     # read image as RGB and add alpha (transparency)
#     #im = Image.open("img1-512px.jpg").convert("RGB")
    
#     # convert to numpy (for convenience)
#     imArray = np.asarray(img)
    
#     polygon = []
#     for i in range(len(roi)):
#         idx_s = roi[i]
#         start_point = (info[idx_s][3], info[idx_s][4])
#         polygon.append(start_point)
    
#     # create mask
#     maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
#     ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
#     mask = np.array(maskIm)

#     # assemble new image (uint8: 0-255)
#     newImArray = np.empty(imArray.shape,dtype='uint8')
    
#     # segmentation
#     newImArray[:,:,0] = np.multiply(imArray[:,:,0], mask)
#     newImArray[:,:,1] = np.multiply(imArray[:,:,1], mask)
#     newImArray[:,:,2] = np.multiply(imArray[:,:,2], mask)

#     return newImArray, mask



#Definindo regiões de interesse
forehead_contour = [10,338,297,332,298,293,334,296,336,9,107,66,105,63,68,103,67,109,10]
chin_contour = [18,313,406,335,273,432,434,364,394,395,369,396,175,171,140,170,169,135,214,212,43,106,182,83,18]
left_cheek_contour = [116,117,118,119,100,142,203,206,216,192,213,147,123,116]
right_cheek_contour = [345,346,347,348,329,371,423,426,436,416,433,376,352,345]

"""
Esta função é responsável pela segmentação ROIs na imagem RGB estática.
"""
# Obs.: Função MediaPipe8() da versão original do Sherlon
def show_roi_segmentation(image_name):
    # le e reduz imagem....
    img = cv.imread(image_name)
    #img = cv.resize(img, None, fx=2/5, fy=2/5, interpolation=cv.INTER_AREA)

    # captura os 468 pontos da imagem de entrada....
    results = face_mesh.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # a imagem em questao tem apenas 1 rosto !!! portanto, a lista tem um elemento apenas "lista[0]"  !!!
    landmarks = results.multi_face_landmarks[0]

    '''
    As coordenadas de cada landmark sao na escala [0,1]. Multiplica-se a coordenada x pela largura
    e a coordenada y pela altura da imagem....
    OBS: neste exemplo, estamos usando apenas x e y, portanto, no plano....
    '''
    shape_a = img.shape[1] # Largura da imagem
    shape_b = img.shape[0] # Altura da imagem
    idx = 0     # Acumula os indices dos landmarks
    info = []   # Armazena as informações calculadas sobre os landmarks (x,y,z,px,py)
    for landmark in landmarks.landmark:
        x = landmark.x
        y = landmark.y
        z = landmark.z
        
        #Posicoes relativas em pixels
        relative_x = int(shape_a * x)
        relative_y = int(shape_b * y)
        
        """
        #Imprimindo as coordenadas dos landmarks
        cv2.circle(img, (relative_x, relative_y), 5, (0, 0, 255), -1)
        
        #Imprimindo os indices dos landmarks
        
        textShown = str(idx)
        position = (relative_x, relative_y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontsize = 0.3
        color = (0, 255, 0)
        thickness = 1
        linetype=cv2.LINE_AA
        
        cv2.putText(img, textShown, position, font, fontsize, color, thickness, linetype)
        """
        idx += 1

        #Salvando as informações dos landmarks
        info.append([x,y,z,relative_x,relative_y])
    
    # contornos amarelos
    # #Imprimindo regiao da testa
    # img = show_region_of_interest(forehead_contour, info, img)
    
    # #Imprimindo regiao do queixo
    # img = show_region_of_interest(chin_contour, info, img)
    
    # #Imprimindo regiao da bochecha esquerda
    # img = show_region_of_interest(left_cheek_contour, info, img)
    
    # #Imprimindo regiao da bochecha direita
    # img = show_region_of_interest(right_cheek_contour, info, img)
    
    #Segmentando ROIs
    img1, m1 = region_of_interest_segmentation(forehead_contour, info, img)
    img2, m2 = region_of_interest_segmentation(chin_contour, info, img)
    img3, m3 = region_of_interest_segmentation(left_cheek_contour, info, img)
    img4, m4 = region_of_interest_segmentation(right_cheek_contour, info, img)
    
    img1_2 = np.maximum(img1, img2)
    img1_2_3 = np.maximum(img1_2, img3)
    img1_2_3_4 = np.maximum(img1_2_3, img4)
    

    return img1_2_3_4
    # Display the image
    #cv.imshow('MediaPipe FaceMesh', img1_2_3_4)

    #cv.waitKey(0)


# def get_img2(index,paths):
#     img = show_roi_segmentation('imagens/'+paths[index])
#     img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     return img




##########################################
## AUTOMATED ROI SEGMENTATION           ##
## INPUT THE IMAGE AND REGIONS AND      ## 
## RETURNS THE SEGMENTED IMAGE          ##
##########################################

def crop_image(img, shape=(300, 300)):
    """
    Finds the bounding box of non-black pixels and crops the image.

    Args:
        img (ndarray): Input image
        shape (tuple, optional): Target size. Defaults to (300, 300).

    Returns:
        ndarray: Cropped and resized image
    """
    # Convert to grayscale to ensure we catch non-black pixels across all channels
    if img.ndim == 3 and img.shape[2] == 3:
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    else:
        gray = img[..., 0]

    # Find coordinates of all non-zero (non-black) pixels
    coords = cv.findNonZero(gray)
    
    # Fallback just in case the image is completely black
    if coords is None:
        return cv.resize(img, shape)

    # Automatically calculate the exact bounding box (x, y, width, height)
    x, y, w, h = cv.boundingRect(coords)

    # Crop using the bounding box
    cropped_image = img[y:y+h, x:x+w]
    
    # Resize to the final target shape
    cropped_image = cv.resize(cropped_image, shape)
    
    return cropped_image



def region_of_interest_removal(roi, info, img):
    """removes a specified region from the image

    Args:
        roi (Array of int Array): array of polygon regions
        info (List of List of int): Landmark coordinates given by mediapipe 
        img (float): Input image

    Returns:
        [0] Output segmented image
        [1] segmentation binary mask 
    """
    
    # read image as RGB and add alpha (transparency)
    #im = Image.open("img1-512px.jpg").convert("RGB")
    
    # convert to numpy (for convenience)
    imArray = np.asarray(img)
    #plt.imshow(imArray)
    #plt.show()
    
    polygon = []
    for i in range(len(roi)):
        idx_s = roi[i]
        start_point = (info[idx_s][3], info[idx_s][4])
        polygon.append(start_point)
    
    # create mask
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = (np.array(maskIm) - 1)**2 
    #print(mask,mask.max())
    #plt.imshow(maskIm)
    #plt.show()

    # assemble new image (uint8: 0-255)
    newImArray = np.empty(imArray.shape,dtype='uint8')
    
    # segmentation
    newImArray[:,:,0] = np.multiply(imArray[:,:,0], mask)
    newImArray[:,:,1] = np.multiply(imArray[:,:,1], mask)
    newImArray[:,:,2] = np.multiply(imArray[:,:,2], mask)
    #plt.imshow(cv.cvtColor(newImArray,cv.COLOR_BGR2RGB))
    #plt.show()

    return newImArray, mask

"""
Função para segmentar uma região de interesse baseado nos indices dos landmarks.
"""

def region_of_interest_segmentation(roi, info, img):
    """ONLY maintains a specified region from the image

    Args:
        roi (Array of int Array): array of polygon regions
        info (List of List of int): Landmark coordinates given by mediapipe 
        img (float): Input image

    Returns:
        [0] Output segmented image
        [1] segmentation binary mask 
    """
    # read image as RGB and add alpha (transparency)
    #im = Image.open("img1-512px.jpg").convert("RGB")
    
    # convert to numpy (for convenience)
    imArray = np.asarray(img)
    
    polygon = []
    for i in range(len(roi)):
        idx_s = roi[i]
        start_point = (info[idx_s][3], info[idx_s][4])
        polygon.append(start_point)
    
    # create mask
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = np.array(maskIm)

    # assemble new image (uint8: 0-255)
    newImArray = np.empty(imArray.shape,dtype='uint8')
    
    # segmentation
    newImArray[:,:,0] = np.multiply(imArray[:,:,0], mask)
    newImArray[:,:,1] = np.multiply(imArray[:,:,1], mask)
    newImArray[:,:,2] = np.multiply(imArray[:,:,2], mask)

    return newImArray, mask



def info_gen(img):
    """ performs mediapipe landmarks retrieval.

    Args:
        img (float): Input image that may contain a HUMAN FACE

    Returns:
        info (List of List of int): Landmark coordinates given by mediapipe 
    """
    #img = cv.resize(img, (300,300), interpolation=cv.INTER_AREA)
    # mp_face_mesh = mp.solutions.face_mesh # type: ignore
    # face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    # os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"    
    # captura os 468 pontos da imagem de entrada....
    results = face_mesh.process(img)
    # del face_mesh
    # del mp_face_mesh
    # a imagem em questao tem apenas 1 rosto !!! portanto, a lista tem um elemento apenas "lista[0]"  !!!
    landmarks = results.multi_face_landmarks[0]

    '''
    As coordenadas de cada landmark sao na escala [0,1]. Multiplica-se a coordenada x pela largura
    e a coordenada y pela altura da imagem....
    OBS: neste exemplo, estamos usando apenas x e y, portanto, no plano....
    '''
    shape_a = img.shape[1] # Largura da imagem
    shape_b = img.shape[0] # Altura da imagem
    info = []   # Armazena as informações calculadas sobre os landmarks (x,y,z,px,py)
    for landmark in landmarks.landmark:
        x = landmark.x
        y = landmark.y
        z = landmark.z
        
        #Posicoes relativas em pixels
        relative_x = int(shape_a * x)
        relative_y = int(shape_b * y)
        

        #Salvando as informações dos landmarks
        info.append([x,y,z,relative_x,relative_y])
    return info


def show_or_remove_roi(img,regions_to_segment,regions_to_remove,crop=False,plot=False,fullplot=False,return_all=False):
    """a function that performs segmentation using polygons based on mediapipe landmarks. 
    Given an input image containing a human face, a list of regions to segment and a list of regions
    to remove the function returns a segmented image.

    Args:
        img (3d uint8 array): input image containing a human face
        regions_to_segment (List of Lists): polygonal regions to maintain
        regions_to_remove (List of Lists): polygonal regions to remove
        crop (bool, optional): crops the output image to the face as an square. Defaults to False.
        plot (bool, optional): plot the image. Defaults to False.
        fullplot (bool, optional): plot all the segmented and removed regions. Defaults to False.
        only_segments (bool, optional): If the process will only segment some regions and not remove any. Defaults to False.

    Returns:
        _type_: _description_
    """
    info = info_gen(img)
    #img = cv.resize(img, (512,512), interpolation=cv.INTER_AREA)



    imgs = []
    if regions_to_remove != []:
        for region in regions_to_remove:
            imgx, m1 = region_of_interest_removal(region, info, img)
            imgs.append(imgx)
    
    if regions_to_segment != []:
        for region in regions_to_segment:
            imgx, m1 = region_of_interest_segmentation(region, info, img)
            imgs.append(imgx)
    
    if regions_to_remove != []:
        result = np.minimum.reduce(imgs)
    else:
        result = np.maximum.reduce(imgs)

    if fullplot:
        plt.figure(frameon = False,figsize=(9,len(imgs)*3))
        for i in range(len(imgs)):
            plt.subplot(len(imgs),3,i+1)
            plt.imshow(imgs[i])
            plt.axis('off')
        plt.show()
    if plot:
        plt.figure(frameon = False,figsize=(5,5))
        plt.imshow(crop_image(result))
        plt.axis('off')
        plt.show()

    if return_all:
        result_C = crop_image(result)
        return result, result_C, imgs
    if crop:
        result = crop_image(result)
        return result
    else:
        return result

#show_or_remove_roi(img,[face],regions,crop=True,plot=True,fullplot=True)
    

# img = cv.imread('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/paper_benchmark/data_manipulation/to extract.png')
# img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

# result = show_or_remove_roi(img,[FACE_WITHOUT_BEARD],[R_EYE,L_EYE],crop=True,plot=True)
# print(result)
    
#%%
# cropped = cv.cvtColor(
# cv.imread('/store/vitorpmatias/TESE/TESE/dissertation/dataset/all_cropped_images_by_class/2/2_Brazilian Faces2-04_face_1.jpg'),
# cv.COLOR_BGR2RGB)

# cropped = show_region_of_interest(L_EYE, info_gen(cropped), cropped)
# # show_or_remove_roi(
# #                 cropped, 
# #                 [FACE_WITHOUT_BEARD],
# #                 [],  
# #                 crop=True)
# plt.imshow(cropped)
# # %%
