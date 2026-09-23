# aquamarine — fix the CRTC wedge and shutdown crash

| | |
|---|---|
| Upstream | [hyprwm/aquamarine](https://github.com/hyprwm/aquamarine) (BSD-3-Clause) |
| Fork | [greenermoose/aquamarine](https://github.com/greenermoose/aquamarine), tag `v0.15.0-fred.2` — [compare with v0.15.0](https://github.com/hyprwm/aquamarine/compare/v0.15.0...greenermoose:aquamarine:v0.15.0-fred.2) |
| Authors | **Nico Duldhardt (klaudworks)** wrote the KMS fix in upstream [PR #395](https://github.com/hyprwm/aquamarine/pull/395), carried unchanged; Codex API (GPT-6), directed by Fred, wrote the null connector guard |
| Patched version | `0.15.0-2.2` (Arch `0.15.0-2` + two patches) |
| Added | 2026-09-11 |
| Retires when | an Arch aquamarine release contains both the KMS disable in `SDRMConnector::disconnect()` and a null connector guard in `flushAsyncCommitEvents()`. Version unknown until both land; check [#386](https://github.com/hyprwm/aquamarine/issues/386) and [#383](https://github.com/hyprwm/aquamarine/issues/383) |
| Upstream state | #395 was closed 2026-09-09 by the vouch bot; #383 remains open with no linked fix PR as of 2026-09-22. Agents never post on hyprwm/* |

## Bug

0.15.0 regression (commit `9d6fed9`, "core/drm: introduce async commits",
#363). `CDRMOutput::commitState()` now rejects any commit on a connector whose
status is not `DRM_MODE_CONNECTED`, and `SDRMConnector::disconnect()` flips the
status *first*, so the compositor's own attempt to disable the output is
refused ("drm: Cannot commit a disconnected output") and `recheckCRTCs()` only
clears aquamarine's bookkeeping ("clearing stale crtc"). The CRTC stays active
in the kernel, still routed to the vanished connector. When that CRTC is later
handed to another connector — after suspend/resume, when a bus-powered USB-C
panel and an HDMI monitor re-announce themselves in arbitrary order — every
atomic `TEST_ONLY` commit fails with `EINVAL`, all the way down to 640×480,
and the compositor can no longer present on any output while input still
works. ("Fault D" in Fred's display runbook.)

**Blast radius:** any suspend/resume or hotplug while an output is active.

**Evidence:** 2026-09-11 11:29 resume (amdgpu, direct HDMI + direct USB-C DP
Alt Mode, no dock, no MST): 648 rejected commits, DP-2 on CRTC 103 / HDMI-A-1
on CRTC 108 swapped versus the kernel.

## KMS fix

Issue a blocking disable-only modeset through the backend while the output
object is still alive, with the async commit queue for that CRTC paused
(22 lines in `src/backend/drm/DRM.cpp`). Multiple confirmations on #386.

**ABI note:** `libaquamarine.so.14` keeps its SONAME, so Hyprland and its
plugins are untouched. Hyprland loads the library at start — log out and back
in after installing.

## Shutdown crash fix

On 2026-09-22 at 18:59:18, Hyprland segfaulted while SDDM stopped for GPU
recovery. GDB showed a null `connector` in `CDRMBackend::flushAsyncCommitEvents()`
at `DRM.cpp:500`. `CDRMBackend::~CDRMBackend()` clears connector slots as it
disconnects them; disconnecting a later output calls `cancelAsyncOutput()` and
then `flushAsyncCommitEvents()`, which visits the already-cleared slots. The
installed Aquamarine 0.15.0 binary dereferenced one of those null slots. A
2026-09-17 ordinary compositor stop had the same stack. [Upstream issue
#383](https://github.com/hyprwm/aquamarine/issues/383) independently reports
the exact stack and a tested one-line guard.

The second patch checks `connector` before `connector->output`. It changes no
public API or library SONAME. The first KMS patch remains intact.

## Verify the shipped binary

```bash
strings /usr/lib/libaquamarine.so.0.15.0 | grep -q 'Disabled KMS output' && echo patched
grep -n 'if (connector && connector->output' \
  /usr/src/debug/aquamarine/aquamarine-0.15.0/src/backend/drm/DRM.cpp
```

The live log then shows `drm: Disabled KMS output <name> before disconnect` on
every unplug/suspend and zero `failed to commit: Invalid argument`.
The installed debug source at line 500 must show the null connector guard;
the packaged library's disassembly must branch over the next dereference when
the connector pointer is zero.

## Files

`PKGBUILD` / `PKGBUILD.arch-orig`, `aquamarine-disable-kms-before-disconnect.patch`
(fork commit `cf638ba`), `aquamarine-guard-null-connectors.patch` (patchset
commit `1cda9c3`), `50-aquamarine-local-patch.hook`, and
`aquamarine-local-patch-check`. Rollback: Arch's `aquamarine-0.15.0-2` package,
then log out and back in; that rollback removes both fixes.
