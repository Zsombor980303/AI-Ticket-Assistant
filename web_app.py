import streamlit as st
import pandas as pd
import os

# 1. Beállítjuk a weboldal címét és ikonját
st.set_page_config(page_title="AI Ticket Asszisztens", page_icon="🤖", layout="wide")

st.title("🤖 Intelligens Ügyfélszolgálati Asszisztens")
st.write("Ez az app automatikusan kategorizálja a beérkező hibajegyeket és hangulatelemzést végez.")

# 2. Megnézzük, létezik-e már az Excel fájlunk
excel_fajl = "elemzett_tickets.xlsx"

if os.path.exists(excel_fajl):
    # Beolvassuk az adatokat az Excelből
    df = pd.read_excel(excel_fajl)

    st.subheader("📊 Feldolgozott hibajegyek statisztikája")

    # Létrehozunk két oszlopot a weboldalon a grafikonoknak
    bal_oszlop, jobb_oszlop = st.columns(2)

    with bal_oszlop:
        st.write("**Levelek megoszlása kategóriák szerint:**")
        # A Streamlit beépített bar_chart parancsával egyetlen sorból rajzolunk grafikont!
        st.bar_chart(df['Kategória'].value_counts())

    with jobb_oszlop:
        st.write("**Ügyfelek hangulata:**")
        st.bar_chart(df['Hangulat'].value_counts())

    st.subheader("📋 Összesített adattáblázat")
    # Kirakjuk a teljes táblázatot egy interaktív, görgethető webes táblázatba
    st.dataframe(df)

    # Teszünk egy üres vonalat és egy gombot a táblázat alá
    st.write("---")
    st.subheader("🔄 Új elemzés indítása")

else:
    st.warning(
        f"⚠️ Nem találom a '{excel_fajl}' fájlt. Kérlek, először futtasd le a 'ticket_asszistens.py' fájlt a PyCharmban!")

if st.button("AI Elemzés Futtatása (Háttérmotor indítása)"):
    with st.spinner("Az AI éppen dolgozik a háttérben... Kérlek várj..."):
        # Importáljuk a tegnapi logikádat, és lefuttatjuk a teljes ticket_asszistens.py fájlt!
        import os

        os.system("python ticket_asszistens.py")

        # Miután lefutott, frissítjük a weboldalt, hogy az új adatok jelenjenek meg
        st.success("✅ Sikeres elemzés! Az adatok frissültek.")
        st.rerun()