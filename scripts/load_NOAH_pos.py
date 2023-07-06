
# import the csv as a list, with each line being one entry

with open("NOAH_sentences_pos.csv", "r", encoding='utf-8') as f:
    lines = f.readlines()

import ast
list_of_sentence_dicts = []
for line in lines:
    list_of_dicts = ast.literal_eval(line)
    list_of_sentence_dicts.append(list_of_dicts)

# iterate over the list of dicts and extract the tags
tags_frequencies = {}

word_pos_freq = {}

counter = 0
for sentence in list_of_sentence_dicts:
    sent_str = ""
    counter += 1
    for dict in sentence:
        sent_str += dict["word"] + " "

        if dict["entity_group"] in word_pos_freq:
            if dict["word"] in word_pos_freq[dict["entity_group"]]:
                word_pos_freq[dict["entity_group"]][dict["word"]] += 1
            else:
                word_pos_freq[dict["entity_group"]][dict["word"]] = 1
        else:
            word_pos_freq[dict["entity_group"]] = {dict["word"]: 1}

        tag = dict["entity_group"]
        if tag in tags_frequencies:
            tags_frequencies[tag] += 1
        else:
            tags_frequencies[tag] = 1
    #print(sent_str)

tags_count = sum(tags_frequencies.values())
#normalize the frequencies
for key in word_pos_freq:
    for word in word_pos_freq[key]:
        word_pos_freq[key][word] = word_pos_freq[key][word]/tags_count


# for each key (tag) in the dictionary, sort the values (words) by frequency
for key in word_pos_freq:
    word_pos_freq[key] = sorted(word_pos_freq[key].items(), key=lambda x: x[1], reverse=True)

# print the top 5 words for each tag
print(word_pos_freq["ADJ"][:5])
print(word_pos_freq["NOUN"][:5])
print(word_pos_freq["VERB"][:5])
print(word_pos_freq["ADV"][:5])



print("\n", "*"*50, "\n")
print(f"Number of sentences: {counter}")
print(f"Number of tags: {sum(tags_frequencies.values())}")
print("\n", "*"*50, "\n")

# sort the tags by frequency
sorted_tags = sorted(tags_frequencies.items(), key=lambda x: x[0], reverse=False)
print(sorted_tags)

# create a plot of the tag frequencies
import matplotlib.pyplot as plt
import numpy as np
# the tags should be the x axis, the frequencies the y axis
# create a list of the tags and a list of the frequencies
NOAH_tags = []
NOAH_frequencies = []
tags_count = sum(tags_frequencies.values())
for tag in sorted_tags:
    NOAH_tags.append(tag[0])
    NOAH_frequencies.append(tag[1]/tags_count)

# create a bar plot
plt.title("POS Tag Frequencies in NOAH Corpus")
plt.bar(NOAH_tags, NOAH_frequencies, alpha=0.5, color="orange")
plt.xticks(rotation=45)
plt.show()
plt.savefig('POS_frequencies_NOAH.png')






