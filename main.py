import random

import requests
from requests import HTTPError

API_ENDPOINT = "https://icanhazdadjoke.com/"


class MarkovSentences:
    def __init__(self):
        self.sentences = []

        self.start_words = set()
        self.end_words = set()

        # Hash key is WORD__NEXTWORD
        self.counts = {}

        # Look up a hash key given a word.
        self.count_lookup = {}

        self.total_word_count = 0
        self.all_words = []

    def build(self):
        for sentence in self.sentences:
            words = sentence.split(' ')
            self.start_words.add(words[0])
            hash_key = ''

            # Count all of the words.
            for i in range(len(words) - 1):
                word = words[i]
                next_word = words[i + 1]
                hash_key = f'{word}__{next_word}'

                self.counts[hash_key] = {
                    'freq': self.counts[hash_key] + 1 if hash_key in self.counts else 1,
                    'word': word,
                    'next_word': next_word,
                    'prob': 0
                }
                self.count_lookup[word] = hash_key
                self.total_word_count = self.total_word_count + 1

            self.counts[hash_key]['next_word'] = 'END_WORD'

            # Find words that end a sentence.
            for word in words:
                if word[-1] in ['.', '!', '?'] and word != '.':
                    self.end_words.add(word)

        # for item in self.counts:
        #     item['prob'] = 1 / self.total_word_count
        #     self.probabilities.append(item['prob'])
        #     self.all_words.append(item['word'])

    def build_pivot_table(self, word):
        hash_keys = self.count_lookup[word]
        total_count = len(hash_keys)

        for hash_key in hash_keys:
            item = self.counts[hash_key]


    def build_pivot_tables(self):
        """
        Memoizing the pivot tables for each set of next_word & its probability
        with respect to any given word is likely to speed up sentence generation
        assuming you are generating lots of sentences. If you're only generating
        one or a handful then on-the-fly probability calculation of our word
        corpus is likely to be faster overall because the initial build step
        would be quicker.

        :return:
        """

    def set_source_data(self, sentences):
        self.sentences = sentences

    def fetch_source_data(self, api_endpoint_url, count):
        for i in range(count):
            try:
                response = requests.get(url=api_endpoint_url, headers={
                    "Accept": "text/plain"
                })
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            else:
                self.sentences.append(response.text)

    def generate_sentence(self, start_word=None, word_length=None):
        start_word = start_word if start_word \
            else random.choice(self.start_words)
        length = word_length if word_length \
            else random.randrange(10, 30)

        new_sentence = [start_word]
        while len(new_sentence) < length:
            next_word = random.choices(self.all_words, weights=self.probabilities)

            if next_word == 'END_WORD':
                continue
            elif next_word in self.end_words:
                if len(new_sentence) > 3:
                    new_sentence.append(next_word)
                    break
                else:
                    continue
            else:
                new_sentence.append(next_word)


test_data = [
    "I finally bought the limited edition Thesaurus that I've always wanted. When I opened it, all the pages were blank. I have no words to describe how angry I am.",
    "I was fired from the keyboard factory yesterday. I wasn't putting in enough shifts.",
]
m = MarkovSentences()
m.set_source_data(test_data)
m.build()
print(m.sentences)
print(m.counts)
print(m.count_lookup)
print(m.start_words)
print(m.end_words)
print(m.total_word_count)
m.generate_sentence()

# Strip non words
# for test_case in test_data:
#     sanitized = test_case.lower()
#     sanitized = re.sub(r'[^a-z ]*', '', sanitized)
#     words = sanitized.split(' ')
