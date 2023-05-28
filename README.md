
[![Build Status](https://github.com/adusachev/QOI-image-compression/actions/workflows/testing.yml/badge.svg)](https://github.com/adusachev/QOI-image-compression/actions/workflows/testing.yml)

# QOI image compression

Python implementation of QOI encoder and decoder

QOI format: https://qoiformat.org/


## Usage

**1) Encode single .png image and save .qoi image**

At the end of `qoi_encoder.py` enter path to .png image and run: 
```
python3 qoi_encoder.py
```


**2) Decode single .qoi image**

At the end of `qoi_decoder.py` enter path to .qoi image and run: 
```
python3 qoi_decoder.py
```


**3) Encode and decode all .png images in some directory, compare decoded .qoi image with original .png image**

At the end of `main.py` choose `dir_with_png` and uncomment line with `run_multiple_experiments(dir_with_png)`, then run:
```
python3 main.py
```

