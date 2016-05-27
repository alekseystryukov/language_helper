from rest_framework.serializers import ModelSerializer
from language.models import Word


class WordSerializer(ModelSerializer):

    class Meta:
        model = Word
