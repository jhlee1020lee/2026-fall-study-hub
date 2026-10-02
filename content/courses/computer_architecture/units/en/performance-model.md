---
title: "Execution Time and Performance Models"
description: "Calculate latency, CPU time, speedup, and Amdahl bounds."
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
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-15-lecture-05", "courses/computer_architecture/lectures/en/2026-09-29-lecture-05"]
---

Specify the work and time measure before comparing performance. Keep units in CPU-time calculations and use unchanged work to bound improvements.

## What latency and throughput measure

Functional correctness asks whether a processor executes instructions according to their specification. Performance asks how efficiently it performs that correct work. After separating these questions, specify the task and metric being measured. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 02:08]] [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 lecture notes]]

Latency is the time from a task's start to its completion, such as handling one network request or responding to a game keystroke. Throughput is the number of tasks completed per unit time, important for batches and aggregate connection completion rates. The bus/race-car analogy similarly distinguishes one journey's duration from the number of passengers transported. [CA M006 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-003) [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 05:26]]

As an illustrative case, suppose two processors continuously handle independent requests, each taking one second. Each request can still have one-second latency while aggregate throughput reaches two requests per second. With concurrency, throughput is not generally $1/latency$. Multiple cores also do not automatically divide one task's latency by their count. Conversely, improving a bottleneck's processing rate can affect total task time, so the metrics are not wholly unrelated. The increase/decrease wording at September 15 08:19 remains unclear; the relationships here follow the definitions. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 08:19]]

## Elapsed time and CPU time

For the same amount of work, expressing $Performance=1/Time$ makes shorter time correspond to higher performance. First identify which time is measured. Throughput comparisons likewise require consistent work and workload conditions. [CA M006 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-004)

| Time measure | Meaning |
|---|---|
| Elapsed or wall-clock time | Actual time from start to finish |
| User CPU time | CPU time executing program code |
| System CPU time | CPU time executing system code on the program's behalf |

The terminal image in [CA M006 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-005) illustrates `time yes hello`, repeatedly printing a string. It reports Real 1.260 s, User 0.002 s, and Sys 0.013 s. CPU time is therefore $0.002+0.013=0.015$ s, and the difference from elapsed time is $1.260-0.015=1.245$ s.

At September 15 13:07, the instructor attributes the long duration to terminal-output I/O. Those three values alone do not provide a complete breakdown of every cause of the 1.245-second difference. They are also a reading of the instructor's existing output, not a new execution or measurement of the command. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 13:07]] Report whether a measurement is CPU time or wall-clock time, and consider conditions such as the unloaded-system measurement recommended in the material.

## Multiplying instruction count, CPI, and clock period

A cycle is an interval defined by the processor's clock. CPI means cycles per instruction; IPC means instructions per cycle; MIPS means million instructions per second. CPI and IPC calculated from totals for the same execution are reciprocals. GHz means $10^9$ cycles/s, not instructions/s.

The CPU execution-time equation is: [CA M006 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006)

$$
T_{CPU}=IC\times CPI_{avg}\times T_{clk}
=\frac{IC\times CPI_{avg}}{f_{clk}}.
$$

Canceling units exposes the relationship:

$$
\frac{instructions}{program}
\times\frac{cycles}{instruction}
\times\frac{seconds}{cycle}
=\frac{seconds}{program}.
$$

For an illustrative execution of $10^9$ instructions at average CPI 2 and a 2 GHz clock, time is $10^9\times2/(2\times10^9)=1$ second. I/O waiting is not automatically included. A clock of $g$ GHz has period $1/(g\times10^9)$ seconds; a rate of $m$ MIPS has average instruction time $1/(m\times10^6)$ seconds. Restore these multipliers when reading the slides' shorthand “1/GHz” and “1/MIPS.”

### Different choices affect the three factors

Arithmetic, memory, and branch instructions can have different costs, making instruction mix affect average CPI. September 15 16:05 compares register-centered operations with memory access to motivate this distinction, without establishing an unconditional ordering for every operation. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 16:05]]

| Factor | Influences identified by the material |
|---|---|
| Clock frequency | Semiconductor technology, microarchitecture |
| CPI | Microarchitecture, ISA |
| IC | ISA, compiler |

A compiler can change instruction count and memory accesses for the same C source. Different implementations can execute the same instruction sequence with different CPI. Neither GHz alone nor source-code length determines execution time. The claim about a “poor design” having smaller CPI at 17:56 conflicts with the equation's direction. **At fixed IC and frequency, reducing CPI reduces time** is an equation-based explanation, not a rewritten transcript quotation. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 17:56]]

The reasoning in recalled Q11(a–b) reverses this same equation. Multiply time by frequency to obtain total cycles, then divide by IC to obtain CPI. A target requires $CPI_{target}=T_{target}f_{new}/IC$. [EX:ca_2025_2_midterm_q11 p.3] The document actually prints an instruction count of “200 billion”; do not silently change its scale to force an expected answer. This is a Fall 2025 reconstruction, not independently verified official wording or answers.

## Speedup and percentage time reduction

“X is $n$ times faster than Y” means, for the same work,

$$
\frac{Performance_X}{Performance_Y}
=\frac{Time_Y}{Time_X}=n.
$$

A claim of “$m\%$ faster” gives performance ratio $1+m/100$. Establishing numerator and denominator first separates increased performance from reduced time. [CA M006 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-010)

In the source example, X takes one second and Y is 50% faster than X. Y therefore takes $1/1.5=2/3\approx0.66667$ seconds. A duration of 0.5 seconds instead represents a 50% time reduction, speedup 2, and a 100% performance increase. The instructor's correction from “times” to “percent” at September 15 27:22 connects to this distinction. The performance ratio 1.5 is dimensionless. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 27:22]]

An enhancement's speedup is similarly $T_{old}/T_{new}$. The improved version's shorter time belongs in the denominator, so an effective improvement gives a ratio above one. If the versions perform different work, the ratio alone no longer establishes how much faster the same task finishes. [CA M006 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-011)

## Amdahl's Law and the work that remains unchanged

Improving only part of a program leaves other execution time unchanged. Let $f$ be the fraction of **original execution time** affected by an enhancement and $S_f$ its speedup. The upper bar in [CA M006 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-012) contains $1-f$ and $f$; the lower retains $1-f$ while shrinking $f$ to $f/S_f$.

$$
T_{new}=T_{old}\left((1-f)+\frac{f}{S_f}\right),
\qquad
S_{overall}=\frac{1}{(1-f)+f/S_f}.
$$

For an illustrative $f=0.8$ and $S_f=4$, the remaining fraction is $0.2+0.8/4=0.4$, giving overall speedup 2.5. Even an infinitely fast enhancement leaves the unchanged 0.2, limiting speedup to 5. Generally, for $f<1$, the upper bound is $1/(1-f)$. Improving a small fraction has limited total effect; this does not make $S_f$ disappear from the equation. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 29:17]]

The reasoning connected to recalled Q6 and Q11(c) begins by bounding unaffected work. [EX:ca_2025_2_midterm_q06 p.2] [EX:ca_2025_2_midterm_q11 p.3] An instruction-**count** fraction $p$ is not automatically the execution-**time** fraction $f$. If the unaffected instructions have CPI $C_u$, their CPU time alone is

$$
T_{unaffected}=\frac{IC(1-p)C_u}{f_{clk}}.
$$

A target shorter than this cannot be met even by eliminating the affected work. Otherwise, the affected part's original cost and achievable improvement still matter. This is a derivation from the CPU-time equation, not reproduction of a complete private exam answer.

The pipeline remarks at September 15 30:18 and September 29 51:38 motivate later designs that use idle stages. They establish neither a general reduction in individual memory-access latency nor completed teaching of detailed hazard handling. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 30:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 51:38]]

## Reading energy and power together

Short execution time does not establish superiority under every processor-evaluation criterion. Finishing sooner may consume more energy; accepting a longer duration may reduce energy.

$$
Power_{avg}=\frac{Energy}{Time}.
$$

As an illustration, two executions each consume 10 J, one over one second and the other over two seconds. Their average powers are 10 W and 5 W. Lower power does not by itself mean lower total energy. Evaluation can consider a function of energy and time, together with implementation cost, reliability, and security. [CA M006 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-007)

At September 15 19:47, heavy workloads motivate the importance of energy, while the course's immediate performance focus remains time and throughput. Detailed energy modeling is only introduced in the material; product anecdotes are not treated as verified efficiency comparisons. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 19:47]]

## Key Takeaways

- With concurrency, throughput need not equal 1/latency.
- CPU time=IC×CPI/frequency and is distinct from elapsed time.
- '50% faster' divides time by 1.5; it does not halve time.
- Amdahl's f is an original-time fraction; unaffected work sets a lower bound.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Correctness, latency, throughput

Which criterion is met by a correct but slow processor? Two independent processors each take one second per request and stay busy: find latency/throughput and relate them to interactive/batch work.

<details><summary>Show solution</summary>

Executing the specification satisfies functional correctness. Each request has one-second latency, while ideal aggregate throughput is two requests/s. Interactive response emphasizes latency; batch processing emphasizes completion rate. Concurrency breaks a universal reciprocal relation, and extra cores do not automatically divide one task. A bottleneck component's rate can still affect total latency, so the metrics are not wholly unrelated.

**Checking points:** Distinguish one-request time from the aggregate completion rate.

</details>

#### Recall Q02 · Elapsed time and CPU usage

The source's `time yes hello` reports Real=1.260 s, User=0.002 s, Sys=0.013 s. Calculate CPU time and the difference, state what this establishes, and specify comparison conditions.

<details><summary>Show solution</summary>

CPU time is 0.015 s and the difference is 1.245 s. User time runs program code; system time runs system code on its behalf; elapsed time spans start to finish. The lecture attributes the long duration to output I/O, but these totals alone do not apportion every cause of the difference. Match work/workload, identify the time measure, and consider the material's unloaded-system condition before using Performance=1/Time. This reads existing output, not a new run.

**Checking points:** Do not assign the entire difference to one unmeasured cause.

</details>

#### Recall Q03 · IC, CPI, and clock units

For IC=10^9, CPI=2, and 2 GHz, calculate CPU time, clock period, IPC, and MIPS. Which factors are influenced by compiler, ISA, microarchitecture, and technology?

<details><summary>Show solution</summary>

Time is 10^9×2/(2×10^9)=1 s, period 0.5 ns, IPC 0.5, and rate 10^9 instructions/s=1000 MIPS. Instruction×cycles/instruction×seconds/cycle cancels to seconds. Technology/microarchitecture influence frequency; microarchitecture/ISA influence CPI; ISA/compiler influence IC. Instruction mix changes average CPI. GHz counts cycles, not instructions. At fixed IC and frequency, lower CPI reduces time; the equation does not automatically include I/O waits.

**Checking points:** Check GHz/MIPS scale factors and that CPI/IPC refer to the same execution.

</details>

#### Recall Q04 · Energy and power

Two executions of the same work each use 10 J and take one and two seconds. Compute average power and explain why low power or short time alone cannot settle every comparison.

<details><summary>Show solution</summary>

Average powers are 10 W and 5 W. The second has lower power but equal energy and longer latency. Designs may trade energy for time or vice versa. Objectives can involve both energy and time, implementation cost, reliability, and security. These observations do not constitute a detailed energy model or a measured brand comparison.

**Checking points:** Distinguish joules from watts and equal energy from equal power.

</details>

#### Recall Q05 · Faster versus reduced time

Against a one-second baseline, compare 50% faster with 50% less time. Give time, speedup, and performance increase for each.

<details><summary>Show solution</summary>

50% faster means ratio 1.5, time 2/3 s, speedup 1.5, and about 33.33% less time. A 50% time reduction gives 0.5 s, speedup 2, and a 100% performance increase. Speedup is old/new time for identical work; the ratio 1.5 is dimensionless.

**Checking points:** Check the ratio direction and distinguish the two percentage measures.

</details>

#### Recall Q06 · Amdahl's equation and bound

Derive overall speedup when fraction f of original time is sped up by S_f. Calculate f=0.8, S_f=4 and the infinite-improvement bound for f=0.1.

<details><summary>Show solution</summary>

Normalize old time to one: unchanged 1−f plus improved f/S_f remains, giving S=1/((1−f)+f/S_f). The first case yields 2.5 with upper bound 5. For f=0.1 the bound is 1/0.9≈1.111. Fraction f measures original time; a small affected fraction limits benefit without eliminating S_f from the formula.

**Checking points:** Include original-time weighting, unchanged work, and the limiting case.

</details>

#### Recall Q07 · Count fraction versus time fraction

Does improving 20% of instructions imply Amdahl f=0.2? Express unaffected-time bound and target CPI using IC, unaffected CPI C_u, count fraction p, and frequency f_clk.

<details><summary>Show solution</summary>

Instruction costs can differ, so count fraction is not time fraction. Unaffected cycles equal IC(1−p)C_u and time equals IC(1−p)C_u/f_clk. A target below that time is impossible even if affected work vanishes. Required average CPI is T_target f_clk/IC. Being above the bound is not alone proof of feasibility; original affected cost and achievable improvement are still needed.

**Checking points:** Convert counts into cycles before time and test the bound first.

</details>

### Apply the ideas

#### Practice P01 · Choose an improvement and reject an impossible target

Newly written synthetic practice. The same 80-million-instruction execution has 25% FP by count at CPI 4; all others have CPI 1. Clock is 2 GHz. Option A accelerates only FP fourfold; B changes only the clock to 2.8 GHz. Compute baseline and both options' times/speedups, then assess FP-only targets of 0.025 s and 0.04 s.

Connection: inverse timing and unaffected-work bounds from [EX:ca_2025_2_midterm_q11 p.3] (a–c), plus partial-improvement limits from [EX:ca_2025_2_midterm_q06 p.2], become a design-choice problem. Prerequisites: Q03, Q05–Q07. The original's printed 200 billion is retained; these numbers and choices are newly written.

<details><summary>Show solution</summary>

Baseline cycles are 20 million×4+60 million×1=140 million, taking 0.07 s. FP consumes 0.04 s, so its time fraction is 4/7, not 1/4. A takes 0.04/4+0.03=0.04 s (speedup 1.75); B takes 140 million/2.8 billion=0.05 s (speedup 1.4). A is faster under these premises. The unchanged 0.03 s makes 0.025 s impossible; its target CPI is 0.625, below the unaffected contribution 0.75. For 0.04 s, FP may occupy 0.01 s, requiring 0.04/0.01=4× improvement. Energy and cost are unspecified, so this does not rank every design criterion.

**Checking points:** Check count/time fractions, both options, and both target-feasibility decisions.

</details>

### Short review plan

Check Q02–Q03's units and time measures, then solve Q05–Q07. In P01, practice deciding feasibility before calculating the required improvement.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes · pipeline motivation only]]
- [lec 04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-007), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-012)
- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 corrected transcript]] — 02:08, 05:26, 08:19, 13:07, 16:05, 17:56, 19:47, 27:22, 29:17, 30:18 (plain timestamps within the page)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 corrected transcript]] — 51:38 (plain timestamps within the page)

The principal evidence is September 15. Unclear latency direction at 08:19, CPI direction at 17:56, and wording/units at 27:22 are distinguished using definitions and equations, not recovered speech. September 29 adds only the idle-stage motivation; it establishes neither detailed pipelines nor reduced individual memory latency. Energy coverage is introductory, and product anecdotes are not comparative evidence.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q06 p.2], [EX:ca_2025_2_midterm_q11 p.3].
- [[exam_questions/ca_2025_2_midterm_q11|2025-2 midterm reconstruction Q11 · existing question preview]]
Recalled Q11 prints IC as 200 billion; its scale is not silently changed.
