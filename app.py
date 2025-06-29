from flask import Flask, redirect, request, abort, render_template
from mail_checker import check_for_livetrack_url
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os, json


load_dotenv()
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SESSION_FILE = os.getenv('SESSION_FILE', 'current_session.txt')
CHECK_TOKEN = os.getenv('CHECK_TOKEN')
SHOW_IFRAME = os.getenv('SHOW_IFRAME', 'true').lower() == 'true'
MAX_SESSION_AGE = int(os.getenv('MAX_SESSION_AGE', 24))  # Default to 24 hours

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
        return "No new Garmin LiveTrack URL found.", 200
    
@app.route('/')
def index():
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            url = data.get('url')
            timestamp_str = data.get('timestamp')
            if not url or not timestamp_str:
                raise ValueError("Invalid session data")
            timestamp = datetime.fromisoformat(timestamp_str)
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        url = None
    
    iframe = 'iframe' in request.args
    external = 'external' in request.args

    # Check if the URL is still valid (not older than MAX_SESSION_AGE hours)
    if url and (datetime.now() - timestamp) > timedelta(hours=MAX_SESSION_AGE):
        url = None
    
    if url:
        if (SHOW_IFRAME or iframe) and not external:
            return render_template('active_session.html', url=url), 200
        return redirect(url, code=302)
    else:
        return render_template('no_active_session.html'), 200
    
if __name__ == '__main__':
    app.run()