from typing import Tuple, List
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from PIL import Image  # type: ignore


def read_png(path_to_png: str, 
             draw_img: bool = False,
             draw_flatten_img: bool = False) -> Tuple[np.ndarray, List[int], List[int], List[int]]:
    """
    Read .png image and return flatten array of each channel
    Draw image and flatten image if required
    
    :return: 1) img - original image, shape=(heigth, width, 3)
             2) R_flat - flatten 1d array of R-cahnnel pixel values, shape=(heigth*width,)
             3) G_flat, B_flat - analogically to R_flat
    """
    img = np.asarray(Image.open(path_to_png))
    img = img[:, :, :3]
    
    R = img[:, :, 0].astype(int)
    G = img[:, :, 1].astype(int)
    B = img[:, :, 2].astype(int)
    R_flat = np.ravel(R)
    G_flat = np.ravel(G)
    B_flat = np.ravel(B)
    
    height, width = img.shape[0], img.shape[1]
    if draw_img:
        plt.imshow(img)
        plt.title(f"Image {height}x{width}")
        plt.xticks([])
        plt.yticks([])
    if draw_flatten_img:
        plt.figure(figsize=(15, 4))
        flatten_img = np.vstack((R_flat, G_flat, B_flat)).T.reshape((1, height*width, 3)) 
        plt.imshow(flatten_img)
        plt.title(f"Flatten image 1x{height * width}")
        plt.xticks([])
        plt.yticks([])
        
    # convert np.array with np.int64 elems to list with int elems 
    # for correct work of n.to_bytes()            
    return img, R_flat.tolist(), G_flat.tolist(), B_flat.tolist()


if __name__ == "__main__":
    path = "/mnt/c/Users/Aleksei/Desktop/image compression/QOI-image-compression/png_images/R_video.png"
    
    res = read_png(path)
