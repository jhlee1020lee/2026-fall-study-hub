---
title: "Dirtree Traversal, Filtering, Output Contracts, and Design"
description: "Check Dirtree's traversal, fixed output fields, statistics, and pattern grammar."
course: "system_programming"
unit_id: "dirtree"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lab 2 input and output.pptx", "assign2_README.md", "lab 2 input and output_2b90a395.pptx"]
private_source_assets: ["assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Read the Dirtree specification as three decisions: visit, display, and count. Check the contract on small trees because depth and filtering change the included set independently.

## Traversing a directory tree under an output contract

Dirtree recursively examines directory entries and prints metadata and statistics. Beyond listing names, it must distinguish **what to visit**, **what to display**, and **what to count**. File metadata, [permissions](permissions.md), and [pointer/storage lifetimes](objects-pointers.md) support these decisions. The later part of the [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 Dirtree lecture]] introduces the contract.

Without root arguments, the root is `.`. The private official README M018 adds a materials-only maximum of 64 roots. `-d <depth>` limits depth, `-f <pattern>` filters names, and `-h` requests help; depth and filtering can be used independently or together. Within each directory, omit `.` and `..`, put directories first, and sort alphabetically within the categories. The source supplies a `dirent_compare` helper. Each root receives a header, entry tree, and summary; multiple roots additionally receive a final aggregate.

This discussion interprets the specification and general design principles rather than providing a complete traversal or current-assignment solution. It does not create public links to the private README or reference binary.

### Fixed fields are a byte-level contract

Read M017 slides 6–8 together with M018's detailed format. Each depth level contributes two indentation spaces, included within the path/name field.

| Field | Width, alignment, and limit |
|---|---|
| Path/name | 54, left-aligned; replace the end with `...` when exceeded |
| User | First 8 bytes, right-aligned |
| Group | First 8 bytes, left-aligned |
| Size | 10, right-aligned |
| Disk blocks | 8, right-aligned |
| Type | 1 |
| Summary text | 68, left-aligned, ellipsis when exceeded |
| Summary total size / blocks | 14 / 9, right-aligned |

The source's complete format, including separators, is a 100-character line. A path/name field exactly 54 units long is not truncated; truncation applies only when it exceeds the limit. UTF-8 byte counts and displayed glyph widths differ, and the source does not establish a complete display-column algorithm. Numeric field overflow is excluded from grading, but totals can exceed `int`, requiring an adequate integer type. Distinguish path-overflow questions from the FAQ's `MAX_PATH_LEN` guidance.

Type markers are blank for regular files, `d` for directories, `l` for symbolic links, `f` for FIFOs, and `s` for sockets. The assignment classifies character and block devices as regular. Its FIFO marker is `f`, not the `p` used by Unix `ls`; output spelling belongs to this program's contract.

## Statistics describe the selected entry set

Do not count the root itself as an entry. Sum selected entries' type counts, byte sizes, and allocated disk blocks. A count of one uses a singular noun; zero and counts of two or more use plurals. Blocks are metadata in 512-byte allocation units, not simply the file size rounded up.

The two-root example on [system_programming:M017 slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) gives:

| Root/result | Type counts | Bytes | Blocks |
|---|---|---:|---:|
| `subdir2` | 2 files, 2 links | 3086 | 16 |
| `subdir3` | 2 files, 1 pipe, 1 socket | 500 | 16 |
| Aggregate | 4 files, 0 directories, 2 links, 1 pipe, 1 socket | 3586 | 32 |

There are `4+0+2+1+1=8` entries, without adding two for the roots. In the original table, compare the per-root footers with the final aggregate to see the accounting boundary. The separate source example `9192+14=9206` bytes/16 blocks and long-name example `256+8192+1000=9448` bytes/24 blocks use different fixtures. Another README demo has 4 files, 3 directories, 2 links, 1 pipe, and 1 socket, totaling 21497 bytes/56 blocks; an expanded tree has 9 files and 25325 bytes/96 blocks. These are not one combined execution.

## Depth and filtering govern different decisions

The root has depth zero and direct children depth one. `-d` sets the maximum included entry depth: valid values are 1–20, with default 20. Entries beyond it contribute neither traversal, display, nor statistics. M017's chain illustrates the consequence:

| Scope | Included objects | Statistics |
|---|---|---|
| `-d 1` | `b` | 1 directory, 4096 bytes, 8 blocks |
| `-d 2` | `b`, `c`, file `f` | 2 directories, 1 file, 8192 bytes, 16 blocks |
| `-d 3` | Previous objects plus `d` | 3 directories, 1 file, 12288 bytes, 24 blocks |
| Complete source example | `b,c,d,e` and two files | 16384 bytes, 32 blocks |

Starting the root at one incorrectly excludes a level. Use the specification's root-zero convention rather than resolving the confused numerical wording at 01:11:03 in the [[courses/system_programming/transcripts/2026-09-23|2026-09-23 transcript]]. The source's `# depth N` annotations explain the example and are not required output.

### A nonmatching ancestor may still need traversal

Filtering is case-sensitive contiguous-substring matching on the basename. Pattern `b` matches within `abc`, but `/home/ta/abc/def` has basename `def`; a matching parent component does not make that basename match. The root is not filtered.

A matching entry receives detailed metadata and contributes to statistics. A nonmatching directory is still visited within the depth limit to find matching descendants. If it has such descendants, display its name only, without metadata or statistical contribution. If no descendant matches, omit that nonmatching subtree. Thus “does not match” is not equivalent to “stop traversing.” The transcript around 01:13 through just before 01:14:44 explains the distinction.

M018's Implementation section contains a conflicting bullet saying not to traverse a nonmatching directory. Here the rule supported by the lecture, M017 slide 18, the README's formal matching rule, and its detailed examples is continued traversal. This source conflict is not presented as newly resolved instructor guidance.

The detailed results on slides 20–21 were skipped in the lecture and are materials-only examples. `a?c` retains files `aXc`, `abc`, and `axc`, totaling three bytes/24 blocks, with `subdir1` shown by name only. The `(ab)*c` example includes `c` and a substring inside `xababcx`, totaling six files/six bytes/48 blocks. `b(ab)*c` excludes `c`, giving five/five/40. M017's excluded name `zxc` and the README's `aZZc` belong to different fixtures.

## Pattern units and grammar boundaries

In this assignment, `?` means exactly one arbitrary character, `*` repeats the immediately preceding character or group zero or more times, and parentheses form a group. Do not import shell-glob or unrelated regex semantics.

| Pattern | Example matching structures |
|---|---|
| `a?c` | `abc`, `axc` |
| `ab*` | `a`, `ab`, `abb`, … |
| `(ab)*c` | `c`, `abc`, `ababc`, … |
| `a(bc)*d` | `ad`, `abcd`, `abcbcd`, … |
| `ab?(de)*f` | `abcf`, `abXf`, `abXdef`, `abXdedef` |

`a(bc)*d` accepts `ad` because the group can repeat zero times. For M018's `abc?d*(ef)`, `abcdef` can match with `?` consuming one `d` and `d*` repeating zero times; `abcXddef` and `abcXef` also fit. Partial matching does not require consuming the entire basename.

Quote a command-line pattern so the shell does not process its metacharacters first. The maximum pattern length is 64 including the terminating NUL. Matching `?`, `*`, `(`, or `)` as literal filename characters is outside the grading domain. The optional-element meaning of `?` in another regex language does not apply here.

### Invalid syntax versus excluded complexity

Invalid examples include an empty pattern, empty group `a()b`, leading `*abc`, consecutive `a**b`, prematurely closing `a)bc(`, and unclosed `(abc`. A star must follow a valid character or group. Thus `a*b` is not an invalid example under this rule; unclear pattern speech at 01:15:40 is not evidence to the contrary.

A star within a group, such as `a(b*c)d`, and nested groups are separately described as complexity excluded from grading. Do not merge that category into the required invalid-syntax list. An explicitly invalid pattern produces only `Invalid pattern syntax` on stderr and exits without listing or statistics. M018 excludes permission failures, nonexistent paths, concurrent rename/removal, and allocation failures from grading, but that does not make them irrelevant in ordinary programs. The precise scoring relationship between M017's “Error and overflow handling 5” rubric and the invalid-only clause remains unresolved.

### Searching start positions versus matching from one position

M017 slide 25 provides partial pseudocode for a star-only version. Outer `match` tries successive basename start positions; inner `submatch` decides whether the pattern continues from one position. In the original, notice the zero-repetition attempt and the unimplemented one-or-more branch below it. Repeated consumption, `?`, grouping, empty suffixes, and complete termination/backtracking conditions are not supplied. The hint is not a finished matcher.

[EX:sp_2025_2_midterm_q02 p.5] asks for related reasoning that separates start-position search from recursive matching at one position. However, its `*` is a wildcard for zero or more arbitrary characters; Dirtree's star repeats the **preceding item**. The exam also assumes initially nonempty input strings and patterns. What transfers is the method of identifying suffix meaning, zero-length choices, progress, and termination separately. Neither the private skeleton's blanks nor the current assignment's missing branches are completed here.

## Storage responsibilities and development tools

Separate coordination of roots, options, headers, summaries, and aggregates from directory collection, sorting, filtering, printing, recursion, and closing. Formatting, summary construction, entry handling, and pattern validation have distinct contracts. This follows M018's materials-only advice to design the flow before examining the skeleton.

The number of entries in a directory has no stated upper bound. Depth twenty does not limit width, and a large local array in a recursive function consumes stack space at every active level. A supposedly large-enough fixed array therefore does not handle all permitted inputs. Account for width, depth, allocated storage, and release times together. These are design constraints; the complete storage-growth algorithm remains an implementation task.

The handout distinguishes `README`, `Makefile`, `src/dirtree.c`, reference, tools, and documentation. `make` builds and `make clean` removes build results; the directory structure must agree with the Makefile. `compare.sh` compares output against the reference, `gentree.sh` creates fixtures from `*.tree` descriptions, and `mksock` creates socket entries. The instructions say not to modify `mksock`. The FAQ's pipe/socket regeneration conflicts concern existing fixtures, not commands executed here.

API roles also remain separate: `strcmp` compares; `strncpy` performs bounded copying; `strdup` creates a separately owned copy requiring `free`; `snprintf` formats within a bound; `opendir/readdir/closedir` traverse; `stat/lstat` obtain metadata; `getpwuid/getgrgid` find names; and `qsort` sorts. `strncpy` does not always terminate with NUL, and `snprintf` can truncate. `qsort` replaces neither collection nor filtering nor statistics, and its name does not guarantee a particular quicksort implementation. External regex libraries and `scandir` are prohibited by the specification.

The latest supplied [system_programming:NM002 slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output_2b90a395.pptx) lists `dirtree.c`, extensionless `readme`, `Makefile`, and genuine compilation history in `history/` for submission. M017/M018's two-file lists are older versions. The supplied deadline is October 9 at 21:00; the later file list is not retroactively September 23 speech. Read the example student number only as `YourID`, and do not derive another deadline from the archive-command year discrepancy. The retained teaching in NM002 does not resolve the filter-bullet and error-rubric conflicts.

## Key Takeaways

- Roots have depth zero and are excluded from entry totals.
- A nonmatching directory can still need traversal to find matching descendants within depth.
- Name-only ancestors differ from entries receiving details and statistical contribution.
- `?` consumes one character; `*` repeats the preceding item. Invalid syntax differs from excluded complexity.
- A depth limit does not bound directory width, and each tool serves a separate contract.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Roots, options, and sorting

Explain omitted roots, maximum root count, `-d/-f/-h`, handling of `.`/`..`, ordering, and output for one versus several roots.

<details><summary>Show solution</summary>

Omission selects current directory `.`; the supplied README allows up to 64 roots. The options request depth, filter, and help; depth/filter may combine or stand alone. Ignore special entries, put directories first, and sort alphabetically within categories. Every root gets a header, tree, and summary; multiple roots also get a final aggregate. The 64-root limit is materials-based detail.

**Checking points:** Check the default, all options, sorting, and aggregate condition.

</details>

#### Recall Q02 · Widths and type markers

Give indentation and widths/alignment for path, user, group, size, blocks, type, and summary. Explain exactly 54 path units, FIFO/device markers, byte versus glyph width, and large totals.

<details><summary>Show solution</summary>

Two spaces per depth belong inside the left-aligned 54-unit path field; truncate only if exceeded. User uses the first eight bytes right-aligned, group the first eight left-aligned, size ten right-aligned, blocks eight right-aligned, and type one. Summary text is 68 left-aligned with ellipsis on overflow; totals use 14/9 right-aligned. The full source format including separators is 100. Exactly 54 is not truncated. Markers are blank/d/l/f/s; character/block devices count as regular for this assignment. UTF-8 bytes differ from glyph columns, and grading exclusions for numeric width do not eliminate totals exceeding int.

**Checking points:** Check every width/alignment, the exact boundary, and FIFO f.

</details>

#### Recall Q03 · Statistical scope and aggregation

Two roots yield 2 files/2 links, 3086 bytes/16 blocks and 2 files/1 pipe/1 socket,500 bytes/16 blocks. Find the aggregate, entry count, and singular/plural labels. Also sum the separate fixtures 9192+14 and 256+8192+1000 and explain blocks versus byte size.

<details><summary>Show solution</summary>

The aggregate is 4 files, 0 directories, 2 links, 1 pipe, 1 socket: eight entries, 3586 bytes, 32 blocks. Do not add roots. Only one is singular; zero and two or more are plural. The separate sums are 9206 and 9448 bytes; their source block counts 16/24 are metadata. Blocks use 512-byte allocation units and are not computed by simply rounding file length. README totals 21497/56 and expanded 25325/96 belong to different fixtures.

**Checking points:** Check 8/3586/32, root exclusion, both separate sums, and block meaning.

</details>

#### Recall Q04 · Depth boundaries

Give root/child depths, valid `-d` range/default, and included objects/statistics in the source chain at depths 1/2/3. What happens beyond the limit?

<details><summary>Show solution</summary>

Root depth is zero, direct children one; valid values are 1–20, default 20. Depth 1 includes b: one directory/4096/8; depth 2 includes b, c, f: two directories and one file/8192/16; depth 3 adds d: three directories and one file/12288/24. The full example has b, c, d, e and two files, 16384/32. Beyond-limit entries are neither visited, printed, nor counted. `# depth N` is explanatory, not output.

**Checking points:** Check the depth origin and all three included sets/totals.

</details>

#### Recall Q05 · Nonmatching ancestors

Does pattern b match basename `def` because its path is `/home/ta/abc/def`? Separate visit/display/count for a nonmatching parent with a matching file below, including the source conflict and the three detailed example totals.

<details><summary>Show solution</summary>

No: match only a case-sensitive contiguous substring of the basename. Do not filter the root. Visit the parent within depth; if a descendant matches, show only its name and exclude its metadata/statistics. If none matches, omit the subtree. The stop-traversing bullet conflicts with speech, formal rules, and examples; continued traversal follows that evidence without claiming the conflict resolved. Materials-only totals are a?c:3 files/3 bytes/24 blocks with name-only subdir1; (ab)*c:6/6/48; b(ab)*c:5/5/40, excluding c.

**Checking points:** Separate all three decisions and retain materials-only status for detailed examples.

</details>

#### Recall Q06 · Pattern consumption units

Define `?`, `*`, and grouping, and explain zero-repeat examples for `ab*`, `(ab)*c`, `a(bc)*d`, `ab?(de)*f`, and `abc?d*(ef)`. Explain quoting, the 64 limit, and substring scope.

<details><summary>Show solution</summary>

? consumes exactly one arbitrary character; * repeats the preceding character/group zero or more times. Examples a, c, ad, abXf match the first four respectively. For the last, abcdef matches with ? consuming d, zero d* repetitions, and (ef) consuming ef; abcXef also matches. A contiguous substring need not consume the entire basename. Quote against shell processing; the 64 maximum includes NUL. Literal operator-character matching is excluded, and another regex's optional-? meaning does not apply.

**Checking points:** Check all five decompositions, zero repetition, and the NUL-inclusive bound.

</details>

#### Recall Q07 · Invalid syntax versus excluded complexity

Classify empty pattern, `a()b`, `*abc`, `a**b`, `a)bc(`, `(abc`, `a*b`, `a(b*c)d`, and nested groups. Give invalid-pattern stream/message/output behavior and the rubric limit.

<details><summary>Show solution</summary>

The first six are invalid. a*b is valid preceding-item repetition; a star inside a group and nested groups are separately excluded complexity. Invalid syntax emits only `Invalid pattern syntax` to stderr and exits without listing/statistics. Excluding permission, missing-path, concurrent-change, and allocation failures from grading does not make them irrelevant to ordinary software. The broader error/overflow rubric's exact relationship to invalid-only grading remains unresolved.

**Checking points:** Do not classify a*b as invalid; distinguish syntax errors from excluded complexity.

</details>

#### Recall Q08 · Starting positions and suffixes

What different questions do outer match and inner submatch answer? Explain zero versus one-or-more repetition and the supplied hint's missing scope.

<details><summary>Show solution</summary>

Outer match searches starting positions; inner submatch checks the remaining pattern at one fixed position. Zero repetition skips the preceding item and tests the remainder; one-or-more requires consumption and subsequent suffix decisions. The star-only hint omits the full repetition branch, ?, groups, empty-suffix handling, and complete termination/backtracking, so it is not a finished matcher. Exam Q2 uses a different arbitrary-sequence wildcard star.

**Checking points:** Explain both responsibilities and missing scope without completing the implementation.

</details>

#### Recall Q09 · Depth versus memory width

Does a maximum depth of twenty make a large fixed entry array inside recursion sufficient for all inputs? Separate coordination, entry processing, and storage-release responsibilities.

<details><summary>Show solution</summary>

No: directory width is unbounded, and large local arrays accumulate across active recursive calls. Separate root/option/header/summary/aggregate coordination from opening, collecting, sorting, filtering, printing, recursion, and closing. Formatting and validation have their own contracts. Plan width, depth, allocation volume, and lifetime together and release unneeded dynamic storage; depth alone does not imply a small memory bound.

**Checking points:** Separate width/depth and explain responsibilities and release timing.

</details>

#### Recall Q10 · Tools, APIs, and source versions

Separate make/clean, compare.sh/gentree.sh/mksock, and the main API roles. State copy/format pitfalls, prohibited APIs, and the latest supplied slide deck’s submission list versus older versions.

<details><summary>Show solution</summary>

`make` builds; clean removes build results; compare checks against the reference; gentree creates .tree fixtures; mksock is the socket helper instructed not to be modified. strcmp compares; strncpy bounds copies without guaranteed NUL; strdup creates owned copies needing free; snprintf bounds formatting but may truncate; opendir/readdir/closedir traverse; stat/lstat inspect metadata; getpwuid/getgrgid find names; qsort sorts. Sorting does not replace collection/filtering/counting or promise quicksort. External regex and scandir are prohibited. The latest supplied list adds Makefile and genuine compilation history/ to dirtree.c and extensionless readme. Retain the supplied October 9, 21:00 deadline; do not infer a new date from the archive example's year.

**Checking points:** Check tool purposes, API limits, and both added items without claiming successful execution.

</details>

### Apply and check

#### Practice P01 · Checking a greedy choice with a counterexample

**Newly written synthetic practice.** Connect start-position search and recursive suffix reasoning from [EX:sp_2025_2_midterm_q02 p.5]. That exam's star is an arbitrary-sequence wildcard; here it repeats the **preceding group** as in Dirtree. Prerequisites are substring matching, grouping, and zero repetition; no matcher code is completed.

Consider basename `xabcdz` and Dirtree pattern `a(bc)*bcd`. Compare starting at x versus a, then zero versus one repetition after a. State the remaining characters/pattern and assess the rule 'consume as many groups as possible, then declare total failure if the suffix fails.'

<details><summary>Show solution</summary>

Starting at x fails the initial literal a. Starting at a consumes it and leaves bcdz. With zero group repetitions, remaining pattern bcd matches the prefix bcd; trailing z is permitted by substring matching. With one repetition, consuming bc leaves dz, which fails the required bcd suffix. Declaring total failure from that path discards the valid zero-repetition path. Starting-position search and repetition choices at a fixed position must be separate.

**Checking points:** State the successful/failed suffixes and do not conflate exam and Dirtree star meanings.

</details>

### Review plan

Annotate a small tree with depth, visit, display, and count columns for Q01–Q05. Solve Q06–Q08 and P01 by writing consumed characters and remaining suffixes, then explain storage/tool responsibilities with Q09–Q10.

## Sources

[[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 · lecture note]]

[lab 2 input and output.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) — slide 5; slide 6; slide 9; slide 10, aggregate table; slide 12; slide 15; slide 19; slide 23; slide 25; slide 28; slide 30

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · corrected transcript]] — 01:13:52–01:14:44

[lab 2 input and output_2b90a395.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output_2b90a395.pptx) — slide 32; slide 30

The official README and reference binary remain private. The stop-traversal bullet conflicts with formal rules/speech/examples, and the error/overflow versus invalid-only rubric relationship remains unresolved. Detailed filter fixtures and the updated slide deck’s submission list are materials-based, not retrospective September 23 speech. Uncertain root-depth/pattern speech is not recovered. No complete UTF-8 display-width algorithm, matcher, or assignment implementation is supplied. Source commands/tools are descriptions, not executed reference comparisons.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.
