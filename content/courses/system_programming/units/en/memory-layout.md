---
title: "Process Memory, Alignment, and Parameter Passing"
description: "Review process storage, padding, unions, value passing, and IA-32 frames."
course: "system_programming"
unit_id: "memory-layout"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["06.MM.Variable.and.Memory.Recap.pptx", "EE209 AssemblyFunctions.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Identify the process and object before interpreting an address. Separate size, alignment, and calling conventions to turn memory diagrams into checkable calculations and traces.

## Process address spaces and actual storage

Identical printed addresses do not prove that two processes share one object. A [pointer](objects-pointers.md) is interpreted within a process's address space; different spaces can use the same numerical addresses. In the [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 memory-layout lecture]], `layout.c` prints addresses of functions, globals, locals, heap objects, and shared objects together with process IDs.

In the supplied output, processes 16074 and 16075 independently advance `global_int` through 0, 1, … even though it has the same numerical virtual address. Their work instead contributes to one `shared_int` sequence from 0 through 7. Mapping and object role, not address equality alone, determine sharing. The [[courses/system_programming/transcripts/2026-09-23|2026-09-23 transcript]] at 09:18–12:08 demonstrates the distinction. Semaphore details were deferred that day; [Virtual Memory](virtual-memory.md) connects it to the actual September 28 `mmap` and `fork` explanation.

Address Space Layout Randomization (ASLR) varies placement between executions to make addresses harder to predict. The source's comparison with and without ASLR illustrates a mitigation, not complete security. The printed numbers are results supplied by the material.

### Executable regions, heap, and stack

M016 slide 11's target model proceeds from low executable regions toward runtime storage.

| Region | Role in the material |
|---|---|
| Read-only `.init`, `.text`, `.rodata` | Initialization/instruction code and placed constants or literals |
| Read/write `.data`, `.bss` | Initialized global data and zero-initialized static storage |
| Heap | Runtime allocation; the traditional `brk` boundary is one model |
| Mapped region | Shared libraries, other mappings, and some allocations |
| User stack | Call-related storage; grows toward lower addresses on the illustrated target |
| Kernel virtual-memory region | OS space distinguished from user space |

An uninitialized global is zero-initialized, not filled with arbitrary values. The `.bss` representation avoids storing every zero byte in the executable. Uninitialized automatic locals do not receive the same guarantee. Large allocations can use mapped regions, so not every `malloc` result lies in one `brk` heap. Nor must every local and parameter reside on the stack: the later assembly explicitly uses parameter registers.

At 17:04–18:01, the transcript separates memory protection from physical storage capability. Read-only and read/write regions can both occupy writable DRAM while allowing different process accesses. The OS, assisted by the CPU, can detect a prohibited write. Read-only therefore does not necessarily mean separate physical ROM. Modifying a string literal nevertheless has undefined behavior in C; one OS protection example does not guarantee a particular crash on every implementation.

## Size and alignment are separate constraints

Machines handle integers, addresses, floating data, and vectors; compilers arrange arrays and structures as bytes. The material surveys 1-, 2-, 4-, and 8-byte integers and 4-, 8-, 10-, and 16-byte floating representations. Storage, representation, and ABI rules must remain distinct.

K-byte alignment requires a start address divisible by K. Four-byte-aligned addresses include 0, 4, 8, and 12. Size measures how much space an object occupies; alignment restricts where it can begin.

| Type | Illustrated x86-64 Linux size/alignment | Illustrated IA32 Linux size/alignment |
|---|---:|---:|
| `long` | 8 / 8 | 4 / 4 |
| `double` | 8 / 8 | 8 / 4 |
| `long double` | 16 / 16 | 12 / 4 |
| `void *` | 8 / 8 | 4 / 4 |

These are M016's target observations, not rules for every platform. An eight-byte `double` has alignment four in the IA32 example. The source's Windows-column `long` size of eight is not adopted as a claim about all Windows ABIs. Historical `long double` representation precision also differs from storage size.

Crossing a boundary can require additional memory transactions or page-boundary handling. Permission, cost, and atomicity depend on the architecture. Neither “all unaligned accesses fail” nor “all aligned accesses of every width are atomic” follows. Compilers insert padding to satisfy the target ABI.

### Observing alignment with a dummy byte

M016 slide 28 defines `SIZE(t)` using `sizeof(t)`. Its `INFO(t)` constructs a temporary structure containing `char dummy` followed by `t data`, and uses `#t` to stringify the type name. `OFS` subtracts the structure's start address from `data`'s address. If the resulting offset is eight, padding is `8 - 1 = 7` bytes because one byte belongs to `dummy`.

The second numbers in the table are observed offsets in this arrangement, exposing alignment. The source's `gcc -m32`/`-m64` outputs illustrate target differences; they are not new executions here. Its integer pointer conversions and abbreviated declarations are not certified as a universally portable measurement utility. Separate the definitions rather than inheriting the size/alignment confusion at transcript 50:07.

## Calculating padding and array stride

For given addresses, a gap equals `current address - previous address - previous object size`. In M016 slide 32, an `int` occupies endings `0x40..0x43`, a `char` is at `0x44`, and a `short` starts at `0x46`: the gap is one. A `long long` at `0x48`, characters at `0x50` and `0x51`, and a `float` at `0x54` leave two bytes. A `char` at `0x58` before a `double` at `0x60` leaves seven; that eight-byte double before `long double` at `0x70` leaves eight. This is an observed global layout, not a universal guarantee of global declaration-order placement.

Structure members preserve declaration order without overlapping, subject to internal and tail padding. Calculate the example on [system_programming:M016 slide 37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx):

```c
struct S2 {
    double v;
    int i[2];
    char c;
};
```

| Member | Starting offset | Size |
|---|---:|---:|
| `v` | 0 | 8 |
| `i[0]` | 8 | 4 |
| `i[1]` | 12 | 4 |
| `c` | 16 | 1 |
| Tail padding | 17 | 7 |

The payload occupies seventeen bytes, but the next structure's `double` must also be eight-byte aligned. Consequently `sizeof(struct S2) = 24`; array elements `a[1]` and `a[2]` begin 24 and 48 bytes after the base. In the original figure, notice the 24-byte element spans and the seven-byte region at the expanded element's end. Tail padding maintains the next element's alignment.

Q1(b), [EX:sp_2025_1_midterm_q01 p.2], continuing on [EX:sp_2025_1_midterm_q01 p.3], demands the same distinction between member offsets, complete structure size, and typed-pointer movement. Align each member, round the total size to the structure's alignment, and only then multiply by the array count. This procedure transfers without reproducing the private question's numerical answers.

### A union overlaps storage rather than adding sizes

Unlike a structure's separate member regions, all union members start at offset zero. Their addresses coincide with the union's beginning, and its alignment must meet the strongest member requirement. Summing member sizes is therefore wrong. M016's `max(member size)` is the starting intuition; a general explanation also allows rounding that size to the union alignment. Overlapping bytes do not hold all member values independently at the same time. Detailed type-punning rules are outside this discussion.

## How C value passing appears at machine level

Suppose the caller has `x = 5`, `y = 6`. If `foo(int a, int b)` doubles `a` and returns `a + b`, local `a` becomes 10 and the result is 16, while caller `x` remains 5. If `foo(int *a, int b)` receives `&x` and doubles `*a`, caller `x` becomes 10 and the result is again 16. Both calls copy values; the second copied value is an address.

In M016 slide 44's target assembly, `mov (%rdi), %eax` loads the pointee's 5. Addition produces 10, and `mov %eax, (%rdi)` stores it in caller memory. The function then adds the 6 in `%esi` for the return. It does not replace pointer register RDI with 10.

Passing an array `x = {0,1,…,9}` and executing `a[2] = 5` changes the third element. The key instruction on slide 46 is:

```asm
movl $0x5, 0x8(%rdi)
```

Index two of four-byte integers gives displacement `2 * 4 = 8` bytes. The instruction writes caller storage without copying the array. This is the supplied target convention, not a universal parameter-register rule. The original `int` function's omitted return should not become a model complete API.

For command-line arguments, `argc` is the argument count and `argv` an array of `char *` values. `argv[0]` is the program name in the material's ordinary invocation example, not an unconditional claim about every C execution environment.

The memory-section demand in Q1(c), [EX:sp_2025_1_midterm_q01 p.3] and [EX:sp_2025_1_midterm_q01 p.4], requires separating pointer objects, literals, and local `const` objects. Observing an object in writable storage does not authorize modification of an originally `const` object after a cast. OS protection outcomes and C validity are separate judgments.

## A materials-only review of IA-32 calls and stack frames

[system_programming:NM004](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/EE209.AssemblyFunctions.pptx) supplies optional IA-32 review. Keep it separate from the x86-64 register-parameter examples above. Jumping to a fixed location and returning to one fixed destination cannot accommodate many callers. Keeping only one return address in EAX also fails for `P → Q → R`, because Q's next call overwrites the earlier return address. Calls finish in reverse nesting order, naturally matching a LIFO stack.

In this material, `pushl` reduces ESP by four and stores a value; `popl` reads and then increases ESP by four. `call` implicitly saves the next instruction's address and transfers control; `ret` returns through the saved address. The table's `pushl %eip`/`pop %eip` illustrates effects, not literal instructions for directly manipulating EIP that way.

For `add3(3,4,5)`, the caller pushes 5, 4, and 3 before calling. On callee entry, the first argument is at `ESP+4`. After pushing old EBP and setting `EBP=ESP`, the arguments are at `EBP+8`, `+12`, and `+16`. ESP may move for locals and additional calls, while EBP supplies a fixed reference. A lone local `d` could occupy `EBP-4`; the full trace first saves EBX, ESI, and EDI for twelve bytes, then reserves four bytes for `d`, placing it at `EBP-16`. These offsets follow the push sequence, without claiming a newly inspected full frame diagram.

The source classifies EAX, ECX, and EDX as caller-save, and EBX, ESI, and EDI as callee-save. When an old value is needed afterward, the responsible party saves and restores it. Saving the latter registers can be unnecessary if `add3` never changes them. The callee restores required registers and ESP/EBP before returning; the caller removes twelve bytes of arguments. The result `3+4+5=12` is in EAX and must be preserved where needed before restoring old EAX.

Slides 52–53 label the EBX/ESI/EDI saves “caller-save,” conflicting with slides 40 and 51; these are callee-save registers in the supplied convention. Slides 59–61 also print malformed `addl %12,%esp`; distinguish that from the `$12` immediate on slides 26 and 58. Each active invocation's frame explains nesting, but not every optimized function must use an EBP frame or stack local. Detailed floating-point and aggregate-return ABIs remain outside this review.

## Key Takeaways

- Equal virtual addresses can name independent private objects in different processes.
- Read-only is an access policy, not necessarily ROM or a guaranteed C crash.
- Size is occupied space; alignment constrains starts, and tail padding aligns the next array element.
- C passes addresses by value, so copying a pointer can still allow writes to caller storage.
- Keep IA-32 stack arguments separate from x86-64 register arguments and trace each push or store.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Same address, different state

Two processes print the same address for `global_int`, yet each advances independently, while `shared_int` jointly advances through 0..7. What determines sharing? What does ASLR change, and what does it not guarantee?

<details><summary>Show solution</summary>

Addresses are interpreted within a process's address space. Private globals can occupy different storage despite equal numbers; shared mappings can designate one object. The independent versus combined sequences demonstrate this distinction. ASLR varies placement to hinder prediction, not to guarantee complete security. Detailed semaphore teaching was deferred on September 23 and must be distinguished from later mapping explanations.

**Checking points:** Separate address values from mappings and retain the observation and ASLR limits.

</details>

#### Recall Q02 · Regions, initialization, and access

Classify `.text/.rodata/.data/.bss`, heap, mappings, and stack. Compare an uninitialized global with an automatic local. Distinguish read-only protection over writable DRAM from the C rules for modifying literals or originally const objects.

<details><summary>Show solution</summary>

Text holds instructions; rodata contains placed constants/literals; data holds initialized globals; bss represents zero-initialized static storage. Heap supports runtime allocation, mappings include libraries/shared storage/some allocations, and the target stack supports calls. Uninitialized globals are zero-initialized; automatic locals lack that guarantee. Not every allocation is in a brk heap or every parameter on the stack. OS/CPU protection can deny process writes to writable DRAM. Modifying literals or originally const objects is a separate C-validity issue: a writable location or absence of a crash does not authorize it.

**Checking points:** Check four sections, runtime regions, global/local initialization, and protection versus C validity.

</details>

#### Recall Q03 · Size and alignment

Define K-byte alignment and give four-byte-aligned addresses. Compare long, double, long double, and pointer size/alignment in the supplied x86-64/IA32 Linux models. Why avoid universal unaligned/atomicity claims?

<details><summary>Show solution</summary>

Address mod K must be zero; examples are 0, 4, 8, 12. The x86-64 pairs are 8/8, 8/8, 16/16, 8/8; IA32 pairs are 4/4, 8/4, 12/4, 4/4. Eight-byte size therefore need not mean eight-byte alignment. Boundary crossing can require extra transactions or page handling; legality, cost, and atomicity depend on architecture and width. Neither universal failure nor universal aligned atomicity follows.

**Checking points:** Check all four pairs in both models and the size/alignment counterexample.

</details>

#### Recall Q04 · The dummy-byte offset

When `INFO(t)` places `t data` after `char dummy`, what do SIZE, OFS, and `#t` do? What is padding for offsets 8 and 4? Does this macro give a portable measurement on every C implementation?

<details><summary>Show solution</summary>

SIZE uses sizeof, OFS subtracts the structure start from the data address, and `#t` stringifies the type name. The offset includes the one-byte dummy, leaving padding 7 or 3. This observed offset exposes alignment separately from size. Integer pointer conversions and abbreviated declarations have portability limits; the supplied `-m32`/`-m64` observations apply to those targets.

**Checking points:** Distinguish offset from padding by one byte and explain all three roles.

</details>

#### Recall Q05 · Calculating observed gaps

Compute gaps from observed addresses: char 0x44→short 0x46, char 0x51→float 0x54, char 0x58→double 0x60, and eight-byte double 0x60→long double 0x70. Why is this not a universal global ordering rule?

<details><summary>Show solution</summary>

Use next start minus previous start minus previous size: 2−1=1, 3−1=2, 8−1=7, and 16−8=8 bytes. This interprets supplied observations; it does not guarantee declaration-order placement of every global by every compiler.

**Checking points:** Give 1/2/7/8 together with the formula.

</details>

#### Recall Q06 · Structure tail padding and stride

Using double 8/8, int 4/4, and char 1/1, calculate member offsets, payload, tail padding, sizeof, and a[1]/a[2] offsets for `struct S2 {double v; int i[2]; char c;};`.

<details><summary>Show solution</summary>

Offsets are 0, 8, 12, 16. Round seventeen payload bytes to the next multiple of eight, giving size 24 and seven tail bytes. Stride is 24, so a[1]=base+24 and a[2]=base+48. Without tail padding the next double would begin at 17, violating alignment; member sizes alone do not determine sizeof.

**Checking points:** Check all four offsets, 17+7=24, and strides 24/48.

</details>

#### Recall Q07 · Overlapping union storage

Compare a union and structure with int 4/4 and double 8/8. Explain union member addresses, size/alignment, and whether both values are independently retained.

<details><summary>Show solution</summary>

All union members overlap at offset zero and require alignment eight. The maximum member size eight already meets that alignment, giving size eight here. Do not add sizes as for separate structure storage. Writes affect overlapping bytes, so independent values are not simultaneously retained. In general the maximum size may need rounding; detailed type-punning rules are outside this question.

**Checking points:** Explain offset zero, size/alignment eight, and overlapping rather than independent storage.

</details>

#### Recall Q08 · Value passing and caller-memory stores

With x=5, y=6, compare doubling value parameter a with doubling pointer target *a before returning a sum. Explain the load/store through RDI, the array target of `movl $0x5,0x8(%rdi)`, and argc/argv.

<details><summary>Show solution</summary>

Both return 16, but x remains 5 in the value case and becomes 10 in the pointer case. Both pass values; the latter copies an address. Loading through RDI obtains 5, computation produces 10, and the store writes that address without replacing RDI itself. With an array base in RDI and four-byte ints, displacement eight selects index two, setting x[2]=5. argc counts arguments and argv is an array of char pointers; argv[0] denotes the program name in the ordinary source invocation.

**Checking points:** Check caller values, common return 16, memory versus register, and the 2×4 offset.

</details>

#### Recall Q09 · Nested calls and return addresses

Why does keeping only one return address in EAX fail for P→Q→R? Explain the supplied pushl/popl/call/ret effects and the status of `pushl %eip`.

<details><summary>Show solution</summary>

Q's call to R overwrites the earlier return address. Returns follow reverse nesting, so each address belongs on a LIFO stack. In this IA-32 model pushl lowers ESP by four then stores, while popl reads then raises it by four. Call implicitly saves the next-instruction address and transfers control; ret returns through the saved address. `pushl %eip`/`pop %eip` are effect pseudocode, not literal executable instructions.

**Checking points:** Check overwriting, LIFO, all four effects, and the pseudocode qualification.

</details>

#### Recall Q10 · Frame offsets and register responsibility

For IA-32 add3(3, 4, 5), calculate push order, argument positions on entry/after the EBP prolog, and d's position alone versus after EBX/ESI/EDI saves. Explain save responsibilities, restoration, argument cleanup, and preserving EAX's return value.

<details><summary>Show solution</summary>

Push 5, 4, 3. The first argument is ESP+4 on entry; after saving old EBP and fixing EBP, arguments are at +8/+12/+16. d alone is EBP−4; after twelve saved-register bytes it is EBP−16. EAX/ECX/EDX are caller-save; EBX/ESI/EDI are callee-save. The responsible party preserves needed old values. The callee restores required registers and ESP/EBP and returns; the caller removes twelve argument bytes. Preserve result 12 from EAX before restoring old EAX. The source's caller-save label and `%12` immediate conflict with its other slides and `$12` notation.

**Checking points:** Check every offset, twelve-byte cleanup, return-value overwrite risk, and both source errors.

</details>

### Apply and check

#### Practice P01 · Changing layout to save space

**Newly written synthetic practice.** Use Q1(b)'s alignment→sizeof→array-stride reasoning [EX:sp_2025_1_midterm_q01 p.2]. Prerequisites are the chapter's structure/union rules with int 4/4, double 8/8, char 1/1; no private numerical answer is reused.

Find offsets, sizeof, and the size of two elements of `struct R {char c; double d; int n;};`. What is saved by reordering to `double d; int n; char c;`? Can a union with those three members retain three independent values?

<details><summary>Show solution</summary>

Original offsets are 0, 8, 16; the last member ends at 20, followed by four tail bytes, giving size 24 and two-element size 48. Reordering gives offsets 0, 8, 12; round endpoint 13 to 16. Two elements occupy 32, saving sixteen bytes. The union has offsets zero and size/alignment eight, but overlapping bytes cannot retain all three independent values. Replacing a structure by a union changes semantics, not just space.

**Checking points:** Explain internal/tail padding in both layouts, array totals, and the union's semantic difference.

</details>

### Review plan

Solve Q03–Q07 in offset/size/alignment columns and rebuild P01's layouts unaided. For Q08 separate caller values from registers/addresses; for Q09–Q10 record ESP and return addresses after each push.

## Sources

[[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 · lecture note]]

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slides 7, 11, 23–24, 27–28, 32, 34, 36–39, 43–46

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · corrected transcript]] — 09:18–12:08 (private globals versus the shared counter), 13:08 (announcement of a later return to the source code), 17:04–18:01 (physical DRAM versus permissions), 21:47 (target stack direction)

[EE209 AssemblyFunctions.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/EE209.AssemblyFunctions.pptx) — slides 10, 26, 29, 40, 51–53, 58–61

Size/alignment figures are target examples; the Windows long column and uncertain size/alignment speech are not universal rules. September 23 shared-state output is a source observation, with detailed synchronization belonging to later teaching. The AssemblyFunctions deck supplies optional IA-32 materials review, separate from x86-64; the worked offsets follow the stated instruction sequence, not unclear graphical details. Its EBX/ESI/EDI caller-save label and malformed `addl %12,%esp` remain explicit discrepancies. Historical crash lists do not determine C validity for const or literal modification.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.

[[exam_questions/sp_2025_1_midterm_q01|2025-1 Midterm Q1 · C pointers (existing preview)]]
