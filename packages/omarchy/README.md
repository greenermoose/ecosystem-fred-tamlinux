# omarchy — bar tooltip border padding

| | |
|---|---|
| Upstream | [basecamp/omarchy](https://github.com/basecamp/omarchy) (MIT) |
| Fork | [greenermoose/omarchy](https://github.com/greenermoose/omarchy), tag `v4.0.4-fred.1` — [compare with v4.0.4](https://github.com/basecamp/omarchy/compare/v4.0.4...greenermoose:omarchy:v4.0.4-fred.1) |
| Packaging source | [omacom/omarchy-pkgs](https://github.com/omacom/omarchy-pkgs) `pkgbuilds/omarchy` @ release `4.0.4` (`PKGBUILD.omarchy-orig`) |
| Patched version | `4.0.4-1.1` (Omarchy packaging `4.0.4-1` + 1 patch) |
| Added | 2026-09-21 |
| Retires when | Omarchy ships a release after 4.0.4 whose bar tooltip sizes like `PanelToolTip` (border reserved in Text padding) |
| Upstream state | Issue draft in `upstream-issue-bar-tooltip.md`; not filed until Dell verification |

**Build model:** same git commit as the Omarchy `4.0.4` package (`_commit=c668141e…`), then apply the local patch in `prepare()`. Never build from the fork's git tree as `OMARCHY_SRC`.

## Patch — `patch/bar-tooltip-border-padding`

`shell/plugins/bar/Bar.qml` sized the shared bar tooltip as `text + 20/14` and
centered the label, without reserving the inset `BorderSurface` border. On
fractional scales (Dell `DP-1` @ 1.25×) that shortfall clips the bottom border
and version footer for every widget using `tooltipText` (`fred.monitor`,
`fred.agents`, `fred.sysinfo`, stock bar widgets). Custom `PopupWindow` hovers
(`fred.tides`) were unaffected.

The patch mirrors `PanelToolTip`: bubble `implicitWidth`/`Height` track the
label; Text padding includes `Border.*` + `Style.spacing.controlPadding{X,Y}`.

*Evidence:* delayed `grim` captures on Dell vs MSI/HP and vs `fred.tides` on the
same Dell output (2026-09-21).

## Verify in binary

```bash
rg -q 'tooltipBorderSpec' /usr/share/omarchy/shell/plugins/bar/Bar.qml \
  && rg -q 'controlPaddingY' /usr/share/omarchy/shell/plugins/bar/Bar.qml
```
