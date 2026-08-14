import os
import threading
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        super().__init__()

    def run(self):
        try:
            self.email_message.send(fail_silently=False)
        except Exception as e:
            logger.error(f"BACKGROUND EMAIL ERROR: {e}")

def send_password_reset_email(user_email, reset_link):
    subject = "Password Reset - Cognilume"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    text_content = f"We received a request to reset your password. Click here to reset it: {reset_link}"

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_file_path = os.path.join(BASE_DIR, 'HtmlWebsite', 'Html', 'password_reset_email.html')

    with open(html_file_path, 'r', encoding='utf-8') as file:
        template_string = file.read()

    template = Template(template_string)
    context = Context({'reset_link': reset_link})
    html_content = template.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    
    EmailThread(msg).start()