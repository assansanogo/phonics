from phonemizer.phonemize import phonemize
from typing import Union

class Phonemizer:
    def __init__(
                self, 
                language: str, 
                stress: bool, 
                n_jobs=1,
                ):

        # phonemizer language
        self.language = language
        # phoonemizer jobs
        self.n_jobs = n_jobs
        # phonemizer stress/intonation
        self.with_stress = stress
    
    def _filter_string(
                        self, 
                        text: str, 
                        allowed_phonemes: list) -> str:

        # return the string convertible in phonemes
        return ''.join([c for c in text if c in allowed_phonemes])
    
    def filter_characters(
                        self, 
                        text: Union[str, list],
                        allowed_phonemes: list
                        ) -> Union[str, list]:

        # filter function working for strings or lists
        if isinstance(text, list):
            return [self._filter_string(t, allowed_phonemes) for t in text]
        
        elif isinstance(text, str):
            return self._filter_string(text, allowed_phonemes)
        else:
            raise TypeError(f'Phonemizer input must be list or str, not {type(text)}')

    def params_or_args(self, args_list):
        res = []
        for x in args_list:
            res.append(x or self.x)
        return res
    
    def __call__(
                self, 
                text: Union[str, list], 
                stress=True, 
                n_jobs=1, 
                language='en-us',
                allowed_phonemes=None)-> Union[str, list]:

        # call function with instance params or arguments (language, njobs, with_stress)
        language, n_jobs, stress = self.params_or_args([language,n_jobs,stress])
        


        # compute raw phonemes without filtration
        raw_phonemes = phonemize(
                            text,
                            language=language,
                            backend='espeak',
                            strip=True,
                            preserve_punctuation=True,
                            with_stress=stress,
                            njobs=n_jobs,
                            language_switch='remove-flags')
        
        
        # return filtrated phonemes
        return self.filter_characters(raw_phonemes, allowed_phonemes)
class Phonemes():

    def __init__(self):
        
        # All English sounds are created by the initiating action of air from the lungs going outward. 
        # These are categorized as pulmonic sounds. In contrast, many other languages have sounds which 
        # use additional kinds of airstream mechanisms. These are called non-pulmonic sounds.
        # Non-pulmonic sounds include clicks, ejectives, and implosives. 
        # They are all types of stop consonants, but they differ in the source and the direction of their airstreams.
        # In creating clicks and implosives, the air direction is ingressive – that is, going into the vocal tract. 
        # The initiation of the airstream occurs at the velum for clicks, and at the glottis for implosives. 
        # Thus, clicks are velaric ingressive sounds, while implosives are glottalic ingressive sounds.
        # Ejectives are glottalic egressive sounds – that is, the air flows out from the vocal tract. 
        # Therefore, ejectives share the direction of the air with pulmonic sounds, 
        # and share their airstream mechanism with implosives.

        self._non_pulmonic_consonants = 'ʘɓǀɗǃʄǂɠǁʛ' 

        # Pulmonic consonants are consonants that depend upon an egressive 
        # (outward-flowing) air stream originating in the lungs.
        
        self._pulmonic_consonants = 'pbtdʈɖcɟkɡqɢʔɴŋɲɳnɱmʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɦɬɮʋɹɻjɰlɭʎʟ' 
        

        self._vowels = 'iyɨʉɯuɪʏʊeøɘəɵɤoɛœɜɞʌɔæɐaɶɑɒᵻ'

        # Suprasegmental, also called prosodic feature, in phonetics,
        # a speech feature such as stress, tone, or word juncture that accompanies 
        # or is added over consonants and vowels; these features are not limited to 
        # single sounds but often extend over syllables, words, or phrases.
        
        self._suprasegmentals = 'ˈˌːˑ' 

        # Diacritics are small signs that are added to a phonetic symbol 
        # in order to transcribe a sound that is related to (but
        # different from) the sound that is usually denoted by the
        # bare symbol (see Figure 2).
        
        self._diacritics = 'ɚ˞ɫ' 

        self._other_symbols = 'ʍwɥʜʢʡɕʑɺɧ' 
 
        # Punctuation can be terminal or between words

        self._punctuations = '!,-.:;? '
        self._not_end_punctuation = ',-.:; '

        # alphabet letters,numbers
        self._alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzäüöß'
        
        self._numbers = '1234567890'


        # initialize phonemes list (with & without punctuation)
        self.list_sound_phonemes()
        self.list_all_phonemes()

    def list_sound_phonemes(self):
        '''
        returns the total list of sound based phonemes excluding punctuation (=115 different phonemes)
        '''
        self._phonemes = sorted(list(
                                    self._vowels + 
                                    self._non_pulmonic_consonants + 
                                    self._pulmonic_consonants + 
                                    self._suprasegmentals + 
                                    self._other_symbols + 
                                    self._diacritics)
                                    )
        return self._phonemes
    
    def list_all_phonemes(self):
        '''
        returns the total list of english phonemes including punctuation (=123 different phonemes)
        '''

        # self._phonemes is a list
        # in order to perform the concatenation 
        # the punctuation must be turned into a list

        self._all_phonemes = sorted(
            self._phonemes + 
            list(self._punctuations)
            )

        return self._all_phonemes

    def list_english_phonemes(self):
        '''
        returns the total list of english phonemes excluding punctuation (=45 different phonemes)
        '''

        # check more @ : https://github.com/rhasspy/larynx & https://github.com/rhasspy/gruut

        self._english_phonemes = list('_|‖#aɪaʊbdd͡ʒeɪfhiiːjklmnoʊpstt͡ʃuːvwzæðŋɑɑːɔɔɪəɛɝɡɪɹʃʊʌʒθ')

        return self._english_phonemes

    def list_all_english_phonemes(self):
        '''
        returns the total list of english phonemes including punctuation (=53 different phonemes)
        '''

        # check more @ : https://github.com/rhasspy/larynx & https://github.com/rhasspy/gruut

        self._all_english_phonemes = list('_|‖#aɪaʊbdd͡ʒeɪfhiiːjklmnoʊpstt͡ʃuːvwzæðŋɑɑːɔɔɪəɛɝɡɪɹʃʊʌʒθ') + list(self._punctuations)

        return self._all_english_phonemes