import logging
import warnings
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense

from Document import Document

logging.basicConfig(level=logging.INFO)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning)


class NeuralMethod:
    def __init__(self, russian_doc_path, german_doc_path) -> None:
        self.data = None
        self.prepare_dataset(russian_doc_path, german_doc_path)
        self.init_model()

    def init_model(self):

        # Filter by text language
        lang = ['Russian', 'German']

        # Select 200 rows for each language
        data_trim = pd.DataFrame(columns=['lang', 'text'])

        for l in lang:
            try:
                lang_trim = self.data[self.data['lang'] == l].sample(500, random_state=100)
            except ValueError:
                lang_trim = self.data[self.data['lang'] == l]  # Используйте все доступные элементы
            data_trim = data_trim.append(lang_trim)

        # Create a random train, valid, test split
        data_shuffle = data_trim.sample(frac=1)

        train = data_shuffle[0:1000]

        # obtain trigrams from each language
        features = {}
        features_set = set()

        for l in lang:
            # get corpus filtered by language
            corpus = train[train.lang == l]['text']

            # get 200 most frequent trigrams
            trigrams = self.get_trigrams(corpus)

            # add to dict and set
            features[l] = trigrams
            features_set.update(trigrams)

        # create vocabulary list using feature set
        vocab = dict()
        for i, f in enumerate(features_set):
            vocab[f] = i

        # create feature matrix for training set
        corpus = train['text']
        self.vectorizer = CountVectorizer(
            analyzer='char', ngram_range=(3, 3), vocabulary=vocab)
        X = self.vectorizer.fit_transform(corpus)

        self.names = self.vectorizer.get_feature_names()
        train_feat = pd.DataFrame(data=X.toarray(), columns=self.names)

        # Scale feature matrix
        self.train_min = train_feat.min()
        self.train_max = train_feat.max()
        train_feat = (train_feat - self.train_min) / \
                     (self.train_max - self.train_min)

        # Add target variable
        train_feat['lang'] = list(train['lang'])

        # Fit encoder
        self.encoder = LabelEncoder()
        self.encoder.fit(['Russian', 'German'])

        # Get training data
        x = train_feat.drop('lang', axis=1)
        y = self.encode(train_feat['lang'], self.encoder)

        # Define model
        model = Sequential()
        self.model = model
        dim = int(x.size / len(x))
        self.model.add(Dense(100, input_dim=dim, activation='relu'))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(2, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adam', metrics=['accuracy'])

        # Train model
        self.model.fit(x, y, epochs=4, batch_size=100, verbose=0)

    def get_trigrams(self, corpus, n_feat=200):
        """
        Returns a list of the N most common character trigrams from a list of sentences
        params
        ------------
            corpus: list of strings
            n_feat: integer
        """

        # fit the n-gram model
        vectorizer = CountVectorizer(analyzer='char',
                                     ngram_range=(3, 3), max_features=n_feat)

        self.X = vectorizer.fit_transform(corpus)

        # Get model feature names
        feature_names = vectorizer.get_feature_names()

        return feature_names

    def encode(self, y, encoder):
        """
        Returns a list of one hot encodings
        Params
        ---------
            y: list of language labels
        """
        from keras.utils import np_utils
        y_encoded = encoder.transform(y)
        y_dummy = np_utils.to_categorical(y_encoded)

        return y_dummy

    def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_language(self, file_path: str) -> str:
        test = pd.DataFrame(
            [['', self.read_file(file_path)]], columns=['lang', 'text'])
        corpus = test['text']
        X = self.vectorizer.fit_transform(corpus)

        test_feat = pd.DataFrame(data=X.toarray(), columns=self.names)
        test_feat = (test_feat - self.train_min) / \
                    (self.train_max - self.train_min)
        test_feat['lang'] = list(test['lang'])

        x_test = test_feat.drop('lang', axis=1)
        labels = np.argmax(self.model.predict(x_test), axis=1)
        predictions = self.encoder.inverse_transform(labels)
        return predictions[0]

    def prepare_dataset(self, russian_doc_path, german_doc_path):
        self.data = pd.DataFrame([], columns=['text', 'lang'])
        russian_text = Document(russian_doc_path).get_text(russian_doc_path)
        n = 50  # chunk length
        chunks = [russian_text[i:i + n] for i in range(0, len(russian_text), n)]
        for chunk in chunks:
            self.data = pd.concat([self.data, pd.DataFrame([[chunk, 'Russian']], columns=['text', 'lang'])])

        german_text = Document(german_doc_path).get_text(german_doc_path)
        chunks = [german_text[i:i + n] for i in range(0, len(german_text), n)]
        for chunk in chunks:
            self.data = pd.concat([self.data, pd.DataFrame([[chunk, 'German']], columns=['text', 'lang'])])
