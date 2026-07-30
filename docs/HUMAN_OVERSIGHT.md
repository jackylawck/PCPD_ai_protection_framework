# 👁️ Human Oversight & Accountability (人為監督與問責機制)

## 1. Governance Principle (管治原則)
本系統作為「輔助性評估工具（Assistive Evaluator）」，旨在為人力資源、採購及合規專業人員提供初步風險分級，**絕不能取代人類決策者（Human Decision-Makers）的專業判斷**。

## 2. Human-in-the-Loop (HITL) Architecture
本系統實施嚴格的「人在環中（HITL）」架構：
* **Recommendation Only**: 系統輸出的治理建議（Governance Actions）僅供參考。
* **Final Accountability**: 無論系統亮起紅燈（拒絕）或綠燈（放行），最終的 AI 專案啟動、預算審批或政策修訂，均必須由授權的主管或合規主任簽署負責。

## 3. Handling System Refusals (處理系統拒答)
當系統觸發 `Out of Scope (超出審查範圍)` 警報時，代表情境已超出 PCPD 管轄範圍（例如涉及勞工法例、性別歧視、知識產權等）。此時必須：
1. 中止依賴本系統的評估。
2. 將案件升級（Escalate）至跨部門 AI 管治委員會（AI Governance Committee）或外部法務顧問。
3. 考慮使用雙軌矩陣中的「方案 B（動態 RAG 沙盒）」進行更深度的語意法規檢索。

## 4. User Competency (使用者勝任要求)
操作本系統的企業用戶應具備基本的資料保障意識，並受過相關的 AI 管治通識培訓，以確保能正確解讀系統輸出的 ISO 42001 及 PCPD 專有名詞。
