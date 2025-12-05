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
        color: inherit; /* mengikuti tema laptop */
        padding: 18px 24px; 
        margin-bottom: 22px;
        border-radius: 16px; 
        box-shadow: 0 4px 18px rgba(0,0,0,0.15); 
        border: 2.7px solid #f7c325;
        font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace;
    }
    .stTitleMain { font-size: 2.4rem; font-family: 'Share Tech Mono','Consolas','Roboto Mono', monospace;
        color: #22d2e9; margin-bottom: 1.4rem;font-weight:800; letter-spacing: 1px; 
        text-shadow: 1px 2px 0px #222,2px 4px 1.5px #fff000aa; }
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

# --- Multilanguage dictionary ---
text = {
    "Indonesia": {
        "title": "Aplikasi Analisis Data Survei",
        "file": "Upload file Excel data survei",
        "analysis_title": "Analisis Data",
        "desc_title": "Distribusi Data",
        "desc_cols": "Pilih variabel numerik untuk analisis deskriptif (histogram & boxplot)",
        "hist": "Histogram",
        "box": "Boxplot",
        "preview": "Preview Data",
        "vra_title": "Analisis Hubungan Variabel",
        "vra_var1": "Pilih Variabel 1",
        "vra_var2": "Pilih Variabel 2",
        "type_num": "Numerik",
        "type_cat": "Kategori",
        "cat_info": "Variabel kategorik → menggunakan Chi-Square",
        "num_info": "Variabel numerik → korelasi Pearson",
        "result_cat_cat": "Tabel Kontingensi",
        "result_num_num": "Korelasi Pearson",
        "chi2": "Chi2 = {:.4f}",
        "pval": "P-value = {:.4f}",
        "dof": "Degrees of freedom = {}",
        "conclusion": "Kesimpulan:",
        "conclude_sig": "Terdapat hubungan signifikan antara variabel (p < 0.05)",
        "conclude_nosig": "Tidak terdapat hubungan signifikan antara variabel (p >= 0.05)",
        "corr_coef": "Koefisien = {:.4f}",
        "corr_pval": "P-value = {:.4f}",
        "corr_conclude_sig": "Terdapat hubungan signifikan (p < 0.05)",
        "corr_conclude_nosig": "Tidak terdapat hubungan signifikan (p >= 0.05)",
        "mix_info": "Kombinasi belum didukung untuk analisis otomatis.",
        "wait_file": "Silakan upload file Excel data survei.",
        "profile_title": "Profil Pembuat",
        "about_title": "Tentang Aplikasi",
        "about_content": "Aplikasi ini dibuat menggunakan Streamlit untuk menganalisis data survei (Excel), analisis deskriptif, dan analisis hubungan variabel otomatis."
    },
    "English": {
        "title": "Survey Data Analysis App",
        "file": "Upload survey Excel file",
        "analysis_title": "Data Analysis",
        "desc_title": "Data Distribution",
        "desc_cols": "Select numeric variables for descriptive analysis (histogram & boxplot)",
        "hist": "Histogram",
        "box": "Boxplot",
        "preview": "Data Preview",
        "vra_title": "Variable Relationship Analysis",
        "vra_var1": "Select Variable 1",
        "vra_var2": "Select Variable 2",
        "type_num": "Numeric",
        "type_cat": "Categorical",
        "cat_info": "Categorical variables → Chi-Square test",
        "num_info": "Numeric variables → Pearson correlation",
        "result_cat_cat": "Contingency Table",
        "result_num_num": "Pearson Correlation",
        "chi2": "Chi2 = {:.4f}",
        "pval": "P-value = {:.4f}",
        "dof": "Degrees of freedom = {}",
        "conclusion": "Conclusion:",
        "conclude_sig": "There is a significant relationship (p < 0.05)",
        "conclude_nosig": "No significant relationship found (p >= 0.05)",
        "corr_coef": "Coefficient = {:.4f}",
        "corr_pval": "P-value = {:.4f}",
        "corr_conclude_sig": "Significant correlation (p < 0.05)",
        "corr_conclude_nosig": "No significant correlation (p >= 0.05)",
        "mix_info": "Mixed variable types are not supported for automatic analysis.",
        "wait_file": "Please upload a survey Excel file.",
        "profile_title": "Author Profile",
        "about_title": "About This App",
        "about_content": "This app is built with Streamlit for survey data (Excel) analysis, descriptive analysis, and automatic relationship testing."
    },

    "日本語": {
        "title": "アンケートデータ分析アプリ",
        "file": "アンケート Excel ファイルをアップロード",
        "analysis_title": "データ分析",
        "desc_title": "データ分布",
        "desc_cols": "数値変数を選択（ヒストグラムと箱ひげ図）",
        "hist": "ヒストグラム",
        "box": "箱ひげ図",
        "preview": "データプレビュー",
        "vra_title": "変数関係分析",
        "vra_var1": "変数 1 を選択",
        "vra_var2": "変数 2 を選択",
        "type_num": "数値",
        "type_cat": "カテゴリ",
        "cat_info": "カテゴリ変数 → カイ二乗検定",
        "num_info": "数値変数 → ピアソン相関",
        "result_cat_cat": "クロス集計表",
        "result_num_num": "ピアソン相関",
        "chi2": "カイ二乗値 = {:.4f}",
        "pval": "P値 = {:.4f}",
        "dof": "自由度 = {}",
        "conclusion": "結論：",
        "conclude_sig": "有意な関係があります (p < 0.05)",
        "conclude_nosig": "有意な関係はありません (p >= 0.05)",
        "corr_coef": "相関係数 = {:.4f}",
        "corr_pval": "P値 = {:.4f}",
        "corr_conclude_sig": "有意な相関があります (p < 0.05)",
        "corr_conclude_nosig": "有意な相関はありません (p >= 0.05)",
        "mix_info": "この組み合わせの自動分析はサポートされていません。",
        "wait_file": "アンケート Excel ファイルをアップロードしてください。",
        "profile_title": "著者プロフィール",
        "about_title": "アプリについて",
        "about_content": "このアプリは Streamlit を使用して、アンケートデータの分布分析および変数関係分析を自動で行います。"
    },

    "简体中文": {
        "title": "调查数据分析应用",
        "file": "上传调查 Excel 文件",
        "analysis_title": "数据分析",
        "desc_title": "数据分布",
        "desc_cols": "选择数值变量进行描述分析（直方图 & 箱线图）",
        "hist": "直方图",
        "box": "箱线图",
        "preview": "数据预览",
        "vra_title": "变量关系分析",
        "vra_var1": "选择变量 1",
        "vra_var2": "选择变量 2",
        "type_num": "数值",
        "type_cat": "类别",
        "cat_info": "类别变量 → 卡方检验",
        "num_info": "数值变量 → 皮尔逊相关",
        "result_cat_cat": "列联表",
        "result_num_num": "皮尔逊相关",
        "chi2": "卡方值 = {:.4f}",
        "pval": "P值 = {:.4f}",
        "dof": "自由度 = {}",
        "conclusion": "结论：",
        "conclude_sig": "变量之间存在显著关系 (p < 0.05)",
        "conclude_nosig": "变量之间不存在显著关系 (p >= 0.05)",
        "corr_coef": "相关系数 = {:.4f}",
        "corr_pval": "P值 = {:.4f}",
        "corr_conclude_sig": "存在显著相关性 (p < 0.05)",
        "corr_conclude_nosig": "不存在显著相关性 (p >= 0.05)",
        "mix_info": "此组合暂不支持自动分析。",
        "wait_file": "请上传调查 Excel 文件。",
        "profile_title": "作者简介",
        "about_title": "关于此应用",
        "about_content": "此应用基于 Streamlit，可用于调查数据的分布分析及变量关系分析。"
    }
}

# Ambil teks sesuai bahasa
tt = text.get(lang, text["Indonesia"])

# ----------------- PROFILE DATA -----------------
profile_data = [
    {
        "name": {
            "Indonesia": "Moh. Trisbintang A. Menu",
            "English": "Moh. Trisbintang A. Menu",
            "日本語": "Moh. Trisbintang A. Menu",
            "简体中文": "Moh. Trisbintang A. Menu",
        },
        "img_file": "tris.jpeg",
        "sid": {
            "Indonesia": "SID: 004202400102",
            "English": "SID: 004202400102",
            "日本語": "SID: 004202400102",
            "简体中文": "SID：004202400102",
        },
        "role": {
            "Indonesia": "⚙️ Distribusi: Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
            "English": "⚙️ Role: Survey, data cleaning, Streamlit dashboard (menu & navigation)",
            "日本語": "⚙️ 役割：調査、データクリーニング、Streamlitダッシュボード",
            "简体中文": "⚙️ 职责：调查、数据清洗、Streamlit仪表板",
        },
        "origin": {
            "Indonesia": "Asal daerah: Gorontalo",
            "English": "Origin: Gorontalo",
            "日本語": "出身地：ゴロンタロ",
            "简体中文": "来自：Gorontalo",
        }
    },
    {
        "name": {
            "Indonesia": "Dwi Anfia Putri Wulandari",
            "English": "Dwi Anfia Putri Wulandari",
            "日本語": "Dwi Anfia Putri Wulandari",
            "简体中文": "Dwi Anfia Putri Wulandari",
        },
        "img_file": "fia.jpeg",
        "sid": {
            "Indonesia": "SID: 004202400034",
            "English": "SID: 004202400034",
            "日本語": "SID: 004202400034",
            "简体中文": "SID：004202400034",
        },
        "role": {
            "Indonesia": "🛠️ Distribusi: Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
            "English": "🛠️ Role: Basic analysis (histogram, boxplot), Python chart coding, Streamlit graphics",
            "日本語": "🛠️ 役割：基本分析、Pythonグラフ作成、Streamlitグラフィック",
            "简体中文": "🛠️ 职责：基础分析、Python绘图、Streamlit图形部分",
        },
        "origin": {
            "Indonesia": "Asal daerah: Bogor",
            "English": "Origin: Bogor",
            "日本語": "出身地：ボゴール",
            "简体中文": "来自：Bogor",
        }
    },
    {
        "name": {
            "Indonesia": "Gina Sonia",
            "English": "Gina Sonia",
            "日本語": "Gina Sonia",
            "简体中文": "Gina Sonia",
        },
        "img_file": "gina.jpeg",
        "sid": {
            "Indonesia": "SID: 004202400076",
            "English": "SID: 004202400076",
            "日本語": "SID: 004202400076",
            "简体中文": "SID：004202400076",
        },
        "role": {
            "Indonesia": "🔧 Distribusi: Fokus laporan & bantu olah data",
            "English": "🔧 Role: Focused on report & assist data processing",
            "日本語": "🔧 役割：レポート担当・データ処理補助",
            "简体中文": "🔧 职责：专注报告并协助数据处理",
        },
        "origin": {
            "Indonesia": "Asal daerah: Cikampek",
            "English": "Origin: Cikampek",
            "日本語": "出身地：チカンペック",
            "简体中文": "来自：Cikampek",
        }
    },
    {
        "name": {
            "Indonesia": "Ananda Fasya Wiratama Putri",
            "English": "Ananda Fasya Wiratama Putri",
            "日本語": "Ananda Fasya Wiratama Putri",
            "简体中文": "Ananda Fasya Wiratama Putri",
        },
        "img_file": "fasya.jpeg",
        "sid": {
            "Indonesia": "SID: 004202400107",
            "English": "SID: 004202400107",
            "日本語": "SID: 004202400107",
            "简体中文": "SID：004202400107",
        },
        "role": {
            "Indonesia": "⚡ Distribusi: Analisis hubungan variabel, penjelasan pengaruh medsos ke mental, Streamlit bagian analisis",
            "English": "⚡ Role: Variable relationship analysis, explanation of social media effect on mental, Streamlit analysis",
            "日本語": "⚡ 役割：変数関係分析、SNSの心理影響解説、Streamlit分析",
            "简体中文": "⚡ 职责：变量关系分析，社交媒体对心理的影响，Streamlit分析部分",
        },
        "origin": {
            "Indonesia": "Asal daerah: Depok",
            "English": "Origin: Depok",
            "日本語": "出身地：デポック",
            "简体中文": "来自：Depok",
        }
    }
]
# ----------------- MAIN CONTENT -----------------

if menu == menu_items[0]:
    st.markdown(f"<div class='stTitleMain'>{tt['profile_title']}</div>", unsafe_allow_html=True)

    for prof in profile_data:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        
        cols = st.columns([1, 3])
        with cols[0]:
            img_path = os.path.join(BASE_DIR, prof["img_file"])
            if os.path.exists(img_path):
                st.image(img_path, width=260)
            else:
                st.warning(f"Gambar tidak ditemukan: {img_path}")
        
      if menu == menu_items[0]:
    st.markdown(f"<div class='stTitleMain'>{tt['profile_title']}</div>", unsafe_allow_html=True)

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
            st.markdown(
                f"<div class='stProfileName'>{prof['name'][lang]} ⚙️</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='stProfileRole'>{prof['role'][lang]}</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"**{prof['sid'][lang]}**")
            st.markdown(
                f"<span class='stOrigin'>{prof['origin'][lang]}</span>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)


        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)


# ----------------- ANALISIS DATA -----------------
elif menu == menu_items[1]:

    st.markdown(f"<div class='stTitleMain'>{tt['analysis_title']}</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(tt["file"], type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        st.subheader(tt["preview"])
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)

        # ------------ DISTRIBUSI DATA ------------
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
                # Histogram
                st.markdown(f"<span class='stLabel'>{tt['hist']}: {col}</span>", unsafe_allow_html=True)
                fig1, ax1 = plt.subplots(figsize=(7, 3))
                ax1.hist(df[col].dropna(), bins=20, color="#1976d2", alpha=0.85)
                ax1.set_facecolor("#223a5e")
                ax1.set_title(f"{tt['hist']}: {col}", fontsize=12)
                st.pyplot(fig1)

                # Boxplot
                st.markdown(f"<span class='stLabel'>{tt['box']}: {col}</span>", unsafe_allow_html=True)
                fig2, ax2 = plt.subplots(figsize=(7, 3))
                ax2.boxplot(df[col].dropna(), vert=False, patch_artist=True,
                            boxprops=dict(facecolor='#f7c325', color='#1976d2'))
                ax2.set_facecolor("#223a5e")
                ax2.set_title(f"{tt['box']}: {col}", fontsize=12)
                st.pyplot(fig2)

        else:
            st.info(tt["desc_cols"])

        st.markdown("</div>", unsafe_allow_html=True)


        # ------------ ANALISIS HUBUNGAN VARIABEL ------------
        st.markdown(f"<div class='stSubHeader'>{tt['vra_title']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            x1 = st.selectbox(tt["vra_var1"], df.columns.tolist())
        with colB:
            x2 = st.selectbox(tt["vra_var2"], df.columns.tolist(), index=1 if len(df.columns) > 1 else 0)

        # DETEKSI TIPE
        tipe_x1 = tt["type_num"] if np.issubdtype(df[x1].dropna().dtype, np.number) else tt["type_cat"]
        tipe_x2 = tt["type_num"] if np.issubdtype(df[x2].dropna().dtype, np.number) else tt["type_cat"]

        st.markdown(f"<span class='stLabel'>{x1}: {tipe_x1}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='stLabel'>{x2}: {tipe_x2}</span>", unsafe_allow_html=True)

        # ------------ KATEGORI vs KATEGORI (Chi-square) ------------
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


        # ------------ NUMERIK vs NUMERIK (Pearson Correlation) ------------
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


        # ------------ Kombinasi tidak didukung ------------
        else:
            st.warning(tt["mix_info"])

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(tt["wait_file"])


# ----------------- ABOUT -----------------
elif menu == menu_items[2]:
    st.markdown(f"<div class='stTitleMain'>{tt['about_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stCard'>{tt['about_content']}</div>", unsafe_allow_html=True)



