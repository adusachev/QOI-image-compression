import unittest

from qoi_decoder import decode_debug
from main import read_png
import numpy as np
import os
import pickle


class TestDebugDecoder(unittest.TestCase):
        
    def test1(self):
        
        files = ['R_video', '28_pixels', 'pixel_diff', 'doge']
        
        for filename in files:        
            # original image
            img, R, G, B = read_png(f'./png_images/{filename}.png')
            width, height = img.shape[0], img.shape[1]
        
            path_to_pickle_files = './data/'
            file = open(os.path.join(path_to_pickle_files, filename), 'rb')
            encoded_img = pickle.load(file)
            file.close()
            
            # qoi decoding (debug)
            R_decoded, G_decoded, B_decoded = decode_debug(encoded_img, width, height)
            
            self.assertTrue(np.all(R_decoded == R), f"Error in decoding {filename}, R channel wrong")
            self.assertTrue(np.all(G_decoded == G), f"Error in decoding {filename}, G channel wrong")
            self.assertTrue(np.all(B_decoded == B), f"Error in decoding {filename}, B channel wrong")
    
    

        
        