
import json

# open comments.json file from downloads
with open("C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/comments_pos.json", "r", encoding='utf-8') as f:
    comments = json.load(f)


tag_frequencies = {}
word_pos_freq = {}
for comment in comments:
    for word in comment["POS"]:
        if word[0]["entity_group"] in tag_frequencies:
            tag_frequencies[word[0]["entity_group"]] += 1
        else:
            tag_frequencies[word[0]["entity_group"]] = 1


        if word[0]["entity_group"] in word_pos_freq:
            if word[0]["word"] in word_pos_freq[word[0]["entity_group"]]:
                word_pos_freq[word[0]["entity_group"]][word[0]["word"]] += 1
            else:
                word_pos_freq[word[0]["entity_group"]][word[0]["word"]] = 1
        else:
            word_pos_freq[word[0]["entity_group"]] = {word[0]["word"]: 1}

tags_count = sum(tag_frequencies.values())
#print(tags_count)
print("BUENZLI")

# normalize the frequencies
for key in word_pos_freq:
    for word in word_pos_freq[key]:
        word_pos_freq[key][word] = word_pos_freq[key][word]/tags_count

# for each key (tag) in the dictionary, sort the values (words) by frequency
for key in word_pos_freq:

    word_pos_freq[key] = sorted(word_pos_freq[key].items(), key=lambda x: x[1], reverse=True)
    # normalize the frequencies


# print the top 5 words for each tag
print(word_pos_freq["ADJ"][:5])
print(word_pos_freq["NOUN"][1:6])
print(word_pos_freq["VERB"][2:7])
print(word_pos_freq["ADV"][:5])
print("\n","----------------------------","\n")
print("NOAH")

# sort the dictionary by value
sorted_tags = sorted(tag_frequencies.items(), key=lambda x: x[0], reverse=False)
#print(sorted_tags)

tags = []
frequencies = []

for tag in sorted_tags:
    tags.append(tag[0])
    frequencies.append(tag[1]/tags_count)

import matplotlib.pyplot as plt
# create a bar plot
from load_NOAH_pos import NOAH_tags, NOAH_frequencies


plt.title("POS Tag Frequencies")
plt.bar(NOAH_tags, NOAH_frequencies, alpha=0.5, color="orange", label="NOAH")
plt.bar(tags, frequencies, alpha=0.5, color="grey", label="Buenzli")
plt.legend()
# increase font size of x ticks
plt.xticks(fontsize=12)
plt.xticks(rotation=45)
plt.xlabel("Part of Speech tag")
plt.ylabel("Percentage")
plt.tight_layout()
plt.show()
plt.savefig('POS_frequencies.png')
