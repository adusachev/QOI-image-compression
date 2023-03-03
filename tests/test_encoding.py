import unittest

from qoi_encoder import *
import numpy as np
import os


class TestEncodeByte(unittest.TestCase):

    # def test_run_simple(self):
    #     byte = np.array([1, 1, 0, 0, 0, 0, 0, 0])  # empty byte with QOI_RUN tag
    #     offset = 2
    #     bits_num = 6
        
    #     run_length = 10
    #     byte = encode_byte_part(run_length, bits_num, offset, byte)
        
    #     # self.assertEqual(byte, [1, 1, 0, 0, 1, 0, 1, 0], "Should be 11001010")  # if type(byte) = List
    #     self.assertTrue(np.all(byte == np.array([1, 1, 0, 0, 1, 0, 1, 0])), "Should be 11001010")  # if type(byte) = np.array
        
        
    # def test_diff_small_simple(self):
    #     byte = np.array([0, 1, 0, 0, 0, 0, 0, 0])  # empty byte with QOI_DIFF_SMALL tag
    #     bits_num = 2
    #     offset = 2

    #     dr = -2  # absolute delta values
    #     dg = 1
    #     db = 0
    #     dr = dr + 2  # delta values with bias 2
    #     dg = dg + 2
    #     db = db + 2

    #     for d_channel in [dr, dg, db]:
    #         byte = encode_byte_part(d_channel, bits_num, offset, byte)
    #         offset += 2
        
    #     self.assertTrue(np.all(byte == np.array([0, 1, 0, 0, 1, 1, 1, 0])), "Should be 01001110")
        
        
        
    def test_encode_run(self):
        # encode
        run_length = 10
        chunk = encode_run(run_length)
        byte = chunk[0]
        
        self.assertTrue(np.all(byte == np.array([1, 1, 0, 0, 1, 0, 1, 0])), 
                        "Should be 11001010")
        
        # write to file
        file = './data/tmp.txt'
        f = open(file, 'w')  # create temporary empty file (or replace existing)
        f.close()
        
        write_chunk(chunk, file)
        file_size = os.path.getsize(file)
        self.assertEqual(file_size, 1, "File size should be 1 byte")
        
        
    def test_encode_rgb(self):
        # encode
        R = 59
        G = 8
        B = 147
        chunk = encode_rgb(R, G, B)
        rgb_tag, byte_R, byte_G, byte_B = chunk
        
        self.assertTrue(np.all(rgb_tag == np.array([1, 1, 1, 1, 1, 1, 1, 0])), 
                        f"Should be 11111110, but get {rgb_tag}")
        
        self.assertTrue(np.all(byte_R == np.array([0, 0, 1, 1, 1, 0, 1, 1])), 
                        f"Should be 00111011, but get {byte_R}")
        
        self.assertTrue(np.all(byte_G == np.array([0, 0, 0, 0, 1, 0, 0, 0])), 
                        f"Should be 00001000, but get {byte_G}")
        
        self.assertTrue(np.all(byte_B == np.array([1, 0, 0, 1, 0, 0, 1, 1])), 
                        f"Should be 10010011, but get {byte_B}")
        
        # write to file
        file = './data/tmp.txt'
        f = open(file, 'w')  # create temporary empty file (or replace existing)
        f.close()
        
        write_chunk(chunk, file)
        file_size = os.path.getsize(file)
        self.assertEqual(file_size, 4, "File size should be 4 bytes")
        
        
        



if __name__ == '__main__':
    unittest.main()
    
    
    
    
    