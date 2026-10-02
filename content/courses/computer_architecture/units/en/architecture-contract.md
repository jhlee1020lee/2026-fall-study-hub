---
title: "Computer Organization and the ISA Contract"
description: "Connect ISA semantics, implementation choices, and scaling limits."
course: "computer_architecture"
unit_id: "architecture-contract"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 01.pdf", "lec 02.pdf", "lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-01-lecture-01", "courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-03-lecture-02"]
---

Separate the behavior promised by an ISA from the circuits that deliver it. Use state changes to connect compatibility, extensibility, and performance limits.

## Separating the ISA from its implementation

A computer is a programmable device that stores, retrieves, and processes data. Mobile devices, desktops, servers, and data centers differ in scale and purpose, but share this ability to perform work under program control. To execute a program on different circuits, we must distinguish the **meaning of an operation** from the **mechanism that implements it**.

The Instruction Set Architecture (ISA) specifies the functionality software can observe and control. Microarchitecture is a processor design that implements that specification; circuits realize it using gates, wires, and transistors. A vehicle's user manual, a particular vehicle design, and its physical components provide a useful analogy. Two processors can implement the same addition instruction while using different datapaths, control logic, or caches, producing different speed and power characteristics. Sharing an ISA supplies a basis for machine-instruction compatibility; it does not guarantee every operating-system and execution-environment requirement. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 03:13]] [CA M008 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-005)

The hierarchy in [CA M001 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-016) places applications, compilers, and the OS above the ISA and microarchitecture, with digital design, circuits, and devices/physics below. Each level uses the contract it needs without reproducing every detail of the level underneath. A compiler needs to know which instruction and operand format can represent addition; it need not place the transistors implementing that addition. [[courses/computer_architecture/lectures/en/2026-09-01-lecture-01|2026-09-01 lecture notes]]

### The contract used by compilers and context switches

A compiler uses operations, registers, data widths, and instruction encodings to translate C computations into machine instructions. A high-level language may hide those details from its user, but system software still needs them. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 04:46]]

An OS context switch lets different processes use the same physical registers at different times. If process A stops and B runs, B's computations can overwrite those registers. Resuming A therefore requires saving A's values to memory and restoring them later. The September 8 explanation connects this save-and-restore operation to the ISA's role as a software–hardware contract. It does not specify a complete OS context structure or scheduling policy. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 05:32]] [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]]

## Stored programs and architectural state

In a stored-program organization, both instructions and data reside in memory. In [CA M001 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-014), the processing block contains a datapath that performs operations and control that sequences them; storage contains both program and data, while I/O connects the computer to its surroundings. The more detailed organization in [CA M001 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-015) places an ALU, register file, and cache inside a CPU, connected through a memory bus to main memory. An I/O bridge leads toward disk, video, keyboard/mouse, and network devices. This illustrates relationships between components, not a mandatory wiring diagram for every computer.

On September 1, the instructor contrasted shared program/data communication with Harvard architecture's separate paths. Separate paths can allow concurrent accesses, but channel count alone does not guarantee greater throughput for every workload. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 23:07]] The corresponding recalled-exam demand is to distinguish what is stored from the paths used to access it: explain where instructions and data reside rather than memorize a true/false sentence. [EX:ca_2025_2_midterm_q01 p.2] This connection uses a Fall 2025 reconstruction whose official wording and answers have not been independently verified.

Architectural state consists of memory, registers, the Program Counter (PC), and other state that expresses program execution. PC supplies an instruction **address**. The sequential model in [CA M008 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-007) fetches the instruction at that address, executes its operation, and updates PC according to the instruction's rules.

| Instruction class | Information read | State effect |
|---|---|---|
| Arithmetic/logical | Source operands | Write a result to a destination, usually continuing sequentially |
| Data movement | A value and its source/destination locations | Change the specified register or memory location |
| Control flow | A condition and target | Select a target or sequential address for the next PC |

As an illustrative application, adding register values 7 and 5 leaves 12 in a destination. A branch instead compares values and determines the next instruction location. These distinct effects make an ISA more than a list of instruction names. It also addresses number formats and sizes, visible state, binary encodings, I/O interfaces, protection/privilege, and software conventions. The detailed implementation of the latter interfaces is beyond this explanation. [CA M008 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-010)

Describing an instruction as an abstract atomic state transition defines its before-and-after meaning. It does not require one physical clock cycle or exclusion of every other processor's memory accesses. This explicit execution model is materials-based review associated with September 3, for which no recording is supplied. [CA M008 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-011) [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]

## Operand formats and RISC simplification

An instruction set is the repertoire of available operations. x86-64, ARM, and RISC-V are different ISAs, but share arithmetic, data movement, and control-flow categories. The lecture introduces RISC-V as an open ISA developed at UC Berkeley and used in embedded processors and accelerators. This explains the course's choice of example; it is not a legal assessment of individual licensing arrangements. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 07:20]] [CA M003 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-006)

The notation in [CA M008 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-013) compares how explicitly an operation identifies its inputs and output.

| Source classification | Notation | Interpretation |
|---|---|---|
| Monadic | `OP in2` | One operand is explicit; other meanings depend on the operation |
| Binatic | `OP inout,in2` | One location acts as both input and output |
| Triadic | `OP out,in1,in2` | One output and two inputs are explicit |

Basic RISC-V register arithmetic uses the last form. Its load-store organization separates memory access from ALU operations. A complicated expression can still be decomposed into simple instructions, with the compiler managing intermediate values and register allocation.

The materials connect initially simple ISAs, CISC complexity associated with assembly programming and microprogramming, and RISC simplification supported by advances in caches and compilers. Fewer formats and regularity can help implementation and compiler optimization. The persistence of x86 also involves compatibility ecosystems and economic factors, rather than one purely technical ranking. This detailed historical comparison is materials-based. The unclear trade-off phrase at September 8 08:20 is not recovered speech merely because the slides support a coherent explanation. [CA M008 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-016) [CA M008 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-017) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 08:20]]

### Leaving room for extension and generality

An ISA is a long-term contract for future programs and implementations, not just the internals of today's processor. A designer may sacrifice immediate optimality for future scalability and compatibility. Parameterizing storage capacity, CPU count, and I/O count, and reserving spare encoding bits, leaves room for later extensions. Using every encoding immediately makes that space harder to recover. The materials also list asynchronous operation of components as a way to avoid excessive dependence on fixed speed relationships; they do not specify a circuit protocol. [CA M008 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-009) [CA M008 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-026)

Generality means supporting applications of different kinds and sizes. The slides connect this to avoiding arbitrary special interpretations of ordinary data patterns, while providing numeric operations, bit manipulation, and fine-grained memory addressing. An ML accelerator offers a contrast: some generality can be exchanged for concentration on particular computations. The design question concerns the intended work and compatibility requirements, not a universal winner. [CA M008 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-027)

## Transistors and the limits of performance scaling

The simplified transistor model is a switch that connects or disconnects a current path under control of an input. The upper example in [CA M001 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-019) connects when control is 1; the lower connects when control is 0. Such switches can form gates that map binary inputs to binary outputs. An inverter reverses its input; NAND reverses the result of AND.

| Input A | Input B | NAND output |
|---:|---:|---:|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

This matches the September 1 explanation. Combining gates produces combinational circuits; adding state-preserving elements supports sequential circuits, memory, and CPUs. The purpose is to connect abstraction levels, not to teach a complete transistor design. The ambiguous NOR-labeled outline on source page 20 is not used to infer a gate's function. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 30:22]] [CA M001 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-021)

### Moore's Law and Dennard Scaling make different claims

Moore's Law is presented as the historical trend of transistor counts roughly doubling every two years. The vertical axis in [CA M001 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-023) is logarithmic: an approximately straight rising pattern does not mean the same fixed number of transistors is added each time. The historical table in [CA M001 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-024) compares these scales:

| Period | Transistors | Clock frequency | IPC | MIPS/MFLOPS |
|---|---:|---:|---:|---:|
| 1970s | 10K–100K | 0.2–2 MHz | <0.1 | <0.2 |
| 1980s | 100K–1M | 2–20 MHz | 0.1–0.9 | 0.2–20 |
| 1990s | 1M–100M | 20 MHz–1 GHz | 0.9–2 | 20–2000 |
| 2010 **extrapolation** | 1B | 10 GHz | 10(?) | 100,000 |

The 2010 row in this table is an extrapolation, not measured achievement. It transposes the rightmost 2010 column of M001 PDF p.24 into a row here; the instructor emphasizes this at September 1 36:16. MIPS/MFLOPS likewise do not make different workloads universally comparable. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 36:16]]

Dennard Scaling concerns smaller devices switching faster while maintaining power density. The slides identify leakage and overheating as limitations. [CA M001 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-025) In the trend plot in [CA M001 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-026), transistor count continues rising while frequency and single-thread performance do not follow at the same rate, and logical core counts increase. The plot shows slower single-thread improvement, not its complete cessation.

Multiple cores can improve throughput by working on independent tasks. Reducing one task's latency requires parallelism within that task. As an illustration, assigning two independent jobs to two cores lets both progress together, but does not automatically halve one job's sequential work. Even linear throughput growth requires sufficient independent work and no limiting shared bottleneck. These are motivations drawn from historical scaling material, not updated product records or predictions. [CA M001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-027) [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 40:38]]

## Key Takeaways

- The same ISA permits different datapaths, caches, speed, and power.
- PC holds an instruction address; instruction semantics determine the next state.
- Regular instructions let compilers build complex computations from simple steps.
- More transistors, constant power density, and faster individual tasks are distinct claims.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Specification and implementation

Two processors support the same instruction semantics but run at different speeds. Explain this using ISA, microarchitecture, and circuits; does sharing the ISA guarantee every execution environment?

<details><summary>Show solution</summary>

The ISA specifies software-visible behavior. Microarchitecture realizes it through datapaths, control, and caches; circuits realize those structures with gates, wires, and transistors. Identical operation meanings can therefore have different timing and power. Compilers and operating systems use the ISA from above, but environment compatibility requires more than shared instruction semantics. Storage, retrieval, and processing remain common computer functions from mobile devices to servers.

**Checking points:** Identify all three levels, an implementation cause of different speed, and the environment limitation.

</details>

#### Recall Q02 · Storage and state transitions

Explain stored-program storage versus Harvard access paths. Connect CPU, memory, and I/O, then compare arithmetic, data movement, and branch state changes.

<details><summary>Show solution</summary>

Instructions and data are stored in memory. The CPU datapath computes and control sequences operations; ALU, register file, and cache connect toward main memory, while I/O exchanges information with devices. Separate Harvard program/data paths permit concurrent access opportunities without guaranteeing greater throughput. After fetch at the PC address, arithmetic writes a computed destination and normally advances sequentially; data movement changes a designated register/memory value; a branch selects a target or sequential PC. Abstract atomic instruction semantics do not require one clock or exclude every other CPU's memory access.

**Checking points:** Distinguish PC from instruction bits and identify each class's state effect.

</details>

#### Recall Q03 · Compilers and context restoration

What ISA information does a compiler need? What goes wrong if B runs without saving A's registers before A resumes, and why is the ISA more than an instruction-name list?

<details><summary>Show solution</summary>

A compiler needs operations, operand locations, registers, numeric formats/widths, and encodings. B can overwrite the same physical registers, so A's saved state must be restored to continue its computation. The contract includes visible state and transitions as well as I/O, protection/privilege, and software conventions. This does not specify a full OS context structure or scheduling policy.

**Checking points:** Explain the overwrite and why save/restore preserves continuation.

</details>

#### Recall Q04 · From switches to NAND

Distinguish a switch that connects at control=1 from its opposite, give all four NAND outputs, and explain inversion and state-holding circuits.

<details><summary>Show solution</summary>

One type connects at 1 and disconnects at 0; the other reverses that response. NAND negates AND, giving 1,1,1,0 for 00,01,10,11. An inverter exchanges 0 and 1. Gates implement combinational transformations; storage elements allow sequential state and memory. The ambiguous NOR outline alone is insufficient evidence of its function, and this is background rather than a transistor-design course.

**Checking points:** Check all four outputs and the role of stored state.

</details>

#### Recall Q05 · Operand forms and the compiler

Compare `OP in2`, `OP inout,in2`, and `OP out,in1,in2`. How can simple RISC instructions implement a complex expression, and what does load-store mean?

<details><summary>Show solution</summary>

The forms explicitly name one operand, share an input/output location, or name one output plus two inputs. Basic RISC-V register arithmetic uses the last form. A compiler decomposes expressions and manages intermediate values and register allocation. Load-store separates data-memory transfers from ALU computation. Regular, few formats help implementation and optimization; they do not place an entire complex computation in one instruction.

**Checking points:** Explain roles as well as the number of explicit operands.

</details>

#### Recall Q06 · ISA history and choice

Name categories shared by x86-64, ARM, and RISC-V; explain the material's CISC/RISC history and the course's RISC-V choice. Can x86 persistence be reduced to one technical ranking?

<details><summary>Show solution</summary>

All three include arithmetic, data movement, and control flow. The material contrasts early simplicity, complexity associated with assembly programming and microprogramming, and simplification supported by caches and compiler advances. RISC-V is introduced as Berkeley's open ISA with embedded and accelerator uses. Compatibility ecosystems and economics also contribute to x86 persistence. These are historical explanations and course motivations, not current market measurements or licensing judgments.

**Checking points:** Include compiler/cache developments and compatibility considerations.

</details>

#### Recall Q07 · Extensibility and generality

What long-term purposes are served by spare encoding bits, capacity parameters, and asynchronous components? Contrast general-purpose design with an ML accelerator.

<details><summary>Show solution</summary>

Spare bits reserve extension space, while storage/CPU/I/O parameters allow scale changes. Asynchronous operation avoids excessive dependence on fixed speed relationships; no detailed protocol is specified. Generality supports varied workloads through numeric/bit operations and fine-grained addressing without arbitrary meanings for ordinary data patterns. An accelerator can trade some breadth for concentration on particular computations. Immediate optimality must be assessed with future compatibility and intended work.

**Checking points:** State each mechanism's purpose and what specialization gives up.

</details>

#### Recall Q08 · Limits of scaling graphs

Interpret a straight rise on a logarithmic transistor plot, the extrapolated 2010 10 GHz/IPC 10(?) entries, and Dennard limits. Does doubling cores halve one sequential task's time?

<details><summary>Show solution</summary>

A similar rise on a log axis indicates multiplicative rather than fixed additive growth. Moore's trend concerns transistor count; the 2010 row in this unit's table is extrapolation, not measurement. It corresponds to the rightmost 2010 column in M001 PDF p.24. Historical IPC ranges <0.1→0.1–0.9→0.9–2 and MIPS/MFLOPS ranges <0.2→0.2–20→20–2000 show changing scale without providing a universal cross-workload score. Dennard scaling concerns device speed and power density, limited by leakage and heat. Slower frequency/single-thread growth is not complete cessation. More cores can increase independent-job throughput; one task needs internal parallelism, sufficient work, and no limiting shared bottleneck.

**Checking points:** Separate measured/extrapolated values, transistor count/frequency, and latency/throughput.

</details>

### Apply the ideas

#### Practice P01 · Diagnose a design claim

Newly written synthetic practice. Designs A and B store instructions and data in one memory, use PC as an address, and implement the same ISA; B has more cores. Someone concludes that shared storage makes both ISA and implementation identical and that every program on B accelerates by the core-count ratio. Repair this explanation using storage organization, implementation, and parallel work.

Connection: [EX:ca_2025_2_midterm_q01 p.2] supplies storage-classification reasoning, extended here into evidence and performance-claim diagnosis. Prerequisites: Q01, Q02, Q08. The source is a reconstruction with unverified official wording.

<details><summary>Show solution</summary>

Shared instruction/data storage describes stored-program organization; it alone does not prove equal ISAs, which is a separate premise here. A shared ISA permits different core counts, caches, and datapaths. Extra cores help independent or parallelizable work but do not automatically divide sequential work. A performance ratio therefore needs workload parallelism and bottleneck assumptions.

**Checking points:** Do not infer ISA equality from storage; distinguish that given premise from implementation and workload effects.

</details>

### Short review plan

Explain levels and state with Q01–Q03, then compare the design choices in Q05–Q07. On the next review, retry Q08 and diagnose P01 without opening the answers.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-01-lecture-01|2026-09-01 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]
- [lec 01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.01.pdf) — [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-011), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-016), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-019), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-021), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-027)
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-005), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-011), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-013), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-017), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-027)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-006)
- [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 corrected transcript]] — 23:07, 30:22, 36:16, 40:38 (plain timestamps within the page)
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 03:13, 04:46, 05:32, 07:20, 08:20 (plain timestamps within the page)

The September 3 execution model, operand classification, ISA history, and extensibility discussion are materials-only review without a recording. Explanations do not recover uncertain September 1/8 speech; transistor design, OS scheduling, and current product comparisons remain outside scope.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q01 p.2].
- [[exam_questions/ca_2025_2_midterm_q01|2025-2 midterm reconstruction Q1 · existing question preview]]
