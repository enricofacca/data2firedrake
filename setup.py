import sys

from setuptools import setup
from setuptools import find_packages

if sys.version_info < (3, 6):
    print("Python 3.6 or higher required, please upgrade.")
    sys.exit(1)

version = "0.1"

p=find_packages('src')

setup(
    name="data2firedrake",
    description="Convert different data format to firedrake functions",
    version=version,
    author="Enrico Facca",
    license="MIT",
    packages=['data2firedrake'],
    package_dir={'':'src'}
)
