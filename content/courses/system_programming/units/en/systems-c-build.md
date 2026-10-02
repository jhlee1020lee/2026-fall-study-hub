---
title: "System Programming and Building C Programs"
description: "Review C control flow, build stages, and the distinction between local and remote work."
course: "system_programming"
unit_id: "systems-c-build"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab 0 setup.pdf", "assign2_README.md", "10.RE.Life.Cycle.of.a.Program.pptx", "11.RE.Linking.and.Loading.pptx"]
private_source_assets: ["lab 0 setup.pdf", "assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-07-lecture-02", "courses/system_programming/lectures/en/2026-09-09-lecture-03", "courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Connect a C program's state changes to the OS services and build steps that make it run. Track the calculation, build stage, and working environment separately to locate failures.

## System Programming and OS services

Consider a program that reads data from a file and computes a result. The program chooses the data and algorithm; the OS manages device access and permissions. System Programming studies this boundary and combines existing OS services for files, memory, and processes through their APIs. The [[courses/system_programming/transcripts/2026-09-02|2026-09-02 transcript]] at 43:28 explicitly frames the course as interaction with an existing OS.

C can express addresses and low-level I/O while organizing computation into types, expressions, and functions larger than individual assembly instructions. Linux provides an open implementation and Unix tools. This choice does not make C universally faster than other languages. Close control of machine behavior also requires checking portability across type sizes, compilers, libraries, and operating systems. The introduction names processes, exceptions, shells, networking, and concurrency as directions; it does not establish complete teaching of those subjects. See the connected [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 System Programming lecture]].

### From a CPU to a datacenter

A CPU executes instructions, memory holds working data, and a network carries data between machines. In the motherboard photograph on [system_programming:M004 slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx), distinguish the CPU socket from the long memory slots beside it. Multiple cores on one chip and connections to memory solve different parts of the system problem. Twice as many cores do not imply twice the application speed when work cannot be divided or memory is the bottleneck.

The lecture's laptop examples of four or eight cores, server examples of sixteen or more, slide range of 4–60 cores, and roughly 1-Gbit/s PC versus 10–100-Gbit/s datacenter networking are dated illustrations. The comparison from ENIAC (1946), mainframes, and Apollo 11 (1969) to smartphones conveys smaller and more widely available computing devices. Cars, watches, and speakers illustrate ubiquitous computing: software operates beyond conventional PCs. Claims of millionfold historical improvement are not controlled measurements of the same workload.

A cloud server handles storage, messages, and computation for many clients. Racks hold multiple servers; datacenters connect them at scale. Scale creates a placement problem as well as adding resources. A Content Distribution Network (CDN) places content copies in several regions so users need not always fetch from a distant origin. The distributed-video example at 11:07 illustrates this idea. A nearby server is a conceptual delivery advantage, not a claim that every browser computes the physically shortest distance itself.

The lecture uses hundreds of thousands of Meta servers, approximately four million Microsoft servers in 2021, and approximately 2.5 million Google servers in 2016 to illustrate scale. At 50:58, spending above 600 billion dollars by hyperscalers in 2026 is presented as a projection, not a verified spending result. The conversion of one billion dollars to roughly 1.4 trillion won is also a dated illustration. These figures supply scale rather than current specifications.

AI training and inference need High-Bandwidth Memory (HBM) to feed computation with data (53:45). Dividing the required memory across GPUs or machines can increase aggregate capacity, but intermediate results must then cross a network. Memory bandwidth, network bandwidth, and latency all influence completion time. The remark about the difficulty of placing 1 PB of HBM in one machine concerns contemporary cost and configuration, not a permanent physical law. This is how software demands reach semiconductor, SoC, and vehicle-hardware design.

## C abstractions and program state

The material introduces BCPL → B → C alongside Unix history. Compared with B's word-oriented model, C's types and byte-level access make low-level operations more expressive. The Multics-to-Unix story is the lecture's simplified history. K&R C is followed by the related ANSI C89 and ISO C90 standard names; the course compiler options select C99. Mentioning C23 does not make it the immediately succeeding standard after C99.

Structured programming decomposes work into subroutines and their calls. Object-oriented programming groups state with interfaces or member functions that operate on it. Breaking a calculation into functions and organizing persistent state behind an object's interface are different ways to manage complexity. The contrast between early Unix and a large Linux codebase motivates abstraction; it does not imply that assembly lacks subroutines.

### Expressions and side effects

Program state can be understood as the values stored in objects. An expression is a syntactic construct that is evaluated. `2 + 3` computes 5; `i = 10` both changes `i` as a side effect and has the value 10. Adding the semicolon makes `i = 10;` an expression statement. `i = j = 0` groups as `i = (j = 0)` and stores zero in both objects. Right associativity is not a general rule for the temporal order in which arbitrary operands are evaluated.

| Operator family | Forms and meaning |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/`, `%`, unary `-`; `%` computes integer remainder |
| Relational/equality | `<`, `>`, `<=`, `>=`, `==`, `!=`; distinguish these from assignment `=` |
| Logical | `&&`, `\|\|`, `!`; combine or negate conditions |
| Bitwise | `<<`, `>>`, `&`, `\|`, `^`; operate on bits |
| Compound assignment | `+=`, `*=` and related forms; update an existing object |

The broad explanation in the 2026-09-02 transcript at 01:39:14–01:42:07 needs a language-level qualification: a `void` function call is an expression but supplies no value. If `f` returns `void`, `f();` can be a statement, while `int n = f();` incorrectly demands a nonexistent integer result. This qualification clarifies the syntax; it is not a reconstruction of uncertain speech.

### Branches, loops, and function calls

`if (i < 0)` is true for `i = -1` and false for `0`, `1`, and `2`. In the separate `switch (i)` example, `1` selects `case 1`, `2` selects `case 2`, and `-1` or `0` selects `default`. A statement bearing the same example label in both fragments need not execute under the same condition. Omitting a case's `break` can allow execution to continue into the following case.

A `for` loop performs initialization, condition test, body, update, and another test. With no body modification of `i` or early exit, `for (int i = 0; i < 10; i++)` executes its body ten times, for `i = 0` through `9`. It tests the condition eleven times, including the final false test at 10. A `while` loop tests first and can execute zero bodies. A `do-while` executes the body first and therefore at least once.

`break` exits the current loop or `switch`; `continue` advances to the next iteration of the current loop. In a `for`, that includes the update expression. Braces group statements into a compound statement. `goto` transfers control to a label. At 01:42:07, the instructor motivates a common error label reached from several failed checks. Cleanup must still distinguish which resources each path has acquired.

This small example regularizes the material's function syntax:

```c
int add(int x, int y)
{
    return x + y;
}
```

`add(3, 5)` computes with its parameter values and returns 8. A function definition and a call expression have different roles. Comments written with `/* ... */` or `//` are not executable commands.

## Reading calculation and intent in a temperature loop

Names can reveal both role and unit. The temperature example on [system_programming:M004 slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx) can be written in regularized C99 form as follows.

```c
#include <stdio.h>

int main(void)
{
    int lower = 0, upper = 300, step = 20;
    for (int fahr = lower; fahr <= upper; fahr += step) {
        double celsius = (5.0 / 9.0) * (fahr - 32.0);
        printf("%3d %6.1f\n", fahr, celsius);
    }
    return 0;
}
```

`fahr`, `celsius`, `lower`, `upper`, and `step` communicate more than `a`, `b`, `c`, `d`, and `e`. Floating division in `5.0 / 9.0` preserves the ratio; integer `5 / 9` gives zero. The actual loop visits `0, 20, …, 300`, so it prints `(300 - 0) / 20 + 1 = 16` rows. After printing 300, the update produces 320 and the condition fails. Substituting 32°F gives 0°C as a separate algebraic check; 32 is not an input visited by this loop.

A function-level comment should explain purpose and the caller's contract rather than translate every line into prose. Small responsibilities, compiler diagnostics, and a reproducible input, symptom, and expected result make debugging more concrete. The lecture's seven-to-ten-hours-per-week suggestion is dated study advice, not a fixed personal requirement.

## Building an executable from source

Including `<stdio.h>` does not insert every implementation used by `printf` into the current source file. A declaration helps the compiler interpret a call; connecting that reference with the definition's machine code is another task. The [[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 build lecture]] and its [[courses/system_programming/transcripts/2026-09-07|transcript]] at 34:43 separate four stages.

| Stage | Example result | Responsibility |
|---|---|---|
| Preprocessing | `hello.i` | Process includes and macros; remove comments |
| Compilation | `hello.s` | Generate target-architecture assembly |
| Assembly | `hello.o` | Produce an object with machine code and linking information |
| Linking | `hello` | Connect references with definitions from other objects/libraries |

The material uses these commands to expose intermediate results:

```sh
gcc800 -E hello.c > hello.i
gcc800 -S hello.i
gcc800 -c hello.s
gcc800 hello.o -lc -o hello
gcc800 hello.c -o hello
```

The last command is the full-pipeline shortcut. The example default output name without `-o` is `a.out`. M003's `libc.a` illustration explains the stage relationship; it does not show that every actual build uses static libc. GCC acts as a compiler driver that invokes the necessary stages.

The central command in the `gcc800` wrapper is:

```sh
gcc -Wall -Werror -pedantic -std=c99 "$@"
```

`-Wall` enables a useful warning group, `-Werror` treats warnings as errors, `-pedantic` requests standards-related diagnostics, and `-std=c99` selects the language mode. `-Wall` does not enable every possible warning, and passing these diagnostics does not establish logical correctness. `"$@"` forwards the caller's arguments while preserving their boundaries.

The preparation described at 44:11 and on M003 slide 27 is to write the wrapper text, grant execution permission with `chmod +x gcc800`, and place it in a directory searched through `PATH`. The material gives `/usr/bin/gcc800` as an example. Being saved, being executable, and being discoverable by command name are separate properties. A file in a current directory outside `PATH` may instead require `./gcc800`. The statement that lab machines were already configured is a historical environment report.

### Separate compilation and the linker's two responsibilities

An optional materials-only review from RM004 slides 6–15, 17 and RM005 slides 5–8 develops the build distinction. Compiling `main.c` and `swap.c` separately allows one changed module to be recompiled before relinking. In the source example, `main.o` defines `main` and `buf` but lists `printf` and `swap` as `UND`. `swap.o` contains `swap`, `bufp0`, and its module-local `static bufp1`, while referencing external `buf`. A local linker symbol is not synonymous with an automatic local variable inside a function.

Symbol resolution associates references with definitions. Relocation adjusts address-dependent references to reflect the locations of combined sections. An object `.o`, executable, and shared object `.so` therefore have distinct roles. Q5(a) at [EX:sp_2025_2_midterm_q05 p.12] asks for these responsibilities. The transferable reasoning is to separate connecting a name from adjusting an address, rather than merely saying that linking combines files. Detailed ELF structures, PC-relative patch bytes, and PLT/GOT behavior lie beyond this review. The older implicit-declaration example is not advice to omit prototypes.

## Local development and remote verification

The same source can build or behave differently when its compiler, headers, libraries, or OS differ. Ubuntu, WSL, and Linux VMs offer ways to manage those differences. The general procedure in the private Lab0 material is to install with `wsl --install` in an administrator Windows command prompt, then open Ubuntu or use `wsl` to enter a Linux shell. `uname -r` queries the kernel release; `lsb_release -a` reports distribution information. These descriptions are not an installation or login success record.

SSH provides an authenticated, encrypted remote shell; SCP copies files. The following examples replace account and host identities with role placeholders. The source's on-campus port 22 and off-campus port 2222 are historical instructions, not verified current endpoints.

```sh
ssh -p 2222 USER@HOST
scp -P 2222 -r assignment1/ USER@HOST:~/
scp -P 2222 -r USER@HOST:~/assignment1/ ./
```

SSH uses lowercase `-p` for the port; SCP uses uppercase `-P`. SCP's first operand is the source, its second the destination, and `-r` enables directory copying. The last line is a pedagogical reversal of the source/destination rule. Conflicting hostname spellings in the original material prevent identifying a current connection target from these examples.

The [[courses/system_programming/transcripts/2026-09-09|2026-09-09 transcript]] at 01:03:10 and 01:31:06–01:32:03, together with the [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 environment lecture]], explains opening remote `src/decomment.c` through Remote SSH. The sequence is extension installation, host/user/port configuration, connection, and remote editing. Although the window is local, the edited file and that remote terminal's build location are on the VM. Editing a local file instead requires a separate transfer followed by checking the remote file and build.

`man strstr` finds a function contract; a compiler translates and diagnoses; a debugger inspects execution; ctags/cscope help source navigation; source management tracks changes; trace tools expose runtime interactions. The later M018 ARM Mac guidance is a materials-only reminder to account for header/API differences and verify in the evaluation environment. Uncertain speech about a particular function's parameters does not establish a verified API difference. The next [objects and pointers discussion](objects-pointers.md) distinguishes the storage that such programs actually read and write.

## Key Takeaways

- A program chooses its work; the OS mediates services such as device access and permissions.
- Cores, memory, and networking can impose different bottlenecks; the lecture's scale figures are dated examples.
- Distinguish declarations, definitions, symbol resolution, and relocation when diagnosing builds.
- Track an expression's value separately from its side effects, and loop bodies separately from tests.
- The location of an editor window need not be the location of the edited or executed file.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Program and OS

A program reads a file and computes a sum. Separate its responsibilities from the OS's, and explain the motivation and limits of using C and Linux.

<details><summary>Show solution</summary>

The program chooses the file and algorithm and calls APIs; the OS manages permissions and device access. C expresses addresses and low-level I/O through types and functions, while Linux supplies an open implementation and Unix tools. This is interaction with an existing kernel, not evidence of universal C speed. Portability still depends on machine and OS differences.

**Checking points:** Identify both roles, both motivations, and the performance/portability qualification.

</details>

#### Recall Q02 · Hardware and performance

Explain CPU sockets, memory slots, networking, and multicore organization. Does doubling the cores double every program's speed? What does the progression from ENIAC to smartphones and vehicles illustrate?

<details><summary>Show solution</summary>

The CPU executes instructions, memory holds working data, and networking transfers data between machines. Multicore means multiple execution cores on a chip. Serial work or memory and communication bottlenecks prevent proportional speedup. The historical examples illustrate smaller, more widespread computing, including embedded uses. The cited core counts, bandwidths, and historical ratios are dated illustrations rather than controlled speedups.

**Checking points:** Connect component roles to bottlenecks and retain the historical scope of numerical examples.

</details>

#### Recall Q03 · Distributed capacity and communication

Connect cloud servers, racks, datacenters, and CDNs. What changes when GPU memory is spread over machines, and how should the lecture's 2026 spending projection be read?

<details><summary>Show solution</summary>

Servers handle client storage, messaging, and computation; racks and datacenters house and connect them. CDNs distribute copies to reduce dependence on a distant origin. Distributed memory expands aggregate capacity but adds communication of intermediate results, making bandwidth, latency, and placement consequential. HBM feeds computation rapidly. The spending figure is a projection, and the 1 PB remark concerns contemporary cost and configuration, not a permanent law.

**Checking points:** Include communication cost, CDN placement, and the distinction between a projection and an observed result.

</details>

#### Recall Q04 · C and abstraction

Explain the role of types and byte access in BCPL→B→C, compare structured programming with OOP, and distinguish the references to C89/C90, C99, and C23.

<details><summary>Show solution</summary>

In the lecture's simplified history, C's types and byte access make low-level control more expressive than B's word-oriented model. Structured programming decomposes work into subroutines; OOP groups state with interfaces that operate on it. Both manage complexity, and assembly can also have subroutines. ANSI C89 and ISO C90 are related standard names; the wrapper selects C99. Mentioning C23 does not make it C99's immediate successor.

**Checking points:** Distinguish task decomposition from state/interface organization and identify the C99 setting.

</details>

#### Recall Q05 · Installation, access, and copying

Explain `wsl --install`, `wsl`, `uname -r`, and `lsb_release -a`. Identify the direction and options of `scp -P 2222 -r assignment1/ USER@HOST:~/`, and contrast SSH with SCP.

<details><summary>Show solution</summary>

The commands install WSL, enter a Linux shell, report the kernel release, and report distribution information. The SCP command copies a local directory to the remote home: source first, destination second. `-P` sets the port and `-r` copies a directory recursively. Reversing the operands reverses the transfer. SSH provides an authenticated encrypted remote shell and uses lowercase `-p` for its port. `USER` and `HOST` are placeholders, not verified endpoints.

**Checking points:** Check each command's role, case-sensitive options, and source/destination direction.

</details>

#### Recall Q06 · Which file is being edited?

Describe opening a remote file with Remote SSH and contrast editing a local copy. Explain evaluation-environment checks and the roles of `man`, a debugger, and source-navigation tools.

<details><summary>Show solution</summary>

Install the extension, configure host/user/port, connect, then open and edit the remote file. The window is local but the file and remote terminal's build are remote. Editing a local copy requires transfer and verification of the actual remote file and build. OS, compiler, header, and library differences can matter. `man` supplies contracts, compilers translate and diagnose, debuggers inspect execution, ctags/cscope navigate source, source management records changes, and tracing exposes runtime interactions.

**Checking points:** Distinguish window and file locations and give concrete reasons for rechecking the environment.

</details>

#### Recall Q07 · Build stages and wrapper

Map the four build stages and results to `-E/-S/-c/-o`. Explain why headers do not remove linking, the wrapper's four diagnostic/language options and `"$@"`, and the difference between execution permission and `PATH`.

<details><summary>Show solution</summary>

Preprocessing produces `.i` after includes/macros/comments; compilation produces `.s`; assembly produces machine-code `.o`; linking connects external definitions into an executable. `-E`, `-S`, and `-c` stop after the corresponding stages; `-o` names the output. A header declaration is not implementation code. `-Wall` enables a warning group, `-Werror` promotes warnings, `-pedantic` requests standards diagnostics, and `-std=c99` selects C99. `"$@"` forwards argument boundaries. Saving the wrapper, granting execution permission, and placing it on `PATH` are separate conditions; an explicit `./gcc800` can be needed. Diagnostics do not prove logic correct.

**Checking points:** Cover all four stages and options, declaration versus definition, and permission versus lookup.

</details>

#### Recall Q08 · Connecting names and addresses

`main.o` lists `UND swap`, while another object defines `swap`. Distinguish symbol resolution from relocation, explain separate compilation, and clarify a local linker symbol.

<details><summary>Show solution</summary>

`UND` means the definition is absent from this object. Resolution binds a reference to its definition; relocation adjusts address-dependent references for final section placement. A changed source can be recompiled alone before relinking. An `.o` is linking input, an executable is a runnable result, and `.so` denotes a shared object. A module's `static` symbol has local linker visibility; this is not the same as an automatic function-local variable.

**Checking points:** Explain both responsibilities separately; `UND` alone does not mean compilation failed.

</details>

#### Recall Q09 · Tracing the temperature table

For the Fahrenheit table from 0 through 300 in steps of 20, give the formula, row count, and terminating state. Is 32°F printed? Explain the `5/9` bug and useful naming, comments, and reproduction information.

<details><summary>Show solution</summary>

Use `(5.0/9.0)*(fahr-32.0)`. The sequence `0,20,…,300` has 16 rows; the final update reaches 320 and fails the test. 32°F→0°C is an independent formula check, not a loop row. Integer `5/9` is zero. Descriptive names expose units and bounds, function comments explain purpose and caller contracts, and a reproducible report records input, symptom, expected result, and diagnostics.

**Checking points:** Check 16 rows, 320 at termination, absence of 32, and the integer-division cause.

</details>

#### Recall Q10 · Values, effects, and operators

Explain the stored values and expression value of `i=j=0`, and distinguish `=`/`==`, `%`, `&&`/`&`, and `+=`; classify the other taught operator families. With `void f(void)`, is `f()` an expression, and is `int n=f();` valid?

<details><summary>Show solution</summary>

Right association gives zero to both variables and to the assignment expression. Association is not a general operand-evaluation order. `=` assigns, `==` compares, `%` gives integer remainder, `&&` combines logical conditions, `&` operates on bits, and `+=` updates an existing value. Other taught families include arithmetic `+`, `-`, `*`, `/` and unary `-`; logical `||` and `!`; relational `!=`, `<`, `>`, `<=`, `>=`; bitwise `<<`, `>>`, `|`, `^`; and compound `*=`. `f()` is a void expression: `f();` is a valid expression statement, but `int n=f();` demands a value that does not exist.

**Checking points:** Separate value, state change, operator families, and the absence of a void value.

</details>

#### Recall Q11 · Branches, loops, and functions

Trace the chapter's `if (i<0)` and `switch` with cases 1, 2, and default for `i=-1` and `i=2`. Explain the body/test counts of `for (int i=0;i<10;i++)`, loop/control distinctions, a common error label, and `add(3,5)`.

<details><summary>Show solution</summary>

For -1, the `if` takes its true branch and the `switch` takes default; for 2, the `if` takes its false branch and the `switch` takes case 2. Missing `break` may cause fall-through. Without body changes or early exits, initialization occurs once, followed by test/body/update cycles: 10 bodies and 11 tests, ending at i=10. An initially false `while` runs zero bodies; `do-while` runs one. `break` exits the relevant loop/switch; `continue` proceeds through the `for` update. A common error label consolidates failures but cleanup must reflect acquired resources. An `add` returning `x+y` gives 8 for this call. Braces group statements; comments do not execute.

**Checking points:** Check both branch cases, 10/11 counts, the `for` update after `continue`, and the function result.

</details>

### Apply and check

#### Practice P01 · Distinguishing two build failures

**Newly written synthetic practice.** Transfer the resolution/relocation distinction from Q5(a) [EX:sp_2025_2_midterm_q05 p.12] to a diagnosis. Prerequisites are the chapter's build stages, separate compilation, and remote-file distinction; PLT/GOT and relocation bytes are excluded.

You changed local `helper.c`, but the remote copy is old. Remote `main.o` lists `UND helper` and linking without `helper.o` fails with an unresolved symbol. (a) Does including the header again fix this? (b) Why might adding the object and linking successfully still omit the change? (c) State what to check at each stage.

<details><summary>Show solution</summary>

(a) No: a declaration does not supply a definition's machine code. The defining object/library is needed. (b) The remote source/object may still be old; link success does not certify the intended source version. (c) Check that the remote file contains the change, recompile it there, include the defining object, resolve references and relocate them for placement, then check behavior. Relocation cannot manufacture a missing definition.

**Checking points:** Identify the missing definition, stale remote copy, and distinction between link success and behavioral verification.

</details>

### Review plan

Draw the build flow from Q07–Q08, then classify P01's failures by stage. Check Q09–Q11 with a table of stored values, outputs, and tests, and use Q05–Q06 to state where the working file resides.

## Sources

[[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 · lecture note]]

[01.CProgrammingExamples.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx) — slides 17, 21–27

[00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx) — slide 30; PDF p.35 / slide 35 (section agenda); PDF p.36 / slide 36 (hardware figure and specifications); PDF p.36 / slide 36; PDF p.37 / slide 37; PDF p.38 / slide 38; slide 46; slide 50; slide 15; slide 63; slide 59; slide 60; slide 56; slide 57

[[courses/system_programming/transcripts/2026-09-02|2026-09-02 · corrected transcript]] — 43:28, 47:03, 11:07, 53:45, 50:58, 01:39:14, 01:42:07

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 · corrected transcript]] — 34:43, 44:11

[[courses/system_programming/transcripts/2026-09-09|2026-09-09 · corrected transcript]] — 01:03:10, 01:31:06, 01:32:03

[10.RE.Life.Cycle.of.a.Program.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/10.RE.Life.Cycle.of.a.Program.pptx) — slide 6; slide 14

[11.RE.Linking.and.Loading.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/11.RE.Linking.and.Loading.pptx) — slide 5

The Lab 0 and official Assignment 2 README originals remain private; account values and passwords are omitted. Conflicting hostnames and uncertain UI/API speech remain unresolved. The September 23 note's ARM Mac guidance and Life Cycle/Linking slides are materials-based supplements, not evidence that the entire decks were taught. Hardware figures and spending projections are dated. Original duplicate `=`, missing do-while semicolon, old implicit-declaration examples, and later Q5 byte-count/call discrepancies are not silently repaired. Uncertain and redacted transcript passages remain limited.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.
