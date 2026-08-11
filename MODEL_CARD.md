# 📋 ISO 42001 Model Card: PCPD AI Protection Framework Evaluator
# ISO 42001 模型卡：PCPD 人工智能保障框架預審評估器

> **ISO 42001 Alignment / ISO 42001 標準對齊**:
> * Controls A.6: AI System Impact Assessment (AI 系統影響評估)
> * Controls A.8: Data for AI Systems (AI 系統數據管治)
> * Controls A.9: Transparency & Accountability (透明度與問責制)
> 
> 

---

## 1. System Overview & Administrative Metadata / 系統概述與管理元數據

* **System Name / 系統名稱**: PCPD AI Protection Framework Deterministic Evaluator (方案 A：決定性預審沙盒)
* **Model Version / 模型版本**: v1.0.0 (Production Sandbox / 生產沙盒版)
* **System Type / 系統類型**: Rule-based Deterministic Expert System / Pre-audit Gatekeeper (基於規則之決定性專家系統 / 預審門神)
* **Primary Developer & Governance Lead / 主開發者與管治負責人**: Jacky Law 羅子淇 (Certified ISO 42001 Lead Auditor / AIGP Candidate)
* **Last Audit Date / 最近審計日期**: 2026-07-30
* **Repository / 程式碼倉庫**: [jackylawck/PCPD_ai_protection_framework](https://github.com/jackylawck/PCPD_ai_protection_framework)

---

## 2. Intended Use & Application Boundaries / 預期用途與應用邊界

### 🇬🇧 English

* **Intended Use Case**:
* Enterprise pre-audit classification for AI project initiation under the 2024 PCPD Model Framework.
* Rapid risk tiering for internal HR, IT procurement, and legal compliance teams.


* **Out-of-Scope / Prohibited Uses**:
* **Legal Advice Disclaimer**: Does not constitute binding legal counsel under the Personal Data (Privacy) Ordinance (PDPO Cap. 486).
* **Cross-Jurisdictional Scope**: Out of scope for non-privacy legal disputes (e.g., Employment Ordinance gender discrimination, Copyright/IP ownership).



### 🇭🇰 中文 (繁體)

* **預期應用情境**:
* 依據私隱專員公署 (PCPD) 2024《模範框架》，為企業內部 AI 專案立項提供預審風險分級。
* 協助企業人力資源 (HR)、資訊科技採購 (IT Procurement) 及合規團隊進行快速風險評估。


* **超出範圍 / 禁止用途**:
* **法律意見免責聲明**：本系統不構成《個人資料（私隱）條例》（第 486 章）下具約束力的法律意見。
* **跨法律範疇限制**：超出私隱條例管轄之法律爭議（如《僱傭條例》性別歧視、版權及知識產權歸屬）均不在評估範圍內。



---

## 3. Governance Architecture & Deterministic Logic / 管治架構與決定性邏輯

### 🇬🇧 English

* **Decision Engine**: Regular Expression (Regex) matching and strict Boolean keyword mapping against PCPD 2024 Core Domains.
* **Zero LLM Non-Determinism**: Eliminates hallucination risks by strictly adhering to pre-coded regulatory decision trees.
* **Fallback & Boundary Enforcement**: Out-of-scope queries (e.g., IP, non-privacy labor law) automatically trigger hardcoded refusal responses (`Out of Scope / System Refusal`) to uphold regulatory integrity.

### 🇭🇰 中文 (繁體)

* **決策引擎**：採用正規表達式 (Regex) 比對與嚴格布林邏輯，將情境精準映射至 PCPD 2024 核心領域。
* **零 LLM 不確定性**：嚴格遵循預先編碼的法規決策樹，徹底排除大語言模型 (LLM) 的幻覺與隨機性風險。
* **退守與邊界控制**：非私隱相關問題（如知識產權、勞工法理爭議）會自動觸發硬性拒絕機制 (`Out of Scope / System Refusal`)，維持監管審計嚴謹度。

---

## 4. Privacy, Security & Data Protection Controls / 私隱、資安與數據保護控制

### 🇬🇧 English

* **Data Sovereignty**: 100% In-memory processing; zero external API telemetry or data exfiltration.
* **Data Minimization**: Users only input text scenarios. No personal identifiers (PII) are ingested or stored.
* **Auditability (ISO 42001 Control A.9.3)**: Every user query generates a local cryptographic log entry for continuous auditability.

### 🇭🇰 中文 (繁體)

* **數據主權 (Data Sovereignty)**：100% 於揮發性記憶體 (RAM) 運算；零外部 API 傳輸或數據外洩風險。
* **數據最小化 (Data Minimization)**：僅接受情境描述文字，系統設計上嚴格禁止並隔離個人識別資訊 (PII)。
* **可審計性 (ISO 42001 Control A.9.3)**：每筆查詢皆自動生成本地密碼学日誌，確保可追溯性與不可否認性。

---

## 5. System Limitations & Known Trade-offs / 系統局限與已知權衡

### 🇬🇧 English

* **Keyword Dependency**: Highly formal phrasing is required; natural language ambiguity or colloquial phrasing may result in conservative "fallback" responses rather than direct risk mapping.
* **Mitigation Strategy**: Deployed in a **Dual-Track Defense Matrix** alongside Project 2 (RAG Advisor) to handle unstructured semantic queries.

### 🇭🇰 中文 (繁體)

* **關鍵字依賴性**：需要較正式的文本描述；過度口語化或模糊的自然語言可能觸發保守的「退守 (Fallback)」機制，而非直接映射風險等級。
* **緩解策略**：作為**雙軌防禦矩陣 (Dual-Track Defense Matrix)** 的第一軌部署，非結構化自然語言查詢可搭配專案二（動態 RAG 沙盒）進行語意檢索。
