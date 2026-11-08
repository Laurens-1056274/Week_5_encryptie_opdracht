import base64
import json
import os
from getpass import getpass

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def maak_sleutel(wachtwoord, salt):
    """Maak een AES-256-sleutel uit het wachtwoord met scrypt."""
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(wachtwoord.encode("utf-8"))


def versleutel(tekst, wachtwoord):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    sleutel = maak_sleutel(wachtwoord, salt)
    versleutelde_tekst = AESGCM(sleutel).encrypt(nonce, tekst.encode("utf-8"), None)

    gegevens = {
        "versie": 1,
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "data": base64.b64encode(versleutelde_tekst).decode("ascii"),
    }
    return json.dumps(gegevens)


def ontsleutel(invoer, wachtwoord):
    gegevens = json.loads(invoer)
    if gegevens["versie"] != 1:
        raise ValueError("Onbekende versie van de versleutelde tekst.")

    salt = base64.b64decode(gegevens["salt"], validate=True)
    nonce = base64.b64decode(gegevens["nonce"], validate=True)
    data = base64.b64decode(gegevens["data"], validate=True)

    if len(salt) != 16 or len(nonce) != 12 or len(data) < 16:
        raise ValueError("Ongeldige versleutelde gegevens.")

    sleutel = maak_sleutel(wachtwoord, salt)
    tekst = AESGCM(sleutel).decrypt(nonce, data, None)
    return tekst.decode("utf-8")


def main():
    print("=== Tekst versleutelen en ontsleutelen ===")
    while True:
        print("\n1. Tekst versleutelen")
        print("2. Tekst ontsleutelen")
        print("3. Afsluiten")
        keuze = input("Maak een keuze (1/2/3): ").strip()

        if keuze == "1":
            tekst = input("Welke tekst wil je versleutelen? ")
            wachtwoord = getpass("Kies een sterk wachtwoord: ")
            if not wachtwoord:
                print("Het wachtwoord mag niet leeg zijn.")
                continue
            print("\nBewaar deze volledige uitvoer om later te ontsleutelen:")
            print(versleutel(tekst, wachtwoord))
        elif keuze == "2":
            invoer = input("Plak de volledige versleutelde tekst (JSON): ")
            wachtwoord = getpass("Voer het wachtwoord in: ")
            try:
                print("\nOntsleutelde tekst:")
                print(ontsleutel(invoer, wachtwoord))
            except (InvalidTag, ValueError, KeyError, TypeError, UnicodeDecodeError):
                print("Ontsleutelen mislukt: verkeerd wachtwoord of ongeldige gegevens.")
        elif keuze == "3":
            print("Programma afgesloten.")
            break
        else:
            print("Ongeldige keuze. Kies 1, 2 of 3.")


if __name__ == "__main__":
    main()
