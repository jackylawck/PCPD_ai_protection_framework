import streamlit as st

# 1. 頁面配置與高管級 UI 設定
st.set_page_config(
    page_title="PCPD AI Governance Scorecard (AIGP v2.1 Aligned)",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# 官方文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"

# 2. 狀態保存機制 (Session State) - 解決表單重整資料遺失問題
if "audit_performed" not in st.session_state:
    st.session_state.audit_performed = False
if "company_context" not in st.session_state:
    st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state:
    st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

# 結構化風險字典矩陣 (Risk Mapping Matrix) - 易於維護與擴展
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH", 
        "reason": "涉及求職者評估、工作表現評核或終止僱傭合約，可能對個人職涯與法律權益造成重大影響。"
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH", 
        "reason": "涉及評估個人的信用可靠程度以作出自動化財務決策，可能令個人無法獲得信貸安排。"
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH", 
        "reason": "涉及 AI 輔助醫學影像分析或治療，直接關乎人身安全與高敏感健康生物辨識數據。"
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW", 
        "reason": "主要用於推送個人化廣告或時裝建議，除非涉及大規模監控，否則對個人造成重大影響的可能性較低。"
    },
    "社福與非牟利機構 (一般行政輔助)": {
        "level": "LOW", 
        "reason": "一般行政辅助或內部翻譯，對持份者權益產生直接重大不利影響的機率相較可控。"
    }
}

# 3. 側邊欄：權威背書與管治框架映射
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("Enterprise AI Auditor")
    st.markdown("### 📘 官方框架精準錨點")
    st.markdown(f"- [第一部：策略及管治 (P.10)]({ZH_PDF_URL}#page=10)")
    st.markdown(f"- [第二部：風險與監督 (P.20)]({ZH_PDF_URL}#page=20)")
    st.markdown(f"- [第三部：模型與管理 (P.27)]({ZH_PDF_URL}#page=27)")
    st.markdown(f"- [第四部：持份者溝通 (P.40)]({ZH_PDF_URL}#page=40)")
    st.markdown("---")
    st.markdown("### 🏛️ 管治框架對齊 (Alignment)")
    st.caption("✅ **IAPP AIGP (v2.1):** Domain II, III, IV")
    st.caption("✅ **ISO 42001:** AI Management System (AIMS) Integration")
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為獨立開發之開源合規沙盒原型（Public Sandbox），並非 PCPD 官方系統，旨在實踐「治理即代碼 (Governance-as-Code)」。")

# 4. 主畫面佈局
st.title("🛡️ PCPD AI 個人資料保障：企業合規風險評分卡")
st.markdown("### Pre-Deployment Audit Scorecard (Board-Level Reporting)")

# 5. 使用者情境輸入區
with st.form("audit_form"):
    st.markdown("#### 📥 第一步：界定 AI 應用情境與監督模式")
    col1, col2 = st.columns(2)
    with col1:
        company_input = st.selectbox(
            "選擇企業類型與核心場景 (Enterprise Context)",
            list(RISK_MATRIX.keys())
        )
    with col2:
        oversight_input = st.selectbox(
            "預期的人為監督模式 (Intended Human Oversight)",
            ["人在環中 (Human-in-the-loop)", "人為管控 (Human-in-command)", "人在環外 (Human-out-of-the-loop)"]
        )
        
    ai_use_case = st.text_area(
        "詳細描述您的 AI 應用場景與涉及的個人資料（Data Inventory）",
        placeholder="例如：我們計劃導入大型語言模型分析員工績效數據並預測離職率，這涉及年資、考績等個人識別資料 (PII)..."
    )
    
    if st.form_submit_button("執行 PCPD 框架動態稽核 🔍"):
        st.session_state.audit_performed = True
        st.session_state.company_context = company_input
        st.session_state.human_oversight_pref = oversight_input

# 6. 稽核結果展示 (動態讀取 Session State)
if st.session_state.audit_performed:
    st.markdown("---")
    st.markdown("### 📋 第二步：合規稽核報告與行動清單")
    
    current_context = st.session_state.company_context
    current_oversight = st.session_state.human_oversight_pref
    risk_info = RISK_MATRIX[current_context]
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 策略及管治", 
        "⚖️ 風險評估與監督", 
        "⚙️ 模型定製與保安", 
        "📢 持份者溝通"
    ])
    
    with tab1:
        st.subheader("董事會問責與管治架構 (Accountability)")
        st.info(f"**當前情境：** {current_context}\n\n**合規行動：** 必須確保高級管理層的支持。建議成立由高階主管領導的跨部門 AI 管治委員會，成員需涵蓋 HR、法務、IT 資訊保安與業務單位，並建立組織內的 AI 系統清單。")
        
    with tab2:
        st.subheader("動態風險判定與監督衝突審查")
        if risk_info["level"] == "HIGH":
            st.error(f"🔴 **高風險用例判定 (High Risk Profile):**\n\n{risk_info['reason']}")
            if current_oversight != "人在環中 (Human-in-the-loop)":
                st.warning(f"⚠️ **管治衝突警告 (Governance Misalignment)：**\n\n高風險 AI 系統**應強制採取「人在環中」**模式，人類決策者必須保留最終決定權以防止出錯。當前選擇的 [{current_oversight}] 極可能違反指引，強烈建議修正。")
            else:
                st.success("✅ **監督模式合規：** 針對高風險場景，已正確配置「人在環中」監督模式。")
        else:
            st.success(f"🟢 **一般風險用例判定 (Minimal Risk Profile):**\n\n{risk_info['reason']}\n\n依據風險比例原則，可考慮採取「人在環外」完全自動化或「人為管控」模式，但需持續進行私隱影響評估。")
            
    with tab3:
        st.subheader("資料準備與資訊保安評分卡 (Data Security Scorecard)")
        st.markdown("請勾選已落實之安全控制措施，系統將即時更新合規就緒度：")
        
        cb1 = st.checkbox("【資料最少化】收集資料屬足夠但不超乎適度，已移除或假名化無關之敏感特徵。")
        cb2 = st.checkbox("【私隱增強技術】處理高敏感數據時，已評估或採用差分私隱、合成數據等 PETs 技術。")
        cb3 = st.checkbox("【持續監察與維護】建立機制定期檢視並以新數據重新訓練模型，防範模型漂移 (Model Drift)。")
        cb4 = st.checkbox("【保安漏洞防護】已制定員工輸入提示詞指引，並建立防禦對抗式攻擊 (Adversarial Attacks) 措施。")
        
        readiness_pct = (sum([cb1, cb2, cb3, cb4]) / 4) * 100
        
        st.markdown(f"#### 📈 第三部稽核就緒度分數：**{readiness_pct:.0f}%**")
        st.progress(readiness_pct / 100)
        
        if readiness_pct == 100:
            st.success("🌟 完美合規！已完全納入貫徹私隱設計（Privacy-by-Design）精神。")
        elif readiness_pct >= 50:
            st.warning("⚠️ 已具備基礎防禦，但仍有安全死角，建議盡快補齊未勾選項目。")
        else:
            st.error("🚨 就緒度極低！缺乏核心隱私防護，存在違反保障資料原則的重大合規風險。")
            
    with tab4:
        st.subheader("透明度與當事人權利保障 (Transparency & Rights)")
        st.markdown("- **顯著披露 (Disclosure)：** 除非使用情況顯而易見，否則必須向受影響群體清楚披露 AI 系統的介入程度。")
        st.markdown("- **救濟機制 (Redress Mechanism)：** 若 AI 決策對個人產生重大影響，機構必須提供官方渠道，讓當事人表達反饋、尋求解釋並要求人為重新介入審視。")
        st.markdown("- **溝通語言：** 所有指引與政策應以淺白易懂的語言 (Plain Language) 撰寫。")
