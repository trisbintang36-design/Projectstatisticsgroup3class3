import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, pearsonr, spearmanr
import matplotlib.pyplot as plt
import os

# --- THEME & STYLE ---
st.set_page_config(page_title="Aplikasi Analisis Data Survei", layout="wide")
st.markdown("""
<style>
/* Styles sama seperti sebelumnya, untuk kartu, label, profil, dsb */
.stCard { background-color: #223a5e; color: #FAFAFA; padding: 18px 24px; margin-bottom: 22px;
    border-radius: 16px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); border: 2.7px solid #f7c325;
    font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace;}
.stTitleMain { font-size: 2.4rem; font-family: 'Share Tech Mono','Consolas','Roboto Mono', monospace;
    color: #22d2e9; margin-bottom: 1.4rem;font-weight:800; letter-spacing: 1px; text-shadow: 1px 2px 0px #222,2px 4px 1.5px #fff000aa; }
.stSubHeader { font-size: 1.29rem; color: #f7c325; margin-top:1rem;
    font-family: 'Share Tech Mono','Consolas','Roboto Mono',monospace; font-weight:700;}
.stProfileName { font-weight:600; font-size:1.16rem; margin-bottom:6px; color:#22d2e9;
    font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;}
.stProfileRole { font-size:1.04rem; color:#FAFAFA; margin-bottom:3px;
    font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;}
.stOrigin { font-size:1.04rem; color:#f7c325; font-style:italic;
    font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;}
.stLabel { background-color: #1976d2; color: #FAFAFA; padding: 4px 12px; border-radius: 8px;
    font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;
    font-size: 0.95rem; display: inline-block; margin: 0 5px 8px 0; font-weight:700;}
.st-df { background-color: #122033; border-radius: 10px; padding: 10px; border:2px solid #f7c325;
    font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;}
hr {border-top:2.5px solid #f7c325; margin-bottom:16px;}
</style>
<link href='https://fonts.googleapis.com/css?family=Share+Tech+Mono' rel='stylesheet'>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(__file__)

# --- Bahasa & Sidebar ---
languages = ["Indonesia", "English", "日本語", "简体中文"]
language_flags = {"Indonesia": "🇮🇩","English": "🇬🇧","日本語": "🇯🇵","简体中文": "🇨🇳"}
selected_lang_label = st.sidebar.selectbox(
    "🌐 Pilih Bahasa / Choose Language / 言語選択 / 选择语言", 
    [f"{language_flags[lang]}  {lang}" for lang in languages])
lang = selected_lang_label.split(maxsplit=1)[-1]

sidebar_menu = {
    "Indonesia": ["Profil Pembuat", "Analisis Data", "Tentang Aplikasi"],
    "English": ["Author Profile", "Data Analysis", "About App"],
    "日本語": ["著者プロフィール", "データ分析", "アプリについて"],
    "简体中文": ["作者简介", "数据分析", "关于应用"],
}
menu_items = sidebar_menu.get(lang, sidebar_menu["Indonesia"])
menu = st.sidebar.radio("Menu", menu_items)

# --- Multilanguage dictionary (disederhanakan) ---
text = {
    "Indonesia": {
        "profile_title": "Profil Pembuat",
        "analysis_title": "Analisis Data",
        "about_title": "Tentang Aplikasi",
        "about_content": "Aplikasi ini dibuat menggunakan Streamlit untuk menganalisis data survei.",
        "upload_info": "Silakan upload file CSV atau Excel untuk memulai analisis.",
        "num_corr": "Variabel numerik: pilih metode korelasi",
        "cat_info": "Variabel kategorik: menggunakan Chi-Square",
        "mix_info": "Kombinasi variabel numerik dan kategorik belum didukung.",
    },
    "English": {
        "profile_title": "Author Profile",
        "analysis_title": "Data Analysis",
        "about_title": "About App",
        "about_content": "This app is built using Streamlit to analyze survey data.",
        "upload_info": "Please upload your CSV or Excel file to start analysis.",
        "num_corr": "Numeric variables: choose correlation method",
        "cat_info": "Categorical variables: using Chi-Square test",
        "mix_info": "Numeric + categorical combination not supported yet.",
    }
    # Bisa ditambahkan untuk jp & zh
}
tt = text.get(lang, text["Indonesia"])

# --- Profil Data ---
profile_data = [
    {"name": "Moh. Trisbintang A. Menu", "img_file": "tris.jpeg", "sid": "SID: 004202400102",
     "role": "⚙️ Distribusi: Survei & Streamlit", "origin": "Gorontalo"},
    {"name": "Dwi Anfia Putri Wulandari", "img_file": "fia.jpeg", "sid": "SID: 004202400034",
     "role": "🛠️ Analisis dasar & grafik", "origin": "Bogor"},
    {"name": "Gina Sonia", "img_file": "gina.jpeg", "sid": "SID: 004202400076",
     "role": "🔧 Fokus laporan & bantu olah data", "origin": "Cikampek"},
    {"name": "Ananda Fasya Wiratama Putri", "img_file": "fasya.jpeg", "sid": "SID: 004202400107",
     "role": "⚡ Analisis hubungan variabel & Streamlit", "origin": "Depok"}
]

# --- HALAMAN MENU ---
if menu == menu_items[0]:
    # Profil
    st.markdown(f"<div class='stTitleMain'>{tt['profile_title']}</div>", unsafe_allow_html=True)
    for prof in profile_data:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(os.path.join(BASE_DIR, prof["img_file"]), width=265)
        with cols[1]:
            st.markdown(f"<div class='stProfileName'>{prof['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stProfileRole'>{prof['role']}</div>", unsafe_allow_html=True)
            st.markdown(f"**{prof['sid']}**")
            st.markdown(f"<span class='stOrigin'>{prof['origin']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

elif menu == menu_items[1]:
    # Analisis Data
    st.markdown(f"<div class='stTitleMain'>{tt['analysis_title']}</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(tt["upload_info"], type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Preview Data")
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)

        # Pilih variabel
        colX1, colX2 = st.columns(2)
        with colX1:
            x1 = st.selectbox("Pilih Variabel 1", df.columns.tolist(), key="var1")
        with colX2:
            x2 = st.selectbox("Pilih Variabel 2", df.columns.tolist(), key="var2")

        tipe_x1 = "num" if pd.api.types.is_numeric_dtype(df[x1]) else "cat"
        tipe_x2 = "num" if pd.api.types.is_numeric_dtype(df[x2]) else "cat"

        st.markdown(f"<span class='stLabel'>{x1} → {tipe_x1}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='stLabel'>{x2} → {tipe_x2}</span>", unsafe_allow_html=True)

        # Analisis numerik
        if tipe_x1 == "num" and tipe_x2 == "num":
            st.info(tt["num_corr"])
            method_options = ["Pearson", "Spearman"]
            corr_method = st.selectbox("Pilih metode korelasi", method_options)

            mask = df[[x1, x2]].dropna()
            if len(mask) >= 2:
                coef, p = pearsonr(mask[x1], mask[x2]) if corr_method=="Pearson" else spearmanr(mask[x1], mask[x2])
                st.write(f"Koefisien: {coef:.4f} | P-value: {p:.4f}")
                st.success("Signifikan" if p<0.05 else "Tidak signifikan")
            else:
                st.warning("Data tidak cukup untuk menghitung korelasi.")

        # Analisis kategori
        elif tipe_x1 == "cat" and tipe_x2 == "cat":
            st.info(tt["cat_info"])
            cont_table = pd.crosstab(df[x1], df[x2])
            st.dataframe(cont_table)
            chi2, p, dof, _ = chi2_contingency(cont_table)
            st.write(f"Chi2 = {chi2:.4f}, P-value = {p:.4f}, df = {dof}")
            st.success("Signifikan" if p<0.05 else "Tidak signifikan")

        else:
            st.warning(tt["mix_info"])

elif menu == menu_items[2]:
    # Tentang Aplikasi
    st.markdown(f"<div class='stTitleMain'>{tt['about_title']}</div>", unsafe_allow_html=True)
    st.info(tt["about_content"])
