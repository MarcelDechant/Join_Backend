

from rest_framework import viewsets
from .serializers import NotesSerializer
from notes_app.models import Note

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class= NotesSerializer