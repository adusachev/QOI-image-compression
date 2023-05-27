from setuptools import setup, find_packages
from src import qoi_compress
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as fl:
    long_description = fl.read()
    
with open(os.path.join(here, "requirements.txt")) as fl:
    required = fl.read().splitlines()

setup(
    name="qoi_compress",
    package_dir={'': 'src'},
    version=qoi_compress.__version__,
    author="Aleksei Usachev",
    author_email="usachev.alexe@gmail.com",
    description=qoi_compress.__docs__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src', include=['qoi_compress*']),
    install_requires=required,
    keywords=['qoi', 'png', 'compression', 'image'],
    python_requires='>=3.8'
)
