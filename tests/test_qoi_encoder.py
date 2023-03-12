import unittest

from qoi_encoder import *
import numpy as np
import os


class TestDebugEncoder(unittest.TestCase):
        
    
    def test1(self):
        filename = 'pixel_diff.png'
        _, R, G, B = read_png(f'./png_images/{filename}')
    
        encoded_img = encode_png_debug(R, G, B)
        
        expected = [{'QOI_RGB': [140, 77, 251]},
                    {'QOI_DIFF_SMALL': [-2, 1, 0]},
                    {'QOI_RGB': [0, 0, 0]},
                    {'QOI_RUN': 1},
                    {'QOI_RGB': [140, 77, 252]},
                    {'QOI_DIFF_MED': [-5, 7, 4]}]
        
        self.assertEqual(encoded_img, expected, f"Error in encoding {filename}")
        
        
    def test2(self):
        filename = 'R_video.png'
        _, R, G, B = read_png(f'./png_images/{filename}')
    
        encoded_img = encode_png_debug(R, G, B)
        
        expected = [{'QOI_RGB': [140, 77, 251]}, {'QOI_RGB': [255, 255, 92]}, {'QOI_RUN': 4}, {'QOI_RGB': [59, 8, 147]}, {'QOI_RGB': [140, 77, 252]}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_DIFF_SMALL': [-2, 1, 0]}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_RUN': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_RUN': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 9}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_RUN': 1}, {'QOI_INDEX': 60}, {'QOI_RUN': 3}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_RUN': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 9}, {'QOI_INDEX': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 9}, {'QOI_DIFF_MED': [-5, 7, 4]}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}, {'QOI_INDEX': 2}, {'QOI_RUN': 2}, {'QOI_INDEX': 60}, {'QOI_INDEX': 30}]
        
        self.assertEqual(encoded_img, expected, f"Error in encoding {filename}")
        
        


if __name__ == '__main__':
    unittest.main()
    
    
    
    
    