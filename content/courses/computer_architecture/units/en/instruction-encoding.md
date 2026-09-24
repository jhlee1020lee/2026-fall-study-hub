---
title: "Instruction Encoding and Address Construction"
description: "Check R/I/S fields, PC-relative displacements, and large constants built with signed immediates."
course: "computer_architecture"
unit_id: "instruction-encoding"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-10-lecture-04"]
---

Decode how instruction fields identify operations, register numbers, constants, and displacements. Preserve signed values and byte units throughout to check formats, branch distances, and large-constant construction.

## Machine code and hexadecimal

Instructions are bit patterns in memory. Instruction encoding specifies how those bits identify operations and operands. Instructions represented in binary are machine code; assembly code is their human-readable notation. After [registers and data representation](data-register-memory.md), the next question is how to represent **the instruction that operates on values**.

The course studies basic 32-bit RISC-V instructions with relatively few formats. Fixed length and recurring field positions make decoding more regular. This does not assert that all RISC-V extensions or other ISAs always use 32-bit instructions. Hexadecimal represents four bits per digit, making long patterns easier to read. [[page_cache/computer_architecture/lec.03/page-023|CA M003 p.23]] gives:

```text
hex:     e    c    a    8    6    4    2    0
binary: 1110 1100 1010 1000 0110 0100 0010 0000
```

Grouping the bits changes notation, not content. Programs can also process other programs because program representations are data. M003 p.29 places machine code for an accounting program, editor, and C compiler alongside payroll data, book text, and the editor's C source. This supports the compiler-processing-source and linker-processing-objects examples. A standardized ISA establishes common binary-instruction meanings and a basis for binary compatibility; complete execution still requires suitable environment conditions. The compiler/linker consequences of this figure are materials-based supplementation.

## R-format: identifying registers and operations

R-format encodes the information needed to read two registers and write a result. From high bits to low bits: [[page_cache/computer_architecture/lec.03/page-025|CA M003 p.25]]

| Bits | Field | Width | Meaning |
|---|---|---|---|
| 31:25 | `funct7` | 7 | Further operation selection |
| 24:20 | `rs2` | 5 | Second source-register number |
| 19:15 | `rs1` | 5 | First source-register number |
| 14:12 | `funct3` | 3 | Further operation selection |
| 11:7 | `rd` | 5 | Destination-register number |
| 6:0 | `opcode` | 7 | Operation code |

The widths total `7+5+5+3+5+7=32`. Five bits identify 32 registers. A register field contains a **number**, not the register's current **value**: `rs1=20` tells execution to read `x20`. The processor interprets `opcode` together with `funct3` and `funct7` to select the operation. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 59:09]]

For the source example `add x9,x20,x21`, `rd=9`, `rs1=20`, `rs2=21`, `funct7=0`, `funct3=0`, and `opcode=51=0x33`:

```text
funct7   rs2   rs1  funct3  rd   opcode
0000000 10101 10100   000  01001 0110011

0000 0001 0101 1010 0000 0100 1011 0011
= 0x015A04B3
```

Assemble by field boundaries, then regroup into four-bit digits to obtain the value in [[page_cache/computer_architecture/lec.03/page-026|CA M003 p.26]]. The assembly operand order `rd,rs1,rs2` differs from the fields' visual order inside the instruction word.

## Shared positions in I-format and S-format

Immediate arithmetic and loads need an immediate instead of a second source-register field. I-format is `imm[11:0] | rs1 | funct3 | rd | opcode`, with widths `12+5+3+5+7`. For `addi`, the immediate is a constant operand. For a load, `GPR[rs1]+sign_extend(immediate)` is the address and `rd` receives the loaded result. I-format is not exclusive to loads. [[page_cache/computer_architecture/lec.03/page-027|CA M003 p.27]]

A general signed 12-bit immediate ranges from `−2048` to `2047`. Using it as an RV64 value replicates `imm[11]` through the upper 52 bits. For example, 12-bit `111111111100` means −4, allowing an address four bytes **before** a base. Zero-extending it would produce 4092. This value-preservation reasoning connects to recalled Q4 and Q13(c). [EX:ca_2025_2_midterm_q04 p.2] [EX:ca_2025_2_midterm_q13 p.5]

A store needs two register inputs, the base address and the data, but no result register:

```text
I: imm[11:0]       | rs1 | funct3 | rd       | opcode
S: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
```

In `sd x9,96(x22)`, `x22` supplies the base and `x9` supplies data. Both are read; memory is the destination. S-format retains `rs1` at bits 19:15 and `rs2` at bits 24:20, splitting its immediate into the remaining 7+5 bits. R- and I-format share `rd` at bits 11:7; S-format uses those bits for the low immediate portion. [[page_cache/computer_architecture/lec.03/page-028|CA M003 p.28]]

This accommodates different operand requirements while preserving register-selection positions and a 32-bit total length. The lecturer explicitly connected the split to keeping both source positions fixed. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 01:03:54–01:04:49]] Recalled Q13(a) calls for this design explanation rather than merely naming fields. [EX:ca_2025_2_midterm_q13 p.5]

## PC-relative branch and jump distances

A label is a readable name that the assembler resolves using actual placement. PC-relative addressing records the distance from the current instruction instead of a complete absolute target address. Since branch targets are often nearby, a short field represents a useful range. Also, moving source and target together by `k` leaves `(target+k)−(PC+k)=target−PC` unchanged. This second property is a derivation from the address formula and connects to recalled Q13(b)'s relative-versus-absolute comparison. [EX:ca_2025_2_midterm_q13 p.5]

M003 p.62 writes `target = PC + immediate × 2`. Here the immediate is a distance **in two-byte units**. For the September 10 example `PC=100` and `target=200`, the byte difference is 100 and the encoded-unit value is 50. Going from 200 back to 100 requires −100 bytes, or −50 such units. The reference PC is the branch's own address. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 01:05:39]]

The SB-format diagram in [[page_cache/computer_architecture/lec.03/page-062|CA M003 p.62]] scatters the immediate pieces across the word. Include the isolated `imm[12]` and `imm[11]` when reconstructing:

```text
SB byte displacement: imm[12] | imm[11] | imm[10:5] | imm[4:1] | 0
UJ byte displacement: imm[20] | imm[19:12] | imm[11] | imm[10:1] | 0
```

After this reconstruction and sign extension, the result is already a **byte displacement**. Multiplying again by two doubles the distance incorrectly. SB's 12 stored bits and implicit low zero give a representable range of −4096 through 4094 bytes in steps of two. Representability and executable instruction alignment are separate conditions; the basic 32-bit examples here place instruction starts four bytes apart.

The UJ-format used by `jal` allocates more immediate bits for a larger PC-relative range. Its actual field layout is `imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode`, distinct from the numerical reconstruction order above. [[page_cache/computer_architecture/lec.03/page-063|CA M003 p.63]]

## Large constants with LUI and signed immediates

Constants outside a 12-bit immediate's range can require several instructions. `lui` places a **20-bit constant** in destination bits 31:12 and clears bits 11:0. On RV64, bit 31 is extended through bits 63:32. Since `31−12+1=20`, the repeated “12-bit” wording at 01:08:10–01:09:07 conflicts with the slide and is corrected here to 20 bits, without rewriting the speech. [[page_cache/computer_architecture/lec.03/page-061|CA M003 p.61]] [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 01:08:10–01:09:07]]

Applying the source's rule gives this explanatory calculation:

```asm
lui  x5, 0x12345
addi x5, x5, 0x678
```

The first instruction produces `0x0000000012345000`; adding `0x678` produces `0x0000000012345678`. But if the desired low 12-bit pattern is at least `0x800`, `addi` interprets that pattern as negative. Simply cutting a constant into upper and lower pieces can then fail.

For `0x12345ABC`, the signed 12-bit value of `0xABC` is `0xABC−0x1000=−0x544`. Raise the upper portion by one:

```asm
lui  x5, 0x12346
addi x5, x5, -1348
```

Since `1348=0x544`, the result is `0x12346000−0x544=0x12345ABC`. These are checked applications of the signed-immediate rule, not recovered lecture examples. M003 p.63 uses the same broad idea for long jumps: construct an upper address with `lui` and supply a register plus low offset to `jalr`. The offset's sign still matters. This introductory construction does not represent every arbitrary 64-bit constant or address in two instructions.

## Key Takeaways

- Register fields encode numbers, not register contents.
- I-format supports immediate arithmetic and loads; stores need base and data inputs in S-format.
- Splitting the S immediate preserves source-register positions.
- Distinguish a branch's two-byte-unit value from its reconstructed byte displacement.
- `lui` inserts 20 bits; a following signed `addi` may require adjusting the upper portion.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Bit notation and program representations

Convert `0xECA86420` to binary and check its width. Explain why compilers/linkers can process other programs and what ISA standardization does and does not guarantee.

<details><summary>Show solution</summary>

Each hex digit supplies four bits: `1110 1100 1010 1000 0110 0100 0010 0000`, totaling 8×4=32 bits. Only notation changes. Source, machine code, and objects are data representations another running program can transform. A standardized ISA shares binary-instruction meanings, without automatically satisfying libraries or execution-environment requirements.

**Checking points:** Check eight nibbles, 32 bits, programs as data, and compatibility limits.

</details>

#### Recall Q02 · Assemble R-format

For `add x9,x20,x21`, use `funct7=0`, `funct3=0`, and `opcode=0x33`. Give all six high-to-low fields with widths/values and assemble the hex word. Does changing `x20`'s current value change the encoding?

<details><summary>Show solution</summary>

The order is `funct7(7)|rs2(5)|rs1(5)|funct3(3)|rd(5)|opcode(7)`. Values are `0000000|10101|10100|000|01001|0110011`, totaling 32 bits and yielding `0x015A04B3`. Positional weighting gives `21×2^20+20×2^15+9×2^7+0x33`. The encoded 20 is a register number, so changing its contents does not change the instruction. Operation selection uses opcode with funct3/funct7.

**Checking points:** Check field versus assembly order, five-bit register numbers, and final hex.

</details>

#### Recall Q03 · Inputs and destinations in I/S

Compare operand roles in `addi`, a load, and `sd x9,96(x22)`. Give I/S field widths, shared register positions, why a store lacks `rd`, and the split immediate for 96.

<details><summary>Show solution</summary>

I uses `imm12|rs1(5)|funct3(3)|rd(5)|opcode(7)`; its immediate is a value for `addi` or an address offset for a load. S uses `imm[11:5](7)|rs2(5)|rs1(5)|funct3(3)|imm[4:0](5)|opcode(7)`. The store reads base `x22` and data `x9` and writes memory, so it has no `rd`. Keeping `rs1` at 19:15 and `rs2` at 24:20 splits 96=`000001100000` into `0000011|00000`. Bits 11:7 hold `rd` in R/I but low immediate in S.

**Checking points:** Check value versus offset, two sources/memory destination, positions, and split.

</details>

#### Recall Q04 · Preserve a negative immediate

Interpret 12-bit `111111111100` signed and identify the bit copied when widening to RV64. Calculate the address from base 100 under sign/zero extension, and derive the signed 12-bit range.

<details><summary>Show solution</summary>

The pattern is 4092 unsigned but `4092−4096=−4` signed. Replicate `imm[11]=1` into the upper 52 bits to preserve −4, giving address 96. Zero extension instead gives 100+4092=4192. The sign-bit weight −2048 and remaining maximum 2047 give range −2048…2047. It is the immediate value, not a register number, that is extended.

**Checking points:** Verify −4, 96, 4192, sign-bit location, 52 bits, and range.

</details>

#### Recall Q05 · Branch units and reconstruction

Calculate byte and two-byte-unit displacements for PC 100→target 200 and the reverse. Distinguish stored SB/UJ fields from byte reconstruction order, distinguish SB range from alignment, and explain two reasons for PC-relative addressing.

<details><summary>Show solution</summary>

The assembler resolves labels from actual instruction placement. Forward is +100 bytes/+50 units; reverse is −100 bytes/−50 units, based on the branch's own PC. Stored SB immediate pieces are scattered as `imm12`, `imm10:5`, `imm4:1`, `imm11`; UJ's high-to-low fields are `imm20|imm10:1|imm11|imm19:12|rd|opcode`. Reconstruct SB as `imm12|imm11|imm10:5|imm4:1|0` and UJ as `imm20|imm19:12|imm11|imm10:1|0`, then sign-extend. This is already a byte displacement; do not double it again. SB spans −4096…4094 bytes in steps of two, while these basic 32-bit instruction starts are four bytes apart. Short fields suit nearby targets, and moving both PC and target by k preserves their difference.

**Checking points:** Check both signs, reconstruction order, units, range/alignment distinction, and both reasons.

</details>

#### Recall Q06 · LUI and signed low bits

Trace `lui x5,0x12345; addi x5,x5,0x678`. Why construct `0x12345ABC` with upper `0x12346` and immediate −1348? Explain LUI width, zero filling, sign extension, and its connection to long jumps.

<details><summary>Show solution</summary>

LUI inserts 20 bits into 31:12, zeroes 11:0, and copies bit31 into 63:32, producing `0x0000000012345000`. Adding `0x678` yields `0x12345678`. As signed 12-bit data, `0xABC−0x1000=−0x544=−1348`, so increase the upper part: `0x12346000−0x544=0x12345ABC`. Long jumps similarly combine an upper address with register-plus-low-offset `jalr`, accounting for the low part's sign. This does not build every arbitrary 64-bit value in two instructions.

**Checking points:** Check 20-bit width, upper/lower behavior, both results, and why upper adjustment is necessary.

</details>

### Apply and diagnose

#### Practice P01 · Format changes and moving code

Newly written synthetic practice transfers the design reasoning of [EX:ca_2025_2_midterm_q13 p.5] (a,b). Prerequisites are I/S fields and PC-relative addressing. (a) Diagnose the proposal to put the S immediate contiguously in bits 31:20 while keeping both R-format source positions. (b) Move a branch from PC=`0x400`, target=`0x3E0` by adding `0x1000` to both. What happens to encoded distance and target? Explain the double-scaling mistake.

<details><summary>Show solution</summary>

(a) `rs2` occupies 24:20 inside the proposed 31:20 immediate, so both cannot retain their information there. S uses a 7+5 split to preserve source positions. (b) The displacement stays −`0x20`=−32 bytes, or −16 units. New PC is `0x1400`, target `0x13E0`. Doubling reconstructed −32 incorrectly targets `0x1400−64=0x13C0`.

**Checking points:** Check overlapping bits, invariant displacement, and correct/incorrect targets.

</details>

#### Practice P02 · When the low pattern is negative

Newly written synthetic practice applies only the sign-extension reasoning of [EX:ca_2025_2_midterm_q04 p.2] and [EX:ca_2025_2_midterm_q13 p.5] (c) to the taught LUI construction. To make `0x2468ABCD`, a proposal combines upper `0x2468A` with low pattern `0xBCD` unchanged. Find the signed low value, incorrect result, and corrected two instructions.

<details><summary>Show solution</summary>

`0xBCD−0x1000=−0x433=−1075`. The incorrect sum is `0x2468A000−0x433=0x24689BCD`, one `0x1000` below the target. Use `lui x5,0x2468B` then `addi x5,x5,-1075`: `0x2468B000−0x433=0x2468ABCD`. Upper adjustment compensates for interpreting the low pattern as a signed operand.

**Checking points:** Verify −1075, the 0x1000 error, corrected upper portion, and final value.

</details>

### Review plan

Draw field boundaries for Q01–Q04 and write intermediate addresses/constants for Q05–Q06. Check design rationale in P01 and signed-immediate errors in P02 before tracing [[courses/computer_architecture/units/en/control-synchronization|control flow and synchronization]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 · lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 · lecture notes]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-022|p.22]], [[page_cache/computer_architecture/lec.03/page-023|p.23]], [[page_cache/computer_architecture/lec.03/page-025|p.25]], [[page_cache/computer_architecture/lec.03/page-026|p.26]], [[page_cache/computer_architecture/lec.03/page-027|p.27]], [[page_cache/computer_architecture/lec.03/page-028|p.28]], [[page_cache/computer_architecture/lec.03/page-029|p.29]], [[page_cache/computer_architecture/lec.03/page-061|p.61]], [[page_cache/computer_architecture/lec.03/page-062|p.62]], [[page_cache/computer_architecture/lec.03/page-063|p.63]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 56:21, 59:09, 01:03:54–01:04:49]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 01:05:39, 01:08:10–01:09:07]]

- This covers the basic 32-bit instruction subset, not every ISA extension's length. Detailed hexadecimal conversion and programs processing programs are materials-based supplementation.
- Unclear spoken field counts and LUI width remain unresolved speech. The materials establish six R fields and a 20-bit LUI constant.
- SB representability differs from instruction alignment. Examples use four-byte instruction starts, and two LUI/ADDI instructions do not construct every arbitrary 64-bit value.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.


---

[[courses/computer_architecture/units/en/data-register-memory|← Previous: Data Representation, Registers, and Memory]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/control-synchronization|Next: Bitwise Operations, Control Flow, and Synchronization →]]
