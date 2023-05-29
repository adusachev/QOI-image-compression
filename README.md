
[![Build Status](https://github.com/adusachev/QOI-image-compression/actions/workflows/testing.yml/badge.svg)](https://github.com/adusachev/QOI-image-compression/actions/workflows/testing.yml)


# QOI image compression

Python implementation of QOI encoder and decoder

QOI format: https://qoiformat.org/

## Installation

```
git clone https://github.com/adusachev/QOI-image-compression.git
```

```
python setup.py install
```


## Usage


1) Encode: convert png image to qoi image
```python
from qoi_compress import qoi_encoder

png_file = "./png_images/doge.png"
qoi_file = "./qoi_images/doge.qoi"  # where to save qoi image

qoi_encoder.run_encoder(png_file, qoi_file)
```

2) Decode: import .qoi file into numpy array
```python
from qoi_compress import qoi_decoder

qoi_file = "./qoi_images/doge.qoi"

img_decoded, time_elapsed = qoi_encoder.run_decoder(qoi_file)
img_decoded
```

3) Test: encode image `png_file` and save it as `qoi_file`, then decode `qoi_file` and compare decoded qoi image with original png image
```python
from qoi_compress.main import run_single_experiment

png_file = "./png_images/doge.png"
qoi_file = "./qoi_images/doge.qoi"

run_single_experiment(png_file, qoi_file)
```


## Benchmarks

| Image size | Encoding time | Decoding time | Compression ratio |
| ---------- | ------------- | ------------- | ----------------- |
| 460x460    | 0.7 sec       | 0.3 sec       | 2.2               |
| 1920x1080  | 5.5 sec       | 2.5 sec       | 2.56              |
| 3840x2400  | 42 sec        | 19 sec        | 1.83              | 


## TODO

Add support for RGBA images
