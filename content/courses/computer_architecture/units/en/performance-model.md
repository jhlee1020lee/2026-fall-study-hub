---
title: "Execution Time and Performance Models"
description: "Evaluate performance claims using latency, CPU time, speedup, and Amdahl's limits."
course: "computer_architecture"
unit_id: "performance-model"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 04.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-15-lecture-05"]
---

First specify which time or throughput metric compares the same correct work. Align IC, CPI, and clock units and isolate unaffected time to test speed claims and partial-optimization targets.

## Functional correctness, latency, and throughput

A processor must first execute instructions according to their specification: functional correctness. Performance evaluates how efficiently it performs that correct work. Building on the [ISA–implementation distinction](architecture-contract.md), comparing two implementations requires specifying the metric. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 02:08]]

Latency is the time from the start of one task to its completion: a game's input response or one server request, for example. Throughput is the number of completed tasks per unit time, important for batch work and concurrent server connections. The bus-versus-race-car analogy similarly distinguishes one journey's duration from passenger-carrying capacity. [[page_cache/computer_architecture/lec.04/page-003|CA M006 p.3]]

With concurrency, throughput is not generally `1/latency`. As an illustrative model, two independent processing units, each taking one second per task and continuously supplied with work, have one-second task service latency but aggregate throughput of two tasks per second. More cores do not automatically reduce one task's execution time proportionally. Nor are the metrics wholly unrelated: improving a bottleneck can affect completion time. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 05:26]] The increase/decrease wording about latency at 08:19 remains unclear; these definitions are not presented as recovered speech.

## Elapsed time and CPU time

For the same completed work, `Performance=1/Time` makes shorter time correspond to higher performance. First specify **which time** is measured. The Unix `time` example distinguishes:

| Metric | What it measures | Source value |
|---|---|---|
| Elapsed or wall-clock time | Actual time from start to finish | 1.260 s |
| User CPU time | CPU time executing program code | 0.002 s |
| System CPU time | CPU time executing system code for the program | 0.013 s |

The terminal output in [[page_cache/computer_architecture/lec.04/page-005|CA M006 p.5]] gives CPU time `0.002+0.013=0.015 s`. The difference from elapsed time is `1.260−0.015=1.245 s`. The lecturer explained the repeated terminal output as an I/O-heavy example in which elapsed time greatly exceeds CPU time. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 13:07]]

These three counters do not provide an exhaustive decomposition of every cause of the difference. They do establish that all 1.260 seconds should not be labeled CPU computation. Report measurement target and conditions; the material recommends measuring wall-clock time on an unloaded system.

## Constructing CPU time from IC, CPI, and clock

Instruction count (IC) counts instructions actually executed. CPI is average cycles per instruction; IPC is instructions per cycle, its reciprocal for the same aggregate. Clock frequency is cycles per second.

$$
T_{\mathrm{CPU}}=IC\times CPI\times t_{\mathrm{cycle}}
=\frac{IC\times CPI}{f_{\mathrm{clock}}}.
$$

The units explain the equation:

$$
\frac{\mathrm{instructions}}{\mathrm{program}}
\times\frac{\mathrm{cycles}}{\mathrm{instruction}}
\times\frac{\mathrm{seconds}}{\mathrm{cycle}}
=\frac{\mathrm{seconds}}{\mathrm{program}}.
$$

For an illustrative `10^9` instructions, CPI=2, and frequency=2 GHz, execution takes `10^9×2/(2×10^9)=1 s`. This is modeled CPU execution time, not automatically elapsed time including I/O waits.

GHz means `10^9 cycles/s` and MIPS means `10^6 instructions/s`. A frequency of `g GHz` therefore has cycle time `1/(g×10^9) s`, and `m MIPS` corresponds to average instruction time `1/(m×10^6) s`. The shorthand `1/GHz` and `1/MIPS` on [[page_cache/computer_architecture/lec.04/page-006|CA M006 p.6]] omits scale factors that must be restored for calculations in seconds.

| Factor in the time equation | Influences identified in the material |
|---|---|
| Frequency | Semiconductor technology, microarchitecture |
| CPI | Microarchitecture, ISA |
| IC | ISA, compiler |

Arithmetic, memory, and branch instructions can have different costs, so instruction mix affects average CPI. Compiler choices can change IC for the same source; different implementations can change CPI for the same sequence. Neither GHz alone nor source-code length determines execution time. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 16:05–18:54]] The unclear “smaller” CPI wording for poor design at 17:56 conflicts with the equation's direction. Holding IC and frequency fixed, lower CPI reduces time; that is an explicit equation-based correction.

For a demand such as recalled Q11(a–b), where time is known and the required CPI is sought, rearrange the same equation: `CPI=T×f_clock/IC`. Check for cycles/instruction and retain the numbers actually printed rather than replacing an unfamiliar scale. The recalled source is not a verified official paper or answer key. [EX:ca_2025_2_midterm_q11 p.3]

## Distinguishing time, energy, and power

A shorter execution time does not make a processor better in every respect. It may use more energy to finish sooner, or execute more slowly while consuming less energy. Average power is:

$$
P_{\mathrm{avg}}=\frac{E}{T}.
$$

As an illustrative calculation, using the same 60 J over 10 seconds gives 6 W; over 5 seconds it gives 12 W. Time halves, total energy stays constant, and average power doubles. These are three different quantities. The material introduces evaluations involving both energy and time, alongside implementation cost, reliability, and security. [[page_cache/computer_architecture/lec.04/page-007|CA M006 p.7]]

This is bounded materials-based background on comparison criteria. The lecture focuses on time and throughput rather than developing a detailed energy model. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 19:47]]

## Speedup and the direction of “50% faster”

For the same work, “X is n times faster than Y” means:

$$
\frac{Performance_X}{Performance_Y}
=\frac{T_Y}{T_X}=n.
$$

“m% faster” makes this performance ratio `1+m/100`. In the source example, X takes one second and Y is 50% faster:

$$
T_Y=\frac{1}{1.5}\ \mathrm{s}\approx0.66667\ \mathrm{s}.
$$

It does not take 0.5 seconds. Half the original time would mean twice the performance, or a 100% performance increase, even though time decreased by 50%. [[page_cache/computer_architecture/lec.04/page-010|CA M006 p.10]] [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 27:22]]

Improvement speedup is likewise `T_old/T_new`. A beneficial improvement has a smaller denominator and speedup greater than one. A performance ratio such as 1.5 is dimensionless; a duration is measured in seconds. Unclear spoken wording that mixes these must not become a numerical rule.

## Amdahl's Law and the unaffected time

When only part of a program becomes faster, its share of the original execution time matters. Let `f` be that original-time fraction and `S_f` the speedup of that part.

![Original Amdahl diagram separating unchanged and accelerated time](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.04/page-012.png)

The upper bar in [[page_cache/computer_architecture/lec.04/page-012|CA M006 p.12]] contains `1−f` and `f`. In the lower bar, `1−f` remains unchanged while `f` shrinks to `f/S_f`:

$$
T_{\mathrm{new}}=T_{\mathrm{old}}\left((1-f)+\frac{f}{S_f}\right),
\qquad
S_{\mathrm{overall}}=\frac{1}{(1-f)+f/S_f}.
$$

Applying the source equation illustratively with `f=0.8` and `S_f=4` leaves time fraction `0.2+0.8/4=0.4`, giving overall speedup 2.5. Even infinite acceleration of that part leaves, for `f<1`:

$$
S_{\mathrm{overall}}\le\frac{1}{1-f}
$$

The example's upper bound is 5 because the unaffected 20% remains. If only 10% can be eliminated, the bound is `1/0.9≈1.11`. “Make the common case fast” means improving what occupies substantial total time; it does not literally remove `S_f` from the equation when `f` is small. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 29:17]] Recalled Q6 also demands distinguishing partial improvement from its overall effect. [EX:ca_2025_2_midterm_q06 p.2]

### Converting instruction-count fractions into time fractions

Amdahl's `f` is an **original execution-time fraction**. If a class constitutes fraction `q` of instructions, differing instruction costs mean its time fraction need not equal `q`. With class CPIs `c_a,c_b` under a common clock:

$$
f=\frac{q\,c_a}{q\,c_a+(1-q)c_b}.
$$

Furthermore, the unaffected class alone requires:

$$
T_{\mathrm{unaffected}}=\frac{IC(1-q)c_b}{f_{\mathrm{clock}}}
$$

If that exceeds a target time, no acceleration of the other class can meet the target. Checking this lower bound first avoids searching for an impossible speedup factor. This is the reasoning transferred from recalled Q11(c); it does not require adding floating-point implementation details to the current syllabus. [EX:ca_2025_2_midterm_q11 p.3] Establishing what a weight measures is equally central to [workloads and performance averages](performance-comparison.md).

## Key Takeaways

- Compare the same functionally correct work using the same metric.
- Elapsed time can differ from user plus system CPU time.
- CPU time is `IC×CPI/frequency`; retain GHz and MIPS scale factors.
- '50% faster' means a performance ratio of 1.5, not halved time.
- Amdahl weights original time. If unaffected time exceeds the target, accelerating the other part cannot suffice.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Correct work and two metrics

Does a processor producing wrong results faster improve the performance of the correct task? With two independent units each taking one second per request and continuous work supply, calculate latency/throughput and explain whether they are reciprocals.

<details><summary>Show solution</summary>

Functional correctness comes first: wrong results do not complete the same correct task. Each request's service latency is one second; aggregate throughput is two requests/s. Concurrency makes that different from `1/latency=1/s`. Extra cores do not automatically shorten one task, though bottleneck changes can affect completion time, so the metrics are not wholly unrelated.

**Checking points:** State correctness, one second, two per second, and the concurrency condition.

</details>

#### Recall Q02 · Which time was measured?

Using Real=1.260 s, User=0.002 s, and Sys=0.013 s, compute CPU time and the difference. Define the counters and explain why the entire difference cannot be assigned to one cause from these values alone.

<details><summary>Show solution</summary>

CPU time is `0.002+0.013=0.015 s`; the difference is `1.260−0.015=1.245 s`. Real measures elapsed time, User CPU time in program code, and Sys CPU time in system code on its behalf. Terminal output motivates an I/O-heavy example, but these counters do not measure every waiting cause separately. Report time type, workload, and environment, including the materials' unloaded-system condition.

**Checking points:** Check both calculations, all three definitions, and attribution limits.

</details>

#### Recall Q03 · Reconstruct time from units

For IC=`10^9`, CPI=2, and clock=2 GHz, compute CPU time, cycle time, and IPC. Find average instruction time at 500 MIPS and required CPI for a 0.75-second target at the same IC/clock.

<details><summary>Show solution</summary>

Total cycles are `2×10^9`, time is `2×10^9/(2×10^9)=1 s`, cycle time is `1/(2×10^9)=0.5 ns`, and IPC is `1/2=0.5`. At 500×10^6 instructions/s, instruction time is 2 ns. Required CPI is `0.75×2×10^9/10^9=1.5 cycles/instruction`. Units cancel to seconds; this CPU model does not automatically include I/O waits.

**Checking points:** Check scale factors, reciprocals, inverse calculation units, and CPU versus elapsed scope.

</details>

#### Recall Q04 · Why GHz alone is insufficient

Connect compiler, ISA, microarchitecture, and semiconductor technology to the three time factors. Explain compiler IC reduction, changing instruction mix, and the meaning of lower CPI at a fixed clock.

<details><summary>Show solution</summary>

The material connects IC to ISA/compiler, CPI to microarchitecture/ISA, and frequency to technology/microarchitecture. Compilers can change sequence length and mix; changing proportions of differently priced instructions changes average CPI. Lower CPI reduces time at fixed IC/frequency, but simultaneous changes require evaluating the full equation. Source-line count or GHz alone omits needed information.

**Checking points:** State influences on all three factors and the hold-other-factors-fixed condition.

</details>

#### Recall Q05 · Energy and power

Two runs each use 60 J and take 10 seconds and 5 seconds. Compare average power, total energy, and time; does shorter time imply superiority on every criterion?

<details><summary>Show solution</summary>

Average powers are `60/10=6 W` and `60/5=12 W`. Time halves, energy stays equal, and power doubles. Slower execution may be chosen for energy savings; cost, reliability, and security also matter. The average relation does not specify a detailed energy model or rank every criterion.

**Checking points:** Check J/s/W units and all three comparisons.

</details>

#### Recall Q06 · Faster versus time reduction

For a one-second task, find the new time for 50% faster performance. Then give speedup, performance increase, and time reduction if the new time is 0.5 seconds.

<details><summary>Show solution</summary>

50% faster means ratio 1.5, giving `Tnew=1/1.5=2/3 s`. At 0.5 seconds, speedup is `1/0.5=2`, performance increase is `(2−1)×100=100%`, and time reduction is `(1−0.5)/1=50%`. Ratios are dimensionless, durations have seconds, and inverse-time comparison assumes the same work.

**Checking points:** Distinguish ratio direction, 2/3 second, 2×, 100%, and 50%.

</details>

#### Recall Q07 · Amdahl's remaining time

If 80% of original time is accelerated fourfold, what time fraction and overall speedup remain? Explain the infinite-acceleration limit and the limit when only 10% can improve.

<details><summary>Show solution</summary>

`Tnew/Told=(1−0.8)+0.8/4=0.4`, giving speedup 2.5. The unaffected 20% leaves limit 5, which finite acceleration cannot exceed. Eliminating only 10% leaves limit `1/0.9≈1.111`. The fraction is original time; a small fraction limits the effect without removing the partial speedup from the equation.

**Checking points:** Separate fixed and shrinking time and verify all three ratios.

</details>

#### Recall Q08 · Instruction share versus time share

Of 100 instructions, class A has 20 at CPI 4 and class B 80 at CPI 1, under one clock. Calculate A's instruction/time shares and overall CPI, then give the cycle lower bound if only A improves.

<details><summary>Show solution</summary>

A consumes 80 cycles and B 80, totaling 160, so overall CPI is 1.6. A has instruction share 0.2 but time share `80/160=0.5`. Even eliminating A's time leaves B's 80 cycles. Substituting count share 0.2 into Amdahl ignores unequal class costs.

**Checking points:** Distinguish 20%/50% and check 160 cycles, CPI 1.6, and the 80-cycle bound.

</details>

### Apply and diagnose

#### Practice P01 · Feasible and infeasible targets

Newly written synthetic practice transfers inverse CPI and the fixed-time bound from [EX:ca_2025_2_midterm_q11 p.3] (a–c), plus partial-improvement reasoning from [EX:ca_2025_2_midterm_q06 p.2]. Prerequisites are the taught CPU model and count-to-time conversion. IC=`2×10^9`, clock=2 GHz; A is 25% of instructions at CPI 6, B 75% at CPI 2. Hold IC, clock, and B fixed while accelerating only A. Find original time/CPI, required average CPI and A speedup for 1.8 seconds, and feasibility of 1.2 seconds. Can finite speedup reach 1.5 seconds?

<details><summary>Show solution</summary>

Original average CPI is `0.25×6+0.75×2=3`, so time is three seconds. A and B each consume 1.5 seconds: A's time share is 50%, not 25%. The 1.8-second target requires average CPI `1.8×2×10^9/(2×10^9)=1.8`. Solving `1.5+1.5/S=1.8` gives S=5 and A CPI=6/5=1.2; overall speedup is 3/1.8=5/3. B alone takes 1.5 seconds, ruling out 1.2. Exactly 1.5 seconds requires zero A time, approached only as S tends to infinity in this model.

**Checking points:** Check count/time shares, inverse calculation, partial/overall speedup, impossibility, and the asymptotic limit.

</details>

### Review plan

Use Q01–Q02 to identify the metric and Q03–Q06 to check units and ratio direction. Start Q07–Q08 and P01 with unaffected time, then carry weight interpretation into [[courses/computer_architecture/units/en/performance-comparison|workloads and means]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 · lecture notes]]

- [lec.04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf): [[page_cache/computer_architecture/lec.04/page-003|p.3]], [[page_cache/computer_architecture/lec.04/page-004|p.4]], [[page_cache/computer_architecture/lec.04/page-005|p.5]], [[page_cache/computer_architecture/lec.04/page-006|p.6]], [[page_cache/computer_architecture/lec.04/page-007|p.7]], [[page_cache/computer_architecture/lec.04/page-010|p.10]], [[page_cache/computer_architecture/lec.04/page-011|p.11]], [[page_cache/computer_architecture/lec.04/page-012|p.12]]

- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT · 02:08, 05:26, 08:19, 13:07, 16:05–18:54, 19:47, 27:22, 29:17]]

- September 15 latency direction at 08:19 and CPI wording at 17:56 remain unclear. Explanations follow definitions/equations, not recovered speech.
- Three timing counters do not fully decompose the elapsed-minus-CPU difference. Energy/power is materials-based background, not a detailed taught energy model.
- The pipeline preview at 30:18 does not establish taught datapath design or guaranteed reduction of individual memory latency.
- Retain Q11's printed 200 billion instructions. New exercise numbers are separate conditions; FP instruction implementation is not part of the transfer.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.

- [[exam_questions/ca_2025_2_midterm_q11|Existing question preview · Q11]]


---

[[courses/computer_architecture/units/en/procedures-stack|← Previous: Procedure Calls, Calling Conventions, and the Stack]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/performance-comparison|Next: Workloads, Means, and Performance Comparison →]]
