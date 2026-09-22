# Upstream issue draft — bar tooltip clips on fractional scale

**Do not file until Fred confirms Dell verification of the local patch.**

Re-check Basecamp/`omacom` contributing rules and AI disclosure requirements
before posting (`docs/agent-guides/upstream-engagement.md`).

---

## Title

Bar tooltip clips bottom border on fractional display scales (e.g. 1.25×)

## Body

### Summary

The shared bar tooltip in `shell/plugins/bar/Bar.qml` sizes its bubble as
`tooltipLabel.implicitWidth + 20` / `implicitHeight + 14` and centers the
label. It does not reserve the inset `BorderSurface` border in that budget.
On fractional scales (reproduced on a Dell S2725DSM at **1.25×**), the bottom
border and version footer clip. Integer scale (1.0) and often 1.5× hide the
shortfall.

`PanelToolTip` already does this correctly: Text padding includes
`Border.*` + `Style.spacing.controlPadding{X,Y}`.

### Repro

1. Use a top bar on an output with fractional scale (1.25×).
2. Hover a multiline `tooltipText` widget (e.g. display info, sysinfo, agents).
3. Observe missing/clipped bottom border on the tooltip chrome.

### Expected

Full border and padding matching `PanelToolTip`.

### Proposed fix

Three commits on fork tag `v4.0.4-fred.2` (padding, `scaleSafeSize`, bubble sizing):

https://github.com/basecamp/omarchy/compare/v4.0.4...greenermoose:omarchy:v4.0.4-fred.2

Local package: `omarchy 4.0.4-1.3` via
https://github.com/greenermoose/omarchy-fred-ecosystem/tree/main/packages/omarchy

Handoff for agents: `packages/omarchy/HANDOFF-bar-tooltip-dell-1.25x.md`

### AI disclosure

Diagnosis, patch, packaging, and this draft were produced with Cursor
(Composer) under Fred's direction. The human verified the clip on Dell and
will re-verify after upstream lands.

---

Filed: **not yet**

## Update 2026-09-21 — scale-safe size + bubble

Border padding alone was insufficient. A second patch adds
`scaleSafeSize` so `size × devicePixelRatio` is an integer physical pixel
count. A third patch applies that sizing to the painted `BorderSurface`
bubble (not only `PopupWindow`), otherwise empty margin grows and the
border still clips. Local package: `4.0.4-1.3` / tag `v4.0.4-fred.2`.
