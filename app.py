import streamlit as st
import re

# ==========================================
# 1. 頁面配置與高管級 UI 設定
# ==========================================
st.set_page_config(
    page_title="PCPD AI Model Framework Intelligence Workspace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stCheckbox > label {font-weight: 500;}
    </style>
""", unsafe_allow_html=True)

# 香港個人資料私隱專員公署 (PCPD) 官方文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"
EN_PDF_URL = "https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf"

# Initialize Session State
if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
if 'messages' not in st.session_state: st.session_state.messages = []
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

is_zh = st.session_state.lang == '繁體中文'

# ==========================================
# 2. 結構化風險字典矩陣 (基於 PCPD 2024 官方高風險定義修正)
# ==========================================
# 依據官方文件第 25 頁圖 12 (Figure 12: Examples of AI Use Cases that May Incur Higher Risk) 精準映射
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12 明文規定，涉及「求職者評估、工作表現評核或終止僱傭合約」之場景，屬法定高風險用例。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'Assessment of job applicants, evaluation of job performance or termination of employment contracts' is strictly classified as High Risk."
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12，涉及「評估個人的信用可靠程度以作出自動化決策」之場景，屬法定高風險用例。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'Evaluation of the creditworthiness of individuals for making automated financial decisions' is strictly classified as High Risk."
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12，涉及「AI 輔助醫學影像分析或治療」之場景，直接關乎人身安全與生物辨識資料，屬法定高風險用例。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'AI-assisted medical imaging analytics or therapies' involving sensitive biometric data is classified as High Risk."
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW", 
        "zh_reason": "依據 PCPD《模範框架》第 20 頁第 24 條，用於推送個人化廣告或時裝建議，不太可能對個人造成重大影響，屬一般/低風險用例。",
        "en_reason": "Per PCPD Model Framework (P.23, Para 24), systems used to present individuals with personalised advertisements are unlikely to have a significant impact, thus lower risk."
    },
    "社福與非牟利機構 (一般行政輔助)": {
        "level": "LOW", 
        "zh_reason": "依據 PCPD《模範框架》第 20 頁第 24 條，用於內部翻譯或一般行政輔助，對個人產生重大影響的可能性較小，屬一般/低風險用例。",
        "en_reason": "Per PCPD Model Framework (P.23, Para 24), AI tools used for internal translation carry a lower risk profile."
    }
}

# ==========================================
# 3. Sidebar UI (強調官方權威與背書)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("PCPD AI Auditor")
    st.header("🌐 UI Language / 介面語言")
    lang_choice = st.radio("Select Language", ['繁體中文', 'English'], index=0 if st.session_state.lang == '繁體中文' else 1)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🏛️ 官方模範框架核對基準" if is_zh else "### 🏛️ Model Framework Baseline")
    st.caption("本系統核心指標 100% 依據香港個人資料私隱專員公署 (PCPD) 於 2024 年 6 月發布之《人工智能：個人資料保障模範框架》進行決定性邏輯編碼。" if is_zh else "100% aligned with the 'Artificial Intelligence: Model Personal Data Protection Framework' published by PCPD in June 2024.")
    st.markdown("---")
    st.markdown("### 🏛️ 全球管治框架對齊 (Alignment)")
    st.caption("✅ **IAPP AIGP (v2.1):** Domain II Laws & Standards")
    st.caption("✅ **ISO/IEC 42001 (AIMS):** AI 管理體系對齊")
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為開源公共利益沙盒原型，旨在推廣與宣傳 PCPD 負責任 AI 原則，並非官方系統。" if is_zh else "⚠️ **Disclaimer:** This is an independent open-source sandbox prototype for public advocacy, not an official PCPD system.")

# ==========================================
# 4. 主畫面與輸入區
# ==========================================
st.title("🛡️ 香港私隱專員公署 (PCPD) 《人工智能保障模範框架》智能審查系統")
st.markdown("### 企業 AI 導入前置合規評分卡 (PCPD 2024 Model Framework Compliance Station)")

with st.form("audit_form"):
    st.markdown("#### 📥 第一步：輸入企業場景脈絡 (Input Operational Context)")
    col1, col2 = st.columns(2)
    with col1:
        company_input = st.selectbox("選擇基礎企業用例 (Base Use Case)", list(RISK_MATRIX.keys()))
    with col2:
        oversight_input = st.selectbox("預期的人為監督模式 (Intended Human Oversight)", ["人在環中 (Human-in-the-loop)", "人為管控 (Human-in-command)", "人在環外 (Human-out-of-the-loop)"])
        
    ai_use_case = st.text_area(
        "請詳細描述您的 AI 應用場景（支援偵測：跨國多法域、跨境數據、第三方現成 API 或黑箱採購等複雜脈絡）",
        placeholder="在此貼上您的情境題進行壓力測試..."
    )
    
    if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍"):
        st.session_state.audit_performed = True
        st.session_state.company_context = company_input
        st.session_state.human_oversight_pref = oversight_input
        st.session_state.case_description = ai_use_case

# ==========================================
# 5. Core Engine: PCPD Model Framework Context Reasoning
# ==========================================
if st.session_state.audit_performed:
    st.markdown("---")
    st.markdown("### 📋 第二步：依據 PCPD 2024《模範框架》產出之高管稽核報告")
    
    ctx_text = st.session_state.case_description.lower()
    base_risk = RISK_MATRIX[st.session_state.company_context]
    current_oversight = st.session_state.human_oversight_pref
    
    tab1, tab2, tab3 = st.tabs([
        "📊 第一、二部：管治架構與風險監督", 
        "⚙️ 第三部：模型定製與第三方風險管理 (TPRM)", 
        "📢 第四部：持份者溝通與透明度要求"
    ])
    
    # ------------------------------------------
    # 分頁一：第一、二部 —— 策略、管治、風險判定與多法域
    # ------------------------------------------
    with tab1:
        st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督")
        
        # 1. 基礎風險判定
        st.info(f"**【基準風險判定】** {base_risk['zh_reason'] if is_zh else base_risk['en_reason']}")
        
        # 2. 多法域與跨境數據動態偵測 (修復缺陷一)
        has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "cross border", "中港", "轉移", "司法管轄", "jurisdiction", "分公司", "總部"])
        has_eu_act = any(w in ctx_text for w in ["歐盟", "eu ai act", "eu", "總部", "headquarter", "歐洲"])
        
        if has_cross_border or has_eu_act:
            st.error("🔴 **深度審計：偵測到多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**")
            st.markdown(
                f"*- **《私隱條例》保障資料第 4(2) 原則與跨境規範（模範框架第 14 頁）：** 機構作為資料使用者，若將個人資料轉移予外地資料處理者進行雲端定製，必須採用**合約規範或其他方法**保障資料保安 [cite: 85, 206]。*\n"
                f"*- **跨國管轄權衝突：** 總部若受《歐盟 AI 法案》監管，香港分公司部署時必須進行雙重合規映射。董事會應指示法律合規部門簽發標準契約條款（SCCs）以應對多法域重疊監管。*"
            )
        
        # 3. 監督衝突審查 (依據指引第 24 頁第 32 條)
        st.markdown("##### 👥 人為監督模式（Human Oversight）合規審查")
        if base_risk["level"] == "HIGH" or has_eu_act:
            if "人在環中" not in current_oversight:
                st.warning(f"⚠️ **管治衝突警告 (Governance Misalignment)：** 依據《模範框架》第二部第 32(i) 條明確規定，高風險 AI 系統**應採取「人在環中」(Human-in-the-loop)** 方式 [cite: 22, 343]。人類決策者必須在過程中保留控制權，以防止或減低自動化偏見 [cite: 22, 343]。當前配置的 [{current_oversight}] 存在重大違規風險！")
            else:
                st.success("✅ **人為監督配置合規：** 符合《模範框架》第 32 條高風險用例採取「人在環中」之規範 [cite: 22, 343]。")
        else:
            st.success(f"🟢 **低/一般風險監督配置：** 依據《模範框架》第 32(ii) 條，低風險場景可採完全自動化之「人在環外」模式 [cite: 22, 344]。")

    # ------------------------------------------
    # 分頁二：第三部 —— 模型定製、實施、與關鍵的 TPRM 採購分支
    # ------------------------------------------
    with tab2:
        st.subheader("第三部：AI 模型的定製與AI系統的實施及管理")
        
        # 4. 區分「第三方採購 API/黑箱」與「內部自主研發」 (修復缺陷二)
        is_third_party = any(w in ctx_text for w in ["第三方", "third party", "third-party", "api", "黑箱", "black box", "採購", "procure", "現成", "off-the-shelf", "無法獲取"])
        
        if is_third_party:
            st.error("🚨 **核心治理分支：第三方黑箱方案 / API 採購軌道 (TPRM Route)**")
            st.markdown(
                f"💡 **高管審計提示（依據《模範框架》第一部第 16 條及第三部第 44 條修正）：**\n\n"
                f"由於企業無法獲取第三方 API 的底層技術細節（Lack of Explainability），此時**無法在技術層面控制其數據準備、微調或模型漂移** 。"
                f"董事會的管治核心必須全面轉向 **合約約束 (Contractual Protections)** 與 **供應商盡職調查 (Supplier Due Diligence)** [cite: 22, 140, 160, 174]："
            )
            
            tp1 = st.checkbox("【資料處理者協議】已與 AI 供應商簽署正式合約，嚴禁供應商將企業輸入的提示詞與 PII 用作其基礎模型的二次訓練。（符合指引第 16(v) 條與第 44(ii) 條）[cite: 168, 514]")
            tp2 = st.checkbox("【合約責任轉嫁】合約中已明訂當第三方 API 產生非法歧視、錯誤內容或發生資料保安事故時的法律責任歸屬與補償機制。（符合指引第 18 條）[cite: 188]")
            tp3 = st.checkbox("【事故應變與暫停】已建立「AI 事故應變計劃」，當第三方供應商遭遇黑客攻擊或單方面變更規格時，企業能指派專人一鍵「暫停」或「停止」系統連線。（符合指引第 46(iv) 條與第 49 條圖 18）[cite: 534, 583, 596]")
            
            tp_score = (sum([tp1, tp2, tp3]) / 3) * 100
            st.markdown(f"##### 📊 第三方採購 (TPRM) 合規就緒度：**{tp_score:.0f}%**")
            st.progress(tp_score / 100)
        else:
            st.success("🛠️ **核心治理分支：自主研發、微調與定製實施軌道 (In-house Customisation Route)**")
            st.markdown(f"*根據《模範框架》第三部第 41 條及第 43 條，自建或微調模型應落實以下技術控制 [cite: 22, 413, 475]：*")
            
            in1 = st.checkbox("【資料最少化】在微調 (Fine-tuning) 數據集中，已刪除或假名化無關之個人特徵（符合指引第 41(ii) 條）。[cite: 426, 428]")
            in2 = st.checkbox("【私隱增強技術】已評估在數據定製或發放前，採用差分私隱 (Differential Privacy) 或合成數據（符合指引第 41(ii) 條）。[cite: 430, 436]")
            in3 = st.checkbox("【模型漂移監查】已指派專人監察模型是否出現「模型漂移 (Model Drift)」或「模型衰退」，定期以新數據微調（符合指引第 48(v) 條）。[cite: 550, 561]")
            
            in_score = (sum([in1, in2, in3]) / 3) * 100
            st.markdown(f"##### 📊 自主研發與定制合規就緒度：**{in_score:.0f}%**")
            st.progress(in_score / 100)

    # ------------------------------------------
    # 分頁三：第四部 —— 持份者溝通、透明度與可解釋性
    # ------------------------------------------
    with tab3:
        st.subheader("第四部：與持份者的溝通及交流")
        st.markdown(f"*依據《模範框架》第四部之規範，向董事會匯報時必須落實以下持份者保障機制 [cite: 22, 626]：*")
        st.markdown("- **顯著披露 (Prominent Disclosure)：** 除非 AI 的使用顯而易見，否則必須向受影響群體（如員工、消費者）清楚披露 AI 系統的介入程度（指引第 53(i) 條）。[cite: 635, 639]")
        st.markdown("- **可解釋性 (Explainable AI)：** 應向資料當事人說明促使 AI 系統做出個別自動化決策的主要因素（局部可解釋性）（指引第 58(iii) 條）。[cite: 655, 660, 661]")
        st.markdown("- **人工介入與救濟 (Redress & Human Intervention)：** 當 AI 輸出結果對個人造成重大影響時，機構**必須提供官方管道讓當事人尋求合理解釋、表達反饋及要求人為重新審視**（指引第 56 條）。[cite: 652]")
