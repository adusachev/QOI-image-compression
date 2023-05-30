import os
from typing import Optional
from pathlib import Path
import numpy as np
from qoi_compress.qoi_encoder import run_encoder
from qoi_compress.qoi_decoder import run_decoder
from qoi_compress.read_png import read_png
from qoi_compress.setup_logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def run_single_experiment(png_filename: str, qoi_filename: str) -> None:
    """
    Run qoi_encoder on image "png_filename" and save qoi image
    Then run qoi_decoder and compare decoded image with original png image

    :raises Exception: if decoded qoi image is not equal to original png image
    """    
    orig_img, _, _, _ = read_png(png_filename)
    logger.info(f"Process image {Path(png_filename).name}, size = {orig_img.shape[0]}x{orig_img.shape[1]}")
        
    # encoding
    qoi_filename, encoding_time = run_encoder(png_filename, qoi_filename)

    # decoding
    img_decoded, decoding_time = run_decoder(qoi_filename)
    
    # check that image encoded and decoded correctly
    if np.all(img_decoded == orig_img):
        logger.debug("OK, decoded qoi image is equal to original png image")
    else:
        logger.error(f"Decoding failed, qoi image {qoi_filename} is not equal to original png image {png_filename}")
        logger.debug(f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")
        raise Exception("Error in encoding/decoding algorithm, qoi image is not equal to original png image")
    


def run_multiple_experiments(dir_with_png: str, dir_with_qoi: str) -> None:
    """ 
    Launch run_single_experiment() for each png file in "dir_with_png"
    """
    for filename in os.listdir(dir_with_png):
        if Path(filename).suffix == ".png":
            name = Path(filename).stem
            png_file = os.path.join(dir_with_png, filename)
            qoi_file = os.path.join(dir_with_qoi, f"{name}.qoi")
                
            run_single_experiment(png_file, qoi_file)
            print('------------------------------------- \n')





if __name__ == '__main__':    
    # png_filename = str(BASE_DIR / "png_images/doge.png")
    # qoi_filename = str(BASE_DIR / 'qoi_images/tmp.qoi')
    # run_single_experiment(png_filename, qoi_filename)
    
    dir_with_png = str(BASE_DIR / "debug_png_images/")
    dir_with_qoi = str(BASE_DIR / "qoi_images/")
    run_multiple_experiments(dir_with_png, dir_with_qoi)
