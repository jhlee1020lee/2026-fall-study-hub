---
title: "Procedure Calls, Calling Conventions, and the Stack"
description: "Trace calling conventions, frames, and preservation/return behavior in leaf, factorial, and string-copy examples."
course: "computer_architecture"
unit_id: "procedures-stack"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-10-lecture-04"]
---

Read function calls as movements of arguments, results, return addresses, and values that must survive. Track frame allocation and restoration separately to check how leaf, recursive, and string-copy procedures preserve their caller's state.

## Arguments, results, and return addresses

A procedure call requires more than jumping to a target. The caller passes arguments; the callee obtains local storage, computes, supplies a result, and returns to the original control flow. Where [branches and control flow](control-synchronization.md) select the next instruction, procedure calls add **where to return and what to preserve**.

In the course's integer-argument examples, `x10`–`x17` hold arguments and `x10` receives a result. The register table also identifies `x10`–`x11` as return-value registers. By contrast, `x1` holds a return address. A return value is a computed result; a return address identifies the caller's continuation. Returning the integer 7 places 7 in `x10` in this example, not in `x1`. [[page_cache/computer_architecture/lec.03/page-041|CA M003 p.41]]

```asm
jal  x1, ProcedureLabel
jalr x0, 0(x1)
```

These are typical call and return forms, respectively. `jal x1,ProcedureLabel` saves the following instruction's address in `x1` and jumps to the target. In the basic 32-bit-instruction examples, that link is `PC+4`. `jalr x0,0(x1)` returns using `x1` and discards its new link through `x0`. `jalr` is not return-only: it jumps using a register-derived address, and the material also mentions computed jumps for `switch`. [[page_cache/computer_architecture/lec.03/page-042|CA M003 p.42]]

At 39:39 on September 10, the lecturer explains placing this computed result in `x10` and identifies `x10` and `x11` as result registers more generally. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 39:39 · result transfer]] In contrast, the phrase “return value … register s one” at 40:28 remains marked unclear in the STT. It neither establishes that `x1` was clearly spoken nor supplies a rule putting the computed result there. The distinction on pp.41–42 is the basis for separating that result from the address of the caller’s continuation. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 40:28 · unclear return explanation]] Recalled Q3 likewise calls for checking **how the target is formed and where the link goes**, rather than memorizing exclusive “call” and “return” labels. [EX:ca_2025_2_midterm_q03 p.2]

## Calling conventions and preservation responsibilities

Caller and callee share the register file. A calling convention lets separately produced functions communicate reliably. A callee must preserve and restore any callee-saved register it changes. A caller cannot assume caller-saved registers survive a call, so it preserves values it still needs afterward. Neither rule requires saving every register unconditionally.

Read the table in [[page_cache/computer_architecture/lec.03/page-048|CA M003 p.48]] in terms of responsibilities:

| Register | Alias/purpose | Responsibility for needed values |
|---|---|---|
| `x0` | `zero` | Always zero |
| `x1` | `ra`, return address | Caller |
| `x2` | `sp`, stack pointer | Callee |
| `x3`, `x4` | `gp`, `tp` | A dash does not designate ordinary temporaries |
| `x5`–`x7` | `t0`–`t2` | Caller |
| `x8`–`x9` | `s0/fp`, `s1` | Callee |
| `x10`–`x17` | `a0`–`a7`, arguments/some results | Caller |
| `x18`–`x27` | `s2`–`s11` | Callee |
| `x28`–`x31` | `t3`–`t6` | Caller |

If the caller needs its old `x5` after a call, it must preserve it. If the callee uses `x18` as workspace, it must restore the original value. Informally using a register “temporarily” does not place it in the convention's Temporary category: `x18` remains callee-saved.

A compiler and library following the same convention can exchange arguments and results even when compiled separately. The lecture used library interoperability to motivate this agreement. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 45:52]] The detailed runtime rules for `gp` and `tp` are not taught here; a blank saver entry is not permission to overwrite them freely.

## Stack frames and memory layout

The conceptual memory layout places reserved space, text, static data, dynamic data, and stack from lower toward higher addresses. Text is program code; static data includes global/static variables and the material's constant-array/string examples; the heap contains dynamic data associated with operations such as `malloc` or `new`. The stack supplies procedure storage. `gp=x3` is associated with a base for offset references into static data. The diagram does not prescribe every OS's exact address layout. [[page_cache/computer_architecture/lec.03/page-055|CA M003 p.55]]

The pictured heap grows toward higher addresses and the stack toward lower addresses. “Top of stack” therefore means the active push/pop end, not the highest address. The stack pointer, `SP=x2`, identifies that end. A procedure frame or activation record holds one invocation's required storage, potentially including saved argument registers, return address, saved registers, and local arrays or structures.

The frame pointer, `FP=x8`, can provide a reference point for the frame. It is a technique used by some compilers, not a mandatory separate value in every function. In the simple integer-argument model, arguments beyond the eight register positions can be passed on the stack. [[page_cache/computer_architecture/lec.03/page-056|CA M003 p.56]] [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 57:36]] Allocating a new frame does not mean the entire program stack is empty, nor does every C local variable necessarily occupy memory.

## Saving, computing, and restoring in a leaf procedure

A leaf procedure calls no other procedure. The source's `leaf_example` receives `g,h,i,j` in `x10,x11,x12,x13` and computes `(g+h)−(i+j)`. It uses `x18` and `x19` for the sums and `x20` for the difference, so all three callee-saved registers need preservation.

Pages 44–46 print `add x19,x12,x1` for the second sum, conflicting with `j=x13` on p.43 and the `i+j` comment. The following listing **corrects that operand to `x13`** using the material's internal evidence. It does not claim the lecturer clearly spoke the corrected operand.

```asm
leaf_example:
    addi sp, sp, -24
    sd   x18, 16(sp)
    sd   x19, 8(sp)
    sd   x20, 0(sp)
    add  x18, x10, x11
    add  x19, x12, x13
    sub  x20, x18, x19
    addi x10, x20, 0
    ld   x20, 0(sp)
    ld   x19, 8(sp)
    ld   x18, 16(sp)
    addi sp, sp, 24
    jalr x0, 0(x1)
```

Three 64-bit saves require the diagram's `3×8=24 bytes`. If entry SP is `S`, the new SP is `S−24`. From low addresses upward, the original `x20`, `x19`, and `x18` occupy `S−24`, `S−16`, and `S−8`. The three pictures in [[page_cache/computer_architecture/lec.03/page-047|CA M003 p.47]] show before allocation, during storage, and after return: SP moves downward in the middle and returns to its original position at the end.

Copying the result into `x10` before restoring `x20` prevents losing the return value. Merely raising SP does not restore register contents: the three loads restore values, and the final `addi` releases frame space. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 42:58]] This 24-byte sequence is the lecture's storage/restoration model, not certification that it meets every external ABI alignment and calling requirement.

## Preserving n and the return address in recursion

A non-leaf procedure calls another procedure. The material's `fact(n)` returns 1 for `n<1` and otherwise returns `n×fact(n−1)`. Both the original `n` and the recursive result use `x10`. The multiplication still needs the original `n`, so it must be preserved. A new `jal` also overwrites `x1`, requiring preservation of the current return address. [[page_cache/computer_architecture/lec.03/page-052|CA M003 p.52]]

The prologue subtracts 16 from SP, saves `x1` at `8(sp)` and `n` at `0(sp)`, computes `x5=n−1`, and uses `bge x5,x0,L1` to select recursion. For ordinary small inputs in the base case, it puts 1 in `x10`, restores SP, and returns. No further call has overwritten the existing `x1`.

The recursive path calls with `x10=n−1`. On return, it copies the result into `x6` before restoring the original `n` into `x10` and the return address into `x1`. It restores SP, computes `x10=n×x6`, and returns. Moving the result first prevents the restored argument from overwriting it.

An illustrative small trace of `fact(2)` is:

| Invocation | Preserved information | Nested work | Result |
|---|---|---|---|
| `fact(2)` | n=2 and its caller's continuation | Multiply `fact(1)` by 2 | 2 |
| `fact(1)` | n=1 and continuation in `fact(2)` | Multiply `fact(0)` by 1 | 1 |
| `fact(0)` | The source prologue still allocates space | Base case | 1 |

Calls descend `2→1→0` and results return `1→1→2`. The lecture explained preservation and the base case but left the `n>=1` path for self-study; the complete recursive trace here is materials-based. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 51:55]] This is not a general implementation handling subtraction/multiplication overflow or stack exhaustion.

## Copying the terminating byte in a string

The source's `strcpy` example uses `while ((x[i]=y[i])!='\0') i+=1;`. Assignment occurs **before** the termination test, so the zero terminator is copied too. `x10` is the destination base, `x11` the source base, and `x19` the index. Because elements are bytes, addresses use `base+i` rather than the `8i` used for doubleword arrays. [[page_cache/computer_architecture/lec.03/page-058|CA M003 p.58]]

The loop portion of p.59 is:

```asm
L1: add  x5, x19, x11
    lbu  x6, 0(x5)
    add  x7, x19, x10
    sb   x6, 0(x7)
    beq  x6, x0, L2
    addi x19, x19, 1
    jal  x0, L1
```

For illustrative source `{'A','B',0}`, the loop performs three byte loads, three byte stores, and two index increments. Moving `beq` before `sb` would stop without storing the terminator. These counts exclude the stack save and restore outside the loop.

Because `x19` is callee-saved, the material saves it in an 8-byte slot, initializes `i=0`, and at `L2` restores it, restores SP, and returns. `lb` and `lbu` may produce different 64-bit results, yet their low byte and zero/nonzero outcome can agree for this immediate `sb` and zero-test use. That does not make the loads generally interchangeable. The lecturer focused on `lbu` and `sb` and assigned the rest of the trace to self-study. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 01:01:31–01:03:52]]

This full loop explanation is materials-based and assumes sufficient destination capacity and a valid terminated source. No length check appears in the code. Return behavior, preservation obligations, and valid memory access remain separate things to verify when combining procedures with data access.

## Key Takeaways

- A return value is a result; a return address is a continuation location.
- Callers preserve needed caller-saved values; callees restore callee-saved values they modify.
- Restoring SP releases space but does not reload saved registers.
- Recursion must preserve original arguments and the current continuation across another call.
- Assignment before the string termination test copies the zero byte as well.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Call results and continuations

A basic 32-bit `jal x1,F` at `0x400` calls F, which returns integer 7. Identify argument/result registers, the value of `x1`, and the purpose of `jalr x0,0(x1)`. Is `jalr` exclusively for return?

<details><summary>Show solution</summary>

Integer arguments use `x10`–`x17`, and this result 7 goes in `x10`. `x1=0x404` identifies the caller's next instruction, not the result. Return jumps using `x1` and discards the new link through `x0`. Since `jalr` uses a register-derived target, it also supports computed jumps. Procedures additionally need local storage, computation, preservation, and result transfer.

**Checking points:** Separate 7 from 0x404, explain discarded linkage, and retain the general use of `jalr`.

</details>

#### Recall Q02 · Who preserves what?

A caller needs old `x5` and `x18` after a callee changes both. Assign responsibility, then classify `ra`, `sp`, temporary/saved/argument registers and interpret the dashes for `gp/tp`.

<details><summary>Show solution</summary>

The caller saves needed `x5` before the call; the callee saves and restores the `x18` it changes. Caller responsibility covers `x1/ra`, `x5`–`x7`, `x28`–`x31`, and `x10`–`x17`; callee responsibility covers `x2/sp`, `x8`–`x9`, and `x18`–`x27`. `x0` stays zero; dashes for `x3/gp` and `x4/tp` do not designate free temporaries. Briefly using `x18` does not change its obligation. Save according to needed/modified values, not every register automatically. A shared convention permits separately compiled library interoperability.

**Checking points:** Check both responsibilities, table categories, conditional preservation, and library motivation.

</details>

#### Recall Q03 · Frames and memory layout

Explain text, static data, heap, stack, and the illustrated growth directions. Describe possible frame contents, SP/FP/gp roles, integer arguments beyond eight positions, and the meaning of stack top.

<details><summary>Show solution</summary>

Text holds code, static data holds global/static objects, the heap dynamic data, and the stack invocation storage. The diagram grows heap upward and stack toward lower addresses, so allocation decreases SP. Frames can contain needed saved arguments, return addresses, saved registers, and local arrays. `sp=x2` marks the active end; optional `fp=x8` provides a frame reference, and `gp=x3` relates to static-data offsets. Additional integer arguments can use the stack in the simple model. Top is not highest address; a new frame neither removes caller frames nor puts every local in memory.

**Checking points:** Check roles, directions, SP/FP, possible contents, and layout limits.

</details>

#### Recall Q04 · Leaf frame and result

For the taught leaf, entry `sp=0x1000`, old `x18,x19,x20=100,200,300`, and arguments `g,h,i,j=9,4,5,2`, trace save addresses, result, and restored registers/SP. Explain the printed `x1` error in the second sum and the ordering of result copy, reloads, and SP restoration.

<details><summary>Show solution</summary>

Allocating 24 bytes gives SP=`0xFE8`. Save old `x20=300` at `0xFE8`, `x19=200` at `0xFF0`, and `x18=100` at `0xFF8`. Sums are 13 and 7, giving 6. Since j is in `x13`, the second sum uses `x12+x13`, not return-address register `x1`. Copy 6 into `x10` before reloading old 100/200/300 and restoring SP=`0x1000`. Raising SP alone does not restore registers; copying after reloading `x20` would return 300.

**Checking points:** Check all addresses, corrected operand, result 6, restored values, and SP; the frame is the classroom model.

</details>

#### Recall Q05 · Arguments and return addresses in recursion

Trace values through the source-model `fact(2)` down to `fact(0)` and back, and calculate peak frame space. Why save both n and `x1`, and copy the recursive result to `x6`? Why needn't the base case reload `x1`?

<details><summary>Show solution</summary>

Calls descend 2→1→0; results return 1→1→2. Each entry allocates 16 bytes, including the base case: peak usage is 48 bytes and deepest SP is S−48. Each frame stores original n at `0(sp)` and the continuation at `8(sp)`. Recursion replaces `x10` with the result and `jal` replaces `x1` with a new link. Copy the result to `x6` before restoring n to `x10`. The base makes no nested call, so `x1` is unchanged and only SP needs restoration there. After all returns, SP is S.

**Checking points:** Check all calls/results, 48 bytes, both preservation reasons, and the base path.

</details>

#### Recall Q06 · String copy and the terminator

For the taught `strcpy` copying `{'A','B',0}`, count loop loads, stores, and increments, and give the address expression. Explain moving the test before `sb`, preserving `x19`, and the limited equivalence of `lb`/`lbu`.

<details><summary>Show solution</summary>

Byte elements use source/destination base+i. Copying before testing includes zero, so there are three loop loads, three stores, and two increments. Testing first omits the terminating store. Since `x19` is callee-saved, save its entry value in the illustrated eight-byte slot, reload it on exit, and restore SP. `lb/lbu` can differ in upper bits but agree on the low byte and zero test for this immediate `sb` use. They are not equivalent for arbitrary register computation; sufficient destination space and a valid terminated source are required.

**Checking points:** Check terminator-inclusive counts, byte offsets, preservation, and the limited load equivalence.

</details>

### Apply and diagnose

#### Practice P01 · Wrong return after a nested call

Newly written synthetic practice combines the target/link distinction in [EX:ca_2025_2_midterm_q03 p.2] with taught preservation rules. The caller executes `0x400: jal x1,F`; F executes `0x810: jal x1,G`. F saves neither its return address nor `x5=9`, which it needs after G, and later proposes putting return value 7 in `x1`. Give each call's link, diagnose all three defects, and specify preservation and result locations. Use the basic 32-bit instruction model.

<details><summary>Show solution</summary>

The first link is `0x404`; the nested link is `0x814`. Without saving old `x1`, F loses the original caller's `0x404` continuation after returning from G. `x5` is caller-saved, so F, as G's caller, must preserve its needed 9 instead of assuming G retains it. Put result 7 in `x10`, restore the outer link into `x1`, restore needed saved state/stack space, and return. Setting `x1=7` incorrectly uses a computed result as a return target.

**Checking points:** Distinguish 0x404/0x814 and resolve return-address, live caller-saved, and return-value issues separately.

</details>

### Review plan

Reconstruct register roles and frame layout with Q01–Q03. Tabulate entry, computation, and return states for Q04–Q06; diagnose missing preservation in P01 before [[courses/computer_architecture/units/en/performance-model|execution-time models]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 · lecture notes]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-041|p.41]], [[page_cache/computer_architecture/lec.03/page-042|p.42]], [[page_cache/computer_architecture/lec.03/page-043|p.43]], [[page_cache/computer_architecture/lec.03/page-044|p.44]], [[page_cache/computer_architecture/lec.03/page-047|p.47]], [[page_cache/computer_architecture/lec.03/page-048|p.48]], [[page_cache/computer_architecture/lec.03/page-049|p.49]], [[page_cache/computer_architecture/lec.03/page-050|p.50]], [[page_cache/computer_architecture/lec.03/page-052|p.52]], [[page_cache/computer_architecture/lec.03/page-055|p.55]], [[page_cache/computer_architecture/lec.03/page-056|p.56]], [[page_cache/computer_architecture/lec.03/page-058|p.58]], [[page_cache/computer_architecture/lec.03/page-059|p.59]]

- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 39:39 · result transfer; 40:28 · unclear return wording; 42:58, 45:52, 51:55, 57:36, 01:01:31–01:03:52]]

- September 10 at 39:39 supports `x10`/`x11` result transfer; 40:28 contains the unclear 'return value … register s one' wording. The latter is not recovered as clearly spoken `x1`.
- The leaf example's printed `x1` operand is corrected to `x13` from its argument mapping. The 24-byte/8-byte frames model storage/restoration, without certifying full ABI alignment compliance.
- The recursive factorial path and full string-copy trace are materials-based self-study. Factorial is not a general implementation handling overflow or stack exhaustion.
- String copy requires a valid terminated source and sufficient destination capacity, without a length check. Memory layout is conceptual, and FP is not a mandatory separate value in every function.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.


---

[[courses/computer_architecture/units/en/control-synchronization|← Previous: Bitwise Operations, Control Flow, and Synchronization]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/performance-model|Next: Execution Time and Performance Models →]]
