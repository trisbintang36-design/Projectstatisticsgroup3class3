import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, pearsonr
import matplotlib.pyplot as plt
import os

# ===== CONFIG STREAMLIT =====
st.set_page_config(page_title="Aplikasi Analisis Data Survei", layout="wide")

# ===== PILIH TEMA =====
theme = st.sidebar.selectbox("Pilih Tema / Choose Theme", ["Gelap 🌑", "Terang ☀️"])

if theme == "Gelap 🌑":
    bg_color = "#223a5e"
    card_color = "#122033"
    text_color = "#22d2e9"
    border_color = "#f7c325"
else:
    bg_color = "#ffffff"
    card_color = "#f0f0f0"
    text_color = "#223a5e"
    border_color = "#1976d2"

# ===== STYLING =====
st.markdown(f"""
<style>
.stCard {{
    background-color: {card_color};
    color: {text_color};
    padding: 18px 24px;
    margin-bottom: 22px;
    border-radius: 16px;
    border: 2px solid {border_color};
    font-family: 'Share Tech Mono', monospace;
}}
.stTitleMain {{
    font-size: 2.4rem;
    font-weight: 800;
    color: {text_color};
    margin-bottom: 1.4rem;
    letter-spacing: 1px;
}}
.stSubHeader {{
    font-size: 1.29rem;
    color: {border_color};
    margin-top: 1rem;
    font-weight: 700;
}}
.stProfileName {{
    font-weight: 600;
    font-size: 1.16rem;
    color: {text_color};
}}
.stProfileRole {{
    font-size: 1.04rem;
}}
.stOrigin {{
    font-size: 1.04rem;
    color: {border_color};
    font-style: italic;
}}
.stLabel {{
    background-color: {border_color};
    color: {bg_color};
    padding: 4px 12px;
    border-radius: 8px;
    font-weight: 700;
    display: inline-block;
    margin: 0 5px 8px 0;
}}
.st-df {{
    background-color: {card_color};
    border-radius: 10px;
    padding: 10px;
    border:2px solid {border_color};
    font-family:'Share Tech Mono', monospace;
}}
hr {{
    border-top:2.5px solid {border_color};
    margin-bottom:16px;
}}
</style>
<link href='https://fonts.googleapis.com/css?family=Share+Tech+Mono' rel='stylesheet'>
""", unsafe_allow_html=True)

# ===== PILIH BAHASA =====
languages = ["Indonesia", "English"]
language_flags = {"Indonesia": "🇮🇩", "English": "🇬🇧"}
languages_w_flag = [f"{language_flags[lang]} {lang}" for lang in languages]
selected_lang_label = st.sidebar.selectbox("🌐 Pilih Bahasa / Choose Language", languages_w_flag)
lang = selected_lang_label.split(maxsplit=1)[-1]

# ===== MENU =====
sidebar_menu = {
    "Indonesia": ["Profil Pembuat", "Analisis Data", "Tentang Aplikasi"],
    "English": ["Author Profile", "Data Analysis", "About App"]
}
menu_items = sidebar_menu.get(lang, sidebar_menu["Indonesia"])
menu = st.sidebar.radio("Menu", menu_items)
# ===== DATA PROFIL =====
profile_data = [
    {
        "name": {"Indonesia": "Moh. Trisbintang A. Menu", "English": "Moh. Trisbintang A. Menu"},
        "img_file": "tris.jpeg",
        "sid": {"Indonesia": "SID: 004202400102", "English": "SID: 004202400102"},
        "role": {"Indonesia": "⚙️ Distribusi: Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
                 "English": "⚙️ Role: Survey, data cleaning, Streamlit dashboard (menu & navigation)"},
        "origin": {"Indonesia": "Asal daerah: Gorontalo", "English": "Origin: Gorontalo"}
    },
    {
        "name": {"Indonesia": "Dwi Anfia Putri Wulandari", "English": "Dwi Anfia Putri Wulandari"},
        "img_file": "fia.jpeg",
        "sid": {"Indonesia": "SID: 004202400034", "English": "SID: 004202400034"},
        "role": {"Indonesia": "🛠️ Distribusi: Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
                 "English": "🛠️ Role: Basic analysis (histogram, boxplot), Python chart coding, Streamlit graphics"},
        "origin": {"Indonesia": "Asal daerah: Bogor", "English": "Origin: Bogor"}
    },
    {
        "name": {"Indonesia": "Gina Sonia", "English": "Gina Sonia"},
        "img_file": "gina.jpeg",
        "sid": {"Indonesia": "SID: 004202400076", "English": "SID: 004202400076"},
        "role": {"Indonesia": "🔧 Distribusi: Fokus laporan & bantu olah data",
                 "English": "🔧 Role: Focused on report & assist data processing"},
        "origin": {"Indonesia": "Asal daerah: Cikampek", "English": "Origin: Cikampek"}
    },
    {
        "name": {"Indonesia": "Ananda Fasya Wiratama Putri", "English": "Ananda Fasya Wiratama Putri"},
        "img_file": "fasya.jpeg",
        "sid": {"Indonesia": "SID: 004202400107", "English": "SID: 004202400107"},
        "role": {"Indonesia": "⚡ Distribusi: Analisis hubungan variabel, pengaruh medsos ke mental, Streamlit bagian analisis",
                 "English": "⚡ Role: Variable relationship analysis, social media effect on mental, Streamlit analysis"},
        "origin": {"Indonesia": "Asal daerah: Depok", "English": "Origin: Depok"}
    }
]

# ===== PROFIL PEMBUAT =====
if menu == menu_items[0]:
    st.markdown(f"<div class='stTitleMain'>{'Profil Pembuat' if lang=='Indonesia' else 'Author Profile'}</div>", unsafe_allow_html=True)

    BASE_DIR = os.path.dirname(__file__)
    
    for prof in profile_data:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            img_path = os.path.join(BASE_DIR, prof["img_file"])
            if os.path.exists(img_path):
                st.image(img_path, width=260)
            else:
                st.warning(f"Gambar tidak ditemukan: {img_path}")
        with cols[1]:
            st.markdown(f"<div class='stProfileName'>{prof['name'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stProfileRole'>{prof['role'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"**{prof['sid'][lang]}**")
            st.markdown(f"<div class='stOrigin'>{prof['origin'][lang]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
# ===== ANALISIS DATA =====
elif menu == menu_items[1]:
    st.markdown(f"<div class='stTitleMain'>{'Analisis Data' if lang=='Indonesia' else 'Data Analysis'}</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader('Upload file Excel data survei' if lang=='Indonesia' else 'Upload survey Excel file', type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # --- Preview Data ---
        st.subheader('Preview Data' if lang=='Indonesia' else 'Data Preview')
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Distribusi Data (Deskriptif) ---
        st.markdown(f"<div class='stSubHeader'>{'Distribusi Data' if lang=='Indonesia' else 'Data Distribution'}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        selected_desc_cols = st.multiselect(
            'Pilih variabel numerik untuk analisis deskriptif (histogram & boxplot)' if lang=='Indonesia' else 'Select numeric variables for descriptive analysis (histogram & boxplot)',
            numeric_cols
        )

        if selected_desc_cols:
            desc = df[selected_desc_cols].describe().T
            desc["skew"] = df[selected_desc_cols].skew()
            desc["kurtosis"] = df[selected_desc_cols].kurtosis()
            st.dataframe(desc)

            for col in selected_desc_cols:
                # Histogram
                st.markdown(f"<span class='stLabel'>{'Histogram' if lang=='Indonesia' else 'Histogram'}: {col}</span>", unsafe_allow_html=True)
                fig1, ax1 = plt.subplots(figsize=(7, 3))
                ax1.hist(df[col].dropna(), bins=20, color="#1976d2", alpha=0.85)
                ax1.set_facecolor("#223a5e")  # Dark theme background
                ax1.set_title(f"{'Histogram' if lang=='Indonesia' else 'Histogram'}: {col}", fontsize=12)
                st.pyplot(fig1)

                # Boxplot
                st.markdown(f"<span class='stLabel'>{'Boxplot' if lang=='Indonesia' else 'Boxplot'}: {col}</span>", unsafe_allow_html=True)
                fig2, ax2 = plt.subplots(figsize=(7, 3))
                ax2.boxplot(df[col].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='#f7c325', color='#1976d2'))
                ax2.set_facecolor("#223a5e")
                ax2.set_title(f"{'Boxplot' if lang=='Indonesia' else 'Boxplot'}: {col}", fontsize=12)
                st.pyplot(fig2)
        else:
            st.info('Silakan pilih variabel numerik' if lang=='Indonesia' else 'Please select numeric variables')
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Analisis Hubungan Variabel ---
        st.markdown(f"<div class='stSubHeader'>{'Analisis Hubungan Variabel' if lang=='Indonesia' else 'Variable Relationship Analysis'}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            x1 = st.selectbox('Pilih Variabel 1' if lang=='Indonesia' else 'Select Variable 1', df.columns.tolist())
        with colB:
            x2 = st.selectbox('Pilih Variabel 2' if lang=='Indonesia' else 'Select Variable 2', df.columns.tolist(), index=1 if len(df.columns) > 1 else 0)

        # DETEKSI TIPE
        tipe_x1 = 'Numerik' if np.issubdtype(df[x1].dropna().dtype, np.number) else 'Kategori'
        tipe_x2 = 'Numerik' if np.issubdtype(df[x2].dropna().dtype, np.number) else 'Kategori'

        st.markdown(f"<span class='stLabel'>{x1}: {tipe_x1}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='stLabel'>{x2}: {tipe_x2}</span>", unsafe_allow_html=True)

        # ----- Kategori vs Kategori (Chi-square) -----
        if tipe_x1 == 'Kategori' and tipe_x2 == 'Kategori':
            st.info('Variabel kategorik → menggunakan Chi-Square' if lang=='Indonesia' else 'Categorical variables → Chi-Square test')
            cont_table = pd.crosstab(df[x1], df[x2])
            st.subheader('Tabel Kontingensi' if lang=='Indonesia' else 'Contingency Table')
            st.markdown("<div class='st-df'>", unsafe_allow_html=True)
            st.dataframe(cont_table)
            st.markdown("</div>", unsafe_allow_html=True)

            chi2_val, p_val, dof, expected = chi2_contingency(cont_table)
            st.write(f"Chi2 = {chi2_val:.4f}")
            st.write(f"P-value = {p_val:.4f}")
            st.write(f"Degrees of freedom = {dof}")
            st.markdown('Kesimpulan:' if lang=='Indonesia' else 'Conclusion:')
            if p_val < 0.05:
                st.success('Terdapat hubungan signifikan antara variabel (p < 0.05)' if lang=='Indonesia' else 'There is a significant relationship (p < 0.05)')
            else:
                st.warning('Tidak terdapat hubungan signifikan antara variabel (p >= 0.05)' if lang=='Indonesia' else 'No significant relationship found (p >= 0.05)')

        # ----- Numerik vs Numerik (Pearson) -----
        elif tipe_x1 == 'Numerik' and tipe_x2 == 'Numerik':
            st.info('Variabel numerik → korelasi Pearson' if lang=='Indonesia' else 'Numeric variables → Pearson correlation')
            coef, p_val = pearsonr(df[x1].dropna(), df[x2].dropna())
            st.subheader('Korelasi Pearson' if lang=='Indonesia' else 'Pearson Correlation')
            st.markdown("<div class='st-df'>", unsafe_allow_html=True)
            st.write(f"Koefisien = {coef:.4f}" if lang=='Indonesia' else f"Coefficient = {coef:.4f}")
            st.write(f"P-value = {p_val:.4f}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('Kesimpulan:' if lang=='Indonesia' else 'Conclusion:')
            if p_val < 0.05:
                st.success('Terdapat hubungan signifikan (p < 0.05)' if lang=='Indonesia' else 'Significant correlation (p < 0.05)')
            else:
                st.warning('Tidak terdapat hubungan signifikan (p >= 0.05)' if lang=='Indonesia' else 'No significant correlation (p >= 0.05)')

        # ----- Kombinasi tidak didukung -----
        else:
            st.warning('Kombinasi belum didukung untuk analisis otomatis.' if lang=='Indonesia' else 'Mixed variable types are not supported for automatic analysis.')

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info('Silakan upload file Excel data survei.' if lang=='Indonesia' else 'Please upload a survey Excel file.')
# ===== TENTANG / ABOUT =====
elif menu == menu_items[2]:
    st.markdown(f"<div class='stTitleMain'>{'Tentang Aplikasi' if lang=='Indonesia' else 'About App'}</div>", unsafe_allow_html=True)

    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown(
        'Aplikasi ini dibuat untuk menganalisis data survei, menampilkan visualisasi, dan membantu dalam laporan data secara interaktif.'
        if lang == 'Indonesia'
        else 'This application is designed to analyze survey data, display visualizations, and assist in interactive reporting.'
    )

    st.markdown('---')

    st.markdown(f"<div class='stSubHeader'>{'Profil Tim' if lang=='Indonesia' else 'Team Profile'}</div>", unsafe_allow_html=True)

    cols = st.columns(4)
    for idx, member in enumerate(profile_data):
        with cols[idx % 4]:
            st.image(member["img_file"], width=100)
            st.markdown(f"**{member['name'][lang]}**")
            st.markdown(member["sid"][lang])
            st.markdown(member["role"][lang])
            st.markdown(member["origin"][lang])

    st.markdown("</div>", unsafe_allow_html=True)
