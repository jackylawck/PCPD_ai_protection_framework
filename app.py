import streamlit as st

# 1. 設定網頁與企業級 UI
st.set_page_config(
    page_title="PCPD AI Protection Framework Guide",
    page_icon="🛡️",
    layout="wide"
)

# 隱藏 Streamlit 預設選單，提升專業度
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# 官方文件公開網址
ZH_PDF_URL = "https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_protection_framework.pdf"
EN_PDF_URL = "https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf"

# 2. 側邊欄：官方權威背書與導讀
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("PCPD AI Governance")
    st.markdown("### 官方指引快速連結")
    st.link_button("繁體中文官方 PDF 🔗", ZH_PDF_URL)
    st.link_button("English Official PDF 🔗", EN_PDF_URL)
    st.markdown("---")
    st.markdown("**💡 公共利益倡導：**")
    st.caption("本系統為開源合規沙盒，直接對接香港個人資料私隱專員公署 (PCPD) 2024 年最新發布之《人工智能：個人資料保障模範框架》，協助企業零成本落地 AI 管治。")

# 3. 主畫面設計
st.title("🛡️ PCPD AI 個人資料保障模範框架：互動式合規評估系統")
st.subheader("Enterprise AI Deployment Pre-Audit (100% Free Open-Access Guide)")
st.markdown("請選擇您的企業類型與預期導入的 AI 場景，系統將根據 PCPD 官方指引的四大核心範疇，自動對照並產出應對的合規稽核清單。")

# 4. 使用者互動輸入區
with st.form("audit_form"):
    col1, col2 = st.columns(2)
    with col1:
        company_context = st.selectbox(
            "1. 選擇企業類型 (Enterprise Type)",
            ["大型跨國企業 (HR 數位轉型 / 考績預測)", "香港金融機構 (信貸評估 / 欺詐偵測)", "醫療與健康科技 (AI 輔助影像分析)", "零售與電子商務 (AI 聊天機械人推薦)", "社福與非牟利機構"]
        )
    with col2:
        human_oversight_pref = st.selectbox(
            "2. 預期的人為監督模式 (Intended Human Oversight)",
            ["人在環中 (Human-in-the-loop) - 人類保留最終控制權", "人為管控 (Human-in-command) - 人類監督系統，必要時介入", "人在環外 (Human-out-of-the-loop) - 完全自動化決策"]
        )
        
    ai_use_case = st.text_area(
        "3. 請簡述您的 AI 應用情境與涉及的個人資料 (例如：收集員工年資、考績以預測離職率)",
        placeholder="在此輸入具體情境..."
    )
    
    submitted = st.form_submit_button("執行 PCPD 框架對照審查 🔍")

# 5. 動態合規對照邏輯 (依據上傳的官方 PDF 內容精準分類)
if submitted:
    st.success("✅ 稽核清單已根據 PCPD 2024《模範框架》官方文件生成。請點擊下方分頁查看各部分的法定與道德要求：")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 第一部：AI 策略及管治", 
        "⚖️ 第二部：風險評估與監督", 
        "⚙️ 第三部：模型定製與管理", 
        "📢 第四部：持份者溝通"
    ])
    
    with tab1:
        st.subheader("第一部：AI 策略及管治 (Part I: AI Strategy & Governance)")
        st.markdown(f"**💡 針對 [{company_context}] 的最高管理層問責建議：**")
        st.markdown("- **成立 AI 管治委員會：** 高級管理層（如行政層或董事會層）必須支持並積極參與。建議由 C-Level 高管領導跨部門團隊（包含 HR、法律合規、數據科學家）。")
        st.markdown("- **建立 AI 清單 (AI Inventory)：** 機構應建立 AI 清單以實施管治措施，並列明機構中不可接受的用途。")
        st.markdown(f"[➡️ 點此至官方 PDF 閱讀第一部詳細條文 (第 10 頁)]({ZH_PDF_URL}#page=10)")
        
    with tab2:
        st.subheader("第二部：風險評估及人為監督 (Part II: Risk Assessment & Human Oversight)")
        st.markdown("**⚖️ 風險判定與人為監督層級對照：**")
        
        # 根據用戶選擇的場景或監督模式進行動態警示
        if "HR" in company_context or "信貸" in company_context or "醫療" in company_context:
            st.error("🔴 **高風險判定 (High Risk Scenario):** 依據 PCPD 指引，涉及「求職者評估、工作表現評核」或「信貸可靠程度自動化決策」屬於高風險用例，可能對個人造成重大影響。")
            if human_oversight_pref != "人在環中 (Human-in-the-loop) - 人類保留最終控制權":
                st.warning("⚠️ **管治衝突警告：** 官方指引第 32 條明確規定，高風險 AI 系統**應採取「人在環中」(Human-in-the-loop)** 模式，人類決策者必須保留控制權，防止完全自動化出錯。")
        else:
            st.info("🟡 **一般風險判定：** 請持續進行私隱影響評估 (PIA)，確保剩餘風險降至可接受水平。")
            
        st.markdown(f"[➡️ 點此至官方 PDF 閱讀第二部詳細條文 (第 20 頁)]({ZH_PDF_URL}#page=20)")
        
    with tab3:
        st.subheader("第三部：AI 模型的定製與系統管理 (Part III: Customisation & Management)")
        st.markdown("**⚙️ 數據準備與資訊保安行動稽核表：**")
        st.checkbox("**貫徹資料最少化 (Data Minimisation)：** 是否已移除或假名化與目的無關的敏感特徵（如姓名、身份證號）？（指引第 41 條）", value=True)
        st.checkbox("**防範模型漂移 (Model Drift)：** 已指派專人定期檢視並以新數據微調模型，防止表現隨時間衰退。（指引第 48 條）")
        st.checkbox("**對抗式攻擊防禦：** 針對輸入端實施內部指引（如限制員工輸入客戶機密隱私），並考慮進行紅隊演練。")
        st.markdown(f"[➡️ 點此至官方 PDF 閱讀第三部詳細條文 (第 27 頁)]({ZH_PDF_URL}#page=27)")
        
    with tab4:
        st.subheader("第四部：與持份者的溝通及交流 (Part IV: Stakeholder Engagement)")
        st.markdown("**📢 透明度與可解釋性 (Transparency & Explainability) 揭露要求：**")
        st.markdown("- **顯著披露：** 除非使用情況顯而易見，否則必須向受影響的個人（如員工或客戶）清楚披露 AI 的使用。")
        st.markdown("- **提供救濟途徑：** 當 AI 輸出結果對個人造成重大影響時，機構**應盡可能提供管道讓個人尋求合理解釋、表達反饋及要求人為介入**。")
        st.markdown(f"[➡️ 點此至官方 PDF 閱讀第四部詳細條文 (第 40 頁)]({ZH_PDF_URL}#page=40)")
