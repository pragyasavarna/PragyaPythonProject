from django.contrib import admin

# Register your models here.
from .models import ContactMessage, UserAccount, UploadedImage, Feedback, BlogPost, CodeExecution,Service,HomePage,AITool, AITutorPage, Subject, Teacher, DayOfWeek, ClassGroup, PeriodTime, TimetableEntry, Technology, SocialSharePlatform, CodeExecution_C, UserSavedCCode
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import Textarea, TextInput
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import DateWidget

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
    list_display = ('email', 'name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)


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