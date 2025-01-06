from django.core.management.base import BaseCommand
import os
import re
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = 'Zpracuje soubor a uloží zpracovaný soubor s příponou _conv'

    def add_arguments(self, parser):
        # Přidání argumentu pro název vstupního souboru
        parser.add_argument('input_filename', type=str, help='Název vstupního souboru')

    def handle(self, *args, **kwargs):
        print(settings.BASE_DIR)
        print('--------------------------------------------------------------')
        input_filename = kwargs['input_filename']
        

        # Opravená cesta k souboru, bez zbytečných složek 'dym'
        file_path = os.path.join(settings.BASE_DIR, 'products', 'locale', 'cs', 'LC_MESSAGES', input_filename)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Soubor '{input_filename}' nebyl nalezen v adresáři {file_path}"))
            return

        try:
            # Otevření souboru a čtení obsahu
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()

            # Provádění požadovaných nahrazení
            content = re.sub(r'^#:.*', '', content, flags=re.MULTILINE)  # Odstranění řádků začínajících #
            content = re.sub(r'msgid "', '', content)                       # Odstranění "msgid"
            content = re.sub(r'msgstr ""', '', content)                     # Odstranění "msgstr """
            content = re.sub(r'"', '', content)                              # Odstranění uvozovek
            content = re.sub(r'^\s*\r?\n', '', content, flags=re.MULTILINE)  # Odstranění prázdných řádků

            # Výstupní soubor
            output_filename = input_filename.replace('.po', '_conv.po')  # Změna přípony na _conv.po
            output_path = os.path.join(settings.BASE_DIR, 'agent', 'locale', 'cs', 'LC_MESSAGES', output_filename)

            # Uložení zpracovaného souboru
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(content)

            self.stdout.write(self.style.SUCCESS(f'File processed successfully: {output_filename}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {str(e)}'))
