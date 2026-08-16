# Awesome AI Coding Sandboxes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of sandboxing and isolation solutions for running the code of autonomous **AI coding agents** (Claude Code, Codex, OpenHands, and friends) — organized **by security posture first**: how strong the isolation boundary is, and what the agent can still reach beyond it.

AI coding agents run arbitrary, model-generated commands. The hard part isn't speed — it's the **security boundary** (isolation) and what the agent can still do through it (**network egress, secrets**), plus **durable workspace state** for long tasks. This list ranks on those, not boot-time benchmarks.

<!-- Keep this date in sync with last_modified_at in _config.yml — it drives
     <lastmod> in sitemap.xml and dateModified in the JSON-LD graph. -->
_Last updated: 2026-08-09 · Actively maintained — PRs welcome._

## Contents

- [Comparison matrix](#comparison-matrix)
- [What the data shows](#what-the-data-shows)
- [Why security-posture-first](#why-security-posture-first)
- [VMs & microVMs](#vms--microvms)
- [Containers & gVisor](#containers--gvisor)
- [Process & namespace sandboxes](#process--namespace-sandboxes)
- [Filesystem & WebAssembly sandboxes](#filesystem--webassembly-sandboxes)
- [Isolation building blocks](#isolation-building-blocks)
- [Adjacent](#adjacent)

## Comparison matrix

**Isolation tier:** microVM (own kernel) > gVisor (user-space kernel) > container (shared kernel) > process.
**Egress control** = can outbound network be restricted — NOT whether it _has_ network. `deny-default` / `allowlist` / `configurable` / `full-by-default` / `none`.
**Secrets** = `brokered` (creds kept OUT via proxy) vs `env-in` (injected). Sorted by isolation tier, then egress strength.
**Abbrev.:** eph = ephemeral · pers = persistent · Prop. = proprietary.

| Project                                                                      | Isolation                             | Egress control                | Secrets    | Self-host / Managed     | State        | License    |
| ---------------------------------------------------------------------------- | ------------------------------------- | ----------------------------- | ---------- | ----------------------- | ------------ | ---------- |
| [Cleanroom](https://github.com/buildkite/cleanroom)                          | Firecracker µVM                       | **deny-default**              | brokered   | Self-host               | eph          | MIT        |
| [smolvm (smol-machines)](https://github.com/smol-machines/smolvm)            | libkrun µVM                           | **deny-default**              | brokered   | Self-host               | both         | Apache     |
| [Leap0](https://leap0.dev)                                                   | Firecracker µVM                       | **deny-default** (allowlist)  | brokered   | Both                    | both         | Prop.      |
| [InstaVM](https://instavm.io)                                                | Firecracker µVM                       | **deny-default** (allowlist)  | brokered   | Both                    | both         | Prop.      |
| [Mitos](https://github.com/mitos-run/mitos)                                  | Firecracker µVM (Kubernetes)          | **deny-default**              | brokered   | Both                    | pers         | Apache     |
| [Sprites (Fly.io)](https://fly.io/sprites)                                   | Firecracker µVM                       | allowlist                     | env-in     | Managed                 | pers         | Prop.      |
| [microsandbox](https://github.com/superradcompany/microsandbox)              | libkrun µVM                           | configurable (deny opt.)      | brokered   | Self-host (+cloud beta) | pers         | Apache     |
| [Superserve](https://superserve.ai)                                          | Firecracker µVM                       | configurable (allowlist)      | brokered   | Both                    | both         | Apache     |
| [Islo](https://islo.dev)                                                     | Cloud Hypervisor µVM                  | configurable (allow/deny)     | brokered   | Both (BYOC)             | both         | Prop.      |
| [Declaw](https://declaw.ai)                                                  | Firecracker µVM                       | configurable (allow/deny, L7) | brokered   | Both (BYOC)             | both         | Prop.      |
| [OmniRun](https://omnirun.io)                                                | Firecracker µVM                       | configurable (allow/deny)     | env-in     | Both                    | eph          | Prop.      |
| [Vercel Sandbox](https://github.com/vercel/sandbox)                          | Firecracker µVM                       | configurable (deny-all)       | brokered   | Managed                 | eph          | Prop.      |
| [BoxLite](https://github.com/boxlite-ai/boxlite)                             | KVM/HVF µVM                           | configurable (allowlist)      | brokered   | Self-host               | pers         | Apache     |
| [OpenComputer](https://opencomputer.dev)                                     | KVM full VM                           | configurable (allowlist, L7)  | brokered   | Both                    | pers         | Apache     |
| [Blaxel](https://blaxel.ai)                                                  | µVM                                   | configurable (preview)        | brokered   | Managed                 | pers         | Prop.      |
| [Qbox](https://qbox.sh)                                                      | Firecracker µVM                       | configurable                  | env-in     | Self-host               | eph          | unverified |
| [Katakate (k7)](https://github.com/Katakate/k7)                              | Kata+FC µVM (K3s)                     | configurable (allowlist)      | env-in     | Self-host               | eph          | Apache     |
| [AgentENV](https://github.com/kvcache-ai/AgentENV)[^agentenv]                | Firecracker µVM                       | full-by-default (cfg)         | env-in     | Self-host               | both         | MIT        |
| [Freestyle](https://freestyle.sh)                                            | Full VM/KVM                           | configurable (on/off)         | unverified | Managed                 | both         | Prop.      |
| [Runloop](https://runloop.ai)                                                | VM + container                        | full-by-default (cfg)         | brokered   | Managed                 | pers         | Prop.      |
| [E2B](https://e2b.dev)                                                       | Firecracker µVM                       | full-by-default (cfg)         | env-in     | Both                    | eph[^resume] | Apache     |
| [Northflank](https://northflank.com)                                         | Kata+FC µVM                           | full-by-default               | env-in     | Both (BYOC)             | pers         | Prop.      |
| [Arrakis](https://github.com/abshkbh/arrakis)                                | Cloud Hypervisor µVM                  | full-by-default               | env-in     | Self-host               | pers         | AGPL       |
| [SmolVM (Celesto AI)](https://github.com/CelestoAI/SmolVM)                   | Firecracker+QEMU µVM                  | full-by-default (allowlist)   | env-in     | Self-host               | both         | Apache     |
| [Morph](https://morph.so)                                                    | µVM (VMM n/s)                         | full-by-default               | env-in     | Both                    | both         | Prop.      |
| [Tensorlake](https://tensorlake.ai)                                          | Firecracker+CH µVM                    | full-by-default (allow/deny)  | env-in     | Both (BYOC)             | both         | Prop.      |
| [Box (ascii.dev)](https://box.ascii.dev)                                     | Linux VM                              | full-by-default               | env-in     | Managed                 | pers         | Prop.      |
| [Novita](https://novita.ai/sandbox)                                          | Firecracker µVM                       | full-by-default               | env-in     | Managed                 | both         | Prop.      |
| [Baponi](https://baponi.ai)                                                  | Container (seccomp+cgroups, zero-cap) | **deny-default**              | brokered   | Both                    | both         | Prop.      |
| [OpenSandbox](https://github.com/alibaba/OpenSandbox)                        | Container (opt. gVisor/Kata/FC)       | configurable (deny avail.)    | brokered   | Self-host               | eph          | Apache     |
| [Cloudflare Sandboxes](https://developers.cloudflare.com/sandbox/)           | VM-backed container                   | configurable (deny avail.)    | brokered   | Managed                 | both         | Prop.      |
| [Daytona](https://daytona.io)                                                | Container (ded. kernel)               | configurable (tier-gated)     | brokered   | Both                    | pers         | AGPL       |
| [AIO Sandbox](https://github.com/agent-infra/sandbox)                        | Container (Docker)                    | configurable (proxy)          | env-in     | Self-host               | eph          | Apache     |
| [Modal](https://modal.com)                                                   | gVisor                                | full-by-default (cfg)         | env-in     | Managed                 | eph          | Prop.      |
| [Beam](https://beam.cloud)                                                   | gVisor + runc                         | full-by-default (cfg)         | env-in     | Both                    | pers         | AGPL       |
| [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | gVisor/Kata (pluggable)               | none (delegated)              | env-in     | Self-host (Kubernetes)  | pers         | Apache     |
| [OpenHands](https://github.com/OpenHands/OpenHands)                          | Container (Docker)                    | none                          | env-in     | Both                    | both         | MIT        |

## What the data shows

**Restricted-by-default egress is the minority.** Deny-by-default: **Cleanroom, smolvm (smol-machines), Leap0, InstaVM, Mitos, Baponi**; allowlist-default: **Sprites**. Sixteen offer _configurable_ egress (opt-in), and the rest ship open outbound or delegate/none (Modal, Beam, Northflank, Arrakis, Box, Morph, Tensorlake, Novita, Kubernetes Agent Sandbox, OpenHands). _Isolation is common; egress control is not._

**Secrets brokering (creds kept out of the sandbox)** is now a real cluster: Cleanroom, smolvm, Leap0, InstaVM, Mitos, Superserve, Islo, Declaw, Vercel Sandbox, BoxLite, OpenComputer, Blaxel, microsandbox, Runloop, Baponi, OpenSandbox, Cloudflare, Daytona. Env-in: AgentENV, E2B, Modal, Northflank, Beam, Arrakis, SmolVM (Celesto), Qbox, Katakate, Sprites, Morph, Tensorlake, Box, Novita, AIO Sandbox, Kubernetes Agent Sandbox, OpenHands, OmniRun.

**The strong-posture set** (µVM/VM **and** restricted egress **and** brokered secrets) is small: **Cleanroom, smolvm (smol-machines), Leap0, InstaVM, Mitos** — plus Superserve/Islo/Declaw/OpenComputer on configurable egress. That's the bar to beat.

**EU data-residency** is offered by two _managed_ entries — **Box (ascii.dev)** (DE/FI/FR) and **OmniRun** (Hetzner/DE). Self-hostable tools (Mitos, Cleanroom, microsandbox, smolvm, …) can additionally be run in the EU _by you_. Still a minority across 37 providers.

**Control-plane reachable from inside** (the "front desk" risk): Sprites documents an in-sandbox management API (reachable); Modal documents it is _not_. Others undocumented.

**Control-plane authentication:** AgentENV currently has no built-in API authorization. Its maintainers explicitly require deployment on a trusted network or behind an authorization proxy.

### How these values were verified

Every cell traces back to the project's own documentation or source repository — not to blog posts, not to vendor comparisons, not to an earlier revision of this list. Where a project documents nothing, the cell says `?` rather than a guess: an honest gap is more useful than a confident error. Contributors quote the supporting phrase in the pull request so a reviewer can check the claim without repeating the research, and the matrix is the single source for [`_data/sandboxes.json`](https://github.com/fhiltscher/awesome-ai-coding-sandboxes/blob/main/_data/sandboxes.json), which CI regenerates and diffs on every change — the structured data this page publishes cannot silently drift from the table above.

### What this ranking does not measure

It reads documentation, not implementations. A **deny-default** cell means the project _documents_ deny-by-default egress; it is not the result of a penetration test, and no escape research was done for this list. Cold-start latency, throughput, pricing, SDK ergonomics and language coverage are deliberately absent — they are covered well elsewhere, and they are not what fails when an agent gets prompt-injected.

A strong row also does not equal a safe deployment. Brokered secrets still require the broker to be configured; an allowlist is only as tight as its entries; a µVM with a mounted host directory has traded its boundary away. Read the matrix as a shortlist filter, then read the docs of the two or three candidates that survive it.

## Why security-posture-first

Community consensus (HN, Reddit, the security literature) is blunt: **containers are not a trust boundary** for untrusted agent code, and **isolation alone "solves the easiest problem"** — the real risk is an agent with legitimate access exfiltrating data via network egress or leaked credentials (prompt injection). So we rank on the boundary _and_ what crosses it, not on cold-start milliseconds (which matter only for ephemeral/high-concurrency workloads, not long-running coding agents).

Key nuance: almost every sandbox _has_ outbound network — that's the problem, not a feature. The differentiator is whether egress can be **default-denied and allowlisted**, and whether **secrets are brokered so the sandbox never holds them**. A strong microVM with unrestricted network still lets a prompt-injected agent phone home with your code — isolation and egress control are **orthogonal**.

## VMs & microVMs

Strongest isolation (own kernel per sandbox), built on Firecracker, libkrun, and Cloud Hypervisor. The verified µVM entries are in the comparison matrix above; the list below adds open-source projects not (yet) in the matrix.

- [Vibe](https://github.com/lynaghk/vibe)
- [Volant](https://github.com/0xchasercat/volant)
- [Netclode](https://github.com/angristan/netclode)
- [Chamber](https://github.com/cirruslabs/chamber)
- [Matchlock](https://github.com/jingkaihe/matchlock)
- [Gondolin](https://github.com/earendil-works/gondolin)

## Containers & gVisor

Shared-kernel isolation; faster, weaker boundary — built on gVisor and Kata Containers. Verified entries are in the matrix above; additional projects:

- [llm-sandbox](https://github.com/vndee/llm-sandbox) - Python library that runs LLM-generated code on Docker, Podman or Kubernetes backends.
- [MCP Runner](https://github.com/abir-taheer/mcp-runner) - Runs dockerized MCP servers as ephemeral, multi-tenant deployments on the gVisor runtime.
- [Kilntainers](https://github.com/Kiln-AI/Kilntainers) - MCP server that gives every agent an ephemeral Linux container for shell commands.
- [packnplay](https://github.com/obra/packnplay) - Launches Claude Code, Codex or Gemini in per-worktree Docker containers; no introspection or access control.
- [yolobox](https://github.com/finbarr/yolobox) - Container wrapper that grants the agent full sudo inside while keeping the host home directory out of reach.
- [vibebin](https://github.com/jgbrwn/vibebin) - Self-hosted Incus/LXC platform for persistent agent sandboxes, with Caddy and direct SSH routing.
- [Leash](https://github.com/strongdm/leash) - Wraps agents in containers and enforces Cedar policies on their activity; experimental container-free mode on macOS.
- [clampdown](https://github.com/89luca89/clampdown) - Hardened container sandbox with an egress-filtering sidecar and an auth proxy that keeps API keys out of the agent container.
- [code-on-incus](https://github.com/mensfeld/code-on-incus) - Gives each agent its own Incus system container with root, systemd and Docker inside.
- [clawker](https://github.com/schmitthub/clawker) - Self-hosted Docker sandboxes for coding agents, running behind an egress filter.

## Process & namespace sandboxes

Syscall/filesystem/network restriction for individual processes, built on Bubblewrap, Landlock, and seccomp.

- [Anthropic Sandbox Runtime](https://github.com/anthropic-experimental/sandbox-runtime) - Filesystem and network restrictions for arbitrary processes via Seatbelt on macOS and bubblewrap on Linux, plus proxy-based domain allowlisting.
- [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) - Agent runtime that enforces declarative YAML policies on file access, exfiltration and network activity (alpha).
- [Greywall](https://github.com/GreyhavenHQ/greywall) - Container-free, deny-by-default sandbox for filesystem, network and syscalls on Linux and macOS, with an allow-by-default watch mode.
- [Fence](https://github.com/fencesandbox/fence) - Lightweight, container-free sandbox that runs commands under network and filesystem restrictions.
- [Landrun](https://github.com/Zouuup/landrun) - Runs any Linux process in an unprivileged Landlock sandbox, firejail-style but kernel-native.
- [sandlock](https://github.com/multikernel/sandlock) - Confines untrusted code with Landlock, seccomp-bpf and seccomp user notification; no root, no cgroups, copy-on-write working directory.
- [HiveBox](https://github.com/TetiAI/hivebox) - Namespaces, cgroups, seccomp and Landlock behind a CLI and REST API, one OpenCode agent per sandbox.
- [ClaudeCage](https://github.com/PACHAKUTlQ/ClaudeCage) - Packs Claude Code into a single portable bubblewrap sandbox scoped to one project directory.

## Filesystem & WebAssembly sandboxes

- [AgentFS](https://docs.turso.tech/agentfs) - Copy-on-write filesystem for agents stored in a single SQLite database; the CLI wraps an existing program in a sandboxed session.
- [LocalSandbox](https://github.com/coplane/localsandbox) - Python SDK combining just-bash, AgentFS and Pyodide into a persistent WebAssembly-backed bash/python environment (beta, unaudited).
- [Wassette](https://github.com/microsoft/wassette) - Security-oriented runtime that serves WebAssembly Components as MCP tools.
- [Eryx](https://github.com/eryx-org/eryx) - Runs untrusted CPython on Wasmtime with memory and CPU limits and no filesystem or network access by default.
- [Capsule](https://github.com/capsulerun/capsule) - Runtime that executes agent tasks as untrusted code in isolated WebAssembly environments.
- [AgentVM](https://github.com/deepclause/agentvm) - Node.js library running an Alpine Linux VM compiled to WebAssembly (container2wasm) in a worker thread.
- [amla-sandbox](https://github.com/amlalabs/amla-sandbox) - WebAssembly sandbox for agent code with capability enforcement, a virtual filesystem and no network.

## Isolation building blocks

| Project                                                                  | Type                                    | License    |
| ------------------------------------------------------------------------ | --------------------------------------- | ---------- |
| [Firecracker](https://github.com/firecracker-microvm/firecracker)        | microVM (KVM)                           | Apache-2.0 |
| [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) | microVM (KVM)                           | Apache-2.0 |
| [Kata Containers](https://github.com/kata-containers/kata-containers)    | microVM (OCI/CRI)                       | Apache-2.0 |
| [gVisor](https://github.com/google/gvisor)                               | user-space kernel                       | Apache-2.0 |
| [libkrun](https://github.com/containers/libkrun)                         | microVM library                         | Apache-2.0 |
| [Flintlock](https://github.com/liquidmetal-dev/flintlock)                | microVM lifecycle mgmt                  | MPL-2.0    |
| [forkd](https://github.com/deeplethe/forkd)                              | fork-from-warm µVM engine (Firecracker) | Apache-2.0 |
| [Bubblewrap](https://github.com/containers/bubblewrap)                   | process sandbox                         | LGPL-2.0   |

## Adjacent

Related but not untrusted-code sandboxes for coding agents:

- [Ona](https://ona.com) - Formerly Gitpod; container-based CDE + agent orchestration. **Acquired by OpenAI (announced June 2026, deal pending); folding into Codex.**
- [Coder](https://coder.com) - Self-hosted CDE; isolation delegated to the provisioned backend. AGPL-3.0 (+ enterprise).
- [CodeSandbox SDK](https://codesandbox.io) - microVM CDE (now part of Together AI); primarily a dev environment.
- [GitHub Codespaces](https://github.com/features/codespaces) - Cloud dev environments; see also [Replit](https://replit.com).
- [Steel.dev](https://steel.dev) - Sandboxed browser sessions (not general code exec).
- [Clusy](https://www.clusy.io) - Agent-native notebook for ML/data science; managed-only, runs agent-written cells on cloud CPU/GPU "managed cloud sandboxes". Isolation mechanism, tenant boundary and egress controls undocumented; workspace separation stated as logical only.
- [ComputeSDK](https://computesdk.com) - Provider-agnostic router/SDK across sandbox backends (no own isolation); see also [VibeKit](https://docs.vibekit.sh).
- [agentbox (madarco)](https://github.com/madarco/agentbox) - Self-hosted CLI running coding agents in parallel (Docker+FUSE / cloud VM); dev-workflow tooling on off-the-shelf isolation. MIT.
- [Giant Swarm Agent Platform](https://www.giantswarm.io/agent-platform) - Kubernetes-based agent governance/orchestration control plane (MCP); ships no dedicated untrusted-code sandbox.
- [Fireactions](https://github.com/hostinger/fireactions) - GitHub-Actions runner orchestrator on Firecracker µVMs; no agent/sandbox API. Apache-2.0.

## Contributing

PRs welcome — **and actually reviewed** (as time allows; no bot auto-closing your PR). See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [Code of Conduct](code-of-conduct.md). Maintained by [@fhiltscher](https://github.com/fhiltscher) ([LinkedIn](https://www.linkedin.com/in/franz-hiltscher/)).

- One project per PR. Every matrix cell needs a **source link** (official docs/repo). Don't know a value? Use `?` — never guess.
- Entries must run agent-generated code with a real isolation boundary; no dead projects, no marketing-only pages. License is not a criterion.
- Spotted stale or wrong data? Open an issue or PR — accuracy is the whole point.

Released under [CC0-1.0](LICENSE) — public domain.

[^resume]: E2B is ephemeral but supports pause/resume.
[^agentenv]: AgentENV sources: [architecture](https://kvcache-ai.github.io/AgentENV/latest/internals/architecture.html), [networking and persistence](https://kvcache-ai.github.io/AgentENV/latest/concepts/sandboxes.html), [environment injection](https://kvcache-ai.github.io/AgentENV/latest/concepts/templates.html), and [license](https://github.com/kvcache-ai/AgentENV/blob/main/LICENSE).
