<!-- SEED für `CONTRIBUTING.md` des Repos `awesome-ai-coding-sandboxes`. -->

# Contributing

Thanks for helping keep this list accurate and useful. The whole point of this list is that **every claim is sourced and every PR is actually reviewed** — unlike the abandoned lists it improves on. Please help us keep that bar.

## What qualifies

A project belongs here if it:

1. **Executes agent-generated or agent-driven code** — not just an agent framework with no execution boundary.
2. **Provides real isolation** (microVM, gVisor/user-space kernel, container, or process/namespace) as a security boundary.
3. **Is publicly usable and documented** — open source, or a commercial product with real docs.

We do **not** list: dead/unmaintained projects, marketing pages with no substance, or agent frameworks without a sandbox. **License is not a criterion** — permissive and copyleft (incl. AGPL) projects are both welcome.

## The one rule that matters: source every claim

This list lives or dies on accuracy. So:

- **Every comparison-matrix cell needs a source link** to the project's **official docs or repo** (not a blog post, not a vendor comparison, not this list).
- **If you don't know a value, use `?`. Never guess.** `?` is honest and expected; a wrong confident value is not.
- Quote the supporting phrase in your PR description so a reviewer can verify without re-researching.

## How to add or update a project

1. **One project per PR.** Small, verifiable PRs get merged faster.
2. Add the project to the **matching isolation-layer section** (the bulleted link list) as:
   `[Name](official-url) — one factual sentence.`
3. Add a row to the **[Comparison matrix](README.md#comparison-matrix)** using the column values below.
4. Keep it factual and neutral. No superlatives, no marketing copy.

### Comparison-matrix column values

- **Isolation** — the boundary + tier: `Firecracker µVM`, `libkrun µVM`, `Cloud Hypervisor µVM`, `gVisor`, `container`, `process`, etc. (microVM > gVisor > container > process).
- **Egress control** — can outbound network be restricted? One of:
  `deny-default` · `allowlist` · `configurable` · `full-by-default` · `none`.
  This is **not** "does it have network" (almost all do). It's whether outbound can be locked down.
- **Secrets** — `brokered` (credentials kept **out** of the sandbox via proxy/injection-at-edge) or `env-in` (passed in as env vars/files).
- **Self-host / Managed** — `Self-host`, `Managed`, or both.
- **Persistence** — `ephemeral`, `persistent`, `both`, or `partial`.
- **License** — SPDX id (e.g. `Apache-2.0`, `MIT`, `AGPL-3.0`) or `Proprietary`. Note if only the SDK/client is open (`Proprietary (SDK MIT)`).

## Reporting stale or wrong data

Found an entry that's out of date or incorrect? **Open an issue or a PR.** Accuracy beats politeness — if a value has changed or was wrong, we want to fix it.

## Review & merge

We review and merge **as time allows** — there's no fixed schedule and no bot auto-closing your PR. Well-sourced, one-project PRs are easiest to merge quickly. If something sits too long, a friendly ping on the PR is welcome.

## Scope notes

- **Adjacent** section is for things that share the substrate but aren't untrusted-code agent sandboxes (e.g. CI-runner orchestrators, CDEs). If unsure whether a project is "core" or "adjacent," propose it and we'll discuss in the PR.
- Building blocks (Firecracker, gVisor, Kata, libkrun, …) go in **Isolation building blocks**, not the main lists.

## License of contributions

By contributing, you agree your additions are released under the list's content license (**[CC0-1.0 / CC-BY-4.0 — TBD]**).
