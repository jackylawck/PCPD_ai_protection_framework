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

# 香港個人資料私隱專員公署 (PCPD) 官方中英文文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"

if 'lang' not in st.session_state: st.session_state.lang = '繁體中文'
if "audit_performed" not in st.session_state: st.session_state.audit_performed = False
if "company_context" not in st.session_state: st.session_state.company_context = "大型跨國企業 (HR 數位轉型 / 考績預測)"
if "human_oversight_pref" not in st.session_state: st.session_state.human_oversight_pref = "人在環中 (Human-in-the-loop)"

is_zh = st.session_state.lang == '繁體中文'

# ==========================================
# 2. 結構化風險字典矩陣 (依據 PCPD 2024 官方高風險定義精準映射)
# ==========================================
RISK_MATRIX = {
    "大型跨國企業 (HR 數位轉型 / 考績預測)": {
        "level": "HIGH",
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12 明文規定，涉及「求職者評估、工作表現評核或終止僱傭合約」之場景，屬法定高風險用例。"
    },
    "香港金融機構 (信貸評估 / 欺詐偵測)": {
        "level": "HIGH",
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12，涉及「評估個人的信用可靠程度以作出自動化財務決策」之場景，屬法定高風險用例。"
    },
    "醫療與健康科技 (AI 輔助影像分析)": {
        "level": "HIGH",
        "zh_reason": "依據 PCPD 2024《模範框架》第 25 頁圖 12，涉及「AI 輔助醫學影像分析或治療」之場景，直接關乎人身安全，屬法定高風險用例。"
    },
    "零售與電子商務 (AI 聊天機械人推薦)": {
        "level": "LOW",
        "zh_reason": "依據 PCPD 2024《模範框架》第 20 頁第 24 條，用於推送個人化廣告或商品推薦，對持份者重大權益影響較低，屬一般/低風險用例。"
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
    st.markdown("**本系統核心指標 100% 依據香港個人資料私隱專員公署 (PCPD) 2024 年最新發布之《人工智能：個人資料保障模範框架》進行決定性邏輯編碼。**")
    st.markdown("---")
    st.markdown("### 🏛️ 全球管治框架對齊" if is_zh else "### 🏛️ Global Frameworks")
    st.caption("✅ **IAPP AIGP (v2.1):** Domain II, III, IV 精準映射")
    st.caption("✅ **ISO/IEC 42001 (AIMS):** 體系整合與可觀測性")
    st.markdown("---")
    st.warning("⚠️ **開源公共利益沙盒：** 純決定性代碼架構，100% 無 AI 幻覺，數據關閉即銷毀。")

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
        "請詳細描述您的 AI 應用場景（系統將自動智能偵測：影子 AI 違規操作、跨國多法域衝突、中港跨境數據、第三方現成 SaaS 採購或自研定製等複雜脈絡）",
        placeholder="例如：總部在歐盟受 EU AI Act 監管，香港分公司向美國廠商採購生成式招聘系統，處理中港跨境數據..."
    )

    if st.form_submit_button("啟動 PCPD 模範框架深度審核 🔍"):
        st.session_state.audit_performed = True
        st.session_state.company_context = company_input
        st.session_state.human_oversight_pref = oversight_input
        st.session_state.case_description = ai_use_case

# ==========================================
# 5. Core Engine: PCPD Model Framework Logic Reasoning
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
    # 分頁一：第一、二部 —— 風險判定與邏輯防偽 (唯一版本)
    # ------------------------------------------
    with tab1:
        st.subheader("第一部：AI 策略及管治 & 第二部：風險評估及人為監督")
        st.info(f"**【基準風險判定】** {base_risk['zh_reason']}")

        # HR 專屬演算法偏見與跨法規聯動警告 (Domain I & II 深度對齊)
        if "HR" in st.session_state.company_context:
            st.warning("⚠️ **跨法規聯動警告 (Employment Ordinance Cross-Compliance)：**\n\n在高度自動化的 HR 績效與解僱決策中，極易引入**演算法偏見（Algorithmic Bias）與間接歧視**。例如，AI 模型可能因單純計算出勤率，而歧視了因合法病假或產假缺勤的員工。這不僅違反公平原則，更可能觸犯香港《僱傭條例》下的不當解僱，引發嚴重的勞資審裁處訴訟。")

        # 智能偵測：多法域與跨境數據流動
        has_cross_border = any(w in ctx_text for w in ["跨境", "cross-border", "中港", "轉移", "外地", "美國", "司法管轄"])
        if has_cross_border:
            st.error("🔴 **深度審計：偵測到多法域重疊管轄與跨境傳輸風險 (Overlapping Jurisdictions)**")
            st.markdown(
                f"- **《私隱條例》保障資料第 4(2) 原則與跨境規範（《模範框架》第 14 頁）：** 機構作為資料使用者，若將個人資料轉移予外地（如美國）資料處理者進行雲端處理，必須採用**合約規範或其他方法**保障資料保安。\n"
                f"- **跨國管轄權衝突（EU AI Act vs PCPD）：** 企業總部若受《歐盟 AI 法案》監管，香港分公司部署時必須進行雙重合規映射。董事會應指示法律合規部門簽發標準契約條款（SCCs）以應對多法域重疊監管。"
            )

        # 語境矛盾偵測 (防範合規幻覺)
        st.markdown("##### 👥 人為監督模式（Human Oversight）合規審查")

        is_text_automated = any(w in ctx_text for w in ["完全自動化", "直接執行", "fully automated", "自動解僱", "直接生成建議", "照單全收"])

        if base_risk["level"] == "HIGH":
            # 交叉比對：表單選了 HITL，但文字描述卻是 HOOTL
            if is_text_automated and "人在環中" in current_oversight:
                st.error("🚨 **管治邏輯嚴重衝突 (Control Design Failure)：**\n\n系統偵測到您在表單勾選了「人在環中」，但在情境描述中卻提及了「完全自動化 / 直接執行」。在 AIGP 實務中，這屬於極度危險的**合規幻覺 (Compliance Illusion)**！\n\n**董事會審計警告：** 若系統自動生成解僱名單，而 HR 僅作「橡皮圖章（Rubber Stamp）」式執行，實質上已降級為違規的「人在環外」。強烈建議暫停部署，重新檢視業務流程設計，確保人類具備實質的最終裁量權。")
            elif "人在環中" not in current_oversight:
                st.warning("⚠️ **管治衝突警告：** 依據 **PCPD 2024《模範框架》第二部第 32(i) 條** 明文規定，高風險 AI 系統**應強制採取「人在環中」(Human-in-the-loop)** 方式。")
            else:
                st.success("✅ **人為監督配置合規：** 系統與表單描述一致，符合 **PCPD 2024《模範框架》第 32 條** 規範。")

    # ------------------------------------------
    # 分頁二：第三部 —— 智能分流與影子 AI 阻斷
    # ------------------------------------------
    with tab2:
        st.subheader("第三部：AI 模型的定製與AI系統的實施及管理")

        is_shadow_ai = any(w in ctx_text for w in ["影子", "shadow", "私下", "員工自行", "繞過", "未授權", "未經批准", "偷偷", "本地工作站"])
        is_third_party = any(w in ctx_text for w in ["第三方", "third party", "api", "黑箱", "black box", "採購", "procure", "saas", "廠商"])

        if is_shadow_ai:
            st.error("🚨 **重大合規危機：偵測到「影子 AI (Shadow AI)」違規操作！**")
            st.markdown(
                "💡 **AIGP 專家審計診斷（依據 PCPD 2024《模範框架》第一部第 1.3 節 AI 系統清單管理延伸）：**\n\n"
                "員工繞過 IT 與採購程序私自運行開源模型，直接違反《私隱條例》保障資料第 4 原則（資料保安）。機構作為資料使用者，未能採取切實可行的步驟防止資料在未獲准許下被處理。"
                "常規的合規打分在此情境下**全面失效**，董事會必須立即啟動以下阻斷與重建機制："
            )
            sh1 = st.checkbox("【技術阻斷與可觀測性】IT 部門已部署 CASB (雲端存取安全代理) 或端點防護，阻擋未經授權的開源模型、Hugging Face 庫或 API 的呼叫。")
            sh2 = st.checkbox("【修訂 AUP 政策】已更新《可接受使用政策 (Acceptable Use Policy)》，明文嚴禁將包含 PII、客戶數據或商業機密的內容輸入未經審批的外部 AI 工具。")
            sh3 = st.checkbox("【建立認可清單 (Whitelisting)】依據《模範框架》第 14 頁精神，「堵不如疏」，已為員工提供經過企業合規審查、承諾零數據留存的內部安全 AI 替代方案。")

            sh_score = (sum([sh1, sh2, sh3]) / 3) * 100
            st.progress(sh_score / 100)

        elif is_third_party:
            st.warning("🚨 **核心治理分支切換：第三方方案 / 外購 SaaS / 廠商 API 採購軌道 (TPRM Route Active)**")
            st.markdown(
                f"💡 **高管審計核心提示（依據 PCPD 2024《模範框架》第一部第 1.2 節「關於採購 AI 方案的管治考慮」與第三部第 44 條修正）：**\n\n"
                f"由於本案屬於「向外部廠商採購現成系統且無法獲取底層細節」，企業在實踐中無法、也無需進行內部的模型微調、控制數據準備或直接監控算法漂移。"
                f"董事會的最高管治核心必須全面轉向 **合約約束 (Contractual Protections)** 與 **第三方風險管理 (Third-Party Risk Management, TPRM)**："
            )

            tp1 = st.checkbox("【資料處理者合約保障】已與外部廠商簽署正式資料處理者協議，明文禁止廠商將香港分公司輸入的求職者 PII 與提示詞用作其模型二次訓練。（符合《模範框架》第 16(v) 及 44(ii) 條規範）")
            tp2 = st.checkbox("【合約責任轉嫁】合約中已明訂當廠商系統產生不當偏見、非法歧視或資料外洩時的法律責任歸屬、罰則與即時通知義務。（符合《模範框架》第 18 條規範）")
            tp3 = st.checkbox("【AI 事故暫停機制】已建立「AI 事故應變計劃」，當供應商遭遇黑客攻擊、單方面規格變更或觸發隱私漏洞時，企業有指定人員能一鍵「暫停」或「停止」系統連線（符合《模範框架》第 46(iv) 及 49 條圖 18 規範） 。")

            tp_score = (sum([tp1, tp2, tp3]) / 3) * 100
            st.markdown(f"##### 📊 第三方採購與供應商管理 (TPRM) 合規就緒度：**{tp_score:.0f}%**")
            st.progress(tp_score / 100)

        else:
            st.success("🛠️ **核心治理分支切換：自主研發與定製實施軌道 (In-House Development Route Active)**")
            st.markdown("**請勾選已落實之開發期控制措施（依據 PCPD 2024《模範框架》第三部「數據準備與定製實施」）：**")
            in1 = st.checkbox("【資料最少化】收集微調數據屬足夠但不超乎適度，已移除或假名化無關之敏感特徵。（符合《模範框架》第 41(ii) 條規範）")
            in2 = st.checkbox("【私隱增強技術】處理高敏感特徵時，已評估或採用差分私隱、合成數據等 PETs 技術。（符合《模範框架》第 41(ii) 條規範）")
            in3 = st.checkbox("【防範模型漂移】已指派技術團隊建立內部日誌監控，防止模型表現隨時間出現「模型漂移 (Model Drift)」。（符合《模範框架》第 48(v) 條規範）")

            in_score = (sum([in1, in2, in3]) / 3) * 100
            st.markdown(f"##### 📊 自主研發與定制合規就緒度：**{in_score:.0f}%**")
            st.progress(in_score / 100)

    # ------------------------------------------
    # 分頁三：第四部 —— 持份者溝通
    # ------------------------------------------
    with tab3:
        st.subheader("第四部：與持份者（求職者、員工、消費者）的溝通及交流")
        st.markdown(f"**依據 PCPD 2024《模範框架》第四部之規範，向董事會匯報時必須落實以下持份者保障機制：**")
        st.markdown("- **顯著披露 (Prominent Disclosure)：** 必須向受影響群體（如求職者）清楚且顯著地披露 AI 系統的使用情況與介入程度（符合**《模範框架》第 53(i) 條**規範）。")
        st.markdown("- **局部可解釋性與救濟途徑 (Redress Mechanism)：** 若 AI 決策對個人產生重大影響（如篩選簡歷不通過），機構**必須提供人為介入的選項**，容許當事人表達反饋、尋求解釋並要求合規人員重新審視（符合**《模範框架》第 56 及 58 條**規範）。")
        st.markdown("- **淺白語言 (Plain Language)：** 與持份者溝通之所有私隱政策與通知，應使用淺白的語言和清楚易明的方式表達（符合**《模範框架》第 60 條**規範）。")
