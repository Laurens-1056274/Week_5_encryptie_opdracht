# Tekst versleutelen en ontsleutelen

## Over het project
Voor deze opdracht heb ik een eenvoudige Python-applicatie gemaakt waarmee je tekst kunt versleutelen en ontsleutelen. De applicatie werkt via een keuzemenu in de terminal.

Ik gebruik hiervoor de bestaande Python-library `cryptography`, omdat het niet verstandig is om zelf een encryptiealgoritme te maken.

## Installatie en gebruik
Je hebt Python 3 en de library `cryptography` nodig.

1. Download of clone deze repository.
2. Open de terminal in de map van het project.
3. Installeer de library:

```bash
python -m pip install cryptography
```

4. Start de applicatie:

```bash
python main.py
```

In het menu kun je kiezen uit:

- **1:** Tekst versleutelen. Je voert tekst in en kiest een wachtwoord. De applicatie geeft vervolgens versleutelde gegevens in JSON-formaat terug.
- **2:** Tekst ontsleutelen. Je plakt de volledige JSON-uitvoer en voert hetzelfde wachtwoord in. Als alles klopt, krijg je de oorspronkelijke tekst terug.
- **3:** Het programma afsluiten.

**Belangrijk:** Bewaar de volledige JSON-uitvoer en onthoud het wachtwoord. Zonder het juiste wachtwoord kun je de tekst niet ontsleutelen.

## Onderzoek: symmetrische en asymmetrische encryptie
Bij **symmetrische encryptie** wordt dezelfde geheime sleutel gebruikt om informatie te versleutelen en weer te ontsleutelen. Dit is meestal snel en geschikt voor grotere hoeveelheden gegevens. Het nadeel is dat beide partijen veilig over dezelfde sleutel moeten beschikken.

Bij **asymmetrische encryptie** worden twee sleutels gebruikt: een publieke en een privésleutel. Met een publieke sleutel kun je informatie versleutelen die alleen met de bijbehorende privésleutel kan worden ontsleuteld.

Dit helpt bij het veilig delen van gegevens, maar is meestal langzamer. In de praktijk worden symmetrische en asymmetrische technieken vaak gecombineerd.

## Gekozen algoritme
Ik heb gekozen voor **AES-256-GCM**. AES is een veelgebruikt symmetrisch encryptiealgoritme. Het getal 256 betekent dat de sleutel 256 bits lang is.

GCM zorgt er niet alleen voor dat de inhoud versleuteld wordt, maar controleert bij het ontsleutelen ook of de versleutelde gegevens zijn aangepast.

Ik gebruik de `AESGCM`-implementatie uit de library `cryptography` en maak het algoritme dus niet zelf. Voor iedere versleuteling wordt een nieuwe willekeurige nonce van 12 bytes aangemaakt.

## Sleutelbeheer
In mijn applicatie typt de gebruiker een wachtwoord. Dat wachtwoord is niet rechtstreeks de AES-sleutel.

Met **scrypt** wordt uit het wachtwoord en een willekeurige salt van 16 bytes een sleutel van 32 bytes gemaakt. Scrypt maakt het voor een aanvaller duurder om veel wachtwoorden uit te proberen.

Het programma slaat het wachtwoord en de afgeleide sleutel niet op in een bestand.

De salt, nonce en versleutelde gegevens komen samen in de JSON-uitvoer te staan. De salt en nonce hoeven niet geheim te zijn.

Bij het ontsleutelen voert de gebruiker opnieuw het wachtwoord in. Met de opgeslagen salt kan dan dezelfde sleutel worden afgeleid.

Er is in deze applicatie geen automatische sleuteluitwisseling. Als iemand anders de tekst moet ontsleutelen, moet die persoon zowel de JSON-uitvoer als het wachtwoord krijgen.

Het wachtwoord moet via een **apart, veilig kanaal** worden gedeeld.

Deze aanpak is eenvoudig voor één gebruiker, maar heeft ook nadelen. De beveiliging hangt sterk af van de kwaliteit van het wachtwoord. Een zwak wachtwoord kan offline worden geraden als iemand de JSON-uitvoer in handen krijgt.

Bij veel gebruikers wordt het veilig verspreiden en beheren van wachtwoorden steeds moeilijker. Dan zou een andere oplossing voor sleutelbeheer, bijvoorbeeld met publieke sleutels, beter passen.

Wie het wachtwoord vergeet, kan de tekst niet meer herstellen.

## Kerckhoffs's Principe
Kerckhoffs's Principe betekent dat een versleutelingssysteem veilig moet blijven, zelfs als iedereen weet hoe het werkt. Alleen de geheime sleutel moet geheim blijven.

Mijn applicatie sluit hierop aan doordat de Python-code en de gebruikte algoritmen openbaar mogen zijn.

Ik vertrouw niet op het geheimhouden van de code, maar op de veiligheid van AES-256-GCM, scrypt en het gekozen wachtwoord. De salt en nonce mogen ook bekend zijn.

Dit betekent niet dat iedere versleuteling automatisch veilig is. Met een zwak wachtwoord blijft de applicatie kwetsbaar.

Het geheimhouden van een sterk wachtwoord is daarom belangrijk.

## Conclusie
Met deze applicatie kan ik tekst via de terminal versleutelen en ontsleutelen.

Door `cryptography` te gebruiken hoef ik geen eigen cryptografie te ontwikkelen.

AES-256-GCM zorgt voor versleuteling en controle op aanpassingen.

Het belangrijkste aandachtspunt blijft het veilig kiezen, bewaren en eventueel delen van het wachtwoord.

## Gebruikte bronnen
- [Cryptography - AESGCM](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM)
- [Cryptography - Scrypt](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#scrypt)
- [NIST - AES (FIPS 197)](https://csrc.nist.gov/pubs/fips/197/final)
- [NIST - GCM (SP 800-38D)](https://csrc.nist.gov/pubs/sp/800/38/d/final)
