import json
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
    sentences = []

    # iterate through files
    for file in files:
        # parse xml file
        tree = ET.parse(path + file)
        # get root element
        root = tree.getroot()
        # iterate through all text elements
        for article in root.iter("document"):
            for sent in article.iter("s"):
                # add sentence to list

                for word in sent.iter("w"):
                    # add word to set
                    words.add(word.text)

    # return set of words
    return words


def import_NOAH_sentences(path):
    """
    Imports the NOAH corpus into a list of strings
    This function needs to reconstruct the sentences from the singular words, as the sentences are not stored in the corpus
    """
    # get all files xml files in path
    files = os.listdir(path)
    sentences = []

    # iterate through files
    for file in files:
        if file.endswith(".xml"):
            # parse xml file
            tree = ET.parse(path + file)
            # get root element
            root = tree.getroot()
            # iterate through all text elements
            for article in root.iter("document"):
                for sent in article.iter("s"):
                    # add sentence to list
                    sentence = ""
                    for word in sent.iter("w"):
                        # add word to set
                        sentence += word.text + " "
                    sentences.append(sentence)

    return sentences

def import_buenzli(path) -> list[dict[str, str]]:
    """
    import the buenzli corpus as sentences
    """
    with open(path, "r") as f:
        comments = json.load(f)

    sentences = []
    for comment in comments:
        sentences.append(comment)

    return sentences

