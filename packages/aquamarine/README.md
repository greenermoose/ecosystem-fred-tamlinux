# aquamarine — disable the KMS pipeline before tearing down a disconnected connector

| | |
|---|---|
| Upstream | [hyprwm/aquamarine](https://github.com/hyprwm/aquamarine) (BSD-3-Clause) |
| Fork | [greenermoose/aquamarine](https://github.com/greenermoose/aquamarine), tag `v0.15.0-fred.1` — [compare with v0.15.0](https://github.com/hyprwm/aquamarine/compare/v0.15.0...greenermoose:aquamarine:v0.15.0-fred.1) |
| Author | **Nico Duldhardt (klaudworks)** — upstream [PR #395](https://github.com/hyprwm/aquamarine/pull/395), carried unchanged with authorship preserved (`git cherry-pick`) |
| Patched version | `0.15.0-2.1` (Arch `0.15.0-2` + patch) |
| Added | 2026-09-11 |
| Retires when | an Arch aquamarine release whose `SDRMConnector::disconnect()` disables KMS before the teardown. Version unknown until it lands — watch [hyprwm/aquamarine#386](https://github.com/hyprwm/aquamarine/issues/386); set `fixed_upstream_version` in the check script then |
| Upstream state | #395 was closed 2026-09-09 by the vouch bot (author not vouched). Not ours to re-file; agents never post on hyprwm/* |

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

## Fix

Issue a blocking disable-only modeset through the backend while the output
object is still alive, with the async commit queue for that CRTC paused
(22 lines in `src/backend/drm/DRM.cpp`). Multiple confirmations on #386.

**ABI note:** `libaquamarine.so.14` keeps its SONAME, so Hyprland and its
plugins are untouched. Hyprland loads the library at start — log out and back
in after installing.

## Verify the shipped binary

```bash
strings /usr/lib/libaquamarine.so.0.15.0 | grep -q 'Disabled KMS output' && echo patched
```

The live log then shows `drm: Disabled KMS output <name> before disconnect` on
every unplug/suspend and zero `failed to commit: Invalid argument`.

## Files

`PKGBUILD` / `PKGBUILD.arch-orig`, `aquamarine-disable-kms-before-disconnect.patch`
(exported from fork commit `cf638ba`), `50-aquamarine-local-patch.hook`,
`aquamarine-local-patch-check`. Rollback: Arch's `aquamarine-0.15.0-2` package,
then log out and back in.
