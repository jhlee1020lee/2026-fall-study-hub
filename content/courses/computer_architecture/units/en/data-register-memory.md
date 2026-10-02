---
title: "Data Representation, Registers, and Memory"
description: "Practice RV64 registers, byte addresses, integer interpretation, and value preservation."
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
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-08-lecture-03", "courses/computer_architecture/lectures/en/2026-09-03-lecture-02", "courses/computer_architecture/lectures/en/2026-09-10-lecture-04"]
---

Track register names, addresses, and stored values separately. Distinguishing byte order from signed interpretation makes load–compute–store errors easier to diagnose.

## The register file as a working space

Registers provide a small, nearby working space for frequently used processor values. The course's RV64 model has 32 general-purpose registers, `x0`–`x31`, each with a 64-bit data width. A 64-bit datum is a doubleword; a 32-bit datum is a word. The nominal sum of the register widths is therefore

$$
32\times64\text{ bits}=2048\text{ bits}=256\text{ bytes}.
$$

However, `x0` is hard-wired zero: it always reads as zero and cannot hold a newly written value. The entire nominal 256 bytes is therefore not freely writable storage. Roles such as `x1=ra` and `x2=sp` are principally calling-convention agreements for other registers. [CA M003 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-009) [CA M003 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-010) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 23:03]]

The spoken “128 bytes” at September 8 20:16 and 24:24 conflicts with the stated `32 × 8 bytes` organization. The 256-byte result is an explicit arithmetic correction in this explanation, not a claim that the transcript says something else. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 20:16]] [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 24:24]] The typical hierarchy register → cache → main memory → SSD/HDD trades increasing capacity for slower access. “Smaller is faster” is a design intuition, not an exceptionless law. [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]]

### Decomposing an expression into two-input operations

The notation `add a,b,c` means adding the register values represented by `b` and `c` and writing the result to `a`. A regular operand format makes common processing logic easier to reuse. In exchange, a compound expression such as `f=(g+h)-(i+j)` requires several instructions. [CA M003 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-007) [CA M003 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-008)

Using the slide's virtual register notation, compute `t0=g+h`, then `t1=i+j`, then `f=t0-t1`. Overwriting the first sum with the second would lose an operand needed by the subtraction. Here `t0`, `t1`, and the variable names are illustrative virtual names, as emphasized at September 8 17:48. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 17:48]]

When the compiler assigns `f,g,h,i,j` to `x19,x20,x21,x22,x23`, the source example becomes:

```asm
add x5,  x20, x21
add x6,  x22, x23
sub x19, x5,  x6
```

For newly supplied illustrative values `g=7,h=5,i=3,j=2`, the successive results are `x5=12`, `x6=5`, and `x19=7`. C variables do not universally belong to those registers; this is one allocation. The unclear spoken second destination is explained using the separate temporaries in slide page 8, without claiming recovered speech. [CA M003 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-011)

## Byte addresses and endianness

Arrays, structures, and dynamic data cannot all fit in a register file. A load-store architecture loads memory values into registers, operates on register values, and stores results back. Fetching an instruction from memory does not make its ALU operation a direct data-memory operation. [CA M003 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-012) The recalled exam's corresponding demand is to identify the actual source of ALU operands. [EX:ca_2025_2_midterm_q02 p.2] Exam connections here use a Fall 2025 reconstruction whose official wording and answers are not independently verified.

In byte-addressable memory, one address identifies one 8-bit byte. A 32-bit integer occupies four consecutive bytes. Endianness specifies their order as addresses increase.

| 32-bit value | Big endian: low to high addresses | Little endian: low to high addresses |
|---|---|---|
| `0xFF000000` | `FF 00 00 00` | `00 00 00 FF` |
| `0x00000001` | `00 00 00 01` | `01 00 00 00` |

The red first row and rightward address arrow in [CA M003 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-013) distinguish a byte's numerical significance from its address order. Little endian places the least-significant byte at the lowest address; big endian places the most-significant byte there. The course's execution model is little endian.

For an illustrative reading, bytes `01 00 00 00` at increasing addresses represent 1 in little endian and $2^{24}=16,777,216$ in big endian. The same bytes can therefore produce different values under different conventions. September 8 30:44 motivates agreement on byte order when machines exchange data over a network. The explanation need not assert particular network APIs or universal behavior across every ISA execution mode. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 30:44]]

## Effective addresses and array offsets

Keep a register name, its contents, and a memory value separate. `GPR[x5]` denotes the contents of `x5`; `MEM[a]` denotes the memory value at address `a`. The general addressing-mode comparison in [CA M008 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-015) uses these forms:

| Mode | Expression identifying the value read |
|---|---|
| Absolute | `MEM[10000]` |
| Register indirect | `MEM[GPR[rbase]]` |
| Displaced/based | `MEM[offset + GPR[rbase]]` |
| Indexed | `MEM[GPR[rbase] + GPR[rindex]]` |
| Memory indirect | `MEM[MEM[GPR[rbase]]]` |

This is materials-based ISA comparison associated with September 3, not a claim that RISC-V implements every form in one instruction. In the last row, the value obtained from memory is itself used as an address; this differs from a single base-plus-offset calculation. [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]

### Translating `A[12] = h + A[8]` into byte offsets

In [CA M003 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-014), `h` is in `x21`, the array base is in `x22`, and each element occupies 8 bytes. With zero-based indexing, `A[8]` is the ninth element, at byte offset $8\times8=64$. The thirteenth element, `A[12]`, begins at offset $12\times8=96$.

```asm
ld  x9, 64(x22)
add x9, x21, x9
sd  x9, 96(x22)
```

The first instruction reads the value at `GPR[x22]+64`; the second adds `h`; the third writes the sum at `GPR[x22]+96`. Offsets 64 and 96 count bytes, not elements. Neither offset is a statement of the array's total size. The “64 bytes array” phrase at 33:54 conflicts with accessing `A[12]` and is not adopted as the total array size. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 33:54]]

### Register allocation and immediate operands

Using memory values in computations introduces loads and stores, so a compiler tries to keep frequently used values in registers. When registers are insufficient, it spills some values to memory. This code-generation choice differs from microarchitectural optimization of the execution of a given instruction sequence. [CA M003 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-015) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 39:47]]

An immediate is a constant included directly in an instruction.

```asm
addi x22, x22, 4
```

This adds 4 to `x22` and writes the result back to it. Small constants such as +1 for an index and +4 or +8 for a pointer occur often. When a constant fits the immediate format, embedding it avoids a separate memory load for that constant. The width condition matters: arbitrary constants do not all fit one immediate. This illustrates “Make the common case fast.” [CA M003 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-016) The damaged compiler flags and default options in the September 10 demonstration are not reconstructed from this general principle. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 05:12]]

## Unsigned integers and two's complement

Endianness concerns byte **placement**; signedness concerns a bit pattern's **numerical meaning**. An $n$-bit unsigned integer is interpreted as

$$
x=\sum_{i=0}^{n-1}b_i2^i,\qquad 0\leq x\leq2^n-1.
$$

Thus `00001011` is $8+2+1=11$, and the 8-bit maximum is 255. The exact 64-bit unsigned maximum is **18,446,744,073,709,551,615**. The printed **18,446,774,073,709,551,615** in [CA M003 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-017) conflicts with that page's $2^{64}-1$ formula; the typo also propagated into historical notes and baselines. The value given here explicitly corrects the arithmetic without rewriting the original source or claiming different speech.

Even a very large fixed-width range cannot represent an arbitrarily large integer in one register. September 8 44:22 explains that larger integer representations in Python or scientific applications are implemented in software above the ISA. The internal algorithms of such libraries are not supplied. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 44:22]]

### Giving the most-significant bit a negative weight

Two's complement changes the most-significant bit's weight:

$$
x=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i,
\qquad -2^{n-1}\leq x\leq2^{n-1}-1.
$$

For 64 bits, the range is −9,223,372,036,854,775,808 through 9,223,372,036,854,775,807. A most-significant bit of 1 indicates a negative value; 0 indicates a non-negative value.

| Pattern | Signed meaning |
|---|---|
| `000…0` | 0 |
| `111…1` | −1 |
| `100…0` | Minimum |
| `011…1` | Maximum |

The source's 32-bit `11111111 11111111 11111111 11111100` evaluates to $-2,147,483,648+2,147,483,644=-4$. At a smaller width, 8-bit `0xFE` is 254 unsigned but $-128+126=-2$ signed. The bits remain unchanged; their interpretation changes. [CA M003 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-018) [CA M003 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-019)

Negation complements every bit and adds one. At 8 bits, +2 is `00000010`; complementing gives `11111101`; adding one gives the −2 pattern `11111110`. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 48:31]] [CA M003 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-020) In fixed-width arithmetic, $x+\mathord{\sim}x$ has all bits set, representing −1 modulo $2^n$. Consequently $\mathord{\sim}x+1$ has the same $n$-bit pattern as $-x$. However, the positive counterpart of the minimum signed value is outside the same signed range. A valid pattern calculation and a representable signed result are separate questions.

## Preserving a value when its width changes

Widening a signed two's-complement value requires copying its sign bit; widening an unsigned value fills the new upper positions with zero. In sign extension, the new negative top-bit weight and the added positive weights together preserve the original numerical value.

| 8-bit value | Value-preserving 16-bit representation |
|---|---|
| +2: `0000 0010` | `0000 0000 0000 0010` |
| −2: `1111 1110` | `1111 1111 1111 1110` |

A 12-bit signed immediate follows the same principle when extended to 64 bits: original bit 11 is copied into the upper 52 positions. That reasoning connects to the extension demand in recalled Q4. [EX:ca_2025_2_midterm_q04 p.2] Substituting zero extension would fail to preserve a negative immediate's value. [CA M003 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021)

For RV64 subword accesses, distinguish memory-access width from destination-register width.

| Memory width | Signed load | Unsigned load | Store |
|---:|---|---|---|
| 8 bits | `lb` | `lbu` | `sb` |
| 16 bits | `lh` | `lhu` | `sh` |
| 32 bits | `lw` | `lwu` | `sw` |

Signed loads sign-extend to the 64-bit destination; unsigned loads zero-extend. Loading memory byte `0x80` with `lb` produces `0xFFFFFFFFFFFFFF80`; `lbu` produces `0x0000000000000080`. Their signed numerical interpretations are −128 and 128. Stores instead write the low 8, 16, or 32 source-register bits, so they need no corresponding signed/unsigned extension distinction. Applying `sb` to either result writes the same byte, `0x80`. [CA M003 PDF p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057)

This joins September 8's byte-extension explanation with September 10's discussion of multiple access widths. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 53:56]] [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 58:31]] [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes]] C types and signedness influence instruction selection. The course's size examples for `char`, `short`, `int`, and `long long` must not be promoted to universal rules for every C implementation. Incorrect width or signedness can change values and cause errors, but the unclear vulnerability qualification at September 8 52:03 and damaged September 10 byte counts establish neither a specific exploit nor new width rules. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 52:03]]

## Key Takeaways

- RV64's 32×64 bits total a nominal 256 bytes; `x0` remains immutable.
- Array offsets equal index×element bytes; ALU computation and memory writes are separate effects.
- Endianness governs placement, signedness governs bit weights, and extension preserves values across widths.
- The unsigned 64-bit maximum is 18,446,744,073,709,551,615.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Register widths and roles

Calculate the nominal capacity of 32 64-bit registers and contrast `x0`, `x1=ra`, and `x2=sp`. What does smaller storage suggest in the hierarchy, without guaranteeing it?

<details><summary>Show solution</summary>

32×64/8=256 bytes, an arithmetic correction to the spoken 128 bytes. The nominal total does not make `x0` writable: it always reads zero, while `ra/sp` roles are principally calling conventions. A word is 32 bits and a doubleword 64 bits. Registers→cache→main memory→SSD/HDD typically trade growing capacity for slower access; smaller-is-faster is an intuition, not an exceptionless law.

**Checking points:** Check units, the `x0` exception, and convention versus enforced behavior.

</details>

#### Recall Q02 · Preserve intermediate sums

For `f=(g+h)-(i+j)`, use `f,g,h,i,j=x19,x20,x21,x22,x23` and `g,h,i,j=7,5,3,2`. Give the sequence and results with two temporaries, and explain destructive reuse of one temporary.

<details><summary>Show solution</summary>

`add x5,x20,x21` yields 12, `add x6,x22,x23` yields 5, and `sub x19,x5,x6` yields 7. Overwriting the first temporary with the second sum loses an operand. Two-input/one-output regularity supports shared hardware, while compound expressions need multiple instructions. The source's `t0/t1` are virtual names; the actual variable allocation is a compiler choice.

**Checking points:** Check all three results and why both sums must remain available.

</details>

#### Recall Q03 · Byte order and operand sources

Write increasing-address big/little-endian bytes for `0xFF000000` and `0x00000001`, and interpret `01 00 00 00` both ways. Does instruction fetch make an ALU operand a direct memory operand?

<details><summary>Show solution</summary>

The first value is big `FF 00 00 00`, little `00 00 00 FF`; the second is big `00 00 00 01`, little `01 00 00 00`. The given bytes mean 1 little-endian or 2^24=16,777,216 big-endian. Each address identifies an eight-bit byte, so 32 bits occupy four addresses. Load-store computation loads large data into registers, operates, then stores. Instruction fetch is distinct from the ALU's data-operand source. Communicating machines need a consistent byte interpretation.

**Checking points:** Distinguish low address from low numerical significance.

</details>

#### Recall Q04 · Address modes and array offsets

Express absolute, register-indirect, based, indexed, and memory-indirect addressing using `MEM`/`GPR`. Then trace `A[12]=h+A[8]` with `h=x21`, `base(A)=x22`, and eight-byte elements.

<details><summary>Show solution</summary>

The forms are `MEM[10000]`, `MEM[GPR[rbase]]`, `MEM[GPR[rbase]+offset]`, `MEM[GPR[rbase]+GPR[rindex]]`, and `MEM[MEM[GPR[rbase]]]`. The last uses a memory value as another address. The array sequence is `ld x9,64(x22); add x9,x21,x9; sd x9,96(x22)`. Offsets are 8×8=64 and 12×8=96 bytes for the ninth and thirteenth elements. They are not total array sizes. The general addressing list does not promise one RISC-V instruction per form.

**Checking points:** Check all five address forms and all three data movements.

</details>

#### Recall Q05 · Allocation, spills, and immediates

Why spill when registers are insufficient, and what is its cost? Explain `addi x22,x22,4` and distinguish compiler from microarchitectural optimization.

<details><summary>Show solution</summary>

Insufficient registers force some values into memory, adding loads/stores and access costs. The compiler changes allocations and instruction sequences; microarchitecture improves how a given sequence executes. `addi` embeds 4 and increments `x22` without a separate constant load. This helps common small constants only when they fit the immediate format.

**Checking points:** Include extra spill accesses and the immediate-width condition.

</details>

#### Recall Q06 · Unsigned values and fixed width

Evaluate `00001011`, the eight-bit unsigned maximum, and the exact 64-bit maximum. Does changing endianness or using large-integer software enlarge one fixed-width register's range?

<details><summary>Show solution</summary>

Positive bit weights give 8+2+1=11 and maximum 2^8−1=255. The exact 2^64−1 is 18,446,744,073,709,551,615; M003 p.17's 18,446,774,073,709,551,615, repeated historically, is a typo. This is an arithmetic correction, not a rewritten quotation. Endianness changes byte placement, not the range at fixed width. Large integers require software representations above the ISA rather than an unlimited single register.

**Checking points:** Check the exact decimal, the explicit source correction, and the width limit.

</details>

#### Recall Q07 · Two's complement and negation

Find signed/unsigned meanings of eight-bit `0xFE`, signed ranges, and zero/−1/min/max patterns. Explain 32-bit `0xFFFFFFFC`, negating +2, and the minimum-value exception.

<details><summary>Show solution</summary>

Eight-bit unsigned is 254, signed is −128+126=−2. The n-bit signed range is −2^(n−1) through 2^(n−1)−1; at 64 bits, −9,223,372,036,854,775,808 through 9,223,372,036,854,775,807. The patterns are `000…0`, `111…1`, `100…0`, `011…1`. The 32-bit example is −2,147,483,648+2,147,483,644=−4. Complementing `00000010` gives `11111101`, then adding one gives `11111110`. Since `x+~x` is all ones, or −1 modulo 2^n, `~x+1` is the −x pattern. The minimum's positive counterpart is outside the signed range, despite the valid modular pattern operation.

**Checking points:** Check negative top-bit weight, the modular justification, and the representability exception.

</details>

#### Recall Q08 · Preserve values while widening

Extend eight-bit +2 and −2 to 16 bits. For a signed 12-bit immediate widened to 64 bits, which bit fills how many positions, and when does zero extension change the value?

<details><summary>Show solution</summary>

The results are `0000000000000010` and `1111111111111110`. Replicated sign bits balance the new negative top weight with added positive weights, preserving the original value. A 12-bit signed immediate copies bit 11 into 52 new upper positions. Zero-extending a negative pattern instead produces a positive value; zero extension is appropriate for unsigned widening.

**Checking points:** Check bit 11, 52 positions, both patterns, and why the value is preserved.

</details>

#### Recall Q09 · Subword loads and stores

Compare widths and extension for `lb/lbu`, `lh/lhu`, `lw/lwu`, and `sb/sh/sw`. Load byte `0x80` with `lb` and `lbu`, then store each result with `sb`.

<details><summary>Show solution</summary>

Loads access 8/16/32 bits; signed variants sign-extend and unsigned variants zero-extend to the 64-bit destination. `lb` yields `0xFFFFFFFFFFFFFF80` (−128), while `lbu` yields `0x0000000000000080` (128). Stores write only low 8/16/32 bits, so either `sb` writes `0x80`. Different register values can therefore yield the same narrow store. C types/signedness affect selection, but example sizes are not universal C rules, and uncertain speech establishes no specific exploit.

**Checking points:** Separate access width from destination width and explain why stores need no extension variant.

</details>

### Apply the ideas

#### Practice P01 · Different values from the same byte

Newly written synthetic practice. Let `x10=0x3000` and byte memory at `0x3003` contain `0xFE`. A executes `lb x5,3(x10); addi x5,x5,1; sb x5,4(x10)`; B replaces only `lb` with `lbu`. Compare register values and stored bytes, then assess 'equal stored bytes imply equal computation meanings' and 'the ALU directly added the memory byte.'

Connection: operand sourcing from [EX:ca_2025_2_midterm_q02 p.2] and value preservation from [EX:ca_2025_2_midterm_q04 p.2] are combined into observation and error diagnosis. Prerequisites: Q03, Q04, Q08, Q09; byte widening is a new application of the taught mechanism.

<details><summary>Show solution</summary>

A loads −2 and adds one to get −1 (`0xFFFFFFFFFFFFFFFF`). B loads 254 and reaches 255 (`0x00000000000000FF`). Both store low byte `FF` at `0x3004`, but their 64-bit meanings differ. The effective load address is 0x3000+3; the load first fills a register. `addi` adds that register value and immediate 1, not a direct memory operand.

**Checking points:** Check both 64-bit results, the common low byte, both effective addresses, and operand sourcing.

</details>

### Short review plan

Trace Q02 and Q04 by hand, then check Q06–Q09 through bit arithmetic. On the next review, repair P01's incorrect explanations before opening its solution.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 lecture notes]]
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057)
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-015)
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 17:48, 20:16, 23:03, 24:24, 30:44, 33:54, 39:47, 44:22, 48:31, 52:03, 53:56 (plain timestamps within the page)
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 corrected transcript]] — 05:12, 58:31 (plain timestamps within the page)

The September 3 addressing-mode comparison is materials-only; not every mode is one RISC-V instruction. Arithmetic and slides distinguish the September 8 128-byte claim, array-size wording, and uncertain temporary name. The M003 p.17 unsigned64 typo propagated to historical notes; the explanation corrects it using 2^64−1. Damaged September 10 compiler flags/byte counts remain unresolved, and C type examples are not universal implementation rules.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
Selected reasoning connections: [EX:ca_2025_2_midterm_q02 p.2], [EX:ca_2025_2_midterm_q04 p.2].
