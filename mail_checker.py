import imaplib, email, re


def check_for_livetrack_url(imap_server, email_user, email_password, session_file):
    mail = imaplib.IMAP4_SSL(imap_server)

    try:
        # Login to the email account
        mail.login(email_user, email_password)
    
        # Select inbox
        mail.select("INBOX")

        # Search for all emails in the selected mailbox
        result, data = mail.search(None, 'ALL')
        # result, data = mail.search(None, 'UNSEEN')

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
                    with open(session_file, "w") as f:
                        f.write(url)
                    return url
        return None
    except imaplib.IMAP4.error:
        return None
    finally:
        mail.logout()
