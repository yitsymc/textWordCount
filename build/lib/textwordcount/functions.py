import string

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import FreqDist
from urllib.request import Request, urlopen

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")

POS_TAGS_DICT = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition or subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS": "List item marker",
    "MD": "Modal",
    "NN": "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP": "Particle",
    "TO": "to",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund or present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
}


def extract_text_from_url(url: str):
    request = Request(url, headers={"User-Agent": "TwcApp/1.0"})
    webpage = urlopen(request).read()
    parse_html = BeautifulSoup(webpage, "html.parser")
    return parse_html.get_text()


class TextWordCount:
    text: str
    language: str
    iso_639_lang: str

    def __init__(
        self, text=None, html_source=None, language="english", iso_639_lang="eng"
    ):
        """

        Args:
            text (str, optional): A string containing the text to be analyzed. Defaults to None.
            html_source (_type_, optional): A string with a URL. Defaults to None.
            language (str, optional): Text language. Defaults to "english".
            iso_639_lang (str, optional): ISO 639 code of the language. Defaults to "eng".

        Raises:
            ValueError: If the function doesn't receive value for text or html_source.
        """
        if not text and not html_source:
            raise ValueError(
                "You need to specify either the text or a source to proceed."
            )

        self.text = text
        if html_source:
            self.text = extract_text_from_url(html_source)
        self.language = language
        self.iso_639_lang = iso_639_lang

    def lemmatize_words(self, words: list):
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(word) for word in words]
        return lemmatized

    def process_text(self, exclude_stop_word=True, lemmatize=True)->list:
        """
        Process the received text in certain language using the NLTK library:
        1. Word tokenization
        2. Remove Stop Words
        3. Lemmatize the list of word

        :param exclude_stop_word: Exclude the stop words in the text

        :return: A list of useful words in a text
        """
        words_in_text = word_tokenize(text=self.text, language=self.language)
        stop_words = set(stopwords.words(self.language))
        punctuation = string.punctuation
        cleaned_list = (
            [
                word
                for word in words_in_text
                if word.casefold() not in stop_words and word not in punctuation
            ]
            if exclude_stop_word
            else [word for word in words_in_text if word not in punctuation]
        )
        if lemmatize:
            return self.lemmatize_words(cleaned_list)
        return cleaned_list

    def get_part_of_speech_tag(self, list_of_words: list)->list:
        """Get the Part of Speech of every word in a list, https://www.nltk.org/api/nltk.tag.pos_tag.html

        Args:
            list_of_words (list): Words to search
        """
        nltk.pos_tag(list_of_words, lang=self.iso_639_lang)

    def top_used_words(self, count: int=10)->list:
        """
        Get the most used words in a text, excluding stop words
        (set of commonly used words, like "a", "an", "is", etc)

        :param count: Number of top words, by 10 default

        :return: A list with the more frequent words in a text.
        """
        _list = self.process_text()
        frequency_by_words = FreqDist(_list)
        top_words = frequency_by_words.most_common(count)
        return [_word[0] for _word in top_words]

    def find_most_used_by_pos(self, pos_list: list, count: int=10)->list:
        """
        Get the most used words in a text, excluding stop words
        for certain Part of speech

        :param pos_list: list of part of speech, allowed values:
        'CC': 'Coordinating conjunction',
        'CD': 'Cardinal number',
        'DT': 'Determiner',
        'EX': 'Existential there',
        'FW': 'Foreign word',
        'IN': 'Preposition or subordinating conjunction',
        'JJ': 'Adjective',
        'JJR': 'Adjective, comparative',
        'JJS': 'Adjective, superlative',
        'LS': 'List item marker',
        'MD': 'Modal',
        'NN': 'Noun, singular or mass',
        'NNS': 'Noun, plural',
        'NNP': 'Proper noun, singular',
        'NNPS': 'Proper noun, plural',
        'PDT': 'Predeterminer',
        'POS': 'Possessive ending',
        'PRP': 'Personal pronoun',
        'PRP$': 'Possessive pronoun',
        'RB': 'Adverb',
        'RBR': 'Adverb, comparative',
        'RBS': 'Adverb, superlative',
        'RP': 'Particle',
        'TO': 'to',
        'UH': 'Interjection',
        'VB': 'Verb, base form',
        'VBD': 'Verb, past tense',
        'VBG': 'Verb, gerund or present participle',
        'VBN': 'Verb, past participle',
        'VBP': 'Verb, non-3rd person singular present',
        'VBZ': 'Verb, 3rd person singular present',
        'WDT': 'Wh-determiner',
        'WP': 'Wh-pronoun',
        'WP$': 'Possessive wh-pronoun',
        'WRB': 'Wh-adverb'

        :param count: Number of top words, by 10 default

        :return:  A list with the more frequent words of certain POS in a text.
        """
        if not set(pos_list).issubset(set(list(POS_TAGS_DICT.keys()))):
            return ValueError("Invalid values in received list")

        _list = self.process_text()
        pos_tag_mapped = nltk.pos_tag(_list)
        filtered = [_word[0] for _word in pos_tag_mapped if _word[1] in pos_list]
        frequency_by_words = FreqDist(filtered)
        top_words = frequency_by_words.most_common(count)
        return [_word[0] for _word in top_words]

    def count_word_usage_in_text(self, search_words: list)->dict:
        """
        Get how many time a word is used in a text

        :param search_words: Word(s) to search

        :return: number of appearance of the word
        """
        words = self.process_text(exclude_stop_word=False, lemmatize=False)
        lower_search_word = list(map(lambda x: x.lower(), search_words))
        count = dict(
            FreqDist(
                word.lower() for word in words if word.lower() in lower_search_word
            )
        )
        return count

    def find_sentences_contain_word_or_phrase(self, search_phrase: str)->list:
        """
        Get all sentences that contains a certain word

        :param search_phrase: Word or phrase to search

        :return: list with sentences
        """
        sentences = sent_tokenize(self.text)
        _list = [sentence for sentence in sentences if search_phrase in sentence]
        return _list
