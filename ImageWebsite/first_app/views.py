import os
import json
import numpy as np
from PIL import Image
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.views.static import serve
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from tensorflow.keras.preprocessing import image
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from .models import UserAccount, ContactMessage, Feedback, BlogPost, CodeExecution
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import importlib.util
import time
import nbformat
from nbconvert import HTMLExporter

# Load your trained model once
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_PATH = os.path.join(BASE_DIR, "../ImageWebsite/AIModel/Model/my_model.keras")
# ANIMAL_MODEL_PATH = os.path.join(BASE_DIR, "../ImageWebsite/AIModel/Model/artifacts/animal_model_final.keras")
# ANIMAL_CLASS_NAMES_PATH = os.path.join(BASE_DIR, "../ImageWebsite/AIModel/Model/artifacts/animal_class_names.json")
ANIMAL_MODEL_PATH = os.path.join(BASE_DIR, "AIModel", "Model", "artifacts", "animal_model_final.keras")
ANIMAL_CLASS_NAMES_PATH = os.path.join(BASE_DIR, "AIModel", "Model", "artifacts", "animal_class_names.json")
AI_NOTES_FILE_PATH = os.path.join(BASE_DIR, "AIModel", "Model", "artifacts","notes","Notes_model.py")

spec = importlib.util.spec_from_file_location("Notes_model", AI_NOTES_FILE_PATH)
AI_Notes_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AI_Notes_model)
saved_model = tf.keras.models.load_model(ANIMAL_MODEL_PATH)
saved_animal_model = tf.keras.models.load_model(ANIMAL_MODEL_PATH)
with open(ANIMAL_CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)

# External AIModel folder

# Map folder names to their actual paths
# STATIC_FOLDERS = {
#     'CSS': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/CSS/'),
#     'Image': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Image/'),
#     'JavaScript': os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/JavaScript/'),
#     'AIModel': os.path.join(BASE_DIR, '../ImageWebsite/AIModel/Model/'),
#     'Artifacts': os.path.join(BASE_DIR, '../ImageWebsite/AIModel/Model/artifacts/'),
# }
# CHANGE THIS ENTIRE DICT TO:

STATIC_FOLDERS = {
    'CSS': os.path.join(BASE_DIR, 'HtmlWebsite', 'CSS'),
    'Image': os.path.join(BASE_DIR, 'HtmlWebsite', 'Image'),
    'JavaScript': os.path.join(BASE_DIR, 'HtmlWebsite', 'JavaScript'),
    'AIModel': os.path.join(BASE_DIR, 'AIModel', 'Model'),
    'Artifacts': os.path.join(BASE_DIR, 'AIModel', 'Model', 'artifacts'),
    'Interview': os.path.join(BASE_DIR, 'Interview'),
}

# ---------------------------------------------------------
# VIEW 1: Dedicated view for the highly customized Coding folder
# ---------------------------------------------------------
def coding_directory_view(request, path=""):
    # 1. Admin Protection
    # if not (request.user.is_authenticated and request.user.is_staff):
    #     return HttpResponse("Permission Denied: Admin access required.", status=403)

    document_root = os.path.join(BASE_DIR, 'Interview')
    full_path = os.path.join(document_root, path)

    # Prevent directory traversal attacks (e.g., trying to access ../../etc/passwd)
    if not os.path.abspath(full_path).startswith(os.path.abspath(document_root)):
        return HttpResponse("Permission Denied.", status=403)

    if not os.path.exists(full_path):
        return HttpResponse("Not Found", status=404)

    # 2. Handle Jupyter Notebooks
    if full_path.endswith('.ipynb'):
        # If the iframe is requesting the raw notebook content
        if request.GET.get('raw') == 'true':
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    notebook_node = nbformat.read(f, as_version=4)
                html_exporter = HTMLExporter()
                (body, resources) = html_exporter.from_notebook_node(notebook_node)
                return HttpResponse(body)
            except Exception as e:
                return HttpResponse(f"Error rendering notebook: {e}", status=500)
        
        # If the user just clicked the link, serve the Cognilume wrapper
        else:
            # Dynamically calculate the parent directory
            parent_dir = os.path.dirname(path)
            
            # If inside a subfolder (like Strings), go to /Interview/Strings/
            # If already in the root, go to /Interview/
            back_url = f"/Interview/{parent_dir}/" if parent_dir else "/Interview/"
            # --- CHANGED: Clean the file name for display ---
            raw_name = os.path.basename(full_path)
            clean_name = os.path.splitext(raw_name)[0].replace('_', ' ')

            context = {
                'file_name': clean_name,
                'current_path': path,
                'back_url': back_url # <-- Passing the exact URL to the template
            }
            return render(request, 'notebook_view.html', context)
    
    # 3. Handle Directories (The Custom UI)
    if os.path.isdir(full_path):
        clean_path = path.strip('/')
        parent_path = os.path.dirname(clean_path) if clean_path else None
        if clean_path:
            formatted_topic = clean_path.replace('_', ' ').replace('/', ' - ').title()
            page_title = f"📂 {formatted_topic} Interview Questions"
        else:
            # If the user is at the root /Interview/ directory, display the main title
            page_title = "📚 Interview Preparation Modules"
        
        directories = []
        files = []
        
        try:
            for item in sorted(os.listdir(full_path)):
                if item.startswith('.'):
                    continue
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    directories.append(item)
                else:
                    clean_name = os.path.splitext(item)[0].replace('_', ' ')
                    files.append({
                        'real_name': item,
                        'display_name': clean_name
                    })
        except Exception as e:
            return HttpResponse(f"Error reading directory: {e}", status=500)

        context = {
            'current_path': clean_path,
            'parent_path': parent_path,
            'directories': directories,
            'files': files,
            'base_folder': 'Interview',
            'page_title': page_title,
        }
        return render(request, 'coding_index.html', context)
    
    # 4. Handle regular files (.py, .txt, etc.)
    return serve(request, path, document_root=document_root)


# ---------------------------------------------------------
# VIEW 2: Simple, lightweight view for CSS, JS, and Images
# ---------------------------------------------------------
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


def predict_image_old(img_file):
    img = Image.open(img_file)
    img = img.resize((200, 200))  # adjust size as per training
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    result = saved_model.predict(img_array)
    return "Dog" if result >= 0.5 else "Cat"

def predict_image(img_file):
    img = Image.open(img_file)
    img = img.resize((200, 200))      # same size as training
    img_array = image.img_to_array(img)   # DO NOT divide by 255
    img_array = np.expand_dims(img_array, axis=0)
    result = saved_animal_model.predict(img_array)
    pred_idx = np.argmax(result)          # pick top predicted class
    return class_names[pred_idx]          # return class name


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


def feedback_page(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        issue_type = request.POST.get("issue_type")
        subject = request.POST.get("subject")
        description = request.POST.get("description")

        Feedback.objects.create(
            name=name,
            email=email,
            issue_type=issue_type,
            subject=subject,
            description=description
        )

        success = True

    return render(request, "feedback.html", {"success": success})

def blog_page(request):
    # Fetch all blogs, ordered by newest date first
    blogs_list = BlogPost.objects.all().order_by('-published_at')
    
    # Set up Pagination: Show 6 blogs per page (adjust this number as you like)
    paginator = Paginator(blogs_list, 6) 
    
    # Get the page number from the URL (e.g., /blog/?page=2)
    page_number = request.POST.get('page') or request.GET.get('page')
    
    # Get the specific blogs for the requested page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj 
    }
    return render(request, "blog.html", context)

def blog_detail(request, slug):
    # Tries to get the blog with this ID, or shows 404 error if not found
    blog_post = get_object_or_404(BlogPost, slug=slug)
    
    return render(request, 'blog_detail.html', {'blog': blog_post})

@csrf_exempt
def process_text(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    data = json.loads(request.body)
    text = data.get("text", "")

    print("User said:", text)

    # Example logic
    if "jarvis" in text.lower():
        reply = "Yes, how can I help you?"
    else:
        reply = "Hey Pragya"

    # TODO: save to DB / call AI model here

    return JsonResponse({
        "reply": reply
    })

@csrf_exempt
def save_execution(request):
    if request.method == "POST":

        code = request.POST.get("code_input", "")
        output = request.POST.get("code_output", "")
        ip = get_client_ip(request)
        location = get_location_from_ip(ip)
        CodeExecution.objects.create(
            user=request.user if request.user.is_authenticated else None,
            code=code,
            output=output,
            ip_address=ip,
            city=location.get("city") if location else None,
            state=location.get("region") if location else None,
            country=location.get("country") if location else None,
        )

        return JsonResponse({"status": "saved", "ip": ip})

    return JsonResponse({"status": "invalid", "ip": ip}, status=400)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

import requests

def get_location_from_ip(ip):
    try:
        g = GeoIP2()
        city = g.city(ip)

        return {
            "city": city.get("city"),
            "region": city.get("region"),        # State
            "country": city.get("country_name"),
        }
    except Exception as e:
        print("GeoIP error:", e)
        return {
            "city": None,
            "region": None,
            "country": None,
        }

@csrf_exempt
def summarize_text(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            text = data.get("text", "")

            summary = AI_Notes_model.summarize_notes(text)
            bullets = AI_Notes_model.bullet_summary(summary)
            keywords = AI_Notes_model.extract_keywords(text)

            return JsonResponse({
                "summary": summary,
                "bullets": bullets,
                "keywords": keywords
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def stream_summary(request):

    text = request.GET.get("text", "")

    def event_stream():

        summary = AI_Notes_model.summarize_notes(text)

        for char in summary:
            yield f"data: {char}\n\n"
            time.sleep(0.01)

        yield "data: [END]\n\n"

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream"
    )