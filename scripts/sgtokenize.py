from transformers import AutoTokenizer
import json
import xml.etree.ElementTree as ET
# load german tokeniser
tokenizer = AutoTokenizer.from_pretrained("noeminaepli/swiss_german_pos_model")

def tokenize_swiss_german(text: str) -> list:
    """
    Tokenizes a text using the swiss_german_pos_model tokenizer
    :param text: the text to be tokenized
    :return: a list of tokens
    """
    return tokenizer.tokenize(text)

def main():
    """
    Tokenize the comments in comments.json and output to new xml file
    """
    with open("comments.json", "r") as f:
        comments = json.load(f)
    # create a new xml file
    root = ET.Element("root")
    tree = ET.ElementTree(root)
    # iterate over comments and tokenize them
    for comment in comments:
        # create a new comment element
        comment_element = ET.SubElement(root, "comment")
        # if the length of the comment is longer than 512, split it into multiple comments
        if len(comment["body"]) > 512:
            # split the comment into 512 character chunks
            chunks = [comment["body"][i:i + 512] for i in range(0, len(comment["body"]), 512)]
            # iterate over the chunks and tokenize them
            for chunk in chunks:
                # create a new comment element
                comment_element = ET.SubElement(root, "comment")
                # tokenize the chunk
                tokens = tokenize_swiss_german(chunk)
                # iterate over tokens and add them to the comment element
                for token in tokens:
                    token_element = ET.SubElement(comment_element, "token")
                    token_element.text = token
                # add the score, id and created_utc to the comment element
                score_element = ET.SubElement(comment_element, "score")
                score_element.text = str(comment["score"])
                id_element = ET.SubElement(comment_element, "id")
                id_element.text = comment["id"]
                created_utc_element = ET.SubElement(comment_element, "created_utc")
                created_utc_element.text = str(comment["created_utc"])
            continue
        # tokenize the comment
        tokens = tokenize_swiss_german(comment["body"])
        # iterate over tokens and add them to the comment element
        for token in tokens:
            token_element = ET.SubElement(comment_element, "token")
            token_element.text = token
        # add the score, id and created_utc to the comment element
        score_element = ET.SubElement(comment_element, "score")
        score_element.text = str(comment["score"])
        id_element = ET.SubElement(comment_element, "id")
        id_element.text = comment["id"]
        created_utc_element = ET.SubElement(comment_element, "created_utc")
        created_utc_element.text = str(comment["created_utc"])
    # write the xml to a file
    tree.write("comments.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
