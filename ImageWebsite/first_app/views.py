import os
import json
import numpy as np
from PIL import Image
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
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
from .models import UserAccount, ContactMessage, Feedback, BlogPost, CodeExecution,Service,HomePage,AITutorPage, AITool, Subject, Teacher, DayOfWeek, ClassGroup, PeriodTime, TimetableEntry, Technology
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import importlib.util
import time
import nbformat
from nbconvert import HTMLExporter
from django.core.cache import cache
from django.views.decorators.cache import never_cache

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

@never_cache
def home_page(request):
    validated_home = cache.get('home_page_data')
    all_services = cache.get('services_data')
    validated_technologies = cache.get('tech_data')
    if not validated_home or not all_services or not validated_technologies:
        all_services = list(Service.objects.all())
        all_technologies = list(Technology.objects.all())
        home_record = HomePage.objects.first()
        # 1. Initialize a perfectly safe dictionary. 
        # This guarantees the template never crashes, even if the database is completely empty.
        validated_home = {
            'title': '',
            'subtitle': '',
            'primary_btn_text': '',
            'primary_btn_link': '',
            'secondary_btn_text': '',
            'secondary_btn_link': '',
            'hero_image': None,
            'image_alt_text': '',
            'services_label': '',
            'services_heading_main': '',
            'services_heading_highlight': ''
        }
        # 2. Perform Backend Validation
        if home_record:
            if home_record.title:
                validated_home['title'] = home_record.title
            
            if home_record.subtitle:
                validated_home['subtitle'] = home_record.subtitle
            
            # VALIDATION: Only pass the primary button if BOTH text and link are filled out
            if home_record.primary_btn_text and home_record.primary_btn_link:
                validated_home['primary_btn_text'] = home_record.primary_btn_text
                validated_home['primary_btn_link'] = home_record.primary_btn_link
            
            # VALIDATION: Only pass the secondary button if BOTH text and link are filled out
            if home_record.secondary_btn_text and home_record.secondary_btn_link:
                validated_home['secondary_btn_text'] = home_record.secondary_btn_text
                validated_home['secondary_btn_link'] = home_record.secondary_btn_link
            
            # VALIDATION: Ensure the image actually exists before passing the file object
            if home_record.hero_image:
                validated_home['hero_image'] = home_record.hero_image
                validated_home['image_alt_text'] = home_record.image_alt_text
                
            # VALIDATION: Pass services text if they exist
            if home_record.services_label:
                validated_home['services_label'] = home_record.services_label
            
            if home_record.services_heading_main:
                validated_home['services_heading_main'] = home_record.services_heading_main
            
            if home_record.services_heading_highlight:
                validated_home['services_heading_highlight'] = home_record.services_heading_highlight
        
        validated_technologies = []
        for tech in all_technologies:
            safe_tech = {
                'name': '',
                'logo': None,
                'order': 0 
            }
            if tech:
                if tech.name:
                    safe_tech['name'] = tech.name
                if tech.logo:
                    safe_tech['logo'] = tech.logo
                if tech.order is not None:
                    safe_tech['order'] = tech.order
                    
            validated_technologies.append(safe_tech)

        # 3. Save this finalized, safe data into the cache for 24 hours (86400 seconds)
        cache.set('home_page_data', validated_home, 86400)
        cache.set('services_data', all_services, 86400)
        cache.set('tech_data', validated_technologies, 86400) 
    context = {
        'services': all_services,
        'technologies': validated_technologies,
        'home': validated_home, # Send the validated dictionary instead of the raw database object
    }
    
    return render(request, 'index.html', context)

@never_cache
def ai_tutor_page(request):
    # ==========================================
    # 1. PAGE TITLE CACHING
    # ==========================================
    cached_title = cache.get('ai_tutor_page_title')
    page_id = cache.get('ai_tutor_page_id')
    if not cached_title or not page_id:
        page_data = AITutorPage.objects.first()
        cached_title = page_data.page_title if page_data and page_data.page_title else "AI Tutor – Core Learning Tools"
        page_id = page_data.id if page_data else None
        cache.set('ai_tutor_page_title', cached_title, 86400)
        cache.set('ai_tutor_page_id', page_id, 86400)

    # ==========================================
    # 2. INDIVIDUAL TOOL CACHING
    # ==========================================
    # Step A: Get a lightweight list of all current tool IDs from the database
    if page_id:
        # We filter using page_id, so we don't need the page_data object!
        tool_ids = list(AITool.objects.filter(page_id=page_id).values_list('id', flat=True))
    else:
        tool_ids = []
    
    # Step B: Generate the cache keys we expect (e.g., ['ai_tool_1', 'ai_tool_2'])
    cache_keys = [f'ai_tool_{tid}' for tid in tool_ids]
    
    # Step C: Ask the cache for all these keys at once (Very fast)
    cached_tools_dict = cache.get_many(cache_keys)
    
    # Step D: Figure out which IDs were NOT in the cache
    missing_ids = [
        tid for tid in tool_ids 
        if f'ai_tool_{tid}' not in cached_tools_dict
    ]
    
    # Step E: Fetch ONLY the missing tools from the database
    if missing_ids:
        missing_tools = AITool.objects.filter(id__in=missing_ids)
        
        # Prepare them to be saved to the cache in bulk
        tools_to_cache = {f'ai_tool_{tool.id}': tool for tool in missing_tools}
        
        # Save the missing ones to the cache for 24 hours
        cache.set_many(tools_to_cache, 86400)
        
        # Merge the newly fetched tools into our main dictionary
        cached_tools_dict.update(tools_to_cache)

    # Step F: Reconstruct the final list
    # Because dictionaries lose order, we must sort them back into their proper 
    # display sequence using the 'order' field you set up in your models!
    final_tools_list = list(cached_tools_dict.values())
    final_tools_list.sort(key=lambda t: (t.order, t.id))

    # ==========================================
    # 3. RENDER TEMPLATE
    # ==========================================
    context = {
        'page_title': cached_title,
        'ai_tools': final_tools_list
    }
    
    return render(request, 'ai-tutor.html', context)

@never_cache
def timetable_page(request):
    # ==========================================
    # 1. CLASS & PERIOD CACHING
    # ==========================================

    # Cache all days (the X-Axis of our grid)
    all_days = cache.get('all_days_data')
    if not all_days:
        all_days = list(DayOfWeek.objects.all().order_by('order'))
        cache.set('all_days_data', all_days, 86400)
    
    days_headers = [day.name for day in all_days]

    # Cache all classes for the dropdown menu
    all_classes = cache.get('all_classes_data')
    if not all_classes:
        all_classes = list(ClassGroup.objects.all())
        cache.set('all_classes_data', all_classes, 86400)

    # Cache all periods (the Y-axis of our grid)
    all_periods = cache.get('all_periods_data')
    if not all_periods:
        all_periods = list(PeriodTime.objects.all().order_by('start_time'))
        cache.set('all_periods_data', all_periods, 86400)

    # Determine which class is currently selected via URL param
    class_id = request.GET.get('class_id')
    active_class = None
    
    if class_id and all_classes:
        # Fast lookup in the cached list
        active_class = next((c for c in all_classes if str(c.id) == str(class_id)), None)
    
    # Fallback to the first class if none selected or invalid ID
    if not active_class and all_classes:
        active_class = all_classes[0]

    active_class_id = active_class.id if active_class else None

    # ==========================================
    # 2. SAFE DICTIONARY INITIALIZATION
    # ==========================================
    # This guarantees the template never crashes, even if the database is completely empty.
    validated_timetable = {
        'class_name': '',
        'class_id': active_class_id,
        'days_headers': days_headers,
        'grid': []
    }

    # Perform Backend Validation for the class header
    if active_class:
        if active_class.name:
            validated_timetable['class_name'] = active_class.name

    # ==========================================
    # 3. INDIVIDUAL TIMETABLE ENTRY CACHING
    # ==========================================
    # Step A: Get a lightweight list of all current entry IDs for this specific class
    if active_class_id:
        entry_ids = list(TimetableEntry.objects.filter(class_group_id=active_class_id).values_list('id', flat=True))
    else:
        entry_ids = []

    # Step B: Generate the cache keys we expect (e.g., ['tt_entry_1', 'tt_entry_2'])
    cache_keys = [f'tt_entry_{eid}' for eid in entry_ids]

    # Step C: Ask the cache for all these keys at once (Very fast)
    cached_entries_dict = cache.get_many(cache_keys)

    # Step D: Figure out which IDs were NOT in the cache
    missing_ids = [
        eid for eid in entry_ids 
        if f'tt_entry_{eid}' not in cached_entries_dict
    ]

    # Step E: Fetch ONLY the missing entries from the database
    if missing_ids:
        # Use select_related to prevent N+1 queries when accessing the teacher/period later
        missing_entries = TimetableEntry.objects.select_related('teacher', 'period', 'subject').prefetch_related('days').filter(id__in=missing_ids)
        
        # Prepare them to be saved to the cache in bulk
        entries_to_cache = {f'tt_entry_{entry.id}': entry for entry in missing_entries}
        
        # Save the missing ones to the cache for 24 hours
        cache.set_many(entries_to_cache, 86400)
        
        # Merge the newly fetched entries into our main dictionary
        cached_entries_dict.update(entries_to_cache)

    # Step F: Create a lookup map (O(1) complexity) to easily place entries into the HTML grid
    final_entries_list = list(cached_entries_dict.values())
    entry_map = {}
    for e in final_entries_list:
        for day_obj in e.days.all():
            entry_map[(e.period_id, day_obj.name)] = e

    # ==========================================
    # 4. GRID CONSTRUCTION & FINAL VALIDATION
    # ==========================================
    timetable_grid = []
    
    for p in all_periods:
        # Validate time formatting
        start = p.start_time.strftime('%H:%M') if p.start_time else ''
        end = p.end_time.strftime('%H:%M') if p.end_time else ''
        
        row_data = {
            'period_name': p.name if p.name else '',
            'time_range': f"{start} - {end}" if start and end else '',
            'is_lunch': p.is_lunch,
            'days': []
        }
        
        if not p.is_lunch:
            for day in validated_timetable['days_headers']:
                entry = entry_map.get((p.id, day))
                
                # Safe defaults for missing lectures
                teacher_name = ''
                subject_name = ''
                
                # VALIDATION: Safely extract teacher and subject
                if entry:
                    if entry.teacher and entry.teacher.name:
                        teacher_name = f"({entry.teacher.name})"
                    if entry.subject and entry.subject.name:
                        subject_name = entry.subject.name
                    else:
                        subject_name = 'Free Period'
                        
                row_data['days'].append({
                    'day_name': day,
                    'teacher': teacher_name,
                    'subject': subject_name
                })
                
        timetable_grid.append(row_data)

    # Assign the finalized, validated grid to our safe dictionary
    validated_timetable['grid'] = timetable_grid

    # ==========================================
    # 5. RENDER TEMPLATE
    # ==========================================
    context = {
        'classes': all_classes,
        'timetable': validated_timetable, # Send the fully validated dictionary, not raw objects
    }
    
    return render(request, 'time_table.html', context)

@never_cache
def manage_timetable(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            # --- DAY OF WEEK ---
            if action == 'create_day':
                DayOfWeek.objects.create(name=request.POST.get('name'), order=request.POST.get('order', 0))
                messages.success(request, "Day added.")
            elif action == 'delete_day':
                DayOfWeek.objects.get(id=request.POST.get('id')).delete()
                messages.success(request, "Day deleted.")

            # --- SUBJECT ---
            elif action == 'create_subject':
                Subject.objects.create(name=request.POST.get('name'))
                messages.success(request, "Subject added.")
            elif action == 'delete_subject':
                Subject.objects.get(id=request.POST.get('id')).delete()
                messages.success(request, "Subject deleted.")

            # --- CLASS GROUP ---
            elif action == 'create_class':
                ClassGroup.objects.create(name=request.POST.get('name'))
                messages.success(request, "Class added.")
            elif action == 'delete_class':
                ClassGroup.objects.get(id=request.POST.get('id')).delete()
                messages.success(request, "Class deleted.")

            # --- PERIOD TIME ---
            elif action == 'create_period':
                PeriodTime.objects.create(
                    name=request.POST.get('name'),
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    is_lunch=request.POST.get('is_lunch') == 'on'
                )
                messages.success(request, "Period added.")
            elif action == 'delete_period':
                PeriodTime.objects.get(id=request.POST.get('id')).delete()
                messages.success(request, "Period deleted.")

            # --- TEACHER ---
            elif action == 'create_teacher':
                teacher = Teacher.objects.create(name=request.POST.get('name'))
                teacher.subjects.set(request.POST.getlist('subjects'))
                messages.success(request, "Teacher added.")
            elif action == 'delete_teacher':
                Teacher.objects.get(id=request.POST.get('id')).delete()
                messages.success(request, "Teacher deleted.")

            # --- TIMETABLE ENTRY ---
            elif action == 'create_entry':
                new_entry = TimetableEntry.objects.create(
                    class_group_id=request.POST.get('class_group'),
                    period_id=request.POST.get('period'),
                    teacher_id=request.POST.get('teacher') or None,
                    subject_id=request.POST.get('subject') or None
                )
                new_entry.days.set(request.POST.getlist('days'))
                messages.success(request, "Timetable entry created.")
            elif action == 'delete_entry':
                entry_id = request.POST.get('id')
                day_id = request.POST.get('day_id') # Capture the specific day
                
                entry = TimetableEntry.objects.get(id=entry_id)
                
                if day_id:
                    # Remove only the specific day from this lecture
                    day_to_remove = DayOfWeek.objects.get(id=day_id)
                    entry.days.remove(day_to_remove)
                    
                    # If there are no days left, delete the orphaned entry completely
                    if entry.days.count() == 0:
                        entry.delete()
                        messages.success(request, "Lecture entry completely removed.")
                    else:
                        messages.success(request, f"Lecture removed from {day_to_remove.name}.")
                else:
                    # Fallback just in case
                    entry.delete()
                    messages.success(request, "Timetable entry deleted.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        cache.clear()
        return redirect('manage_timetable')

    # GET REQUEST: Fetch all data
    all_days = DayOfWeek.objects.all().order_by('order')
    all_periods = PeriodTime.objects.all().order_by('start_time')
    all_classes = ClassGroup.objects.all().order_by('name')
    teachers = Teacher.objects.prefetch_related('subjects').order_by('name')
    entries = TimetableEntry.objects.select_related('class_group', 'period', 'teacher', 'subject').prefetch_related('days')
    
    # ---------------------------------------------------------------------
    # NEW: Build the 2D Grid Structure for the Management Dashboard
    # ---------------------------------------------------------------------
    entry_map = {}
    for entry in entries:
        for day in entry.days.all():
            # Map entry by (class_id, period_id, day_id)
            entry_map[(entry.class_group_id, entry.period_id, day.id)] = entry

    grouped_timetables = []
    for cls in all_classes:
        grid = []
        for p in all_periods:
            row_data = {'period': p, 'days': []}
            if not p.is_lunch:
                for d in all_days:
                    row_data['days'].append({
                        'day': d,
                        'entry': entry_map.get((cls.id, p.id, d.id))
                    })
            grid.append(row_data)
        
        grouped_timetables.append({
            'class_info': cls,
            'grid': grid
        })

    # Teacher JSON for the dropdown
    teacher_subjects_map = {}
    for teacher in teachers:
        teacher_subjects_map[teacher.id] = [
            {'id': sub.id, 'name': sub.name} for sub in teacher.subjects.all()
        ]

    context = {
        'days': all_days,
        'subjects': Subject.objects.all().order_by('name'),
        'classes': all_classes,
        'periods': all_periods,
        'teachers': teachers,
        'grouped_timetables': grouped_timetables, # Pass the new 2D grid
        'teacher_subjects_json': teacher_subjects_map
    }
    
    return render(request, 'manage_timetable.html', context)

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

def robots_txt(request):
    path = os.path.join(
        BASE_DIR,
        "../ImageWebsite/HtmlWebsite/robots.txt"
    )

    return FileResponse(
        open(path, "rb"),
        content_type="text/plain",
    )

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