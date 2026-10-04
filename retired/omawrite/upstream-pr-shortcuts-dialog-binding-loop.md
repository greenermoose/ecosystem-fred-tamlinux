# Upstream PR draft — omacom/omawrite

Status: **filed 2026-09-17** as https://github.com/omacom/omawrite/pull/72 after
Fred confirmed the local build (`0.5.0-1.4`). Branch
`fix-shortcuts-dialog-binding-loop` on the `greenermoose/omawrite` fork,
checkout at `~/Code/omawrite` (commit `fab54d3`).

## Title

Fix the implicitWidth binding loop reported by the shortcuts dialog on every launch

## Body

Every launch of Omawrite 0.5.0 logs this four times, before any dialog is opened:

```
qrc:/Main.qml:327:5: QML Dialog: Binding loop detected for property "implicitWidth":
qrc:/qt-project.org/imports/QtQuick/Controls/Material/Dialog.qml:14:5
```

It comes from the Ctrl+? "Keyboard shortcuts" `Dialog`, which assigns a bare
`Label` as its `contentItem`. Material's `Dialog.qml` derives `implicitWidth`
from the content item's implicit width, and with a custom content item that
value feeds back into the popup's own sizing while the binding is still being
evaluated, so QML flags a loop. The dialog still renders and sizes correctly,
which is why it is easy to miss; it is also easy to miss because Qt routes the
message to journald rather than stderr whenever stderr is not a TTY.

Declaring the `Label` as a child of the `Dialog` instead (so the default
content item owns the sizing) removes the loop with identical geometry —
measured offscreen with Qt 6.11.2: implicit size 269.6 × 456 before and
after, warnings 2 → 0. Wrapping the label in a `Column` while keeping
`contentItem:` does not help; the loop is in the custom-content-item path.

The added test loads `Main.qml`, opens the dialog, and fails on any
"Binding loop detected" message. It fails against the current dialog (2 loops)
and passes with this change.

Reproduce on stock 0.5.0:

```
QT_FORCE_STDERR_LOGGING=1 QT_QPA_PLATFORM=offscreen timeout -s TERM 4 omawrite some.md 2>&1 | grep -c 'Binding loop'
# 4 before, 0 after
```

## Diff to submit

The `src/Main.qml` and `tests/tst_omawrite.cpp` hunks of
`~/pkgs/omawrite/omawrite-shortcuts-dialog-binding-loop.patch` (drop the `#`
header; it applies to upstream `main` at line 327 with a 5-line offset because
the local tree also carries the close-button and stale-dialog patches, so
regenerate against a clean checkout). The `objectName: "shortcutsDialog"` line
exists only so the test can find the dialog.

Commit trailers per Fred's conventions: `Co-authored-by: Antigravity <antigravity-bot@users.noreply.github.com>` is for Antigravity-developed work only — this one was Claude-assisted, so use
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
