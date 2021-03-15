import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import scipy
import numpy as np

# TODO tests functions below

def check_files(file_path):
    '''
    utility function to check that files exist and are >0 bytes
    '''
    try:
        assert os.path.exists(f_path), "Make sure that the file_path (input) is correct"
        assert os.stat(f_path).st_size > 0, "Make sure the file size is >0 bytes"
        res = True
    except AssertionError:
        res = False
    return res


def check_extension(file_path, ext=".png"):
    '''
    check whether a file has the required extension applicable to:( ".npy",".h5",".jpg",".png", ".txt", ".mp3", ".wav")
    '''
    good_extension = False
    if os.path(file_path).endswith(ext):
       good_extension = True
    return good_extension


def file_to_mel(f_path, dst_path, save=True):
    '''
    utility function to convert file to mel spectrogram
    '''
    input_path_validity = check_files(f_path)
    destination_path_validity = check_files(dst_path)

    assert input_path_validity and destination_path_validity == True, 'Issues with the filepaths, pls check with the function: check_files'
    # to refactor with regex
    dst_numpy_path = dst_path.replace(".wav",".npy").replace(".mp3",".npy")
   
   # takes f_path: file_path as input
    # returns the audio signal
    # and sample rate
    y, sr = librosa.load(librosa.util.example_audio_file())

    # takes y: the signal as input
    # sr : target sampling rate
    # returns the mel
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), fmax=8000)
    if save:
        plt.savefig(dst_path, S)
        np.save(S, dst_numpy_path)
    return S


def read_numpy_file(f_path):
    '''
    checks whether a file has the correct extension
    '''
    assert check_extension(file_path, ext=".npy") is True
    assert check_files(f_path) is True:
        return np.load(f_path)


def mel_to_sound(dst_sound_file_path, mel_spectogram, sample_rate, method = 'griffin_lim'):

    '''
    converts mel spectrogram (librosa object) to sound file with defined sample rate and 1 method:
    griffin_lim
    https://paperswithcode.com/method/griffin-lim-algorithm
    '''
    inverted_features = librosa.feature.inverse.mel_to_stft(mel_spectogram)
    audio_signal = librosa.griffinlim(inverted_features)
    scipy.io.wavfile.write(dst_sound_file_path, audio_signal, sample_rate)


if __name__ == '__main__':
    # TESTS to run
    test_file = ""
    test_dst_file = ""
    sample_rate = 8000

    check_files(test_file)
    check_extension(test_file)
    mel_spectrogram_plus_visuals = file_to_mel(f_path, dst_path,save=True)
    mel_spectrogram = file_to_mel(f_path, dst_path,save=False)
    read_numpy_file(f_path)
    mel_to_sound(test_dst_file, mel_spectogram, sample_rate, method = 'griffin_lim')
