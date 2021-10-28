# video2spectrogram

![supported versions](https://img.shields.io/badge/python-3.x-green.svg)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=dataset2database&video&to&sql&converter&url=https://github.com/alexandrosstergiou/dataset2database&hashtags=VideoConverter)
----------------------
About
----------------------

This package is meant to automate the process of extracting audio files from videos and saving the plots computed from these audio frequencies in the Mel scale ([Sectrogram](https://en.wikipedia.org/wiki/Spectrogram)). Videos are processed in parallel with the audio extracted by `ffmpeg` stored in `.wav` files which are then used to create spectrograms stored as `.JPEG` and can be used by any audio-based method.

Currently supported video formats include `.mp4`,`mpeg-4`,`.avi`,`.wmv`. If you have a different extension, you can simply change the script to include them (in the `video2spectrogram/get_spectrogram.py`)

----------------------
Package requirements
----------------------
+ `librosa`
+ `numpy`
+ `matplotlib`

Make sure that the above packages are installed before running any functions.

**`ffmpeg`**: You will need to have installed `ffmpeg` in order to perform the audio extraction from the video files.

**Multiprocessing:** The code uses multiprocessing for improving speeds, thus the total time required for the conversion varies across different processors. The code has been tested on an AMD Ryzen 3950X with an average conversion time of 4 minutes for ~1K videos (with an average resolution of 480p and length of 5s.)


----------------------
Dataset structure
----------------------

The package assumes a fixed video dataset structure:

```
<dataset>    
  │
  └──<class 1>
  │     │
  │     │─── <video_1.mp4>
  │     │─── <video_2.mp4>
  │     │─── ...
  │    ...      
  │
  └───<class 2>
  │      │
  │      │─── <video_1.mp4>
  │      │─── <video_2.mp4>
  │      │─── ...
 ...    ...

```

----------------------
Usage
----------------------

The main code is at the `get_spectrograme.py` file. To run the convertor simply call the `convert` function with the base directory of the dataset and the destination directory for where to save the audio.
Additional arguments that can be used:
+ `verbose_lvl`: Integer for verbosity.
+ `save_wav`: Boolean to determine if the created wav files are to be stored and not deleted.
+ `ar`: Integer for the ffmpeg option for specifying the audio sampling frequency.
+ `res_h`: Integer for the height of the spectrogram image to be saved.
+ `res_w`: Integer for the width of the spectrogram image to be saved.
+ `dpi`: Integer for the display's dot's per inch. Needs to be set to avoid inconsistencies to the `res` argument.

```python
from video2spectrogram import convert
#or
from get_spectrogram import convert

convert(my_dataset_dir, my_target_dir)

```

-------------------------
Installation through git
-------------------------

Please make sure, Git is installed in your machine:
```
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/alexandrosstergiou/video2spectrogram.git
$ cd dataset2database
$ pip install .
```

You can then use it as any other package installed through pip.

-------------------------
Installation through pip
-------------------------

The latest stable release is also available for download through pip
```
$ pip install video2spectrogram
```
