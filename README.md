# Active Model

**Experimental AI research system for verifier-backed optimization, systems research, and algorithm discovery.**

Active Model investigates whether a frontier model can operate as an experimental researcher rather than merely as a coding assistant:

```text
objective + evaluator
        ↓
reconnaissance → hypotheses → implementation → experiments
        ↓
measurement → failure analysis → next hypothesis
```

The emphasis is on **externally checkable results**.

## Highlights

### 🥇 Reached #1 — NVIDIA SOL-ExecBench kernel 094, B200

**094_time_decay_exponential_stabilization** · **SOL score 0.998564**

[Leaderboard](https://research.nvidia.com/benchmarks/sol-execbench/leaderboard/kernel/94/B200)

Active Model attacked the benchmark from the public specification, reference implementation and evaluator, and reached a locally measured **0.997900** on this kernel — ≈**#8** on the board at the time — in its first 4 hours, before human research steering began.

**Autonomy boundary.** Active Model produced every implementation, experiment, measurement and attribution in this campaign. A human research lead set strategy and, after the first measured round, named specific techniques to try (wider per-thread ownership, asynchronous shared-memory staging, moving max-state off the dependency chain). The model implemented and adjudicated 13 such proposals against its own measurements — adopting 3 and refuting 10 with identified mechanisms — and independently found the largest single defect of the campaign: a compiler-flag regression costing ~1.6× on the hot path.

> **The first 4 autonomous hours reached a locally measured 0.997900 — ≈#8 on the board at the time. Model-generated engineering under human research direction reached #1.**

This distinction is intentional: I do not describe the complete run as autonomous. Nor was the autonomous phase exhausted — it had already diagnosed the compiler-flag defect on its own and had 4 further candidates queued when steering began. Whether it would have reached #1 unaided is untested.

[Technical case study](./sol-execbench-094/README.md)

### modded-nanogpt — autonomous LLM-training optimization on 8×H100

[PR #358](https://github.com/KellerJordan/modded-nanogpt/pull/358) *(open)*

For this experiment, Active Model received a **single high-level objective** and conducted the optimization search autonomously. It inspected the existing record implementation, selected optimization targets, implemented the modifications, designed and ran the performance experiments, checked the validation-loss constraint, and prepared the submission.

Measured improvement: **−0.729 s mean** against the previous Track 1 implementation in paired same-machine measurements on two independent **8×H100** leases — **6.0× and 8.7×** the corresponding A/A noise floors (mean val loss 3.27886, p = 0.0014 over 20 runs).

This is currently the clearest experiment in the repository demonstrating the fully autonomous operating mode.

### Production systems optimization

* **llama.cpp** — [PR #27478](https://github.com/ggml-org/llama.cpp/pull/27478) *(open)*: "ggml : speed up batch-1 CPU decode, align large allocations". Up to **+15.29%** end-to-end token-generation throughput on Ryzen 7 9700X (attention change alone +10.67%) and **+9.22%** on Neoverse-N1, measured on Qwen3-30B-A3B Q4_K_M at 8192-token context.
* **zstd** — three optimization PRs on encode/decode hot paths submitted upstream: [#4729](https://github.com/facebook/zstd/pull/4729) · [#4732](https://github.com/facebook/zstd/pull/4732) · [#4733](https://github.com/facebook/zstd/pull/4733). Includes a decompression-hot-loop optimization removing a loop-carried memory dependency, improving decode throughput by **+2.7–3.4%** with GCC and **+5.5–9.3%** with Clang on Zen 5, with the same direction on Intel Raptor Lake.
* **dav1d** — two AV1 decoder optimizations submitted upstream. [!1967 *refmvs: collapse runs of identical temporal MVs*](https://code.videolan.org/videolan/dav1d/-/merge_requests/1967): 77.5% of scanned temporal cells are bit-identical to their predecessor, so collapsing each run into one weighted call removes 77.5% of `add_temporal_candidate()` invocations (39.6M → 8.9M) — **+0.5–0.8%** decode across x86-64 and AArch64, up to **+2.96%** on high-redundancy content. [!1968 *mc: avg_direct for full-pel compound blocks*](https://code.videolan.org/videolan/dav1d/-/merge_requests/1968): for full-pel compound blocks the two-buffer scratch round trip reduces exactly to `(a + b + 1) >> 1`, eliminating it for 37.6–78.3% of compound plane-predictions — **+0.9–2.8%** depending on how strong the baseline SIMD path is. Both are exact by construction: bit-identical decoded output across 12 streams.

## Two operating modes

**Autonomous research** — the human supplies the objective, evaluator, constraints, tools and compute; the model chooses what to investigate and performs the technical search. *Example: modded-nanogpt.*

**Human-steered research** — the model still generates, implements and adjudicates the concrete solutions, but a human acts as a research lead: redirecting the search, questioning conclusions, and naming areas or techniques worth investigating. *Example: SOL-ExecBench 094 after the autonomous phase.*

The repository reports the two separately, because a result obtained with strategic steering demonstrates something different from a fully autonomous one.

## Other verifier-backed results

* [**n=32 circle packing**](./n32_circle_packing) — improved by 4.45e-8 over Berthold et al. (Jan 2026), verified with the published verifier.
* [**n=21 rectangle packing**](./n21_circle_packing_rectangle) — validated against the published **AlphaEvolve** result.
* [**n=26**](./n26_circle_packing) · [**n=26 rectangle**](./n26_circle_packing_rectangle) · [**n=27 rectangle**](./n27_circle_packing_rectangle) — further circle-packing results.
* [**Spherical codes**](./spherical_codes) — new best-known S⁵ configurations for N=86 and N=98, registered with spherical-codes.org.
* [**Pegase AC-OPF**](./minlplib) — improved primal for the 13,659-bus European grid (386,108.81 → 386,106.54), accepted into MINLPLib.
* [**Lennard-Jones clusters**](./lennard_jones) — canonical minima matched for LJ38, LJ75 and LJ104.
* [**Santa 2025 tree packing**](./santa2025_tree_packing).

See the individual result directories for evidence, verification procedures and caveats.

## What these experiments suggest

The common feature of the successful tasks is increasingly clear. It is **not** geometry, CUDA, or any particular optimization algorithm. It is the existence of:

1. a concrete objective;
2. a reliable evaluator;
3. an experimental environment;
4. enough freedom to modify the proposed solution;
5. a feedback loop fast enough for repeated hypothesis testing.

Under those conditions, frontier models appear capable of substantially more open-ended technical search than one-shot code generation. How far that extends is the research question behind Active Model.

## Verification

Claims here should be independently checkable through official benchmark leaderboards, upstream tests and CI, externally maintained verifiers, paired performance measurements with measured noise floors, exact-output checking, or independent benchmark maintainers.

Failed experiments are useful evidence too. The objective is not to make every run look successful, but to understand which research loops work.

## Source and trace policy

This repository is primarily a **results and verification archive**. The full Active Model harness, operating rules and complete research traces are not currently public.

For actively competitive benchmarks the winning implementation may be withheld temporarily even when the verified result and methodology are public — the current #1 SOL-ExecBench kernel is not being released while the benchmark remains actively contested. The performance claim does not depend on it: the result is published by NVIDIA's own evaluator and leaderboard.

Selected implementation details can be shared privately for serious technical review or research collaboration.

## Research interests

autonomous research agents · AI for systems · model self-improvement through experimental feedback · GPU and CPU performance engineering · LLM training and inference optimization · algorithm discovery · verifier-guided mathematical and computational search

## Contact

Matevž Kovačič — [matevz.celje@gmail.com](mailto:matevz.celje@gmail.com)
