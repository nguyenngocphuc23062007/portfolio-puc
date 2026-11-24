---
name: portfolio-pipeline
description: Run the portfolio design workflow, from research to a Figma file the user approves, then implementation and QA. Use when designing, redesigning or extending this portfolio.
---
# Portfolio pipeline

Each stage reads the previous output and writes its own. Do not skip either gate.

| # | Agent | Input | Output |
|---|---|---|---|
| 1 | `ux-researcher` | user's request, references | `design/01-research.md` |
| 2 | `ux-architect` | 1 | `design/02-structure.md` |
| 3a | `ui-designer` with the `frontend-design` skill | 1, 2 | 3 to 5 clearly different directions, first screen only, in Figma |
| **GATE 1** | **the user** | directions | **picks or mixes a direction in chat; do not choose for them** |
| 3b | `ui-designer` | chosen direction | `design/BRIEF.md` |
| 4 | `motion-designer`, `whimsy-injector` | 3 | `design/03-motion.md` |
| 5 | `ux-microcopy-reviewer`, `accessibility-tester` | 2, 3, 4 | fixes folded into 3 and 4 |
| 6 | `figma-handoff` | all | Figma file |
| 7 | `ui-finish-gate-reviewer` | Figma file | `design/04-finish-gate.md`, PASS or HOLD |
| **GATE 2** | **the user** | Figma link | **approval in chat** |
| 8 | `frontend-developer` | approved Figma | site |
| 9 | `accessibility-tester`, `performance-engineer`, `seo-specialist` | site | QA report, using skills `accessibility`, `core-web-vitals`, `performance`, `seo`, `best-practices`, `web-quality-audit`, `webapp-testing` |

Rules: content the user has not supplied stays in [brackets]. Feedback on Figma goes back to the earliest stage it affects.
