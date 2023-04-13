import os
import time
from pathlib import Path
import logging
import numpy as np

from qoi_encoder import encode
from qoi_decoder import decode
from read_png import read_png


logger = logging.getLogger(__name__)
loglevel = "DEBUG"
logger.setLevel(loglevel)
handler = logging.StreamHandler()
handler.setLevel(loglevel)
format = '%(levelname)s - %(filename)s - %(funcName)s: %(message)s'
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)



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

    logger.debug(f"Image encoded and saved as {qoi_filename}")
    logger.debug(f"Encoding time: {end_time - start_time} sec")
    
    
    
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
    
        
    if np.all(img_decoded == orig_img):
        logger.debug("Decoded qoi image is equal to original png image")
    else:
        logger.error(f"Decoding failed, qoi image {qoi_filename} is not equal to original png image {png_filename}")
        logger.debug(f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")
        raise Exception("Error in decoding algorithm, qoi image is not equal to original png image")
    
    logger.debug(f"Decoding time: {end_time - start_time} sec")




if __name__ == '__main__':
    
    dir_with_png = './png_images'
    for name in os.listdir(dir_with_png):
        if Path(name).suffix == ".png":
            png_filename = os.path.join(dir_with_png, name)
    
            name = Path(png_filename).stem
            qoi_filename = f'./qoi_images/{name}.qoi'
            logger.info(f"Process image {name}.png")            
            run_encoder(png_filename, qoi_filename)
            run_decoder(qoi_filename, png_filename)
            print('------------------------------------- \n')
    
    