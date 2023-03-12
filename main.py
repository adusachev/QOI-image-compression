import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# from qoi_encoder import *




def read_png(path_to_png, draw_img=False, draw_flatten_img=False):
    """
    Read .png image and return flatten array of each channel
    Draw image and flatten image if required
    
    :return: 1) img - original image, shape=(heigth, width, 3)
             2) R_flat - flatten 1d array of R-cahnnel pixel values, shape=(heigth*width,)
             3) G_flat, B_flat - analogically to R_flat
    """
    img = cv.imread(path_to_png)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # BGR -> RGB
    
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
        
    return img, R_flat, G_flat, B_flat




def main():
    path = './png_images/R_video.png'
    _, R, G, B = read_png(path)
    
    output_path = './qoi_images/R_video.qoi'
    encode(R, G, B, output_path)



if __name__ == '__main__':
    main()