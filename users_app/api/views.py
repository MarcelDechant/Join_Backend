

from rest_framework import viewsets
from .serializers import UserSerializer
from users_app.models import User

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= UserSerializer