import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.exceptions import ValidationError

# 1. Create a strict storage class that deletes old files instead of renaming new ones
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            try:
                # Attempt to overwrite the file
                os.remove(os.path.join(self.location, name))
            except PermissionError:
                # If Windows locks the file, do not crash! 
                # Just skip the deletion and let Django rename it safely.
                pass 
                
        # Use Django's built-in safely logic to return the final name
        return super().get_available_name(name, max_length)

# 2. Apply it to your target folder
custom_image_storage = OverwriteStorage(
    location=os.path.join(settings.BASE_DIR, 'HtmlWebsite', 'Image'),
    base_url='/Image/'
)

class HomePage(models.Model):
    title = models.CharField(max_length=100, default="Cognilume", help_text="Main heading")
    subtitle = models.TextField()
    
    # Primary Button (Sign Up)
    primary_btn_text = models.CharField(max_length=50, default="Sign up for Cognilume")
    primary_btn_link = models.CharField(max_length=200, default="/register/")
    
    # Secondary Button (Try AI Tutor)
    secondary_btn_text = models.CharField(max_length=50, default="Try AI Tutor free")
    secondary_btn_link = models.CharField(max_length=200, default="/ai-tutor/")
    
    # Image Configuration
    hero_image = models.ImageField(
        storage=custom_image_storage,
        upload_to='Home/',
        blank=True, 
        null=True, 
        help_text="Upload your brain image here"
    )
    image_alt_text = models.CharField(max_length=100, default="Cognilume Intelligence")
    services_label = models.CharField(max_length=50, blank=True, default="WHAT WE DO")
    services_heading_main = models.CharField(max_length=100, blank=True, default="Intelligent Solutions for a")
    services_heading_highlight = models.CharField(max_length=50, blank=True, default="Smarter Tomorrow")
    class Meta:
        verbose_name_plural = "Home Page Content" 

    def __str__(self):
        return "Home Page Settings"

class Service(models.Model):
    home_page = models.ForeignKey('HomePage', on_delete=models.CASCADE, related_name='services', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or FontAwesome class (e.g., 🧠 or 'fas fa-brain')")
    link = models.CharField(max_length=200, blank=True, null=True, help_text="Link for the 'Learn More' button")
    order = models.IntegerField(default=0, help_text="Order in which it appears on the page")

    class Meta:
        ordering = ['order'] # Ensures they display in the correct order

    def __str__(self):
        return self.title

class Technology(models.Model):
    # Added the ForeignKey to match the Service model structure
    home_page = models.ForeignKey('HomePage', on_delete=models.CASCADE, related_name='technologies', null=True)
    
    name = models.CharField(max_length=50) # e.g., 'Python', 'React'
    logo = models.ImageField(
        storage=custom_image_storage,
        upload_to='Home/Technology',
        blank=True, 
        null=True, 
        help_text="Upload your logo image here"
    )
    order = models.IntegerField(default=0, help_text="Order in which they appear")

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

class SocialSharePlatform(models.Model):
    title = models.CharField(max_length=50, help_text="e.g., Twitter, Facebook, Truth Social")
    css_class = models.CharField(max_length=50, help_text="e.g., twitter, facebook, truth, bsky")
    share_url_base = models.CharField(max_length=500, help_text="Base URL (e.g., https://twitter.com/intent/tweet?text=Check+this+out!&url=)")
    svg_code = models.TextField(help_text="Paste the entire <svg> tag here")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the icons appear")

    class Meta:
        ordering = ['order']
        verbose_name = "Share Platform"
        verbose_name_plural = "Share Platforms"

    def __str__(self):
        return self.title

# 1. Tripwire for the Home Page text/images
@receiver(post_save, sender=HomePage)
@receiver(post_delete, sender=HomePage)
def clear_homepage_cache(sender, **kwargs):
    cache.clear()  # This instantly deletes the saved HTML snapshot

# 2. Tripwire for the nested Services table
@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
def clear_service_cache(sender, **kwargs):
    cache.clear()

# 3. Tripwire for the Technology stack
@receiver(post_save, sender=Technology)
@receiver(post_delete, sender=Technology)
def clear_technology_cache(sender, **kwargs):
    cache.clear()

@receiver(post_save, sender=SocialSharePlatform)
@receiver(post_delete, sender=SocialSharePlatform)
def clear_share_platforms_cache(sender, **kwargs):
    cache.delete('footer_data')

class AITutorPage(models.Model):
    page_title = models.CharField(max_length=255, default="AI Tutor – Core Learning Tools")

    def __str__(self):
        return self.page_title

class AITool(models.Model):
    page = models.ForeignKey(AITutorPage, related_name='tools', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    is_coming_soon = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    # NEW: The backend handles the logic here
    @property
    def css_class(self):
        if self.is_coming_soon:
            return "coming-soon"
        return ""

# 1. Tripwire for the AI Tutor Page (Page Title)
@receiver(post_save, sender=AITutorPage)
@receiver(post_delete, sender=AITutorPage)
def clear_ai_tutor_page_cache(sender, instance, **kwargs):
    # This specifically deletes only the title cache
    cache.delete('ai_tutor_page_title')
    print("DEBUG: AI Tutor Page title cache cleared!")

# 2. Tripwire for the individual AI Tools
@receiver(post_save, sender=AITool)
@receiver(post_delete, sender=AITool)
def clear_ai_tool_cache(sender, instance, **kwargs):
    # This surgically deletes ONLY the specific tool you just edited
    # keeping all your other tools safely cached!
    cache.delete(f'ai_tool_{instance.id}')
    print(f"DEBUG: Cache cleared for AI Tool ID: {instance.id}")

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.subject}"

class Feedback(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('General Feedback', 'General Feedback'),
        ('Bug', 'Bug'),
        ('Feature Request', 'Feature Request'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.issue_type} - {self.subject}"

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True, help_text="URL-friendly name (e.g. my-first-post)")
    category = models.CharField(max_length=100, help_text="e.g. Deep Learning, Web Dev")
    # This field lets you apply the 'tech-web' class for the Cyan color
    category_css_class = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Leave empty for Pink. Type 'tech-web' for Cyan."
    )
    content = models.TextField()
    published_at = models.DateField()
    link = models.URLField(blank=True, null=True, help_text="Link to full article (optional)")

    def __str__(self):
        return self.title

class CodeExecution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    output = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        user_display = self.user.name if self.user else "Unknown"
        # show IST on header
        from django.utils.timezone import localtime
        ist_time = localtime(self.executed_at)
        return f"{user_display} - {ist_time.strftime('%b %d, %Y %I:%M %p')}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'subject_table'
        ordering = ['name']

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    # A teacher can teach many subjects, and a subject can be taught by many teachers
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    class Meta:
        db_table = 'teacher_table'

    def __str__(self):
        return self.name

class ClassGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'class_table'

    def __str__(self):
        return self.name

class PeriodTime(models.Model):
    period_number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_lunch = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class DayOfWeek(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.IntegerField(default=0, help_text="Use this to sort days (e.g., Monday=1, Tuesday=2)")

    class Meta:
        db_table = 'day_of_week_table'
        ordering = ['order']

    def __str__(self):
        return self.name

class TimetableEntry(models.Model):
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='schedule')
    days = models.ManyToManyField(DayOfWeek, related_name='timetable_entries')
    period = models.ForeignKey(PeriodTime, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.class_group.name} - {self.period.name}"

# ==========================================
# 1. Tripwire for Class Groups (Dropdown Menu)
# ==========================================
@receiver(post_save, sender=ClassGroup)
@receiver(post_delete, sender=ClassGroup)
def clear_class_group_cache(sender, instance, **kwargs):
    # Clears the cached list of classes used in the header dropdown
    cache.delete('all_classes_data')
    print(f"DEBUG: 'all_classes_data' cache cleared due to ClassGroup update!")

# ==========================================
# 2. Tripwire for Periods (The Y-Axis Grid)
# ==========================================
@receiver(post_save, sender=PeriodTime)
@receiver(post_delete, sender=PeriodTime)
def clear_period_time_cache(sender, instance, **kwargs):
    # Clears the structural layout of the timetable grid
    cache.delete('all_periods_data')
    print(f"DEBUG: 'all_periods_data' cache cleared due to PeriodTime update!")

# ==========================================
# 3. Tripwire for Individual Timetable Entries
# ==========================================
@receiver(post_save, sender=TimetableEntry)
@receiver(post_delete, sender=TimetableEntry)
def clear_timetable_entry_cache(sender, instance, **kwargs):
    # Surgically deletes ONLY the specific day/period lecture you just edited
    cache.delete(f'tt_entry_{instance.id}')
    print(f"DEBUG: Cache cleared for TimetableEntry ID: {instance.id}")

# ==========================================
# 4. Tripwire for Teacher Updates (Cascading Cache Clear)
# ==========================================
@receiver(post_save, sender=Teacher)
@receiver(post_delete, sender=Teacher)
def clear_teacher_cascade_cache(sender, instance, **kwargs):
    # If you change a Teacher's name or subject, this finds EVERY lecture 
    # they are assigned to and surgically clears those specific entry caches.
    affected_entries = TimetableEntry.objects.filter(teacher=instance)
    
    # Generate the exact cache keys that need deleting
    keys_to_delete = [f'tt_entry_{entry.id}' for entry in affected_entries]
    
    # Delete them all at once (bulk delete is faster)
    cache.delete_many(keys_to_delete)
    print(f"DEBUG: Cleared {len(keys_to_delete)} TimetableEntry caches due to Teacher ID: {instance.id} update.")

# ==========================================
# 5. Tripwire for Subject Updates
# ==========================================
@receiver(post_save, sender=Subject)
@receiver(post_delete, sender=Subject)
def clear_subject_cascade_cache(sender, instance, **kwargs):
    affected_entries = TimetableEntry.objects.filter(subject=instance)
    keys_to_delete = [f'tt_entry_{entry.id}' for entry in affected_entries]
    if keys_to_delete:
        cache.delete_many(keys_to_delete)
        print(f"DEBUG: Cleared {len(keys_to_delete)} caches due to Subject: {instance.name} update.")
        # ==========================================
# 6. Tripwire for DayOfWeek Updates
# ==========================================
@receiver(post_save, sender=DayOfWeek)
@receiver(post_delete, sender=DayOfWeek)
def clear_days_cache(sender, instance, **kwargs):
    cache.delete('all_days_data')
    print("DEBUG: 'all_days_data' cache cleared due to DayOfWeek update!")