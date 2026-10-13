# Survey: Free Software Foundations & Desktop Standards

## Overview

Tamlinux exists squarely within the Free Software tradition and the cooperative ecosystem of Unix-like operating systems. Operating systems are not merely technical assemblies of code; they are social and ethical contracts between developers, tools, and users. 

This survey covers the ethical foundation provided by the Free Software Foundation (FSF), the interoperability specifications developed by freedesktop.org, and the monolithic driver and abstraction core provided by the Linux kernel.

## 1. Free Software Foundation (FSF) and User Freedom

### Context & Bookmarked Resource
- **Bookmark:** Free Software Foundation (`https://www.fsf.org/`)
- **Status:** `selected` (Core philosophical foundation)

### The Four Essential Freedoms
The Free Software definition established by Richard Stallman and the FSF in 1986 defines software freedom through four non-negotiable rights:
1. **Freedom 0:** The freedom to run the program as you wish, for any purpose.
2. **Freedom 1:** The freedom to study how the program works, and change it so it does your computing as you wish. Access to the source code is a precondition for this.
3. **Freedom 2:** The freedom to redistribute copies so you can help others.
4. **Freedom 3:** The freedom to distribute copies of your modified versions to others. By doing this you can give the whole community a chance to benefit from your changes.

### Copyleft and GPL-3.0-or-later in Tamlinux
Tamlinux distributes all of its original scripts, commands, desktop components, and documentation under the **GNU General Public License, version 3.0 or later (GPL-3.0-or-later)**.
- **Why Copyleft Matters:** While permissive licenses (MIT, BSD, Apache) allow downstream proprietary redistribution, copyleft protects the software against enclosure. It guarantees that any party redistributing Tamlinux, or deriving work from it, must grant the exact same freedoms to their end users.
- **Upstream Terms Preserved:** Third-party upstream works retain their own licenses. For example, Sway is MIT, wlroots is MIT, Hyprland and aquamarine are BSD-3-Clause, GTK4 is LGPL-2.1+, Quickshell is LGPL-3.0, and Linux is GPL-2.0. Tamlinux adheres strictly to all upstream licensing terms, and credits every upstream author in [`ACKNOWLEDGEMENTS.md`](../ACKNOWLEDGEMENTS.md).

---

## 2. freedesktop.org (XDG) Interoperability Standards

### Context & Bookmarked Resource
- **Bookmark:** freedesktop.org (`https://www.freedesktop.org/`)
- **Status:** `selected` (Architectural standard for desktop decoupling)

### Role in the Decoupled Desktop
freedesktop.org (formerly the X Desktop Group or XDG) produces the interoperability specifications that prevent the free desktop from fragmenting into incompatible vendor silos. Tamlinux implements and relies upon core freedesktop.org specifications:

1. **XDG Base Directory Specification:**
   - Defines the standard layout for user configuration, cache, and state files:
     - `$XDG_CONFIG_HOME` (`~/.config`): User-editable configuration files.
     - `$XDG_DATA_HOME` (`~/.local/share`): Persistent data files, offline knowledge pages, icons, fonts.
     - `$XDG_STATE_HOME` (`~/.local/state`): Machine/session state written by tools (e.g., display text size, welcome status).
     - `$XDG_CACHE_HOME` (`~/.cache`): Ephemeral caches that can be safely wiped without losing configuration.
   - **Tamlinux Strict Adherence (D110, D123):** Tamlinux moved all historical root-home litter (`.omarchy`, untracked config files) into strict XDG paths (`~/.config/tamlinux`, `~/.local/state/tamlinux`).

2. **Standard Wayland Protocols:**
   - Wayland protocols governed by freedesktop.org allow desktop components (like the Tamlinux Shell) to interact with the display compositor across clean boundaries:
     - `wlr-layer-shell-unstable-v1`: Allows panels, bars, wallpapers, and notification bubbles to anchor to screen edges and reserve desktop struts without taking window focus.
     - `ext-workspace-v1`: Standardizes workspace tracking and switching across compositors without requiring proprietary compositor-specific IPC (D125).
     - `ext-idle-notify-v1`: Standardizes idle notification timers so power management tools can sleep displays without polling.

3. **Desktop Entry & Icon Specifications:**
   - `.desktop` files in `/usr/share/applications` and `~/.local/share/applications` provide standard menus, icon resolution, and mime-type association for Tamlinux application launching.

4. **Desktop Notifications (`org.freedesktop.Notifications`):**
   - Standard D-Bus protocol for delivering user alerts and notifications. Tamlinux's shell implements a native D-Bus notification server (`tamlinux/desktop/shell/services/notification/`) providing clean visual popups.

---

## 3. The Linux Kernel

### Context & Bookmarked Resource
- **Bookmark:** Linux Kernel Archives (`https://www.kernel.org/`)
- **Status:** `selected` (Hardware abstraction and core OS kernel)

### Kernel Capabilities Leveraged by Tamlinux
Tamlinux operates on vanilla Linux kernels (Arch `linux`, Void `linux-vanilla`, antiX `linux-image`). The architecture relies on specific kernel subsystems:

1. **Direct Rendering Manager & Kernel Mode Setting (DRM/KMS):**
   - Atomic modesetting APIs (`/dev/dri/card*`, `/dev/dri/renderD*`) provide low-latency, tear-free display management.
   - Allows Wayland compositors (Sway, Hyprland) to talk directly to GPU scanout planes without legacy X11 server mediation.
   - Software pixman rendering paths utilize dumb buffers when hardware acceleration is unavailable on vintage 2006-class hardware.

2. **EVDEV Input Subsystem:**
   - Unified `/dev/input/event*` subsystem managed through `libinput`.
   - Provides smooth touch gestures, precise pointer acceleration, and keyboard event routing.

3. **ZRAM Swap Compression (`zram-generator`):**
   - Creates a compressed block device in RAM using `zstd` or `lz4`.
   - Essential for low-RAM machines: effectively doubles usable memory without grinding disks to thrash swap files, preventing system freezes during high memory pressure.

4. **cgroups v2 & Resource Accounting:**
   - Kernel control groups enforce resource isolation and memory ceilings, preventing runaway processes from exhausting memory.

---

## Summary: Tamlinux Cultural Alignment

Tamlinux does not seek to reinvent Unix or establish a closed walled garden. By rooting itself in FSF ethics, honoring freedesktop.org specifications, and leveraging clean Linux kernel interfaces, Tamlinux builds a modular, enduring workstation environment where the user remains the sole sovereign authority.
