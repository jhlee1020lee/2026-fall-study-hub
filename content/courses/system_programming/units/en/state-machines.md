---
title: "Character Processing, DFAs, and Decommenter Boundaries"
description: "Review character-processing boundaries through DFA transitions and three test observables."
course: "system_programming"
unit_id: "state-machines"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab-1-decommenter.pdf"]
private_source_assets: ["lab-1-decommenter.pdf"]
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-07-lecture-02", "courses/system_programming/lectures/en/2026-09-09-lecture-03"]
---

Represent what must be remembered after each character as state. Separate word boundaries, comments, literals and EOF to check output and error contracts.

## Character streams: distinguishing bytes from EOF

A character-at-a-time program can process a large input without storing it all. It needs the current character and only the state required for the next decision. Building on [[courses/system_programming/units/en/systems-c-build|expressions and loops]] and [[courses/system_programming/units/en/objects-pointers|C types and strings]], separate input values, termination, and remembered context.

In ASCII, `'0'`–`'9'` have codes 48–57, `'A'`–`'Z'` 65–90, and `'a'`–`'z'` 97–122. Printing the source expressions `97`, `'a'+3`, and `122` as characters gives `a d z`. `'C'+'a'-'A'` gives `c`; `'c'-('a'-'A')` gives `C`. These calculations depend on ASCII layout. Character literals express intent better than numbers such as 97, but manually testing contiguous alphabetic ranges still embeds character-set assumptions. [C examples slides 3–10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

`isalpha`, `isdigit`, and `isspace` use library classification rules, which can also depend on locale. Store `getchar`'s result in an `int` to preserve valid character values and the separate `EOF` state. Narrowing to `char` first can lose that distinction. EOF is not an ordinary byte in the input; the slide's -1 illustration is not its only possible definition.

```c
int c;
int alphaCount = 0, digitCount = 0, othersCount = 0;

while ((c = getchar()) != EOF) {
    if (isalpha(c))
        alphaCount++;
    else if (isdigit(c))
        digitCount++;
    else
        othersCount++;
}
```

This is the classification portion of the source example, using `<stdio.h>` and `<ctype.h>`. Exactly one branch increments for each character. When passing an ordinary `char` variable to a `ctype` function, also respect the requirement that the argument be representable as `unsigned char` or equal EOF. This loop retains `getchar`'s result and excludes EOF before classification.

The displayed results of 253 alphabetic, 4 digit, and 289 other characters belong to the supplied `count.c` input. They are not fixed outputs for an edited source file or arbitrary input.

## Word counting through state transitions

Counting words requires remembering whether the preceding input was already inside a word. Here, a word means a consecutive run of non-whitespace characters, not a dictionary entry. The [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 14:04]] explicitly defines this and uses `isspace` to include spaces, tabs, and newlines.

The initial state is OUT. Actions in this table occur when reading the current character.

| Current state | Input | Next state | Action |
|---|---|---|---|
| OUT | Whitespace | OUT | None |
| OUT | Non-whitespace | IN | Increment word count |
| IN | Non-whitespace | IN | None |
| IN | Whitespace | OUT | None |

`I am a boy` crosses OUT→IN four times, so it contains four words under this definition. For two spaces, `ab`, a tab, a newline, `c`, and EOF, the initial spaces preserve OUT. The `a` starts the first word; `b` preserves IN. The tab returns to OUT, the newline preserves it, and `c` starts the second word. The result is two. No increment is needed at EOF, even without trailing whitespace, because the last word was counted at its start.

State records precisely the distinction that a whitespace counter lacks. Several consecutive whitespace characters do not create extra words. [C examples slides 11–12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## Representing necessary memory with a DFA

A DFA, Deterministic Finite State Automata in the lecture terminology, has finitely many states and input-labeled transitions. Teaching diagrams can attach actions to transitions. An incoming arrow marks the initial state; a double circle marks an accepting state. The word counter retains IN/OUT rather than the entire input history because that is enough for its next decision.

### Recognizing prefixes in SNUCSE and integers

On C examples slide 13, reading `S,N,U,C,S,E` follows `S→1→2→3→4→5→F`, where the first S is the initial state. The numbered states track progress through a prefix. A mismatch need not discard all progress: from state 5, an input `N` returns to state 2, preserving an overlapping prefix. The slide additionally states that `S` from states 1, 2, 3, and 5 goes to state 1. Not every failure transition is drawn.

The integer language on the same page is `0` or `[+-]?[1-9][0-9]*`. Notice the separate accepting path for zero and the repeated-digit path after a nonzero first digit. Treating the whole input as one integer, `0` is accepted, `+0` rejected, and `+12` accepted. The last input consumes a sign, reaches an accepting state on `1`, and loops there on `2`. Here `?` means zero or one occurrence of the preceding item. It differs from the “one arbitrary character” operator in [[courses/system_programming/units/en/dirtree|Dirtree patterns]]. [C examples slide 13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

### Named constants and invariants

IN and OUT communicate meaning better than unexplained 0 and 1 values. One source formulation is:

```c
enum DFAState { IN, OUT };
```

The enumerators are integer constants, here 0 and 1. `#define IN 0` performs preprocessing token replacement, whereas `const int IN = 0;` declares an object whose modification is restricted. Equal numerical values do not make these mechanisms interchangeable in every C99 context. In particular, the `const int` and `case`-label discussion at [[courses/system_programming/transcripts/2026-09-07|31:14–33:09 on September 7]] was left unresolved in class. C99's integer-constant-expression requirements must be distinguished from an object declaration.

The source's `default: assert(0);` detects a violation of the internal invariant that the state is IN or OUT. An assertion helps reveal an internal error; it is not a replacement for every external-input error contract in every build. Likewise, a function comment should describe “count words from stdin and print the count” from the caller's perspective rather than narrate each character-processing instruction. [C examples slides 14–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## Decommenting: a character's meaning depends on context

A decommenter transforms C source by removing comments. Merely finding `/` and `*` is insufficient: removing `/*` inside a string would change program data. The necessary state comes from the context in which a character is read. The [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 01:09:39]] introduces this transformation.

Input arrives on `stdin`, transformed source goes to `stdout`, and diagnostics go to `stderr`. With generic filenames, Lab 1 PDF page 3's redirection example is:

```sh
./decomment < input.c > output 2> errors
```

The shell connects `input.c` to stdin, descriptor 0; `output` to stdout, descriptor 1; and `errors` to stderr, descriptor 2. The program does not need a separate filename parser to implement these connections. A diagnostic written to stdout contaminates the transformed source, so the destination stream is part of correctness.

### Replacing comments with a space while preserving newlines

Lab 1 requires both `/* ... */` and `// ...` comments to become one space, while original newlines remain. Thus `abc/*def*/ghi` becomes `abc ghi`. Deleting the comment without a replacement could create the different token `abcghi`. Preserving newlines inside a block comment keeps the physical line numbers of later code.

Block comments do not nest. In `abc/*def/*ghi*/jkl*/mno`, the first `/*` opens the comment and the next `*/` closes it, giving `abc jkl*/mno`. Treating the remaining `*/` as another comment terminator would change the contract.

Each input line below is assumed to end with a real newline.

| Input | Output |
|---|---|
| `abc/*def*/ghi` | `abc ghi` |
| `abc//def` | `abc ` followed by the original newline |
| `abc"def/*ghi*/jkl"mno` | Unchanged |

In the PDF pages 4–7 tables, subscript `s` and `n` are visual markers for space and newline, not literal characters to emit.

### Quotes and escapes preserve literal context

Inside a string or character literal, comment markers remain ordinary content. Treat a backslash and its following character together so that an escaped quote is not mistaken for the end of the literal. PDF page 8 includes this input:

```text
abc"def\"ghi"jkl
```

The quote in `\"` does not close the string. Preserve both characters; the later unescaped quote ends it. The analogous distinction applies to `\'` inside a character literal.

Combining those source rules gives the explanatory example `abc"def\"/*ghi*/jkl"mno`, which also remains unchanged, including its final newline. After the escaped quote, the input is still inside the string, so `/*ghi*/` is content. This combined example is a pedagogical application of the rules, not a claimed classroom execution.

## Distinguishing states at EOF

EOF does not have the same consequence in every state. Lab 1 PDF pages 9–12 require no warnings or errors for a newline within a literal or for an unterminated string or character literal. This assignment is not a complete C compiler syntax checker. Nor should the slide's discussion of multicharacter character constants be generalized into a universal C syntax prohibition.

An unclosed block comment at EOF is different. Report the line where it **started**, then terminate with `EXIT_FAILURE`. In page 11's example, a comment starts on line two, so stderr contains this line followed by a newline:

```text
Error: line 2: unterminated comment
```

Other cases terminate with `EXIT_SUCCESS`. Tracking only the current line can lose the opening location; current position and the start of an open comment are distinct pieces of state.

Input lines may be arbitrarily long. A small fixed line buffer cannot be assumed sufficient. The specification assumes that the last line ends with a newline and that backslash-newline sequences do not occur. Physical and logical lines consequently coincide within this assignment's scope, not throughout general C preprocessing.

## Verifying a transformation at state boundaries

Designing a state-transition diagram first separates the information needed at comment openings and endings, quotes, escapes, newlines, and EOF. Lab 1 proceeds from the diagram to source changes, a `make` build, and comparison with the reference.

Feed the same input to both implementations and compare stdout and stderr separately. The `diff` explanation at [[courses/system_programming/transcripts/2026-09-09|September 9, 01:20:03]] concerns file contents; it does not automatically verify exit status. For an unterminated comment, correctness includes the transformed output, the diagnostic's stderr destination, the opening line, and failure termination. The six supplied tests are starting examples, not evidence that all boundaries are covered.

Clear names, caller-oriented function comments, small functions, and the seventy-two-character line guideline help maintain these distinctions. The dated submission structure preserves the provided Makefile, real compilation history, a single `decomment.c`, and an extensionless `readme` so that the build and work history remain reproducible. The exact diagram submission location cannot be established from the supplied directory list alone. The same separation of syntax, selection, and output contracts supports [[courses/system_programming/units/en/dirtree|directory traversal and pattern processing]].

## Key Takeaways

- State preserves how the consumed prefix affects the next character.
- Counting word entry avoids double counting at EOF.
- Comment removal must preserve tokens, newlines and literals together.
- Stream separation also matters in [[courses/system_programming/units/en/io-streams|I/O and buffering]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Characters and EOF

In ASCII, what do 97, `'a'+3` and 122 represent, and how does case conversion use the letter gap? Why use int for getchar, and what are the ctype constraints?

<details><summary>Show solution</summary>

97 is a, a+3 is d and 122 is z. Adding the a−A code gap to C yields c; subtracting it from c yields C. Use int for `getchar` to distinguish every byte from EOF. Increment only one alphabet/digit/other category per character. Ctype arguments must be EOF or unsigned-char-representable values, with locale effects. Counts 253/4/289 belong to a particular input.

**Check:** Check a/d/z, case gap, EOF preservation and single classification.

</details>

#### Recall Q02 · Word boundaries

Trace OUT/IN for two spaces, ab, tab, newline, c and EOF; mark exactly when the count increases.

<details><summary>Show solution</summary>

Start OUT; both spaces preserve it. a causes OUT→IN and count=1; b stays IN. Tab returns OUT, newline stays OUT, c causes the second OUT→IN and count=2. EOF adds nothing. Counting entry into a non-whitespace run handles a final word without trailing whitespace.

**Check:** Identify both counted transitions and explain why EOF adds nothing.

</details>

#### Recall Q03 · DFAs and state names

Trace SNUCSE and overlapping prefixes, classify 0, +0, +12 in the integer DFA, and explain state notation, macro/const/enum and assert.

<details><summary>Show solution</summary>

An incoming arrow marks initial state; a double circle marks acceptance. SNUCSE follows S→1→2→3→4→5→F. N from state5 returns to state2 (prefix SN), while S from states1/2/3/5 returns to 1; failure transitions are not all drawn. `0|[+-]?[1-9][0-9]*` accepts 0/+12 and rejects +0; ? here means optional. `#define IN 0` replaces tokens; `const int` is an object; `enum {IN,OUT}` gives integer constants 0/1, with different C99 constraints. Names/caller-oriented comments expose intent. A default assert detects an invalid-state invariant, not every external error in every build.

**Check:** Check overlap, integer acceptance, all three naming forms and assert limits.

</details>

#### Recall Q04 · Preserving comments and literals

Explain the three streams in `./decomment < input.c > output 2> errors`. Handle token separation, an apparent nested comment and quoted text with escaped quotes.

<details><summary>Show solution</summary>

stdin(0) reads input.c; stdout(1) writes output; stderr(2) writes errors. Replace a comment with one space, producing `abc def`, and preserve internal newlines. Block comments do not nest: `abc/*def/*ghi*/jkl*/mno` yields `abc jkl*/mno`. Line comments have their own boundary. Inputs `abc"def\"ghi"jkl` plus newline and `abc"def\"/*ghi*/jkl"mno` plus newline are each unchanged: backslash, escaped quote and comment-looking literal text remain. Both give empty stderr and success. Character literals likewise need quote/escape state.

**Check:** Check token separation, newlines, non-nesting, both preserved literals and streams.

</details>

#### Recall Q05 · EOF contracts

A block comment opens on line2 and reaches EOF. What diagnostic and status follow? Are unterminated string/character literals or newlines inside literals the same error?

<details><summary>Show solution</summary>

Write exactly `Error: line 2: unterminated comment` plus newline to stderr and return `EXIT_FAILURE`. Remember the opening line, not the last line. This assignment gives no separate warning for unfinished string/character literals or literal newlines and succeeds absent a block-comment error. Preserve arbitrary-length input and the stated final-newline/no-backslash-newline assumptions; this is not a full C syntax checker.

**Check:** Check exact diagnostic, opening line, status and non-error cases.

</details>

#### Recall Q06 · Three observable test results

Explain design-to-reference testing. Is matching stdout sufficient, and how should the supplied Makefile/history and six examples be treated?

<details><summary>Show solution</summary>

Design states/transitions, implement, build with make, then compare stdout, stderr and exit status separately on identical inputs. Matching stdout can hide wrong diagnostics/status. Six examples begin boundary testing rather than proving all inputs. Use focused functions, names/comments and the 72-column guidance; preserve supplied Makefile/history. The decomment.c/readme requirements are dated guidance; diagram submission remains unclear. No actual reference-run success is claimed here.

**Check:** Check all three observables, boundary tests and source limits.

</details>

### Practice

#### Practice P01 · Tests that distinguish failures

**Lecture-based general practice.** Three designs are faulty: A deletes comments without replacement; B treats /* inside literals as comments; C reports every unfinished state at EOF as an error. Give distinguishing inputs and expected stdout/stderr/status.

New general practice based on the lecture and Lab1 requirements. The complete candidate index has no direct word-DFA/decommenter literal/newline/EOF contract question. A different wildcard grammar supplies no claimed exam style. Prerequisites: Q02/Q04–Q06.

<details><summary>Show solution</summary>

For A use `a/*x*/b` plus newline: stdout `a b` plus newline, empty stderr, success. For B use `"/*x*/"` plus newline: unchanged stdout, empty stderr, success. For C use unfinished `"abc` plus newline then EOF: preserve the literal text, empty stderr, success. Contrast an actual unfinished block comment `a\n/*x\n`: stdout `a\n \n`, stderr `Error: line 2: unterminated comment` plus newline, failure. These distinguish token, literal and EOF classification.

**Check:** Supply all three observables per input and identify the bug exposed.

</details>

### Review plan

Draw Q02/Q03 state paths first. Answer Q04/Q05 in stdout/stderr/status columns, then design distinct boundary tests in P01.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 lecture notes]]

### Materials and lecture passages

- [C examples slides 3–10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 11–12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slide 13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 14–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 14:04]]
- [[courses/system_programming/transcripts/2026-09-07|31:14–33:09 on September 7]]
- [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 01:09:39]]
- [[courses/system_programming/transcripts/2026-09-09|September 9, 01:20:03]]
- Lab 1 decommenter handout: supplied PDF, with no catalogued public URL; its stream and EOF requirements support this review.

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

- [00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### Scope to retain

- The September2 entry includes associated materials; later explanations are not retroactively attributed to that lecture.
- The integer DFA uses ? as optional, unlike Dirtree. Omitted transitions and uncertain speech are not invented.
- Submission/environment guidance is dated; diagram submission remains unclear. Six examples establish neither exhaustive coverage nor actual run success.
- No directly corresponding indexed exam evidence exists; P01 is general practice.


---

[[courses/system_programming/units/en/objects-pointers|← Previous: C Objects, Types, Addresses, and Pointers]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/files-metadata|Next: Unix Files, Directories, Inodes, and Metadata →]]
