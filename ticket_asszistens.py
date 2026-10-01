import json
import pandas as pd
from google import genai
from google.genai import types
import random

AI_KAPCSOLÓ = False;

# AI Kliens indítása - Ide kell a lementett api kulcsom, ezt itt nem adom meg
client = genai.Client(api_key="EZ_EGY_KAMU_KULCS_A_GITHUB_MIATT_12345")

print("--- Intelligens Ügyfélszolgálati Asszisztens indítása ---")

# Teszt adatok betöltése
teszt_adatok = {
    'ugyfel_neve': ['Kovács Péter', 'Szabó Anna', 'Kiss Béla'],
    'email_szoveg': [
        "Jó napot! Érdeklődni szeretnék, hogy a megrendelt cipőm mikor érkezik meg? A rendelésszámom: 44512.",
        "Már megint nem működik a belépés a weboldalra! Egyszerűen felháborító, hogy fizetek a szolgáltatásért, és nem tudom használni! Azonnal javítsák meg!",
        "Tisztelt Cég! Szeretném lemondani az előfizetésemet, mert sajnos költözés miatt a jövőben nem lesz rá szükségem. Köszönöm az eddigi segítséget."
    ]
}
df = pd.DataFrame(teszt_adatok)

# --- Kamu adatok a teszteléshez ---
def kamu_gemini_hivashoz(ugyfel_neve):
    rnd = random.randint(0, 2)

    if rnd == 0:
        return """{
          "kategoria": "Technikai hiba",
          "hangulat": "Dühös",
          "surgos": "Igen",
          "valasz_tervezet": "Tisztelt Ügyfelünk! Sajnálattal halljuk a hibát, a technikai csapatunk azonnal kivizsgálja a belépési problémát."
        }"""
    elif rnd == 1:
        return """{
          "kategoria": "Szállítás",
          "hangulat": "Nyugodt",
          "surgos": "Nem",
          "valasz_tervezet": "Tisztelt Ügyfelünk! Köszönjük a megkeresést, a csomagja úton van, várhatóan 2 napon belül megérkezik."
        }"""
    else:
        return """{
          "kategoria": "Előfizetés",
          "hangulat": "Kedves",
          "surgos": "Nem",
          "valasz_tervezet": "Kedves Ügyfelünk! Örömmel segítünk az előfizetése megújításában, küldjük a részleteket."
        }"""

# Létrehozunk üres listákat, ahova az AI által generált eredményeket fogjuk gyűjteni
kategoriak = []
hangulatok = []
surgossegek = []
valaszok = []

print("\nAI elemzés indítása a táblázaton...")

# Soronként feldolgozzuk az emaileket
for _, sor in df.iterrows():
    print(f"-> {sor['ugyfel_neve']} levelének elemzése... ", end="", flush=True)

    try:
        if(AI_KAPCSOLÓ == False ):
            # Az éles Google hívás helyett a fenti kamu funkciót indítjuk el
            kamu_szoveg = kamu_gemini_hivashoz(sor['ugyfel_neve'])
            # --- [DEBUG] KIÍRATJUK A SZIMULÁLT VÁLASZT ---
            print(f"\n[DEBUG] {sor['ugyfel_neve']} szimulált AI válasza:")
            print(kamu_szoveg)
            print("---------------")

            # A kamu szöveget alakítjuk át valódi Python szótárrá
            adat = json.loads(kamu_szoveg)
        else:
            # Megkérjük a Geminit, hogy elemezzen, és szigorúan tiszta JSON formátumban válaszoljon
            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=f"""
            Te egy ügyfélszolgálati AI vagy. A feladatod az emailek elemzése.
            KÖTELEZŐEN egyetlen JSON objektumot kell visszaadnod a következő kulcsokkal, felesleges duma nélkül:
            - kategoria (lehetséges értékek: Szállítás, Technikai hiba, Előfizetés)
            - hangulat (lehetséges értékek: Nyugodt, Dühös, Kedves)
            - surgos (lehetséges értékek: Igen, Nem)
            - valasz_tervezet (egy udvarias, hivatalos válaszlevél magyarul)
    
            Elemezd ezt az ügyfélszolgálati levelet: '{sor['email_szoveg']}'
            """,
                response_format={"type": "text", "mime_type": "application/json"}
            )
            print(f"\n[DEBUG] {sor['ugyfel_neve']} nyers AI válasza:")
            print(interaction.output_text)
            print("---------------")

            # A Gemini szöveges JSON válaszát átalakítjuk valódi Python szótárrá (dictionary)
            adat = json.loads(interaction.output_text)

        # Elmentjük az adatokat a listáinkba. Az első paraméterrel (pl kategoria, hangulat) megmondjuk hogy azt keresse meg a program, a második pedig fallback érték, ha valamiért nem találna semmit
        kategoriak.append(adat.get('kategoria', 'Általános'))
        hangulatok.append(adat.get('hangulat', 'Nyugodt'))
        surgossegek.append(adat.get('surgos', 'Nem'))
        valaszok.append(adat.get('valasz_tervezet', ''))
        print("Kész!")
    except Exception as e:
        print(f"Hiba a feldolgozás során: {e}")
        kategoriak.append('Hiba')
        hangulatok.append('Hiba')
        surgossegek.append('Hiba')
        valaszok.append('')

# Feldolgozzuk az eredményeket
df['Kategória'] = kategoriak
df['Hangulat'] = hangulatok
df['Sürgős?'] = surgossegek
df['Választervezet'] = valaszok

print("\n=== AI FELDOLGOZÁS VÉGEREDMÉNYE ===")
print(df[['ugyfel_neve', 'Kategória', 'Hangulat', 'Sürgős?']])
print("===================================\n")

# Excel file-ba mentés
df.to_excel("elemzett_tickets.xlsx", index=False)
print("💾 Szuper! Az eredményeket elmentettem az 'elemzett_tickets.xlsx' fájlba.")