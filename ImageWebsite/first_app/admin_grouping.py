from django.contrib import admin
from django.urls import reverse
from django.conf import settings

# 1. Configuration Map: (Group Name, Set of Model Object Names)
GROUPS_CONFIG = {
    'code_output': ('Code Output', {'CodeExecution', 'CodeExecution_C', 'UserSavedCCode'}),
    'time_table': ('Time Table', {'ClassGroup', 'DayOfWeek', 'PeriodTime', 'Subject', 'Teacher', 'TimetableEntry'}),
    'ai_tutor': ('AI Tutor', {'AITutorPage', 'AITool'}),
    'contact_feedback': ('Contact & Feedback', {'ContactMessage', 'Feedback'}),
    'homepage_management': ('Homepage Management', {'HomePage', 'Service', 'Technology', 'SocialSharePlatform'}),
    'blogging': ('Blogging', {'BlogPost'}),
    'legal_pages': ('Legal Pages', {'PrivacyPolicy'}),
    'accounts': ('Accounts', {'UserAccount'}),
}
OTP_LABELS = {'otp_static', 'otp_totp', 'otp_email'}

original_get_app_list = admin.site.get_app_list

def custom_get_app_list(request, app_label=None):
    app_list = original_get_app_list(request, app_label)
    
    first_app = next((app for app in app_list if app['app_label'].lower() == 'first_app'), None)
    if not first_app:
        return app_list

    try:
        main_url = reverse('admin:index')
    except Exception:
        main_url = f"/{settings.ADMIN_URL}"

    # Build empty target containers dynamically
    groups = {
        key: {'name': name, 'app_label': key, 'app_url': main_url, 'has_module_perms': True, 'models': []}
        for key, (name, _) in GROUPS_CONFIG.items()
    }
    other_models, otp_models = [], []

    # Sort first_app models
    for model in first_app['models']:
        name = model['object_name']
        if name == 'OutgoingEmailLog':
            otp_models.append(model)
            continue
        
        # Match model against config
        matched = next((key for key, (_, models) in GROUPS_CONFIG.items() if name in models), None)
        if matched:
            groups[matched]['models'].append(model)
        else:
            other_models.append(model)

    # Collect models from OTP apps and strip them along with first_app
    for app in app_list:
        if app['app_label'].lower() in OTP_LABELS:
            otp_models.extend(app['models'])
            
    app_list = [app for app in app_list if app['app_label'].lower() not in (OTP_LABELS | {'first_app'})]

    # Insert Two-Factor Authentication at index 1
    if otp_models:
        app_list.insert(1, {
            'name': 'Two-Factor Authentication',
            'app_label': 'two_factor_auth',
            'app_url': main_url,
            'has_module_perms': True,
            'models': otp_models,
        })

    # Append non-empty custom groups and remainder group
    app_list.extend(g for g in groups.values() if g['models'])
    if other_models:
        app_list.append({
            'name': 'Other Pages',
            'app_label': 'other_pages',
            'app_url': main_url,
            'has_module_perms': True,
            'models': other_models,
        })

    return app_list

def apply_custom_admin_structure():
    admin.site.get_app_list = custom_get_app_list