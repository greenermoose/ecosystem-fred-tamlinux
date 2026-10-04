# AI Collaboration & Provenance

This repository practices transparent AI-assisted engineering. The patches it
records were written by AI coding agents under Fred's direction; this file and
[`docs/ai/sessions.md`](docs/ai/sessions.md) say which tool, which model, and
what Fred asked for. Every commit co-authored with an agent carries
`Co-authored-by:`, `AI-Tool:` and `AI-Model:` trailers.

This matters more here than in most repos: several upstream projects (notably
the Hyprland organisation) refuse AI-authored contributions, which is one
reason these fixes are published as fork branches and recipes rather than
pull requests. See [`README.md`](README.md) §"Why this exists".

## How to read this record

This repository follows the Tamlinux [AI provenance standard](https://github.com/greenermoose/tamlinux/blob/main/docs/ai-provenance-standard.md). In
brief: commits made with AI help carry `AI-Tool` and `AI-Model` trailers, and
each session record in [`docs/ai/`](docs/ai/) gives the date, tool version,
model, Fred's guiding prompts verbatim, the commits, and the decisions. Session
transcripts are retained privately by the author, so the records carry no
session IDs or local transcript paths.

---

## 1. Fred's Multi-Agent AI Toolchain

| Tool & Interface | CLI Version | Backing Models | Primary Role |
| :-- | :-- | :-- | :-- |
| **Claude Code** (`claude`) | `2.1.289` | Claude Opus 5.5 (`claude-opus-5-5`), Claude Opus 5 | Architecture, planning, this repository's design and first content; diagnosis and patches for the hyprland and omawrite rigs; aquamarine 0.15.1 and hyprland 0.56.2-4.1 rebases; gtk4 retirement. |
| **Codex CLI** (`codex`) | `0.160.0` | `gpt-6-astra`, `gpt-5.6-sol`, `gpt-6-sol` | Second opinion on plans and upstream survey documentation. |
| **Codex API** | N/A (API session) | GPT-6 | Diagnosed and patched the Aquamarine null connector shutdown crash. |
| **Antigravity CLI** (`agy`) | `1.2.16` | Gemini 3.8 Flash (High) | Coding and implementation on the plugin side; omawrite close-button and 80-column patches; documentation audits and repository alignment. |
| **OpenCode** (`opencode`) | `1.18.31` | Big Pickle | Arch/Omarchy Q&A. |
| **Grok CLI** (`grok`) | `1.0.25` | Grok 4.6 | Workstation support. |
| **Cursor** (`cursor`) | `3.23.12` | `composer` | Omarchy bar-tooltip fractional scaling patches; daily CLI rename and branding. |

Versions captured 2026-10-04 (`claude --version`, `agy --version`, `codex --version`, `opencode --version`, `grok --version`, `cursor --version`).

## 2. Milestones

| Milestone | Version | Primary AI Partner | Notes |
| :-- | :-- | :-- | :-- |
| Registry design, policy, scaffold, first four packages | `v0.1.0` | Claude Code `2.1.274` (Claude Opus 5) | Fork/registry/consumer three-tier design; upstream-engagement policy after Hyprland#16290 was auto-closed; `omarchy-fred-ecosystem` command. |
| CLI rename to `tam-ecosystem` | `v0.1.0` | Cursor `3.21.16` (`composer`) | Daily name `tam-ecosystem`; long alias `ecosystem-fred-tamlinux`. |
| Tamlinux branding | `v0.1.0` | Cursor `3.21.16` (`composer`) | README and `ecosystem.json` description say Fred's Tamlinux workstations. |

## 3. Per-package origin of the patches

| Package | Patch | Written by | Human decisions |
| :-- | :-- | :-- | :-- |
| gtk4 | dmabuf format-table munmap | upstream (GTK MR !10166); backport and rig by Claude Code (2026-09-06); retired 2026-10-04 | Fred: patch rather than wait; retire when Arch 1:4.22.5-1 shipped |
| aquamarine | disable KMS before disconnect | klaudworks (upstream PR #395), carried unchanged; rig by Claude Code (2026-09-11); retired 2026-10-04 | Fred: adopt the closed PR; retired when upstream #410 merged into 0.15.1 |
| aquamarine | guard null connectors during async event flush | Codex API (GPT-6; fork patchset commit `1291a49`, 2026-09-22) | Fred: asked to fix the proven shutdown segfault locally; keep active in 0.15.1-1.1 |
| hyprland | inherit DPMS state on connect | Claude Code (Claude Opus 5; fork commit `68a4dfe2`, 2026-09-13) | Fred: reproduce with a 15 s idle timeout, ship locally |
| hyprland | idle-notify inhibit unchanged no-op | Claude Code (Claude Opus 5; fork commit `a7a03d6f`, 2026-09-17) | Fred: overnight incident triage, ship locally |
| hyprland | dpms state per monitor | Claude Code (Claude Opus 5; fork commit `3e4303a7`, 2026-09-17) | Fred: isolate per-monitor blanking from global mouse wake, ship locally |
| omawrite | in-window close button | Antigravity `agy` (Gemini 3.8 Flash (High); 2026-09-10) | Fred: requested the control |
| omawrite | always open the CLI file | Claude Code, 2026-09-11 (`fix(omawrite): verify desktop review documents`) | Fred: open requested file rather than Untitled.md |
| omawrite | stale "File removed" dialog | Claude Code (Claude Opus 5; 2026-09-11, config commit `d5c9187`) | Fred: agents rewrite open files; Reload must work |
| omawrite | shortcuts dialog binding loop | Claude Code (Claude Opus 5; fork commit `293ba59`, 2026-09-17; PR omacom/omawrite#72) | — |
| omawrite | editor width 65 → 80 columns | Antigravity `agy` (Gemini 3.8 Flash (High); 2026-09-17) | Fred: 65 columns wrapped standard text on wide displays |
| omarchy | bar-tooltip border padding, scale-safe size, bubble sizing | Cursor (composer; fork commits `afe057b0`, `dd0ad03c`, `6edc29cc`, 2026-09-21) | Fred: bar tooltip clipped bottom border on fractional display scale (Dell 1.25×); verify locally before filing upstream |

Each attribution above was taken from the session transcript, not
reconstructed from memory. The transcripts are retained privately by the
author; see [How to read this record](#how-to-read-this-record).

## 2026-09-22 repository rename

Codex CLI `0.155.1` (`gpt-6-sol`) updated canonical GitHub links for `ecosystem-fred-tamlinux`. [Session record](docs/ai/2026-09-22-github-repository-rename.md).

## 2026-09-23 upstream survey foundation

Codex CLI `0.156.1` (`gpt-6-sol`) established the root upstream reference
and dated survey directory for this repository. This was documentation only;
no field survey or runtime change was made.
[Session record](docs/ai/2026-09-23-upstream-survey-foundation.md).

## 2026-09-28 private session IDs

Claude Code `2.1.283` (`claude-opus-5-5`) removed session IDs and local
transcript paths from this repository's AI records and linked the public
provenance standard. Documentation only.
[Session record](docs/ai/2026-09-28-private-session-ids.md).

## 2026-10-04 upstream rebases, GTK4 retirement, and review workflow update

Claude Code `2.1.289` (`claude-opus-5-5`) rebased aquamarine onto 0.15.1-1.1
(dropping the merged KMS teardown patch, retaining the null connector guard
#383), rebuilt hyprland to 0.56.2-4.1 against Arch 0.56.2-4, retired gtk4 after
Arch shipped 1:4.22.5-1, corrected the pacman repository precedence rule in
README/ECOSYSTEM.md, and updated `omawrite-local-patch-check` to reflect the
transition from `omawrite-review` to `micro-review`.

## 2026-10-04 documentation status audit and synchronization

Antigravity CLI `1.2.16` (`gemini-3.8-flash-high`) audited all repository
records against the live workstation state, aligning `ecosystem.json`,
`ECOSYSTEM.md`, `UPSTREAM.md`, `packages/hyprland/README.md`,
`packages/omawrite/README.md`, `retired/gtk4/README.md`, and AI session history.
