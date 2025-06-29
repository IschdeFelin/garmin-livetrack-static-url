import imaplib, email, re, json
from datetime import datetime


def check_for_livetrack_url(imap_server, email_user, email_password, session_file):
    mail = imaplib.IMAP4_SSL(imap_server)

    try:
        # Login to the email account
        mail.login(email_user, email_password)
    
        # Select inbox
        mail.select("INBOX")

        # Search for all emails in the selected mailbox
        result, data = mail.search(None, '(ALL FROM "noreply@garmin.com")')
        # result, data = mail.search(None, '(UNSEEN FROM "noreply@garmin.com")')

        if result != 'OK':
            return None
        
        mail_ids = data[0].split()
        if not mail_ids:
            return None
        
        # Fetch newest email
        for mail_id in reversed(mail_ids):
            result, msg_data = mail.fetch(mail_id, '(RFC822)')
            if result != 'OK':
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() in ['text/plain', 'text/html']:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')

            if body:
                match = re.search(r'https://livetrack\.garmin\.com/session/[^\s"<>]+', body)
                if match:
                    url = match.group(0)

                    # Check if the URL is already saved in the session file
                    try:
                        with open(session_file, "r") as f:
                            existing_data = json.load(f)
                            if existing_data.get('url') == url:
                                return None  # URL already exists, no need to update
                    except (FileNotFoundError, json.JSONDecodeError):
                        pass

                    # Save the new URL and timestamp to the session file
                    data = {
                        'url': url,
                        'timestamp': datetime.now().isoformat(),
                    }
                    with open(session_file, "w") as f:
                        json.dump(data, f)
                    return url
        return None
    except imaplib.IMAP4.error:
        return None
    finally:
        mail.logout()
