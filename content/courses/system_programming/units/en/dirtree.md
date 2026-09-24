---
title: "Dirtree Traversal, Filtering, Output Contracts, and Design"
description: "Check Dirtree’s output contract, depth, filter and storage responsibilities."
course: "system_programming"
unit_id: "dirtree"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lab 2 input and output.pptx", "assign2_README.md"]
private_source_assets: ["assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Review traversal, display and statistics as distinct decisions. Trace which entries are visited, shown and counted when depth and pattern boundaries interact.

## Traversing a directory tree under an output contract

Dirtree connects [[courses/system_programming/units/en/files-metadata|Directory Entries and Metadata]] to the responsibilities of a real program. Reading names from one directory is insufficient to print a tree. The program must classify entries, establish an order, descend into appropriate subdirectories, and coordinate displayed information with totals. [Lab 2: Input and Output, slides 2–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) combines recursive traversal, formatting, and statistics.

With no root argument, the program uses the current directory, `.`. The detailed handout specification allows up to 64 roots. The option `-d <depth>` specifies maximum depth, `-f <pattern>` supplies a name filter, and `-h` requests help. Depth and filtering can be used separately or together. Multiple roots retain separate headers, trees, footers, and summaries, followed by aggregate totals; they are not merged into one artificial tree.

Within each directory, `.` and `..` are excluded. Directories come first, with alphabetical ordering within the directory group and within the remaining entries. The source's `dirent_compare` helper serves this comparison responsibility. Sorting all names together alphabetically would incorrectly allow an early-named regular file to precede a directory.

Metadata selection matters as well. The distinction between [[courses/system_programming/units/en/files-metadata|stat and lstat]] explains why reporting a link's own type and size differs from reporting its target's properties. The contract below treats links as a separate type. Following a link unintentionally and classifying it as a directory would alter both output and statistics.

## Column widths and metadata representation

### Indentation belongs inside the name field

Each level adds two spaces of indentation. These spaces belong **inside** the 54-character path/name field rather than being prefixed outside it. A deeper entry therefore has less of that field available for its name. [Slides 6 and 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) and the handout's Output format and FAQ 2 establish the following contract.

| Field | Width | Alignment and length handling |
| --- | ---: | --- |
| Path/name | 54 | Left-aligned; truncate and end with `...` when too long |
| User | 8 | First eight bytes, right-aligned |
| Group | 8 | First eight bytes, left-aligned |
| Size | 10 | Right-aligned, in bytes |
| Blocks | 8 | Right-aligned |
| Type | 1 | The specified character |
| Summary text | 68 | Left-aligned; truncate with trailing `...` when too long |
| Total size | 14 | Right-aligned |
| Total blocks | 9 | Right-aligned |

A colon separates user and group. The entry-field widths sum to 89; with separator spaces and the colon, the source format occupies 100 characters. Correct individual widths alone do not establish a correct complete line. A summary row uses its own 68-, 14-, and 9-character fields and spacing. A name or summary exactly equal to its maximum width remains intact: truncation applies only when the limit is **exceeded**.

The handout assumes UTF-8 filenames and explicitly illustrates the user/group byte limit with formatting such as `printf("%.8s")`. UTF-8 byte counts and displayed glyph widths need not coincide. This does not establish a new, detailed Unicode display-column algorithm as part of the assignment. First distinguish a field's intended width from a string's storage length.

Numeric values overflowing the displayed field width are outside the stated assessment scope. That is separate from totals exceeding the range of `int`. Accumulation still requires an integer type wide enough for the target. The handout's Linux `long`-family suggestion should not be assumed to have the same width under every ABI.

### File-type characters belong to the tool's contract

| Metadata category | Dirtree representation |
| --- | --- |
| Regular file | Blank |
| Directory | `d` |
| Symbolic link | `l` |
| FIFO | `f` |
| Socket | `s` |
| Character or block device | Classified as a regular file in this assignment |

The FIFO marker `f` is Dirtree's convention. Copying the `p` marker seen in `ls` would violate this output format. Treating devices as regular files is likewise an assignment simplification, not Unix's general classification. Name, ownership, logical byte size, allocated blocks, and type are distinct metadata fields; one should not be guessed from another.

## Entry statistics and totals across roots

A root anchors traversal and is not itself counted as an entry in the totals. Selected entries, subject to depth and filtering, contribute type counts, byte sizes, and block counts. These quantities must be accumulated separately. Summary nouns use the singular only when the count is exactly one, and the plural for zero or at least two.

The two-root example in [slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) makes the units explicit.

| Entries under the root | Bytes | Blocks |
| --- | ---: | ---: |
| `subdir2`: 2 files, 2 links | 3086 | 16 |
| `subdir3`: 2 files, 1 pipe, 1 socket | 500 | 16 |
| Combined | 3586 | 32 |

For the first root, `1024 + 2048 + 8 + 6 = 3086` bytes. For the second, `200 + 300 + 0 + 0 = 500` bytes. Together they contain 4 files, 0 directories, 2 links, 1 pipe, and 1 socket. The entry count is `4 + 0 + 2 + 1 + 1 = 8`, without adding the two roots again. The aggregate includes total entries; the source's one-line per-root summary does not acquire an additional entry-count field.

Blocks use the source's 512-byte allocation units. Their count should not be reconstructed by rounding logical size up to a multiple of 512. Sparse files and short symbolic links demonstrate that logical bytes and allocated storage can differ. The distinction in [[courses/system_programming/units/en/files-metadata|File Size and Allocated Blocks]] prevents incorrect totals here.

The materials contain several different fixtures, or test-directory arrangements. Different totals do not imply that one printed run contradicts another.

| Separate source example | Calculation or result within that example |
| --- | --- |
| Earlier two-root example | `9192 + 14 = 9206` bytes, 16 blocks |
| Three-file long-name example | `256 + 8192 + 1000 = 9448` bytes, 24 blocks |
| Initial complete handout demo | 4 files, 3 directories, 2 links, 1 pipe, 1 socket; 21497 bytes, 56 blocks |
| Expanded complete handout demo | 9 files; 25325 bytes, 96 blocks |

Combining the expanded demo's file count with the initial demo's byte total would destroy consistency. These numbers belong to the supplied examples; they are not promised filesystem-allocation results for a newly created tree.

## Depth defines the traversal boundary

The root is depth 0 and its immediate children are depth 1. The `-d` value is the **maximum included entry depth**, with valid values 1–20 and default 20. Entries beyond it are excluded from display, traversal, and statistics. Hiding deeper names while adding their sizes would violate the contract.

[Slides 12–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) show the depth rules and examples. The complete chain appears on slide 12 and in the handout's Option 1: Depth limit, Examples: root `a` is followed by directories `b`, `c`, `d`, and `e`. A file `f` occurs under `b` at depth 2, and another `f` occurs under `e` at depth 5. Each illustrated directory has size 4096 bytes and 8 blocks; the two files have size zero and zero blocks.

| Boundary | Principal included entries | Files / directories | Bytes / blocks |
| --- | --- | ---: | ---: |
| `-d 1` | `b` | 0 / 1 | 4096 / 8 |
| `-d 2` | `b`, `c`, and the `f` under `b` | 1 / 2 | 8192 / 16 |
| `-d 3` | The preceding entries plus `d` | 1 / 3 | 12288 / 24 |
| Complete illustrated chain | `b,c,d,e` and both files | 2 / 4 | 16384 / 32 |

Displaying `c` with `-d 2` does not imply descending to its children. The directory entry at depth 2 differs from its descendants at depth 3. The source's `# depth N` annotations explain the figure and are not additional strings to print.

The [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:11:03]] first describes root depth as 0 but later contains a conflicting reading of 2. The calculation here follows the formal specification and visual example, using root depth 0; it does not claim to recover the unclear utterance.

## Basename filtering and the shape of the tree

### Matching an entry and entering a directory are different decisions

The filter is case-sensitive and applies to the basename, the final name component, rather than the full path. Pattern `b` can match within `abc`, but the basename `def` in `/home/ta/abc/def` does not contain `abc`. Searching ancestor names as well would change a file's matching behavior simply because it was moved beneath a differently named directory.

Matching is partial: a contiguous substring of the basename may satisfy the pattern. Matching files, links, pipes, and sockets receive detailed output and contribute to statistics. A matching directory does too. However, **a non-matching directory must still be traversed within the permitted depth** to look for matching descendants.

When such a directory contains a matching descendant, its name remains as a tree placeholder. Its ownership, size, blocks, and type are omitted, and it contributes nothing to statistics. If it has no matching descendants, the non-matching subtree is omitted. The root itself is not filtered. Consequently, “its name appears in the tree” and “it contributes to the totals” are not always equivalent.

[Slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) and the [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:13:52]] support continued traversal through non-matching directories. A handout Implementation bullet says the opposite. The formal matching rule, slides, and lecture agree on continued traversal, which is the rule used here. This conflict is directly relevant to why display filtering and traversal should not be collapsed into one predicate.

### Name-only ancestors and selected totals

In the `a?c` example of [slides 20–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx), the selected files are `aXc`, `abc`, and `axc`. The ancestor `subdir1` does not match, but its name remains to locate a matching descendant. Each selected file has size one byte and eight blocks, producing 3 files, 3 bytes, and 24 blocks. The placeholder directory's 4096 bytes are not added. A different excluded name appears in the slide and the handout, so the two fixtures should not be treated as one identical listing.

The `(ab)*c` example accepts the zero-repetition case `c` and a substring within `xababcx`, producing 6 files, 6 bytes, and 48 blocks. Requiring an initial `b` with `b(ab)*c` excludes `c` and gives 5 files, 5 bytes, and 40 blocks. Even `abc` can match the second pattern through its substring `bc`. Requiring the entire basename to have the pattern's matched length would miss this behavior.

These detailed examples are materials-based supplementation. At [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:14:44]], the lecturer explains operators and then skips some examples; the full calculations should not be described as all having been worked through in that speech.

## The pattern language and its boundaries

### Interpret the three operators independently

This small pattern language is neither a complete general regex language nor the shell's entire wildcard language.

| Element | Meaning | Source example |
| --- | --- | --- |
| `?` | Exactly one arbitrary character | `a?c` matches `abc` and `axc`. |
| `*` | Zero or more repetitions of the immediately preceding character or group | `ab*` matches `a`, `ab`, and `abb`. |
| `()` | Treat several elements as one group | `(ab)*c` matches `c`, `abc`, and `ababc`. |

In `a(bc)*d`, the complete `bc` group repeats, allowing `ad`, `abcd`, and `abcbcd`. In `ab?(de)*f`, the `?` must consume one character while the `de` group may be absent, allowing `abcf`, `abXf`, `abXdef`, and `abXdedef`.

The handout's `abc?d*(ef)` also becomes clearer when decomposed. In `abcdef`, `?` consumes `d`, `d*` repeats zero times, and the final group consumes `ef`. In `abcXddef`, `?` consumes `X` and `d*` consumes two `d` characters. In `abcXef`, the `d*` component is again absent.

Quote a command-line pattern so that the shell does not interpret it first. Its maximum length is 64 including the terminating NUL. Matching operator characters as literal filename characters is outside the stated assessment scope; this does not authorize adding an invented escape syntax or other regex operators. Also distinguish this “one arbitrary character” `?` from the optional-element `?` used in the [[courses/system_programming/units/en/state-machines|Integer DFA's regular-expression notation]].

### Invalid syntax versus excluded complexity

Before using a pattern as matching input, its syntax must be assessed.

| Invalid pattern | Structural problem |
| --- | --- |
| Empty pattern | No element |
| `a()b` | Empty group |
| `*abc` | No preceding element for `*` to repeat |
| `a**b` | Disallowed consecutive `*` operators |
| `a)bc(` | Closing parenthesis appears first |
| `(abc` | Unclosed group |

The pattern `a*b` is valid under these rules: it repeats the preceding `a` zero or more times. The [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:15:40]] contains unclear or contradictory recognition around that example; it should not turn a valid pattern into an invalid one.

A `*` inside a group, such as `a(b*c)d`, and nested groups are separately excluded complexities. “Not included in assessment” does not mean “must be rejected as invalid.” An invalid pattern uses the supplied `panic()` path to print only `Invalid pattern syntax` to `stderr` and terminate, without a directory listing or statistics.

The handout excludes other errors from assessment, including permission denied, nonexistent paths, rename/removal during traversal, and allocation failure. Such errors still exist and matter in general filesystem programs. The slides' broader error/overflow label also does not establish a hidden, more detailed grading rule beyond the handout.

### Searching for a starting position versus matching at that position

The hint in [slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) is **partial pseudocode** for a `*`-only version. Its outer `match` moves through possible starting positions to seek a partial match; `submatch` examines whether the pattern continues from one chosen position. Separating these responsibilities distinguishes “where does matching begin?” from “how often is this element repeated?”

One repetition branch first tries zero repetitions and checks the remaining pattern. If that fails, a path consuming further copies of the preceding character is needed. The source leaves the one-or-more branch at comment level and does not complete `?` handling, grouping, empty-suffix behavior, or every termination and backtracking condition. Transcribing the hint therefore does not yield a complete matcher.

The historical question [EX:sp_2025_2_midterm_q02 p.5] is relevant to distinguishing an outer starting-position search from matching at one position. **Its `*` consumes an arbitrary sequence of zero or more characters, whereas the current assignment's `*` repeats the preceding character or group.** Responsibility separation and checking the zero-consumption path transfer; operator semantics and a completed historical function do not transfer unchanged to this assignment.

## Entry storage and separation of program responsibilities

### Directory width and recursion depth consume different resources

The handout recommends outlining a design before reading the skeleton. The conceptual role of `main` is to coordinate options and roots, per-root headers and summaries, and the final aggregate. Directory processing is responsible for opening, collecting entries, sorting, applying display/filter decisions, performing necessary recursive traversal, and closing. Separating formatting, statistics, and pattern validation makes it easier to trace which input condition affects which result.

No upper bound on the number of entries in one directory is supplied. An arbitrarily “large enough” fixed array does not therefore cover every input. A large local array in a recursive function consumes stack storage at each active depth. Maximum depth 20 does not impose a small bound on directory **width** or total allocation.

The distinction between [[courses/system_programming/units/en/memory-layout|Stack and Heap Storage]] also clarifies lifetime. Collected entries and owned copies of names must remain valid while used; dynamically allocated storage should be released when no longer needed. Storage still used by a descendant call must not be freed prematurely. These choices interact with where sorting and filtering responsibilities reside. The discussion establishes responsibilities and lifetime conditions without providing the assignment's complete traversal or matcher implementation.

### Libraries and test tools have bounded roles

The handout and [slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) distribute useful operations across the following functions and tools.

| Purpose | Function or tool | Boundary to remember |
| --- | --- | --- |
| String comparison | `strcmp` | Connect case-sensitive comparison to the required ordering. |
| Limited copying | `strncpy` | NUL termination is not guaranteed when the source reaches the limit. |
| Owning a name copy | `strdup`, `free` | Track ownership and the point at which the copy is no longer needed. |
| Formatting into a bounded buffer | `snprintf` | Staying within the buffer does not prove that the desired text was not truncated. |
| Reading a directory | `opendir`, `readdir`, `closedir` | Collect entries and release the directory resource. |
| Metadata and owner names | `stat`, `lstat`, `getpwuid`, `getgrgid` | Distinguish links from their targets and numeric IDs from names. |
| Sorting collected entries | `qsort` | It does not perform traversal, and its name does not guarantee a specific quicksort implementation. |

The assignment prohibits `scandir` and external pattern-matching libraries such as `regex.h`. Knowing that a library can perform a related operation does not establish permission to substitute it for the required filter.

In the handout, `README.md` defines the contract, `Makefile` drives the build, `src/dirtree.c` is the skeleton, `doc/` contains Doxygen-related documentation, `reference/` holds the comparison implementation, and `tools/` contains fixture utilities. The roles of `make` and `make clean` are building and removing build products; the directory structure must agree with the Makefile's expectations.

The tool `gentree.sh` creates a directory fixture from a `*.tree` description, while `compare.sh` compares the student's output with the reference output. The `mksock` helper creates socket entries and is not to be modified. The FAQ's collision when recreating existing pipes or sockets illustrates that a test environment itself has state. Conversely, one matching output does not establish behavior at every depth boundary, non-matching ancestor, zero-repetition case, or column limit. Source fixtures and comparison tools provide concrete starting points for checking those distinct contracts.

## Key Takeaways

- Traverse nonmatching ancestors to find matching descendants.
- Name-only placeholders contribute no statistics.
- Current * repeats the preceding element and differs from the historical wildcard.
- Connect [[courses/system_programming/units/en/files-metadata|files/directories]] and [[courses/system_programming/units/en/memory-layout|storage lifetime]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Roots, sorting and output units

Explain default/max roots and -d/-f/-h. How are multiple roots, per-directory sorting and symlink classification handled?

<details><summary>Show solution</summary>

Omitted roots mean .; up to 64 roots are allowed. -d limits depth, -f filters names, -h requests help; depth/filter can combine. Each root keeps its own header/tree/footer/summary before a final aggregate. Exclude dot/dot-dot, place directories first, and alphabetize within each group. Sorting all names together is insufficient. Distinguish a symlink’s own type/size from target metadata to avoid counting it as a directory.

**Check:** Check64, separate root output, directories-first sorting and link metadata.

</details>

#### Recall Q02 · Field widths and types

Explain alignment/overflow for name54, user8, group8, size 10, blocks 8, type 1, summary fields and indentation. Include type codes, UTF-8 and large totals.

<details><summary>Show solution</summary>

Name is left-aligned with ... only on overflow, including two indentation spaces per depth inside54. User uses its first 8 bytes, right-aligned; group first 8, left-aligned; size 10/blocks 8 are right-aligned; type occupies 1. Widths total 89, with colon/spaces making100. Summary text68, left/truncated, total size 14 and blocks 9, right, use separate spacing. Exactly54/68 is not truncated. Types: regular blank, directory d, link l, FIFO f, socket s; devices are treated as regular here. UTF-8 bytes and displayed glyph widths differ without establishing a new Unicode algorithm. Excluded numeric field overflow does not prevent totals exceeding int; use a sufficiently wide target type.

**Check:** Check widths, alignment, boundaries, FIFO f, bytes/display and accumulation type.

</details>

#### Recall Q03 · Summary units

Combine roots with 2 files+2 links=3086 bytes/16 blocks and 2 files+pipe+socket=500/16. Explain roots, pluralization, separate fixtures and block totals.

<details><summary>Show solution</summary>

Aggregate:4 files, 0 directories, 2 links, 1 pipe, 1 socket; 8 entries, 3586 bytes, 32 blocks. The byte sums are1024+2048+8+6 and 200+300+0+0. Do not add the roots. Only1 is singular; 0 and≥2 are plural; total entries is an aggregate field. Sum metadata block counts in 512-byte allocation units rather than rounding logical size. Separate fixtures yielding9206/16, 9448/24, 21497/56 and expanded-demo25325/96 must not be merged.

**Check:** Check8/3586/32, excluded roots and independent allocation totals.

</details>

#### Recall Q04 · What depth excludes

Root a has directory chain b, c, d, e, plus a file under b at depth 2 and another under e at depth 5. Each directory is4096 bytes/8 blocks; files0/0. Explain `-d 1`/2/3/default totals and boundaries.

<details><summary>Show solution</summary>

Root depth 0; valid limits 1..20, default 20. `-d 1` includes b:0 files/1 directory, 4096/8; `-d 2` adds c/f:1/2, 8192/16; `-d 3` adds d:1/3, 12288/24; full tree:2/4, 16384/32. Beyond-limit entries are excluded from traversal and totals, not just display. Showing c at depth 2 does not visit its children. Diagram #depth annotations are not output. Use formal depth 0 while retaining the transcript’s conflicting0/2 wording as uncertain.

**Check:** Check all boundaries/totals and exclusion from traversal/statistics.

</details>

#### Recall Q05 · Separating filtering and traversal

Does filtering use paths or basenames? Explain nonmatching directories, roots/placeholders and the a?c/group-pattern fixture totals.

<details><summary>Show solution</summary>

Matching is case-sensitive, partial and basename-only. Traverse nonmatching directories within depth to find descendants. A nonmatching ancestor with matches remains name-only, with no detailed metadata or statistical contribution; omit its subtree if none match. The root is not filtered. The a?c example selects aXc, abc, axc:3 files/3 bytes/24 blocks. (ab)*c yields 6/6/48; b(ab)*c yields 5/5/40. Even abc contains bc, using zero group repetitions in the latter. Slide zxc and handout aZZc belong to different fixtures. The Implementation bullet saying to stop at a nonmatch conflicts with formal rules, slides and lecture and is not adopted.

**Check:** Check basename, continued traversal, zero placeholder totals, 3/6/5 selections and the conflict.

</details>

#### Recall Q06 · The current pattern grammar

Explain ?, *, () and decompose a(bc)*d, ab?(de)*f, abc?d*(ef). Why do abcdef, abcXddef and abcXef match the last pattern?

<details><summary>Show solution</summary>

? matches exactly one character; * repeats the immediately preceding character/group zero or more times; () groups. a(bc)*d permits ad. ab?(de)*f is ab+one character+repeated de+f. For abc?d*(ef), abcdef uses ?=d, d* zero; abcXddef uses ?=X, d* twice; abcXef uses ?=X, d* zero. Quote patterns against shell expansion. Maximum64 includes NUL, leaving63 payload bytes. No literal-operator escape or full regex language is introduced.

**Check:** Check each consumption path, zero repetition, quoting and 63-byte payload.

</details>

#### Recall Q07 · Invalid versus excluded cases

Classify empty, a()b, *abc, a**b, a)bc(, (abc, a*b. Must a(b*c)d and ((ab)) be rejected? State the diagnostic and assessment scope.

<details><summary>Show solution</summary>

The first six are invalid:empty pattern/group, star without a preceding element, repeated star, misplaced/unmatched parentheses. `a*b` is valid: zero or more a then b. Slides 22/24 and the handout identify `a**b` as invalid. The uncertain or contradictory `a*b` wording is in the September 23 STT at 01:15:40, not an invalid label on those slides. Star inside a group and nested groups are excluded complexities, not mandatory rejection cases. Invalid syntax uses panic to emit only `Invalid pattern syntax` on stderr and terminate without listing/statistics. Permission/path/race/allocation errors are outside the stated assessment, not nonexistent or evidence of invented hidden rules.

**Check:** Check valid a*b, excluded≠invalid and stderr-only output.

</details>

#### Recall Q08 · Two matcher responsibilities

Why separate outer match from submatch/matchat, and test zero repetition? Why is the hint incomplete, and how does historical * differ?

<details><summary>Show solution</summary>

Outer match tries starting positions; submatch checks pattern consumption at one position. Zero repetition advances past the repeated element without consuming input; if it fails, positive repetition paths may be needed. The star-only hint leaves the positive branch at comment level and does not complete ?, groups, empty suffixes, termination or backtracking. In [EX:sp_2025_2_midterm_q02 p.5], * matches an arbitrary sequence; here it repeats the preceding element. Transfer only responsibility separation/zero-branch reasoning, retaining historical nonempty-input assumptions and distinct grammars.

**Check:** Check starting-position versus local matching, zero consumption and missing mechanisms.

</details>

#### Recall Q09 · Directory width and lifetime

Does depth 20 justify a large fixed entry array? Explain recursive local storage, owned-name lifetime and separation of program responsibilities.

<details><summary>Show solution</summary>

No entry-count bound is supplied, so depth 20 does not bound directory width. Large locals accumulate across active recursive calls. Entry/name storage must survive sorting, printing and descendant use; free owned copies after final use without prematurely freeing ancestors’ needed data. `main` coordinates options, roots, headers, summaries/aggregate; directory processing opens, collects, sorts, filters, recurses as required, and closes. Separate formatting, statistics and pattern validation to review their conditions. These are responsibilities, not a complete traversal implementation.

**Check:** Check width/depth, recursive stack, lifetime and responsibility separation.

</details>

#### Recall Q10 · Tools and test scope

Explain string, directory, metadata and sorting APIs plus README/Makefile/src/doc/reference/tools. Identify prohibited APIs and test-state/coverage limits.

<details><summary>Show solution</summary>

strcmp compares; strncpy limits copying without guaranteeing NUL; strdup/free manage owned copies; snprintf bounds writes but may truncate. Use `opendir/readdir/closedir` for directories; stat/lstat differ on links, getpwuid/getgrgid resolve names, and qsort sorts collected entries without traversing or guaranteeing a particular quicksort algorithm. `scandir` and external matchers such as regex.h are prohibited. README is the contract, Makefile the build driver, src the skeleton, doc Doxygen material, reference the comparator, and tools fixture utilities. `gentree.sh` reads *.tree, compare checks output, mksock creates sockets and must remain unchanged. Make clean/build concern build state; recreated pipe/socket collisions concern fixture state. One matching run does not cover all depth/filter/width/zero-repeat boundaries.

**Check:** Check API limits, prohibitions, tool roles and test state.

</details>

### Practice

#### Practice P01 · A witness separating grammars

**Newly written synthetic practice.** Apply current pattern a*b to basename zzb. Explain outer search and the zero-repeat branch. Does the same pattern under historical arbitrary-sequence-star semantics give the same result? Give consumption paths, not a matcher.

[EX:sp_2025_2_midterm_q02 p.5] transfers outer/local responsibility and zero-consumption reasoning into a witness distinguishing grammars. Prerequisites: Q06/Q08. Historical * semantics and nonempty assumptions are not copied into current requirements.

<details><summary>Show solution</summary>

At the final b, current matching takes zero repetitions of a and matches b. At preceding z positions the zero branch fails on b versus z, so starting-position search matters too. Historical semantics require literal a, then arbitrary-sequence star, then b; zzb contains no a, so fails. Both inputs are nonempty, within the historical assumption. This witness proves no completed handling of ?, groups or termination.

**Check:** Justify current success, historical failure, starting position and zero consumption.

</details>

#### Practice P02 · Depth and filter together

**Lecture-based general practice.** A new tree has nonmatching docs at depth 1 containing aXc at depth 2, size 1, blocks 8. Root also has abc at depth 1, size 5, blocks 8, and aZZc, size 9, blocks 8. With filter a?c, compare `-d 1` and `-d 2` display/totals.

New general practice combining current lecture/handout rules. No indexed exam directly establishes this depth/filter/statistics style. Prerequisites: Q02–Q05; this is not a reference-program execution report.

<details><summary>Show solution</summary>

With `-d 1`, aXc is beyond traversal, so omit docs and print only abc in detail:1 file, 0 directories, 5 bytes, 8 blocks. With `-d 2`, docs becomes a name-only placeholder and aXc/abc are detailed:2 files, 0 directories, 6 bytes, 16 blocks. aZZc fails because ? cannot consume two characters. Neither root nor placeholder contributes to totals.

**Check:** Check1/5/8 versus2/6/16, placeholder handling and depth exclusion.

</details>

### Review plan

Recompute Q01–Q05 using visit/display/count columns and field widths. Mark consumed characters in Q06–Q08 and compare grammars with P01. Record Q09–Q10 lifetime/test limits, then combine options in P02.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 lecture notes]]

### Materials and lecture passages

- [Lab 2: Input and Output, slides 2–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slides 6 and 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slides 12–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx): depth rules and examples. The complete chain appears on slide 12 and in the private handout's Option 1: Depth limit, Examples.
- [Slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [slides 20–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:11:03]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:13:52]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:14:44]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 STT, 01:15:40]]
- September 23 Assignment 2 handout: requirements are discussed as a materials supplement; the private original and complete implementation are not linked.

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

### Scope to retain

- September23 speech/slides and the private handout jointly support the unit; detailed material requirements are not all verified speech. No complete assignment implementation or original handout is supplied.
- The uncertain root-depth 0/2 wording remains; formal depth 0 is used.
- The Implementation bullet stopping nonmatching traversal conflicts with formal rules, slides and lecture. Slides 22/24 and the handout identify `a**b` as invalid; `a*b` is valid under preceding-element repetition. The uncertain or contradictory `a*b` wording is in the September 23 STT at 01:15:40, not an invalid label on those slides.
- Star-in-group/nested groups are excluded complexity, not automatic invalidity. Different slide/handout fixtures and totals stay separate.
- The hint is incomplete star-only pseudocode. The exam uses different star semantics and nonempty assumptions; provided answers are not authority. No new preview or private answer is supplied.


---

[[courses/system_programming/units/en/memory-layout|← Previous: Process Memory, Alignment, and Parameter Passing]] · [[courses/system_programming/units/index|Unit contents]]
