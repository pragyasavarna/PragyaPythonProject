import os

import numpy as np
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.views.static import serve
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from tensorflow.keras.preprocessing import image
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from .models import UserAccount, ContactMessage

# Load your trained model once
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "../ImageWebsite/AIModel/Model/my_model.keras")

saved_model = tf.keras.models.load_model(MODEL_PATH)
# External AIModel folder

# Map folder names to their actual paths
STATIC_FOLDERS = {
    'CSS': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/CSS/'),
    'Image': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Image/'),
    'JavaScript': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/JavaScript/'),
    'AIModel': os.path.join(BASE_DIR, '../ImageWebsite/AIModel/Model/'),
}


def serve_static(request, folder, path):
    if folder in STATIC_FOLDERS:
        return serve(request, path, document_root=STATIC_FOLDERS[folder])
    else:
        return HttpResponse("Not Found", status=404)

# Serve dynamic HTML files
def serve_html(request, html_file='index.html'):  # default to index.html
    # Automatically append .html if not present
    print(get_token(request))
    if not html_file.endswith('.html'):
        html_file += '.html'
    # Build absolute path
    html_path = os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Html/', html_file)
    html_path = os.path.normpath(html_path)  # normalize path

    # Debug: print path
    print(f"Base Dir: {BASE_DIR}")
    print(f"Loading HTML file: {html_path}")

    # Check if file exists
    if os.path.exists(html_path):
        # with open(html_path, 'r', encoding='utf-8') as f:
        #     content = f.read()
        # return HttpResponse(content)
        template = loader.get_template(html_file)
        return HttpResponse(template.render({}, request))
    else:
        return HttpResponse(f"HTML file not found: {html_file}", status=404)


def predict_image(img_file):
    img = Image.open(img_file)
    img = img.resize((200, 200))  # adjust size as per training
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    result = saved_model.predict(img_array)
    return "Dog" if result >= 0.5 else "Cat"

@csrf_exempt
def upload_and_predict(request):
    print("COOKIES:", request.COOKIES)
    print("POST csrf:", request.POST.get('csrfmiddlewaretoken'))
    # Path to your HTML file
    html_path = os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Html/', "project.html")
    if not os.path.exists(html_path):
        return HttpResponse("HTML file not found", status=404)
    context = {}  # Variables for the template

    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]
        prediction = predict_image(img_file)
        context["result"] = f"Prediction: {prediction}"
    else:
        context["result"] = ""

    # The path here should be relative to your Django TEMPLATES settings
    # e.g., 'project.html' should be inside a templates directory
    return render(request, "project.html", context)



def contact_page(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        success = True

    return render(request, "contact.html", {"success": success})

def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        user = UserAccount.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "register.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

        login(request, user)
        return redirect("/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/")

def forgot_password(request):
    message = None
    error = None

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = UserAccount.objects.get(email=email)

            # Create password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f"/reset-password/{uid}/{token}/"
            )

            # Send email
            send_mail(
                subject="Password Reset - Cognilume",
                message=f"Click the link to reset your password:\n\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            message = "A reset link has been sent to your email."

        except UserAccount.DoesNotExist:
            error = "No account found with this email."

    return render(request, "forgot_password.html", {
        "message": message,
        "error": error,
    })

def reset_password(request, uidb64, token):
    error = None
    success = None

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAccount.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("password")
            user.set_password(new_password)
            user.save()

            success = "Your password has been reset successfully!"
            return render(request, "reset_password.html", {"success": success})

        return render(request, "reset_password.html")

    else:
        error = "Invalid or expired password reset link."
        return render(request, "reset_password.html", {"error": error})
