"""
URL configuration for MyWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.static import serve
from django.http import HttpResponse
import os
from . import views

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # path('', views.serve_html, name='home'),
    path('project/', views.upload_and_predict, name='project'),
    # Optional: serve root-level CSS/JS/Image if HTML uses /CSS/... directly
    re_path(r'^(?P<folder>CSS|Image|JavaScript|AIModel)/(?P<path>.*)$',
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
]
