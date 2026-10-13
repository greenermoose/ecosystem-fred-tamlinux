# Survey: Windowing Systems and Display Protocols (Wayland vs X11)

## Overview

The windowing system is the architecture responsible for displaying graphical windows on screens, coordinating input devices (keyboard, mouse, touch), and synchronizing video frames with the monitor's vertical refresh.

For four decades, the X Window System (X11) served as the standard display architecture across Unix and Linux. Today, the modern **Wayland display protocol** has superseded X11.

Tamlinux is built as a pure, native Wayland environment. This survey examines why Wayland was selected, why X11 was phased out, and how standard Wayland protocols enable Tamlinux's decoupled desktop shell.

---

## 1. Architectural Comparison Matrix

| Architectural Feature | Wayland Display Protocol | X Window System (X11 / X.Org) |
|---|---|---|
| **Upstream URL** | [wayland.freedesktop.org](https://wayland.freedesktop.org/) | [x.org](https://www.x.org/) |
| **Status in Tamlinux** | `selected` (Core display protocol) | `retired` (Legacy; Xwayland fallback only) |
| **Server Role** | The Compositor *is* the Display Server | Dedicated X Server process sits between WM and Compositor |
| **IPC Mechanism** | Unix domain sockets with binary wire protocol | X11 network protocol (large request/reply roundtrips) |
| **Client Isolation** | Strict isolation; clients cannot read others' windows or keystrokes | Open global state; any client can spy on keystrokes and screen |
| **Frame Synchronization** | "Every frame is perfect" (atomic KMS modesetting, zero tearing) | Prone to screen tearing without external compositors (picom) |
| **Multi-Monitor Refresh & DPI** | Independent per-monitor refresh rates and fractional display scaling | Single global virtual screen; struggles with mixed DPI and refresh |
| **Display Power Management** | Granular per-output DPMS (`wlopm`, compositor protocols) | Global DPMS across all outputs |
| **Legacy Codebase** | Clean, minimal modern protocol | 40+ years of legacy rendering code, core fonts, print extensions |

---

## 2. In-Depth Analysis

### Why X11 Was Phased Out
X11 was designed in 1984 for networked mainframe workstations where applications rendered basic 2D primitives (lines, text, rectangles) on a remote terminal. Over forty years, the computing model transformed: applications began rendering their own client-side pixels using OpenGL, Vulkan, and software backends, reducing the X Server to an inefficient middleman.

Critical shortcomings that led to X11's retirement:
1. **Security Vulnerabilities:** Under X11, any connected client can query the global window tree, inject arbitrary keystrokes (`XSendEvent`), and read raw keystrokes globally (`XGrabKeyboard`). A malicious background script can easily act as a keylogger.
2. **Screen Tearing and Latency:** The traditional X11 pipeline passed buffers through multiple handoffs (Client → X Server → Window Manager → Compositor → DRM/KMS), causing frame drops, latency, and screen tearing.
3. **Mixed Display Incompatibility:** X11 maps all physical displays into a single contiguous bounding box. If a user connects a 4K monitor alongside a 1080p display, X11 cannot scale them independently with fractional scaling without rendering blurring artifacts.

### The Wayland Architecture
In Wayland, Kristian Høgsberg re-engineered the display pipeline from first principles:
- **Direct Rendering:** The client renders its contents directly into a shared memory (`shm`) or GPU buffer (`dmabuf`).
- **The Compositor as Display Server:** The client simply passes a handle to this buffer to the Wayland compositor (Sway, Hyprland). The compositor coordinates directly with the Linux kernel's Direct Rendering Manager (DRM/KMS) to scan out the buffer directly to the display hardware.
- **Client Sandboxing:** Clients cannot inspect each other's buffers, snoop global keystrokes, or resize other windows without explicit compositor protocol consent.

---

## 3. Standard Wayland Protocols Powering Tamlinux

Tamlinux achieves true desktop decoupling by relying on standardized, vendor-neutral Wayland protocols rather than private compositor APIs (D125):

1. **`wlr-layer-shell-unstable-v1`:**
   - Defines desktop surfaces that live above or below normal application windows:
     - `background`: Desktop wallpaper (`tamlinux/desktop/shell/services/background`).
     - `bottom`: Desktop widgets.
     - `top`: The main status bar and panel hosts (`tamlinux/desktop/shell/bar`).
     - `overlay`: High-priority menus, popups, and lock screens.
   - Allows the Tamlinux Shell (built in Quickshell) to reserve display edge space ("struts") seamlessly on both Sway and Hyprland.

2. **`ext-workspace-v1`:**
   - Standardized freedesktop.org protocol for discovering workspaces, tracking window counts, and switching active virtual desktops.
   - Powers Tamlinux's compositor-neutral `ProtocolState.qml` abstraction (D125).

3. **`wl_output` & Display Scaling:**
   - Reports physical dimensions, refresh rates, and display scaling factors per monitor.
   - Enables fractional scaling (e.g. Dell 1.25× display scaling) without clipping window borders or tooltips.

4. **`ext-idle-notify-v1`:**
   - Provides idle notifications so power managers can blank inactive monitors without constant CPU polling.
   - Patched in Tamlinux (`hyprland-idle-inhibit-unchanged-noop.patch`) to ensure focus events do not erroneously reset idle timers.

---

## Summary

Wayland is not an optional experimental layer in Tamlinux; it is the rock-solid foundation. By retiring X11 and building exclusively for Wayland protocols, Tamlinux provides users with a tear-free, secure, and resource-efficient desktop environment capable of powering both vintage single-screen laptops and multi-monitor developer workstations.
