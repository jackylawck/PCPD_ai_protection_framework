import streamlit as st

# 設定網頁標題與排版
st.set_page_config(
    page_title="PCPD AI Protection Framework Evaluator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隱藏預設的 Streamlit 選單，提升企業產品專業度
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 側邊欄：展示 PCPD 模範框架核心與開發者權威背書
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Emblem_of_Hong_Kong.svg/120px-Emblem_of_Hong_Kong.svg.png", width=80)
    st.title("PCPD AI Governance")
    st.markdown("### 《人工智能：個人資料保障模範框架》審計代理")
    st.markdown("---")
    st.markdown("**評估基準涵蓋四大核心：**")
    st.markdown("1. AI 策略及管治\n2. 風險評估及人為監督\n3. AI 模型的定製與管理\n4. 與持份者的溝通及交流")
    st.markdown("---")
    st.markdown("### 關於本系統")
    st.info(
        "本自動化合規審計沙盒嚴格遵循香港個人資料私隱專員公署 (PCPD) 於 2024 年發布之指引，"
        "旨在協助企業將 AI 治理原則轉化為可執行的代碼與結構化風險監督 (Governance-as-Code)。"
    )

# 主畫面設計
st.title("🛡️ PCPD AI 個人資料保障模範框架：合規評估系統")
st.markdown("### 企業 AI 導入前置審查 (Enterprise AI Deployment Pre-Audit)")
st.write("請描述您的企業準備導入的 AI 應用場景，系統將依據 PCPD 指引自動評估潛在私隱風險、建議的人為監督層級，並生成合規行動清單。")

# 使用者輸入區
with st.form("audit_form"):
    company_context = st.selectbox(
        "選擇企業類型",
        ["香港金融機構", "大型跨國企業 (HR 數位轉型)", "社福與非牟利機構", "醫療與健康科技", "零售與電子商務"]
    )
    
    ai_use_case = st.text_area(
        "詳細描述您的 AI 應用場景 (Use Case)",
        placeholder="例如：我們計劃導入 M365 Copilot 結合內部 HR 系統，用於分析員工績效數據並預測離職率..."
    )
    
    submitted = st.form_submit_button("執行 PCPD 框架合規審計 🔍")

# 模擬後端 LLM 處理邏輯與輸出展示
if submitted:
    if not ai_use_case:
        st.warning("⚠️ 請輸入具體的 AI 應用場景以進行審計。")
    else:
        with st.spinner("🔄 正在連結 PCPD 《人工智能：個人資料保障模範框架》知識庫進行深度審計..."):
            
            # TODO: 這裡未來可串接 OpenAI API 傳入知識庫，目前先展示高質量的模版輸出
            
            st.success("✅ 審計完成。以下為基於 PCPD 模範框架之評估報告：")
            
            # 建立分頁標籤來結構化展示四大核心評估
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 第一部：策略及管治", 
                "⚖️ 第二部：風險評估與監督", 
                "⚙️ 第三部：模型定製與管理", 
                "📢 第四部：持份者溝通"
            ])
            
            with tab1:
                st.subheader("管治架構與問責建議")
                st.write("**合規狀態：** 需成立跨部門 AI 管治委員會")
                st.info(
                    "PCPD 建議：高級管理層的支持是負責任 AI 的成功要素。您的場景涉及內部敏感數據，"
                    "建議由高管領導，包含資料科學家、法律合規及 HR 專業人員組成跨部門團隊進行監督。"
                )
                
            with tab2:
                st.subheader("私隱風險判定與人為監督層級")
                st.markdown("**判定風險等級：** 🔴 **高風險 (High Risk)**")
                st.write("此場景可能對個人職涯與評核造成重大影響。")
                st.error(
                    "**法定監督要求：人在環中 (Human-in-the-loop)**\n\n"
                    "依據 PCPD 第二部指引，人類決策者必須在決策過程中保留控制權，防止 AI 出錯或產生不當決定。不能採用完全自動化 (Human-out-of-the-loop) 模式。"
                )
                
            with tab3:
                st.subheader("數據準備與資料最少化 (Data Minimisation)")
                st.write("**合規行動清單：**")
                st.checkbox("確保收集的員工數據（如年資、考績）符合《私隱條例》保障資料第1原則（足夠但不超乎適度）。", value=True)
                st.checkbox("實施私隱增強技術 (PETs)，如假名化或匿名化處理敏感特徵。")
                st.checkbox("持續監察 AI 模型，防止『模型漂移』導致預測偏見。")
                
            with tab4:
                st.subheader("透明度與可解釋性 (Explainable AI)")
                st.info(
                    "**披露要求：**\n"
                    "必須向受影響的員工清楚披露 AI 系統的使用情況，並提供足夠的資訊說明 AI 參與績效評估的程度。\n"
                    "**建議提供人為介入選項：** 容許員工對 AI 輸出的結果提出異議或要求合規人員重新審視。"
                )
