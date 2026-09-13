# From two unpublished ≈#2 results to a verified #1 — SOL-ExecBench kernel 049

## Active Model on NVIDIA B200

**Benchmark:** NVIDIA SOL-ExecBench · NVIDIA runs the evaluator
**Kernel:** `049`
**Hardware:** NVIDIA B200
**SOL score:** **0.588237**
**Result:** **#1 on the official NVIDIA B200 leaderboard**
**Before external steering:** two unpublished Active Model solutions whose measured performance would have placed them **#2 at the time**

[Public leaderboard](https://research.nvidia.com/benchmarks/sol-execbench/leaderboard/kernel/49/B200)

*This page describes the research process and verified outcome. While the benchmark remains actively contested, the final implementation and performance-critical techniques are deliberately withheld.*

## The question this tests

Active Model is an experimental research harness built around a simple loop:

```text
hypothesis
    ↓
implementation
    ↓
experiment
    ↓
measurement
    ↓
analysis
    ↓
next hypothesis
```

On kernel 049, that process got very close to the top on its own.

Active Model produced two separate kernels whose measured performance would have placed them **#2 on the public leaderboard**. Neither was submitted.

But the existing #1 was substantially harder to crack. Continued local iteration was producing strong candidates without closing the remaining gap.

I therefore changed the research process rather than the implementation system.

## Phase 1 — Active Model reaches approximately #2

Active Model received the benchmark, evaluator, tools and B200 access and conducted the optimization campaign.

It generated candidate implementations, evaluated them, analyzed workload-level performance and iterated.

Two independently produced candidates eventually reached performance that would have ranked **#2 on the leaderboard at the time**.

At that point the campaign had reached a strong local frontier.

The problem was no longer producing a competitive kernel.

The problem was finding a qualitatively better direction.

## Phase 2 — external reasoning rounds

I began periodically taking the **current best Active Model solution and its measurements** and pasting them into ChatGPT using **Astra at maximum reasoning effort**.

I asked for new candidate approaches: architectural changes, unexplored variations, explanations for the remaining gap, and experiments that might distinguish between competing hypotheses.

Those suggestions were then passed back into Active Model.

Active Model remained responsible for the actual research execution:

* interpreting the proposed direction;
* implementing concrete kernel variants;
* compiling and validating them;
* running them on B200;
* measuring performance;
* analyzing the results;
* retaining or rejecting ideas based on evidence.

I then took the improved solution and its new measurements back into another Astra reasoning round.

The loop was repeated several times.

```text
Active Model
current best kernel + measurements
        |
        v
ChatGPT / Astra
maximum-effort reasoning
        |
        v
candidate directions
        |
        v
Active Model
implementation + B200 experiments
        |
        v
new best kernel + measurements
        |
        +--------------------+
        |                    |
        +------ repeat ------+
```

The important point is that Astra did not produce a kernel that was simply submitted.

It proposed research directions.

Active Model turned those directions into actual implementations and experimentally adjudicated them.

## Autonomy boundary

The roles were distinct.

### Active Model

Active Model was the implementation and experimental engine throughout the campaign.

It produced the actual kernels, ran experiments, analyzed measurements and decided which ideas survived.

Before external steering began, it had already independently reached approximately #2-level performance with two separate solutions.

### ChatGPT / Astra

Astra was used as an external research adviser after the initial campaign reached that frontier.

It was shown the current solution and experimental evidence and asked to propose new directions.

Its output was research advice rather than executable submissions.

### Human role

I orchestrated the loop.

I decided when the current research state should be subjected to another external reasoning pass, transferred the relevant solution and measurements to Astra, and passed its proposed directions back into Active Model.

The resulting process was therefore a **human-orchestrated model-to-model research loop closed by hardware experiments**.

## Why repeated rounds mattered

There was no single insight that immediately transformed the #2-level kernel into #1.

The incumbent was strong enough that the search had to proceed iteratively.

Each reasoning round started from a different state because Active Model had already implemented and tested suggestions from the previous one.

So Astra was not repeatedly solving the original benchmark from scratch.

It was reasoning over an **evolving body of experimental evidence**.

```text
strong kernel
    ↓
reason about remaining gap
    ↓
new hypotheses
    ↓
implement
    ↓
measure on B200
    ↓
updated kernel
    ↓
reason again
```

That continued until the combined process broke through the incumbent.

## Measurement remained the authority

Near the top of the leaderboard, plausible optimization ideas are easy to generate and actual improvements are difficult.

A suggestion could help one workload and hurt another. A theoretically attractive change could measure flat. A small apparent gain could disappear under repeated evaluation.

For that reason, suggestions from Astra had no privileged status.

Every useful idea still had to pass through:

```text
proposal
    ↓
implementation
    ↓
correctness
    ↓
B200 measurement
    ↓
evidence
```

The models generated hypotheses.

The hardware decided which ones survived.

## Outcome

The full campaign reduced to:

```text
SOL-ExecBench kernel 049
        |
        v
Active Model optimization
        |
        v
two unpublished ≈#2-level solutions
        |
        v
strong local frontier
        |
        v
current kernel + measurements
        |
        v
ChatGPT / Astra
maximum-effort reasoning
        |
        v
new candidate directions
        |
        v
Active Model
implementation + B200 experimentation
        |
        v
updated research state
        |
        +-------------------------+
        |                         |
        +---- repeated rounds ----+
        |
        v
final kernel
        |
        v
NVIDIA evaluation
        |
        v
#1 on B200
SOL 0.588237
```

## What this does and does not establish

This is one kernel on one hardware target.

It does not establish that this research structure is generally better than a single autonomous agent.

It also does not establish that Active Model could not eventually have reached #1 unaided; that counterfactual was not run.

What happened here is narrower and directly measurable:

**Active Model independently reached approximately #2-level performance with two separate solutions. Repeated maximum-effort reasoning rounds over those solutions generated additional research directions. Active Model converted those directions into implementations and hardware experiments, and the resulting loop eventually produced an NVIDIA-measured #1 result with a SOL score of 0.588237.**

The implementation and performance-critical details remain private while the benchmark is actively contested.
