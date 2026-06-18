from dataclasses import dataclass
from pathlib import Path
import random


@dataclass
class PersonData:
    meno: str
    priezvisko: str
    rodne_cislo: str | None = None
    text: str | None = None


def pop_random_person_from_file(file_path: str) -> PersonData:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError(f"Súbor '{file_path}' neobsahuje žiadne údaje.")

    random_index = random.randrange(len(lines))
    selected_line = lines.pop(random_index)

    with path.open("w", encoding="utf-8") as file:
        for line in lines:
            file.write(f"{line}\n")

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