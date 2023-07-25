from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import *

@registry.register_document
class Center_document(Document):
    class Index:
        name = 'center'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    class Django:
        model = Center
        fields = [
            'name_center',
            'address_center',
        ]