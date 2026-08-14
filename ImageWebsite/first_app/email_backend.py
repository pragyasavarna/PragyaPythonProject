import logging
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import OutgoingEmailLog

logger = logging.getLogger(__name__)

class SendGridEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'SENDGRID_API_KEY', None)
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY is missing in settings.")
        self.client = SendGridAPIClient(self.api_key)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        return num_sent

    def _send(self, message):
        from_email = message.from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        
        # Extract HTML alternative if available
        html_content = None
        if hasattr(message, 'alternatives'):
            for content, mimetype in message.alternatives:
                if mimetype == 'text/html':
                    html_content = content
                    break

        mail = Mail(
            from_email=from_email,
            to_emails=message.to,
            subject=message.subject,
            plain_text_content=message.body or None,
            html_content=html_content or (message.body if getattr(message, 'content_subtype', '') == 'html' else None)
        )

        try:
            response = self.client.send(mail)
            if response.status_code in [200, 201, 202]:
                for recipient in message.to:
                    OutgoingEmailLog.objects.create(recipient=recipient)
                return True
            logger.error(f"SendGrid API returned status {response.status_code}: {response.body}")
            return False
        except Exception as e:
            if not self.fail_silently:
                raise
            logger.error(f"SendGrid sending error: {e}")
            return False