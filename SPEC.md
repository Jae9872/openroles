# SPEC.md — System Specification & Invariants
# Project: openroles | Date: 2026-11-03

## 1. Goal & Non-Goals
- **Primary Goal:** Free forever portal: every live role at funded startups, freshnessStamped, human-trail — seekers never pay
- **Non-Goals:** No bloated unverified dependencies; no untrusted multi-agent decision splits.

## 2. System Architecture & Invariants
- **INV-01 (Machine Proof):** Every card must produce a deterministic exit-code 0 check in `reports/<CARD>.json`.
- **INV-02 (Maker-Checker):** The agent writing code cannot self-certify its readiness audit.
- **INV-03 (Frontend via Stitch MCP):** All UI screens must be generated from this SPEC using Stitch MCP.

## 3. Acceptance Verification Table
| Test ID | Requirement | Verifier Command | Expected Output |
|---|---|---|---|
| T-01 | Baseline health check | python3 scripts/playground up | [ONLINE] |
| T-02 | Core test suite | pytest tests/ | passed |
| T-03 | UI Screen Generation | python3 -m stitch_verify | screens generated |
