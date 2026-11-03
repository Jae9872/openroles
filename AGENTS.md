# AGENTS.md — project session bootstrap

Any agent working in THIS folder must do, at session start, before anything else:

1. Run: `architect check` — logs new commits + card reports into BRIEF.md (JSON lines).
2. Run: `architect start` — writes SESSION.md (rules + plan + current card + output contract).
3. Read `SESSION.md` and do SECTION 4 only. Do not drift.
4. When the card finishes or gets blocked: write `reports/<CARD>.json` EXACTLY:
   {"card":"C1","status":"done|blocked","when":"<iso>","command":"<real run>","output":"<real output>","files":[],"note":""}
   English claims alone are NOT done.
5. Then run `architect check` again and let the brief classify it.

Never edit BRIEF.md's ONE-LINE / PLAN sections manually. CHANGE LOG = append JSON lines only.
architect missing? Read README.md + skills/<stage>/SKILL.md, obey the SESSION.md contract anyway.
