# Build dist using this ----> py -m build
# Upload using this     ----> python -m twine upload dist/*

from os import path
from setuptools import setup, find_packages

# Read contents of README
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="EarthMC",
    version="3.4.2",
    description="Provides data on people, places and more on the EarthMC Minecraft server.",
    author="Owen3H",
    license="MIT",
    url="https://github.com/EarthMC-Toolkit/EarthMC-Py",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=False,
    install_requires=["requests", "cachetools"]
)