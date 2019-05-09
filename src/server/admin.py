from django.contrib import admin
from server.models import (
    DataSource,
    DataDomain,
    TrainingSet,
    GeneratedSentence,
    MarkovChainWord,
)

admin.site.register(DataSource)
admin.site.register(DataDomain)
admin.site.register(TrainingSet)
admin.site.register(GeneratedSentence)
admin.site.register(MarkovChainWord)
