import numpy as np
import os
import time
import sys
import glob
import librosa
import librosa.display
from matplotlib import pyplot as plt
import subprocess
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor as Pool
plt.rcParams.update({'figure.max_open_warning': 0})


'''
---  S T A R T  O F  F U N C T I O N  W A V _ W O R K E R ---
    [About]
        Worker function for audio grabbing from video files.
    [Args]
        - file_i: Tuple or list containing:
                  + A string for the directory in which the `.wav` file is to be saved in (first element).
                  + A string for the video file name from which the audio is to be extracted form (seccond element).
                  + A string or an integer for the audio smapling frequency (third element).
    [Returns]
        - None
'''
def wav_worker(file_i):
    dst_dir = file_i[0]
    ar = file_i[2]
    prec = file_i[3]
    file_i = file_i[1]

    # Only consider videos
    if (extension in file_i for extention in ['.mp4','mpeg-4','.avi','.wmv']):
        # Feedback message
        if (v_lvl>=2):
            print('[{:.2f}] videos2spectrogram:: process #{} is converting file: {}'.format(prec,multiprocessing.current_process().name,file_i))
        sys.stdout.flush()
    else:
        if (v_lvl>=1):
            print('[{:.2f}] videos2spectrogram:: process #{} no video file found: {}'.format(prec, multiprocessing.current_process().name,file_i))
        return

    # Name without extension
    # Get file without extension
    name, ext = os.path.splitext(file_i)
    name = os.path.join(*(name.split(os.path.sep)[1:]))

    # Create destination directory for video
    dst_directory = os.path.join(dst_dir, name)
    dst_file = os.path.join(dst_directory,'audio.wav')
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)
    try:
        os.system('ffmpeg -y -i {} -acodec pcm_s16le -ar {} {}'.format(repr(file_i), ar, repr(dst_file)))
    except:
        if (v_lvl>=1):
            print('[{:.2f}] videos2spectrogram:: process #{} run to an Exception:'.format(prec, multiprocessing.current_process().name))
            print(dst_directory_path)
        return
'''
---  E N D  O F  F U N C T I O N  W A V _ W O R K E R ---
'''



'''
---  S T A R T  O F  F U N C T I O N  S P E C T O G R A M _ W O R K E R ---
    [About]
        Worker function for converting audion (.wav) files to spectrograms and saving them as .jpg images.
    [Args]
        - wav_file: Tuple or list containing:
                  + A boolean that determines if the .wav file is to be kept.
                  + A string for the .wav filepath.
    [Returns]
        - None
'''
def spectrogram_worker(wav_file):
    keep_file = wav_file[0]
    cm = wav_file[2]
    dpi = wav_file[3]
    prec = wav_file[4]
    wav_file = wav_file[1]

    # Use same naming as the .wav file
    name, ext = os.path.splitext(wav_file)
    name += '.jpg'
    (sig, rate) = librosa.load(wav_file, sr=None, mono=True,  dtype=np.float32)

    plt.specgram(sig, Fs=rate,cmap=cm)
    plt.axis('off')
    plt.savefig(name,bbox_inches='tight',pad_inches=0,format='jpeg',dpi=dpi)
    print('[{:.2f}] videos2spectrogram:: process #{} saved spectrogram in file: {}'.format(prec, multiprocessing.current_process().name,name))
    if not keep_file:
        os.remove(wav_file)
    return
'''
---  E N D  O F  F U N C T I O N  S P E C T O G R A M _ W O R K E R ---
'''



'''
---  S T A R T  O F  F U N C T I O N  C O N V E R T  ---
    [About]
        Main function for creating spectrograms from audio in videos.
    [Args]
        - base_dir: String for the dataset directory.
        - dst_dir: String for the directory to save the audio files.
        - verbose_lvl: Integer for verbosity.
        - save_wav: Boolean to determine if the created wav files are to be stored and not deleted.
        - ar: Integer for the ffmpeg option for specifying the audio sampling frequency.
        - res_h: Integer for the height of the spectrogram image to be saved.
        - res_w: Integer for the width of the spectrogram image to be saved.
        - dpi: Integer for the display's dot's per inch. Needs to be set to avoid inconsistencies to the `res` argument.
    [Returns]
        - None
'''
def convert(base_dir,dst_dir,verbose_lvl=2,save_wav=True,ar=16000,colormap='binary',res_h=300,res_w=600,dpi=100):
    start = time.time()

    global v_lvl
    v_lvl = verbose_lvl

    #--- Extract files from folder following pattern
    files   = glob.glob(os.path.join(base_dir,"*/*.mp4"))+\
              glob.glob(os.path.join(base_dir,"*/*.mpeg-4"))+\
              glob.glob(os.path.join(base_dir,"*/*.avi"))+\
              glob.glob(os.path.join(base_dir,"*/*.wmv"))
    n_files = len(files)
    if (verbose_lvl>=1):
        print('video2spectrogram:: Number of files in folder: ', n_files)

    classes = len(os.listdir(base_dir))
    for i,c in enumerate(os.listdir(base_dir)):

        # --- AUDIO EXTRACTION IS DONE HERE
        base_files = glob.glob(os.path.join(base_dir,c)+"/*.mp4")+\
                     glob.glob(os.path.join(base_dir,c)+"/*.mpeg-4")+\
                     glob.glob(os.path.join(base_dir,c)+"/*.avi")+\
                     glob.glob(os.path.join(base_dir,c)+"/*.wmv")
        if (verbose_lvl>=2):
            print('video2spectrogram:: Converting {} with {} files'.format(c,len(base_files)))
        tmp = [[dst_dir,f,ar,float(i/classes)] for f in base_files]
        try:
            with Pool() as p1:
                p1.map(wav_worker, tmp)

        except KeyboardInterrupt:
            if (verbose_lvl>=1):
                print("video2spectrogram:: Caught KeyboardInterrupt, terminating")
            p1.terminate()
            p1.join()

        # --- MEL SPECTROGRAM IS DONE HERE
        dist_files = glob.glob(os.path.join(dst_dir,c)+"/*/*.wav")
        dist_files = [[save_wav,file,colormap,dpi,i/classes] for file in dist_files]

        # set image size in inches
        plt.rcParams["figure.figsize"] = (res_h/dpi, res_w/dpi)

        try:
            with Pool() as p2:
                p2.map(spectrogram_worker, dist_files)

        except KeyboardInterrupt:
            if (verbose_lvl>=1):
                print("video2spectrogram:: Caught KeyboardInterrupt, terminating")
            p2.terminate()
            p2.join()

    end = time.time()
    if (verbose_lvl>=1):
        print('video2spectrogram:: Conversion finished successfully in %d secs' %(end-start))
'''
---  E N D  O F  F U N C T I O N  C O N V E R T  ---
'''
