import random
import re
import json

import requests
from requests import HTTPError


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


class ProbDist(dict):
    """
    A Probability Distribution; an {outcome: probability} mapping.
    """
    def __init__(self, mapping=(), **kwargs):
        super().__init__(**kwargs)
        self.update(mapping, **kwargs)

        # Make probabilities sum to 1.0 and assert no negative probabilities.
        total = sum(self.values())
        for outcome in self:
            self[outcome] = self[outcome] / total
            assert self[outcome] >= 0


class MarkovStateMachine:
    @staticmethod
    def compute_weights(counts):
        """
        :param counts: dict {value1: n1, value2: n2, ...}
        :return: dict {value1: p1, value2: p2, ...}
        """
        n_edges = len(counts)
        p_edges = {}

        for k,v in counts.items():
            p_edges[k] = v / n_edges

        return p_edges

    @staticmethod
    def get_new_edge(edges, weights):
        return random.choices(edges, weights=weights)


class MarkovChainText:
    @staticmethod
    def build_chain(text, m_chain=None):
        """
        Normally I would use NumPy tensors or Pandas DataFrames for all the
        heavy lifting. But if I understand the exercise correctly it is to build
        something from scratch.

        :return:
        """
        start_words = set()
        end_words = set()
        m_chain = {} if m_chain is None else m_chain

        # Have a special class of words: start words, so we can have a
        # better chance of the joke sounding "natural".
        words = re.split(r"\s+", text)
        start_words.add(words[0])

        # Count all of the words.
        for i in range(0, len(words) - 1):
            word = words[i]
            next_word = words[i + 1]

            if word not in m_chain:
                m_chain[word] = {
                    'next_words': {
                        next_word: {
                            'count': 1,
                            'prob': None
                        }
                    },
                    'total_count': 1
                }
            if next_word not in m_chain[word]['next_words']:
                m_chain[word]['next_words'][next_word] = {
                    'count': 1,
                    'prob': None
                }
            else:
                m_chain[word]['next_words'][next_word]['count'] += 1

            m_chain[word]['total_count'] += 1

            if word[-1] in ['.', '!', '?'] and word != '.':
                start_words.add(next_word)

        # Find words that end a sentence for the converse reason we track
        # start words.
        for word in words:
            if word[-1] in ['.', '!', '?'] and word != '.':
                end_words.add(word)

        pm_chain = dict(m_chain)

        # print(json.dumps(m_chains, indent=4))
        # Calculate next_words probability.
        for word, metadata in m_chain.items():
            for next_word, count in metadata['next_words'].items():
                pm_chain[word]['next_words'][next_word]['prob'] = \
                    pm_chain[word]['next_words'][next_word]['count'] / metadata['total_count']

        print(mydict(pm_chain), start_words, end_words)
        return pm_chain, start_words, end_words

    @staticmethod
    def generate_sentence(m_chain, start_words, end_words, start_word=None, word_length=None):
        word = start_word if start_word else random.choice(list(start_words))
        length = word_length if word_length else random.randrange(10, 30)

        new_sentence = [word]
        while len(new_sentence) < length:
            # possible_next_words = k for k, v in m_chain[word]['next_words']
            next_word = random.choices(
                list(m_chain[word]['next_words'].keys()),
                weights=list(m_chain[word]['next_words'].values()))

            print(next_word)

            if next_word in end_words:
                if len(new_sentence) > 3:
                    new_sentence.append(next_word)
                    break
                else:
                    continue
            else:
                new_sentence.append(next_word)

            word = next_word


def fetch_source_data(api_endpoint_url, count=100):
    sentences = []
    for i in range(count):
        try:
            response = requests.get(url=api_endpoint_url, headers={
                "Accept": "text/plain"
            })
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        else:
            sentences.append(response.text)

    return sentences
