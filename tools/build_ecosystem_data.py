import json
import os

with open("ecosystem.json", "r", encoding="utf-8") as f:
    current = json.load(f)

# Update description and version
current["version"] = "0.2.0"
current["description"] = (
    "Comprehensive record of third-party software patched by Tamlinux, "
    "complete survey of packages and dependencies evaluated across all system layers, "
    "and knowledge resource explaining the software, architectural, and cultural choices of Tamlinux."
)

current["conventions"]["evaluation_statuses"] = {
    "selected": "Adopted component for Tamlinux long-term architecture and delivery",
    "active": "Currently running in the Tamlinux 0.x workstation development environment",
    "evaluated": "Formally surveyed and assessed as an alternative, peer, or architectural reference",
    "fallback": "Designated standby component if the primary selected component hits showstoppers",
    "deferred": "Scheduled for future milestone evaluation pending explicit criteria or triggers",
    "retired": "Previously supported or carried, now systematically removed or phased out",
    "rejected": "Explicitly excluded due to architectural, resource, or philosophical incompatibility"
}

current["philosophy"] = {
    "user_freedom": {
        "title": "User Freedom and the Free Software Movement",
        "description": "Software must grant users the four essential freedoms (run, study, modify, distribute). Tamlinux licenses its own code under GPL-3.0-or-later, ensuring that user freedom and source availability remain perpetual. Upstream works retain their respective licenses (GPL, LGPL, MIT, BSD)."
    },
    "resource_efficiency": {
        "title": "Resource Efficiency and 'Value per Watt'",
        "description": "Tamlinux maximizes computing value while minimizing hardware resource usage and energy consumption. Avoid bloated background daemons, non-deterministic background loops, and unnecessary service layers. Software must earn its memory, CPU, and power footprint (D139, D140)."
    },
    "hardware_longevity": {
        "title": "Hardware Longevity and Fighting Planned Obsolescence",
        "description": "Computing should be durable. Tamlinux is designed to run gracefully on older and lower-resource hardware (validation floor: circa-2006 machines with 32-bit/low-RAM and OpenGL 2.1 graphics using software pixman rendering) through modern multi-monitor workstations, extending device lifespans and curbing electronic waste."
    },
    "decoupled_architecture": {
        "title": "Decoupled Architecture and the Unix Philosophy",
        "description": "Components must do one job well with standard protocols (freedesktop.org XDG, standard Wayland protocols). Window management, display power, panels, menus, and system services communicate via well-defined contracts rather than monolithic single-vendor lock-in."
    },
    "offline_resilience": {
        "title": "Offline Sovereignty and Local Resilience",
        "description": "A workstation must be fully usable without network connectivity. Core documentation (the 'tam' offline guide), man pages, system utilities, and configuration engines run locally from disk without cloud dependencies or telemetry."
    },
    "supervised_determinism": {
        "title": "Deterministic Tools and Supervised Human Agency",
        "description": "Favor deterministic programs that humans or supervised AI agents can control. AI coding assistants (Claude, Codex, agy, OpenCode) are employed under direct human supervision with transparent provenance (AI_PROVENANCE.md), rejecting autonomous runaway agent daemons."
    }
}

current["categories"] = {
    "free_software_foundations": {
        "title": "Free Software Foundations & Standards",
        "description": "The ethical, legal, and interoperability pillars of modern computing"
    },
    "c_libraries": {
        "title": "C Standard Libraries",
        "description": "The foundational userland interface between applications and the Linux kernel"
    },
    "distros": {
        "title": "Operating System Distributions",
        "description": "Base Linux distributions evaluated as hosts and development baselines"
    },
    "package_managers": {
        "title": "Package Managers & Delivery Mechanisms",
        "description": "Tools responsible for building, packaging, deploying, and rolling back software"
    },
    "system_managers": {
        "title": "System Managers & Service Supervision",
        "description": "Init systems, PID 1 architectures, service managers, and process supervisors"
    },
    "windowing_systems": {
        "title": "Windowing Systems & Display Protocols",
        "description": "Low-level display server architectures and client protocols"
    },
    "compositors": {
        "title": "Wayland Compositors & Window Managers",
        "description": "Display servers managing client surfaces, tiling layouts, and input dispatch"
    },
    "compositor_building_blocks": {
        "title": "Compositor Building Blocks & Backends",
        "description": "Hardware abstraction libraries, DRM/KMS backends, and compositor toolkits"
    },
    "gui_toolkits": {
        "title": "GUI Toolkits & Widget Engines",
        "description": "Frameworks for building reactive user interfaces, desktop panels, and dialogs"
    },
    "graphical_shells": {
        "title": "Graphical Shells & Desktop Environments",
        "description": "The visible desktop environment: bars, widgets, system menus, and notification hosts"
    },
    "x11_window_managers": {
        "title": "X11 Window Managers (Legacy)",
        "description": "Historic window managers providing architectural and ergonomic precedent"
    },
    "virtualization": {
        "title": "Virtualization, Emulation & Containment",
        "description": "Engines for hardware emulation, containerization, and cross-platform compatibility"
    },
    "ai_and_agents": {
        "title": "AI & Developer Tooling",
        "description": "AI models, code agents, and developer environments guided by human supervision"
    },
    "applications_and_mission": {
        "title": "Applications & Community Mission",
        "description": "Local applications embodying sustainability, community resilience, and civic utility"
    }
}

# Now populate considered_packages
# Each item corresponds to bookmarks and Tamlinux decisions
considered = [
    # Free Software Foundations
    {
        "name": "fsf",
        "display_name": "Free Software Foundation (FSF)",
        "category": "free_software_foundations",
        "url": "https://www.fsf.org/",
        "license": "GPL / FDL",
        "status": "selected",
        "role": "Ethical and philosophical foundation of Tamlinux user sovereignty",
        "decision_ref": "Core philosophy; LICENSE GPL-3.0",
        "summary": "The organization defending the four essential freedoms of computer users.",
        "resource_profile": "N/A (Philosophical / Legal)",
        "rationale": "Tamlinux exists squarely within the Free Software tradition. Copyleft licensing (GPL-3.0-or-later) ensures that all Tamlinux scripts, tools, and configurations remain permanently accessible, inspectable, and modifiable by users, preventing proprietary enclosure."
    },
    {
        "name": "freedesktop",
        "display_name": "freedesktop.org (XDG)",
        "category": "free_software_foundations",
        "url": "https://www.freedesktop.org/",
        "license": "Open Specifications (MIT / CC-BY-SA)",
        "status": "selected",
        "role": "Desktop interoperability standards across Linux environments",
        "decision_ref": "D110, D125, D138 (XDG Base Directory, Wayland protocols)",
        "summary": "Interoperability specifications for the free desktop (XDG paths, portals, Wayland protocols, notifications).",
        "resource_profile": "N/A (Standards)",
        "rationale": "Tamlinux adheres strictly to freedesktop.org standards: XDG Base Directory specification ($XDG_CONFIG_HOME, $XDG_STATE_HOME, $XDG_DATA_HOME) prevents home directory clutter; desktop entries, fontconfig, and standard Wayland protocols (ext-workspace-v1, wl_output, wlr-layer-shell) enable modular shell construction."
    },
    {
        "name": "linux_kernel",
        "display_name": "The Linux Kernel",
        "category": "free_software_foundations",
        "url": "https://www.kernel.org/",
        "license": "GPL-2.0-only",
        "status": "selected",
        "role": "Operating system kernel providing hardware abstraction and system calls",
        "decision_ref": "D53, D100, base-operating-system.md",
        "summary": "The monolithic operating system kernel providing hardware drivers, memory management, DRM/KMS, and scheduling.",
        "resource_profile": "Core kernel space (~20-50 MB RAM baseline depending on config)",
        "rationale": "Tamlinux runs on standard vanilla Linux kernels (Arch linux, Void linux-vanilla, antiX kernel). Features relied upon include Direct Rendering Manager (DRM/KMS), EVDEV input subsystem, Btrfs filesystem support, ZRAM swap compression, and cgroups."
    },

    # C Libraries
    {
        "name": "glibc",
        "display_name": "The GNU C Library (glibc)",
        "category": "c_libraries",
        "url": "https://sourceware.org/glibc/",
        "license": "LGPL-2.1-or-later",
        "status": "active",
        "role": "Current standard C library on Arch Linux workstation and primary Void tier",
        "decision_ref": "base-operating-system.md §C Library Evaluation",
        "summary": "The ubiquitous, feature-complete standard C library for GNU/Linux systems.",
        "resource_profile": "Standard memory footprint, dynamic linker NSS modules, locale support",
        "rationale": "glibc is the active userland anchor on Arch Linux. Provides total binary compatibility with upstream binaries (Google Chrome, VS Code, Cursor, proprietary graphics drivers) and comprehensive POSIX/GNU extensions. Evaluated against musl for the upcoming Void pilot."
    },
    {
        "name": "musl",
        "display_name": "musl libc",
        "category": "c_libraries",
        "url": "https://musl.libc.org/",
        "license": "MIT",
        "status": "deferred",
        "role": "Alternative C library evaluated for minimal footprint Void/Alpine profiles",
        "decision_ref": "base-operating-system.md §C Library Evaluation",
        "summary": "A clean, lightweight, standards-conformant C library designed for static linking and efficiency.",
        "resource_profile": "Ultra-small memory and disk footprint (~600 KB total size), fast thread creation",
        "rationale": "musl offers unmatched simplicity, strict POSIX compliance, and minimal memory usage. Deferred to Void pilot milestone 1.2 to measure real-world workstation impact. Showstoppers to test include proprietary browser/IDE execution and proprietary GPU driver support."
    },

    # Operating System Distributions
    {
        "name": "arch",
        "display_name": "Arch Linux",
        "category": "distros",
        "url": "https://archlinux.org/",
        "license": "GPL-2.0 and various open-source licenses",
        "status": "active",
        "role": "Working development distribution for Tamlinux 0.x workstation",
        "decision_ref": "D124, D126, D136; base-operating-system.md",
        "summary": "A lightweight, flexible rolling-release distribution following the KISS principle.",
        "resource_profile": "Pacman binary packages, bleeding-edge kernels, systemd default",
        "rationale": "Arch is the current daily development workstation base for Tamlinux. Its rolling release delivers the newest toolchains, Mesa drivers, and compositor builds. Tamlinux runs with local package overrides in [local-patches], transitioning toward independent base delivery in 0.6."
    },
    {
        "name": "void",
        "display_name": "Void Linux",
        "category": "distros",
        "url": "https://voidlinux.org/",
        "license": "BSD-2-Clause and various",
        "status": "selected",
        "role": "Target base distribution for independent Tamlinux cultivar at milestone 1.2",
        "decision_ref": "D68, D126; base-operating-system.md",
        "summary": "An independent, general-purpose rolling distribution featuring runit and the XBPS package manager.",
        "resource_profile": "Minimal memory overhead, no systemd daemons, native runit init, glibc/musl options",
        "rationale": "Void was selected as Tamlinux's primary future base because of its independence (not a downstream fork of Debian or Red Hat), native runit service supervision, XBPS package management with xbps-src templates, and availability of both glibc and musl architectures. Tamlinux plans to maintain its own signed repository and xbps-src templates."
    },
    {
        "name": "antix",
        "display_name": "antiX Linux (Core)",
        "category": "distros",
        "url": "https://antixlinux.com/",
        "license": "GPL and various",
        "status": "fallback",
        "role": "Designated fallback distribution if Void presents showstoppers",
        "decision_ref": "D68, D126; base-operating-system.md §Target and fallback",
        "summary": "A fast, lightweight, systemd-free desktop/core distribution built on Debian Stable/Testing.",
        "resource_profile": "Extremely low RAM footprint (~150MB base), runit init, older hardware optimization",
        "rationale": "antiX Core with runit is the designated fallback target. Its Debian foundation offers vast binary package availability while completely decoupling from systemd. Chosen for its proven track record keeping older hardware useful."
    },
    {
        "name": "debian",
        "display_name": "Debian GNU/Linux",
        "category": "distros",
        "url": "https://www.debian.org/",
        "license": "Debian Free Software Guidelines (DFSG)",
        "status": "evaluated",
        "role": "Universal OS benchmark and package archive upstream",
        "decision_ref": "base-operating-system.md, D68",
        "summary": "The universal operating system, foundational to the Free Software movement.",
        "resource_profile": "Conservative, rock-solid stability, dpkg/APT package system",
        "rationale": "Debian represents the gold standard of distribution governance and Free Software compliance. While its default systemd integration and conservative release cycle led Tamlinux to select Void and Arch, Debian remains the foundation of fallback antiX and a key reference for packaging rigor."
    },
    {
        "name": "alpine",
        "display_name": "Alpine Linux",
        "category": "distros",
        "url": "https://alpinelinux.org/",
        "license": "GPL-2.0 and various",
        "status": "evaluated",
        "role": "Security-oriented, ultra-lightweight musl + BusyBox reference distribution",
        "decision_ref": "base-operating-system.md, peer-projects survey",
        "summary": "A minimalist, security-oriented distribution based on musl libc, BusyBox, and OpenRC.",
        "resource_profile": "Tiny base footprint (~5MB container / ~50MB installed), PaX/grsecurity heritage",
        "rationale": "Alpine is the benchmark for minimal footprint and musl adoption. Evaluated for Tamlinux minimal/embedded appliances. However, OpenRC and BusyBox userland differences make Void with runit a more ergonomic target for a full developer workstation."
    },
    {
        "name": "puppy",
        "display_name": "Puppy Linux",
        "category": "distros",
        "url": "https://puppylinux-woof-ce.github.io/",
        "license": "GPL and various",
        "status": "evaluated",
        "role": "Pioneering lightweight distribution running entirely in RAM",
        "decision_ref": "Resource efficiency and hardware longevity research",
        "summary": "A lightweight Linux distribution designed to load entirely into RAM for incredible speed.",
        "resource_profile": "Runs entirely in RAM, layered squashfs union filesystems",
        "rationale": "Puppy Linux demonstrates the outer boundary of hardware longevity and RAM-based speed. Studied for its techniques in keeping systems responsive on low-spec hardware and layered read-only squashfs system filesystems."
    },
    {
        "name": "tinycore",
        "display_name": "Tiny Core Linux",
        "category": "distros",
        "url": "http://www.tinycorelinux.net/",
        "license": "GPL-2.0",
        "status": "evaluated",
        "role": "Modular, ultra-minimalist Linux desktop architecture",
        "decision_ref": "Resource efficiency research",
        "summary": "An ultra-minimalist Linux desktop operating system starting at just 16 MB.",
        "resource_profile": "Base starts in 16MB RAM; modular dynamic extension mounting",
        "rationale": "Tiny Core exemplifies extreme modularity: the base OS boots into RAM, and extensions are loop-mounted as needed. Demonstrates how few resources are actually necessary for a functioning Linux desktop."
    },
    {
        "name": "gentoo",
        "display_name": "Gentoo Linux",
        "category": "distros",
        "url": "https://www.gentoo.org/",
        "license": "GPL-2.0",
        "status": "evaluated",
        "role": "Source-based distribution benchmark for fine-grained compilation control",
        "decision_ref": "Package management and compilation research",
        "summary": "A highly flexible, source-based Linux distribution powered by the Portage package manager.",
        "resource_profile": "Configurable compiler flags (-march=native), customized feature sets via USE flags",
        "rationale": "Gentoo was evaluated for its ability to strip unnecessary features at compile time. While source compilation for every package is too resource-intensive for Tamlinux's rapid workstation updates, Gentoo's modular dependency modeling informs Tamlinux's package pruning."
    },
    {
        "name": "opensuse",
        "display_name": "openSUSE (Tumbleweed / Leap)",
        "category": "distros",
        "url": "https://www.opensuse.org/",
        "license": "GPL and various",
        "status": "evaluated",
        "role": "Enterprise-grade rolling and stable RPM distribution",
        "decision_ref": "Peer survey §10",
        "summary": "A community distribution sponsored by SUSE, featuring Zypper, YaST, and Open Build Service.",
        "resource_profile": "Full-featured RPM distribution, Snapper Btrfs integration",
        "rationale": "openSUSE's implementation of Snapper Btrfs snapshots for rollback was analyzed as a design reference for Tamlinux's Btrfs recovery plan on Void."
    },
    {
        "name": "centos_rhel",
        "display_name": "CentOS / Red Hat Enterprise Linux (RHEL)",
        "category": "distros",
        "url": "https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux",
        "license": "GPL and various",
        "status": "evaluated",
        "role": "Enterprise Linux standard and server baseline",
        "decision_ref": "Enterprise compatibility survey",
        "summary": "The enterprise standard for commercial and server Linux deployments.",
        "resource_profile": "Conservative enterprise packaging, SELinux enforcement, long lifecycle",
        "rationale": "Evaluated as an architectural contrast: Tamlinux focuses on agile, developer-centric, resource-efficient personal workstations rather than enterprise multi-tenant server infrastructure."
    },
    {
        "name": "lubuntu_ubuntu",
        "display_name": "Ubuntu & Lubuntu",
        "category": "distros",
        "url": "https://lubuntu.me/",
        "license": "GPL and various",
        "status": "evaluated",
        "role": "Popular consumer desktop distribution and LXQt lightweight derivative",
        "decision_ref": "Desktop shell and distribution peer survey",
        "summary": "Canonical's consumer distribution and its lightweight LXQt spin.",
        "resource_profile": "Canonical snap daemon, systemd, desktop conveniences",
        "rationale": "Lubuntu represents traditional lightweight desktop design (LXQt on Openbox/X11). Evaluated against Tamlinux's modern Wayland/Quickshell direction. Canonical's Snap package architecture was rejected for Tamlinux due to auto-updating daemons and loopback mount overhead."
    },
    {
        "name": "bedrock",
        "display_name": "Bedrock Linux",
        "category": "distros",
        "url": "https://bedrocklinux.org/",
        "license": "GPL-2.0",
        "status": "evaluated",
        "role": "Meta-distribution providing cross-distro package integration",
        "decision_ref": "Package distribution architecture",
        "summary": "A meta-Linux distribution that allows users to mix and match components from multiple distributions seamlessly.",
        "resource_profile": "FUSE/chroot virtualization layers and stratum filesystem redirection",
        "rationale": "Bedrock's ability to run Arch pacman alongside Debian apt and Void xbps was surveyed. While innovative, its complex filesystem redirection introduces debugging complexity; Tamlinux chose Nix/Home Manager for cross-distro package delivery instead."
    },

    # Package Managers & Delivery
    {
        "name": "nix",
        "display_name": "Nix / NixOS",
        "category": "package_managers",
        "url": "https://nixos.org/",
        "license": "LGPL-2.1-only",
        "status": "selected",
        "role": "Reproducible package and deployment framework for Tamlinux software",
        "decision_ref": "D132, D114, D72; LIFECYCLE.md §3",
        "summary": "A purely functional package manager providing reproducible builds, atomic upgrades, and instant rollback.",
        "resource_profile": "Immutable /nix/store, symlink trees, flake.lock pinning, no runtime daemon",
        "rationale": "Nix is selected for Tamlinux's software delivery layer (tamlinux-packages and Home Manager). It allows Tamlinux to package its shell, tools, and plugins into immutable, bit-for-bit reproducible store paths. Test and Run deployments point to exact flake commits, making rollbacks instantaneous and rock-solid across any host."
    },
    {
        "name": "pacman",
        "display_name": "Pacman (Arch Linux)",
        "category": "package_managers",
        "url": "https://pacman.archlinux.page/",
        "license": "GPL-2.0-or-later",
        "status": "active",
        "role": "Host package manager for the active Arch workstation and local patches",
        "decision_ref": "README.md, bin/tam-ecosystem",
        "summary": "The fast, lightweight package manager combining a simple binary package format with an easy build system.",
        "resource_profile": "Written in C (libalpm), extremely fast, zero daemon overhead",
        "rationale": "Pacman manages the active Arch OS. In ecosystem-fred-tamlinux, pacman's repository precedence rules allow [local-patches] to take priority over upstream Arch packages, keeping patched builds locked until intentionally retired."
    },
    {
        "name": "xbps",
        "display_name": "XBPS (X Binary Package System)",
        "category": "package_managers",
        "url": "https://docs.voidlinux.org/xbps/",
        "license": "BSD-2-Clause",
        "status": "selected",
        "role": "Target native package manager on Void Linux base",
        "decision_ref": "D68, D126; base-operating-system.md §Package and service ownership",
        "summary": "A fast, native C package manager developed for Void Linux, featuring atomic transactions and xbps-src.",
        "resource_profile": "Fastest package manager in its class, clean library design, no background daemon",
        "rationale": "XBPS was built from scratch in C for Void. It offers atomic package transactions, rapid dependency resolution, and xbps-src, a clean chroot-based source package build system. Tamlinux will maintain native xbps-src templates for its workstation components."
    },
    {
        "name": "apt_dpkg",
        "display_name": "dpkg & APT (Debian Packaging)",
        "category": "package_managers",
        "url": "https://wiki.debian.org/Packaging/Intro",
        "license": "GPL-2.0-or-later",
        "status": "evaluated",
        "role": "Debian package format and dependency resolver",
        "decision_ref": "Non-negotiable guardrails; fallback antiX base",
        "summary": "The foundational package management system powering Debian, Ubuntu, and antiX.",
        "resource_profile": "Complex script hooks (preinst/postinst), multi-arch resolution",
        "rationale": "APT/dpkg is the package manager of fallback antiX Core. In accordance with Tamlinux guardrails, .deb packages are never unpacked directly on the Arch or Void host; software is built through native package recipes."
    },
    {
        "name": "portage",
        "display_name": "Portage (Gentoo)",
        "category": "package_managers",
        "url": "https://wiki.gentoo.org/wiki/Portage",
        "license": "GPL-2.0-only",
        "status": "evaluated",
        "role": "Source build and dependency resolver benchmark",
        "decision_ref": "Package management research",
        "summary": "Gentoo's advanced package management system inspired by FreeBSD ports.",
        "resource_profile": "Python runtime, comprehensive dependency graph resolution, local compilation",
        "rationale": "Evaluated for its granular control over package compilation and features. Studied as a reference for conditional dependency compilation."
    },

    # System Managers & Init Systems
    {
        "name": "runit",
        "display_name": "runit",
        "category": "system_managers",
        "url": "https://smarden.org/runit/",
        "license": "BSD-3-Clause",
        "status": "selected",
        "role": "Selected init and service supervision system for Void/antiX base",
        "decision_ref": "D68, D126; base-operating-system.md §Target and fallback",
        "summary": "A UNIX init scheme with service supervision, created by Gerrit Pape.",
        "resource_profile": "Tiny memory footprint (~sub-megabyte), near-instant boot, process supervision via runsvdir/runsv",
        "rationale": "runit embodies the Unix philosophy of doing one thing well. It provides deterministic, rock-solid service supervision (automatically restarting failed daemons), lightning-fast boot times, and tiny memory usage without creeping into network, logging, or device management."
    },
    {
        "name": "systemd",
        "display_name": "systemd",
        "category": "system_managers",
        "url": "https://systemd.io/",
        "license": "LGPL-2.1-or-later",
        "status": "active",
        "role": "Active system manager on Arch Linux 0.x workstation; target for removal in 1.2",
        "decision_ref": "D68, D126, D136; base-operating-system.md",
        "summary": "A system and service manager for Linux operating systems, providing unified system plumbing.",
        "resource_profile": "Monolithic PID 1, journald, udev, cgroups v2 management, logind session tracking",
        "rationale": "systemd manages the current Arch workstation. While powerful, its monolithic scope, invasive daemon ecosystem, and heavy background footprint conflict with Tamlinux's long-term 'value per watt' and modularity goals. Tamlinux is actively decoupling all shell services from systemd-specific APIs (D136)."
    },

    # Windowing Systems & Protocols
    {
        "name": "wayland",
        "display_name": "Wayland Display Protocol",
        "category": "windowing_systems",
        "url": "https://wayland.freedesktop.org/",
        "license": "MIT",
        "status": "selected",
        "role": "Display server protocol powering the Tamlinux graphical environment",
        "decision_ref": "D64, D125; compositor-protocol-layer.md",
        "summary": "A clean, modern replacement for the X Window System, where every frame is perfect and client isolation is enforced.",
        "resource_profile": "Zero IPC overhead beyond Unix domain sockets, direct DRM/KMS rendering, tear-free",
        "rationale": "Wayland is the foundational display architecture of Tamlinux. Eliminates the legacy bloat, tearing, and insecurity of X11. Modern protocols (ext-workspace-v1, wl_output, wlr-layer-shell) provide all necessary primitives for Tamlinux's decoupled shell architecture."
    },
    {
        "name": "x11",
        "display_name": "X Window System (X.Org)",
        "category": "windowing_systems",
        "url": "https://www.x.org/",
        "license": "MIT",
        "status": "retired",
        "role": "Historic windowing architecture; phased out in Tamlinux",
        "decision_ref": "Wayland architectural transition",
        "summary": "The 40-year-old network-transparent windowing system.",
        "resource_profile": "Heavy client-server roundtrips, root-window snooping, tearing without compositors",
        "rationale": "X11 lacks modern security isolation (any client can log keystrokes or grab screen pixels), struggles with mixed-DPI fractional scaling, and imposes legacy complexity. Tamlinux is a pure Wayland environment; Xwayland is available only as an isolated compatibility fallback."
    },

    # Wayland Compositors
    {
        "name": "sway",
        "display_name": "Sway",
        "category": "compositors",
        "url": "https://swaywm.org/",
        "license": "MIT",
        "status": "selected",
        "role": "Selected long-term tiling Wayland compositor for Tamlinux (0.7–1.0+)",
        "decision_ref": "D64, D119, D120, D124, D126; compositor survey 2026-10-03",
        "summary": "An i3-compatible Wayland compositor built on wlroots, written in clean C.",
        "resource_profile": "Minimal idle CPU/RAM usage (~30-50MB), wlroots pixman CPU rendering for vintage GPUs, seatd compatibility",
        "rationale": "Sway was decisively chosen as Tamlinux's long-term compositor. Key reasons: (1) Clean, stable C codebase without rapid breaking API changes; (2) Built on modular wlroots; (3) Fully operational with seatd/libseat without requiring systemd or elogind; (4) Supports WLR_RENDERER=pixman CPU rendering, enabling operation on vintage circa-2006 GPUs lacking OpenGL 3; (5) Rock-solid i3 IPC and standard Wayland protocol support."
    },
    {
        "name": "hyprland",
        "display_name": "Hyprland",
        "category": "compositors",
        "url": "https://hypr.land/",
        "license": "BSD-3-Clause",
        "status": "active",
        "role": "Active interim compositor on Tamlinux 0.x workstation; scheduled for removal at 1.0",
        "decision_ref": "D64, D124; packages/hyprland",
        "summary": "A dynamic tiling Wayland compositor featuring fluid animations, blur, and modern visual effects.",
        "resource_profile": "Heavier C++23 codebase, GPU acceleration required, rapid plugin ABI churn",
        "rationale": "Hyprland serves as the interim compositor for Tamlinux 0.x while the Tamlinux shell and plugin suite are decoupled. However, it requires modern GPU acceleration, has high C++ toolchain churn, carries strict AI-contribution restrictions, and introduces frequent breaking changes. Scheduled for retirement at 1.0 in favor of Sway."
    },
    {
        "name": "niri",
        "display_name": "Niri",
        "category": "compositors",
        "url": "https://github.com/niri-wm/niri",
        "license": "GPL-3.0-or-later",
        "status": "evaluated",
        "role": "Scrollable-tiling Wayland compositor written in Rust",
        "decision_ref": "compositor survey 2026-10-03, peer survey §11",
        "summary": "A scrollable-tiling Wayland compositor offering an infinite horizontal ribbon workflow.",
        "resource_profile": "Written in Rust on Smithay; requires hardware OpenGL/Vulkan (rejects software EGL)",
        "rationale": "Niri offers an intuitive horizontal window ribbon paradigm. Evaluated during the 2026-10-03 compositor survey. Disqualified for the baseline because it strictly requires hardware OpenGL/Vulkan and cannot run on software pixman renderers for older hardware."
    },
    {
        "name": "riverwm",
        "display_name": "river",
        "category": "compositors",
        "url": "https://github.com/riverwm/river",
        "license": "GPL-3.0-only",
        "status": "evaluated",
        "role": "Dynamic tiling Wayland compositor written in Zig",
        "decision_ref": "compositor survey 2026-10-03, peer survey §11",
        "summary": "A dynamic tiling Wayland compositor with a modular external layout generator architecture.",
        "resource_profile": "Written in Zig on wlroots, low idle footprint, external layout processes",
        "rationale": "river's architecture separates window management from layout generation (layouts run as external standalone processes). Highly regarded, but Sway's mature i3 IPC and established multi-display output management made Sway the superior choice for Tamlinux."
    },
    {
        "name": "labwc",
        "display_name": "labwc",
        "category": "compositors",
        "url": "https://github.com/labwc/labwc",
        "license": "GPL-2.0-only",
        "status": "evaluated",
        "role": "Stacking Wayland compositor inspired by Openbox",
        "decision_ref": "compositor survey 2026-10-03",
        "summary": "A stacking Wayland compositor with Openbox-like configuration and look-and-feel.",
        "resource_profile": "C codebase on wlroots, extremely lightweight, low resource consumption",
        "rationale": "labwc is the premier stacking compositor for users who prefer traditional floating window workflows. Evaluated as an alternative for floating desktop cultivars."
    },
    {
        "name": "wayfire",
        "display_name": "Wayfire",
        "category": "compositors",
        "url": "https://wayfire.org/",
        "license": "MIT",
        "status": "evaluated",
        "role": "3D visual effects Wayland compositor inspired by Compiz",
        "decision_ref": "compositor survey",
        "summary": "A 3D Wayland compositor designed to create customizable desktop effects without high overhead.",
        "resource_profile": "C++ on wlroots, OpenGL ES 2 required for 3D shaders",
        "rationale": "Evaluated for visual effects capability. While efficient for a 3D compositor, 3D effect pipelines increase power consumption and require GPU capabilities beyond Tamlinux's baseline target."
    },
    {
        "name": "miracle_wm",
        "display_name": "miracle-wm",
        "category": "compositors",
        "url": "https://github.com/miracle-wm-org/miracle-wm",
        "license": "GPL-3.0-only",
        "status": "evaluated",
        "role": "Tiling Wayland compositor built on Canonical's Mir",
        "decision_ref": "compositor survey",
        "summary": "A tiling Wayland compositor built atop Canonical's Mir display server library.",
        "resource_profile": "C++ on Mir backend",
        "rationale": "Evaluated as an alternative tiling implementation. The Mir dependency stack is more tightly linked to Ubuntu ecosystems compared to the widely adopted wlroots ecosystem."
    },
    {
        "name": "mangowm",
        "display_name": "mangowm",
        "category": "compositors",
        "url": "https://mangowm.github.io/docs/",
        "license": "GPL-3.0-or-later",
        "status": "evaluated",
        "role": "Lightweight Wayland compositor",
        "decision_ref": "compositor survey 2026-10-03",
        "summary": "A simple, lightweight Wayland window manager.",
        "resource_profile": "Minimal footprint",
        "rationale": "Surveyed during initial candidate sweeps; lacks the ecosystem maturity, IPC stability, and multi-monitor layout handling of Sway."
    },
    {
        "name": "weston",
        "display_name": "Weston",
        "category": "compositors",
        "url": "https://wayland.pages.freedesktop.org/weston/index.html",
        "license": "MIT",
        "status": "evaluated",
        "role": "Reference Wayland compositor by the Wayland project",
        "decision_ref": "Display architecture survey",
        "summary": "The reference implementation of a Wayland compositor by freedesktop.org.",
        "resource_profile": "Reference C implementation, minimal dependencies",
        "rationale": "Weston is the canonical implementation proving the Wayland protocol. While primarily designed as a reference and testing platform rather than a daily workstation environment, its codebase is a vital standard reference."
    },

    # Compositor Building Blocks
    {
        "name": "wlroots",
        "display_name": "wlroots",
        "category": "compositor_building_blocks",
        "url": "https://gitlab.freedesktop.org/wlroots/wlroots",
        "license": "MIT",
        "status": "selected",
        "role": "Modular Wayland compositor library powering Sway and Tamlinux display stack",
        "decision_ref": "D64, D125, D126; compositor-protocol-layer.md",
        "summary": "A modular, unopinionated C library providing the foundational backends for Wayland compositors.",
        "resource_profile": "Highly optimized C, pluggable DRM/KMS/pixman renderers, seatd session integration",
        "rationale": "wlroots is the gold standard for independent Wayland compositors. It implements DRM/KMS, input devices, output management, and Wayland protocol extensions without imposing desktop policy. Crucially for Tamlinux, wlroots supports WLR_RENDERER=pixman for pure CPU software rendering."
    },
    {
        "name": "aquamarine",
        "display_name": "aquamarine",
        "category": "compositor_building_blocks",
        "url": "https://github.com/hyprwm/aquamarine",
        "license": "BSD-3-Clause",
        "status": "active",
        "role": "Rendering abstraction backend for Hyprland; carried patched in Tamlinux",
        "decision_ref": "packages/aquamarine; ECOSYSTEM.md",
        "summary": "Hardware rendering backend library created for Hyprland.",
        "resource_profile": "Modern C++, DRM/KMS backend",
        "rationale": "aquamarine powers Hyprland's display hardware interface. Carried in ecosystem-fred-tamlinux with a crucial patch (aquamarine-guard-null-connectors.patch) to prevent shutdown SIGSEGV crashes. Will retire when Hyprland is replaced by Sway."
    },
    {
        "name": "smithay",
        "display_name": "Smithay",
        "category": "compositor_building_blocks",
        "url": "https://github.com/Smithay/smithay/",
        "license": "MIT",
        "status": "evaluated",
        "role": "Rust framework for building custom Wayland compositors",
        "decision_ref": "Peer survey §11",
        "summary": "A modular engine for building Wayland compositors in Rust, powering Cosmic Epoch and Niri.",
        "resource_profile": "Memory-safe Rust implementation, modern GPU backend focus",
        "rationale": "Smithay is the leading Rust foundation for Wayland. Evaluated during compositor surveys; its reliance on modern GPU hardware acceleration limits its use for Tamlinux's vintage hardware targets."
    },
    {
        "name": "mir",
        "display_name": "Canonical Mir",
        "category": "compositor_building_blocks",
        "url": "https://github.com/canonical/mir",
        "license": "GPL-2.0 / LGPL-3.0",
        "status": "evaluated",
        "role": "Display server library by Canonical",
        "decision_ref": "Compositor survey",
        "summary": "Canonical's set of libraries for building Wayland compositors and IoT display servers.",
        "resource_profile": "C++ library, Ubuntu integration focus",
        "rationale": "Mir provides high-level abstractions for compositing. Evaluated via miracle-wm; wlroots was preferred for broader community adoption and software rendering support."
    },
    {
        "name": "libweston",
        "display_name": "Libweston",
        "category": "compositor_building_blocks",
        "url": "https://wayland.pages.freedesktop.org/weston/toc/libweston.html",
        "license": "MIT",
        "status": "evaluated",
        "role": "Reusable core compositor library from the Weston project",
        "decision_ref": "Compositor architecture survey",
        "summary": "The reusable compositor engine extracted from Weston.",
        "resource_profile": "Reference C implementation",
        "rationale": "Libweston was studied as a compositor library alternative; wlroots provides more active protocol evolution and wider tiling WM support."
    },
    {
        "name": "mutter",
        "display_name": "GNOME Mutter",
        "category": "compositor_building_blocks",
        "url": "https://mutter.gnome.org/",
        "license": "GPL-2.0-or-later",
        "status": "rejected",
        "role": "Monolithic display server and compositor for GNOME Shell",
        "decision_ref": "Desktop architecture evaluation",
        "summary": "The Wayland display server and X11 window manager powering GNOME.",
        "resource_profile": "Monolithic, heavy GObject/C/JavaScript dependencies, deep systemd integration",
        "rationale": "Mutter is tightly coupled to GNOME Shell and the systemd ecosystem. Incompatible with Tamlinux's goals for lightweight, decoupled, non-systemd modularity."
    },
    {
        "name": "kwin",
        "display_name": "KDE KWin",
        "category": "compositor_building_blocks",
        "url": "https://github.com/KDE/kwin",
        "license": "GPL-2.0-or-later",
        "status": "evaluated",
        "role": "Compositor and window manager for the KDE Plasma desktop",
        "decision_ref": "Compositor architecture evaluation",
        "summary": "The window manager and Wayland compositor powering KDE Plasma.",
        "resource_profile": "Heavy C++/Qt/KDE Frameworks dependency tree",
        "rationale": "KWin provides superb Wayland feature completeness. However, its tight coupling to KDE Frameworks and large dependency tree make it unsuitable as a minimal, standalone compositor."
    },
    {
        "name": "qt_wayland",
        "display_name": "Qt Wayland Compositor",
        "category": "compositor_building_blocks",
        "url": "https://doc.qt.io/qt-6/qtwaylandcompositor-index.html",
        "license": "GPL-3.0 / LGPL-3.0",
        "status": "evaluated",
        "role": "QML/C++ compositor development framework in Qt",
        "decision_ref": "Desktop shell and compositor evaluation",
        "summary": "A module enabling the creation of custom Wayland compositors using Qt Quick and QML.",
        "resource_profile": "Qt 6 runtime, QML scene graph rendering",
        "rationale": "Evaluated during exploratory shell research. While Quickshell uses Qt Quick for the desktop shell/panels, keeping the compositor (Sway/wlroots) in clean C separated from the Qt UI shell ensures superior stability and fault isolation."
    },

    # GUI Toolkits
    {
        "name": "quickshell",
        "display_name": "Quickshell",
        "category": "gui_toolkits",
        "url": "https://quickshell.org/",
        "license": "LGPL-3.0-only",
        "status": "selected",
        "role": "Desktop shell toolkit powering the Tamlinux shell, bar widgets, and panels",
        "decision_ref": "D102, D126, D136; tamlinux/desktop/shell",
        "summary": "A flexible, hardware-accelerated desktop shell framework built on Qt Quick and QML.",
        "resource_profile": "Qt 6 QML engine, ~60-80MB RAM for full multi-monitor shell, wlr-layer-shell client",
        "rationale": "Quickshell enables declarative, reactive desktop UI development with QML while interfacing natively with Wayland protocols (wlr-layer-shell) and system IPC. Powers the independent Tamlinux shell. Its memory profile was measured (D126) and found to provide excellent responsiveness without full desktop environment overhead."
    },
    {
        "name": "qt",
        "display_name": "Qt (Qt 6)",
        "category": "gui_toolkits",
        "url": "https://www.qt.io/",
        "license": "LGPL-3.0 / GPL-3.0",
        "status": "selected",
        "role": "Core application and UI framework providing QML scene graph and Wayland integration",
        "decision_ref": "tamlinux/desktop/shell",
        "summary": "A comprehensive cross-platform C++ application framework and declarative UI engine.",
        "resource_profile": "High performance GPU-accelerated scene graph, modular libraries",
        "rationale": "Qt 6 provides the rendering foundation for Quickshell. Its declarative QML engine enables rich animations, responsive layouts, and clean separation of UI presentation from backend system logic."
    },
    {
        "name": "gtk",
        "display_name": "GTK (GTK 3 & GTK 4)",
        "category": "gui_toolkits",
        "url": "https://www.gtk.org/",
        "license": "LGPL-2.1-or-later",
        "status": "active",
        "role": "Primary GUI toolkit for standard Linux desktop applications",
        "decision_ref": "packages/gtk4; ECOSYSTEM.md",
        "summary": "The cross-platform widget toolkit used by GNOME and thousands of Linux applications.",
        "resource_profile": "Standard C/GObject library, Wayland client integration",
        "rationale": "GTK is essential for running core desktop software. In ecosystem-fred-tamlinux, GTK4 was carried patched for a critical Wayland dmabuf format table munmap crash until upstream 4.22.5 resolved it."
    },
    {
        "name": "astal_ags",
        "display_name": "Astal & AGS (Aylur's GTK Shell)",
        "category": "gui_toolkits",
        "url": "https://www.astal.dev/",
        "license": "GPL-3.0-only",
        "status": "evaluated",
        "role": "TypeScript and GTK-based desktop widget system",
        "decision_ref": "Desktop toolkit peer survey",
        "summary": "A framework for building Wayland desktop widgets using GTK 3/4 and TypeScript/Rust.",
        "resource_profile": "GJS / JavaScript runtime + GTK layers",
        "rationale": "Astal/AGS allows developers to write desktop bars in TypeScript. Evaluated against Quickshell. Quickshell was selected for Tamlinux because Qt Quick/QML provides superior declarative reactive binding and better performance compared to GJS."
    },
    {
        "name": "eww",
        "display_name": "EWW (ElKowars wacky widgets)",
        "category": "gui_toolkits",
        "url": "https://github.com/elkowar/eww",
        "license": "MIT",
        "status": "evaluated",
        "role": "Standalone widget system written in Rust with Yuck/SCSS",
        "decision_ref": "Desktop widget survey",
        "summary": "A standalone widget system made in Rust that enables customized desktop widgets.",
        "resource_profile": "Rust binary + GTK3 backend, Yuck S-expression configuration",
        "rationale": "EWW is popular for standalone ricing. However, its custom Yuck S-expression language and IPC limitations make it less extensible than QML for complex desktop panel hierarchies with dynamic menus and state."
    },

    # Graphical Shells & Desktop Environments
    {
        "name": "tamlinux_shell",
        "display_name": "The Tamlinux Shell",
        "category": "graphical_shells",
        "url": "https://github.com/greenermoose/tamlinux",
        "license": "GPL-3.0-or-later",
        "status": "selected",
        "role": "The official desktop shell of Tamlinux (bar, menus, plugins, indicators)",
        "decision_ref": "D102, D114, D124, D136; tamlinux/desktop/shell",
        "summary": "The independent desktop shell for Tamlinux, built with Quickshell, fully decoupled from Omarchy.",
        "resource_profile": "Quickshell QML, store-linked deployed copies via Home Manager, compositor-agnostic protocol abstraction",
        "rationale": "Originally ported from Omarchy 4.0.4, the Tamlinux Shell has achieved complete independence (D136). It features native workspace visualization (fred.workspaces), unified hover architectures (D128), system menus, custom theme engines, and a compositor-neutral protocol state layer (D125)."
    },
    {
        "name": "omarchy",
        "display_name": "Omarchy Desktop Shell",
        "category": "graphical_shells",
        "url": "https://github.com/omacom/omarchy",
        "license": "MIT",
        "status": "retired",
        "role": "Ancestral desktop shell base; 100% decoupled and removed in Tamlinux 0.4.3",
        "decision_ref": "D99, D102, D103, D124, D136; plans/18-remove-omarchy.md",
        "summary": "The opinionated Arch/Hyprland desktop environment created by David Heinemeier Hansson (DHH).",
        "resource_profile": "Quickshell QML shell with centralized system scripts and plugin marketplace",
        "rationale": "Omarchy provided the original UI inspiration and starting codebase for Tamlinux. However, Omarchy's hardcoded paths, centralized control, unstable package hooks, and upstream breaking changes prompted Tamlinux's deliberate plan to achieve complete software and package independence (0.4.3)."
    },
    {
        "name": "waybar",
        "display_name": "Waybar",
        "category": "graphical_shells",
        "url": "https://waybar.net/",
        "license": "MIT",
        "status": "evaluated",
        "role": "Widely used modular Wayland status bar",
        "decision_ref": "Shell architecture survey",
        "summary": "A highly customizable Wayland bar for Sway and Wlroots-based compositors, written in C++.",
        "resource_profile": "C++ / GTK3 / JSON configuration, lightweight (~20-30MB RAM)",
        "rationale": "Waybar is the industry benchmark for Sway status bars. Evaluated as an alternative; Quickshell was selected for Tamlinux because QML supports rich popup panels, interactive menus, and unified hover tooltips far beyond static CSS/JSON bars."
    },
    {
        "name": "noctalia",
        "display_name": "Noctalia",
        "category": "graphical_shells",
        "url": "https://noctalia.dev/",
        "license": "GPL-3.0 / MIT",
        "status": "evaluated",
        "role": "Family of native Wayland desktop tools and shell components",
        "decision_ref": "Peer survey §10",
        "summary": "An open collection of native Wayland projects designed for lightweight desktop workflows.",
        "resource_profile": "Modular Wayland clients",
        "rationale": "Studied during peer project surveys (2026-10-08) as an example of modular, native Wayland desktop component architecture."
    },
    {
        "name": "dank_material_shell",
        "display_name": "DankMaterialShell",
        "category": "graphical_shells",
        "url": "https://danklinux.com/",
        "license": "GPL-3.0-only",
        "status": "evaluated",
        "role": "Material Design desktop shell for Wayland",
        "decision_ref": "Peer survey §1",
        "summary": "A complete desktop shell adhering to Google Material Design standards on Wayland.",
        "resource_profile": "Full desktop environment shell",
        "rationale": "Surveyed as a peer project building a standalone shell across compositors; reinforced Tamlinux's decision to use standard protocol layers (ext-workspace-v1) rather than compositor-specific private IPC."
    },

    # X11 Window Managers
    {
        "name": "openbox",
        "display_name": "Openbox",
        "category": "x11_window_managers",
        "url": "https://openbox.org/",
        "license": "GPL-2.0-or-later",
        "status": "retired",
        "role": "Historic lightweight stacking window manager providing ergonomic precedent",
        "decision_ref": "Ergonomics and lightweight desktop research",
        "summary": "A highly configurable, lightweight next-generation window manager for X11.",
        "resource_profile": "Tiny memory footprint (~5-10MB RAM), fast C execution",
        "rationale": "Openbox set the gold standard for lightweight, unbloated desktop UX for over two decades. Its xml-based keybinding ergonomics and pipe-menus heavily influenced modern tools like labwc and Tamlinux's menu workflows."
    },

    # Virtualization & Containment
    {
        "name": "qemu",
        "display_name": "QEMU",
        "category": "virtualization",
        "url": "https://www.qemu.org/",
        "license": "GPL-2.0",
        "status": "selected",
        "role": "Foundational machine emulator and virtualizer for testing Tamlinux on diverse architectures",
        "decision_ref": "Tamlinux testing and architecture validation",
        "summary": "A generic and open source machine emulator and virtualizer.",
        "resource_profile": "Hardware-accelerated KVM virtualization or full dynamic binary translation",
        "rationale": "QEMU is indispensable for clean-room testing of Tamlinux installation media, validating non-systemd Void/antiX images, and verifying software pixman rendering on simulated legacy hardware."
    },
    {
        "name": "docker",
        "display_name": "Docker",
        "category": "virtualization",
        "url": "https://www.docker.com/",
        "license": "Apache-2.0",
        "status": "selected",
        "role": "Containerization platform for reproducible build environments and test harnesses",
        "decision_ref": "Development and build harness",
        "summary": "A platform using OS-level virtualization to deliver software in packages called containers.",
        "resource_profile": "Linux cgroups and namespaces, near-native execution speed",
        "rationale": "Docker containers provide isolated build scratch environments for compiling Tamlinux components, ensuring host isolation and clean dependency testing."
    },
    {
        "name": "wsl",
        "display_name": "Windows Subsystem for Linux (WSL)",
        "category": "virtualization",
        "url": "https://learn.microsoft.com/en-us/windows/wsl/",
        "license": "Proprietary wrapper / GPL Linux kernel",
        "status": "evaluated",
        "role": "Compatibility environment for running Linux toolchains on Windows",
        "decision_ref": "D116; Suspra Tier 2 compatibility",
        "summary": "A compatibility layer for running Linux binary executables natively on Windows 10/11.",
        "resource_profile": "Hyper-V lightweight VM running custom Linux kernel",
        "rationale": "Relevant for Suspra Tier 2 virtualized developer experiences on non-Linux host platforms."
    },
    {
        "name": "utm",
        "display_name": "UTM (macOS)",
        "category": "virtualization",
        "url": "https://mac.getutm.app/",
        "license": "Apache-2.0",
        "status": "evaluated",
        "role": "Open-source QEMU-based virtual machine manager for macOS",
        "decision_ref": "D116; cross-platform validation",
        "summary": "A full-featured system emulator and virtual machine host for iOS and macOS.",
        "resource_profile": "Apple Hypervisor.framework + QEMU backend",
        "rationale": "Enables cross-platform testing and development of Tamlinux on Apple Silicon hardware."
    },
    {
        "name": "tart",
        "display_name": "Tart (macOS)",
        "category": "virtualization",
        "url": "https://tart.run/",
        "license": "Fair Source / Apache-2.0",
        "status": "evaluated",
        "role": "Lightweight macOS virtualization tool for Linux and macOS VMs",
        "decision_ref": "CI/CD and cross-platform automation",
        "summary": "A lightweight virtualization tool built on Apple's Virtualization.Framework for automation and CI.",
        "resource_profile": "Near-instant startup, OCI image distribution",
        "rationale": "Evaluated for CI/CD test automation of Tamlinux builds across non-native hosts."
    },
    {
        "name": "orbstack",
        "display_name": "OrbStack (macOS)",
        "category": "virtualization",
        "url": "https://orbstack.dev/",
        "license": "Proprietary",
        "status": "evaluated",
        "role": "High-efficiency macOS container and Linux machine runtime",
        "decision_ref": "Developer tooling survey",
        "summary": "A fast, light, and simple way to run Docker containers and Linux machines on macOS.",
        "resource_profile": "Ultra-low CPU/battery usage, fast Rosetta translation",
        "rationale": "Benchmark for developer ergonomics and power efficiency on macOS. While proprietary, its energy-efficient architecture aligns with Tamlinux's 'value per watt' emphasis."
    },

    # AI & Developer Tooling
    {
        "name": "claude",
        "display_name": "Claude (Anthropic)",
        "category": "ai_and_agents",
        "url": "https://claude.ai/",
        "license": "Proprietary Service",
        "status": "selected",
        "role": "Primary reasoning and architectural orchestration agent for Tamlinux development",
        "decision_ref": "D115, D130, D138; AGENTS.md, AI_PROVENANCE.md",
        "summary": "Advanced AI assistant developed by Anthropic, used for complex system design, policy synthesis, and orchestration.",
        "resource_profile": "Cloud API; direct human steering by Fred",
        "rationale": "Claude is employed as an interactive pair programmer and orchestrator. In Tamlinux, AI does not run in uncontrolled autonomous loops; Fred directs every plan, decision, and release. Provenance is tracked in AI_PROVENANCE.md."
    },
    {
        "name": "codex",
        "display_name": "Codex / OpenAI API",
        "category": "ai_and_agents",
        "url": "https://openai.com/",
        "license": "Proprietary Service",
        "status": "selected",
        "role": "High-speed code synthesis, mechanical refactoring, and test generation agent",
        "decision_ref": "D115, D127; delegation briefs, AI_PROVENANCE.md",
        "summary": "Code synthesis and execution engine used for precise transformations and delegation briefs.",
        "resource_profile": "Cloud API; scoped delegation with byte-accurate verification",
        "rationale": "Codex is delegated bounded coding tasks (e.g., panel ports, test suites, exact refactors). Governed by tam-work concurrency locks and verified before merge."
    },
    {
        "name": "gemini",
        "display_name": "Gemini (Google DeepMind) / agy",
        "category": "ai_and_agents",
        "url": "https://gemini.google.com/app",
        "license": "Proprietary Service",
        "status": "selected",
        "role": "Antigravity CLI (agy) pair-programming assistant for codebase refactoring and analysis",
        "decision_ref": "D107, D129, D131; AI_PROVENANCE.md",
        "summary": "Google DeepMind's multimodal model driving the Antigravity (agy) agent for deep repository analysis and execution.",
        "resource_profile": "Cloud API / local terminal agent (agy)",
        "rationale": "agy is utilized for large-scale codebase surveys, fast symbol analysis, and comprehensive repository expansions under Fred's direct guidance."
    },
    {
        "name": "chatgpt",
        "display_name": "ChatGPT (OpenAI)",
        "category": "ai_and_agents",
        "url": "https://chatgpt.com/",
        "license": "Proprietary Service",
        "status": "evaluated",
        "role": "Exploratory research and general query interface",
        "decision_ref": "Developer tooling bookmarks",
        "summary": "Conversational AI platform for exploratory inquiry and concept drafting.",
        "resource_profile": "Web interface",
        "rationale": "Used for initial conceptual ideation before formal planning in improvements-fred-tamlinux."
    },
    {
        "name": "cursor",
        "display_name": "Cursor IDE",
        "category": "ai_and_agents",
        "url": "https://cursor.com/",
        "license": "Proprietary / VS Code Fork",
        "status": "active",
        "role": "AI-first developer editor packaged for the Tamlinux workstation",
        "decision_ref": "cursor-update.md runbook",
        "summary": "An AI-powered code editor built on VS Code, packaged as a native Arch package for Tamlinux.",
        "resource_profile": "Electron / Chromium runtime, packaged via native Arch PKGBUILD",
        "rationale": "Cursor is Fred's primary graphical code editor. Packaged cleanly as a native Arch package (wrapping upstream binaries without raw .deb unpacking) via a dedicated runbook."
    },

    # Applications & Community Mission
    {
        "name": "suspra",
        "display_name": "Suspra & Earth Day in Brunswick",
        "category": "applications_and_mission",
        "url": "https://earthdayinbrunswick.com/",
        "license": "GPL-3.0-or-later / Open Source",
        "status": "selected",
        "role": "The community resilience, environmental sustainability, and local civic software suite",
        "decision_ref": "D116; transition/05-suspra-software-and-workstations.md",
        "summary": "Local web applications and community initiatives dedicated to sustainability and civic empowerment.",
        "resource_profile": "Lightweight web apps (localhost:8000), static staging, zero cloud lock-in",
        "rationale": "Tamlinux is not an abstract exercise; it is the workstation foundation for Suspra's mission. By maximizing hardware longevity, eliminating e-waste, and optimizing energy use ('value per watt'), Tamlinux directly supports community resilience and environmental stewardship."
    }
]

current["considered_packages"] = considered

with open("ecosystem.json", "w", encoding="utf-8") as f:
    json.dump(current, f, indent=2)
    f.write("\n")

print(f"Updated ecosystem.json: {len(considered)} considered packages added across {len(current['categories'])} categories.")
