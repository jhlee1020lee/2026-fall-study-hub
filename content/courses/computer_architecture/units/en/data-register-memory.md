---
title: "Data Representation, Registers, and Memory"
description: "Check register arithmetic, byte addresses, endianness, integer representations, and load/store widths."
course: "computer_architecture"
unit_id: "data-register-memory"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf", "lec 02.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-03-lecture-02", "courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-10-lecture-04"]
---

Trace code by distinguishing register values, memory bytes, and addresses. Explicit element sizes and signedness let you diagnose offset and load/store mistakes.

## The register file and storage hierarchy

Where values reside affects both instruction structure and execution cost. Registers, introduced in the [architectural-state model](architecture-contract.md), are small storage locations inside the processor. The course's RV64 model has **32 general-purpose registers, `x0`–`x31`, each 64 bits wide**. A 64-bit datum is a doubleword; a 32-bit datum is a word. A 64-bit register does not make every memory access or instruction 64 bits long. [[page_cache/computer_architecture/lec.03/page-009|CA M003 p.9]]

The nominal combined width is `32 × 64 / 8 = 256 bytes`. At 20:16 on September 8, “32 times 8 bytes” conflicts with the spoken “128 bytes.” **256 bytes is the correction derived from the stated organization**, not a repaired quotation. Moreover, `x0` is hard-wired zero: attempts to write it do not change subsequent reads. All 256 nominal bytes are therefore not freely writable storage. Roles such as `x1=ra` and `x2=sp` are primarily calling-convention agreements. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 20:16–23:03]]

The typical hierarchy proceeds from registers through cache and main memory to SSD/HDD storage, with increasing capacity and slower access. Frequently used values belong in the small, fast end when possible. “Smaller is faster” expresses a design intuition; the lecturer explicitly qualified it rather than asserting a universal law. Cache implementation is a later topic.

## Arithmetic and preserving intermediate results

`add a,b,c` adds the register values `b` and `c` and writes `a`. A regular two-source, one-destination form makes hardware processing logic easier to share: “Simplicity favors regularity.” Compound expressions are decomposed into these small operations.

For `f = (g + h) - (i + j)`, compute the two sums before subtracting. An abstract notation is `add t0,g,h; add t1,i,j; sub f,t0,t1`. Here `t0` and `t1` name intermediate virtual registers in the example. Overwriting the first sum while producing the second would destroy an input needed by the subtraction. M003 p.8 uses `t1` as the second destination; that material supports the explanation where the transcript's `t0`/`t1` wording is unclear.

With `f,g,h,i,j` allocated to `x19,x20,x21,x22,x23`, the source's concrete sequence is: [[page_cache/computer_architecture/lec.03/page-011|CA M003 p.11]]

```asm
add x5,  x20, x21
add x6,  x22, x23
sub x19, x5,  x6
```

For an illustrative `g=8,h=3,i=4,j=2`, the intermediate values are `x5=11` and `x6=6`, giving `x19=5`. A C variable does not intrinsically belong to one architectural register; the compiler chooses this allocation. Regular instruction forms simplify implementation while requiring multiple instructions for compound computations.

## Load-store organization and byte-addressable memory

Large arrays, structures, and dynamic data do not fit entirely into the register file. A load-store architecture loads memory data into registers, computes on register values, and stores results back. The rule that ALU instructions do not directly use memory operands is compatible with using register values to calculate addresses. Recalled 2025-2 Q2 demands precisely that distinction. [EX:ca_2025_2_midterm_q02 p.2]

In byte-addressable memory, one address identifies one 8-bit byte. A 32-bit integer occupies four consecutive byte addresses. Endianness relates byte significance to increasing address order.

| 32-bit value | Big endian: increasing addresses | Little endian: increasing addresses |
|---|---|---|
| `0xFF000000` | `FF 00 00 00` | `00 00 00 FF` |
| `0x00000001` | `00 00 00 01` | `01 00 00 00` |

The address arrows in [[page_cache/computer_architecture/lec.03/page-013|CA M003 p.13]] point rightward. Big endian places the most-significant byte first; little endian places the least-significant byte first. Neither operation reverses the bits inside each byte. Bytes `01 00 00 00` in increasing address order mean 1 in little endian but `1 × 256³ = 16,777,216` in big endian.

The course uses a little-endian model, without establishing that every environment uses that order. The lecturer added the network motivation: machines exchanging multibyte values must agree on how to interpret their bytes. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 30:44]] Endianness concerns storage order; signedness concerns the numerical interpretation of a pattern.

## Addressing modes and array byte offsets

`GPR[x5]` denotes a register value and `MEM[a]` a memory value at address `a`. An addressing mode specifies how to locate the desired data. The September 3 materials compare these general modes; they are not all necessarily single RISC-V instructions. [[page_cache/computer_architecture/lec.02/page-015|CA M008 p.15]]

| Mode | Value being read |
|---|---|
| Absolute | `MEM[10000]` |
| Register indirect | `MEM[GPR[rbase]]` |
| Displaced/based | `MEM[GPR[rbase] + offset]` |
| Indexed | `MEM[GPR[rbase] + GPR[rindex]]` |
| Memory indirect | `MEM[MEM[GPR[rbase]]]` |

The source's `ld x9,64(x22)` reads a doubleword from the address obtained by adding 64 **bytes** to `x22`. For `A[12] = h + A[8]` with `h=x21`, array base `x22`, and 8-byte elements:

```asm
ld  x9, 64(x22)
add x9, x21, x9
sd  x9, 96(x22)
```

Zero-based `A[8]` is the ninth element, at offset `8×8=64`. `A[12]` is the thirteenth, at `12×8=96`. With an illustrative base `0x1000`, the read address is `0x1040` and the write address `0x1060`. Adding 12 directly confuses an element count with a byte displacement. [[page_cache/computer_architecture/lec.03/page-014|CA M003 p.14]] The spoken “64 bytes array” cannot describe this example's entire array: `A[12]` must also occupy valid storage.

## Register allocation and immediates

Register allocation assigns frequently used values to registers. When too many values are needed simultaneously, the compiler may spill some to memory and load them again later. This changes the instruction sequence being generated; it is distinct from microarchitectural optimization of a fixed sequence.

An immediate is a constant represented directly inside an instruction. `addi x22,x22,4` adds 4 and writes the result back to `x22`. Increments such as +1 for loop indices and +4 or +8 for pointers are common. Avoiding a separate memory load for an encodable constant illustrates “Make the common case fast.” [[page_cache/computer_architecture/lec.03/page-016|CA M003 p.16]] [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 39:47]]

The same C source can produce different instruction counts and memory accesses under different compiler choices. The September 10 demonstration commands and options at 05:12–06:12 are unclear, so they do not establish a particular flag or universal speedup factor. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 05:12–06:12]] Immediate ranges are also limited; [instruction encoding and address construction](instruction-encoding.md) explains larger constants.

## Unsigned interpretation and two's complement

A numerical value comes from applying weights to a bit pattern. For bits `b_i` in an n-bit unsigned integer:

$$
x=\sum_{i=0}^{n-1}b_i2^i,\qquad 0\le x\le 2^n-1.
$$

M003 p.17's `00001011` is `8+2+1=11`. The final subscript 10 indicates decimal notation, not a result of 1110. The maximum unsigned 64-bit value is **`2^64−1 = 18,446,744,073,709,551,615`**. Subtracting one from `2^64 = 18,446,744,073,709,551,616` gives this result. The decimal maximum printed on [[page_cache/computer_architecture/lec.03/page-017|CA M003 p.17]] and carried into the earlier baseline is an arithmetic typo; the calculation here explicitly corrects it. The range is large but finite. Larger integers mentioned in the Python/scientific-application discussion are represented by software above the ISA using more storage, not by an infinitely wide register. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 44:22]]

Two's complement changes the weight of the most-significant bit to a negative weight:

$$
x=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i,\qquad
-2^{n-1}\le x\le 2^{n-1}-1.
$$

| Pattern | Signed meaning |
|---|---|
| `000…0` | 0 |
| `111…1` | −1 |
| `100…0` | Minimum, `−2^(n−1)` |
| `011…1` | Maximum, `2^(n−1)−1` |

A leading 1 indicates a negative value; a leading 0 indicates a nonnegative value. The 64-bit range is −9,223,372,036,854,775,808 through 9,223,372,036,854,775,807. M003 p.18's 32-bit `111…1100` gives `−2,147,483,648+2,147,483,644=−4`. The 8-bit pattern `11111110` is 254 unsigned but `−128+126=−2` signed. There is no separate signedness tag attached to those stored bits.

To negate, complement every bit and add one. Starting with 8-bit +2, `00000010` becomes `11111101`, then `11111110`, representing −2. [[page_cache/computer_architecture/lec.03/page-020|CA M003 p.20]] Fixed-width representability still matters: the positive counterpart of the minimum signed value exceeds the maximum by one and cannot be represented at that width.

## Sign extension and load/store widths

To widen a value while preserving it, use sign extension for two's-complement signed values and zero extension for unsigned values. Widening from 8 to 16 bits maps +2 as `0000 0010 → 0000 0000 0000 0010` and −2 as `1111 1110 → 1111 1111 1111 1110`. Filling −2's upper bits with zeros would produce 254 instead. [[page_cache/computer_architecture/lec.03/page-021|CA M003 p.21]]

An RV64 load can read fewer bits than its destination register holds, so it must define the remaining upper bits.

| Access width | Sign-extended load | Zero-extended load | Store of that width |
|---|---|---|---|
| Byte, 8 bits | `lb` | `lbu` | `sb` |
| Halfword, 16 bits | `lh` | `lhu` | `sh` |
| Word, 32 bits | `lw` | `lwu` | `sw` |

Loading memory byte `0x80` with `lb` produces `0xFFFFFFFFFFFFFF80`; `lbu` produces `0x0000000000000080`. Their signed interpretations are −128 and 128. In contrast, `sb`, `sh`, and `sw` write only the low 8, 16, or 32 source-register bits. They need no signed/unsigned distinction for filling high bits. [[page_cache/computer_architecture/lec.03/page-057|CA M003 p.57]]

C type widths and signedness affect the compiler's load selection. The lecture warned that an unintended extension can change a value and cause errors or vulnerabilities. [[courses/computer_architecture/transcripts/2026-09-08|September 8 STT, 53:56]] This does not establish a particular exploit or make the lecture's C-size examples universal rules for all implementations. The same preservation principle applies when widening a negative immediate: extend **the immediate's value**, not a register number.

## Key Takeaways

- The RV64 register file has a nominal 256-byte width; `x0` remains zero.
- Preserve intermediate results until their last use.
- Array displacement is index times element size in bytes; an address differs from its contents.
- Endianness specifies byte order; signedness specifies numerical interpretation.
- Narrow loads define upper bits, while stores write only the specified low bits.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Register capacity and widths

Calculate nominal register-file bytes from RV64's count and width, explaining `x0`'s limitation. Distinguish word, doubleword, instruction length, and the typical storage hierarchy.

<details><summary>Show solution</summary>

`32×64/8=256 bytes`, but writes to `x0` do not persist: it reads zero. A word is 32-bit data and a doubleword 64-bit data; register width does not determine every access or instruction length. Registers→cache→main memory→SSD/HDD typically increases capacity and access time. Roles such as `ra`/`sp` are conventions, and smaller storage is not universally faster.

**Checking points:** Check 256 bytes, `x0`, width distinctions, and the qualified hierarchy.

</details>

#### Recall Q02 · Preserve intermediate sums

With `g,h,i,j=8,3,4,2` in `x20`–`x23`, compute `f=(g+h)-(i+j)` using `x5` and `x6`. Explain the error of also writing the second sum into `x5`, and whether C variables have these registers intrinsically.

<details><summary>Show solution</summary>

`add x5,x20,x21` produces 11; `add x6,x22,x23` produces 6; `sub x19,x5,x6` produces 5. Overwriting the first sum loses the required 11. Multiple regular two-source/one-destination operations implement the expression, and the register allocation is a compiler choice.

**Checking points:** Show all three values, the preservation requirement, and the nature of allocation.

</details>

#### Recall Q03 · Interpreting memory bytes

Why do large arrays need load/store access? Interpret bytes `01 00 00 00` in increasing addresses as little- and big-endian unsigned values; give both byte orders for `0xFF000000` and explain the communication issue.

<details><summary>Show solution</summary>

Large arrays exceed small register storage, and ALU computation uses loaded register values. The bytes mean 1 little-endian and `1×256³=16,777,216` big-endian. `0xFF000000` is `FF 00 00 00` big-endian and `00 00 00 FF` little-endian. One address identifies one byte; bits inside a byte are not reversed. Communicating machines must agree on multibyte interpretation.

**Checking points:** Check both values, both byte orders, load-store motivation, and communication implications.

</details>

#### Recall Q04 · Read addressing modes as expressions

Let `rbase=100`, `rindex=8`, and offset=4. Write expressions for absolute `MEM[10000]`, register-indirect, based, indexed, and memory-indirect reads. If `MEM[100]=500`, what is the final memory-indirect address?

<details><summary>Show solution</summary>

They read `MEM[10000]`, `MEM[100]`, `MEM[104]`, `MEM[108]`, and `MEM[MEM[100]]=MEM[500]`. The last uses the value 500 read at address 100 as another address; register contents, the first memory value, and final data differ. This is a general mode comparison, not a claim that every expression is one RISC-V instruction.

**Checking points:** Check all five expressions and the two memory references in memory-indirect access.

</details>

#### Recall Q05 · From array index to byte offset

For 8-byte elements, base `0x1000`, `h=5`, and `A[8]=7`, trace the taught `A[12]=h+A[8]`. Give read/write addresses, result, and minimum array space needed.

<details><summary>Show solution</summary>

The load displacement is `8×8=64`, giving `0x1040`. Load 7, add 5, and store 12 at displacement `12×8=96`, address `0x1060`. These are the ninth and thirteenth elements, requiring at least 13 elements or 104 bytes. A whole-array size of 64 bytes cannot accommodate these accesses.

**Checking points:** Separate addresses from data; include scaling and storage for the final element.

</details>

#### Recall Q06 · Spilling and immediates

What can a compiler do when registers are insufficient, and how does that differ from microarchitectural optimization? Explain the benefit and limit of immediate 4 in `addi x22,x22,4`.

<details><summary>Show solution</summary>

The compiler can spill values to memory and reload them, changing the instruction sequence and accesses. Microarchitecture can improve how a given sequence executes. Encoding 4 inside the instruction avoids a separate constant load and helps common small increments. The constant must fit the immediate field; unclear demonstration wording supplies no particular flag or universal speedup.

**Checking points:** Explain spill/reload, optimization layers, avoided load, and the encoding-range condition.

</details>

#### Recall Q07 · Finite unsigned ranges

Compute 8-bit `00001011` and all ones from positional weights. Give the exact unsigned 64-bit maximum and explain why larger Python integers do not imply an infinitely wide register.

<details><summary>Show solution</summary>

`00001011=8+2+1=11`; eight ones give `Σ2^i` for `i=0…7`, or 255. The maximum is `2^n−1`, hence `18,446,744,073,709,551,615` for 64 bits: one less than `18,446,744,073,709,551,616`. This corrects the slide's decimal typo. Software can represent larger integers using multiple storage locations. Endianness concerns byte placement, not this positional weighting rule.

**Checking points:** Check 11, 255, the exact 64-bit value, and the finite-width/software distinction.

</details>

#### Recall Q08 · Two's complement and negation

Interpret 8-bit `11111110` unsigned and signed, then negate +2. Give the patterns for zero, −1, minimum, and maximum signed 8-bit values and explain negating the minimum.

<details><summary>Show solution</summary>

Unsigned it is 254; signed it is `−128+126=−2`. Complementing +2 (`00000010`) gives `11111101`, then adding one gives `11111110`. Zero is `00000000`, −1 is `11111111`, minimum −128 is `10000000`, and maximum 127 is `01111111`. Positive 128 is outside −128…127, so negating the minimum cannot represent its mathematical positive counterpart. The same asymmetry holds for `−2^63…2^63−1`.

**Checking points:** Check weights, both negation steps, all four patterns, and the representability boundary.

</details>

#### Recall Q09 · Extension and store width

Compare sign and zero extension of −2 from 8 to 16 bits. Give RV64 widths for `lb/lbu`, `lh/lhu`, `lw/lwu`, and `sb/sh/sw`; explain what differs and agrees when loading byte `0x80` and then using `sb`.

<details><summary>Show solution</summary>

Sign extension of `11111110` gives `1111111111111110` (−2); zero extension gives `0000000011111110` (254). The signed/unsigned load pairs read 8, 16, and 32 bits and sign/zero extend respectively. Loading `0x80` yields `0xFFFFFFFFFFFFFF80` (−128) with `lb`, versus `0x0000000000000080` (128) with `lbu`. Stores `sb/sh/sw` write low 8/16/32 bits, so either result stored by `sb` writes `0x80`. Load choice depends on intended type/width; stores do not fill upper bits.

**Checking points:** Check all widths, both extensions, and why equal stored bytes do not imply equal register values.

</details>

### Apply and diagnose

#### Practice P01 · Different values hidden by the same byte

Newly written synthetic practice extends the load-store operand distinction in [EX:ca_2025_2_midterm_q02 p.2]. Prerequisites are the taught immediates, extension, and store widths. Valid address `x10=0x2000` holds byte `0x80`; output address `0x2001` is valid too. One run starts with `lb x5,0(x10)`, the other with `lbu x5,0(x10)`, then both execute `addi x5,x5,1; sb x5,1(x10)`. Compare final `x5` and output byte; does equal output prove equal computations?

<details><summary>Show solution</summary>

The `lb` path computes −128+1=−127, `x5=0xFFFFFFFFFFFFFF81`; the `lbu` path computes 128+1=129, `x5=0x0000000000000081`. Both stores write low byte `0x81`. `addi` operates on a register value and immediate, not directly on memory or the address held in `x10`. Different final register values disprove the claim that equal stored bytes establish equal computations.

**Checking points:** Check both full-width results, output address/byte, and register-operand semantics.

</details>

### Review plan

Work through storage, arithmetic, and addressing in Q01–Q06, then calculate bit weights and extensions in Q07–Q09. Use P01 to check whether an identical stored byte hid different register values, then continue to [[courses/computer_architecture/units/en/instruction-encoding|instruction encoding]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 · materials-only review]]
- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 · lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 · lecture notes]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-007|p.7]], [[page_cache/computer_architecture/lec.03/page-008|p.8]], [[page_cache/computer_architecture/lec.03/page-009|p.9]], [[page_cache/computer_architecture/lec.03/page-011|p.11]], [[page_cache/computer_architecture/lec.03/page-012|p.12]], [[page_cache/computer_architecture/lec.03/page-013|p.13]], [[page_cache/computer_architecture/lec.03/page-014|p.14]], [[page_cache/computer_architecture/lec.03/page-015|p.15]], [[page_cache/computer_architecture/lec.03/page-016|p.16]], [[page_cache/computer_architecture/lec.03/page-017|p.17]], [[page_cache/computer_architecture/lec.03/page-019|p.19]], [[page_cache/computer_architecture/lec.03/page-020|p.20]], [[page_cache/computer_architecture/lec.03/page-021|p.21]], [[page_cache/computer_architecture/lec.03/page-057|p.57]]
- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-015|p.15]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 20:16–23:03, 30:44, 39:47, 44:22, 53:56]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 05:12–06:12, 58:31–01:03:52]]

- The general addressing-mode classification supplements September 3 materials without a recording; not every mode is one RISC-V instruction.
- The September 8 claim of 128 bytes conflicts with 32×8=256. Unclear second-sum destination and whole-array-size wording are distinguished using the materials, not recovered as speech.
- The unsigned 64-bit decimal numeral on lec.03 p.17 is an arithmetic typo; the correct maximum is 18,446,744,073,709,551,615.
- Unclear compiler-option demonstration and vulnerability wording remain unresolved. Detailed load/store widths combine both dates and do not establish universal C type sizes.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.


---

[[courses/computer_architecture/units/en/program-translation-loading|← Previous: Program Translation, Linking, and Loading]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/instruction-encoding|Next: Instruction Encoding and Address Construction →]]
