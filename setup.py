from setuptools import setup

with open("README.md", "r") as fh:

    long_description = fh.read()

setup(name='video2spectrogram',
      version='0.1',
      description='Script for extracting audio and saving it in .WAV files and computing their Mel spectrogram and saving it in .JPEG file',
      url='https://github.com/alexandrosstergiou/video2spectrogram',
      author='Alexandros Stergiou',
      author_email='alexstergiou5@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['video2spectrogram'],
      zip_safe=False)
