App: https://ai-ticket-assistant-smdxsj9kscfkmsxcxddvwy.streamlit.app/

# AI-Powered Ticket Assistant & Dashboard

Egy modern, Python-alapú intelligens ügyfélszolgálati asszisztens és vezetői dashboard, amely nagy nyelvi modellt (LLM) használ a beérkező hibajegyek automatizált feldolgozására és vizualizációjára.

# Főbb Funkciók
- Automatizált Adatfeldolgozás:** Beérkező ügyfél-emailek tömeges beolvasása és kezelése `Pandas` segítségével.
- Strukturált AI Elemzés:** A `Google Gemini API` (gemini-3.8-flash) integrációjával a rendszer automatikusan kinyeri az alábbi adatokat szigorú JSON formátumban:
   - Kategorizálás (Szállítás, Technikai hiba, Előfizetés)
   - Hangulatelemzés (Nyugodt, Dühös, Kedves)
   - Sürgősségi szint (Igen / Nem)
   - Személyre szabott választervezet** (Hivatalos, udvarias válaszlevél generálása)
- Vezetői Dashboard: Interaktív, modern webes felület `Streamlit` használatával, valós idejű statisztikai grafikonokkal és görgethető adattáblázattal.
- Vállalati Szintű Hibatűrés: Beépített védelem az API rátalinitek (RateLimit 429) és szerveroldali túlterhelések ellen.
- Feature Toggle (Kapcsoló): Integrált szimulációs (Mock) üzemmód a költséghatékony és korlátlan helyi tesztelés érdekében.

# Alkalmazott Technológiák
- Nyelv:** Python 3.14+
- AI / LLM: Google Gen AI (Gemini 3.8 Flash model)
- Adatkezelés: Pandas, OpenPyXL (Excel integráció)
- Kezelőfelület: Streamlit Web Framework

# Helyi Futtatás
1. Telepítsd a szükséges csomagokat:
   ```bash
   pip install -r requirements.txt
   ```
2. Indítsd el a webes alkalmazást:
   ```bash
   streamlit run web_app.py
   ```

## 📊 Licensz
Ez a projekt oktatási és demonstrációs célból készült az önéletrajzom részét képező portfólióhoz.
