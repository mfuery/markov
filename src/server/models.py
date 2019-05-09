import math

import requests
from logging import getLogger
from django.db import models
from requests import HTTPError

logger = getLogger(__name__)


class DataSources(models.Model):
    """Data source for building Markov Chains"""
    url = models.URLField()



    @staticmethod
    def fetch_jokes(api_endpoint_url, count=100, current_page=1):
        results = []

        n_requests = math.floor(count / MAX_JOKE_REQUEST_SIZE)
        n_requests += 1 if count % MAX_JOKE_REQUEST_SIZE > 0 else 0
        print(n_requests)

        for i in range(n_requests):
            limit = count % MAX_JOKE_REQUEST_SIZE if i == n_requests else MAX_JOKE_REQUEST_SIZE
            try:
                response = requests.get(
                    url=api_endpoint_url,
                    headers={
                        "Accept": "application/json"
                    },
                    params={
                        "limit": limit,
                        "page": current_page
                    }
                )
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            else:
                results.append(response.json())
                current_page += 1

        return results


class DataDomains(models.Model):
    """What is this? Dad Joke? Scientific Literature? Slang?"""
    data_source = models.ForeignKey(DataSources, on_delete=models.CASCADE)


class TrainingSets(models.Model):
    """Text content of data retrieved from a given DataSource"""
    uuid = models.CharField(max_length=36, blank=False, db_index=True, unique=True)
    content = models.CharField(max_length=2048, blank=False)
    data_source = models.ForeignKey(DataSources, on_delete=models.CASCADE)
    domain = models.ForeignKey(DataDomains, on_delete=models.CASCADE)


class GeneratedSentences(models.Model):
    """Generated content"""
    domain = models.ForeignKey(DataDomains, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=2048, blank=False)
    created = models.DateTimeField(auto_now=True)


class MarkovChainWords(models.Model):
    domain = models.ForeignKey(DataDomains, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, blank=False)
    next_word = models.CharField(max_length=255, blank=False)
    weight = models.FloatField(blank=False)

