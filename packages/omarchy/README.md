# omarchy — bar tooltip border padding + scale-safe size

| | |
|---|---|
| Upstream | [basecamp/omarchy](https://github.com/basecamp/omarchy) (MIT) |
| Fork | [greenermoose/omarchy](https://github.com/greenermoose/omarchy), tag `v4.0.4-fred.2` — [compare with v4.0.4](https://github.com/basecamp/omarchy/compare/v4.0.4...greenermoose:omarchy:v4.0.4-fred.2) |
| Packaging source | [omacom/omarchy-pkgs](https://github.com/omacom/omarchy-pkgs) `pkgbuilds/omarchy` @ release `4.0.4` (`PKGBUILD.omarchy-orig`) |
| Patched version | `4.0.4-1.3` (Omarchy packaging `4.0.4-1` + 3 patches) |
| Added | 2026-09-21 |
| Retires when | Omarchy ships a release after 4.0.4 whose bar tooltip both reserves border in padding and sizes the painted bubble so logical size × DPR is an integer physical pixel count |
| Upstream state | Issue draft in `upstream-issue-bar-tooltip.md`; not filed until Dell verification |
| **Agent handoff** | **[`HANDOFF-bar-tooltip-dell-1.25x.md`](HANDOFF-bar-tooltip-dell-1.25x.md)** — read this first when continuing hover work |

**Build model:** same git commit as the Omarchy `4.0.4` package (`_commit=c668141e…`), then apply the three local patches in `prepare()`. Never build from the fork's already-patched git tree as `OMARCHY_SRC`.

## Patch 1 — `omarchy-bar-tooltip-border-padding.patch`

Mirrors `PanelToolTip`: bubble tracks label; Text padding includes `Border.*` + control padding.

## Patch 2 — `omarchy-bar-tooltip-scale-safe-size.patch`

Adds `scaleSafeSize(logical)` for integer physical pixels at fractional DPR.

## Patch 3 — `omarchy-bar-tooltip-scale-safe-bubble.patch`

Applies `scaleSafeSize` to the **BorderSurface bubble**, not only `PopupWindow` margin.

## Verify in binary

```bash
rg -q 'tooltipBorderSpec' /usr/share/omarchy/shell/plugins/bar/Bar.qml \
  && rg -q 'scaleSafeSize' /usr/share/omarchy/shell/plugins/bar/Bar.qml \
  && rg -q 'scaleSafeSize(tooltipLabel' /usr/share/omarchy/shell/plugins/bar/Bar.qml
```
