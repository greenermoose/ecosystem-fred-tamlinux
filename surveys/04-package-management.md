# Survey: Package Managers and Software Delivery

## Overview

Software packaging and delivery is one of the most critical challenges in operating system design. Traditional imperative package managers overwrite files in global hierarchies (`/usr/bin`, `/usr/lib`), making upgrades destructive, rollbacks difficult, and mixed-version development fragile.

Tamlinux solves this challenge by employing a **dual-track architecture**:
1. **Nix & Home Manager (`selected`):** Declarative, reproducible packaging for Tamlinux's own desktop software, commands, plugins, and configs across any host.
2. **Native Base Package Managers:** Fast, transparent native package managers for operating system primitives: **Pacman** on Arch, and **XBPS** on Void.

---

## 1. Candidate Comparison Matrix

| Package Manager | Ecosystem | Model | Atomic Rollback | Build Mechanism | Status in Tamlinux | Role in Tamlinux |
|---|---|---|---|---|---|---|
| **Nix** | Nix / NixOS | Functional, Declarative | Yes (Instant generation rollback) | Nix expressions / Flakes | `selected` | Reproducible deployment of Tamlinux packages |
| **Pacman (ALPM)** | Arch Linux | Imperative binary | No (Manual archive cache install) | `makepkg` (`PKGBUILD`) | `active` | Workstation OS packages & `[local-patches]` |
| **XBPS** | Void Linux | Imperative binary | Transactional (Btrfs snapshot integration) | `xbps-src` (sh chroot) | `selected` | Target native OS packaging on Void base |
| **dpkg / APT** | Debian / antiX | Imperative binary | No | `debuild` / `rules` | `evaluated` | Package system of fallback antiX base |
| **Portage** | Gentoo | Source compilation | No | ebuilds (Bash) | `evaluated` | Reference for fine-grained build options |

---

## 2. In-Depth Analysis

### Nix & Home Manager (`https://nixos.org/`)
- **How it works:** Packages are built into `/nix/store/<hash>-<name>-<version>` using purely functional recipes where all inputs (source code, compiler, dependencies, flags) are hashed into the store path. Symlink trees assemble active generations.
- **Why Tamlinux Selected Nix for Delivery (D132):**
  - **Identical Deployments for Test and Run:** Fred established in D132 that testing a package candidate and running a daily driver use the exact same deployment mechanism. Nix builds immutable packages committed in `tamlinux-packages`.
  - **Instant Rollback:** If a candidate desktop package has a bug, switching back to the previous generation is instantaneous (`home-manager switch --generation <N>`). No files were overwritten or corrupted.
  - **Cross-Distribution Portability (D72):** A Nix flake package can be grafted onto Arch, Void, Debian, or Fedora, delivering the exact same tested binaries and desktop shell across any Linux host.
  - **Decoupled Development (D114):** Development takes place in checkouts without altering the running system until Fred tests a newly built assembly.

### Pacman (`https://pacman.archlinux.page/`)
- **How it works:** Implemented in C (`libalpm`), Pacman is legendary for its speed and straightforward `PKGBUILD` format.
- **Role in Tamlinux Workstation:**
  - Pacman manages base OS packages (Linux kernel, Mesa, Wayland libraries).
  - In `ecosystem-fred-tamlinux`, Pacman's repository precedence rules are used to pin locally patched packages: `[local-patches]` is listed first in `/etc/pacman.conf`, ensuring patched builds stay pinned even when upstream releases new versions.

### XBPS (X Binary Package System) (`https://docs.voidlinux.org/xbps/`)
- **How it works:** Created by Juan RP for Void Linux. Implemented entirely in C, XBPS features atomic package transactions, rapid dependency resolution, and `xbps-src`—a chroot-isolated source build system that turns templates into binary `.xbps` archives.
- **Why Selected for Void Base:**
  - Extremely fast execution with minimal CPU and memory overhead.
  - Transparent template syntax written in standard POSIX shell.
  - Clean separation: Tamlinux will maintain its own signed XBPS repository and templates for native Void delivery, paired with Btrfs snapshots for atomic system-wide rollback.

### Debian APT & dpkg (`https://wiki.debian.org/Packaging/Intro`)
- **How it works:** The foundation of Debian, Ubuntu, and antiX. Relies on `.deb` archives containing `data.tar` and `control.tar` with pre/post-installation shell scripts.
- **Assessment in Tamlinux:**
  - Powers the fallback antiX Core system.
  - Strict guardrail: In Tamlinux, third-party `.deb` files are never unpacked directly onto the workstation; software is always built through native recipes (e.g. Cursor IDE repackaged as a native Arch package via `cursor-update.md`).

### Gentoo Portage (`https://wiki.gentoo.org/wiki/Portage`)
- **How it works:** Highly flexible source-based package manager inspired by FreeBSD Ports. Ebuilds configure packages dynamically using global and per-package USE flags.
- **Assessment:**
  - Portage provides maximal optimization, but the compilation time for large graphical packages (Qt, Chromium, WebKit) on older hardware is prohibitive.
  - Studied as an architectural reference for conditional dependency stripping.

---

## 3. Summary: Tamlinux Package Architecture

Tamlinux separates **base OS packages** from **workstation desktop packages**:
- The **base operating system** (kernel, firmware, init, drivers, C runtime) is owned and updated by the native package manager (**Pacman** on Arch today, **XBPS** on Void tomorrow).
- The **Tamlinux desktop and userland suite** (Tamlinux shell, plugins, `tam` command, themes, and configs) is deployed through **Nix / Home Manager** via pinned commits in `tamlinux-packages`.

This separation guarantees that base hardware drivers remain native and fast, while Tamlinux's unique desktop experience remains reproducible, isolated, and instantly rollback-safe.
