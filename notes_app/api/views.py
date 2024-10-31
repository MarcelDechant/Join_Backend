

from rest_framework import viewsets
from .serializers import NotesSerializer, SubtaskSerializer
from notes_app.models import Note ,Subtask


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class= NotesSerializer
    
    
class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer