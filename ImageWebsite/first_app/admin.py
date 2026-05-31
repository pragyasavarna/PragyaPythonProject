from django.contrib import admin

# Register your models here.
from .models import ContactMessage, UserAccount, UploadedImage, Feedback, BlogPost, CodeExecution
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

User = get_user_model()

admin.site.register(ContactMessage)
admin.site.register(Feedback)
admin.site.register(UploadedImage)

# 1. Register BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'published_at')
    ordering = ('-published_at',)
    prepopulated_fields = {'slug': ('title',)}

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
