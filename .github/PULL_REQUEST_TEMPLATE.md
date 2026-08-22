<!-- One project per PR. See CONTRIBUTING.md. -->

**Project:** <!-- name + official URL -->

**Section:** <!-- VMs & microVMs / Containers & gVisor / Process & namespace / Filesystem & WebAssembly / Isolation building blocks / Adjacent -->

**What it is:** <!-- one factual sentence: what enforces the isolation boundary -->

## Sources

<!-- Official docs or repo only — not a blog post, not a vendor comparison, not
     this list. Quote the supporting phrase so a reviewer can verify without
     re-researching. One line per claim you are making or changing. -->

- Isolation:
- Egress control:
- Secrets:

## Checklist

- [ ] One project per PR
- [ ] Entry is `- [Name](official-url) - One factual sentence.`, stating the mechanism, not the pitch
- [ ] Every matrix cell I added or changed has a source above; unknown values are `?`, not guesses
- [ ] If I touched the matrix: re-ran `script/sandboxes-data.py`
- [ ] `npx awesome-lint` passes
