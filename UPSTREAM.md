# Upstream Sources and Field Surveys

This repository maintains two primary records of upstream open-source software:
1. **The Carried Patches Registry:** Records carried patches to third-party packages. Start with [ECOSYSTEM.md](ECOSYSTEM.md), [ecosystem.json](ecosystem.json), and the [package records](packages/) for the exact upstream release, fork branch, patch source, and retirement condition of each carried fix. The current active package set includes aquamarine, Hyprland, and omarchy (with gtk4 and omawrite retired).
2. **The Considered Packages Surveys:** Comprehensive architectural surveys across 11 system layers in [`surveys/`](surveys/), covering 66 packages and dependencies evaluated for Tamlinux across C libraries, distributions, package managers, init systems, windowing protocols, compositors, GUI toolkits, shells, virtualization, and developer tools.

For a Fred-requested survey of a patch or replacement, inspect the recorded upstream project first, then its newer releases, issues, forks, and independent approaches. Save a dated comparison in [upstream/](upstream/) or [surveys/](surveys/) and link it here. A finding does not by itself authorize changing a package, publishing a patch, or contacting upstream. Keep package ancestry and authorship in the package record and fork history.
