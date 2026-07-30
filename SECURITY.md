# 🛡️ Security Policy (資安與漏洞揭露政策)

## Supported Versions
目前僅對最新版本提供安全性更新與維護支援。

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## CI/CD Security Pipeline (企業級防線)
本專案已全面啟用 GitHub Actions 企業級資安防線：
* **CodeQL Analysis**: 實時掃描潛在的代碼級漏洞（SAST）。
* **Bandit Python Security**: 針對 Python 執行環境阻截常見的語法安全漏洞。
* 所有提交（Commits）與合併請求（Pull Requests）必須通過上述掃描（全綠燈 `✓`）方可合併。

## Reporting a Vulnerability (漏洞通報機制)
我們高度重視企業 AI 系統的安全性。如果您在本專案中發現任何安全漏洞（Vulnerability）或數據隔離缺陷，請 **不要** 直接建立公開的 GitHub Issue。

請透過以下方式通報：
1. 前往本倉庫的 [Security Advisory] 頁面（若已啟用）私下回報。
2. 描述漏洞的重現步驟與潛在的安全影響範圍。
3. 專案的管治團隊將在 72 小時內進行分流（Triage）並評估漏洞嚴重性（CVSS）。

我們致力於以負責任的態度（Responsible Disclosure）修復並發布安全更新。
