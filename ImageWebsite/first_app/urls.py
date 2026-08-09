from django.urls import path, re_path
from django.views.static import serve
from django.http import HttpResponse
import os
from . import views

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # path('', views.serve_html, name='home'),
   
    # 1. Route specifically for the Coding folder and all its sub-paths
    # We use a non-capturing group for the optional trailing path
    re_path(r'^Interview(?:/(?P<path>.*))?/$', views.coding_directory_view, name='interview'),

    # 2. Route for standard static assets (CSS, JS, Images, etc.)
    # Optional: serve root-level CSS/JS/Image if HTML uses /CSS/... directly
    re_path(r'^(?P<folder>CSS|Image|JavaScript|AIModel|Artifacts)/(?P<path>.*)$',
            lambda request, folder, path: views.serve_static(request, folder, path)),
    path('', views.home_page, name="home"),
    path('ai-tutor/', views.ai_tutor_page, name="ai-tutor"),
    path('timetable/', views.timetable_page, name="timetable"),
    path('timetable/manage/', views.manage_timetable, name='manage_timetable'),
    path('about/', lambda request: views.serve_html(request, 'about_us.html'), name='about'),
    path("contact/", views.contact_page, name="contact"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    path('feedback/', views.feedback_page, name='feedback'),
    path('blog/', views.blog_page, name='blog'),
    path('blog-<slug:slug>/', views.blog_detail, name='blog_detail'),
    path("process-text/", views.process_text, name="process_text"),
    path("save-execution/", views.save_execution, name="save_execution"),
    path('ai-tutor/animal-classifier/', views.upload_and_predict, name='animal-classifier'),
    path('ai-tutor/python-compiler/', lambda request: views.serve_html(request, 'python_compiler.html'), name='python-compiler'),
    path("ai-tutor/ai-notes/", lambda request: views.serve_html(request, 'ai_notes.html'), name='ai-notes'),
    path('ai-tutor/c-compiler/', views.c_compiler_view, name='c_compiler'),
    path('ai-tutor/save-code/', views.save_code, name='save_code'),
    path('ai-tutor/load-code/', views.load_code, name='load_code'),
    path("summarize-text/", views.summarize_text, name="summarize_text"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("ads.txt", views.ads_txt, name="ads"),
    path('privacy/', views.privacy_policy_view, name='privacy_policy'),
]
