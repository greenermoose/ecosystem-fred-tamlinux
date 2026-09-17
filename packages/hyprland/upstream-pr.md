# Draft PR for hyprwm/Hyprland

Status: **filed 2026-09-17** as https://github.com/hyprwm/Hyprland/pull/16290
(fork `greenermoose/Hyprland`, branch `monitor-inherit-dpms-on-connect`,
checkout `~/Code/Hyprland`, commit `13fd6355`). On `main` the hunk applies at an
18-line offset and the log call had to become `LOG(Log::DEBUG, ...)`; the
`Monitor.cpp` object compiles there.

## Title

monitor: inherit compositor DPMS state when a monitor connects

## Description

### Describe your PR, what does it fix/add?

`CMonitor::onConnect()` always brings a new monitor up enabled: `m_dpmsStatus`
defaults to `true` and the output is committed with `setEnabled(true)` before
`applyMonitorRule()`. It never looks at `g_pCompositor->m_dpmsStateOn`.

Many monitors drop HPD a few seconds after losing signal and reconnect
shortly after (input auto-scan — see the later comments on #5557). With DPMS
off, that hotplug destroys and re-creates the `CMonitor`, and the new one is
modeset and lit. Net effect: `dpms off` lasts about 8 seconds, then the
desktop is back on with nobody at the keyboard. On a bus-powered USB-C panel
the re-creation is also a cold DP link training that can come up marginal.

Reproduced on amdgpu with an HP 22cwa (HDMI) and an MSI MP161 (USB-C DP Alt
Mode): after `hyprctl dispatch dpms off`, hypridle's log shows a `wl_output`
removed/added pair per monitor at +6 s and +8 s, and the compositor log shows a
fresh `Modesetting` for each.

This PR sets `m_dpmsStatus` from `g_pCompositor->m_dpmsStateOn` in the
new-monitor path of `onConnect()` and commits the output with that
enabled-state. When DPMS is globally off the monitor is still registered
(wl_output, workspaces, layout; `applyMonitorRule()` records the mode, its
commit is a disable commit) but is not lit and not link-trained. All existing
DPMS-on paths (`dpms` dispatcher, `misc:mouse_move_enables_dpms`,
`misc:key_press_enables_dpms`, wlr-output-power) go through `setDPMS(true)`,
which enables a monitor with `m_dpmsStatus == false` exactly as for any other
DPMS-off monitor. With DPMS on (default, startup) nothing changes.

### Is there anything you want to mention? (unusual edge cases, things
### you might not have thought of, etc.)

- Only the new-monitor path is changed. The earlier path in `onConnect()`
  that re-applies a rule to an already-enabled monitor is left alone.
- Monitors created by a DRM lease / non-desktop outputs return before this
  point, so they are unaffected.
- `m_dpmsStateOn` is only tracked by the dispatcher; a wlr-output-power
  client that turned one monitor off does not set it, so a monitor
  reconnecting in that situation still comes up on — same as today.

### Is it ready for merging, or does it need work?

Ready. Running locally on 0.56.2 (Arch) since 2026-09-13; a 15 s idle
timeout now blanks and stays blank through the HPD reconnect, and input
wakes both monitors normally.

---

# Draft PR #2 for hyprwm/Hyprland

Status: **draft, not filed** (2026-09-17). Same fork/checkout as above
(`greenermoose/Hyprland`, `~/Code/Hyprland`); suggested branch
`idle-notify-inhibit-unchanged-noop`. The hunk is against
`src/protocols/IdleNotify.cpp`, which is identical on `main` as of 2026-09-17
(fetched raw file), so it should apply without offset.

## Title

idle-notify: do not reset notifications when the inhibit state is unchanged

## Description

### Describe your PR, what does it fix/add?

`CIdleNotifyProtocol::setInhibit()` calls `update(0)` on every
inhibitor-obeying `ext_idle_notification` each time it is invoked, whether or
not `inhibited` actually differs from `isInhibited`. `update(0)` `reset()`s the
notification — sending `resumed` if it was idled — and restarts its timer from
zero.

`setInhibit()` is reached from `CInputManager::recheckIdleInhibitorStatus()`,
which runs on every window focus change (`CFocusState::rawWindowFocus`) and
ends in `setInhibit(false)` whenever no inhibitor is active. So any focus
change while the desktop is idle is reported to every ext-idle-notify client
as activity, even though no input happened and no inhibitor appeared or went
away. Clients with several timeouts (hypridle: 5 min DPMS off, 30 min
suspend) keep firing the short one and never reach the long one.

Repro: with hypridle configured with `timeout = 15` (dpms off) and
`timeout = 60` (suspend), let it idle, then from a `sleep 20; hyprctl dispatch
focusmonitor …` (or anything that focuses a window: a notification daemon, a
monitor hotplug handler re-anchoring focus, an app opening a window) —
hypridle logs `Resumed` and the 60 s rule never fires. In practice: a monitor
that drops HPD on signal loss (input auto-scan; common) plus a bar widget that
re-anchors focus on `monitorremoved` gave 85 blank/resume cycles in one night
and no suspend.

This PR returns early from `setInhibit()` when the state is unchanged. A real
transition still updates the notifications: `true -> false` restarts the
timers (an inhibitor went away — the protocol's intent), and `false -> true`
still resets idled notifications. Only the no-op re-evaluation stops counting
as activity. Real input goes through `onActivity()` and is untouched.

### Is there anything you want to mention? (unusual edge cases, things you might not have thought of, etc.)

- Behavioural change for users: a window opening or being focused while
  idle no longer resets idle timers unless it holds an idle inhibitor
  (video players do, via idle-inhibit-unstable-v1 or the `idleinhibit`
  window rule). That matches the ext-idle-notify spec (only input and
  inhibitors count) and wlroots-based compositors.
- The DEBUG log line in the unchanged branch is there so the behaviour is
  visible in the log if anyone bisects an idle issue; drop it if too chatty.

### Is it ready for merging, or does it need work?

Ready. Running locally on 0.56.2 (Arch) since 2026-09-17.

## Diff

```diff
--- a/src/protocols/IdleNotify.cpp
+++ b/src/protocols/IdleNotify.cpp
@@ -116,6 +116,13 @@
 }
 
 void CIdleNotifyProtocol::setInhibit(bool inhibited) {
+    // Re-evaluations that do not change the inhibit state (every window focus
+    // change ends up here via recheckIdleInhibitorStatus) are not activity:
+    // do not reset the notifications or their timers.
+    if (isInhibited == inhibited) {
+        LOGM(Log::DEBUG, "idle: inhibit state unchanged ({}), ignoring", inhibited);
+        return;
+    }
     isInhibited = inhibited;
     for (auto const& n : m_notifications) {
         if (n->inhibitorsAreObeyed())
```
