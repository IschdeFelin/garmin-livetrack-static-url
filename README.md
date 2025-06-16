# Garmin LiveTrack Static URL

Dieses kleine Python/Flask-Projekt stellt eine statische URL bereit, die automatisch auf die aktuellste Garmin LiveTrack-Session weiterleitet.

## Features

- Automatisches Abrufen der LiveTrack-URL aus dem E-Mail-Postfach
- Speicherung der aktuellsten Session-URL in einer Datei
- Webserver mit Weiterleitung zur aktuellen LiveTrack-Session
- Schutz der Mail-Abfrage durch Token
- Konfiguration über eine `.env`-Datei

## Installation

1. Repository klonen:
```bash
git clone https://github.com/ischdefelin/garmin-livetrack-static-url.git
cd garmin-livetrack-static-url
```

2. (Optional) Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv .venv
source .venv/bin/activate  # für Linux/macOS
.venv\Scripts\activate     # für Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. .env-Datei anlegen und konfigurieren:
```env
IMAP_SERVER=dein-imap-server
EMAIL_USER=deine-email@example.com
EMAIL_PASSWORD=dein-email-passwort
SESSION_FILE=current_session.txt
CHECK_TOKEN=dein-geheimer-token
```

## Nutzung
1. Webserver starten:
```bash
python app.py
```

2. LiveTrack-URL aktualisieren (z.B. per Cronjob oder manuell):
```
http://dein-server/check-mail?token=dein-geheimer-token
```

3. Die statische URL zur LiveTrack-Session ist erreichbar unter:
```
http://dein-server/
```

## Hinweise
- Die aktuellste LiveTrack-URL wird in der Datei `current_session.txt` gespeichert.

- Die `/check-mail`-Route sollte durch einen sicheren Token geschützt werden, um unberechtigte Zugriffe zu vermeiden.