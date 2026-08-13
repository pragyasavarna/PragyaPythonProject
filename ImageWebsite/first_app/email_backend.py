from django.core.mail.backends.smtp import EmailBackend
from .models import OutgoingEmailLog

class LoggingEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        # 1. Hand the email off to the standard SMTP backend to actually send it
        sent_count = super().send_messages(email_messages)
        
        # 2. If it was successfully handed to Google, log it in our database
        if sent_count > 0:
            for message in email_messages:
                for recipient in message.to:
                    OutgoingEmailLog.objects.create(recipient=recipient)
                    
        return sent_count