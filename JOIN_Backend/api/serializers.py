from rest_framework import serializers
from JOIN_Backend.models import User, Contact, Task

class UserSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(required=False)

class ContactSerializer(serializers.ModelSerializer):
    contactId = serializers.UUIDField()
    
    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        contact_id = validated_data.get('contactId', None)

        if not contact_id:
            raise serializers.ValidationError("contactId is required")
        validated_data['contactId'] = contact_id
        contact = Contact(**validated_data)
        contact.save()
       
        return contact

class TaskSerializer(serializers.ModelSerializer):
    subTasks = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField()
        ),
        default=list
    )
    contacts = serializers.ListField(
        child=serializers.CharField(), 
        default=list
    )

    class Meta:
        model = Task
        fields = ['id', 'user', 'category', 'title', 'description', 'date', 'priority', 'status', 'subTasks', 'contacts']