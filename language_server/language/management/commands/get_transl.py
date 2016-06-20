from django.core.management.base import BaseCommand, CommandError
from language.utils import get_meanings, clear_word
from language.models import *


parts_of_speech = ('v', 'n', 'adj', 'adv')


class Command(BaseCommand):

    def handle(self, *args, **options):

        for w in Word.objects.filter(meanings__isnull=True):
            w.name = clear_word(w.name)
            w.save()

            for pos, decr in get_meanings(w.name):
                Meaning.objects.create(
                    word=w,
                    part_of_speech_id=parts_of_speech.index(pos),
                    description=decr,
                )
