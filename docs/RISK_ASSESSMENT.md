# ⚠️ AI System Risk Assessment (系統風險評估)

## 1. Risk Tiering (風險分級)
依據國際 AI 管治標準，本「決定性預審系統」不涉及機器學習預測、不處理生物辨識特徵、不進行自動化決策（Automated Decision-Making, ADM），被歸類為 **低風險（Low-Risk）/ 輔助型管理工具**。

## 2. Identified Vulnerabilities & Limitations (已識別風險與局限)
儘管為低風險，系統仍存在以下操作與技術管治限制：

| 識別風險 (Risk Identified) | 潛在影響 (Potential Impact) | 緩解措施 (Mitigation Strategy) |
| :--- | :--- | :--- |
| **Keyword Dependency (關鍵字依賴)** | 用戶使用過於口語化的詞彙（如「丟進」而非「上傳」）可能導致系統無法匹配，給出無效的 `System Ready` 狀態。 | 於 UI 介面提供標準輸入範例；引導用戶使用 RAG 沙盒（方案 B）處理非結構化語意。 |
| **Domain Overflow (管轄權溢出)** | 用戶可能誤以為本系統能處理《版權條例》或《性別歧視條例》的合規問題。 | 設置嚴格的正則表達式邊界控制，一旦偵測到無關領域，立即強制觸發紅燈拒絕作答。 |
| **False Sense of Security (虛假安全感)** | 員工可能將系統的「綠燈」視為絕對法律豁免權。 | 於系統醒目處標示免責聲明（Disclaimer），強調人為監督（Human Oversight）的不可替代性。 |

## 3. Continuous Risk Triage (持續風險評估)
專案管治負責人將定期檢視使用者輸入模式（User Input Patterns），若發現頻繁觸發邊界盲區，將透過版本更新（Versioning）來擴充決策樹字典。
