
import langid
from py3langid.langid import LanguageIdentifier, MODEL_FILE
import langdetect
import spacy
from textblob import TextBlob as tb
import os
import xml.etree.ElementTree as ET

def import_NOAH(path):
    """
    Imports the NOAH corpus into a list of strings
    :param path: path to NOAH corpus
    :return: list of strings
    """
    # get all files in path
    files = os.listdir(path)
    # create set of words used in corpus
    articles = []

    # iterate through files
    for file in files:
        # parse xml file
        tree = ET.parse(path + file)
        # get root element
        root = tree.getroot()
        # iterate through all text elements
        for article in root.iter("document"):
            articles_ls = []
            articles.append(articles_ls)
            for sent in article.iter("s"):
                sent_ls = []
                articles_ls.append(sent_ls)
                for word in sent.iter("w"):
                    sent_ls.append(word.text)

    # return set of words
    return articles


identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
identifier.set_languages(['de', 'en', 'fr', 'it'])

def identify_language(text):
    pass

NOAH_path = "C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/NOAH-Corpus-master/"
NOAH = import_NOAH(NOAH_path)

for article in NOAH:
    for sentence in article:
        for word in sentence:
            word_analysis = identifier.classify(word)
            if word_analysis[1] > 0.8 and word_analysis[0] != 'de':
                print(word)
                print(word_analysis)