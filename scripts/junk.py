import langdetect

def detect_language(text):
    """
    Detects the language of a text
    :param text: the text to detect the language of
    :return: the language of the text
    """
    return langdetect.detect(text)

print(detect_language("de"))


