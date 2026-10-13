# Tamlinux Ecosystem Surveys: Architectural Choices and Evaluations

This directory contains the detailed surveys and architectural evaluations of the software, libraries, and frameworks considered for Tamlinux.

Tamlinux is an independent, continuing Linux workstation environment engineered to deliver the best possible user experience while maximizing resource efficiency, hardware longevity, and user freedom. Building Tamlinux involves picking and choosing among a vast field of possibilities across every layer of the operating system stack: from the C runtime up through kernel drivers, init systems, package managers, display compositors, and graphical shells.

## Evaluation Framework

Every package, library, and tool considered for Tamlinux is evaluated against six fundamental tenets:

1. **User Freedom & Sovereignty:** Does the software respect user freedom? Is it free software under copyleft or permissive open licenses? Does it protect the user from proprietary telemetry, licensing lock-in, and remote kill switches?
2. **Resource Efficiency & "Value per Watt":** Does the component justify its memory, CPU, and electrical footprint? Does it idle silently, or does it burn cycles with polling and unnecessary background daemons (D139, D140)?
3. **Hardware Longevity:** Can the software run gracefully on older and lower-spec hardware (such as vintage circa-2006 machines with 32-bit CPUs and OpenGL 2.1-class graphics via CPU software rendering) as well as modern multi-monitor workstations?
4. **Decoupled Modularity:** Does the component adhere to the Unix philosophy? Can it communicate via open, standard protocols (XDG Base Directory, standard Wayland protocols) rather than forcing monolithic single-vendor lock-in?
5. **Offline Sovereignty & Local Resilience:** Can the system boot, operate, and be maintained without network access or cloud daemons? Is documentation bundled offline (as with the `tam` offline guide)?
6. **Deterministic Human Agency:** Does the system favor deterministic, predictable tools that humans and supervised AI coding agents can control, rather than non-deterministic autonomous background loops?

## Evaluation Statuses

Each considered package is assigned an explicit evaluation status:

| Status | Meaning | Examples in Tamlinux |
|---|---|---|
| **`selected`** | Formally adopted for Tamlinux's long-term architecture and delivery | Sway, Void Linux, runit, Nix deployment, Quickshell, wlroots, Tamlinux Shell, Btrfs |
| **`active`** | Currently in daily use in the 0.x Arch development workstation | Arch Linux, Pacman, Hyprland, aquamarine, glibc, systemd |
| **`evaluated`** | Formally surveyed and assessed as an architectural reference or alternative | Debian, Alpine, river, labwc, Astal/AGS, Smithay, Waybar |
| **`fallback`** | Designated standby target if the selected primary component encounters showstoppers | antiX Linux Core with runit (fallback for Void) |
| **`deferred`** | Scheduled for evaluation at a future milestone pending explicit triggers | Void musl vs glibc pilot (1.2), secondary distributions (1.1) |
| **`retired`** | Previously used or supported; now systematically phased out or decoupled | Omarchy (0.4.3), OpenClaw (D139), Hermes (D140), GTK4 dmabuf patch |
| **`rejected`** | Excluded due to fundamental incompatibilities with Tamlinux tenets | Monolithic compositors (Mutter), raw .deb/.rpm installs, non-deterministic agent daemons |

## Survey Index

The surveys are organized by system layer:

1. [`01-free-software-and-standards.md`](01-free-software-and-standards.md) — Free Software Foundation, copyleft ethics, freedesktop.org XDG standards, and the Linux kernel.
2. [`02-c-libraries.md`](02-c-libraries.md) — Foundational C runtimes: the GNU C Library (`glibc`) versus `musl libc`.
3. [`03-distributions-and-base-os.md`](03-distributions-and-base-os.md) — Comprehensive survey of 12 distributions: Arch, Void, antiX, Debian, Alpine, Puppy, Tiny Core, Gentoo, openSUSE, CentOS/RHEL, Ubuntu/Lubuntu, and Bedrock.
4. [`04-package-management.md`](04-package-management.md) — Package management & delivery: Nix reproducible deployments, Pacman local patches, Void XBPS, Debian APT/dpkg, and Gentoo Portage.
5. [`05-system-managers-and-init.md`](05-system-managers-and-init.md) — Process supervision and init: `runit` deterministic supervision versus `systemd` monolithic management.
6. [`06-windowing-and-protocols.md`](06-windowing-and-protocols.md) — Display architecture: modern Wayland display protocol versus legacy X11; security, tearing, and fractional scaling.
7. [`07-compositors-and-building-blocks.md`](07-compositors-and-building-blocks.md) — Wayland compositors & backends: Sway, Hyprland, Niri, river, labwc, Wayfire, Weston, and building blocks (`wlroots`, `aquamarine`, `Smithay`, `Mir`, `libweston`).
8. [`08-gui-toolkits-and-shells.md`](08-gui-toolkits-and-shells.md) — Graphical shell toolkits: Quickshell (Qt Quick/QML), Qt 6, GTK 3/4, Astal/AGS, EWW; the Tamlinux Shell versus Omarchy, Waybar, Noctalia, and DankMaterialShell.
9. [`09-virtualization-and-compatibility.md`](09-virtualization-and-compatibility.md) — Virtualization and containment: QEMU, Docker, WSL, UTM, Tart, and OrbStack.
10. [`10-ai-and-developer-tooling.md`](10-ai-and-developer-tooling.md) — AI coding tools and human agency: Claude, Codex, Gemini, Cursor; public provenance, value per watt, and supervised determinism (D139, D140).
11. [`11-sustainability-and-hardware-longevity.md`](11-sustainability-and-hardware-longevity.md) — The mission: Suspra, community resilience, reducing e-waste, extending vintage hardware lifespans, and local computing.
