from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from data import import_NOAH_sentences

model = AutoModelForTokenClassification.from_pretrained("noeminaepli/swiss_german_pos_model")
tokenizer = AutoTokenizer.from_pretrained("noeminaepli/swiss_german_pos_model")

pos_tagger = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")



def pos_tag(text: str) -> list:
    """
    Tags a text with part of speech tags
    :param text: the text to be tagged
    :return: a list of tuples containing the token and its tag
    """
    return pos_tagger(text)


NOAH_corpus = import_NOAH_sentences("../NOAH-Corpus/")
NOAH_corpus_w_pos = {}

counter = 0
for sent in NOAH_corpus:
    counter += 1
    if counter > 20:
        break
    if counter % 10 == 0:
        print(f"iteration: {counter}")
    NOAH_corpus_w_pos[counter] = {"text":sent, "info": pos_tag(sent)}


for k, v in NOAH_corpus_w_pos:
    # change all scores to strings
    for i in range(len(v["info"])):
        v["info"][i]["score"] = str(v["info"][i]["score"])


import json
with open("../NOAH-Corpus/NOAH_corpus_w_pos.json", "w", encoding="utf-8") as f:
    json.dump(NOAH_corpus_w_pos, f, ensure_ascii=False, indent=2)
