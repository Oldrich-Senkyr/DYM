from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand, CommandError
from integral.ares.utils import get_entity_info

class Command(BaseCommand):
    help = 'Get entity info by code'

    def add_arguments(self, parser):
        parser.add_argument('code', type=int, help='The code of the entity')

    def handle(self, *args, **options):
        code = options['code']
        name, entity_type = get_entity_info(code)
        if name == "Unknown":
            raise CommandError(f"Code {code} not found in the registry.")
        self.stdout.write(self.style.SUCCESS(f'Kód: {code}, Název: {name}, Typ: {entity_type}'))

# To use this command, save it in a management/commands directory within one of your Django apps
# and run it with: python manage.py <command_name> <code>
