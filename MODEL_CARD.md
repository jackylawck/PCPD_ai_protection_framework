# 📋 ISO 42001 Model Card: PCPD AI Protection Framework Evaluator

> **ISO 42001 Alignment**: Controls A.6 (AI System Impact Assessment), A.8 (Data for AI Systems), and A.9 (Transparency & Accountability).

---

## 1. System Overview & Administrative Metadata
* **System Name**: PCPD AI Protection Framework Deterministic Evaluator (方案 A：決定性預審沙盒)
* **Model Version**: v1.0.0 (Production Sandbox)
* **System Type**: Rule-based Deterministic Expert System / Pre-audit Gatekeeper
* **Primary Developer / Governance Lead**: Jacky Law (Certified ISO 42001 Lead Auditor / AIGP Candidate)
* **Last Audit Date**: 2026-07-30
* **Repository**: [jackylawck/PCPD_ai_protection_framework](https://github.com/jackylawck/PCPD_ai_protection_framework)

---

## 2. Intended Use & Application Boundaries
* **Intended Use Case**: 
  * Enterprise pre-audit classification for AI project initiation under the 2024 PCPD Model Framework.
  * Rapid risk tiering for internal HR, IT procurement, and legal compliance teams.
* **Out-of-Scope / Prohibited Uses**:
  * **Legal Advice Disclaimer**: Does not constitute binding legal counsel under the Personal Data (Privacy) Ordinance (PDPO Cap. 486).
  * **Cross-Jurisdictional Scope**: Out of scope for non-privacy legal disputes (e.g., Employment Ordinance gender discrimination, Copyright/IP ownership).

---

## 3. Governance Architecture & Deterministic Logic
* **Decision Engine**:
  * Regular Expression (Regex) matching and strict Boolean keyword mapping against PCPD 2024 Core Domains.
  * **Zero LLM Non-Determinism**: Eliminates hallucination risks by strictly adhering to pre-coded regulatory decision trees.
* **Fallback & Boundary Enforcement**:
  * Out-of-scope queries (e.g., IP, non-privacy labor law) automatically trigger hardcoded refusal responses (`Out of Scope / System Refusal`) to uphold regulatory integrity.

---

## 4. Privacy, Security & Data Protection Controls
* **Data Sovereignty**: 100% In-memory processing; zero external API telemetry or data exfiltration.
* **Data Minimization**: Users only input text scenarios. No personal identifiers (PII) are ingested or stored.
* **Auditability (ISO 42001 Control A.9.3)**: Every user query generates a local cryptographic log entry for continuous auditability.

---

## 5. System Limitations & Known Trade-offs
* **Keyword Dependency**: Highly formal phrasing is required; natural language ambiguity or colloquial phrasing may result in conservative "fallback" responses rather than direct risk mapping.
* **Mitigation Strategy**: Deployed in a **Dual-Track Defense Matrix** alongside Project 2 (RAG Advisor) to handle unstructured semantic queries.
