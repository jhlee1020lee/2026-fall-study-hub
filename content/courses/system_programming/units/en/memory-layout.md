---
title: "Process Memory, Alignment, and Parameter Passing"
description: "Review memory sections, padding, stride and parameter passing in bytes."
course: "system_programming"
unit_id: "memory-layout"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Connect C types and lifetimes to process layout, protection and calls. Make alignment and address calculations explicit to check diagrams in bytes.

## Virtual addresses and process-specific memory

In [[courses/system_programming/units/en/objects-pointers|Objects and Pointers]], an address identified where an object could be accessed. That account now needs a scope: a virtual address is interpreted within a process's address space. Two processes can print the same numerical address without reading or writing the same storage there.

The `layout.c` examples in [Variable and Memory Recap, slides 5–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) print addresses of functions, globals, locals, heap objects, and shared objects alongside process IDs. Corresponding addresses repeat in the illustrated runs without Address Space Layout Randomization (ASLR), while some layout addresses change between the runs with it enabled. ASLR makes useful addresses harder for an attacker to predict. A difference between printed addresses does not establish that a program has no vulnerabilities or that every attack is prevented.

The more revealing comparison concerns **changes in values**. In the source example, processes with PIDs 16074 and 16075 increment their own `global_int`. Even where its numerical virtual address is identical, each process follows its own sequence 0, 1, …. The explicitly shared `shared_int` instead produces a sequence continuing from 0 through 7 across the two processes. Private versus shared state depends on the mapping and the storage accessed, rather than the appearance of a printed address.

Shared memory and a semaphore are components of this demonstration. Its current teaching value is the distinction visible in the output. The [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 13:08]] postpones the full `layout.c` source discussion, and 42:29–43:27 postpones page-table translation. Neither an unseen synchronization implementation nor a completed address-translation algorithm is needed to understand this observation.

## Memory sections and access permissions

### From executable bytes to runtime storage

The process-memory diagram in [slide 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) separates regions by role as addresses increase. Above a low unused region are executable-backed read-only and read/write segments, the runtime heap, mapped regions such as shared libraries, the user stack, and a kernel virtual-memory region. The useful questions are **what bytes a region holds, when its storage is established, and which accesses are permitted**. Memorizing absolute addresses is not the purpose.

| Region | Role in the source explanation | Important distinction |
| --- | --- | --- |
| `.text` | Machine instructions to execute | A function name is not thereby a separate data object. |
| `.rodata` | Constant data and string literals placed in this region | Not every `const` object must occupy this section in every implementation. |
| `.data` | Writable static storage such as initialized global data | Having an initial value and being writable during execution are different properties. |
| `.bss` | Zero-initialized static storage | A global without an explicit initializer does not start with an arbitrary garbage value. |
| Heap | Runtime storage requested through operations such as `malloc` | An allocation need not come from one continuous `brk` region. |
| Mapped regions | Mappings including shared libraries | A mapping does not by itself imply that all its bytes are shared with another process. |
| Stack | A principal region for call-related storage | A local or parameter need not occupy a memory-resident stack slot. |

The `.bss` representation lets the loader establish zero-initialized storage without storing every zero byte in the executable. An uninitialized automatic local does not receive that same guarantee. The language distinctions in [[courses/system_programming/units/en/objects-pointers|Storage Duration and Initialization]] remain necessary when interpreting physical layouts.

In the diagram, `brk` labels a traditional heap boundary and the heap expands upward. Large allocations may use separate mappings. The illustrated user stack grows in the opposite direction, from higher to lower addresses; the [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 21:47]] also describes this direction for the Intel target. This is an explanatory x86-64 Linux layout, not a fixed map for every platform.

### Writable DRAM can back a read-only mapping

A read-only region need not reside in special RAM that is physically incapable of being written. The [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 17:04–18:01]] explains that read-only and read/write regions can both use ordinary writable DRAM. The storage device's ability to change bytes is separate from **whether this process is allowed to perform that write**.

The OS enforces permissions with CPU assistance. It can detect a prohibited write and terminate the process. Being backed by RAM therefore does not authorize a program to modify an instruction or a string literal.

There is a further distinction between language rules and an observed protection mechanism. Modifying a string literal is undefined behavior in C. A particular environment's read-only protection may detect the attempted write, but this does not promise an identical crash in every C implementation. Language permission and a particular OS's response should not be merged into one universal rule.

## How size and alignment determine placement

### Equal sizes need not imply equal alignment

At the machine level, the source discusses 1-, 2-, 4-, and 8-byte integers and addresses, floating-point data of several sizes, and vector data. A C array or structure is not itself a special machine-level aggregate operation. The compiler represents it as contiguous bytes and offset calculations. The Application Binary Interface (ABI) supplies part of the contract governing this representation.

Size is the number of bytes an object occupies. Alignment constrains its starting address. K-byte alignment means the address is divisible by K: addresses 0, 4, 8, 12, … satisfy 4-byte alignment, while 1, 2, and 3 do not. **An 8-byte size does not imply 8-byte alignment on every ABI.**

The Linux examples in [slides 23–29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) give the following values. Each entry is size/alignment, in bytes.

| C type | x86-64 Linux | IA32 Linux |
| --- | ---: | ---: |
| `char` | 1/1 | 1/1 |
| `short` | 2/2 | 2/2 |
| `int` | 4/4 | 4/4 |
| `long` | 8/8 | 4/4 |
| `long long` | 8/8 | 8/4 |
| `float` | 4/4 | 4/4 |
| `double` | 8/8 | 8/4 |
| `long double` | 16/16 | 12/4 |
| `void *` | 8/8 | 4/4 |

The `long double` entries describe storage and alignment. The historical extended format discussed in the source involves a 10-byte, or 80-bit, representation; 16 bytes of storage do not automatically mean binary128 precision. Crossed-out types and historical qualifications on the slide do not remove alignment as a topic. Calculations here follow the source's Linux targets rather than generalizing the table, including its Windows `long` entry, to every platform.

Unaligned accesses matter for reasons beyond stylistic consistency. A datum spanning a memory-access boundary or a page boundary can require extra transactions or handling. Architectures differ in what they permit and in the performance and atomicity conditions involved. Neither “every unaligned access fails” nor “every aligned access is atomic at any width” follows from these examples.

### Observing offsets with a dummy member

The `INFO(t)` macro in [slide 28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) constructs a temporary structure to expose placement. Its `INFO(double)` expansion contains this structure:

```c
struct {
    char dummy;
    double data;
} s;
```

In the original macro, `SIZE(t)` expands to `sizeof(t)`, and `#t` turns the type tokens into a string used as an output label. `OFS(s)` subtracts the address of `s` from that of `s.data` to obtain the member offset. The slide converts those pointers to `unsigned long` before subtraction. This is a teaching observation for the shown target, not an endorsement of that conversion or the original `main` declaration as a complete portable measurement tool.

The `dummy` occupies one byte. If `data` starts at offset 8 in the x86-64 example, those eight bytes contain **one dummy byte and seven padding bytes**. Calling all eight bytes padding counts the dummy twice. For the illustrated IA32 `double`, the size is 8 but its offset is 4, leaving three padding bytes after the dummy.

The source's `gcc -m32` and `gcc -m64` outputs illustrate the table above; they are not measurements newly performed on a reader's machine. Where the [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 50:07]] has unclear size/alignment wording, the address difference and the type's size keep these quantities distinct.

## Padding and the size of composite objects

### Calculating gaps between global addresses

[Slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) prints global addresses and calculates the gaps after preceding objects. The following addresses show the last two digits after a common prefix `0x56183b8ac0`. They are **hexadecimal**: `40` means the full address `0x56183b8ac040`.

| Object | Last two address digits | Size | Gap after preceding object |
| --- | --- | ---: | ---: |
| `int i` | `40` | 4 | First item |
| `char c` | `44` | 1 | 0 |
| `short s` | `46` | 2 | 1 |
| `long long ll` | `48` | 8 | 0 |
| `char c2` | `50` | 1 | 0 |
| `char c3` | `51` | 1 | 0 |
| `float f` | `54` | 4 | 2 |
| `char c4` | `58` | 1 | 0 |
| `double d` | `60` | 8 | 7 |
| `long double ld` | `70` | 16 | 8 |
| `long l` | `80` | 8 | 0 |

The calculation is `current address − previous address − previous size`. Since `char c` occupies the byte at `0x44` and `short s` starts at `0x46`, the byte at `0x45` is a gap. Between `char c3` and `float f`, the gap is `0x54 - 0x51 - 1 = 2`. Between `char c4` and `double d` it is `0x60 - 0x58 - 1 = 7`; between that `double` and `long double` it is `0x70 - 0x60 - 8 = 8`. Subtracting hexadecimal suffixes as though they were decimal gives incorrect results.

This is an observed global layout, not a guarantee that every compiler places globals in declaration order. Structure layout, in contrast, uses ordered members and the applicable target ABI's alignment rules.

### Why a structure needs padding at its end

Consider the example in [slides 35–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx):

```c
struct S2 {
    double v;
    int i[2];
    char c;
} a[10];
```

On the illustrated x86-64 Linux target, `v` occupies eight bytes starting at offset 0, `i[0]` occupies four at offset 8, `i[1]` occupies four at offset 12, and `c` occupies one at offset 16. Member payload therefore totals 17 bytes.

However, the `double v` in **every** array element must satisfy 8-byte alignment. Placing the next element 17 bytes after an aligned first element would break that condition. Seven bytes of tail padding increase `sizeof(struct S2)` to 24. In the figure, look for the seven-byte space after `c` and the repeating element starts at byte offsets 0, 24, 48, 72, …. Labels such as `a+24` in that diagram describe **byte offsets**; they must not be read as the C typed-pointer expression `a + 24`.

An array's stride, the distance between adjacent element starts, is its element's `sizeof`. Thus `&a[1]` is 24 bytes beyond the beginning, `&a[2]` is 48 bytes beyond it, and the complete `a` occupies 240 bytes. In general, place each member at a suitable alignment and round the final size up to a multiple of the strongest member alignment so the next element can also be aligned.

The structure-layout reasoning requested by Q1(b) in [EX:sp_2025_1_midterm_q01 p.2] follows this same separation: fix the target sizes and alignments, then calculate member offsets, tail padding, and typed strides. The `S2` calculation above is the lecture example, not a reproduction of the private exam's structure or supplied answer.

### A union places members at one shared starting point

A structure lays its members out in order without overlap. A union starts every member at offset 0, overlapping their storage. In [slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx), the horizontal regions representing the members share the same starting line; they are not concatenated side by side.

A union must satisfy the strongest alignment required by any member. Its size starts from the largest member size, with any tail padding needed to satisfy the union's alignment. Adding all member sizes, as if they occupied independent locations, is wrong. For example, applying the source's rule to a simple union containing an `int` and a `double` on this target gives eight bytes of storage with 8-byte alignment, rather than 4+8 bytes. This is an explanatory application of the rule.

Shared bytes also do not preserve multiple independent member values simultaneously. Writing one member changes the bytes overlapped by the others. The topic here is this storage relationship; the detailed rules for type-punning through a different member are a separate subject.

## Argument copies and changes to caller memory

### Copying a scalar value versus copying an address

Distinguishing the caller from the callee removes ambiguity from “the function changes its argument.” The first function in [slides 41–44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) receives scalar values:

```c
int foo(int a, int b)
{
    a = 2 * a;
    return a + b;
}
```

If the caller has `x = 5` and `y = 6` and invokes `foo(x, y)`, the callee's `a` receives a copy of 5, becomes 10, and contributes to the return value 16. The caller's `x` remains 5. Treating `a` and `x` as the same storage would make this result inexplicable.

The source's separate pointer-taking function is:

```c
int foo2(int *a, int b)
{
    *a = 2 * *a;
    return *a + b;
}
```

With `foo2(&x, y)`, `a` receives a copy of the address of `x`. Doubling `*a` updates the object at that address, so the caller's `x` becomes 10 and the return value is again 16. C copies values in both calls. In the second call, the copied value is an address through which caller storage can be accessed. The slides' “pass by reference” describes this effect; it does not introduce a separate C reference-parameter mechanism.

### Registers and memory operands expose the difference

The x86-64 assembly on slide 44 makes the relationship concrete. These are the source instructions with spacing normalized:

```asm
mov (%rdi),%eax
add %eax,%eax
mov %eax,(%rdi)
add %esi,%eax
ret
```

For this call, `%rdi` holds the address of `x` and `%esi` holds the second argument, 6. The first instruction reads 5 from the memory addressed by `(%rdi)` into `%eax`. The next produces 10; the third stores 10 back into the caller's memory. Adding 6 then forms the return value 16.

The pointer register `%rdi` itself does not become 10. The difference between a bare register and the memory operand `(%rdi)` mirrors the difference between holding an address and accessing the contents at that address. This register-passing example also explains why parameters should not invariably be pictured as stack slots.

### Array elements and command-line strings

In [slides 45–46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx), a function receiving the elements of `int x[10] = {0,1,2,3,4,5,6,7,8,9};` performs `a[2] = 5;`. It receives a pointer rather than a separately copied array, so the caller's `x[2]` changes from 2 to 5. Since `int` occupies four bytes on this target, the byte offset is `2 * 4 = 8`.

```asm
movl $0x5,0x8(%rdi)
ret
```

The operand `0x8(%rdi)` directs the store eight bytes beyond the base address. The slide's C fragment has an `int` return type without a return statement; the useful point here is its store and address calculation, rather than treating it as a complete model function.

The declaration `main(int argc, char *argv[])` in [slide 47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) uses the same relationships. `argc` counts arguments, while `argv` provides access to an array of `char *` values pointing to strings. In the source's normal command-line invocation, `argv[0]` is the program name and subsequent entries are user-supplied arguments. Each `argv[i]` points to a string's beginning rather than containing a value-copy of the complete character array.

The loop `for (i = 0; i < argc; i++)` visits valid argument indices in order. The normal example's `argc >= 1` should not become an unconditional claim about every possible C environment. Keeping pointer values and pointed-to storage separate also helps when considering [[courses/system_programming/units/en/dirtree|Dirtree options and roots]]: option strings, owned copies of entry names, and storage consumed by recursive calls have distinct roles.

## Key Takeaways

- Equal virtual addresses alone do not establish sharing.
- Size, alignment and precision are distinct.
- Tail padding preserves alignment of the next array element.
- Revisit [[courses/system_programming/units/en/objects-pointers|objects and pointers]] when pointer foundations are unclear.

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Virtual addresses and sharing

Does the same virtual address in two processes identify the same object? Explain independent/shared counters, ASLR and deferred scope.

<details><summary>Show solution</summary>

Processes have distinct address spaces, so equal numbers alone do not establish sharing. Independent globals can each progress0, 1; the shared example jointly progresses0..7. ASLR varies placement to hinder prediction, not to provide complete security. September23 passages13:08 and 42:29–43:27 distinguish this recap from later discussion; page-table/TLB calculations are deferred.

**Check:** Separate equal numbers from shared objects, both counters and ASLR limits.

</details>

#### Recall Q02 · Sections and protection

Classify text, rodata, data, bss, heap and stack. Explain read-only storage on writable DRAM, bss versus automatic variables, malloc/brk and literal modification.

<details><summary>Show solution</summary>

Text holds instructions, rodata literals/read-only data, data initialized writable static storage, and bss zero-initialized static storage. Bss need not occupy literal zero bytes in the executable; uninitialized automatic objects are not implicitly zeroed. Dynamic allocation may use brk or mappings. The target stack grows downward, but parameters may reside in registers. Physically writable DRAM differs from logical protection enforced by CPU/OS. Modifying literals/const objects is not legalized by absence of a crash. Page-translation implementation is outside this recap.

**Check:** Check all six regions, static/automatic initialization and physical/logical protection.

</details>

#### Recall Q03 · Size and alignment tables

Distinguish size from K-byte alignment and compare x86-64/IA32 Linux type sizes/alignments. Explain long-double and unaligned-access cautions.

<details><summary>Show solution</summary>

Alignment K constrains the starting address to a multiple of K.

|Type|x86-64 size/align|IA32 size/align|
|---|---|---|
|char|1/1|1/1|
|short|2/2|2/2|
|int, float|4/4|4/4|
|long, pointer|8/8|4/4|
|long long, double|8/8|8/4|
|long double|16/16|12/4|

Sixteen-byte long-double storage is not128-bit precision; distinguish the source’s80-bit extended representation. Unaligned access may need extra boundary handling, without proving universal failure or atomicity.

**Check:** Check both quantities, IA32 exceptions and precision limits.

</details>

#### Recall Q04 · A macro for observing alignment

For INFO(double), a struct places double data after char dummy. Explain SIZE, #t, OFS and calculate offsets/padding on both targets.

<details><summary>Show solution</summary>

SIZE is sizeof(type); #t stringifies the macro argument; OFS subtracts struct start from data’s address. On x86-64, data starts at 8 after a one-byte dummy, giving 7 padding bytes. IA32 Linux uses offset 4, padding3 while double remains8 bytes. Do not confuse offset and size. The source’s unsigned-long address casts and main spelling limit portability; these are not newly executed measurements.

**Check:** Check8/7, 4/3, double8 and stringification.

</details>

#### Recall Q05 · Padding and array stride

Calculate gaps between hexadecimal address tails44(char1)→46, 51(char1)→54, 58(char1)→60 and 60(double8)→70. Then lay out S2={double v; int i[2]; char c; } and a ten-element array of S2.

<details><summary>Show solution</summary>

Gap=current address−previous address−previous size gives 1, 2, 7, 8 bytes. This global order is not a general C guarantee. S2 has v at 0, i[0]8, i[1]12, c16:17 used bytes plus7 tail padding gives size 24, alignment 8. Ten elements occupy 240 bytes; indices 1/2 begin at byte 24/48. Tail padding aligns the next element too. Diagram a+24 denotes a byte location, not typed-pointer addition by 24.

**Check:** Check all four gaps, member offsets, tail 7 and stride24.

</details>

#### Recall Q06 · Union overlap

Compare union and struct layout for int/double. Explain union size/alignment and whether members retain independent simultaneous values.

<details><summary>Show solution</summary>

Struct members occupy ordered nonoverlapping storage plus padding. Union members overlap at offset 0; storage accommodates the largest member rounded to the maximum alignment. This target’s int/double union has size 8, alignment 8, not4+8=12. It does not preserve two independent simultaneous values or authorize arbitrary type-punning.

**Check:** Check offset 0, maximum/rounding and lack of independent simultaneous values.

</details>

#### Recall Q07 · Value copies and indirect mutation

With x=5, y=6 compare scalar foo and pointer foo2. Trace load/add/store assembly, a[2]=5’s byte offset and argc/argv parameter types.

<details><summary>Show solution</summary>

Scalar foo doubles local a to 10 and returns 16, leaving caller x=5. `foo2` copies &x, stores10 through it and returns 16: both use C value passing. Assembly loads5 from(%rdi), doubles eax to 10, stores through(%rdi), adds esi’s6 and returns 16; rdi does not become10. For four-byte ints, a[2] is byte 8, so `movl $0x5,0x8(%rdi)` changes the caller’s element. Do not invent a return value for the source int function’s omitted return. Argc counts arguments; parameter `char *argv[]` adjusts to char**, with string-pointer elements. Normally argv[0] names the program and i<argc bounds iteration; argc>=1 is not guaranteed across all C environments.

**Check:** Check x5/x10, return 16, unchanged address in rdi, offset 8 and argv adjustment.

</details>

### Practice

#### Practice P01 · Member order and total size

**Newly written synthetic practice.** On x86-64 Linux, lay out struct A {char tag; double value; char ready; } and struct B {double value; char tag; char ready; }. Find offsets, sizes and two-element array sizes. Can a union of the chars preserve both flags independently?

[EX:sp_2025_1_midterm_q01 p.2] Q1(b) contributes alignment/stride reasoning, transferred to comparing layouts and a storage-design decision. Prerequisites: Q03/Q05/Q06. The private structure, address-difference expressions and crash question are not reproduced. [[exam_questions/sp_2025_1_midterm_q01|Authorized related question preview]]

<details><summary>Show solution</summary>

A uses offsets 0, 8, 16: round17 occupied bytes to 24. B uses 0, 8, 9: round10 to 16. Two-element arrays occupy 48/32 bytes. Reordering changes internal/tail padding while alignment stays8. A char union overlaps at 0 and cannot replace two independent flags.

**Check:** Check offsets, tail rounding, 48/32 and the union-design limitation.

</details>

### Review plan

Sketch address spaces/regions for Q01–Q02, then keep size/alignment/offset in separate columns for Q03–Q06. Solve P01 unseen and identify the actually changed objects in Q07.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 lecture notes]]

### Materials and lecture passages

- [Variable and Memory Recap, slides 5–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slide 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slides 23–29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slide 28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slides 35–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slides 41–44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slides 45–46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [slide 47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 13:08]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 21:47]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 17:04–18:01]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 50:07]]

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

### Scope to retain

- This is the September23 memory recap, not evidence of completed page-table, TLB or translation calculations.
- Addresses, global ordering, assembly and ABI values are target examples, not measurements run on this PC.
- Preserve source limits including omitted returns and unsigned-long address-cast portability.
- Supplied exam crash answers do not define C validity. Only bounded Q1(b) alignment reasoning is used.


---

[[courses/system_programming/units/en/io-streams|← Previous: Unix I/O, Open-File State, and Standard I/O Buffering]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/dirtree|Next: Dirtree Traversal, Filtering, Output Contracts, and Design →]]
