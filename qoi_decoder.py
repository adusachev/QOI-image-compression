import numpy as np
from termcolor import colored
import os
import pickle












def decode_debug(encoded_img):
    
    width = 8  # должно записываться в файл (!)
    heigth = 8
    n = width * heigth
    
    R_decoded = np.zeros(n)
    G_decoded = np.zeros(n)
    B_decoded = np.zeros(n)
    
    m = len(encoded_img)
    
    j = 0  # image counter
    
    for i in range(m):
        # 1) get tag
        elem = encoded_img[i]
        tag = list(elem.keys())[0]

        if tag == 'QOI_RGB':
            r, g, b = encoded_img[i][tag]
            
            R_decoded[j] = r
            G_decoded[j] = g
            B_decoded[j] = b
            j += 1
            continue
        
        elif tag == 'QOI_RUN':
            run_length = encoded_img[i][tag]
            for t in range(run_length):
                R_decoded[j] = R_decoded[j-1]
                G_decoded[j] = G_decoded[j-1]
                B_decoded[j] = B_decoded[j-1]
                j += 1
        
        elif tag == 'QOI_INDEX':
            pass



if __name__ == '__main__':
    
    filename = 'R_video'
    path_to_pickle_files = './data/'
    file = open(os.path.join(path_to_pickle_files, filename), 'rb')
    encoded_img = pickle.load(file)
    file.close()

    
    
    





