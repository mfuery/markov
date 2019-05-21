from django.core.management.base import BaseCommand

from server.markov import MarkovChain
from server.models import TrainingSet, DataDomain


class Command(BaseCommand):
    help = 'Train and generate dad jokes from DB training dataset.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            type=int,
            default=1,
            help='The number of Dad Jokes to generate.')

    def handle(self, *args, **kwargs):
        domain = DataDomain.objects.get(name='dad_jokes')
        training_set = TrainingSet.objects.filter(domain=domain)
        jokes = []
        for row in training_set:
            jokes.append(row.content)

        book = ' '.join(jokes)

        # Build chain.
        m_chain, start_words, end_words = MarkovChain.train(book)

        sentences = []
        for i in range(kwargs['number']):
            sentence = MarkovChain.generate_sentence(m_chain, start_words, end_words)
            sentences.append(sentence)
            print(sentence)
