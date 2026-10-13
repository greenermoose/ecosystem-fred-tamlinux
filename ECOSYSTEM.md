# The Tamlinux Ecosystem: Patches, Packages, and Choices

The public record of the software, cultural, and philosophical ecosystem of [Tamlinux](https://github.com/greenermoose/tamlinux):
1. **The Carried Patch Registry:** Third-party packages Fred's workstation runs patched, and the software depending on those patches.
2. **The Considered Packages Survey:** A complete survey and record of packages, libraries, and dependencies evaluated across all operating system layers to select the optimal components for performance, user sovereignty, and resource efficiency.

The explanation of why Tamlinux makes these choices lives in the offline guide of the [`tam`](https://github.com/greenermoose/tam) command (`tam show ecosystem`, `tam explain <topic>`).

---

## Part 1: Carried Patches Registry

Generated table from [`ecosystem.json`](ecosystem.json) (`tam-ecosystem render`); the prose around it is hand-written. One row per third-party package. "Local version" is the Arch version with a `pkgrel` suffix (`<arch>.N`). The local repository is listed first in `pacman.conf`, so it holds that build until the patch is rebased or retired; a newer Arch build is reported, not installed.

<!-- registry:begin -->
| Package | Status | Local version | Fork (compare view) | Patches | Filed upstream | Retires when | Depended on by |
|---|---|---|---|---|---|---|---|
| [gtk4](patches/gtk4/README.md) | retired | `1:4.22.4-1.1` | none (upstream has it) | 1 | — | Arch ships gtk4 >= 4.22.5 (but not 4.23.0-4.23.2) or >= 4.23.3; the pacman hook does the comparison | private workstation checkout |
| [aquamarine](patches/aquamarine/README.md) | active | `0.15.1-1.1` | [v0.15.1-fred.1](https://github.com/hyprwm/aquamarine/compare/v0.15.1...greenermoose:aquamarine:v0.15.1-fred.1) | 1 | [hyprwm/aquamarine/issues/383](https://github.com/hyprwm/aquamarine/issues/383) | an Arch aquamarine release with a null connector guard in flushAsyncCommitEvents() (#383) | private workstation checkout, fred.monitor (planned) |
| [hyprland](patches/hyprland/README.md) | active | `0.56.2-4.1` | [v0.56.2-fred.3](https://github.com/hyprwm/Hyprland/compare/v0.56.2...greenermoose:Hyprland:v0.56.2-fred.3) | 3 | [hyprwm/Hyprland/pull/16290](https://github.com/hyprwm/Hyprland/pull/16290) | an Arch hyprland release containing all three fixes (onConnect() honours the compositor DPMS state; setInhibit() guards the unchanged case; a filtered `dpms off` no longer marks the compositor DPMS-off). If only some land, drop those patches and rebuild as <arch>.1 | private workstation checkout, workspaces-fred-tamlinux, fred.monitor (planned) |
| [omawrite](patches/omawrite/README.md) | retired | `0.5.0-1.5` | [v0.5.0-fred.5](https://github.com/omacom/omawrite/compare/v0.5.0...greenermoose:omawrite:v0.5.0-fred.5) | 5 | [omacom/omawrite/issues/73](https://github.com/omacom/omawrite/issues/73), [omacom/omawrite/pull/72](https://github.com/omacom/omawrite/pull/72) | Arch ships omawrite >= 0.5.1 with a native close button, reliable CLI opening, a working Reload in the 'File removed' dialog, a loop-free shortcuts dialog and >= 80-column width; otherwise rebase the stack onto the new release | private workstation checkout |
| [omarchy](patches/omarchy/README.md) | active | `4.0.4-1.3` | [v4.0.4-fred.2](https://github.com/basecamp/omarchy/compare/v4.0.4...greenermoose:omarchy:v4.0.4-fred.2) | 3 | — | Omarchy ships a release after 4.0.4 whose bar tooltip both reserves border in padding and sizes the popup so logical size × DPR is an integer physical pixel count; then retire via tam-ecosystem retire omarchy | private workstation checkout, fred.agents, fred.monitor, fred.sysinfo, fred.clock, fred.workspaces |
<!-- registry:end -->

### Reading a row

- **Fork (compare view)** opens GitHub's diff of the fork tag against the upstream release it patches — the patches in context. The fork's default branch `fred` always points at the current patch set; `patch/<slug>` holds each patch alone and `patchset/<tag>` the integration branch.
- **Filed upstream** is where a project's rules allowed posting. Where they do not (hyprwm/*), nothing is filed and the fork is the only public copy — see the policy in the [README](README.md#why-this-exists-instead-of-upstream-pull-requests).
- **Depended on by** names Fred's own repositories that need the patch to behave as documented; each carries an `ECOSYSTEM.md` at its root that says what breaks without it.

### Consumers

| Repository | Needs | Because |
|---|---|---|
| Private workstation checkout | all four | the workstation itself (aquamarine shutdown crash guard, hyprland DPMS/idle blanking, omawrite editor usability, omarchy bar tooltip scale safety) |
| [workspaces-fred-tamlinux](https://github.com/greenermoose/workspaces-fred-tamlinux) | hyprland | its per-monitor idle blanking depends on per-output DPMS isolation (patch 3); its hotplug `reconcile` focuses windows, which on stock Hyprland resets the idle clock (patch 2); and a reconnecting monitor stays dark (patch 1) |
| Omarchy bar plugins (`fred.agents`, `fred.monitor`, `fred.sysinfo`, `fred.clock`, `fred.workspaces`) | omarchy | its shared bar tooltip reserves border padding and sizes the popup so logical size × DPR is integer physical pixels; without it, bottom border clips on fractional scale (Dell 1.25×) across bar widgets |
| fred.monitor (planned) | aquamarine, hyprland | per-display reset/retrain assumes stable shutdown/reconnect (aquamarine null-connector guard #383) and DPMS-aware reconnects (the Fault D KMS teardown fix is upstream in aquamarine 0.15.1) |

### Retired Patches

Retired entries remain in [`patches/`](patches/) with their status marked retired and their full history preserved; the fork tag stays in place.

| Package | Retired | Upstream resolution |
|---|---|---|
| [gtk4](patches/gtk4/README.md) | 2026-10-04 | Arch shipped `1:4.22.5-1`, which includes GTK MR !10166 fixing the Wayland dmabuf format table munmap crash |
| [omawrite](patches/omawrite/README.md) | 2026-10-04 | Agent review workflow transitioned to `micro-review` skill; editor retired from workstation suite |

---

## Part 2: Considered Packages and Architectural Survey

Tamlinux picks and chooses among a large field of possibilities to construct an operating system that maximizes resource efficiency, hardware longevity, and user freedom.

### Evaluation Framework

- **`selected`:** Adopted for Tamlinux long-term architecture and delivery (Sway, Void Linux, runit, Nix deployment, Quickshell, wlroots, Tamlinux Shell, Btrfs).
- **`active`:** Currently in daily use in the 0.x Arch development workstation (Arch Linux, Pacman, Hyprland, aquamarine, glibc, systemd).
- **`evaluated`:** Formally surveyed and assessed as an architectural reference or alternative (Debian, Alpine, river, labwc, Astal/AGS, Smithay, Waybar).
- **`fallback`:** Designated standby target if the selected primary component encounters showstoppers (antiX Linux Core with runit).
- **`deferred`:** Scheduled for evaluation at a future milestone pending explicit triggers (Void musl vs glibc pilot at 1.2).
- **`retired`:** Previously used or supported; now systematically phased out or decoupled (Omarchy at 0.4.3; OpenClaw and Hermes support).
- **`rejected`:** Excluded due to fundamental incompatibilities with Tamlinux tenets (monolithic compositors, raw .deb/.rpm installs, non-deterministic agent daemons).

### Explanations in the `tam` guide

Chapters explaining these choices (philosophy, distributions, packaging, init, compositors, toolkits, desktop applications, C libraries, carried patches, virtualization, AI tooling, and sustainability) are part of the `tam` offline guide, in [`tam/knowledge/ecosystem/`](https://github.com/greenermoose/tam/tree/develop/knowledge/ecosystem). Read them with `tam show ecosystem`. The desktop application survey behind one of them is [`docs/desktop-application-suites.md`](docs/desktop-application-suites.md).

### Complete Considered Packages Dossier

Generated from [`ecosystem.json`](ecosystem.json) via `tam-ecosystem render`:

<!-- considered:begin -->
| Package | Category | Status | Role | License | References |
|---|---|---|---|---|---|
| [Free Software Foundation (FSF)](https://www.fsf.org/) | Free Software Foundations & Standards | **selected** | Ethical and philosophical foundation of Tamlinux user sovereignty | GPL / FDL | Core philosophy; LICENSE GPL-3.0 |
| [freedesktop.org (XDG)](https://www.freedesktop.org/) | Free Software Foundations & Standards | **selected** | Desktop interoperability standards across Linux environments | Open Specifications (MIT / CC-BY-SA) | — |
| [The Linux Kernel](https://www.kernel.org/) | Free Software Foundations & Standards | **selected** | Operating system kernel providing hardware abstraction and system calls | GPL-2.0-only | base-operating-system.md |
| [The GNU C Library (glibc)](https://sourceware.org/glibc/) | C Standard Libraries | **active** | Current standard C library on Arch Linux workstation and primary Void tier | LGPL-2.1-or-later | base-operating-system.md §C Library Evaluation |
| [musl libc](https://musl.libc.org/) | C Standard Libraries | *deferred* | Alternative C library evaluated for minimal footprint Void/Alpine profiles | MIT | base-operating-system.md §C Library Evaluation |
| [Arch Linux](https://archlinux.org/) | Operating System Distributions | **active** | Working development distribution for Tamlinux 0.x workstation | GPL-2.0 and various open-source licenses | base-operating-system.md |
| [Void Linux](https://voidlinux.org/) | Operating System Distributions | **selected** | Target base distribution for independent Tamlinux cultivar at milestone 1.2 | BSD-2-Clause and various | base-operating-system.md |
| [antiX Linux (Core)](https://antixlinux.com/) | Operating System Distributions | *fallback* | Designated fallback distribution if Void presents showstoppers | GPL and various | base-operating-system.md §Target and fallback |
| [Debian GNU/Linux](https://www.debian.org/) | Operating System Distributions | *evaluated* | Universal OS benchmark and package archive upstream | Debian Free Software Guidelines (DFSG) | base-operating-system.md |
| [Alpine Linux](https://alpinelinux.org/) | Operating System Distributions | *evaluated* | Security-oriented, ultra-lightweight musl + BusyBox reference distribution | GPL-2.0 and various | base-operating-system.md |
| [Puppy Linux](https://puppylinux-woof-ce.github.io/) | Operating System Distributions | *evaluated* | Pioneering lightweight distribution running entirely in RAM | GPL and various | — |
| [Tiny Core Linux](http://www.tinycorelinux.net/) | Operating System Distributions | *evaluated* | Modular, ultra-minimalist Linux desktop architecture | GPL-2.0 | — |
| [Gentoo Linux](https://www.gentoo.org/) | Operating System Distributions | *evaluated* | Source-based distribution benchmark for fine-grained compilation control | GPL-2.0 | — |
| [openSUSE (Tumbleweed / Leap)](https://www.opensuse.org/) | Operating System Distributions | *evaluated* | Enterprise-grade rolling and stable RPM distribution | GPL and various | — |
| [CentOS / Red Hat Enterprise Linux (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) | Operating System Distributions | *evaluated* | Enterprise Linux standard and server baseline | GPL and various | — |
| [Ubuntu & Lubuntu](https://lubuntu.me/) | Operating System Distributions | *evaluated* | Popular consumer desktop distribution and LXQt lightweight derivative | GPL and various | — |
| [Bedrock Linux](https://bedrocklinux.org/) | Operating System Distributions | *evaluated* | Meta-distribution providing cross-distro package integration | GPL-2.0 | — |
| [Nix / NixOS](https://nixos.org/) | Package Managers & Delivery Mechanisms | **selected** | Reproducible package and deployment framework for Tamlinux software | LGPL-2.1-only | — |
| [Pacman (Arch Linux)](https://pacman.archlinux.page/) | Package Managers & Delivery Mechanisms | **active** | Host package manager for the active Arch workstation and local patches | GPL-2.0-or-later | README.md; bin/tam-ecosystem |
| [XBPS (X Binary Package System)](https://docs.voidlinux.org/xbps/) | Package Managers & Delivery Mechanisms | **selected** | Target native package manager on Void Linux base | BSD-2-Clause | base-operating-system.md §Package and service ownership |
| [dpkg & APT (Debian Packaging)](https://wiki.debian.org/Packaging/Intro) | Package Managers & Delivery Mechanisms | *evaluated* | Debian package format and dependency resolver | GPL-2.0-or-later | — |
| [Portage (Gentoo)](https://wiki.gentoo.org/wiki/Portage) | Package Managers & Delivery Mechanisms | *evaluated* | Source build and dependency resolver benchmark | GPL-2.0-only | — |
| [runit](https://smarden.org/runit/) | System Managers & Service Supervision | **selected** | Selected init and service supervision system for Void/antiX base | BSD-3-Clause | base-operating-system.md §Target and fallback |
| [systemd](https://systemd.io/) | System Managers & Service Supervision | **active** | Active system manager on Arch Linux 0.x workstation; target for removal in 1.2 | LGPL-2.1-or-later | base-operating-system.md |
| [Wayland Display Protocol](https://wayland.freedesktop.org/) | Windowing Systems & Display Protocols | **selected** | Display server protocol powering the Tamlinux graphical environment | MIT | compositor-protocol-layer.md |
| [X Window System (X.Org)](https://www.x.org/) | Windowing Systems & Display Protocols | *retired* | Historic windowing architecture; phased out in Tamlinux | MIT | — |
| [Sway](https://swaywm.org/) | Wayland Compositors & Window Managers | **selected** | Selected long-term tiling Wayland compositor for Tamlinux (0.7–1.0+) | MIT | compositor survey 2026-10-03 |
| [Hyprland](https://hypr.land/) | Wayland Compositors & Window Managers | **active** | Active interim compositor on Tamlinux 0.x workstation; scheduled for removal at 1.0 | BSD-3-Clause | patches/hyprland |
| [Niri](https://github.com/niri-wm/niri) | Wayland Compositors & Window Managers | *evaluated* | Scrollable-tiling Wayland compositor written in Rust | GPL-3.0-or-later | compositor survey 2026-10-03 |
| [river](https://github.com/riverwm/river) | Wayland Compositors & Window Managers | *evaluated* | Dynamic tiling Wayland compositor written in Zig | GPL-3.0-only | compositor survey 2026-10-03 |
| [labwc](https://github.com/labwc/labwc) | Wayland Compositors & Window Managers | *evaluated* | Stacking Wayland compositor inspired by Openbox | GPL-2.0-only | compositor survey 2026-10-03 |
| [Wayfire](https://wayfire.org/) | Wayland Compositors & Window Managers | *evaluated* | 3D visual effects Wayland compositor inspired by Compiz | MIT | compositor survey |
| [miracle-wm](https://github.com/miracle-wm-org/miracle-wm) | Wayland Compositors & Window Managers | *evaluated* | Tiling Wayland compositor built on Canonical's Mir | GPL-3.0-only | compositor survey |
| [mangowm](https://mangowm.github.io/docs/) | Wayland Compositors & Window Managers | *evaluated* | Lightweight Wayland compositor | GPL-3.0-or-later | compositor survey 2026-10-03 |
| [Weston](https://wayland.pages.freedesktop.org/weston/index.html) | Wayland Compositors & Window Managers | *evaluated* | Reference Wayland compositor by the Wayland project | MIT | — |
| [wlroots](https://gitlab.freedesktop.org/wlroots/wlroots) | Compositor Building Blocks & Backends | **selected** | Modular Wayland compositor library powering Sway and Tamlinux display stack | MIT | compositor-protocol-layer.md |
| [aquamarine](https://github.com/hyprwm/aquamarine) | Compositor Building Blocks & Backends | **active** | Rendering abstraction backend for Hyprland; carried patched in Tamlinux | BSD-3-Clause | patches/aquamarine; ECOSYSTEM.md |
| [Smithay](https://github.com/Smithay/smithay/) | Compositor Building Blocks & Backends | *evaluated* | Rust framework for building custom Wayland compositors | MIT | — |
| [Canonical Mir](https://github.com/canonical/mir) | Compositor Building Blocks & Backends | *evaluated* | Display server library by Canonical | GPL-2.0 / LGPL-3.0 | Compositor survey |
| [Libweston](https://wayland.pages.freedesktop.org/weston/toc/libweston.html) | Compositor Building Blocks & Backends | *evaluated* | Reusable core compositor library from the Weston project | MIT | — |
| [GNOME Mutter](https://mutter.gnome.org/) | Compositor Building Blocks & Backends | *rejected* | Monolithic display server and compositor for GNOME Shell | GPL-2.0-or-later | — |
| [KDE KWin](https://github.com/KDE/kwin) | Compositor Building Blocks & Backends | *evaluated* | Compositor and window manager for the KDE Plasma desktop | GPL-2.0-or-later | — |
| [Qt Wayland Compositor](https://doc.qt.io/qt-6/qtwaylandcompositor-index.html) | Compositor Building Blocks & Backends | *evaluated* | QML/C++ compositor development framework in Qt | GPL-3.0 / LGPL-3.0 | — |
| [Quickshell](https://quickshell.org/) | GUI Toolkits & Widget Engines | **selected** | Desktop shell toolkit powering the Tamlinux shell, bar widgets, and panels | LGPL-3.0-only | tamlinux/desktop/shell |
| [Qt (Qt 6)](https://www.qt.io/) | GUI Toolkits & Widget Engines | **selected** | Core application and UI framework providing QML scene graph and Wayland integration | LGPL-3.0 / GPL-3.0 | tamlinux/desktop/shell |
| [GTK (GTK 3 & GTK 4)](https://www.gtk.org/) | GUI Toolkits & Widget Engines | **active** | Primary GUI toolkit for standard Linux desktop applications | LGPL-2.1-or-later | patches/gtk4; ECOSYSTEM.md |
| [Astal & AGS (Aylur's GTK Shell)](https://www.astal.dev/) | GUI Toolkits & Widget Engines | *evaluated* | TypeScript and GTK-based desktop widget system | GPL-3.0-only | — |
| [EWW (ElKowars wacky widgets)](https://github.com/elkowar/eww) | GUI Toolkits & Widget Engines | *evaluated* | Standalone widget system written in Rust with Yuck/SCSS | MIT | — |
| [The Tamlinux Shell](https://github.com/greenermoose/tamlinux) | Graphical Shells & Desktop Environments | **selected** | The official desktop shell of Tamlinux (bar, menus, plugins, indicators) | GPL-3.0-or-later | tamlinux/desktop/shell |
| [Omarchy Desktop Shell](https://github.com/omacom/omarchy) | Graphical Shells & Desktop Environments | *retired* | Ancestral desktop shell base; Tamlinux is removing its remaining dependencies in 0.4.3 | MIT | — |
| [Waybar](https://waybar.net/) | Graphical Shells & Desktop Environments | *evaluated* | Widely used modular Wayland status bar | MIT | — |
| [Noctalia](https://noctalia.dev/) | Graphical Shells & Desktop Environments | *evaluated* | Family of native Wayland desktop tools and shell components | GPL-3.0 / MIT | — |
| [DankMaterialShell](https://danklinux.com/) | Graphical Shells & Desktop Environments | *evaluated* | Material Design desktop shell for Wayland | GPL-3.0-only | — |
| [Openbox](https://openbox.org/) | X11 Window Managers (Legacy) | *retired* | Historic lightweight stacking window manager providing ergonomic precedent | GPL-2.0-or-later | — |
| [QEMU](https://www.qemu.org/) | Virtualization, Emulation & Containment | *evaluated* | Foundational machine emulator and virtualizer for testing Tamlinux on diverse architectures | GPL-2.0 | — |
| [Docker](https://www.docker.com/) | Virtualization, Emulation & Containment | *evaluated* | Containerization platform for reproducible build environments and test harnesses | Apache-2.0 | — |
| [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/) | Virtualization, Emulation & Containment | *evaluated* | Compatibility environment for running Linux toolchains on Windows | Proprietary wrapper / GPL Linux kernel | — |
| [UTM (macOS)](https://mac.getutm.app/) | Virtualization, Emulation & Containment | *evaluated* | Open-source QEMU-based virtual machine manager for macOS | Apache-2.0 | — |
| [Tart (macOS)](https://tart.run/) | Virtualization, Emulation & Containment | *evaluated* | Lightweight macOS virtualization tool for Linux and macOS VMs | Fair Source / Apache-2.0 | — |
| [OrbStack (macOS)](https://orbstack.dev/) | Virtualization, Emulation & Containment | *evaluated* | High-efficiency macOS container and Linux machine runtime | Proprietary | — |
| [Claude (Anthropic)](https://claude.ai/) | AI & Developer Tooling | **selected** | Primary reasoning and architectural orchestration agent for Tamlinux development | Proprietary Service | AI_PROVENANCE.md |
| [Codex / OpenAI API](https://openai.com/) | AI & Developer Tooling | **selected** | High-speed code synthesis, mechanical refactoring, and test generation agent | Proprietary Service | AI_PROVENANCE.md |
| [Gemini (Google DeepMind) / agy](https://gemini.google.com/app) | AI & Developer Tooling | **selected** | Antigravity CLI (agy) pair-programming assistant for codebase refactoring and analysis | Proprietary Service | AI_PROVENANCE.md |
| [ChatGPT (OpenAI)](https://chatgpt.com/) | AI & Developer Tooling | *evaluated* | Exploratory research and general query interface | Proprietary Service | — |
| [Cursor IDE](https://cursor.com/) | AI & Developer Tooling | **active** | AI-first developer editor packaged for the Tamlinux workstation | Proprietary / VS Code Fork | — |
| [KDE Gear](https://apps.kde.org/) | Desktop Application Suites | *evaluated* | Primary modular application suite for Tamlinux graphical utilities | GPL-2.0-or-later / LGPL-2.1-or-later | docs/desktop-application-suites.md |
| [GNOME Core Applications](https://apps.gnome.org/) | Desktop Application Suites | *evaluated* | Architectural reference and alternative application suite | GPL-3.0-or-later / LGPL-2.1-or-later | docs/desktop-application-suites.md |
| [Okular](https://okular.kde.org/) | Desktop Application Suites | *evaluated* | Universal document and PDF viewer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.3 |
| [Kate](https://kate-editor.org/) | Desktop Application Suites | *evaluated* | Advanced graphical text editor and lightweight IDE | LGPL-2.0-or-later | docs/desktop-application-suites.md §2.2 |
| [Dolphin](https://apps.kde.org/dolphin/) | Desktop Application Suites | *evaluated* | Advanced dual-pane file manager | GPL-2.0-or-later | docs/desktop-application-suites.md §2.1 |
| [Nautilus (GNOME Files)](https://apps.gnome.org/Nautilus/) | Desktop Application Suites | *evaluated* | Minimalist graphical file manager | GPL-3.0-or-later | docs/desktop-application-suites.md §2.1 |
| [Loupe (GNOME Image Viewer)](https://apps.gnome.org/Loupe/) | Desktop Application Suites | *evaluated* | Sandboxed graphical image viewer | GPL-3.0-or-later | docs/desktop-application-suites.md §2.4 |
| [Papers](https://gitlab.gnome.org/GNOME/Incubator/papers) | Desktop Application Suites | *evaluated* | Modern GTK 4 document viewer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.3 |
| [KCalc](https://apps.kde.org/kcalc/) | Desktop Application Suites | *evaluated* | Scientific and programming calculator | GPL-2.0-or-later | docs/desktop-application-suites.md §2.7 |
| [Filelight](https://apps.kde.org/filelight/) | Desktop Application Suites | *evaluated* | Interactive disk space usage visualizer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.6 |
| [KDE Connect](https://kdeconnect.kde.org/) | Desktop Application Suites | *evaluated* | Secure cross-device phone-to-desktop bridge | GPL-2.0-or-later | docs/desktop-application-suites.md §2.7 |
<!-- considered:end -->
