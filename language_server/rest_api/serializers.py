from rest_framework.serializers import ModelSerializer, ListField, SerializerMethodField
from language.models import Word, Meaning


class WordSerializer(ModelSerializer):

    meanings_list = ListField()

    class Meta:
        model = Word


class WordTestSerializer(WordSerializer):

    meanings = SerializerMethodField()

    def get_meanings(self, obj):
        meanings_list = obj.meanings_list

        meanings = []
        if meanings_list:
            meanings.append({'text': meanings_list[0][1], 'right': True})

        meanings += [{'text': m.description, 'right': False}
                     for m in Meaning.objects.exclude(word=obj).order_by('?')[:2]]

        return sorted(meanings, key=lambda i: i['text'])
