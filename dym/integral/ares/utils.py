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
            company_name = str(data.get("obchodniJmeno", ""))
            company_ID =  str(data.get("ico", ""))
            vat_ID = str(data.get("dic", ""))
            
            # Rejstrik obchodnich spolecnosti
            ROS = data.get("pravniForma", "")
            legal_form, entity_type = get_entity_info(int(ROS))
            return {
                "Company Name": company_name,
                "Company ID": company_ID,
                "VAT ID": vat_ID,
                "Legal Form": legal_form,
                "Entity Type": entity_type,
            }
        else:
            print(f"Chyba: API vrátilo status {response.status_code} pro IČO {ico}")
            return None
    except Exception as e:
        print(f"Chyba při získávání dat pro IČO {ico}: {e}")
        return None



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
#code = 121
#name, entity_type = get_entity_info(code)
#print(f"Kód: {code}, Název: {name}, Typ: {entity_type}")

# Output will be:
# Kód: 121, Název: Akciová společnost, Typ: právnická osoba
