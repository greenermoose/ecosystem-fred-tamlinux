# Survey: Sustainability, Hardware Longevity, and the Suspra Mission

## Overview

Software development often proceeds under the assumption of infinite resources: faster CPUs, gigabytes of surplus RAM, multi-terabyte SSDs, and constant high-speed cloud connectivity. This assumption drives a vicious cycle of software bloat, forced hardware obsolescence, and millions of tons of toxic electronic waste (e-waste).

Tamlinux is motivated by an alternative vision: **computing as a sustainable, enduring craft**.

This survey explores how Tamlinux connects to the **Suspra** software suite, local community resilience initiatives (such as the Earth Day Festival in Brunswick), and the technical discipline of supporting hardware across its full lifespan.

---

## 1. The Ecological Cost of Planned Obsolescence

### The Hardware Replacement Treadmill
Every year, millions of functional computers, laptops, and displays are discarded because newer operating systems and bloated web applications refuse to run on them. 
- Over 70% of a computer's total lifetime carbon footprint is generated during its **manufacturing and extraction phase** (mining rare earth minerals, silicon fabrication, toxic chemical processing), not its operational electricity use.
- Extending the operational lifespan of existing computers from 3–4 years to 10–20 years directly reduces global carbon emissions and curtails e-waste.

### The Software Efficiency Imperative
When an operating system requires 4 GB of RAM just to boot an empty desktop, older computers become unusable. Conversely, an operating system engineered to idle at 150 MB of RAM with efficient CPU rendering breathes a second decade of productive life into existing machines.

---

## 2. Technical Pillars of Hardware Longevity in Tamlinux

Tamlinux establishes concrete engineering standards to ensure durable performance:

1. **The Vintage Hardware Floor (Circa-2006 Baseline):**
   - Tamlinux uses vintage circa-2006 hardware (e.g. Intel Core 2 Duo, 32-bit/64-bit transitions, Intel GMA 950 graphics, 1–2 GB RAM) as an active validation baseline.
   - If a core desktop component cannot function acceptably on this floor, it must be evaluated for software fallbacks or replacement.

2. **CPU Software Rendering (`pixman` on wlroots):**
   - Many vintage machines feature graphics processors that lack modern OpenGL 3.0 or Vulkan drivers.
   - Sway's ability to run with pure CPU software rendering (`WLR_RENDERER=pixman`) via the Linux kernel's Direct Rendering Manager (DRM/KMS) ensures that a graphical desktop displays cleanly without requiring 3D GPU acceleration.

3. **ZRAM Swap Compression:**
   - Rather than thrashing slow mechanical hard drives or wearing out solid-state disks with heavy virtual memory paging, Tamlinux utilizes in-memory compressed RAM swap (`zram`). This provides low-RAM machines with effectively double their physical memory buffer.

4. **Eliminating Background Polling and Daemons:**
   - Background polling loops wake up the CPU constantly, preventing low-power C-states and draining laptop batteries.
   - Tamlinux eliminates unneeded background daemons, favors event-driven architectures (`epoll`, Wayland event loops), and retires autonomous background AI loops (D139, D140).

---

## 3. The Suspra Suite and Community Resilience

### Context & Bookmarked Resources
- **Bookmarks:**
  - `http://localhost:8000/` (Local development server)
  - EDIB - Staging (`https://suspra-earthday-staging.netlify.app/`)
  - Earth Day Festival in Brunswick (`https://earthdayinbrunswick.com/`)
- **Status in Tamlinux:** `selected` (Core application mission)

### The Three Suspra Tiers (D116)
In Decision D116, Fred clarified the relationship between Tamlinux and Suspra:
- **Tier 1 (Web Experience):** Accessible via standard web browsers at `suspra.com` for universal accessibility.
- **Tier 2 (Virtualized Experience):** Packaged virtual environments on macOS and Windows hosts for cross-platform developers.
- **Tier 3 (Native Tamlinux Workstation):** The full, native, sovereign experience running directly on Tamlinux hardware with zero cloud dependencies and maximum capability.

### Local Computing and Community Sovereignty
Suspra represents technology dedicated to environmental stewardship and civic action:
- **Offline Sovereignty:** Community data and local sustainability projects must not rely on fragile external cloud connections. Tamlinux provides a completely self-sufficient environment where web apps, databases, and offline documentation operate smoothly on local hardware.
- **Community Empowerment:** By proving that low-cost, refurbished computers can run a modern, elegant, keyboard-driven Linux workstation, Tamlinux empowers community members, schools, and environmental organizations with sovereign digital tools.

---

## Summary

Tamlinux is built on the principle that the most sustainable computer is the one you already own. By combining rigorous software discipline, copyleft freedom, and local computing architecture, Tamlinux proves that Free Software can be a powerful engine for environmental sustainability and civic resilience.
