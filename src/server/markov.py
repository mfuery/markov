import random

import requests
from requests import HTTPError


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
    def build_chain(text):
        """
        Normally I would use NumPy tensors or Pandas DataFrames for all the
        heavy lifting. But if I understand the exercise correctly it is to build
        something from scratch.

        :return:
        """
        start_words = set()
        end_words = set()
        m_chains = {}

        # Have a special class of words: start words, so we can have a
        # better chance of the joke sounding "natural".
        words = text.split(r'\s+')
        start_words.add(words[0])

        # Count all of the words.
        for i in range(0, len(words) - 1):
            word = words[i]
            next_word = words[i + 1]

            if word not in m_chains:
                m_chains[word] = {
                    'next_words': {
                        next_word: 1
                    },
                    'total_count': 1
                }
            if next_word not in m_chains[word]['next_words']:
                m_chains[word]['next_words'][next_word] = 1
            else:
                m_chains[word]['next_words'][next_word] += 1

            m_chains[word]['total_count'] += 1

        end_words.add(words[-1])

        # Find words that end a sentence for the converse reason we track
        # start words.
        for word in words:
            if word[-1] in ['.', '!', '?'] and word != '.':
                end_words.add(word)

        # Convert counts to probabilities.
        for word in m_chains:
            for next_word in word['next_words']:
                word['next_words'][next_word] /= word['total_count']

        return m_chains, start_words, end_words

    @staticmethod
    def generate_sentence(m_chain, start_words, end_words, start_word=None, word_length=None):
        word = start_word if start_word else random.choice(start_words)
        length = word_length if word_length else random.randrange(10, 30)

        new_sentence = [word]
        while len(new_sentence) < length:
            next_word = random.choices(
                m_chain[word]['next_words'].keys(),
                weights=m_chain[word]['next_words'].values())

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
