"""This module consists necessary for natural language processing functions,
such as preprocessing and similarity assessing
"""

from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from pymystem3 import Mystem

# A set of unimportant words for assessing similarity
stopwords = set(stopwords.words('russian'))


def clean(text: str, delete_words: set = stopwords, lemmatize: bool=True) -> str:
    """The function performs preprocessing of the text in the form
    of removing punctuations, unimportant words and converting to lower case

    :param text: text with punctuation for cleaning
    :param delete_words: words that do not carry much meaning
    :return: preprocessed text
    """
    text = text.lower().replace('ё', 'е')
    text = ''.join([word for word in text if word not in punctuation])

    # Delete unimportant words if necessary
    if delete_words:
        text = ' '.join([word for word in text.split() if word not in delete_words])

    if lemmatize:
        m = Mystem()
        lemmas = m.lemmatize(text)
        text = ''.join(lemmas)
    print(text)
    return text


def similarity(message: str, patterns: list) -> float:
    """Returns similarity score between message and list of phrases.
    Similarity comparison occurs by converting words to vectors and estimating the cosine distance

    :param message: single string
    :param patterns: phrases to assess similarity with message
    :return: maximum similarity score from 0 to 1
    """

    # Delete words in stopwords, that exists in patterns
    cos_sim = []

    for word in patterns:
        unimportant_words = stopwords.difference(' '.join(word).split(' '))
        # Preprocess and concatenate data
        # data = [clean(message, unimportant_words), word]
        data = [message, word]
        # Converts each word to vector
        to_vector = CountVectorizer(lowercase=False).fit_transform(data)

        vectors = to_vector.toarray()
        # Calculates cosine distance
        cos_sim.append(cosine_similarity(vectors)[0, 1])

    # Returns maximal score
    return max(cos_sim)