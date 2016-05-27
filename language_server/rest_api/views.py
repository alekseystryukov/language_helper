from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN, HTTP_200_OK

from language.models import Word
from .serializers import WordSerializer


class RandomWordApiView(RetrieveAPIView):
    serializer_class = WordSerializer
    permission_classes = tuple()

    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.all().order_by('?').first()
        except Word.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(data=self.serializer_class(word).data)