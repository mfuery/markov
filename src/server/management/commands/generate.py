from django.core.management.base import BaseCommand

from server.markov import MarkovChain
from server.models import TrainingSet, DataDomain


class Command(BaseCommand):
    help = 'Train and generate dad jokes from DB training dataset.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--min-length',
            type=int,
            default=15,
            help='Minimum length of sentence generated.')
        parser.add_argument(
            '-b',
            '--max-length',
            type=int,
            default=30,
            help='Maximum length of sentence generated.')
        parser.add_argument(
            'domain',
            type=str,
            help='Name of the domain of training set data to use.\n'
                 'One of: [dad_jokes|platitudes]')
        parser.add_argument(
            '-n',
            '--number',
            type=int,
            default=1,
            help='The number of sentences to generate.')

    def handle(self, *args, **kwargs):
        domain = DataDomain.objects.get(name=kwargs['domain'])
        training_set = TrainingSet.objects.filter(domain=domain)
        jokes = []
        for row in training_set:
            jokes.append(row.content)

        book = ' '.join(jokes)

        # Build chain.
        m_chain, start_words, end_words = MarkovChain.train(book)

        for i in range(kwargs['number']):
            sentence = MarkovChain.generate_sentence(
                m_chain,
                start_words,
                end_words,
                min_len=kwargs['min_length'],
                max_len=kwargs['max_length']
            )
            print(sentence)
