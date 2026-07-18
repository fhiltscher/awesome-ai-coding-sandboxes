# Awesome AI Coding Sandboxes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of sandboxing and isolation solutions for running the code of autonomous **AI coding agents** (Claude Code, Codex, OpenHands, and friends) — organized **security-posture-first**: how strong the isolation boundary is, and what the agent can still reach beyond it.

AI coding agents run arbitrary, model-generated commands. The hard part isn't speed — it's the **security boundary** (isolation) and what the agent can still do through it (**network egress, secrets**), plus **durable workspace state** for long tasks. This list ranks on those, not boot-time benchmarks.

*Last updated: 2026-07-18 · Actively maintained — [PRs welcome](CONTRIBUTING.md).*

## Contents
- [Comparison matrix](#comparison-matrix)
- [Why security-posture-first?](#why-security-posture-first)
- [VMs & microVMs](#vms--microvms)
- [Containers & gVisor](#containers--gvisor)
- [Process & namespace sandboxes](#process--namespace-sandboxes)
- [Filesystem & WASM sandboxes](#filesystem--wasm-sandboxes)
- [Isolation building blocks](#isolation-building-blocks)
- [Adjacent](#adjacent)
- [Related lists](#related-lists)
- [Contributing](#contributing)
- [License](#license)

## Comparison matrix

**Isolation tier:** microVM (own kernel) > gVisor (user-space kernel) > container (shared kernel) > process.
**Egress control** = can outbound network be restricted — NOT whether it *has* network. `deny-default` / `allowlist` / `configurable` / `full-by-default` / `none`.
**Secrets** = `brokered` (creds kept OUT via proxy) vs `env-in` (injected). Sorted by isolation tier, then egress strength.

| Project | Isolation | Egress control | Secrets | Self-host / Managed | Persistence | License |
|---|---|---|---|---|---|---|
| [Cleanroom](https://github.com/buildkite/cleanroom) | Firecracker µVM | **deny-default** | brokered | Self-host | ephemeral | MIT |
| [smolvm (smol-machines)](https://github.com/smol-machines/smolvm) | libkrun µVM | **deny-default** | brokered | Self-host | both | Apache-2.0 |
| [Leap0](https://leap0.dev) | Firecracker µVM | **deny-default** (allowlist) | brokered | Both | both | Proprietary (SDK Apache-2.0) |
| [InstaVM](https://instavm.io) | Firecracker µVM | **deny-default** (allowlist) | brokered | Both | both | Proprietary (CodeRunner Apache-2.0) |
| [Mitos](https://mitos.run) | Firecracker µVM (K8s) | **deny-default** | brokered (vsock) | Both | persistent | Apache-2.0 ⚠️ pre-1.0 |
| [Sprites (Fly.io)](https://fly.io/sprites) | Firecracker µVM | allowlist | env-in (ephemeral) | Managed | persistent | Proprietary |
| [microsandbox](https://github.com/superradcompany/microsandbox) | libkrun µVM | configurable (deny opt.) | brokered | Self-host (+cloud beta) | persistent | Apache-2.0 |
| [Superserve](https://superserve.ai) | Firecracker µVM | configurable (allowlist) | brokered | Both | both | Apache-2.0 |
| [Islo](https://islo.dev) | Cloud Hypervisor µVM | configurable (allow/deny) | brokered | Both (BYOC) | both | Proprietary |
| [Declaw](https://declaw.ai) | Firecracker µVM | configurable (allow/deny, L7) | brokered | Both (BYOC) | both | Proprietary (SDK Apache-2.0) |
| [Vercel Sandbox](https://github.com/vercel/sandbox) | Firecracker µVM | configurable (deny-all) | brokered | Managed | ephemeral | Apache-2.0 (SDK) |
| [BoxLite](https://github.com/boxlite-ai/boxlite) | KVM/HVF µVM | configurable (allowlist) | brokered | Self-host | persistent | Apache-2.0 |
| [Blaxel](https://blaxel.ai) | µVM | configurable (preview) | brokered | Managed | persistent | MIT (SDK) |
| [Qbox](https://qbox.sh) | Firecracker µVM | configurable | unverified | Self-host | ephemeral | unverified |
| [Katakate (k7)](https://github.com/Katakate/k7) | Kata+FC µVM (K3s) | configurable (allowlist) | env-in | Self-host | ephemeral | Apache-2.0 |
| [Runloop](https://runloop.ai) | VM + container | full-by-default (cfg) | brokered | Managed | persistent | Proprietary (SDK MIT) |
| [E2B](https://e2b.dev) | Firecracker µVM | full-by-default (cfg) | env-in | Both | ephemeral (pause/resume) | Apache-2.0 |
| [Northflank](https://northflank.com) | Kata+FC µVM | full-by-default | env-in | Both (BYOC) | persistent | Proprietary |
| [Arrakis](https://github.com/abshkbh/arrakis) | Cloud Hypervisor µVM | full-by-default | env-in | Self-host | persistent | AGPL-3.0 |
| [SmolVM (Celesto AI)](https://github.com/CelestoAI/SmolVM) | Firecracker+QEMU µVM | full-by-default (allowlist) | env-in | Self-host | both | Apache-2.0 |
| [Morph](https://morph.so) | µVM (VMM n/s) | unverified | env-in | Both | both | Proprietary (SDK OSS) |
| [Tensorlake](https://tensorlake.ai) | Firecracker+CH µVM | unverified | env-in | Both (BYOC) | both | Proprietary (SDK Apache-2.0) |
| [Freestyle](https://freestyle.sh) | Full VM/KVM | unverified | unverified | Managed | both | Proprietary (SDK OSS) |
| [Box (ascii.dev)](https://box.ascii.dev) | Linux VM | full-by-default | env-in | Managed | persistent | Proprietary · **EU regions** |
| [OpenComputer](https://opencomputer.dev) | KVM full VM | unverified | env-in | Both | persistent | Apache-2.0 |
| [Novita](https://novita.ai/sandbox) | Firecracker µVM | full-by-default | unverified | Managed | both | Proprietary |
| [Baponi](https://baponi.ai) | Container (seccomp+cgroups, zero-cap) | **deny-default** | brokered | Both | both | Proprietary |
| [OpenSandbox](https://github.com/alibaba/OpenSandbox) | Container (opt. gVisor/Kata/FC) | configurable (deny avail.) | brokered (Credential Vault) | Self-host | ephemeral | Apache-2.0 |
| [Cloudflare Sandboxes](https://developers.cloudflare.com/sandbox/) | VM-backed container | configurable (deny avail.) | brokered | Managed | both | Proprietary (SDK OSS) |
| [Daytona](https://daytona.io) | Container (ded. kernel) | configurable (tier-gated) | brokered | Both | persistent | AGPL-3.0 |
| [AIO Sandbox](https://github.com/agent-infra/sandbox) | Container (Docker) | configurable (proxy) | env-in | Self-host | ephemeral | Apache-2.0 |
| [Modal](https://modal.com) | gVisor | full-by-default (cfg) | env-in | Managed | ephemeral | Proprietary |
| [Beam](https://beam.cloud) | gVisor + runc | full-by-default (cfg) | env-in | Both | persistent | AGPL-3.0 |
| [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | gVisor/Kata (pluggable) | none (delegated) | env-in | Self-host (K8s) | persistent | Apache-2.0 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Container (Docker) | none | env-in | Both | ? | MIT |

### What the data shows (this is the differentiator)
- **Restricted-by-default egress is the minority.** Deny-by-default: **Cleanroom, smolvm (smol-machines), Leap0, InstaVM, Mitos, Baponi**; allowlist-default: **Sprites**. Roughly a dozen offer *configurable* egress (opt-in), and the rest ship open outbound or delegate/none (Modal, Beam, Northflank, Arrakis, Box, Novita, K8s Agent Sandbox, OpenHands). *Isolation is common; egress control is not.*
- **Secrets brokering (creds kept out of the sandbox)** is now a real cluster: Cleanroom, smolvm, Leap0, InstaVM, Superserve, Islo, Declaw, Vercel Sandbox, BoxLite, Blaxel, microsandbox, Runloop, Baponi, OpenSandbox, Cloudflare, Daytona. Env-in: E2B, Modal, Northflank, Beam, Arrakis, SmolVM (Celesto), Katakate, Sprites, Morph, Tensorlake, Box, OpenComputer, AIO Sandbox, K8s Agent Sandbox, OpenHands.
- **The strong-posture set** (µVM **and** restricted egress **and** brokered secrets) is small: **Cleanroom, smolvm (smol-machines), Leap0, InstaVM, Mitos** — plus Superserve/Islo/Declaw on configurable egress. That's the bar to beat.
- **EU data-residency** is advertised by exactly one *managed* entry (**Box (ascii.dev)** — DE/FI/FR). Self-hostable tools (Mitos, Cleanroom, microsandbox, smolvm, …) can be run in the EU *by you*, but no vendor offers an EU-native/sovereign *managed* service. Unaddressed across 35 providers.
- **Control-plane reachable from inside** (the "front desk" risk): Sprites documents an in-sandbox management API (reachable); Modal documents it is *not*. Others undocumented.

## Why security-posture-first?
Community consensus (HN, Reddit, the security literature) is blunt: **containers are not a trust boundary** for untrusted agent code, and **isolation alone "solves the easiest problem"** — the real risk is an agent with legitimate access exfiltrating data via network egress or leaked credentials (prompt injection). So we rank on the boundary *and* what crosses it, not on cold-start milliseconds (which matter only for ephemeral/high-concurrency workloads, not long-running coding agents).

Key nuance: almost every sandbox *has* outbound network — that's the problem, not a feature. The differentiator is whether egress can be **default-denied and allowlisted**, and whether **secrets are brokered so the sandbox never holds them**. A strong microVM with unrestricted network still lets a prompt-injected agent phone home with your code — isolation and egress control are **orthogonal**.

## VMs & microVMs
Strongest isolation (own kernel per sandbox). Built on [Firecracker](https://github.com/firecracker-microvm/firecracker), [libkrun](https://github.com/containers/libkrun), [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor).

Managed/commercial: [E2B](https://e2b.dev) · [Daytona](https://daytona.io) · [Modal](https://modal.com) · [Northflank](https://northflank.com) · [Vercel Sandbox](https://github.com/vercel/sandbox) · [Sprites (Fly.io)](https://fly.io/sprites) · [Runloop](https://runloop.ai) · [Blaxel](https://blaxel.ai) · [Superserve](https://superserve.ai) · [Islo](https://islo.dev) · [Leap0](https://leap0.dev) · [Declaw](https://declaw.ai) · [InstaVM](https://instavm.io) · [Tensorlake](https://tensorlake.ai) · [Morph](https://morph.so) · [Freestyle](https://freestyle.sh) · [Box (ascii.dev)](https://box.ascii.dev) · [OpenComputer](https://opencomputer.dev) · [Novita](https://novita.ai/sandbox) · [Qbox](https://qbox.sh)

Open-source / self-host: [microsandbox](https://github.com/superradcompany/microsandbox) · [smolvm (smol-machines)](https://github.com/smol-machines/smolvm) · [SmolVM (Celesto AI)](https://github.com/CelestoAI/SmolVM) · [Arrakis](https://github.com/abshkbh/arrakis) · [Cleanroom](https://github.com/buildkite/cleanroom) · [Mitos](https://mitos.run) · [Katakate (k7)](https://github.com/Katakate/k7) · [BoxLite](https://github.com/boxlite-ai/boxlite) · [ERA](https://github.com/BinSquare/ERA) · [Vibe](https://github.com/lynaghk/vibe) · [Volant](https://github.com/volantvm/volant) · [Netclode](https://github.com/angristan/netclode) · [yolo-cage](https://github.com/borenstein/yolo-cage) · [Chamber](https://github.com/cirruslabs/chamber) · [Matchlock](https://github.com/jingkaihe/matchlock) · [Gondolin](https://github.com/earendil-works/gondolin)

## Containers & gVisor
Shared-kernel isolation; faster, weaker boundary. Built on [gVisor](https://github.com/google/gvisor), [Kata Containers](https://github.com/kata-containers/kata-containers).

[OpenSandbox](https://github.com/alibaba/OpenSandbox) · [Cloudflare Sandboxes](https://developers.cloudflare.com/sandbox/) · [Beam](https://beam.cloud) · [Baponi](https://baponi.ai) · [AIO Sandbox](https://github.com/agent-infra/sandbox) · [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) · [OpenHands](https://github.com/OpenHands/OpenHands) · [SandboxAI](https://github.com/substratusai/sandboxai) · [llm-sandbox](https://github.com/vndee/llm-sandbox) · [MCP Runner](https://github.com/abir-taheer/mcp-runner) · [Sandboxer](https://github.com/ammmir/sandboxer) · [Kilntainers](https://github.com/Kiln-AI/Kilntainers) · [packnplay](https://github.com/obra/packnplay) · [yolobox](https://github.com/finbarr/yolobox) · [vibebin](https://github.com/jgbrwn/vibebin)

## Process & namespace sandboxes
Syscall/filesystem/network restriction for individual processes. Built on [Bubblewrap](https://github.com/containers/bubblewrap), Landlock, seccomp.

[Anthropic Sandbox Runtime](https://github.com/anthropic-experimental/sandbox-runtime) · [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) · [Leash](https://github.com/strongdm/leash) · [Fence (Tusk)](https://github.com/use-tusk/fence) · [Landrun](https://github.com/Zouuup/landrun) · [sandlock](https://github.com/multikernel/sandlock) · [PythonSafeEval](https://github.com/s3131212/PythonSafeEval)

## Filesystem & WASM sandboxes
[AgentFS](https://docs.turso.tech/agentfs) · [LocalSandbox](https://github.com/coplane/localsandbox) · [Wassette](https://github.com/microsoft/wassette) · [Eryx](https://github.com/eryx-org/eryx) · [Capsule](https://github.com/mavdol/capsule) · [AgentVM](https://github.com/deepclause/agentvm) · [amla-sandbox](https://github.com/amlalabs/amla-sandbox)

## Isolation building blocks
| Project | Type | License |
|---|---|---|
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | microVM (KVM) | Apache-2.0 |
| [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) | microVM (KVM) | Apache-2.0 |
| [Kata Containers](https://github.com/kata-containers/kata-containers) | microVM (OCI/CRI) | Apache-2.0 |
| [gVisor](https://github.com/google/gvisor) | user-space kernel | Apache-2.0 |
| [libkrun](https://github.com/containers/libkrun) | microVM library | Apache-2.0 |
| [Flintlock](https://github.com/liquidmetal-dev/flintlock) | microVM lifecycle mgmt | MPL-2.0 |
| [forkd](https://github.com/deeplethe/forkd) | fork-from-warm µVM engine (Firecracker) | Apache-2.0 |
| [Bubblewrap](https://github.com/containers/bubblewrap) | process sandbox | LGPL-2.0 |

## Adjacent
Related but not untrusted-code sandboxes for coding agents:
- [Ona](https://ona.com) — ex-Gitpod; container-based CDE + agent orchestration. **Acquired by OpenAI (announced June 2026, deal pending); folding into Codex.**
- [Coder](https://coder.com) — self-hosted CDE; isolation delegated to the provisioned backend. AGPL-3.0 (+ enterprise).
- [CodeSandbox SDK](https://codesandbox.io) — microVM CDE (now part of Together AI); primarily a dev environment.
- [Gitpod](https://gitpod.io) · [GitHub Codespaces](https://github.com/features/codespaces) · [Replit](https://replit.com) — cloud dev environments.
- [Steel.dev](https://steel.dev) — sandboxed browser sessions (not general code exec).
- [ComputeSDK](https://computesdk.com) · [VibeKit](https://docs.vibekit.sh) — routers/SDKs across sandbox providers (no own isolation).
- [agentbox (madarco)](https://github.com/madarco/agentbox) — self-hosted CLI running coding agents in parallel (Docker+FUSE / cloud VM); dev-workflow tooling on off-the-shelf isolation. MIT.
- [Giant Swarm Agent Platform](https://www.giantswarm.io/agent-platform) — Kubernetes-based agent governance/orchestration control plane (MCP); ships no dedicated untrusted-code sandbox.
- [Fireactions](https://github.com/hostinger/fireactions) — GitHub-Actions runner orchestrator on Firecracker µVMs; no agent/sandbox API. Apache-2.0.

## Related lists
[arjan/awesome-agent-sandboxes](https://github.com/arjan/awesome-agent-sandboxes) · [dloss/awesome-agent-sandboxes](https://github.com/dloss/awesome-agent-sandboxes) · [restyler/awesome-sandbox](https://github.com/restyler/awesome-sandbox) · [tizkovatereza/awesome-ai-sandboxes](https://github.com/tizkovatereza/awesome-ai-sandboxes) · [webcoyote/awesome-AI-sandbox](https://github.com/webcoyote/awesome-AI-sandbox)

## Contributing
PRs welcome — **and actually reviewed** (as time allows; no bot auto-closing your PR). See [`CONTRIBUTING.md`](CONTRIBUTING.md).
- One project per PR. Every matrix cell needs a **source link** (official docs/repo). Don't know a value? Use `?` — never guess.
- Entries must run agent-generated code with a real isolation boundary; no dead projects, no marketing-only pages. License is not a criterion.
- Spotted stale or wrong data? Open an issue or PR — accuracy is the whole point.

## Maintainers
Maintained by [@handle]. Contributions welcome.

## License
Content under [CC0-1.0 / CC-BY-4.0 — entscheiden].

