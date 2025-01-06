from django.core.management.base import BaseCommand
import os
import re
from django.conf import settings

class Command(BaseCommand):
    help = 'Zpracuje soubor a uloží zpracovaný soubor s příponou _conv'

    def add_arguments(self, parser):
        parser.add_argument('input_filename', type=str, help='Název vstupního souboru')

    def handle(self, *args, **kwargs):
        input_filename = kwargs['input_filename']
        
        # Opravená cesta k souboru, bez zbytečných složek 'dym'
        file_path = os.path.join(settings.BASE_DIR, 'orders', 'locale', 'cs', 'LC_MESSAGES', input_filename)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Soubor '{input_filename}' nebyl nalezen v adresáři {file_path}"))
            return

        try:
            # Otevření souboru a čtení obsahu
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()

            # Regulární výraz pro hledání bloků msgid a msgstr
            msgid_msgstr_pattern = r'msgid "(.*?)"\s*msgstr ""'
            
            # Vyhledání všech výskytů msgid, kde je msgstr prázdný
            matches = re.findall(msgid_msgstr_pattern, content)

            # Pokud byly nalezeny odpovídající msgid hodnoty, zapisujeme je
            if matches:
                output_filename = input_filename.replace('.po', '_conv.po')  # Změna přípony na _conv.po
                output_path = os.path.join(settings.BASE_DIR, 'orders', 'locale', 'cs', 'LC_MESSAGES', output_filename)

                # Uložení msgid na každý řádek ve výstupním souboru
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    for msgid in matches:
                        outfile.write(msgid + '\n')

                self.stdout.write(self.style.SUCCESS(f'File processed successfully: {output_filename}'))

            else:
                self.stdout.write(self.style.WARNING('No msgid with empty msgstr found in the file.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {str(e)}'))
