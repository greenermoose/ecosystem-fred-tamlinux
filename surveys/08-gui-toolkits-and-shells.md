# Survey: GUI Toolkits, Desktop Shells, and Widget Engines

## Overview

A modern Linux desktop environment consists of two distinct graphical layers:
1. **The Window Manager / Compositor:** Coordinates window positioning, tiling math, focus, and input routing (e.g. Sway).
2. **The Graphical Desktop Shell:** Renders user-facing panels, status bars, system trays, notification popups, workspace switchers, quick settings menus, and launchers.

Historically, full desktop environments (GNOME Shell, KDE Plasma, XFCE) welded these two layers together into monolithic desktop suites. Tamlinux separates them cleanly: Sway manages windows, while an independent desktop shell handles the visual presentation.

This survey examines the GUI toolkits (Quickshell, Qt 6, GTK 3/4, Astal/AGS, EWW) and shell frameworks (Tamlinux Shell, Omarchy, Waybar, Noctalia, DankMaterialShell) evaluated for Tamlinux.

---

## 1. Candidate Comparison Matrix

| Project | Category | Toolkit / Runtime | Configuration Language | Layer Shell Protocol | Status in Tamlinux | Role / Assessment |
|---|---|---|---|---|---|---|
| **Quickshell** | Shell Toolkit | Qt 6 Quick / QML | Declarative QML + JS | Native (`wlr-layer-shell`) | `selected` | Shell toolkit powering Tamlinux Shell |
| **Tamlinux Shell** | Graphical Shell | Quickshell / Qt 6 | QML + TOML | Native | `selected` | Official desktop shell (`tamlinux/desktop/shell`) |
| **Omarchy Shell** | Graphical Shell | Quickshell / Qt 6 | QML | Native | `retired` | Ancestral shell base; decoupled at 0.4.3 |
| **Qt (Qt 6)** | GUI Toolkit | C++ / QML | C++ / QML | Via QtWayland / QML | `selected` | Core UI engine powering Quickshell |
| **GTK (3 & 4)** | GUI Toolkit | C / GObject | C / XML / CSS | Via `gtk-layer-shell` | `active` | Core application toolkit (GTK4 patched) |
| **Astal / AGS** | Shell Toolkit | GTK 3/4 / GJS | TypeScript / JavaScript | `gtk-layer-shell` | `evaluated` | GJS/TypeScript desktop widgets |
| **EWW** | Shell Toolkit | Rust / GTK 3 | Yuck (S-expressions) + SCSS | `gtk-layer-shell` | `evaluated` | Standalone widgets; limited panel logic |
| **Waybar** | Status Bar | C++ / GTK 3 | JSONC + CSS | `wlr-layer-shell` | `evaluated` | Standard Wayland bar; lacks popup menus |
| **Noctalia** | Shell Suite | Native Wayland | C / Custom | Native | `evaluated` | Family of native Wayland tools |
| **DankMaterialShell**| Graphical Shell | Web / Custom | Material CSS | Custom | `evaluated` | Material Design shell |

---

## 2. In-Depth Analysis: The Desktop Shell Toolkit

### Why Quickshell Was Selected (`https://quickshell.org/`)
Quickshell, developed by outfoxxed, is a desktop shell development framework built on Qt Quick and QML.
1. **Hardware-Accelerated Declarative UI:** QML provides reactive property bindings (e.g. `text: BatteryService.percentage + "%"` automatically updates whenever the battery state changes). QML renders through Qt's hardware-accelerated scene graph, ensuring smooth 60fps animations with minimal CPU overhead.
2. **First-Class Wayland Layer Shell Integration:** Quickshell exposes native QML primitives (`PanelWindow`, `Variants`, `WlrLayershell`) that talk directly to `wlr-layer-shell`. Panels can anchor to any screen edge, configure exclusive margins, and handle keyboard grabs without external helper daemons.
3. **Multi-Monitor Awareness:** Quickshell provides `Variants` over connected Wayland outputs (`Quickshell.screens`), automatically duplicating bars and adjusting geometries when external monitors are hotplugged.
4. **Measured Memory Overhead (D126):** In peer surveys and physical workstation benchmarks, a complete multi-monitor Quickshell shell session consumes ~60–80 MB of RAM—a fraction of GNOME Shell or Electron-based shells.

### Evaluation of Alternatives: Astal, AGS, and EWW
- **Astal & AGS (Aylur's GTK Shell) (`https://astal.dev/`):** Allows building Wayland shells in TypeScript using GJS and GTK 3/4. While popular among web developers, GJS (GNOME JavaScript runtime) incurs higher memory overhead and garbage collection pauses compared to Qt's compiled QML engine.
- **EWW (ElKowars wacky widgets) (`https://github.com/elkowar/eww`):** Standalone Rust widget engine configured with Yuck S-expressions. While excellent for simple static bars, creating deep interactive menus, unified hover tooltips, and dynamic sub-panels in Yuck is awkward and fragile.
- **Waybar (`https://waybar.net/`):** The standard C++ status bar for Sway. Highly optimized and lightweight (~20-30 MB RAM). However, Waybar is strictly a bar; it cannot render complex interactive popup windows, calendar dropdowns, monitor calibration sliders, or system settings menus.

---

## 3. The Tamlinux Shell vs Omarchy: Decoupling and Independence

### Ancestry from Omarchy 4.0.4
Tamlinux's desktop shell began as an adapted checkout of Omarchy 4.0.4 (created by David Heinemeier Hansson / DHH). Omarchy introduced clean visual aesthetics:
- A slim top status bar.
- Numbered workspace pills.
- Clean typography (IBM Plex font family).
- Integrated popups for audio, network, Bluetooth, and system power.

### Why Tamlinux Decoupled Completely (0.4.3 & D136)
While Omarchy provided an initial visual template, fundamental flaws necessitated a complete, clean fork and decoupling (D102, D103, D124, D136):
1. **Hardcoded Upstream Paths & Single-Vendor Control:** Omarchy hardcoded `/usr/share/omarchy/bin`, assumed root ownership of user settings, and distributed updates through a monolithic repository that frequently broke user configurations.
2. **Unstable Packaging Hooks:** Omarchy installed invasive Pacman hooks that attempted to rewrite `/etc/pacman.conf` and user configurations on upgrades. Tamlinux froze the `[omarchy]` repository (D99) and removed all runtime references.
3. **Compositor Protocol Neutrality (D125):** Omarchy relied exclusively on private Hyprland IPC. Tamlinux rewrote the shell's state engine into a compositor-neutral `ProtocolState.qml` supporting standard Wayland protocols and Sway (D125).
4. **Unified Plugin Hover Architecture (D128):** Tamlinux replaced duplicate popup windows across plugins with a shared, standardized tooltip and version footer component (`Tam.Ui.VersionFooter`).
5. **Clean Software Ownership (D137):** Tamlinux moved all ported utilities, panels, and services into the public `tamlinux` repository under GPL-3.0-or-later. Step 0.4.3 proves that Tamlinux installs and runs on a clean machine with zero Omarchy packages, repositories, or runtime dependencies.

---

## Summary

The Tamlinux Shell represents a new category of Linux desktop:
- Lightweight and responsive (powered by **Quickshell** and **Qt Quick**).
- Decoupled and compositor-neutral (talking standard **Wayland protocols**).
- Modular and reproducible (packaged and deployed via **Nix / Home Manager**).
- Free from vendor lock-in (100% independent under **GPL-3.0-or-later**).
