import sys
import os
import django
from pathlib import Path



current_directory = Path(__file__).resolve().parent.parent.parent
savingsBot_path = current_directory / 'savingsBot'
savingsBot_path=savingsBot_path.as_posix().replace('/', '\\')
sys.path.append(savingsBot_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'savingsBot.settings'
django.setup()
