import time
import numpy as np

QOI_RUN = 0xc0
QOI_RUN_ARRAY = np.array([1, 1, 0, 0, 0, 0, 0, 0])

N = 10000000

def func_1():
    for i in range(N):
        byte = np.unpackbits(np.array([QOI_RUN], dtype=np.uint8))
        
        
def func_2():
    for i in range(N):
        byte = np.array([1, 1, 0, 0, 0, 0, 0, 0])  
        
        
def func_3():
    for i in range(N):
        byte = np.copy(QOI_RUN_ARRAY)



start_time = time.time()
func_1()
end_time = time.time()
print("--- func 1: %s seconds ---" % (end_time - start_time))

start_time = time.time()
func_2()
end_time = time.time()
print("--- func 2: %s seconds ---" % (end_time - start_time))


start_time = time.time()
func_3()
end_time = time.time()
print("--- func 3: %s seconds ---" % (end_time - start_time))

















