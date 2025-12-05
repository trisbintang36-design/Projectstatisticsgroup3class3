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
    .stCard { background-color: #223a5e; color: #FAFAFA; padding: 18px 24px; margin-bottom: 22px;
        border-radius: 16px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); border: 2.7px solid #f7c325;
        font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace;}
    .stTitleMain { font-size: 2.4rem; font-family: 'Share Tech Mono','Consolas','Roboto Mono', monospace;
        color: #22d2e9; margin-bottom: 1.4rem;font-weight:800; letter-spacing: 1px; text-shadow: 1px 2px 0px #222,2px 4px 1.5px #fff000aa; }
    .stSubHeader { font-size: 1.29rem; color: #f7c325; margin-top:1rem;
        font-family: 'Share Tech Mono', 'Consolas', 'Roboto Mono', monospace; font-weight:700;}
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
        "type_num": "Numerik", "type_cat": "Kategori",
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
        "about_content": "Aplikasi ini dibuat menggunakan Streamlit untuk menganalisis data survei (Excel), analisis deskriptif, dan analisis hubungan variabel otomatis.",
    },
    "English": {
        "title": "Survey Data Analysis App",
        "file": "Upload your survey Excel file",
        "analysis_title": "Data Analysis",
        "desc_title": "Data Distribution",
        "desc_cols": "Select numeric variables for descriptive analysis (histogram & boxplot)",
        "hist": "Histogram",
        "box": "Boxplot",
        "preview": "Preview Data",
        "vra_title": "Variable Relationship Analysis",
        "vra_var1": "Select Variable 1",
        "vra_var2": "Select Variable 2",
        "type_num": "Numeric", "type_cat": "Category",
        "cat_info": "Categorical variables → Chi-Square test",
        "num_info": "Numeric variables → Pearson correlation",
        "result_cat_cat": "Contingency Table",
        "result_num_num": "Pearson Correlation",
        "chi2": "Chi2 = {:.4f}",
        "pval": "P-value = {:.4f}",
        "dof": "Degrees of freedom = {}",
        "conclusion": "Conclusion:",
        "conclude_sig": "Significant relationship between variables (p < 0.05)",
        "conclude_nosig": "No significant relationship between variables (p >= 0.05)",
        "corr_coef": "Coefficient = {:.4f}",
        "corr_pval": "P-value = {:.4f}",
        "corr_conclude_sig": "Significant relationship (p < 0.05)",
        "corr_conclude_nosig": "No significant relationship (p >= 0.05)",
        "mix_info": "The combination is not supported yet.",
        "wait_file": "Please upload your Excel survey file.",
        "profile_title": "Author Profile",
        "about_title": "About App",
        "about_content": "This app is built using Streamlit to analyze survey data, descriptive analysis, and variable relationships automatically.",
    },
    "日本語": {
        "title": "調査データ分析アプリ",
        "file": "Excel調査ファイルをアップロード",
        "analysis_title": "データ分析",
        "desc_title": "データ分布",
        "desc_cols": "記述分析用の数値変数を選択（ヒストグラム＆箱ひげ図）",
        "hist": "ヒストグラム",
        "box": "箱ひげ図",
        "preview": "データプレビュー",
        "vra_title": "変数の関係分析",
        "vra_var1": "変数1を選択",
        "vra_var2": "変数2を選択",
        "type_num": "数値型", "type_cat": "カテゴリ型",
        "cat_info": "カテゴリ型変数 → カイ二乗検定",
        "num_info": "数値型変数 → ピアソン相関",
        "result_cat_cat": "クロス集計表",
        "result_num_num": "ピアソン相関",
        "chi2": "カイ二乗 = {:.4f}",
        "pval": "p値 = {:.4f}",
        "dof": "自由度 = {}",
        "conclusion": "結論：",
        "conclude_sig": "変数間に有意な関係あり (p < 0.05)",
        "conclude_nosig": "変数間に有意な関係なし (p >= 0.05)",
        "corr_coef": "相関係数 = {:.4f}",
        "corr_pval": "p値 = {:.4f}",
        "corr_conclude_sig": "有意な関係あり (p < 0.05)",
        "corr_conclude_nosig": "有意な関係なし (p >= 0.05)",
        "mix_info": "混合変数の自動分析は未対応です。",
        "wait_file": "調査ファイルをアップロードしてください。",
        "profile_title": "著者プロフィール",
        "about_title": "アプリについて",
        "about_content": "本アプリはStreamlitで作成され、調査データの自動分析が可能です。",
    },
    "简体中文": {
        "title": "调查数据分析应用",
        "file": "上传您的调查Excel文件",
        "analysis_title": "数据分析",
        "desc_title": "数据分布",
        "desc_cols": "选择用于描述性分析的数字变量（直方图与箱线图）",
        "hist": "直方图",
        "box": "箱线图",
        "preview": "数据预览",
        "vra_title": "变量关系分析",
        "vra_var1": "选择变量1",
        "vra_var2": "选择变量2",
        "type_num": "数字型", "type_cat": "分类型",
        "cat_info": "分类型变量 → 卡方检验",
        "num_info": "数字型变量 → 皮尔逊相关性",
        "result_cat_cat": "列联表",
        "result_num_num": "皮尔逊相关性",
        "chi2": "卡方值 = {:.4f}",
        "pval": "显著性水平（p值）= {:.4f}",
        "dof": "自由度 = {}",
        "conclusion": "结论：",
        "conclude_sig": "变量间存在显著关系 (p < 0.05)",
        "conclude_nosig": "变量间不存在显著关系 (p >= 0.05)",
        "corr_coef": "相关系数 = {:.4f}",
        "corr_pval": "p值 = {:.4f}",
        "corr_conclude_sig": "存在显著关系 (p < 0.05)",
        "corr_conclude_nosig": "不存在显著关系 (p >= 0.05)",
        "mix_info": "混合变量暂不支持自动分析。",
        "wait_file": "请上传您的调查数据文件。",
        "profile_title": "作者简介",
        "about_title": "关于应用",
        "about_content": "本应用采用Streamlit开发，可自动分析调查数据、描述性分析与变量关系。",
    }
}
tt = text.get(lang, text["Indonesia"])

# --- Profil Pembuat (diperbarui) ---
profile_data = [
    {
        "name": {
            "Indonesia": "Moh. Trisbintang",
            "English": "Moh. Trisbintang",
            "日本語": "モハメド・トリスビンタン",
            "简体中文": "穆罕默德·特里斯宾唐"
        },
        "img_file": "tris.jpeg",
        "sid": {
            "Indonesia": "SID: 004202400102",
            "English": "SID: 004202400102",
            "日本語": "SID: 004202400102",
            "简体中文": "SID：004202400102",
        },
        "role": {
            "Indonesia": "Pembuat Aplikasi",
            "English": "App Creator",
            "日本語": "アプリ制作者",
            "简体中文": "应用程序创建者",
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
            "Indonesia": "Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
            "English": "Basic analysis (histogram, boxplot), Python chart coding, Streamlit graphics",
            "日本語": "基本分析、Pythonグラフ作成、Streamlitグラフィック",
            "简体中文": "基础分析、Python绘图、Streamlit图形部分",
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
            "Indonesia": "Fokus laporan & bantu olah data",
            "English": "Focused on report & assist data processing",
            "日本語": "レポート担当・データ処理補助",
            "简体中文": "专注报告并协助数据处理",
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
            "Indonesia": "Analisis hubungan variabel, penjelasan pengaruh medsos ke mental, Streamlit bagian analisis",
            "English": "Variable relationship analysis, explanation of social media effect on mental, Streamlit analysis",
            "日本語": "変数関係分析、SNSの心理影響解説、Streamlit分析",
            "简体中文": "变量关系分析，社交媒体对心理的影响，Streamlit分析部分",
        },
        "origin": {
            "Indonesia": "Asal daerah: Depok",
            "English": "Origin: Depok",
            "日本語": "出身地：デポック",
            "简体中文": "来自：Depok",
        }
    }
]

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
            st.markdown(f"<div class='stProfileName'>{prof['name'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stProfileRole'>{prof['role'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stOrigin'>{prof['origin'][lang]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stProfileRole'>{prof['sid'][lang]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == menu_items[1]:
    st.markdown(f"<div class='stTitleMain'>{tt['analysis_title']}</div>", unsafe_allow_html=True)
    st.info(tt['wait_file'])
elif menu == menu_items[2]:
    st.markdown(f"<div class='stTitleMain'>{tt['about_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stCard'>{tt['about_content']}</div>", unsafe_allow_html=True)
elif menu == menu_items[1]:  # Analisis Data / Data Analysis
    st.markdown(f"<div class='stTitleMain'>{tt['analysis_title']}</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(tt['file'], type=['xlsx'])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.markdown(f"<div class='stSubHeader'>{tt['preview']}</div>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        
        # --- Descriptive Analysis ---
        st.markdown(f"<div class='stSubHeader'>{tt['desc_title']}</div>", unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        selected_cols = st.multiselect(tt['desc_cols'], numeric_cols)
        
        for col in selected_cols:
            fig, ax = plt.subplots(1,2, figsize=(10,4))
            ax[0].hist(df[col].dropna(), bins=15, color='#1976d2', edgecolor='black')
            ax[0].set_title(f"{tt['hist']} {col}")
            ax[1].boxplot(df[col].dropna())
            ax[1].set_title(f"{tt['box']} {col}")
            st.pyplot(fig)
        
        # --- Variable Relationship Analysis ---
        st.markdown(f"<div class='stSubHeader'>{tt['vra_title']}</div>", unsafe_allow_html=True)
        var1 = st.selectbox(tt['vra_var1'], df.columns)
        var2 = st.selectbox(tt['vra_var2'], df.columns)
        
        type1 = 'num' if np.issubdtype(df[var1].dtype, np.number) else 'cat'
        type2 = 'num' if np.issubdtype(df[var2].dtype, np.number) else 'cat'
        
        if type1 == 'cat' and type2 == 'cat':
            st.markdown(tt['cat_info'])
            ct = pd.crosstab(df[var1], df[var2])
            st.markdown(f"**{tt['result_cat_cat']}**")
            st.dataframe(ct)
            chi2, p, dof, _ = chi2_contingency(ct)
            st.write(tt['chi2'].format(chi2))
            st.write(tt['pval'].format(p))
            st.write(tt['dof'].format(dof))
            conclusion = tt['conclude_sig'] if p<0.05 else tt['conclude_nosig']
            st.write(f"{tt['conclusion']} {conclusion}")
        
        elif type1 == 'num' and type2 == 'num':
            st.markdown(tt['num_info'])
            coef, p = pearsonr(df[var1].dropna(), df[var2].dropna())
            st.markdown(f"**{tt['result_num_num']}**")
            st.write(tt['corr_coef'].format(coef))
            st.write(tt['corr_pval'].format(p))
            conclusion = tt['corr_conclude_sig'] if p<0.05 else tt['corr_conclude_nosig']
            st.write(f"{tt['conclusion']} {conclusion}")
        
        else:
            st.warning(tt['mix_info'])
            
    else:
        st.info(tt['wait_file'])

