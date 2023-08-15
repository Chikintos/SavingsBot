import sys
import os
import django

sys.path.append('savingsBot')
os.environ['DJANGO_SETTINGS_MODULE'] = 'savingsBot.settings'
django.setup()