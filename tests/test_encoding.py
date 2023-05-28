import unittest
import os
from pathlib import Path

from qoi_compress.qoi_encoder import *

BASE_DIR = Path(__file__).resolve().parent.parent

if not os.path.exists(BASE_DIR / "data"):
    os.mkdir(BASE_DIR / "data")


class TestEncodeChunk(unittest.TestCase):
        
    def test_encode_run(self):
        # encode
        run_length = 10
        chunk = encode_run(run_length)
        byte = chunk[0]
                
        self.assertEqual(byte, 0b11001010 - 1, 
                        f"Should be 0b11001010, but get {bin(byte)}")
        
        # write to file
        filename = str(BASE_DIR / "data/tmp.txt")
        
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
        
        self.assertEqual(byte, 0b01111001, 
                        f"Should be 0b01111001, but get {bin(byte)}")
        
        # write to file
        filename = str(BASE_DIR / "data/tmp.txt")
        
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
        
        self.assertEqual(byte1, 0b10011011, 
                        f"Should be 0b10011011, but get {bin(byte1)}")
        
        self.assertEqual(byte2, 0b11111100, 
                        f"Should be 0b11111100, but get {bin(byte2)}")
        
        # write to file
        filename = str(BASE_DIR / "data/tmp.txt")
        
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
        
        self.assertEqual(rgb_tag, 0b11111110, 
                        f"Should be 0b11111110, but get {bin(rgb_tag)}")
        
        self.assertEqual(byte_R, 0b00111011, 
                        f"Should be 00111011, but get {bin(byte_R)}")
        
        self.assertEqual(byte_G, 0b00001000,
                        f"Should be 00001000, but get {bin(byte_G)}")
        
        self.assertEqual(byte_B, 0b10010011, 
                        f"Should be 10010011, but get {bin(byte_B)}")
        
        # write to file
        filename = str(BASE_DIR / "data/tmp.txt")
        
        with open(filename, 'wb') as file:
            write_chunk(chunk, file)
        file_size = os.path.getsize(filename)
        self.assertEqual(file_size, 4, "File size should be 4 bytes")
        
        


if __name__ == '__main__':
    unittest.main()
    
    