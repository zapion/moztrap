"WSGI entry-point for MozTrap."""
import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

# Set default settings and instantiate application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cc.settings.default")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
