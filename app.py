import streamlit as st

# ==========================================
# 1. 頁面配置與高管級 UI 設定
# ==========================================
st.set_page_config(
    page_title="AIGP & PCPD Intelligence Workspace",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stCheckbox > label {font-weight: 500;}
    .stRadio > label {font-weight: bold; color: #2E4053;}
    </style>
""", unsafe_allow_html=True)

ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"

# ==========================================
# 2. 狀態保存機制 (Session State 初始化)
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
is_zh = st.session_state.lang == '繁體中文'

# 評分卡狀態
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "HR_Perf"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "HITL"

# 模擬考場狀態
if "quiz_index" not in st.session_state: st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state: st.session_state.quiz_answered = False
if "user_choice" not in st.session_state: st.session_state.user_choice = None
if "weak_domains" not in st.session_state: st.session_state.weak_domains = set()

# ==========================================
# 3. AIGP 模擬考題庫 (Scenario-based MCQs)
# ==========================================
QUIZ_BANK = [
    {
        "domain": "Domain III: Governing AI Development & Domain IV: Deployment Oversight",
        "topic": "影子 AI (Shadow AI) 與資料保安",
        "scenario": "某跨國企業的香港行銷團隊為了趕工，私下繞過 IT 部門，將包含客戶個人識別資料 (PII) 的檔案上傳至一個未經授權的免費開源 GenAI 模型中生成企劃案。作為 AI 治理專員，您應向董事會建議的最優先處置為何？",
        "options": [
            "A. 立即要求內部工程師對該開源模型進行微調 (Fine-tuning)，以確保其符合公司風格。",
            "B. 部署雲端存取安全代理 (CASB) 進行技術阻斷，並立即修訂《可接受使用政策》(AUP) 嚴禁此行為。",
            "C. 要求行銷團隊在企劃案上加註「本內容由 AI 生成」的顯著披露聲明。",
            "D. 進行數據假名化 (Pseudonymisation)，然後允許團隊繼續使用該開源模型。"
        ],
        "answer": "B. 部署雲端存取安全代理 (CASB) 進行技術阻斷，並立即修訂《可接受使用政策》(AUP) 嚴禁此行為。",
        "explanation": """
        **✅ 正確選項 (B) 解析：**
        影子 AI (Shadow AI) 構成極高的資料外洩風險，直接違反 PCPD 保障資料第 4 原則（資料保安）。最關鍵的第一步是**技術阻斷 (Visibility & Blocking)** 與 **政策修訂 (Policy Control)**，徹底切斷未授權的數據流出。

        **❌ 錯誤選項解析：**
        - **(A) 錯誤：** 企業根本無法對外部未授權的免費模型進行微調。這是典型的「將自研框架錯用於未授權外購/開源工具」的合規幻覺。
        - **(C) 錯誤：** 顯著披露 (透明度) 是部署階段對消費者的義務，無法解決前端員工私自外洩 PII 的根本保安問題。
        - **(D) 錯誤：** 雖然假名化是良好的 PETs 技術，但治標不治本。未經授權的工具本身就不應處於企業的 IT 環境中，應優先實施白名單 (Whitelisting) 管理。
        """
    },
    {
        "domain": "Domain II: Laws & Frameworks & Domain I: Foundations",
        "topic": "第三方風險管理 (TPRM) 與黑箱系統",
        "scenario": "企業向美國供應商採購了一套完全封閉的「黑箱 (Black-box)」SaaS AI 招聘篩選系統。合規團隊無法獲取其底層演算法權重。依據 PCPD《模範框架》，企業應如何防範 AI 偏見與隱私風險？",
        "options": [
            "A. 要求內部資料科學家對該系統進行反向工程 (Reverse Engineering) 以確保局部可解釋性。",
            "B. 全面信任供應商的安全聲明，因為責任完全在開發者 (Developer) 身上，部署者 (Deployer) 無需負責。",
            "C. 透過簽署資料處理者協議 (DPA) 嚴禁 PII 用於二次訓練，並在合約中確立責任轉嫁與暫停連線機制。",
            "D. 強制所有求職者簽署免責聲明，承諾不對 AI 篩選結果提出異議。"
        ],
        "answer": "C. 透過簽署資料處理者協議 (DPA) 嚴禁 PII 用於二次訓練，並在合約中確立責任轉嫁與暫停連線機制。",
        "explanation": """
        **✅ 正確選項 (C) 解析：**
        面對無法獲取底層細節的現成 SaaS，企業 (Deployer) 的管治核心必須轉向 **第三方風險管理 (TPRM) 與合約約束 (Contractual Protections)**。禁止二次訓練與確立 AI 事故應變計劃 (Kill Switch) 是 PCPD 第 16 及 44 條的核心要求。

        **❌ 錯誤選項解析：**
        - **(A) 錯誤：** 商業上不切實際且可能違反 SaaS 的服務條款 (Terms of Service) 與智慧財產權。
        - **(B) 錯誤：** 嚴重錯誤。依據 PCPD 與全球法規，企業作為「資料使用者 / 部署者」，必須對處理其客戶/員工資料的 AI 系統承擔最終問責 (Accountability)。
        - **(D) 錯誤：** 剝奪資料當事人要求人工介入與合理解釋的權利，直接違反 PCPD 第 56 條的救濟機制要求。
        """
    },
    {
        "domain": "Domain IV: Governing AI Deployment and Use",
        "topic": "多法域衝突與人在環中 (HITL)",
        "scenario": "一家總部位於歐盟的跨國銀行，指示其香港分行導入一套「完全自動化」的 AI 績效評估系統，直接依據數據生成解僱名單交由 HR 執行。此舉面臨的最大管治衝突為何？",
        "options": [
            "A. 違反《歐盟 AI 法案》的透明度要求，因為沒有向客戶說明使用了 AI。",
            "B. 違反 PCPD 對於高風險系統應採取「人在環中 (HITL)」的規範，HR 淪為橡皮圖章，剝奪了實質裁量權。",
            "C. 沒有衝突。只要歐盟總部批准，香港分行即可直接豁免本地法規。",
            "D. 演算法可能會因為計算速度過快，導致模型漂移 (Model Drift)。"
        ],
        "answer": "B. 違反 PCPD 對於高風險系統應採取「人在環中 (HITL)」的規範，HR 淪為橡皮圖章，剝奪了實質裁量權。",
        "explanation": """
        **✅ 正確選項 (B) 解析：**
        解僱決策屬於典型的「高風險 (High-Risk)」用例。若 AI 直接生成名單而 HR 僅照單全收（完全自動化 / 人在環外），這構成了極度危險的**合規幻覺 (Compliance Illusion)**。依據 PCPD 第 32 條，人類必須保留最終的控制權與實質裁量權 (HITL)。

        **❌ 錯誤選項解析：**
        - **(A) 錯誤：** 績效評估影響的是「內部員工」而非外部客戶，且此處的致命傷是決策監督機制的缺失，而非僅僅是透明度披露。
        - **(C) 錯誤：** 跨國企業必須處理**多法域重疊管轄 (Overlapping Jurisdictions)**，必須同時符合 EU AI Act 與香港本地的 PDPO 及僱傭條例。
        - **(D) 錯誤：** 模型漂移 (Model Drift) 發生於數據分佈隨時間改變而導致準確率下降，與「完全自動化」的管治流程缺失無直接因果關聯。
        """
    }
]

# ==========================================
# 4. 結構化風險字典與選項庫
# ==========================================
RISK_MATRIX = {
    "HR_Perf": {"label": "大型跨國企業 (HR 數位轉型 / 考績預測)", "level": "HIGH", "reason": "依據 PCPD《模範框架》圖 12，涉及「工作表現評核或終止僱傭合約」屬法定高風險用例。"},
    "Finance_Fraud": {"label": "香港金融機構 (信貸評估 / 欺詐偵測)", "level": "HIGH", "reason": "涉及評估個人的信用可靠程度以作出自動化財務決策，屬法定高風險用例。"},
    "Med_Tech": {"label": "醫療與健康科技 (AI 輔助影像分析)", "level": "HIGH", "reason": "涉及 AI 輔助醫學影像分析或治療，直接關乎人身安全，屬法定高風險用例。"},
    "Retail_Bot": {"label": "零售與電子商務 (AI 聊天推薦)", "level": "LOW", "reason": "用於推送個人化廣告，對持份者重大權益影響較低，屬一般/低風險用例。"}
}
OVERSIGHT_OPTIONS = {
    "HITL": "人在環中 (Human-in-the-loop)",
    "HIC": "人為管控 (Human-in-command)",
    "HOOTL": "人在環外 (Human-out-of-the-loop)"
}

# ==========================================
# 5. Sidebar UI
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("AIGP & PCPD Auditor")
    st.markdown("---")
    st.markdown("### 🏛️ 專業管治雙引擎")
    st.caption("🎓 **AIGP 模擬考場:** 高管情境式決策演練")
    st.caption("📋 **PCPD 評分卡:** 企業合規落地稽核工具")
    st.markdown("---")
    st.warning("⚠️ **開源公共利益沙盒：** 純決定性代碼架構，100% 無 AI 幻覺，數據關閉即銷毀。")

# ==========================================
# 6. 核心雙軌架構 (Tabs)
# ==========================================
st.title("🛡️ AIGP 企業 AI 管治實戰工作站")
st.markdown("### IAPP AIGP (v2.1) & PCPD 2024 Model Framework Station")

tab_quiz, tab_audit = st.tabs([
    "🎓 AIGP 模擬考場與場景診斷 (Scenario Q&A)", 
    "📋 企業 AI 導入前置合規評分卡 (Self-Audit Scorecard)"
])

# ------------------------------------------
# 軌道一：AIGP 模擬考場 (單題場景問答)
# ------------------------------------------
with tab_quiz:
    st.subheader("💡 AIGP 實戰情境診斷 (Board-level Scenario Drills)")
    st.markdown("本區專為 AI 治理專業人員設計，透過真實企業挑戰，精準診斷您在 AIGP 四大領域的決策能力。")
    st.markdown("---")

    if st.session_state.quiz_index < len(QUIZ_BANK):
        q = QUIZ_BANK[st.session_state.quiz_index]
        
        st.info(f"**📍 考察領域：** {q['domain']}\n\n**📌 核心議題：** {q['topic']}")
        st.markdown(f"#### 📖 情境 (Scenario)：\n{q['scenario']}")
        
        # 答題表單
        with st.form(key=f"quiz_form_{st.session_state.quiz_index}"):
            choice = st.radio("請選擇最佳的治理處置方式：", q['options'], index=None)
            submit_ans = st.form_submit_button("送出診斷 🔍")
            
            if submit_ans and choice:
                st.session_state.user_choice = choice
                st.session_state.quiz_answered = True
                
                # 記錄分數與弱點
                if choice == q['answer']:
                    st.session_state.quiz_score += 1
                else:
                    st.session_state.weak_domains.add(q['domain'])
                st.rerun()

        # 顯示解答與解析
        if st.session_state.quiz_answered:
            if st.session_state.user_choice == q['answer']:
                st.success("🎯 **診斷正確！ (Correct)**")
            else:
                st.error("⚠️ **診斷失誤 (Incorrect)。這可能導致重大的合規漏洞。**")
            
            st.markdown(f"**正確解答：** {q['answer']}")
            st.markdown(q['explanation'])
            
            if st.button("下一題 (Next Question) ➡️"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.user_choice = None
                st.rerun()

    else:
        # 測驗完成結果報告
        st.balloons()
        st.success(f"🏆 **AIGP 場景診斷完成！您的總得分為：{st.session_state.quiz_score} / {len(QUIZ_BANK)}**")
        
        if st.session_state.weak_domains:
            st.warning("📊 **診斷報告：您在以下治理領域存在弱點，建議加強複習：**")
            for w in st.session_state.weak_domains:
                st.markdown(f"- {w}")
        else:
            st.info("📊 **診斷報告：表現優異！您已展現出堅實的 AIGP 高管決策視野。**")
            
        if st.button("🔄 重新啟動模擬考場 (Restart)"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.weak_domains = set()
            st.session_state.quiz_answered = False
            st.rerun()

# ------------------------------------------
# 軌道二：企業 AI 導入前置合規評分卡
# ------------------------------------------
with tab_audit:
    with st.form("audit_form"):
        st.markdown("#### 📥 第一步：輸入企業場景脈絡 (Input Operational Context)")
        col1, col2 = st.columns(2)
        with col1:
            company_input = st.selectbox("選擇基礎企業用例 (Base Use Case)", list(RISK_MATRIX.keys()), format_func=lambda x: RISK_MATRIX[x]["label"])
        with col2:
            oversight_input = st.selectbox("預期的人為監督模式 (Intended Human Oversight)", list(OVERSIGHT_OPTIONS.keys()), format_func=lambda x: OVERSIGHT_OPTIONS[x])
            
        ai_use_case = st.text_area(
            "請詳細描述您的 AI 應用場景（系統將自動智能偵測：影子 AI、跨國多法域、TPRM 黑箱採購等複雜脈絡）",
            placeholder="例如：總部在歐盟受 EU AI Act 監管，香港分公司向美國廠商採購生成式招聘系統..."
        )
        
        if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍"):
            st.session_state.audit_performed = True
            st.session_state.company_context = company_input
            st.session_state.human_oversight_pref = oversight_input
            st.session_state.case_description = ai_use_case

    if st.session_state.audit_performed:
        st.markdown("---")
        st.markdown("### 📋 第二步：高管稽核報告 (Board-Level Audit Report)")
        
        ctx_text = st.session_state.case_description.lower()
        base_risk = RISK_MATRIX[st.session_state.company_context]
        current_oversight = st.session_state.human_oversight_pref
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 第一、二部：管治與風險監督", "⚙️ 第三部：模型定製與 TPRM", "📢 第四部：持份者透明度"])
        
        with sub_tab1:
            st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督")
            st.info(f"**【基準風險判定】** {base_risk['reason']}")
            
            if "HR" in st.session_state.company_context:
                st.warning("⚠️ **跨法規聯動警告 (Employment Ordinance Cross-Compliance)：**\n在高度自動化的 HR 決策中，極易引入**演算法偏見與間接歧視**，可能觸犯香港《僱傭條例》下的不當解僱。")

            has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "轉移", "美國", "司法管轄", "eu ai act", "歐盟"])
            if has_cross_border:
                st.error("🔴 **深度審計：多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**\n- 需採用**合約規範**保障跨境資料保安（PCPD 第 14 頁）。\n- 需簽發標準契約條款（SCCs）以應對多法域衝突。")
            
            st.markdown("##### 👥 人為監督模式（Human Oversight）審查")
            is_text_automated = any(w in ctx_text for w in ["完全自動化", "直接執行", "fully automated", "自動解僱", "照單全收"])
            
            if base_risk["level"] == "HIGH":
                if is_text_automated and current_oversight == "HITL":
                    st.error("🚨 **管治邏輯嚴重衝突 (Control Design Failure)：**\n表單選擇「人在環中」，但描述為「完全自動化」。若 HR 僅作橡皮圖章，實質為違規的「人在環外」。強烈建議重新檢視流程。")
                elif current_oversight != "HITL":
                    st.warning("⚠️ **管治衝突警告：** 高風險 AI 系統**應強制採取「人在環中」(HITL)** 方式（PCPD 第 32(i) 條）。")
                else:
                    st.success("✅ **人為監督配置合規：** 符合 PCPD 第 32 條規範。")

        with sub_tab2:
            st.subheader("第三部：AI 模型的定製與AI系統的實施及管理")
            is_shadow_ai = any(w in ctx_text for w in ["影子", "shadow", "私下", "員工自行", "繞過", "未經批准", "偷偷"])
            is_third_party = any(w in ctx_text for w in ["第三方", "third party", "api", "黑箱", "採購", "saas", "廠商"])
            
            if is_shadow_ai:
                st.error("🚨 **重大合規危機：偵測到「影子 AI (Shadow AI)」違規操作！**")
                st.markdown("常規打分全面失效，必須立即啟動阻斷機制：")
                sh1 = st.checkbox("【技術阻斷】部署 CASB 或端點防護，阻擋未授權模型呼叫。")
                sh2 = st.checkbox("【修訂 AUP】嚴禁將 PII 輸入未經審批的外部 AI。")
                sh3 = st.checkbox("【建立白名單】為員工提供安全 AI 替代方案。")
                st.progress((sum([sh1, sh2, sh3]) / 3))
                
            elif is_third_party:
                st.warning("🚨 **核心分支切換：外購 SaaS / 廠商 API 採購軌道 (TPRM Route Active)**")
                st.markdown("由於無法獲取底層細節，管治核心全面轉向 **合約約束** 與 **第三方風險管理**：")
                tp1 = st.checkbox("【DPA 合約保障】明文禁止廠商將 PII 用作二次訓練（PCPD 第 16/44 條）。")
                tp2 = st.checkbox("【責任轉嫁】明訂資料外洩時的法律責任與罰則（PCPD 第 18 條）。")
                tp3 = st.checkbox("【事故暫停機制】具備一鍵停止系統連線能力（PCPD 第 46/49 條）。")
                st.progress((sum([tp1, tp2, tp3]) / 3))
                
            else:
                st.success("🛠️ **核心分支切換：自主研發與定製軌道 (In-House Route Active)**")
                in1 = st.checkbox("【資料最少化】移除或假名化微調數據中無關之敏感特徵（PCPD 第 41 條）。")
                in2 = st.checkbox("【私隱增強技術】評估或採用差分私隱等 PETs 技術（PCPD 第 41 條）。")
                in3 = st.checkbox("【防範模型漂移】建立日誌監控，防止模型隨時間衰退（PCPD 第 48 條）。")
                st.progress((sum([in1, in2, in3]) / 3))

        with sub_tab3:
            st.subheader("第四部：與持份者的溝通及交流")
            st.markdown("- **顯著披露 (Prominent Disclosure)：** 清楚披露 AI 系統的介入程度（PCPD 第 53(i) 條）。")
            st.markdown("- **局部可解釋性與救濟途徑 (Redress Mechanism)：** 若決策對個人產生重大影響，必須提供人為介入選項，容許當事人尋求解釋並要求重新審視（PCPD 第 56/58 條）。")
            st.markdown("- **淺白語言 (Plain Language)：** 私隱政策與通知應使用淺白方式表達（PCPD 第 60 條）。")
