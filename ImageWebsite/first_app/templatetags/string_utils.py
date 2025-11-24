import os
import xml.etree.ElementTree as ET
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_string(key):
    try:
        # Construct path to strings.xml
        # Assuming first_app is the app name and it's in the project root or similar
        # We can try to find it relative to this file
        
        current_file = os.path.abspath(__file__)
        # templatetags dir -> first_app dir -> strings.xml
        strings_path = os.path.join(os.path.dirname(os.path.dirname(current_file)), 'strings.xml')
        
        if not os.path.exists(strings_path):
             # Fallback if not found relative to file, try using settings.BASE_DIR if available
             # But relative path should work if structure is standard
             return "Strings File Not Found"

        tree = ET.parse(strings_path)
        root = tree.getroot()
        
        # Find the string with name="key"
        for string in root.findall('string'):
            if string.get('name') == key:
                return string.text
                
        return f"String '{key}' Not Found"
        
    except Exception as e:
        return f"Error loading string: {str(e)}"
