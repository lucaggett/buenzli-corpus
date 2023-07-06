from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from data import import_buenzli, import_NOAH_sentences
import json
import tqdm

model = AutoModelForTokenClassification.from_pretrained("noeminaepli/swiss_german_pos_model")
tokenizer = AutoTokenizer.from_pretrained("noeminaepli/swiss_german_pos_model")

pos_tagger = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")



def pos_tag(text: str) -> list[dict]:
    """
    Tags a text with part of speech tags
    :param text: the text to be tagged
    :return: a list of tuples containing the token and its tag
    """
    return pos_tagger(text)

def tag_buenzli():
    word_limit = 100
    # import the comments
    comments = import_buenzli("../scripts/comments.json")
    # iterate over the comments and tag them
    print(f"applying POS tags to {word_limit if word_limit else len(comments)} words in buenzli corpus")
    for comment in tqdm.tqdm(comments[:word_limit]):
        pos_tags = []
        for word in comment["body"].split():
            word.lower().strip(".,!?;:()[]{}")
            pos_tags.append(pos_tag(word))

        comment["POS"] = pos_tags

        for word in pos_tags:
            for tag_dict in word:
                for attr in tag_dict:
                    if not isinstance(tag_dict[attr], str):
                        tag_dict[attr] = str(tag_dict[attr])

    # write the comments to a new json file
    with open("comments_pos.json", "w") as f:
        json.dump(comments[:word_limit], f, indent=4)

def tag_NOAH():
    # import the sentences
    sentences = import_NOAH_sentences("../NOAH-Corpus/")
    # iterate over the sentences and tag them
    tagged_sentences = []
    for sentence in tqdm.tqdm(sentences):
        tagged_sentences.append(pos_tag(sentence))

    # write the sentences to a new file
    with open("NOAH_sentences_pos.csv", "w", encoding='utf-8') as f:
        for sentence in tagged_sentences:
            f.write(str(sentence) + "\n")


if __name__ == "__main__":
    #tag_buenzli()
    tag_NOAH()