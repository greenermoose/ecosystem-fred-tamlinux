# The Tamlinux Ecosystem

The authoritative public registry, architectural survey, and knowledge guide to the software and cultural ecosystem of [Tamlinux](https://github.com/greenermoose/tamlinux).

This repository is organized around **two core pillars**:
1. **The Ecosystem Knowledge Base (`knowledge/`):** A comprehensive survey and offline guide explaining the packages, libraries, and architectural alternatives evaluated for Tamlinux across every layer of the operating system stack (from C runtimes and distributions to init systems, compositors, shells, and developer tools), integrated directly with the [`tam`](https://github.com/greenermoose/tamlinux) command.
2. **The Carried Patches Registry (`patches/`):** The disciplined, public record of every third-party package Tamlinux workstation environments run **patched**, why the fix exists, how it is built, and when it retires.

---

## Consolidated Repository Structure

```
ecosystem-fred-tamlinux/
├── bin/
│   └── tam-ecosystem           # CLI for surveys, guide viewing, indexing, and patch verification
├── docs/
│   └── ai/                     # Session history and development provenance records
├── knowledge/                  # The offline knowledge corpus and search index for `tam`
│   ├── index.html              # Knowledge base root
│   ├── index.json              # Machine-readable topic index
│   ├── index.tsv               # Tab-separated search index consumed by `tam search`
│   └── ecosystem/              # Thematic survey & decision chapters (HTML with semantic metadata)
│       ├── philosophy.html     # Free Software ethics, user sovereignty, and "value per watt"
│       ├── distros.html        # Distributions: Arch Linux today, Void Linux 1.2+, antiX fallback
│       ├── compositors.html    # Compositors: Sway on wlroots selected for 1.0; Hyprland retiring
│       ├── packaging.html      # Packaging: Nix & Home Manager reproducible delivery + native XBPS
│       ├── init-systems.html   # Init & Supervision: runit vs. monolithic systemd; seatd
│       ├── toolkits.html       # Desktop Shell: Quickshell (Qt Quick/QML) and Omarchy decoupling
│       ├── c-libraries.html    # C Libraries: glibc compatibility vs. musl libc simplicity
│       ├── virtualization.html # Virtualization: QEMU, Docker, WSL, and Suspra multi-tier testing
│       ├── patches.html        # Patches: Public forks, patch rigs, and upstream relationship
│       ├── ai-and-agency.html  # AI Tooling: Supervised pair programming vs. runaway daemons
│       └── sustainability.html # Sustainability: Suspra, e-waste abatement, 2006 hardware floor
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
├── VERSION                     # Version string (0.2.0)
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

## Integration with the `tam` Command

The [`knowledge/`](knowledge/) directory provides an offline semantic HTML corpus designed specifically for the [`tam`](https://github.com/greenermoose/tamlinux) command-line mentor tool:

- **`tam explain ecosystem`** — Displays the ecosystem overview directly in your terminal pager.
- **`tam explain sway`** — Displays the compositors chapter explaining why Sway on wlroots was selected over Hyprland.
- **`tam explain runit`** — Displays the init systems chapter explaining the choice of runit.
- **`tam search <term>`** — Searches `knowledge/index.tsv` using field-weighted keyword matching and Levenshtein fuzzy suggestions.
- **`tam show <path>`** — Renders any semantic HTML page from the knowledge corpus into ANSI-styled terminal output.

To export the knowledge pages into the system `tam` documentation path:
```bash
./bin/tam-ecosystem export-knowledge
```

---

## Using `tam-ecosystem`

The [`bin/tam-ecosystem`](bin/tam-ecosystem) tool provides commands for browsing the ecosystem registry, reading offline guides, and maintaining patch rigs:

```bash
# Browse the Considered Packages Registry
tam-ecosystem survey                 # view survey category overview and counts
tam-ecosystem survey distros         # list all considered distributions
tam-ecosystem survey sway            # view full evaluation dossier for Sway
tam-ecosystem survey runit           # view full evaluation dossier for runit

# Terminal Knowledge Guide
tam-ecosystem guide                  # open the ecosystem guide in the terminal pager
tam-ecosystem guide compositors      # open the compositors chapter
tam-ecosystem guide | head -20       # pipe plain text to stdout

# Indexing and Documentation Sync
tam-ecosystem render                 # rebuild ECOSYSTEM.md tables and knowledge indexes
tam-ecosystem index                  # rebuild knowledge/index.tsv and knowledge/index.json
tam-ecosystem export-knowledge [dir] # export knowledge pages to tam knowledge corpus

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
2. **Value per Watt (D139):** Eliminating unnecessary background polling, heavy daemons, and runaway loops so machines run cool, quiet, and energy-efficiently.
3. **Hardware Longevity:** Engineered to run on vintage circa-2006 hardware (leveraging `wlroots` `pixman` CPU rendering) as well as modern multi-display rigs.
4. **Decoupled Modularity:** Adhering to the Unix philosophy; separating window management (Sway) from desktop presentation (Tamlinux Shell) using standard Wayland protocols (`wlr-layer-shell`, `ext-workspace-v1`).
5. **Offline Sovereignty:** Complete offline local documentation and tools; zero mandatory cloud daemons or network dependencies.
6. **Supervised Determinism:** Prioritizing deterministic programs directed by humans, explicitly rejecting autonomous runaway agent loops (D139, D140).
