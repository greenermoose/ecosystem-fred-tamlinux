# AI Collaboration Session Archive: `ecosystem-fred-tamlinux`

Prompt history, tools, models and key decisions for this repository. Patches
themselves were authored in earlier sessions recorded in the private
workstation config and summarised in `AI_PROVENANCE.md` §3.

---

## Session: 2026-09-17 — Public forks + registry design and first release (v0.1.0)

- **CLI Tool**: `claude` `2.1.274` (Claude Code)
- **Model**: Claude Opus 5 (`claude-opus-5`)
- **Transcript**: Retained privately by the author.
- **Participants**: Fred (@greenermoose), Claude Code

### Guiding Prompt
> **Fred:**
> "We provided PRs for some packages we had to patch to fix bugs on this system. See these replies from those package maintainers. Create a plan for how we will keep our own fork and note the patches required for our system to work well. I'm thinking we will maintain a public fork of third-party packages that we depend on. Our patches will be in those forks so people can see our patches in context. In the repos of our own software that requires patched versions of third-party software we will keep track of that. I'm thinking of something like an ecosystem folder or the like. Ponder this problem and propose a plan. Also, remember that PRs submitted to upstream packages are being phased out due to the volumne of pull requests that AIs are producing. If helpful, do some web research so you understand why open source projects are not starting not to accept PRs from the public any more."
>
> (followed by the hyprwm bot's closure notice for Hyprland#16290: "Hyprland and hypr* no longer accept contributions from unvouched contributors.")

> **Fred (on naming):**
> "Does ecosystem- as a command name conflict with any other public projects? Perhaps omafred- could be a standard prefix we could for utilities we write to avoid name conflicts. If we do that, our commands would be omafred-ecosystem-export and omafred-ecosystem-verify. Or how about omafred-ecosystem as the command, and export and verify are flags or modes we pass to it? Does it make sense to have just one ecosystem command with many flags and modes, or a bunch of them, each specialized for one type of task?"

### Key Decisions & Implementation Notes
- Research: PR queues are closing sector-wide (GitHub collaborator-only PR
  controls 2026-08-27; arXiv 2609.12236 "stewardship" model); hyprwm gates on
  a hand-written vouch and its AI policy bans AI-written PR text. Decision:
  fork + registry is the primary sharing mechanism; no hyprwm vouch request;
  agents never post on hyprwm/*.
- Three tiers, one source of truth each: fork branches (code), this registry
  (recipes + index), `ECOSYSTEM.md` in consuming repos.
- Builds stay tarball + patches (Hyprland's plugin-ABI hash must not change).
- Fred chose: new repo (not a section of `omarchy-fred-plugin`); `~/pkgs`
  stays the build scratch and `omarchy-fred-sync` publishes a second copy here;
  `ECOSYSTEM.md` file (not folder) in consumers; keep the `omarchy-fred-`
  prefix; one command with subcommands.
- Name check: `ecosystem` unused in Arch/AUR/PyPI (one unrelated npm package);
  `omafred` unused anywhere — rejected to avoid a second namespace.

### Verification
- See the plan's verification list: `omarchy-fred-ecosystem verify` clean;
  `makepkg -o` tree identical before/after patch re-export; sync mirrors both
  destinations byte-identically; fork landing pages show the `fred` branch.

## Session: 2026-09-22 — Aquamarine shutdown crash fix (0.15.0-2.2)

- **Tool**: Codex API (CLI version not applicable)
- **Model**: GPT-6
- **Transcript reference**: This API conversation; no local Codex CLI rollout ID was available
- **Participants**: Fred, Codex
- **Fork patchset commit**: `1cda9c3` (cherry-picked from `704dbe9`)

### Guiding prompts

> **Fred:** "Can you trace the aquamarine function and see if you can find the source of the segfault? Any bug reports or PRs online that might be applicable?"

> **Fred:** "Can we fix the Aquamarine bug on this system?"

### Decision and verification

- The 2026-09-22 Hyprland core showed a null connector at
  `CDRMBackend::flushAsyncCommitEvents()` in Aquamarine 0.15.0. Upstream
  [issue #383](https://github.com/hyprwm/aquamarine/issues/383) independently
  reports the exact stack and proposed one-line guard.
- Added that guard as a second fork patch, retaining the existing KMS
  disconnect fix from PR #395. Exported both patches into the Arch package
  recipe and built `aquamarine` and `aquamarine-debug` 0.15.0-2.2 with `makepkg`.
- The installed library's disassembly skips null connector entries before
  dereferencing them; the KMS disable string remains. The pacman hook reports
  `patched`, and `omarchy-fred-ecosystem verify aquamarine` passes.
- A live Hyprland shutdown has not been used as a test; the new library is
  loaded when a new graphical session starts.

## Session: 2026-09-22 — Rename the registry CLI to tam-ecosystem

- **CLI Tool**: Cursor `3.21.16`
- **Model**: `composer`
- **Commit**: `30bb5a6`
- **Transcript**: Retained privately by the author.

Daily command is `tam-ecosystem`; long alias is `ecosystem-fred-tamlinux`.
No leftover `omarchy-fred-ecosystem` command after the Home Manager switch.

## Session: 2026-09-21 — Omarchy bar tooltip fractional scaling fixes (4.0.4-1.3)

- **CLI Tool**: Cursor `3.21.16`
- **Model**: `composer`
- **Commits**: `a98764c`, `270d3e6`, `32f25b1`
- **Transcript**: Retained privately by the author.
- **Participants**: Fred, Cursor (Composer)

### Decisions and implementation
- Shared bar tooltip in Omarchy's `Bar.qml` clipped bottom border and chrome on
  fractional scales (Dell S2725DSM at 1.25×).
- Created a 3-patch stack on fork tag `v4.0.4-fred.2`:
  1. `omarchy-bar-tooltip-border-padding.patch` (`afe057b0`): reserves border padding like `PanelToolTip`.
  2. `omarchy-bar-tooltip-scale-safe-size.patch` (`dd0ad03c`): adds `scaleSafeSize` helper ensuring integer physical pixels.
  3. `omarchy-bar-tooltip-scale-safe-bubble.patch` (`6edc29cc`): applies scale-safe sizing to the `BorderSurface` bubble itself.
- Registered package `omarchy 4.0.4-1.3` and documented verification in `HANDOFF-bar-tooltip-dell-1.25x.md`.

## 2026-09-23 upstream survey foundation

- [Codex session record](2026-09-23-upstream-survey-foundation.md).

## 2026-09-28 private session IDs

- [Claude Code session record](2026-09-28-private-session-ids.md).

## Session: 2026-10-04 — Upstream rebases, GTK4 retirement, and pacman precedence correction

- **CLI Tool**: `claude` `2.1.289` (Claude Code)
- **Model**: Claude Opus 5.5 (`claude-opus-5-5`)
- **Commit**: `a9456d4`
- **Transcript**: Retained privately by the author.
- **Participants**: Fred, Claude Code

### Decisions and implementation
- Rebased aquamarine onto Arch `0.15.1-1` (local `0.15.1-1.1`, tag `v0.15.1-fred.1`).
  Retired the KMS-disable patch (#395) because upstream merged the identical fix
  as #410; retained the null-connector guard (#383) as `flushAsyncCommitEvents()`
  remains unguarded in v0.15.1.
- Rebuilt hyprland as `0.56.2-4.1` against Arch's `0.56.2-4` (pkgrel rebuild
  against aquamarine 0.15.1). Patchset and fork tag `v0.56.2-fred.3` unchanged.
- Retired gtk4: Arch shipped `1:4.22.5-1` containing MR !10166. Moved recipe to
  `retired/gtk4`.
- Corrected the pacman repository precedence rule in `README.md` and
  `ECOSYSTEM.md`: pacman selects the package from the first configured
  repository regardless of version numbers, so local builds stay pinned until
  rebased or retired.

## Session: 2026-10-04 — Omawrite check script alignment with micro-review

- **CLI Tool**: `claude` `2.1.289` (Claude Code)
- **Model**: Claude Opus 5.5 (`claude-opus-5-5`)
- **Commit**: `b3d21e7`
- **Transcript**: Retained privately by the author.
- **Participants**: Fred, Claude Code

### Decisions and implementation
- Updated `packages/omawrite/omawrite-local-patch-check` to note that the
  workstation review workflow now uses `micro-review` and no longer depends on
  Omawrite patches.

## Session: 2026-10-04 — System status documentation audit and synchronization

- **CLI Tool**: `agy` `1.2.16` (Antigravity)
- **Model**: Gemini 3.8 Flash (High)
- **Transcript**: Retained privately by the author.
- **Participants**: Fred (@greenermoose), Antigravity

### Guiding prompt
> **Fred:**
> "Review all the files in ecosystem-fred-tamlinux and compare against the current status of this system. Update any docs that are out of date, then commit and push your changes. Ask if you have questions."

### Decisions and implementation
- Compared all registry entries and documents against the live system state:
  installed package versions (`aquamarine 0.15.1-1.1`, `hyprland 0.56.2-4.1`,
  `omawrite 0.5.0-1.5`, `omarchy 4.0.4-1.3`, `gtk4 1:4.22.5-1`), pacman hooks,
  `/usr/local/bin/*-check` scripts, and AI toolchain versions.
- Updated `ecosystem.json`: corrected `local_version` convention description to
  match repository precedence rules; updated omawrite summary and dependents
  to reflect the transition to `micro-review`.
- Re-rendered `ECOSYSTEM.md` table and updated hand-written sections: added
  omarchy and its plugin dependents to Consumers; updated `fred.monitor` note;
  listed gtk4 in Retired.
- Updated `UPSTREAM.md`: noted active packages and gtk4 retirement.
- Updated `packages/hyprland/README.md`: aligned patched version to `0.56.2-4.1`
  and rollback target to `0.56.2-4`; updated tag in `upstream-pr.md`.
- Updated `packages/omawrite/README.md`: aligned title, rationale, and verify
  instructions with the micro-review workflow transition.
- Updated `retired/gtk4/README.md`: noted retirement date (2026-10-04) and local
  system file cleanup.
- Updated `AI_PROVENANCE.md`: refreshed toolchain versions as of 2026-10-04;
  added omarchy patches and recorded recent maintenance sessions.

