import random
import xml.etree.ElementTree as ET
import json
import logging
from collections import Counter
from typing import List

import numpy as np

from data import import_NOAH_sentences, import_buenzli


def create_swiss_german_dictionary() -> set:
    """
    Creates a set of swiss german words from files contained in NOAHs corpus
    :return: a set of swiss german words
    """
    word_count = 0
    sentence_count = 0
    # files are in NOAH-corpus/ and are as follows: blick.xml, blogs.xml, schobinger.xml, swatch.xml, wiki.xml
    files = ("blick.xml", "blogs.xml", "schobinger.xml", "swatch.xml", "wiki.xml")
    swiss_german_words = set()
    for file in files:
        tree = ET.parse(f"../NOAH-Corpus/{file}")
        root = tree.getroot()
        for article in root:
            for sentence in article:
                sentence_count += 1
                for word in sentence:
                    word_count += 1
                    swiss_german_words.add(word.text)
    return swiss_german_words


class NgramTokenizer:
    def __init__(self, ngram_order: int):
        self.ngram_order = ngram_order

    def __call__(self, text: str) -> List[str]:
        """
        Tokenize text into ngrams, yielding each ngram in turn to reduce memory usage. This assumes the text is already pretokenized and split by spaces
        """

        tokens = text.split(" ")

        for i in range(len(tokens) - self.ngram_order + 1):
            yield " ".join(tokens[i:i + self.ngram_order])


class BigramLanguagePredictor:

    def __init__(self, ngram_order: int = None, model_is_trained: bool = False):
        assert (ngram_order is not None) or model_is_trained

        self.ngram_order = ngram_order

        self.probs = {}

    def create_propabilities(self, text: str):
        """
        Train language model on text, should be able to recognise if a given ngram is in the language it was trained on
        """

        tokenizer = NgramTokenizer(self.ngram_order)

        ngrams = tokenizer(text)
        count = Counter(ngrams)
        total = sum(count.values())
        self.probs = {ngram: np.log(count[ngram] / total) for ngram in count}

        self.model_is_trained = True

    def predict(self, text: str):
        """
        Predict the probability of a given text being in the language the model was trained on
        """
        tokenizer = NgramTokenizer(self.ngram_order)

        ngrams = tokenizer(text)
        ngrams = [ngram for ngram in ngrams]

        return sum(self.probs[ngram] if ngram in self.probs else -100 for ngram in ngrams) / (1 + len(ngrams)/5)

    def load(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as handle:
            self.probs = json.load(handle)

        self.ngram_order = self.probs["__ORDER__"]

        return self

    def save(self, file_path):
        self.probs["__ORDER__"] = self.ngram_order

        with open(file_path, 'w') as handle:
            json.dump(self.probs, handle, ensure_ascii=True, indent=2)


def create_swiss_german_model():
    sentences = import_NOAH_sentences("../NOAH-Corpus/")

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(sentences))

    model.save("../models/swiss_german_model.json")
    logging.info("Saved model")
    return model

def create_english_model():
    with open("../other_data/train.en", "r") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))

    model.save("../models/english_model.json")

    return model

def create_german_model():
    with open("../other_data/train.de", "r") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))

    model.save("../models/german_model.json")

    return model

def create_dutch_model():
    with open("../other_data/train.nl", "r") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))

    model.save("../models/dutch_model.json")

    return model

def create_italian_model():
    with open("../other_data/train.it", "r") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))

    model.save("../models/italian_model.json")

    return model

def main():
    logging.basicConfig(level=logging.INFO)
    models = {
        "GSW": create_swiss_german_model(),
        "EN": create_english_model(),
        "DE": create_german_model(),
        "NL": create_dutch_model(),
        "IT": create_italian_model(),
    }

    buenzli_corpus = import_buenzli("../buenzli-corpus/comments.json")

    for comment in buenzli_corpus:
        comment["language"] = (max(models, key=lambda x: models[x].predict(comment["body"])))

    GSW_comments = []
    other_comments = {lang: [] for lang in models if lang != "GSW"}

    for comment in buenzli_corpus:
        if comment["language"] != "GSW":
            other_comments[comment["language"]].append(comment["body"])
        else:
            GSW_comments.append(comment["body"])
    print("\n"*5)
    print("GSW: ", len(GSW_comments))
    for lang in other_comments:
        print(lang, len(other_comments[lang]))

    # print a sample of the each language
    for lang in other_comments:
        print("\n"*5)
        print("*"*10, lang, "*"*10)
        for comment in random.sample(other_comments[lang], 10):
            print(comment)
            print("-"*20)

        print("\n"*5)
        print("*"*10, "GSW", "*"*10)
        for comment in random.sample(GSW_comments, 10):
            print(comment)
            print("-"*20)





    """
    This performs pretty okay overall. 
    The dutch classification mostly catches swiss german sentences, so it could be removed.
    The italian classification is catches some swiss german sentences
    
    GSW: 51853
    non-GSW: 7098
    EN: 1242
    DE: 5583
    NL: 206
    IT: 67
    """

if __name__ == "__main__":
    main()