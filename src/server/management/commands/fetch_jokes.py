from django.core.management.base import BaseCommand

from server.api import dad_jokes
from server.models import DataSource, TrainingSet, DataDomain


class Command(BaseCommand):
    help = 'Fetch Data Jokes From ICANHAZDADJOKES API'

    def handle(self, *args, **kwargs):
        domain = DataDomain.objects.get(name='dad_jokes')
        data_sources = DataSource.objects.filter(datadomain=domain)

        # Download data from source(s).
        for data_source in data_sources:
            result_set = dad_jokes.fetch_jokes(data_source.url, kwargs['total'])

            # Combine results of requests into one list. We don't care about
            # request metadata here.
            joke_set = []
            for result in result_set:
                joke_set += result['results']

            # Todo: combine into single bulk upsert.
            for joke in joke_set:
                TrainingSet.objects.get_or_create(
                    uuid=joke['id'],
                    defaults={
                        'content': joke['joke'],
                        'data_source': data_source,
                        'domain': domain
                    }
                )
