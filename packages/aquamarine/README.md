# aquamarine — fix the shutdown crash (the CRTC wedge fix is now upstream)

| | |
|---|---|
| Upstream | [hyprwm/aquamarine](https://github.com/hyprwm/aquamarine) (BSD-3-Clause) |
| Fork | [greenermoose/aquamarine](https://github.com/greenermoose/aquamarine), tag `v0.15.1-fred.1` — [compare with v0.15.1](https://github.com/hyprwm/aquamarine/compare/v0.15.1...greenermoose:aquamarine:v0.15.1-fred.1) |
| Authors | Codex API (GPT-6), directed by Fred, wrote the null connector guard. Until 0.15.0-2.2 the rig also carried **Nico Duldhardt (klaudworks)**'s KMS fix from upstream [PR #395](https://github.com/hyprwm/aquamarine/pull/395) |
| Patched version | `0.15.1-1.1` (Arch `0.15.1-1` + one patch) |
| Added | 2026-09-11; rebased onto 0.15.1 on 2026-10-04 |
| Retires when | an Arch aquamarine release contains a null connector guard in `flushAsyncCommitEvents()`; check [#383](https://github.com/hyprwm/aquamarine/issues/383) |
| Upstream state | #383 is open, and v0.15.1 has no guard (checked 2026-10-04). Agents never post on hyprwm/* |

## Shutdown crash fix

On 2026-09-22 at 18:59:18, Hyprland segfaulted while SDDM stopped for GPU
recovery. GDB showed a null `connector` in `CDRMBackend::flushAsyncCommitEvents()`
at `DRM.cpp:500`. `CDRMBackend::~CDRMBackend()` clears connector slots as it
disconnects them; disconnecting a later output calls `cancelAsyncOutput()` and
then `flushAsyncCommitEvents()`, which visits the already-cleared slots. The
installed Aquamarine 0.15.0 binary dereferenced one of those null slots. A
2026-09-17 ordinary compositor stop had the same stack. [Upstream issue
#383](https://github.com/hyprwm/aquamarine/issues/383) independently reports
the exact stack and a tested one-line guard. v0.15.1's `flushAsyncCommitEvents()`
is unchanged, so the patch stays.

The patch checks `connector` before `connector->output`. It changes no public
API or library SONAME (`libaquamarine.so.14`), so Hyprland and its plugins are
untouched. Hyprland loads the library at start — log out and back in after
installing.

## Retired: the KMS-disable fix (CRTC wedge, "Fault D")

0.15.0 regression (commit `9d6fed9`, "core/drm: introduce async commits",
#363): `SDRMConnector::disconnect()` flipped the connector status before the
compositor's disable commit, so the CRTC stayed active in the kernel. After
suspend/resume every atomic commit then failed with `EINVAL`, and the
compositor could not present on any output. Evidence: 2026-09-11 11:29 resume,
648 rejected commits, CRTCs 103/108 swapped versus the kernel.

The rig carried klaudworks' PR #395 for it (fork tags `v0.15.0-fred.1` and
`.2`, which remain). Upstream merged the same fix as
[#410](https://github.com/hyprwm/aquamarine/pull/410) ("drm: release output on
disconnect manually", `3c3292c`), released in **v0.15.1**, which logs the same
`Disabled KMS output` line. The patch was dropped on 2026-10-04.

## Verify the shipped binary

```bash
grep -n 'if (connector && connector->output' \
  /usr/src/debug/aquamarine/aquamarine-0.15.1/src/backend/drm/DRM.cpp
strings /usr/lib/libaquamarine.so.0.15.1 | grep -q 'Disabled KMS output' && echo "upstream KMS fix present"
```

The installed debug source at line 500 must show the null connector guard.

## Files

`PKGBUILD` / `PKGBUILD.arch-orig`, `aquamarine-guard-null-connectors.patch`
(patchset commit `1291a49`), `50-aquamarine-local-patch.hook`, and
`aquamarine-local-patch-check`. Rollback: Arch's `aquamarine-0.15.1-1` package,
then log out and back in; that rollback removes the null guard only.
