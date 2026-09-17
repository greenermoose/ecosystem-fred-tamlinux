# "File removed" dialog: Reload is a dead click, and the verdict goes stale when the file comes back

Status: **filed 2026-09-17** as https://github.com/omacom/omawrite/issues/73 (patch inline).

**Version:** 0.5.0 (tag `v0.5.0`, also current `main`)
**Platform:** Omarchy (Arch), Qt 6, Wayland

## What happens

Rewrite an open file with a tool that does unlink-then-create (many editors,
`git checkout`, most AI coding agents, some atomic-save libraries). Omawrite
shows the **File removed** dialog. The file is back on disk before you can
read the dialog, but the dialog never notices. Click **Reload** and nothing
happens at all — no reload, no status line, the dialog just stays open.

## Why

1. `src/backend.cpp` decides `deleted` once, at the instant `QFileSystemWatcher::fileChanged` fires:
   ```cpp
   const bool deleted = !QFileInfo::exists(path);
   ...
   emit externalChangeDetected(deleted, m_modified);
   ```
   For unlink-then-create the handler runs in the gap, so `deleted == true`.
   inotify drops the watch on the old inode, the new inode is never watched,
   and nothing re-evaluates. Confirmed by comparing the running process's
   `/proc/<pid>/fdinfo/<inotify fd>` watch list against the file's inode:
   the recreated file is not being watched.

2. `src/ExternalChangeDialog.qml` disables Reload in that state:
   ```qml
   SquareDialogButton {
       id: reloadButton
       text: "Reload"
       enabled: !root.deleted
   ```
   A disabled `Button` never emits `clicked`, so `backend.reloadFromDisk()` never runs.

3. `src/SquareDialogButton.qml` overrides `background` and `contentItem` and
   never consults `control.enabled`. The disabled Reload is painted exactly
   like an enabled primary button — bright blue, white text — so the user
   sees a working button that swallows clicks.

## Reproduce

```sh
printf 'hello\n' > /tmp/t.md
omawrite /tmp/t.md &
sleep 2
rm /tmp/t.md; sleep 0.3; printf 'rewritten\n' > /tmp/t.md
```

Dialog says "File removed". `ls /tmp/t.md` shows it exists. Reload does nothing.

## Suggested fix

Patch against v0.5.0, with two regression tests
(`reportsRemovedFileComingBack`, `reloadOfMissingFileKeepsText`):

- After reporting a removal, watch the parent directory. When the path
  reappears, re-arm the file watch and emit `externalChangeDetected(false, …)`
  if contents differ, or a new `externalFileRestored()` if they are
  byte-identical (Main.qml uses that to close a stale "File removed" dialog).
- `reloadFromDisk()` re-checks `QFileInfo::exists()`; if the file is still
  gone it falls back to `keepExternalVersion()` and sets a status line, so
  Reload is never a dead click.
- Drop `enabled: !root.deleted` on Reload; give `SquareDialogButton` an
  `opacity: enabled ? 1 : 0.45` so any future disabled button looks disabled.

Patch: (attach `omawrite-stale-file-removed-dialog.patch`, strip the local
header comment). Happy to open it as a PR if that is preferred.
