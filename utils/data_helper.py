from dataclasses import dataclass
from pathlib import Path
import random
from faker import Faker
import string

@dataclass
class PersonData:
    pohlavie: str
    meno: str
    priezvisko: str
    rodne_cislo: str
    datum_narodenia: str
    vekovy_rozsah: list[int]
    text: str


def pop_random_person_from_file(file_path: str) -> PersonData:
    path = Path(file_path)

    with path.open("r", encoding="utf-8", newline="") as file:
        lines = file.readlines()

    valid_indexes = [i for i, line in enumerate(lines) if line.strip()]

    if not valid_indexes:
        raise ValueError(f"Súbor '{file_path}' neobsahuje žiadne údaje.")

    selected_index = random.choice(valid_indexes)
    selected_line = lines.pop(selected_index).rstrip("\r\n")

    with path.open("w", encoding="utf-8", newline="") as file:
        file.writelines(lines)

    parts = [part.strip() for part in selected_line.split(";")]

    if len(parts) == 2:
        return PersonData(
            meno=parts[0],
            priezvisko=parts[1],
        )
    elif len(parts) == 3:
        return PersonData(
            meno=parts[0],
            priezvisko=parts[1],
            rodne_cislo=parts[2],
        )
    elif len(parts) == 4:
        return PersonData(
            meno=parts[0],
            priezvisko=parts[1],
            rodne_cislo=parts[2],
            text=parts[3],
        )
    else:
        raise ValueError(
            f"Neplatný formát riadku v súbore '{file_path}': {selected_line}"
        )
    
fake = Faker([
    "en_US", "en_GB", "fr_FR", "de_DE", "es_ES",
    "it_IT", "pt_BR", "nl_NL", "pl_PL", "cs_CZ",
    "sk_SK", "hu_HU", "ro_RO", "tr_TR",
    "sv_SE", "da_DK", "fi_FI", "hr_HR"
])

used_full_names = set()
used_birth_numbers = set()

def _generate_random_text() -> str:
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    digits = ''.join(random.choices("123456789", k=6))
    return f"{letters}{digits}"

def _generate_valid_birth_number_from_date(birth_date, gender: str) -> str:
    yy = birth_date.year % 100
    mm = birth_date.month + (50 if gender == "female" else 0)
    dd = birth_date.day
    date_part = f"{yy:02d}{mm:02d}{dd:02d}"

    suffixes = list(range(1000))
    random.shuffle(suffixes)

    for suffix in suffixes:
        base9 = f"{date_part}{suffix:03d}"
        remainder = int(base9) % 11

        check_digit = (11 - remainder) % 11
        if check_digit == 10:
            continue

        rc_no_slash = f"{base9}{check_digit}"

        if rc_no_slash not in used_birth_numbers and int(rc_no_slash) % 11 == 0:
            used_birth_numbers.add(rc_no_slash)
            return f"{rc_no_slash[:6]}/{rc_no_slash[6:]}"

    raise ValueError("Nepodarilo sa nájsť validné rodné číslo pre daný dátum.")


def generate_unique_person(age=None, min_age=1, max_age=18, gender=None) -> PersonData:
    if age is not None:
        min_age = age
        max_age = age

    for _ in range(10000):
        selected_gender = gender or random.choice(["male", "female"])

        if selected_gender == "male":
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()

        last_name = fake.last_name()
        full_name_key = (first_name.strip(), last_name.strip())

        if full_name_key in used_full_names:
            continue

        birth_date = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
        birth_number = _generate_valid_birth_number_from_date(birth_date, selected_gender)
        text = _generate_random_text()

        used_full_names.add(full_name_key)

        return PersonData(
            pohlavie=selected_gender,
            meno=first_name,
            priezvisko=last_name,
            rodne_cislo=birth_number,
            datum_narodenia=birth_date.isoformat(),
            vekovy_rozsah=[min_age, max_age],
            text=text,
        )

    raise ValueError("Nepodarilo sa vygenerovat unikatnu kombinaciu mena a priezviska.")