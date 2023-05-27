import os
import time
from pathlib import Path
import logging
import numpy as np

from qoi_compress.qoi_encoder import run_encoder
from qoi_compress.qoi_decoder import run_decoder
from qoi_compress.read_png import read_png

BASE_DIR = Path(__file__).resolve().parent.parent.parent


logger = logging.getLogger(__name__)
loglevel = "DEBUG"
logger.setLevel(loglevel)
handler = logging.StreamHandler()
handler.setLevel(loglevel)
format = '%(levelname)s - %(filename)s - %(funcName)s: %(message)s'
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)





def run_single_experiment(png_filename, qoi_filename=None):
    """
    Run qoi_encoder on image "png_filename" and save qoi image
    Then run qoi_decoder and compare decoded image with original png image

    :raises Exception: if decoded qoi image is not equal to original png image
    """
    if qoi_filename is None:
        name = Path(png_filename).stem
        qoi_filename = os.path.join(BASE_DIR, f'./qoi_images/{name}.qoi')
        
        if not os.path.exists(os.path.join(os.getcwd(), 'qoi_images')):
            os.mkdir('qoi_images')
    
    orig_img, _, _, _ = read_png(png_filename)
    logger.info(f"Process image {Path(png_filename).name}, size = {orig_img.shape[0]}x{orig_img.shape[1]}")
        
    # encoding
    qoi_filename, encoding_time = run_encoder(png_filename, qoi_filename)
    logger.debug(f"Image encoded and saved as {qoi_filename}")
    logger.debug(f"Encoding time: {1000 * encoding_time:.3f} ms")

    # decoding
    img_decoded, decoding_time = run_decoder(qoi_filename)
    
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
                
            run_single_experiment(png_filename)
            print('------------------------------------- \n')





if __name__ == '__main__':    
    png_filename = str(BASE_DIR / "png_images/doge.png")
    qoi_filename = str(BASE_DIR / 'qoi_images/tmp.qoi')
    run_single_experiment(png_filename, qoi_filename=qoi_filename)
    
    # dir_with_png = str(BASE_DIR / "png_images/")
    # run_multiple_experiments(dir_with_png)
    