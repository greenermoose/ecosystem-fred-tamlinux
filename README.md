# ecosystem-fred-tamlinux

The public record of every third-party package Fred's [Tamlinux](https://github.com/greenermoose/tamlinux) workstations
run **patched**, and of the software of his that depends on those patches.

Each entry answers: what is broken upstream, what the fix is, where to read it
in context, how it is built, and when it goes away.

| | |
|---|---|
| Registry | [`ECOSYSTEM.md`](ECOSYSTEM.md) (human) · [`ecosystem.json`](ecosystem.json) (machine) |
| Recipes | [`packages/<pkg>/`](packages/) — Arch `PKGBUILD` + exported patches + the pacman hook that watches for retirement |
| Code, in context | fork branches on `greenermoose/<Upstream>`; every entry links a GitHub *compare* view against the release it patches |
| Tool | [`bin/tam-ecosystem`](bin/tam-ecosystem) — `export`, `verify`, `status`, `retire`, `install` |
| Consumers | Fred's own repos carry an `ECOSYSTEM.md` naming the patches they rely on |

## Why this exists instead of upstream pull requests

Open-source projects are closing their pull-request queues. Writing code got
cheap; reviewing it did not, and maintainers are drowning in machine-generated
submissions — GitHub shipped collaborator-only PR controls in August 2026, and
projects from Ghostty and tldraw to Zig, GIMP and QEMU now refuse outside code
(background: [arXiv 2609.12236](https://arxiv.org/html/2609.12236),
[The Register](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/)).
The Hyprland organisation gates on a hand-written vouch and
[forbids](https://github.com/hyprwm/.github/blob/main/policies/AI_USAGE.md)
AI-written PRs outright.

The patches here are produced by AI coding agents working under Fred's
direction, with the tool, model and prompts recorded
([`AI_PROVENANCE.md`](AI_PROVENANCE.md)). That is honest — and it is exactly
what those projects do not want to review. So the fixes are published the way
that costs nobody a review: a branch on a public fork that anyone, upstream
included, can read in context and take, plus the recipe that turns it into a
package. An upstream merge is welcome; it is not the deliverable.

## How a patch is carried

```
greenermoose/<Upstream>        fred/<slug> topic branches off the shipped release tag,
        │                      fred/<tag> integration branch, tag <tag>-fred.N, default branch `fred`
        │  tam-ecosystem export       (git format-patch)
        ▼
~/pkgs/<pkg>/                  Arch's PKGBUILD with pkgrel <arch>.N + the patches   (build scratch)
        │  tam-sync                   (mirror)
        ▼
packages/<pkg>/                this repo — the recipe, the hook, the notes
```

- **Builds stay tarball + patches.** The fork is for reading and for
  `format-patch`; `makepkg` keeps consuming Arch's source tarball, so things
  like Hyprland's plugin-ABI hash are unchanged.
- **Patches retire themselves.** The rebuilt package carries `pkgrel <arch>.N`,
  which outranks Arch's build of the same version and loses to any newer Arch
  build. A pacman hook (`packages/<pkg>/50-*.hook`) reports whether the newer
  build contains the fix. Nothing is pinned; `IgnorePkg` is never used.
- **No binaries are published.** This repo shares recipes, not packages. Build
  them yourself: see below.

## Building one package

```bash
git clone https://github.com/greenermoose/ecosystem-fred-tamlinux ~/Code/tamlinux/ecosystem-fred-tamlinux
cd ~/Code/tamlinux/ecosystem-fred-tamlinux/packages/<pkg>
makepkg -Cf --noconfirm              # as your user, never root
pkexec pacman -U ./<pkg>-*.pkg.tar.zst
```

`tam-ecosystem install <pkg>` does the same and also publishes into a
local `[local-patches]` pacman repository so upgrades keep the precedence rule
above. The full procedure — building, the local repo, the retirement hook,
rollback — is Fred's `local-package-patching.md` runbook in the private
workstation config (the relevant parts are reproduced in each package's
`README.md`).

## Licence

Scripts and documentation in this repository: GPL-3.0-or-later
([`LICENSE`](LICENSE)). Each `packages/<pkg>/*.patch` is a modification of the
upstream project and is offered under that project's licence (named in the
package's `README.md`: BSD-3-Clause for Hyprland and aquamarine, MIT for
omawrite, LGPL-2.1+ for GTK). `PKGBUILD` files derive from Arch Linux packaging
(0BSD).

## Related

- [`plugin-fred-tamlinux`](https://github.com/greenermoose/plugin-fred-tamlinux)
  — the `fred.*` plugin suite manager and the ecosystem showcase site.
- [`AI_PROVENANCE.md`](AI_PROVENANCE.md) and
  [`docs/ai/sessions.md`](docs/ai/sessions.md) — which tools and models did what.
