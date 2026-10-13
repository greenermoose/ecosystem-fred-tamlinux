# The Tamlinux Ecosystem

The comprehensive public registry and guide to the software, architectural, and cultural ecosystem of [Tamlinux](https://github.com/greenermoose/tamlinux).

This repository serves three core purposes:
1. **The Carried Patch Registry & Recipes:** The public record of every third-party package Tamlinux workstation environments run **patched**, why the fix exists, how it is built, and when it retires.
2. **The Considered Packages Survey:** A complete record of the packages, libraries, and dependencies evaluated across every layer of the operating system stack (from C runtimes and distributions to init systems, compositors, shells, and developer tools) to select the optimal choices for performance, user sovereignty, and resource efficiency.
3. **The `tam` Offline Knowledge Resource:** Semantic HTML guide pages and structured topic indices designed for the `tam` command (`tam show ecosystem`, `tam explain <topic>`), giving users an offline understanding of the choices made for Tamlinux.

| Resource | Purpose | Format |
|---|---|---|
| [`ECOSYSTEM.md`](ECOSYSTEM.md) | Human-readable patch registry & considered packages summary | Markdown |
| [`ecosystem.json`](ecosystem.json) | Complete machine-readable registry, taxonomy, and package dossiers | JSON |
| [`surveys/`](surveys/) | In-depth technical surveys across 11 system layers | Markdown |
| [`knowledge/ecosystem/`](knowledge/ecosystem/) | Offline guide pages formatted for the `tam` command | Semantic HTML |
| [`packages/<pkg>/`](packages/) | Arch `PKGBUILD` recipes, exported patches, and retirement hooks | Package Rig |
| [`bin/tam-ecosystem`](bin/tam-ecosystem) | Ecosystem management CLI (`survey`, `guide`, `export-knowledge`, `render`, `verify`, `status`) | Bash |

---

## The Tamlinux Architectural Vision

Tamlinux is an independent, continuing Linux workstation environment engineered to deliver the best possible user experience while maximizing resource efficiency ("value per watt"), hardware longevity, and user sovereignty:

- **User Freedom:** All original Tamlinux code is licensed under **GPL-3.0-or-later**, ensuring that user freedom and source code availability remain perpetual.
- **Value per Watt (D139):** Eliminating background polling, daemons, and runaway loops so the machine uses energy efficiently and stays quiet.
- **Hardware Longevity:** Engineered to run acceptably on vintage circa-2006 hardware (using software `pixman` CPU rendering) through modern multi-monitor workstations.
- **Decoupled Modularity:** Adhering to the Unix philosophy; separating window management (Sway) from desktop presentation (Tamlinux Shell) using standard Wayland protocols (`wlr-layer-shell`, `ext-workspace-v1`).
- **Offline Sovereignty:** Complete offline guides and tools; zero mandatory cloud daemons.
- **Supervised Determinism:** Prioritizing deterministic programs directed by humans, rejecting autonomous runaway agent daemons (D139, D140).

---

## Architectural Surveys

Detailed technical survey dossiers are maintained in [`surveys/`](surveys/):

1. [`01-free-software-and-standards.md`](surveys/01-free-software-and-standards.md) — Free Software Foundation (FSF), copyleft ethics, freedesktop.org XDG standards, and the Linux kernel.
2. [`02-c-libraries.md`](surveys/02-c-libraries.md) — Foundational C runtimes: the GNU C Library (`glibc`) versus `musl libc`.
3. [`03-distributions-and-base-os.md`](surveys/03-distributions-and-base-os.md) — Survey of 12 distributions: Arch Linux (current), Void Linux (target), antiX Core (fallback), Debian, Alpine, Puppy, Tiny Core, Gentoo, openSUSE, CentOS/RHEL, Ubuntu/Lubuntu, Bedrock.
4. [`04-package-management.md`](surveys/04-package-management.md) — Nix reproducible delivery, Pacman local patches, Void XBPS, Debian APT/dpkg, and Gentoo Portage.
5. [`05-system-managers-and-init.md`](surveys/05-system-managers-and-init.md) — `runit` deterministic service supervision versus `systemd` monolithic management.
6. [`06-windowing-and-protocols.md`](surveys/06-windowing-and-protocols.md) — Modern Wayland display protocols versus legacy X11; security, tearing, and fractional scaling.
7. [`07-compositors-and-building-blocks.md`](surveys/07-compositors-and-building-blocks.md) — Wayland compositors (Sway, Hyprland, Niri, river, labwc, Wayfire, Weston) and backends (`wlroots`, `aquamarine`, `Smithay`, `Mir`, `libweston`).
8. [`08-gui-toolkits-and-shells.md`](surveys/08-gui-toolkits-and-shells.md) — Desktop UI toolkits: Quickshell (Qt Quick/QML), Qt 6, GTK 3/4, Astal/AGS, EWW; Tamlinux Shell versus Omarchy, Waybar, Noctalia, DankMaterialShell.
9. [`09-virtualization-and-compatibility.md`](surveys/09-virtualization-and-compatibility.md) — Virtualization and containment: QEMU, Docker, WSL, UTM, Tart, OrbStack.
10. [`10-ai-and-developer-tooling.md`](surveys/10-ai-and-developer-tooling.md) — AI coding tools: Claude, Codex, Gemini, Cursor; public provenance, value per watt, and human agency (D139, D140).
11. [`11-sustainability-and-hardware-longevity.md`](surveys/11-sustainability-and-hardware-longevity.md) — Sustainability: Suspra, community resilience, reducing e-waste, and supporting vintage 2006 hardware.

---

## Using `tam-ecosystem`

The [`bin/tam-ecosystem`](bin/tam-ecosystem) CLI provides complete access to the registry and surveys:

```bash
# Query considered packages and categories
tam-ecosystem survey                 # view survey category overview and counts
tam-ecosystem survey distros         # list all considered distributions
tam-ecosystem survey sway            # view full evaluation dossier for Sway
tam-ecosystem survey runit           # view full evaluation dossier for runit

# View the offline guide via tam (or text fallback)
tam-ecosystem guide                  # open the ecosystem guide in the terminal pager
tam-ecosystem guide compositors      # open the compositors chapter
tam-ecosystem guide | head -20       # pipe plain text to stdout

# Export knowledge pages directly to the tam knowledge corpus
tam-ecosystem export-knowledge [dir] # exports knowledge/ecosystem/ into tam knowledge

# Manage carried patches
tam-ecosystem status                 # show patch status and installed hook state
tam-ecosystem verify                 # verify patch integrity against fork commits
tam-ecosystem render                 # regenerate markdown tables in ECOSYSTEM.md
tam-ecosystem install <pkg>          # build and install a patched package rig
tam-ecosystem retire <pkg>           # retire a carried patch
```

---

## Why Carried Patches Exist Instead of Pull Requests

Open-source projects are closing their pull-request queues. Writing code got cheap; reviewing it did not, and maintainers are drowning in machine-generated submissions — GitHub shipped collaborator-only PR controls in August 2026, and projects from Ghostty and tldraw to Zig, GIMP, and QEMU now refuse outside code (background: [arXiv 2609.12236](https://arxiv.org/html/2609.12236), [The Register](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/)). The Hyprland organisation gates on a hand-written vouch and [forbids](https://github.com/hyprwm/.github/blob/main/policies/AI_USAGE.md) AI-written PRs outright.

The patches here are produced by AI coding agents working under Fred's direction, with the tool, model, and prompts recorded ([`AI_PROVENANCE.md`](AI_PROVENANCE.md)). That is honest — and it is exactly what those projects do not want to review. So the fixes are published the way that costs nobody a review: a branch on a public fork that anyone, upstream included, can read in context and take, plus the recipe that turns it into a package. An upstream merge is welcome; it is not the deliverable.

### How a Patch Is Carried

```
greenermoose/<Upstream>        fred/<slug> topic branches off the shipped release tag,
        │                      fred/<tag> integration branch, tag <tag>-fred.N, default branch `fred`
        │  tam-ecosystem export       (git format-patch)
        ▼
~/pkgs/<pkg>/                  Arch's PKGBUILD with pkgrel <arch>.N + the patches   (build scratch)
        │  tam-sync                   (mirror)
        ▼
packages/<pkg>/                this repo — the recipe, the hook, the notes
```

- **Builds stay tarball + patches:** The fork is for reading and for `format-patch`; `makepkg` consumes Arch's source tarball, preserving plugin ABI hashes.
- **Patches are pinned loudly, then retired by hand:** The rebuilt package carries `pkgrel <arch>.N`, and the local repository is listed first in `pacman.conf`. A check run after every pacman transaction warns when Arch moves ahead. `IgnorePkg` is never used.
- **No binaries are published:** This repo shares recipes and surveys, not binaries.

---

## Licence

Scripts, surveys, and documentation in this repository: GPL-3.0-or-later ([`LICENSE`](LICENSE)). Each `packages/<pkg>/*.patch` is a modification of the upstream project and is offered under that project's licence (named in the package's `README.md`: BSD-3-Clause for Hyprland and aquamarine, MIT for omawrite, LGPL-2.1+ for GTK). `PKGBUILD` files derive from Arch Linux packaging (0BSD).

## Related

- [`tamlinux`](https://github.com/greenermoose/tamlinux) — the core Tamlinux product and desktop shell.
- [`tam`](https://github.com/greenermoose/tam) — the offline terminal knowledge command.
- [`tamlinux-packages`](https://github.com/greenermoose/tamlinux-packages) — Nix packaging and deployment definitions.
- [`AI_PROVENANCE.md`](AI_PROVENANCE.md) — public AI authorship records.
