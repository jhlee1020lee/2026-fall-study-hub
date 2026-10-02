---
title: "Multi-cycle CPU Datapath, Control, and Performance"
description: "Connect the 50 ps FSM, MasterEn, ROM size, and workload performance."
course: "computer_architecture"
unit_id: "multicycle-datapath-control"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 06.pdf", "lec 03.pdf", "lec 05 typo fixed.pdf", "lec 04.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-29-lecture-05", "courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-10-lecture-04", "courses/computer_architecture/lectures/en/2026-09-15-lecture-05"]
---

Count the work on each instruction path and locate its completion boundary. Evaluate a shorter clock through CPI and instruction mix as well as frequency.

## Different instruction work under one common clock

Programmer-visible state (PVS) includes PC, architectural registers, and memory that determine program meaning. A single-cycle implementation computes the next state from current state and the instruction and completes the required updates at one clock boundary. The common cycle must therefore accommodate the longest supported instruction path. The September 29 multi-cycle discussion begins with the inefficiency of making shorter instructions wait for that boundary. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 04:01]] [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]

When reading [CA NM002 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-003)–[CA NM002 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-004), separate PC's **address**, the instruction's **bits**, and register **data**. The instruction is 32 bits, with `rs1=[19:15]`, `rs2=[24:20]`, `rd=[11:7]`, and `opcode=[6:0]`. Selected register values and the main datapath are 64 bits. The wording at 04:01 that PC stores the instruction conflicts with the wiring. The diagram-supported explanation is that PC provides the instruction-memory address.

| Stage | Work | Instruction-dependent distinction |
|---|---|---|
| IF | Read instruction bits | Arithmetic still needs fetch |
| ID | Decode and read register operands | The source's JAL timing case omits the register read |
| EX | Perform an ALU operation | Produce arithmetic data or a load/store address |
| MEM | Read or write data memory | Unnecessary for R/I arithmetic |
| WB | Write the destination register | Loaded data for a load; ALU result for arithmetic |

R/I-type **arithmetic** uses IF → ID → EX → WB; `lw` uses all five functions. I-type encoding does not by itself imply no MEM stage: a load can also use I-type. The repeated R-type wording at 04:56 is interpreted with the clarification at 06:49 and the slides to distinguish R/I arithmetic. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 04:56]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 06:49]]

Selecting register/immediate ALU input, selecting ALU/memory write-back data, and selecting PC+4/target are different mux responsibilities. Branch shift-left-1 concerns displacement encoding units, not doubling every immediate. The diagram supports a basic subset, not complete circuitry for all jump variants. [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034) Relevant representations connect to [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]], while branch and link semantics connect to [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes]].

## Calculating the longest path from component delays

[CA NM002 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005) assumes 200 ps for memory reads/writes, 100 ps for ALU addition, 50 ps for register-file reads/writes, and 0 ps for other combinational logic. September 29 07:50 explicitly presents this as a simplified example. The contradictory memory-size wording at 06:49 and actual memory latency remain separate from these assumptions. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 07:50]]

| Source instruction class | IF | ID | EX | MEM | WB | Total |
|---|---:|---:|---:|---:|---:|---:|
| R/I arithmetic | 200 | 50 | 100 | — | 50 | 400 ps |
| `lw` | 200 | 50 | 100 | 200 | 50 | 600 ps |
| `sw` | 200 | 50 | 100 | 200 | — | 550 ps |
| Bxx / JALR, omitted-WB condition | 200 | 50 | 100 | — | — | 350 ps |
| JAL, omitted-ID/WB condition | 200 | — | 100 | — | — | 300 ps |

The load's 600 ps includes separate 200 ps instruction-fetch and data-memory accesses. This subset requires a single-cycle period of at least 600 ps, giving the ideal maximum frequency

$$
f_{single}=\frac{1}{600\times10^{-12}\text{ s}}
\approx1.667\text{ GHz}.
$$

Although an R-type useful path takes 400 ps, the next common boundary is 600 ps away. The extra 200 ps is timing slack, not proof that arithmetic actually reads data memory.

### Discarding a jump link versus preserving it

The crossed-out WB entries are not universal branch/jump rules. A conditional branch may complete with only a PC update, but `jal/jalr` writing a return address to a destination other than `x0` loses an architectural effect if that register update is removed. September 29 08:47–09:40 explicitly qualifies omitted WB. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 08:47]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 09:40]]

Thus, the 350/300 ps values belong to the displayed paths that do not need to retain a link. The source supplies no complete additional state schedule for link-writing cases. Zero-cost muxes, wires, and control likewise simplify calculation rather than guarantee real timing.

## A 50 ps microcycle and MasterEn

The initial multi-cycle model divides 600 ps into 50 ps microcycles and uses only the required count for each instruction. IF needs four, ID one, EX two, MEM four, and WB one. R-type arithmetic takes eight microcycles or 400 ps; a load takes twelve or 600 ps. [CA NM002 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-006) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 12:25]]

Merely applying a faster clock is insufficient. Writing registers or memory on intermediate edges before computation settles can preserve incorrect values. MasterEn permits the appropriate PVS updates at the completion boundary of the instruction's sequence. The controller's state register still advances on intermediate microcycles.

MasterEn does not replace RegWrite or MemWrite. Instruction-specific controls determine **what to write**; MasterEn determines **when completed effects may be accepted** in this initial model. MasterEn=1 does not mean writing every register and memory location. [CA NM002 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-007) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 14:04]] At 13:11, a contradictory negation says an update cannot occur even with MasterEn=1. The explanation here follows the subsequent account and the figure's completion transitions, without claiming recovered speech. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 13:11]]

## Reading CPI from FSM paths

A finite-state machine (FSM) uses current state and inputs to determine next state and control. This example has twelve states: IF1–IF4, ID, EX1–EX2, MEM1–MEM4, and WB. Four IF states allocate the 200 ps fetch of one instruction; they do not fetch four separate instructions. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 15:55]]

![CA NM002 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-008.png)

Most arrows advance sequentially, while IF4, EX2, and MEM4 select paths according to instruction class. The red MasterEn=1 annotations label completion **transitions** back to IF1. They do not permit arbitrary continuous writing throughout IF1.

| Class | Microcycles counted along its path | CPI | Completion transition |
|---|---|---:|---|
| R/I arithmetic | 4 IF + 1 ID + 2 EX + 1 WB | 8 | WB → IF1 |
| `lw` | 4 IF + 1 ID + 2 EX + 4 MEM + 1 WB | 12 | WB → IF1 |
| `sw` | 4 IF + 1 ID + 2 EX + 4 MEM | 11 | MEM4 → IF1 |
| Bxx / JALR, omitted-WB condition | 4 IF + 1 ID + 2 EX | 7 | EX2 → IF1 |
| JAL, omitted-ID/WB condition | 4 IF + 2 EX | 6 | EX2 → IF1 |

JAL bypasses ID from IF4 to EX1. After EX2, arithmetic goes to WB, loads/stores to MEM1, and the displayed branch/jump paths to IF1. At MEM4, a load continues to WB while a store finishes. The table in [CA NM002 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-009) expresses the same FSM. Having twelve total states does not mean every instruction visits twelve states. Nor should the next instruction's IF1 be added to the previous instruction's CPI. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 18:48]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 22:23]]

This initial model describes a combinational path from PVS to the next PVS and its final update. Do not import PC-update timing from the later resource-reuse design that introduces IR and intermediate storage as though the two diagrams were one identical circuit.

## Inputs and outputs of a ROM microsequencer

Implementing the FSM as a lookup table uses current state and instruction class as inputs, and datapath control and next state as outputs. Twelve states require $\lceil\log_2 12\rceil=4$ bits. Four next-state outputs, NS3–NS0, feed the state register on the next clock and determine controller progress. They are distinct from an ALU result. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 20:43]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 21:41]]

The generic diagram in [CA NM002 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-010) uses six opcode bits and four state bits. Outputs include PCWrite, PCWriteCond, IorD, MemRead, MemWrite, IRWrite, MemtoReg, PCSource, ALUOp, ALUSrcA/B, RegWrite, RegDst, and next state. These names illustrate control over muxes, the ALU, and writes; they must not be transplanted into the current Lab1's signal specification.

Actual RISC-V opcode field `[6:0]` has seven bits. Keep the generic six-bit figure distinct from the incorrect six-bit RISC-V assertion at September 29 20:43. The depicted table has ten input bits and $2^{10}=1024$ rows. A hypothetical design using all seven raw RISC-V opcode bits and four state bits has $2^{11}=2048$ rows. Predecoding an instruction class would produce a different width again. [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034)

A complete ROM table with $n$ input bits and $m$ output bits stores $m2^n$ bits. For an illustrative $n=10,m=20$, capacity is 20,480 bits; adding one input yields 40,960 bits, while adding just one output yields 21,504 bits. Distinguish row count from row width. The spoken $n2^n$ at 34:04 conflicts with that distinction and is not adopted as the general formula. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 34:04]] Table capacity is also not a direct prediction of minimized PLA gate count or delay. Large tables and repeated next-state information motivate microcode decomposition.

## Comparing average execution time using an instruction mix

For the same binary and execution path, or an explicitly equal IC, $T=IC\times CPI_{avg}\times T_{clk}$. Merely sharing an ISA does not make arbitrary programs' IC equal. September 29 24:33 calls this wall-clock time under the assumption that one program consumes all machine cycles. In general settings with I/O, waiting, or concurrent work, retain the CPU-time/elapsed-time distinction explained in [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 lecture notes]]. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 24:33]] [CA M006 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006)

For instruction-count fractions $w_i$,

$$
\sum_iw_i=1,\qquad CPI_{avg}=\sum_iw_iCPI_i,
\qquad IPC_{avg}=\frac{1}{\sum_i(w_i/IPC_i)}.
$$

Here $IPC_i=1/CPI_i$, making aggregate IPC the weighted harmonic mean with these instruction-count weights. Substituting time fractions or an arithmetic mean of IPC produces a different quantity from total instructions divided by total cycles. [CA M006 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-018) Recalled Q5 connects to identifying the quantity and weighting before selecting an averaging rule. [EX:ca_2025_2_midterm_q05 p.2] Its wording comes from a reconstruction, not an independently verified official paper, and supplies no universal rule for averaging performance.

### Calculating both mixes printed in the source

The headers in [CA NM002 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-012)–[CA NM002 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-013) specify SW 15% and ALU 40%, while the equations use SW 10% and ALU 45%. The other entries agree. Preserve both input sets rather than combine them into one supposedly settled example.

| Class | CPI | Header mix | Equation mix |
|---|---:|---:|---:|
| LW | 12 | 25% | 25% |
| SW | 11 | 15% | 10% |
| ALU | 8 | 40% | 45% |
| Branch | 7 | 15% | 15% |
| Jumps | 6 | 5% | 5% |

The last row's six-cycle cost uses the displayed JAL path. It does not apply unchanged to seven-cycle JALR or jumps requiring a link write.

The equation mix gives $0.25(12)+0.10(11)+0.45(8)+0.15(7)+0.05(6)=9.05$. The header mix gives $0.25(12)+0.15(11)+0.40(8)+0.15(7)+0.05(6)=9.20$. A 50 ps microclock is **20 GHz**; the 600 ps single-cycle clock is approximately 1.667 GHz.

| Metric | Single-cycle | Equation mix | Header mix |
|---|---:|---:|---:|
| CPI | 1 | 9.05 | 9.20 |
| IPC | 1 | 0.110497 | 0.108696 |
| Average instruction time | 600 ps | 452.5 ps | 460 ps |
| MIPS | 1666.667 | 2209.945 | 2173.913 |
| Speedup at equal IC | 1 | 1.325967 | 1.304348 |

MIPS equals $IPC\times f_{MHz}$. Using the slide's displayed IPC 0.1104 yields its approximate $0.1104\times20000=2208$ MIPS; distinguish this from calculation with exact $1/9.05$. The numerical speech at 26:18, 0.114 at 28:07, 208 at 29:06, and 2.2 GHz at 31:04 are not recovered into a consistent utterance. The calculations here explicitly distinguish **about 2.2 billion instructions/s from 20 billion cycles/s**. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 26:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 28:07]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 29:06]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 31:04]]

Both mixes have average CPI below twelve and improve time in this ideal model. An all-load stream instead takes $12\times50=600$ ps per instruction, giving the same latency. The judgment connected to recalled Q8 therefore compares period, required cycles, workload, and overhead rather than assuming multi-cycle execution is always substantially faster. [EX:ca_2025_2_midterm_q08 p.2] Ignoring real control and latch overhead cannot establish universal implementation superiority.

## Key Takeaways

- Arithmetic's ALU result is data; a load's ALU result is an address.
- MasterEn permits completed PVS updates without stopping controller progression.
- CPI counts visited microcycles, not all available states.
- 50 ps means 20 GHz; the two printed mixes yield separate CPIs of 9.05 and 9.20.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Stages and data widths

Compare IF/ID/EX/MEM/WB for R/I arithmetic and `lw`. Distinguish PC, the 32-bit instruction's register/opcode fields, 64-bit data, and the three mux purposes.

<details><summary>Show solution</summary>

PC is an address; IF retrieves instruction bits. Fields are `rs1=[19:15]`, `rs2=[24:20]`, `rd=[11:7]`, opcode=`[6:0]`; selected register values are 64 bits. Arithmetic follows IF→ID→EX→WB; a load uses EX's EA in MEM before WB. I-type format alone cannot imply no MEM, since loads can be I-type. ALU register/immediate selection, ALU/memory write-back selection, and PC+4/target selection serve distinct purposes. A branch shift handles displacement units, not every immediate.

**Checking points:** Separate PC/instruction, index/data, and arithmetic result/address.

</details>

#### Recall Q02 · Delay sums and link conditions

With memory 200 ps, ALU 100 ps, register read/write 50 ps each, and other logic zero, compute arithmetic, `lw`, `sw`, omitted-WB Bxx/JALR, and omitted-ID/WB JAL times. Find the common clock and explain link limits.

<details><summary>Show solution</summary>

Arithmetic is 200+50+100+50=400 ps; load adds MEM 200 for 600 ps; store omits WB for 550 ps; the displayed Bxx/JALR costs 350 ps and JAL 300 ps. The common single-cycle period is at least 600 ps, about 1.667 GHz maximum. Arithmetic's 200 ps slack is not a data-memory read. Link-writing `jal/jalr` with `rd≠x0` must preserve that register effect. The table supplies no full added schedule, so omitted-WB costs are not universal jump costs.

**Checking points:** Count IF and MEM separately and qualify jump costs.

</details>

#### Recall Q03 · MasterEn and controller progress

At 50 ps, count IF/ID/EX/MEM/WB microcycles. With MasterEn=0, which updates are withheld and which continue? Does MasterEn=1 write everything?

<details><summary>Show solution</summary>

Counts are 4,1,2,4,1. The initial model commits architectural PVS effects at the instruction's completion, while controller state progresses through intermediate states such as IF1→IF2. Otherwise it could never reach completion. MasterEn combines with instruction-specific RegWrite/MemWrite; it does not write every location. It labels completion transitions, not continuous writes throughout IF1. The contradictory negation at 13:11 remains distinct from the diagram/14:04 explanation.

**Checking points:** Distinguish controller/architectural state and when/what to write.

</details>

#### Recall Q04 · FSM paths and CPI

Give class CPIs and completion transitions in the twelve-state model. Explain decisions at IF4, EX2, MEM4 and whether the next IF1 belongs in the prior CPI.

<details><summary>Show solution</summary>

Arithmetic visits 4 IF+1 ID+2 EX+1 WB=8; `lw` adds 4 MEM for 12; `sw` omits WB for 11. Omitted-WB Bxx/JALR costs 7; JAL also omits ID for 6. IF4 sends JAL directly to EX1; EX2 sends arithmetic to WB, loads/stores to MEM1, and displayed branch/jump paths to IF1. MEM4 sends a load to WB and a store to IF1. MasterEn labels terminal WB→IF1, store MEM4→IF1, or relevant EX2→IF1. The next IF1 belongs to the next instruction, and not every path visits all twelve states.

**Checking points:** Justify five costs and three terminal-transition forms by visited states.

</details>

#### Recall Q05 · ROM rows and output width

Find state bits and ROM rows for twelve states with generic six-bit versus raw seven-bit RISC-V opcode input. Compare adding one input/output to a 10-input/20-output ROM, and explain control versus NS outputs.

<details><summary>Show solution</summary>

Twelve states require ceil(log2 12)=4 bits. The generic figure has 6+4=10 inputs and 1024 rows; raw RISC-V opcode gives 7+4=11 and 2048 rows. Predecoded classes could differ. Capacity m×2^n gives 20,480 bits; adding an input gives 40,960 and adding only an output gives 21,504. Datapath controls select ALU, muxes, and accesses; NS3–NS0 feed the next controller state. The spoken n×2^n formula and six-bit RISC-V assertion are not adopted. ROM capacity does not directly determine minimized PLA gate count/delay.

**Checking points:** Base calculations on input-selected rows and output row width.

</details>

#### Recall Q06 · Two mixes, two timing results

Given LW/SW/ALU/Branch/JAL CPIs (12,11,8,7,6), evaluate header weights (25,15,40,15,5)% and equation weights (25,10,45,15,5)% separately: CPI, IPC, average time, MIPS, and speedup over 600 ps. Microclock is 50 ps.

<details><summary>Show solution</summary>

Equation weights give .25×12+.10×11+.45×8+.15×7+.05×6=9.05; header weights give .25×12+.15×11+.40×8+.15×7+.05×6=9.20.

|Mix|IPC|Time|MIPS|Speedup|
|---|---:|---:|---:|---:|
|Equation|1/9.05≈0.110497|452.5 ps|2209.945|1.325967|
|Header|1/9.20≈0.108696|460 ps|2173.913|1.304348|

Clock is 1/(50×10^-12)=20 GHz=20000 MHz, so MIPS=IPC×20000. The 600 ps single-cycle case has CPI 1 and about 1666.667 MIPS. The source's rounded .1104 yields 2208 MIPS rather than the exact-reciprocal result. Keep the conflicting weights separate, and restrict Jumps CPI 6 to the displayed omitted-WB JAL path.

**Checking points:** Check weight sums, time=CPI×50, and speedup=600/time.

</details>

#### Recall Q07 · Aggregate IPC and comparison conditions

Derive CPI and IPC from instruction-count weights w_i and explain the arithmetic-mean IPC pitfall. Assess an all-load stream and equal ISAs with unequal IC.

<details><summary>Show solution</summary>

Total cycles are IC Σw_i CPI_i, hence CPI_avg=Σw_i CPI_i and IPC_avg=1/Σ(w_i/IPC_i), a harmonic mean with those count weights. Substituting time weights or arithmetic-mean IPC changes the quantity. All loads take 12×50=600 ps, matching ideal single-cycle latency. General comparisons require IC×CPI×period; equal ISA does not ensure equal IC. CPU and elapsed time also differ outside the all-cycles-used assumption. About 2.2 billion instructions/s is not 2.2 GHz, and ignored overhead prevents universal superiority claims.

**Checking points:** Verify through total instructions/total cycles and state comparison premises.

</details>

### Apply the ideas

#### Practice P01 · When overhead changes the conclusion

Newly written synthetic practice. An equal-IC execution is 50% arithmetic and 50% loads, with CPIs 8 and 12. Single-cycle period is 600 ps; multi-cycle initially uses 50 ps. Compute average CPI/IPC and speedup, then reassess if implementation overhead raises the microperiod to 65 ps. Find the break-even microperiod.

Connection: quantity/weight selection from [EX:ca_2025_2_midterm_q05 p.2] and conditional-throughput reasoning from [EX:ca_2025_2_midterm_q08 p.2] become a boundary where the conclusion reverses. Prerequisites: Q02, Q04, Q06, Q07; overhead is a newly specified assumption.

<details><summary>Show solution</summary>

Average CPI is .5×8+.5×12=10, IPC .1. Arithmetic averaging category IPC gives .5/8+.5/12≈.104167, inconsistent with total cycles. At 50 ps, average time is 500 ps and speedup 1.2. At 65 ps it is 650 ps and speedup 12/13≈.9231, a slowdown. Break-even period is 600/10=60 ps. A much faster clock still needs multiplication by cycles per instruction and overhead.

**Checking points:** Check equal IC, aggregate averaging, the 60 ps boundary, and the reversal.

</details>

### Short review plan

Redraw Q02–Q04's paths and completion transitions, then calculate Q05's ROM dimensions. Recompute Q06–Q07's two mixes separately and predict P01's overhead boundary before solving.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-15-lecture-05|2026-09-15 lecture notes]]
- [lec 06.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-013)
- [lec 05 typo fixed.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf) — [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063)
- [lec 04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-018)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 corrected transcript]] — 04:01, 04:56, 06:49, 07:50, 08:47, 09:40, 12:25, 13:11, 14:04, 15:55, 16:57, 18:48, 20:43, 21:41, 22:23, 24:33, 26:18, 28:07, 29:06, 31:04, 34:04 (plain timestamps within the page)

September 29 does not establish the date/full coverage of an unavailable earlier class. Zero-cost other logic and a 50 ps microclock are ideal teaching assumptions. Omitted jump WB applies only to the displayed paths discarding the link. Keep six-bit generic versus seven-bit RISC-V opcodes, both mixes, and conflicting MIPS/GHz figures distinct. The initial MasterEn model and later IR resource-reuse design do not share one update schedule.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q05 p.2], [EX:ca_2025_2_midterm_q08 p.2].
