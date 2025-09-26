import os

import numpy as np
from PIL import Image
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.views.static import serve
from tensorflow.keras.preprocessing import image

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
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
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
    # Always load your external HTML file
    html_path = os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Html/', "index.html")
    if not os.path.exists(html_path):
        return HttpResponse("HTML file not found", status=404)

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if request.method == "POST" and "image" in request.FILES:
        img_file = request.FILES["image"]
        prediction = predict_image(img_file)
        content = content.replace("{{result}}", f"<h3>Prediction: {prediction}</h3>")
    else:
        content = content.replace("{{result}}", "")

        # Force CSRF cookie to be created

    response = HttpResponse(content)
    return response


@csrf_exempt
def upload_and_predict1(request):
    # Debug logs
    print("COOKIES:", request.COOKIES)
    print("POST csrf:", request.POST.get('csrfmiddlewaretoken'))

    # Path to your HTML file
    html_path = os.path.join(BASE_DIR, '../ImageWebsite/HtmlWebsite/Html/', "index.html")
    if not os.path.exists(html_path):
        return HttpResponse("HTML file not found", status=404)

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]
        prediction = predict_image(img_file)
        content = content.replace("{{result}}", f"<h3>Prediction: {prediction}</h3>")
    else:
        # No result placeholder if no POST
        content = content.replace("{{result}}", "")

    return HttpResponse(content)