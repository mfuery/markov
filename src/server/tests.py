from .markov import MarkovChain, FitnessFn
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
    m_chain, start_words, end_words = MarkovChain.train(test_sentences[0])
    # print(mydict(m_chain))
    assert m_chain == {
        "i": {
            "next_words": {
                "finally": {
                    "weight": 2,
                    "prob": 0.4
                },
                "opened": {
                    "weight": 1,
                    "prob": 0.2
                },
                "have": {
                    "weight": 1,
                    "prob": 0.2
                },
                "am.": {
                    "weight": 1,
                    "prob": 0.2
                }
            },
            "total_count": 5
        },
        "finally": {
            "next_words": {
                "bought": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "bought": {
            "next_words": {
                "the": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "the": {
            "next_words": {
                "limited": {
                    "weight": 2,
                    "prob": 0.6666666666666666
                },
                "pages": {
                    "weight": 1,
                    "prob": 0.3333333333333333
                }
            },
            "total_count": 3
        },
        "limited": {
            "next_words": {
                "edition": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "edition": {
            "next_words": {
                "thesaurus": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "thesaurus": {
            "next_words": {
                "that": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "that": {
            "next_words": {
                "i've": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "i've": {
            "next_words": {
                "always": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "always": {
            "next_words": {
                "wanted.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wanted.": {
            "next_words": {
                "when": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "when": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "opened": {
            "next_words": {
                "it,": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "it,": {
            "next_words": {
                "all": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "all": {
            "next_words": {
                "the": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "pages": {
            "next_words": {
                "were": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "were": {
            "next_words": {
                "blank.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "blank.": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "have": {
            "next_words": {
                "no": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "no": {
            "next_words": {
                "words": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "words": {
            "next_words": {
                "to": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "to": {
            "next_words": {
                "describe": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "describe": {
            "next_words": {
                "how": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "how": {
            "next_words": {
                "angry": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "angry": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        }
    }
    assert start_words == {
        'i',
        'when'
    }
    assert end_words == {
        'wanted.',
        'blank.',
        'am.'
    }


def test_build_chain_run_two_times():
    m_chain, start_words, end_words = MarkovChain.train(
        test_sentences[0])
    m_chain, start_words, end_words = MarkovChain.train(
        test_sentences[1], m_chain, start_words, end_words)
    print(mydict(m_chain), start_words, end_words)

    assert m_chain == {
        "i": {
            "next_words": {
                "finally": {
                    "weight": 2,
                    "prob": 0.2857142857142857
                },
                "opened": {
                    "weight": 1,
                    "prob": 0.14285714285714285
                },
                "have": {
                    "weight": 1,
                    "prob": 0.14285714285714285
                },
                "am.": {
                    "weight": 1,
                    "prob": 0.14285714285714285
                },
                "was": {
                    "weight": 1,
                    "prob": 0.14285714285714285
                },
                "wasn't": {
                    "weight": 1,
                    "prob": 0.14285714285714285
                }
            },
            "total_count": 7
        },
        "finally": {
            "next_words": {
                "bought": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "bought": {
            "next_words": {
                "the": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "the": {
            "next_words": {
                "limited": {
                    "weight": 2,
                    "prob": 0.5
                },
                "pages": {
                    "weight": 1,
                    "prob": 0.25
                },
                "keyboard": {
                    "weight": 1,
                    "prob": 0.25
                }
            },
            "total_count": 4
        },
        "limited": {
            "next_words": {
                "edition": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "edition": {
            "next_words": {
                "thesaurus": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "thesaurus": {
            "next_words": {
                "that": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "that": {
            "next_words": {
                "i've": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "i've": {
            "next_words": {
                "always": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "always": {
            "next_words": {
                "wanted.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wanted.": {
            "next_words": {
                "when": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "when": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "opened": {
            "next_words": {
                "it,": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "it,": {
            "next_words": {
                "all": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "all": {
            "next_words": {
                "the": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "pages": {
            "next_words": {
                "were": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "were": {
            "next_words": {
                "blank.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "blank.": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "have": {
            "next_words": {
                "no": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "no": {
            "next_words": {
                "words": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "words": {
            "next_words": {
                "to": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "to": {
            "next_words": {
                "describe": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "describe": {
            "next_words": {
                "how": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "how": {
            "next_words": {
                "angry": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "angry": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "was": {
            "next_words": {
                "fired": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "fired": {
            "next_words": {
                "from": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "from": {
            "next_words": {
                "the": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "keyboard": {
            "next_words": {
                "factory": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "factory": {
            "next_words": {
                "yesterday.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "yesterday.": {
            "next_words": {
                "i": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "wasn't": {
            "next_words": {
                "putting": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "putting": {
            "next_words": {
                "in": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "in": {
            "next_words": {
                "enough": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        },
        "enough": {
            "next_words": {
                "shifts.": {
                    "weight": 2,
                    "prob": 1.0
                }
            },
            "total_count": 2
        }
    }

    assert start_words == {
        'i',
        'when'
    }
    assert end_words == {
        'wanted.',
        'yesterday.',
        'shifts.',
        'blank.',
        'am.'
    }


def test_generate_sentence():
    m_chain, start_words, end_words = MarkovChain.train(
        test_sentences[0])
    actual = MarkovChain.generate_sentence(
        m_chain,
        start_words,
        end_words
    )
    print(actual)
    assert len(actual) > 1


def test_apply_fitness():
    m_chain = {
        "finally": {
            "next_words": {
                "bought": {
                    "weight": 1,
                    "prob": 1.0
                },
            },
            "total_count": 1
        },
    }

    assert MarkovChain.apply_fitness(m_chain, f=lambda a, b: a) == {
        "finally": {
            "next_words": {
                "bought": {
                    "weight": 2,
                    "prob": 1.0
                },
            },
            "total_count": 1
        },
    }
