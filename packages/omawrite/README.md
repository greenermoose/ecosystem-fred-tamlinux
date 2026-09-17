# omawrite — five fixes the `omawrite-review` workflow depends on

| | |
|---|---|
| Upstream | [omacom/omawrite](https://github.com/omacom/omawrite) (MIT) |
| Fork | [greenermoose/omawrite](https://github.com/greenermoose/omawrite), tag `v0.5.0-fred.5` — [compare with v0.5.0](https://github.com/omacom/omawrite/compare/v0.5.0...greenermoose:omawrite:v0.5.0-fred.5) |
| Patched version | `0.5.0-1.5` (Arch `0.5.0-1` + 5 patches, **stacked** — apply in the order below) |
| Added | 2026-09-10; expanded 2026-09-11 ×2, 2026-09-17 ×2 |
| Retires when | Arch ships omawrite ≥ 0.5.1 with a native close button, reliable CLI opening, a working Reload in the "File removed" dialog, a loop-free shortcuts dialog and ≥ 80-column width; otherwise rebase the stack onto the new release |
| Upstream state | [#72](https://github.com/omacom/omawrite/pull/72) (PR, patch 4) and [#73](https://github.com/omacom/omawrite/issues/73) (issue with patch 3 inline) open since 2026-09-17; one PR at a time, AI use disclosed |

**Why it matters:** `omawrite-review` is how every agent on Fred's workstation
shows him a plan or draft — it launches `omawrite <file>` and verifies the
window title. Stock 0.5.0 can ignore the file argument and open `Untitled.md`,
so losing this patch set means agents cannot show their work.

## The stack (fork branch `patchset/v0.5.0`)

1. **`patch/window-close-button`** — Omawrite has no titlebar or in-window
   close control, unlike the other Omarchy desktop apps; adds one top-right
   (`WindowCloseButton.qml`).
2. **`patch/open-cli-file`** — QML startup can mark the blank editor modified
   before `main.cpp` processes argv; the `!backend.modified()` guard then
   ignored an explicit `omawrite /path/file.md`. Removes the guard for an
   explicit request.
3. **`patch/stale-file-removed-dialog`** — the backend sampled
   `!QFileInfo::exists()` once when the watcher fired; a tool that rewrites by
   unlink-then-create (agents, `git checkout`) produced a "File removed"
   verdict that was stale before the user read it, the recreated inode was
   never watched, and `SquareDialogButton` painted the disabled Reload exactly
   like an enabled one. Now re-checks, re-watches, and Reload works.
4. **`patch/shortcuts-dialog-binding-loop`** — the Ctrl+? dialog used a bare
   `contentItem: Label`, and Material's `Dialog.qml` `implicitWidth` binding
   fed back through it: four `Binding loop detected` reports per launch, sent
   to journald (Qt logs there when stderr is not a TTY). Declaring the Label
   as a child gives identical geometry with no loop.
5. **`patch/editor-width-80-col`** — the editor clamped line width to 65
   characters, wrapping standard 80-column text prematurely on wide displays;
   raises the ceiling to 80 while keeping the responsive shrink on narrow
   windows.

Each patch carries a Qt unit test in `tests/tst_omawrite.cpp`
(`closesFromWindowCloseButton`, `reportsRemovedFileComingBack`,
`reloadOfMissingFileKeepsText`, `shortcutsDialogHasNoBindingLoop`) and the
PKGBUILD's `check()` runs the suite offscreen, so `makepkg` fails if a patch
stops doing what it claims. Build with `makepkg -Cf`.

## Verify the shipped binary

```bash
strings -el /usr/bin/omawrite | grep -c 'no longer on disk'   # 1
QT_FORCE_STDERR_LOGGING=1 QT_QPA_PLATFORM=offscreen timeout -s TERM 4 omawrite ~/some.md 2>&1 | grep -c 'Binding loop'   # 0 (4 on stock)
omawrite-review /absolute/path/file.md   # Hyprland reports that exact filename in the window title
```

Windows opened before the install still run the old binary — reopen them.

## Files

`PKGBUILD` / `PKGBUILD.arch-orig`, five patches (exported from fork commits
`ba36baf`, `306f148`, `371390c`, `293ba59`, `d914ed8`),
`50-omawrite-local-patch.hook`, `omawrite-local-patch-check`, and the draft
upstream texts (`upstream-issue-stale-file-removed.md`,
`upstream-pr-shortcuts-dialog-binding-loop.md`). Rollback:
`pkexec pacman -U /var/cache/pacman/pkg/omawrite-0.5.0-1-x86_64.pkg.tar.zst`.
