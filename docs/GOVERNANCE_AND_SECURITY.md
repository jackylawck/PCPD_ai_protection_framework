# 🛡️ Integrated Governance & Security Policy
# 綜合 AI 管治與資訊安全政策

> **Compliance Standards / 遵循標準**: 
> * ISO/IEC 42001:2023 AI Management System (AIMS) Controls A.6, A.8, A.9, A.10
> * PCPD 2024 Model Framework (香港私隱專員公署《個人資料保障模範框架》)
> * IAPP AIGP Body of Knowledge (Domains I - IV)

---

## 1. Governance Principles & Human Oversight (管治原則與人為監督)

### 🇬🇧 English
* **Deterministic Gatekeeping**: The system employs explicit Regular Expression (Regex) matching and strict Boolean decision trees. This design yields 100% deterministic risk classification based on PCPD 2024 domains, completely eliminating non-deterministic LLM hallucinations.
* **Human-in-the-Loop (HITL) Architecture**: System outputs serve strictly as assistive pre-audit recommendations. Final project approvals, risk acceptances, or legal determinations remain solely under the authority of designated human compliance officers.
* **Jurisdictional Boundary Control**: Inquiries falling outside privacy legislation (e.g., Employment Ordinance disputes, Copyright/IP ownership) automatically trigger hardcoded system refusals (`Out of Scope`) to preserve regulatory integrity.

### 🇭🇰 中文 (繁體)
* **決定性門神機制**：本系統採用嚴格的正則表達式（Regex）與布林決策樹，針對 PCPD 2024 框架提供 100% 決定性的風險分級，徹底消除大語言模型（LLM）的機率型幻覺。
* **人在環中（HITL）架構**：系統輸出僅作為輔助性預審建議。最終的專案啟動、風險接受或法律決策，完全由授權的合規官與管理員人為掌控。
* **管轄邊界硬性控制**：超出《個人資料（私隱）條例》管轄範圍的查詢（如勞資糾紛、知識產權歸屬），系統會自動觸發硬性拒絕（`Out of Scope`），維持審計嚴謹性。

---

## 2. Data Governance & Privacy Controls (數據管治與私隱控制)

### 🇬🇧 English
* **Zero Data Retention (ZDR)**: Operates under a strict stateless model. User inputs are evaluated exclusively within transient session memory (RAM) and are physically purged upon session closure or browser refresh. Zero data is persisted to disk or external cloud storage.
* **Data Minimization & PII Isolation**: The system is architected to ingest scenario descriptions only. It strictly prohibits and isolates Personally Identifiable Information (PII).
* **Cryptographic Auditability (ISO 42001 Control A.9.3)**: Every evaluation generates a unique SHA-256 cryptographic audit hash with a UTC timestamp, establishing a non-repudiable audit trail without logging raw user text.

### 🇭🇰 中文 (繁體)
* **零數據留存（ZDR）**：貫徹極致的無狀態運算模式。用戶輸入僅於揮發性記憶體（RAM）中評估，網頁關閉或刷新後即刻物理銷毀，資料完全不落地。
* **數據最小化與 PII 隔離**：系統設計僅接收管理情境描述，嚴格隔離並禁止讀入個人識別資訊（PII）。
* **密碼學可審計性（ISO 42001 Control A.9.3）**：每筆評估即時生成 SHA-256 密碼學哈希值與 UTC 時間戳，在不記錄用戶原始文字的前提下，建立不可篡改的審計軌跡。

---

## 3. Risk Assessment & Threat Modeling (風險評估與威脅建模)

### 🇬🇧 English
* **System Risk Classification**: Classified as a **Low-Risk / Assistive Governance Tool** as it performs no automated decision-making (ADM), processes no biometric data, and exerts no direct operational control.
* **Threat Mitigation Matrix**:

| Identified Threat / 識別威脅 | Impact / 潛在影響 | Mitigation Control / 緩解控制措施 |
| :--- | :--- | :--- |
| **Keyword Evasion (語詞規避)** | User colloquialisms bypass rule matching. (口語化輸入導致未匹配) | Provide standardized UI scenario prompts; route unstructured queries to Project 2 (RAG). |
| **Over-reliance (過度依賴)** | Users treat green-light pre-audits as absolute legal immunity. (誤將預審綠燈視為法律豁免) | Enforce prominent UI disclaimers highlighting mandatory human oversight (HITL). |
| **Domain Overflow (管轄溢出)** | Users input labor or IP disputes expecting privacy answers. (誤輸入非私隱法規情境) | Enforce hardcoded refusal rules for non-privacy legal domains. |

### 🇭🇰 中文 (繁體)
* **系統風險等級**：本系統不涉及自動化決策（ADM）、不處理生物辨識特徵，評定為 **低風險 / 輔助型管治工具**。
* **威脅緩解矩陣**：如上表所示，透過標準化 UI 提示、免責聲明及硬性邊界攔截，將殘餘風險降至最低。

---

## 4. Lifecycle Management & DevSecOps (生命週期與開發安全)

### 🇬🇧 English
* **Automated Security Pipeline**: Continuous integration triggers GitHub Actions SAST scanning using `CodeQL` (semantic code analysis) and `Bandit` (Python security vulnerability checks). Code merges require 100% pass rates (`✓`).
* **Trigger-Based Maintenance**: Regulatory mapping logic is reviewed and updated within 30 calendar days of any official revisions published by the Hong Kong PCPD.
* **System Decommissioning**: Upon retirement, GitHub repositories will be archived, and all transient server instances destroyed, leaving zero residual data footprint.

### 🇭🇰 中文 (繁體)
* **自動化資安防線**：每次程式碼提交均由 GitHub Actions 自動執行 SAST 掃描（`CodeQL` 靜態語意分析與 `Bandit` Python 漏洞阻斷），必須 100% 通過（全綠燈 `✓`）方可合併。
* **觸發式維護**：當香港私隱專員公署（PCPD）發布新版指引時，管治團隊將於 30 日內完成規則庫更新。
* **系統退役**：系統停用時，GitHub 倉庫將轉為封存狀態，所有雲端實例即時銷毀，不留存任何歷史數據。
