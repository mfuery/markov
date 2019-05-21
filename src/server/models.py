from logging import getLogger
from django.db import models

logger = getLogger(__name__)


class DataSource(models.Model):
    """Data source for building Markov Chains"""
    url = models.URLField()


class DataDomain(models.Model):
    """
    What domain does this data belong to?
        Dad Jokes?
        Scientific Literature?
        Slang?
        Trump tweets?

    This is not a DataSource b/c a domain can pull from several data sources.
    """
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)


class TrainingSet(models.Model):
    """Text content of data retrieved from a given DataSource"""
    uuid = models.CharField(max_length=36, blank=False, db_index=True, unique=True)
    content = models.CharField(max_length=2048, blank=False)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    domain = models.ForeignKey(DataDomain, on_delete=models.CASCADE)


class GeneratedSentence(models.Model):
    """Generated content"""
    domain = models.ForeignKey(DataDomain, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=2048, blank=False)
    created = models.DateTimeField(auto_now=True)


class MarkovChainWord(models.Model):
    domain = models.ForeignKey(DataDomain, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, blank=False)
    next_word = models.CharField(max_length=255, blank=False)
    weight = models.FloatField(blank=False)

    class Meta:
        unique_together = ('domain', 'word', 'next_word',)

    # def recalculate_weights(self, domain=None):
    #     pass
    #
    # def save_chain(self, m_chain):
    #     for word in m_chain:
    #
    #
    #     try:
    #         MarkovChainWord.objects.create(
    #             domain
    #         )
    #     except models.AlreadyExists:
    #         pass
    #
    # def load_chain(self):
    #     chain = {}
    #     return chain


# class StartWords(models.Model):
#
# class EndWords(models.Model):
#
