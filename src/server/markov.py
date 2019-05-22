import random
import re


class FitnessFn:
    """
    These fitness functions borrowed from here:
    https://medium.com/@G3Kappa/writing-a-weight-adjustable-markov-chain-based-text-generator-in-python-9bbde6437fb4
    """

    @staticmethod
    def favor_simplicity(a, b):
        return len(set([c for c in a + b])) / len(a + b)

    @staticmethod
    def favor_complexity(a, b):
        return 1 - FitnessFn.favor_simplicity(a, b)

    @staticmethod
    def favor_alternating_complexity(a, b):
        return (FitnessFn.favor_simplicity(b, b) + FitnessFn.favor_complexity(a, a)) / 2

    @staticmethod
    def favor_rhymes(a, b):
        a, b = sorted([a, b], key=min)
        return sum([1 if p[0] == p[1] else 0 for p in zip(b[len(b) - len(a):], a)]) / len(a)

    @staticmethod
    def favor_alliterations(a, b):
        a, b = sorted([a, b], key=min)
        return sum([1 if p[0] == p[1] else 0 for p in zip(b[:len(b) - len(a)], a)]) / len(a)

    @staticmethod
    def favor_vowels(a, b):
        return sum([1 if c in 'aeiouy' else 0 for c in a + b]) / len(a + b)

    @staticmethod
    def favor_consonants(a, b):
        return 1 - FitnessFn.favor_vowels(a, b)

    @staticmethod
    def favor_punctuation(a, b):
        return sum(map(lambda x: 0.5 if x[-1] in '.,;?!:()[]{}' else 0, [a, b]))

    @staticmethod
    def favor_illegibility(a, b):
        return 1 - FitnessFn.favor_punctuation(a, b)

    @staticmethod
    def mul(f, k):
        """
        Returns a fitness function multiplied by a constant k.
        """
        return lambda a, b: f(a, b) * k


class MarkovChain:
    SANITIZE_RE = r"[^a-zA-Z0-9']*"
    PUNCTUATION = {
        '!': 0.15,
        '?': 0.25,
        '.': 0.45,
        ',': 0.10,
        ';': 0.05,
    }
    ENDING_PUNCTUATION = {
        '!': 0.15,
        '?': 0.25,
        '.': 0.60,
    }

    @staticmethod
    def get_random_punctuation():
        return random.choices(
            list(MarkovChain.PUNCTUATION.keys()),
            weights=list(MarkovChain.PUNCTUATION.values())
        )[0]

    @staticmethod
    def get_random_ending_punctuation():
        return random.choices(
            list(MarkovChain.ENDING_PUNCTUATION.keys()),
            weights=list(MarkovChain.ENDING_PUNCTUATION.values())
        )[0]

    @staticmethod
    def train(text, m_chain=None, start_words=None, end_words=None, factor=1):
        """
        Normally I would use NumPy tensors or Pandas DataFrames for all the
        heavy lifting. But if I understand the exercise correctly it is to build
        something from scratch.

        :param text:
        :param m_chain: dict
        :param start_words: set
        :param end_words: set
        :param factor: float Increasing this gives more influence to the
        weightings generated from this block of text
        :return:
        """
        start_words = set() if start_words is None else start_words
        end_words = set() if end_words is None else end_words
        m_chain = {} if m_chain is None else m_chain

        # Split words on any whitespace, strip out double quotes.
        # Todo: would it be useful to keep track of which words occur inside
        #  double quotes?
        words = filter(lambda s: len(s) > 0, re.split(r"[\s\"]+", text))

        # Lowercase everything so the chain builds case-insensitive.
        words = [w.lower() for w in words]

        # Have a special class of words: start words, so we can have a
        # better chance of the joke sounding "natural".
        start_words.add(re.sub(MarkovChain.SANITIZE_RE, '', words[0]))

        # Count all of the words.
        for i in range(0, len(words) - 1):
            word = words[i]
            next_word = words[i + 1]

            if word[-1] in ['.', '!', '?'] and word != '.':
                start_words.add(re.sub(MarkovChain.SANITIZE_RE, '', next_word))

            # Strip non-alphanumerics.
            word = re.sub(MarkovChain.SANITIZE_RE, '', word)
            next_word = re.sub(MarkovChain.SANITIZE_RE, '', next_word)

            if word not in m_chain:
                m_chain[word] = {
                    'next_words': {
                        next_word: {
                            'weight': 1 * factor,
                            'prob': None
                        }
                    },
                    'total_count': 1
                }
            if next_word not in m_chain[word]['next_words']:
                m_chain[word]['next_words'][next_word] = {
                    'weight': 1 * factor,
                    'prob': None
                }
            else:
                m_chain[word]['next_words'][next_word]['weight'] += 1 * factor

            m_chain[word]['total_count'] += 1

        # Last word in the joke must be an end word.
        end_words.add(re.sub(MarkovChain.SANITIZE_RE, '', words[-1]))

        # Find words that end a sentence for the converse reason we track
        # start words.
        for word in words:
            if word[-1] in ['.', '!', '?'] and word != '.':
                end_words.add(re.sub(MarkovChain.SANITIZE_RE, '', word))

        # Calculate next_words probabilities.
        pm_chain = MarkovChain.recalculate_probabilities(m_chain)

        # print(mydict(pm_chain), start_words, end_words)
        return pm_chain, start_words, end_words

    @staticmethod
    def generate_sentence(m_chain, start_words=None, end_words=None, start_word=None, min_len=15, max_len=30):
        if not start_words:
            start_words = list(m_chain.keys())

        word = start_word if start_word else random.choice(list(start_words))
        length = max_len if min_len == max_len else random.randrange(min_len, max_len)

        new_sentence = [word]
        while len(new_sentence) < length - 1:
            # Occasionally, a word has no next_words, e.g. "provalone!". Skip.
            if word not in m_chain:
                new_sentence[-1] += MarkovChain.get_random_punctuation()
                word = random.choice(list(start_words))
                continue

            word_choices = list(
                k for k in m_chain[word]['next_words'].keys()
            )
            probs = list(
                v['prob'] for v in m_chain[word]['next_words'].values()
            )

            # Let's add that entropy!
            if word in end_words:
                new_sentence[-1] += MarkovChain.get_random_ending_punctuation()

                # If we just ended a sentence, use a start word!
                next_word = random.choices(list(start_words))[0]
            else:
                next_word = random.choices(word_choices, weights=probs)[0]

            new_sentence.append(next_word)
            word = next_word

        # Always end with an end word, if available.
        if end_words and new_sentence[-1] not in end_words:
            new_sentence.append(random.choice(list(end_words)))

        new_sentence[-1] += MarkovChain.get_random_ending_punctuation()

        return ' '.join(new_sentence)

    @staticmethod
    def apply_fitness(m_chain, f, recalculate_probabilities=True):
        """
        Modifies chain in-place for a random pair of generated words.

        :param m_chain: MarkovChain
        :param f:
        :param factor:
        :param recalculate_probabilities:
        :return:
        """
        generated_pair = MarkovChain.generate_sentence(m_chain, min_len=2, max_len=2)
        print(m_chain)
        print(generated_pair)
        a, b = re.split(r'\s+', re.sub(MarkovChain.SANITIZE_RE, '', generated_pair))
        print(a, b)
        factor = f(a, b)
        m_chain[a]['next_words'][b]['weight'] *= factor

        if recalculate_probabilities:
            for next_word in m_chain[a]['next_words']:
                m_chain[a]['next_words'][next_word]['prob'] = \
                    m_chain[a]['next_words'][next_word]['weight'] / m_chain[a]['total_count']
        print(m_chain)
        return m_chain

    @staticmethod
    def recalculate_probabilities(m_chain):
        pm_chain = dict(m_chain)
        for word, metadata in m_chain.items():
            for next_word, count in metadata['next_words'].items():
                pm_chain[word]['next_words'][next_word]['prob'] = \
                    pm_chain[word]['next_words'][next_word]['weight'] / pm_chain[word]['total_count']

        return pm_chain
