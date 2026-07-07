import streamlit as st

# ==========================================
# 1. 頁面配置與 UI 設定
# ==========================================
st.set_page_config(
    page_title="PCPD AI Model Framework Compliance Station",
    page_icon="🛡️",
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

# 香港個人資料私隱專員公署 (PCPD) 官方文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"

# ==========================================
# 2. 狀態保存機制 (Session State 初始化)
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
is_zh = st.session_state.lang == '繁體中文'

if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "HR_Perf"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "HITL"

if "quiz_index" not in st.session_state: st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state: st.session_state.quiz_answered = False
if "user_choice" not in st.session_state: st.session_state.user_choice = None
if "weak_domains" not in st.session_state: st.session_state.weak_domains = set()

# ==========================================
# 3. PCPD 官方指引情境測驗庫
# ==========================================
QUIZ_BANK = [
    {
        "domain": "第一部：AI 策略及管治",
        "topic": "採購 AI 方案的管治考慮（第 16 條）",
        "scenario": "企業計劃向第三方供應商採購現成的 AI 雲端方案處理客戶個人資料。由於模型在供應商的雲端平台上運作，企業無法干預其底層演算法。依據 PCPD《模範框架》，企業最關鍵的管治措施為何？",
        "options": [
            "A. 要求內部工程師對該雲端模型進行逆向工程，以測試其安全性。",
            "B. 簽署資料處理者協議，明訂隱私與保安責任，並禁止供應商將資料用於其自身目的（如二次訓練模型）。",
            "C. 要求客戶簽署免責聲明，企業不對第三方供應商造成的資料外洩負責。",
            "D. 直接採取「人在環外」的完全自動化模式，以節省人為監督成本。"
        ],
        "answer": "B. 簽署資料處理者協議，明訂隱私與保安責任，並禁止供應商將資料用於其自身目的（如二次訓練模型）。",
        "explanation": """
        **✅ 正確選項 (B) 解析：**
        依據 PCPD《模範框架》第 16(v) 條，如機構採購 AI 方案涉及聘用資料處理者（例如在雲端平台上運作），必須簽署資料處理者協議，防範資料被未獲准許使用。

        **❌ 錯誤選項解析：**
        - (A) 違反採購實務，且無助於資料保護。
        - (C) 違反《私隱條例》，機構作為「資料使用者」對資料的處理承擔最終責任。
        - (D) 忽視風險評估，且與採購管治無關。
        """
    },
    {
        "domain": "第二部：風險評估及人為監督",
        "topic": "決定人為監督的程度（第 32 條）",
        "scenario": "醫院計劃導入一套 AI 輔助醫學影像分析系統。此系統的輸出結果會直接影響病患的診斷與治療方案。依據 PCPD《模範框架》，此系統應採取何種人為監督模式？",
        "options": [
            "A. 人在環外 (Human-out-of-the-loop)，以達到完全自動化的最高效率。",
            "B. 人為管控 (Human-in-command)，由人類事後隨機抽查即可。",
            "C. 人在環中 (Human-in-the-loop)，人類決策者在決策過程中保留著控制權，以防止及減低 AI 出錯。",
            "D. 無需人為監督，因醫療 AI 模型的準確率通常高於人類。"
        ],
        "answer": "C. 人在環中 (Human-in-the-loop)，人類決策者在決策過程中保留著控制權，以防止及減低 AI 出錯。",
        "explanation": """
        **✅ 正確選項 (C) 解析：**
        依據 PCPD《模範框架》圖 12，AI 輔助醫學影像分析屬高風險應用。第 32(i) 條明文規定：「高風險的 AI 系統應採取『人在環中』方式進行人為監督。人類決策者在決策過程中保留著控制權」。

        **❌ 錯誤選項解析：**
        - (A) 與 (B) 僅適用於風險最小或較低的 AI 系統（第 32(ii) 及 (iii) 條）。
        - (D) 完全違反指引中「人為監督」的 AI 道德原則。
        """
    },
    {
        "domain": "第四部：與持份者的溝通及交流",
        "topic": "資料當事人的權利及反饋（第 56 條）",
        "scenario": "某企業使用 AI 系統自動篩選求職者履歷。一名被 AI 淘汰的求職者對結果表示不滿。為符合 PCPD《模範框架》的建議，企業應該怎麼做？",
        "options": [
            "A. 拒絕回應，因為 AI 的演算法是商業機密。",
            "B. 提供途徑讓求職者作出反饋、尋求解釋，並容許其要求人為重新介入審視。",
            "C. 告知求職者 AI 絕對客觀，結果無法更改。",
            "D. 僅提供系統生成的標準拒絕信，不提供任何人為介入選項。"
        ],
        "answer": "B. 提供途徑讓求職者作出反饋、尋求解釋，並容許其要求人為重新介入審視。",
        "explanation": """
        **✅ 正確選項 (B) 解析：**
        依據 PCPD《模範框架》第 56 條規定：「如 AI 系統的決策/輸出結果可能對個人造成重大影響，機構應盡可能向個人提供途徑，讓他們作出反饋、尋求解釋及/或要求人為介入」。

        **❌ 錯誤選項解析：**
        - (A)、(C) 及 (D) 均剝奪了資料當事人尋求解釋與要求人為介入的權利，違反了透明度與可解釋性原則。
        """
    }
]

# ==========================================
# 4. 結構化風險字典與選項庫 (嚴格依據 PCPD 框架)
# ==========================================
RISK_MATRIX = {
    "HR_Perf": {"label": "工作表現評核或終止僱傭合約", "level": "HIGH", "reason": "依據 PCPD《模範框架》圖 12，涉及「工作表現評核或終止僱傭合約」屬高風險用例。"},
    "Finance_Fraud": {"label": "自動化財務決策 (如信貸評估)", "level": "HIGH", "reason": "依據 PCPD《模範框架》圖 12，涉及「評估個人的信用可靠程度以作出自動化財務決策」，屬高風險用例。"},
    "Med_Tech": {"label": "AI 輔助醫學影像分析或治療", "level": "HIGH", "reason": "依據 PCPD《模範框架》圖 12，直接關乎人身安全，屬高風險用例。"},
    "Retail_Bot": {"label": "個人化廣告或商品推薦", "level": "LOW", "reason": "依據 PCPD《模範框架》第 24 條，用於推送廣告，對個人造成重大影響的可能性較低，屬低風險用例。"}
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
    st.title("PCPD 模範框架智庫")
    st.markdown("---")
    st.markdown("### 🏛️ 官方指引雙引擎")
    st.caption("📖 **情境測驗:** 依據官方指引之決策演練")
    st.caption("📋 **評分卡:** 企業前置合規稽核工具")
    st.markdown("---")
    st.warning("⚠️ **免責聲明：** 本系統為獨立開發之純決定性代碼工具，內容 100% 取自香港私隱專員公署 2024 年發布之《人工智能：個人資料保障模範框架》，並非官方系統。")

# ==========================================
# 6. 核心雙軌架構 (Tabs)
# ==========================================
st.title("🛡️ 香港私隱專員公署 (PCPD) 模範框架實戰工作站")
st.markdown("### 《人工智能：個人資料保障模範框架》動態合規工具")

tab_quiz, tab_audit = st.tabs([
    "📖 模範框架情境測驗 (Scenario Q&A)", 
    "📋 企業 AI 導入前置合規評分卡 (Compliance Scorecard)"
])

# ------------------------------------------
# 軌道一：PCPD 模擬考場
# ------------------------------------------
with tab_quiz:
    st.subheader("💡 官方指引情境診斷")
    st.markdown("本區題目與解析 **100% 嚴格依據 PCPD《模範框架》** 原文編寫，協助檢視您對官方指引的熟悉度。")
    st.markdown("---")

    if st.session_state.quiz_index < len(QUIZ_BANK):
        q = QUIZ_BANK[st.session_state.quiz_index]
        
        st.info(f"**📍 相關章節：** {q['domain']}\n\n**📌 核心指引：** {q['topic']}")
        st.markdown(f"#### 📖 情境 (Scenario)：\n{q['scenario']}")
        
        with st.form(key=f"quiz_form_{st.session_state.quiz_index}"):
            choice = st.radio("請依據 PCPD 指引選擇最佳的管治方式：", q['options'], index=None)
            submit_ans = st.form_submit_button("提交答案 🔍")
            
            if submit_ans and choice:
                st.session_state.user_choice = choice
                st.session_state.quiz_answered = True
                
                if choice == q['answer']:
                    st.session_state.quiz_score += 1
                else:
                    st.session_state.weak_domains.add(q['domain'])
                st.rerun()

        if st.session_state.quiz_answered:
            if st.session_state.user_choice == q['answer']:
                st.success("🎯 **判斷正確！**")
            else:
                st.error("⚠️ **判斷有誤。請參考下方官方指引解析。**")
            
            st.markdown(f"**正確解答：** {q['answer']}")
            st.markdown(q['explanation'])
            
            if st.button("下一題 ➡️"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.user_choice = None
                st.rerun()
    else:
        st.balloons()
        st.success(f"🏆 **測驗完成！您的總得分為：{st.session_state.quiz_score} / {len(QUIZ_BANK)}**")
        
        if st.session_state.weak_domains:
            st.warning("📊 **報告：您在以下《模範框架》章節存在弱點，建議查閱官方文件：**")
            for w in st.session_state.weak_domains:
                st.markdown(f"- {w}")
        else:
            st.info("📊 **報告：表現優異！您已完全掌握 PCPD《模範框架》的核心規範。**")
            
        if st.button("🔄 重新測驗"):
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
        st.markdown("#### 📥 第一步：輸入企業場景脈絡")
        col1, col2 = st.columns(2)
        with col1:
            company_input = st.selectbox("選擇基礎企業用例", list(RISK_MATRIX.keys()), format_func=lambda x: RISK_MATRIX[x]["label"])
        with col2:
            oversight_input = st.selectbox("預期的人為監督模式", list(OVERSIGHT_OPTIONS.keys()), format_func=lambda x: OVERSIGHT_OPTIONS[x])
            
        ai_use_case = st.text_area(
            "請詳細描述您的 AI 應用場景（系統將自動依據 PCPD 指引偵測：跨境資料傳輸、第三方採購或內部定製等合規脈絡）",
            placeholder="例如：向外部供應商採購現成的 AI 招聘系統，並涉及將香港員工的資料傳輸至海外伺服器..."
        )
        
        if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍"):
            st.session_state.audit_performed = True
            st.session_state.company_context = company_input
            st.session_state.human_oversight_pref = oversight_input
            st.session_state.case_description = ai_use_case

    if st.session_state.audit_performed:
        st.markdown("---")
        st.markdown("### 📋 第二步：依據 PCPD《模範框架》產出之合規報告")
        
        ctx_text = st.session_state.case_description.lower()
        base_risk = RISK_MATRIX[st.session_state.company_context]
        current_oversight = st.session_state.human_oversight_pref
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 第一、二部：管治與風險", "⚙️ 第三部：模型定製與實施", "📢 第四部：持份者溝通"])
        
        with sub_tab1:
            st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督")
            st.info(f"**【基準風險判定】** {base_risk['reason']}")
            
            has_cross_border = any(w in ctx_text for w in ["跨境", "傳輸", "轉移", "海外", "外地", "雲端"])
            if has_cross_border:
                st.error("🔴 **合規提示：涉及跨境資料轉移的合法性**\n\n依據《模範框架》第 14 頁：若機構將個人資料轉移予外地資料處理者，必須採用**合約規範或其他方法**（依據《私隱條例》保障資料第 4(2) 原則），防止資料未獲准許被查閱或使用。")
            
            st.markdown("##### 👥 人為監督模式合規審查")
            is_text_automated = any(w in ctx_text for w in ["完全自動化", "直接決定", "無須人工"])
            
            if base_risk["level"] == "HIGH":
                if is_text_automated and current_oversight == "HITL":
                    st.error("🚨 **管治邏輯衝突：** 表單選擇「人在環中」，但描述為「完全自動化」。依據指引，高風險用例必須保留人類實質的控制權。")
                elif current_oversight != "HITL":
                    st.warning("⚠️ **合規警告：** 依據《模範框架》第 32(i) 條，高風險 AI 系統**應採取「人在環中」**方式進行人為監督。")
                else:
                    st.success("✅ **人為監督配置合規：** 符合《模範框架》第 32 條「人在環中」之規範。")

        with sub_tab2:
            st.subheader("第三部：AI 模型的定製與 AI 系統的實施及管理")
            is_third_party = any(w in ctx_text for w in ["第三方", "供應商", "採購", "現成", "外購"])
            is_unauthorized = any(w in ctx_text for w in ["私下", "未經授權", "繞過"])
            
            if is_unauthorized:
                st.error("🚨 **資料保安危機：偵測到未經授權的 AI 使用！**")
                st.markdown("違反《私隱條例》保障資料第 4 原則。機構必須立即採取技術與政策措施（如更新內部指引、實施存取控制）以防止資料外洩。")
                
            elif is_third_party:
                st.warning("🚨 **合規焦點：關於採購 AI 方案的管治考慮（第 16 條）**")
                st.markdown("由於採購第三方方案，機構應落實以下合約與管理措施：")
                tp1 = st.checkbox("【資料處理者協議】已簽署協議，明文禁止供應商將資料用於其自身目的（如二次訓練）（第 16(v) 條）。")
                tp2 = st.checkbox("【責任與罰則】合約中已明訂私隱和保安的責任及道德規定（第 16(ii) 條）。")
                tp3 = st.checkbox("【AI 事故應變計劃】已制定應變計劃，有需要時能迅速暫停 AI 系統（第 46(iv) 及 49 條）。")
                st.progress((sum([tp1, tp2, tp3]) / 3))
                
            else:
                st.success("🛠️ **合規焦點：為定製及使用 AI 準備數據（第 41 條）**")
                in1 = st.checkbox("【資料最少化】僅收集及使用為達致特定目的相關的個人資料，已刪除無關資料。")
                in2 = st.checkbox("【私隱增強技術】在適當情況下，已使用匿名化、假名化或合成數據。")
                in3 = st.checkbox("【持續監察】定期以新數據微調及再訓練 AI 模型，防範「模型漂移」（第 48(v) 條）。")
                st.progress((sum([in1, in2, in3]) / 3))

        with sub_tab3:
            st.subheader("第四部：與持份者的溝通及交流")
            st.markdown("- **顯著披露：** 除非情況顯而易見，否則應清楚及用顯著的方式披露 AI 系統的使用（第 53(i) 條）。")
            st.markdown("- **反饋與人工介入：** 若 AI 決策可能對個人造成重大影響，應提供途徑讓當事人尋求解釋及要求人為介入（第 56 條）。")
            st.markdown("- **淺白溝通：** 與持份者溝通應使用淺白的語言和清楚易明的方式（第 60 條）。")
