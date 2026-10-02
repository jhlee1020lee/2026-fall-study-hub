---
title: "Program Translation, Linking, and Loading"
description: "Trace symbols and relocation through loading into register and memory changes."
course: "computer_architecture"
unit_id: "program-translation-loading"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 02.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-03-lecture-02", "courses/computer_architecture/lectures/en/2026-09-08-lecture-03"]
---

Translating each file still leaves names and addresses to connect. Separate linking, loading, and execution to track when values actually change.

## Separate compilation and symbol connections

A program divided among source files must still find its functions and data in one consistent address space when it runs. Separate compilation translates each file independently, but need not determine every final address of a name defined elsewhere. Linking closes that gap. This discussion reviews the instructor material associated with [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]; it does not reconstruct that day's unrecorded spoken coverage.

In [CA M008 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-019), `main.c` defines `int buf[2] = {1, 2};` and calls `swap()` from `main`. The accompanying `swap.c` is:

```c
extern int buf[];
int *bufp0 = &buf[0];
static int *bufp1;

void swap()
{
    int temp;
    bufp1 = &buf[1];
    temp = *bufp0;
    *bufp0 = *bufp1;
    *bufp1 = temp;
}
```

A pointer holds an address; `*bufp0` accesses the value at that address. After `bufp0` points to the first element and `bufp1` to the second, the assignments have these effects:

| Statement completed | `temp` | `buf[0]` | `buf[1]` |
|---|---:|---:|---:|
| `temp = *bufp0;` | 1 | 1 | 2 |
| `*bufp0 = *bufp1;` | 1 | 2 | 2 |
| `*bufp1 = temp;` | 1 | 2 | 1 |

The second assignment overwrites the first element, so its old value must first be preserved in `temp`. The final array is `{2, 1}`. This is a trace of the instructor's small example, not a current assignment implementation or a newly executed experiment.

### Global symbols, external references, and local symbols

A symbol is a name through which linking connects definitions and references. The red annotations in [CA M008 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-020) distinguish a C local variable from a linker-local symbol.

| Example element | Role in linking |
|---|---|
| Definitions of `main` and `buf` in `main.c` | Global symbols available for cross-file connections |
| Use of `swap` in `main.c` | External reference requiring a definition elsewhere |
| Definitions of `swap` and `bufp0` in `swap.c` | Global symbols |
| `extern int buf[]` and uses of `buf` in `swap.c` | References to an array defined in another file |
| File-scope `static int *bufp1` | A linker-local symbol restricted to that file |
| Automatic `temp` inside the function | A run-time local variable, not a cross-file symbol-resolution target in this example |

In particular, `bufp0` is a pointer defined in this file, while its initialization depends on the address of `buf` defined elsewhere. Defining one name and referencing another within that definition can happen together. Calling both `static bufp1` and automatic `temp` merely “local” hides a distinction the linker needs.

## From translation to an executable

Assembly code is human-readable notation for machine instructions, and an assembler translates it into binary machine code. A pseudo-instruction can expand into multiple machine instructions, so assembly source lines need not equal the final instruction count. [CA M008 PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-028)

In [CA M008 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-021), `main.c` and `swap.c` independently pass through translators `cpp`, `cc1`, and `as`, yielding `main.o` and `swap.o`. These objects are both separately compiled and relocatable. A compiler driver can coordinate the tool invocations; linker `ld` connects the objects into executable `p`. The driver command printed in the slide illustrates this flow; it is not a command executed here.

Linking remains necessary even after binary instructions exist. **Symbol resolution** determines which definition a name denotes. **Relocation** adjusts address references to match the final placement of code and data. Identifying an object and determining its final address are related but distinct tasks.

Reading [CA M008 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-022) from the separate objects on the left toward the executable on the right reveals these relationships:

| Content | Location in the objects | Meaning after linking |
|---|---|---|
| Code for `main` and `swap` | Each object's `.text` | Included in the executable's code layout |
| Initialized `buf` and `bufp0` | `.data` | Data placement and referenced addresses are determined |
| File-scope `bufp1` | `.bss` | Storage is assigned in the combined layout |
| Headers, `.symtab`, `.debug` | Format, symbol, and debugging information | Not all equivalent to ordinary run-time program data |

Thus, simply concatenating object files is an incomplete account. References crossing object boundaries must agree with the final layout. Detailed relocation types and dynamic-linker implementation are beyond this figure.

## Loading and instruction-driven state changes

A loader prepares an executable's memory image for execution. [CA M008 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-023) places ELF sections beside a run-time memory layout. It groups `.init`, `.text`, and `.rodata` into a read-only segment, and `.data` and `.bss` into a read/write segment. The runtime also includes a heap, a shared-library mapping region, and a user stack, with a kernel region above. The addresses illustrate a particular 32-bit address space, not a fixed layout for every RV64 program.

File information and run-time storage are not identical categories. Symbol and debugging information, for example, should not all be treated as the ordinary data segment containing program variables. Loading prepares the execution environment; the ISA supplies the meaning of the instructions placed there.

### Tracing values and addresses through three instructions

The starting state in [CA M008 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-024) is `PC = 0x1000`, `GPR[x10] = 0x2000`, and `MEM[0x2000] = 41`. Here `GPR[x10]` denotes the value in a register, while `MEM[a]` denotes the memory value at address `a`.

```asm
lw   x5, 0(x10)
addi x5, x5, 1
sw   x5, 0(x10)
```

| Instruction address | Operation | `x5` afterward | `MEM[0x2000]` afterward | Next PC |
|---|---|---:|---:|---|
| `0x1000` | Read a word at base `0x2000` plus offset 0 | 41 | 41 | `0x1004` |
| `0x1004` | Add immediate 1 to the register value | 42 | 41 | `0x1008` |
| `0x1008` | Store the register's word at the same address | 42 | 42 | `0x100C` |

The value 41 read by `lw` is different from its address `0x2000`. After `addi` changes the register to 42, memory still contains 41. Only the final `sw` changes memory to 42. Each instruction in this sequential example is 32 bits, or 4 bytes, so PC advances by 4. This trace connects the instructions produced by translation to the state changed by execution, and leads into the register and load-store explanations in [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes]].

## Key Takeaways

- Symbol resolution chooses definitions; relocation adjusts final address references.
- File-scope `static` and automatic function locals have different linker roles.
- Loading prepares a memory image; instruction semantics govern subsequent state changes.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Trace the swap

Given `buf={1,2}`, `bufp0=&buf[0]`, `bufp1=&buf[1]`, trace `temp=*bufp0; *bufp0=*bufp1; *bufp1=temp;` one assignment at a time. Why retain `temp`?

<details><summary>Show solution</summary>

First `temp=1` and the array remains `{1,2}`; next it becomes `{2,2}`; finally `{2,1}`. A pointer stores an address, while dereferencing accesses its value. Saving 1 before overwriting the first element preserves the value needed for the last assignment.

**Checking points:** Check addresses versus values, all intermediate arrays, and preservation of the old value.

</details>

#### Recall Q02 · Three symbol roles

Classify `main`, `buf`, and the use of `swap` in `main.c`, then `swap`, `bufp0`, `extern int buf[]`, file-scope `static bufp1`, and automatic `temp` in `swap.c`.

<details><summary>Show solution</summary>

Definitions of `main`, `buf`, `swap`, and `bufp0` are global symbols. The `swap` use in `main.c` and `buf` reference in `swap.c` require definitions elsewhere. Defining `bufp0` can simultaneously reference the external address of `buf`. File-scope `static bufp1` is linker-local; automatic `temp` is a run-time function local, not this example's cross-file symbol-resolution target.

**Checking points:** Include the simultaneous definition of `bufp0` and reference to `buf`.

</details>

#### Recall Q03 · Objects into an executable

Connect `cpp`, `cc1`, `as`, and `ld` with symbol resolution, relocation, and `.text`, `.data`, `.bss`, `.symtab`, `.debug`. Why link existing machine code, and why not count assembly lines as machine instructions?

<details><summary>Show solution</summary>

Each C file passes through preprocessing, compilation, and assembly to a separate relocatable object; `ld` links the executable, and a driver can coordinate these tools. Resolution selects a definition; relocation adjusts references to final placement, so concatenation is insufficient. `main`/`swap` code belongs to `.text`, initialized `buf`/`bufp0` to `.data`, and `bufp1` to `.bss`. Headers and symbol/debug information are not ordinary variable data. Pseudo-instructions can expand into several machine instructions, so line count need not equal IC.

**Checking points:** Separate name binding from address adjustment and classify all example sections.

</details>

#### Recall Q04 · Loading and the address space

Explain the ELF figure's read-only/read-write segments and heap, shared-library, stack, and kernel regions. Separate loader and ISA responsibilities; are the illustrated addresses fixed for every RV64 execution?

<details><summary>Show solution</summary>

The figure groups `.init/.text/.rodata` as read-only and `.data/.bss` as read/write, alongside the run-time heap, shared-library mappings, user stack, and upper kernel region. The loader prepares the image; the ISA defines how loaded instructions transform state. Symbol/debug information is not all ordinary variable data. This particular 32-bit address-space illustration does not fix every RV64 layout.

**Checking points:** Distinguish file sections from run-time regions and retain the 32-bit-example limit.

</details>

#### Recall Q05 · Load, compute, then store

Start with `PC=0x1000`, `x10=0x2000`, and `MEM[0x2000]=41`. Trace `lw x5,0(x10); addi x5,x5,1; sw x5,0(x10)` through `x5`, memory, and PC after each four-byte instruction.

<details><summary>Show solution</summary>

The triples `(x5,memory,PC)` are `(41,41,0x1004)`, `(42,41,0x1008)`, and `(42,42,0x100C)`. Address `0x2000` is distinct from value 41. Arithmetic changes the register; only the store changes memory. PC advances once per four-byte instruction.

**Checking points:** Check that memory is still 41 immediately after `addi`.

</details>

### Apply the ideas

#### Practice P01 · What does each stage establish?

Newly written material-based general practice. Someone argues that producing both `.o` files fixes the external `swap` address and has already swapped `buf`, and calls all `.debug` information variable data. Diagnose each claim and identify the steps needed to establish the execution result.

None of the 18 candidates directly tests symbol resolution, relocation, or ELF loading, so no matching exam-style evidence is claimed.

<details><summary>Show solution</summary>

Object generation establishes separate translation. Linking must resolve cross-file names and relocate final references. Loading prepares an image; the swap assignments must execute before `{2,1}` follows. `.debug` is debugging information, distinct from initialized variables in `.data`. Completion of one stage does not establish later execution effects.

**Checking points:** Give the stage order and what each stage does and does not establish.

</details>

### Short review plan

Classify symbols and sections with Q01–Q03, then connect Q04–Q05. Use P01 to identify what each stage proves; redraw Q05's register/memory trace the next day.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 lecture notes · materials only]]
- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 lecture notes · related prerequisites]]
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-024), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-028)

This is September 3 materials-only review, not recorded spoken coverage. The September 8 note supplies related register/load-store explanations. The source code is a reading example, not an executed experiment or current assignment implementation.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
