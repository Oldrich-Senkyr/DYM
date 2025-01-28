import os,sys
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Loaddata in UTF-8 encoding'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        # Zvýšení limitu rekurze
        sys.setrecursionlimit(2000)
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        filename = kwargs['filename']
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                call_command('loaddata', filename)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {filename} in UTF-8 encoding'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data from {filename}: {e}'))
