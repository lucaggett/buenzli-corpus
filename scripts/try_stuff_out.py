import langid
from py3langid.langid import LanguageIdentifier, MODEL_FILE
import langdetect
import spacy
from textblob import TextBlob as tb
import os
import xml.etree.ElementTree as ET
identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
identifier.set_languages(['de', 'en', 'fr', 'it'])
from DOMINIC_import_dict import fr_word_ls, it_word_ls, en_word_ls

def swiss_german_check(word):
    #catch swiss german verbs in 2nd person plural that look like english participles
    if len(word) >= 4 and word[-2:] == "ed" and word[-4] == "e":
        return True
    elif word.lower() == "also":
        return True
    else:
        return False


sentence = ["Das", "isch", "un", "piacere", "italiano", "salute", "benvenuti", "buongiorno"]



for word in sentence:
    count_in_sentence = 0
    word_analysis = identifier.classify(word)
    if word_analysis[1] > 0.95 and word_analysis[0] != 'de':
        if (word_analysis[0] == 'fr' and word in fr_word_ls) or (word_analysis[0] == 'it' and word in it_word_ls) or (
                word_analysis[0] == 'en' and word in en_word_ls) and swiss_german_check is False:
            count_in_sentence += 1
    print(word)
    print(word_analysis)
if count_in_sentence >= len(sentence) > 2:
    print(f"Supposed foreign sentence: {sentence}")