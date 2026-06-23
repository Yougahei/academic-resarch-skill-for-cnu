# Phase-by-phase Invocation Contract (v3.9.2)

Common rules for phase-by-phase invocation across all skills in the ARS pipeline. Each skill has its own phase structure and agent roster; this file defines the shared Mode A/B framework.

## Invocation Modes

**Mode A — orchestrator-driven (default):** `pipeline_orchestrator_agent` (in `academic-pipeline` skill) runs all phases end-to-end with state tracking via Material Passport.

**Mode B — phase-by-phase (cross-session resume):** User invokes one agent per phase across sessions for long-running projects. Supports `ARS_PASSPORT_RESET=1` + `resume_from_passport=<hash>` (see `academic-pipeline/references/passport_as_reset_boundary.md`).

## Agent Bucket Classification

Per `docs/design/2026-05-18-ars-v3.9.2-agent-phase-classification.md`, agents are classified into two buckets:

**Bucket A — single-phase agents:** Stay strictly within their assigned phase for writes. Reads from upstream phases are allowed. Each skill's SKILL.md lists its Bucket A agents with their phase assignments.

**Bucket B — multi-phase agents:** Do exactly the work specified by the caller's invocation for that phase — no extension to other phases in the same call. Each skill's SKILL.md lists its Bucket B agents with their phase assignments.

## Mode B Routing

Routing into Mode B requires explicit user signal — `/ars-<mode>` slash command or `[direct-mode]` prefix. Ambiguous cross-phase input defaults to clarification per `shared/references/routing_discipline.md` and `shared/references/intent_clarification_protocol.md`.

## Enforcement

**Current (v3.9.2):** prompt-level via Phase Boundary blocks on Bucket A agents + advisory verifier (`scripts/check_pipeline_integrity.py`).

**Deferred:** Deterministic PreToolUse hook + multi-phase envelope → v3.10 active conductor (#134).
