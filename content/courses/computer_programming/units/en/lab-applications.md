---
title: "Input Validation, Board Evaluation, Object Interaction, and Game Platform Labs"
description: "Review input validation, boards, Player/Fight contracts, and Lab04 game boundaries."
course: "computer_programming"
unit_id: "lab-applications"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lab02 v4.pdf", "Lab02 official assignment metadata", "Lab03 v2.pdf", "Lab03 skeleton.zip", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: ["Lab02 official assignment metadata", "Lab03 skeleton.zip"]
source_lectures: ["courses/computer_programming/lectures/en/2026-09-10-lecture-04", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

Trace results and state from the specified input units, decision order, and object responsibilities. Compare Lab02–04 boundaries while keeping printing, returns, and actual round counts separate.

## Input validation: reading the input contract before processing values

Without a clear input unit and decision order, syntactically correct code can implement the wrong behavior. Input validation defines accepted values and failure paths. Lab02 separates line input, ordered validation, and evaluation of a stored board. The earlier context is available in the [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|September 10 lecture notes · Lab02]].

### A complete line and the `exit` sentinel

The first step repeatedly reads a String line and prints it unchanged. A line such as `Computer Programming` includes its space. Reading one token and returning only `Computer` changes the input contract. `Scanner(System.in)` is a hint about preparing input; the unit to read and the condition ending repetition are separate decisions. [Computer Programming M008 PDF pp.16–17]

The sentinel `exit` follows a different path from ordinary data. The [console example on p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017) echoes `abc`, `Computer Programming`, and `2018-12345`, but has no echo after the final `exit`. Input and output lines must be distinguished. The [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 transcript at 09:38]] likewise explains reading a line and terminating at `exit`.

### Length, separator, then digits

The `XXXX-XXXXX` format is checked in a specified order. Report the **first failure**, rather than all violated conditions. The [[courses/computer_programming/transcripts/2026-09-10|September 10 transcript, 15:25–18:22]] emphasizes that the order determines the message and that examples of later failures must pass the earlier checks.

| Stage | Check | Source example | Outcome |
|---|---|---|---|
| 1 | Is the length `10`? | `2018-1234` | `The input length should be 10.` |
| 2 | Is the fifth character, index `4`, `'-'`? | `2018_12345` | An error beginning `Fifth character should be`, displaying the required hyphen |
| 3 | Is every character except index 4 a digit? | `e018-12345` | `Contains an invalid digit.` |
| Success | All three conditions hold | `2018-12345` | `2018-12345 is valid.` |

Checking length first also avoids prematurely calling `charAt(4)` on an undersized string. The quotation marks around the hyphen in the separator message differ between M008 PDF pp.18 and 20; this chapter does not choose a new authoritative grader string. Physical PDF p.18 is printed slide 19, another distinction useful when locating the source.

M008 p.19 gives these character predicates. They are individual source conditions, not a completed validator:

```java
ch >= '0' && ch <= '9'  // digit
ch < '0' || ch > '9'    // outside the digit range
ch >= 'a' && ch <= 'z'  // lowercase English letters
ch >= 'A' && ch <= 'Z'  // uppercase English letters
```

The character `'0'` is not the integer value `0`. These expressions test consecutive character-code intervals, not every Unicode character resembling a number. Membership requires satisfying both boundaries, hence `&&`; being outside requires violating either boundary, hence `||`. Separating length, position, and character range makes the reason for each failure explainable.

## Board evaluation: marks, storage, and decision priority

Lab02's TicTacToe evaluates an input board. Nine integers are stored row by row in a `3×3` int array. Here, `0` and `1` represent Player 0 and Player 1: **zero is not an empty cell**. Input `0 1 0 1 0 0 1 1 1` becomes rows `[0,1,0]`, `[1,0,0]`, and `[1,1,1]`. The supplied `printBoard` operation helps check that layout. [M008 PDF pp.22–23]

A winning candidate fills a complete horizontal, vertical, or diagonal line with one player's mark. Finding one winning line is not enough to declare a valid victory. If both players win, or their mark counts differ by more than one, the result is `Invalid game.`. On a valid board, exactly one winner gives `Player 0 win.` or `Player 1 win.`; no winner gives `Tie.`. [M008 PDF p.24] [[courses/computer_programming/transcripts/2026-09-10|September 10 transcript, 38:21–39:19]]

### Five boards and five distinct explanations

The examples on [M008 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025) can be read as follows. A slash is explanatory row separation within this table.

| Three rows | Result | Decisive evidence |
|---|---|---|
| `0 1 0 / 1 0 0 / 1 1 1` | Player 1 wins | The final row consists entirely of ones. |
| `0 1 1 / 1 0 0 / 1 1 0` | Player 0 wins | Zeros fill the upper-left to lower-right diagonal. |
| `0 1 0 / 1 0 0 / 1 0 1` | Tie | No complete winning line exists. |
| `0 0 0 / 0 0 0 / 0 0 1` | Invalid | The mark counts are eight against one. |
| `0 1 1 / 0 1 1 / 0 0 1` | Invalid | The first column of zeros and last column of ones both win. |

The highlighted row and diagonal in the first two source boards, and the two columns in the last, show why “many matching marks” differs from “a complete line.” The transcript's unclear `role` wording does not introduce a different rule; the PDF establishes the line condition. The material does not specify a starting player or require reconstruction of every possible move history. Preserve the supplied input assumptions and decision rules without adding a different game-history validator.

### What changes in `N×N`

The extension reads `N` first and then `N²` marks. M008 p.26 assumes `N >= 3`. The winning line length and numbers of rows and columns become N, so input size, loop bounds, and indices must change together. This is not a mechanical replacement of every literal 3. Player marks, simultaneous-win invalidity, and the mark-count condition remain the same.

The first p.27 example has `N = 4`; its third row `1 1 1 1` gives Player 1 a win. The second has **`N = 5`**, with a complete zero row followed by a complete one row, so it is invalid. The last has `N = 4`, seven zeros, and nine ones, making it invalid by count difference two. The [[courses/computer_programming/transcripts/2026-09-10|September 10 transcript, 50:11–51:05]] has an unclear lower-bound phrase and calls the examples “four by four.” The `N >= 3` assumption and actual `4/5/4` dimensions come from the PDF, not a fabricated repair of that speech.

## Separating Player state from actions

Lab03's Fighting Game Simulation organizes input, conditions, and repetition around object responsibilities. `Player` manages individual identity, health, and actions; `Fight` manages interaction and rounds; `Main` manages input and overall flow. The recording associated with the [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|September 17 lecture notes · Lab03]] ends during the final Player segment labeled `17:39`. The precise declarations and later Fight/Main requirements below include **official M014/M015 material acquired on September 19**. They are not recovered speech from an unrecorded continuation.

### Initial state and the constructor

M014 pp.20–22 specify private `String userId`, private `int health = 50`, and `Random random` without an access modifier. The first two fields are not invitations for outside code to modify them arbitrarily. Distinguish the initial value from the maintained range:

\[
h_{\text{initial}}=50,\qquad 0\le h\le50.
\]

Zero is both the lower valid bound and the defeat boundary. The [[courses/computer_programming/transcripts/2026-09-17|September 17 transcript at 15:41]] contains the incomplete phrase “health attribute should be and.” Its missing type is not restored as speech; `int` is confirmed by the later material. Also distinguish p.19's descriptive `userID` from the declared `userId`, and its `attach()` typo from `attack(Player opponent)`.

`Player(String userId, int randomSeed)` receives an ID and seed. The example on PDF p.22 assigns the ID and initializes the random object with `new Random(randomSeed)`. The private skeleton's Player constructor and five method bodies remain unimplemented, however. Do not assume that the PDF's initialization example is already completed in that ZIP. Additional methods for reading information are permitted, but specific getter names or counts are not prescribed.

A seed initializes the random generator's starting state; it is not initial health or a round count. A Player's `random` reference is also different from one class-wide static state. A seed alone does not determine a trace without regard to the generator, called methods, arguments, and call order. Comparing the same sequence requires those choices to agree. No particular seed output or completed assignment implementation is supplied here.

### Targets and return contracts of the five methods

| Method | Responsibility | Boundary or result |
|---|---|---|
| `public void attack(Player opponent)` | Damage the opponent | Random integer 1–5 inclusive; opponent health must remain nonnegative. |
| `private void getDamaged(int damage)` | Apply the specified damage to self | It does not independently select another random damage amount. |
| `public void heal()` | Restore own health | Random integer 1–3 inclusive; health must not exceed 50. |
| `isAlive()` | Test survival | `true` for `health > 0`, otherwise `false`. |
| `public char getTactic()` | Report an action choice | Attack with 70% returns `'a'`; heal with 30% returns `'h'`. |

These contracts are established by M014 p.21. Its `public Boolean isAlive()` differs from the skeleton's `public boolean isAlive()`: Boolean is a wrapper, boolean a primitive. The survival condition agrees, but the declarations must not be represented as identical.

For **boundary reasoning**, health `2` minus damage `5` gives arithmetic `-3`, which cannot be the final health under the contract. Likewise, health `49` plus selected healing `3` gives `52`, exceeding the cap. A boundary-limited interpretation produces `0` and `50`, so the actual state change can differ from the selected amount. These calculations explain the limits without specifying a unique implementation. `isAlive()` is true at `1` and false at `0`; it is a predicate, not the operation that runs or terminates the whole game.

The [[courses/computer_programming/transcripts/2026-09-17|September 17 transcript, 16:37–17:39]] discusses damage, healing, survival, and tactics, but the final character statement is incomplete and the attack phrase “70” lacks an explicit percent unit. The PDF establishes `70%` and `'a'`/`'h'`. A 70% probability also does not require exactly seven attacks in every ten choices. Returning `'a'` reports a choice; it does not establish that an attack has already changed health. `random.nextInt()` and `random.nextFloat()` are hints rather than uniquely required implementations.

## Fight: connecting references and sequencing a round

Once Player owns its state, Fight coordinates the operations. The following details come from M014 pp.23–26 beyond the recording cutoff. `int timeLimit = 100` is a **maximum number of rounds**, not seconds or minutes. `int currRound = 0` denotes the pre-round state; the first displayed round is 1. The fields `Player p1`, `Player p2`, and constructor `Fight(Player p1, Player p2)` have no access modifiers.

The supplied constructor saves its input references into `this.p1` and `this.p2`. It does not create or clone players internally. Unlike the unfinished Player constructor, this reference connection is present in the skeleton, but it does not complete the game's subsequent behavior. [M014 PDF p.26; private structural comparison with M015]

### Why intermediate state matters in a sequential round

`public void proceed()` begins a round by printing `Round <Round_Number>`, then performs the action chosen by p1's tactic. If p2 remains alive, p2 performs its chosen action. The actions are sequential, not simultaneous. If p1 reduces p2's health to zero, p2 performs neither attack nor healing. Allowing p2 to heal back to life in that round would change the specification. After the actions, print the health lines in this format, replacing the angle-bracket placeholders with actual values. [M014 PDF p.25]

```text
<Player1_userID> health : <Player1_health>
<Player2_userID> health : <Player2_health>
```

This order rules out using initial `currRound = 0` as the first displayed round or printing pre-action health as the final state. Which getter supplies the information is an implementation choice; the material does not prescribe new getter names.

### Completion and winner selection return different things

`isFinished()` becomes true when either player's health reaches zero **or** the last round has completed. Both conditions are not required simultaneously. If both remain alive, completion of round 99 does not end the fight by the round limit, while completion of round 100 does. Skipping round 100 or proceeding to round 101 implements a different boundary. The PDF spells the result type `Boolean`, while the skeleton uses primitive `boolean`.

`public Player getWinner()` returns the player with greater health. Equal health awards victory to **p2**, justified in the source by p1 acting first. It is not a draw or a p1 victory. The return is a Player reference, not an ID String or a boolean. [M014 PDF p.25]

`Main`'s `public static void main(String[] args)` reads two int seeds using Scanner, constructs players with the specified fictional IDs `Gryffindor` and `Slytherin`, and connects them to a Fight. It proceeds until completion and prints `<userID> is the winner!` using the winner's ID. The inputs do not set health or the round limit. Although the heading on M014 p.28 mentions Constructor, the displayed member is `main`; no additional Main constructor is required by that heading. The orchestration loop and assignment bodies remain for the learner to implement. [M014 PDF pp.27–28]

## Lab04 packages and a common game call

Lab04 applies [Packages](packages.md) and [Encapsulation](encapsulation.md) to game execution. **NM003 v4 is the latest supplied version**, a source-version distinction rather than a new recording or live verification. Requirements shared with NM002 v2 remain the same; differences remain explicit.

The structure contains class `Platform` in package `Platform`, with `Dice` and `ChamChamCham` in the separate package `Platform.Games`. In `Platform.Platform`, the first word is a package and the second a class. The games use exactly this declaration:

```java
package Platform.Games;
```

The screen sequence on NM003 pp.27–32 creates package `Platform` from `src` using New → Package, then class `Platform`, the nested package `Platform.Games`, and the two game classes. `Platform` and `Platform.Games` are distinct packages, so public accessible classes/methods and the correct import or qualified name matter. Preserve the assigned capitalization of `Platform`, `Games`, and `ChamChamCham`.

| Qualified class name | Required calls |
|---|---|
| `Platform.Games.Dice` | `public int playGame()` |
| `Platform.Games.ChamChamCham` | `public int playGame()` |
| `Platform.Platform` | `public double run()`, `public void setRounds()` |

The `return -1` and `return -0.0` bodies on p.33 are layout placeholders, not completed implementations making every game a loss. V2 p.24 names `Lab04_skeleton.zip`, while v4 p.26 names `Lab04.zip`; **neither Lab04 archive is supplied here**. Test-class names are visible, but their internal comparisons and seed rules are not. M015 is the Lab03 ZIP and cannot stand in for a Lab04 implementation.

### Separating Dice values, printing, and returns

Unlike a conventional six-sided die, this Dice game gives the user and opponent one random integer each in **0–99 inclusive**. Before returning, it prints the user value first and the opponent value second, separated by one space. A larger user value returns `1`, a smaller value `-1`, and equality a draw `0`. [NM003 PDF pp.34–35; NM002 PDF pp.32–33]

| Printed pair | Comparison | Returned result |
|---|---|---|
| Source example `47 11` | User wins | `1` |
| Source example `40 42` | User loses | `-1` |
| Equal values | Specification's draw case | `0` |

The two printed numbers and the outcome returned to the caller convey different information. To understand the `Math.random()` hint, consider how mapping `0 ≤ r < 1` into 100 integer intervals gives 100 possible integers, from `0` through `99`. This is a mathematical explanation of the hint, not a completed `playGame()` implementation. V4's `10mins` label is lab work time, not a random rule or a program execution limit.

### Case-sensitive input in ChamChamCham

ChamChamCham provides the same `public int playGame()` shape but a different rule. The user enters exactly one of lowercase `up`, `down`, `left`, or `right`; the opponent chooses a random pose. Matching valid poses give victory `1`, differing poses loss `-1`. Any other input, including `Up`, is invalid and loses with `-1`. Automatically converting it to lowercase changes the case-sensitive requirement. [NM003 PDF pp.36–37; NM002 PDF pp.34–35]

For valid input, print the user's and opponent's poses separated by a space before returning. The supplied `up right` example gives `-1`, and `left left` gives `1`. **Matching values mean victory here, not Dice's draw.** No separate draw return is specified. Additional error messages or retries for invalid input are also not prescribed. “Similar interface” describes the common calling form, not a Java `interface` or `implements` declaration in the supplied skeleton layout.

## Platform: one-time configuration and win rate

`setRounds()` is not an ordinary setter that overwrites a value on every call. The initial round count is `1`; **only its first call randomly selects a count from 5 through 10 inclusive**. Subsequent calls cannot change that count. If the first call chooses 6, it must still be 6 after the second. Assuming the initial count is already 5–10 or drawing a new count on every call changes the state contract. [NM003 PDF p.39; NM002 PDF p.37]

`run()` first reads console integer `0` or `1`. Zero selects Dice; one selects ChamChamCham. It runs the selected game for the configured number of rounds and returns a double win rate. Configuration and execution have different responsibilities.

\[
\text{win rate}=\frac{\text{rounds won by the user}}{\text{total rounds played}}.
\]

A Dice draw is not a victory, but it is a played round and remains in the denominator. For an **explanatory outcome trace** of win, loss, draw, win, the rate is `2/4 = 0.5`. Excluding the draw to produce `2/3` computes a different measure. Dividing two ints first can also truncate `4/6` to `0`; distinguish a double ratio from integer division.

The source does not prescribe handling for selections outside 0/1, a seed, exact private field names, or a required getter count. The motivation for generalization on NM003 p.38 refers forward to inheritance; it does not make a new inheritance structure compulsory for this assignment.

### Counting actual rounds in the two console examples

[NM003 PDF p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-040) and NM002 p.38 show the same two runs:

| Round | Dice pair | User outcome | ChamChamCham pair | User outcome |
|---|---|---|---|---|
| 1 | `73 38` | Win | `up left` | Loss |
| 2 | `58 10` | Win | `left up` | Loss |
| 3 | `95 26` | Win | `down right` | Loss |
| 4 | `69 39` | Win | `down down` | Win |
| 5 | `2 65` | Loss | `up right` | Loss |
| 6 | `38 77` | Loss | `down up` | Loss |

The first rate is `4/6 = 2/3`; displayed `0.6666667` is an approximation. Only the fourth pose pair matches in the second run, so the rate is `1/6`, displayed as `0.16666666666666666`. In the right console, a standalone input line `down` and the subsequent output line `down down` are not two rounds; they are the input and result of one round.

Both examples having six rounds does not fix the permitted range to six. Nor do the differing decimal lengths prescribe a particular output formatter. The required result is a double win rate. Keep the sample's display separate from the return contract.

## Key Takeaways

- A first-failure validator's order is part of its contract. Board invalidity can override a candidate winning line.
- Player owns state/actions, Fight sequences rounds, and Main connects input to overall flow.
- Randomly choosing a tactic neither performs the action nor guarantees a fixed count in ten choices.
- Equal Dice values draw; equal valid ChamChamCham poses win. Input case is part of the specification.
- Only the first setRounds call configures rounds; run returns wins/all rounds as a double, including draws in the denominator.

## Recall and Practice

### Inputs and boards

#### Recall Q01 · Whole lines and the sentinel

How does the echo stage handle `Computer Programming` versus `exit`? Does merely preparing a Scanner satisfy the whole-line contract?

<details><summary>Show solution</summary>

Echo the entire first line, including its space, and continue. `exit` is a sentinel and is not echoed in the source example. Reading only one token and outputting Computer changes the contract. Scanner(System.in) is an input-preparation hint; line granularity, termination, and echo order still need separate decisions.

**Checking points:** Check space preservation and the non-echoed exit sentinel.

</details>

#### Recall Q02 · First failure and character ranges

State the length/separator/digit order and classify the four source inputs. Explain in/out digit predicates and lowercase/uppercase English-letter ranges.

<details><summary>Show solution</summary>

Check length 10, then '-' at index 4, then digits everywhere else. The inputs fail length, separator, digits, and then pass respectively. Length prints `The input length should be 10.`, digit failure `Contains an invalid digit.`, and success appends `is valid.`. Testing a later check requires passing earlier ones; checking length first also avoids premature charAt(4). Digits satisfy `ch>='0' && ch<='9'`; non-digits satisfy `ch<'0' || ch>'9'`. Lowercase and uppercase use both bounds of 'a'–'z' and 'A'–'Z'. Character '0' differs from integer 0; these are not all Unicode numerals. Preserve the separator-message quote discrepancy.

**Checking points:** Check order, first-failure behavior, AND/OR logic, and character constants.

</details>

#### Recall Q03 · Five board decisions

Explain 0/1 marks and row-major input. Classify these boards in order with reasons: `010/100/111`, `011/100/110`, `010/100/101`, `000/000/001`, `011/011/001`.

<details><summary>Show solution</summary>

Zero and one denote players, not empty cells. Store nine inputs in successive groups of three rows; `printBoard` checks that layout.

| Board | Result | Reason |
|---|---|---|
| `010/100/111` | Player 1 win | Last row 111; counts 4/5 |
| `011/100/110` | Player 0 win | Main diagonal 000; counts 4/5 |
| `010/100/101` | Tie | No complete line; counts 5/4 |
| `000/000/001` | Invalid | Counts 8/1 differ by 7 |
| `011/011/001` | Invalid | First column 000 and last column 111 both win |

A whole row, column, or diagonal must match. Simultaneous wins or count difference >1 override a candidate win. Do not add a starter or complete move-history rule.

**Checking points:** Check storage, all five decisions, and the distinct invalidity causes.

</details>

#### Recall Q04 · Boundaries controlled by N

For N=5, do three matching values at the start of a row win? Explain changed input/index/line bounds, unchanged rules, and p.27's 4/5/4 examples.

<details><summary>Show solution</summary>

No: all N marks must agree. Read N first, then N² marks; adapt N rows, N columns, and N entries per line. The material assumes N>=3 while retaining 0/1 meanings, simultaneous-win invalidity, and the count rule. The first N=4 example has a winning third row of ones; the N=5 example has complete zero and one rows and is invalid; the last N=4 example is invalid with counts 7 and 9. Dimensions and the lower bound come from the PDF, not the unclear speech calling all examples 4×4.

**Checking points:** Check N² inputs, N-long lines, retained rules, and all three examples.

</details>

### Objects and rounds

#### Recall Q05 · Player state and construction

Explain Player/Fight/Main responsibilities, the Player declarations and initial state, and constructor inputs. Does the PDF initialization example mean the ZIP constructor is completed?

<details><summary>Show solution</summary>

Player manages ID, health, and actions; Fight manages interactions/rounds; Main manages input and flow. Fields are private String userId, private int health=50, and package-access Random random. Health stays in 0–50 with zero the defeat boundary. Player(String userId,int randomSeed) receives identity and generator initialization inputs. The PDF shows ID assignment/new Random(randomSeed), but the ZIP constructor and five method bodies remain unfinished. Distinguish descriptive userID/attach from declared userId/attack. Extra accessors are allowed without prescribed names/counts. The interrupted spoken type is not recovered speech.

**Checking points:** Check responsibilities, exact field types/access, 50 versus 0, and PDF/skeleton differences.

</details>

#### Recall Q06 · Contracts of five methods

(a) Distinguish attack/getDamaged/heal targets, ranges, and returns. (b) Assess damage 5 at health 2, healing 3 at health 49, and isAlive(). (c) Explain getTactic's return/probability and the PDF/skeleton type discrepancy.

<details><summary>Show solution</summary>

(a) public void attack(Player opponent) selects damage 1–5 for the opponent; private void getDamaged(int damage) applies a specified amount to self rather than choosing damage again. public void heal selects 1–3 for self. 

(b) A boundary-limited interpretation gives 0 and 50 in the examples; -3/52 violate the bounds. isAlive tests health>0, true at 1 and false at 0. 

(c) Retain PDF Boolean versus skeleton boolean. public char getTactic returns the 70% 'a'/30% 'h' choice, without performing an attack or guaranteeing seven attacks in ten trials. The PDF establishes these details; nextInt/nextFloat are hints.

**Checking points:** Separate targets, ranges, boundaries, predicate, and choice return.

</details>

#### Recall Q07 · Reference connection and one round

What do Fight's constructor, timeLimit=100, and currRound=0 mean? Explain first-round output/action order and the case where p1 leaves p2 dead.

<details><summary>Show solution</summary>

The constructor stores the supplied Player references, connecting existing objects without constructing or cloning them. Fields and constructor omit access modifiers. timeLimit is a maximum round count, not time; currRound=0 is pre-round, so the first heading is Round 1. Print the round, perform p1's chosen action, let p2 act only if still alive, then print both final health values in the specified player-ID/health format. If p1 reduces p2 to zero, p2 neither attacks nor heals. Specific getter names are not prescribed.

**Checking points:** Check reference connection, first number, intermediate survival, and final-state output order.

</details>

#### Recall Q08 · Completion and winner return

Compare completion after rounds 99/100 while both survive with completion at zero health. What wins a final tie, what type is returned, and how do PDF/ZIP declarations differ?

<details><summary>Show solution</summary>

Either zero health or completion of the last round ends the fight. With both alive, round 99 does not meet the limit but completed round 100 does; round 101 is outside the contract. Higher health wins, with p2 winning ties under the rule accounting for p1 acting first. getWinner returns a Player reference, not an ID or boolean. isFinished uses Boolean in the PDF and boolean in the skeleton; matching intent does not make declarations identical. Completion and winner selection have separate return contracts.

**Checking points:** Check OR termination, the 99/100 boundary, p2 on ties, and the Player result.

</details>

#### Recall Q09 · Main and seeds

Explain the flow from Main's two int inputs to its winner message. Does matching a seed guarantee matching output for any implementation?

<details><summary>Show solution</summary>

The ints initialize each Player's random generator. Create the fictional Gryffindor/Slytherin players, pass their references to Fight, proceed until completion, and use the returned winner's ID in `<userID> is the winner!`. Seeds are neither health nor round counts; per-Player Random references are not one static state. Comparable random traces also require matching generators, called methods, arguments, and call order. Page 28's Constructor heading adds no Main-constructor requirement; the ZIP main body is unfinished. This flow comes from material beyond the recording cutoff.

**Checking points:** Check input purpose, object connections, reference-to-ID use, and seed comparison conditions.

</details>

### Games and Platform

#### Recall Q10 · Exact Lab04 membership

Explain the Platform.Platform/Platform.Games structure, creation sequence, required methods, placeholders, and archive limitations.

<details><summary>Show solution</summary>

Create package Platform under src, class Platform within it, then separate package Platform.Games and Dice/ChamChamCham. Qualified names are Platform.Platform, Platform.Games.Dice, and Platform.Games.ChamChamCham; game declarations use `package Platform.Games;`. Separate packages require accessible public classes/methods and correct imports or qualification. Games expose public int playGame(); Platform exposes public double run() and public void setRounds(). -1/-0.0 bodies are placeholders. Neither the v2-named Lab04_skeleton.zip nor v4-named Lab04.zip is supplied; M015 belongs to Lab03. Visible test names do not disclose their internals.

**Checking points:** Check exact case, signatures, separate packages, and absent archives.

</details>

#### Recall Q11 · Dice printing and returns

Explain Dice's range and user/opponent order, then return results for `47 11`, `40 42`, and equal values. Explain the Math.random hint's endpoints.

<details><summary>Show solution</summary>

Each side receives one integer in 0–99. Before returning, print the user's value, one space, and the opponent's value. The three return results are 1,-1,0. Distinguish a printed numerical value from the separate outcome code. Mapping 0≤r<1 into 100 integer intervals gives 0 through 99, excluding 100; this is not a conventional 1–6 die. V4's 10mins is lab work time, and TestDice seed/internal checks are not supplied.

**Checking points:** Check both endpoints, printing order, all outcomes, and the hint's range.

</details>

#### Recall Q12 · Pose case and matching

Give results for `Up`, valid up/right, and left/left, and compare Dice equality. Does 'similar interface' imply a Java interface declaration?

<details><summary>Show solution</summary>

Up is not one of the exact lowercase up/down/left/right inputs, so it loses with -1. Valid up/right differs and returns -1; left/left matches and returns 1. The opponent chooses randomly; with valid input, print user/opponent poses separated by a space before returning. Matching poses win, unlike Dice's equal-value draw 0. Do not prescribe lowercase conversion, extra error messages, or retries. The common public int playGame() shape does not establish an interface/implements declaration in the supplied layout.

**Checking points:** Check invalid/different/matching paths and avoid adding unspecified behavior.

</details>

#### Recall Q13 · One-time configuration and ratios

Explain initial rounds, first/second setRounds calls, and run's 0/1 selection. Compute the win/loss/draw/win rate and explain integer-division risk.

<details><summary>Show solution</summary>

Initially rounds=1. Only the first call chooses 5–10 inclusive; later calls preserve that choice, so a first result of 6 remains 6. run selects Dice with 0 or ChamChamCham with 1, plays the configured rounds, and returns a double win rate. The four outcomes give 2/4=0.5; draws remain in the denominator, so 2/3 is wrong. Performing int 4/6 first truncates to 0, which later conversion cannot repair. Do not add unspecified selection handling, seeds, field/accessor names, or required inheritance design.

**Checking points:** Check one-time configuration, selection, draw denominator, and division types.

</details>

#### Recall Q14 · Counting console rounds

Compute rates for Dice pairs 73/38,58/10,95/26,69/39,2/65,38/77 and pose pairs up/left,left/up,down/right,down/down,up/right,down/up. How do standalone down input and down down output count?

<details><summary>Show solution</summary>

Dice wins the first four of six rounds: 4/6=2/3. Only the fourth pose pair matches: 1/6. Standalone down and the subsequent down down are the input/output of one round. Displays 0.6666667 and 0.16666666666666666 illustrate ratios without prescribing a formatter. Two six-round samples do not fix the configurable range at six. V2 p.38 and v4 p.40 use the same values, not different numerical rules.

**Checking points:** Check both fractions, one input/output pair per round, and display versus contract.

</details>

### Application practice

#### Practice P01 · Isolating failure stages

New lecture/material-based general practice. The date candidate has calendar/leap-year demands, while the file-input candidate requires exceptions/resource handling, so neither establishes this lab's direct exam style. Evaluate claims that input `x` tests the digit stage and that three initial matching marks win an N=5 row. Give the flaw and a focused check for each.

<details><summary>Show solution</summary>

`x` has length 1 and stops at the first stage, so it does not observe digit validation. A length-10 input with a hyphen at index 4 and another nondigit, such as `e018-12345`, isolates that later check. An N=5 row needs all five marks: [0,0,0,1,1] refutes a three-entry row check. That row alone is not winning; full-board classification still requires other lines and counts.

**Checking points:** Explain reachability and complete-line length without supplying a complete validator or board implementation.

</details>

#### Practice P02 · Decisions before and after an action

New materials-based general practice; no indexed question directly supports this round-contract style. Immediately before p1 acts, p2 health is 2 and selected damage is 5. A reviewer proposes executing p2's planned heal first, stopping after round 99 while both live, or returning only an ID from getWinner. Explain all three mismatches.

<details><summary>Show solution</summary>

The specified order is p1 then p2. Applying the nonnegative boundary leaves p2 at 0, so the intermediate survival check suppresses its heal. Healing first changes both order and survival behavior. Completed round 99 with both alive has not reached final round 100. getWinner returns a Player reference; Main reads its ID for the message. Returning only the ID changes both responsibility and return type. The damage is a stated reasoning input, not a seed-derived output.

**Checking points:** Check order, intermediate state, the round-100 boundary, and return responsibility.

</details>

#### Practice P03 · Different contracts behind similar results

New materials-based general practice; no indexed style evidence directly combines these games with one-time configuration. The first setRounds chooses 5 and it is called again. Dice outcomes are 1,0,-1,1,0. Give round count/rate and evaluate proposals to return draw 0 for matching poses or count input/output lines as separate rounds.

<details><summary>Show solution</summary>

The second configuration call preserves 5 rounds; two wins out of five give 0.4, with both draws in the denominator. Equal valid poses return 1 in ChamChamCham, not Dice's 0. A shared playGame signature does not make winning conditions identical. Console input and its result describe one round; counting both lines inflates the denominator. No completed game body or unseen test implementation is needed.

**Checking points:** Check one-time configuration, five rounds, 0.4, each game's equality rule, and the round unit.

</details>

### Short review plan

Reclassify Q02–Q04 by failure reason, then recall Q06–Q09 as state/return contracts. Next day, calculate Q13–Q14 and P03 to catch errors involving draws, input lines, and the second configuration call.

## Sources

Lab02 connects to September 10 and part of Lab03 to September 17. The latter recording ends in the Player segment at 17:39; exact types, probabilities/characters, and later Fight/Main requirements are supplemented by official materials obtained September 19, not recovered speech. Lab04 v2/v4 are materials-only. Original assignment ZIPs and administrative metadata have no public links; Lab04 archive/test internals are absent. Complete assignment implementations are outside this review.

### Dated notes and transcripts

- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · lecture notes]]

- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · lecture notes]]

- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 · corrected transcript · 09:38; 15:25–18:22; 38:21–39:19; 50:11–51:05]]

- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 · corrected transcript · 14:47–17:39 (final recorded segment)]]

### Materials and relevant pages

- [Lab02 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-027)

- [Lab03 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-028)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-024), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-038)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-040)

Without a direct indexed exam-style match, P questions are presented as lecture/material-based general practice.
