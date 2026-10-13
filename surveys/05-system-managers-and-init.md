# Survey: System Managers and Service Supervision (runit vs systemd)

## Overview

Process ID 1 (PID 1) is the ancestor of every process on a Linux system. It initializes the hardware, mounts filesystems, manages background services, and handles orphaned child processes.

In the Linux world, the choice of init system and service manager is a deep architectural and philosophical dividing line. Tamlinux evaluates **runit** and **systemd** against the principles of resource efficiency, deterministic behavior, and modularity.

---

## 1. Candidate Comparison Matrix

| Dimension | `runit` | `systemd` |
|---|---|---|
| **Author / Heritage** | Gerrit Pape (daemontools heritage) | Lennart Poettering, Kay Sievers, Red Hat |
| **Upstream URL** | [smarden.org/runit](https://smarden.org/runit/) | [systemd.io](https://systemd.io/) |
| **License** | BSD-3-Clause | LGPL-2.1-or-later |
| **Status in Tamlinux** | `selected` (Target init for Void / antiX base) | `active` (Current Arch base; phased out in 1.2) |
| **Lines of Code** | ~5,000 lines of pure C | ~1,500,000+ lines of C |
| **Architectural Scope** | Init, service supervision, process reaping only | PID 1, journald, udev, networkd, logind, resolved, timesyncd, homed |
| **Service Definition** | Simple executable POSIX scripts (`run`, `finish`) | Declarative `.service` INI unit files |
| **Process Supervision** | Direct parent-child supervision via `runsv` | Cgroups v2 tracking, PID file polling |
| **Restart Guarantee** | Instantaneous, deterministic restart on exit | Configurable restart rules (`Restart=on-failure`) |
| **Memory Baseline** | Sub-megabyte (~300–600 KB total RSS) | ~30–50+ MB RSS across systemd daemons |
| **Boot Speed** | Instantaneous; minimal fork/exec overhead | Fast via parallel socket activation |
| **Session Tracking** | Delegated to `seatd` / `turnstile` / `pam_rundir` | Built-in `systemd-logind` |

---

## 2. In-Depth Analysis

### The Case for `runit`
`runit` was designed by Gerrit Pape as a modern, UNIX-philosophical service supervision replacement for classic SysV init.
1. **Unrivaled Simplicity & Transparency:**
   - A service in `runit` is simply a directory containing an executable script named `./run`.
   - To enable a service: create a symlink in `/var/service/`.
   - To disable a service: delete the symlink.
   - To inspect a service: run `sv status <name>`.
   - There are no complex state machines, binary journals, or opaque D-Bus dependencies.
2. **Deterministic Supervision:**
   - In traditional SysV init or poorly configured systemd setups, a daemon that crashes might stay dead. In `runit`, `runsv` is the direct parent of the supervised process. If the daemon terminates, `runsv` detects the `SIGCHLD` immediately and restarts it deterministically.
3. **Ultra-Low Resource Footprint:**
   - `runit` consumes less than 1 MB of RAM across the entire system. On vintage 2006 hardware with limited RAM, eliminating memory-hungry background daemons directly prevents memory starvation.
4. **Fast and Clean Boot:**
   - Boots in stages: `1` (system initialization: mount filesystems, load modules), `2` (service supervision via `runsvdir`), `3` (shutdown/reboot).

### The Case for `systemd`
`systemd` is the standard init across major commercial Linux distributions (RHEL, Ubuntu, Debian, Arch, Fedora).
1. **Integrated Ecosystem:**
   - `systemd` integrates device management (`udev`), binary logging (`journald`), network management (`networkd`), and seat tracking (`logind`) into a coherent platform.
2. **Socket & D-Bus Activation:**
   - Services start on demand when their network sockets or D-Bus interfaces receive traffic, reducing cold-boot time on modern multicore systems.
3. **Cgroup Resource Sandboxing:**
   - First-class support for Linux cgroups v2, allowing fine-grained memory limits, CPU quotas, and I/O scheduling per unit.

---

## 3. Why Tamlinux Chose `runit` for its Target Base

Despite systemd's widespread adoption, Tamlinux deliberately selected **runit** for its independent base (D68, D126):

1. **Alignment with "Value per Watt" (D139):**
   - Tamlinux favors deterministic programs with minimal background activity. `systemd` introduces dozens of background worker threads, periodic timers, D-Bus listeners, and binary journal flushers that wake up the CPU unnecessarily. `runit` sleeps quietly until an event occurs.
2. **Freedom from Monolithic Scope Creep:**
   - `systemd` has continually absorbed subsystems that were historically modular (DNS resolution via `systemd-resolved`, time sync via `systemd-timesyncd`, home directory encryption via `systemd-homed`). Tamlinux prefers the Unix philosophy: decoupled tools composed through clean contracts.
3. **Session Management without systemd:**
   - A common barrier to adopting non-systemd inits on Wayland was the assumption that Wayland compositors require `systemd-logind` for DRM/input seat arbitration.
   - In modern Linux, this is solved cleanly by **`seatd`** and **`libseat`** (created by Kenny Levinsen). `seatd` provides minimal, rootless seat management in a lightweight standalone daemon (~50 KB RSS), allowing Sway to run smoothly on Void and antiX without systemd or elogind.

---

## 4. Current State and Transition Path

- **Current State (Tamlinux 0.x):** Running on Arch Linux with `systemd`. User session services in `tamlinux/desktop/shell` are explicitly decoupled from systemd-specific environment markers and D-Bus assumptions (D136).
- **Target State (Tamlinux 1.2+):** Void Linux with native `runit` service management and `seatd` seat arbitration.
