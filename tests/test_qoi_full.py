import os
from pathlib import Path
import unittest
import numpy as np

from qoi_compress.qoi_decoder import run_decoder
from qoi_compress.qoi_encoder import run_encoder
from qoi_compress.read_png import read_png


BASE_DIR = Path(__file__).resolve().parent.parent


class TestQOI(unittest.TestCase):
    
    def test_single_image(self):
        
        png_filename = str(BASE_DIR / "png_images/R_video.png")
        
        # encoding
        qoi_filename, _ = run_encoder(png_filename)

        # decoding
        img_decoded, _ = run_decoder(qoi_filename)
        
        # compare with original image
        orig_img, _, _, _ = read_png(png_filename)
        
        self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")

    
    def test_multiple_images(self):
        
        dir_with_png = str(BASE_DIR / "png_images/")
        
        for name in os.listdir(dir_with_png):
            if Path(name).suffix == ".png":
                png_filename = os.path.join(dir_with_png, name)
                
                # encoding
                qoi_filename, _ = run_encoder(png_filename)

                # decoding
                img_decoded, _ = run_decoder(qoi_filename)
                
                # compare with original image
                orig_img, _, _, _ = read_png(png_filename)
                
                self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding of image {qoi_filename} failed at indexes {np.where(img_decoded != orig_img)[0]}")
                


if __name__ == '__main__':
    unittest.main()
