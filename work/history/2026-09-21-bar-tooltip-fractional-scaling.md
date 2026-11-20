# Session: 2026-09-21 — Omarchy bar tooltip fractional scaling fixes (4.0.4-1.3)

- **CLI Tool**: Cursor `3.21.16`
- **Model**: `composer`
- **Commits**: `a98764c`, `270d3e6`, `32f25b1`
- **Transcript**: Retained privately by the author.
- **Participants**: Fred, Cursor (Composer)

## Decisions and Implementation

- Shared bar tooltip in Omarchy's `Bar.qml` clipped bottom border and chrome on fractional scales (Dell S2725DSM at 1.25×).
- Created a 3-patch stack on fork tag `v4.0.4-fred.2`:
  1. `omarchy-bar-tooltip-border-padding.patch` (`afe057b0`): reserves border padding like `PanelToolTip`.
  2. `omarchy-bar-tooltip-scale-safe-size.patch` (`dd0ad03c`): adds `scaleSafeSize` helper ensuring integer physical pixels.
  3. `omarchy-bar-tooltip-scale-safe-bubble.patch` (`6edc29cc`): applies scale-safe sizing to the `BorderSurface` bubble itself.
- Registered package `omarchy 4.0.4-1.3` and documented verification in `HANDOFF-bar-tooltip-dell-1.25x.md`.
