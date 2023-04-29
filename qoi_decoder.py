import numpy as np
import os
from qoi_encoder import Pixel
from read_png import read_png
from typing import Tuple
import time



def decode_byte_part(byte: int, right_offset: int, bits_num: int) -> int:
    """
    Extract part of given legnth from a byte

    :param byte: single byte (0-255)
    :param right_offset: e.g. right_offset=4 if we want to extract 1011 from byte 1011xxxx 
    :param bits_num: number of bits in desired part of byte
    """
    byte = byte >> right_offset  # cut right part of byte of length "right_offset"
    res = byte >> bits_num  # cut right part of byte of length "bits_num"
    mask = res << bits_num  # add "bits_num" zeros to the end of "res"
    byte_part = (byte - mask) 
    return byte_part



def decode_diff_small(byte: int) -> Tuple[int, int, int]:
    """
    Extract dr, dg, db from diff small byte
    """
    dr = decode_byte_part(byte, right_offset=4, bits_num=2)
    dg = decode_byte_part(byte, right_offset=2, bits_num=2)
    db = decode_byte_part(byte, right_offset=0, bits_num=2)
    dr -= 2  # bias
    dg -= 2
    db -= 2
    
    return dr, dg, db


def decode_diff_med(byte1: int, byte2: int) -> Tuple[int, int, int]:
    """
    Extract dr, dg, db from diff med bytes
    """
    dg = decode_byte_part(byte1, right_offset=0, bits_num=6)
    dr_dg = decode_byte_part(byte2, right_offset=4, bits_num=4)
    db_dg = decode_byte_part(byte2, right_offset=0, bits_num=4)
    dg -= 32  # bias
    dr_dg -= 8
    db_dg -= 8
    dr = dr_dg + dg
    db = db_dg + dg
    
    return dr, dg, db



def read_qoi_header(qoi_bytes: bytes) -> Tuple[int, int, int, int]:
    """
    Read qoi header and return info about image
    """
    assert qoi_bytes[:4] == b'qoif', "There is no magic QOI bytes in the file header"
    
    width_bytes = qoi_bytes[4:8]
    height_bytes = qoi_bytes[8:12]
    channels = qoi_bytes[12]
    colorspace = qoi_bytes[13]
    
    width = int.from_bytes(width_bytes, byteorder='big')
    height = int.from_bytes(height_bytes, byteorder='big')
        
    return height, width, channels, colorspace





def decode(filename: str):
    """
    Algorithm of QOI decoder
    
    :return: 1) R_decoded, G_decoded, B_decoded - 1d arrays of pixels of each image channel 
             2) height, width - image size
    """
    
    with open(filename, 'rb') as f:
        qoi_bytes = f.read()
        
    height, width, _, _ = read_qoi_header(qoi_bytes)
    
    n = width * height
    
    R_decoded = np.zeros(n)
    G_decoded = np.zeros(n)
    B_decoded = np.zeros(n)
    hash_array = [None for i in range(64)]
    
    m = len(qoi_bytes)
    
    pixel_counter = 0  # flatten image counter
    byte_counter = 14  # qoi bytes counter, starts from 14 because qoi header takes 14 bytes
    
    cur_pixel = Pixel(0, 0, 0)
    
    while byte_counter != m:
        
        prev_pixel = cur_pixel
        
        byte = qoi_bytes[byte_counter]
        tag = byte >> 6  # first 2 numbers of byte (e.g. ab from abxxxxxx)
        
        if byte == 0b11111110:
            tag_name = 'rgb'
            cur_pixel = Pixel(qoi_bytes[byte_counter+1],
                              qoi_bytes[byte_counter+2], 
                              qoi_bytes[byte_counter+3])         
            byte_counter += 4
            
        elif tag == 0b11:
            tag_name = 'run'
            run_length = decode_byte_part(byte, right_offset=0, bits_num=6)
            run_length += 1  # bias
            for i in range(run_length):
                R_decoded[pixel_counter + i] = prev_pixel.r
                G_decoded[pixel_counter + i] = prev_pixel.g
                B_decoded[pixel_counter + i] = prev_pixel.b
            pixel_counter += run_length
            byte_counter += 1
            continue
            
        elif tag == 0b00:
            tag_name = 'index'
            hash_index = decode_byte_part(byte, right_offset=0, bits_num=6)
            cur_pixel = hash_array[hash_index]
            byte_counter += 1
            
            if hash_array[hash_index] is None:
                raise ValueError("smth wrong with hashes, it may be error in byte indexing")
        
        elif tag == 0b01:
            tag_name = 'diff_small'
            dr, dg, db = decode_diff_small(byte)
            cur_pixel = Pixel(prev_pixel.r + dr, prev_pixel.g + dg, prev_pixel.b + db)
            byte_counter += 1
            
        elif tag == 0b10:
            tag_name = 'diff_med'
            next_byte = qoi_bytes[byte_counter+1]
            dr, dg, db = decode_diff_med(byte, next_byte)
            cur_pixel = Pixel(prev_pixel.r + dr, prev_pixel.g + dg, prev_pixel.b + db)
            byte_counter += 2

        else:
            raise ValueError(f"Unknown tag value: {bin(tag)} in byte {bin(byte)}")
        
        hash_index = int(cur_pixel.hash_value())
        hash_array[hash_index] = cur_pixel
        
        R_decoded[pixel_counter] = cur_pixel.r
        G_decoded[pixel_counter] = cur_pixel.g
        B_decoded[pixel_counter] = cur_pixel.b
        pixel_counter += 1
        
    return R_decoded, G_decoded, B_decoded, height, width
            
    



def test_decode():
    # png_filename = './png_images/long_run.png'
    # png_filename = './png_images/R_video.png'
    # png_filename = './png_images/28_pixels.png'
    # png_filename = './png_images/doge.png'
    # png_filename = './png_images/huge_6k.png'
    png_filename = './png_images/pixel_diff.png'    
    
    qoi_filename = './data/tmp_v2.txt'
    
    img, R, G, B = read_png(png_filename)
    width, height = img.shape[0], img.shape[1]
    
    start_time = time.time()
    R_decoded, G_decoded, B_decoded = decode(qoi_filename, width, height)
    end_time = time.time()

    print(np.all(R_decoded == R), np.where(R_decoded != R)[0])
    print(np.all(G_decoded == G), np.where(G_decoded != G)[0])
    print(np.all(B_decoded == B), np.where(B_decoded != B)[0])

    print(f"Time elapsed: {end_time - start_time} sec")


if __name__ == '__main__':
    test_decode()
    
    
        





