import os
import time
from pathlib import Path
import numpy as np

from qoi_encoder import encode
from qoi_decoder import decode
from read_png import read_png





def run_encoder(png_filename, qoi_filename=None):
    if qoi_filename is None:
        name = Path(png_filename).stem
        qoi_filename = f'./qoi_images/{name}.qoi'
    
    _, R, G, B = read_png(png_filename)
    
    # create empty qoi file (or replace existing)
    file = open(qoi_filename, 'w')
    file.close()
    
    start_time = time.time()
    with open(qoi_filename, 'ab') as file:
        encode(R, G, B, file)
    end_time = time.time()

    print(f"Image encoded and saved as {qoi_filename}")
    print(f"Time elapsed: {end_time - start_time} sec", '\n')
    
    
    
def run_decoder(qoi_filename, png_filename):
    
    orig_img, R, G, B = read_png(png_filename)
    height, width = orig_img.shape[0], orig_img.shape[1]

    start_time = time.time()
    R_decoded, G_decoded, B_decoded = decode(qoi_filename, width, height)
    end_time = time.time()

    img_decoded = np.zeros((height, width, 3), dtype=int)
    img_decoded[:, :, 0] = R_decoded.reshape((height, width))
    img_decoded[:, :, 1] = G_decoded.reshape((height, width))
    img_decoded[:, :, 2] = B_decoded.reshape((height, width))
    
    assert np.all(img_decoded == orig_img), \
        f"Decoded qoi image {qoi_filename} is not equal to original png image {png_filename}"
        
    print("Decoded qoi image is equal to original png image:", np.all(img_decoded == orig_img))
    print(f"Time elapsed: {end_time - start_time} sec")




if __name__ == '__main__':
    
    dir_with_png = './more_png_images'
    for name in os.listdir(dir_with_png):
        if Path(name).suffix == ".png":
            png_filename = os.path.join(dir_with_png, name)
    
            name = Path(png_filename).stem
            if name == "huge_6k":
                continue
            qoi_filename = f'./qoi_images/{name}.qoi'
            run_encoder(png_filename, qoi_filename)
            run_decoder(qoi_filename, png_filename)
            print('-------------------------------------')
    
    