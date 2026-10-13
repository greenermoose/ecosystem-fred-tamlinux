# The Tamlinux Ecosystem

The public registry and architectural survey of the software ecosystem of [Tamlinux](https://github.com/greenermoose/tamlinux).

This repository has two parts:
1. **The Carried Patches Registry (`patches/`):** The public record of every third-party package Tamlinux workstation environments run **patched**, why the fix exists, how it is built, and when it retires.
2. **The Considered Packages Survey (`ecosystem.json`, `ECOSYSTEM.md`):** The packages, libraries, and alternatives evaluated for Tamlinux across every layer of the system, from C libraries and distributions to init systems, compositors, shells, and developer tools.

The explanations of *why* Tamlinux makes these choices are chapters of the offline guide of the [`tam`](https://github.com/greenermoose/tam) command; read them with `tam show ecosystem`.

---

## Consolidated Repository Structure

```
ecosystem-fred-tamlinux/
├── bin/
│   └── tam-ecosystem           # CLI for surveys, table rendering, and patch verification
├── docs/
│   ├── ai/                     # Session history and development provenance records
│   └── desktop-application-suites.md  # KDE and GNOME application survey
├── patches/                    # All carried third-party patch rigs (active and retired)
│   ├── aquamarine/             # Active KMS pipeline disconnect fix
│   ├── gtk4/                   # Retired dmabuf format table munmap fix
│   ├── hyprland/               # Active DPMS inheritance and idle inhibit noop fixes
│   ├── omarchy/                # Active tooltip border and scaling fixes
│   └── omawrite/               # Retired editor fixes
├── packages -> patches         # Backward-compatibility symlink for external scripts
├── ecosystem.json              # Single source of truth database (considered pkgs + patches)
├── ECOSYSTEM.md                # Human-readable catalog generated from ecosystem.json
├── README.md                   # Repository guide and architectural overview
├── ACKNOWLEDGEMENTS.md         # Upstream & author acknowledgements
├── AI_PROVENANCE.md            # Provenance log
├── VERSION                     # Version string (0.3.0)
└── LICENSE                     # GPL-3.0-or-later
```

---

## Upstream Policy and Relationships

### How Tamlinux Uses the Term "Upstream"
In open-source software, **"upstream"** is an external relationship—it refers to the original creators, maintainers, and canonical code repositories of a project (e.g., `torvalds/linux`, `swaywm/sway`, `hyprwm/hyprland`).

In this repository, "upstream" is treated as an **attribute and relationship**, not an internal folder:
1. **In Considered Package Metadata (`ecosystem.json`):** Every evaluated package records its upstream URL, maintainers, and license.
2. **In Carried Patches (`patches/<pkg>/`):** Every carried patch documents its upstream issue, pull request URL (if submitted), and concrete **retirement condition** (the upstream version or commit that renders our patch obsolete).

### Why Carried Patches Live on Public Forks Instead of Stalled PRs
Open-source maintainers are increasingly overwhelmed by high-volume, low-quality machine-generated PRs. Many upstream projects (such as Zig, Ghostty, GIMP, and Hyprwm) have restricted outside PRs or enacted strict anti-AI contribution policies.

Tamlinux is developed through human-directed AI pair programming with complete transparency ([`AI_PROVENANCE.md`](AI_PROVENANCE.md)). Rather than burdening upstream maintainers with pull requests they do not wish to review, Tamlinux carries necessary bugfixes openly:
- **Public Fork Branches:** Fixes are committed to `greenermoose/<Upstream>` topic branches based cleanly on released upstream tags. Anyone, including upstream maintainers, can cherry-pick them.
- **Local Patch Rigs:** Clean Arch/PKGBUILD recipes consume Arch's source tarballs and apply minimal patch files, maintaining package integrity.
- **Retirement on Merge:** As soon as an upstream release resolves an issue, the local patch is retired immediately.

---

## Using `tam-ecosystem`

The [`bin/tam-ecosystem`](bin/tam-ecosystem) tool provides commands for browsing the ecosystem registry and maintaining patch rigs:

```bash
# Browse the Considered Packages Registry
tam-ecosystem survey                 # view survey category overview and counts
tam-ecosystem survey distros         # list all considered distributions
tam-ecosystem survey sway            # view full evaluation dossier for Sway
tam-ecosystem survey runit           # view full evaluation dossier for runit

# Documentation
tam-ecosystem render                 # rebuild the ECOSYSTEM.md tables from ecosystem.json

# Patch Maintenance
tam-ecosystem status                 # show patch status and installed hook state
tam-ecosystem verify                 # verify patch integrity against fork commits
tam-ecosystem install <pkg>          # build and install a patched package rig
tam-ecosystem retire <pkg>           # mark a carried patch as retired
```

---

## Core Architectural Principles

Every package choice and survey in Tamlinux is evaluated against six foundational tenets:

1. **User Freedom:** Licensed under **GPL-3.0-or-later**, ensuring that user freedom, inspectability, and software modification remain perpetual rights.
2. **Resource Efficiency:** Event-driven, bounded work with no polling loops and no unnecessary resident daemons, so machines run cool, quiet, and energy-efficiently.
3. **Hardware Longevity:** The best possible experience on any hardware, choosing a graphical or terminal profile by capability; circa-2006 machines remain useful validation examples.
4. **Decoupled Modularity:** Adhering to the Unix philosophy; separating window management (Sway) from desktop presentation (Tamlinux Shell) using standard Wayland protocols (`wlr-layer-shell`, `ext-workspace-v1`).
5. **Offline First:** Local documentation and tools with no mandatory cloud services or network dependencies.
6. **Human Direction:** Deterministic tools that people direct; AI assistance is used under human direction with public provenance.
