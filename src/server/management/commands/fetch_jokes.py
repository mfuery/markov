from django.core.management.base import BaseCommand
from django.db import transaction

from server import dad_jokes
from server.models import DataSource, TrainingSet


class Command(BaseCommand):
    help = 'Fetch Data Jokes From ICANHAZDADJOKES'

    def add_arguments(self, parser):
        parser.add_argument(
            'total',
            type=int,
            help='Indicates the number of Dad Jokes to download and save to db')

    def handle(self, *args, **kwargs):
        data_sources = DataSource.objects.filter(data_domain__name='dad_jokes')
        resultset = dad_jokes.fetch_jokes(data_sources, kwargs['total'])

        # Combine results of requests into one list. We don't care about request
        # metadata at this point.
        jokeset = []
        for result in resultset:
            jokeset += result['results']
        print(jokeset)

        # with transaction.atomic():
        #     for jokes in jokeset:
        #         for joke in jokes.results:
        #             joke = TrainingSet.objects.get_or_create(uuid=joke['id'])
        #
        #             if (joke.percentile is None) or np.isnan(row.percentile):
        #                 # if it's already None, why set it to None?
        #                 row.percentile = None
        #
        #             mv.percentile = row.percentile
        #             mv.save()
