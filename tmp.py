import time
import numpy as np
from termcolor import colored


QOI_RUN = 0xc0
QOI_RUN_ARRAY = np.array([1, 1, 0, 0, 0, 0, 0, 0])

# N = 10000

# def func_1():
#     for i in range(N):
#         byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
        
        
# def func_2():
#     for i in range(N):
#         byte = np.array([1, 1, 0, 0, 0, 0, 0, 0])  
        
        
# def func_3():
#     for i in range(N):
#         byte = np.copy(QOI_RUN_ARRAY)



# start_time = time.time()
# func_1()
# end_time = time.time()
# print("--- func 1: %s seconds ---" % (end_time - start_time))

# start_time = time.time()
# func_2()
# end_time = time.time()
# print("--- func 2: %s seconds ---" % (end_time - start_time))


# start_time = time.time()
# func_3()
# end_time = time.time()
# print("--- func 3: %s seconds ---" % (end_time - start_time))




# print(colored('hello', 'magenta'), colored('world', 'green'))







def encode_byte_part_1(value: int, bits_num: int, offset: int, byte: np.array) -> np.array:
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




def encode_run_1(run_length: int) -> list:
    """
    Encode QOI_RUN chunk

    :param run_length: run-length repeating the previous pixel
    :return: list of bytes encoding QOI_RUN chunk (here list of one byte, byte is np.array of length 8)
    """
    # byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
    byte = np.copy(QOI_RUN_ARRAY)

    byte = encode_byte_part_1(value=run_length, bits_num=6, offset=2, byte=byte)
    chunk = [byte]
    
    return chunk



def encode_byte_part_2(value: int, bits_num: int, right_offset: int, byte: int) -> int:
    """
    Write value to a part of byte

    :param value: decimal value to encode (0-255)
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





def encode_run_2(run_length: int) -> list:
    """
    Encode QOI_RUN chunk

    :param run_length: run-length repeating the previous pixel (0-63)
    :return: list of bytes encoding QOI_RUN chunk (here list of one byte, byte is np.array of length 8)
    """
    byte = QOI_RUN
    byte = encode_byte_part_2(value=run_length, bits_num=6, right_offset=0, byte=byte)
    chunk = [byte]
    
    return chunk






start_time = time.time()
for i in range(100000):
    chunk =  encode_run_1(20)
end_time = time.time()
    
print("--- encode_run_1: %s seconds ---" % (end_time - start_time))
    


start_time = time.time()
for i in range(100000):
    chunk =  encode_run_2(20)
end_time = time.time()
    
print("--- encode_run_2: %s seconds ---" % (end_time - start_time))

