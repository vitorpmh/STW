import cv2 as cv
import numpy as np
from scipy.stats import mode, skew, kurtosis
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm
from sklearn.decomposition import PCA
# import scienceplots
# plt.style.use('science')

def ccv(img, tau=0.01, normalize = True, ignore_black = True, return_plot = False):
    """_summary_

    Args:
        img (uint8): 1d image

    Returns:
        _type_: _description_
    """

    factor = 1
    if normalize:
        factor = img.shape[0] * img.shape[1]

    pixel_qty = int(img.shape[0] * img.shape[1] * tau)

    values = np.unique(img)
    coherent_list = [0 for i in range(max(values)+1)]
    incoherent_list = [0 for i in range(max(values)+1)]
    if return_plot:
        plot = np.zeros_like(img)
        for pixel_val in values:
            if ignore_black:
                if pixel_val == 0:
                    continue
            connected_components = cv.connectedComponentsWithStats((img == pixel_val).astype(
                np.uint8), connectivity=8)  # conectivity 8 as the article
            neighbours = np.unique(
                connected_components[1][img == pixel_val], return_counts=True)

            coherent = 0
            incoherent = 0
            for val, neighbours_size in zip(neighbours[0],neighbours[1]):
                if neighbours_size >= pixel_qty:
                    coherent += neighbours_size
                    plot[connected_components[1] == val] = 2
                else:
                    incoherent += neighbours_size
                    plot[connected_components[1] == val] = 1

            coherent_list[pixel_val] += coherent
            incoherent_list[pixel_val] += incoherent
        return np.array(coherent_list)/factor, np.array(incoherent_list)/factor, plot

    else:
        for pixel_val in values:
            if ignore_black:
                if pixel_val == 0:
                    continue
            connected_components = cv.connectedComponentsWithStats((img == pixel_val).astype(
                np.uint8), connectivity=8)  # conectivity 8 as the article
            neighbours = np.unique(
                connected_components[1][img == pixel_val], return_counts=True)

            coherent = 0
            incoherent = 0
            for neighbours_size in neighbours[1]:
                if neighbours_size >= pixel_qty:
                    coherent += neighbours_size
                else:
                    incoherent += neighbours_size

            coherent_list[pixel_val] += coherent
            incoherent_list[pixel_val] += incoherent

        return np.array(coherent_list)/factor, np.array(incoherent_list)/factor


def histogram(img, bins=256, normalized=True, ignore_black=True, ignore_white=True):
    """

    Args:
        img (3d uint8 array): input image
    """
    img = img.astype(np.float32)

    if ignore_black:
        black_mask = (img == 0).all(axis=2)
        img[black_mask] = np.nan
    elif ignore_black and ignore_white:
        white_mask = (img == 255).all(axis=2)
        img[white_mask] = np.nan

    pixel_quantity = 1
    if normalized:
        pixel_quantity = img.shape[0] * img.shape[1]

    hists = []
    for channel in range(img.shape[2]):
        img_channel = img[:, :, channel]

        # channel_hist = [((img_channel==i) & boolean).sum().astype(float)/pixel_quantity for i in range(256)]

        channel_hist = np.histogram(img_channel, bins, [0, 255])[0]
        channel_hist = channel_hist/pixel_quantity
        hists.append(channel_hist)

    return hists


def oppo_space(img):

    img = img.astype(np.float32)
    black_mask = (img == 0).all(axis=2)

    img[black_mask] = np.nan

    r = img[..., 0]
    g = img[..., 1]
    b = img[..., 2]

    out_r = (r - g)/np.sqrt(2)
    out_g = (r + g - 2 * b)/np.sqrt(6)
    out_b = (r + g + b)/np.sqrt(3)

    out = np.stack([out_r, out_g, out_b], axis=-1)
    return out


def oppo_hist(img, bins=None, normalized=True):
    """_summary_

    Args:
        img (_type_): _description_
        bins (_type_, optional): _description_. Defaults to None.
        normalized (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    top = np.nanmax(img)
    low = np.nanmin(img)

    pixel_quantity = 1
    if normalized:
        pixel_quantity = img.shape[0] * img.shape[1]

    if bins is None:
        bins = int(top-low)

    hists = []
    for channel in range(img.shape[2]):
        img_channel = img[:, :, channel]

        channel_hist = np.histogram(img_channel, bins, [low, top])[0]
        channel_hist = channel_hist/pixel_quantity

        hists.append(channel_hist)

    return hists


def img_statistics(img, normalize=True, ignore_black=True):
    """_summary_

    Args:
        img (_type_): _description_
        normalize (bool, optional): _description_. Defaults to True.
        ignore_black (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    if ignore_black:
        img = img.astype(np.float32)
        black_mask = (img == 0).all(axis=2)
        img[black_mask] = np.nan

    # Calculate statistics for each channel
    stats = {
        'Minimum': [],
        'Maximum': [],
        'Mean': [],
        'Median': [],
        'Mode': [],
        'Standard Deviation': [],
        'Variance': [],
        'Skewness': [],
        'Kurtosis': []
    }
    stats['Skewness'] = skew(
        histogram(img, normalized=True, ignore_white=False), axis=1, nan_policy='omit')
    stats['Kurtosis'] = kurtosis(
        histogram(img, normalized=True, ignore_white=False), axis=1, nan_policy='omit')

    if normalize:
        img = img.astype(np.float32)
        img = img/255

    for i in range(img.shape[2]):
        channel = img[:, :, i]
        stats['Minimum'].append(np.nanmin(channel))
        stats['Maximum'].append(np.nanmax(channel))
        stats['Mean'].append(np.nanmean(channel))
        stats['Median'].append(np.nanmedian(channel))
        stats['Mode'].append(mode(channel, axis=0, nan_policy='omit')[0][0])
        stats['Standard Deviation'].append(np.nanstd(channel))
        stats['Variance'].append(np.nanvar(channel))

    # stats = np.array([np.array(a) for a in stats.values()])
    # stats = stats.flatten()

    return stats


def quantization(img):
    channel_1 = img[..., 0]
    channel_2 = img[..., 1]
    channel_3 = img[..., 2]
    # 192 = 0b11000000 which only gathers the first two
    channel_1_new = (channel_1 & 192) >> 2
    channel_2_new = (channel_2 & 192) >> 4
    channel_3_new = (channel_3 & 192) >> 6
    conjugate = channel_1_new | channel_2_new | channel_3_new
    return conjugate


def gch(img, normalized=True, ignore_black=True):
    """_summary_

    Args:
        img (_type_): _description_
        normalized (bool, optional): _description_. Defaults to True.
    """
    factor = 1
    if normalized:
        factor = img.shape[0] * img.shape[1]
    
    black_count = (img==0).all(axis=2).sum()
    out = quantization(img)

    hist = np.histogram(out,bins=64)[0]
    if ignore_black:
        hist[0] = hist[0] - black_count
        return hist/factor
    else:
        return hist/factor

def bic(img, normalize=True, return_plot=False, connectivity_eight=False):
    """border interior image descriptor with 64 values quantization

    Args:
        img (_type_): rgb image
        normalize (bool, optional): returns the border and interior histograms as normalized. Defaults to True
        return_plot (bool, optional): unlocks the return of a image illustrating the border and interior. Defaults to False.
        connectivity_eight (bool, optional): if true the diagonal values are also checked for connectivity. Defaults to False.

    Returns:
        list of int or float: border histogram either normalized or as regarded by the arg normalize = True 
        list of int or float: interior histogram either normalized or as regarded by the arg normalize = True 
        IF RETURN_PLOT = TRUE
        3bit image: returns a image containing the background = 0, border = 1, and interior = 2.
    """

    out = quantization(img)

    # guide threshold to calculate bic only inside the segmented regions.
    _, thresh = cv.threshold(out, 0, 1, cv.THRESH_BINARY)

    factor = 1
    if normalize:
        factor = img.shape[0] * img.shape[1]

    # plot is the border/interior image result
    if return_plot:
        plot = np.zeros_like(out)

    border = [0 for _ in range(64)]
    interior = [0 for _ in range(64)]
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            # if the value in the thresholded guide is not 1 (hence it is a 0) all the process will be skipped.
            if thresh[i][j] != 1:
                continue
            aux = out[i][j]
            # print(aux)
            if not connectivity_eight:
                if ((aux == out[i+1][j]) and
                    (aux == out[i-1][j]) and
                    (aux == out[i][j-1]) and
                        (aux == out[i][j+1])):
                    interior[aux] += 1
                    if return_plot:
                        plot[i][j] = 2
                else:
                    border[aux] += 1
                    if return_plot:
                        plot[i][j] = 1
            else:  # conectivity eight = True
                if ((aux == out[i+1][j]) and
                    (aux == out[i-1][j]) and
                    (aux == out[i][j-1]) and
                    (aux == out[i][j+1]) and
                    (aux == out[i-1][j-1]) and
                    (aux == out[i-1][j+1]) and
                    (aux == out[i+1][j-1]) and
                        (aux == out[i+1][j+1])):
                    interior[aux] += 1
                    if return_plot:
                        plot[i][j] = 2
                else:
                    border[aux] += 1
                    if return_plot:
                        plot[i][j] = 1

    if return_plot:
        return np.divide(border, factor), np.divide(interior, factor), plot
    else:
        return np.divide(border, factor), np.divide(interior, factor)


def descriptors_generator(img, bins=64, normalize=True, ignore_black=True):
    """
    Generates a comprehensive set of image descriptors from the input image, returning them as a dictionary.

    Parameters:
    ----------
    img : numpy.ndarray
        The input image (in BGR format) for which descriptors are to be generated.
    bins : int, optional
        The number of bins to use for histograms. Default is 64.
    normalize : bool, optional
        Whether to normalize the histograms and other descriptors. Default is True.
    ignore_black : bool, optional
        If True, ignores black pixels in histograms. Default is True.

    Returns:
    -------
    feature_dict : dict
        A dictionary where each key is a string representing the descriptor name and index, and each value is the corresponding descriptor value.
        The dictionary includes color histograms (RGB, Lab, YCrCb, HSV), GCH (Global Color Histogram), CCV (Color Coherence Vector), BIC (Border-Interior Classification),
        and various statistical features.
    end_of_histograms : int
        The index indicating where the histograms end in the dictionary, useful for separating histogram features from other features.

    Notes:
    -----
    - The function converts the input image to multiple color spaces (Lab, YCrCb, HSV) and computes histograms for specific channels.
    - A Global Color Histogram (GCH) is computed using the `gch` function.
    - Coherent and incoherent texture features are computed using a Color Coherence Vector (CCV) with 64 bins.
    - The BIC (Border-Interior Classification) algorithm is applied to the image to calculate border and interior descriptors.
    - Statistical features of the image are extracted using the `img_statistics` function.
    - The feature dictionary is structured with keys formatted as `descriptor_name_index` and values corresponding to the descriptor values.
    - The `end_of_histograms` index helps in distinguishing histogram features from the statistical features in the resulting dictionary.
    """
    # channel histograms
    r_hist, g_hist, b_hist = histogram(
        img,
        bins=bins,
        normalized=normalize, ignore_black=ignore_black, ignore_white=False)

    labimg = cv.cvtColor(img,cv.COLOR_BGR2Lab)
    hist_l_lab = histogram(labimg,bins=bins,ignore_black=True)[0]
    ycrcbimg = cv.cvtColor(img,cv.COLOR_BGR2YCrCb)
    hist_y_ycrcb = histogram(ycrcbimg,bins=bins,ignore_black=True)[0]
    hsvimg = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    hist_v_hsv = histogram(hsvimg,bins=bins,ignore_black=True)[2]
    
    # GCH
    gch_hist = gch(img)

    # ccv with 64 bins
    coherent_64, incoherent_64 = ccv(
        quantization(cv.GaussianBlur(img, (5, 5), 0)))
    coherent_64[0] = 0
    incoherent_64[0] = 0
    coherent_64 = np.pad(coherent_64, (0, 64-len(coherent_64)))
    incoherent_64 = np.pad(incoherent_64, (0, 64-len(incoherent_64)))

    # BIC
    border, interior = bic(img, normalize=normalize, connectivity_eight=True)


    # stats
    stats = img_statistics(img)


    feature_dict = {}
    def add_to_dict(base_name, lst):
        for i in range(len(lst)):
            feature_dict[f"{base_name}_{i}"] = lst[i]

    add_to_dict("r_hist", r_hist)
    add_to_dict("g_hist", g_hist)
    add_to_dict("b_hist", b_hist)
    add_to_dict("hist_l_lab", hist_l_lab)
    add_to_dict("hist_y_ycrcb", hist_y_ycrcb)
    add_to_dict("hist_v_hsv", hist_v_hsv)
    add_to_dict("gch_hist", gch_hist)
    add_to_dict("coherent_64", coherent_64)
    add_to_dict("incoherent_64", incoherent_64)
    add_to_dict("border", border)
    add_to_dict("interior", interior)
    end_of_histograms = len(feature_dict.values())

    for key,values in stats.items():
        for idx,val in enumerate(values): 
            feature_dict[key + f'_{idx}'] = val

    return feature_dict, end_of_histograms


class BorutaFeatureSelection:
    def __init__(self, n_estimators=100, max_iter=100, random_state=None, verbose=True):
        self.n_estimators = n_estimators
        self.max_iter = max_iter
        self.random_state = random_state
        self.importance = None
        self.verbose = verbose

    def fit(self, X, y):
        self.importance = self._calculate_feature_importance(X, y)

    def _calculate_feature_importance(self, X, y):
        rf = RandomForestClassifier(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=8
        )
        rf.fit(X, y)
        return rf.feature_importances_

    def select_features(self, X, y, threshold=0.01):
        selected_features = np.full(X.shape[1], False)
        for _ in tqdm(range(self.max_iter), disable=~self.verbose):
            importances = self._calculate_feature_importance(X, y)
            z_scores = self._calculate_z_scores(importances)
            selected_features |= importances > threshold
            if np.all(z_scores[selected_features] < 0):
                break
        return np.where(selected_features)[0]

    def _calculate_z_scores(self, importances):
        mean = np.mean(importances)
        std = np.std(importances)
        return (importances - mean) / std


def get_selected_features(X, y, verbose=True):
    boruta_selector = BorutaFeatureSelection(
        n_estimators=100,
        max_iter=40,
        random_state=42,
        verbose=verbose
    )
    boruta_selector.fit(X, y)

    selected_features_indices = boruta_selector.select_features(X, y)
    selected_features = X.columns[selected_features_indices].tolist()
    print("Selected features:", selected_features)
    return selected_features


def pca_select_features(X, var=0.9):
    pca = PCA(n_components=var)
    pca_X = pca.fit_transform(X)
    return pca_X, pca


# src_path = '/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/data/OurData/images/5/19_Brazilian Faces_19-06.jpg'
# src = cv.cvtColor(cv.imread(src_path), cv.COLOR_BGR2RGB)



# quant = quantization(src)
# _,_, bic_img = bic(src,return_plot=True)

# fig,axes = plt.subplots(1,4,figsize=(10,2.5))

# axes[0].imshow(src)
# axes[1].imshow(quant,cmap='gray')
# axes[2].imshow(bic_img,cmap='gray')
# axes[2].legend(
#     [
#         plt.Rectangle((0,0),1,1, color='gray'),
#         plt.Rectangle((0,0),1,1, color='white')
#         ],
#     ['Border','Interior'], 
#     loc='upper left',
#     prop={'size':6},
#     frameon=True, framealpha=1)

# img = quantization(cv.GaussianBlur(src, (5, 5), 0))
# _,_,ccv_image = ccv(img, tau=0.01, normalize = True, ignore_black = True, return_plot = True)


# axes[3].imshow(ccv_image,cmap='gray')
# axes[3].legend(
#     [
#         plt.Rectangle((0,0),1,1, color='gray'),
#         plt.Rectangle((0,0),1,1, color='white')
#         ],
#     ['Incoherent','Coherent'], 
#     loc='upper left',
#     prop={'size':6},
#     frameon=True, framealpha=1)

# for i in range(4):
#     axes[i].axis('off')


# plt.subplots_adjust(
#     top=0.969,
#     bottom=0.031,
#     left=0.007,
#     right=0.993,
#     hspace=0.125,
#     wspace=0.029)

# plt.savefig('descriptors.eps', dpi=300)
# plt.show()