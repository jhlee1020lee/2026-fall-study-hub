---
title: "Input Validation, Board Evaluation, and Object Interaction Labs"
description: "Check validation, board rules, and Player/Fight/Main contracts through bounded traces and examples."
course: "computer_programming"
unit_id: "lab-applications"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lab02 v4.pdf", "Lab02 official assignment metadata", "Lab03 v2.pdf", "Lab03 skeleton.zip"]
private_source_assets: ["Lab02 official assignment metadata", "Lab03 skeleton.zip"]
source_lectures: ["courses/computer_programming/lectures/en/2026-09-10-lecture-04", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

Read lab specifications as contracts for inputs, validation order, state changes, and output. Trace board decisions and object interactions by hand to choose useful checks before implementation.

## A line of input and an exit sentinel have different contracts

Designing a lab starts with the unit of input and the required response to each input. Lab02 combines [[courses/computer_programming/units/en/types-expressions|Scanner and String]] with [[courses/computer_programming/units/en/control-flow|branching and loops]]: repeatedly read a line and print it unchanged. The String `exit` is a sentinel selecting termination rather than ordinary data.

Read the Input/Output labels on [Computer Programming M008, Lab02 PDF pp.16–17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) as follows:

| Input line | Required response |
| --- | --- |
| `abc` | Print `abc` and continue reading. |
| `Computer Programming` | Print the complete line, including its space. |
| `2018-12345` | Print that line. |
| `exit` | Terminate; the source example does not echo exit. |

The final exit in the source figure has an Input label without a following Output label. Echoing unconditionally before deciding whether to terminate would therefore differ from the example. Together with [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 09:38]], this separates reading, ordinary processing, and termination into distinct paths. `Scanner(System.in)` is the input-setup hint; a space within a line is not a termination signal.

## Ordered validation gives failures a priority

The Student ID Validator next checks the shape `XXXX-XXXXX`. These numeric Strings are assignment examples, not identifying information about a particular student. M008 PDF p.18, printed slide 19, requires this **order**:

| Order | Check | Meaning of failure or success |
| --- | --- | --- |
| 1 | Is the length 10? | Otherwise print `The input length should be 10.` |
| 2 | Is the fifth character, index 4, `'-'`? | Otherwise report the separator error. |
| 3 | Are all characters other than index 4 digits? | Otherwise print `Contains an invalid digit.` |
| 4 | Did all earlier checks pass? | Append ` is valid.` to the input. |

Even if several conditions fail, the first failing check determines the message. Checking length first also avoids accessing `charAt(4)` prematurely on a short String. Validation therefore specifies both safe evaluation order and reporting priority, not merely a set of predicates. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 15:25]]

`charAt(index)` returns a character. The material expresses its required digit range and its complement as:

```java
ch >= '0' && ch <= '9'  // within the required digit range
ch < '0' || ch > '9'    // outside that range
```

These are expressions classifying a `char ch`, not a complete validator. The character `'0'` is not the integer zero itself. This is the ASCII digit interval, not acceptance of every digit-looking Unicode character. The material also introduces the separate contiguous ranges `'a'`…`'z'` and `'A'`…`'Z'`.

Applying the checks in order, `2018-1234` fails length, `2018_12345` fails the separator check, and `e018-12345` fails the digit check. `2018-12345` passes and prints `2018-12345 is valid.`. A digit-failure example must first pass length and separator checks to reach the third test.

The separator message differs between pages: PDF p.18 encloses the hyphen after `Fifth character should be` in backticks, while p.20, printed slide 21, uses curved quotation marks. That source discrepancy remains; this explanation does not designate a newly authoritative grading string.

## Storing and evaluating a 3×3 board

The next lab stores nine integers in a [[courses/computer_programming/units/en/arrays|two-dimensional array]]. Inputs are 0 or 1, representing Player 0 and Player 1 marks. **Zero is not an empty cell.** M008 PDF p.23, printed slide 25, maps this input to rows:

```text
input: 0 1 0 1 0 0 1 1 1

0 1 0
1 0 0
1 1 1
```

Fill one row before advancing to the next. The supplied printBoard operation helps observe whether that mapping is correct before testing the outcome. Adjusting winner conditions cannot repair a board stored in the wrong positions.

### A winning line is not the whole validity decision

A complete horizontal, vertical, or diagonal line of one player's marks is a winning line. Finding one is not enough to declare a final winner. If both players have winning lines, or their mark counts differ by more than one, the result is `Invalid game.`. On a valid board, exactly one winner produces `Player 0 win.` or `Player 1 win.`; no winner produces `Tie.`. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 38:21]]; M008 PDF pp.24–25.

The five boards on PDF p.25 can be read row by row below. A slash separates rows here; it is not an input symbol.

| Three rows | Evidence | Result |
| --- | --- | --- |
| `010 / 100 / 111` | The final row is all 1 | `Player 1 win.` |
| `011 / 100 / 110` | The main diagonal is all 0 | `Player 0 win.` |
| `010 / 100 / 101` | No completed line; count difference is one | `Tie.` |
| `000 / 000 / 001` | Eight 0 marks and one 1 mark | `Invalid game.` |
| `011 / 011 / 001` | First column all 0, last column all 1 | `Invalid game.` |

The first board has four 0s and five 1s. The third has five 0s and four 1s, but no complete row, column, or either diagonal. The final board's count difference is only one; it fails the independent **both-players-win** condition. Collapsing the two invalidity checks loses that distinction.

These are the specified board-evaluation rules. Do not add unprovided requirements about who moved first or whether play continued after an earlier win and then claim to validate every legal game history.

### Generalizing to N×N changes meaningful bounds

M008 PDF p.26 reads N first, then N×N marks, assuming `N >= 3`. A completed line now has N cells; row and column counts and index bounds must also follow N. The mark meanings, conflicting-winner rule, and mark-count-difference rule stay the same.

PDF p.27 contains three examples of different sizes:

| Source example | Evidence | Result |
| --- | --- | --- |
| First 4×4 | Third row is `1 1 1 1` | `Player 1 win.` |
| 5×5 | First row all 0, second row all 1 | `Invalid game.` |
| Last 4×4 | Seven 0s and nine 1s, a difference of two | `Invalid game.` |

For N=5, three consecutive matching cells are insufficient; a complete five-cell line is required. Around [[courses/computer_programming/transcripts/2026-09-10|2026-09-10, 50:11]], the spoken description calls all examples 4×4 and the lower-bound wording is damaged. The source PDF establishes the actual sizes 4,5,4 and `N >= 3`. Generalization requires reconnecting input counts, tested lines, and index meanings, rather than blindly replacing every numeral 3.

## Player, Fight, and Main divide responsibilities

Lab03's Fighting Game Simulation combines [[courses/computer_programming/units/en/objects-references|object state and reference passing]], [[courses/computer_programming/units/en/methods|method contracts]], and [[courses/computer_programming/units/en/encapsulation|encapsulation]]. Player owns an individual's ID, health, and actions; Fight manages interaction and rounds; Main manages input and overall flow. Separating responsibilities makes mutation targets and calls easier to follow.

The [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 recording]], 14:47–17:39, contains part of the Player explanation and ends during the character-return description at 17:39. The precise fields, numeric contracts, and Fight/Main details below are **supplemented from official Lab03 materials acquired September 19**. They are not a reconstruction of a missing recorded tail. [M014, Lab03 PDF pp.18–28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf)

### Player's starting state and constructor

Player contains `private String userId`, `private int health = 50`, and `Random random` with no access modifier. Health must remain between 0 and 50 inclusive; zero is the losing state. The constructor parameters are `Player(String userId, int randomSeed)`. PDF p.22 shows assigning the ID and initializing `new Random(randomSeed)`. The supplied skeleton's Player constructor body is still unfinished, however; only health=50 is already provided at the field declaration. The PDF initialization example does not prove the skeleton implements it.

The broken spoken phrase “health attribute should be and” does not recover a spoken int type; int comes from the material. Likewise, p.19's descriptive `userID` and `attach()` must be distinguished from the declarations `userId` and `attack(Player opponent)`. Additional information-access methods are allowed, but no particular getter name or count is specified.

### Actions, helpers, predicates, and tactic selection

| Method | Target and effect | Range or return |
| --- | --- | --- |
| `public void attack(Player opponent)` | Apply random damage to the opponent | Integer 1–5 inclusive; resulting health cannot be negative |
| `private void getDamaged(int damage)` | Apply specified damage to this player's health | An internal action respecting the lower health bound |
| `public void heal()` | Restore this player's health by a random amount | Integer 1–3 inclusive; resulting health≤50 |
| `isAlive()` | Query the current survival predicate | True for health>0, false otherwise |
| `public char getTactic()` | Choose the next action | Attack 70% returns `'a'`; heal 30% returns `'h'` |

These are call contracts, not completed method bodies. Damaging oneself during attack or healing the opponent during heal confuses the target. At health=2 with damage=5, the result must be limited to 0 rather than −3. At health=49 with healing amount=3, the result must be limited to 50 rather than 52. These examples unpack the specification's boundaries.

PDF p.21 writes `public Boolean isAlive()` while the actual skeleton uses `public boolean isAlive()`. The recording's “70” lacks its percent unit and the final character sentence is unfinished, so 70% and `'a'`/`'h'` are established by the PDF. They do not erase the limits at [[courses/computer_programming/transcripts/2026-09-17|2026-09-17, 16:37–17:39]].

`Random.nextInt()` and `nextFloat()` are hints, not a unique required implementation. No seed-specific output or extra distribution contract is established here. Choosing a tactic also differs from performing its action.

## Fight connects references and orders each round

Fight's `int timeLimit = 100` counts maximum rounds, not seconds or minutes. `int currRound = 0` describes the pre-start state, while the first printed round is 1. The unmodified-access fields `Player p1` and `Player p2` and constructor `Fight(Player p1, Player p2)` connect the players. The supplied constructor stores the incoming references; it does not create new Players inside Fight. Changes to a participating player's health are consequently visible through Main's references too.

The specified `public void proceed()` advances one round. It first prints `Round <Round_Number>` and performs the action selected by p1's tactic. It then selects and performs p2's action **only if p2 remains alive**. If p1's attack reduces p2 to zero, p2 neither attacks nor heals. These actions are sequential, not simultaneous; their order and the survival check affect the result.

Afterward, the two health lines use the following format, with angle-bracketed parts replaced by actual values:

```text
<Player1_userID> health : <Player1_health>
<Player2_userID> health : <Player2_health>
```

This detailed order is a materials-based contract from M014 PDF pp.23–26, not an assumed continuation of the Player recording.

### A termination predicate differs from a winner reference

`isFinished()` is true when either player's health reaches zero or the final round has ended. The default range is rounds 1–100, with earlier termination through health. Confusing pre-start currRound=0 with first round=1 creates an off-by-one error in the number of rounds. This method is also written with Boolean on PDF p.25 and boolean in the skeleton.

The return type of `getWinner()` is **Player**. The player with higher health wins; equal health favors p2. The material gives p1's first-action advantage as the tie-rule rationale. Thus equal health after the final round is neither a draw nor a p1 victory. The returned Player reference differs from the ID String later printed. Simulation termination also does not imply immediate garbage collection.

## Main assembles input, objects, progress, and output

Main's `public static void main(String[] args)` connects the simulation. The two integer inputs on M014 PDF p.27 are random seeds, not initial health values or round counts. Main creates Players with IDs `Gryffindor` and `Slytherin`, constructs a Fight connecting their references, and advances it until termination.

It then uses the winner Player's ID to print `<userID> is the winner!`. A seed's relationship to generator behavior is different from having a source-provided complete trace for that seed. The sequence of random calls also matters, so no invented winner or seed-specific output is established here.

Although PDF p.28's heading says Constructor, the actual code is main; it does not demand an additional Main constructor. The skeleton's Main contains the main signature and an unfinished marker, while Fight's progress, termination, and winner methods are also unfinished beyond its provided constructor. Because methods requiring return values are empty, this scaffold is not a completed runnable program. Implementing these responsibilities and contracts remains the learner's task; this explanation does not replace the full submission bodies.

## Key Takeaways

- A sentinel takes a different path from ordinary input; validation includes first-failure order.
- Board zero is Player0's mark, and invalidity must be considered before declaring a winner.
- N×N generalization changes input count, line length, and index bounds together.
- Player owns individual state/actions, Fight order/rounds, and Main input/assembly.
- Distinguish tactic selection, action execution, termination predicates, and winner-reference return.

## Recall and Practice

### Explain and trace

#### Recall Q01 · A line and a sentinel

Inputs arrive as abc, Computer Programming, exit. Give the Lab02 echo output and termination point. May spaces be discarded or exit echoed first?

<details><summary>Show solution</summary>

Print abc and the complete Computer Programming line, preserving its space. The source labels exit as input with no following output, so termination occurs without echoing it. Read a line, distinguish the sentinel, and echo ordinary data. A space is not a termination signal and does not justify discarding the rest.

**Checking points:** Check both outputs, space preservation, and the sentinel-only exit path.

</details>

#### Recall Q02 · First-failure priority

Validate length10, then hyphen at index4, then other digits. Classify 2018-1234, 2018_12345, e018-12345, and 2018-12345; explain safety and reporting order.

<details><summary>Show solution</summary>

The first yields `The input length should be 10.`, the second the separator error, the third `Contains an invalid digit.`, and the fourth `2018-12345 is valid.`. Only the first failure is reported, so digit tests need length/separator to pass. Length-first ordering also protects charAt(4) on short input. The two pages differ in separator-message quotes; this does not designate a new exact grading string.

**Checking points:** Explain all classifications and connect priority to safe access.

</details>

#### Recall Q03 · ASCII digit boundaries

Give charAt's result type and the ASCII digit predicate/complement. Compare '0','9','A', and a digit-looking character outside ASCII0…9; state alphabet ranges.

<details><summary>Show solution</summary>

charAt returns char. `'0'<=ch && ch<='9'` accepts the interval; `ch<'0'||ch>'9'` rejects its complement. The boundary characters pass; A and outside-range digit-looking characters fail. Character '0' is not integer zero. Lowercase a…z and uppercase A…Z are separate intervals. This is not a test accepting every Unicode digit.

**Checking points:** Explain inclusive endpoints, AND/OR, char versus int, and ASCII scope.

</details>

#### Recall Q04 · Board storage and five decisions

Store input `0 1 0 1 0 0 1 1 1` in a3×3 board. Then classify separate boards 010/100/111, 011/100/110, 010/100/101, 000/000/001, and 011/011/001; slash separates rows.

<details><summary>Show solution</summary>

The input fills rows010,100,111. Zero is Player0's mark, not an empty cell.

| Board | Evidence | Result |
| --- | --- | --- |
| 010/100/111 | Counts4/5; final row all1 | Player 1 win. |
| 011/100/110 | Counts4/5; main diagonal all0 | Player 0 win. |
| 010/100/101 | Counts5/4; no row, column, or diagonal wins | Tie. |
| 000/000/001 | Counts8/1 | Invalid game. |
| 011/011/001 | Counts4/5; first column0 and final column1 both win | Invalid game. |

Stopping at one winning line misses count imbalance>1 or conflicting winners. printBoard checks storage order; extra first-move/history legality rules are not specified here.

**Checking points:** Verify storage, all five decisions, and both independent invalidity conditions.

</details>

#### Recall Q05 · Bounds that depend on N

State input count, minimum N, winning-line length, and unchanged rules for N×N. Classify each filled board below; slash separates rows.

- 4×4: `0100/1001/1111/1000`
- 5×5: `00000/11111/00011/11100/10100`
- 4×4: `0101/1010/0101/1011`

<details><summary>Show solution</summary>

Read N first and N² marks, with N ≥ 3. Row/column counts, indices, and winning-line length follow N. Mark meanings and invalidity for both winners or a count difference > 1 remain unchanged.

The first board has eight of each mark and a winning third row of ones, giving `Player 1 win.`. The second has acceptable counts 13/12, but its first row of zeros and second row of ones both win, giving `Invalid game.`. The third has counts 7/9, so the difference of two already makes it `Invalid game.`. At N = 5, all five cells must match; three are insufficient. Preserve PDF sizes 4, 5, 4 despite speech describing all three as 4×4.

**Checking points:** Explain changing bounds, retained rules, and distinct invalidity causes.

</details>

#### Recall Q06 · Player initialization and responsibility

Explain Player/Fight/Main responsibilities, Player fields, constructor parameters, and health bounds. Distinguish the PDF initialization example from scaffold completion and interpret userID/attach spellings.

<details><summary>Show solution</summary>

Player owns ID/health/actions, Fight interaction/rounds, and Main input/assembly. Fields are private String userId, private int health=50, and Random random with omitted modifier. The constructor takes String userId,int randomSeed; health stays0…50 and zero is losing. The PDF shows ID/seeded-Random initialization but the scaffold constructor is unfinished; health50 is already a field initializer. Distinguish descriptive userID/attach from declarations userId/attack, without inventing required getter names/counts. These precise details are September19 materials supplements.

**Checking points:** Cover responsibilities, fields, seed, unfinished constructor, and scope.

</details>

#### Recall Q07 · Five distinct method contracts

Summarize access, targets, ranges, and returns for attack/getDamaged/heal/isAlive/getTactic. Evaluate health2/damage5 and health49/heal3; preserve Boolean/boolean and the recorded70/character limitations.

<details><summary>Show solution</summary>

`public void` attack(Player opponent) applies damage1…5 to the opponent; private void getDamaged(int damage) reduces this player's health but not below zero. `public void` heal restores this player's health by1…3 but not above50. The boundary results are zero and50. isAlive tests health>0; PDF says Boolean and skeleton boolean. `public char` getTactic selects attack70%/'a' or heal30%/'h'; selection is not action execution. nextInt/nextFloat are hints. Recorded70 lacks a unit and character explanation cuts off at17:39, so exact percentages/characters come from the PDF.

**Checking points:** Cover all five contracts, targets, both boundary results, and type/source distinctions.

</details>

#### Recall Q08 · Reference connections and one round

Fight stores this.p1=p1 and this.p2=p2 in its constructor. Are new Players created? Explain timeLimit100/currRound0, proceed output/action order, and p2 reaching zero after p1's attack.

<details><summary>Show solution</summary>

It stores reference values for the same Players used by Main, so health changes are visible there. One hundred is a round limit, not a time unit; zero is pre-start and the first display is Round1. proceed prints `Round <Round_Number>`, then performs p1's tactic/action. It chooses/performs p2's action only if p2 is alive, so reaching zero skips both attack and heal. It then prints each `<userID> health : <health>` line in p1,p2 order. Actions are sequential; these details are materials-based.

**Checking points:** Check shared references, round units, order, and no action after defeat.

</details>

#### Recall Q09 · Termination versus winner return

What does isFinished return for health zero or the final completed round? Explain default round range, getWinner type/tie rule, and its difference from Main's printed ID.

<details><summary>Show solution</summary>

Either condition makes it true. Rounds are1…100 after pre-start zero, with earlier health-based termination. Retain PDF Boolean versus scaffold boolean. getWinner returns the Player reference with higher health, or p2 at equality, with p1's first-action advantage as the stated tie rationale. It returns neither an ID String nor a draw; Main separately reads the winner's ID. Simulation termination does not prove immediate GC.

**Checking points:** Distinguish predicate/Player return, p2 ties, round boundaries, and GC.

</details>

#### Recall Q10 · Main input and unfinished scope

Where do Main's two ints go and what objects does it assemble? Explain the final message, p28's Constructor heading, unfinished scaffold, and why no seed-specific winner is established.

<details><summary>Show solution</summary>

The ints seed the two Players' random generators, not health or round counts. Main creates Players with IDs Gryffindor/Slytherin, connects their references in Fight, and advances until termination. It prints `<userID> is the winner!` from the returned Player's ID. P28's code is main despite its Constructor heading; no additional Main constructor is required. Main, Player initialization, and Fight progress/termination/winner bodies remain unfinished, including empty value-returning methods. Generator use/order affects results and no supplied complete seed trace establishes a particular winner.

**Checking points:** Explain seed→Players→Fight→winner ID and unfinished implementation status.

</details>

### Apply the ideas

#### Practice P01 · Cases that isolate failure stages

**Newly written lecture-based general practice; no direct indexed style match.** Test inputs A,1234_56789,1234-56A89,1234-56789,exit. Give the first applicable result and explain why A alone cannot test digit validation.

<details><summary>Show solution</summary>

A fails length, so index4/digit checks are never reached. The second has length10 but fails separator. The third passes length/hyphen and fails digits because of A. The fourth passes. `exit` takes the termination path before ordinary validation/echo. To isolate the digit check, use a counterexample that passes earlier checks, such as the third input. Retain the source's separator-quote discrepancy rather than establishing a new grading string.

**Checking points:** Explain all five paths, first-failure priority, and isolated testing.

</details>

#### Practice P02 · Trace a round with stipulated events

**Newly written lecture-based general practice; no direct indexed style match.** This exercise stipulates p1 attack with damage5; it is not a seed-derived result. Initially currRound0,p1 health4,p2 health3, IDs Gryffindor/Slytherin. Trace one round's health, output, termination, and winner. Could p2 execute a supposedly prepared heal?

<details><summary>Show solution</summary>

In round1, p1 applies damage5, clamping p2 to zero while p1 stays4. Defeated p2 does not enter tactic/action processing and cannot heal. The health condition ends the fight; getWinner returns p1, and Main prints its ID.

```text
Round 1
Gryffindor health : 4
Slytherin health : 0
Gryffindor is the winner!
```

The final line belongs to Main after termination, not proceed itself. A supposedly prepared heal cannot override the no-action-after-defeat contract. This traces stipulated events, not actual seeded behavior or a complete implementation.

**Checking points:** Check clamp-to-zero, skipped p2, output ownership, Player versus ID, and stipulated scope.

</details>

### Review plan

Create input/error examples with Q01–Q03, then verify Q04–Q05 boards through rows, columns, diagonals, and counts. State responsibilities/return types in Q06–Q10 and check validation/round order in P01–P02.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 corrected transcript]] — 09:38, 15:25, 38:21, 50:11.
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 corrected transcript]] — 15:41, 16:37.

### Materials and page views

- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-020), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-027).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-028).

Lab02's separator-message quotation marks differ on PDF p18/p20; no new authoritative grading string is chosen. Board rules evaluate the supplied filled board, not every legal game history. The September17 recording ends at17:39. Lab03's precise declarations/numbers and detailed Fight/Main contracts are supplements from materials acquired September19. Retain PDF Boolean versus skeleton boolean and userID/userId, attach/attack differences. The scaffold has unfinished methods; no complete run or seed-specific winner is established.


---

[[courses/computer_programming/units/en/encapsulation|← Previous: Encapsulation, Access Control, and State Design]] · [[courses/computer_programming/units/index|Unit contents]]
