---
title: "Workloads, Means, and Performance Comparison"
description: "Aggregate runtimes, normalized ratios, and IPC using explicit workloads and weights."
course: "computer_architecture"
unit_id: "performance-comparison"
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

Identify whether you are combining amounts, ratios, or rates before averaging results. State weight meanings and ratio directions to see why AM, GM, and HM answer different questions about the same measurements.

## Workloads determine what a comparison means

Being able to calculate [CPU execution time and speedup](performance-model.md) does not establish which usage scenario the result represents. A workload combines applications and amounts of execution. Computer X can be faster on application A without being faster by the same factor on B, and Y may win on C. Different proportions of games, AI, or other research work can change a user's overall comparison of the same machines. [[page_cache/computer_architecture/lec.04/page-013|CA M006 p.13]] [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 31:13–33:15]]

Before summarizing several results, identify what is being combined: amounts such as runtime, ratios relative to a reference machine, or rates per unit time or cycle. Start with the total quantity and its denominator rather than choosing a named mean first.

## Arithmetic means and execution-count weights

The arithmetic mean (AM) of `n` runtimes is:

$$
AM(T)=\frac{1}{n}\sum_{i=1}^{n}T_i.
$$

If each application is executed equally often, comparing AMs is equivalent to comparing total runtime. With the same workload on both machines, `AM_X/AM_Y` is Y's speedup over X. Longer applications contribute more because the quantity being summed is time. That is not automatically an error. The problem arises when an **equal-run-count assumption** fails to represent actual use, such as running short applications far more often. [[page_cache/computer_architecture/lec.04/page-014|CA M006 p.14]]

Let `w_i` be the fraction of executions belonging to application `i`, with weights summing to one. The weighted arithmetic mean (WAM) is:

$$
WAM(T)=\sum_i w_iT_i,\qquad \sum_iw_i=1.
$$

As an illustrative workload, run a one-second application nine times and a ten-second application once. Total runtime is `9×1+1×10=19 s` and average runtime `19/10=1.9 s/run`, equivalently `0.9×1+0.1×10=1.9`. Giving the two application types equal weight would produce 5.5 seconds and describe a different execution pattern. [[page_cache/computer_architecture/lec.04/page-015|CA M006 p.15]]

A weight is not a device for arbitrarily weakening large values. Here it measures **a fraction of application runs**. Applying the same weights to both machines is necessary to compare the same workload.

### CPI averages require instruction-count weights

CPI is total cycles divided by total instructions. If instruction class `i` has count `I_i` and CPI `c_i`:

$$
CPI_{\mathrm{all}}=
\frac{\sum_i I_ic_i}{\sum_i I_i}
=\sum_i\left(\frac{I_i}{\sum_jI_j}\right)c_i.
$$

The weights are instruction-count fractions. At 37:12 on September 15, the arithmetic-90%/movement-10% example used the words “of the time.” Those words are not rewritten here as an instruction-count claim. Time fractions cannot be inserted directly into this formula without establishing what was measured and the costs of the instruction classes. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 37:12]]

## Geometric means of normalized time ratios

When benchmark runtimes have different scales, first form a ratio to a reference machine. Define `r_i=T_Xi/T_Yi`. The geometric mean (GM) is:

$$
G=\left(\prod_{i=1}^{n}r_i\right)^{1/n}.
$$

It summarizes multiplicative changes in positive ratios. Illustrative ratios 0.5 and 2 have GM `sqrt(0.5×2)=1`, expressing a balance between half the time on one benchmark and twice the time on another. It does **not** establish equal total runtime. For example, Y taking 2 and 100 seconds and X taking 1 and 200 seconds yields those same ratios, but totals of 102 and 201 seconds.

The actual fraction on [[page_cache/computer_architecture/lec.04/page-016|CA M006 p.16]] is `Time_X/Time_Y`. Thus `G<1` indicates relatively shorter times for X. The same slide's “relative speedup” wording points in the opposite direction from X's previously defined speedup, `Time_Y/Time_X`. The correction is to distinguish **time ratio G from speedup direction 1/G**. A time-ratio GM of 0.8 corresponds to a speedup GM of `1/0.8=1.25`. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 39:09]]

GM has the property:

$$
\frac{GM(X_i)}{GM(Y_i)}=GM\left(\frac{X_i}{Y_i}\right).
$$

Normalizing the same benchmark set to a common reference `Z_i` gives `GM(X_i/Z_i)/GM(Y_i/Z_i)=GM(X_i/Y_i)`: the reference cancels. This requires the same comparisons and a consistent direction. It does not license ignoring execution frequencies or conclude that one machine wins on every task.

## Harmonic means from total work divided by total time

Construct an average rate as **total work/total time**. In the source example, travel the first 10 km at 30 km/h and the next 10 km at 90 km/h:

$$
v_{\mathrm{avg}}=
\frac{20}{10/30+10/90}
=\frac{20}{4/9}
=45\ \mathrm{km/h}.
$$

The segments take 1/3 hour and 1/9 hour. The slower equal-distance segment occupies three times as much time, explaining why the result is not the arithmetic mean of 60 km/h. [[page_cache/computer_architecture/lec.04/page-017|CA M006 p.17]]

For equal work `W` performed at positive rates `r_i`, each duration is `W/r_i`. Divide total work `nW` by the sum of durations to obtain the harmonic mean (HM). With work fractions `w_i` summing to one, the weighted harmonic mean (WHM) follows:

$$
HM(r)=\frac{n}{\sum_i1/r_i},
\qquad
WHM(r)=\frac{1}{\sum_iw_i/r_i}.
$$

These weights are **fractions of work**, not time fractions or unspecified importance. “Always use HM for rates” loses the condition. Traveling at 30 and 90 km/h for equal durations instead gives 60 km/h when total distance is divided by total time. What is held equal determines the formula.

## Aggregate IPC and its relationship to CPI

Aggregate IPC is total instructions divided by total cycles. If execution `i` processes `I_i` instructions at `CPI_i`:

$$
IPC_{\mathrm{all}}=
\frac{\sum_i I_i}{\sum_i I_iCPI_i}.
$$

When every execution has the same count `I`:

$$
IPC_{\mathrm{all}}=
\frac{nI}{\sum_i ICPI_i}
=\frac{1}{AM(CPI)}
=HM(IPC).
$$

[[page_cache/computer_architecture/lec.04/page-018|CA M006 p.18]] explains this using equal frequency and equal instruction count. Its “Avg. Time = Avg. CPI” shorthand omits the common factor `I/f_clock` and expresses proportionality, not equality of seconds with cycles/instruction. The unclear spoken derivation at 42:11 is distinguished from this total-quantity calculation. [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 42:11]]

For equal instruction counts at IPC 1 and 2, aggregate IPC is `2/(1+1/2)=4/3`, not 1.5. In another illustrative calculation, 100 instructions at CPI 1 and 100 at CPI 3 consume 100 and 300 cycles. Aggregate IPC is `200/400=0.5`; the arithmetic mean of individual IPCs 1 and 1/3 would incorrectly give 2/3.

For unequal counts, use `w_i=I_i/ΣI_i`, giving `IPC_all=1/Σ(w_i CPI_i)=1/Σ(w_i/IPC_i)`. This explains why recalled Q5 should prompt a distinction between **an actual aggregate processing rate** and **a summary of normalized benchmark ratios**, rather than selecting GM or HM merely because IPC appears in the wording. [EX:ca_2025_2_midterm_q05 p.2]

| Quantity being combined | Condition to establish | Appropriate expression |
|---|---|---|
| Runtime | Number of runs of each application | AM or run-count WAM |
| Normalized ratio | Same benchmark set, reference, and ratio direction | GM |
| Rate | Equal work or known work fractions | HM or WHM |

Numerators, denominators, and weights come before the names. A geometric mean of normalized rate ratios and the actual rate for all completed work are different statistics.

## Standard benchmarks and representative measurements

Because users care about different applications, standard benchmarks provide common workloads and comparison rules. The lecture introduced the SPEC benchmark collection as a shared basis for systems/architecture evaluation. The material describes applications selected by a cross-industry committee, updates as technology and use change, and an imperfect but useful common standard. [[page_cache/computer_architecture/lec.04/page-020|CA M006 p.20]] [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 44:10–45:07]]

The integer/floating-point suite list on M006 p.21 names programs, languages, and uses; it does not establish instruction on every program's operation. The learning point is that **a shared benchmark may not represent a particular user's workload**, rather than memorizing names. The slide's distribution wording also does not certify every benchmark's current license.

Report the measurement purpose, actual workload and execution amounts, type of time, environment and method, ratio direction, and weights. A 2× result for one application does not establish a universally 2× faster computer. If a single-number summary lacks justification, show individual results and make raw data available for interpretation. [[page_cache/computer_architecture/lec.04/page-022|CA M006 p.22]] [[courses/computer_architecture/transcripts/2026-09-15|September 15 STT, 46:06–48:47]] Readers need to know **what the result measures** to judge whether it applies to their workload.

## Key Takeaways

- Which applications run, and how often, determines the comparison.
- Runtime WAM uses execution-count weights; CPI WAM uses instruction-count weights.
- GM summarizes positive normalized ratios rather than total runtime.
- Derive rates from total work/total time: HM for equal work, WHM for known work fractions.
- Actual IPC is total instructions/total cycles, distinct from a GM of benchmark ratios.
- Common benchmarks do not perfectly represent individual use; inspect results and measurement conditions.

## Recall and Practice

### Recall and trace

#### Recall Q01 · What does the result represent?

A report gives X a speedup of 2 on one application. Why does this not imply twice the speed for every use? List information needed for readers to reinterpret the result.

<details><summary>Show solution</summary>

Other applications differ in instruction mix, bottlenecks, and execution amounts, potentially reversing rankings. Report purpose, applications/run counts, time type, environment/method, comparison baseline/direction, and the summary formula/weights. Show individual results and raw data when a single summary lacks representativeness. Describing workload establishes the result's scope.

**Checking points:** Explain workload dependence and concrete reporting details for interpretation.

</details>

#### Recall Q02 · Run-count weights for runtime

Run A=1 second nine times and B=10 seconds once. Compare total, per-run mean, and equal-type-weight mean. Under what conditions and in which direction can AM/WAM ratios be read as speedup?

<details><summary>Show solution</summary>

Total is 19 seconds and per-run mean 19/10=1.9 seconds, with weights 0.9/0.1. Equal type weights give `(1+10)/2=5.5`, describing another run pattern. AM compares totals when applications run equally often; WAM comparisons require identical run-count weights on both machines. `WAM_X/WAM_Y` is Y's speedup over X. A long run contributing more to total time is not itself an error.

**Checking points:** Check 19, 1.9, 5.5, weight meaning, common workload, and speedup direction.

</details>

#### Recall Q03 · What weights CPI?

Find aggregate CPI for 90 A instructions at CPI 1 and 10 B instructions at CPI 5. Can you use the same calculation if only told that A takes 90% of time?

<details><summary>Show solution</summary>

Total cycles are 90+50=140 and instructions 100, so CPI is 1.4. Weights 0.9/0.1 in `0.9×1+0.1×5` are instruction-count fractions. A's actual time share at one clock is 90/140=9/14, not 90%. Given time fractions, first establish their relation to counts rather than inserting them unchanged. The lecture's 'of the time' wording is not silently converted.

**Checking points:** Derive 140/100 and distinguish instruction from time weights.

</details>

#### Recall Q04 · GM direction versus totals

Y's two runtimes are 2 and 100 seconds, X's 1 and 200. Compare the GM of `T_X/T_Y` with totals. What is speedup GM when a separate time-ratio GM is 0.8? Does a common reference Z change the comparison?

<details><summary>Show solution</summary>

Ratios 0.5 and 2 have GM 1, while totals are Y=102 and X=201 seconds. GM summarizes multiplicative ratios. Time-ratio 0.8 corresponds to reciprocal speedup 1.25. For the same positive benchmark values, `GM(X/Z)/GM(Y/Z)=GM(X/Y)`, canceling Z. Keep the set/direction consistent; cancellation does not replace run frequencies or total runtime.

**Checking points:** Check GM 1 despite unequal totals, the 1.25 direction, and common-reference conditions.

</details>

#### Recall Q05 · Equal distance versus equal time

Find average speed for 10 km each at 30 and 90 km/h. Why does equal time at each speed differ? Then find work weights and WHM for 20 km at the first speed and 10 km at the second.

<details><summary>Show solution</summary>

For equal distance, `20/(10/30+10/90)=45 km/h`; durations are 1/3 and 1/9 hour, not equal, so AM 60 is wrong here. Equal durations t give distance `(30+90)t` over time 2t, hence 60. Work fractions for 20/10 km are 2/3 and 1/3, so `WHM=1/((2/3)/30+(1/3)/90)=270/7≈38.57 km/h`. These follow from total work/time under positive rates and work-fraction weights.

**Checking points:** Check 45, 60, 270/7, and which quantity is held equal in each case.

</details>

#### Recall Q06 · Derive aggregate IPC from totals

Two segments each execute 100 instructions at CPI 1 and 3. Find aggregate CPI/IPC; then change only the second count to 300. Why is p.18's Time=CPI not dimensional equality, and why is aggregate IPC different from GM of normalized ratios?

<details><summary>Show solution</summary>

With equal counts, cycles=100+300=400, CPI=400/200=2, and IPC=0.5. AM of individual IPCs, 2/3, is wrong; `1/AM(CPI)=HM(IPC)` applies. With the second count 300, cycles=100+900=1000, instructions=400, CPI=2.5, and IPC=0.4. Weight CPI by 1/4 and 3/4, then invert. Time is proportional to CPI through common factor I/f when count/frequency match. Actual IPC totals and a multiplicative summary of benchmark ratios answer different questions.

**Checking points:** Check totals/reciprocals for both count cases, CPI weights, dimensions, and rate versus ratio.

</details>

#### Recall Q07 · Use and limits of common benchmarks

Why are common benchmarks such as SPEC useful without representing every user's workload? Do these materials establish required suite-name memorization, current licensing, or individual-program behavior?

<details><summary>Show solution</summary>

Shared applications and rules make designs comparable and motivate updates as technology/use change. Different user execution mixes and bottlenecks can still separate a common score from actual experience. The suite list introduces names/uses, not detailed program behavior or current licenses. The lecture's learning point is the existence and limits of benchmark sets rather than name memorization.

**Checking points:** Separate common comparability from representativeness and retain the source limits.

</details>

### Apply and diagnose

#### Practice P01 · Do not choose a mean from the name IPC

Newly written synthetic practice transfers the rate/ratio distinction from [EX:ca_2025_2_midterm_q05 p.2]. Prerequisites are this unit's totals, weights, GM, and HM. X executes 100 instructions at IPC 1 for A and 300 at IPC 2 for B. Reference IPC is 1 for each benchmark. A report calculates the GM of normalized IPC ratios and labels it X's IPC over all completed work. Find actual IPC, appropriate weights, and GM, and diagnose the report. Is unweighted HM valid here?

<details><summary>Show solution</summary>

X uses 100/1=100 cycles for A and 300/2=150 for B, totaling 250. Aggregate IPC is 400/250=1.6, equivalently `1/((1/4)/1+(3/4)/2)` using work weights 1/4 and 3/4. Normalized ratios are 1 and 2, whose GM is `√2≈1.414`, a different statistic. Unweighted HM=`2/(1+1/2)=4/3` assumes equal instruction counts and does not describe this workload. Label GM as benchmark-relative change and report total-work IPC separately.

**Checking points:** Show 400/250, count weights, √2, and why unweighted HM's condition fails.

</details>

### Review plan

State workload and weights in Q01–Q03; derive numerators and denominators before naming means in Q04–Q06. Separate actual rate from normalized ratios in P01, then audit a short performance report using Q07. Revisit Q03 in [[courses/computer_architecture/units/en/performance-model|execution-time models]] if units are unclear.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 · lecture notes]]

- [lec.04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf): [[page_cache/computer_architecture/lec.04/page-013|p.13]], [[page_cache/computer_architecture/lec.04/page-014|p.14]], [[page_cache/computer_architecture/lec.04/page-015|p.15]], [[page_cache/computer_architecture/lec.04/page-016|p.16]], [[page_cache/computer_architecture/lec.04/page-017|p.17]], [[page_cache/computer_architecture/lec.04/page-018|p.18]], [[page_cache/computer_architecture/lec.04/page-019|p.19]], [[page_cache/computer_architecture/lec.04/page-020|p.20]], [[page_cache/computer_architecture/lec.04/page-022|p.22]]

- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT · 31:13–33:15, 37:12, 39:09, 42:11, 44:10–45:07, 46:06–48:47]]

- The words 'of the time' at September 15 37:12 are not rewritten as instruction-count evidence. CPI aggregation requires instruction-count weights.
- lec.04 p.16 uses `Time_X/Time_Y` while calling it relative speedup; distinguish the time ratio from reciprocal speedup.
- Time=CPI on p.18 omits the common I/f proportionality factor; it is not dimensional equality. Unclear spoken derivation at 42:11 remains unresolved.
- SPEC supplies background on common benchmarking. Individual suite behavior, name memorization, and current licensing are not established by this material. Retain transparent measurement principles without personal anecdotes.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.


---

[[courses/computer_architecture/units/en/performance-model|← Previous: Execution Time and Performance Models]] · [[courses/computer_architecture/units/index|Unit contents]]
