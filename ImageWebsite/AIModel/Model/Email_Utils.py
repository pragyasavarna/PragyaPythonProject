import os
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Template, Context

def send_password_reset_email(user_email, reset_link):
    subject = "Password Reset - Cognilume"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    # Plain text fallback for email clients that don't support HTML
    text_content = f"We received a request to reset your password. Click here to reset it: {reset_link}"

    # 1. Get the path to the HTML file in the same directory as this script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_file_path = os.path.join(BASE_DIR, 'HtmlWebsite', 'Html', 'password_reset_email.html')

    # 2. Read the HTML file and render it with the reset link
    with open(html_file_path, 'r', encoding='utf-8') as file:
        template_string = file.read()
        
    template = Template(template_string)
    context = Context({'reset_link': reset_link})
    html_content = template.render(context)

    # 3. Create and send the email
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()