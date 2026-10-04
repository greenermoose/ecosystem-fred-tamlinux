# gtk4 — Wayland dmabuf format table: munmap of the wrong pointer

| | |
|---|---|
| Upstream | [GNOME/gtk](https://gitlab.gnome.org/GNOME/gtk) (LGPL-2.1-or-later) |
| Fork | **none** — the fix is already upstream; this is a backport of GTK MR [!10166](https://gitlab.gnome.org/GNOME/gtk/-/merge_requests/10166) |
| Patched version | `1:4.22.4-1.1` (Arch `1:4.22.4-1` + patch) |
| Added | 2026-09-06 |
| Retires when | Arch ships gtk4 ≥ 4.22.5 (but not 4.23.0–4.23.2) or ≥ 4.23.3 — the hook does the comparison |

## Bug

`linux_dmabuf_format_table()` in `gdk/wayland/gdkdmabuf-wayland.c` called
`munmap(info->dmabuf_formats, …)` instead of `munmap(info->dmabuf_format_table, …)`,
punching a hole in the heap and leaving a dangling pointer. The next
`zwp_linux_dmabuf_feedback_v1.done` dereferenced it in `dmabuf_formats_free()`
→ SIGSEGV. It needs a second dmabuf feedback round, which compositors send
when the output set changes — on a machine whose outputs churn (lock-screen
teardown loop, hotplug), that is every few seconds.

**Blast radius:** every GTK4 Wayland application.

**Evidence:** nautilus core dump 2026-09-05 07:45:13; faulting address
page-aligned with a 2-page hole exactly `16 × 395 = 6320` bytes wide, matching
the munmap's arguments.

## Verify the shipped binary

```bash
DEBUGINFOD_URLS= gdb -q -batch -ex 'disassemble /s linux_dmabuf_format_table' /usr/lib/libgtk-4.so.1 \
  | grep -q 'mov    0x20(%rdi),%rdi' && echo patched
```

Offset `+0x20` is `dmabuf_format_table`; the crashing build loaded `+0x28`
(`dmabuf_formats`).

## Files

`PKGBUILD` (diff against `PKGBUILD.arch-orig` is the whole change), the patch,
Arch's own `*.hook`/`*.script` install hooks (unchanged, sourced by the
PKGBUILD), and — on the machine — `/etc/pacman.d/hooks/50-gtk4-local-patch.hook`,
`/usr/local/bin/gtk4-local-patch-check`, `/var/lib/gtk4-local-patch/`.

Rollback: `pkexec pacman -U /var/cache/pacman/pkg/gtk4-1:4.22.4-1-x86_64.pkg.tar.zst`.
