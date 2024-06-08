"""
Prepare rfb dataset for token classification task.
"""

import pandas as pd
from sklearn.model_selection import train_test_split


def get_tokens(cleaned_text: str):
    """
    Get tokens from preprocessed OCR text.
    """
    return cleaned_text.split()


def get_labels(silver_annotation: str):
    """
    Extract BIO tags from a sequence of spans in the form `token@tag:index`
    """
    mappings = {"BR": "B-ROLE", "IR": "I-ROLE", "BF": "B-FILL", "IF": "I-FILL"}
    labels = []
    for labeled_tok in silver_annotation.split():
        tok, label = labeled_tok.split("@")
        if ":" in label:
            label = label.split(":")[0]
            label = mappings[label]
        labels.append(label)
    return labels


if __name__ == "__main__":
    original_df = pd.read_csv("annotations.csv")
    tokens = original_df["scene_label"] + " " + original_df["cleaned_text"]
    tokens = tokens.map(get_tokens)
    labels = original_df["silver_standard_annotation"].map(get_labels).tolist()
    labels = [["O"] + label_seq for label_seq in labels]
    for idx, tok_seq in enumerate(tokens):
        lab_seq = labels[idx]
        # sanity check to make sure token and tag seqs are the same length
        if len(lab_seq) != len(tok_seq):
            print(
                "Length of tokens does not match length of labels: ",
                len(labels[idx]),
                len(tok_seq),
            )
            print(tok_seq, lab_seq)
    output_df = pd.DataFrame(data={"tokens": tokens, "labels": labels})
    train, val = train_test_split(output_df, test_size=0.2, random_state=42)
    train.to_json("rfb_train.json", orient="records", lines=True)
    val, test = train_test_split(val, test_size=0.5, random_state=42)
    val.to_json("rfb_val.json", orient="records", lines=True)
    test.to_json("rfb_test.json", orient="records", lines=True)
