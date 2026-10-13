# Survey: AI Tooling, Human Agency, and "Value per Watt"

## Overview

Artificial Intelligence coding assistants and large language models (LLMs) have transformed software engineering. In the Tamlinux project, AI tools are not passive query boxes; they are active pair programmers, code transformers, and architectural researchers.

However, Tamlinux maintains a rigorous, principled philosophy regarding AI development:
1. **Direct Human Supervision & Agency:** AI tools work under the explicit direction and steering of Fred (the project maintainer). They never commit autonomous decisions or authorize releases on their own.
2. **Transparent Public Provenance:** Every tool, model, prompt, and action taken by an AI assistant is documented publicly in [`AI_PROVENANCE.md`](../AI_PROVENANCE.md).
3. **Resource Efficiency & "Value per Watt":** Tamlinux explicitly rejects non-deterministic, autonomous background AI daemon loops (such as OpenClaw and Hermes, D139, D140) in favor of deterministic tools supervised by humans.

This survey outlines the models, tools, and ethical operating policies governing AI in Tamlinux.

---

## 1. Candidate Comparison Matrix

| Tool / Model | Creator / Provider | Primary Role in Tamlinux | Concurrency & Execution Context | Status in Tamlinux | Role / Assessment |
|---|---|---|---|---|---|
| **Claude** (Opus / Sonnet) | Anthropic | Architectural design, decision interviews, core plan synthesis | Interactive CLI / Web sessions | `selected` | Primary orchestrator and reasoning partner |
| **Codex API** | OpenAI | Bounded delegation briefs, panel ports, mechanical refactoring | Batch task execution (`review.py`, delegation) | `selected` | High-speed code synthesis and testing |
| **Gemini / agy** | Google DeepMind | Antigravity CLI pair programming, repository-wide surveys | Interactive terminal agent (`agy`) | `selected` | Broad analysis and cross-repo execution |
| **ChatGPT** | OpenAI | Exploratory research and initial ideation | Web interactive | `evaluated` | Early conceptual research |
| **Cursor IDE** | Cursor / Anysphere | Graphical developer editor with inline AI agent | Native desktop application | `active` | Primary graphical IDE on workstation |
| **OpenClaw** | OpenClaw Project | Autonomous AI agent framework | Background daemon | `retired` | Retired from Tamlinux defaults (D139) |
| **Hermes** | Hermes Project | Dedicated agent integration | Service loop | `retired` | Retired from Tamlinux defaults (D140) |

---

## 2. The Tamlinux AI Philosophy: Human Agency and "Value per Watt"

### The Decision to Retire Autonomous Agent Daemons (D139 & D140)
On 2026-10-12, Fred made two landmark architectural decisions regarding AI integration in Tamlinux:
- **Decision D139:** *Retire OpenClaw support from the Tamlinux product.*
- **Decision D140:** *Retire dedicated Hermes integration from Tamlinux's supported defaults.*

**The Core Rationale: "Value per Watt"**
> *"Non-deterministic autonomous AI loops may consume substantial computing resources and energy with uncertain return, adding less predictable value than ordinary daemons, which Tamlinux also minimizes. Deterministic tools offer more predictable resource use and value per watt... Until AI systems are more intelligent, we want to run them under the direct supervision of humans."* — Fred Horch (D139)

Tamlinux strictly separates **deterministic computer software** from **supervised AI collaboration**:
- An operating system must be predictable, auditable, and reliable. Tamlinux refuses to embed autonomous AI background processes that poll in endless loops, consume CPU cycles, and execute arbitrary unverified actions.
- AI belongs in the developer seat, working side-by-side with human engineers during conscious development sessions.

---

## 3. The Orchestration and Delegation Model

Tamlinux operates a multi-agent development workflow coordinated by `tam-work`:
1. **Human Steering:** Fred sets priorities, approves plans, conducts interviews, tests candidate packages, and makes all release decisions (`LIFECYCLE.md`).
2. **Path-Granular Concurrency (`tam-work`):**
   - Sessions claim exact repository paths before editing (`tam-work begin --scope ...`), preventing file conflicts between concurrent agents.
   - Separate sessions (Claude, Codex, agy) share checkouts cleanly without overwriting work.
3. **Bounded Delegation:**
   - Complex mechanical tasks (e.g. porting 6,900 lines of panel UI code from Omarchy to Tamlinux, D106, D107) are specified in structured briefs with declared inputs, outputs, and expected test failures.
   - Orchestrator agents review diffs byte-for-byte before merging into `develop`.

---

## 4. Public Provenance and Upstream Engagement

### Public Provenance (`AI_PROVENANCE.md`)
Tamlinux embraces complete transparency regarding AI authorship:
- Every public repository (`tamlinux`, `tamlinux-packages`, `tam`, `libtam`, `ecosystem-fred-tamlinux`) maintains an `AI_PROVENANCE.md` file at its root.
- Each entry records the date, owning task, tool/agent name, model version, and user prompt.
- In accordance with privacy and security runbooks (`public-ai-provenance.md`), internal session IDs and local paths are recorded only in private logs, while public repositories maintain clear, reproducible public records.

### Upstream AI Policies and Honest Engagement
Tamlinux interacts honestly with upstream open-source projects:
- **Hyprland:** Banned AI-written pull requests outright; Tamlinux respects this policy by maintaining public forks (`greenermoose/Hyprland`) and publishing patch recipes here in `ecosystem-fred-tamlinux` rather than spamming upstream review queues.
- **Void Linux:** Enforces human-only contributions and mandatory AI disclosure across all project spaces (June 2026); Tamlinux carries its own `xbps-src` templates permanently, and any upstream contact is written by Fred personally.

---

## Summary

Tamlinux proves that AI coding tools can be used with integrity, discipline, and environmental responsibility. By rejecting autonomous background agent loops, documenting provenance publicly, and maintaining direct human supervision over every commit, Tamlinux harnesses AI power while upholding the highest standards of software craft.
