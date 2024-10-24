from rest_framework import serializers
from notes_app.models import Note


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'