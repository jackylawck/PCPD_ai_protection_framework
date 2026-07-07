import streamlit as st
import re

# ==========================================
# 1. Page Configuration & UI Initialization
# ==========================================
st.set_page_config(
    page_title="PCPD AI Governance Workspace (AIGP v2.1 Aligned)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隱藏 Streamlit 預設選單，提升企業產品專業度
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stCheckbox > label {font-weight: 500;}
    </style>
""", unsafe_allow_html=True)

# 官方文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"
EN_PDF_URL = "https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf"

# Initialize Session State
if 'lang' not in st.session_state:
    st.session_state.lang = '繁體中文'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if "audit_performed" not in st.session_state:
    st.session_state.audit_performed = False
if "company_context" not in st.session_state:
    st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state:
    st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

# ==========================================
# 2. Dual-Layer Knowledge Base & Risk Matrix
# ==========================================
# 結構化風險字典矩陣 (Bilingual Risk Mapping Matrix)
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH", 
        "zh_reason": "涉及求職者評估、工作表現評核或終止僱傭合約，可能對個人職涯與法律權益造成重大影響。",
        "en_reason": "Involves assessment of job applicants, evaluation of job performance or termination of employment contracts, which may significantly impact individuals' careers."
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH", 
        "zh_reason": "涉及評估個人的信用可靠程度以作出自動化財務決策，可能令個人無法獲得信貸安排。",
        "en_reason": "Involves evaluating creditworthiness for automated financial decisions, potentially denying access to credit facilities."
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH", 
        "zh_reason": "涉及 AI 輔助醫學影像分析或治療，直接關乎人身安全與高敏感健康生物辨識數據。",
        "en_reason": "Involves AI-assisted medical imaging analytics or therapies, directly affecting personal safety and highly sensitive health/biometric data."
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW", 
        "zh_reason": "主要用於推送個人化廣告或時裝建議，除非涉及大規模監控，否則對個人造成重大影響的可能性較低。",
        "en_reason": "Primarily used for personalized ads or fashion recommendations; less likely to cause significant impact unless large-scale surveillance is involved."
    },
    "社福與非牟利機構 (一般行政輔助)": {
        "level": "LOW", 
        "zh_reason": "一般行政辅助或內部翻譯，對持份者權益產生直接重大不利影響的機率相較可控。",
        "en_reason": "General administrative assistance or internal translation; the probability of direct significant adverse effects on stakeholders is controllable."
    }
}

# PCPD 四大部核心知識庫 (Chatbot & Audit 專用)
PCPD_DB = {
    "part1": {
        "keys": ["策略", "管治", "strategy", "governance", "委員會", "committee", "採購", "procurement"],
        "zh": {
            "title": "第一部：AI 策略及管治",
            "statute": "高級管理層的支持是成功的要素。機構應建立內部的 AI 管治策略，包含 AI 策略、採購考慮及成立跨部門的 AI 管治委員會。",
            "red_flag": "缺乏最高管理層（董事會級別）的參與，或將高風險的 AI 採購決策完全下放至單一業務部門。",
            "board_advice": "明確指派 C-Level 級別高管領導跨部門團隊，並建立企業內的 AI 清單（AI Inventory），確保透明度與問責制。"
        },
        "en": {
            "title": "Part I: AI Strategy and Governance",
            "statute": "Top management support is essential. Organizations should establish an internal AI governance strategy, including AI strategy, procurement considerations, and an AI governance committee.",
            "red_flag": "Lack of Board-level involvement, or delegating high-risk AI procurement decisions entirely to siloed business units.",
            "board_advice": "Designate a C-level executive to lead a cross-functional team and establish an enterprise AI Inventory to ensure transparency and accountability."
        }
    },
    "part2": {
        "keys": ["風險", "risk", " oversight", "監督", "人在環中", "human-in-the-loop", "影響評估", "pia"],
        "zh": {
            "title": "第二部：風險評估及人為監督",
            "statute": "必須進行全面的風險評估以識別私隱風險。高風險 AI 系統應採取「人在環中」(human-in-the-loop) 方式，由人類決策者保留控制權。",
            "red_flag": "在涉及員工考績、信貸拒絕等高風險用例上，採用完全自動化（人在環外）決策，剝奪了人類的最終裁量權。",
            "board_advice": "將人為監督（Human Oversight）級別直接與私隱影響評估（PIA）結果掛鉤，強制高風險場景必須具備人類介入的審計軌跡（Audit Trail）。"
        },
        "en": {
            "title": "Part II: Risk Assessment and Human Oversight",
            "statute": "Comprehensive risk assessments must be conducted. High-risk AI systems should adopt a 'human-in-the-loop' approach where human actors retain control.",
            "red_flag": "Deploying fully automated ('human-out-of-the-loop') decisions in high-risk use cases like HR appraisals or credit denials, stripping away final human discretion.",
            "board_advice": "Directly link the level of Human Oversight to Privacy Impact Assessment (PIA) results. Mandate human-intervention audit trails for high-risk scenarios."
        }
    },
    "part3": {
        "keys": ["模型", "model", "數據", "data", " security", "保安", "定製", "customisation", "漂移", "drift", "測試", "testing"],
        "zh": {
            "title": "第三部：AI 模型的定製與管理",
            "statute": "定製 AI 模型時須遵守資料最少化原則，並確保數據質素。必須防範模型漂移 (Model Drift) 及應對對抗式攻擊，並制定 AI 事故應變計劃。",
            "red_flag": "使用未經匿名化處理的過度敏感個人資料（PII）微調模型，或缺乏對開源框架的安全審查。",
            "board_advice": "實施嚴格的數據準備 SOP。投資於私隱增強技術（PETs，如差分私隱），並建立常態化的紅隊演練（Red Teaming）與模型重新訓練機制。"
        },
        "en": {
            "title": "Part III: Customisation and Management of AI Systems",
            "statute": "Data minimisation and data quality must be ensured during customisation. Organizations must prevent model drift, defend against adversarial attacks, and establish an AI Incident Response Plan.",
            "red_flag": "Fine-tuning models using excessive, non-anonymized PII, or lacking security audits for open-source frameworks.",
            "board_advice": "Implement strict Data Preparation SOPs. Invest in Privacy-Enhancing Technologies (PETs) and establish routine Red Teaming and model re-training mechanisms."
        }
    },
    "part4": {
        "keys": ["持份者", "stakeholder", "透明度", "transparency", "解釋", "explainable", "溝通", "communication", "反饋", "feedback"],
        "zh": {
            "title": "第四部：與持份者的溝通及交流",
            "statute": "應清楚向持份者披露 AI 系統的使用，並在可行情況下解釋 AI 的決策。若決策產生重大影響，應提供途徑讓個人尋求人為介入。",
            "red_flag": "隱瞞 AI 的介入程度，或在受影響員工/客戶要求覆核時，無法給出具意義的 AI 決策解釋（黑盒效應）。",
            "board_advice": "建立標準化的透明度披露指引。確保前端介面具備「退出選項（Opt-out）」及「要求人工覆核」的雙向溝通渠道。"
        },
        "en": {
            "title": "Part IV: Communication and Engagement with Stakeholders",
            "statute": "Clearly disclose the use of AI systems to stakeholders and explain AI decisions where feasible. Provide channels for human intervention if decisions have significant impacts.",
            "red_flag": "Concealing AI involvement or failing to provide meaningful explanations when affected employees/customers request reviews (the 'Black Box' effect).",
            "board_advice": "Establish standardized transparency disclosure guidelines. Ensure user interfaces feature clear 'Opt-out' options and bi-directional channels for requesting human review."
        }
    }
}

# ==========================================
# 3. Sidebar UI (Architect Profile & Settings)
# ==========================================
with st.sidebar:
    st.header("🌐 UI Language / 介面語言")
    lang_choice = st.radio("Select Language / 選擇語言", ['繁體中文', 'English'], index=0 if st.session_state.lang == '繁體中文' else 1)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()
    
    is_zh = st.session_state.lang == '繁體中文'
    
    st.markdown("---")
    if is_zh:
        st.markdown("### ⚙️ 系統設計與安全防護")
        st.markdown("""
        * **研發定位**: 專為企業高管及 IT 審計師設計的 AI 管治前置審查系統。
        * **治理框架**: 架構嚴格對齊 **IAPP AIGP (v2.1)** 部署監督規範與 **ISO/IEC 42001** (AIMS) 體系思維。
        * **架構安全性**: **100% 無 AI / 無 RAG 技術**。採用純決定性代碼架構，杜絕「AI 幻覺」風險。
        * **數據零留底**: 系統無後台數據庫。網頁一經關閉，所有輸入的企業場景數據立即在雲端**全部歸零**，確保貫徹私隱設計 (Privacy-by-Design)。
        """)
    else:
        st.markdown("### ⚙️ System Design & Security")
        st.markdown("""
        * **Positioning**: An AI governance pre-audit system engineered for corporate executives and IT auditors.
        * **Governance**: Architecture strictly aligned with **IAPP AIGP (v2.1)** deployment oversight and **ISO/IEC 42001** (AIMS).
        * **Core Technology**: **100% AI-Free / No RAG**. Built entirely on deterministic logic to eliminate "AI hallucinations."
        * **Data Sovereignty**: Zero back-end databases. All inputs are **completely wiped from memory** upon closing the page, embodying Privacy-by-Design.
        """)
        
    st.markdown("---")
    st.markdown("### 📘 官方框架精準錨點" if is_zh else "### 📘 Official Framework Links")
    st.markdown(f"- [{'第一部：策略及管治 (P.10)' if is_zh else 'Part I: Strategy & Gov (P.10)'}]({ZH_PDF_URL if is_zh else EN_PDF_URL}#page=10)")
    st.markdown(f"- [{'第二部：風險與監督 (P.20)' if is_zh else 'Part II: Risk & Oversight (P.20)'}]({ZH_PDF_URL if is_zh else EN_PDF_URL}#page=20)")
    st.markdown(f"- [{'第三部：模型與管理 (P.27)' if is_zh else 'Part III: Model & Mgmt (P.27)'}]({ZH_PDF_URL if is_zh else EN_PDF_URL}#page=27)")
    st.markdown(f"- [{'第四部：持份者溝通 (P.40)' if is_zh else 'Part IV: Stakeholder Comms (P.40)'}]({ZH_PDF_URL if is_zh else EN_PDF_URL}#page=40)")
    
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為獨立開發之開源合規沙盒原型，並非 PCPD 官方系統。" if is_zh else "⚠️ **Disclaimer:** This is an independent open-source compliance sandbox prototype, not an official PCPD system.")

# ==========================================
# 4. Helper Functions for Logic
# ==========================================
def search_knowledge_base(query):
    query_lower = query.lower()
    results = []
    for ch_id, ch_data in PCPD_DB.items():
        if any(key in query_lower for key in ch_data["keys"]):
            results.append({"type": "chapter", "data": ch_data, "id": ch_id})
    return results

# ==========================================
# 5. Main UI Layout (Three-Track)
# ==========================================
st.title("🛡️ PCPD AI Governance Workspace")
if is_zh:
    st.subheader("100% 決定性合規・香港人工智能個人資料保障模範框架審計")
else:
    st.subheader("100% Deterministic Compliance · PCPD AI Model Framework Auditor")

tab_chat, tab_matrix, tab_audit = st.tabs([
    "💬 Chatbot (動態法規導航 / Policy Navigator)", 
    "⚖️ Risk Matrix (動態情境判定 / Scenario Evaluator)", 
    "📋 Overall Scorecard (全局合規計分卡 / Executive Audit)"
])

# ------------------------------------------
# Track A: Chatbot Interface (Bilingual)
# ------------------------------------------
with tab_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("請輸入關鍵字（例如：'風險', '透明度', '模型漂移', '監督'）..." if is_zh else "Enter keywords (e.g., 'risk', 'transparency', 'model drift')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            matches = search_knowledge_base(prompt)
            if not matches:
                fallback_msg = "🔍 **未找到直接匹配的關鍵字 (No direct match found).**\n\n請嘗試使用更明確的法規術語，或直接點擊側邊欄查閱官方 PDF 文件。\n\nPlease try using specific regulatory terms or refer to the official PDF links in the sidebar."
                st.markdown(fallback_msg)
                st.session_state.messages.append({"role": "assistant", "content": fallback_msg})
            else:
                combined_response = ""
                for match in matches:
                    data_zh = match["data"]["zh"]
                    data_en = match["data"]["en"]
                    
                    st.info(f"**📖 {data_zh['title']} / {data_en['title']}**\n\n**Statutory Core / 法定核心:**\n{data_zh['statute']}\n\n*English:* {data_en['statute']}")
                    st.error(f"**🚨 Red Flags / 違法紅線:**\n{data_zh['red_flag']}\n\n*English:* {data_en['red_flag']}")
                    st.warning(f"**🛡️ Board-Level Governance / 董事會治理建議:**\n{data_zh['board_advice']}\n\n*English:* {data_en['board_advice']}")
                    st.markdown("---")
                    
                    combined_response += f"**{data_zh['title']}**\n\n*Statute:* {data_zh['statute']}\n\n---\n"
                
                st.session_state.messages.append({"role": "assistant", "content": combined_response})

# ------------------------------------------
# Track B: Risk Matrix (Scenario Evaluator)
# ------------------------------------------
with tab_matrix:
    st.markdown("#### 📥 1. 界定 AI 應用情境與監督模式 (Define Use Case & Oversight)" if is_zh else "#### 📥 1. Define AI Use Case & Oversight Model")
    
    with st.form("risk_form"):
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
            "詳細描述您的 AI 應用場景與涉及的個人資料（Data Inventory）" if is_zh else "Detailed AI Use Case & Data Inventory",
            placeholder="例如：我們計劃導入大型語言模型分析員工績效數據並預測離職率..." if is_zh else "e.g., We plan to deploy an LLM to predict staff turnover..."
        )
        
        if st.form_submit_button("執行情境風險判定 🔍" if is_zh else "Execute Risk Evaluation 🔍"):
            st.session_state.audit_performed = True
            st.session_state.company_context = company_input
            st.session_state.human_oversight_pref = oversight_input

    if st.session_state.audit_performed:
        st.markdown("---")
        current_context = st.session_state.company_context
        current_oversight = st.session_state.human_oversight_pref
        risk_info = RISK_MATRIX[current_context]
        
        st.subheader("⚖️ 動態風險判定與監督衝突審查" if is_zh else "⚖️ Dynamic Risk & Governance Misalignment Check")
        
        reason_text = risk_info['zh_reason'] if is_zh else risk_info['en_reason']
        
        if risk_info["level"] == "HIGH":
            st.error(f"🔴 **法定高風險用例 (High Risk Profile):**\n\n{reason_text}")
            if current_oversight != "人在環中 (Human-in-the-loop)":
                warning_msg = f"⚠️ **管治衝突警告 (Governance Misalignment)：**\n\n高風險 AI 系統**應強制採取「人在環中」**模式，人類決策者必須保留最終決定權以防止出錯。當前選擇極可能違反指引，強烈建議修正。" if is_zh else f"⚠️ **Governance Misalignment:** High-risk systems must enforce a 'Human-in-the-loop' model. Your current selection poses severe compliance risks."
                st.warning(warning_msg)
            else:
                success_msg = "✅ **監督模式合規：** 針對高風險場景，已正確配置「人在環中」監督模式。" if is_zh else "✅ **Oversight Compliant:** 'Human-in-the-loop' is correctly configured for this high-risk scenario."
                st.success(success_msg)
        else:
            success_msg = f"🟢 **一般風險用例 (Minimal Risk Profile):**\n\n{reason_text}\n\n依據風險比例原則，可考慮採取「人在環外」完全自動化或「人為管控」模式，但需持續進行私隱影響評估。" if is_zh else f"🟢 **Minimal Risk Profile:**\n\n{reason_text}\n\n'Human-out-of-the-loop' or 'Human-in-command' may be considered, subject to continuous Privacy Impact Assessments."
            st.success(success_msg)

# ------------------------------------------
# Track C: Overall Scorecard (Executive Audit)
# ------------------------------------------
with tab_audit:
    if is_zh:
        st.markdown("### 📋 企業級全局合規自我審查 (Executive Audit Scorecard)")
        st.caption("基於 AIGP 部署監督理念：將 PCPD 四大部靜態指引轉化為可量化之核取清單。")
    else:
        st.markdown("### 📋 Enterprise Executive Audit Scorecard")
        st.caption("Aligned with AIGP Deployment Oversight: Quantifying the 4 Parts of the PCPD framework.")

    lang_key = "zh" if is_zh else "en"
    total_checks = 0
    passed_checks = 0

    # 動態生成 4 大部的 Expander 清單
    for ch_id, ch_data in PCPD_DB.items():
        data = ch_data[lang_key]
        with st.expander(f"✅ {data['title']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**📝 {'Statutory Requirement' if not is_zh else '法定核心'}:** {data['statute']}")
                st.markdown(f"**🚨 {'Risk Flag' if not is_zh else '違法紅線'}:** {data['red_flag']}")
                st.markdown(f"**🛡️ {'Board Advice' if not is_zh else '董事會治理建議'}:** {data['board_advice']}")
            
            with col2:
                st.markdown("**Checklist:**")
                c1 = st.checkbox(f"Policy Updated ({ch_id})", key=f"{ch_id}_c1")
                c2 = st.checkbox(f"Staff Trained ({ch_id})", key=f"{ch_id}_c2")
                c3 = st.checkbox(f"System Enforced ({ch_id})", key=f"{ch_id}_c3")
                
                total_checks += 3
                passed_checks += sum([c1, c2, c3])
                score = (sum([c1, c2, c3]) / 3) * 100
                st.metric("Section Score", f"{score:.0f}%")

    # Overall Compliance Score
    st.markdown("---")
    overall_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    st.subheader(f"📈 {'整體合規就緒度 / Overall Compliance Readiness'}: {overall_score:.1f}%")
    st.progress(overall_score / 100)
    
    if overall_score == 100:
        st.success("🌟 完美合規！已完全納入貫徹私隱設計（Privacy-by-Design）精神。" if is_zh else "🌟 Fully Compliant! Privacy-by-Design fully integrated.")
        st.balloons()
    elif overall_score >= 50:
        st.warning("⚠️ 已具備基礎防禦，但仍有治理死角，建議盡快補齊未勾選項目。" if is_zh else "⚠️ Foundation established, but governance blind spots remain. Complete unchecked items.")
    else:
        st.error("🚨 就緒度極低！缺乏核心防護，存在違反保障資料原則的重大合規風險。" if is_zh else "🚨 Extremely low readiness! Major compliance risks exist regarding Data Protection Principles.")
