# Session: 2026-10-13 — Move the guide chapters to `tam`; public-content cleanup (v0.3.0)

- **CLI tool:** Claude Code `2.1.296`
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`)
- **Transcript:** Retained privately by the author.
- **Scope:** `knowledge/` (removed), `bin/tam-ecosystem`, `ecosystem.json`, `ECOSYSTEM.md`, `README.md`, `docs/`, `AI_PROVENANCE.md`, `VERSION`.

## User direction

Fred's guiding prompts, verbatim:

> I think we are building a knowledge corpus for the tam command in two places: 1) the tam repo, and 2) the ecosystem-fred-tamlinux repo. Please look into that and give me your thoughts about what should be done.

> agy was working in the ecosystem repo but it should be done now. If you're able to, please claim the paths and do steps 1, 2 and 3.

> Make sure you don't bleed private ideas and plans into any public repos.

> Remove any private info that agy inadvertently put in a public repo. You don't have to do surgery to remove history, but make sure the latest version of each public repo is clean.

## Decisions and implementation

1. **One corpus, owned by `tam`.** `tam` reads a single knowledge root, so a
   second corpus here could only replace tam's guide, not join it. The
   ecosystem chapters moved into the `tam` repository
   (`knowledge/ecosystem/`), where they are tested, indexed and packaged with
   the command. This repository keeps the registry: `ecosystem.json`,
   `patches/`, `ECOSYSTEM.md`, and the survey documents in `docs/`.
2. **`tam-ecosystem` 0.3.0.** Removed the `index`, `guide` and
   `export-knowledge` subcommands and the duplicate indexer; `render` only
   rewrites the `ECOSYSTEM.md` tables. The References column renders `—` when
   an entry has no public reference.
3. **Public content only.** The 0.2.x expansion cited private planning records
   and described unpublished plans. References to private records were removed,
   text that relied on them was rewritten from public sources (the
   `tamlinux` README and plans, upstream documentation), and an entry about an
   unannounced project was removed. Survey recommendations that were never
   decided (KDE applications, QEMU, Docker) changed from `selected` to
   `evaluated`, and the desktop-suite survey now says its verdicts are
   recommendations.

## Verification

- `bin/tam-ecosystem render` regenerates both tables; `bash -n` passes.
- The current tree was searched for private-record references and the removed
  terms; none remain outside dated provenance records.
