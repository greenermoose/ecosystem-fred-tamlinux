# Survey: Operating System Distributions and Base OS Architecture

## Overview

Choosing a base operating system distribution for Tamlinux requires balancing bleeding-edge software freshness, package management speed, init system cleanliness, resource efficiency, and freedom from proprietary lock-in.

Tamlinux is designed to run as an independent cultivar. While early versions run on Arch Linux, the planned long-term architecture adopts **Void Linux** as the native base, with **antiX Linux Core** as a designated fallback.

This survey examines the 12 distributions considered for Tamlinux from Fred's bookmarks and project research.

---

## 1. Candidate Overview Matrix

| Distribution | Init System | Package Manager | libc | Release Model | Status in Tamlinux | Role / Assessment |
|---|---|---|---|---|---|---|
| **Arch Linux** | `systemd` | Pacman (ALPM) | glibc | Rolling | `active` | Current 0.x daily driver development base |
| **Void Linux** | `runit` | XBPS | glibc / musl | Rolling | `selected` | Target base distribution for Tamlinux 1.2+ |
| **antiX Linux (Core)**| `runit` / SysV | APT / dpkg | glibc | Point / Semi-rolling | `fallback` | Designated fallback if Void hits showstoppers |
| **Debian** | `systemd` / SysV | APT / dpkg | glibc | Point / Stable | `evaluated` | Universal OS upstream; DFSG benchmark |
| **Alpine Linux** | OpenRC | apk | musl | Rolling / Stable | `evaluated` | Minimal container benchmark; musl reference |
| **Puppy Linux** | SysV / custom | Woof-CE / custom | glibc | Point | `evaluated` | Extreme RAM-based execution benchmark |
| **Tiny Core Linux** | BusyBox init | tce-load | uClibc / glibc | Modular | `evaluated` | Extreme minimalism (16MB base) |
| **Gentoo Linux** | OpenRC / systemd| Portage | glibc / musl | Rolling | `evaluated` | Source build and USE-flag reference |
| **openSUSE** | `systemd` | Zypper | glibc | Rolling / Point | `evaluated` | Btrfs / Snapper rollback design reference |
| **CentOS / RHEL** | `systemd` | DNF / RPM | glibc | Fixed enterprise | `evaluated` | Enterprise server standard; antithesis of desktop agility |
| **Ubuntu / Lubuntu** | `systemd` | APT / snapd | glibc | Point (6-month) | `evaluated` | Canonical snap daemon overhead rejected |
| **Bedrock Linux** | Passthrough | Multi-manager | Multi-libc | Meta | `evaluated` | Cross-distro layering; too much complexity |

---

## 2. In-Depth Distribution Profiles

### Arch Linux (`https://archlinux.org/`)
- **Strengths:** Bleeding-edge packages, official Arch Build System (`PKGBUILD`), transparent KISS configuration, vast AUR documentation.
- **Why used today:** Arch was the host OS of Omarchy when Tamlinux began. It enables rapid daily driver iteration because compilers, Qt libraries, and Wayland protocols are always updated.
- **Why moving away:** Arch defaults to `systemd` with tight architectural coupling; Arch does not officially support alternative inits; updates can occasionally introduce upstream breaking churn that requires manual intervention.

### Void Linux (`https://voidlinux.org/`)
- **Strengths:** Complete architectural independence (not a fork of Debian or Red Hat); native `runit` init; ultra-fast C-implemented `XBPS` package manager; native `xbps-src` chroot compilation; ships both `glibc` and `musl` repositories; rolling release with high package stability.
- **Tamlinux Decision (D68, D126):** Void is selected as Tamlinux's primary future distribution base. It aligns perfectly with Tamlinux's desire for a minimal, non-systemd, resource-efficient foundation. Tamlinux will carry its own signed package repository and `xbps-src` templates.
- **Considerations:** Void enforce a strict human-authored AI contribution policy (June 2026), so Tamlinux templates will be maintained permanently within Tamlinux repositories rather than submitted upstream to `void-packages` (D126).

### antiX Linux Core (`https://antixlinux.com/`)
- **Strengths:** Dedicated to running fast on low-spec and older hardware; completely systemd-free with `runit` support; built on rock-solid Debian package archives; ultra-low idle memory footprint (~150MB).
- **Tamlinux Role:** Designated fallback target if Void Linux presents insurmountable showstoppers during milestone 1.2 testing.

### Debian (`https://www.debian.org/`)
- **Strengths:** The Universal Operating System. Unmatched stability, rigorous Debian Free Software Guidelines (DFSG), multi-architecture support.
- **Assessment:** While Debian is foundational, its conservative package versions lag modern Wayland compositor features, and its default installer deeply binds `systemd`. However, Debian remains the vital upstream ancestor of antiX.

### Alpine Linux (`https://alpinelinux.org/`)
- **Strengths:** Ultra-small footprint, `musl libc`, BusyBox userland, `apk` package manager, PaX/grsecurity hardening.
- **Assessment:** Dominant in container workloads. Evaluated for Tamlinux minimal/appliance profiles. However, OpenRC service management and BusyBox toolchain variations make it less ergonomic than Void for a developer workstation.

### Puppy Linux & Tiny Core Linux
- **Puppy Linux (`puppylinux-woof-ce.github.io`):** Boots entirely into RAM and runs from union squashfs layers. Shows how responsive an OS can feel when disk I/O latency is completely eliminated.
- **Tiny Core Linux (`tinycorelinux.net`):** Starts at just 16 MB with a dynamic extension mounting model (`.tce`).
- **Assessment:** Both serve as philosophical inspirations for Tamlinux's hardware longevity goals and proof that functional Linux desktops do not require gigabytes of RAM.

### Gentoo Linux (`https://www.gentoo.org/`)
- **Strengths:** Source-based distribution with Portage. Unrivaled customization via USE flags, stripping unneeded features at compile time.
- **Assessment:** Compiling entire browser and desktop stacks from source on older hardware is impractical for rapid daily updates. However, Gentoo's modular dependency model directly influences Tamlinux's package pruning.

### openSUSE (Tumbleweed / Leap) (`https://opensuse.org/`)
- **Strengths:** Open Build Service (OBS), automated openQA testing, and pioneered automated Btrfs snapshots with `snapper`.
- **Assessment:** openSUSE's Btrfs snapshot-and-rollback architecture served as an explicit technical reference for Tamlinux's planned Btrfs snapshot recovery mechanism on Void.

### Canonical Ubuntu & Lubuntu (`https://lubuntu.me/`)
- **Strengths:** Large user base, commercial support, Lubuntu's lightweight LXQt desktop.
- **Assessment:** Canonical's heavy reliance on `snapd` (auto-updating background daemons, loopback mount proliferation, proprietary backend) directly violates Tamlinux's 'value per watt' and local sovereignty principles.

### Bedrock Linux (`https://bedrocklinux.org/`)
- **Strengths:** Innovative meta-distribution that transparently integrates filesystems from multiple distros (e.g. running Pacman and APT on the same machine).
- **Assessment:** Ingenious technology, but the complex filesystem virtualization and stratum redirection add severe debugging opacity. Tamlinux chose clean Nix reproducible delivery over meta-distro filesystem interception.

---

## 3. The Roadmap: From Arch to Void

Tamlinux's progression is phased deliberately to protect developer productivity:
1. **Milestones 0.1–0.6:** Develop and prove the independent desktop shell, plugins, and theme system on Arch Linux.
2. **Milestone 0.7–1.0:** Integrate and standardize on Sway as the primary Wayland compositor, proving multi-monitor resilience and software pixman rendering.
3. **Milestone 1.1:** Build native distribution abstraction layers and evaluate secondary distributions.
4. **Milestone 1.2:** Deploy the native **Void Linux + runit + Btrfs** pilot, benchmarking glibc and musl on target hardware.
