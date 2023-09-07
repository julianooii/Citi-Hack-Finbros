import spacy
from spacy.tokens import Doc
from wasabi import msg

# Load in the coref model
# You can download the model here
# https://github.com/explosion/spacy-experimental/releases/tag/v0.6.0
nlp = spacy.load("en_coreference_web_trf")

# Process example sentence
# Other examples:
# Philip plays the bass because he loves it.
# Sarah enjoys a nice cup of tea in the morning. She likes it with sugar and a drop of milk.
# John said hi. Big old John is always around.
doc = nlp("John said hi. Big old John is always around.")

# Print out component names
msg.info("Pipeline components")
for i, pipe in enumerate(nlp.pipe_names):
    print(f"{i}: {pipe}")

# Print out clusters
msg.info("Found clusters")
for cluster in doc.spans:
    print(f"{cluster}: {doc.spans[cluster]}")

# Define lightweight function for resolving references in text
def resolve_references(doc: Doc) -> str:
    """Function for resolving references with the coref ouput
    doc (Doc): The Doc object processed by the coref pipeline
    RETURNS (str): The Doc string with resolved references
    """
    # token.idx : token.text
    token_mention_mapper = {}
    output_string = ""
    clusters = [
        val for key, val in doc.spans.items() if key.startswith("coref_cluster")
    ]

    # Iterate through every found cluster
    for cluster in clusters:
        first_mention = cluster[0]
        # Iterate through every other span in the cluster
        for mention_span in list(cluster)[1:]:
            # Set first_mention as value for the first token in mention_span in the token_mention_mapper
            token_mention_mapper[mention_span[0].idx] = first_mention.text + mention_span[0].whitespace_
            
            for token in mention_span[1:]:
                # Set empty string for all the other tokens in mention_span
                token_mention_mapper[token.idx] = ""

    # Iterate through every token in the Doc
    for token in doc:
        # Check if token exists in token_mention_mapper
        if token.idx in token_mention_mapper:
            output_string += token_mention_mapper[token.idx]
        # Else add original token text
        else:
            output_string += token.text + token.whitespace_

    return output_string


msg.info("Document with resolved references")
print(resolve_references(doc))