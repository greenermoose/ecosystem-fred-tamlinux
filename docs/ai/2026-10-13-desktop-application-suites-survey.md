# Session: 2026-10-13 — Research KDE & GNOME desktop application suites

- **CLI tool:** Antigravity CLI `1.3.4` (`agy`, dynamically verified via `agy --version`)
- **Model:** `gemini-3.8-flash-high`, verified from session metadata.
- **Transcript:** Retained privately by the author.
- **Scope:** `docs/desktop-application-suites.md`, `knowledge/ecosystem/desktop-suites.html`, `knowledge/ecosystem/index.html`, `ecosystem.json`, `ECOSYSTEM.md`, `AI_PROVENANCE.md`, `docs/ai/`.

## User direction

Fred's guiding prompt verbatim:

> For ecosystem-fred-tamlinux, do careful research about the suites of software KDE and GNOME provide. Create a report or a series of files that contains information about the applications that KDE and GNOME deliver as part of their desktop environments. We'll use this to inform our choice of applications that we include in Tamlinux. In particular, we need to understand the functionality and the dependencies of the KDE and GNOME software. It may be that we can or it might be that we cannot run those applications on the root-stock and Tamlinux cultivar we are developing. Either way is fine; we just need to know that so we can decide whether to include those applications, port them to Tamlinux, or use them as inspiration for a new suite we create ourselves.

## Architectural Analysis & Implementation

1. **Botanical Taxonomy Framing:**
   - Evaluated candidate applications against the Tamlinux botanical architecture:
     - **The Root-stock:** Minimal Void Linux with `runit` and `seatd` (primary target; strictly no systemd PID 1 or elogind), antiX Core (fallback), and Arch Linux (current development base).
     - **The Cultivar:** Sway (wlroots) compositor + Quickshell (Qt Quick/QML) shell + Tamarack design system.
   - Core tenets assessed: User Freedom (GPL-3.0+), Value per Watt (D139 - no perpetual background polling or runaway loops), and Hardware Longevity (circa-2006 hardware floor).

2. **Technical Findings:**
   - **KDE Frameworks 6 (KF6) & KDE Gear:** Superior architectural fit. KF6 Tiers 1–3 are POSIX/libc clean and completely decoupled from systemd, running cleanly on Void Linux with runit + seatd. Because Tamlinux's Quickshell desktop is built with Qt Quick/QML, KDE apps share Qt 6 runtimes, font rendering, and memory allocations. They support Server-Side Decorations (SSD), surrendering borders cleanly to Sway.
   - **GNOME Core & Libadwaita:** Heavy friction. Libadwaita enforces Client-Side Decorations (CSD headerbars) that consume 40–50 vertical pixels in tiling Sway. GNOME applications increasingly rely on systemd user units, `org.freedesktop.login1`, and background indexing daemons (TinySPARQL/Tracker).
   - **Daemon Pruning:** Heavy PIM engines (Akonadi in KDE, Evolution-Data-Server in GNOME) and background file indexing (Baloo in KDE, Tracker in GNOME) violate Value per Watt and thrash 2006 hardware. However, Baloo is trivially disabled via `baloofilerc` (`Indexing-Enabled=false`), whereas Tracker is tightly bound to GNOME Core file operations.

3. **Deliverables:**
   - Authored comprehensive architectural report: `docs/desktop-application-suites.md`.
   - Created semantic HTML knowledge chapter: `knowledge/ecosystem/desktop-suites.html` (indexed for `tam explain ecosystem-desktop-suites` and `tam search`).
   - Updated `knowledge/ecosystem/index.html` topic directory.
   - Added `desktop_application_suites` category and 11 considered package evaluations to `ecosystem.json`.
   - Regenerated `ECOSYSTEM.md`, `knowledge/index.tsv`, and `knowledge/index.json` via `tam-ecosystem render`.
