import os
import time
from pathlib import Path
import logging
import numpy as np

import qoi_encoder
import qoi_decoder
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
    """
    Run qoi encode algorithm on image "png_filename" and save qoi image as "qoi_filename" 
    """
    if qoi_filename is None:
        name = Path(png_filename).stem
        qoi_filename = f'./qoi_images/{name}.qoi'
    
    img, R, G, B = read_png(png_filename)
    
    # create empty qoi file with header (or replace existing)
    file = open(qoi_filename, 'wb')
    qoi_encoder.write_qoi_header(img, file)
    file.close()
    
    start_time = time.time()
    with open(qoi_filename, 'ab') as file:
        qoi_encoder.encode(R, G, B, file)
    end_time = time.time()
        
    time_elapsed = end_time - start_time
        
    return qoi_filename, time_elapsed
    

    
    
def run_decoder(qoi_filename, png_filename):
    """
    Run qoi decode algorithm on image "qoi_filename" 
    """
    start_time = time.time()
    R_decoded, G_decoded, B_decoded, height, width = qoi_decoder.decode(qoi_filename)
    end_time = time.time()
    
    time_elapsed = end_time - start_time

    # reshape decoded 1d arrays into image with 3 channels
    img_decoded = np.zeros((height, width, 3), dtype=int)
    img_decoded[:, :, 0] = R_decoded.reshape((height, width))
    img_decoded[:, :, 1] = G_decoded.reshape((height, width))
    img_decoded[:, :, 2] = B_decoded.reshape((height, width))
    
    orig_img, _, _, _ = read_png(png_filename)  # TODO: read png image in other place
    
    return img_decoded, orig_img, time_elapsed



def run_single_experiment(png_filename):
    """_summary_

    :param png_filename: _description_
    :raises Exception: _description_
    """
    # encoding
    qoi_filename, encoding_time = run_encoder(png_filename)
    logger.debug(f"Image encoded and saved as {qoi_filename}")
    logger.debug(f"Encoding time: {1000 * encoding_time:.3f} ms")

    # decoding
    img_decoded, orig_img, decoding_time = run_decoder(qoi_filename, png_filename)
    
    # check that image encoded and decoded correctly
    if np.all(img_decoded == orig_img):
        logger.debug("OK, decoded qoi image is equal to original png image")
    else:
        logger.error(f"Decoding failed, qoi image {qoi_filename} is not equal to original png image {png_filename}")
        logger.debug(f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")
        raise Exception("Error in encoding/decoding algorithm, qoi image is not equal to original png image")
    
    logger.debug(f"Decoding time: {1000 * decoding_time:.3f} ms")



def run_multiple_experiments(dir_with_png):
    """ 
    Launch run_single_experiment() for each png file in "dir_with_png"
    """
    for name in os.listdir(dir_with_png):
        if Path(name).suffix == ".png":
            png_filename = os.path.join(dir_with_png, name)
    
            name = Path(png_filename).stem
            logger.info(f"Process image {name}.png")            
            run_single_experiment(png_filename)
            print('------------------------------------- \n')





if __name__ == '__main__':
    # png_filename = "./png_images/R_video.png"
    # run_single_experiment(png_filename)
    
    dir_with_png = './png_images'
    run_multiple_experiments(dir_with_png)
    
    # png_filename = "./png_images/R_video.png"
    # run_encoder(png_filename, qoi_filename='./data/tmp.txt')
    