import os
from pathlib import Path
import unittest
import numpy as np
from qoi_compress.qoi_decoder import run_decoder
from qoi_compress.qoi_encoder import run_encoder
from qoi_compress.read_png import read_png


BASE_DIR = Path(__file__).resolve().parent.parent

if not os.path.exists(BASE_DIR / "qoi_images"):
    os.mkdir(BASE_DIR / "qoi_images")


class TestQOI(unittest.TestCase):
    
    def test_single_image(self):
        
        png_filename = str(BASE_DIR / "png_images/R_video.png")
        qoi_filename = str(BASE_DIR / "qoi_images/R_video.qoi")
        
        # encoding
        qoi_filename, _ = run_encoder(png_filename, qoi_filename)

        # decoding
        img_decoded, _ = run_decoder(qoi_filename)
        
        # compare with original image
        orig_img, _, _, _ = read_png(png_filename)
        
        self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding failed at indexes {np.where(img_decoded != orig_img)[0]}")

    
    def test_multiple_images(self):
        
        dir_with_png = str(BASE_DIR / "png_images")
        dir_with_qoi = str(BASE_DIR / "qoi_images")
        
        for filename in os.listdir(dir_with_png):
            if Path(filename).suffix == ".png":
                name = Path(filename).stem
                png_file = os.path.join(dir_with_png, filename)
                qoi_file = os.path.join(dir_with_qoi, f"{name}.qoi")
                
                # encoding
                qoi_filename, _ = run_encoder(png_file, qoi_file)

                # decoding
                img_decoded, _ = run_decoder(qoi_file)
                
                # compare with original image
                orig_img, _, _, _ = read_png(png_file)
                
                self.assertTrue(np.all(img_decoded == orig_img), 
                        f"Decoding of image {qoi_filename} failed at indexes {np.where(img_decoded != orig_img)[0]}")
                


if __name__ == '__main__':
    unittest.main()
