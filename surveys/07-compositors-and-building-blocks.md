# Survey: Wayland Compositors and Compositor Building Blocks

## Overview

In a Wayland environment, the compositor is the central display authority: it acts as display server, window manager, input arbitrator, and hardware modesetting coordinator all at once.

Tamlinux conducted extensive field surveys (dated 2026-10-03 and 2026-10-08) to evaluate tiling Wayland compositors and compositor backends. While Tamlinux 0.x currently runs on **Hyprland** with the **aquamarine** rendering backend, Fred decisively chose **Sway** built on **wlroots** as the permanent long-term compositor for Tamlinux (D64, D124).

This survey details the technical, architectural, and resource trade-offs among all evaluated compositors and building blocks.

---

## 1. Wayland Compositors Comparison Matrix

| Compositor | Language | Backend / Toolkit | Layout Model | Systemd-Free (`seatd`) | CPU Software Rendering (`pixman`) | Status in Tamlinux | Role / Assessment |
|---|---|---|---|---|---|---|---|
| **Sway** | C | `wlroots` | Manual / Dynamic Tiling (i3) | Yes (First-class) | Yes (`WLR_RENDERER=pixman`) | `selected` | Chosen long-term compositor (0.7–1.0+) |
| **Hyprland** | C++23 | `aquamarine` | Dynamic Tiling (dwindle/master) | No (Assumes systemd / elogind) | No (Requires GPU GLES2/Vulkan) | `active` | Interim 0.x compositor; retiring at 1.0 |
| **Niri** | Rust | `Smithay` | Infinite Scrollable Ribbon | Yes | No (Strict hardware GL; rejects soft-EGL) | `evaluated` | Intuitive ribbon model, but GPU-bound |
| **river** | Zig | `wlroots` | Modular Dynamic (external layout) | Yes | Yes (wlroots backend) | `evaluated` | Clean layout separation, less mature IPC |
| **labwc** | C | `wlroots` | Stacking / Floating (Openbox UX) | Yes | Yes (wlroots backend) | `evaluated` | Superb floating option on wlroots |
| **Wayfire** | C++ | `wlroots` | 3D Desktop Effects (Compiz UX) | Yes | No (3D shader pipeline) | `evaluated` | Excessive GPU energy use for core shell |
| **miracle-wm** | C++ | Canonical `Mir` | Tiling | Partial | Partial | `evaluated` | Mir dependency ecosystem |
| **mangowm** | C | Custom | Lightweight Tiling | Yes | Unknown | `evaluated` | Early development; unproven multi-output |
| **Weston** | C | `libweston` | Floating Reference | Yes | Yes (`pixman` backend) | `evaluated` | Canonical reference; lacks tiling IPC |

---

## 2. In-Depth Analysis: The Compositor Choice

### Why Sway Was Selected
Sway, created by Drew DeVault, was chosen on 2026-10-03 as Tamlinux's permanent compositor based on clear, demonstrable architectural advantages:

1. **Clean, Enduring C Codebase:**
   - Sway is written in clean, disciplined C99. It avoids massive C++ template bloat and toolchain instability, ensuring fast compilation and decades of stability.
2. **First-Class Software CPU Rendering (`WLR_RENDERER=pixman`):**
   - Tamlinux is designed to run acceptably on older and lower-resource hardware (validation floor: vintage circa-2006 hardware with Intel GMA 950 or legacy Radeon/GeForce chips that lack OpenGL 3 acceleration).
   - Sway and wlroots support pure CPU rendering via `pixman`, requiring only kernel modesetting (KMS). This allows Tamlinux to boot and display a fluid graphical desktop even on machines where hardware 3D acceleration is completely broken.
3. **Pure Systemd Independence with `seatd`:**
   - Sway runs natively with `seatd`/`libseat`, allowing rootless unprivileged execution on Void Linux and antiX Linux without pulling in `elogind` or `systemd-logind`.
4. **Mature, Rock-Solid IPC Protocol:**
   - Sway inherits and stabilizes the i3 JSON IPC socket protocol. Tamlinux's shell, plugins (`fred.workspaces`, `fred.monitor`), and external scripts can discover outputs, move windows, and bind hotkeys with deterministic reliability.
5. **Decoupled User Configuration:**
   - Configuration splits cleanly into user-owned declarative settings and Tamlinux system defaults (e.g. `~/.config/sway/config.d/tamlinux-outputs.conf`, D119).

### Why Hyprland Is Being Retired at 1.0
Hyprland, created by Vaxry, is a visually impressive compositor that provided the early environment for Tamlinux 0.x. However, systematic issues led to the decision to replace it at 1.0 (D64):
1. **Rapid API Churn and Breaking Changes:** Hyprland frequently refactors internal data structures, breaking external plugins on minor point releases. (See [`hyprland-plugin-abi.md`](../../AGENTS.md)).
2. **Heavy Toolchain & Hardware Requirements:** Written in bleeding-edge C++23; requires modern GPU hardware acceleration with no viable CPU software rendering fallback for vintage hardware.
3. **Upstream AI Governance Friction:** Hyprwm maintains a strict, hostile policy regarding AI-assisted code contributions (requiring hand-vouched human signatures and banning AI pull requests outright). Because Tamlinux is actively developed through AI pair programming, carrying fixes upstream created unnecessary friction.
4. **Carried Local Patches:** Tamlinux had to maintain multiple local patches (`hyprland-dpms-off-on-connect.patch`, `hyprland-idle-inhibit-unchanged-noop.patch`, `hyprland-dpms-state-per-monitor.patch`) to prevent multi-monitor blanking loops.

### Evaluation of Niri, river, and labwc
- **Niri (Rust / Smithay):** Niri's scrollable horizontal ribbon window model is ergonomically brilliant for wide monitors. However, Niri strictly requires hardware OpenGL/Vulkan and explicitly rejects software EGL devices by default, violating Tamlinux's 2006 hardware longevity requirement.
- **river (Zig / wlroots):** river implements a fascinating design where window layouts are computed by separate external processes (e.g. `rivertile`) over Wayland protocols. While admired, its IPC ecosystem is less mature than Sway's i3 IPC, which Tamlinux plugins already target.
- **labwc (C / wlroots):** labwc is an outstanding stacking compositor implementing Openbox-style configuration on wlroots. It is kept in view as an ideal candidate for floating desktop variants.

---

## 3. Compositor Building Blocks and Backends

A compositor rarely talks to hardware directly; it uses a backend library.

### `wlroots` (`https://gitlab.freedesktop.org/wlroots/wlroots`)
- **Status in Tamlinux:** `selected`
- **Assessment:** Created by Drew DeVault and the Sway team, `wlroots` provides modular C implementations of DRM/KMS, input backends (libinput), seat management (libseat), and standard Wayland protocols without dictating window layout policy. It powers Sway, river, labwc, and Wayfire.

### `aquamarine` (`https://github.com/hyprwm/aquamarine`)
- **Status in Tamlinux:** `active` (temporary)
- **Assessment:** Hardware abstraction library extracted from Hyprland. Carried patched in `ecosystem-fred-tamlinux` (`aquamarine-guard-null-connectors.patch`) to fix a null-pointer SIGSEGV crash during output teardown. Retires when Hyprland is phased out.

### `Smithay` (`https://github.com/Smithay/smithay/`)
- **Status in Tamlinux:** `evaluated`
- **Assessment:** Modular Rust framework for building Wayland compositors (powers Cosmic Epoch and Niri). Offers strong memory safety, but currently focuses on modern GPU pipelines.

### `Canonical Mir` (`https://github.com/canonical/mir`)
- **Status in Tamlinux:** `evaluated`
- **Assessment:** Canonical's display server library powering `miracle-wm`. Tightly tied to Ubuntu packaging; less modular than wlroots.

### `Libweston` (`https://wayland.pages.freedesktop.org/weston/`)
- **Status in Tamlinux:** `evaluated`
- **Assessment:** Reusable core from the reference Weston project. Stable, but conservative in implementing advanced desktop protocols.

### `GNOME Mutter` & `KDE KWin`
- **Status in Tamlinux:** `rejected` / `evaluated`
- **Assessment:** Both are monolithic compositors deeply coupled to their respective desktop environments (GNOME Shell / KDE Plasma). Both pull in massive dependency trees (GObject introspection, KDE Frameworks) and invasive `systemd` assumptions, disqualifying them from Tamlinux's minimal, decoupled architecture.

### `Qt Wayland Compositor` (`https://doc.qt.io/qt-6/qtwaylandcompositor-index.html`)
- **Status in Tamlinux:** `evaluated`
- **Assessment:** Allows developing compositors in QML/C++. While Tamlinux uses Qt Quick for its shell, keeping the display compositor in clean C (`Sway` / `wlroots`) ensures fault isolation: if a UI widget in the shell encounters a QML engine exception, the compositor stays alive and application windows remain safe.

---

## Summary: The Tamlinux Display Stack

Tamlinux's long-term display stack combines:
1. **The Linux DRM/KMS Subsystem** (Kernel modesetting).
2. **`seatd`** (Minimal, systemd-free rootless seat management).
3. **`wlroots`** (Modular Wayland abstraction with `pixman` CPU fallback).
4. **`Sway`** (Clean C tiling compositor with i3 IPC).
5. **The Tamlinux Protocol Layer** (`ProtocolState.qml`, unifying standard Wayland protocols).
6. **The Tamlinux Shell** (Hardware-accelerated Qt Quick / QML desktop shell).
