from django.db import models
from .utils import *

# Create your models here.

parts_of_speech = ('Verb', 'Noun', 'Adjective', 'Adverb', 'Pronoun',
                   'Preposition', 'Conjunction', 'Interjection')

short_pos = ('v', 'n', 'adj', 'adv')


class Word(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_with_meanings(cls, name):
        name = clear_word(name)
        try:
            word = cls.objects.get(name=name)
        except cls.DoesNotExist:
            pass
        else:
            return word

        meanings = get_meanings(name)
        if meanings:
            word = cls.objects.create(name=name)
            for pos, desc in meanings:
                Meaning.objects.create(
                    word=word,
                    part_of_speech_id=short_pos.index(pos),
                    description=desc,
                )
            return word

    @property
    def meanings_list(self):
        return [(m.part_of_speech, m.description) for m in self.meanings.all()]


class Meaning(models.Model):
    word = models.ForeignKey(Word, related_name='meanings')
    part_of_speech_id = models.SmallIntegerField(null=True, blank=True)
    description = models.CharField(max_length=200)

    @property
    def part_of_speech(self):
        if self.part_of_speech_id is None:
            return None
        return parts_of_speech[int(self.part_of_speech_id)]

    def __str__(self):
        return "%s - %s" % (self.part_of_speech, self.description)
