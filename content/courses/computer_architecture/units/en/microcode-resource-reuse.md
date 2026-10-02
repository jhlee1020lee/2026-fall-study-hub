---
title: "Microcode Controllers and Hardware Resource Reuse"
description: "Connect μPC, dispatch, shared ALUs, retained state, and design trade-offs."
course: "computer_architecture"
unit_id: "microcode-resource-reuse"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 06.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-29-lecture-05"]
---

Microcode expresses repeated control sequences as a small program. Study the hardware that sharing removes together with the intermediate information it must preserve.

## Expressing repeated next-state behavior as a microprogram

A multi-cycle controller uses instruction class and current state to choose control outputs and the next state. A monolithic ROM stores an entry for every opcode/state combination, repeating transitions shared by many instructions. For example, must progression through an intermediate IF state or EX1 be stored separately for every opcode? September 29 35:59–39:27 introduces microcode control by separating this repetition. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 35:59]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 39:27]] [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]

The microprogram counter, μPC, holds the address of the current **micro-state**. It differs from the user program's PC, which identifies a machine-instruction address. Indexing μprogram ROM with μPC selects a μinstruction whose fields specify datapath control and next-address selection. An incrementer handles sequential μPC+1 progression; small dispatch ROMs supply targets when the opcode requires different paths. [CA NM002 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014) Distinguish this μPC-indexed structure from the wording at 37:51 describing a “micro instruction” as the lookup-table input. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 37:51]]

### AddrCtl and two dispatch ROMs

![CA NM002 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-015.png)

The upper state register holds current μPC, and the adder produces its incremented value. A mux selects state 0, Dispatch ROM 1, Dispatch ROM 2, or the incremented state as the next μPC. The μprogram's control output sets AddrCtl: selecting the next control location is itself part of the small program.

| AddrCtl | Source of next state |
|---:|---|
| 0 | State 0 |
| 1 | Dispatch ROM 1 |
| 2 | Dispatch ROM 2 |
| 3 | Current state + 1 |

For an illustrative μPC=5 and AddrCtl=3, the next μPC is 6. This is not the user PC's four-byte increment; it selects the next microinstruction address in this model.

| Instruction name in this figure | Six-bit opcode in this figure | Dispatch ROM 1 target | Dispatch ROM 2 target |
|---|---|---|---|
| R-format | 000000 | 0110 | — |
| jmp | 000010 | 1001 | — |
| beq | 000100 | 1000 | — |
| lw | 100011 | 0010 | 0011 |
| sw | 101011 | 0010 | 0101 |

The first dispatch sends lw and sw to a shared target; the second separates their later paths. Meanwhile, the incrementer expresses ordinary next-state progression without repeating it in a large opcode-indexed table. This establishes the principle of reducing repetition, not a measured amount of area or delay reduction.

**These opcodes and target numbers belong to a different illustrative machine from the preceding twelve-state RISC-V timing FSM.** At September 29 43:18 and 44:26, the instructor explicitly says this example does not implement the earlier FSM. Do not assign target `0110` an arbitrary earlier state meaning or memorize `000000` as the actual RISC-V R-type opcode. The spoken R-type target at 41:27 also differs from printed `0110`; the account here reads the figure rather than reconstructing speech. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 41:27]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 43:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 44:26]]

## Reusing one ALU at different times

The physical datapath can be simplified as well as control storage. A single-cycle diagram can contain both a PC+4 adder and a register-arithmetic ALU, allowing simultaneous work within one cycle. Splitting an instruction across time separates the need for PC+4 from the EX calculation, creating an opportunity to reuse one ALU sequentially. [CA NM002 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-017) [CA NM002 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-018) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 45:27]]

The input muxes in [CA NM002 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020) are the key:

| Required work | ALU input sources | Use of result |
|---|---|---|
| Sequential PC calculation | PC and constant 4 | Next sequential instruction address |
| Register arithmetic | Two register-file values | Arithmetic result |
| Immediate-based operation | Register value and required immediate | Operation result or address |

September 29 47:25 contrasts selecting PC and 4 with selecting register values during EX. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 47:25]] The idea is not to eliminate arithmetic functionality, but to change **input sources and use times** for the same resource.

Even single-cycle execution shares one ALU across different instructions. The additional idea here is sharing it across **different stages of one instruction**. Fewer adders can reduce area and manufacturing cost, but require muxes, control, and retained intermediate values, while giving up simultaneous computation. Resource savings alone therefore do not guarantee faster execution.

PC+4 belongs to this 32-bit, four-byte instruction model. The spoken “always four” does not establish instruction lengths for every unsupplied RISC-V extension. Also, page 18's 16→32-bit immediate label belongs to an older illustrative datapath; do not combine it with the earlier RV64 32-bit-instruction/64-bit-data model into one implementation specification.

## Preserving the current instruction when PC changes

With PC directly connected to instruction memory's address input, changing PC changes the memory output through a combinational path. If resource reuse updates PC to PC+4 before the current instruction finishes, later stages relying directly on that output may see the next instruction's opcode and register fields. This is the timing problem explained at September 29 48:04. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 48:04]]

![CA NM002 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-022.png)

The Instruction Register (IR) sits **between instruction-memory output and the decode/register-file side**. It therefore retains fetched instruction bits. For example, capturing instruction $I_A$ while PC=A allows decode and EX to keep using IR's $I_A$ after PC changes to A+4. Controlling the capture point and retaining the bits for the required interval solves the information-preservation problem. [CA NM002 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021)

At 49:03 and 49:43, the speech describes IR as retaining a previous instruction counter or PC and hesitates over location and update timing. The **instruction-bit** interpretation above is an explicit note-side correction based on the actual wiring, not recovered speech. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 49:03]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 49:43]]

The lecture's “latch-based control” expresses the idea of preserving information across propagation and update boundaries. The figure does not specify active levels, setup/hold constraints, or a two-phase latch implementation. Nor should the initial MasterEn model's final PVS update be conflated with PC timing in this later IR-based design. They are different development stages of the implementation.

## Shared memory and intermediate execution state

At September 29 52:36, instruction/data memory reuse is briefly introduced and its details deferred to the following week. The block interpretation of [CA NM002 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023) below is therefore **materials-based supplementation**. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 52:36]]

Using one memory for IF and data access at different times requires selecting the appropriate address. Values from one operation must also survive until the operation that consumes them.

| Internal storage | Information retained in the figure | Purpose |
|---|---|---|
| IR | Fetched instruction bits | Preserve fields during later decode/execution |
| Memory Data Register (MDR) | Data read from memory | Retain a load result until WB |
| A and B | Two register-file read values | Preserve operands for subsequent stages |
| ALUOut | ALU result | Retain an address or result for later use |

For a load, retain the instruction in IR, calculate the effective address from base and immediate, preserve that address for the memory access, and retain the loaded data for WB. A store needs both its address and store operand to remain available until the memory stage. This explains information lifetimes, not a complete IR/MDR-enable or per-instruction control schedule.

These internal registers differ from architectural general-purpose registers directly named by software. Sharing one memory over time within an instruction also differs from overlapping several instructions in a pipeline. The September 29 50:46–51:38 preview motivates using otherwise idle IF/ID resources while an earlier instruction occupies EX. Hazards, forwarding, flushing, and actual pipeline CPI are not developed here. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 50:46]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 51:38]]

## Allocating complexity between datapath and microcode

A microcontroller can be viewed as a small processor that sequences operations and branches, rather than merely counts states. Arranging simple actions into a μprogram raises the possibility of supporting complex instructions or operations not initially anticipated. Long sequences and repetition may require internal μISA state such as loop counters. Adding that internal state differs from adding programmer-visible registers. [CA NM002 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)

| Design direction in the source | Allocation of work | Considerations following from the principles |
|---|---|---|
| Complex datapath + simple microcoding | Put more functionality directly into circuits | Potentially simpler sequences, with circuit-area and design costs |
| Simple datapath + complex microcoding | Reuse simpler resources through more micro-operations | Sequence length, control storage, and internal-state costs |
| Simple datapath + simple microcoding | Keep instructions and datapath/control simple together | Choice between supported functionality and simplicity |

These trade-offs are explanatory consequences of resource use and sequential execution, not measured proof that one option is always faster or cheaper. Loop counters and the formal three-way comparison are slide details; deciding how to split work between the main processor and microcontroller is directly discussed at September 29 53:36–54:28. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 53:36]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 54:28]]

The microcoded multi-cycle side of recalled Q16(a) can be approached this way: first explain the operation sequence and resource-reuse times, then reason about how sequence length and clock period affect latency. [EX:ca_2025_2_midterm_q16 p.8] A complete comparison with that question's hardwired-pipeline side requires later pipeline study. The reconstruction has no independently verified official wording or answers, and the label “microcoded” alone establishes no universal performance ranking. Likewise, the lecture's x86/CISC example does not verify a particular modern product's microcode organization or update procedures.

## Key Takeaways

- μPC addresses microinstructions and is distinct from the user's PC.
- The incrementer handles common sequential progress; dispatch ROMs select class-dependent paths.
- Sharing one ALU for PC+4 and EX requires input selection and retained intermediate values.
- IR retains instruction bits, MDR load data; time-sharing differs from pipeline overlap.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · μPC and AddrCtl

How is repetition in a monolithic ROM separated? Explain μPC, μprogram ROM, μinstruction, incrementer, dispatch, and AddrCtl 0–3; trace μPC=5 with AddrCtl=3.

<details><summary>Show solution</summary>

Rather than repeat identical transitions for every opcode, μPC indexes a μprogram ROM whose selected μinstruction supplies datapath control and next-address selection. An incrementer handles common progress; small dispatch ROMs handle opcode-dependent choices. AddrCtl 0 selects state0, 1 dispatch1, 2 dispatch2, 3 current+1, yielding μPC=6. This is not the user PC's instruction address or four-byte increment. Reduced repetition is established, not a measured area/delay saving.

**Checking points:** Separate ROM address input from selected instruction output and PC from μPC.

</details>

#### Recall Q02 · Two dispatch tables

Give dispatch1 targets for R-format, jmp, beq, lw, sw and dispatch2 targets for lw/sw. Why share an early target and split later, and why not reuse the earlier FSM's state meanings?

<details><summary>Show solution</summary>

The figure gives R `000000→0110`, jmp `000010→1001`, beq `000100→1000`, lw `100011→0010`, sw `101011→0010`. Dispatch2 maps lw→`0011` and sw→`0101`. Shared earlier work can precede distinct load/store paths. This is a separate machine: target `0110` cannot be assigned an earlier EX1 meaning, and the six-bit R opcode is not a RISC-V encoding. The spoken target discrepancy at 41:27 remains explicit.

**Checking points:** Check both tables and restrict state meanings to their own example.

</details>

#### Recall Q03 · Time-sharing one ALU

How must inputs and timing change to share one ALU between PC+4 and register EX? Distinguish this from sharing an ALU across instructions in a single-cycle design.

<details><summary>Show solution</summary>

Muxes select PC and constant4 for PC progress, then register operands or register/immediate for EX. Beyond single-cycle sharing across different instructions, this shares hardware across stages of one instruction. Fewer adders may reduce area but require muxes, stage-dependent control, and retained results while sacrificing simultaneous work. PC+4 belongs to this four-byte-instruction model; the older diagram's 16→32 immediate is not a combined RV64 specification.

**Checking points:** State which inputs are needed when and the costs of sharing.

</details>

#### Recall Q04 · How IR prevents wrong decoding

PC changes from A to A+4 before the current instruction finishes. Explain the problem for decode directly driven by instruction memory and the IR's location, contents, and capture requirement.

<details><summary>Show solution</summary>

Combinational memory output changes to the instruction at A+4, so later stages could see wrong opcode/register fields. Place IR between memory output and decode, capture instruction bits fetched at A, and retain them as needed—not address A itself. Capture must be controlled, but the diagram does not specify latch levels, setup/hold, or two-phase implementation. The PC-storage wording at 49:03/49:43 is distinguished through the wiring, and this timing must not be merged with the initial MasterEn design.

**Checking points:** Identify propagation, the retained information, and unspecified timing details.

</details>

#### Recall Q05 · Information in intermediate registers

What do IR, MDR, A, B, and ALUOut preserve, and why do load/store paths need them? Is time-sharing one memory the same as pipeline overlap?

<details><summary>Show solution</summary>

IR retains instruction bits; MDR memory-read data; A/B the two register-read values; ALUOut an ALU result/address. A load needs its EA until memory access and its loaded value until WB; a store needs both address and data. Alternating one memory between IF and data access also requires address selection. These internal states differ from software-named GPRs. Pipelining overlaps several instructions, distinct from time-sharing within one instruction. Detailed blocks are material supplementation; enables, hazards, forwarding, flushes, and pipeline CPI are not supplied.

**Checking points:** Check all five storage roles and load/store value lifetimes.

</details>

#### Recall Q06 · Where to place complexity

Compare complex-datapath/simple-microcode, simple-datapath/complex-microcode, and simple/simple designs. Why might μISA loop counters be needed, and are they architectural registers?

<details><summary>Show solution</summary>

Dedicated circuitry can simplify/shorten sequences at circuit-area and design cost. Repeated μoperations can reuse simpler resources at sequence-length, control-memory, and internal-state cost. Simple/simple keeps supported instructions and datapath/control simple together. Loop counters can track repeated internal work without adding software-visible registers. These are design directions, not universal RISC/CISC rankings or verified facts about modern x86 implementations.

**Checking points:** Compare all three directions through sequence, area, and internal-state costs.

</details>

### Apply the ideas

#### Practice P01 · Conditions for comparing shared designs

Newly written synthetic practice. Designs A and B have the same architectural effect. A uses a dedicated adder and shorter μsequence; B shares an ALU through a longer μsequence. All you know is that B has a faster clock. Assess whether B must have lower latency, name the required measurements, and identify information needed if PC changes early.

Connection: the microcoded multi-cycle reasoning of [EX:ca_2025_2_midterm_q16 p.8] (a) becomes a comparison of resources, timing, and correctness. Prerequisites: preceding CPI×period reasoning and Q03, Q04, Q06. Part (b)'s hardwired-pipeline comparison is deferred for later prerequisites.

<details><summary>Show solution</summary>

Latency equals required microcycle count×period, so a faster clock may or may not offset a longer sequence. Compare path counts, periods, overhead, and workload. Area includes added muxes, control, and storage as well as the removed adder. Early PC change requires IR to retain current instruction bits and storage to retain intermediate results until consumption. The supplied material does not fix exact capture scheduling. Resource reuse is explainable without a universal latency/throughput ranking.

**Checking points:** Name missing quantities and include information preservation alongside performance.

</details>

### Short review plan

Trace μPC and both dispatches in Q01–Q02, then mark value lifetimes in Q03–Q05. Answer Q06 and P01 by comparing timing, area, and internal state together.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]
- [lec 06.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf) — [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-018), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 corrected transcript]] — 35:59, 37:51, 39:27, 41:27, 43:18, 44:26, 45:27, 47:25, 48:04, 49:03, 49:43, 50:46, 51:38, 52:36, 53:36, 54:28 (plain timestamps within the page)

The six-bit dispatch opcodes/state numbers belong to a different example from the preceding twelve-state RISC-V FSM. Diagram-based explanations distinguish conflicting target/input wording without recovering speech. IR holds instruction bits, not PC. Shared-memory register details and loop counters are material supplements; September 29 only previews pipeline motivation. Detailed latch timing, complete control schedules, and modern-product microcode/update mechanisms are outside scope.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q16 p.8].
- [[exam_questions/ca_2025_2_midterm_q16|2025-2 midterm reconstruction Q16 · existing question preview]]
Only Q16(a)'s microcoded side is connected; (b)'s hardwired-pipeline comparison requires later study.
