# import packages
import os
import re
import csv
import codecs
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from string import punctuation

from gensim.models import KeyedVectors
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers.merge import concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# set directories and parameters
BASE_DIR = 'data/'
CONVERTED_FILE = BASE_DIR + 'word_vectors'
MAX_SEQUENCE_LENGTH = 30
MAX_NB_WORDS = 200000
EMBEDDING_DIM = 300
VALIDATION_SPLIT = 0.1

test_question_1 = raw_input('Enter the first question: ')
test_question_2 = raw_input('Enter the second question: ')


# index word vectors - key value pair for word and feature vector
#  computing an index mapping words to known embeddings, by parsing the data dump of pre-trained embeddings
print('Indexing word vectors')
word2vec = KeyedVectors.load(CONVERTED_FILE,mmap='r')
print('Found %s word vectors of word2vec' % len(word2vec.vocab))


# process texts in datasets
print('Processing text dataset')

# Clean the text, with the option to remove stopwords and to stem words.
def text_to_wordlist(text, remove_stopwords=False, stem_words=False):
    
    # Convert words to lower case and split them
    text = text.lower().split()

    # Optionally, remove stop words
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
    
    text = " ".join(text)

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    
    # Optionally, shorten words to their stems
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
    
    # Return a list of words
    return(text)

test_texts_1 = []
test_texts_2 = []
test_texts_1.append(text_to_wordlist(test_question_1))
test_texts_2.append(text_to_wordlist(test_question_2))

'''
Word2vec needs to be fed words rather than whole sentences, so the next step is to tokenize the data. 
To tokenize a text is to break it up into its atomic units, creating a new token each time you hit a white space.
'''
tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(test_texts_1 + test_texts_2)

test_sequences_1 = tokenizer.texts_to_sequences(test_texts_1)
test_sequences_2 = tokenizer.texts_to_sequences(test_texts_2)

word_index = tokenizer.word_index
print('Found %s unique tokens' % len(word_index))

test_data_1 = pad_sequences(test_sequences_1, maxlen=MAX_SEQUENCE_LENGTH)
test_data_2 = pad_sequences(test_sequences_2, maxlen=MAX_SEQUENCE_LENGTH)

# prepare embeddings
# converting discrete labels into continuous vector space
print('Preparing embedding matrix')

nb_words = min(MAX_NB_WORDS, len(word_index))+1

embedding_matrix = np.zeros((nb_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if word in word2vec.vocab:
        embedding_matrix[i] = word2vec.word_vec(word)
print('Null word embeddings: %d' % np.sum(np.sum(embedding_matrix, axis=1) == 0))



bst_model_path = [model_compiled for model_compiled in os.listdir('./') if model_compiled.find('.h5')!=-1][0]

# loading model here
print('Pre-trained model: ',bst_model_path)
model = load_model(bst_model_path)

print('Predicting on test data')
preds = model.predict([test_data_1, test_data_2], batch_size=1, verbose=1)
preds += model.predict([test_data_2, test_data_1], batch_size=1, verbose=1)
preds /= 2
if preds.ravel()[0]>0.5:    # setting a threshold of 0.5
    print('Yes')
else:
    print('No')





