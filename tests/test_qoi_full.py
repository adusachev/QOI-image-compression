import os
from pathlib import Path
import unittest
import numpy as np

import sys
sys.path.append("..")
from main import run_encoder, run_decoder


class TestQOI(unittest.TestCase):
    
    def test_single_image(self):
        
        png_filename = "./png_images/R_video.png"
        
        # encoding
        qoi_filename, _ = run_encoder(png_filename)

        # decoding
        img_decoded, orig_img, _ = run_decoder(qoi_filename, png_filename)
        
        self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")

    
    def test_multiple_images(self):
        
        dir_with_png = "./png_images"
        
        for name in os.listdir(dir_with_png):
            if Path(name).suffix == ".png":
                png_filename = os.path.join(dir_with_png, name)
                
                # encoding
                qoi_filename, _ = run_encoder(png_filename)

                # decoding
                img_decoded, orig_img, _ = run_decoder(qoi_filename, png_filename)
                
                self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding of image {qoi_filename} failed at indexes {np.where(img_decoded != orig_img)[0]}")
                


if __name__ == '__main__':
    unittest.main()
