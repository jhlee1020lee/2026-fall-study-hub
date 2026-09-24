---
title: "System Programming and Building C Programs"
description: "Review C execution, development environments and build stages."
course: "system_programming"
unit_id: "systems-c-build"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab 0 setup.pdf", "assign2_README.md"]
private_source_assets: ["lab 0 setup.pdf", "assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-07-lecture-02", "courses/system_programming/lectures/en/2026-09-09-lecture-03", "courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Connect C state changes to executable generation. Use tool, environment and OS roles to explain where failure occurs.

## System Programming: programs that cooperate with an OS

A program that reads a file normally asks the operating system for a service rather than driving the storage device itself. The program chooses the data and algorithm; the kernel manages permissions and device access. System Programming begins with using files, memory, and processes correctly across this boundary. The [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 43:28]] explicitly takes the perspective of interacting with an existing OS.

C combines address and byte-level control with expressions larger than individual assembly instructions. Linux offers an open implementation and a Unix tool environment, making the route from program intent to machine operations accessible. This does not make C universally faster or other languages inappropriate. Greater control also brings responsibility for object lifetimes, valid addresses, and platform differences. Processes, exceptions, shells, networks, and concurrency are directions for later study. [Introduction slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### CPU, memory, and network costs

The CPU computes, memory holds data and instructions, and the network transfers data between machines. A multicore CPU has several execution cores on one chip. More cores help when work can be divided; twice as many cores do not automatically halve every program's running time.

In the mainboard photograph on slide 36, distinguish the CPU socket from the long memory slots. The accompanying 4–60 cores and 10–100-Gigabit Ethernet labels illustrate the hardware discussed in the lecture. The tentative component identification in the [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 47:03]] does not establish that a pictured component is a GPU. Laptop examples of four or eight cores, servers with sixteen or more, and a PC link near 1 Gbit/s are dated examples.

Slides 37–38 connect ENIAC (1946), a mainframe/Apollo 11 example (1969), and smartphones, then compare older cars and watches with computing-equipped versions. Look for changes in size and application setting. The “millions of times” wording is not a benchmark of one controlled workload. Ubiquitous computing extends software's reach to cars, watches, speakers, and devices for pets. [Introduction slides 36–38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### Data movement in clouds and CDNs

A cloud server handles storage, messaging, or computation for clients. A rack holds multiple server machines; a datacenter connects them at scale. A CDN, or Content Distribution Network, places content copies in multiple regions, reducing dependence on a distant origin server. This is a distribution principle, not a claim that every browser directly computes the physically nearest server. [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 11:07]]

The lecture's hundreds of thousands of Meta machines, roughly four million Microsoft servers in 2021, and roughly 2.5 million Google servers in 2016 are dated scale illustrations. At [[courses/system_programming/transcripts/2026-09-02|September 2, 50:58]], spending above 600 billion dollars in 2026 is expressed as a forecast, not a confirmed expenditure. The conversion of one billion dollars to approximately 1.4 trillion won is likewise part of that explanation.

AI training and inference create demand for HBM, High-Bandwidth Memory. Distributing a workload across GPUs or machines can increase available memory, but intermediate data must then cross a network. Capacity alone does not determine execution time: bandwidth and latency can become bottlenecks. The [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 53:45]] connects software demands to memory, semiconductor, SoC, and network design. Its cost-based discussion of HBM capacity in one machine is not an eternal physical limit.

## C abstractions and changes to program state

The BCPL→B→C lineage, presented alongside Unix, illustrates the search for expressive low-level control. Compared with B's word-centered representation, C expresses types and byte-level access. The lecture sketches Multics and Unix, K&R C, ANSI C89/ISO C90, and C99. The course build options select C99; the mention of C23 does not mean it immediately followed C99. [Introduction slides 45–50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

Structured programming decomposes work into functions and their interactions. Object-oriented programming groups state with interfaces that operate on it. These are complementary ways of managing complexity. Assembly can also implement subroutines; the point is that higher-level languages make the organization of large programs easier to express.

### Expressions, statements, and side effects

Think of execution as changes to a current state. An expression is a construct that is evaluated: `2 + 3` has value 5, and the literal `2` has value 2. The expression `i = 10` both stores 10 into `i`, a side effect, and has value 10. Adding a semicolon gives the expression statement `i = 10;`. [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:39:14]]

`i = j = 0` groups as `i = (j = 0)`. Both objects receive zero, and the whole assignment expression has value zero. This is an associativity rule, not a general rule about evaluation order for all operands. `=` stores a value; `==` tests equality.

| Purpose | Operators | Interpretation |
|---|---|---|
| Arithmetic | `+ - * / %`, unary `-` | Compute values; `%` is integer remainder |
| Logical | `&& \|\| !` | Combine or negate truth conditions |
| Relational | `== != < > <= >=` | Compare values |
| Bitwise | `<< >> & \| ^` | Shift bits or combine corresponding bits |
| Compound assignment | `+= -= *= /= %= <<= >>= ^= \|=` | Compute and update an existing value |

This organizes the roles of the operators. Slide 55 repeats `=` in its assignment list; no missing original symbol is reconstructed here. The statement “expressions produce values” also needs a qualification: a `void` function call is an expression without a value. If `f` returns `void`, `f();` is valid, but `int n = f();` requests a nonexistent result.

### Following branches, loops, and calls

`if (i < 0)` branches on negativity; `switch (i)` enters the matching case. In the two separate examples on slide 56, `i=-1` selects the first `if` statement but the `switch` default. `i=2` selects the `else` statement and `case 2`. A `break` leaves the switch; without it, execution can continue into the following case.

The order of `for (int i = 0; i < 10; i++)` is initialization once, condition, body, increment, and another condition. If the body neither changes `i` nor exits early, it executes ten times, for 0 through 9. The condition is checked eleven times, including the final false check at 10. An initially false `while` executes its body zero times; a `do-while` executes it once. Correct C syntax includes the final semicolon in `do { ... } while (condition);`.

`break` ends the nearest applicable loop or switch. `continue` skips the rest of the current iteration; in a `for` loop, the increment still precedes the next test. `goto label;` transfers control to a label. The [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:42:07]] motivates a shared error label for multiple failure paths. Cleanup must still account for which resources each path actually acquired.

A function definition describes a computation, whereas a call requests it. Slide 60's example is:

```c
int add(int x, int y)
{
    return x + y;
}
/* Inside a calling function: */
int sum = add(3, 5);
```

The call supplies 3 and 5 and receives 8. Braces combine statements into a compound statement; `/* ... */` and `//` introduce comments for readers.

## A readable Fahrenheit–Celsius computation

The temperature table connects state, conditions, and repetition. This is slide 63's program with ordinary C quotation marks and operators.

```c
#include <stdio.h>

/* Print a Fahrenheit-Celsius table for 0, 20, ..., 300. */
int main(void)
{
    float fahr, celsius;
    int lower = 0, upper = 300, step = 20;

    for (fahr = lower; fahr <= upper; fahr = fahr + step) {
        celsius = (5.0 / 9.0) * (fahr - 32.0);
        printf("%3.0f %6.1f\n", fahr, celsius);
    }
    return 0;
}
```

The loop prints sixteen rows, including both 0 and 300. The first Celsius result is (5.0/9.0) × (−32) ≈ −17.8. Substituting 32°F into the formula gives 0°C, although 32 is not a row in this twenty-degree sequence. Replacing `5.0 / 9.0` with integer division `5 / 9` yields zero and destroys the conversion ratio. `%3.0f` displays no fractional digits; `%6.1f` displays one.

Names such as `fahr`, `celsius`, `lower`, `upper`, and `step` expose units and roles that `a,b,c,d,e` conceal. A function comment should explain what its caller can expect, rather than translate each instruction. Small functions, clear names, compiler diagnostics, and a precise account of input, expected output, and observed symptoms make debugging systematic. The lecture's seven-to-ten-hour weekly suggestion is planning advice, not a fixed requirement for every learner. [Introduction slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx), [C examples slides 17–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## From source code to an executable

`#include <stdio.h>` makes header contents, including the declaration of `printf`, available during preprocessing. Knowing a declaration is different from obtaining the implementation. Even a small `hello.c` passes through distinct stages.

| Stage | Example output | Responsibility |
|---|---|---|
| Preprocessing | `hello.i` | Expand includes and macros; remove comments |
| Compilation | `hello.s` | Translate C into target assembly |
| Assembly | `hello.o` | Produce machine-code object data |
| Linking | `hello` | Connect object files and library references |

The reference to `printf` can remain unresolved in `hello.o`. The `libc.a` example on slides 21–26 illustrates linking to an implementation; it does not establish that every actual build is statically linked. [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 34:43]]

```sh
gcc800 -E hello.c > hello.i
gcc800 -S hello.i
gcc800 -c hello.s
gcc800 hello.o -lc -o hello
gcc800 hello.c -o hello
```

The first four commands expose individual stages; the last requests the complete build. `-o hello` chooses an output name; the example without `-o` uses `a.out`. [C examples slides 20–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

An optional deeper distinction separates symbol resolution, which identifies the definition corresponding to an external name, from relocation, which adjusts address references for final placement. Historical Q5(a) demands that distinction. It extends the basic build explanation without making archive search order or PLT/GOT implementation prerequisites for this unit. [EX:sp_2025_2_midterm_q05 p.12]

### gcc800 diagnostics and shell lookup

The course wrapper runs:

```sh
gcc -Wall -Werror -pedantic -std=c99 "$@"
```

`-Wall` enables a collection of common warnings; `-Werror` treats warnings as errors. `-pedantic` requests diagnostics associated with the chosen language standard, and `-std=c99` selects that standard. Neither all possible warnings nor proof of logical correctness follows from these options. `"$@"` forwards the caller's arguments, including source filenames and `-o`.

Saving a wrapper, granting execution permission, and making its name discoverable are separate actions. The materials explain `chmod +x gcc800` and placement in a directory searched through `PATH`. If the current directory is not searched, an explicit path such as `./gcc800` is needed. [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 44:11]]

## Local development and remote execution

A program runs within a combination of compiler, headers, libraries, and OS. Local success does not establish that it will build and behave identically in the assessment environment. Lab 0 introduces Ubuntu, Linux VMs, and WSL, and recommends local development followed by testing in the Bacchus environment. The later Assignment 2 platform guidance also allows development on ARM Macs while requiring attention to Linux header and API differences; that detail is a handout supplement.

The supplied Windows procedure installs with `wsl --install` from an administrator command prompt, then opens the Linux shell through Ubuntu or `wsl`. `uname -r` identifies the kernel release; `lsb_release -a` identifies the distribution release. These are different layers. The following source-based examples replace account and host details with placeholders.

```sh
ssh -p 2222 USER@HOST
scp -P 2222 -r assignment1/ USER@HOST:~/
scp -P 2222 -r USER@HOST:~/assignment1/ ./
```

SSH provides an encrypted, authenticated remote shell; SCP copies files. SSH uses lowercase `-p` for the port, SCP uppercase `-P`, and SCP's `-r` copies a directory recursively. The two copy commands go local-to-remote and remote-to-local respectively. Ports 22 and 2222 belong to the dated lab guidance, not a newly verified endpoint.

With Remote SSH, a locally displayed editor can edit remote files, and its remote terminal builds on that machine. The [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 01:31:06–01:32:03]] describes installing the extension, configuring host/user/port, connecting, and opening a remote file. Editing a local file instead requires a separate transfer.

A manual lookup such as `man strstr` finds a function contract. Compilers translate and diagnose, debuggers expose execution state, ctags/cscope navigate code, source management records changes, and tracing tools expose calls. Connectivity alone does not establish correctness. [[courses/system_programming/units/en/objects-pointers|C objects and pointers]] next makes the distinction between stored values and addresses concrete.

## Key Takeaways

- Separate application, compiler and kernel responsibilities.
- Use units and names to check arithmetic and loop bounds.
- Verify execution separately from building.
- Continue with [[courses/system_programming/units/en/objects-pointers|objects and pointers]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · OS roles

Explain the responsibilities of a file-reading application and kernel, and the motivation for C and Linux.

<details><summary>Show solution</summary>

The application selects a file and algorithm and calls APIs; the kernel manages access and device services. C exposes addresses and low-level I/O, and Linux provides inspectable implementation and Unix tools. This means neither implementing the kernel nor proving C universally fastest. Future network/concurrency topics are not completed prerequisites.

**Check:** Separate requests, services, motivation and limits.

</details>

#### Recall Q02 · Components and bottlenecks

Explain CPU sockets, memory slots, networks and limits to scaling cores. What do historical and everyday computing examples show?

<details><summary>Show solution</summary>

CPUs in sockets execute instructions; memory in slots holds data; networks move data between machines. Limited parallelism or memory/communication stalls prevent proportional speedup when cores or bandwidth double. ENIAC (1946), Apollo/mainframes (1969), smartphones, cars and watches illustrate widespread computing. Dated figures are not current specifications; uncertain GPU speech remains uncertain.

**Check:** Give all three roles and a speedup counterexample.

</details>

#### Recall Q03 · Cloud and HBM

Connect servers, racks, datacenters and CDNs; explain the cost of spreading HBM capacity across machines.

<details><summary>Show solution</summary>

Servers form racks and datacenters. CDNs distribute content copies without guaranteeing that browsers directly select the physically nearest server. AI bandwidth demand motivates HBM. Distributing capacity introduces data-exchange bandwidth, latency and placement costs. Lecture server counts and the 2026 $600 billion spending figure are dated figures or projections, not verified outcomes.

**Check:** Distinguish capacity from communication cost and forecasts from outcomes.

</details>

#### Recall Q04 · C and abstraction

Relate BCPL/B/C, K&R, C89/C90/C99 and function/object-oriented organization.

<details><summary>Show solution</summary>

C developed from the BCPL/B lineage; K&R is an early description. ANSI C89 and ISO C90 mark standardization; the tools select C99. C23 is not C99’s immediate successor. Functions organize work/calls; objects organize related state/interfaces. Both can coexist, and assembly also has subroutines.

**Check:** Separate history, selected dialect and both organizing principles.

</details>

#### Recall Q05 · Local and remote

Explain WSL commands, SSH/SCP and port flags, copy direction and Remote SSH saves. Why verify in the lab, and which tools serve which roles?

<details><summary>Show solution</summary>

`wsl --install` installs; Ubuntu/`wsl` enters Linux; `uname -r` reports the kernel and `lsb_release -a` the distribution. SSH supplies an authenticated encrypted shell with `-p`; SCP copies with `-P` and recursive `-r`. `scp -P 2222 -r assignment1/ USER@HOST:~/` copies local to remote; reversing endpoints reverses direction. This dated syntax does not verify a current endpoint. Configuring/connecting/opening a folder through Remote SSH makes saves remote; local editing requires copying. Rebuild/run in the lab because OS, compiler, headers and libraries differ. `man strstr` explains APIs; debuggers inspect execution, ctags/cscope navigate, source management tracks changes, and tracing observes interactions.

**Check:** Check command roles, option case, save location and environmental differences.

</details>

#### Recall Q06 · Build stages

Explain source-to-executable stages/files/options, headers versus linking, and gcc800 options, permissions and PATH.

<details><summary>Show solution</summary>

Preprocessing handles includes/macros/comments to `.i` (`-E`); compilation yields `.s` (`-S`); assembly yields `.o` (`-c`); linking combines external definitions into an executable. `-o` names output; the default executable is `a.out`. Declarations are not implementation code. `-Wall` enables common warnings, `-Werror` makes warnings errors, `-pedantic` requests standard diagnostics and `-std=c99` selects the dialect; none proves correctness. `"$@"` preserves argument boundaries. Saving, `chmod +x` execution permission and `PATH` lookup are separate; `./gcc800` supplies a path. The `libc.a` diagram does not imply universal static linking.

**Check:** Check all stages/options, declaration/definition and permission/lookup.

</details>

#### Recall Q07 · Checking a temperature table

Calculate rows and first Celsius value for Fahrenheit 0..300 step 20, convert 32, and diagnose `5/9`. How do names/comments help?

<details><summary>Show solution</summary>

There are `300/20+1=16` rows. `(5.0/9.0)*(0-32)` is about −17.8; 32 converts to 0°C but is not a table row. Integer `5/9` becomes zero. Unit/bound/step names and caller-oriented comments expose intent for input/expected/actual checks. Study-time advice is not a fixed policy.

**Check:** Check 16, −17.8, the absent 32 row and integer division.

</details>

#### Recall Q08 · Expressions and statements

Explain `i=j=0`, `=`/`==` and `f();`/`int n=f();` for `void f(void)`; distinguish operator families.

<details><summary>Show solution</summary>

Right associativity stores 0 in j and i and yields 0; it does not dictate all operand evaluation order. `=` stores and `==` compares. `f()` is a void expression: `f();` is valid, but `int n=f();` demands a nonexistent value. Arithmetic/remainder, relations, logical `&& || !`, bitwise `& | ^ << >>` and compound assignment differ.

**Check:** Check state, value, void expressions and operator distinctions.

</details>

#### Recall Q09 · Branch and loop tracing

Trace −1 and 2 through `if(i<0)` and a switch with cases 1, 2/default. Explain the for counts, while/do-while, break/continue, error labels and `add(3,5)`.

<details><summary>Show solution</summary>

−1 takes if statement1 and switch default statement3; 2 takes statement2 in both. Without early exits or changes to i, initialization runs once, the body 10 times and tests 11 times, ending at i=10. A false-start while runs zero times, do-while once with its trailing semicolon. `break` exits the nearest loop/switch; `continue` proceeds to the next iteration step, including the for increment. A shared error label centralizes cleanup but must track acquired resources. `add(3,5)` passes arguments and returns 8; braces group statements and comments explain intent.

**Check:** Check branches, 10/11 counts and cleanup conditions.

</details>

### Practice

#### Practice P01 · Diagnosing a link failure

**Newly written synthetic practice.** A calls an external function and B defines it. A alone lacks the definition; combining A/B changes placement addresses. Distinguish the tasks and assess recopying the header.

[EX:sp_2025_2_midterm_q05 p.12] Q5(a) transfers the distinction between linker tasks to failure diagnosis. Prerequisite: Q06 objects/external names. Archive ordering, PLT/GOT and byte calculations are excluded.

<details><summary>Show solution</summary>

Symbol resolution connects references and definitions; relocation adjusts address-dependent references for combined placement. A header supplies no implementation, so cannot repair the missing definition. Providing B still leaves placement adjustment as a separate task.

**Check:** Distinguish definition binding and address adjustment.

</details>

### Review plan

Explain Q01–Q04 through roles/bottlenecks and connect Q05–Q06 as environment→build. Trace Q07–Q09 on paper, then classify the failure in P01.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 associated materials]]

### Materials and lecture passages

- [Introduction slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 36–38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 45–50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [C examples slides 17–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 20–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 43:28]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 47:03]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 11:07]]
- [[courses/system_programming/transcripts/2026-09-02|September 2, 50:58]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 53:45]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:39:14]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:42:07]]
- [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 34:43]]
- [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 44:11]]
- [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 01:31:06–01:32:03]]
- Lab 0 setup handout: local supplied PDF; no public link is available. ARM Mac setup is material-only evidence.
- September 23 Assignment 2 handout: requirements are discussed as a materials supplement; the private original and complete implementation are not linked.

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

### Scope to retain

- Hardware/cloud figures and spending projections are dated examples, not current measurements.
- ARM Mac instructions and the September 23 handout supplement are material-only. Endpoint discrepancies and uncertain speech remain unresolved.
- Only Q5(a) is selected. Later swap declaration/call discrepancies and nine bytes in an eight-byte answer slot are not adopted; supplied answers are not treated as authority.


---

[[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/objects-pointers|Next: C Objects, Types, Addresses, and Pointers →]]
