# Routing Discipline (v3.9.2)

The authoritative routing rules live in `.claude/CLAUDE.md` "Routing Discipline (v3.9.2)". This file summarises the routing contract that every top-level skill must honour.

## Principle

**Each skill assumes routing has already settled before it is invoked.** Ambiguous cross-phase materials should have been clarified upstream by the orchestrator or by the user-facing routing layer. A skill does not re-litigate routing decisions.

## Routing Precedence

1. **Explicit clear intent** — user invokes a specific skill via `/ars-*` slash command, or uses an unambiguous trigger keyword → route directly; no clarification, no orchestrator detour.

2. **Cross-phase materials detected** — user provides artifacts spanning ≥ 2 pipeline phases without naming a specific skill → **clarify**. Do NOT auto-route to a single-phase agent. List candidate workflows per `shared/references/intent_clarification_protocol.md`.

3. **Ambiguous intent, no materials** — user provides no artifacts and no clear request → clarify per `shared/references/intent_clarification_protocol.md`.

## Escape Hatch

`[direct-mode]` prefix (case-insensitive, byte-0 token) bypasses the cross-phase clarification gate (Step 2). The stripped message is routed per Step 1 explicit-intent handling. If the stripped message has no clear skill named, Step 1 falls through to Step 3 clarification.

## Anti-Pattern

Receiving ambiguous cross-phase materials and silently auto-routing to a single-phase agent based on which phase the materials "look closest to." This bypasses orchestrator-level reconciliation and lets the subagent inherit the full ambiguity without independent oversight.

## Forward Note (v3.10)

Active conductor (#134) will reframe this gate as structured intake with task envelope dispatch. v3.9.2 ships clarification-only as interim.
