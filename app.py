from flask import Flask, redirect, request, abort
from mail_checker import check_for_livetrack_url
from dotenv import load_dotenv
import os


load_dotenv()
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SESSION_FILE = os.getenv('SESSION_FILE', 'current_session.txt')
CHECK_TOKEN = os.getenv('CHECK_TOKEN')

app = Flask(__name__)

@app.route('/check-mail')
def check_mail():
    token = request.args.get('token')
    if token != CHECK_TOKEN:
        abort(403)

    url = check_for_livetrack_url(IMAP_SERVER, EMAIL_USER, EMAIL_PASSWORD, SESSION_FILE)

    if url:
        return f"Updated: {url}", 200
    else:
        return "No new Garmin LiveTrack URL found.", 204
    
@app.route('/')
def index():
    try:
        with open(SESSION_FILE) as f:
            url = f.read().strip()
    except FileNotFoundError:
        return "<h1>Keine aktive Garmin LiveTrack Session vorhanden.</h1>"
    
    if url:
        return redirect(url)
    else:
        return "<h1>Keine aktive Garmin LiveTrack Session vorhanden.</h1>"
    
if __name__ == '__main__':
    app.run()