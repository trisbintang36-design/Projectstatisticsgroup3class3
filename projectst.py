import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, pearsonr
import matplotlib.pyplot as plt
import os

# --- THEME: Teknik/Engineering Blue/Yellow, Card tebal, font digital ---
st.set_page_config(page_title="Aplikasi Analisis Data Survei", layout="wide")
st.markdown("""
    <style>
    .stCard { 
        background-color: #223a5e; 
        color: inherit; /* ← otomatis mengikuti tema laptop */
        padding: 18px 24px; 
        margin-bottom: 22px;
        border-radius: 16px; 
        box-shadow: 0 4px 18px rgba(0,0,0,0.15); 
        border: 2.7px solid #f7c325;
        font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace;
    }
    .stTitleMain { font-size: 2.4rem; font-family: 'Share Tech Mono','Consolas','Roboto Mono', monospace;
        color: #22d2e9; margin-bottom: 1.4rem;font-weight:800; letter-spacing: 1px; text-shadow: 1px 2px 0px #222,2px 4px 1.5px #fff000aa; }
    .stSubHeader { font-size: 1.29rem; color: #f7c325; margin-top:1rem;
        font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace; font-weight:700;}
    .stProfileName { font-weight:600; font-size:1.16rem; margin-bottom:6px; color:#22d2e9;
        font-family:'Share Tech Mono','Consolas','Roboto Mono',monospace;}
    .stProfileRole { font-size:1.04rem; margin-bottom:3px;
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

# --- Bahasa & bendera (sidebar) ---
languages = ["Indonesia", "English", "日本語", "简体中文"]
language_flags = {
    "Indonesia": "🇮🇩",
    "English": "🇬🇧",
    "日本語": "🇯🇵",
    "简体中文": "🇨🇳"
}
languages_w_flag = [f"{language_flags[lang]}  {lang}" for lang in languages]
selected_lang_label = st.sidebar.selectbox(
    "🌐 Pilih Bahasa / Choose Language / 言語選択 / 选择语言", languages_w_flag)
lang = selected_lang_label.split(maxsplit=1)[-1]

sidebar_menu = {
    "Indonesia": ["Profil Pembuat", "Analisis Data", "Tentang Aplikasi"],
    "English": ["Author Profile", "Data Analysis", "About App"],
    "日本語": ["著者プロフィール", "データ分析", "アプリについて"],
    "简体中文": ["作者简介", "数据分析", "关于应用"],
}
menu_items = sidebar_menu.get(lang, sidebar_menu["Indonesia"])
menu = st.sidebar.radio("Menu", menu_items)

# --- Multilanguage dictionary untuk semua label ---
text = { ... (SEMUA DICTIONARY ANDA TETAP SAMA, TIDAK DIUBAH) ... }

tt = text.get(lang, text["Indonesia"])

profile_data = [ ... (DATA PROFIL TETAP SAMA, TIDAK DIUBAH) ... ]

# --- MAIN CONTENT ---
if menu == menu_items[0]:
    st.markdown(f"<div class='stTitleMain'>{tt['profile_title']}</div>", unsafe_allow_html=True)
    for prof in profile_data:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        cols = st.columns([1,3])
        with cols[0]:
            img_path = os.path.join(BASE_DIR, prof["img_file"])
            st.image(img_path, width=265)
        with cols[1]:
            st.markdown(f"<div class='stProfileName'>{prof['name'][lang]} ⚙️</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stProfileRole'>{prof['role'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"**{prof['sid'][lang]}**")
            st.markdown(f"<span class='stOrigin'>{prof['origin'][lang]}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

elif menu == menu_items[1]:
    st.markdown(f"<div class='stTitleMain'>{tt['analysis_title']}</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(tt["file"], type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.subheader(tt["preview"])
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Distribusi Data ---
        st.markdown(f"<div class='stSubHeader'>{tt['desc_title']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        selected_desc_cols = st.multiselect(tt["desc_cols"], numeric_cols)

        if selected_desc_cols:
            desc = df[selected_desc_cols].describe().T
            desc["skew"] = df[selected_desc_cols].skew()
            desc["kurtosis"] = df[selected_desc_cols].kurtosis()
            st.dataframe(desc)

            for col in selected_desc_cols:
                st.markdown(f"<span class='stLabel'>{tt['hist']}: {col}</span>", unsafe_allow_html=True)
                fig1, ax1 = plt.subplots(figsize=(7,3))
                ax1.hist(df[col].dropna(), bins=20, color="#1976d2", alpha=0.86)
                ax1.set_facecolor("#223a5e")
                ax1.set_title(f"{tt['hist']}: {col}", fontsize=13, fontweight="bold")
                st.pyplot(fig1)

                st.markdown(f"<span class='stLabel'>{tt['box']}: {col}</span>", unsafe_allow_html=True)
                fig2, ax2 = plt.subplots(figsize=(7,3))
                ax2.boxplot(df[col].dropna(), vert=False, patch_artist=True,
                            boxprops=dict(facecolor='#f7c325', color='#1976d2'))
                ax2.set_facecolor("#223a5e")
                ax2.set_title(f"{tt['box']}: {col}", fontsize=13, fontweight="bold")
                st.pyplot(fig2)
        else:
            st.info(tt["desc_cols"])
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Analisis Hubungan Variabel ---
        st.markdown(f"<div class='stSubHeader'>{tt['vra_title']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        colX1, colX2 = st.columns(2)
        with colX1:
            x1 = st.selectbox(tt["vra_var1"], df.columns.tolist())
        with colX2:
            x2 = st.selectbox(tt["vra_var2"], df.columns.tolist(), index=1 if len(df.columns)>1 else 0)

        tipe_x1 = tt["type_num"] if np.issubdtype(df[x1].dropna().dtype, np.number) else tt["type_cat"]
        tipe_x2 = tt["type_num"] if np.issubdtype(df[x2].dropna().dtype, np.number) else tt["type_cat"]

        st.markdown(f"<span class='stLabel'>{x1} → {tipe_x1}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='stLabel'>{x2} → {tipe_x2}</span>", unsafe_allow_html=True)

        if tipe_x1 == tt["type_cat"] and tipe_x2 == tt["type_cat"]:
            st.info(tt["cat_info"])
            cont_table = pd.crosstab(df[x1], df[x2])
            st.subheader(tt["result_cat_cat"])
            st.markdown("<div class='st-df'>", unsafe_allow_html=True)
            st.dataframe(cont_table)
            st.markdown("</div>", unsafe_allow_html=True)

            chi2, p, dof, expected = chi2_contingency(cont_table)
            st.write(tt["chi2"].format(chi2))
            st.write(tt["pval"].format(p))
            st.write(tt["dof"].format(dof))

            st.markdown(tt["conclusion"])
            if p < 0.05:
                st.success(tt["conclude_sig"])
            else:
                st.warning(tt["conclude_nosig"])

        elif tipe_x1 == tt["type_num"] and tipe_x2 == tt["type_num"]:
            st.info(tt["num_info"])
            coef, p = pearsonr(df[x1].dropna(), df[x2].dropna())
            st.subheader(tt["result_num_num"])
            st.markdown("<div class='st-df'>", unsafe_allow_html=True)
            st.write(tt["corr_coef"].format(coef))
            st.write(tt["corr_pval"].format(p))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(tt["conclusion"])
            if p < 0.05:
                st.success(tt["corr_conclude_sig"])
            else:
                st.warning(tt["corr_conclude_nosig"])
        else:
            st.warning(tt["mix_info"])

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(tt["wait_file"])

elif menu == menu_items[2]:
    st.markdown(f"<div class='stTitleMain'>{tt['about_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stCard'>{tt['about_content']}</div>", unsafe_allow_html=True)
