from django.contrib import admin

# Register your models here.
from .models import ContactMessage, UserAccount, UploadedImage, Feedback, BlogPost
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(ContactMessage)
admin.site.register(Feedback)
admin.site.register(UploadedImage)

# 1. Register BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
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
