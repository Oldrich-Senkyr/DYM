import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Dumpdata in UTF-8 encoding'

    def handle(self, *args, **kwargs):
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        current_time = datetime.now().strftime('%y%m%d_%H%M')
        filename = f'backup_{current_time}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            call_command('dumpdata', stdout=f)
        self.stdout.write(self.style.SUCCESS(f'Successfully dumped data to {filename} in UTF-8 encoding'))

