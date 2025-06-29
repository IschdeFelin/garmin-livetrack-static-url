from flask import Flask, redirect, request, abort, render_template
from mail_checker import check_for_livetrack_url
from dotenv import load_dotenv
import os


load_dotenv()
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SESSION_FILE = os.getenv('SESSION_FILE', 'current_session.txt')
CHECK_TOKEN = os.getenv('CHECK_TOKEN')
SHOW_IFRAME = os.getenv('SHOW_IFRAME', 'true').lower() == 'true'

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
        url = None
    
    iframe = 'iframe' in request.args
    external = 'external' in request.args
    
    if url:
        if (SHOW_IFRAME or iframe) and not external:
            return render_template('active_session.html', url=url), 200
        return redirect(url, code=302)
    else:
        return render_template('no_active_session.html'), 200
    
if __name__ == '__main__':
    app.run()