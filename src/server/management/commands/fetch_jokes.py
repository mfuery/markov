import json

from django.core.management.base import BaseCommand

from server import dad_jokes
from server.markov import MarkovChainText
from server.models import DataSource, TrainingSet, DataDomain


# This is for debugging.
class mydict(dict):
    def __str__(self):
        return json.dumps(self)


class Command(BaseCommand):
    help = 'Fetch Data Jokes From ICANHAZDADJOKES'

    def add_arguments(self, parser):
        parser.add_argument(
            'total',
            type=int,
            help='Indicates the number of Dad Jokes to download and save to db')

    def handle(self, *args, **kwargs):
        domain = DataDomain.objects.get(name='dad_jokes')
        data_sources = DataSource.objects.filter(datadomain=domain)

        # Download data from source(s).
        for data_source in data_sources:
            resultset = dad_jokes.fetch_jokes(data_source.url, kwargs['total'])

            # Combine results of requests into one list. We don't care about
            # request metadata here.
            jokeset = []
            for result in resultset:
                jokeset += result['results']

            # Todo: combine into single bulk upsert.
            for joke in jokeset:
                row = TrainingSet.objects.get_or_create(
                    uuid=joke['id'],
                    defaults={
                        'content': joke['joke'],
                        'data_source': data_source,
                        'domain': domain
                    }
                )

        training_set = TrainingSet.objects.filter(domain=domain)
        jokes = []
        for row in training_set:
            jokes.append(row.content)

        book = ' '.join(jokes)

        # Build chain.
        m_chain, start_words, end_words = MarkovChainText.build_chain(book)

        # print(mydict(m_chain), start_words, end_words)

        print(f"\nHere are some generated sentences:\n")
        sentences = []
        for i in range(20):
            sentence = MarkovChainText.generate_sentence(m_chain, start_words, end_words)
            sentences.append(sentence)
            print(sentence)
