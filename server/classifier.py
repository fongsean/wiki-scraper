import numpy as np
import json
from collections import Counter


class Classifier:
    def __init__(self):
        self.category_words_map = json.load(open('./categories.json'))

        # generate (single word, category) key-value pairs
        self.word_category_pairs = {
            word: category
            for category, words in self.category_words_map.items()
            for word in words
        }

        # load word-embedding matrix
        self.embed_index = {}
        with open("./glove.6B.100d.txt") as glove_file:
            for line in glove_file:
                values = line.split()
                word = values[0]
                self.embed_index[word] = np.array(values[1:], dtype=np.float32)

        # generate embeddings for words in local dataset
        self.word_embed_map = {
            word: embed
            for word, embed in self.embed_index.items()
            if word in self.word_category_pairs.keys()
        }

    # Measures similarity between embeddings of query and defined words
    def predict(self, query):
        if query not in self.embed_index:
            return None

        query_embed = self.embed_index[query]
        scores = {}
        for word, embed in self.word_embed_map.items():
            category = self.word_category_pairs[word]
            similarity = (query_embed @ embed) / len(self.category_words_map[category])
            scores[category] = scores.get(category, 0) + similarity
        return scores
