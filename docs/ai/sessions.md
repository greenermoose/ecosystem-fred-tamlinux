# AI Collaboration Session Archive: `omarchy-fred-ecosystem`

Prompt history, tools, models and key decisions for this repository. Patches
themselves were authored in earlier sessions recorded in
`omarchy-fred-config` (private) and summarised in `AI_PROVENANCE.md` §3.

---

## Session: 2026-09-17 — Public forks + registry design and first release (v0.1.0)

- **CLI Tool**: `claude` `2.1.274` (Claude Code)
- **Model**: Claude Opus 5 (`claude-opus-5`)
- **Transcript Reference**: `d6c65ea2-7efb-41ed-bae1-86bc3f78d651`
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
- **Transcript Reference**: `68f9fa04-2323-4102-841a-25ab29a68985`

Daily command is `tam-ecosystem`; long alias is `ecosystem-fred-tamlinux`.
No leftover `omarchy-fred-ecosystem` command after the Home Manager switch.

