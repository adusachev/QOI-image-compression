import unittest

from qoi_decoder import decode_debug
from main import read_png
import numpy as np
import os
import pickle
from qoi_decoder import decode_byte_part, decode_byte_part_0


class TestDecoder(unittest.TestCase):
    
    def test_decode_byte_part_2(self):
        
        # run test
        byte = 0b11001010
        run_length = decode_byte_part(byte, right_offset=0, bits_num=6)
        self.assertEqual(run_length, 0b001010, f"Expected {bin(0b001010)} but got {bin(run_length)}")
        
        # diff small test
        byte = 0b01111001
        dr = decode_byte_part(byte, right_offset=4, bits_num=2)
        self.assertEqual(dr, 0b11, f"Expected {bin(0b11)} but got {bin(dr)}")
        
        dg = decode_byte_part(byte, right_offset=2, bits_num=2)
        self.assertEqual(dg, 0b10, f"Expected {bin(0b10)} but got {bin(dg)}")
        
        db = decode_byte_part(byte, right_offset=0, bits_num=2)
        self.assertEqual(db, 0b01, f"Expected {bin(0b01)} but got {bin(db)}")
        
        # diff med test (byte1)
        byte = 0b10011011
        dg = decode_byte_part(byte, right_offset=0, bits_num=6)
        self.assertEqual(dg, 0b011011, f"Expected {0b011011} but got {bin(dg)}")
        
        # diff med test (byte2)
        byte = 0b11111100
        db_dg = decode_byte_part(byte, right_offset=0, bits_num=4)
        self.assertEqual(db_dg, 0b1100, f"Expected {bin(0b1100)} but got {bin(db_dg)}")
        
        dr_dg = decode_byte_part(byte, right_offset=4, bits_num=4)
        self.assertEqual(dr_dg, 0b1111, f"Expected {bin(0b1111)} but got {bin(dr_dg)}")
    
        
    def test_decode_byte_part_0(self):
        
        # run test
        byte = 0b11001010
        run_length = decode_byte_part_0(byte, part_length=6)
        self.assertEqual(run_length, 0b001010, f"Expected {bin(0b001010)} but got {bin(run_length)}")
        
        # diff small test
        byte = 0b01111001
        db = decode_byte_part_0(byte, part_length=2)
        self.assertEqual(db, 0b01, f"Expected {bin(0b01)} but got {bin(db)}")
        
        # diff med test (byte1)
        byte = 0b10011011
        dg = decode_byte_part_0(byte, part_length=6)
        self.assertEqual(dg, 0b011011, f"Expected {0b011011} but got {bin(dg)}")
        
        # diff med test (byte2)
        byte = 0b11111100
        db_dg = decode_byte_part_0(byte, part_length=4)
        self.assertEqual(db_dg, 0b1100, f"Expected {bin(0b1100)} but got {bin(db_dg)}")
        
    
    
        
        
        
        
        
    def test_debug_decoder(self):
        
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
    
    

        
        