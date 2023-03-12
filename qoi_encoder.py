import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from main import read_png
from termcolor import colored



# QOI_RUN = 0xc0  # 11xxxxxx
# QOI_DIFF_SMALL = 0x40  # 01xxxxxx
# QOI_DIFF_MED = 0x80  # 10xxxxxx
# QOI_RGB = 0xfe # 11111110
# EMPTY_BYTE = 0x0  # xxxxxxxx
QOI_RUN = np.array([1, 1, 0, 0, 0, 0, 0, 0])
QOI_DIFF_SMALL = np.array([0, 1, 0, 0, 0, 0, 0, 0])
QOI_DIFF_MED = np.array([1, 0, 0, 0, 0, 0, 0, 0])
QOI_INDEX = np.array([0, 0, 0, 0, 0, 0, 0, 0])
QOI_RGB = np.array([1, 1, 1, 1, 1, 1, 1, 0])
EMPTY_BYTE = np.array([0, 0, 0, 0, 0, 0, 0, 0])




def encode_byte_part(value: int, bits_num: int, offset: int, byte: np.array) -> np.array:
    """
    Write value to a part of byte

    :param value: decimal value to encode (0-255)
    :param bits_num: number of bits, needed to encode value (1-8)
    :param offset: bit offset (e.g. the binary value 101 written in byte 00000000 with offset=2 will give 00101000)  
    :param byte: the byte in which our value will be written (byte is np.array of length 8)
    :return: byte with written value
    """
    assert 0 <= value <= (2**bits_num), f"{value} is too large to be written in {bits_num} bits"
    assert (offset + bits_num) <= 8, \
        f"{bits_num} bits with offset {offset} can't be paced in single byte"
    
    value_encoded = [int(i) for i in f"{{0:0{bits_num}b}}".format(value)]
    assert len(value_encoded) == bits_num
    
    byte[offset : offset + bits_num] = value_encoded
    
    return byte




def encode_run(run_length: int) -> list:
    """
    Encode QOI_RUN chunk

    :param run_length: run-length repeating the previous pixel
    :return: list of bytes encoding QOI_RUN chunk (here list of one byte, byte is np.array of length 8)
    """
    # byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
    byte = np.copy(QOI_RUN)

    byte = encode_byte_part(value=run_length, bits_num=6, offset=2, byte=byte)
    chunk = [byte]
    
    return chunk



def encode_diff_small(dr: int, dg: int, db: int) -> list:
    """
    Encode QOI_DIFF_SMALL chunk

    :param dr: red channel difference from the previous pixel
    :param dg: green channel difference from the previous pixel
    :param db: blue channel difference from the previous pixel
    :return: list of bytes encoding QOI_DIFF_SMALL chunk (here list of one byte, byte is np.array of length 8)
    """
    assert (-2 <= dr <= 1) and (-2 <= dg <= 1) and (-2 <= db <= 1), \
        f"one of the values dr={dr}, dg={dg}, db={db} does not lie in the range [-2, 1]"
        
    # byte = np.unpackbits(np.array([QOI_DIFF_SMALL], dtype=np.uint8))
    byte = np.copy(QOI_DIFF_SMALL)
    offset = 2
    for d_channel in [dr, dg, db]:
        d_channel += 2  # values are stored with a bias of 2
        byte = encode_byte_part(value=d_channel, bits_num=2, offset=offset, byte=byte)
        offset += 2

    chunk = [byte]
    return chunk



def encode_diff_med(dr: int, dg: int, db: int) -> list:
    """
    Encode QOI_DIFF_MED chunk

    :param dr: red channel difference from the previous pixel
    :param dg: green channel difference from the previous pixel
    :param db: blue channel difference from the previous pixel
    :return: list of bytes encoding QOI_DIFF_MED chunk (here list of two bytes, each byte is np.array of length 8)
    """
    dr_dg = dr - dg
    db_dg = db - dg
    assert -32 <= dg <= 31, f"value dg={dg} does not lie in the range [-32, 31]"
    assert (-8 <= dr_dg <= 7) and (-8 <= db_dg <= 7), \
        f"values (dr-dg)={dr_dg}, (db-dg)={db_dg} does not lie in the range [-8, 7]"
    
    # Values are stored with a bias of 32 for the green channel 
    # and a bias of 8 for the red and blue channel:
    dg += 32
    dr_dg += 8
    db_dg += 8
    
    # byte1 = np.unpackbits(np.array([QOI_DIFF_MED], dtype=np.uint8))
    byte1 = np.copy(QOI_DIFF_MED)
    byte1 = encode_byte_part(value=dg, bits_num=6, offset=2, byte=byte1)
    
    # byte2 = np.unpackbits(np.array([EMPTY_BYTE], dtype=np.uint8))
    byte2 = np.copy(EMPTY_BYTE)
    byte2 = encode_byte_part(value=dr_dg, bits_num=4, offset=0, byte=byte2)
    byte2 = encode_byte_part(value=db_dg, bits_num=4, offset=4, byte=byte2)

    chunk = [byte1, byte2]    
    return chunk
    
    
def hash(r: int, g: int, b: int) -> int:
    """
    Hash function for QOI_INDEX
    """
    return (r * 3 + g * 5 + b * 7) % 64
    
    
def encode_index(hash_index: int) -> list:
    """
    Encode QOI_INDEX chunk

    :param run_length: run-length repeating the previous pixel
    :return: list of bytes encoding QOI_RUN chunk (here list of one byte, byte is np.array of length 8)
    """
    byte = np.copy(QOI_INDEX)

    byte = encode_byte_part(value=hash_index, bits_num=6, offset=2, byte=byte)
    chunk = [byte]
    
    return chunk
    

def encode_rgb(R: int, G: int, B: int) -> list:
    """
    Encode QOI_RGB chunk

    :param R: 8-bit red channel value
    :param G: 8-bit green channel value
    :param B: 8-bit blue channel value
    :return: list of bytes encoding QOI_RGB chunk (here list of four bytes, each byte is np.array of length 8)
    """
    # byte1 = np.unpackbits(np.array([QOI_RGB], dtype=np.uint8))
    byte1 = np.copy(QOI_RGB)
    chunk = [byte1]

    for channel in [R, G, B]:
        # byte = np.unpackbits(np.array([EMPTY_BYTE], dtype=np.uint8))
        byte = np.copy(EMPTY_BYTE)
        byte = encode_byte_part(value=channel, bits_num=8, offset=0, byte=byte)
        chunk.append(byte)
    
    return chunk

    

def write_chunk(chunk: list, file: str) -> None:
    """
    Writes bytes from single chunk to file

    :param chunk: list of bytes (each byte is np.array of length 8)
    :param file: path to file
    """
    for byte in chunk:
        byte_dec = np.packbits(byte)[0]  # decimal representation of byte
        binary = bytes([byte_dec])  # convert decimal num (0, 256) to type bytes
        
        with open(file, 'ab') as f:
            f.write(binary)




def encode_png_debug(R, G, B):
    
    QOI_RUN = False
    QOI_DIFF_SMALL = False
    QOI_DIFF_MED = False
    QOI_INDEX = False
    QOI_RGB = False

    n = len(R)
    
    hash_array = [None for i in range(64)]

    encoded_img = []
    # rgb_elem = {'QOI_RGB': [R[0], G[0], B[0]]}
    # hash_index = hash(R[0], G[0], B[0])
    # encoded_img.append(rgb_elem)

    run_length = 0

    for i in range(n):
        cur_pixel = [ R[i], G[i], B[i] ]
        
        if i == 0:
            prev_pixel = [0, 0, 255]
        else:
            prev_pixel = [ R[i-1], G[i-1], B[i-1] ]
        
        if cur_pixel == prev_pixel:
            QOI_RUN = True
            run_length += 1
            continue
        elif QOI_RUN:
            run_elem = {'QOI_RUN': run_length}
            encoded_img.append(run_elem)
            run_length = 0
            QOI_RUN = False
        
        
        dr = R[i] - R[i-1]
        dg = G[i] - G[i-1]
        db = B[i] - B[i-1]
        # print(dr, dg, db)
        
        hash_index = hash(R[i], G[i], B[i])
        
        if hash_array[hash_index] == cur_pixel:
            index_elem = {'QOI_INDEX': hash_index}
            encoded_img.append(index_elem)
            continue
        elif hash_array[hash_index] is None:
            hash_array[hash_index] = cur_pixel
                    
        # (!) более сильное условие, чем последующее (его проверка должна илти первой)
        if (-2 <= dr <= 1) and (-2 <= dg <= 1) and (-2 <= db <= 1):
            small_diff_elem = {'QOI_DIFF_SMALL': [dr, dg, db]}
            encoded_img.append(small_diff_elem)
            continue
        
        if (-32 <= dg <= 31) and (-8 <= (dr-dg) <= 7) and (-8 <= (db-dg) <= 7):
            med_diff_elem = {'QOI_DIFF_MED': [dg, (dr-dg), (db-dg)]}
            encoded_img.append(med_diff_elem)
            continue
            
        # else:
        rgb_elem = {'QOI_RGB': [R[i], G[i], B[i]]}
        encoded_img.append(rgb_elem)
        

    # last run processing
    if QOI_RUN:
        run_elem = {'QOI_RUN': run_length}
        encoded_img.append(run_elem)
        run_length = 0
        QOI_RUN = False
        
    return encoded_img


    



if __name__ == '__main__':
    _, R, G, B = read_png('./png_images/R_video.png')
    
    encoded_img = encode_png_debug(R, G, B)
    
    
    print('------------------------')
    tag_colors = {'QOI_RUN': 'white', 
                  'QOI_DIFF_SMALL': 'light_green', 
                  'QOI_DIFF_MED': 'green', 'QOI_INDEX': 'light_yellow',
                  'QOI_RGB': 'magenta'}
    
    for elem in encoded_img:
        tag = list(elem.keys())[0]
        color = tag_colors[tag]
        print(colored(f'{elem}', color))
    