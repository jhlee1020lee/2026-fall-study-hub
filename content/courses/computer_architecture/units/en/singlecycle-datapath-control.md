---
title: "State, Datapath, and Control in a Single-Cycle CPU"
description: "Trace single-cycle operands, addresses, control, and clock constraints."
course: "computer_architecture"
unit_id: "singlecycle-datapath-control"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 05 typo fixed.pdf", "lec 05.pdf", "lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-10-lecture-04"]
---

See how instruction state changes become data and control paths within one clock. Trace values versus addresses, mux selections versus write enables.

## Circuits that transform architectural state

Viewed as an abstract finite-state machine (FSM), an ISA defines how one instruction transforms current program-visible state (PVS) into the next state. Before-and-after values of PC, architectural registers, and memory express that rule. “One state transition per instruction” does not require one physical clock cycle or exclusion of every other processor's memory accesses. [CA RM001 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-006)

A single-cycle CPU implements that transition within one clock cycle. Combinational logic reads current state and computes next values; storage accepts permitted values at the clock boundary. This detailed circuit account is a materials-based prerequisite review of the instructor's single-cycle deck, not a reconstruction of an unrecorded meeting's date or complete spoken coverage. Related register and representation rules appear in [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]], and branch/procedure semantics in [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes]].

### Combinational reads and synchronous writes

The two read selects and one write select in [CA RM001 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-007) each use 5 bits. Since $2^5=32$, each selects one of 32 registers. A 5-bit register **number** differs from the 64-bit **data** in that register.

The educational “magic” memory/register file in [CA RM001 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-008) assumes combinational reads: changing a read select or stored contents changes read data through the combinational path. Synchronous writes instead change selected storage on a positive clock edge when write enable is asserted. As an illustration, if `x5=7` and write data is 10, a disabled write leaves `x5=7`. Control must determine **where and when to write**, not merely which value to calculate.

This simplified timing model does not specify the latency, ports, or clock behavior of real DRAM and caches. The corresponding technical discussion in original version RM002 agrees, while its source identity and announcement version remain distinct. [CA RM002 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-008)

## Instruction fetch and the register-arithmetic path

A datapath connects registers, the ALU, multiplexers (muxes), and memories to process values and addresses. IF, ID, EX, MEM, and WB name the work involved.

| Stage | Role |
|---|---|
| IF | Fetch the instruction addressed by PC |
| ID | Decode the instruction and read register operands |
| EX | Perform an ALU operation or effective-address calculation |
| MEM | Access data memory when required |
| WB | Write a result back to the register file |

In a single-cycle design these are functional divisions, not five clocks. [CA RM001 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-009) PC supplies instruction memory's read address; its output is a different value, the 32-bit instruction. A separate adder calculates PC+4, preparing the next address for this deck's 4-byte instruction model. [CA RM001 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-012)

For `add rd,rs1,rs2`, instruction `[19:15]` identifies `rs1`, `[24:20]` identifies `rs2`, and `[11:7]` identifies `rd`. The two selected 64-bit register values pass through read ports into the ALU; the sum returns as destination write data. For an illustrative PC=100 and source values 7 and 5, the destination receives 12 and PC becomes 104. If `rd=x0`, the existing hard-wired-zero rule remains in force. [CA RM001 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-013) [CA RM001 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-015)

The instruction needs no data-memory read or write. It still needs **memory access for instruction fetch**. Treating IF and MEM as the same work merely because both mention memory gives the wrong execution path.

## Immediate generation and ALU input selection

`addi rd,rs1,immediate12` adds a signed immediate to a source register, writes the result to the destination, and continues at PC+4. The Immediate Generator does not sign-extend the entire instruction as one signed number. It extracts or reconstructs the fields required by the format and produces the 64-bit immediate value. [CA RM001 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-016) [CA RM001 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-017)

For example, 12-bit pattern `0xFFC` is 4092 unsigned but $4092-4096=-4$ as a signed immediate. Sign extension preserves −4. Applying it to an illustrative `x5=10` produces 6; zero-extending and adding 4092 would implement a different meaning. The reasoning connected to recalled Q13(c) therefore explains **value preservation** for negative operands, not merely the mechanical filling of upper bits. [EX:ca_2025_2_midterm_q13 p.5] This connection uses a Fall 2025 reconstruction whose official wording and answers have not been independently verified.

R-type arithmetic needs register-file Read data2 at the ALU's second input; immediate arithmetic needs the immediate. A mux controlled by ALUSrc selects between them while preserving the shared first input and write-back path. Loads and stores also reuse this immediate path for base-plus-offset address calculation. [CA RM001 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-018) [CA RM001 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-019)

Do not treat every format's immediate as the same contiguous 12-bit field. Stores reassemble two pieces; branches account for scattered displacement bits and an omitted low zero. RM001 page 17's “selected 12 bits” is an overview; use [CA M003 PDF p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062) for the actual branch layout. Sign extension can be represented by replicated sign-bit wires, and a fixed one-bit shift by rerouting wires. That differs from a general variable shifter. [CA RM001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027)

## Separating addresses from data in loads and stores

For a load, the ALU result is the **address of the value**, not the value itself. `lw` adds a base register and sign-extended offset to form the effective address (EA), reads the word there, and sends it to the destination. `sw` performs the same address calculation, but obtains memory write data from `rs2` and writes no general register. For an illustrative base of 1000 and offset 12, both have EA=1012, but their data flows run in opposite directions. [CA RM001 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-021) [CA RM001 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-022)

In [CA RM001 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-023), register-file Read data2 also connects separately to memory's write-data input. Thus ALUSrc can select an immediate while store data travels along another path. A write-back mux is also needed because the destination value may come from the ALU or memory.

| Signal | Selection or action |
|---|---|
| ALUSrc | Second ALU input: Read data2 or immediate |
| MemtoReg | Register write data: ALU result or memory read data |
| MemRead | Data-memory read |
| MemWrite | Data-memory write |
| RegWrite | Register-file write |

ALUSrc and MemtoReg have different positions and purposes: one selects a **computation input**, the other the **source of a stored result**.

The `lw/sw` examples access 4-byte words. RV64 `lw` sign-extends the word to 64 bits, while `sw` writes the source's low 32 bits. The later control table uses `ld/sd`, accessing 8-byte doublewords; do not merge their widths. [CA M003 PDF p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057) The leftover “load 4-byte word” caption on RM001 page 22 contradicts its SW heading, mnemonic, and state transition and is a source typo. Likewise, `translate(EA)` marks an abstract address-translation boundary, not a completed virtual-memory, exception, or alignment-handling circuit.

## BEQ's condition and the next PC

`beq` selects a PC-relative target when its source registers are equal and PC+4 otherwise. The source circuit subtracts the values and uses the ALU's Zero output to test equality. A separate adder adds the signed branch displacement to the current PC. For this BEQ subset, $PCSrc=Branch\land Zero$: recognizing a branch opcode does not by itself make the branch taken. [CA RM001 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-025) [CA RM001 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-026)

The shift-left-1 in [CA RM001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027) converts a two-byte-unit immediate into a byte displacement. For illustrative PC=100 and target=200, the difference is 100 bytes, corresponding to 50 two-byte units. If SB reconstruction has already appended the low zero and produced 100, shifting again is wrong. Read the Immediate Generator's output convention consistently.

`jal` transfers control without an equality test and writes PC+4 to `rd` as a link. With `rd=x0`, that stored result is discarded. RM001 page 28 prints a “branch if equal” caption and `PC + (immediate20 << 2)` under JAL, conflicting with unconditional JAL semantics and the UJ fields shown there and in [CA M003 PDF p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063). Reconstruct $\{imm[20],imm[19:12],imm[11],imm[10:1],0\}$ as a signed byte displacement and add it to the current PC. This is an explicit explanatory correction based on source bit layouts. The basic datapath below should not be read as a complete JAL/JALR link-and-target circuit. [CA RM001 PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-028)

## From opcodes to ALU control and write enables

Single-cycle control is a combinational function of the current instruction. The decoder determines accesses, ALU operations, and mux selections. Instruction opcodes and internal control encodings occupy different levels. [CA RM001 PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-030) [CA RM001 PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-031)

The educational ALU in [CA RM001 PDF p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-032) has a 4-bit control input: `0000=AND`, `0001=OR`, `0010=add`, and `0110=subtract`. Main control derives a 2-bit ALUOp from the opcode; ALU control interprets it with function fields.

| Instruction | ALUOp | funct7 | funct3 | ALU action | Internal ALU control |
|---|---|---|---|---|---|
| `ld/sd` | 00 | X | X | Address addition | 0010 |
| `beq` | 01 | X | X | Subtraction for comparison | 0110 |
| R-type `add` | 10 | 0000000 | 000 | Add | 0010 |
| R-type `sub` | 10 | 0100000 | 000 | Subtract | 0110 |
| R-type `and` | 10 | 0000000 | 111 | AND | 0000 |
| R-type `or` | 10 | 0000000 | 110 | OR | 0001 |

X means the field is not consulted to determine that row's result, not that arbitrary unknown hardware values are universally safe. Main control in [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034) receives instruction `[6:0]`; ALU control receives ALUOp and instruction `[30,14:12]`. Within this limited legal-instruction set, other funct7 bits are fixed, so only the distinguishing bit is exposed. This is not complete validation of the entire ISA. The branch/jump names listed on page 31 likewise do not establish a separate canonical opcode for every name.

### Reading the control table as value movement

The single-bit signals in [CA RM001 PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-033) combine as follows:

| Class | ALUSrc | MemtoReg | RegWrite | MemRead | MemWrite | Branch | ALUOp |
|---|---:|---:|---:|---:|---:|---:|---|
| R-format | 0 | 0 | 1 | 0 | 0 | 0 | 10 |
| `ld` | 1 | 1 | 1 | 1 | 0 | 0 | 00 |
| `sd` | 1 | X | 0 | 0 | 1 | 0 | 00 |
| `beq` | 0 | X | 0 | 0 | 0 | 1 | 01 |

Store and branch have RegWrite=0, so the MemtoReg choice cannot change a register; its entry is X. Store still requires MemWrite=1 to produce its memory effect.

![CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.05.typo.fixed/page-034.png)

Distinguish **field-selection wires** from the instruction, **data paths** between the register file, ALU, and memory, and the blue **control wires**. R-type uses two registers → ALU → destination. Load uses base/immediate → address → memory → destination. Store separately carries `rs2` to memory write data while calculating the address. BEQ combines the register comparison and PC-relative adder at the next-PC mux. The next three source pages highlight these distinct paths. [CA RM001 PDF p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-035) [CA RM001 PDF p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-036) [CA RM001 PDF p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-037)

A single-cycle design must allow the path from fetch to the necessary final value to settle in one cycle. Consequently, a common clock long enough for the load also applies to shorter ALU instructions. The reasoning demanded by recalled Q7 is to find a boundary accommodating **every supported path**, rather than select the fastest path. [EX:ca_2025_2_midterm_q07 p.2] This motivates multi-cycle execution. [CA RM001 PDF p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-038) Actual performance must compare both cycle length and CPI, and these educational control encodings must not be transplanted as the answer to Lab1, whose control definitions differ.

## Key Takeaways

- Combinational reads differ from enabled edge-triggered writes.
- ALUSrc chooses an ALU input; MemtoReg chooses register write-back data.
- A branch needs condition and target calculations; do not shift a reconstructed byte displacement twice.
- The common clock must accommodate the longest supported path.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Read and write boundaries

Compare changing a read selector with changing only write data. What are index/data widths for 32 RV64 registers, and must one abstract ISA transition take one clock?

<details><summary>Show solution</summary>

Index width is five bits because 2^5=32; data width is 64 bits. Combinational read outputs follow selectors and stored contents. Storage changes only with the positive edge and write enable: `x5=7` remains 7 despite write data 10 when disabled. The ISA defines observable before/after PC, register, and memory state; one clock versus microcycles is an implementation choice, not universal exclusion of other CPUs' memory accesses.

**Checking points:** Separate selector, data, enable, and edge.

</details>

#### Recall Q02 · Information flow for add

Trace PC, the 32-bit instruction, `[19:15]`, `[24:20]`, `[11:7]`, and register data for `add rd,rs1,rs2`. With PC=100 and operands 7 and 5, give the result and stage roles.

<details><summary>Show solution</summary>

IF uses the PC address to read instruction bits; ID uses those fields as `rs1`, `rs2`, and `rd` indices. Two 64-bit values enter the EX ALU, producing 12 for destination WB; next PC is 104. If `rd=x0`, the write is discarded. No data-memory MEM operation is needed, but instruction fetch remains necessary. Stage names are functional divisions within one cycle, not five clocks or a completed pipeline.

**Checking points:** Keep instruction bits, register numbers, and values distinct.

</details>

#### Recall Q03 · Immediate generation and ALUSrc

Sign-extend 12-bit `0xFFC` and add it to 10. Does the generator extend the whole instruction? Explain ALU sharing, store/branch field handling, and fixed-shift cautions.

<details><summary>Show solution</summary>

4092−4096=−4, preserved at 64 bits, so the sum is 6. The generator extracts/reassembles fields, not the entire instruction. ALUSrc selects register Read data2 or an immediate for the shared ALU and write-back. Loads/stores reuse it for base+offset. Stores combine two immediate pieces; branches reconstruct scattered bits and the low zero. Sign-bit replication and fixed shifts can be wiring, unlike a variable shifter. An already reconstructed byte displacement must not be shifted again.

**Checking points:** Include value preservation, input selection, and format-specific reconstruction.

</details>

#### Recall Q04 · Load/store write destinations

At base 1000 and offset 12, compare `lw` and `sw` addresses, data sources, and write destinations. Explain ALUSrc, MemtoReg, MemRead, MemWrite, RegWrite and word/doubleword widths.

<details><summary>Show solution</summary>

Both EAs are 1012. `lw` reads a 32-bit memory word, sign-extends to 64 bits, and writes `rd`; `sw` writes low 32 bits of `rs2` to memory without a general-register write. ALUSrc selects the offset for address addition; MemtoReg selects ALU versus memory result for register write-back. Store data travels separately from Read data2. MemRead/MemWrite/RegWrite enable their named accesses. Later `ld/sd` use eight bytes, not the word width; `translate(EA)` is an abstract boundary rather than full translation hardware.

**Checking points:** Do not confuse EA with loaded data or the input mux with the result mux.

</details>

#### Recall Q05 · PC selection for beq and jal

At PC=100 and branch target=200, explain equality, Branch, Zero, PCSrc, and displacement units. Where do unequal operands go? Contrast `jal` link/target and the p.28 discrepancy.

<details><summary>Show solution</summary>

Subtraction's Zero tests equality, and this BEQ subset uses PCSrc=Branch AND Zero. Unequal operands give PC=104 even with Branch=1. The target difference is 100 bytes or 50 two-byte units; an appended low zero already reconstructing 100 must not be doubled again. `jal` transfers unconditionally and writes link PC+4=104 to `rd` unless it is `x0`. Reconstruct `{imm[20],imm[19:12],imm[11],imm[10:1],0}` as a signed byte displacement. The p.28 equality caption and `<<2` conflict with that meaning/layout. The basic diagram is not complete jump circuitry.

**Checking points:** Separate condition, target, and link; retain the source discrepancy.

</details>

#### Recall Q06 · Two-level ALU decoding

Distinguish main-control and ALU-control inputs/outputs. Reconstruct ALUOp, function distinctions, and internal controls for `ld/sd`, `beq`, and R-type `add/sub/and/or`.

<details><summary>Show solution</summary>

Main control maps opcode `[6:0]` to two-bit ALUOp and other controls. ALU control combines ALUOp with function information (`[30,14:12]` in the limited diagram) to select a four-bit operation. `ld/sd`: 00→add `0010`; `beq`: 01→subtract `0110`, ignoring funct. With R-type ALUOp=10, `add` uses `0000000/000`→`0010`, `sub` `0100000/000`→`0110`, `and` `0000000/111`→`0000`, and `or` `0000000/110`→`0001`. Internal encoding differs from ISA opcode; other funct7 bits are fixed in this legal subset. X means unconsulted information in that row, not universal safety for hardware unknowns.

**Checking points:** Separate class decoding from funct decoding and two-bit from four-bit controls.

</details>

#### Recall Q07 · Read the control table as paths

Give R-type, `ld`, `sd`, `beq` rows in order (ALUSrc,MemtoReg,RegWrite,MemRead,MemWrite,Branch,ALUOp). Explain X entries and each active data path.

<details><summary>Show solution</summary>

Rows are R=(0,0,1,0,0,0,10), `ld`=(1,1,1,1,0,0,00), `sd`=(1,X,0,0,1,0,00), `beq`=(0,X,0,0,0,1,01). R sends two registers→ALU→rd; load sends base+immediate→address→memory→rd; store separately carries rs2 to memory while computing its address; BEQ combines comparison Zero and a PC-relative adder at the next-PC mux. For store/branch, RegWrite=0 makes MemtoReg irrelevant to registers. Store still requires MemWrite=1 to change memory.

**Checking points:** Match every signal to its path and justify rather than memorize X.

</details>

#### Recall Q08 · The common-clock constraint

What fails if the common clock is chosen for a short ALU path while loads need longer? Does calling a design multi-cycle establish a speed improvement?

<details><summary>Show solution</summary>

A load needs fetch, address calculation, memory read, and write-back values to settle before the boundary. A clock fitting only the short path may capture an unfinished result. The longest supported path therefore constrains every instruction's common period. Multi-cycle execution permits different required counts, but comparison still needs period×CPI, workload, and overhead.

**Checking points:** Base the boundary on the longest required path, not the fastest one.

</details>

### Apply the ideas

#### Practice P01 · Two independent defects

Newly written synthetic practice. An educational single-cycle design has a 350 ps R-type path and a 570 ps load path; all others are shorter. Its designer uses a 350 ps clock and zero-extends `addi` immediate `0xFFC`. Starting from `x5=10`, find the intended and erroneous sums and explain whether either repair substitutes for the other.

Connection: longest-path reasoning from [EX:ca_2025_2_midterm_q07 p.2] and signed-value preservation from [EX:ca_2025_2_midterm_q13 p.5] (c) become independent functional/timing diagnosis. Prerequisites: Q01, Q03, Q08. Full encoding design in Q13(a,b) is not selected.

<details><summary>Show solution</summary>

Signed `0xFFC` is −4, so the intended sum is 6; zero extension gives 4092 and the erroneous sum 4102. Fixing extension does not make a 350 ps clock support a 570 ps load. The common period must be at least 570 ps under these assumptions. Slowing the clock alone leaves the wrong operand semantics intact. Correct meaning and settled boundary values are separate conditions, with real overhead still to consider.

**Checking points:** Check 6, 4102, 570 ps, and why both repairs are necessary.

</details>

### Short review plan

Sketch data origins and destinations for Q02–Q05, then reconstruct Q06–Q08's controls with reasons. On the next review, diagnose P01's two failures separately.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes · related prerequisites]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes · related prerequisites]]
- [lec 05 typo fixed.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-009), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-013), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-019), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-023), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-028), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-038)
- [lec 05.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-006), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-008), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-038)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063)

The detailed circuit is materials-only prerequisite review; linked September 8/10 notes do not establish its complete spoken coverage. 'Magic' memory is an educational timing model, and RM001/RM002 remain distinct versions. The load caption on RM001 p.22 and JAL condition/shift on p.28 conflict with instruction meanings/bit layouts. Classroom control encodings are not Lab1 specifications; full JAL/JALR and address-translation circuits are not supplied.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q07 p.2], [EX:ca_2025_2_midterm_q13 p.5].
Only Q13(c) is connected. Part (b)'s immediate×2 requires distinguishing encoded units from reconstructed bytes; this is not a solution of all of (a,b).
