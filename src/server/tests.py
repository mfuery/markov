from django.test import TestCase
from .markov import MarkovChainText


class MarkovChainTextTest:
    test_sentences = [
        "I finally bought the limited edition Thesaurus that I've always wanted. "
        "When I opened it, all the pages were blank. I have no words to describe "
        "how angry I am.",

        "I was fired from the keyboard factory yesterday. I wasn't putting in "
        "enough shifts.",
    ]

    def test_build_chain(self):
        """Todo assert some things"""
        MarkovChainText.build_chain(self.test_sentences)


def test_fetch_source_data(self):
    """Todo"""
    pass
