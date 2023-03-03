import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


# QOI_RUN = 0xc0  # 11xxxxxx
# QOI_DIFF_SMALL = 0x40  # 01xxxxxx
# QOI_DIFF_MED = 0x80  # 10xxxxxx
# QOI_RGB = 0xfe # 11111110
# EMPTY_BYTE = 0x0  # xxxxxxxx
QOI_RUN = np.array([1, 1, 0, 0, 0, 0, 0, 0])
QOI_DIFF_SMALL = np.array([0, 1, 0, 0, 0, 0, 0, 0])
QOI_DIFF_MED = np.array([1, 0, 0, 0, 0, 0, 0, 0])
QOI_RGB = np.array([1, 1, 1, 1, 1, 1, 1, 0])
EMPTY_BYTE = np.array([0, 0, 0, 0, 0, 0, 0, 0])




def encode_byte_part(value: int, bits_num: int, offset: int, byte: np.array) -> np.array:
    """
    _summary_

    :param value: _description_
    :param bits_num: _description_
    :param offset: _description_
    :param byte: _description_
    :return: _description_
    """
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
    :return: _description_
    """
    # byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
    byte = np.copy(QOI_RUN)

    byte = encode_byte_part(value=run_length, bits_num=6, offset=2, byte=byte)
    chunk = [byte]
    
    return chunk



def encode_diff_small(dr: int, dg: int, db: int) -> list:
    """_summary_

    :param dr: _description_
    :param dg: _description_
    :param db: _description_
    :return: _description_
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
    """_summary_

    :param dr: _description_
    :param dg: _description_
    :param db: _description_
    :return: _description_
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
    
    

def encode_rgb(R: int, G: int, B: int) -> list:
    """_summary_

    :param R: _description_
    :param G: _description_
    :param B: _description_
    :return: _description_
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
    """_summary_

    :param byte: _description_
    :param file: _description_
    """
    for byte in chunk:
        byte_dec = np.packbits(byte)[0]  # decimal representation of byte
        binary = bytes([byte_dec])  # convert decimal num (0, 256) to type bytes
        
        with open(file, 'ab') as f:
            f.write(binary)


