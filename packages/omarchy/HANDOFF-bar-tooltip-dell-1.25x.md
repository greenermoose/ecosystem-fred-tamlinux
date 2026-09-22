# Handoff — Omarchy bar tooltip clip (Dell 1.25×)

**Start here** if you are picking up Fred's bar-hover / tooltip clipping work after another agent session (2026-09-21, Cursor).

## Status (machine state)

| Item | Value |
|------|--------|
| Installed package | `omarchy 4.0.4-1.3` (`pacman -Q omarchy`) |
| Local repo | `[local-patches]` → `/var/cache/local-patches/` |
| Fork tag | `v4.0.4-fred.2` @ `6edc29cc` ([greenermoose/omarchy](https://github.com/greenermoose/omarchy)) |
| Patches (3) | border padding → scale-safe helper → **bubble** sizing (not PopupWindow-only) |
| Registry | `omarchy-fred-ecosystem` entry `packages/omarchy/` + `ecosystem.json` |
| Hook stamp | `/var/lib/omarchy-local-patch/patched-version` → `4.0.4-1.3` |
| Reload after install | `omarchy-qmlcache-purge && omarchy-restart-shell` (reboot **not** required) |

Verify on disk:

```bash
rg 'scaleSafeSize\(tooltipLabel' /usr/share/omarchy/shell/plugins/bar/Bar.qml
omarchy-fred-ecosystem verify omarchy
```

## Problem

Shared bar tooltip in `shell/plugins/bar/Bar.qml` clips the **bottom border** on Dell **DP-1 @ 1.25×** for widgets using `tooltipText` (`fred.monitor`, `fred.agents`, `fred.sysinfo`, workspaces, stock bar). Custom plugin popups (`fred.tides`) were fine.

Root cause (confirmed in session):

1. Bubble did not reserve inset border in Text padding (fixed patch 1, like `PanelToolTip`).
2. Fractional DPR → non-integer physical height (patch 2 `scaleSafeSize`).
3. **1.2 regression:** `scaleSafeSize` on `PopupWindow` only grew transparent margin; patch 3 applies sizing to the **BorderSurface bubble** + `anchors.centerIn` on the label.

## What is done

- Fork commits on `patch/bar-tooltip-scale-safe-size` / tag `v4.0.4-fred.2`.
- Built, published, installed `4.0.4-1.3` on this workstation.
- `omarchy-fred-ecosystem verify omarchy` **PASS** (when stamp matches).
- Automated Dell `grim` captures (Fred-assisted): right-bar hovers (`fred.monitor`, `fred.agents`, `fred.sysinfo`) looked **OK** in accent-pixel analysis (`bot/top ≈ 2.5`). Workspace hovers **1–5** were hard to capture reliably in one script; left-side crops often had **no tooltip** (timing) — do **not** treat old `ws*- CLIPPED?` analyzer output as proof without a fresh Fred-held hover.

## What is **not** done / next agent

1. **Fred sign-off on Dell** — deliberate hovers with `fred-plugin-hover` choreography ([`docs/agent-guides/plugin-hover-messages.md`](file:///home/fred/docs/agent-guides/plugin-hover-messages.md), [`docs/agent-guides/omarchy-customization.md#screenshots-of-hover-states`](file:///home/fred/docs/agent-guides/omarchy-customization.md)). Targets: workspace **1, 2, 4, 5** (previously bad heights), plus `fred.monitor` / `fred.agents` / `fred.sysinfo`.
2. **Upstream issue** — draft only: `upstream-issue-bar-tooltip.md`. Do **not** file until Fred confirms verification (see [`docs/agent-guides/upstream-engagement.md`](file:///home/fred/docs/agent-guides/upstream-engagement.md)).
3. **Workspace horizontal slide** — tooltips stay pinned to output left edge on wide workspace hovers (`PopupAdjustment.Slide`); separate from bottom-border clip; out of scope unless Fred asks.
4. **Push fork tag** if `git ls-remote origin v4.0.4-fred.2` is empty: `git push origin v4.0.4-fred.2` and ensure `fred` / `patchset/v4.0.4` match.

## Rebuild recipe (if needed)

Runbook: [`docs/agent-runbooks/local-package-patching.md`](file:///home/fred/docs/agent-runbooks/local-package-patching.md).

```bash
cd ~/pkgs/omarchy
# Build from upstream _commit + patches — NOT OMARCHY_SRC=~/Code/omarchy (already patched)
makepkg -Cf
cp omarchy-4.0.4-1.3-*.pkg.tar.zst /var/cache/local-patches/
repo-add /var/cache/local-patches/local-patches.db.tar.zst /var/cache/local-patches/omarchy-4.0.4-1.3-*.pkg.tar.zst
pkexec pacman -Sy --noconfirm local-patches/omarchy
pkexec bash -c 'printf "%s\n" "4.0.4-1.3" > /var/lib/omarchy-local-patch/patched-version'
omarchy-qmlcache-purge && omarchy-restart-shell
```

**PKGBUILD note:** `if OMARCHY_SRC` / `else` branches need **separate** `sha256sums`; `updpkgsums` breaks conditional blocks.

## Evidence paths (ephemeral)

Screenshots from verification live under `/tmp/` (not committed):

- `/tmp/monitor-hover-fixed-crop.png`, `/tmp/agents-hover-fixed-crop.png`, `/tmp/sysinfo-hover-fixed-crop.png`
- `/tmp/ws-hover-fixed-*-crop.png` (may be empty of tooltip if capture missed hover)

## Related plan (do not edit)

Cursor plan: `~/.cursor/plans/scale-safe_tooltip_height_25713f94.plan.md`

## fred.agents

**No plugin change** required for this fix (uses stock bar `tooltipText`). No pending `fred.agents` commits from this hover work in `omarchy-fred-agents` or `omarchy-fred-config`.
