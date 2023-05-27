import unittest

from qoi_compress.qoi_decoder import decode_byte_part



class TestDecoder(unittest.TestCase):
    
    def test_decode_byte_part(self):
        
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



if __name__ == '__main__':
    unittest.main()
