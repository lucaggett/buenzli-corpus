# read in the train fr file
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

with open("../other_data/train.fr", "r", encoding="utf-8") as f:
    text = f.readlines()

    # remove all newlines
    text = [line.replace("\n", "") for line in text]
    # remove all lines that are empty
    text = [line for line in text if line != ""]
    # remove all lines that are only one character long
    text = [line for line in text if len(line) > 1]
    # remove all lines that start with *
    text = [line for line in text if not line.startswith("*")]
    #replace all = with a space
    text = [line.replace("= ", "") for line in text]
    # join all lines to one string
    text = " ".join(text)
    # split into sentences using the nltk sentence tokenizer
    sentences = sent_tokenize(text)

    # write the sentences to a file
    with open("../other_data/clean_train.fr", "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")
