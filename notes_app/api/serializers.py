from rest_framework import serializers
from notes_app.models import Note, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'note', 'title', 'is_completed', 'created_at', 'updated_at']


class NotesSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'category', 'title', 'description', 'prio', 'created_at', 'updated_at', 'subtasks']