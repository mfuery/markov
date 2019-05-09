import random
import re


class MarkovChainText:
    @staticmethod
    def build_chain(text, m_chain=None, start_words=None, end_words=None):
        """
        Normally I would use NumPy tensors or Pandas DataFrames for all the
        heavy lifting. But if I understand the exercise correctly it is to build
        something from scratch.

        :return:
        """
        start_words = set() if start_words is None else start_words
        end_words = set() if end_words is None else end_words
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

        # Last word in the joke must be an end word.
        end_words.add(words[-1])

        # Find words that end a sentence for the converse reason we track
        # start words.
        for word in words:
            if word[-1] in ['.', '!', '?'] and word != '.':
                end_words.add(word)

        pm_chain = dict(m_chain)

        # print(json.dumps(m_chains, indent=4))
        # Calculate next_words probabilities.
        for word, metadata in m_chain.items():
            for next_word, count in metadata['next_words'].items():
                pm_chain[word]['next_words'][next_word]['prob'] = \
                    pm_chain[word]['next_words'][next_word]['count'] / metadata['total_count']

        # print(mydict(pm_chain), start_words, end_words)
        return pm_chain, start_words, end_words

    @staticmethod
    def generate_sentence(m_chain, start_words, end_words, start_word=None, word_length=None):
        word = start_word if start_word else random.choice(list(start_words))
        length = word_length if word_length else random.randrange(10, 30)

        new_sentence = [word]
        while len(new_sentence) < length:
            word_choices = list(
                {
                    k: k for k, v in m_chain[word]['next_words'].items()
                }.keys()
            )

            probs = list(
                {
                    k: v['prob'] for k, v in m_chain[word]['next_words'].items()
                }.values()
            )

            # Let's add that entropy!
            next_word = random.choices(word_choices, weights=probs)[0]

            if next_word in end_words:
                # Allow 2 word sentences, like "I am."
                if len(new_sentence) > 0:
                    new_sentence.append(next_word)
                    break
                else:
                    continue
            else:
                new_sentence.append(next_word)

            word = next_word

        return ' '.join(new_sentence)
