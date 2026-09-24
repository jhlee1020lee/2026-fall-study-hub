---
title: "Program Translation, Linking, and Loading"
description: "Trace separate compilation, linking, loading, and the state changes of three instructions."
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
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-03-lecture-02"]
---

Follow how separately translated files become an executable program. Distinguish connecting symbols, adjusting address references, and preparing a memory image to explain why machine code alone may not be ready to run.

## Separate compilation and symbols across files

Splitting a program into files lets each file be translated independently. If one file uses a function or variable defined elsewhere, a later step must connect that reference to the correct definition. While the [ISA and architectural state](architecture-contract.md) define execution, translation, linking, and loading prepare the program to execute. The following example assumes basic familiarity with C functions, arrays, and pointers and reviews the September 3 materials, for which no recording is supplied.

In [[page_cache/computer_architecture/lec.02/page-019|CA M008 p.19]], `main.c` defines `int buf[2] = {1, 2};` and calls `swap` from `main`. The other file, `swap.c`, contains:

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

`extern int buf[];` declares an array whose definition is supplied elsewhere. `bufp0` points to the first element, and the function makes `bufp1` point to the second. It saves 1 in `temp`, writes 2 into the first element, and writes the saved 1 into the second, producing `{2, 1}`. Without preserving the first value before overwriting it, the final assignment would lose its required input.

A symbol identifies a function or object during linking. The arrows in [[page_cache/computer_architecture/lec.02/page-020|CA M008 p.20]] distinguish:

| Name or use | Role from the linker's perspective |
|---|---|
| Definitions of `main` and `buf` in `main.c` | Global symbols accessible from other files |
| Definitions of `swap` and `bufp0` in `swap.c` | Global symbols |
| Use of `swap` in `main.c` and `buf` in `swap.c` | External references requiring definitions elsewhere |
| File-scope `static bufp1` | A local symbol confined to this file |
| `temp` inside the function | An automatic local variable used during execution |

Both `bufp1` and `temp` may informally sound “local,” but in different senses. The file-scope `static` restricts linkage, and its storage differs from an automatic variable associated with a function invocation. `temp` holds a value needed during one execution of `swap`. The diagram's “Linker knows nothing of temp” means that this variable is not resolved between files; it does not mean the value is unnecessary at runtime.

## Translation and relocatable object files

Assembly code is a human-readable notation for instructions; an assembler translates it into binary machine code. A compiler translates higher-level operations into instructions. A pseudo-instruction can expand into several machine instructions, so counting assembly-source lines does not necessarily count executed instructions. [[page_cache/computer_architecture/lec.02/page-028|CA M008 p.28]]

In [[page_cache/computer_architecture/lec.02/page-021|CA M008 p.21]], `main.c` and `swap.c` each pass through translators labeled `cpp`, `cc1`, and `as` to produce `main.o` and `swap.o`. Preprocessing, compilation, and assembly produce separate outputs; a compiler driver can invoke these stages together.

These `.o` files are relocatable object files. They may contain machine code while still having unresolved cross-file symbols or unfinished address placement. For example, `main.o` contains a call to `swap`, but the location of `swap`'s code is established when the files are linked. Producing machine code and producing a complete executable are therefore distinct accomplishments.

## Symbol resolution and relocation

The linker connects definitions and references across object files and establishes the final code/data layout. Symbol resolution answers “Which definition does this name identify?” Relocation answers “How must this address reference change to match the final placement?”

![Original diagram of object-file code and data merging into executable sections](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.02/page-022.png)

In [[page_cache/computer_architecture/lec.02/page-022|CA M008 p.22]], the smaller `main.o` and `swap.o` boxes on the left feed the executable on the right. Code for `main` and `swap` appears in `.text`, initialized `buf` and `bufp0` in `.data`, and file-scope `bufp1` in `.bss`. The automatic `temp` does not belong in this list of global/static data.

`bufp0` contains the address of `buf[0]`, so that reference must agree with the final placement of `buf`. A call target must likewise agree with its final code location. Headers, `.symtab`, and `.debug` appear separately in the diagram, demonstrating that not every byte in an executable file is an instruction or ordinary program data. This is an introductory static-linking model, not an enumeration of all relocation types or dynamic-linker mechanisms.

## ELF loading and the runtime memory layout

Loading prepares the memory image needed to run an executable. The ELF diagram in [[page_cache/computer_architecture/lec.02/page-023|CA M008 p.23]] distinguishes the file layout on the left from runtime memory on the right. It groups `.init`, `.text`, and `.rodata` into a read-only segment and `.data` and `.bss` into a read/write segment. Above them are a runtime heap, a shared-library mapping region, a user stack, and a kernel region.

The key distinction is that **the file's section list is not the entire runtime memory layout**. All symbol/debug information should not be treated as ordinary program data, and the heap and stack serve their own runtime purposes. The addresses shown belong to an example 32-bit address space; they are not fixed loading addresses for every OS or RV64 program.

## How loaded instructions change state

After the loader prepares the program, the ISA determines each instruction's effect. [[page_cache/computer_architecture/lec.02/page-024|CA M008 p.24]] starts with `PC=0x1000`, `GPR[x10]=0x2000`, and `MEM[0x2000]=41`. Here `GPR[x10]` denotes the register's value and `MEM[a]` the memory value at address `a`.

```asm
lw   x5, 0(x10)
addi x5, x5, 1
sw   x5, 0(x10)
```

| Address of executed instruction | Operation | `x5` afterward | Memory value | Next PC |
|---|---|---|---|---|
| `0x1000` | `lw` reads address `0x2000` | 41 | 41 | `0x1004` |
| `0x1004` | `addi` adds 1 | 42 | 41 | `0x1008` |
| `0x1008` | `sw` writes the result to that address | 42 | 42 | `0x100C` |

In the middle row, the register has become 42 while memory remains 41. Register arithmetic does not itself perform a memory store. This example uses basic 32-bit instructions, so the PC advances by 4 bytes each time. The width of a data register and the length of an instruction are separate properties. [Data representation, registers, and memory](data-register-memory.md) develops that distinction further.

## Key Takeaways

- File-local linkage from `static` differs from an automatic variable's local scope.
- Object files may contain machine code while external symbols and final placement remain unresolved.
- Symbol resolution connects definitions; relocation adjusts address references to final placement.
- ELF file sections and runtime heap/stack are different views.
- A register computation changes memory only through a subsequent store.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Symbol categories and preserving values

Explain the order that swaps `{1,2}` in the teaching example. Classify `buf`, `swap`, `bufp0`, file-scope `static bufp1`, and function-local `temp` for linking, and explain why `temp` is needed without cross-file resolution.

<details><summary>Show solution</summary>

Save the first value, 1, in `temp`; write 2 into the first element; then write the saved 1 into the second, producing `{2,1}`. Definitions of `buf`, `swap`, and `bufp0` are global symbols; cross-file uses of `buf`/`swap` are external references. `bufp1` has file-local linkage and static storage, whereas `temp` is an automatic variable for an invocation. Its runtime preservation role exists even though the linker does not resolve it across files.

**Checking points:** Show the three assignment stages and distinguish global, external, file-local, and automatic roles.

</details>

#### Recall Q02 · Machine code versus an executable

Describe the stages from `main.c`/`swap.c` to two `.o` files and one executable. Distinguish compiler, assembler, compiler driver, and pseudo-instruction line counts.

<details><summary>Show solution</summary>

Each source passes through preprocessing, compilation, and assembly to a separately compiled relocatable object. A compiler translates high-level operations, an assembler encodes assembly, and a driver can invoke several stages. The linker combines objects. Machine code in `.o` does not settle external references or final placement; a pseudo-instruction may expand, so source-line count is not executed-instruction count.

**Checking points:** Check stage order, tool roles, relocatability, and the pseudo-instruction counting caveat.

</details>

#### Recall Q03 · Name resolution and address adjustment

Use the call to `swap` and `bufp0=&buf[0]` to distinguish symbol resolution from relocation. Classify code, initialized data, `bufp1`, and symbol/debug information in the example.

<details><summary>Show solution</summary>

Resolution determines which definitions the names `swap` and `buf` denote. Relocation adjusts call and pointer address references to final code/data placement. The diagram puts `main`/`swap` in `.text`, initialized `buf`/`bufp0` in `.data`, and `bufp1` in `.bss`. Headers, `.symtab`, and `.debug` are distinct from ordinary instructions/data; `temp` does not belong in the global/static section list.

**Checking points:** Distinguish definition selection from address adjustment, including the initialized pointer.

</details>

#### Recall Q04 · ELF file and runtime memory

What is missed by equating the ELF section list with the entire runtime memory layout? Distinguish read-only/read-write content, heap, shared libraries, and stack.

<details><summary>Show solution</summary>

The figure groups `.init`, `.text`, and `.rodata` as read-only, and `.data`/`.bss` as read/write. Runtime also distinguishes heap, shared-library mappings, user stack, and a kernel region. Treating all symbol/debug information as ordinary data confuses tooling information with execution state. The loader prepares the runtime image; the displayed addresses illustrate one 32-bit layout.

**Checking points:** Check both segment groups, additional runtime regions, and the illustrative address scope.

</details>

#### Recall Q05 · Register and memory updates

Initially `PC=0x1000`, `x10=0x2000`, and `MEM[0x2000]=41`. Trace `x5`, memory, and PC after the taught `lw x5,0(x10)` → `addi x5,x5,1` → `sw x5,0(x10)`, distinguishing loader from ISA.

<details><summary>Show solution</summary>

After the load, `(x5,memory,PC)=(41,41,0x1004)`; after addition, `(42,41,0x1008)`; after the store, `(42,42,0x100C)`. Memory stays 41 until the store. The loader prepares executable content; the ISA defines each state change. PC advances by four because these instructions are 32 bits long.

**Checking points:** Check all three states without confusing data-register width with instruction length.

</details>

### Apply and diagnose

#### Practice P01 · Find confused stages

Newly written materials-based general practice; the supplied 18-question index has no direct linking/loading style evidence. Correct each claim: (a) An address initializer in `bufp0` is valid for every final layout as soon as `.o` is created. (b) Since `temp` is absent from `.bss`, swap cannot preserve the first value. (c) Loading `addi` immediately changes memory's 41 to 42.

<details><summary>Show solution</summary>

(a) The pointer reference must match `buf`'s final placement; the claim ignores relocation. (b) Automatic `temp` preserves the original value at runtime independently of global/static section classification. (c) Loading differs from execution, and executing `addi` changes only the register here. Memory becomes 42 after the store executes.

**Checking points:** Diagnose the three errors using relocation, storage roles, and execution effects.

</details>

### Review plan

Explain symbols, translation, and address linking using Q01–Q03, then redraw the file/memory distinction and state table in Q04–Q05. Diagnose P01 before strengthening address/value/width distinctions in [[courses/computer_architecture/units/en/data-register-memory|registers and memory]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-03-lecture-02|2026-09-03 · materials-only review]]

- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-019|p.19]], [[page_cache/computer_architecture/lec.02/page-020|p.20]], [[page_cache/computer_architecture/lec.02/page-028|p.28]], [[page_cache/computer_architecture/lec.02/page-021|p.21]], [[page_cache/computer_architecture/lec.02/page-022|p.22]], [[page_cache/computer_architecture/lec.02/page-023|p.23]], [[page_cache/computer_architecture/lec.02/page-024|p.24]]

- This entire unit reviews September 3 lec.02 materials without a recording or STT; exact spoken progress is unverified.
- The ELF address diagram is a 32-bit illustration, not a fixed layout for all OS/RV64 systems. Linking uses an introductory static model without all relocation types or dynamic-linker mechanisms.
- Traces assume basic 32-bit instructions and valid data addresses; they are reasoning exercises, not results from executing source commands or assignment implementations.


---

[[courses/computer_architecture/units/en/architecture-contract|← Previous: Computer Organization and the ISA Contract]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/data-register-memory|Next: Data Representation, Registers, and Memory →]]
