# The Tamlinux Ecosystem: Patches, Packages, and Choices

The public record of the software, cultural, and philosophical ecosystem of [Tamlinux](https://github.com/greenermoose/tamlinux):
1. **The Carried Patch Registry:** Third-party packages Fred's workstation runs patched, and the software depending on those patches.
2. **The Considered Packages Survey:** A complete survey and record of packages, libraries, and dependencies evaluated across all operating system layers to select the optimal components for performance, user sovereignty, and resource efficiency.
3. **The Knowledge Guide:** Offline resources for the `tam` terminal command (`tam show ecosystem`, `tam explain <topic>`) helping users understand why Tamlinux makes the choices it makes.

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

Tamlinux picks and chooses among a large field of possibilities to construct an operating system that maximizes resource efficiency ("value per watt"), hardware longevity, and user freedom.

### Evaluation Framework

- **`selected`:** Adopted for Tamlinux long-term architecture and delivery (Sway, Void Linux, runit, Nix deployment, Quickshell, wlroots, Tamlinux Shell, Btrfs).
- **`active`:** Currently in daily use in the 0.x Arch development workstation (Arch Linux, Pacman, Hyprland, aquamarine, glibc, systemd).
- **`evaluated`:** Formally surveyed and assessed as an architectural reference or alternative (Debian, Alpine, river, labwc, Astal/AGS, Smithay, Waybar).
- **`fallback`:** Designated standby target if the selected primary component encounters showstoppers (antiX Linux Core with runit).
- **`deferred`:** Scheduled for evaluation at a future milestone pending explicit triggers (Void musl vs glibc pilot at 1.2).
- **`retired`:** Previously used or supported; now systematically phased out or decoupled (Omarchy at 0.4.3, OpenClaw at D139, Hermes at D140).
- **`rejected`:** Excluded due to fundamental incompatibilities with Tamlinux tenets (monolithic compositors, raw .deb/.rpm installs, non-deterministic agent daemons).

### Detailed Architectural Knowledge Guides

Comprehensive survey dossiers and architectural chapters are maintained in [`knowledge/ecosystem/`](knowledge/ecosystem/) (accessible in the terminal via `tam explain <topic>` or `tam-ecosystem guide <page>`):

1. [`knowledge/ecosystem/philosophy.html`](knowledge/ecosystem/philosophy.html) — Free Software Foundation, copyleft (GPL-3.0), freedesktop.org XDG standards, and Linux kernel.
2. [`knowledge/ecosystem/c-libraries.html`](knowledge/ecosystem/c-libraries.html) — C standard libraries: `glibc` vs `musl libc` on developer workstations.
3. [`knowledge/ecosystem/distros.html`](knowledge/ecosystem/distros.html) — Survey of 12 distributions: Arch, Void, antiX, Debian, Alpine, Puppy, Tiny Core, Gentoo, openSUSE, CentOS/RHEL, Ubuntu/Lubuntu, Bedrock.
4. [`knowledge/ecosystem/packaging.html`](knowledge/ecosystem/packaging.html) — Nix reproducible delivery, Pacman local patches, Void XBPS, Debian APT/dpkg, and Gentoo Portage.
5. [`knowledge/ecosystem/init-systems.html`](knowledge/ecosystem/init-systems.html) — `runit` deterministic service supervision versus `systemd` monolithic management.
6. [`knowledge/ecosystem/compositors.html`](knowledge/ecosystem/compositors.html) — Wayland display protocols, Sway on wlroots, Hyprland retirement, and compositors (Niri, river, labwc, Wayfire).
7. [`knowledge/ecosystem/toolkits.html`](knowledge/ecosystem/toolkits.html) — Desktop UI toolkits: Quickshell (Qt Quick/QML), Qt 6, GTK 3/4, Astal/AGS, EWW; Tamlinux Shell versus Omarchy.
8. [`knowledge/ecosystem/virtualization.html`](knowledge/ecosystem/virtualization.html) — Virtualization and containment: QEMU, Docker, WSL, UTM, Tart, OrbStack.
9. [`knowledge/ecosystem/patches.html`](knowledge/ecosystem/patches.html) — Carried patches: public forks, patch rigs, and upstream relationships.
10. [`knowledge/ecosystem/ai-and-agency.html`](knowledge/ecosystem/ai-and-agency.html) — AI coding tools: Claude, Codex, Gemini, Cursor; public provenance, value per watt, and human agency (D139, D140).
11. [`knowledge/ecosystem/sustainability.html`](knowledge/ecosystem/sustainability.html) — Sustainability: Suspra, community resilience, reducing e-waste, and supporting vintage 2006 hardware.
12. [`knowledge/ecosystem/desktop-suites.html`](knowledge/ecosystem/desktop-suites.html) — Desktop application suites: KDE Gear (Okular, Kate, Dolphin, KCalc, Filelight) and GNOME Core/Circle evaluation.

### Complete Considered Packages Dossier

Generated from [`ecosystem.json`](ecosystem.json) via `tam-ecosystem render`:

<!-- considered:begin -->
| Package | Category | Status | Role | License | Decision / Survey |
|---|---|---|---|---|---|
| [Free Software Foundation (FSF)](https://www.fsf.org/) | Free Software Foundations & Standards | **selected** | Ethical and philosophical foundation of Tamlinux user sovereignty | GPL / FDL | Core philosophy; LICENSE GPL-3.0 |
| [freedesktop.org (XDG)](https://www.freedesktop.org/) | Free Software Foundations & Standards | **selected** | Desktop interoperability standards across Linux environments | Open Specifications (MIT / CC-BY-SA) | D110, D125, D138 (XDG Base Directory, Wayland protocols) |
| [The Linux Kernel](https://www.kernel.org/) | Free Software Foundations & Standards | **selected** | Operating system kernel providing hardware abstraction and system calls | GPL-2.0-only | D53, D100, base-operating-system.md |
| [The GNU C Library (glibc)](https://sourceware.org/glibc/) | C Standard Libraries | **active** | Current standard C library on Arch Linux workstation and primary Void tier | LGPL-2.1-or-later | base-operating-system.md §C Library Evaluation |
| [musl libc](https://musl.libc.org/) | C Standard Libraries | *deferred* | Alternative C library evaluated for minimal footprint Void/Alpine profiles | MIT | base-operating-system.md §C Library Evaluation |
| [Arch Linux](https://archlinux.org/) | Operating System Distributions | **active** | Working development distribution for Tamlinux 0.x workstation | GPL-2.0 and various open-source licenses | D124, D126, D136; base-operating-system.md |
| [Void Linux](https://voidlinux.org/) | Operating System Distributions | **selected** | Target base distribution for independent Tamlinux cultivar at milestone 1.2 | BSD-2-Clause and various | D68, D126; base-operating-system.md |
| [antiX Linux (Core)](https://antixlinux.com/) | Operating System Distributions | *fallback* | Designated fallback distribution if Void presents showstoppers | GPL and various | D68, D126; base-operating-system.md §Target and fallback |
| [Debian GNU/Linux](https://www.debian.org/) | Operating System Distributions | *evaluated* | Universal OS benchmark and package archive upstream | Debian Free Software Guidelines (DFSG) | base-operating-system.md, D68 |
| [Alpine Linux](https://alpinelinux.org/) | Operating System Distributions | *evaluated* | Security-oriented, ultra-lightweight musl + BusyBox reference distribution | GPL-2.0 and various | base-operating-system.md, peer-projects survey |
| [Puppy Linux](https://puppylinux-woof-ce.github.io/) | Operating System Distributions | *evaluated* | Pioneering lightweight distribution running entirely in RAM | GPL and various | Resource efficiency and hardware longevity research |
| [Tiny Core Linux](http://www.tinycorelinux.net/) | Operating System Distributions | *evaluated* | Modular, ultra-minimalist Linux desktop architecture | GPL-2.0 | Resource efficiency research |
| [Gentoo Linux](https://www.gentoo.org/) | Operating System Distributions | *evaluated* | Source-based distribution benchmark for fine-grained compilation control | GPL-2.0 | Package management and compilation research |
| [openSUSE (Tumbleweed / Leap)](https://www.opensuse.org/) | Operating System Distributions | *evaluated* | Enterprise-grade rolling and stable RPM distribution | GPL and various | Peer survey §10 |
| [CentOS / Red Hat Enterprise Linux (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) | Operating System Distributions | *evaluated* | Enterprise Linux standard and server baseline | GPL and various | Enterprise compatibility survey |
| [Ubuntu & Lubuntu](https://lubuntu.me/) | Operating System Distributions | *evaluated* | Popular consumer desktop distribution and LXQt lightweight derivative | GPL and various | Desktop shell and distribution peer survey |
| [Bedrock Linux](https://bedrocklinux.org/) | Operating System Distributions | *evaluated* | Meta-distribution providing cross-distro package integration | GPL-2.0 | Package distribution architecture |
| [Nix / NixOS](https://nixos.org/) | Package Managers & Delivery Mechanisms | **selected** | Reproducible package and deployment framework for Tamlinux software | LGPL-2.1-only | D132, D114, D72; LIFECYCLE.md §3 |
| [Pacman (Arch Linux)](https://pacman.archlinux.page/) | Package Managers & Delivery Mechanisms | **active** | Host package manager for the active Arch workstation and local patches | GPL-2.0-or-later | README.md, bin/tam-ecosystem |
| [XBPS (X Binary Package System)](https://docs.voidlinux.org/xbps/) | Package Managers & Delivery Mechanisms | **selected** | Target native package manager on Void Linux base | BSD-2-Clause | D68, D126; base-operating-system.md §Package and service ownership |
| [dpkg & APT (Debian Packaging)](https://wiki.debian.org/Packaging/Intro) | Package Managers & Delivery Mechanisms | *evaluated* | Debian package format and dependency resolver | GPL-2.0-or-later | Non-negotiable guardrails; fallback antiX base |
| [Portage (Gentoo)](https://wiki.gentoo.org/wiki/Portage) | Package Managers & Delivery Mechanisms | *evaluated* | Source build and dependency resolver benchmark | GPL-2.0-only | Package management research |
| [runit](https://smarden.org/runit/) | System Managers & Service Supervision | **selected** | Selected init and service supervision system for Void/antiX base | BSD-3-Clause | D68, D126; base-operating-system.md §Target and fallback |
| [systemd](https://systemd.io/) | System Managers & Service Supervision | **active** | Active system manager on Arch Linux 0.x workstation; target for removal in 1.2 | LGPL-2.1-or-later | D68, D126, D136; base-operating-system.md |
| [Wayland Display Protocol](https://wayland.freedesktop.org/) | Windowing Systems & Display Protocols | **selected** | Display server protocol powering the Tamlinux graphical environment | MIT | D64, D125; compositor-protocol-layer.md |
| [X Window System (X.Org)](https://www.x.org/) | Windowing Systems & Display Protocols | *retired* | Historic windowing architecture; phased out in Tamlinux | MIT | Wayland architectural transition |
| [Sway](https://swaywm.org/) | Wayland Compositors & Window Managers | **selected** | Selected long-term tiling Wayland compositor for Tamlinux (0.7–1.0+) | MIT | D64, D119, D120, D124, D126; compositor survey 2026-10-03 |
| [Hyprland](https://hypr.land/) | Wayland Compositors & Window Managers | **active** | Active interim compositor on Tamlinux 0.x workstation; scheduled for removal at 1.0 | BSD-3-Clause | D64, D124; packages/hyprland |
| [Niri](https://github.com/niri-wm/niri) | Wayland Compositors & Window Managers | *evaluated* | Scrollable-tiling Wayland compositor written in Rust | GPL-3.0-or-later | compositor survey 2026-10-03, peer survey §11 |
| [river](https://github.com/riverwm/river) | Wayland Compositors & Window Managers | *evaluated* | Dynamic tiling Wayland compositor written in Zig | GPL-3.0-only | compositor survey 2026-10-03, peer survey §11 |
| [labwc](https://github.com/labwc/labwc) | Wayland Compositors & Window Managers | *evaluated* | Stacking Wayland compositor inspired by Openbox | GPL-2.0-only | compositor survey 2026-10-03 |
| [Wayfire](https://wayfire.org/) | Wayland Compositors & Window Managers | *evaluated* | 3D visual effects Wayland compositor inspired by Compiz | MIT | compositor survey |
| [miracle-wm](https://github.com/miracle-wm-org/miracle-wm) | Wayland Compositors & Window Managers | *evaluated* | Tiling Wayland compositor built on Canonical's Mir | GPL-3.0-only | compositor survey |
| [mangowm](https://mangowm.github.io/docs/) | Wayland Compositors & Window Managers | *evaluated* | Lightweight Wayland compositor | GPL-3.0-or-later | compositor survey 2026-10-03 |
| [Weston](https://wayland.pages.freedesktop.org/weston/index.html) | Wayland Compositors & Window Managers | *evaluated* | Reference Wayland compositor by the Wayland project | MIT | Display architecture survey |
| [wlroots](https://gitlab.freedesktop.org/wlroots/wlroots) | Compositor Building Blocks & Backends | **selected** | Modular Wayland compositor library powering Sway and Tamlinux display stack | MIT | D64, D125, D126; compositor-protocol-layer.md |
| [aquamarine](https://github.com/hyprwm/aquamarine) | Compositor Building Blocks & Backends | **active** | Rendering abstraction backend for Hyprland; carried patched in Tamlinux | BSD-3-Clause | packages/aquamarine; ECOSYSTEM.md |
| [Smithay](https://github.com/Smithay/smithay/) | Compositor Building Blocks & Backends | *evaluated* | Rust framework for building custom Wayland compositors | MIT | Peer survey §11 |
| [Canonical Mir](https://github.com/canonical/mir) | Compositor Building Blocks & Backends | *evaluated* | Display server library by Canonical | GPL-2.0 / LGPL-3.0 | Compositor survey |
| [Libweston](https://wayland.pages.freedesktop.org/weston/toc/libweston.html) | Compositor Building Blocks & Backends | *evaluated* | Reusable core compositor library from the Weston project | MIT | Compositor architecture survey |
| [GNOME Mutter](https://mutter.gnome.org/) | Compositor Building Blocks & Backends | *rejected* | Monolithic display server and compositor for GNOME Shell | GPL-2.0-or-later | Desktop architecture evaluation |
| [KDE KWin](https://github.com/KDE/kwin) | Compositor Building Blocks & Backends | *evaluated* | Compositor and window manager for the KDE Plasma desktop | GPL-2.0-or-later | Compositor architecture evaluation |
| [Qt Wayland Compositor](https://doc.qt.io/qt-6/qtwaylandcompositor-index.html) | Compositor Building Blocks & Backends | *evaluated* | QML/C++ compositor development framework in Qt | GPL-3.0 / LGPL-3.0 | Desktop shell and compositor evaluation |
| [Quickshell](https://quickshell.org/) | GUI Toolkits & Widget Engines | **selected** | Desktop shell toolkit powering the Tamlinux shell, bar widgets, and panels | LGPL-3.0-only | D102, D126, D136; tamlinux/desktop/shell |
| [Qt (Qt 6)](https://www.qt.io/) | GUI Toolkits & Widget Engines | **selected** | Core application and UI framework providing QML scene graph and Wayland integration | LGPL-3.0 / GPL-3.0 | tamlinux/desktop/shell |
| [GTK (GTK 3 & GTK 4)](https://www.gtk.org/) | GUI Toolkits & Widget Engines | **active** | Primary GUI toolkit for standard Linux desktop applications | LGPL-2.1-or-later | packages/gtk4; ECOSYSTEM.md |
| [Astal & AGS (Aylur's GTK Shell)](https://www.astal.dev/) | GUI Toolkits & Widget Engines | *evaluated* | TypeScript and GTK-based desktop widget system | GPL-3.0-only | Desktop toolkit peer survey |
| [EWW (ElKowars wacky widgets)](https://github.com/elkowar/eww) | GUI Toolkits & Widget Engines | *evaluated* | Standalone widget system written in Rust with Yuck/SCSS | MIT | Desktop widget survey |
| [The Tamlinux Shell](https://github.com/greenermoose/tamlinux) | Graphical Shells & Desktop Environments | **selected** | The official desktop shell of Tamlinux (bar, menus, plugins, indicators) | GPL-3.0-or-later | D102, D114, D124, D136; tamlinux/desktop/shell |
| [Omarchy Desktop Shell](https://github.com/omacom/omarchy) | Graphical Shells & Desktop Environments | *retired* | Ancestral desktop shell base; 100% decoupled and removed in Tamlinux 0.4.3 | MIT | D99, D102, D103, D124, D136; plans/18-remove-omarchy.md |
| [Waybar](https://waybar.net/) | Graphical Shells & Desktop Environments | *evaluated* | Widely used modular Wayland status bar | MIT | Shell architecture survey |
| [Noctalia](https://noctalia.dev/) | Graphical Shells & Desktop Environments | *evaluated* | Family of native Wayland desktop tools and shell components | GPL-3.0 / MIT | Peer survey §10 |
| [DankMaterialShell](https://danklinux.com/) | Graphical Shells & Desktop Environments | *evaluated* | Material Design desktop shell for Wayland | GPL-3.0-only | Peer survey §1 |
| [Openbox](https://openbox.org/) | X11 Window Managers (Legacy) | *retired* | Historic lightweight stacking window manager providing ergonomic precedent | GPL-2.0-or-later | Ergonomics and lightweight desktop research |
| [QEMU](https://www.qemu.org/) | Virtualization, Emulation & Containment | **selected** | Foundational machine emulator and virtualizer for testing Tamlinux on diverse architectures | GPL-2.0 | Tamlinux testing and architecture validation |
| [Docker](https://www.docker.com/) | Virtualization, Emulation & Containment | **selected** | Containerization platform for reproducible build environments and test harnesses | Apache-2.0 | Development and build harness |
| [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/) | Virtualization, Emulation & Containment | *evaluated* | Compatibility environment for running Linux toolchains on Windows | Proprietary wrapper / GPL Linux kernel | D116; Suspra Tier 2 compatibility |
| [UTM (macOS)](https://mac.getutm.app/) | Virtualization, Emulation & Containment | *evaluated* | Open-source QEMU-based virtual machine manager for macOS | Apache-2.0 | D116; cross-platform validation |
| [Tart (macOS)](https://tart.run/) | Virtualization, Emulation & Containment | *evaluated* | Lightweight macOS virtualization tool for Linux and macOS VMs | Fair Source / Apache-2.0 | CI/CD and cross-platform automation |
| [OrbStack (macOS)](https://orbstack.dev/) | Virtualization, Emulation & Containment | *evaluated* | High-efficiency macOS container and Linux machine runtime | Proprietary | Developer tooling survey |
| [Claude (Anthropic)](https://claude.ai/) | AI & Developer Tooling | **selected** | Primary reasoning and architectural orchestration agent for Tamlinux development | Proprietary Service | D115, D130, D138; AGENTS.md, AI_PROVENANCE.md |
| [Codex / OpenAI API](https://openai.com/) | AI & Developer Tooling | **selected** | High-speed code synthesis, mechanical refactoring, and test generation agent | Proprietary Service | D115, D127; delegation briefs, AI_PROVENANCE.md |
| [Gemini (Google DeepMind) / agy](https://gemini.google.com/app) | AI & Developer Tooling | **selected** | Antigravity CLI (agy) pair-programming assistant for codebase refactoring and analysis | Proprietary Service | D107, D129, D131; AI_PROVENANCE.md |
| [ChatGPT (OpenAI)](https://chatgpt.com/) | AI & Developer Tooling | *evaluated* | Exploratory research and general query interface | Proprietary Service | Developer tooling bookmarks |
| [Cursor IDE](https://cursor.com/) | AI & Developer Tooling | **active** | AI-first developer editor packaged for the Tamlinux workstation | Proprietary / VS Code Fork | cursor-update.md runbook |
| [Suspra & Earth Day in Brunswick](https://earthdayinbrunswick.com/) | Applications & Community Mission | **selected** | The community resilience, environmental sustainability, and local civic software suite | GPL-3.0-or-later / Open Source | D116; transition/05-suspra-software-and-workstations.md |
| [KDE Gear](https://apps.kde.org/) | Desktop Application Suites | **selected** | Primary modular application suite for Tamlinux graphical utilities | GPL-2.0-or-later / LGPL-2.1-or-later | docs/desktop-application-suites.md |
| [GNOME Core Applications](https://apps.gnome.org/) | Desktop Application Suites | *evaluated* | Architectural reference and alternative application suite | GPL-3.0-or-later / LGPL-2.1-or-later | docs/desktop-application-suites.md |
| [Okular](https://okular.kde.org/) | Desktop Application Suites | **selected** | Universal document and PDF viewer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.3 |
| [Kate](https://kate-editor.org/) | Desktop Application Suites | **selected** | Advanced graphical text editor and lightweight IDE | LGPL-2.0-or-later | docs/desktop-application-suites.md §2.2 |
| [Dolphin](https://apps.kde.org/dolphin/) | Desktop Application Suites | **selected** | Advanced dual-pane file manager | GPL-2.0-or-later | docs/desktop-application-suites.md §2.1 |
| [Nautilus (GNOME Files)](https://apps.gnome.org/Nautilus/) | Desktop Application Suites | *evaluated* | Minimalist graphical file manager | GPL-3.0-or-later | docs/desktop-application-suites.md §2.1 |
| [Loupe (GNOME Image Viewer)](https://apps.gnome.org/Loupe/) | Desktop Application Suites | *evaluated* | Sandboxed graphical image viewer | GPL-3.0-or-later | docs/desktop-application-suites.md §2.4 |
| [Papers](https://gitlab.gnome.org/GNOME/Incubator/papers) | Desktop Application Suites | *evaluated* | Modern GTK 4 document viewer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.3 |
| [KCalc](https://apps.kde.org/kcalc/) | Desktop Application Suites | **selected** | Scientific and programming calculator | GPL-2.0-or-later | docs/desktop-application-suites.md §2.7 |
| [Filelight](https://apps.kde.org/filelight/) | Desktop Application Suites | **selected** | Interactive disk space usage visualizer | GPL-2.0-or-later | docs/desktop-application-suites.md §2.6 |
| [KDE Connect](https://kdeconnect.kde.org/) | Desktop Application Suites | **selected** | Secure cross-device phone-to-desktop bridge | GPL-2.0-or-later | docs/desktop-application-suites.md §2.7 |
<!-- considered:end -->

---

## Part 3: Knowledge Guide for the `tam` Command

The knowledge resources in [`knowledge/ecosystem/`](knowledge/ecosystem/) are authored as semantic HTML matching the offline guide specification of the `tam` terminal command:

- View in pager: `tam-ecosystem guide [page]` or `TAM_KNOWLEDGE_DIR=knowledge tam show ecosystem`
- Explain topics: `TAM_KNOWLEDGE_DIR=knowledge tam explain sway`
- Search topics: `TAM_KNOWLEDGE_DIR=knowledge tam search <query>`
- Export to system corpus: `tam-ecosystem export-knowledge [target_dir]`
