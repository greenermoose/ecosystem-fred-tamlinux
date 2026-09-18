# The ecosystem: what runs patched, and what depends on it

Generated table from [`ecosystem.json`](ecosystem.json) (`omarchy-fred-ecosystem render`);
the prose around it is hand-written. One row per third-party package. "Local
version" is the Arch version with the `pkgrel` suffix that makes the patch
outrank Arch's build of the same release and lose to any newer one.

<!-- registry:begin -->
| Package | Status | Local version | Fork (compare view) | Patches | Filed upstream | Retires when | Depended on by |
|---|---|---|---|---|---|---|---|
| [gtk4](packages/gtk4/README.md) | active | `1:4.22.4-1.1` | none (upstream has it) | 1 | — | Arch ships gtk4 >= 4.22.5 (but not 4.23.0-4.23.2) or >= 4.23.3; the pacman hook does the comparison | omarchy-fred-config |
| [aquamarine](packages/aquamarine/README.md) | active | `0.15.0-2.1` | [v0.15.0-fred.1](https://github.com/hyprwm/aquamarine/compare/v0.15.0...greenermoose:aquamarine:v0.15.0-fred.1) | 1 | [hyprwm/aquamarine/pull/395](https://github.com/hyprwm/aquamarine/pull/395) | an Arch aquamarine release whose SDRMConnector::disconnect() disables KMS before the teardown (watch hyprwm/aquamarine#386); version unknown until it lands | omarchy-fred-config, fred.monitor (planned) |
| [hyprland](packages/hyprland/README.md) | active | `0.56.2-3.3` | [v0.56.2-fred.3](https://github.com/hyprwm/Hyprland/compare/v0.56.2...greenermoose:Hyprland:v0.56.2-fred.3) | 3 | [hyprwm/Hyprland/pull/16290](https://github.com/hyprwm/Hyprland/pull/16290) | an Arch hyprland release containing all three fixes (onConnect() honours the compositor DPMS state; setInhibit() guards the unchanged case; a filtered `dpms off` no longer marks the compositor DPMS-off). If only some land, drop those patches and rebuild as <arch>.1 | omarchy-fred-config, omarchy-fred-workspaces, fred.monitor (planned) |
| [omawrite](packages/omawrite/README.md) | active | `0.5.0-1.5` | [v0.5.0-fred.5](https://github.com/omacom/omawrite/compare/v0.5.0...greenermoose:omawrite:v0.5.0-fred.5) | 5 | [omacom/omawrite/issues/73](https://github.com/omacom/omawrite/issues/73), [omacom/omawrite/pull/72](https://github.com/omacom/omawrite/pull/72) | Arch ships omawrite >= 0.5.1 with a native close button, reliable CLI opening, a working Reload in the 'File removed' dialog, a loop-free shortcuts dialog and >= 80-column width; otherwise rebase the stack onto the new release | omarchy-fred-config (omawrite-review, skill omawrite-review) |
<!-- registry:end -->

## Reading a row

- **Fork (compare view)** opens GitHub's diff of the fork tag against the
  upstream release it patches — the patches in context. The fork's default
  branch `fred` always points at the current patch set; `patch/<slug>` holds
  each patch alone and `patchset/<tag>` the integration branch.
- **Filed upstream** is where a project's rules allowed posting. Where they
  do not (hyprwm/\*), nothing is filed and the fork is the only public copy —
  see the policy in the [README](README.md#why-this-exists-instead-of-upstream-pull-requests).
- **Depended on by** names Fred's own repositories that need the patch to
  behave as documented; each carries an `ECOSYSTEM.md` at its root that says
  what breaks without it.

## Consumers

| Repository | Needs | Because |
|---|---|---|
| [omarchy-fred-config](https://github.com/greenermoose/omarchy-fred-config) (private) | all four | the workstation itself; `omawrite-review` (how agents show Fred their plans) hard-depends on the omawrite patches |
| [omarchy-fred-workspaces](https://github.com/greenermoose/omarchy-fred-workspaces) | hyprland | its per-monitor idle blanking depends on per-output DPMS isolation (patch 3); its hotplug `reconcile` focuses windows, which on stock Hyprland resets the idle clock (patch 2); and a reconnecting monitor stays dark (patch 1) |
| fred.monitor (planned) | aquamarine, hyprland | per-display reset/retrain assumes a KMS teardown that does not wedge on resume (Fault D) and DPMS-aware reconnects |

## Retired

Nothing yet. Retired entries move to [`retired/`](retired/) with their last
recipe and README so the history stays readable; the fork tag stays in place.
