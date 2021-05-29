from message_responce import file_to_list
from recognizing import clean
import os


def preprocess(path, delete_words, lemmatize):
    for filename in os.listdir(path):
        print(filename)

        data = sorted(set(file_to_list(f'{path}/{filename}')))
        for i, text in enumerate(data):
            data[i] = clean(text, delete_words, lemmatize)

        with open(f'{path}/{filename}', 'wt', encoding='utf-8') as file:
            file.write('\n'.join(data))


def make_vocabulary(path):
    words = []
    for filename in os.listdir(path):
        print(filename)
        for text in file_to_list(f'{path}/{filename}'):
            words.extend(text.split(' '))

    with open(f'{path}/VOCABULARY.txt', 'wt', encoding='utf-8') as file:
        file.write('\n'.join(sorted(set(words))))


# make_vocabulary('resources/replicas')
# make_vocabulary('resources/forecasts')
