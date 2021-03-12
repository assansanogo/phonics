import pandas as pd
import os
import glob2
import datetime
from phonemes import Phonemes, Phonemizer
from tqdm import tqdm
from utils import df_multicores

tqdm.pandas()


output = "dataset/processed"
stats = f"{output}/stats"
report = os.path.join(stats, "report.csv")
meta_file = "dataset/raw/LJSpeech-1.1/metadata.csv"


def list_data_folders(dataset_folder = "dataset"):
    '''
    checks that the folder structure respects the following structure:
    dataset_folder
    |--- raw
    |--- processed
    
    '''
    folders = glob2.glob(f'./{dataset_folder}/*')
    assert len(folders) == 2
    assert folders == [f'./{dataset_folder}/processed', f'./{dataset_folder}/raw'], "please respect the folder structure described in the documentation"
    return True

def read_meta_datafile(meta_data_file, 
                    file_separator='|', 
                    file_header=None):
    '''
    reads the metadatafile (id, first version of the text, second version of the text)
    ex: 
    LJ001-0024|But the first Bible actually dated (which also was printed at Maintz by Peter Schoeffer in the year 1462)|But the first Bible actually dated (which also was printed at Maintz by Peter Schoeffer in the year fourteen sixty-two)
    '''
    if file_header is None:
        file_header = ["id", "text1", "text2"]

    if list_data_folders():
        # read csv file with args: metadata file name, separator, header
        df = pd.read_csv(meta_data_file, 
                        sep=file_separator,
                        names=file_header)
    return df

def file_statistics(meta_data_file, 
                    file_separator='|', 
                    file_header=None):
    '''
    returns simple file statistics (first number of files)
    TODO words frequencies
    TODO create a readme.md file to create metadata + phonemes report
    '''

    df = read_meta_datafile(meta_data_file, file_separator='|', file_header=None)
    df_n_columns = df.shape[1]
    df_n_rows = df.shape[0]

    os.makedirs(stats, exist_ok=True)
    with open(report, "w") as f:

        f.write(f" {str(datetime.datetime.now())},the raw dataset has {df_n_rows} lines and {df_n_columns} columns\n")

def phone_transform(
                    text_job,
                    header,
                    allowed_phonemes,
                    phonemizer):

    # in case the header is not specified it is given the value : ["file_ID","text1","text2"]
    if  header is None:
        header = ["file_ID","text1","text2"]

    
    try:
        # creates a phonemization job
        phonemization = phonemizer(
                                text=text_job, 
                                stress=True, 
                                n_jobs=1, 
                                language='en-us',
                                allowed_phonemes=allowed_phonemes)[0]
    except:
        # in case of failing save the phonemization with the value NONE
        phonemization = None
        print(text_job)
        pass

    return phonemization

def wrapped_phone_transform(x):
    phonemizer =  Phonemizer(language='eng-us',
                            stress=True,
                            n_jobs=1)
    phonemz = Phonemes()
    allowed_phonemes = phonemz.list_all_phonemes()
    return phone_transform(x, header=None,allowed_phonemes=allowed_phonemes, phonemizer=phonemizer)

def create_phonemes(accelerated = False):
    '''
    routine performing default transformation (text to phonemes)
    it outputs the results in the processed folder under the filename: raw_phonemes.csv
    '''

    df = read_meta_datafile(
        meta_data_file=meta_file, 
        file_separator='|', 
        file_header=None)

    if accelerated:
        # progressbar + multicore acceleration
        df["phonemes"] = df_multicores(
                                    df=df, 
                                    df_f_name='progress_apply', 
                                    subset=['text2'], 
                                    njobs=-1, 
                                    func=wrapped_phone_transform, axis=1)
    else:
        # progressbar while processing the phonemes 1K/min
        df["phonemes"] = df["text2"].progress_apply(lambda x:wrapped_phone_transform(x))
        df["phonemes"] = df["phonemes"].apply(lambda x: x[0]) 
    # save the processed dataframe to disk
    df.to_csv(f"{output}/raw_phonemes.csv", 
            sep ='|')

def test():
    file_statistics(
                    meta_data_file=meta_file, 
                    file_separator='|', 
                    file_header=None)

    phonemz = Phonemes()

    tot_phonemes = phonemz.list_all_phonemes()
    sound_phonemes = phonemz.list_sound_phonemes()
    tot_eng_phonemes = phonemz.list_all_english_phonemes()
    eng_phonemes = phonemz.list_english_phonemes()

    print(f"> There are: {len(tot_phonemes)} total phonemes (=including punctuation)")
    print(f"> There are: {len(sound_phonemes)} sound phonemes (=excluding punctuation)")
    print(f"> There are: {len(tot_eng_phonemes)} total english phonemes (=including punctuation)")
    print(f"> There are: {len(eng_phonemes)} english phonemes (=excluding punctuation)")


    current_phonemizer = Phonemizer(language='eng-us',
                            stress=True,
                            n_jobs=1)
    
    header = ["id", "text1", "text2"]

    df = read_meta_datafile(
                meta_data_file=meta_file, 
                file_separator='|', 
                file_header=header)

    text_job = df["text2"].values[0]

    text_job_phonemized = phone_transform(text_job=text_job,
                    header=None,
                    phonemizer=current_phonemizer,
                    allowed_phonemes=tot_phonemes)

    

    print(text_job_phonemized)

if __name__=='__main__':
    create_phonemes(accelerated=True)
    #df = pd.read_csv('dataset/processed/raw_phonemes.csv', sep='|')
    #print(df['phonemes'].apply(lambda x: str(x)))
    #print(df.head())

    
    
