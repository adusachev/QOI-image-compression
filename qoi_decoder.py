import numpy as np
from termcolor import colored
import os
import pickle
from qoi_encoder import Pixel
from main import read_png


def decode_byte_part_0(byte: int, part_length: int) -> int:
    """
    Return right part of byte of given length
     (i.e. slice byte[ 8 - part_length: ])
    """
    res = byte >> part_length

    res2 = res << part_length

    return (byte - res2)


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



def decode_diff_small(byte: int) -> tuple(int):
    """
    Extract dr, dg, db from diff small byte
    """
    dr = decode_byte_part(byte, right_offset=4, bits_num=2)
    dg = decode_byte_part(byte, right_offset=2, bits_num=2)
    db = decode_byte_part(byte, right_offset=0, bits_num=2)
    
    return dr, dg, db


def decode_diff_med(byte1: int, byte2: int) -> tuple(int):
    """
    Extract dr, dg, db from diff med bytes
    """
    dg = decode_byte_part(byte1, right_offset=0, bits_num=6)
    dr_dg = decode_byte_part(byte2, right_offset=4, bits_num=4)
    db_dg = decode_byte_part(byte2, right_offset=0, bits_num=4)
    
    dr = dr_dg + dg
    db = db_dg + dg
    
    return dr, dg, db



def decode(filename, width, height):
    """
    Algorithm of QOI decoder
    """
    
    with open('./data/tmp_v2.txt', 'rb') as f:
        qoi_bytes = f.read()
    
    n = width * height
    
    R_decoded = np.zeros(n)
    G_decoded = np.zeros(n)
    B_decoded = np.zeros(n)
    hash_array = [None for i in range(64)]
    
    m = len(encoded_img)
    
    pixel_counter = 0  # flatten image counter
    byte_counter = 0  # qoi bytes counter
    
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
            
            for i in range(run_length):
                R_decoded[pixel_counter + i] = prev_pixel.r
                G_decoded[pixel_counter + i] = prev_pixel.g
                B_decoded[pixel_counter + i] = prev_pixel.b
            pixel_counter += run_length
            continue
            
        elif tag == 0b00:
            tag_name = 'index'
            hash_index = decode_byte_part(byte, right_offset=0, bits_num=6)
            cur_pixel = hash_array[hash_index]
            byte_counter += 1
            
            if hash_array[hash_index] is None:
                raise ValueError("smth wrong with hashes")
        
        elif tag == 0b01:
            tag_name = 'diff_small'
            dr, dg, db = decode_diff_small(byte)
            cur_pixel = Pixel(prev_pixel.r + dr, prev_pixel.g + dg, prev_pixel.b + db)
            byte_counter += 1
            
        elif tag == 0b10:
            tag_name = 'diff_med'
            next_byte = qoi_bytes[i+1]
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
            
    
    



def decode_debug(encoded_img, width=None, height=None):
    
    n = width * height
    
    R_decoded = np.zeros(n)
    G_decoded = np.zeros(n)
    B_decoded = np.zeros(n)
    hash_array = [None for i in range(64)]
    
    m = len(encoded_img)
    
    j = 0  # flatten image counter
    
    for i in range(m):
        # get tag
        elem = encoded_img[i]
        tag = list(elem.keys())[0]

        if tag == 'QOI_RGB':
            r, g, b = encoded_img[i][tag]
            R_decoded[j] = r
            G_decoded[j] = g
            B_decoded[j] = b
            cur_pixel = Pixel(R_decoded[j], G_decoded[j], B_decoded[j])    # for hash array
            j += 1
        
        elif tag == 'QOI_RUN':
            run_length = encoded_img[i][tag]
            
            cur_pixel = Pixel(R_decoded[j-1], G_decoded[j-1], B_decoded[j-1])  # for hash array
            
            for t in range(run_length):
                R_decoded[j] = R_decoded[j-1]
                G_decoded[j] = G_decoded[j-1]
                B_decoded[j] = B_decoded[j-1]
                j += 1
                
        elif tag == 'QOI_DIFF_SMALL':
            dr, dg, db = encoded_img[i][tag]
            R_decoded[j] = R_decoded[j-1] + dr
            G_decoded[j] = G_decoded[j-1] + dg
            B_decoded[j] = B_decoded[j-1] + db
            cur_pixel = Pixel(R_decoded[j], G_decoded[j], B_decoded[j])    # for hash array
            j += 1
            
        elif tag == 'QOI_DIFF_MED':
            dg, dr_dg, db_dg = encoded_img[i][tag]
            dr = dr_dg + dg
            db = db_dg + dg
            R_decoded[j] = R_decoded[j-1] + dr
            G_decoded[j] = G_decoded[j-1] + dg
            B_decoded[j] = B_decoded[j-1] + db
            cur_pixel = Pixel(R_decoded[j], G_decoded[j], B_decoded[j])    # for hash array
            j += 1
        
        elif tag == 'QOI_INDEX':
            index = encoded_img[i][tag]  # pixel index in hash array
            assert hash_array[index] is not None, 'smth wrong with hash_array'
            pixel = hash_array[index]
            
            R_decoded[j] = pixel.r
            G_decoded[j] = pixel.g 
            B_decoded[j] = pixel.b
            j += 1
            continue
      
        hash_index = int(cur_pixel.hash_value())
        if hash_array[hash_index] is None:
            hash_array[hash_index] = cur_pixel
        
    return R_decoded, G_decoded, B_decoded



if __name__ == '__main__':
    
    filename = 'R_video'
    # filename = '28_pixels'
    # filename = 'pixel_diff'
    # filename = 'doge'
    
    img, R, G, B = read_png(f'./png_images/{filename}.png')
    width, height = img.shape[0], img.shape[1]
    
    path_to_pickle_files = './data/'
    file = open(os.path.join(path_to_pickle_files, filename), 'rb')
    encoded_img = pickle.load(file)
    file.close()

    
    R_decoded, G_decoded, B_decoded = decode_debug(encoded_img, width, height)
    
    print(R_decoded)
    print()
    
    print(R)
    
    assert np.all(R_decoded == R), 'R cahnnel wrong'
    assert np.all(G_decoded == G), 'G cahnnel wrong'
    assert np.all(B_decoded == B), 'B cahnnel wrong'
    
        





