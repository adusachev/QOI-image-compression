import unittest

from qoi_encoder import *
import numpy as np
import os


class TestEncodeChunk(unittest.TestCase):
        
        
    def test_encode_run(self):
        # encode
        run_length = 10
        chunk = encode_run(run_length)
        byte = chunk[0]
        
        self.assertTrue(np.all(byte == np.array([1, 1, 0, 0, 1, 0, 1, 0])), 
                        f"Should be 11001010, but get {byte}")
        
        # write to file
        filename = './data/tmp.txt'
        
        with open(filename, 'wb') as file:
            write_chunk(chunk, file)
        file_size = os.path.getsize(filename)
        self.assertEqual(file_size, 1, "File size should be 1 byte")
        
        
    def test_encode_diff_small(self):
        dr = 1
        dg = 0
        db = -1
        chunk = encode_diff_small(dr, dg, db)
        byte = chunk[0]
        
        self.assertTrue(np.all(byte == np.array([0, 1, 1, 1, 1, 0, 0, 1])), 
                        f"Should be 01111001, but get {byte}")
        
        # write to file
        filename = './data/tmp.txt'
        
        with open(filename, 'wb') as file:
            write_chunk(chunk, file)
        file_size = os.path.getsize(filename)
        self.assertEqual(file_size, 1, "File size should be 1 byte")
        
        
        
    def test_encode_diff_med(self):
        dr = 2
        dg = -5
        db = -1
        chunk = encode_diff_med(dr, dg, db)
        byte1, byte2 = chunk
        
        self.assertTrue(np.all(byte1 == np.array([1, 0, 0, 1, 1, 0, 1, 1])), 
                        f"Should be 10011011, but get {byte1}")
        
        self.assertTrue(np.all(byte2 == np.array([1, 1, 1, 1, 1, 1, 0, 0])), 
                        f"Should be 11111100, but get {byte2}")
        
        # write to file
        filename = './data/tmp.txt'
        
        with open(filename, 'wb') as file:
            write_chunk(chunk, file)
        file_size = os.path.getsize(filename)
        self.assertEqual(file_size, 2, "File size should be 2 bytes")
        
        
          
    
        
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
        filename = './data/tmp.txt'
        
        with open(filename, 'wb') as file:
            write_chunk(chunk, file)
        file_size = os.path.getsize(filename)
        self.assertEqual(file_size, 4, "File size should be 4 bytes")
        
        
        



if __name__ == '__main__':
    unittest.main()
    
    
    
    
    