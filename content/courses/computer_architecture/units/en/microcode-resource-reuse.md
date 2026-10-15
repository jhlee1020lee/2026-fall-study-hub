---
title: "Microcode, Resource Reuse, Pipelining, and Hazards"
description: "Questions and worked answers connect microcoded resource reuse with pipeline timing, data and control hazards, and branch policy."
course: "computer_architecture"
unit_id: "microcode-resource-reuse"
lang: "en"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["lec 06.pdf", "lec 07.pdf", "lec 08.pdf", "lec 09.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-29-lecture-05"]
---

## Microprograms and next-state selection

When an instruction takes several cycles, the controller must determine both what the datapath does now and which control state follows. A large ROM addressed by opcode and current state can repeat next-state information even where the transition does not depend on the opcode. A **microprogram** expresses the control sequence as a separate small program. The **μPC**, or microprogram counter, addresses a microinstruction in the μprogram ROM. It is distinct from the architectural PC, which identifies an instruction in the user's program.

In [computer_architecture:NM002 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015), follow the μPC into the address input of the μprogram ROM. The output supplies datapath control and an `AddrCtl` selection for the next μPC. The incrementer and dispatch ROMs generate different candidates for that next address.

| AddrCtl | Next μPC selection | Purpose |
|---|---|---|
| 0 | 0 | Return to the common starting state |
| 1 | Dispatch ROM 1 output | First opcode-dependent dispatch |
| 2 | Dispatch ROM 2 output | A later opcode-dependent dispatch |
| 3 | μPC + 1 | Continue to the next microinstruction |

In this figure, Dispatch ROM 1 maps the R-format opcode `000000` to address `0110`, `jmp` opcode `000010` to `1001`, and `beq` opcode `000100` to `1000`. Both `lw` (`100011`) and `sw` (`101011`) initially map to `0010`. Dispatch ROM 2 separates them into `0011` and `0101`. A shared address-calculation sequence can therefore precede different load and store operations.

For example, μPC=5 with `AddrCtl=3` selects μPC=6. Dispatching an R-format instruction also selects address 6 in this particular diagram, but the same number in another FSM need not mean the same operation. This is a legacy example with a 6-bit opcode, not a RISC-V 7-bit opcode table. The [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] discusses the incrementer at 39:27 and distinguishes the different FSM examples at 43:18 and 44:26. The earlier multi-cycle control sequence connects to the [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 Computer Architecture lecture notes]]. Microprogramming alone does not establish a particular area saving or speed improvement.

## Sharing an ALU over time and preserving the instruction

### Different operations on the same hardware

In a single-cycle datapath, instruction arithmetic and sequential-PC calculation may be needed in the same cycle, motivating a separate PC adder alongside the ALU. A multi-cycle implementation can separate these operations in time. During IF, the ALU receives PC and 4. During EX, it receives register operands or an immediate. Input **multiplexers**, or muxes, choose the values, while control determines the selection and operation for each cycle. One physical ALU does not perform two independent additions simultaneously. [computer_architecture:NM002 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020); [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] 45:27 and 47:25.

Consider an explanatory example in a model with 4-byte instructions. PC is `0x3000`, and instruction K at that address adds 10 and 12. The IF calculation is `0x3000 + 4 = 0x3004`; the later EX calculation is `10 + 12 = 22`. These results have different meanings and destinations. The first is the next instruction address; the second is K's arithmetic result. PC+4 follows from this instruction-length assumption, not from a claim that every RISC-V instruction is four bytes long.

The legacy datapath figures in L06 and L07 also show 16-to-32-bit sign extension. Those are widths of that example, not the 32-bit instruction-word and 64-bit register-data widths of the RV64 model.

Sharing can eliminate duplicated arithmetic hardware, but it requires muxes, control, and intermediate storage. It can also introduce more cycles or a longer path through input selection. Saving an adder and reducing program execution time are therefore separate questions.

### An early PC update must not replace the current instruction

Suppose instruction memory produces its output combinationally from its address. Updating PC early to `0x3004` can change the memory output to the next instruction. If K's decode and register reads still depend directly on that output, the identity of the instruction being executed can change underneath the datapath.

The **Instruction Register (IR)** captures fetched instruction bits and creates a storage boundary. In [computer_architecture:NM002 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022), the important connection is the IR after the memory output. Once the IR has captured K and holds it, decode continues to see K even when PC changes. In the example, the IR stores K's bit pattern, not the address `0x3000` itself. This explains the need to distinguish capture from hold; the diagram does not establish a particular latch active level or setup time.

The [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] explains the changing instruction output at 48:04. The wording at 49:03 and 49:43 mixes PC and instruction terminology and should not define the IR's contents literally. Calling those contents instruction bits here is an interpretation of the material's wiring.

## Shared memory and the lifetime of intermediate values

Memory, like the ALU, can be shared over time between instruction fetch and data access. In the multi-cycle diagram in [computer_architecture:NM002 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023), the memory address is selected from PC or a computed data address. Values that must survive across cycles need storage of their own.

| Internal storage | Preserved value | Why it must survive |
|---|---|---|
| IR | Fetched instruction bits | Decode must retain its instruction when PC and memory output change |
| MDR | Data read from memory | The value must reach a later writeback |
| A, B | Operands read from the register file | Later arithmetic or a store may need them |
| ALUOut | An ALU result or address | A later memory access or writeback uses it |

A load must preserve its effective address until memory access, then preserve the returned data until register writeback. A store must preserve both the location and the value until the memory operation. Addresses and data are both bit vectors, but they are not interchangeable. These storage elements are microarchitectural state, distinct from programmer-visible general-purpose registers.

This reuse exploits different cycles of one instruction. In a pipeline, IF of one instruction and MEM of another can occur in the same cycle. A single-port memory cannot simply satisfy two simultaneous accesses without a mechanism to handle the conflict. Sharing that works in a sequential multi-cycle diagram does not automatically work in an overlapping pipeline. The 2026-09-29 lecture at 51:38 motivates overlap by pointing to idle stages; its shared-memory discussion at 52:36 does not supply a complete arbitration or enable schedule.

## Placing complexity in the datapath or microcontroller

A complex instruction can be implemented in different ways. A datapath with more specialized functions can perform substantial work when invoked by a short microprogram. A simpler datapath can compose its basic operations through a longer sequence, making the microprogram and its sequencing more elaborate. A microprogrammed loop also needs internal state, such as a loop counter. Such state belongs to the internal μISA or controller and is not automatically a programmer-visible register. [computer_architecture:NM002 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024); [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] 53:36–54:28.

The material contrasts a complex datapath with simple microcode, a simple datapath with complex microcode, and the RISC ideal of simple datapath and simple control. Compare hardware area and delay, microinstruction count, control storage, and internal state. This is a framework for locating implementation complexity, not a universal ranking of RISC and CISC or a description of every modern processor.

## Pipeline latency and throughput

### Overlap preserves each task's internal order

A **pipeline** divides a task into stages and overlaps different tasks. If washing, drying, folding, and storing each take 30 minutes, one laundry load has a **latency** of 120 minutes. With a separate resource for each stage, completed loads can then emerge every 30 minutes. The steady **throughput** is four times that of sequential processing, although the first load's latency has not decreased.

If drying takes 60 minutes, that bottleneck limits completion spacing to 60 minutes. Two dryers, started alternately, can accept a new load every 30 minutes again, but this improvement uses an additional resource. It does not remove the order between washing and drying for any one load. The pipeline foundations and data hazards below are a materials-based study of L07 and L08, not a reconstruction of speech on an unrecorded class date. [computer_architecture:NM005 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006); [computer_architecture:NM005 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007); [computer_architecture:NM005 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008).

Let total combinational delay be T, stage-boundary latch overhead be S, and the number of equally balanced stages be k. With enough independent work, the idealized model gives:

| Quantity | Unpipelined | k-stage pipeline |
|---|---|---|
| Clock period | T + S | T/k + S |
| Steady throughput | 1/(T + S) | 1/(T/k + S) |
| Latency of one task | T + S | T + kS |
| Cost with logic cost G and boundary-storage cost L | G + L | G + kL |

For positive S, increasing k cannot raise throughput beyond the limiting value 1/S. Latency and storage cost increase. With unbalanced stages, the slowest stage delay replaces T/k in the clock constraint. [computer_architecture:NM005 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011); [computer_architecture:NM005 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012).

### The 800ps model and finite fill/drain

L07 assigns IF, ID, EX, MEM, and WB delays of 200, 100, 200, 200, and 100ps, totaling 800ps. The separate L06 multi-cycle example uses 200, 50, 100, 200, and 50ps, totaling 600ps. Combining one example's register-file delay with the other's ALU delay describes neither model. The L07 figure also allows register-file writing and reading in different halves of the same clock. That assumption must not silently be transferred to the later no-forwarding hazard calculation. [computer_architecture:NM005 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015); [computer_architecture:NM002 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005).

Ignoring latch overhead and hazards in L07, the pipeline clock is 200ps. Traversing five stages gives one instruction a latency of 1000ps, longer than the 800ps single-cycle latency. Once full, however, the pipeline completes an instruction every 200ps. The steady throughput improvement is 800/200=4, not automatically five just because there are five stages.

Starting with an empty pipeline and counting through the last WB, N consecutive instructions require N+4 cycles. The first completion takes five cycles; the remaining N−1 completions occur one per cycle. For N=3, the pipelined execution takes 7×200=1400ps, while sequential single-cycle execution takes 3×800=2400ps. Speedup is 12/7, approximately 1.714. This finite execution, including fill/drain, is different from the steady factor of four. [computer_architecture:NM005 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016).

A multi-cycle design must be evaluated using both its shorter clock and its instruction-dependent cycle counts. With average CPI c and period t, time per instruction is ct; a shorter clock alone does not guarantee better throughput. Likewise, pipeline latency and throughput must be compared separately. These distinctions supply the reasoning demanded by performance judgments in the recalled examination, without defining the current examination scope. [EX:ca_2025_2_midterm_q08 p.2] [EX:ca_2025_2_midterm_q09 p.2]

For a comparison on common terms, write instruction i’s microcoded multi-cycle latency as cᵢtₘ and its average completion spacing as c̄tₘ. A hazard-free five-stage pipeline has latency 5tₚ and steady completion spacing tₚ; with hazards, its average spacing becomes CPI×tₚ. Multi-cycle design can tailor the steps needed by each instruction while reusing resources. Pipelining reduces completion spacing by overlapping instructions. Neither a microcode ROM and dispatch mechanism nor hardwired control alone determines tₘ, tₚ, or c̄, so the implementation labels do not establish a universal winner in latency, clock speed, or throughput. [EX:ca_2025_2_midterm_q16 p.8]

## Data and control travel with their instruction

### The destination must cross pipeline boundaries too

IF/ID, ID/EX, EX/MEM, and MEM/WB registers carry an instruction's intermediate information between stages. Instruction bits or required fields, PC-related values, operands and immediates, ALU results, store data, load data, and destination-register numbers must survive until their respective uses. A value need not be used in every intervening stage to require preservation across it.

Read the L07 legacy-ISA example `lw $10, 20($1)` followed by `sub $11, $2, $3` as a timeline. The register spelling belongs to that example; this is not code rewritten into RV64 syntax.

| Cycle | lw | sub |
|---|---|---|
| 1 | IF | — |
| 2 | ID | IF |
| 3 | EX: calculate address | ID: read operands |
| 4 | MEM: read load data | EX: subtract |
| 5 | WB: write $10 | Pass through MEM stage |
| 6 | — | WB: write $11 |

Passing through the MEM stage does not make `sub` perform a memory write. At cycle 5, the load's destination is still `$10`. Taking the destination from a different instruction currently being decoded would pair the load's value with the wrong register number. In the cycle-3 diagram in [computer_architecture:NM005 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030), `sub` is being decoded on the left while `lw` executes farther right. An operation view follows one instruction through time; a resource view shows simultaneous stage occupancy in one cycle. They describe the same execution. [computer_architecture:NM005 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027).

### Control has the same lifetime as its data

Driving an older instruction in MEM directly with the control decoded for the current instruction in ID creates the same ownership error. One design decodes once in ID, separates EX, MEM, and WB controls, and carries them alongside the data. EX controls are consumed where needed; MEM and WB controls continue through EX/MEM, and the remaining WB controls pass through MEM/WB. `RegWrite` and the writeback-result selection must remain aligned with the corresponding result and destination. [computer_architecture:NM005 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052).

Another design carries the relevant instruction fields and decodes locally in each stage. Both designs must preserve instruction ownership. Decode-once transports decoded control; local decode transports instruction information and uses stage-local decoders. The diagram alone does not establish a universally smaller or faster choice.

Real pipelines face three departures from the simple ideal: instructions do different work, tasks depend on one another, and stage delays are unequal. These motivate multifunction stages and selection, dependence handling, and stage regrouping or added resources. A **structural hazard**, such as two simultaneous requests for one memory port, has a different cause from a **data hazard**, such as requesting an unfinished value. A register file may also be shared by placing reads and writes at different times within a cycle, so “one dedicated resource per stage” is an incomplete design rule.

## When a dependence becomes a hazard

**RAW**, read after write, is a true dependence: a later instruction needs an earlier result. If an instruction calculates r3 and a later one uses r3 to calculate r5, the later calculation needs the new r3. **WAR**, write after read, requires an earlier read of an old value to occur before a later overwrite. **WAW**, write after write, requires writes to the same destination to retain their final program order. More than one dependence can exist between a pair of instructions.

A dependence is an ordering requirement in the program. A hazard occurs when an implementation's timing threatens that requirement. In an in-order, fixed five-stage model with all reads in ID and all writes in WB, a later write does not overtake an earlier read or write. WAR and WAW dependences therefore do not automatically produce WAR or WAW stalls in this model. Explaining that timing relationship is the depth needed for the recalled examination's WAR item. [EX:ca_2025_2_midterm_q10 p.2]

Now consider L08's model without forwarding, where a producer's WB must finish before the consumer can read its new value in ID. Define adjacent instructions to have distance 1 and instructions with one intervening instruction to have distance 2. Since ID cannot read a newly written value in the same cycle as WB in this model, RAW distances 1, 2, and 3 can cause hazards; distance 4 is safe. A register file that writes early and reads late within the same cycle has a different boundary. Do not combine L07's half-clock register file with this L08 stall count. [computer_architecture:NM006 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013).

Matching bit fields is not enough. The producer must actually write a register, the consumer must actually use that field as a source, and writes to `x0` must be excluded. R/I arithmetic, `lw`, `jal`, and `jalr` can produce register results in this model. Stores and branches do not produce GPR results. Source uses include R/I operands, a load's base, a store's base and data, branch operands, and a `jalr` base. `jal` has no GPR source. Treating every bit field at a fixed position as a source regardless of opcode creates false hazards.

## A stall holds only the work that must wait

If the required value is not available in the register file, the consumer must wait. A **stall** holds PC and upstream pipeline registers so the consumer and younger work do not advance. The position that the consumer would enter in EX receives a **bubble**, a slot with no valid operation. Its `RegWrite` and `MemWrite` controls must be disabled. Downstream stages, including the producer, continue advancing so the missing value can become available. Freezing every stage would also freeze the result being awaited.

The following explanatory timeline restates L08's no-forwarding model, with no same-cycle read of a new RF write, using the producer's IF as t0. The adjacent consumer reads that producer's result.

| Cycle | Producer | Consumer |
|---|---|---|
| t0 | IF | — |
| t1 | ID | IF |
| t2 | EX | Wait in ID |
| t3 | MEM | Wait in ID |
| t4 | WB | Wait in ID |
| t5 | Complete | ID: read the new value |
| t6 | — | EX |
| t7 | — | MEM |
| t8 | — | WB |

The three waits preserve the consumer rather than discard it. The original figure in [computer_architecture:NM006 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018) includes an earlier instruction and uses a different time origin; the critical relationship is the producer's WB followed by the consumer's successful ID. A detector can compare ID's two actual sources against valid destinations in EX, MEM, and WB, then OR the six matches. Each match also needs the write-enable and non-`x0` qualifications.

In steady accounting, N useful instructions with S additional stall cycles give CPI=(N+S)/N=1+S/N and IPC=N/(N+S). For an explanatory example with N=100 and S=25, CPI=1.25 and IPC=0.8. Counting from an empty five-stage pipeline through the last WB adds four fill/drain cycles: 129 cycles and IPC=100/129. A single stall can resolve several dependences simultaneously, so penalties must not be added independently for every dependence.

## Forwarding and the load-use timing boundary

**Forwarding** sends an already computed result directly to its consumer before register-file writeback. It helps when the result exists but lacks a path to the consumer. It cannot produce a value before its computation has finished.

When several in-flight destinations match one source register, the consumer needs the youngest older writer: the closest preceding producer in program order. L08 gives the nearer EX match priority over older MEM and WB matches. If the nearer producer is a load whose result is not ready, selecting an older available value is incorrect. The consumer must wait for the right value. [computer_architecture:NM006 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042).

The stage table in [computer_architecture:NM006 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043) distinguishes **when an operand is consumed** from **when a result is produced**.

| Instruction class | Actual operand use | Result production |
|---|---|---|
| R/I arithmetic and logic | EX | EX |
| Load | Base/address calculation in EX | MEM |
| Store | Address in EX; store data in MEM | No GPR result |
| Conditional branch | EX | No GPR result |
| jal | No GPR source | Link result in EX |
| jalr | EX | Link result in EX |

An ALU producer completing EX at the end of t2 can forward to the next consumer's EX in t3. A load calculating its address in t2 EX and receiving data only at the end of t3 MEM cannot supply a consumer that needs the value at the beginning of t3 EX. Moving the consumer's EX to t4 requires one bubble. This is the **load-use hazard**. Detecting the match in ID and consuming the operand in EX are different events.

The basic condition checks whether a real ID source matches the destination of an EX load and whether `MemRead_EX` is asserted. Omitting the source's use time, however, can misclassify stores. A store's address base is needed in EX, while its store data is used in MEM. With a suitable path forwarding store data into MEM, the same register dependence may need a different number of stalls from an EX-operand dependence. “Any use immediately after a load always needs one stall” is not a sufficient rule.

For a trace, first identify each instruction's sources and destination, align production and consumption stages, and then apply the available bypass paths and RF timing. Continue through the last instruction's WB; the end of a printed grid is not necessarily the end of execution. The recalled examination's dependence identification, forwarding trace, and stall discussion demand this reasoning. Its printed cycle 1–8 grid can require extension, and unspecified same-cycle RF or store-data forwarding behavior must be stated as assumptions. [EX:ca_2025_2_midterm_q15 p.7]

## Static scheduling and deeper pipelines

### Reading the operand relationships in a loop

The MIPS-style teaching loop in L08 starts with `j=i-1` and checks `j>=0` and `v[j]>v[j+1]`. In the sequence from NM006 p.33 below, `$s0` holds i, `$s1` holds j, and `$a0` is the array base address. The dots stand for an unprovided loop body; the sequence must not be read as a RISC-V program.

```asm
addi $s1, $s0, -1
for2tst: slti $t0, $s1, 0
bne $t0, $zero, exit2
sll $t1, $s1, 2
add $t2, $a0, $t1
lw $t3, 0($t2)
lw $t4, 4($t2)
slt $t0, $t4, $t3
beq $t0, $zero, exit2
.........
addi $s1, $s1, -1
j for2tst
exit2:
```

The initial `addi $s1, $s0, -1` subtracts one from i in `$s0` and initializes j=i−1 in `$s1`. It precedes `for2tst`, so repetition does not reinitialize j to i−1. At `for2tst`, `slti $t0, $s1, 0` sets `$t0` to 1 when j<0 and to 0 otherwise. The following `bne $t0, $zero, exit2` exits when that flag is nonzero. A negative j therefore leaves the loop instead of proceeding to the array condition; only a nonnegative j proceeds to the next comparison.

The two-bit left shift in `sll $t1, $s1, 2` forms the byte offset 4j for 4-byte word elements. Then `add $t2, $a0, $t1` adds that offset to the array base in `$a0`, making `$t2=base+4j`, the address of v[j]. The two `lw` instructions use the same base register `$t2` with offsets 0 and 4 to access adjacent words.

The first load reads v[j], the second reads v[j+1], and the comparison tests `$t4 < $t3`, or v[j+1]<v[j]. That is the original condition with its operands expressed in the opposite order. Swapping the comparison operands would change its meaning. [computer_architecture:NM006 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033).

Only when v[j]>v[j+1] is true does `slt $t0, $t4, $t3` produce 1. The following `beq $t0, $zero, exit2` exits when the comparison produces 0, meaning v[j]≤v[j+1]. Execution reaches the dotted body only after both guards succeed. The dots do not establish any swap instructions. After that omitted body, `addi $s1, $s1, -1` decrements j, and `j for2tst` repeats the guard beginning with the negative-index test. Thus the visible structure is initialization→guard→address and value comparison→body→decrement→guard, while the body's actual work remains unknown.

In the no-forwarding annotations, each of six adjacent RAW pairs receives three stalls: `addi→slti`, `slti→bne`, `sll→add`, `add→first lw`, `second lw→slt`, and `slt→beq`. These are annotations at the identified points, not a complete execution-cycle count including the omitted loop body and branch outcomes. [computer_architecture:NM006 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034).

**Static scheduling** lets a compiler place independent instructions in otherwise waiting positions while preserving program meaning. An **interlock** detects a hazard in hardware and waits during execution. Runtime stall, flush, and forwarding behavior is distinct from rearranging instruction order statically.

In the material's MIPS R2000 **load delay slot**, the instruction immediately after a load must not consume its result. The minimum required distance is two, and the example places a `nop` between the second load and `slt`. A safely movable independent instruction can do useful work there; otherwise the `nop` preserves the required spacing. This is a constraint on load-result availability, distinct from the branch delay slot below. [computer_architecture:NM006 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047).

Page 47 retains the same initialization, two guards, address calculation, and post-body decrement followed by `j for2tst`. Its added `nop` fills the load-use slot between the second `lw` and the `slt` that consumes its result. Neither the dotted body nor additional branch delay-slot instructions can be recovered from that figure.

### Shorter clocks do not remove dependent latency

**Superpipelining** splits stages further. In the material's 32-bit-adder example, EX1 computes the lower 16 bits and carry, while EX2 processes the upper 16 bits with that carry. The earlier low result and later high result must be stored and aligned as parts of the same operation to form one complete 32-bit result. [computer_architecture:NM006 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049).

Shorter stages may reduce the clock period, but a dependent instruction can then wait more cycles for the complete result. Additional stage-register overhead and branch penalties also matter. The ability to overlap internal execution while preserving ISA-visible sequential results does not permit ignoring dependencies. Comparing pipeline benefits and limitations therefore connects throughput to latency, hardware and control costs, and hazard handling, as demanded by the recalled examination's comparison item. [EX:ca_2025_2_midterm_q16 p.8]

## PC dependence and the next fetch

Control flow also has producers and consumers. Every instruction fetch consumes PC; the preceding instruction determines the next PC. A **control dependence** can therefore be viewed as a data dependence on the next instruction address. The [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|undated lecture (computer_architecture:NT002)]] uses the fact that PC is a register at 05:10 to explain this connection. The L09 material from this section onward belongs to course study but exceeds the current midterm cutoff of L08 plus Lab1.

This undated transcript is text compared with the materials without verified original audio, not a complete verbatim recovery. Missing speech, the actual class date, and speaker identities have not been recovered.

The conservative L09 model determines next PC in ID for ordinary R/I instructions, loads, and stores, and in EX for conditional branches, `jal`, and `jalr`. Fetch needs that address in IF. [computer_architecture:NM007 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005). Without prediction, if non-branch h occupies IF at t0 and ID at t1, the next instruction i cannot fetch until t2. Repeating that rule gives j's IF at t4 and k's at t6. Even non-branches leave idle fetch cycles. The stage in which next PC becomes known is a datapath assumption, not an immutable ISA rule.

Selecting the sequential PC in advance can avoid this wait. **Speculation** proceeds using a choice that has not yet been confirmed. Here the prediction is PC+4 in the four-byte-instruction model. A correct choice permits the work to be retained. An incorrect choice requires preventing wrong-path instructions from changing architectural state.

## Branch resolution, redirect, and flush

Knowing in ID that an instruction is a branch does not establish both its outcome and target. The undated lecture, computer_architecture:NT002, emphasizes this distinction at 17:37. The following timeline uses L09's model: branch h resolves taken at the end of EX, with k as the correct target instruction. Instructions i and j were fetched incorrectly along the sequential path.

| Cycle | h | i | j | k |
|---|---|---|---|---|
| t0 | IF | — | — | — |
| t1 | ID | IF | — | — |
| t2 | EX: taken resolved at end | ID | IF | — |
| t3 | MEM | Bubble in EX position | Bubble in ID position | IF |
| t4 | WB | Bubble in MEM position | Bubble in EX position | ID |
| t5 | Complete | Bubble in WB position | Bubble in MEM position | EX |
| t6 | — | — | Bubble in WB position | MEM |
| t7 | — | — | — | WB |

**Redirect** changes the fetch address to k. **Flush** invalidates i and j. Fetching k at t3 does not instantly turn the older wrong-path positions into useful work. Their bubbles advance without causing register or memory writes. The branch h and older correct instructions are not discarded with them. [computer_architecture:NM007 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022); [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|undated lecture (computer_architecture:NT002)]] 23:27.

A stall preserves an instruction to continue later; a flush invalidates an instruction that must not execute. The two bubbles here correspond to two wrong fetches and a two-cycle penalty in this design. They do not establish a two-cycle penalty for all processors. Likewise, “no penalty for a correct prediction” assumes no other data or resource hazard.

## Misprediction probability, CPI, and IPC

The L09 profile gives a 20% control-flow fraction, a 50% taken rate for forward branches, a 90% taken rate for backward branches, and a 70% overall taken rate for control flow. Forward and backward refer to target-address direction, not earlier and later execution times. Without the relative numbers of the two kinds, 50% and 90% alone do not determine 70%; use the overall 70% as a separately supplied value. [computer_architecture:NM007 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012). [computer_architecture:NM007 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030); [computer_architecture:NM007 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031).

With predict-not-taken, the sequential choice is correct for the 80% non-control-flow instructions and for the 30% not-taken portion of control flow. Thus:

- Correct-guess probability = 0.8 + 0.2×0.3 = 0.86.
- Wrong-guess probability = 0.2×0.7 = 0.14.
- With ideal CPI=1, no additional data hazards, and two cycles per misprediction, CPI = 1 + 0.14×2 = 1.28.
- IPC = 1/1.28 = 0.78125, approximately 0.78.

Applying those proportions to 100 useful instructions gives 86 correct predictions and 14 incorrect ones. The latter add 28 cycles, for 128 cycles in steady accounting. Fill/drain is excluded. The quantity 0.28 is additional cycles per instruction; the IPC decrease is 1−0.78125=0.21875. At the same instruction count and clock period, execution time rises by 28% while throughput falls by 21.875%. These percentages describe different quantities.

The undated lecture retains numerical expressions at 14:56, 26:58, 27:42, and 28:41 that conflict with these probabilities or leave the quantity ambiguous. The calculation above is an explicit mathematical explanation using the material's 20%, 70%, and two-cycle model, not a corrected quotation of that speech. Excluding data hazards for this calculation also does not mean declaring the program free of data dependences.

Separate three factors when considering improvements. Control-flow frequency belongs to the program; prediction accuracy determines the fraction guessed incorrectly; resolution and redirect timing help determine the implementation's loss per wrong guess. Better prediction reduces the number of mistakes, while earlier resolution can reduce each mistake's cost. The implementation-dependent discussion at 27:42 connects to this distinction. Detailed predictor algorithms require evidence beyond these sources. Simplifying a branch whose condition is known at compile time additionally requires confirming the actual condition and preserving relevant side effects; an uncertain spoken variable value does not establish an always-true branch.

## The architectural meaning of a branch delay slot

The material's MIPS R2000 **branch delay slot** requires the PC+4 instruction immediately after a branch to execute whether or not the branch is taken. The following instruction—the second successor—is at the target if taken or PC+8 if not taken. This contract differs from flushing the speculatively fetched sequential instructions in the previous model. In [computer_architecture:NM007 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032), observe that the instruction immediately after the branch retains its place, while an early branch decision selects the subsequent fetch.

Moving an instruction into the slot requires preserving program meaning on both taken and not-taken paths. A store needed on only one path, or an operation whose operands are not ready, cannot be moved there casually. If no suitable instruction exists, the compiler uses a `nop`. The material's approximately 80% slot-filling statement is a historical claim in that discussion, not a guarantee for every program or a measure of current compiler performance. Filling the slot with useful work can approach ideal IPC=1 when there are no other hazards, but counting a `nop` as useful work inflates performance.

A load delay slot constrains the spacing of a load and its consumer. A branch delay slot specifies the execution of the instruction after a branch. Both expose constraints to the compiler, but their meanings differ. The related recalled-examination item reinforces the distinction between an ISA-visible rule and a hardware bubble; it does not add L09 to the current midterm scope. [EX:ca_2025_2_midterm_q17 p.8]

## Architectural effects and cache state under speculation

Flushing wrong-path instructions must prevent incorrect architectural register or memory updates. That does not by itself prove that all traces of execution disappear. A **microarchitectural effect**, such as which data occupies the cache, can affect the timing of later accesses. Restoring architecturally correct state and eliminating observable internal effects are different requirements.

The permission-condition example in [computer_architecture:NM007 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033) asks what effects an access under a predicted condition might leave. The [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|undated lecture (computer_architecture:NT002)]] continues with cache state at 35:17–35:35. The supported principle is that canceling architectural results does not remove the need to examine cache and other internal state separately. Detailed hit/miss behavior and timing observation connect to subsequent cache study.

That conditional example alone does not specify compiled branch polarity, an actual permission-bypass mechanism, or the extent of data an attacker could obtain. The names Spectre and Meltdown in the discussion also do not make their distinct mechanisms interchangeable. This pipeline example neither establishes a shared vulnerability in every processor nor certifies the security state of current products.

## Recall and Practice

### Review sequence

Explain resources and saved values with Q01–Q05, then calculate finite execution time with Q06–Q09 and P01. For Q10–Q18 and P02, write producer→consumer relations and cycle traces before checking solutions. Use Q19–Q24 and P03–P04 as supplementary study beyond the cutoff, checking PC resolution, flushes, and probability units in that order.

### Microcode and resource reuse

#### Recall Q01 · μPC and dispatch

Connect the roles of μPC, μprogram ROM, incrementer, dispatch ROMs, and `AddrCtl`. With μPC=5, find the next addresses for `AddrCtl=0` and `3`, the R-format target for `1`, and explain how the two dispatches handle `lw` and `sw`.

<details><summary>Show solution</summary>

The μPC addresses a microinstruction, rather than a user instruction. The μprogram ROM supplies datapath control and next-address selection; the incrementer forms μPC+1, while dispatch ROMs provide opcode-dependent addresses. `AddrCtl=0` selects 0 and `3` selects 6; `1` selects ROM 1 and `2` selects ROM 2. ROM 1 sends R-format `000000` to `0110`, `jmp` to `1001`, `beq` to `1000`, and both `lw` and `sw` to `0010`. ROM 2 separates `lw→0011` from `sw→0101`, permitting a shared address-calculation sequence before different operations. These six-bit opcodes and state addresses belong to this example; address 6 need not mean state 6 in a separate RISC-V FSM. The printed `0110` remains distinct from uncertain 0,1,0 speech at 41:27. The μPC-indexed ROM explanation likewise does not reconstruct the lookup-input wording at 37:51.

Checking points: Check all four selections, architectural PC versus μPC, the common and separate load/store paths, and the distinct opcode namespace.

Sources: [L06 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014) · [L06 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015)

</details>

#### Recall Q02 · Two calculations on one ALU

In a four-byte-instruction model, PC=`0x3000` and the current instruction computes 10+12. Give the IF and EX inputs, results, and purposes. Why can both inputs not remain fixed to the RF, and what costs and width distinctions accompany reuse?

<details><summary>Show solution</summary>

IF selects PC and 4 to form next address `0x3004`; EX selects 10 and 12 to form arithmetic result 22. Fixed RF inputs cannot select PC and 4, so input muxes and stage-specific control are required. Each result must survive until its use; one ALU does not perform both additions simultaneously. Reduced adder duplication trades against mux delay, storage, control, and cycle costs. PC+4 assumes four-byte instructions here. The L06/L07 16-to-32-bit immediate example must remain separate from RV64 32-bit instructions and 64-bit data.

Checking points: Distinguish address `0x3004` from data 22, and explain selection, preservation, and timing costs.

Sources: [L06 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020)

</details>

#### Recall Q03 · Early PC update and the IR

After fetching instruction K at PC=A, the processor changes PC to A+4 before K finishes. With combinational instruction memory, what does decode see with and without an IR? Would storing address A in the IR solve the problem?

<details><summary>Show solution</summary>

Without an IR, the changed PC propagates to memory and can replace the opcode and operand fields being decoded with those of the next instruction. The IR captures K’s instruction bits fetched from A, not address A, and holds them through K’s remaining stages. Decode therefore retains K despite the changed memory output. This establishes the storage boundary, not a particular latch active level or setup time. The transcript’s mixed PC/IR wording is not a precise definition of the stored value.

Checking points: Check the propagation path, instruction-bit capture and hold, and the distinction between an address and its fetched instruction.

Sources: [L06 p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021) · [L06 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022)

</details>

#### Recall Q04 · Lifetimes of intermediate values

What do IR, MDR, A, B, and ALUOut preserve? Explain address/data lifetimes for a load and a store, then decide whether multi-cycle reuse of one memory also solves simultaneous pipeline IF/MEM access.

<details><summary>Show solution</summary>

IR preserves instruction bits; MDR holds memory-read data; A and B hold RF operands; ALUOut holds an ALU result or effective address. A load needs its address through memory access and returned data through WB. A store needs both address and data through its memory write. These are internal execution states, distinct from programmer-visible GPRs. Sequential accesses in different cycles can share memory, but simultaneous IF and MEM requests from different instructions conflict on a single port. The September 29 preview does not establish complete pipeline teaching or control.

Checking points: Check all five storage roles, both load/store lifetimes, and sequential sharing versus simultaneous conflict.

Sources: [L06 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023)

</details>

#### Recall Q05 · Where complexity resides

Compare dedicated datapath hardware with a long μprogram on a simpler datapath for a complex instruction. Why might a loop counter be needed, and must it become an ISA register?

<details><summary>Show solution</summary>

Dedicated hardware can perform more work per invocation and shorten the control sequence, at an area, delay, and design cost. Reusing simpler hardware can increase micro-operation count, control storage, sequencing, and internal-state requirements. A looping μprogram may need a counter, but that is internal μISA state and does not automatically become a program-visible GPR. The material’s simple RISC datapath/control is another design direction. Compare latency, area, and control costs rather than ranking implementations by the presence of microcode.

Checking points: Compare both hardware and sequence costs; separate internal from architectural state.

Sources: [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)

</details>

### Pipeline timing and state

#### Recall Q06 · Throughput, latency, and cost

For four 30-minute laundry stages, give one-load latency and steady completion spacing. What changes with a 60-minute dryer, and what do two dryers recover? For balanced k-stage logic with delay T, boundary overhead S>0, logic cost G, and boundary cost L, give clock, latency, cost, and the throughput limit.

<details><summary>Show solution</summary>

Balanced laundry has latency 4×30=120 minutes and steady completion spacing 30 minutes. A 60-minute dryer makes one-load latency 150 minutes and bottlenecks spacing at 60 minutes. Alternating two dryers recovers a 30-minute acceptance/completion interval, while each load still dries for 60 minutes and hardware cost increases. Balanced logic has clock=T/k+S, task latency=T+kS, cost=G+kL, and rate=1/(T/k+S). The unpartitioned case has T+S and G+L; as k grows, rate approaches 1/S. With unequal stages, the slowest stage constrains the clock.

Checking points: Check first completion versus steady spacing, added resources, and the S-dependent rate limit, latency, and cost.

Sources: [L07 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006) · [L07 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007) · [L07 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008) · [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011) · [L07 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012)

</details>

#### Recall Q07 · An initially empty pipeline

Use L07 stage delays 200, 100, 200, 200, and 100ps, ignoring overhead and hazards. Compare the first instruction, three independent instructions, and steady throughput with single-cycle execution. Why must L06 delays 200, 50, 100, 200, and 50ps remain separate?

<details><summary>Show solution</summary>

L07 single-cycle time is the sum, 800ps. Pipeline clock is the maximum, 200ps, and first-instruction latency is 5×200=1000ps. From empty through last WB, N instructions take N+4 cycles: three take 7×200=1400ps, versus 2400ps sequentially, giving finite speedup 12/7≈1.714. Steady spacing is 200ps, so long-stream throughput improves by four. Five stages do not imply lower latency or fivefold speedup. L06’s 600ps total uses different component delays; mixing entries invents another model. L07’s half-clock RF assumption also differs from L08’s no-same-cycle-read no-forwarding model.

Checking points: Check the distinct meanings of 800, 200, 1000, and 1400ps, 12/7 and four, and the origin of N+4.

Sources: [L07 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015) · [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016) · [L06 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005)

</details>

#### Recall Q08 · Ownership in the load/SUB trace

The teaching’s `lw $10, 20($1)` is followed by `sub $11, $2, $3` without hazards. List stages through cycles 1–6 and identify the owner of cycle 5’s writeback value and destination. What besides data must pipeline registers preserve, and how do operation/resource views differ?

<details><summary>Show solution</summary>

The load follows IF1→ID2→EX3→MEM4→WB5; SUB follows IF2→ID3→EX4→MEM5→WB6. Cycle 5 must pair the load data with `$10`. SUB merely passes through its MEM position, retaining its ALU result and `$11` for WB6; it does not write memory. IF/ID, ID/EX, EX/MEM, and MEM/WB carry required instruction fields, PC-related values, operands/immediates, addresses/results, store/load data, and destinations until use. An operation view follows one instruction over time; a resource view shows simultaneous occupancy. Load EX and SUB ID in cycle 3 are the same event in either view.

Checking points: Check six-cycle timing, correct value/destination ownership, and stage occupancy versus a memory effect.

Sources: [L07 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-020) · [L07 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027) · [L07 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030)

</details>

#### Recall Q09 · Control travels with its instruction

Why is it unsafe to apply a new ID-stage store’s `MemWrite=1` directly to current MEM? Compare decode-once with local decode, then explain how real pipelines violate identical-work, independent-work, and balanced-stage ideals and how each issue is addressed.

<details><summary>Show solution</summary>

MEM holds an older instruction; applying the new store’s control would change that older instruction’s memory effects. Decode-once creates EX/MEM/WB controls in ID and carries them with their data: EX controls are consumed in EX, MEM/WB continue into EX/MEM, and WB continues into MEM/WB. Local decode instead transports required instruction fields and uses stage-local decoders. Neither is universally superior. Different instruction work needs multifunction stages and selection; dependences/resource conflicts need detection, waiting, forwarding, or extra resources; unequal delays motivate repartitioning. A single-port conflict is structural, whereas an unfinished operand causes a data hazard.

Checking points: Check instruction ownership, both decoding choices, and all three practical constraints with their corresponding responses.

Sources: [L07 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052) · [L07 p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-055)

</details>

### Data hazards and bypassing

#### Recall Q10 · Dependence versus hazard

For A: `r3←r1+r2`, B: `r5←r3+r4`, C: `r3←r6+r7`, identify RAW, WAR, and WAW relations. Must WAR/WAW cause stalls in a fixed in-order five-stage pipeline with all reads in ID and writes in WB? The connection to recalled Q10 (p.2) is explaining whether read/write ordering can actually create a WAR hazard. [EX:ca_2025_2_midterm_q10 p.2]

<details><summary>Show solution</summary>

A→B on r3 is RAW: B needs A’s new value. B→C on r3 is WAR: B must read before C overwrites. A→C on r3 is WAW: C must provide the final r3 value. Dependence is required program order; a hazard is a timing threat to it. In this fixed in-order model, C’s WB cannot overtake B’s ID or A’s WB, so WAR/WAW do not automatically cause stalls. For RAW, availability at the actual use time still matters.

Checking points: Identify each register/order relation and do not infer a hazard from dependence alone.

Sources: [L08 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-004) · [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013)

</details>

#### Recall Q11 · Actual sources and instruction distance

Assume no forwarding and no ID read of a new WB value in the same cycle. Is a consumer separated from its producer by one independent instruction hazardous? What about distances three and four? Include GPR uses/writes of R/I, load, store, branch, `jal`, `jalr`, and the `x0` condition.

<details><summary>Show solution</summary>

Adjacent instructions have distance one, so one intervening instruction gives distance two and satisfies L08’s distance≤3 condition. At distance three, WB and ID coincide and the consumer must still wait; distance four puts ID after WB and is safe. R/I arithmetic, loads, `jal`, and `jalr` can write a GPR; stores and branches do not. Actual sources include R/I operands, load base, store base/data, branch operands, and `jalr` base; `jal` has no GPR source. A match needs real `RegWrite`, opcode-specific source use, and exclusion of `x0`. Early WB write/late ID read would change the distance-three boundary.

Checking points: Check distance definition, equality’s RF assumption, instruction classes, and `x0`.

Sources: [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013)

</details>

#### Recall Q12 · What stalls and what advances

A producer runs from IF at t0 to WB at t4; its adjacent consumer arrives at ID at t2. With no forwarding and no same-cycle read of the new RF value, give the consumer’s successful ID through WB and bubble count. Explain what is held and the detector’s six comparisons.

<details><summary>Show solution</summary>

The consumer waits at t2, t3, and t4, then performs ID at t5, EX at t6, MEM at t7, and WB at t8. Hold PC and upstream instruction storage while inserting three EX bubbles with `RegWrite=0` and `MemWrite=0`. Downstream stages must advance so the producer can write at t4. Compare each of ID’s two actual sources against EX, MEM, and WB destinations: OR the six qualified matches. Each requires actual source use, a valid writer with `RegWrite`, and non-`x0`. A stall preserves its consumer; a flush discards wrong-path work.

Checking points: Check t5 restart, t8 completion, three bubbles, and continued producer progress.

Sources: [L08 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018) · [L08 p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-029) · [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031)

</details>

#### Recall Q13 · Accounting for stalls and finite execution

For 100 useful instructions, 25 additional stall cycles are observed. Find steady CPI/IPC and cycles/IPC from an empty five-stage pipeline through last WB. May separately estimated penalties for two dependences always be added?

<details><summary>Show solution</summary>

Steady accounting gives 100+25=125 cycles, CPI=125/100=1.25, and IPC=100/125=0.8. Empty-to-last-WB execution adds four fill/drain cycles: 129 cycles and IPC=100/129≈0.7752. One waiting interval can let multiple producers advance and resolve several dependences together. Thus pairwise penalties need not sum to actual S; count additional cycles in the schedule.

Checking points: Track useful instructions and cycles, and add the four fill/drain cycles exactly once.

Sources: [L08 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-032)

</details>

#### Recall Q14 · The youngest older writer

A consumer source matches an EX-stage load and an older MEM-stage ALU writer. The MEM value is ready but load data is not. Which value is required? Does EX→MEM→WB priority mean all values are produced in EX?

<details><summary>Show solution</summary>

The consumer needs the last preceding writer in program order: the nearer EX load. Using the ready MEM result would read an obsolete version. Wait until the load result can be supplied. EX→MEM→WB is matching-producer age priority, not a claim that all results exist in EX. ID-stage match detection also differs from actual operand consumption in EX or MEM. Apply actual-source and non-`x0` qualifications.

Checking points: First identify the required writer, then test readiness and the available path.

Sources: [L08 p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-037) · [L08 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042)

</details>

#### Recall Q15 · Production and consumption times

An ALU producer finishes at the end of t2 EX; a load produces data at the end of t3 MEM. What happens if the next instruction needs that value at the start of t3 EX? Also distinguish store base/data, branch, and `jal`/`jalr` use/production stages.

<details><summary>Show solution</summary>

The ALU value can forward to t3 EX. Load data does not exist at the start of t3 EX, so one bubble moves consumer EX to t4. Detect a real ID-source match with an EX load’s rd and asserted `MemRead_EX`, but also inspect the use time. R/I uses operands and produces results in EX; a load uses its base in EX and produces data in MEM. A store needs its base in EX and data in MEM, with no GPR result. A store-data bypass into MEM can therefore make adjacent load-to-store-data differ from an EX-use case. Branch operands are used in EX, with no GPR result. In this material’s model, `jal` has no GPR source and produces a link in EX; `jalr` both uses its source and produces its link in EX.

Checking points: Check the timing reason for one load-use bubble, the two store use times, and the instruction-class table.

Sources: [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043)

</details>

#### Recall Q16 · Loop comparison direction and RAW pairs

Explain the loop’s `slti`, two-bit `sll`, two `lw` operations, and `slt $t0, $t4, $t3`. List the six adjacent RAW pairs marked without forwarding. Do those markings determine the whole loop CPI?

Distinguish initialization from loop re-entry, then explain both `bne`/`beq` exits, the `base+4j` address, the decrement after the body, and the destination of `j for2tst`.

<details><summary>Show solution</summary>

After `j=i-1`, `slti` tests j<0 for the exit check; the two-bit `sll` forms offset 4j for four-byte elements. Adding the base yields v[j]’s address. The loads read v[j] and v[j+1], so `slt $t0, $t4, $t3` tests v[j+1]<v[j], equivalent to the original v[j]>v[j+1]. Reversing operands changes the condition. Marked RAW pairs are `addi→slti`, `slti→bne`, `sll→add`, `add→first lw`, `second lw→slt`, and `slt→beq`, each marked with three stalls in that no-forwarding model. The omitted body and branch outcomes prevent treating the marking sum 18 as whole-loop cycles or CPI.

Initialization `addi $s1, $s0, -1` sets j=i−1 once before `for2tst`. If `slti $t0, $s1, 0` produces 1, `bne $t0, $zero, exit2` exits for negative j before an array access. Otherwise, add the shifted offset 4j to `$a0` to form `$t2=base+4j`; offsets 0 and 4 then load the adjacent elements. A comparison result of 0 means v[j]≤v[j+1], so `beq $t0, $zero, exit2` exits. Only two successful guards reach the omitted body. After that body, `addi $s1, $s1, -1` decrements j and `j for2tst` returns to the negative-index test. Returning after initialization preserves the decremented j rather than resetting it to i−1. The omitted body cannot be assumed to perform a swap.

Checking points: Check the negative-index test, 4j, comparison direction, all six pairs, and the legacy `$` spelling. Also check initialization versus re-entry, both branch flags and exit conditions, base+4j, and the post-body decrement.

Sources: [L08 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033) · [L08 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034)

</details>

#### Recall Q17 · Load delay slot and interlocks

What does the `nop` between the second `lw` and its dependent `slt` guarantee? Explain when independent work may replace it and distinguish static scheduling from an interlock.

<details><summary>Show solution</summary>

In the material’s MIPS R2000 example, the instruction immediately after a load must not require its result. The `nop` puts `slt` at distance two. Moving useful independent work into that position must preserve operand readiness and original program meaning. Static scheduling chooses order at compile time; an interlock detects a hazard and waits in hardware at runtime. Runtime stall, flush, and forwarding differ from static rearrangement. A load slot constrains result-use spacing; a branch slot instead requires the following instruction to execute regardless of outcome.

Checking points: Check distance two, semantic safety, compile time versus runtime, and the distinct slot contracts.

Sources: [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044) · [L08 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047) · [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050)

</details>

#### Recall Q18 · Dependent latency in a split adder

A 32-bit adder is split into low-16-bit EX1 and high-16-bit EX2. What happens to the carry and earlier low result? Must the next instruction using the full result become faster?

<details><summary>Show solution</summary>

Carry from EX1 feeds the high-half calculation in EX2; the low result must be stored and aligned with the high result from the same instruction. Having the low half does not make the full 32-bit value ready. Shorter stages may shorten the clock but increase the number of cycles a dependent consumer waits. Boundary overhead and branch penalties also matter, so neither dependent-chain latency nor total performance must improve. Internal overlap is correct only while preserving ISA-visible sequential results.

Checking points: Check carry transfer, low/high instruction ownership, and clock period versus dependent latency.

Sources: [L08 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049) · [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011)

</details>

### Control hazards and branch policy

#### Recall Q19 · PC producers and consumers

In L09’s no-prediction model, where does every instruction use PC, and when do R/I, loads/stores, branches, `jal`, and `jalr` determine next PC? If non-branch h enters IF at t0, give i/j/k fetch times and explain why early PC+4 selection is prediction.

<details><summary>Show solution</summary>

Every fetch consumes PC in IF. In this conservative model, R/I and loads/stores determine next PC in ID; branches, `jal`, and `jalr` do so in EX. With h at IF t0 and ID t1, i fetches at t2, j at t4, and k at t6. Waiting for confirmation creates gaps even between non-branches. Choosing PC+4 before decode and resolution finish predicts an unconfirmed sequential path. The production stages are implementation assumptions, and PC+4 assumes four-byte instructions. L09 lies beyond the current L08+Lab1 midterm cutoff.

Checking points: Check IF consumption, both production stages, alternating fetches, and the scope boundary.

Sources: [L09 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-004) · [L09 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005)

</details>

#### Recall Q20 · Two bubbles after a taken branch

Branch h enters IF t0, ID t1, and resolves taken at the end of EX t2; its target is k. Where are sequentially fetched i and j at t2? Trace h/i/j/k through k’s final WB, distinguishing decode, resolution, redirect, and flush.

<details><summary>Show solution</summary>

At t2, h is in EX, i in ID, and j in IF. Decode at t1 identifies a branch but does not yet establish its outcome and target. After resolution at the end of t2, redirect fetch to k at t3 and flush i/j. h continues through MEM t3 and WB t4. i’s bubble advances EX t3→MEM t4→WB t5; j’s advances ID t3→EX t4→MEM t5→WB t6, with no register/memory writes. k follows IF t3→ID t4→EX t5→MEM t6→WB t7. A stall retains work for later execution; a flush invalidates wrong work. Two bubbles belong to this EX-resolution model, excluding other hazards.

Checking points: Retain h, invalidate only i/j, check redirect t3 and completion t7, and suppress wrong-path effects.

Sources: [L09 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-015) · [L09 p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-017) · [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022)

</details>

#### Recall Q21 · Probability and cycle units

Assume 20% control flow, 70% taken within control flow, predict-not-taken, two cycles per wrong guess, base CPI=1, and no other hazards or fill/drain. For 100 useful instructions, calculate correct/wrong guesses, extra cycles, CPI, IPC, time increase, and throughput decrease. Can forward 50% and backward 90% alone establish overall 70%?

<details><summary>Show solution</summary>

The 80 non-control instructions and six not-taken branches give 86 correct and 14 wrong guesses. Extra cycles are 14×2=28; total=128, CPI=1.28, and IPC=100/128=0.78125. Wrong probability 0.14 is dimensionless, penalty two is cycles per wrong guess, and their product 0.28 is cycles per instruction. At fixed IC and clock, time rises 28% but throughput falls 1−0.78125=0.21875, or 21.875%. Forward/backward denotes target-address direction; missing mix weights prevent deriving 70% from 50% and 90% alone. This applies the material’s assumptions; it does not silently repair conflicting speech at undated 14:56, 26:58, 27:42, or 28:41.

Checking points: Check 86/14, 28, 1.28, 0.78125 and their units, plus the missing direction weights.

Sources: [L09 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012) · [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030)

</details>

#### Recall Q22 · Frequency, accuracy, and loss

What determines control-flow frequency, prediction error rate, and loss per wrong guess? Distinguish earlier resolution from better prediction, and explain why uncertain speech about an always-true condition cannot justify deleting a branch.

<details><summary>Show solution</summary>

Frequency comes from the program’s instruction mix; error rate depends on prediction and actual control behavior; loss depends on implementation timing, including resolution and redirect. Better prediction reduces wrong guesses; earlier resolution can reduce each mistake’s cost. A deeper pipeline may cancel more younger work, so two cycles is not universal. Eliminating a branch requires a confirmed condition and preservation of relevant side effects and program meaning. An uncertain variable value without its comparison does not establish an always-true condition. No detailed predictor algorithm or promised IPC≈0.9 improvement follows.

Checking points: Separate all three factors and both improvement mechanisms, and require condition/side-effect evidence.

Sources: [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031)

</details>

#### Recall Q23 · The branch-delay-slot contract

For the material’s MIPS R2000 branch, what happens to PC+4 and the following fetch when taken versus not taken? Explain safe slot filling, `nop`, the historical 80% figure, and the difference from a load delay slot.

<details><summary>Show solution</summary>

The PC+4 instruction executes for either outcome. The following instruction comes from the target if taken or PC+8 if not taken. The slot is therefore ISA-visible behavior, not speculative wrong-path work to discard. A moved instruction must be safe and appropriate on both paths, have ready operands, and preserve the branch decision and other effects. If none is suitable, use a `nop`; counting it as useful work inflates throughput. Approximately 80% automatic slot filling is a historical source claim, not a guarantee. A load slot instead prohibits immediate consumption of a load’s result. L09 branch-slot study remains beyond the current midterm cutoff.

Checking points: Check both address sequences, safe movement, useful work versus `nop`, and distinct slot meanings.

Sources: [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032) · [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044)

</details>

#### Recall Q24 · Limits of architectural recovery

Wrong-path register and memory writes are suppressed. Does that prove no cache change or observable timing effect remains? Name at least three conclusions that the permission-condition example cannot establish.

<details><summary>Show solution</summary>

Preventing wrong architectural results and restoring internal cache state are separate requirements. A speculative access may change cache contents and later access timing, so architectural flush alone does not prove the absence of internal effects. The example does not specify compiled branch polarity, a permission-bypass mechanism, attacker preparation, a network path, or the extent of leakage. Naming Spectre and Meltdown neither equates their mechanisms nor demonstrates success on every processor. Detailed cache/attack mechanisms are later study; this is not a current-product security judgment.

Checking points: Explain both state levels and avoid turning a conceptual example into proof of an attack or all-memory disclosure.

Sources: [L09 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033)

</details>

### Newly written integrated practice

#### Practice P01 · Evaluating two designs

Newly written synthetic practice transfers conditional performance comparison from recalled 2025-2 Q8/Q9 (p.2) and Q16 (p.8), adding a first-result versus finite-stream decision. Prerequisites: μprograms, CPI×clock, and five-stage fill/drain. The recalled source and answers are not authenticated, and it does not define the current scope. [EX:ca_2025_2_midterm_q08 p.2] [EX:ca_2025_2_midterm_q09 p.2] [EX:ca_2025_2_midterm_q16 p.8]

Hypothetical M executes each instruction sequentially in three 200ps cycles. P is a five-stage, 160ps pipeline. There are no hazards or extra overhead beyond the stated clocks; each run starts empty. (a) Compare first-instruction latency and steady spacing. (b) Find total times for N=1 and N=2 and the smallest N favoring P. (c) Does calling M microcoded and P hardwired generalize the result to other designs?

<details><summary>Show solution</summary>

M’s latency and spacing are both 3×200=600ps. P’s first latency is 5×160=800ps, but steady spacing is 160ps. For N=1, M takes 600ps and P 800ps, favoring M. For N=2, M takes 1200ps and P 6×160=960ps, favoring P. In general, 160(N+4)<600N gives N>640/440=16/11, so the smallest integer N is two. First-result and sustained-work goals can favor different choices. Control-style labels do not establish the stated clocks or cycle counts; another implementation requires its actual timings and hazards.

Checking points: Check 600/800ps latency, 600/160ps spacing, the finite-N inequality, and the limits of implementation labels.

Sources: [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024) · [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016)

</details>

#### Practice P02 · Dependence, bypassing, and rescheduling

Newly written synthetic practice transfers recalled Q15’s RAW identification, forwarding trace, and stall comparison into a safe-rescheduling decision. Prerequisites: real sources/destinations, result readiness, and ID/WB timing. Do not truncate completion to the source’s cycle 1–8 grid. [EX:ca_2025_2_midterm_q15 p.7]

```asm
A: lw x8, 0(x20)
B: add x9, x8, x10
C: addi x14, x14, 1
D: sub x11, x9, x8
```

Start an empty in-order five-stage pipeline with A IF in cycle 1. ALU results arrive at EX end and load data at MEM end. Required forwarding paths into EX exist; there are no other hazards. (a) Identify RAW relations and trace through last WB. (b) Remove forwarding and disallow same-cycle WB-to-ID reads: how many stalls result? (c) C is guaranteed independent of the other lines with no other effects from moving it. How does A,C,B,D change the forwarding execution?

<details><summary>Show solution</summary>

RAW relations are A→B(x8), A→D(x8), and B→D(x9). With forwarding, B waits one load-use cycle.

|Instruction|IF|ID|EX|MEM|WB|
|---|---|---|---|---|---|
|A|1|2|3|4|5|
|B|2|3–4 (includes waiting)|5|6|7|
|C|3–4 (held)|5|6|7|8|
|D|5|6|7|8|9|

A’s data reaches B EX5; B’s result reaches D EX7. Total=4+4+1=9 cycles. Without forwarding, B waits three cycles, then ID6→EX7→MEM8→WB9 after A WB5. C follows ID7→EX8→MEM9→WB10. D waits at ID8 and ID9, then performs ID10→EX11→MEM12→WB13. Extra stalls total 3+2=5; total cycles=4+4+5=13. Do not add A→D again. In A,C,B,D, independent C fills the load-use gap: A EX3/MEM4, C EX4, B EX5, D EX6, and last WB8. Rescheduling is safe under the explicitly stated independence condition.

Checking points: Check all three RAW relations and explain original nine, no-forwarding thirteen, and reordered eight cycles.

Sources: [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013) · [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031) · [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043) · [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050)

</details>

#### Practice P03 · Must the slot execute?

Newly written synthetic practice transfers recalled Q17’s simple-pipeline delay-slot reasoning to safety on both branch paths. Prerequisites: delay-slot semantics and flush. This is L09 supplementary study beyond the current midterm cutoff. [EX:ca_2025_2_midterm_q17 p.8]

Instructions are four bytes. A branch is at `0x400`, targeting `0x500`. Candidate A is an independent addition required once on either path, with ready operands and no effect on the branch condition. Candidate B is a store required only on the taken path. (a) Give the two execution addresses following the branch for each outcome. (b) Choose the safe candidate and justify it. (c) What if none is safe, and how does this differ from the teaching’s EX-resolution prediction model?

<details><summary>Show solution</summary>

With a delay slot, taken execution is `0x404→0x500`; not-taken is `0x404→0x408`. A can move under the stated conditions because both paths require its independent work. B would incorrectly store on the not-taken path. If no useful instruction is safe, use a `nop` without counting it as useful work. In the prediction model, younger PC+4/PC+8 instructions are flushed when wrong-path and fetch redirects to the target. Those two bubbles are not architectural delay-slot instructions.

Checking points: Check both address sequences, A/B effects on both outcomes, and `nop` versus flush.

Sources: [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022) · [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032)

</details>

#### Practice P04 · Comparing two improvements in time

Newly written lecture-based general practice. No indexed candidate directly combines branch probability, penalty, and clock in this way, so no exam-style claim is made. This is L09 supplementary study; prerequisites are Q21/Q22 and CPI×clock.

The baseline predicts not taken and has 20% control flow, 70% taken within it, two cycles per wrong guess, and base CPI=1. Improvement A keeps error frequency but cuts the penalty to one and increases clock period by 10%. B reduces error rate within control flow to 35%, retaining penalty two and the original clock. Ignore other hazards and fill/drain. Compare equal-instruction-count execution times in baseline clock units.

<details><summary>Show solution</summary>

Baseline CPI=1+0.2×0.7×2=1.28. A has CPI=1+0.2×0.7×1=1.14, but time per instruction is 1.14×1.10=1.254 baseline clock units. B also has CPI=1+0.2×0.35×2=1.14, with unchanged clock, so its time is 1.14. Both beat the baseline; B is faster. A changes loss per error, B error frequency, and equal CPI does not imply equal time at different clocks. These stipulated hypothetical numbers do not promise actual predictor performance.

Checking points: Check whole-stream error fractions 0.14/0.07 and time comparison 1.28/1.254/1.14.

Sources: [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030) · [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031)

</details>

## Sources

### Lectures and materials

[[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 · Microcode, resource reuse, and lab briefing]]

- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 (computer_architecture:NT001)]] 37:51, 39:27, 41:27, 43:18, 44:26, 45:27, 47:25, 48:04, 49:03, 49:43, 51:38, 52:36, 53:36, 54:28 — Transcript of the dated lecture.

- [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|Undated lecture (computer_architecture:NT002)]] 03:17, 05:10, 14:56, 17:37, 23:27, 26:58, 27:42, 28:41, 31:19, 33:03, 34:01, 35:17, 35:35, 37:02, 38:23, 39:22 — Lecture date unknown; uncertain speech remains distinct from material-based explanation. This TXT transcript was compared with the materials; original audio is unverified. It is not a complete verbatim transcript and does not recover missing speech, the actual class date, or speaker identities.

- [L06 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf): [L06 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005), [L06 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014), [L06 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015), [L06 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020), [L06 p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021), [L06 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022), [L06 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023), [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024). L06 linked to the September 29 transcript; preserve its separate legacy opcodes, widths, and delays.

- [L07 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.07.pdf): [L07 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006), [L07 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007), [L07 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008), [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011), [L07 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012), [L07 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015), [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016), [L07 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-020), [L07 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027), [L07 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030), [L07 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052), [L07 p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-055). Material-only prerequisites; no separate lecture date or speech is established.

- [L08 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf): [L08 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-004), [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013), [L08 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018), [L08 p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-029), [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031), [L08 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-032), [L08 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033), [L08 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034), [L08 p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-037), [L08 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042), [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043), [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044), [L08 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047), [L08 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049), [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050). Material-only prerequisites; no separate lecture date or speech is established.

- [L09 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf): [L09 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-004), [L09 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005), [L09 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012), [L09 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-015), [L09 p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-017), [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022), [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030), [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031), [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032), [L09 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033). Course content beyond the current L08+Lab1 midterm cutoff.

### Recalled-exam connections

The 2025-2 midterm reconstruction is not an authenticated official paper or answer key. Connections concern reasoning demands, not predictions or a claim that new exercises are past questions. Answers in that source belong to its reconstruction author.

Q08/Q09 (p.2) and Q16 (p.8) inform latency/throughput and implementation comparisons; Q10 (p.2) informs dependence classification; Q15 (p.7) informs RAW and pipeline tracing; Q17 (p.8) informs delay-slot semantics. New problems specify timing assumptions rather than inheriting Q15’s limited cycle 1–8 grid or unspecified RF/store bypass details. Q17 connects only to supplementary L09 study beyond the current cutoff.

Existing question-only previews: [[exam_questions/ca_2025_2_midterm_q09|2025-2 midterm reconstruction Q9]] · [[exam_questions/ca_2025_2_midterm_q15|2025-2 midterm reconstruction Q15]] · [[exam_questions/ca_2025_2_midterm_q16|2025-2 midterm reconstruction Q16]].

Source wording: L07 p.16 prints `predicated` and p.27 prints `state`. Explanations of prediction and stages interpret the model without altering those source quotations. Likewise, keep September 29’s IR/PC confusion at 49:03/49:43 and the undated lecture’s numerical/timing discrepancies distinct from material-based explanations.


---

[[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/lab-environment-specification|Next: Docker Lab Environment and CPU Assignment Specifications →]]
