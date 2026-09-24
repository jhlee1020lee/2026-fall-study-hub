---
title: "Computer Organization and the ISA Contract"
description: "Connect the ISA contract, computer components, RISC design choices, and the motivation for multicore."
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
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-01-lecture-01", "courses/computer_architecture/lectures/en/2026-09-03-lecture-02", "courses/computer_architecture/lectures/en/2026-09-08-lecture-03"]
---

Separate the behavior specified by an ISA from the design that implements it. Connect state changes, compiler and OS needs, and scaling limits to explain why computers executing the same instructions can perform differently.

## The responsibilities of ISA and microarchitecture

A computer is a programmable device that stores, retrieves, and processes data. Phones, desktops, servers, and data centers differ in scale, but each executes computations requested by programs. Separate the **meaning of an operation** from the **method used to implement it** to understand the layers involved.

The Instruction Set Architecture (ISA) specifies behavior that software can observe and control. Microarchitecture is a processor design implementing that specification. Circuits realize the design using gates, wires, and transistors. Two processors can understand the same addition instruction yet use different datapaths, control logic, and caches. Their execution time and power can differ without their ISAs differing. This specification-versus-implementation distinction was explicit in [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 03:13]].

The hierarchy in [[page_cache/computer_architecture/lec.01/page-016|CA M001 p.16]] places ISA and microarchitecture below applications, compilers, and OS, and above digital design, circuits, and devices/physics. The ISA is the software–hardware interface; the lower layers implement its meaning. An analogy is the distinction between a car's operating instructions, a particular vehicle design, and its physical parts. Sharing an ISA establishes compatible machine-instruction meanings, but does not automatically satisfy every library and execution-environment requirement.

## Stored programs and architectural state

In a stored-program organization, instructions and data both have representations in memory. Changing the program changes the task, while the processor interprets fetched instruction bits according to the ISA. [[page_cache/computer_architecture/lec.01/page-014|CA M001 p.14]] connects control and datapath within processing, program/data storage, and I/O. The next page connects the CPU's ALU, register file, and cache to main memory and I/O components. These are models of component roles, not wiring diagrams every computer must follow.

Architectural state is the programmer-visible state expressing execution. Registers are small storage locations in the processor; memory holds more instructions and data; the Program Counter (PC) identifies an instruction address. In the sequential model, the processor fetches the instruction identified by the PC, executes it, and updates the PC according to that instruction. This explicit state-transition account is a materials-based review of the September 3 deck, for which no recording is supplied. [[page_cache/computer_architecture/lec.02/page-007|CA M008 p.7]] [[page_cache/computer_architecture/lec.02/page-010|CA M008 p.10]]

| Instruction class | Principal state effect | Next execution location |
|---|---|---|
| Arithmetic/logical | Compute from inputs and write a destination | Usually the next sequential instruction |
| Data movement | Transfer a value between storage locations | Usually the next sequential instruction |
| Control flow | Select execution order using a condition and target | Target or sequential location |

For example, `add` writes an arithmetic result to a destination register, whereas a conditional branch chooses the next PC. A branch target is not a register receiving an arithmetic result. An ISA also addresses numeric formats and sizes, binary encoding, visible state, I/O interfaces, protection and privilege, and software conventions. Introducing those categories does not amount to teaching their detailed implementations.

On September 1, the lecturer contrasted the shared program/data path explanation with Harvard architecture's separate paths. Storage organization, access paths, and a particular cache organization are distinct questions; their names alone establish no universal performance ranking. [[courses/computer_architecture/transcripts/2026-09-01|September 1 STT, 22:25–23:07]] Recalled 2025-2 Q1 similarly demands a distinction about instruction/data storage. It is neither evidence of current lecture speech nor an official answer. [EX:ca_2025_2_midterm_q01 p.2]

## Why compilers and context switches need the ISA

A compiler translates a C expression into a machine-instruction sequence. Correct translation requires knowing which operands an operation accepts, which registers exist, and how data is represented. A high-level language may hide this information from its user, but the underlying agreement still exists.

An operating system's context switch demonstrates another use of that agreement. If process A leaves intermediate values in registers and process B then uses the same physical registers, B can overwrite A's values. Resuming A requires preserving its state, for example in memory, and restoring it later. The lecture specifically described storing current register values and retrieving another process's values into the registers. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 04:46–05:32]] The preservable state and recovery operations depend on the architecture, but this example does not specify a complete OS context structure or scheduling policy.

## From transistor switches to gates

Implementing the specification requires physical representations of binary values. In the lecture's simplified model, a transistor is a switch that connects or disconnects a current path according to a control input. The upper type in [[page_cache/computer_architecture/lec.01/page-019|CA M001 p.19]] connects when control is 1; the lower type connects when control is 0. The figure does not assign every transistor the same control polarity.

A logic gate maps binary inputs to a binary output. An inverter reverses its input; NAND reverses the AND result. NAND therefore produces 0 only when both inputs are 1.

| A | B | AND | NAND |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

This matches [[courses/computer_architecture/transcripts/2026-09-01|September 1 STT, 30:22]]. The outline labeled NOR on M001 p.20 resembles the NAND outline and is not a reliable basis for inferring NOR's function. Gates can form combinational circuits, whose outputs depend on current inputs, and sequential circuits that retain state, leading to memory and processors. Understanding this connection is the purpose here; detailed transistor-level design is separate prerequisite study.

## Operand forms and RISC simplification

An instruction set is a computer's repertoire of operations. x86-64, ARM, and RISC-V differ, but all address arithmetic, data movement, and control flow. The lecture introduced RISC-V as an open ISA developed at UC Berkeley, used in embedded processors and accelerators as well as education. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 07:20–11:44]]

M008 contrasts monadic `OP in2`, binatic `OP inout,in2`, and triadic `OP out,in1,in2` forms. The first leaves some input/result locations implicit, the second shares one input/output location, and the third names a result and two inputs separately. Basic RISC-V register arithmetic follows the third form. [[page_cache/computer_architecture/lec.02/page-013|CA M008 p.13]]

A RISC load-store organization separates ALU computation from memory access and uses relatively few formats. A compound expression can still be evaluated using several simpler instructions. The compiler arranges the sequence, retains intermediate values, and allocates registers. Simplicity does not mean an entire computation must fit into one instruction.

The September 3 materials distinguish early simple ISAs, CISC complexity associated with assembly programming and microprogramming, and RISC simplification in the context of improved caches and compilers. They also connect x86's persistence with compatibility ecosystems and economic factors. This is materials-based history, not a reconstruction of the unclear trade-off wording in the September 8 transcript. [[page_cache/computer_architecture/lec.02/page-016|CA M008 pp.16–17]]

## Extensibility and general-purpose design

An ISA is a long-term contract for later programs and implementations. Immediate optimality can conflict with future compatibility and scalability. M008 introduces parameterizing storage capacity, CPU count, and I/O count, and reserving spare instruction-encoding bits. Spare space can allow extensions without changing established bit-pattern meanings; it does not solve every compatibility problem by itself. [[page_cache/computer_architecture/lec.02/page-026|CA M008 p.26]]

General-purpose design supports applications of different sizes and kinds. It avoids imposing arbitrary special meanings on ordinary data patterns while providing needed numeric operations, bit manipulation, and fine-grained memory addressing. Bits used as a character need not always be interpreted as a character. An ML accelerator illustrates sacrificing some generality to improve particular computations. The material's “asynchronous operation” is an introductory design item about avoiding excessive dependence on one fixed component-speed model, not a detailed circuit protocol. [[page_cache/computer_architecture/lec.02/page-027|CA M008 p.27]]

## Moore's Law and the motivation for multicore

Moore's Law is introduced as the historical trend of transistor counts roughly doubling every two years. The vertical axis of M001 p.23 is logarithmic: equal vertical increments represent multiplicative changes, not equal additions. More transistors alone do not establish a proportional reduction in one program's execution time.

The table in [[page_cache/computer_architecture/lec.01/page-024|CA M001 p.24]] associates the 1970s with 10K–100K transistors and 0.2–2 MHz, the 1980s with 100K–1M and 2–20 MHz, and the 1990s with 1M–100M and 20 MHz–1 GHz. Its final 2010 column lists 1B transistors, 10 GHz, IPC 10(?), and MIPS/MFLOPS 100,000 as **extrapolated** values. The lecturer explicitly identified that status; these are not measured achievements. [[courses/computer_architecture/transcripts/2026-09-01|September 1 STT, 36:16]]

Dennard Scaling supplies the background expectation that smaller devices can switch faster while maintaining power density. The materials identify leakage and overheating as limitations. In [[page_cache/computer_architecture/lec.01/page-026|CA M001 p.26]], transistor count continues upward while frequency and single-thread performance do not follow proportionally. Read the slowing frequency trend together with increasing logical-core counts. The graph does not show single-thread performance becoming completely constant.

Multicore can improve throughput by executing independent work concurrently. Reducing one task's latency requires that task to be parallelizable. As an illustrative application, two independent equal-duration jobs assigned to two cores can ideally finish together; one indivisible job does not automatically finish in half the time. Even linear throughput growth requires enough independent work and no limiting bottleneck. This distinction leads into [execution time and performance models](performance-model.md).

## Key Takeaways

- The ISA defines observable meaning; microarchitecture implements it.
- Track PC, registers, and memory to distinguish a computed result from the next execution location.
- Compiler translation and OS context switching depend on the same architectural contract.
- Regular operands, extension space, and generality address different design requirements.
- Transistor growth, frequency, single-task latency, and aggregate throughput are distinct quantities.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Specification and implementation

Two processors execute the same `add` but differ in speed and power. Explain the ISA, microarchitecture, and circuit layers, and whether sharing an ISA guarantees that a whole program runs.

<details><summary>Show solution</summary>

The ISA specifies observable effects such as the result of `add`. Datapath, control, and cache choices belong to microarchitecture; gates, wires, and transistors realize them at circuit level. The same meaning can therefore have different costs. Libraries and execution-environment requirements can still prevent a whole program from running.

**Checking points:** Identify all three responsibilities, explain differing performance, and retain execution-environment conditions.

</details>

#### Recall Q02 · Components and storage

Name the two kinds of content stored in a stored-program machine and relate control, datapath, storage, and I/O. Does comparison with Harvard's separate paths prove a universal speed advantage?

<details><summary>Show solution</summary>

Memory contains instructions and data. Control directs execution, the datapath processes values, storage retains programs and values, and I/O exchanges information externally. The ALU/register-file/cache/main-memory diagram models component roles. What is stored and whether access paths are shared are separate questions; performance needs workload and implementation conditions.

**Checking points:** Cover instruction/data storage and all four roles; do not infer performance from path count alone.

</details>

#### Recall Q03 · State changed by instructions

Compare `add`, data movement, and a conditional branch in terms of registers, memory, and PC. What does an ISA specify beyond these operation names?

<details><summary>Show solution</summary>

`add` writes a value computed from source registers and normally advances PC sequentially. Data movement transfers values between storage locations; a branch selects a target or sequential PC from its condition. The target is not an arithmetic-result register. The ISA also covers data sizes/formats, visible state, encodings, I/O interfaces, protection/privilege, and software conventions; naming them does not teach their detailed implementation.

**Checking points:** Separate results from control flow and explain the PC-based execution model and wider contract.

</details>

#### Recall Q04 · Compiler and execution context

Give at least two ISA facts a compiler needs to translate C addition. What must happen before resuming process A after B has reused its physical registers?

<details><summary>Show solution</summary>

The compiler needs operations, operand/register choices, and data formats/encoding. A's intermediate state must be saved, for example to memory, before B reuses it, then restored when A resumes. Otherwise A continues with B's values. Hiding details at language level does not remove the translation and state-preservation contract.

**Checking points:** Explain both compiler requirements and the causal need for save/restore.

</details>

#### Recall Q05 · Switches and NAND

Do the two illustrated transistor types have the same control polarity? Give NAND outputs for 00, 01, 10, 11, explain an inverter, and distinguish combinational from sequential circuits.

<details><summary>Show solution</summary>

The upper type connects for control 1, the lower for 0. NAND negates AND, giving 1, 1, 1, 0; an inverter reverses its input. Combinational circuits depend on current inputs, while sequential circuits retain state. This explains the route from gates to memory and CPUs without inferring a NOR function from the unreliable outline or inventing transistor circuitry.

**Checking points:** Check polarity, all four outputs, and the state-retention distinction.

</details>

#### Recall Q06 · Operands and RISC choices

Explain implicit, shared, and separate operands in monadic, binatic, and triadic forms. Relate complex expressions built from simple RISC operations to the materials' CISC-to-RISC historical background. What categories do different ISAs share, and why is RISC-V a useful teaching example?

<details><summary>Show solution</summary>

`OP in2` leaves some operands/results implicit; `OP inout,in2` shares one input/output location; `OP out,in1,in2` names a result and two inputs separately. Basic RISC-V register arithmetic uses the last form. Compilers decompose expressions and manage intermediates/registers. The materials associate CISC complexity with assembly programming/microprogramming and RISC simplification with caches/compiler advances; compatibility ecosystems and economics also help explain x86 persistence. x86-64, ARM, and RISC-V differ but share arithmetic, data movement, and control-flow categories. RISC-V is an open ISA developed at Berkeley and used in embedded processors and accelerators as well as education, connecting those common concepts to a practical processor example.

**Checking points:** Distinguish all forms, compiler work, historical context, shared ISA categories, and the example's motivation; simplicity does not imply one instruction per computation.

</details>

#### Recall Q07 · Extensibility and generality

Why reserve encoding bits and parameterize storage, CPU, and I/O counts? Explain general-purpose design, the accelerator trade-off, and the limited meaning of asynchronous operation here.

<details><summary>Show solution</summary>

They leave room for future features and scale while preserving existing pattern meanings; immediate optimality and long-term compatibility can conflict. General-purpose design avoids arbitrary special meanings for ordinary data and supports numeric/bit operations and fine-grained addressing. An accelerator can sacrifice some generality for particular computations. Asynchronous operation is introduced as avoiding excessive dependence on a fixed component-speed model, not as a circuit protocol.

**Checking points:** Explain extension space, its limits, the generality trade-off, and the bounded asynchronous claim.

</details>

#### Recall Q08 · Scaling graphs and multicore

How should equal vertical steps on a log axis and the 2010 column be read? Explain why transistor growth does not imply proportional frequency or single-task speed, and state multicore's latency/throughput conditions.

<details><summary>Show solution</summary>

Equal log-axis steps represent equal factors; the 2010 column is extrapolated. Moore's transistor-count trend differs from Dennard's speed/power-density expectation, whose limits include leakage and heat. The graph shows slower single-thread growth, not a complete stop. Extra cores can increase throughput with enough independent work and no bottleneck; one task's latency depends on whether it can be divided.

**Checking points:** Include extrapolation versus measurement, both scaling ideas, and single-task versus independent-work conditions.

</details>

### Apply and diagnose

#### Practice P01 · Evidence for three claims

Newly written synthetic practice transfers the storage distinction in [EX:ca_2025_2_midterm_q01 p.2]. Prerequisites are this unit's ISA, stored-program, and multicore explanations. Two processors implement the same ISA and store instructions/data in memory; B has two cores. (a) Must execution times match? (b) Can you infer access-path organization? (c) Contrast one indivisible one-second job with two independent one-second jobs on B. Assume equal per-core speed and no additional bottleneck.

<details><summary>Show solution</summary>

(a) No: implementations of the same semantics can differ. (b) No: memory representation does not specify access paths or cache organization. (c) The indivisible job still takes one second. The two independent jobs can ideally finish together in one second on two cores, versus two seconds sequentially on one core. Each job's service latency remains one second.

**Checking points:** Justify each conclusion separately; reduced batch completion time is not reduced individual service latency.

</details>

### Review plan

Explain the contract and state changes with Q01–Q04, then reconstruct Q05–Q08 without the figures. Use P01 to separate the evidence each claim needs before continuing to [[courses/computer_architecture/units/en/program-translation-loading|translation and loading]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-01-lecture-01|2026-09-01 · lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 · materials-only review]]
- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 · lecture notes]]

- [lec.01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.01.pdf): [[page_cache/computer_architecture/lec.01/page-011|p.11]], [[page_cache/computer_architecture/lec.01/page-014|p.14]], [[page_cache/computer_architecture/lec.01/page-015|p.15]], [[page_cache/computer_architecture/lec.01/page-016|p.16]], [[page_cache/computer_architecture/lec.01/page-019|p.19]], [[page_cache/computer_architecture/lec.01/page-020|p.20]], [[page_cache/computer_architecture/lec.01/page-021|p.21]], [[page_cache/computer_architecture/lec.01/page-023|p.23]], [[page_cache/computer_architecture/lec.01/page-024|p.24]], [[page_cache/computer_architecture/lec.01/page-025|p.25]], [[page_cache/computer_architecture/lec.01/page-026|p.26]], [[page_cache/computer_architecture/lec.01/page-027|p.27]]
- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-005|p.5]], [[page_cache/computer_architecture/lec.02/page-007|p.7]], [[page_cache/computer_architecture/lec.02/page-009|p.9]], [[page_cache/computer_architecture/lec.02/page-010|p.10]], [[page_cache/computer_architecture/lec.02/page-013|p.13]], [[page_cache/computer_architecture/lec.02/page-016|p.16]], [[page_cache/computer_architecture/lec.02/page-017|p.17]], [[page_cache/computer_architecture/lec.02/page-026|p.26]], [[page_cache/computer_architecture/lec.02/page-027|p.27]]
- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-006|p.6]]

- [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT · 22:25–23:07, 30:22, 36:16]]
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 03:13, 04:46–05:32, 07:20–11:44]]

- September 3 lec.02 is a materials-only review without a recording; operand classifications, history, extensibility, and the explicit state model do not establish exact spoken progress.
- Unclear September 8 wording at 03:55 and 08:20 remains unresolved. Context switching motivates register preservation, without specifying a complete OS policy.
- Gate figures are simplified models; the NOR outline on p.20 is not reliable functional evidence. Detailed transistor circuits are outside scope.
- The 2010 table contains extrapolations, not measured product records. Ideal multicore throughput requires independent work and no limiting bottleneck.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.

- [[exam_questions/ca_2025_2_midterm_q01|Existing question preview · Q01]]


---

[[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/program-translation-loading|Next: Program Translation, Linking, and Loading →]]
