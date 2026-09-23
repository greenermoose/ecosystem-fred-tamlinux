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

## 1. Fred's Multi-Agent AI Toolchain

| Tool & Interface | CLI Version | Backing Models | Primary Role |
| :-- | :-- | :-- | :-- |
| **Claude Code** (`claude`) | `2.1.274` | Claude Opus 5 (`claude-opus-5`) | Architecture, planning, this repository's design and first content; diagnosis and patches for the hyprland and omawrite rigs. |
| **Codex CLI** (`codex`) | `0.154.0` | `gpt-6-astra`, `gpt-5.6-sol` | Second opinion on plans. |
| **Codex API** | N/A (API session) | GPT-6 | Diagnosed and patched the Aquamarine null connector shutdown crash. |
| **Antigravity CLI** (`agy`) | `1.2.3` | Gemini 3.8 Flash (High) | Coding and implementation on the plugin side; omawrite close-button and 80-column patches. |
| **OpenCode** (`opencode`) | `1.18.30` | Big Pickle | Arch/Omarchy Q&A. |
| **Grok CLI** (`grok`) | `1.0.25` | Grok 4.6 | Workstation support. |

Versions captured 2026-09-17 (`claude --version`); others as last recorded in
`omarchy-fred-workspaces/AI_PROVENANCE.md` (2026-09-13).

## 2. Milestones

| Milestone | Version | Primary AI Partner | Notes |
| :-- | :-- | :-- | :-- |
| Registry design, policy, scaffold, first four packages | `v0.1.0` | Claude Code `2.1.274` (Claude Opus 5) | Fork/registry/consumer three-tier design; upstream-engagement policy after Hyprland#16290 was auto-closed; `omarchy-fred-ecosystem` command. |

## 3. Per-package origin of the patches

| Package | Patch | Written by | Human decisions |
| :-- | :-- | :-- | :-- |
| gtk4 | dmabuf format-table munmap | upstream (GTK MR !10166); backport and rig by Claude Code (session `d35cb8fc`, 2026-09-06) | Fred: patch rather than wait; retire-when rule |
| aquamarine | disable KMS before disconnect | klaudworks (upstream PR #395), carried unchanged; rig by Claude Code (2026-09-11) | Fred: adopt the closed PR; authorship preserved on the fork |
| aquamarine | guard null connectors during async event flush | Codex API (GPT-6; fork patchset commit `1cda9c3`, 2026-09-22) | Fred: asked to fix the proven shutdown segfault locally; keep the KMS patch |
| hyprland | inherit DPMS state on connect | Claude Code (Claude Opus 5; fork commit `13fd6355`, 2026-09-13) | Fred: reproduce with a 15 s idle timeout, ship locally |
| hyprland | idle-notify inhibit unchanged no-op | Claude Code (Claude Opus 5; session `cee8d980`, 2026-09-17) | Fred: overnight incident triage, ship locally |
| omawrite | in-window close button | Antigravity `agy` (Gemini 3.8 Flash (High); session `41fe8bbb`, 2026-09-10) | Fred: requested the control |
| omawrite | always open the CLI file | Claude Code, 2026-09-11 (`fix(omawrite): verify desktop review documents`) | Fred: `omawrite-review` must be able to prove which file is shown |
| omawrite | stale "File removed" dialog | Claude Code (Claude Opus 5; 2026-09-11, config commit `d5c9187`) | Fred: agents rewrite open files; Reload must work |
| omawrite | shortcuts dialog binding loop | Claude Code (Claude Opus 5; fork commit `fab54d3`, 2026-09-17; PR omacom/omawrite#72) | — |
| omawrite | editor width 65 → 80 columns | Antigravity `agy` (Gemini 3.8 Flash (High); session `97c52d40`, 2026-09-17) | Fred: 65 columns wrapped standard text on wide displays |

Session ids are transcript identifiers in the workstation's local session
stores (Claude: `~/.claude/projects/-home-fred/<id>.jsonl`; Antigravity:
`~/.gemini/antigravity-cli/brain/<id>/`), listed so the provenance can be
audited, not reconstructed.

## 2026-09-22 repository rename

Codex CLI `0.155.1` (`gpt-6-sol`) updated canonical GitHub links for `ecosystem-fred-tamlinux`. [Session record](docs/ai/2026-09-22-github-repository-rename.md).
