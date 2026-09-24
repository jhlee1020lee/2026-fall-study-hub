---
title: "Bitwise Operations, Control Flow, and Synchronization"
description: "Connect masks, branches, array loops, signed comparisons, and the two checks in LR/SC updates."
course: "computer_architecture"
unit_id: "control-synchronization"
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

Trace executed paths and changing values from bit operations through branches and loops. With shared memory, separate the predicate on loaded data from conditional-store success to reason correctly about retries.

## Logical shifts and fixed-width bit patterns

Bitwise operations move, select, or invert individual bits rather than treating a number only as a magnitude. They are useful for scaling an array index into a byte offset and extracting parts of a bit pattern. The distinctions between width and signedness in [data representation](data-register-memory.md), and between fields in [instruction encoding](instruction-encoding.md), establish the prerequisites.

`slli` shifts left and `srli` shifts right, filling vacant positions with zeros. The source's small examples are `0001 → 0010` and `0010 → 0001`. A left shift by `i` corresponds to a multiplication pattern by `2^i`, but bits shifted beyond the register width are discarded. Logical right shift corresponds to unsigned division by `2^i` with truncation; it does not preserve a negative value's sign. For an illustrative 8-bit `11110000`, shifting right once gives `01111000`.

The RV64 immediate-shift layout in [[page_cache/computer_architecture/lec.03/page-031|CA M003 p.31]] is `funct6(6) | shamt(6) | rs1(5) | funct3(3) | rd(5) | opcode(7)`. The widths total 32; the I-format's 12-bit area is divided between operation selection and shift amount. Six `shamt` bits represent shifts 0–63 for a 64-bit register. The lecturer corrected an initial R-type description to I-type. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 12:50]] September 8 only previewed this topic; the detailed teaching followed on September 10.

## AND, OR, XOR, and masks

A mask selects bit positions. AND produces 1 when both inputs are 1; OR when at least one is 1; XOR when the inputs differ.

| Inputs A,B | AND | OR | XOR |
|---|---|---|---|
| 0,0 | 0 | 0 | 0 |
| 0,1 | 0 | 1 | 1 |
| 1,0 | 0 | 1 | 1 |
| 1,1 | 1 | 1 | 0 |

An AND mask preserves positions containing mask bit 1 and clears positions containing 0. An OR mask sets selected positions; an XOR mask **toggles** them. For the source values `x10=0x0DC0` and `x11=0x3C00`, AND gives `0x0C00` and OR gives `0x3DC0`. [[page_cache/computer_architecture/lec.03/page-032|CA M003 pp.32–33]]

```asm
and x9, x10, x11
or  x9, x10, x11
xor x9, x10, x12
```

The first two lines are separate examples whose results should be inspected individually. For the third, the source makes every bit of `x12` one, thereby inverting `x10`. M003 p.34's wording “Set some bits to 1” is not a correct general definition of XOR. The truth table and depicted inversion support the explicit correction: selected bits are toggled.

C/Java notation `&`, `|`, `^`, and `~` corresponds to bitwise AND, OR, XOR, and NOT. RISC-V also has immediate forms `andi`, `ori`, and `xori`. Sign-extending −1 produces all ones, so `xori rd,rs1,-1` can invert every bit. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 16:27]] The source's Java logical-right-shift notation is `>>>`. C's `>>` should not be equated with `srli` without considering the operand type.

## Conditional branches and if/else paths

`beq rs1,rs2,L1` branches to `L1` when the register values are equal; `bne` branches when they differ. A false condition proceeds sequentially. The last operand is a branch target, not a result register.

The material translates `if (i==j) f=g+h; else f=g-h;` with `f,g,h,i,j` in `x19,x20,x21,x22,x23`: [[page_cache/computer_architecture/lec.03/page-036|CA M003 p.36]]

```asm
      bne x22, x23, Else
      add x19, x20, x21
      beq x0, x0, Exit
Else: sub x19, x20, x21
Exit:
```

Equal inputs fall through to addition and then jump to `Exit`. Unequal inputs jump directly to subtraction. Since `x0` always reads zero, `beq x0,x0,Exit` is unconditional. Omitting it would let the equal-input path fall through into subtraction and overwrite its result. Separating paths also requires preventing execution of the other path when they merge. The assembler resolves label placement. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 22:49]]

## Array loops and basic blocks

A loop separates address calculation, condition testing, update, and repetition. The source's `while (save[i] == k) i += 1;` uses `i=x22`, `k=x24`, base `x25`, and 8-byte elements. [[page_cache/computer_architecture/lec.03/page-037|CA M003 p.37]]

```asm
Loop: slli x10, x22, 3
      add  x10, x10, x25
      ld   x9, 0(x10)
      bne  x9, x24, Exit
      addi x22, x22, 1
      beq  x0, x0, Loop
Exit:
```

The first line computes `8i` and the second computes `base+8i`. The load obtains **the element at that address**, not the address itself. A mismatch exits; a match increments `i` and returns to calculate a fresh address. For illustrative `save={7,7,9}`, `k=7`, and initial `i=0`:

| Tested i | Loaded value | Comparison | Next action |
|---|---|---|---|
| 0 | 7 | Equal | Increment i to 1 |
| 1 | 7 | Equal | Increment i to 2 |
| 2 | 9 | Different | Exit with i=2 |

This code has no array-bounds check. It does not establish safe behavior if every valid element equals `k`.

A basic block is an instruction sequence with no internal branch and no internal branch target: a branch can appear at its end, and a target at its beginning. The four instructions from `slli` through `bne` form a block because normal control flow neither splits nor enters midway. Adding an incoming target at `ld` would split it there. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 27:52]] Compilers and processors can exploit such regions while preserving semantics. The definition does not prohibit exceptions or interrupts.

## Signed comparisons and inverted conditions

The same pattern can compare differently under different interpretations. `blt` and `bge` perform signed comparisons; `bltu` and `bgeu` perform unsigned comparisons. In the 32-bit example on [[page_cache/computer_architecture/lec.03/page-040|CA M003 p.40]], all ones versus 1 means `−1<1` signed but `4,294,967,295>1` unsigned. If the entire RV64 register is all ones, its unsigned value is `2^64−1`; the diagram's 32-bit number must not be reused for that case.

For `if (a>b) a+=1;` with `a=x22` and `b=x23`, invert the test to skip the body:

```asm
      bge  x23, x22, Exit
      addi x22, x22, 1
Exit:
```

The branch skips the increment when `b>=a`. Reading only the mnemonic and ignoring operand order misses how this implements the original condition. [[page_cache/computer_architecture/lec.03/page-039|CA M003 p.39]]

The same reasoning transfers to recalled Q12's conditional array store: determine which comparison enters or skips the body, distinguish the stored value from the array address, and select the store width from the data model. In particular, the lecture's 8-byte-element example cannot be applied indiscriminately to every `int` array. Establishing the comparison semantics, valid address, and store width in that order connects branch, address, and store concepts consistently. [EX:ca_2025_2_midterm_q12 p.4]

## LR/SC and retrying an atomic update

When processors modify shared memory, an ordinary load followed by a store cannot by itself detect intervening interference. Giving a read-modify-write sequence an atomic effect requires hardware support.

`lr.d` loads a value and establishes a reservation. `sc.d` performs its conditional store only when the reservation conditions are satisfied, returning status 0 on success and nonzero on failure. The source's representative failure case is an intervening change to the location. A reservation is not itself a lock that blocks other processors' writes, and that one case does not enumerate every possible failure condition. [[page_cache/computer_architecture/lec.03/page-065|CA M003 p.65]]

The first source example is an atomic swap. The `sc.d` operand order below deliberately preserves **the slide's notation**, `status,(address),data`; it is not presented as newly validated assembler input syntax.

```text
again: lr.d x10,(x20)
       sc.d x11,(x20),x23
       bne x11,x0,again
       addi x23,x10,0
```

`x10` contains loaded **data**, while `x11` contains **status**. Failure restarts at `lr.d` rather than pretending the swap completed. For an illustrative successful attempt with memory=7 and `x23=9`, memory becomes 9 and the final copy makes `x23=7`. A failed attempt has not completed that exchange. [[page_cache/computer_architecture/lec.03/page-066|CA M003 p.66]]

The second lock example on that page is materials-based self-study. It prepares 1, checks that the loaded lock value is 0, and attempts to store 1 conditionally. An already-held lock or a failed SC causes retry; unlocking stores 0. The lecture distinguished its explanation of the first swap from self-study of the second example. [[courses/computer_architecture/transcripts/2026-09-10|September 10 STT, 01:15:16–01:16:49]]

Recalled Q18 asks for a more advanced conditional update using word-sized `lr.w` and `sc.w`. The useful connection here is to distinguish **the data predicate** from **SC success** and to reevaluate the predicate using a newly loaded value after failure. [EX:ca_2025_2_midterm_q18 p.9] Reasoning about a complete counting semaphore requires additional conditions. In particular, the introductory reservation account does not settle the memory-ordering requirements of a practical lock.

## Key Takeaways

- Logical shifts zero-fill and discard bits beyond the fixed width.
- AND selects/clears, OR sets, and XOR toggles.
- If/else needs a skip over the unchosen arm to prevent overwriting results.
- Separate address calculation, loading, testing, updating, and the back edge in loops.
- Signedness determines comparison meaning; LR data and SC status answer different questions.

## Recall and Practice

### Recall and trace

#### Recall Q01 · Fixed-width shifts

Find one-bit logical right and left shifts of 8-bit `11110000`. Explain sign/multiplication limits and the field widths of RV64 immediate shifts.

<details><summary>Show solution</summary>

Right gives `01111000` (120); left discards the high bit and gives `11100000` (224). Zero filling does not preserve a negative signed value, and a fixed-width left shift cannot retain the unbounded product 240×2=480. RV64 uses `funct6(6)|shamt(6)|rs1(5)|funct3(3)|rd(5)|opcode(7)`, totaling 32; six shamt bits express 0…63. This divides the I-format immediate area.

**Checking points:** Check both patterns, fixed width, zero filling, and the 32-bit field total.

</details>

#### Recall Q02 · Masks and toggling

Compute AND/OR/XOR for `a=1010`, mask=`1100`, explaining each mask's role. Also compute AND/OR for `0x0DC0` and `0x3C00`, explain `xori rd,rs1,-1`, and note the C/Java notation caveat.

<details><summary>Show solution</summary>

Results are `1000`, `1110`, and `0110`. AND preserves positions selected by mask ones, OR sets them, and XOR toggles them, including turning existing ones off. Hex results are `0x0C00` and `0x3DC0`. Sign-extended −1 is all ones, so `xori` inverts every bit. `& | ^ ~` are bitwise operators; the material's Java logical right shift is `>>>`, and C `>>` cannot be equated with `srli` without type conditions.

**Checking points:** Check all results, toggle versus set, and why immediate −1 works.

</details>

#### Recall Q03 · Both if/else paths

In the taught translation of `if(i==j) f=g+h; else f=g-h;`, let `g=9,h=4`. Trace equal and unequal cases and explain deleting `beq x0,x0,Exit` after the addition.

<details><summary>Show solution</summary>

With equality, the first `bne` falls through, computes 13, then skips subtraction using the unconditional branch. With inequality it jumps to `Else` and computes 5. Removing the skip makes the equal case fall through into subtraction, overwriting 13 with 5. Two reads of `x0` are always equal; the label is a target, not a destination register.

**Checking points:** Explain both correct results and the overwrite on the faulty path.

</details>

#### Recall Q04 · Each array-loop iteration

For 8-byte `save={7,7,9}`, base `0x1000`, `k=7`, and initial `i=0`, trace loaded addresses/values, final `i`, and load count. Is safe termination guaranteed if all valid elements are 7?

<details><summary>Show solution</summary>

`slli` and `add` recompute `base+8i`. Loads at `0x1000`, `0x1008`, and `0x1010` read 7, 7, and 9. The first two matches increment; the third exits via `bne`, leaving `i=2`, with three loads and two increments. Without a bounds check, an all-7 valid array can lead to an out-of-bounds read rather than guaranteed safe termination.

**Checking points:** Separate addresses/data, preserve test/update order, and count the mismatching load.

</details>

#### Recall Q05 · Basic-block boundaries

Why can the loop's `slli; add; ld; bne` be one basic block? Where must it split if another branch targets `ld`, and does a basic block forbid interrupts?

<details><summary>Show solution</summary>

There is no internal branch or entry target; control splits only at the final `bne`. A new target at `ld` creates `slli; add` and `ld; bne` blocks. Compilers/processors can exploit this normal-control-flow structure while preserving semantics. It says nothing about the impossibility of interrupts or exceptions.

**Checking points:** State the end-branch/start-target conditions and the new split point.

</details>

#### Recall Q06 · Signedness and inverted tests

Compare all ones with 1 using `blt` and `bltu` at the same width. Then check operand order and cases `a=b` and `a=-1,b=1` for `if(a>b) a+=1` implemented with `bge x23,x22,Exit`, where `a=x22,b=x23`.

<details><summary>Show solution</summary>

Signed all ones is −1, so `blt` branches; unsigned it is `2^n−1`, so `bltu` does not. `bge x23,x22` tests `b>=a`, skipping when the original condition is false. It skips equality and also `a=-1,b=1` because `1>=−1`, leaving a unchanged. The 32-bit maximum 4,294,967,295 is not the value of an all-ones RV64 register.

**Checking points:** Check both interpretations, equality/negative cases, and operand order.

</details>

#### Recall Q07 · LR data and SC status

Why does ordinary load/store not guarantee an atomic swap? For a successful source-model attempt with memory=7 and new data=9, give memory and the returned old value. What must repeat after nonzero SC status, and what two checks does the second lock perform?

<details><summary>Show solution</summary>

Another processor may change the location between accesses. LR loads data and creates a reservation; SC conditionally stores and returns status. With success status 0, memory becomes 9 and the final copy returns old data 7. Failure status is not data and the swap is incomplete, so restart at LR. The lock separately checks loaded data equals 0 and SC status equals 0; it retries on failure and unlocks by storing 0. The reservation does not block other writes.

**Checking points:** Explain data/status separation, both outcomes, both lock tests, and unlocking.

</details>

### Apply and diagnose

#### Practice P01 · Store a conditional array result

Newly written synthetic practice transfers path/address/store reasoning from [EX:ca_2025_2_midterm_q12 p.4], adding a variable index and arithmetic. Prerequisites are taught shifts, signed branches, and eight-byte addressing. Let signed 64-bit `a=x20,b=x21`, valid index `i=x22`, and eight-byte array base=`x25`, with no overflow. Store `a-b` at `A[i]` if `a>b`, otherwise `a+b`; `x5,x6` are scratch registers. Check `(a,b)=(7,2),(2,2),(-3,1)`.

<details><summary>Show solution</summary>

Compute the address first and branch to Else on the false condition.

```asm
slli x5, x22, 3
add  x5, x25, x5
bge  x21, x20, Else
sub  x6, x20, x21
beq  x0, x0, Store
Else: add x6, x20, x21
Store: sd x6, 0(x5)
```

`b>=a` selects the false arm. Results are difference 5, equality-case sum 4, and negative-case sum −2. Both paths execute one `sd` to `base+8i`, and the first skips Else. Eight-byte storage is an explicit new condition, not an assumption about every `int` in the recollection.

**Checking points:** Check signed comparison, equality, 8i, both result paths, and one store.

</details>

#### Practice P02 · Recheck the predicate after failure

Newly written synthetic practice applies only the data-predicate/SC-status distinction from [EX:ca_2025_2_midterm_q18 p.9]. Its prerequisite is the taught materials-based lock example. First LR reads 0 but SC fails; the next LR reads 1; a later LR reads 0 and its SC succeeds. State ownership and next action at each point. Why is it wrong to take the success path using the first stale zero?

<details><summary>Show solution</summary>

The first zero permits an attempt, but failed SC means no acquisition; restart at LR. Reading 1 indicates a held lock, so that attempt must retry without proceeding to SC. Acquisition occurs in this model only after a later zero and successful status-0 SC storing 1. A stale predicate proves neither current data nor store success. This is not a complete semaphore or a proof of production-lock ordering/fairness.

**Checking points:** Distinguish data=0 from status=0 and return failures to a fresh LR.

</details>

### Review plan

Calculate Q01–Q02 bit by bit, then mark only executed instructions for Q03–Q06. Keep separate columns for data predicates and status in Q07/P02; check both paths, equality, and negative inputs in P01 before [[courses/computer_architecture/units/en/procedures-stack|procedures and the stack]].

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-08-lecture-03|2026-09-08 · lecture notes]]
- [[courses/computer_architecture/lectures/en/2026-09-10-lecture-04|2026-09-10 · lecture notes]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-030|p.30]], [[page_cache/computer_architecture/lec.03/page-031|p.31]], [[page_cache/computer_architecture/lec.03/page-032|p.32]], [[page_cache/computer_architecture/lec.03/page-034|p.34]], [[page_cache/computer_architecture/lec.03/page-035|p.35]], [[page_cache/computer_architecture/lec.03/page-036|p.36]], [[page_cache/computer_architecture/lec.03/page-037|p.37]], [[page_cache/computer_architecture/lec.03/page-038|p.38]], [[page_cache/computer_architecture/lec.03/page-039|p.39]], [[page_cache/computer_architecture/lec.03/page-040|p.40]], [[page_cache/computer_architecture/lec.03/page-064|p.64]], [[page_cache/computer_architecture/lec.03/page-065|p.65]], [[page_cache/computer_architecture/lec.03/page-066|p.66]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 01:05:42 · preview]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 12:50, 16:27, 22:49, 27:52, 01:15:16–01:16:49]]

- September 8 previews logical operations; detailed shifts/control are supported on September 10. The slide's XOR 'set' wording is corrected to toggling using the truth table and inversion example.
- Basic blocks describe normal control flow, not immunity to exceptions/interrupts. The array loop has no bounds check.
- Unlike the explained atomic swap, the second lock is materials-based self-study. The slide's SC operand order is not newly validated assembler syntax.
- A reservation does not block other writes, and all SC failure conditions are not enumerated. The Q18 connection is limited to predicates, status, and retries; full semaphores, memory ordering, and fairness are outside scope.
- The 2025-2 questions are recollections; official wording and answers are unverified. Connections identify reasoning demands, not predictions.

- [[exam_questions/ca_2025_2_midterm_q12|Existing question preview · Q12]]
- [[exam_questions/ca_2025_2_midterm_q18|Existing question preview · Q18]]


---

[[courses/computer_architecture/units/en/instruction-encoding|← Previous: Instruction Encoding and Address Construction]] · [[courses/computer_architecture/units/index|Unit contents]] · [[courses/computer_architecture/units/en/procedures-stack|Next: Procedure Calls, Calling Conventions, and the Stack →]]
