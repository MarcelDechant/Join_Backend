
# Join - Projektmanagement-Tool

**Join** ist ein Projektmanagement-Tool, das dazu dient, den Status und die Verantwortlichkeiten von Aufgaben zu visualisieren. Es hilft dabei, den Überblick über Projekte und deren Fortschritt zu behalten und Aufgaben klar zuzuordnen.

---

## Installation

### Frontend

1. Klone das Repository:
   ```bash
   git clone https://github.com/MarcelDechant/Join_Frontend_new
   cd Join/frontend
   ```
   
2. Öffne die `index.html`-Datei mit einem Live Server. (Du kannst den Live Server in Visual Studio Code oder einem anderen Editor verwenden.)

   **Hinweis:** Du musst keine weiteren Schritte für das Frontend durchführen.

### Backend

1. Klone das Repository:
   ```bash
   git clone https://github.com/MarcelDechant/Join_Backend
   cd Join/backend
   ```

2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

3. Erstelle einen Superuser, um Zugriff auf den Admin-Bereich zu erhalten:
   ```bash
   python manage.py createsuperuser
   ```

4. Starte den Server:
   ```bash
   python manage.py runserver
   ```

---

## Verwendung

- **Frontend:** Das Frontend ist mit HTML, CSS und JavaScript (inkl. `index.html`) entwickelt. Es visualisiert die Aufgaben und deren Status. Du kannst es einfach über den Live Server starten und benutzen.
  
- **Backend:** Das Backend wurde mit Python und Django entwickelt. Es nutzt das Django REST Framework zur Bereitstellung der API. Du kannst den Admin-Bereich nach der Erstellung des Superusers über den `admin/`-Pfad erreichen.



## Technologien

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Django, Django REST Framework

---

## Beitrag

Wenn du zu diesem Projekt beitragen möchtest, erstelle einen Pull-Request und beschreibe die Änderungen, die du vorgenommen hast.

---

## Autor

Dieses Projekt wurde von **Marcel Dechant** erstellt.
