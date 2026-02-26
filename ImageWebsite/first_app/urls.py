from django.urls import path, re_path
from django.views.static import serve
from django.http import HttpResponse
import os
from . import views

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # path('', views.serve_html, name='home'),
   
    # Optional: serve root-level CSS/JS/Image if HTML uses /CSS/... directly
    re_path(r'^(?P<folder>CSS|Image|JavaScript|AIModel|Artifacts)/(?P<path>.*)$',
            lambda request, folder, path: views.serve_static(request, folder, path)),
    path('', lambda request: views.serve_html(request, 'index.html'), name='index'),
    path('about/', lambda request: views.serve_html(request, 'about_us.html'), name='about'),
    path("contact/", views.contact_page, name="contact"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    path('face_model/', lambda request: views.serve_html(request, 'face_recognition.html'), name='face-model'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('blog/', views.blog_page, name='blog'),
    path('blog-<slug:slug>', views.blog_detail, name='blog_detail'),
    path('srs/', lambda request: views.serve_html(request, 'srs.html'), name='srs'),
    path("process-text/", views.process_text, name="process_text"),
    path("save-execution/", views.save_execution, name="save_execution"),
    path('ai-tutor/', lambda request: views.serve_html(request, 'ai-tutor.html'), name='ai-tutor'),
    path('ai-tutor/animal-classifier/', views.upload_and_predict, name='animal-classifier'),
    path('ai-tutor/python-compiler/', lambda request: views.serve_html(request, 'python_compiler.html'), name='python-compiler'),
]
