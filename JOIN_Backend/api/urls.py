from django.urls import path
from .views import UserView, ContactView, TaskView,api_dispatcher

urlpatterns = [
    path('', api_dispatcher, name='dispatcher'),
    
    path('users/', UserView.as_view(), name='users'),  # Neuer Endpunkt für Benutzer
    path('contacts/<str:user_email>/', ContactView.as_view(), name='contacts'),
    path('tasks/<str:user_email>/', TaskView.as_view(), name='tasks'),  # Neuer Endpunkt für Tasks
]