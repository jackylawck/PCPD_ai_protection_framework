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

ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"

if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

is_zh = st.session_state.lang == '繁體中文'

# ==========================================
# 2. 結構化風險字典矩陣
# ==========================================
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12 明文規定，涉及「求職者評估、工作表現評核或終止僱傭合約」之場景，屬法定高風險用例[cite: 3]。"
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12，涉及「評估個人的信用可靠程度以作出自動化決策」之場景，屬法定高風險用例[cite: 3]。"
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH", 
        "zh_reason": "依據 PCPD《模範框架》第 25 頁圖 12，涉及「AI 輔助醫學影像分析或治療」之場景，直接關乎人身安全，屬法定高風險用例[cite: 3]。"
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW", 
        "zh_reason": "依據 PCPD《模範框架》第 20 頁第 24 條，用於推送個人化廣告或商品推薦，對持份者重大權益影響較低，屬一般/低風險用例[cite: 3]。"
    }
}

# ==========================================
# 3. Sidebar UI
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("PCPD AI Auditor")
    st.markdown("---")
    st.markdown("### 🏛️ 全球管治框架對齊")
    st.caption("✅ **IAPP AIGP (v2.1):** 涵蓋影子 AI (Shadow AI) 防護、TPRM 與多法域合規。")
    st.caption("✅ **ISO/IEC 42001:** 體系整合與可觀測性。")
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為獨立開發之開源公共利益沙盒原型，並非 PCPD 官方系統。")

# ==========================================
# 4. 主畫面佈局與輸入區
# ==========================================
st.title("🛡️ 香港私隱專員公署 (PCPD) 《人工智能保障模範框架》智能審查系統")
st.markdown("### 企業 AI 導入前置合規評分卡 (PCPD 2024 Model Framework Compliance Station)")

with st.form("audit_form"):
    col1, col2 = st.columns(2)
    with col1:
        company_input = st.selectbox("選擇基礎企業用例 (Base Use Case)", list(RISK_MATRIX.keys()))
    with col2:
        oversight_input = st.selectbox("預期的人為監督模式 (Intended Human Oversight)", ["人在環中 (Human-in-the-loop)", "人為管控 (Human-in-command)", "人在環外 (Human-out-of-the-loop)"])
        
    ai_use_case = st.text_area(
        "請詳細描述您的 AI 應用場景（系統具備智能偵測：影子 AI 違規操作、跨國多法域、第三方現成 SaaS 採購或自研定製等複雜脈絡）",
        placeholder="例如：員工為了加快篩選履歷，私下在本地工作站下載開源模型運行..."
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
        "⚙️ 第三部：系統落地、TPRM 與影子 AI 阻斷", 
        "📢 第四部：持份者溝通與透明度要求"
    ])
    
    # ------------------------------------------
    # 分頁一：風險判定與多法域
    # ------------------------------------------
    with tab1:
        st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督[cite: 3, 4]")
        st.info(f"**【基準風險判定】** {base_risk['zh_reason']}")
        
        has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "中港", "轉移", "外地", "美國", "司法管轄"])
        if has_cross_border:
            st.error("🔴 **深度審計：偵測到多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**\n\n依據《私隱條例》保障資料第 4(2) 原則與跨境規範，機構必須採用**合約規範或其他方法**保障資料保安[cite: 3]。")
        
        st.markdown("##### 👥 人為監督模式（Human Oversight）合規審查")
        if base_risk["level"] == "HIGH":
            if "人在環中" not in current_oversight:
                st.warning(f"⚠️ **管治衝突警告：** 依據《模範框架》第二部第 32(i) 條明確規定，高風險 AI 系統**應強制採取「人在環中」(Human-in-the-loop)** 方式[cite: 3]。人類決策者必須在決策過程中保留控制權[cite: 3]。")
            else:
                st.success("✅ **人為監督配置合規：** 符合《模範框架》第 32 條高風險用例採取「人在環中」之規範，人類保留最終裁量權[cite: 3]。")

    # ------------------------------------------
    # 分頁二：動態智能分流（影子 AI vs 採購 vs 自研）
    # ------------------------------------------
    with tab2:
        st.subheader("第三部：AI 模型的定製與系統管理[cite: 3, 4]")
        
        is_shadow_ai = any(w in ctx_text for w in ["影子", "shadow", "私下", "員工自行", "繞過", "未授權", "未經批准", "偷偷", "本地工作站"])
        is_third_party = any(w in ctx_text for w in ["第三方", "third party", "api", "黑箱", "black box", "採購", "procure", "saas", "廠商"])
        
        if is_shadow_ai:
            st.error("🚨 **重大合規危機：偵測到「影子 AI (Shadow AI)」違規操作！(Critical System Failure)**")
            st.markdown(
                "💡 **AIGP 專家審計診斷：**\n"
                "員工繞過 IT 與採購程序私自運行 AI 模型，直接違反《私隱條例》保障資料第 4 原則（資料保安）[cite: 3]。機構作為資料使用者，未能採取切實可行的步驟防止資料在未獲准許下被處理[cite: 3]。"
                "常規的合規打分在此情境下**無效**，董事會必須立即啟動以下阻斷與重建機制："
            )
            sh1 = st.checkbox("【技術阻斷與可觀測性】IT 部門已部署 CASB (雲端存取安全代理) 或端點防護，阻擋未經授權的開源模型、Hugging Face 庫或 API 的呼叫。")
            sh2 = st.checkbox("【修訂 AUP 政策】已更新《可接受使用政策 (Acceptable Use Policy)》，明文嚴禁將包含 PII、客戶數據或商業機密的內容輸入未經審批的外部 AI 工具。")
            sh3 = st.checkbox("【建立認可清單 (Whitelisting)】堵不如疏，已為員工提供經過企業合規審查、承諾零數據留存的內部安全 AI 替代方案。")
            
            sh_score = (sum([sh1, sh2, sh3]) / 3) * 100
            st.progress(sh_score / 100)
            if sh_score < 100: st.warning("⚠️ 必須完成所有阻斷與規範措施，否則企業將持續暴露於嚴重的資料外洩風險中。")
            
        elif is_third_party:
            st.warning("🚨 **核心治理分支切換：第三方方案 / 廠商 API 採購軌道 (TPRM Route Active)**")
            st.markdown("💡 **高管審計核心提示：** 面對黑箱系統，治理核心必須全面轉向 **合約約束 (Contractual Protections)** 與 **第三方風險管理 (TPRM)**[cite: 3]。")
            tp1 = st.checkbox("【資料處理者合約保障】已簽署正式協議，嚴禁廠商將 PII 用作模型二次訓練（符合指引第 16(v) 條）[cite: 3]。")
            tp2 = st.checkbox("【合約責任轉嫁】已明訂非法歧視或資料外洩時的法律責任歸屬與補償機制（符合指引第 18 條）[cite: 3]。")
            tp3 = st.checkbox("【AI 事故暫停機制】已建立「一鍵斷開」的 AI 事故應變計劃（符合指引第 49 條圖 18）[cite: 3]。")
            
            tp_score = (sum([tp1, tp2, tp3]) / 3) * 100
            st.markdown(f"##### 📊 第三方採購 (TPRM) 合規就緒度：**{tp_score:.0f}%**")
            st.progress(tp_score / 100)
            
        else:
            st.success("🛠️ **核心治理分支切換：自主研發與定製實施軌道 (In-House Development Route Active)**")
            st.markdown("請勾選已落實之開發期控制措施（依據指引第三部「數據準備與定製實施」）：")
            in1 = st.checkbox("【資料最少化】收集微調數據屬足夠但不超乎適度，已移除或假名化無關之敏感特徵。（指引第 41(ii) 條）[cite: 3]")
            in2 = st.checkbox("【私隱增強技術】處理高敏感特徵時，已評估或採用差分私隱、合成數據等 PETs 技術。（指引第 41(ii) 條）[cite: 3]")
            in3 = st.checkbox("【防範模型漂移】已建立內部日誌監控，防止模型表現隨時間出現「模型漂移 (Model Drift)」（指引第 48(v) 條）[cite: 3]。")
            
            in_score = (sum([in1, in2, in3]) / 3) * 100
            st.markdown(f"##### 📊 自主研發與定制合規就緒度：**{in_score:.0f}%**")
            st.progress(in_score / 100)

    # ------------------------------------------
    # 分頁三：第四部 —— 持份者溝通
    # ------------------------------------------
    with tab3:
        st.subheader("第四部：與持份者（求職者、員工、消費者）的溝通及交流[cite: 3, 4]")
        st.markdown("- **顯著披露 (Prominent Disclosure)：** 必須向受影響群體清楚且顯著地披露 AI 系統的使用情況（指引第 53(i) 條）[cite: 3]。")
        st.markdown("- **局部可解釋性與救濟途徑 (Redress Mechanism)：** 若 AI 決策對個人產生重大影響，機構必須提供人為介入的選項，容許當事人表達反饋並要求重新審視（指引第 56/58 條）[cite: 3]。")
