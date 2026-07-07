import streamlit as st

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

# Initialize Session State
if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

is_zh = st.session_state.lang == '繁體中文'

# ==========================================
# 2. 結構化風險字典矩陣 (基於 PCPD 2024 官方高風險定義精準映射)
# ==========================================
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12 明文規定，涉及「求職者評估、工作表現評核或終止僱傭合約」之場景，屬法定高風險用例[cite: 3]。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'Assessment of job applicants, evaluation of job performance or termination of employment contracts' is classified as High Risk[cite: 4]."
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架}$第 25 頁圖 12，涉及「評估個人的信用可靠程度以作出自動化決策」之場景，屬法定高風險用例[cite: 3]。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'Evaluation of the creditworthiness of individuals for making automated financial decisions' is classified as High Risk[cite: 4]."
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12，涉及「AI 輔助醫學影像分析或治療」之場景，直接關乎人身安全，屬法定高風險用例[cite: 3]。",
        "en_reason": "Per PCPD Model Framework (P.29, Fig 12), 'AI-assisted medical imaging analytics or therapies' is classified as High Risk[cite: 4]."
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW", 
        "zh_reason": "依據 PCPD《模範框架》第 20 頁第 24 條，用於推送個人化廣告或商品推薦，對持份者重大權益影響較低，屬一般/低風險用例[cite: 3]。",
        "en_reason": "Per PCPD Model Framework (P.23, Para 24), systems used to present individuals with personalised advertisements are lower risk[cite: 4]."
    }
}

# ==========================================
# 3. Sidebar UI (側邊欄官方框架導航)
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
    st.caption("核心指標 100% 依據香港個人資料私隱專員公署 (PCPD) 《人工智能：個人資料保障模範框架》進行決定性邏輯編碼[cite: 3, 4]加粗。")
    st.markdown("---")
    st.markdown("### 🏛️ 全球管治框架對齊" if is_zh else "### 🏛️ Global Frameworks")
    st.caption("✅ **IAPP AIGP (v2.1):** Domain II, III, IV 精準映射")
    st.caption("✅ **ISO/IEC 42001 (AIMS):** 體系整合")
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為獨立開發之開源公共利益沙盒原型，並非 PCPD 官方系統。")

# ==========================================
# 4. 主畫面佈局與輸入區
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
        "請詳細描述您的 AI 應用場景（系統將自動智能偵測：跨國多法域衝突、中港跨境數據、第三方現成 SaaS 採購或自研定製等複雜脈絡）",
        placeholder="例如：總部在歐盟受 EU AI Act 監管，香港分公司向美國廠商採購生成式招聘系統，處理中港跨境數據..."
    )
    
    if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍"):
        st.session_state.audit_performed = True
        st.session_state.company_context = company_input
        st.session_state.human_oversight_pref = oversight_input
        st.session_state.case_description = ai_use_case

# ==========================================
# 5. Core Engine: PCPD Dynamic Logic Reasoning
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
        st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督[cite: 3, 4]")
        st.info(f"**【基準風險判定】** {base_risk['zh_reason']}")
        
        # 智能偵測：多法域與跨境數據流動
        has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "cross border", "中港", "轉移", "外地", "美國", "司法管轄", "jurisdiction"])
        has_eu_act = any(w in ctx_text for w in ["歐盟", "eu ai act", "eu", "總部", "headquarter", "歐洲"])
        
        if has_cross_border or has_eu_act:
            st.error("🔴 **深度審計：偵測到多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**")
            st.markdown(
                f"- **《私隱條例》保障資料第 4(2) 原則與跨境規範（模範框架第 14 頁）：** 機構作為資料使用者，若將個人資料轉移予外地（如美國）資料處理者進行雲端處理，必須採用**合約規範或其他方法**保障資料保安[cite: 3]。\n"
                f"- **跨國管轄權衝突（EU AI Act vs PCPD）：** 企業總部若受《歐盟 AI 法案》監管，香港分公司部署時必須進行雙重合規映射。董事會應指示法律合規部門簽發標準契約條款（SCCs）以應對多法域重疊監管[cite: 3]。"
            )
        
        st.markdown("##### 👥 人為監督模式（Human Oversight）合規審查")
        if base_risk["level"] == "HIGH" or has_eu_act:
            if "人在環中" not in current_oversight:
                st.warning(f"⚠️ **管治衝突警告 (Governance Misalignment)：** 依據《模範框架》第二部第 32(i) 條明確規定，高風險 AI 系統**應強制採取「人在環中」(Human-in-the-loop)** 方式[cite: 3]。人類決策者必須在決策過程中保留控制權，以防止或減低 AI 出錯或不當自動化決定[cite: 3]。")
            else:
                st.success("✅ **人為監督配置合規：** 符合《模範框架》第 32 條高風險用例採取「人在環中」之規範，人類保留最終裁量權[cite: 3]。")

    # ------------------------------------------
    # 分頁二：第三部 —— 徹底修復缺陷！智能分流「採購 TPRM」與「自研」
    # ------------------------------------------
    with tab2:
        st.subheader("第三部：AI 模型的定製與AI系統的實施及管理[cite: 3, 4]")
        
        # 🌟 智能識別：區分「第三方採購/SaaS/API」與「內部自主研發」
        is_third_party = any(w in ctx_text for w in ["第三方", "third party", "third-party", "api", "黑箱", "black box", "採購", "procure", "現成", "off-the-shelf", "廠商", "saas"])
        
        if is_third_party:
            st.error("🚨 **核心治理分支切換：偵測到第三方方案 / 外購 SaaS / 廠商 API 採購軌道 (TPRM Route Active)**")
            st.markdown(
                f"💡 **高管審計核心提示（依據《模範框架》第一部第 16 條及第三部第 44 條修正）[cite: 3]：**\n\n"
                f"由於本案屬於「向外部廠商採購現成系統且無法獲取底層細節」[cite: 3]，企業在實踐中**無法、也無需進行內部的模型微調、控制數據準備或直接監控算法漂移**[cite: 3]。"
                f"董事會的最高管治核心必須全面轉向 **合約約束 (Contractual Protections)** 與 **第三方風險管理 (Third-Party Risk Management, TPRM)**[cite: 3]："
            )
            
            tp1 = st.checkbox("【資料處理者合約保障】已與外部廠商簽署正式資料處理者協議，明文禁止廠商將香港分公司輸入的求職者 PII 與提示詞用作其模型二次訓練。（符合指引第 16(v) 及 44(ii) 條）[cite: 3]")
            tp2 = st.checkbox("【合約責任轉嫁】合約中已明訂當廠商系統產生不當偏見、非法歧視或資料外洩時的法律責任歸屬、罰則與即時通知義務。（符合指引第 18 條）[cite: 3]")
            tp3 = st.checkbox("【AI 事故暫停機制】已建立「AI 事故應變計劃」，當供應商遭遇黑客攻擊、單方面規格變更或觸發隱私漏洞時，企業有指定人員能一鍵「暫停」或「停止」系統連線（符合指引第 46(iv) 及 49 條圖 18）[cite: 3] 。")
            
            tp_score = (sum([tp1, tp2, tp3]) / 3) * 100
            st.markdown(f"##### 📊 第三方採購與供應商管理 (TPRM) 合規就緒度：**{tp_score:.0f}%**")
            st.progress(tp_score / 100)
            
        else:
            st.success("🛠️ **核心治理分支切換：自主研發、自建模型或深度微調軌道 (In-House Development Route Active)**")
            st.markdown("請勾選已落實之開發期控制措施（依據指引第三部「數據準備與定製實施」）：")
            
            cb1 = st.checkbox("【資料最少化】收集微調數據屬足夠但不超乎適度，已移除或假名化無關之敏感特徵。（指引第 41(ii) 條）[cite: 3]")
            cb2 = st.checkbox("【私隱增強技術】處理高敏感特徵時，已評估或採用差分私隱、合成數據等 PETs 技術。（指引第 41(ii) 條）[cite: 3]")
            cb3 = st.checkbox("【防範模型漂移】已指派技術團隊建立內部日誌監控，防止模型表現隨時間出現「模型漂移 (Model Drift)」。（指引第 48(v) 條）[cite: 3]")
            
            in_score = (sum([in1, in2, in3]) / 3) * 100
            st.markdown(f"##### 📊 自主研發與定制合規就緒度：**{in_score:.0f}%**")
            st.progress(in_score / 100)

    # ------------------------------------------
    # 分頁三：第四部 —— 持份者溝通、透明度與可解釋性
    # ------------------------------------------
    with tab3:
        st.subheader("第四部：與持份者（求職者、員工、消費者）的溝通及交流[cite: 3, 4]")
        st.markdown("- **顯著披露 (Prominent Disclosure)：** 必須向受影響群體（如求職者）清楚且顯著地披露 AI 系統的使用情況與介入程度（指引第 53(i) 條）[cite: 3]。")
        st.markdown("- **局部可解釋性與救濟途徑 (Redress Mechanism)：** 若 AI 決策對個人產生重大影響（如篩選簡歷不通過），機構**必須提供人為介入的選項**，容許當事人表達反饋、尋求解釋並要求合規人員重新審視（指引第 56/58 條）[cite: 3]。")
        st.markdown("- **淺白語言 (Plain Language)：** 與持份者溝通之所有私隱政策與通知，應使用淺白的語言和清楚易明的方式表達（指引第 60 條）[cite: 3]。")
