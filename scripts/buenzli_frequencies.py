import json
from copy import copy
with open("../buenzli-corpus/comments.json", "r", encoding="utf-8") as f:
    comments = json.load(f)

word_frequencies = {}
for comment in comments:
    sentence = comment["body"]
    for word in sentence.split(" "):
        word = word.lower()
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

total_words = sum(word_frequencies.values())

average_word_length = sum(len(word) * freq for word, freq in word_frequencies.items()) / total_words

#print(average_word_length, sep="\n")


#print(sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:100])

buenzli_frequencies = copy(word_frequencies)

