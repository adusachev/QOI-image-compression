import os
import io
import time
from pathlib import Path
from typing import List, Tuple, Optional
from enum import Enum
import numpy as np
from qoi_compress.read_png import read_png
from qoi_compress.setup_logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ChunkType(int, Enum):
    """Tags for qoi chuncks"""
    QOI_RUN = 0b11000000
    QOI_DIFF_SMALL = 0b01000000
    QOI_DIFF_MED = 0b10000000
    QOI_INDEX = 0b00000000
    QOI_RGB = 0b11111110
    EMPTY_BYTE = 0b00000000
    
    
class MagicBytes(int, Enum):
    """Magic bytes for qoi file header"""
    MAGIC_Q = 0b01110001
    MAGIC_O = 0b01101111
    MAGIC_I = 0b01101001
    MAGIC_F = 0b01100110
    FILE_END_0 = 0b00000000
    FILE_END_1 = 0b00000001


class Pixel:
    """
    Class to store pixel channels values
    """
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b
        
    def __eq__(self, other):
        return (self.r == other.r) and (self.g == other.g) and (self.b == other.b)
        
    def hash_value(self) -> int:
        """Hash function for QOI_INDEX"""
        return (self.r * 3 + self.g * 5 + self.b * 7) % 64
        # return (self.r * 3 + self.g * 5 + self.b * 7 + 255 * 11) % 64  # to compare



def encode_byte_part(value: int, bits_num: int, right_offset: int, byte: int) -> int:
    """
    Write value to a part of byte

    :param value: value to encode (0-255)
    :param bits_num: number of bits, needed to encode value (1-8)
    :param right_offset: bit offset 
     (e.g. the binary value 101 written in byte 00000000 with right_offset=2 will give 00010100) 
    :param byte: the byte in which our value will be written
    :return: byte with written value
    """
    assert 0 <= value <= (2**bits_num), f"{value} is too large to be written in {bits_num} bits"
    assert (right_offset + bits_num) <= 8, \
        f"{bits_num} bits with right offset {right_offset} can't be placed in single byte"
    
    value_encoded = value << right_offset  # shift "value" left (regarding to 0b0) by "right_offset" bits
    byte += value_encoded
    
    return byte



def encode_run(run_length: int) -> List[int]:
    """
    Encode QOI_RUN chunk

    :param run_length: run-length repeating the previous pixel (1-62)
    :return: list of bytes encoding QOI_RUN chunk (here list of one byte, byte is int)
    """
    byte = ChunkType.QOI_RUN.value
    run_length -= 1  # run-length is stored with a bias of -1 (i.e. values are 0-61)
    byte = encode_byte_part(value=run_length, bits_num=6, right_offset=0, byte=byte)
    chunk = [byte]
    
    return chunk



def encode_diff_small(dr: int, dg: int, db: int) -> List[int]:
    """
    Encode QOI_DIFF_SMALL chunk

    :param dr: red channel difference from the previous pixel
    :param dg: green channel difference from the previous pixel
    :param db: blue channel difference from the previous pixel
    :return: list of bytes encoding QOI_DIFF_SMALL chunk
    """
    assert (-2 <= dr <= 1) and (-2 <= dg <= 1) and (-2 <= db <= 1), \
        f"one of the values dr={dr}, dg={dg}, db={db} does not lie in the range [-2, 1]"
        
    byte = ChunkType.QOI_DIFF_SMALL.value
    right_offset = 4
    for d_channel in [dr, dg, db]:
        d_channel += 2  # values are stored with a bias of 2
        byte = encode_byte_part(value=d_channel, bits_num=2, right_offset=right_offset, byte=byte)
        right_offset -= 2

    chunk = [byte]
    return chunk



def encode_diff_med(dr: int, dg: int, db: int) -> List[int]:
    """
    Encode QOI_DIFF_MED chunk

    :param dr: red channel difference from the previous pixel
    :param dg: green channel difference from the previous pixel
    :param db: blue channel difference from the previous pixel
    :return: list of bytes encoding QOI_DIFF_MED chunk (here list of two ints)
    """
    dr_dg = dr - dg
    db_dg = db - dg
    assert -32 <= dg <= 31, f"value dg={dg} does not lie in the range [-32, 31]"
    assert (-8 <= dr_dg <= 7) and (-8 <= db_dg <= 7), \
        f"values (dr-dg)={dr_dg}, (db-dg)={db_dg} does not lie in the range [-8, 7]"
    
    # Values are stored with a bias of 32 for the green channel 
    #  and a bias of 8 for the red and blue channel:
    dg += 32
    dr_dg += 8
    db_dg += 8
    
    byte1 = ChunkType.QOI_DIFF_MED.value
    byte1 = encode_byte_part(value=dg, bits_num=6, right_offset=0, byte=byte1)
    
    byte2 = ChunkType.EMPTY_BYTE.value
    byte2 = encode_byte_part(value=dr_dg, bits_num=4, right_offset=4, byte=byte2)
    byte2 = encode_byte_part(value=db_dg, bits_num=4, right_offset=0, byte=byte2)

    chunk = [byte1, byte2]    
    return chunk
    
    

def encode_index(hash_index: int) -> List[int]:
    """
    Encode QOI_INDEX chunk

    :param hash_index: hash value of the pixel
    :return: list of bytes encoding QOI_INDEX chunk
    """
    byte = ChunkType.QOI_INDEX.value

    byte = encode_byte_part(value=hash_index, bits_num=6, right_offset=0, byte=byte)
    chunk = [byte]
    
    return chunk
    


def encode_rgb(r_value: int, g_value: int, b_value: int) -> List[int]:
    """
    Encode QOI_RGB chunk

    :param R: 8-bit red channel value
    :param G: 8-bit green channel value
    :param B: 8-bit blue channel value
    :return: list of bytes encoding QOI_RGB chunk
    """
    byte1 = ChunkType.QOI_RGB.value
    chunk = [byte1]

    for channel in [r_value, g_value, b_value]:
        byte = ChunkType.EMPTY_BYTE.value
        byte = encode_byte_part(value=channel, bits_num=8, right_offset=0, byte=byte)
        chunk.append(byte)
    
    return chunk

    

def write_chunk(chunk: List[int], file_content: io.BufferedWriter) -> None:
    """
    Writes bytes from single chunk to file

    :param chunk: list of bytes
    :param file: buffered binary stream of file
    """
    for byte_val in chunk:
        val_binary = byte_val.to_bytes(length=1, byteorder='big')
        file_content.write(val_binary)



def write_qoi_header(image: np.ndarray, file_content: io.BufferedWriter) -> None:
    """
    Write qoi header bytes to file

    :param image: input image
    :param f: buffered binary stream of file
    """
    height, width, channels = image.shape
    
    channels = int(channels)
    colorspace = 0  # TODO
    magic_chunk = [MagicBytes.MAGIC_Q.value, MagicBytes.MAGIC_O.value, 
                   MagicBytes.MAGIC_I.value, MagicBytes.MAGIC_F.value]
    
    height_binary = height.to_bytes(length=4, byteorder='big')
    width_binary = width.to_bytes(length=4, byteorder='big')
    
    write_chunk(magic_chunk, file_content)
    file_content.write(width_binary)
    file_content.write(height_binary)
    file_content.write(channels.to_bytes(length=1, byteorder='big'))
    file_content.write(colorspace.to_bytes(length=1, byteorder='big'))
    
    

def write_qoi_end(file_content: io.BufferedWriter) -> None:
    """
    Write qoi end bytes to file
    """
    end_chunk = [MagicBytes.FILE_END_0.value for i in range(7)]
    end_chunk.append(MagicBytes.FILE_END_1.value)
    
    write_chunk(end_chunk, file_content)




def encode(R: List[int], 
           G: List[int], 
           B: List[int], 
           file: io.BufferedWriter) -> None:
    """
    QOI encoder algorithm

    :param R: list with R-channel values
    :param G: list with G-channel values
    :param B: list with B-channel values
    :param file: encoded bytes
    """
    is_run = False
    run_length = 0
    hash_array = [Pixel(0, 0, 0) for i in range(64)]
    cur_pixel = Pixel(0, 0, 0)
    n = len(R)

    for i in range(n):
        prev_pixel = cur_pixel
        cur_pixel = Pixel(R[i], G[i], B[i])
        
        if cur_pixel == prev_pixel:
            is_run = True
            run_length += 1
            if run_length == 62:
                run_chunk = encode_run(run_length)
                write_chunk(run_chunk, file)
                run_length = 0
                is_run = False        
            continue
        elif is_run:
            run_chunk = encode_run(run_length)
            write_chunk(run_chunk, file)
            run_length = 0
            is_run = False
        
        hash_index = cur_pixel.hash_value()
        
        if hash_array[hash_index] == Pixel(0, 0, 0):
            hash_array[hash_index] = cur_pixel
            
        elif hash_array[hash_index] == cur_pixel:
            index_chunk = encode_index(hash_index)
            write_chunk(index_chunk, file)
            continue
        else:
            hash_array[hash_index] = cur_pixel  # update hash_index array 
            
        dr = cur_pixel.r - prev_pixel.r
        dg = cur_pixel.g - prev_pixel.g
        db = cur_pixel.b - prev_pixel.b
                    
        if (-2 <= dr <= 1) and (-2 <= dg <= 1) and (-2 <= db <= 1):
            diff_small_chunk = encode_diff_small(dr, dg, db)
            write_chunk(diff_small_chunk, file)
            continue
        
        if (-32 <= dg <= 31) and (-8 <= (dr-dg) <= 7) and (-8 <= (db-dg) <= 7):
            diff_med_chunk = encode_diff_med(dr, dg, db)
            write_chunk(diff_med_chunk, file)
            continue
            
        rgb_chunk = encode_rgb(cur_pixel.r, cur_pixel.g, cur_pixel.b)
        write_chunk(rgb_chunk, file)

    # last run processing
    if is_run:
        run_chunk = encode_run(run_length)
        write_chunk(run_chunk, file)
        run_length = 0
        is_run = False
        
    write_qoi_end(file)
    



def run_encoder(png_filename: str, qoi_filename: Optional[str] = None) -> Tuple[str, float]:
    """
    Run qoi encode algorithm on image "png_filename"
    Save encoded qoi image as "qoi_filename"
    """
    if qoi_filename is None:
        name = Path(png_filename).stem
        qoi_filename = str(BASE_DIR / 'qoi_images' / f'{name}.qoi')
        
        if not os.path.exists(BASE_DIR / 'qoi_images'):
            os.mkdir(BASE_DIR / 'qoi_images')
    
    img, R, G, B = read_png(png_filename)
    
    # create empty qoi file with header (or replace existing)
    file = open(qoi_filename, 'wb')
    write_qoi_header(img, file)
    file.close()
    
    start_time = time.time()
    with open(qoi_filename, 'ab') as file:
        encode(R, G, B, file)
    end_time = time.time()
        
    time_elapsed = end_time - start_time
    logger.debug(f"Image encoded and saved as {qoi_filename}")
    logger.debug(f"Encoding time: {1000 * time_elapsed:.3f} ms")
        
    return qoi_filename, time_elapsed
    



if __name__ == '__main__':
    png_filename = str(BASE_DIR / "png_images/doge.png")
    
    qoi_filename, time_elapsed = run_encoder(png_filename)
