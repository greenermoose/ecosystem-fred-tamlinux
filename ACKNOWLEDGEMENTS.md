# Acknowledgements — ecosystem-fred-tamlinux

Researched 2026-10-09. Thank you to the people whose software, designs, maintenance, testing and public reports make this work possible.

Names are ordered alphabetically by the displayed public name (case and accents ignored for sorting). A self-published profile name is used when available; otherwise the public handle or name in an upstream credit is retained. No private identities, locations, phone numbers or commit-email harvesting are included. Affiliations below are self-reported public profile fields or explicitly attributed project roles; they are not independently verified employment records. Contact links and emails are only those publicly offered by the person or their project.

Tamlinux additions are distributed under GPL-3.0-or-later; see [LICENSE](LICENSE). Upstream works retain their own terms. Copyright notices are attributed to works and their stated holders, not inferred from contributor counts. The Free Software Foundation copyright on a GPL/LGPL license document is not treated as ownership of the software. These thanks supplement, and do not replace, required license and source notices.

[UPSTREAM.md](UPSTREAM.md) records this repository’s code ancestry and design references. A runtime dependency, design inspiration, bug report and copied component are different contributions; the entries say which connection is established.

Each named entry identifies an authored component, a documented design influence, a specific change or public report, or responsibility for a foundation used by this repository. Contributor-roster membership alone is not enough for a named entry. Wider communities are credited collectively below.

**Version scope:** Hyprland and Aquamarine credits describe the temporary Tamlinux 0.x platform and its compatibility patches. Tamlinux’s [public roadmap](https://github.com/greenermoose/tamlinux/blob/main/README.md) removes Hyprland at 1.0 in favor of Sway. Remove these dependency-only entries from future acknowledgements when the stack is no longer used. Historical forks and any retained derived code keep their applicable source notices.

## People

| Public name and brief background / contribution | Public affiliation and contact |
| --- | --- |
| **Aleksandra Samuļenkova** — IBM Plex contributor: Cyrillic and Greek design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Andrew Gaspar (`AndrewGaspar`)** — Author of the upstream wrong-pointer munmap fix backported for GTK4 and later retired from the local patch set. [Work, license and copyright](#gtk). [Evidence](https://github.com/GNOME/gtk/commit/a8a5692ce3c334672ac325cf8f1257a138843bf6) | @facebook [Public profile / project contact](https://github.com/AndrewGaspar) |
| **Barbara Bigosińska** — IBM Plex contributor: Font production and Latin design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **David Heinemeier Hansson (`dhh`)** — Creator of Omarchy. Its shell, UI conventions and plugin host form the current base and the documented ancestry of several fred.* components. [Work, license and copyright](#omarchy). Original Omawrite author; the editor source is the base of the Tamlinux patch fork. [Work, license and copyright](#omawrite). [Evidence 1](https://github.com/omacom/omarchy) [Evidence 2](https://github.com/omacom/omawrite) [Evidence 3](https://github.com/omacom/omarchy/commit/b83505d7380bbe0525f56f5dc556c103848d34d5) | 37signals [Public profile / project contact](https://github.com/dhh); [Website](https://dhh.dk); [Public email](mailto:dhh@hey.com) |
| **Diana Ovezea** — IBM Plex contributor: Font production and Latin design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **DK (`dkIT25`)** — Public reporter of issue #383, with a matching null-connector diagnosis and proposed guard independently corroborating the local crash fix. This does not assign authorship of Fred’s separately recorded patch. [Work, license and copyright](#aquamarine). [Evidence](https://github.com/hyprwm/aquamarine/issues/383) | No affiliation stated in the inspected public profile/credit. [Public profile / project contact](https://github.com/dkIT25) |
| **Edgar Walthert** — IBM Plex contributor: Font engineering and Latin design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Fred Horch (`greenermoose`)** — Tamlinux creator and maintainer. Directed this repository’s design, implementation, testing and upstream integration, including the separately documented AI-assisted work. [Evidence](https://github.com/greenermoose/tamlinux) | No affiliation stated in the inspected public profile/credit. [Public profile / project contact](https://github.com/greenermoose) |
| **Jasper Terra** — IBM Plex contributor: Font engineering and Latin design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Kristian Høgsberg** — Wayland’s original author and a named copyright holder. Its client/compositor protocol enables both the current shell and the planned Sway desktop. [Work, license and copyright](#wayland). [Evidence](https://github.com/wayland-mirror/wayland/blob/main/COPYING) | Wayland project [Public profile / project contact](https://wayland.freedesktop.org/) |
| **Lars Knoll** — Longtime Qt engineer and Qt chief maintainer at the time of the project’s 2020 technical conference. His engineering leadership helped develop the UI framework used by Quickshell and Omawrite. [Work, license and copyright](#qt). [Evidence](https://www.qt.io/development/resources/videos/foundation-for-the-future-are-we-excited-qt-virtual-tech-con-2020) | Qt project; historical role stated in the 2020 source [Public profile / project contact](https://www.qt.io/development/resources/videos/foundation-for-the-future-are-we-excited-qt-virtual-tech-con-2020) |
| **lemachinarbo (`lemachinarbo`)** — Omawrite developer whose source changes improve editor/theme colors, prevent link-paste layout freezes and bound portal D-Bus calls. These changes are part of the editor inherited by the Tamlinux fork. [Work, license and copyright](#omawrite). [Evidence](https://github.com/omacom/omawrite/commit/c885e935c9cd142418364528cc5d48bd52c06d19) | No affiliation stated in the inspected public profile/credit. [Public profile / project contact](https://github.com/lemachinarbo) |
| **Marko Hrastovec** — IBM Plex contributor: Font production. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | IBM Plex project [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Mike Abbink** — IBM Plex contributor: Creative direction and design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | IBM Design [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Nico Duldhardt (`klaudworks`)** — Author of the KMS disconnect fix in PR #395, carried historically by Tamlinux before it was superseded; retained here as historical patch credit. [Work, license and copyright](#aquamarine). [Evidence](https://github.com/hyprwm/aquamarine/pull/395) | Self-employed Contractor [Public profile / project contact](https://github.com/klaudworks) |
| **outfoxxed (`outfoxxed`)** — Lead developer of Quickshell, the Qt Quick toolkit that runs the shell, bar widgets, layer surfaces, IPC and helper processes. [Work, license and copyright](#quickshell). [Evidence](https://quickshell.org/) | No affiliation stated in the inspected public profile/credit. [Public profile / project contact](https://github.com/outfoxxed); [Website](https://outfoxxed.me); [Public email](mailto:outfoxxed@outfoxxed.me) |
| **Pablo Gámez** — IBM Plex contributor: Font production. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | IBM Plex project [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Paul van der Laan** — IBM Plex contributor: Type direction and design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Pieter van Rosmalen** — IBM Plex contributor: Type direction and design. Omawrite includes the font family; this credits the upstream typeface project, not authorship of the editor. [Work, license and copyright](#ibm-plex). [Evidence](https://www.ibm.com/plex/specs/) | Bold Monday [Public profile / project contact](https://www.ibm.com/plex/specs/) |
| **Ryan Hughes (`ryanrhughes`)** — Omarchy shell and plugin-system contributor. The v4.0.4 history records work on widget scaling, theme tokens, built-in plugins and plugin management. [Work, license and copyright](#omarchy). [Evidence 1](https://github.com/omacom/omarchy) [Evidence 2](https://github.com/omacom/omarchy/commit/4f0bdb790b75603a6506daa6603b3576349373d6) [Evidence 3](https://github.com/omacom/omarchy/commit/e8fc2ef08f3aad9f6219b85a8ab8884f27fc953a) | Oodle [Public profile / project contact](https://github.com/ryanrhughes); [Website](https://heyoodle.com); [Public email](mailto:ryan@heyoodle.com) |
| **Vaxry (`vaxerski`)** — Hypr Development contributor; upstream display-backend maintenance supports the carried display fixes, including PR #410. [Work, license and copyright](#aquamarine). Creator of Hyprland. Its monitor/workspace control and IPC support the current 0.x desktop while Tamlinux moves to Sway; this dependency credit ends when Hyprland is removed. [Work, license and copyright](#hyprland). [Evidence 1](https://github.com/hyprwm/Hyprland) [Evidence 2](https://github.com/hyprwm/aquamarine/pull/410) | @hyprwm [Public profile / project contact](https://github.com/vaxerski); [Website](https://vaxry.net) |

## Works, licenses and stated copyright notices

The source links below are the authority for complete notices and exceptions. A short notice here is a reference, not a replacement license text. Names in a copyright notice are reproduced as the holder wrote them even when the person now uses a different public display name.

<a id="aquamarine"></a>
### Aquamarine

- **Connection:** Display backend of the temporary Hyprland stack and source of the compatibility fork; its dependency-only credits retire with that stack.
- **License:** BSD-3-Clause. [License/source notices](https://github.com/hyprwm/aquamarine/blob/main/LICENSE).
- **Stated copyright / limits:** Copyright (c) 2024, Hypr Development
- **Source:** [Upstream project](https://github.com/hyprwm/aquamarine). [Wider contributor community](https://github.com/hyprwm/aquamarine/graphs/contributors).

<a id="gtk"></a>
### GTK

- **Connection:** Historical GTK4 crash-fix backport recorded in the ecosystem registry.
- **License:** LGPL-2.1-or-later; per-file notices apply. [License/source notices](https://github.com/GNOME/gtk/blob/main/COPYING).
- **Stated copyright / limits:** Many GTK contributors; the fix commit does not establish exclusive ownership.
- **Source:** [Upstream project](https://github.com/GNOME/gtk/blob/main/COPYING).

<a id="hyprland"></a>
### Hyprland

- **Connection:** Temporary compositor for the Tamlinux 0.x transition and source of the compatibility fork. The public roadmap removes Hyprland at 1.0.
- **License:** BSD-3-Clause. [License/source notices](https://github.com/hyprwm/Hyprland/blob/main/LICENSE).
- **Stated copyright / limits:** Copyright (c) 2022-2026, vaxerski
- **Source:** [Upstream project](https://github.com/hyprwm/Hyprland). [Wider contributor community](https://github.com/hyprwm/Hyprland/graphs/contributors).

<a id="ibm-plex"></a>
### IBM Plex

- **Connection:** Typeface bundled in the Omawrite fork.
- **License:** OFL-1.1. [License/source notices](https://github.com/omacom/omawrite/blob/master/fonts/OFL.txt).
- **Stated copyright / limits:** Copyright © 2017 IBM Corp. with Reserved Font Name "Plex".
- **Source:** [Upstream project](https://github.com/omacom/omawrite/blob/master/fonts/OFL.txt).

<a id="omarchy"></a>
### Omarchy

- **Connection:** Current Tamlinux 0.x base, shell/plugin integration, and documented cloned components.
- **License:** MIT. [License/source notices](https://github.com/omacom/omarchy/blob/quattro/LICENSE).
- **Stated copyright / limits:** Copyright (c) David Heinemeier Hansson
- **Source:** [Upstream project](https://github.com/omacom/omarchy). [Wider contributor community](https://github.com/omacom/omarchy/graphs/contributors).

<a id="omawrite"></a>
### Omawrite

- **Connection:** Qt editor whose source is carried in the Tamlinux patch fork.
- **License:** MIT. [License/source notices](https://github.com/omacom/omawrite/blob/master/LICENSE).
- **Stated copyright / limits:** Copyright (c) 2026 David Heinemeier Hansson
- **Source:** [Upstream project](https://github.com/omacom/omawrite). [Wider contributor community](https://github.com/omacom/omawrite/graphs/contributors).

<a id="qt"></a>
### Qt / Qt Quick

- **Connection:** UI, QML, controls and graphics foundations used by the shell and Omawrite.
- **License:** Qt module-specific LGPL/GPL or commercial terms; see installed module licenses. [License/source notices](https://www.qt.io/licensing/open-source-lgpl-obligations).
- **Stated copyright / limits:** The Qt Company and many other contributors; module source files retain their notices.
- **Source:** [Upstream project](https://www.qt.io/licensing/open-source-lgpl-obligations).

<a id="quickshell"></a>
### Quickshell

- **Connection:** Runtime for the QML shell and fred.* widgets.
- **License:** LGPL-3.0; consult file SPDX headers for applicable terms. [License/source notices](https://github.com/quickshell-mirror/quickshell/blob/master/LICENSE).
- **Stated copyright / limits:** No project-specific holder established from the inspected license text; see source notices. The license-text author is not assumed to own the software.
- **Source:** [Upstream project](https://github.com/quickshell-mirror/quickshell). [Wider contributor community](https://github.com/quickshell-mirror/quickshell/graphs/contributors).

<a id="wayland"></a>
### Wayland

- **Connection:** Display protocol used by the current desktop and the planned Sway desktop; a foundation independent of Hyprland.
- **License:** MIT-style license; consult individual file notices. [License/source notices](https://github.com/wayland-mirror/wayland/blob/main/COPYING).
- **Stated copyright / limits:** Copyright © 2008-2012 Kristian Høgsberg; Copyright © 2010-2012 Intel Corporation; Copyright © 2011 Benjamin Franzke; Copyright © 2012 Collabora, Ltd.
- **Source:** [Upstream project](https://wayland.freedesktop.org/). [Wider contributor community](https://github.com/wayland-mirror/wayland/graphs/contributors).

## Community credit and coverage

We also thank the wider upstream communities: reviewers, translators, documentation writers, package maintainers, testers, issue reporters and accessibility contributors. The project/community links above recognize their wider work. This researched list emphasizes identifiable connections to this repository; it is not a complete census of every transitive dependency or a claim of endorsement. Public profiles and affiliations can change; the date above identifies this review.

The [Qt contributors](https://code.qt.io/), [Wayland contributors](https://gitlab.freedesktop.org/wayland/wayland), [Arch package maintainers](https://archlinux.org/people/) and their dependency communities provide additional foundations. Their licenses and copyright notices remain in the individual upstream projects and installed packages; no blanket ownership or single license is assigned to those communities.

The broader alphabetical list for the public Tamlinux ecosystem, including design, data, typeface, toolchain and planned-base contributions, is in [Tamlinux’s acknowledgements](https://github.com/greenermoose/tamlinux/blob/main/ACKNOWLEDGEMENTS.md).

To correct a name, attribution, affiliation or contact preference, please open an issue in this repository or contact [Fred’s public account](https://github.com/greenermoose). Only evidence-backed additions should be made; do not infer identities behind pseudonyms.

Research and compilation were AI-assisted by Codex under Fred’s direction. AI systems and provider organizations are not listed as humans; existing AI provenance records, where present, describe their separate role.
