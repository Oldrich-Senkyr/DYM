# core/management/commands/generate_csv.py

import csv, os
from django.core.management.base import BaseCommand
from integral.ares.utils import get_data_from_ares

class Command(BaseCommand):
    help = "Vytvoří CSV soubor s daty z ARES na základě zadaných IČO."

    def add_arguments(self, parser):
        parser.add_argument(
            'icos', nargs='+', type=str, 
            help="Seznam IČO oddělených mezerou. Např.: 12345678 87654321"
        )
        parser.add_argument(
            '--output', type=str, default='ares_data_V01.csv',
            help="Název výstupního CSV souboru."
        )

    def handle(self, *args, **kwargs):
        icos = kwargs['icos']
        filename = kwargs['output']

        directory = 'dev_files/mock_data' 
        output_file = os.path.join(directory, filename)



        data_list = []
        for ico in icos:
            try:
                data = get_data_from_ares(ico)  # Zde dostanu data 
                data_list.append(data)
                self.stdout.write(self.style.SUCCESS(f"Data načtena pro IČO {ico}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Chyba u IČO {ico}: {e}"))

        # Vytvoření CSV souboru
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Company Name", "Company ID", "VAT ID", "Legal Form","Entity Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)


            writer.writeheader()
            writer.writerows(data_list)

        self.stdout.write(self.style.SUCCESS(f"CSV soubor byl úspěšně vytvořen: {output_file}"))


