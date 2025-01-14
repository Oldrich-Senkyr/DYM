import csv
import requests
from django.core.management.base import BaseCommand


# Funkce pro získání dat z API ARES
def get_data_from_ares(ico):
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "Company Name": data.get("obchodniJmeno", ""),
                "Company ID": data.get("ico", ""),
                "VAT ID": data.get("dic", ""),
            }
        else:
            print(f"Chyba: API vrátilo status {response.status_code} pro IČO {ico}")
            return None
    except Exception as e:
        print(f"Chyba při získávání dat pro IČO {ico}: {e}")
        return None


class Command(BaseCommand):
    help = "Načte data z ARES pro zadané IČO a zapíše je do CSV souboru."

    def add_arguments(self, parser):
        parser.add_argument(
            "ico_list",
            nargs="+",
            help="Seznam IČO pro načtení dat z ARES",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="ares_data.csv",
            help="Cesta k výstupnímu CSV souboru",
        )

    def handle(self, *args, **options):
        ico_list = options["ico_list"]
        output_file = options["output"]

        # Inicializace seznamu pro data
        data_list = []

        # Načtení dat pro každé IČO
        for ico in ico_list:
            data = get_data_from_ares(ico)
            if data:
                data_list.append(data)
                print(f"Data načtena pro IČO {ico}")
            else:
                print(f"Data nebyla načtena pro IČO {ico}")

        if not data_list:
            print("Žádná data k zapsání.")
            return

        # Hlavička CSV
        fieldnames = ["Company Name", "Company ID", "VAT ID"]

        # Zapsání dat do CSV souboru
        try:
            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            print(f"CSV soubor '{output_file}' byl vytvořen s daty z ARES.")
        except ValueError as e:
            print(f"Chyba při zápisu do CSV: {e}")


# Dictionary mapping codes to their corresponding names and types
entity_dict = {
    121: ("Akciová společnost", "právnická osoba"),
    721: ("Církve a náboženské společnosti", "právnická osoba"),
    313: ("Česká národní banka", "právnická osoba"),
    362: ("Česká tisková kancelář", "právnická osoba"),
    771: ("Dobrovolný svazek obcí", "právnická osoba"),
    205: ("Družstvo", "právnická osoba"),
    722: ("Evidované církevní právnické osoby", "právnická osoba"),
    933: ("Evropská družstevní společnost", "právnická osoba"),
    932: ("Evropská společnost", "právnická osoba"),
    931: ("Evropské hospodářské zájmové sdružení", "právnická osoba"),
    941: ("Evropské seskupení pro územní spolupráci", "právnická osoba"),
    152: ("Garanční fond obchodníků s cennými papíry", "právnická osoba"),
    761: ("Honební společenstvo", "právnická osoba"),
    151: ("Komoditní burza", "právnická osoba"),
    745: ("Komora (hospodářská, agrární)", "právnická osoba"),
    804: ("Kraj", "právnická osoba"),
    811: ("Městská část, městský obvod", "právnická osoba"),
    921: ("Mezinárodní nevládní organizace", "právnická osoba"),
    907: ("Mezinárodní odborová organizace", "právnická osoba"),
    908: ("Mezinárodní organizace zaměstnavatelů", "právnická osoba"),
    951: ("Mezinárodní vojenská organizace vzniklá na základě mezinárodní smlouvy", "právnická osoba"),
    117: ("Nadace", "právnická osoba"),
    118: ("Nadační fond", "právnická osoba"),
    302: ("Národní podnik", "právnická osoba"),
    801: ("Obec", "právnická osoba"),
    141: ("Obecně prospěšná společnost", "právnická osoba"),
    707: ("Odborová organizace", "právnická osoba"),
    501: ("Odštěpný závod", "právnická osoba"),
    425: ("Odštěpný závod zahraniční fyzické osoby", "fyzická osoba"),
    421: ("Odštěpný závod zahraniční právnické osoby", "právnická osoba"),
    708: ("Organizace zaměstnavatelů", "právnická osoba"),
    922: ("Organizační jednotka mezinárodní nevládní organizace", "právnická osoba"),
    734: ("Organizační jednotka zvláštní organizace pro zastoupení českých zájmů v mezinárodních nevládních organizacích", "právnická osoba"),
    325: ("Organizační složka státu", "právnická osoba"),
    423: ("Organizační složka zahraniční nadace", "právnická osoba"),
    422: ("Organizační složka zahraničního nadačního fondu", "právnická osoba"),
    736: ("Pobočný spolek", "právnická osoba"),
    100: ("Podnikající fyzická osoba tuzemská", "fyzická osoba"),
    711: ("Politická strana, politické hnutí", "právnická osoba"),
    960: ("Právnická osoba zřízená zvláštním zákonem zapisovaná do veřejného rejstříku", "právnická osoba"),
    331: ("Příspěvková organizace zřízená územním samosprávným celkem", "právnická osoba"),
    353: ("Rada pro veřejný dohled nad auditem", "právnická osoba"),
    805: ("Regionální rada regionu soudržnosti", "právnická osoba"),
    741: ("Samosprávná stavovská organizace (profesní komora}", "právnická osoba"),
    521: ("Samostatná drobná provozovna (obecního úřadu)", "právnická osoba"),
    145: ("Společenství vlastníků jednotek", "právnická osoba"),
    113: ("Společnost komanditní", "právnická osoba"),
    112: ("Společnost s ručením omezeným", "právnická osoba"),
    706: ("Spolek", "právnická osoba"),
    352: ("Správa železniční dopravní cesty, státní organizace", "právnická osoba"),
    326: ("Stálý rozhodčí soud", "právnická osoba"),
    381: ("Státní fond ze zákona", "právnická osoba"),
    382: ("Státní fond ze zákona nezapisující se do obchodního rejstříku", "právnická osoba"),
    301: ("Státní podnik", "právnická osoba"),
    332: ("Státní příspěvková organizace", "právnická osoba"),
    723: ("Svazy církví a náboženských společností", "právnická osoba"),
    961: ("Svěřenský fond", "právnická osoba"),
    641: ("Školská právnická osoba", "právnická osoba"),
    161: ("Ústav", "právnická osoba"),
    111: ("Veřejná obchodní společnost", "právnická osoba"),
    661: ("Veřejná výzkumná instituce", "právnická osoba"),
    361: ("Veřejnoprávní instituce", "právnická osoba"),
    525: ("Vnitřní organizační jednotka organizační složky státu", "právnická osoba"),
    392: ("Všeobecná zdravotní pojišťovna", "právnická osoba"),
    601: ("Vysoká škola (veřejná, státní)", "právnická osoba"),
    424: ("Zahraniční fyzická osoba", "fyzická osoba"),
    936: ("Zahraniční pobočný spolek", "právnická osoba"),
    906: ("Zahraniční spolek", "právnická osoba"),
    962: ("Zahraniční svěřenský fond", "právnická osoba"),
    751: ("Zájmové sdružení právnických osob", "právnická osoba"),
    426: ("Zastoupení zahraniční banky", "právnická osoba"),
    391: ("Zdravotní pojišťovna (mimo VZP)", "právnická osoba"),
    704: ("Zvláštní organizace pro zastoupení českých zájmů v mezinárodních nevládních organizacích", "právnická osoba")
}

def get_entity_info(code):
    return entity_dict.get(code, ("Unknown", "Unknown"))

# Example usage:
code = 121
name, entity_type = get_entity_info(code)
print(f"Kód: {code}, Název: {name}, Typ: {entity_type}")

# Output will be:
# Kód: 121, Název: Akciová společnost, Typ: právnická osoba
