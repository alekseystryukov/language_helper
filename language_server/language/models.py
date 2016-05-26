from django.db import models

# Create your models here.

parts_of_speech = ('Verb', )


class Word(models.Model):
    name = models.CharField(max_length=50)
    translation = models.TextField(null=True, blank=True)
    part_of_speech_id = models.SmallIntegerField(null=True, blank=True)

    # verbs
    past_form = models.CharField(max_length=50, null=True, blank=True)
    participle_form = models.CharField(max_length=50, null=True, blank=True)

    @property
    def part_of_speech(self):
        if self.part_of_speech_id is None:
            return None
        return parts_of_speech[int(self.part_of_speech_id)]

    def __str__(self):
        return self.name
