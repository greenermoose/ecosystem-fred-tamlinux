# hyprland — three fixes for a desktop that blanks and sleeps on schedule

| | |
|---|---|
| Upstream | [hyprwm/Hyprland](https://github.com/hyprwm/Hyprland) (BSD-3-Clause) |
| Fork | [greenermoose/Hyprland](https://github.com/greenermoose/Hyprland), tag `v0.56.2-fred.3` — [compare with v0.56.2](https://github.com/hyprwm/Hyprland/compare/v0.56.2...greenermoose:Hyprland:v0.56.2-fred.3) |
| Patched version | `0.56.2-3.3` (Arch packaging tag `0.56.2-3` + 3 patches; only `hyprland` and `hyprland-debug` are built, `hyprpm` is left to Arch) |
| Added | 2026-09-13 (patch 1), 2026-09-17 (patches 2 and 3) |
| Retires when | an Arch hyprland release containing **all three** fixes. If only some land first, drop those patches from the PKGBUILD and rebuild as `<arch>.1` |
| Upstream state | patch 1 was filed as [#16290](https://github.com/hyprwm/Hyprland/pull/16290) and closed 2026-09-17 by the vouch bot; patches 2 and 3 were never filed. None will be (re-)filed — hyprwm's AI-usage policy bans AI-authored PRs and these are AI-authored. The draft texts stay in `upstream-pr.md` as documentation |

**Build model:** the same release tarball as Arch, so `GIT_COMMIT_HASH` and the
plugin-ABI string are unchanged and `hyprbars` keeps loading. Never build this
from the fork's git tree.

## Patch 1 — `patch/monitor-inherit-dpms-on-connect`: a monitor that connects while DPMS is off stays dark

`CMonitor::onConnect()` (`src/output/Monitor.cpp`, new-monitor path) brought
every new monitor up enabled — `m_dpmsStatus` defaults to `true`,
`setEnabled(true)` before `applyMonitorRule()` — without consulting
`g_pCompositor->m_dpmsStateOn`. Many panels drop HPD ~6 s after losing signal
and reconnect ~1 s later (input auto-scan), so every DPMS-off re-created the
monitors **lit**: the blank lasted ~8 s. Each re-creation is also a cold DP
link training, which on a bus-powered USB-C panel intermittently comes up
jittering.

The patch sets `m_dpmsStatus` from the compositor-wide state and commits the
output with that enabled-state. The monitor is still registered (wl_output,
workspaces, layout) but not lit and not link-trained; every DPMS-on path goes
through `setDPMS(true)` and enables it as any other DPMS-off monitor. With
DPMS on (default, startup) nothing changes.

*Evidence:* 2026-09-13, 15 s idle timeout: hypridle `removed iface`/`got iface`
pairs at +6.3 s and +8.4 s after `dpms off`; compositor log `Modesetting DP-2`
on each reconnect. Upstream discussions #5557 / #8377 describe the symptom.

## Patch 2 — `patch/idle-notify-inhibit-unchanged-noop`: an unchanged inhibit re-evaluation no longer resets idle timers

`CIdleNotifyProtocol::setInhibit()` (`src/protocols/IdleNotify.cpp`) called
`update(0)` on every inhibitor-obeying notification whenever it was invoked,
even when `inhibited == isInhibited`. `update(0)` resets the notification
(sends `resumed` if idled) and restarts its timer. `setInhibit(false)` is
reached from `recheckIdleInhibitorStatus()` on **every window focus change**,
so anything that focuses a window while idle — a hotplug handler re-anchoring
focus, a notification, an app opening a window — counted as user activity for
every ext-idle-notify client. hypridle's 300 s rule fired forever and its
1800 s suspend rule was never reached.

The patch returns early when the state is unchanged. Real transitions still
restart timers; hardware input (`onActivity()`) is untouched. A DEBUG log line
marks the skipped case so the binary can be checked.

*Evidence:* 2026-09-16/17 overnight: 85 `Idled`/`Resumed` pairs 7–8 s apart,
23:38 → 06:50, no suspend.

*Behavioural change:* a program focusing a window while the desktop is idle no
longer resets the idle clock unless it holds an idle inhibitor (video players
do). That is the protocol's intent, but it is a change.

## Patch 3 — `patch/dpms-state-per-monitor`: a per-monitor `dpms off` no longer wakes on input elsewhere

`g_pCompositor->m_dpmsStateOn` is what `misc:mouse_move_enables_dpms` and
`misc:key_press_enables_dpms` consult: while it is false, any pointer or
keyboard event runs `dpms(ENABLE, nullopt)` and lights **every** monitor. The
dpms dispatcher (`Actions::dpms`, `src/config/shared/actions/ConfigActions.cpp`)
assigned that flag from the last monitor it touched, even with a monitor
filter, so `dpms off <one monitor>` marked the whole compositor DPMS-off and
the next mouse move on a lit monitor switched the blanked one back on. The
wlr-output-power-management path (`src/protocols/OutputPower.cpp`) never
updated the flag at all.

The patch derives the flag in `CMonitor::setDPMS()` (and `onDisconnect()`)
from every enabled monitor — false only when all are off — and drops the
assignment from the dispatcher. It also remembers, by output name, monitors
that were switched off, and `onConnect()` (patch 1's hook) brings a returning
output up dark if its name is remembered: without that, a panel that drops
HPD after losing signal and reconnects a second later would come back lit
after every per-monitor blank. An unfiltered `dpms on` (what the input-driven
wake issues) forgets all names; a per-monitor `dpms on` forgets that one. No
class layout changes, so plugins built against unpatched headers are fine.

*Evidence:* 2026-09-17 23:02, three-monitor desktop: an idle per-monitor blank
of HDMI-A-1 went dark on time and came back on as soon as the pointer moved
on DP-1 — no input on HDMI-A-1, no hypridle `Resumed`, no dpms-on dispatch.

*Behavioural change:* with only some monitors dark, input on a lit monitor no
longer wakes the dark ones; with all dark, input wakes everything as before.

## Verify the shipped binary

```bash
strings /usr/bin/Hyprland | grep -c 'connected while DPMS is off'   # 1
strings /usr/bin/Hyprland | grep -c 'inhibit state unchanged'       # 1
strings /usr/bin/Hyprland | grep -c 'compositor-wide'               # 1
```

Behaviourally, with `timeout = 15`/`60` in `hypridle.conf`: `Idled` at 15 s,
the HDMI panel's HPD pair at +7/+8 s, **no `Resumed`**, then the 60 s rule's
`Idled`; `sleep 20; hyprctl dispatch 'hl.dsp.focus({ monitor = "DP-1" })'`
while dark produces no `Resumed`, whereas a mouse move does. For patch 3:
`hyprctl dispatch 'hl.dsp.dpms({ action = "off", monitor = "HDMI-A-1" })'`,
then move the mouse on another monitor — HDMI-A-1 stays dark and
`hyprctl monitors -j` shows `dpmsStatus: false` for it only. The running
compositor keeps the old binary — log out and back in after installing.

## Files

`PKGBUILD` / `PKGBUILD.arch-orig`, the three patches (exported from fork commits
`68a4dfe2`, `a7a03d6f` and `3e4303a7`, in that order), `50-hyprland-local-patch.hook`,
`hyprland-local-patch-check`, `upstream-pr.md` (draft texts, not to be filed).
Rollback: Arch's `hyprland-0.56.2-2` package, then log out and back in.
