import numpy as np
from termcolor import colored
import os
import pickle
from qoi_encoder import Pixel
from main import read_png







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
    
        





