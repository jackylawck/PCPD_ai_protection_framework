# 📊 Data Governance & Privacy Controls (數據管治與私隱控制)

## 1. Zero Data Retention (零數據留存政策)
本系統貫徹最高規格的數據最小化（Data Minimisation）與貫徹私隱設計（Privacy by Design）原則。
* **No PII Ingestion**: 系統設計僅接收情境描述（Scenario descriptions），禁止且無法儲存任何個人識別資訊（PII）。
* **Ephemeral Processing**: 所有用戶輸入僅在當下會話的內存（Session RAM）中進行字串比對，網頁關閉或重新整理後，資料即刻物理性銷毀。

## 2. Input Boundary Enforcement (輸入邊界控制)
* 作為企業級沙盒，系統強制要求使用者將輸入內容控制在「管理與管治情境（Management and Governance Contexts）」。
* 對於包含過多雜訊或非合規情境的輸入，系統將觸發 `Out of Scope` 機制，拒絕處理，以防範數據污染。

## 3. Audit Logging (審計軌跡)
* 為符合 ISO 42001 要求，系統生成具備密碼學特徵的 HashID（SHA-256）審計日誌。
* **Privacy-Preserving Logs**: 日誌僅記錄系統判定結果與時間戳記（Timestamp），絕不將用戶的原始敏感查詢明文寫入永久日誌檔。

## 4. Data Lineage (數據血統)
本系統不依賴外部訓練數據（Training Data）。系統的「知識」100% 來自代碼中硬編碼（Hardcoded）的 PCPD 2024《模範框架》核心分類，確保數據血統的單一真實來源（Single Source of Truth, SSOT）。
