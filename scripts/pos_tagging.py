from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from data import import_buenzli

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

def main():
    # import the comments
    comments = import_buenzli("data/buenzli/")
    # iterate over the comments and tag them
    for comment in comments:
        comment["pos_tags"] = pos_tag(comment["body"])
