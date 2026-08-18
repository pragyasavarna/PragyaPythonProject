from django.contrib import admin

# Register your models here.
from .models import ContactMessage, UserAccount, UploadedImage, Feedback, BlogPost,BlogPageImage, CodeExecution,Service,HomePage,AITool, AITutorPage, Subject, Teacher, DayOfWeek, ClassGroup, PeriodTime, TimetableEntry, Technology, SocialSharePlatform, CodeExecution_C, UserSavedCCode, PrivacyPolicy, OutgoingEmailLog
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import Textarea, TextInput
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import DateWidget
from .admin_grouping import apply_custom_admin_structure
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_static.admin import StaticDeviceAdmin
from django.core.files.base import ContentFile
from django.utils.html import mark_safe
from io import BytesIO
from PIL import Image
import os

User = get_user_model()

admin.site.register(ContactMessage)
admin.site.register(Feedback)
admin.site.register(UploadedImage)

# 1. Register BlogPost
@admin.register(BlogPost)
class BlogPostResource(ImportExportModelAdmin):
    # This specifically tells the importer how to parse the date string 
    # for BOTH importing and comparing against existing records.
    published_at = fields.Field(
        column_name='published_at',
        attribute='published_at',
        widget=DateWidget(format='%d-%m-%Y') 
    )

    class Meta:
        model = BlogPost
        # Optional: This tells it to use the 'slug' to check if a post already exists, 
        # rather than needing an ID.
        import_id_fields = ('slug',)
    # Add the tool to readonly fields
    readonly_fields = ('image_inserter',)
    
    # Optional: Define the order of fields so the tool sits right above 'content'
    fields = (
        'title', 
        'slug', 
        'category', 
        'category_css_class', 
        'image_inserter', # 🟢 The custom image tool
        'content', 
        'published_at', 
        'link'
    )

    # The custom Image Inserter Interface
    def image_inserter(self, obj):
        import os
        from django.utils.html import mark_safe
        from django.template import Template, Context
        from .models import BlogPageImage
        
        # 1. Fetch all saved images from the database
        images = BlogPageImage.objects.exclude(
            image_full_url__isnull=True
        ).exclude(
            image_full_url__exact=''
        )
        
        if not images.exists():
            return mark_safe("<strong style='color: red;'>No images found. Please upload images in the 'Blog Page Image' tab first.</strong>")
        
        # 2. Prepare the data list to pass to the HTML file
        image_data = []
        for img in images:
            file_name = img.blog_image.name.split('/')[-1] if img.blog_image else "Image"
            image_data.append({
                'url': img.image_full_url,
                'name': file_name,
                'id': img.pk
            })
        
        # 3. Dynamically locate your HTML file in 'AIModel/Model/image_inserter.html'
        # This goes from first_app -> up to ImageWebsite -> down to AIModel/Model
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) 
        html_path = os.path.join(project_root, 'AIModel', 'Model','Html','image_inserter.html')
        
        # 4. Read and render the file
        try:
            with open(html_path, 'r', encoding='utf-8') as file:
                raw_html = file.read()
                
            # Process the {% for %} loops using Django's engine
            template = Template(raw_html)
            context = Context({'images': image_data})
            
            return mark_safe(template.render(context))
            
        except FileNotFoundError:
            return mark_safe(f"<strong style='color: red;'>Error: Could not find HTML file at {html_path}</strong>")
    
    image_inserter.short_description = 'Media Manager' 

@admin.register(BlogPageImage)
class BlogPageImageAdmin(ImportExportModelAdmin):
    # 1. Change 'image_url_display' to the new database field 'image_full_url'
    list_display = ('__str__', 'image_preview', 'image_full_url')
    
    # 2. Make the new database field read-only in the form
    readonly_fields = ('image_preview', 'image_full_url')

    # Custom field to show a mini preview of the image
    def image_preview(self, obj):
        if obj.blog_image:
            return mark_safe(f'<img src="{obj.blog_image.url}" style="max-height: 100px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" />')
        return "No Image Uploaded"
    image_preview.short_description = 'Preview'

    # (The old image_url_display function has been completely removed)

    # 3. Intercept the save to convert the image to PNG AND save the full URL
    def save_model(self, request, obj, form, change):
        # Check if a new image was uploaded
        if 'blog_image' in form.changed_data and obj.blog_image:
            uploaded_file = form.cleaned_data.get('blog_image')
            
            if uploaded_file:
                # Open the image in memory and convert to RGBA (supports transparency)
                img = Image.open(uploaded_file).convert("RGBA")
                buffer = BytesIO()
                
                # Save into the buffer strictly as a PNG
                img.save(buffer, format="PNG")
                
                # Strip the old extension and force .png
                original_name = os.path.splitext(uploaded_file.name)[0]
                new_filename = f"{original_name}.png"
                
                # Save the new PNG file to the model field (save=False prevents double DB hits)
                obj.blog_image.save(new_filename, ContentFile(buffer.getvalue()), save=False)
        
        # 🟢 NEW: Generate and save the absolute URL directly to the database
        if obj.blog_image:
            # request.build_absolute_uri dynamically grabs the current domain (local or live)
            obj.image_full_url = request.build_absolute_uri(obj.blog_image.url)
        else:
            obj.image_full_url = ""
                
        # Commit the object to the database
        super().save_model(request, obj, form, change)

# 1. Create the nested "Inline" table for Services
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1  # Shows one blank row by default for easy adding
    ordering = ('order',)  # Keeps your sorting logic intact inside the grid
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30})}, # cols controls width
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},         # size controls width
        models.URLField:  {'widget': TextInput(attrs={'size': '20'})},
    }

class TechnologyInline(admin.TabularInline):
    model = Technology
    extra = 1  # Shows one blank row by default for easy adding
    ordering = ('order',)  # Keeps your sorting logic intact inside the grid
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})}, # size controls width
    }

# 2. Attach the inline to your existing Home Page Admin
@admin.register(HomePage)
class HomePageAdmin(ImportExportModelAdmin):
    list_display = ('__str__', 'title')
    inlines = [ServiceInline, TechnologyInline]

@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('title', 'icon', 'order')

@admin.register(Technology)
class TechnologyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'order')

@admin.register(SocialSharePlatform)
class SocialSharePlatformAdmin(ImportExportModelAdmin):
    list_display = ('title', 'css_class', 'order')
    list_editable = ('order',)
    
# This tells Django to display the tools as a list inside the Page view
class AIToolInline(admin.TabularInline):
    model = AITool
    extra = 1 # Shows one blank extra row at the bottom for easy adding

# This registers the Page, and attaches the list of tools to it
@admin.register(AITutorPage)
class AITutorPageAdmin(ImportExportModelAdmin):
    inlines = [AIToolInline]

@admin.register(AITool)
class AIToolAdmin(ImportExportModelAdmin):
    list_display = ('name', 'url', 'is_coming_soon', 'order')
    list_editable = ('is_coming_soon', 'order')

@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    # 'get_subjects' is a custom method to display the ManyToMany relationship in the list view
    list_display = ('name', 'get_subjects')
    search_fields = ('name',)
    filter_horizontal = ('subjects',) 

    def get_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    get_subjects.short_description = 'Assigned Subjects'

class TimetableEntryInline(admin.TabularInline):
    model = TimetableEntry
    extra = 1
    autocomplete_fields = ['teacher', 'period', 'subject'] # Added subject here

@admin.register(ClassGroup)
class ClassGroupAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [TimetableEntryInline]

@admin.register(PeriodTime)
class PeriodTimeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'period_number', 'start_time', 'end_time', 'is_lunch')
    list_editable = ('start_time', 'end_time', 'is_lunch')
    ordering = ('start_time',)
    search_fields = ('name',)

@admin.register(DayOfWeek)
class DayOfWeekAdmin(ImportExportModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    ordering = ('order',)

@admin.register(TimetableEntry)
class TimetableEntryAdmin(ImportExportModelAdmin):
    list_display = ('class_group', 'get_days', 'period', 'teacher', 'subject')
    list_editable = ('teacher', 'subject')
    list_filter = ('class_group', 'period', 'teacher', 'subject')
    filter_horizontal = ('days',)

    def get_days(self, obj):
        return ", ".join([d.name for d in obj.days.all()])
    get_days.short_description = 'Days'

class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'name', 'profile', 'dob', 'phone', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'profile', 'dob', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'profile', 'dob', 'phone', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )


admin.site.register(UserAccount, CustomUserAdmin)

@admin.register(CodeExecution)
class CodeExecutionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'display_user', 'short_code', 'short_output', 'ip_address', 'city', 'state', 'country', 'executed_at')
    ordering = ('-executed_at',)
    search_fields = ('user__email', 'user__name', 'code', 'output', 'ip_address', 'city', 'state', 'country')
    list_filter = ('executed_at',)

    # --- Add Unknown to dropdown ---
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            qs = User.objects.all()
            kwargs["queryset"] = qs

            # Add "Unknown" option manually
            kwargs["empty_label"] = "Unknown"

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Enable searching "Unknown"
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # If admin typed "unknown", include rows with user=NULL
        if search_term.lower() == "unknown":
            queryset |= self.model.objects.filter(user__isnull=True)
        
        return queryset, use_distinct

    def display_user(self, obj):
        return obj.user.name if obj.user else "Unknown"
    display_user.short_description = "User"

    # Short preview of code
    def short_code(self, obj):
        return (obj.code[:50] + "...") if len(obj.code) > 50 else obj.code

    # Short preview of output
    def short_output(self, obj):
        return (obj.output[:50] + "...") if len(obj.output) > 50 else obj.output

    short_code.short_description = "Code Input"
    short_output.short_description = "Code Output"

@admin.register(CodeExecution_C)
class CodeExecution_CAdmin(ImportExportModelAdmin):
    list_display = ('id', 'display_user', 'short_code', 'short_output', 'ip_address', 'city', 'state', 'country', 'executed_at')
    ordering = ('-executed_at',)
    search_fields = ('user__email', 'user__name', 'code', 'output', 'ip_address', 'city', 'state', 'country')
    list_filter = ('executed_at',)

    # --- Add Unknown to dropdown ---
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            qs = User.objects.all()
            kwargs["queryset"] = qs

            # Add "Unknown" option manually
            kwargs["empty_label"] = "Unknown"

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Enable searching "Unknown"
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # If admin typed "unknown", include rows with user=NULL
        if search_term.lower() == "unknown":
            queryset |= self.model.objects.filter(user__isnull=True)
        
        return queryset, use_distinct

    def display_user(self, obj):
        return obj.user.name if obj.user else "Unknown"
    display_user.short_description = "User"

    # Short preview of code
    def short_code(self, obj):
        return (obj.code[:50] + "...") if len(obj.code) > 50 else obj.code

    # Short preview of output
    def short_output(self, obj):
        return (obj.output[:50] + "...") if len(obj.output) > 50 else obj.output

    short_code.short_description = "Code Input"
    short_output.short_description = "Code Output"

@admin.register(UserSavedCCode)
class UserSavedCCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(ImportExportModelAdmin):
    list_display = ('title', 'updated_at')

# 1. Unregister the default StaticDevice admin
admin.site.unregister(StaticDevice)

# 2. Re-register it with our brand new custom action
@admin.register(StaticDevice)
class CustomStaticDeviceAdmin(StaticDeviceAdmin):
    actions = ['generate_random_tokens']

    def generate_random_tokens(self, request, queryset):
        for device in queryset:
            # Generates 5 completely random, secure tokens per device
            for _ in range(5):
                token = StaticToken.random_token()
                StaticToken.objects.create(device=device, token=token)
                
        self.message_user(request, "Successfully generated 5 random tokens for selected devices.")
        
    generate_random_tokens.short_description = "Generate 5 random static tokens"

@admin.register(OutgoingEmailLog)
class OutgoingEmailLogAdmin(ImportExportModelAdmin):
    list_display = ('recipient', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('recipient',)
    
    # Make it read-only for security
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False

apply_custom_admin_structure()