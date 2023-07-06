import json
from copy import copy
with open("../buenzli-corpus/comments.json", "r", encoding="utf-8") as f:
    comments = json.load(f)

def remove_punct(corpus):
    corpus.pop(".", None)
    corpus.pop(",", None)
    corpus.pop(":", None)
    corpus.pop(";", None)
    corpus.pop("!", None)
    corpus.pop("?", None)
    corpus.pop("(", None)
    corpus.pop(")", None)
    corpus.pop("'", None)
    corpus.pop('"', None)
    corpus.pop("–", None)
    corpus.pop("..", None)
    corpus.pop("...", None)
    corpus.pop("«", None)
    corpus.pop("»", None)
    corpus.pop(" ", None)

word_frequencies = {}
for comment in comments:
    sentence = comment["body"]
    for word in sentence.split(" "):
        word = word.lower()
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

remove_punct(word_frequencies)

total_words = sum(word_frequencies.values())

average_word_length = sum(len(word) * freq for word, freq in word_frequencies.items()) / total_words

#print(average_word_length, sep="\n")

sorted_buenzli = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
#print(sorted_buenzli)

buenzli_frequencies = copy(word_frequencies)



word_length_count_buenzli = {}
for elem in sorted_buenzli:
    if len(elem[0]) in word_length_count_buenzli:
        word_length_count_buenzli[len(elem[0])] += int(elem[1])
    else:
        word_length_count_buenzli[len(elem[0])] = int(1)

# sort word_length_count_buenzli by value
word_length_count_buenzli = {k: v for k, v in sorted(word_length_count_buenzli.items(), key=lambda item: item[1], reverse=True)}
#print(word_length_count_buenzli)
