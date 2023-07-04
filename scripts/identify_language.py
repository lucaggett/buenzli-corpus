import xml.etree.ElementTree as ET


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
    #print(f"Number of words: {word_count}")
    #print(f"Number of sentences: {sentence_count}")
    return swiss_german_words

