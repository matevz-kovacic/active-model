# From a locally measured ≈#8 to a verified #1 — SOL-ExecBench kernel 094

## Active Model on NVIDIA B200

**Benchmark:** NVIDIA SOL-ExecBench · scores kernels against hardware speed-of-light limits rather than a framework baseline; NVIDIA runs the evaluator
**Kernel:** `094_time_decay_exponential_stabilization`
**Hardware:** NVIDIA B200
**SOL score:** **0.999092** · **16/16 workloads correct**
**Result:** **#1** — reached in the first campaign, lost to another participant days later, retaken with a new kernel architecture in a second campaign (see Chapter 2)
**Campaign duration:** ~20 hours over one weekend — 4 h autonomous, ~16 h under research direction; plus a later round three days on (see postscript); plus a second campaign of ~16 hours the following weekend (see Chapter 2)
**Implementations evaluated:** 240 distinct configurations on B200 — 50 in the first campaign (3 in the autonomous phase, 41 under steering, 6 in the later round) and 190 in the second campaign
**Prior GPU-kernel experience:** none

[Public leaderboard](https://research.nvidia.com/benchmarks/sol-execbench/leaderboard/kernel/94/B200) · [Kernel](https://research.nvidia.com/benchmarks/sol-execbench/kernel/94)

*This page describes the research process and the verified outcome. While the benchmark remains actively contested, implementation details, the techniques adopted and the experiments that refuted the others are deliberately withheld; they are kept in the campaign records and can be shared privately for serious technical review.*

## The question this tests

Most published work on AI-generated kernels trains or scaffolds specifically for the task — fine-tuned kernel models, RL-trained kernel agents, kernel-specific search harnesses. That leaves a narrower question open: what happens when a **general-purpose** research harness, built for unrelated optimization problems and never designed for GPUs, is pointed at a kernel benchmark cold?

Active Model is that harness. I had never written a GPU kernel. This is one data point on what it did over a weekend — including how far it got unaided, and what changed when I began steering.

The model was not asked to generate CUDA once. It conducted an iterative optimization campaign: reproducing prior work, diagnosing unexplained performance gaps, generating alternative mathematical formulations, designing new kernel architectures, running controlled experiments, analyzing performance workload by workload, abandoning attractive ideas when measurements rejected them, and combining independently successful ideas — until an external evaluator placed the result at the top of the leaderboard. The sections below are the record of that process.

## Autonomy boundary

### Phase 1 — autonomous

Active Model received the problem, evaluator, tools and compute budget. It investigated the problem, generated implementations, ran experiments, evaluated results and iterated on its own hypotheses.

With no technique-level input it wrote and evaluated **3 candidate architectures on B200 in under four hours**, starting from the public specification and reference implementation. The best of them measured **0.997900** on our own B200 runs — equivalent to **#8** on the leaderboard as it stood. That figure was never submitted to NVIDIA, so it is a locally measured position, not an officially evaluated one.

The boundary is worth stating precisely. I chose the target kernel — from a "frontier reproducibility" criterion, favouring problems where many independent teams cluster near the top — and directed the model to mine public prior work before writing code. Everything downstream of that was the model's own.

**This phase was interrupted, not exhausted.** When I began steering, the model had already diagnosed the largest single defect of the campaign on its own — a defect in how the submissions were being built, inherited by every prior version — and had four further candidates queued. Whether it would have continued improving unaided is untested; I did not run that counterfactual.

### Phase 2 — human-steered research

After the first measured round I began acting as a research lead. My interventions ranged from strategy — *"analyze which workloads are actually losing"*, *"don't assume another parameter sweep is the answer"*, *"investigate why this supposedly fast implementation is unexpectedly slow"* — to naming specific techniques worth testing.

I made **13 technique-level proposals. The model adopted 3 and refuted 10**, each with a mechanism identified.

What the model owned throughout: deciding *how* to implement each idea, designing the experiments, measuring, attributing results per workload, and — repeatedly — **rejecting suggestions that its measurements refuted**.

Steered phase: **~16 hours · 41 variants measured · 13 proposals**.

> **The first 4 autonomous hours reached a locally measured ≈#8. Model-generated engineering under human research direction reached #1.**

## What the model found on its own

* **A build defect inherited by every prior submission.** Noticed because a reproduction ran at a fraction of the speed its public source claimed; confirmed by an instruction census of the compiled code rather than by argument.
* **A numerical contract hidden in a reference implementation.** On a different kernel in the same campaign, the reference imposed a precision constraint that structurally forbids the obvious library solution. Two GPU debugging rounds had chased the wrong cause; a $0 CPU bisection settled it.
* **The binding constraint, via profiling.** Hardware profiles showed that the resource limiting the dominant workloads was not the one prior work had assumed, which redirected the rest of the campaign.

## Ideas tested — and the ones that failed

The campaign explored ten distinct lines of attack on the kernel. Most were refuted, and refutations mattered as much as wins, because each one redirected the search: every refuted idea was closed with a measured runtime change and an identified mechanism, and none was retried without new evidence. The list itself is withheld while the benchmark is contested.

## Workload specialization

A turning point was recognizing that the 16 benchmark workloads occupy different performance regimes, and that no single kernel topology was optimal across them. The final solution routes each workload to the implementation that measured fastest for it.

## Measurement discipline

Near the top of a leaderboard, noise masquerades as progress — and automated kernel optimization has already produced headline speedups that turned out to be artifacts of the evaluation harness rather than real work. The campaign used repeated same-machine measurements, per-workload attribution, measured noise floors, rejection of improvements that did not clear noise, and repeated evaluation of final candidates before submission.

One finding is worth stating explicitly: the official evaluator's run-to-run variation is a **global per-run bias** (~15e-6, with 14 of 16 workloads moving together), not per-workload jitter — so any single-run improvement below ~20e-6 is meaningless. The published results were reproduced across independent official evaluations.

This is also why the campaign did not stop when it first took the lead. **#1 was reached 3.4 hours into the steered phase; the remaining ~13 hours produced no change in rank.** They raised the margin over the previous leader from +0.000013 to +0.000071 — converting a result inside evaluator noise into one comfortably outside it.

None of the scores on this page are self-reported. They are the scores **measured** and shown by **NVIDIA's SOL-ExecBench** leaderboard.

## Outcome

```text
benchmark + evaluator
        |
autonomous Active Model research         ->  ~#8    (3 architectures, 4 h)
        |
high-level human research steering             (13 proposals: 3 adopted, 10 refuted)
        |
model-generated hypotheses -> multiple kernel architectures
        |
B200 experiments and per-workload attribution  (41 variants, ~16 h)
        |
workload-specialized solution
        |
NVIDIA evaluation                        ->  #1, SOL 0.998564
        |
later round: offline analysis, no GPU          (6 variants, 1 rental)
        |
NVIDIA evaluation                        ->  #1, SOL 0.998647
        |
another participant posts 0.999005       ->  #2
        |
second campaign: new kernel architecture
(autonomous), integrated selectively
into the existing dispatcher             ->  0.999015, ahead by 10 ppm (private)
        |
three written review rounds                    (~33 proposals: 5 adopted, the rest refuted)
        |
NVIDIA evaluation                        ->  #1, SOL 0.999092 (+87 ppm over the new #2)
```

## Postscript — a later round, after the campaign was called finished

The campaign's own records closed this kernel with the verdict that its idea space was exhausted. That verdict rested on hardware profiles taken on a subset of the routes; several others had never been profiled at all.

Asked what could be learned **without renting a GPU**, the model re-derived where the score was actually sensitive, found an unprofiled tier with real headroom, and identified a remedy in the one place the launch geometry left room for it.

The entire candidate set was generated, compiled for the B200 target, and screened for resource usage and scheduling problems **locally, on a machine with no GPU**, using the CUDA toolchain already present in a container. One configuration was eliminated on that evidence before it ever consumed GPU time. A single 17-minute rental measured the rest, against a byte-identical control in the same session.

**0.998564 → 0.998647.** The margin over the previous leader went from +0.000071 to **+0.000154**. Outputs are numerically identical to the previous version — not merely inside tolerance.

Two results are worth reporting against interest. The predicted gain was **2.5× larger** than the measured one: the mechanism was right, the magnitude was not. And a control configuration included specifically to falsify the model's own reasoning did falsify part of it.

Unlike the steered phase, this round involved no technique-level human input. The direction given was to look for opportunities that did not require renting hardware, and later to run the experiment and submit the result.

## Chapter 2 — overtaken, then #1 again with a new architecture

A day after the postscript, the lead was gone. Another participant posted **0.999005**, 358 ppm above 0.998647, and the campaign's own closing verdict — "idea space exhausted" — was now a verdict about a #2 kernel.

I opened a second campaign in a separate directory with one instruction: start from the current kernel, do not copy the first campaign's attempts, and bring it back to #1. The first campaign's kernel, tooling and dead-end registry were read-only inputs, and the two campaigns were isolated from each other at the infrastructure level.

### What the model built on its own

The second campaign developed a substantially different time-parallel architecture for the workloads the first campaign had identified as limiting — one the first campaign's records had concluded was not achievable without a cost it could not afford. The design was first validated mathematically, against a CPU model of the kernel, before any GPU was rented, and then integrated selectively into the existing workload dispatcher, one workload at a time, wherever it measured faster than the incumbent.

Its first official measurement scored **0.999015** — above the new leader, by 10 ppm. By the evaluator-noise standard of the first campaign, that is not a lead. The next sixteen hours bought the margin.

### Three rounds of review

I wrote three review plans, roughly 8, 13 and 12 technique-level proposals each. The model adopted five and refuted the rest, each refutation measured on the same rental against a byte-identical control, with the reading of each possible outcome written down before the rental started.

The largest single gain was not one of my proposals as written: the model extended a proposed experiment one step beyond the ladder I had specified, after the specified rungs had measured nothing, and identified the mechanism behind the gain. Every composed candidate was validated twice on the same rental against two controls before it was submitted.

### Calibration before belief

Each round started with a measurement rather than a design: the attainable device figure for this kernel's access pattern, a replay of the evaluator's own preconditioning, per-block timing distributions, and finally a calibration build of the kernel that established the remaining gap was not reachable by the mechanisms under review. That last measurement is what closed the campaign.

### Reported against interest

One adopted route gained on every rental and did not transfer to official evaluation. Another adopted change gains partly from measurement rather than from less work, and the campaign records say so. My highest-confidence proposal of the third round was predicted at 10–20 ppm and delivered 0; the mechanism I had assumed was not operating. The third review round as a whole produced nothing.

**0.998647 → 0.999015 → 0.99906 → 0.999084 → 0.999092.** 43 B200 rentals, 12.2 GPU-hours, $45. The margin over the participant who had overtaken us went from −358 ppm to **+87 ppm**, reproduced across four official evaluations that moved by +3, 0, −10 and −8 ppm relative to their same-session rentals.

## What this does and does not establish

This is one kernel, on one hardware target, in one campaign. It does not establish that a general-purpose harness matches kernel-specialized systems in general, and it does not separate the harness's contribution from the underlying model's.

It also does not establish that the steering was necessary. The autonomous phase was four hours old and still producing new results when I intervened; I stopped it to steer rather than because it had stopped improving. What the campaign shows is that the model produced frontier work under research direction — not that it could not have got there without it, and not that it would have.

What it does establish is narrower and, I think, still worth reporting: a harness built for unrelated optimization problems transferred into an unfamiliar domain with no kernel-specific scaffolding, reached a credible position autonomously, and produced externally verified frontier work under research direction.
