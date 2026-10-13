# Architectural Survey: KDE and GNOME Desktop Application Suites for Tamlinux

**Repository:** `ecosystem-fred-tamlinux`  
**Date:** 2026-10-13  
**Status:** Evaluated Architectural Dossier. Its verdicts are survey recommendations, not project decisions.  
**Topic:** Desktop Application Suites (KDE Gear & Plasma Apps vs. GNOME Core & Circle)  
**Target Architecture:** Tamlinux Cultivar (Sway + Quickshell) grafted onto Root-stock (Minimal Void Linux with `runit` + `seatd`, antiX fallback, Arch development base)

---

## Executive Summary & Botanical Framing

Tamlinux is an independent, user-sovereign workstation environment built on a clean four-layer botanical architecture:
- **The Pot (Limine):** Fast, declarative UEFI boot loader with atomic Btrfs snapshot selection.
- **The Nut (Unified Kernel Image - UKI):** Sealed, cryptographically signed `.efi` binary bundling kernel, initramfs, and cmdline.
- **The Root-stock (Core System Files & Base OS):** Minimal **Void Linux** utilizing **runit** for deterministic service supervision, **seatd** for minimal seat arbitration, and **XBPS** for clean, fast package management (with **antiX Core** as fallback and **Arch Linux** as the 0.x development baseline).
- **The Cultivar (Complete Tamlinux System):** The user-facing workstation layer comprising **Sway** on **wlroots**, **Quickshell** (Qt Quick / QML) desktop shell with 8 sandboxed `fred.*` plugins, the **Tamarack** design system, and the **`tam`** CLI mentor tool.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        TAMLINUX CULTIVAR                               │
│      Sway (wlroots) + Quickshell (Qt Quick/QML) + fred.* Plugins       │
│      Tamarack Theme + tam CLI + Selected Application Suite             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ grafted onto
┌───────────────────────────────────▼────────────────────────────────────┐
│                       TAMLINUX ROOT-STOCK                              │
│      Minimal Void Linux: runit init + seatd + XBPS + Btrfs             │
│      (Strictly no systemd PID 1; antiX fallback; Arch dev baseline)    │
└────────────────────────────────────────────────────────────────────────┘
```

The workstation desktop experience requires a dependable suite of daily-driver graphical applications: file manager, document viewer, text/code editor, image viewer, media player, terminal, calculator, archiver, disk visualizer, and system monitors.

This survey evaluates the software suites delivered by the two major open-source desktop platforms—**KDE** (KDE Gear, Plasma Applications, KDE Frameworks 6) and **GNOME** (GNOME Core Applications, GNOME Circle, Libadwaita)—to determine:
1. **Functionality:** Breadth, ergonomics, and suitability for keyboard-driven tiling workflows.
2. **Dependencies & Couplings:** Required runtimes, background daemons, IPC buses, and system integration points.
3. **Root-stock Portability:** Whether applications can operate on a minimal `runit` + `seatd` Void Linux host without `systemd` daemons or monolithic session managers.
4. **Cultivar Harmony:** How cleanly applications integrate with a Qt Quick / Sway desktop, respect external color themes (Tamarack), and adhere to Tamlinux's core tenet of **resource efficiency** (zero unnecessary background polling, no runaway indexing loops, 2006 hardware longevity).

---

## 1. High-Level Architectural Comparison

| Dimension | GNOME Software Suite | KDE Software Suite (KDE Gear) | Tamlinux Cultivar Implication |
| :--- | :--- | :--- | :--- |
| **Primary UI Toolkit** | GTK 4 + Libadwaita (some GTK 3 legacy) | Qt 6 + Qt Quick / QML + Kirigami | Tamlinux shell is **Qt Quick / QML**; KDE apps share runtime, style engine, and font stack. |
| **Foundation Libraries** | GLib, GObject, GIO, Cairo, Pango | Qt6-base, Qt6-declarative, KDE Frameworks 6 | Both are mature C/C++ runtimes. KF6 separates into tiered modular libraries. |
| **Configuration Engine** | GSettings / dconf (binary database) | KConfig / KConfigXT (human-readable INI in `~/.config/`) | KConfig is transparent and inspectable; dconf requires specialized schema compilation and binary queries. |
| **Window Decorations** | Client-Side Decorations (CSD) enforced by Libadwaita | Server-Side Decorations (SSD) native; clean protocol negotiation | Libadwaita forces large headerbars that waste vertical space in tiling Sway; KDE apps cleanly surrender window frames to Sway. |
| **Theming Sovereignty** | Rigidly restricted by Libadwaita stylesheet | Declarative palette (`kdeglobals`), Qt style engines (`breeze`, `kvantum`) | Tamarack palette easily themes KDE/Qt apps; Libadwaita actively resists user CSS overriding. |
| **Init & Supervisor Dependency** | Increasing coupling to `systemd` (logind, user units, timedated) | Protocol-based; zero hard systemd requirement across apps | KDE apps run cleanly on Void (`runit` + `seatd`); GNOME apps frequently expect `logind`/`elogind`. |
| **Background Indexing Daemons** | `TinySPARQL` / `Tracker3` / `localsearch` | `Baloo` (`baloo_file`) | Both indexing daemons violate **resource efficiency** on vintage hardware, but Baloo is trivially disabled via config. |
| **Personal Information (PIM)** | Evolution-Data-Server (EDS) | Akonadi (embedded MariaDB/SQLite + D-Bus agents) | **Both are disqualified** for lean default delivery; heavy database daemons choke 2006 hardware floor. |
| **Hardware Floor (RAM/CPU)** | Moderate: ~40–120 MB per app; GJS apps carry JavaScript engine overhead | Highly variable: Tier 1/2 apps are tiny (~15–35 MB); WebEngine apps are heavy | KDE's standalone utilities (KCalc, Kate, Okular) are exceptionally lightweight. |

---

## 2. Comprehensive Domain-by-Domain Application Breakdown

### 2.1 File Management

#### GNOME: Nautilus (`org.gnome.Nautilus` / Files)
- **Functionality:** Clean, task-oriented file browsing with grid/list views, starred files, batch renaming, archive compression integration, and search-driven file retrieval.
- **Dependencies:** GTK 4, Libadwaita, GIO/GVFS (D-Bus), `tinysparql` (formerly Tracker 3 core), `localsearch` (Tracker miners), `gnome-autoar`, `libcloudproviders`, `dconf`.
- **Root-stock (Void + runit):** Runs if `gvfs` and `tinysparql` are installed. However, Tracker filesystem miners run background inotify trees that consume battery and I/O cycles. Without systemd user units, service lifecycle management for background indexers is fragile.
- **Cultivar (Sway + Quickshell):** Enforces Libadwaita CSD headerbars. Keyboard shortcuts are mouse/gesture-biased. Theming does not follow Tamarack tokens automatically.

#### KDE: Dolphin (`org.kde.dolphin`)
- **Functionality:** Industry benchmark for desktop file management. Features dual-pane split view (`F3`), embedded terminal (`F4` via `konsolepart`), tabbed browsing, customizable columns, configurable toolbars, multi-selection modes, and deep KIO integration (trash, sftp, smb, fish protocols).
- **Dependencies:** Qt 6, KF6 (`kio`, `kio-extras`, `kparts`, `kcoreaddons`, `kxmlgui`, `solid`), optional `baloo`.
- **Root-stock (Void + runit):** Packaged natively in Void Linux XBPS. Operates completely without systemd. KIO workers spawn on-demand as ephemeral helper processes rather than perpetual daemons.
- **Cultivar (Sway + Quickshell):** Exceptional fit for power users and keyboard tiling. Can hide all menus/toolbars for an ultra-minimal look. When Baloo is disabled in `~/.config/baloofilerc` (`[Basic Settings] Indexing-Enabled=false`), idle memory footprint is ~40 MB with zero background polling.
- **Tamlinux Recommendation:** **Dolphin (Selected with Baloo disabled)** or paired with a terminal file manager (Yazi/Ranger).

---

### 2.2 Text Editing & Software Development

#### GNOME: GNOME Text Editor (`gnome-text-editor`) & GNOME Builder
- **Functionality:**
  - *Text Editor:* Minimalist, modern notepad with syntax highlighting (`gtksourceview5`), session restoration, vim emulation mode, and inline spell checking (`libspelling`).
  - *Builder:* Full-fledged IDE tailored for Flatpak, Meson, C, Rust, and Python development within the GNOME platform ecosystem.
- **Dependencies:** GTK 4, Libadwaita, `gtksourceview5`, `libspelling`, `editorconfig-core-c`.
- **Root-stock (Void + runit):** Completely portable; self-contained GTK4 application with zero systemd couplings.
- **Cultivar (Sway + Quickshell):** Clean and fast, though Libadwaita limits custom theming and window geometry.

#### KDE: Kate (`kate`), KWrite & KDevelop
- **Functionality:**
  - *Kate:* Powerhouse text editor and lightweight IDE. Features multi-cursor editing, native LSP client (Language Server Protocol with autocompletion, diagnostics, symbol jumping), integrated terminal dock, Git status integration, split editing panes, regex search/replace across folders, vi input mode, and project management.
  - *KWrite:* Lightweight single-document editor using the same `ktexteditor` component.
  - *KDevelop:* Advanced IDE with deep C++/Python semantic analysis.
- **Dependencies:** Qt 6, KF6 (`ktexteditor`, `syntax-highlighting`, `kio`, `kparts`, `kxmlgui`). **Zero background daemons.**
- **Root-stock (Void + runit):** Extremely clean build in Void Linux. No systemd or D-Bus service dependencies required for core editing.
- **Cultivar (Sway + Quickshell):** Flawless integration. Kate provides IDE-grade capabilities in a lean ~35 MB footprint. It respects system color schemes (`kdeglobals`), uses the Atkinson Hyperlegible monospace font cleanly, and complements terminal-based editing (Micro / Neovim).
- **Tamlinux Recommendation:** **Kate (Selected)** as primary graphical editor; pair with Micro for terminal workflows.

---

### 2.3 Universal Document & PDF Viewing

#### GNOME: Papers (`papers`) & Evince
- **Functionality:** Clean document viewing supporting PDF, PostScript, DjVu, and TIFF. *Papers* is the modern GNOME 46+ GTK4/Libadwaita rewrite of the venerable Evince.
- **Dependencies:** GTK 4, Libadwaita, Poppler-glib, `libarchive`, `libspelling`, `djvulibre`, `dconf`.
- **Root-stock (Void + runit):** Highly portable. Requires standard rendering libraries.
- **Cultivar (Sway + Quickshell):** Modern, touch-friendly UI, but titlebar takes space in tiling layouts.

#### KDE: Okular (`okular`)
- **Functionality:** Universally recognized as the most versatile, high-performance document viewer in open-source computing.
  - Supported formats: PDF, ePub, PostScript, DjVu, Markdown, CHM, DVI, FictionBook, CBR/CBZ (comic books), and raster images.
  - Features: Rich annotations (inline notes, highlighter, stamps, freehand drawing), text-to-speech support (`qt6-speech`), form filling, cryptographic signature verification, table selection tool, trim margins mode, and presentation mode.
- **Dependencies:** Qt 6, KF6 (`kparts`, `kio`, `kxmlgui`, `kwallet`), Poppler-qt6, `libkexiv2`, `threadweaver`.
- **Root-stock (Void + runit):** Native Void Linux package. Works without systemd.
- **Cultivar (Sway + Quickshell):** Flawless behavior. High rendering speed via Poppler-qt6; memory footprint is lean (~30 MB base); handles multi-hundred-page technical specifications effortlessly.
- **Tamlinux Recommendation:** **Okular (Selected)** — undisputed best-in-class utility.

---

### 2.4 Image Viewing & Graphics

#### GNOME: Loupe (`loupe`) & Eye of GNOME (`eog`)
- **Functionality:** Loupe is GNOME's modern image viewer built in Rust and GTK4. Smooth trackpad zooming, image rotation, and metadata inspector.
- **Architecture & Security:** Employs **Glycin**—an image decoding framework that sandboxes image decoders inside **Bubblewrap** (`bwrap`) containers with restricted `seccomp` profiles. Malicious image payloads cannot compromise user memory.
- **Dependencies:** GTK 4, Libadwaita, Glycin, Bubblewrap, `libseccomp`, Rust runtime.
- **Root-stock (Void + runit):** Requires unprivileged user namespaces (`kernel.unprivileged_userns_clone=1`) or suid bubblewrap. If user namespaces are disabled, Glycin decoders fail.
- **Cultivar (Sway + Quickshell):** Sleek, secure, but Libadwaita styling and sandbox prerequisites require root-stock tuning.

#### KDE: Gwenview (`gwenview`) & Kolourpaint
- **Functionality:**
  - *Gwenview:* Image viewer and basic editor. Features folder thumbnail browsing, lossless JPEG crop/rotation, resize, red-eye reduction, color management (LCMS2), and Exif/IPTC metadata editing.
  - *Kolourpaint:* Simple, lightweight raster painting tool (resembling MS Paint) for fast diagram markup and annotations.
- **Dependencies:** Qt 6, KF6 (`kio`, `kparts`, `kfilemetadata`), `exiv2`, `lcms2`, optional `baloo`.
- **Root-stock (Void + runit):** Native Void XBPS package, no systemd ties.
- **Cultivar (Sway + Quickshell):** Fast, full-featured image management.
- **Tamlinux Recommendation:** **Gwenview** or **Loupe** (evaluated); Kolourpaint for fast desktop markup.

---

### 2.5 Media Playback & Audio Processing

#### GNOME: Showtime (Video), Decibels (Audio) & Totem
- **Functionality:**
  - *Decibels:* Audio player designed for previewing individual voice memos and sound files with waveform scrubbing.
  - *Showtime:* Clean GStreamer-backed video player introduced in GNOME 47.
  - *Totem:* Legacy GNOME Videos player.
- **Dependencies:** GTK 4, Libadwaita, GStreamer (`gst-plugins-base`, `gst-plugins-good`, `gst-plugins-bad`), `gjs` (JavaScript runtime for Decibels).
- **Assessment:** Decibels utilizes `gjs`, pulling a full SpiderMonkey JavaScript engine for a simple audio player—inefficient from a resource-efficiency perspective.

#### KDE: Haruna (`haruna`), Elisa (`elisa`) & Kdenlive
- **Functionality:**
  - *Haruna:* Open-source video player built on **Qt Quick / Kirigami** and **`libmpv`**. Hardware-accelerated video decoding via VAAPI/VDPAU, playlist management, keyboard scrubbing, YouTube-dl/yt-dlp integration.
  - *Elisa:* Music library player with album art indexing and playlist management.
  - *Kdenlive:* Multi-track non-linear video editing suite (MLT engine).
- **Dependencies:**
  - Haruna: Qt 6, `libmpv`, Kirigami.
  - Elisa: Qt 6, KF6, `libvlc` or `qt6-multimedia`.
- **Assessment:** Haruna provides outstanding performance and minimal CPU overhead by leveraging `mpv`.
- **Tamlinux Recommendation:** **Haruna** (video) or pure `mpv`; terminal audio players or lightweight Qt players.

---

### 2.6 System Telemetry & Disk Management

#### GNOME: GNOME System Monitor, Baobab & GNOME Disks
- **Functionality:**
  - *GNOME System Monitor:* Tabbed overview of processes, CPU/memory history, and mounted filesystems.
  - *Baobab (Disk Usage Analyzer):* Ring chart visualizer of directory space consumption.
  - *GNOME Disks (`gnome-disk-utility`):* Formatting, SMART status, LUKS partition encryption, disk image restoration.
- **Dependencies:** GTK 4, Libadwaita, `libgtop`, `udisks2`, `polkit`.
- **Assessment:** Baobab is lightweight and universally useful. GNOME Disks relies heavily on `udisks2` and polkit D-Bus services.

#### KDE: Plasma System Monitor, Filelight & KDE Partition Manager
- **Functionality:**
  - *Filelight:* Interactive concentric pie-chart visualization of disk usage. Built natively with Qt Quick and QML.
  - *KDE Partition Manager:* GUI disk partitioning tool built on `kpmcore`. Handles Btrfs subvolumes, LUKS encryption, LVM, and partition resizing.
  - *Plasma System Monitor:* Modern Kirigami-based sensor dashboard with customizable layout cards and per-application resource attribution.
- **Dependencies:**
  - Filelight: Qt 6, KF6 (`kquickcharts`, `kirigami`). Zero system daemons.
  - Partition Manager: Qt 6, KF6, `kpmcore`, `polkit-qt`.
- **Assessment:** **Filelight is a natural match for Tamlinux.** Built on Qt Quick, it visualizes storage instantly with sub-25 MB memory usage.
- **Tamlinux Recommendation:** **Filelight (Selected)** for disk visualization; CLI tools (`btop`, `tam inspect`) for telemetry; `kpmcore`/`partitionmanager` or `gparted` for storage management.

---

### 2.7 Utilities: Calculator, Archiver, Device Integration

| Domain | GNOME Offering | KDE Offering | Architectural Winner for Tamlinux |
| :--- | :--- | :--- | :--- |
| **Calculator** | *GNOME Calculator* (GTK4, GMP/MPFR, currency conversion) | *KCalc* (Qt6, GMP/MPFR, scientific/hex modes, ~15 MB RAM) | **KCalc:** Ultra-lightweight, zero daemons, instant launch. |
| **Archiver** | *File Roller* (GTK3/4 frontend for tar/zip/7z) | *Ark* (KF6/Qt6 frontend for `libarchive`, `libzip`) | **Ark:** Clean Qt integration, handles multi-part archives cleanly. |
| **Device Bridge** | *GNOME Connections* (RDP/VNC); GSConnect (Shell extension) | *KDE Connect* (Phone/desktop bridge: clipboard, notifications, files, SMS) | **KDE Connect:** Peerless protocol design; runs standalone on Sway! |
| **Screen Capture** | Built into GNOME Shell compositor | *Spectacle* (Wayland native, screen recording, annotations, OCR) | **Tamlinux native scripts** (`grim`/`slurp`) for speed; Spectacle for rich annotations. |

---

### 2.8 Personal Information Management (PIM): A Cautionary Architectural Study

Both desktop environments offer full PIM suites (Email, Calendar, Contacts, Tasks):
- **GNOME PIM:** GNOME Calendar, GNOME Contacts, Geary / Evolution, powered by **Evolution-Data-Server (EDS)**.
- **KDE PIM:** KMail, KOrganizer, KAddressBook, Merkuro (Kalendar), Kontact, powered by **Akonadi**.

#### The Akonadi & EDS Architectural Tax
Under Tamlinux's botanical design, the PIM stacks of both environments represent an **anti-pattern**:

```text
┌────────────────────────────────────────────────────────┐
│           TRADITIONAL PIM DAEMON OVERHEAD              │
├──────────────────────────────────┬─────────────────────┤
│ KDE Akonadi                      │ GNOME EDS           │
├──────────────────────────────────┼─────────────────────┤
│ • Embedded MariaDB/SQLite engine │ • evolution-source- │
│ • akonadiserver daemon           │   registry          │
│ • Resource agents (mail, cal)    │ • calendar-factory  │
│ • Continuous inotify & polling   │ • addressbook-fact. │
│ • 250–500 MB idle RAM footprint  │ • 150–300 MB RAM    │
│ • High CPU wakeup frequency      │ • Periodic wakeups  │
└──────────────────────────────────┴─────────────────────┘
```

- **Violates resource efficiency:** Akonadi runs continuous database transactions and polling threads, preventing the CPU from entering deep C-states.
- **Violation of 2006 Hardware Floor:** On an Intel Core 2 Duo with 2 GB RAM, launching Akonadi induces immediate disk swap thrashing.
- **Init Fragility on Void Linux:** Both Akonadi and EDS assume complex D-Bus autostart and session lifecycle management typically handled by `systemd --user`. Under `runit`, orphaned daemon processes and locked SQLite sockets frequently occur during abrupt logouts.
- **Tamlinux Decision:** **Reject both Akonadi and EDS suites from standard Tamlinux installations.** Provide terminal-based PIM tools (`calcurse`, `aerc`, `neomutt`) and lean, file-backed Quickshell widgets for calendar display.

---

### 2.9 Desktop Control & System Settings

- **GNOME Control Center (`gnome-control-center`):** Hard-coupled to `gnome-shell`, `mutter`, `accountsservice`, and `gnome-settings-daemon`. It cannot run meaningfully outside a running GNOME Shell session. **Disqualified.**
- **KDE System Settings (`systemsettings`):** Configures KWin, Plasma desktop panels, and KDE workspace components. Under Sway + Quickshell, 90% of its configuration modules (KCMs) are irrelevant or non-functional. **Disqualified.**
- **Tamlinux Requirement:** Tamlinux requires its own dedicated configuration surface:
  - System settings and package management via the **`tam`** CLI (`tam install`, `tam update`, `tam inspect`).
  - Display geometry and multi-monitor management via **`fred.monitor`**.
  - Audio, brightness, and keybindings via Tamlinux native Quickshell control overlays.

---

## 3. Root-stock Compatibility Analysis (Void Linux + `runit` + `seatd`)

A critical requirement of Tamlinux is that applications must run reliably on the target **Root-stock**: a minimal installation of **Void Linux** supervised by **`runit`** and arbitrated by **`seatd`**, with no `systemd` PID 1 and no `elogind` emulation layer.

### 3.1 Why KDE Frameworks 6 Excels on Void Linux

KDE Frameworks (KF6) was engineered around modularity and cross-platform portability:
1. **Tiered Dependency Architecture:**
   - *Tier 1 (e.g., KArchive, KConfig, KCoreAddons, Solid, Sonnet):* Depend solely on Qt and standard C/POSIX runtimes. Zero D-Bus or desktop environment dependencies.
   - *Tier 2 (e.g., KAuth, KCompletion, KCrash, KJobWidgets):* Depend only on Tier 1 and Qt.
   - *Tier 3 (e.g., KIO, KParts, KTextEditor, KXmlGui):* Higher-level application components; talk standard D-Bus protocols.
2. **Init & Seat Agnosticism:** None of the core KF6 libraries require `systemd-logind` or `systemd --user`. Hardware inspection in `Solid` cleanly queries `udev` and fallback sysfs paths when monolithic daemons are missing.
3. **Void Packaging Health:** Void Linux maintains first-class binary packages for Qt 6, KDE Frameworks 6, and core KDE Gear applications (Kate, Okular, Dolphin, Ark, KCalc).

### 3.2 Where GNOME Applications Encounter Root-stock Friction

1. **The `logind` Dependency:** Many GNOME utilities query `org.freedesktop.login1` for session status, power state, and idle management. In a pure `seatd` environment without `elogind`, applications log repeated D-Bus timeout errors.
2. **XDG Desktop Portals:** GNOME applications expect `xdg-desktop-portal-gnome`. Under Sway, this portal fails because `org.gnome.Mutter` is absent. Tamlinux must deploy `xdg-desktop-portal-wlr` combined with `xdg-desktop-portal-gtk`.
3. **Background Daemon Lifecycle:** GNOME apps assume that helpers (Tracker, GVFS volume monitors) are terminated automatically by `systemd --user` session targets. Under `runit`, these helpers can linger across session restarts unless cleaned up by explicit logout traps.

---

## 4. Cultivar Compatibility Analysis (Sway + Quickshell + Tamarack)

The Tamlinux Cultivar is a keyboard-centric tiling environment running **Sway** on **wlroots** with a **Quickshell** desktop shell styled according to the **Tamarack** design tokens.

### 4.1 Window Decoration & Screen Real Estate

- **Libadwaita / GTK 4 (GNOME):** Enforces Client-Side Decorations (CSD). Windows render a thick top headerbar containing window controls, titles, and action buttons. In Sway's auto-tiling layout:
  - Headerbars waste 40–50 physical pixels of vertical screen height.
  - Window control buttons (close/minimize) are redundant when window lifecycle is managed via keyboard bindings (`Super+Q`, `Super+Shift+C`).
  - While CSS hacks (`~/.config/gtk-4.0/gtk.css`) can suppress headerbars, Libadwaita frequently breaks external CSS overrides across point releases.
- **Qt 6 / KF6 (KDE):** Natively supports Server-Side Decorations (SSD). When running under Sway, KDE applications detect `xdg-decoration-unstable-v1`, surrender window border rendering to Sway, and maximize content area. Menubars can be collapsed into a compact hamburger icon.

### 4.2 Theming Sovereignty & Tamarack Palette

Tamlinux enforces a unified visual palette (**Tamarack**):
- **Qt 6 Integration:** Qt reads color palettes directly from `~/.config/kdeglobals` and standard Qt style plugins (`breeze`, `qt6ct`). Applying the Tamarack palette to Qt applications guarantees consistent background, foreground, selection, and accent colors across Quickshell and KDE applications.
- **Libadwaita Barrier:** Libadwaita intentionally rejects standard GTK `settings.ini` theme switches, strictly enforcing its built-in Adwaita palette. Overriding this requires third-party tools like `adw-gtk3` and manual stylesheet injections.

---

## 5. Strategic Roadmap: The Three Application Pathways

To build the application suite for Tamlinux, we recommend categorizing candidate software into three disciplined paths:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   TAMLINUX APPLICATION STRATEGY                        │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. CHERRY-PICK     │ 2. SANDBOX & PORT  │ 3. CULTIVAR NATIVE           │
│ Direct Upstream    │ Configured / Shim  │ Built in Quickshell + libtam │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ • Okular           │ • Dolphin          │ • Tamlinux Settings          │
│ • Kate             │   (Baloo disabled) │ • Tamlinux Launcher          │
│ • KCalc            │ • Haruna (mpv core)│ • fred.clock / Calendar      │
│ • Filelight        │ • Loupe            │ • fred.sysinfo telemetry     │
│ • Ark              │   (bwrap userns)   │ • Display/Audio Overlays     │
│ • KDE Connect      │ • Papers (doc)     │ • CLI tools (tam explain)    │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

### Path 1: Cherry-Pick Standouts for Immediate Inclusion
High-value, lightweight, self-contained applications that run with zero systemd couplings, provide outstanding ergonomics, and integrate smoothly with Sway and Qt:
1. **Okular:** Universal document and PDF viewer.
2. **Kate:** Graphical code and text editor.
3. **KCalc:** Scientific and mathematical calculator.
4. **Filelight:** Interactive radial disk space analyzer.
5. **Ark:** Lightweight archive manager.
6. **KDE Connect:** Cross-device mobile integration daemon and client.

### Path 2: Selective Configuration & Sandboxed Porting
Applications with exceptional utility that require specific configuration recipes or environment guards to prevent resource thrashing or portal friction:
1. **Dolphin (File Manager):** Include Dolphin, but ship declarative defaults in `/etc/skel/.config/baloofilerc` disabling file indexing (`Indexing-Enabled=false`). This secures best-in-class dual-pane browsing while eliminating background polling.
2. **Haruna (Media Player):** Package Haruna with native VAAPI hardware acceleration enabled, providing lean video playback on modern GPUs and efficient software decoding on older chips.
3. **Loupe (Image Viewer):** If unprivileged user namespaces are enabled in the root-stock kernel, Loupe provides memory-safe image decoding via Glycin and Bubblewrap.

### Path 3: Tamlinux Cultivar Native Suite (Custom QML Applications)
Areas where both KDE and GNOME software are ill-suited (due to monolithic desktop coupling, heavy daemons, or mismatched tiling paradigms). Tamlinux should provide native Quickshell / Qt Quick tools:
1. **Tamlinux Settings:** A declarative, keyboard-navigable control panel built on Quickshell and `libtam` to manage display layouts (`fred.monitor`), audio volume, network profiles, and theme toggles.
2. **Tamlinux Launcher & Menu:** Fast keyboard application launcher and power menu integrated directly into the shell.
3. **Tamlinux Calendar & Clock:** A clean, file-backed (iCal/CalDAV via curl/vdirsyncer) calendar viewer built into `fred.clock`, entirely replacing Akonadi and Evolution-Data-Server.
4. **Tamlinux System Monitor:** Expanding `fred.sysinfo` into an interactive full-screen process inspector reading directly from `/proc` and `sysfs`.

---

## 6. Comprehensive Evaluation Matrix

| Application | Suite | Primary Role | Toolkit | Dependencies & Daemons | Void/runit Portability | Cultivar Alignment | Tamlinux Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Okular** | KDE | Document / PDF Viewer | Qt 6 / KF6 | Poppler-qt6; no daemons | **Flawless** | **Excellent** | **Selected (Core)** |
| **Kate** | KDE | Advanced Text Editor | Qt 6 / KF6 | SyntaxHighlighting, KIO; no daemons | **Flawless** | **Excellent** | **Selected (Core)** |
| **KCalc** | KDE | Scientific Calculator | Qt 6 / KF6 | GMP, MPFR; no daemons | **Flawless** | **Excellent** | **Selected (Core)** |
| **Filelight** | KDE | Disk Space Visualizer | Qt 6 / QML | KF6; no daemons | **Flawless** | **Excellent** | **Selected (Core)** |
| **Ark** | KDE | Archive Manager | Qt 6 / KF6 | libarchive; no daemons | **Flawless** | **Excellent** | **Selected (Core)** |
| **KDE Connect** | KDE | Mobile Device Sync | Qt 6 / KF6 | D-Bus, QCA; standalone daemon | **Flawless** | **Excellent** | **Selected (Optional)** |
| **Dolphin** | KDE | File Manager | Qt 6 / KF6 | KIO; Baloo (disable via config) | **High** (disable Baloo) | **High** (SSD friendly) | **Selected (Conditioned)** |
| **Haruna** | KDE | Video Player | Qt 6 / QML | libmpv; no daemons | **Flawless** | **Excellent** | **Selected (Media)** |
| **Gwenview** | KDE | Image Viewer / Tools | Qt 6 / KF6 | Exiv2; optional Baloo | **High** | **High** | **Selected (Images)** |
| **Loupe** | GNOME | Sandboxed Image Viewer | GTK 4 / Rust | Glycin, Bubblewrap, seccomp | **Moderate** (needs userns) | **Moderate** (CSD bar) | **Evaluated** |
| **Papers** | GNOME | Modern Document Viewer | GTK 4 / Libadwaita | Poppler-glib, libarchive | **High** | **Moderate** (CSD bar) | **Evaluated** |
| **Nautilus** | GNOME | File Manager | GTK 4 / Libadwaita | GVFS, TinySPARQL/Tracker, dconf | **Moderate** (heavy indexers)| **Moderate** (CSD bar) | **Evaluated / Alternative** |
| **GNOME Text Editor** | GNOME | Clean Text Notepad | GTK 4 / Libadwaita | GtkSourceView5, libspelling | **High** | **Moderate** (CSD bar) | **Evaluated** |
| **Decibels** | GNOME | Waveform Audio Player | GTK 4 / GJS | GStreamer, GJS (JavaScript runtime) | **High** | **Low** (GJS memory) | **Rejected** (resource efficiency) |
| **KMail / Akonadi** | KDE | Email Client & Engine | Qt 6 / KF6 | Akonadi, MariaDB/SQLite, agents | **Poor** (daemon fragility) | **Low** (memory/poll churn)| **Rejected** (Resource Tax) |
| **GNOME Calendar (EDS)**| GNOME | Calendar Client | GTK 4 / Libadwaita | Evolution-Data-Server, geoclue | **Poor** (daemon fragility) | **Low** (daemon sprawl) | **Rejected** (Resource Tax) |
| **GNOME Control Center** | GNOME | System Settings | GTK 4 / Libadwaita | GNOME Shell, Mutter, systemd | **Incompatible** | **Incompatible** | **Rejected** (Hard Coupling) |
| **Plasma System Settings**| KDE | Plasma Settings | Qt 6 / QML | Plasma workspace, KWin | **Incompatible** | **Incompatible** | **Rejected** (Hard Coupling) |

---

## Conclusion & Recommended Action Plan

The survey reveals a decisive architectural alignment:

1. **KDE Frameworks 6 and modular KDE Gear applications align substantially better with Tamlinux than GNOME's software stack.** Because Tamlinux's Cultivar shell is built on **Qt Quick / QML**, KDE applications naturally share memory pages, font rendering caches, and graphics contexts with the desktop shell.
2. **KDE applications respect windowing protocols under Sway.** They support Server-Side Decorations, allowing Sway to manage window borders cleanly without wasting vertical screen space on redundant headerbars.
3. **KDE's modular libraries (KF6 Tiers 1–3) are completely free of `systemd` couplings**, compiling and executing flawlessly on minimal **Void Linux (`runit` + `seatd`)** and **antiX** root-stocks.
4. **Care must be taken to prune heavy daemons.** The background indexing daemons (Baloo in KDE, Tracker/TinySPARQL in GNOME) and the heavy PIM database daemons (Akonadi in KDE, Evolution-Data-Server in GNOME) must be excluded or disabled by default to uphold Tamlinux's **resource efficiency** and preserve the 2006 vintage hardware floor.
5. **Standout applications (Okular, Kate, KCalc, Filelight, Ark, Dolphin without Baloo) can be directly included in Tamlinux.** System settings, status indicators, and desktop menus should remain native Tamlinux Cultivar components built in Quickshell and `libtam`.
