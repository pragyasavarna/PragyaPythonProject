import os
import sys
import django

# ==========================================
# 1. MANUALLY CONFIGURE DJANGO
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate UP two folders from AIModel/Model to reach the main project root
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(project_root)

# Tell Django where your settings file is
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ImageWebsite.settings")

# Boot up Django!
django.setup()

# ==========================================
# 2. RUN THE SCRIPT
# ==========================================
# Note: We must import the cache AFTER django.setup() is called
from django.core.cache import cache

def run_cleanup():
    print("Starting daily cache cleanup...")
    
    # Nuke the entire cache
    cache.clear()
    
    print("SUCCESS: Cleared the website cache for a fresh day!")

# Run the function if this script is executed directly
if __name__ == "__main__":
    run_cleanup()