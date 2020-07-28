from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


async def verification_email(key, to, link):
    message = Mail(
        from_email='kml.kdk@gmail.com',
        to_emails=to,
        subject='Please verify your email address',
        html_content='<strong>Confirm your email</strong> {}'.format(link))

    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        if response:
            return True
        else:
            return False
    except Exception:
        return False
