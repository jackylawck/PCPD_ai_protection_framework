# 🔄 AI System Lifecycle Management (AI 系統生命週期管理)

## 1. Overview
本文件規範了「PCPD AI Protection Framework Evaluator」從規劃、部署、維護到退役的完整生命週期（AI System Lifecycle），確保系統運作持續符合香港個人資料私隱專員公署（PCPD）的最新指引。

## 2. Phase 1: Planning & Design (規劃與設計)
* **Objective-Driven Design**: 本系統專為企業初期 AI 專案提供「決定性預審（Deterministic Pre-audit）」。
* **Architecture Selection**: 採用基於規則的正則表達式（Rule-based Regex）架構，徹底消除大語言模型（LLM）可能產生的「幻覺（Hallucinations）」。

## 3. Phase 2: Deployment & Integration (部署與整合)
* **Stateless Operation**: 系統以無狀態（Stateless）模式部署於 Streamlit，每次重啟即清空歷史，確保零狀態殘留。
* **CI/CD Security**: 透過 GitHub Actions 強制執行 `CodeQL` 與 `Bandit` 靜態應用程式安全測試（SAST），阻斷任何含漏洞的程式碼部署上線。

## 4. Phase 3: Monitoring & Maintenance (監控與維護)
* **Trigger-based Updates**: 當 PCPD 發布新版《模範框架》或相關執法指引時，管治團隊將於 30 日內更新系統的關鍵字詞庫（Keyword Lexicon）與決策樹。
* **Drift Management**: 作為決定性系統，本專案不存在機器學習的「模型漂移（Model Drift）」問題，維護重點聚焦於法規映射（Regulatory Mapping）的精準度。

## 5. Phase 4: System Retirement (系統退役)
若系統被更先進的管治工具取代，將執行標準退役程序，包括封存 GitHub 倉庫（Archiving repository）、銷毀所有本地合規日誌（Compliance Logs），並向持份者發布停用通知。
