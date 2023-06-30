import xml.etree.ElementTree as ET
import os


def import_NOAH(path):
    """
    Imports the NOAH corpus into a list of strings
    :param path: path to NOAH corpus
    :return: list of strings
    """
# get all files in path
files = os.listdir(path)
# create set of words used in corpus
words = set()

# iterate through files
for file in files:
    # parse xml file
    tree = ET.parse(path + file)
    # get root element
    root = tree.getroot()
    # iterate through all text elements
    for article in root.iter("document"):
        for sent in article.iter("s"):
            for word in sent.iter("w"):
                # add word to set
                words.add(word.text)
# return set of words
return words

