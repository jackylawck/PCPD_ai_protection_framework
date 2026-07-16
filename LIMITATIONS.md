# 系統限制與邊界控制 (System Limitations & Boundary Control)

## 1. 嚴格決定性架構 (Strict Deterministic Architecture)
- **中文：** 本系統 100% 採用決定性代碼（Deterministic Code）與預設管治路由。系統內部不包含、亦不調用任何大型語言模型（LLM）API。此設計旨在徹底杜絕生成式 AI 的「幻覺（Hallucination）」風險，確保所有合規審計判定均具備 100% 的可再現性。
- **English:** This system is 100% powered by deterministic logic rules. It does not integrate or call any Large Language Model (LLM) APIs. This architectural control is implemented to eliminate "hallucination" risks, ensuring 100% reproducibility in compliance audit outputs.

## 2. 知識庫邊界與「寧可藏拙」原則 (Uncompromising Knowledge Boundary)
- **中文：** 本系統的知識庫邊界**嚴格且僅限於**香港個人資料私隱專員公署（PCPD）2024 年發布之《人工智能：個人資料保障模範框架》。若使用者的提問或輸入場景超出了該框架的法規文本範圍（例如尋求技術程式碼編寫、非隱私類的資安技術細節等），系統將觸發防禦性機制，**硬性拒絕作答**，絕不提供任何推測性、衍生性或未經官方證實的管治建議。
- **English:** The system's knowledge boundary is **strictly confined** to the PCPD 2024 "Model Personal Data Protection Framework". If user text inputs fall outside this regulatory text (e.g., technical coding, general IT security details), the system triggers a defensive fallback to **explicitly refuse to answer**, avoiding speculative or unauthorized compliance interpretation.
