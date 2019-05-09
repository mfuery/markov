from .markov import MarkovChainText, fetch_source_data
import json


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


test_sentences = [
    "I finally bought the limited edition Thesaurus that I've always wanted. "
    "When I opened it, all the pages were blank. I have no words to describe "
    "how angry I am.",

    "I was fired from the keyboard factory yesterday. I wasn't putting in "
    "enough shifts.",

    "It doesn't matter how much you push the envelope. It will still be "
    "stationary."
]


def test_build_chain():
    m_chain, start_words, end_words = MarkovChainText.build_chain(
        test_sentences[0])
    assert m_chain == {
        "I": {
            "next_words": {
                "finally": {
                    "count": 2,
                    "prob": 0.4
                },
                "opened": {
                    "count": 1,
                    "prob": 0.2
                },
                "have": {
                    "count": 1,
                    "prob": 0.2
                },
                "am.": {
                    "count": 1,
                    "prob": 0.2
                }
            },
            "total_count": 5
        },
        "finally": {
            "next_words": {
                "bought": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "bought": {
            "next_words": {
                "the": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "the": {
            "next_words": {
                "limited": {
                    "count": 2,
                    "prob": 0.6666666666666666
                },
                "pages": {
                    "count": 1,
                    "prob": 0.3333333333333333
                }
            },
            "total_count": 3
        },
        "limited": {
            "next_words": {
                "edition": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "edition": {
            "next_words": {
                "Thesaurus": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "Thesaurus": {
            "next_words": {
                "that": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "that": {
            "next_words": {
                "I've": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "I've": {
            "next_words": {
                "always": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "always": {
            "next_words": {
                "wanted.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wanted.": {
            "next_words": {
                "When": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "When": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "opened": {
            "next_words": {
                "it,": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "it,": {
            "next_words": {
                "all": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "all": {
            "next_words": {
                "the": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "pages": {
            "next_words": {
                "were": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "were": {
            "next_words": {
                "blank.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "blank.": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "have": {
            "next_words": {
                "no": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "no": {
            "next_words": {
                "words": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "words": {
            "next_words": {
                "to": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "to": {
            "next_words": {
                "describe": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "describe": {
            "next_words": {
                "how": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "how": {
            "next_words": {
                "angry": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "angry": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        }
    }
    assert start_words == {'When', 'I'}
    assert end_words == {'blank.', 'am.', 'wanted.'}


def test_build_chain_run_two_times():
    m_chain, start_words, end_words = MarkovChainText.build_chain(
        test_sentences[0])
    m_chain, start_words, end_words = MarkovChainText.build_chain(
        test_sentences[1], m_chain, start_words, end_words)

    print(mydict(m_chain), start_words, end_words)

    assert m_chain == {
        "I": {
            "next_words": {
                "finally": {
                    "count": 2,
                    "prob": 0.2857142857142857
                },
                "opened": {
                    "count": 1,
                    "prob": 0.14285714285714285
                },
                "have": {
                    "count": 1,
                    "prob": 0.14285714285714285
                },
                "am.": {
                    "count": 1,
                    "prob": 0.14285714285714285
                },
                "was": {
                    "count": 1,
                    "prob": 0.14285714285714285
                },
                "wasn't": {
                    "count": 1,
                    "prob": 0.14285714285714285
                }
            },
            "total_count": 7
        },
        "finally": {
            "next_words": {
                "bought": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "bought": {
            "next_words": {
                "the": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "the": {
            "next_words": {
                "limited": {
                    "count": 2,
                    "prob": 0.5
                },
                "pages": {
                    "count": 1,
                    "prob": 0.25
                },
                "keyboard": {
                    "count": 1,
                    "prob": 0.25
                }
            },
            "total_count": 4
        },
        "limited": {
            "next_words": {
                "edition": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "edition": {
            "next_words": {
                "Thesaurus": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "Thesaurus": {
            "next_words": {
                "that": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "that": {
            "next_words": {
                "I've": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "I've": {
            "next_words": {
                "always": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "always": {
            "next_words": {
                "wanted.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wanted.": {
            "next_words": {
                "When": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "When": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "opened": {
            "next_words": {
                "it,": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "it,": {
            "next_words": {
                "all": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "all": {
            "next_words": {
                "the": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "pages": {
            "next_words": {
                "were": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "were": {
            "next_words": {
                "blank.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "blank.": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "have": {
            "next_words": {
                "no": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "no": {
            "next_words": {
                "words": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "words": {
            "next_words": {
                "to": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "to": {
            "next_words": {
                "describe": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "describe": {
            "next_words": {
                "how": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "how": {
            "next_words": {
                "angry": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "angry": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "was": {
            "next_words": {
                "fired": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "fired": {
            "next_words": {
                "from": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "from": {
            "next_words": {
                "the": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "keyboard": {
            "next_words": {
                "factory": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "factory": {
            "next_words": {
                "yesterday.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "yesterday.": {
            "next_words": {
                "I": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wasn't": {
            "next_words": {
                "putting": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "putting": {
            "next_words": {
                "in": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "in": {
            "next_words": {
                "enough": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "enough": {
            "next_words": {
                "shifts.": {
                    "count": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        }
    }

    assert start_words == {'When', 'I'}
    assert end_words == {'am.', 'blank.', 'yesterday.', 'shifts.', 'wanted.'}


def test_generate_sentence():
    m_chain, start_words, end_words = MarkovChainText.build_chain(
        test_sentences[0])
    actual = MarkovChainText.generate_sentence(
        m_chain,
        start_words,
        end_words
    )
    print(actual)
    assert len(actual) > 1
