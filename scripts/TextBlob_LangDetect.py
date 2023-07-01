import langid
from py3langid.langid import LanguageIdentifier, MODEL_FILE
import langdetect
import spacy
from textblob import TextBlob as tb
import os
import xml.etree.ElementTree as ET


from textblob import TextBlob
from langdetect import detect_langs

def detect_sentence_language(sentence):
    return detect_langs(sentence)[0].lang

def detect_word_languages(sentence, languages):
    blob = TextBlob(sentence)
    word_languages = []

    for word in blob.words:
        probabilities = detect_langs(word)
        top_language = None
        top_probability = 0.0

        for lang in probabilities:
            if lang.lang in languages and lang.prob > top_probability:
                top_language = lang.lang
                top_probability = lang.prob

        if top_language:
            word_languages.append((word, top_language))

    return word_languages

# Example usage
sentences = ["Ich han en gfrögt aber kei ahnig che cazzo de wott", "Es triggered mich hert", "Ich weiss nöd, aber es isch so whack", "Was meinsch, giovedi oder lieber mardi?", "Je ne crois pas"]

foreign_manual = ['che', 'cazzo', 'triggered', 'whack', 'giovedi', 'mardi']
foreign_system = []

languages_to_look_for = ['de', 'fr', 'it', 'en']  # Specify the languages to look for

for sentence in sentences:
    sentence_language = detect_sentence_language(sentence)
    word_languages = detect_word_languages(sentence, languages_to_look_for)
    for word in word_languages:
        if word[1] != 'de' and sentence_language == 'de':
            foreign_system.append(word[0])
    print("Sentence language:", sentence_language)
    print("Word languages:", word_languages, "\n")

print(foreign_system)
print(foreign_manual)

accuracy = len([word for word in foreign_system if word in foreign_manual]) / len(foreign_system)
print(f"Accuracy: {accuracy}")
recall = len([word for word in foreign_manual if word in foreign_system]) / len(foreign_manual)
print(f"Recall: {recall}")



