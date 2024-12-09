from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from JOIN_Backend.models import User, Contact, Task
from .serializers import UserSerializer, ContactSerializer, TaskSerializer

import json
from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from django.test.client import RequestFactory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest
import uuid

def debuggin_post(request):
    
    if request.method == 'POST':
        # Ausgabe der Anfrage-Details im Terminal
        print("POST-Anfrage empfangen:")
        print(f"Pfad: {request.path}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Body: {request.body.decode('utf-8')}")
    
    return JsonResponse({"message": "Anfrage verarbeitet"})

@csrf_exempt
def api_dispatcher(request):
    debuggin_post(request)
    print("Anfrage-Objekt:", request)
    
    
    API_VIEWS = {
        "users": UserView,
        "contacts": ContactView,
        "tasks": TaskView,
    }

    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
    
    try:
        body = json.loads(request.body)
        key = body.get('key')
        print("Body nach JSON-Parsing:", body)
        print("Extrahierter Schlüssel (key):", key)

        if not key:
            print("Fehler: Key fehlt im Body")
            return JsonResponse({"status": "error", "message": "Key is missing"}, status=400)
        
        if "/" in key:
            key_parts = key.split("/", 1)  # Nur in zwei Teile aufteilen
            resource_key = key_parts[0]
            identifier = key_parts[1]
            print("Resource Key:", resource_key)
            print("Identifier:", identifier)      

            if resource_key in ["tasks", "contacts"]:
                view_class = API_VIEWS.get(resource_key)
                if not view_class:
                    print("Fehler: Unbekannter Resource Key:", resource_key)
                    return JsonResponse(
                        {"status": "error", "message": f"Unknown resource key: {resource_key}"},
                        status=400,
                    )

                # Add user_email to the request object
                request.user_email = identifier
                print(f"Weiterleitung an View: {view_class.__name__} mit user_email: {identifier}")
                return view_class.as_view()(request)
            
            else:
                print(f"Fehler: Zweiteiliger Key ist für Ressource '{resource_key}' nicht erlaubt")
                return JsonResponse(
                    {"status": "error", "message": f"Invalid two-part key for resource: {resource_key}"},
                    status=400,
                )
        else:
            # Einteiliger Key: Nur für "users" erlaubt
            view_class = API_VIEWS.get(key)
            if not view_class:
                print(f"Fehler: Unbekannter Key '{key}'")
                return JsonResponse(
                    {"status": "error", "message": f"Unknown key: {key}"},
                    status=400,
                )

            print(f"Weiterleitung an View: {view_class.__name__}")
            return view_class.as_view()(request)


    except json.JSONDecodeError:
        print("Fehler: Ungültiges JSON")
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Unerwarteter Fehler: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    parser_classes = [JSONParser]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Incoming user data for creation:", [{"email": d.get('email')} for d in request.data.get('value', [])])

        data = request.data.get('value', [])
        if not data:
            return Response({"detail": "Missing 'value' field in request."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data, many=True)

        if serializer.is_valid():
            created_users = []
            skipped_users = []

            for user_data in serializer.validated_data:
                email = user_data.get('email')

                if User.objects.filter(email=email).exists():
                    skipped_users.append(user_data)
                    continue

                User.objects.create(**user_data)
                created_users.append(user_data)

            return Response({
                "created": created_users,
                "skipped": skipped_users,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    def get(self, request, user_email):
        # Benutzer anhand der E-Mail finden
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Tasks für diesen Benutzer holen
        tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
    # Nutzer-Email aus dem Dispatcher holen
        user_email = getattr(request, 'user_email', None)
        if not user_email:
            return Response({"detail": "User email not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Batch-Tasks in request.data verarbeiten
        tasks_data = request.data.get('value', [])
        if not tasks_data:
            return Response({"detail": "No task data provided."}, status=status.HTTP_400_BAD_REQUEST)

        created_tasks = []
        errors = []

        for task in tasks_data:
            task['user'] = user.id
            serializer = TaskSerializer(data=task)
            if serializer.is_valid():
                created_task = serializer.save()
                created_tasks.append(created_task)
            else:
                errors.append({"task": task, "errors": serializer.errors})

        if errors:
            return Response({
                "detail": "Some tasks could not be created.",
                "created_tasks": TaskSerializer(created_tasks, many=True).data,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response(TaskSerializer(created_tasks, many=True).data, status=status.HTTP_201_CREATED)


    
class ContactView(APIView):
    def get(self, request, user_email):
        print("GET Request erhalten mit user_email:", user_email)
        try:
            user = User.objects.get(email=user_email)
            print("Benutzer gefunden:", user)
        except User.DoesNotExist:
            print("Benutzer mit E-Mail nicht gefunden:", user_email)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Kontakte für diesen Benutzer holen
        contacts = Contact.objects.filter(user=user)
        print("Gefundene Kontakte:", contacts)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data) 
       
    def post(self, request, *args, **kwargs):
        # Nutzer-Email aus dem Dispatcher holen
        user_email = getattr(request, 'user_email', None)
        print(f"POST Request - Nutzer-E-Mail aus Dispatcher: {user_email}")
        if not user_email:
            print("Fehler: Keine user_email im Request")
            return Response({"detail": "User email not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
            print(f"Benutzer gefunden: {user}")
        except User.DoesNotExist:
            print("Benutzer mit E-Mail nicht gefunden:", user_email)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Kontakte aus den Request-Daten holen
        contacts_data = request.data.get('value', [])
        print(f"Kontaktdaten aus dem Request: {contacts_data}")
        if not contacts_data:
            print("Fehler: Keine Kontaktdaten bereitgestellt")
            return Response({"detail": "No contact data provided."}, status=status.HTTP_400_BAD_REQUEST)

        created_contacts = []
        errors = []

        # Verarbeite jeden Kontakt
        for contact_data in contacts_data:
            contact_data['user'] = user.id# Benutzer-ID zu den Kontakt-Daten hinzufügen
            print("Kontakt-Daten zur Verarbeitung:", contact_data)
            serializer = ContactSerializer(data=contact_data)
            if serializer.is_valid():
                created_contact = serializer.save()  # Kontakt speichern
                print("Kontakt erfolgreich erstellt:", created_contact)
                created_contacts.append(created_contact)
            else:
                print("Fehler beim Speichern eines Kontakts:", serializer.errors) 
                errors.append({"contact": contact_data, "errors": serializer.errors})

        # Wenn es Fehler gibt, gib eine detaillierte Antwort zurück
        if errors:
            print("Fehlerhafte Kontakte:", errors) 
            return Response({
                "detail": "Some contacts could not be created.",
                "created_contacts": ContactSerializer(created_contacts, many=True).data,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)

        # Erfolgreich erstellte Kontakte zurückgeben
        print(f"Erfolgreich erstellte Kontakte: {created_contacts}")
        return Response(ContactSerializer(created_contacts, many=True).data, status=status.HTTP_201_CREATED)