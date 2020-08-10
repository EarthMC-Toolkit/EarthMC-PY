from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="EarthMC",
    version="1.0.3",
    description="Provides info on the EarthMC Minecraft server.",
    author="Owen77Stubbs",
    license="MIT",
    py_modules=["Nations", "Towns", "Players"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True
)

# Build dist using this: python setup.py sdist bdist_wheel
# Upload using this: python -m twine upload dist/*