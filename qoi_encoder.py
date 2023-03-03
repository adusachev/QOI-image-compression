import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


QOI_RUN = 0xc0  # 11xxxxxx
QOI_DIFF_SMALL = 0x40  # 01xxxxxx
QOI_DIFF_MED = 0x80  # 10xxxxxx
QOI_RGB = 0xfe # 11111110

EMPTY_BYTE = 0x0  # xxxxxxxx




def encode_byte_part(value: int, bits_num: int, offset: int, byte: np.array) -> np.array:
    """
    _summary_

    :param value: _description_
    :param bits_num: _description_
    :param offset: _description_
    :param byte: _description_
    :return: _description_
    """
    assert 0 <= value <= 255, f"{value} is too large to be written in a single byte"
    assert 0 <= value <= (2**bits_num), f"{value} is too large to be written in {bits_num} bits"
    assert (offset + bits_num) <= 8, \
        f"{bits_num} bits with offset {offset} can't be paced in single byte"
    
    value_encoded = [int(i) for i in f"{{0:0{bits_num}b}}".format(value)]
    assert len(value_encoded) == bits_num
    
    byte[offset : offset + bits_num] = value_encoded
    
    return byte




def encode_run(run_length: int) -> list:
    """_summary_

    :param run_length: _description_
    """
    byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
    # byte = np.array([1, 1, 0, 0, 0, 0, 0, 0])  # or hardcode tag

    byte = encode_byte_part(value=run_length, bits_num=6, offset=2, byte=byte)
    chunk = [byte]
    
    return chunk



def encode_diff_small(dr: int, dg: int, db: int) -> list:
    """_summary_

    :param dr: _description_
    :param dg: _description_
    :param db: _description_
    :return:
    """
    byte = np.unpackbits(np.array([QOI_DIFF_SMALL], dtype=np.uint8))
    offset = 2
    for d_channel in [dr, dg, db]:
        d_channel += 2  # delta values with bias 2
        byte = encode_byte_part(value=d_channel, bits_num=2, offset=offset, byte=byte)
        offset += 2

    chunk = [byte]    
    return chunk



def encode_diff_med(dr: int, dg: int, db: int) -> list:
    """_summary_

    :param dr: _description_
    :param dg: _description_
    :param db: _description_
    :return:
    """
    byte1 = np.unpackbits(np.array([QOI_DIFF_MED], dtype=np.uint8))
    byte1 = encode_byte_part(value=dg, bits_num=6, offset=2, byte=byte1)
    
    byte2 = np.unpackbits(np.array([EMPTY_BYTE], dtype=np.uint8))
    byte2 = encode_byte_part(value=(dr-dg), bits_num=4, offset=0, byte=byte2)
    byte2 = encode_byte_part(value=(db-dg), bits_num=4, offset=4, byte=byte2)

    chunk = [byte1, byte2]    
    return chunk
    
    
    

def encode_rgb(R: int, G: int, B: int) -> list:
    """_summary_

    :param R: _description_
    :param G: _description_
    :param B: _description_
    :return: _description_
    """
    byte1 = np.unpackbits(np.array([QOI_RGB], dtype=np.uint8))
    chunk = [byte1]

    for channel in [R, G, B]:
        byte = np.unpackbits(np.array([EMPTY_BYTE], dtype=np.uint8))
        byte = encode_byte_part(value=channel, bits_num=8, offset=0, byte=byte)
        chunk.append(byte)
    
    return chunk



    

def write_chunk(chunk: list, file: str) -> None:
    """_summary_

    :param byte: _description_
    :param file: _description_
    """    
    for byte in chunk:
        byte_dec = np.packbits(byte)[0]  # decimal representation of byte
        binary = bytes([byte_dec])  # convert decimal num (0, 256) to type bytes
        
        with open(file, 'ab') as f:
            f.write(binary)




