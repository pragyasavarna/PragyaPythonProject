from django.contrib import admin
from django.urls import reverse
from django.conf import settings

# 1. Save the original Django function so we can use it as a base
original_get_app_list = admin.site.get_app_list

def custom_get_app_list(request, app_label=None):
    # Get the default list of apps from Django
    app_list = original_get_app_list(request, app_label)
    
    # Find your specific app (Replace 'first_app' if your app is named differently)
    first_app_data = next((app for app in app_list if app['app_label'].lower() == 'first_app'), None)
    
    if not first_app_data:
        return app_list
        
    # Remove the original massive app from the list
    app_list = [app for app in app_list if app['app_label'].lower() != 'first_app']
    
    all_models = first_app_data['models']
    
    # 2. Define your groupings using the exact Model names
    code_output_models = ['CodeExecution', 'CodeExecution_C', 'UserSavedCCode']
    time_table_models = ['ClassGroup', 'DayOfWeek', 'PeriodTime', 'Subject', 'Teacher', 'TimetableEntry']

    # 3. Create empty groups linking back to the main dashboard
    try:
        main_app_url = reverse('admin:index')
    except Exception:
        main_app_url = f"/{settings.ADMIN_URL}"
    code_group = {'name': 'Code Output', 'app_label': 'code_output', 'app_url': main_app_url, 'has_module_perms': True, 'models': []}
    time_group = {'name': 'Time Table', 'app_label': 'time_table', 'app_url': main_app_url, 'has_module_perms': True, 'models': []}
    other_group = {'name': 'Other Pages', 'app_label': 'other_pages', 'app_url': main_app_url, 'has_module_perms': True, 'models': []}

    # 4. Sort the models into their respective groups
    for model in all_models:
        if model['object_name'] in code_output_models:
            code_group['models'].append(model)
        elif model['object_name'] in time_table_models:
            time_group['models'].append(model)
        elif model['object_name'] == 'OutgoingEmailLog':
            email_log_model = model
        else:
            other_group['models'].append(model)

    # 5. Add the new groups back to the main list
    if code_group['models']: app_list.append(code_group)
    if time_group['models']: app_list.append(time_group)
    if other_group['models']: app_list.append(other_group)
    
    otp_models = []
    # Extract models from both OTP apps
    for label in ['otp_static', 'otp_totp', 'otp_email']:
        app_data = next((app for app in app_list if app['app_label'].lower() == label), None)
        if app_data:
            otp_models.extend(app_data['models'])
    
    # Push the intercepted Email Log model into the Two-Factor list
    if email_log_model:
        otp_models.append(email_log_model)
        
    # Remove the original separated OTP apps from the main list
    app_list = [app for app in app_list if app['app_label'].lower() not in ['otp_static', 'otp_totp', 'otp_email']]
    
    # Create a new combined group and add it to the list
    if otp_models:
        otp_group = {
            'name': 'Two-Factor Authentication', 
            'app_label': 'two_factor_auth', 
            'app_url': main_app_url, 
            'has_module_perms': True, 
            'models': otp_models
        }
        # Insert it right below Authentication and Authorization (which is usually index 0 or 1)
        app_list.insert(1, otp_group)
        
    return app_list

# 6. Create a helper function to apply the override
def apply_custom_admin_structure():
    admin.site.get_app_list = custom_get_app_list