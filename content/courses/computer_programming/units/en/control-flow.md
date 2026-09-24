---
title: "Boolean Conditions, Branching, Loops, and Execution Tracing"
description: "Trace booleans, branches, and loops, including boundaries, running maxima, and delimiters."
course: "computer_programming"
unit_id: "control-flow"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 2 Java Basics 1.pdf", "3 java basics 2.pdf", "Lab02 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-08-lecture-03", "courses/computer_programming/lectures/en/2026-09-10-lecture-04"]
---

Track a condition's value separately from the statements that execute. Use branch/loop boundaries and accumulated state to explain off-by-one errors and skipped evaluations.

## Boolean expressions define execution conditions

Once an [[courses/computer_programming/units/en/types-expressions|expression has a value]], that value can select an execution path. A condition is a boolean expression, `true` or `false`. It is a value that can be stored and combined, not something meaningful only inside `if`.

| `a` | `b` | `a && b` | `a \|\| b` |
| --- | --- | --- | --- |
| `true` | `true` | `true` | `true` |
| `true` | `false` | `false` | `true` |
| `false` | `true` | `false` | `true` |
| `false` | `false` | `false` | `false` |

Negation `!` reverses a boolean. Thus `(!a) && (!b)` is equivalent to `!(a || b)`, and `(!a) || (!b)` is equivalent to `!(a && b)`. The expression `(x > 0 && x > 1) || (x < 0 && x < -1)` on [Computer Programming M006, PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) simplifies to `x > 1 || x < -1`: each stronger comparison already implies the weaker one beside it.

The material's odd-number test `x % 2 == 1` requires a domain qualification. In Java, `-3 % 2` is −1, so that test misses negative odd integers. `x % 2 != 0` covers signed integers. This is a factual supplement to the example at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 55:16]], not a claim that the lecturer originally restricted the input to nonnegative values.

### What short-circuit evaluation skips

Short-circuit evaluation skips the right operand when the result is already determined: `&&` skips it after a false left operand; `||` skips it after a true left operand.

```java
int denominator = 0;
int num = 100;
if (denominator != 0 && num / denominator == 1) {
    // body
}
```

In this example from [M002 PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf), the false left condition prevents division from being attempted. Reversing the operands would attempt division by zero before the guard could help.

`true || complexCondition` skips the right condition but makes the whole condition true, so an enclosing `if` body executes. `false && complexCondition` skips the right condition and makes the whole condition false, so that body does not execute. The lecturer corrects this distinction at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 24:17–27:10]]. Skipping condition evaluation and skipping the body are different events.

## Branches select paths

The flowchart on M006 p.16 is a materials-based analogy: find a related menu item or button, click it, then branch toward completion or retry according to whether it worked. Read the outgoing paths at each condition and whether a failed path returns to the earlier choice. This does not establish that every detail of the figure was explained aloud.

The keyword is lowercase `if`, not `If` or `IF`. A linked `if–else if–else` chain checks from the top and selects the first true branch.

```java
int time = 22;
if (time < 10) {
    System.out.println("Good morning.");
} else if (time < 20) {
    System.out.println("Good day.");
} else {
    System.out.println("Good evening.");
}
```

M006 p.21 uses `time = 22`, which reaches the last branch. As an explanatory change, setting `time = 8` executes only the first branch. Although 8 is also less than 20, the second greeting is not printed. A linked chain differs from several independent `if` statements. The recap at [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 05:12]] connects conditions to the chosen path.

The ternary expression `condition ? expressionTrue : expressionFalse` chooses a value. With the material's `a = 10, b = 20`, `a > b ? "a is greater" : "b is greater"` chooses the second String. However, its false branch actually covers `a <= b`, including equality. An output label is not a substitute for reading the condition. Similarly, the complement of `x < 3` is `x >= 3`, not merely `x > 3`.

### Colon-style switch and fall-through

A `switch` begins execution at the `case` matching one expression's value. The current examples cover `byte`, `short`, `char`, `int`, and String. M006 p.26 uses:

```java
char grade = 'B';
switch (grade) {
    case 'A':
        System.out.println("Your score is 4.");
        break;
    case 'B':
        System.out.println("Your score is 3.");
        break;
    default:
        System.out.println("There is no grade " + grade + ".");
}
```

Execution begins at B and exits through `break`, printing only `Your score is 3.`. Removing both breaks, as on p.27, allows execution to fall through into `default` and also print `There is no grade B.`. Default is both a possible entry point when no case matches and a place execution can reach by fall-through.

Reaching the end of the block also exits the switch normally. The explanation at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:03:51]] should not be expanded into “only break can terminate a switch.” The String switch and `equals`-based if/else on M006 p.28 both compare `"something"` with `"x"` and `"y"` and print `end`. Intentional fall-through is possible, but the lecturer prefers if/else because omitted breaks are easy to miss. This discussion concerns the supplied colon-style switch.

## Loop tests, bodies, and updates

A loop repeats a body while its evolving state permits it. A `while` tests before the body and may execute zero times. A `do-while` tests afterward and executes at least once; its final semicolon is required.

These separate examples from [Lab02 M008, PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) each start with `i = 0`:

```java
int i = 0;
while (i < 5) {
    System.out.print(i++ + ",");
}
```

```java
int i = 0;
do {
    System.out.print(i++ + ",");
} while (i < 5);
```

Both print `0,1,2,3,4,` and finish with `i = 5`. Changing only the starting value to 5 is an explanatory variant: while prints nothing, whereas do-while prints `5,` once and finishes at 6.

The discussion after [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:07:46]] describes a temporary boolean that starts true, but its exact original condition is unclear. A separate pedagogical schematic is:

```text
boolean first = true;
while (first || condition) {
    first = false;
    BODY
}
```

Here `BODY` and `condition` are placeholders, not actual identifiers from executable source. Assume `first` is a fresh variable that BODY does not modify. The first entry skips the condition through short-circuiting; later entries test it. Clearing `first` **before** BODY ensures a continue cannot leave it true and bypass later tests. Break exits without another test. This is not recovered demonstration code.

### for and for-each

A `for(initialization; condition; update)` performs initialization once, then repeats condition → body → update → condition. If `for(int i = 0; i < 5; i++)` prints `i`, it prints 0 through 4; the final update makes `i` equal to 5 and the test fails.

```java
String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};
for (String car : cars) {
    System.out.print(car + " ");
}
System.out.println();
```

For-each supplies each element value to the variable on the left. This example prints each name followed by a space, then ends the line outside the loop. An indexed loop can produce the same output. Ordinary for is useful when an index is needed; for-each reduces counter management when reading values. Equal effects in this example do not make all for loops interchangeable with for-each. See [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 05:12–06:06]] and M008 p.11.

### break, continue, and body boundaries

```java
for (int i = 0; i < 5; i++) {
    if (i == 3) {
        break;
    }
    System.out.println(i);
}
```

M006 p.37 checks for 3 before printing, so break produces only 0, 1, 2. Replacing it with continue skips the remainder of that iteration, producing 0, 1, 2, 4. In this for loop, continue proceeds through `i++` before the next condition; it does not leave execution stuck at 3. The enclosing for is the break target; the if is not a loop.

Braces may be omitted for a single-statement body, but a newline does not add another statement to that body. `while (true) System.out.println("Infinite");` continues printing because the condition stays true and there is no exit. Many internal exits make a loop harder to understand from its header, so clear execution boundaries matter more than brevity.

## Tracing nested loops and accumulated state

A nested loop repeats its inner initialization for every outer iteration. M006 p.39 makes that order visible:

```java
for (int i = 5; i > 0; i--) {
    for (int j = 0; j < i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
```

As `i` takes 5, 4, 3, 2, 1, `j` restarts at zero and prints that many stars. Print stays on the current line; println outside the inner loop ends the row. The result has five rows, descending from five stars to one, totaling 5+4+3+2+1=15. On row two, `i = 4` and `j = 0,1,2,3` produce four stars before the newline. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:20:10]]

### Initializing a running maximum

```java
int[] nums = {23, -43, -25, 14, 36};
int max = Integer.MIN_VALUE;
for (int num : nums) {
    if (num > max) {
        max = num;
    }
}
System.out.println("The max number is " + max);
```

On M006 p.40, `max` retains the largest value seen so far. Starting at −2,147,483,648, it becomes 23 at the first element, stays there for −43, −25, and 14, and becomes 36 at the final element. The output is `The max number is 36`. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:22:46]]

Starting at zero would incorrectly retain a value absent from an entirely negative array. For an empty array, the supplied code performs no update and retains its initial sentinel. These are deductions from the code, not claims that the example defines the maximum of an empty set.

### Fenceposts and the final delimiter

M006 p.41 separates the last element to avoid a trailing comma:

```java
char[] chars = {'c', 'o', 'm', 'p', 'u', 't', 'e', 'r'};
for (int i = 0; i < chars.length - 1; i++) {
    System.out.print(chars[i] + ",");
}
System.out.println(chars[chars.length - 1]);
```

The loop prints each character through e followed by a comma; the final r is printed without one. The result is `c,o,m,p,u,t,e,r` and a newline. `'c'` is a char and `","` is a String, so their combination forms the output String. A Java `char[]` and a String are distinct types. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:25:36]]

With length one, the loop executes zero times and only the final print remains. With length zero, the final access is invalid. The form therefore assumes a nonempty array. Full traversal's `length` and this delimiter-handling bound `length - 1` serve different purposes.

As optional secondary application, the recalled 2025-1 date-calculation item combines division, remainder, conditions, accumulation, and boundary definitions. Before counting months, distinguish elapsed days starting at zero from a day number starting at one; also distinguish completed months from the counted part of the current month. The recalled source restricts inputs to 2001 while also requesting leap-year handling. Since 2001 is not a leap year, that branch is not exercised within its stated domain. Do not silently enlarge the domain or infer exam frequency from the sample. This is recalled material without an official answer key. [EX:cp_2025_1_midterm_q09 p.6]

## Key Takeaways

- Short-circuiting skips a right condition; that alone does not determine whether the if body executes.
- An if chain selects the first true branch; colon-style switch runs from the match until an exit or block end.
- Track tests, bodies, updates, and the destinations of continue/break separately.
- Maximum initialization, per-row counts, final delimiters, and empty inputs impose different boundaries.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Booleans and negative odd values

Give &&/|| for TT,TF,FT,FF and both negation equivalences. Simplify `(x>0&&x>1)||(x<0&&x<-1)` and compare x%2==1 with x%2!=0 at x=−3.

<details><summary>Show solution</summary>

AND yields T,F,F,F and OR T,T,T,F. `(!a)&&(!b)` equals `!(a||b)`; `(!a)||(!b)` equals `!(a&&b)`. The stronger comparisons imply the weaker ones, reducing the expression to `x>1||x<-1`. Since −3%2=−1, ==1 is false and !=0 true. A signed odd test needs nonzero remainder; this qualification does not rewrite the source as originally excluding negatives.

**Checking points:** Cover truth values, equivalences, implication, and signed remainder.

</details>

#### Recall Q02 · Skipped condition versus executed body

Compare `denominator!=0 && 100/denominator==1` with the reversed order at denominator=0. For true||complexCondition and false&&complexCondition, identify right-operand and if-body execution.

<details><summary>Show solution</summary>

The original order sees false on the left, skips division, and yields false. Reversal attempts integer division by zero before a guard. `true` OR skips the right operand but executes the if body; false AND skips both. Record skipped evaluation/side effects separately from the resulting boolean.

**Checking points:** Explain guard ordering and all right-operand/body decisions.

</details>

#### Recall Q03 · First true branch and false domain

For the greeting chain time<10, else if time<20, else, trace 22 and 8. What does `a>b?"a is greater":"b is greater"` select at equality? Explain a retry arrow in a flowchart.

<details><summary>Show solution</summary>

22 selects Good evening.; 8 selects only Good morning. An else-if is tested only after the preceding condition fails, unlike independent if statements. At equality, the ternary selects the second text, but its actual domain is a<=b. Likewise the complement of x<3 is x>=3. A failed flowchart path returning to an earlier choice means retry rather than successful exit. The keyword is lowercase `if`.

**Checking points:** Use actual condition domains and select only the first true branch.

</details>

#### Recall Q04 · Switch after a match

Grade B matches a case printing score3, followed by default printing a no-grade message. Compare a break after B with no break; explain default entry, block-end exit, and the example comparing "something" with x/y.

<details><summary>Show solution</summary>

With break, only `Your score is 3.` prints; without it, `There is no grade B.` follows. Default can be entered on no match or reached by fall-through. Reaching the closing brace also exits, so break is not the only exit. With the String something, neither x nor y matches; both the supplied switch and equals-based if/else print end. These are bounded colon-style examples, not a complete supported-type specification.

**Checking points:** Explain default reached by fall-through as well as no match.

</details>

#### Recall Q05 · Test timing and first execution

With independent initial i, both while(i<5) and do...while(i<5); use body print(i++ + ","). Compare outputs and final i when starting at zero and five.

<details><summary>Show solution</summary>

At zero, both print `0,1,2,3,4,` and finish i=5. At five, while's initial false test leaves i=5 and prints nothing; do-while prints `5,` once and finishes i=6. Postfix supplies the old value and updates storage. A post-test loop executes at least once and requires its final semicolon.

**Checking points:** Distinguish all outputs/final states and the test position.

</details>

#### Recall Q06 · `first` flag and continue

In the teaching's separate schematic while(first||condition), first starts true and BODY does not modify it. Why is resetting first after BODY unsafe with continue? What happens with break?

<details><summary>Show solution</summary>

The first entry short-circuits the condition. With reset after BODY, continue can skip it, leaving first true and bypassing later tests too. Reset before BODY makes subsequent entries test condition. Break exits without another test. This assumes a fresh first variable and is an explanatory schematic, not recovery of the unclear original temp condition.

**Checking points:** Explain reset placement, continue's path, and the source limitation.

</details>

#### Recall Q07 · for and for-each

Explain the order and printed i values of for(int i=0;i<5;i++). Interpret both sides of for(String car:cars), the newline placement, and when an index is needed.

<details><summary>Show solution</summary>

Initialization runs once, followed by test→body→update→test. Values 0…4 print; the final update produces five and the next test fails. The colon's left declares an element type/variable; the right names the array. print(car+" ") leaves a space after each name and println outside ends the row. Index-based for supports position-dependent slot work; for-each simplifies reading values. The forms are not universally interchangeable.

**Checking points:** Check update timing, colon structure, formatting, and purpose.

</details>

#### Recall Q08 · Exit, skip, and body scope

For 0≤i<5, test i==3 before printing and use break or continue. Compare output and next steps. Explain unbraced bodies and while(true) println("Infinite").

<details><summary>Show solution</summary>

Break prints 0,1,2 and exits the loop. Continue prints 0,1,2,4: at three it skips the remaining body, runs the for update to four, and retests. The inner if is not the loop targeted by break. Without braces, only one statement belongs to the body; newlines do not extend it. A true loop with no exit prints Infinite indefinitely.

**Checking points:** Include the post-continue update and identify body boundaries.

</details>

#### Recall Q09 · Triangle inner iterations

Outer i descends from five while positive; inner j starts zero and prints * while j<i; println follows the inner loop. Give rows, total stars, and second-row j values.

<details><summary>Show solution</summary>

Rows contain 5,4,3,2,1 stars, totaling 15. The second outer iteration has i=4 and j=0,1,2,3, so four prints occur. Inner initialization repeats per outer iteration; one newline after the inner loop forms each row. Moving println changes the shape even if counts agree.

**Checking points:** Explain reset and newline placement, not just the sum.

</details>

#### Recall Q10 · Running maximum initialization

Trace nums={23,−43,−25,14,36}, starting max=Integer.MIN_VALUE and updating on num>max. Explain zero initialization and empty input.

<details><summary>Show solution</summary>

The value moves from −2147483648 to 23, stays 23 for −43/−25/14, then becomes 36. It represents the maximum visited value. Starting zero fails for all-negative data by retaining an absent zero. Empty input performs no update and leaves the sentinel; the code does not define a maximum of an empty set.

**Checking points:** Explain each update and distinguish all-negative from empty-input issues.

</details>

#### Recall Q11 · The final delimiter

The computer char[] loop prints chars[i]+"," while i<length−1, then println prints the final char. Explain output, lengths one/zero, and char versus String.

<details><summary>Show solution</summary>

Output is `c,o,m,p,u,t,e,r` plus newline. Commas follow through e; separating r avoids a trailing comma. 'c' is char and "," a String, making concatenation a String; char[] itself is not String. At length one, the loop skips and the only char prints. At zero, final index −1 is invalid, so the form assumes nonempty input.

**Checking points:** Explain delimiter placement and both boundary cases.

</details>

### Apply the ideas

#### Practice P01 · Elapsed quantity versus position

**Newly written synthetic exam-style practice.** Transfer domain, completed/current-part, and zero-based elapsed reasoning from [EX:cp_2025_1_midterm_q09 p.6]. Prerequisites are arrays, conditions, and loops, not date/leap-year implementation. The recalled source combines a 2001 domain with leap-year requirements and provides no official key.

Three consecutive segments have lengths {4,6,3}. For segment index s and zero-based within-segment position p, use elapsed=p and add lengths[i] for 0≤i<s. Find elapsed and one-based overall positions for (0,0),(1,0),(1,5). What error would i<=s cause, and what is the valid p range?

<details><summary>Show solution</summary>

Elapsed values are 0,4,9; one-based overall positions are 1,5,10. At s=1, add only the completed first segment's four units and count p within the current one. Using i<=s incorrectly adds the whole current segment too: (1,0) becomes ten instead of four. Valid inputs satisfy 0≤s<3 and 0≤p<lengths[s]. Adding one to obtain an ordinal position differs from adding an uncompleted segment.

**Checking points:** Provide all results, completed/current distinction, a counterexample, and input bounds.

</details>

#### Practice P02 · Review output boundaries

**Newly written lecture-based general practice; no direct indexed style match.** A nonempty char[] formatter loops with i<=chars.length−1, appending a comma each time, then prints the last element again. What fails at length one? Give the teaching's bound and where empty handling belongs.

<details><summary>Show solution</summary>

For the single char a, the loop prints `a,` and the final print repeats a, giving `a,a`. Use i<chars.length−1 so the loop excludes the final element, then print it once. Handle empty input in a separate path before the final indexed access; correcting the loop bound alone does not remove index −1 at length zero.

**Checking points:** Diagnose duplicate output and empty access as separate issues.

</details>

### Review plan

For Q01–Q04, separate truth values from executed statements; draw loop paths for Q05–Q08. Check Q09–Q11 boundaries, compare zero-/one-based counting in P01, and fix both bounds in P02.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 55:16, 27:10, 24:17, 01:03:51, 01:07:46, 01:20:10, 01:22:46, 01:25:36.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 corrected transcript]] — 05:12.

### Materials and page views

- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-069), [p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-070).
- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-018), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-021), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-023), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-028), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-031), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-033), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-041).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-012).

The original temporary condition at September 8, 01:07:46 is unclear. The first-flag schematic is explanatory, not recovered code. Negative-odd and empty-input cases are deductions from code. Switch discussion is limited to colon-style.

Exam connection: P01 transfers only domain, elapsed-quantity, and boundary reasoning from [EX:cp_2025_1_midterm_q09 p.6]. That recalled source restricts dates to 2001 while requesting leap-year handling; that year does not exercise the leap branch. No official answer key is supplied, and no full private prompt or new preview is reproduced.


---

[[courses/computer_programming/units/en/arrays|← Previous: Array Creation, References, and Multidimensional Data]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/methods|Next: Method Contracts, Calls, Returns, and Reuse →]]
