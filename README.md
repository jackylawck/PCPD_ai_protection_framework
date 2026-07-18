# 🛡️ PCPD AI Protection Framework Evaluator

本專案是一個動態合規審計沙盒原型，嚴格遵循香港個人資料私隱專員公署 (PCPD) 於 2024 年發布之《人工智能：個人資料保障模範框架》進行決定性（Deterministic）邏輯編碼。

This project is an automated compliance audit sandbox prototype, strictly designed in accordance with the "Artificial Intelligence: Model Personal Data Protection Framework" published by the Office of the Privacy Commissioner for Personal Data (PCPD), Hong Kong, in 2024.

👉 **[🚀 點此立即訪問線上動態合規風險評分卡系統 (Live Sandbox App)](https://pcpd-ai-protection-framework.streamlit.app/)**

---

## 🏛️ 獨家管治方法論 (Governance Methodology)

本系統之底層映射邏輯，採用由 Jacky Law 提出的 **「人本 AI 管治五層架構 (Human-Centred AI Governance Stack)」** 進行落地方案審查：
1. **Purpose & Accountability** (策略與董事會問責) - 映射模範框架第一部
2. **People & Workforce Impact** (組織、人才與勞資權益) - 映射模範框架第二部及香港《僱傭條例》
3. **Data & Privacy Controls** (數據私隱與跨境流動) - 映射模範框架第三部及《私隱條例》
4. **Model & Decision Assurance** (模型可信度與決策監督) - 映射模範框架第三、四部
5. **Evidence & Resolution** (合規證據、事故應變與調解機制) - 映射模範框架第四部

詳細控制點說明請參閱專案內之 `GOVERNANCE_MODEL.md`。

---

## ⚠️ 免責聲明 (Disclaimer)

本系統為獨立開發之管治概念驗證 (Proof of Concept) 工具，**並非**香港個人資料私隱專員公署 (PCPD) 的官方系統，亦不代表任何官方法律意見。

- **嚴格邊界控制 (Strict Boundary Control)：** 為確保合規評估的精準度，本系統的邏輯基準 100% 嚴格鎖定於 PCPD《模範框架》文本內容，消除了生成式 AI 的「幻覺」風險。
  - For precision in compliance assessment, the logic base of this system is 100% strictly locked to the text of the PCPD "Model Framework", eliminating LLM hallucination risks.
- **邊界外拒絕作答 (Refusal to Answer Outside Scope)：** 若查詢內容超出《模範框架》的適用範圍，系統將觸發防禦性機制硬性拒絕作答，以避免造成合規幻覺 (Compliance Illusion)。
  - Queries falling outside the scope of the "Model Framework" will be rejected to prevent the creation of "Compliance Illusions".
- **使用建議 (Usage Advice)：** 評估結果僅供企業內部進行風險評估與管治流程 (Governance Workflow) 參考，實際合規部署請諮詢專業法律或資料保護顧問。
  - Evaluation results are for internal risk assessment and governance workflow reference only. Please consult professional legal or data protection counsel for actual compliance deployment.

---

## 👥 聯絡與專業交流 (Contact & Professional Engagement)

如果您對本系統的管治邏輯、PCPD《模範框架》的落地實踐，或企業 AI 導入的合規審計有任何學術與專業上的探討，歡迎透過 LinkedIn 與我聯絡。

If you have any academic or professional inquiries regarding this system's governance logic, the practical implementation of the PCPD "Model Framework", or corporate AI compliance auditing, please feel free to connect via LinkedIn.

👉 **[🌐 Connect on LinkedIn | 羅子淇 Jacky Law](https://www.linkedin.com/in/jackylawck)**
