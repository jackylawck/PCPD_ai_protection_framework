import streamlit as st

# ==========================================
# 1. 頁面配置與高管級 UI 設定
# ==========================================
st.set_page_config(
    page_title="PCPD AI Model Framework Auditor",
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

# 香港個人資料私隱專員公署 (PCPD) 官方中英文文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"
EN_PDF_URL = "https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf"

# Initialize Session State
if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "HR_Perf"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "HITL"
if 'chat_messages' not in st.session_state: st.session_state.chat_messages = []

is_zh = st.session_state.lang == '繁體中文'
PDF_URL = ZH_PDF_URL if is_zh else EN_PDF_URL

# ==========================================
# 2. 結構化風險字典矩陣 (雙語化 & PCPD 嚴格映射)
# ==========================================
RISK_MATRIX = {
    "HR_Perf": {
        "zh_label": "大型跨國企業 (HR 數位轉型 / 考績預測)", "en_label": "MNC (HR Digital Transformation / Performance Prediction)",
        "level": "HIGH", 
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12 明文規定，涉及「求職者評估、工作表現評核或終止僱傭合約」之場景，屬法定高風險用例。",
        "en_reason": "Per PCPD 2024 Model Framework (P.29, Fig 12), 'Assessment of job applicants, evaluation of job performance or termination of employment contracts' is a statutory High-Risk use case."
    },
    "Finance_Fraud": {
        "zh_label": "香港金融機構 (信貸評估 / 欺詐偵測)", "en_label": "HK Financial Institution (Credit Scoring / Fraud Detection)",
        "level": "HIGH", 
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12，涉及「評估個人的信用可靠程度以作出自動化財務決策」之場景，屬法定高風險用例。",
        "en_reason": "Per PCPD 2024 Model Framework (P.29, Fig 12), 'Evaluation of the creditworthiness of individuals for making automated financial decisions' is a statutory High-Risk use case."
    },
    "Med_Tech": {
        "zh_label": "醫療與健康科技 (AI 輔助影像分析)", "en_label": "HealthTech (AI-Assisted Medical Imaging Analytics)",
        "level": "HIGH", 
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12，涉及「AI 輔助醫學影像分析或治療」之場景，直接關乎人身安全，屬法定高風險用例。",
        "en_reason": "Per PCPD 2024 Model Framework (P.29, Fig 12), 'AI-assisted medical imaging analytics or therapies' is a statutory High-Risk use case."
    },
    "Retail_Bot": {
        "zh_label": "零售與電子商務 (AI 聊天推薦)", "en_label": "Retail & E-commerce (AI Chatbot Recommendations)",
        "level": "LOW", 
        "zh_reason": "依據 PCPD 2024《模範框架》第 20 頁第 24 條，用於推送個人化廣告或商品推薦，對持份者重大權益影響較低，屬一般/低風險用例。",
        "en_reason": "Per PCPD 2024 Model Framework (P.23, Para 24), systems used to present individuals with personalised advertisements pose a lower risk."
    }
}

OVERSIGHT_OPTIONS = {
    "HITL": {"zh": "人在環中 (Human-in-the-loop)", "en": "Human-in-the-loop (HITL)"},
    "HIC": {"zh": "人為管控 (Human-in-command)", "en": "Human-in-command (HIC)"},
    "HOOTL": {"zh": "人在環外 (Human-out-of-the-loop)", "en": "Human-out-of-the-loop (HOOTL)"}
}

# ==========================================
# 3. Sidebar UI (邊界鎖定、專業聯絡與免責聲明)
# ==========================================
with st.sidebar:
    st.markdown("## 🏛️ PCPD AI Auditor")
    
    st.header("🌐 UI Language / 介面語言")
    lang_choice = st.radio("Select Language / 選擇語言", ['繁體中文', 'English'], index=0 if st.session_state.lang == '繁體中文' else 1, label_visibility="collapsed")
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🏛️ 官方模範框架核對基準" if is_zh else "### 🏛️ Model Framework Baseline")
    st.markdown("**本系統核心指標 100% 依據香港個人資料私隱專員公署 (PCPD) 2024 年發布之《人工智能：個人資料保障模範框架》進行決定性邏輯編碼。**" if is_zh else "**This system's core metrics are 100% deterministically coded based on the PCPD's 2024 'Artificial Intelligence: Model Personal Data Protection Framework'.**")
    st.markdown("---")
    
    if is_zh:
        st.warning("⚠️ **嚴格邊界聲明**\n\n本系統為獨立開發之開源工具，**並非 PCPD 官方系統**。系統採嚴格邊界控制，**僅依據《模範框架》文本作答；對框架外之議題一律拒絕提供推測性建議**，以防範合規幻覺。")
    else:
        st.warning("⚠️ **Strict Boundary Disclaimer**\n\nThis is an independent open-source tool, **NOT an official PCPD system**. It operates under strict boundary controls, answering ONLY based on the Model Framework text. Queries outside this scope will be rejected to prevent compliance illusions.")

    # ------------------------------------------
    # 側邊欄底部：專業 LinkedIn 聯絡按鈕
    # ------------------------------------------
    st.markdown("---")
    st.markdown("### 👤 " + ("專業聯絡" if is_zh else "Contact Specialist"))
    
    linkedin_url = "https://www.linkedin.com/in/jackylawck"
    
    if is_zh:
        st.markdown("如有 AI 管治、合規審計或法規映射之專業探討，歡迎聯絡專案作者：")
        st.link_button("🌐 訪問作者 LinkedIn 檔案", linkedin_url, type="primary")
    else:
        st.markdown("For professional inquiries regarding AI governance, compliance auditing, or regulatory mapping, connect with the author:")
        st.link_button("🌐 Connect on LinkedIn", linkedin_url, type="primary")

# ==========================================
# 4. 智能語義路由 (Chatbot 藏拙與防禦邏輯)
# ==========================================
def get_pcpd_advice(query, is_zh):
    query = query.lower()
    advice = []
    
    # 擴充關鍵字白名單，確保涵蓋員工行為與實務數據操作
    keywords = [
        "策略", "管治", "風險", "監督", "採購", "第三方", "api", "披露", "透明度", "解釋", 
        "影子", "shadow", "跨境", "cross-border", "saas", "vendor", "hr", "招聘", "考績",
        "私自", "私下", "員工", "上傳", "名單", "客戶", "資料", "數據", "外洩", "安全", "pii",
        "解僱", "評核", "評充", "評估", "信貸", "醫療"
    ]
    
    if not any(w in query for w in keywords):
        advice.append({
            "title": "🛑 超出審查範圍 / 拒絕作答 (Out of Scope)",
            "content": "您的輸入情境未觸發 PCPD《模範框架》之核心規範。為堅守「100% 決定性合規」原則，**本系統寧可拒絕作答，也絕不提供《模範框架》文本以外的推測性建議**。請嘗試輸入與 AI 採購、資料保安、人為監督或持份者披露相關的具體場景。" if is_zh else "Query falls outside the PCPD Model Framework. To maintain 100% compliance accuracy, **this system refuses to generate speculative advice beyond the official text**. Please input scenarios related to AI procurement, data security, human oversight, or disclosure."
        })
        return advice

    # Shadow AI 違規操作
    if any(w in query for w in ["影子", "shadow", "私下", "私自", "員工自行", "繞過", "未授權", "偷偷", "unauthorized", "bypass", "上傳"]):
        advice.append({
            "title": "🚨 影子 AI 違規操作與資料保安危機 (Shadow AI Breach)" if is_zh else "🚨 Shadow AI Breach & Data Security Crisis",
            "content": "直接違反《私隱條例》保障資料第 4 原則（資料保安）。董事會必須立即啟動技術阻斷 (如部署 CASB) 並修訂《可接受使用政策》(AUP)，嚴禁將未經匿名化的 PII 輸入外部 AI 工具。" if is_zh else "Directly violates DPP 4 (Data Security). The Board must immediately deploy technical blocking (e.g., CASB) and update the Acceptable Use Policy (AUP) to strictly prohibit inputting unanonymised PII into external AI tools."
        })
    
    # TPRM 採購與第三方風險
    if any(w in query for w in ["第三方", "api", "廠商", "saas", "外購", "vendor", "third party", "procure"]):
        advice.append({
            "title": "⚙️ 採購 AI 方案的管治與第三方風險管理 (TPRM)" if is_zh else "⚙️ AI Procurement & Third-Party Risk Management (TPRM)",
            "content": "依據《模範框架》第 16 及 44 條，無法獲取底層細節時，管治核心全面轉向合約约束：簽署資料處理者協議 (DPA)、確立責任轉嫁及 AI 事故應變計劃 (Kill Switch)。" if is_zh else "Per Model Framework Para 16 & 44, when lacking underlying access, governance pivots to contractual protections: DPA, liability transfer, and AI Incident Response Plans (Kill Switch)."
        })
        
    # Cross-border 跨境資料流動
    if any(w in query for w in ["跨境", "歐盟", "eu", "中港", "海外", "cross-border", "transfer"]):
        advice.append({
            "title": "🔴 多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)" if is_zh else "🔴 Overlapping Jurisdictions & Cross-Border Risks",
            "content": "依據《模範框架》第 14 頁：將個人資料轉移予外地資料處理者，必須採用合約規範保障資料保安。若遇歐盟等法規，需簽發標準契約條款 (SCCs) 應對多法域衝突。" if is_zh else "Per Model Framework P.17: Cross-border data transfers to overseas processors require contractual safeguards. Standard Contractual Clauses (SCCs) may be needed for dual compliance."
        })
        
    # HR / High Risk 核心高風險應用
    if any(w in query for w in ["hr", "招聘", "考績", "解僱", "信貸", "醫療", "hire", "performance", "medical", "評估", "評核"]):
        advice.append({
            "title": "👥 高風險用例與人為監督 (High-Risk & Human Oversight)" if is_zh else "👥 High-Risk Use Case & Human Oversight",
            "content": "依據《模範框架》第 32 條，高風險 AI 系統應強制採取「人在環中」(Human-in-the-loop) 方式。完全自動化將導致違規的「合規幻覺」。同時需防範演算法間接歧視觸犯香港相關反歧視或僱傭條例。" if is_zh else "Per Model Framework Para 32, High-Risk AI must enforce a 'Human-in-the-loop' approach. Fully automated decisions risk severe compliance illusions and algorithmic bias, potentially violating employment ordinances."
        })

    # 若關鍵字通過但未觸發上述特定場景 (Fallback)
    if not advice:
        advice.append({
            "title": "🔍 系統就緒 (System Ready)",
            "content": "已接收您的關鍵字。請提供更具體的行為描述（例如：HR 篩選履歷、第三方 SaaS 採購、員工私自使用開源模型等），以便系統為您精準映射 PCPD 官方指引。" if is_zh else "Keywords received. Please describe a specific action (e.g., HR screening, SaaS procurement, unauthorized Shadow AI usage) for precise PCPD Model Framework mapping."
        })

    return advice

# ==========================================
# 5. 主畫面佈局
# ==========================================
st.title("🛡️ " + ("香港個人資料私隱專員公署 (PCPD) 模範框架審查系統" if is_zh else "PCPD AI Model Framework Auditor"))
st.markdown("### " + ("企業 AI 導入前置合規評分卡" if is_zh else "Enterprise AI Pre-Deployment Audit Scorecard"))

tab_chat, tab_audit = st.tabs([
    "💬 " + ("智能情境審查 (Smart Chatbox)" if is_zh else "Smart Context Chatbox"), 
    "📋 " + ("企業前置合規評分卡 (Compliance Scorecard)" if is_zh else "Pre-Deployment Compliance Scorecard")
])

# ------------------------------------------
# 軌道一：智能情境 Chatbox
# ------------------------------------------
with tab_chat:
    st.markdown("請描述您在企業中遇到的 AI 管治情境（例如：員工私自上傳客戶名單、採購海外 API 系統），系統將為您進行風險拆解：" if is_zh else "Describe your AI governance scenario (e.g., employee secretly uploading client list to an external AI), and the system will map the risks:")
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("請輸入企業情境..." if is_zh else "Enter enterprise scenario..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            advice_list = get_pcpd_advice(prompt, is_zh)
            response_text = ""
            for adv in advice_list:
                st.error(f"### {adv['title']}")
                st.info(f"**{'治理建議 (Governance Action):' if is_zh else 'Governance Action:'}** {adv['content']}")
                response_text += f"### {adv['title']}\n{adv['content']}\n\n"
            st.markdown(f"[🔗 {'查閱官方指引詳情' if is_zh else 'Read Official Framework'}]({PDF_URL})")
            
            st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

# ------------------------------------------
# 軌道二：企業 AI 導入前置合規評分卡
# ------------------------------------------
with tab_audit:
    with st.form("audit_form"):
        st.markdown("#### 📥 " + ("第一步：輸入企業場景脈絡 (Input Operational Context)" if is_zh else "Step 1: Input Operational Context"))
        col1, col2 = st.columns(2)
        with col1:
            company_input = st.selectbox(
                "選擇基礎企業用例 (Base Use Case)" if is_zh else "Select Base Use Case", 
                list(RISK_MATRIX.keys()), 
                format_func=lambda x: RISK_MATRIX[x]["zh_label"] if is_zh else RISK_MATRIX[x]["en_label"]
            )
        with col2:
            oversight_input = st.selectbox(
                "預期的人為監督模式 (Intended Human Oversight)" if is_zh else "Intended Human Oversight", 
                list(OVERSIGHT_OPTIONS.keys()),
                format_func=lambda x: OVERSIGHT_OPTIONS[x]["zh"] if is_zh else OVERSIGHT_OPTIONS[x]["en"]
            )
            
        ai_use_case = st.text_area(
            "請詳細描述您的 AI 應用場景（系統將自動智能偵測：影子 AI 違規操作、跨國多法域衝突、第三方 SaaS 採購或自研定製等複雜脈絡）" if is_zh else "Describe your AI use case in detail (System will auto-detect Shadow AI, cross-border data, TPRM, etc.):",
            placeholder="例如：總部在歐盟受 EU AI Act 監管，香港分公司向美國廠商採購生成式招聘系統..." if is_zh else "e.g., HQ governed by EU AI Act, HK branch procuring SaaS HR system..."
        )
        
        if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍" if is_zh else "Execute PCPD Deep Audit 🔍"):
            st.session_state.audit_performed = True
            st.session_state.company_context = company_input
            st.session_state.human_oversight_pref = oversight_input
            st.session_state.case_description = ai_use_case

    if st.session_state.audit_performed:
        st.markdown("---")
        st.markdown("### 📋 " + ("第二步：依據 PCPD 2024《模範框架》產出之高管稽核報告" if is_zh else "Step 2: Board-Level Audit Report per PCPD 2024 Framework"))
        
        ctx_text = st.session_state.case_description.lower()
        base_risk = RISK_MATRIX[st.session_state.company_context]
        current_oversight = st.session_state.human_oversight_pref
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "📊 " + ("第一、二部：管治與風險監督" if is_zh else "Parts I & II: Gov. & Risk Oversight"), 
            "⚙️ " + ("第三部：模型定製與第三方風險管理 (TPRM)" if is_zh else "Part III: Customisation & TPRM"), 
            "📢 " + ("第四部：持份者溝通與透明度要求" if is_zh else "Part IV: Stakeholder Comms")
        ])
        
        with sub_tab1:
            st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督" if is_zh else "Part I: Strategy & Part II: Risk Assessment")
            st.info(f"**【{'基準風險判定' if is_zh else 'Baseline Risk Assessment'}】** {base_risk['zh_reason'] if is_zh else base_risk['en_reason']}")
            
            if "HR" in st.session_state.company_context:
                st.warning("⚠️ **跨法規聯動警告 (Employment Ordinance Cross-Compliance)：**\n\n在高度自動化的 HR 績效與解僱決策中，極易引入**演算法偏見（Algorithmic Bias）與間接歧視**。這不僅違反公平原則，更可能觸犯香港《僱傭條例》下的不當解僱。" if is_zh else "⚠️ **Employment Ordinance Cross-Compliance:** Highly automated HR decisions can introduce Algorithmic Bias, risking unfair dismissal claims under the HK Employment Ordinance.")

            has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "中港", "轉移", "外地", "美國", "司法管轄", "jurisdiction", "eu ai act", "歐盟"])
            if has_cross_border:
                st.error("🔴 **深度審計：偵測到多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**" if is_zh else "🔴 **Deep Audit: Overlapping Jurisdictions & Cross-Border Data Transfer Risk Detected**")
                st.markdown(
                    f"- **《私隱條例》保障資料第 4(2) 原則與跨境規範（《模範框架》第 14 頁）：** 必須採用**合約規範或其他方法**保障資料保安。\n- **跨國管轄權衝突：** 董事會應指示簽發標準契約條款（SCCs）以應對多法域重疊監管。"
                    if is_zh else
                    "- **DPP 4(2) & Cross-Border Rules (Model Framework P.17):** Must adopt contractual means to protect data security.\n- **Jurisdictional Conflict:** Board must instruct Legal to issue SCCs."
                )
            
            st.markdown("##### 👥 " + ("人為監督模式（Human Oversight）合規審查" if is_zh else "Human Oversight Compliance Check"))
            is_text_automated = any(w in ctx_text for w in ["完全自動化", "直接執行", "fully automated", "自動解僱", "直接生成建議", "照單全收"])
            
            if base_risk["level"] == "HIGH":
                if is_text_automated and current_oversight == "HITL":
                    st.error("🚨 **管治邏輯嚴重衝突 (Control Design Failure)：** 表單選擇「人在環中」，但描述為「完全自動化」。實質已降級為違規的「人在環外」。確保人類具備實質最終裁量權。" if is_zh else "🚨 **Control Design Failure:** Selected 'Human-in-the-loop' but described 'fully automated' processes. Redesign workflows to ensure final human discretion.")
                elif current_oversight != "HITL":
                    st.warning("⚠️ **管治衝突警告：** 依據 PCPD 2024《模範框架》第二部第 32(i) 條，高風險 AI 系統**應強制採取「人在環中」(Human-in-the-loop)** 方式。" if is_zh else "⚠️ **Governance Misalignment:** Per PCPD Model Framework Para 32(i), high-risk systems **must adopt a 'Human-in-the-loop' approach**.")
                else:
                    st.success("✅ **人為監督配置合規：** 系統與表單描述一致，符合 PCPD 2024《模範框架》第 32 條規範。" if is_zh else "✅ **Oversight Compliant:** Fully compliant with PCPD 2024 Model Framework Para 32.")

        with sub_tab2:
            st.subheader("第三部：AI 模型的定製與系統管理" if is_zh else "Part III: Customisation & System Management")
            
            is_shadow_ai = any(w in ctx_text for w in ["影子", "shadow", "私下", "員工自行", "繞過", "未授權", "未經批准", "偷偷", "本地工作站", "unauthorized", "bypass"])
            is_third_party = any(w in ctx_text for w in ["第三方", "third party", "third-party", "api", "黑箱", "black box", "採購", "procure", "saas", "廠商", "vendor"])
            
            if is_shadow_ai:
                st.error("🚨 **重大合規危機：偵測到「影子 AI (Shadow AI)」違規操作！**" if is_zh else "🚨 **Critical Breach: 'Shadow AI' Unauthorized Operation Detected!**")
                sh1 = st.checkbox("【技術阻斷與可觀測性】IT 部門已部署 CASB 或端點防護，阻擋未經授權的 API 呼叫。" if is_zh else "[Visibility & Blocking] IT deployed CASB/endpoint protection to block unauthorized API calls.")
                sh2 = st.checkbox("【修訂 AUP 政策】嚴禁將 PII 輸入未經審批的外部 AI 工具。" if is_zh else "[Revise AUP] Strictly prohibit inputting PII into unapproved AI tools.")
                sh3 = st.checkbox("【建立認可清單】提供承諾零數據留存的內部安全 AI 替代方案。" if is_zh else "[Whitelisting] Provided approved, zero-data-retention AI alternatives.")
                st.progress((sum([sh1, sh2, sh3]) / 3))
                
            elif is_third_party:
                st.warning("🚨 **核心治理分支切換：第三方 SaaS / 廠商 API 採購軌道 (TPRM Route Active)**" if is_zh else "🚨 **Governance Branch: Third-Party SaaS / Vendor API Track (TPRM Route Active)**")
                tp1 = st.checkbox("【資料處理者協議 DPA】明文禁止廠商將 PII 用作其模型二次訓練（符合《模範框架》第 16 及 44 條）。" if is_zh else "[Data Processor DPA] Signed formal DPA strictly prohibiting vendors from using PII for secondary model training.")
                tp2 = st.checkbox("【合約責任轉嫁】明訂當廠商系統產生不當偏見或資料外洩時的法律責任歸屬（符合《模範框架》第 18 條）。" if is_zh else "[Liability Transfer] Contract clearly dictates liability for bias or data breaches (Para 18).")
                tp3 = st.checkbox("【AI 事故暫停機制】具備一鍵「暫停」系統連線能力與事故應變計劃（符合《模範框架》第 46 及 49 條） 。" if is_zh else "[AI Incident Kill Switch] AI Incident Response Plan established with capabilities to 'pause' system connections.")
                st.progress((sum([tp1, tp2, tp3]) / 3))
                
            else:
                st.success("🛠️ **核心治理分支切換：自主研發與定製實施軌道 (In-House Development Route Active)**" if is_zh else "🛠️ **Governance Branch: In-House Development Track Active**")
                st.markdown("**請勾選已落實之開發期控制措施（依據 PCPD 2024《模範框架》第三部「數據準備與定製實施」）：**" if is_zh else "**Please check implemented development controls (per PCPD 2024 Model Framework Part III):**")
                in1 = st.checkbox("【資料最少化】移除或假名化無關之敏感特徵（符合《模範框架》第 41(ii) 條規範）。" if is_zh else "[Data Minimisation] Removed or pseudonymised irrelevant sensitive features from fine-tuning datasets.")
                in2 = st.checkbox("【私隱增強技術】評估或採用差分私隱、合成數據等 PETs 技術。" if is_zh else "[PETs] Evaluated/adopted Privacy Enhancing Technologies (e.g., differential privacy).")
                in3 = st.checkbox("【防範模型漂移與投毒】建立內部日誌監控與紅隊演練，防止模型表現衰退或遭對抗式攻擊（符合《模範框架》第 46(i) 與 48(v) 條規範）。" if is_zh else "[Security & Drift Prevention] Establish red teaming against adversarial attacks and monitor to prevent 'Model Drift' over time (Para 46 & 48).")
                st.progress((sum([in1, in2, in3]) / 3))

        with sub_tab3:
            st.subheader("第四部：與持份者的溝通及交流" if is_zh else "Part IV: Communication and Engagement with Stakeholders")
            st.markdown("- **顯著披露 (Prominent Disclosure)：** 向受影響群體清楚且顯著地披露 AI 系統的使用情況與介入程度（符合《模範框架》第 53 條）。" if is_zh else "- **Prominent Disclosure:** Clearly disclose the use and level of AI involvement to affected groups (Para 53).")
            st.markdown("- **全局與局部可解釋性 (Global & Local Explainability)：** 若決策對個人產生重大影響，機構**必須提供人為介入的選項**，容許當事人尋求解釋並要求合規人員重新審視（符合《模範框架》第 56 與 58 條）。" if is_zh else "- **Explainability & Redress:** Provide human intervention options for feedback, explanation, and human review (Para 56 & 58).")
            st.markdown("- **淺白語言 (Plain Language)：** 所有私隱政策與通知應使用淺白的語言，並設法讓持份者知悉（符合《模範框架》第 60 條）。" if is_zh else "- **Plain Language:** All privacy policies/notices must be expressed in plain, clear, and understandable language (Para 60).")
