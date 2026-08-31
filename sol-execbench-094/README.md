# From autonomous ≈#8 to #1 on SOL-ExecBench kernel 094

## Active Model on NVIDIA B200

**Benchmark:** NVIDIA SOL-ExecBench · scores kernels against hardware speed-of-light limits rather than a framework baseline; NVIDIA runs the evaluator
**Kernel:** `094_time_decay_exponential_stabilization`
**Hardware:** NVIDIA B200
**SOL score:** **0.998564** · **16/16 workloads correct**
**Result:** **#1**
**Campaign duration:** four hours over one weekend · three candidate implementations evaluated
**Prior GPU-kernel experience:** none

[Public leaderboard](https://research.nvidia.com/benchmarks/sol-execbench/leaderboard/kernel/94/B200) · [Kernel](https://research.nvidia.com/benchmarks/sol-execbench/kernel/94)

## The question this tests

Most published work on AI-generated kernels trains or scaffolds specifically for the task — fine-tuned kernel models, RL-trained kernel agents, kernel-specific search harnesses. That leaves a narrower question open: what happens when a **general-purpose** research harness, built for unrelated optimization problems and never designed for GPUs, is pointed at a kernel benchmark cold?

Active Model is that harness. I had never written a GPU kernel. This is one data point on what it did over a weekend — including where it stopped on its own, and what it took to get past that.

The model was not asked to generate CUDA once. It conducted an iterative optimization campaign: reproducing prior work, diagnosing unexplained performance gaps, generating alternative mathematical formulations, designing new kernel architectures, running controlled experiments, analyzing performance workload by workload, abandoning attractive ideas when measurements rejected them, and combining independently successful ideas — until an external evaluator placed the result at the top of the leaderboard. The sections below are the record of that, refutations included.

## Autonomy boundary

### Phase 1 — autonomous

Active Model received the problem, evaluator, tools and compute budget. It investigated the problem, generated implementations, ran experiments, evaluated results and iterated on its own hypotheses. This phase reached approximately **#8** on this kernel, with no intervention.

### Phase 2 — human-steered research

After the autonomous search plateaued I acted as a research lead. My interventions ranged from strategy — *"analyze which workloads are actually losing"*, *"don't assume another parameter sweep is the answer"*, *"investigate why this supposedly fast implementation is unexpectedly slow"* — to naming specific techniques worth testing.

What the model owned throughout: deciding *how* to implement each idea, designing the experiments, measuring, attributing results per workload, and — repeatedly — **rejecting suggestions that its measurements refuted**. Three of my proposals became winning changes; four were killed by the model's own data, each with a mechanism identified.

> **Active Model autonomously reached ≈#8. With research-lead steering, it generated the technical work that reached #1.**

## What the model found on its own

* **A compiler-flag regression worth ~1.6×.** Custom `cuda_cflags` silently *replace* the evaluator's `--use_fast_math` default, so every submission had been compiling its fp32 divides down the IEEE slow path. Confirmed by SASS instruction census (1.63–1.69× bloat) after the model noticed a reproduction running at half the speed its public source claimed.
* **A numerical contract hidden in a reference implementation.** On a different kernel in the same campaign, a reference rounded intermediates to bf16 before softmax, which structurally forbids library attention kernels. Two GPU debugging rounds had chased the wrong cause; a $0 CPU bisection settled it.
* **The binding constraint, via profiling.** Nsight Compute showed the dominant workloads running at **0.69 waves/SM** — 512 blocks against ~740 concurrent slots, 21% achieved occupancy — while still reaching 78–82% of DRAM peak from per-thread memory-level parallelism alone. The kernel was parallelism-starved, not bandwidth-bound.

## Ideas tested — and the ones that failed

Explored: persistent recurrent lanes; a raw-state reformulation that removes one transcendental from the sequential hot loop; reuse of intermediate exponential products; moving max-state off the per-token dependency chain; time-chunk parallelization; coalesced chunk layouts; shared-memory caching; low-batch tiled kernels; adjacent-channel vectorization; workload-specific launch and kernel selection.

Refutations mattered as much as wins, because each one redirected the search. Every entry below is a rejected idea; the *result* column reports «define the convention here — e.g. change in kernel runtime, so all figures are slowdowns».

| idea | result | mechanism identified |
|---|---|---|
| shared-memory tiling at high batch | −199% | 8-channel blocks issue 32-byte memory requests where the hardware wants 128 |
| O(C²) → O(C) prefix restructure | −44% | the "redundant" work was L2-resident arithmetic hidden under memory latency; the fix added a launch and a global round-trip |
| finer per-thread ownership | +11–16% | same bytes in flight at double the load-instruction count |
| streaming cache hints | +10–25% | L1 caching was doing real work on those streams |
| custom exponential (SFU bypass) | killed before spending | profiler showed compute pipelines 65% idle — the SFU was never the limiter |

## Workload specialization

A turning point was recognizing that the 16 benchmark workloads occupy different performance regimes: tiny batches with insufficient recurrent-lane parallelism; intermediate workloads dominated by recurrence and special-function latency; large batches approaching streaming-memory limits.

No single kernel topology was optimal across all three. The final solution routes each workload to the architecture that measured fastest for it.

## Measurement discipline

Near the top of a leaderboard, noise masquerades as progress — and automated kernel optimization has already produced headline speedups that turned out to be artifacts of the evaluation harness rather than real work. The campaign used repeated same-machine measurements, per-workload attribution, measured noise floors, rejection of improvements that did not clear noise, and repeated evaluation of final candidates before submission.

One finding is worth stating explicitly: the official evaluator's run-to-run variation is a **global per-run bias** (~15e-6, with 14 of 16 workloads moving together), not per-workload jitter — so any single-run improvement below ~20e-6 is meaningless. The published result was reproduced across independent official evaluations.

The **0.998564** figure is not self-reported. It is the score **measured** and shown by **NVIDIA's SOL-ExecBench** leaderboard.

## Outcome

```text
benchmark + evaluator
        ↓
autonomous Active Model research        →  ≈#8
        ↓
high-level human research steering
        ↓
model-generated hypotheses → multiple kernel architectures
        ↓
B200 experiments and per-workload attribution
        ↓
workload-specialized solution
        ↓
NVIDIA evaluation                       →  #1, SOL 0.998564
```

## What this does and does not establish

This is one kernel, on one hardware target, in one campaign. It does not establish that a general-purpose harness matches kernel-specialized systems in general, and it does not separate the harness's contribution from the underlying model's. The autonomous phase plateaued at ≈#8 and did not recover on its own — more iterations produced more variants of the same strategy, not a new one. Getting past that took a human naming directions to try.

What it does establish is narrower and, I think, still worth reporting: a harness built for unrelated optimization problems transferred into an unfamiliar domain with no kernel-specific scaffolding, reached a credible position autonomously, and produced externally verified frontier work under research direction.

## Implementation

The performance claim does not depend on private benchmarking — it is published by NVIDIA's evaluator. I may release the implementation once the competition has moved on. For serious research review or collaboration I am open to sharing implementation details privately.
