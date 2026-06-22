import re
from bs4 import BeautifulSoup
from random import randint
from datetime import date
from datetime import datetime

class Helper:
    @staticmethod
    def vygeneruj_tel_cislo() -> str:
        cislo1 = randint(100, 999)
        cislo2 = randint(100, 999)
        telefon = '+421999' + str(cislo1) + str(cislo2)
        return telefon

    @staticmethod
    def aktualny_datum():
        dnes = date.today()
        return f"{dnes.day:02d}", f"{dnes.month:02d}", str(dnes.year)
    
    @staticmethod
    def rc_to_datum_narodenia(rc: str) -> str:
        cislo = rc.replace("/", "").strip()

        if not cislo or len(cislo) < 6:
            raise ValueError(f"Nesprávny formát rodného čísla: {rc}")

        rok_kod = int(cislo[0:2])
        mesiac_kod = int(cislo[2:4])
        den = int(cislo[4:6])

        mesiac = mesiac_kod - 50 if mesiac_kod > 50 else mesiac_kod

        if 0 <= rok_kod <= 71:
            plny_rok = 2000 + rok_kod
        else:
            plny_rok = 1900 + rok_kod

        datum_str = f"{plny_rok:04d}-{mesiac:02d}-{den:02d}"

        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            return datum.strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError(f"Nedá sa skonvertovať rodné číslo na platný dátum: {rc}")

    @staticmethod
    def get_pohlavie(rc: str) -> str:
        cislo = "".join(ch for ch in rc if ch.isdigit())

        if not cislo or len(cislo) < 4:
            raise ValueError(f"Nesprávny formát rodného čísla: {rc}")

        mesiac = int(cislo[2:4])

        if mesiac <= 12:
            return "mužské"
        return "ženské"
    
    @staticmethod
    def cleanup_email_text(text: str) -> str:
        if text is None:
            return None

        # 1. extrakcia čistého textu z HTML
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # 2. odstraň cid:... odkazy
        text = re.sub(r"\[?cid:[^\s\]]+\]?", "", text)

        # 3. všetky whitespace → jedna medzera
        text = re.sub(r"\s+", " ", text)

        return text.strip()
        
    @staticmethod
    def inkrementuj_identifikator(identifikator: str) -> str:
        prefix, number_part = identifikator.rsplit("-", 1)
        return f"{prefix}-{int(number_part) + 1}"