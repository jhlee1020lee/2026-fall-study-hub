---
title: "Packages, Namespaces, and Java API Use"
description: "Connect namespaces, version-specific branches, imports, and API documentation."
course: "computer_programming"
unit_id: "packages"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["5 encapsulation.pdf", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-15-lecture-05"]
---

Start by identifying a class through its qualified type name. Then check imports, access, and API contracts separately to avoid confusing similarly named types.

## Packages: giving the same short name different namespaces

Combining classes written by different people can bring together unrelated types with the same name. A package groups related classes and interfaces, providing a namespace and an access boundary. In the diagram on [M012 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-026), both the File I/O component and the UI component contain `Tools.class`. The merged area on the right exposes the collision. Page 27 separates `FileIO`, `Graphic`, and `UI`, distinguishing `Project/FileIO/Tools.class` from `Project/UI/Tools.class`. The lesson is not to memorize the diagram's filenames: **adding membership to a name makes the types distinguishable**.

This chapter connects Lab04 materials with the package portion of M012 as materials-only study. The recorded scope associated with the [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|September 15 lecture notes · access control and the next topic]] reaches the encapsulation material through M012 p.23. At [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 01:30:43]], the lecturer explicitly postpones packages. No new taught date is assigned to the detailed material here.

### Two `Keyboard` classes are two different types

The Lab04 example places `Keyboard`, `Monitor`, and `Mouse` in `computer`; `Drum`, `Guitar`, and `Keyboard` in `instrument`; and a `Mart` class containing `main()` outside an explicitly declared package. The keyboards' qualified names are `computer.Keyboard` and `instrument.Keyboard`. Only their final name component is the same. They are distinct types, so one need not be arbitrarily renamed. [Computer Programming NM003 PDF pp.11–14; NM002 PDF pp.9–12]

`package computer;` declares membership and corresponds to the example project's `computer` source directory. The displayed label “Default” means the unnamed package obtained by omitting a package declaration; it is not an instruction to write `package default;`. A subpackage is also a separate package. A directory appearing beneath another directory does not automatically share that package's package-private access. This is essential when applying the phrase “same package” from [Encapsulation](encapsulation.md).

## Tracing qualified construction and each object's branch

Each `Keyboard` class stores private `id` and `name` fields using its constructor and supplies `printCompanyInfo()`. Having a method with the same name does not establish an inheritance relationship between the two classes. Each class evaluates `id % 10` using its own code and selects its own branch.

| `id % 10` | Lab04 `computer.Keyboard` | `instrument.Keyboard` |
|---|---|---|
| `1` | `Corsair` | `Samick` |
| `2` | `Razor` | `Yamaha` |
| Otherwise | `Realforce` | `Gipson` |

`Gipson` and `Razor` retain the source's spelling. These are strings in code branches, not independently researched statements about brands. `Mart` constructs the objects as follows. [NM003 PDF pp.12–14]

```java
computer.Keyboard keyboardComputer =
    new computer.Keyboard(15523, "H Gaming keyboard");
instrument.Keyboard keyboardMusic =
    new instrument.Keyboard(131511, "Black and white keyboard");
```

The first object has `15523 % 10 = 3`, so it takes the `else` branch. The Lab04 code therefore gives `H Gaming keyboard: Realforce's device`. The second has `131511 % 10 = 1`, giving `Black and white keyboard: Samick's device`. First identify the class named by construction, then trace the branch inside that class.

However, the [output box on NM003 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-015) prints `Razor` for the first object. NM002 v2 p.13 contains the same discrepancy. This is an **internal conflict between the code and its displayed output**. The screenshot does not change remainder `3` to `2`, and it is not evidence of a verified execution. The `Realforce` result above follows directly from the supplied code.

The older computer-keyboard example in M012 pp.29–34 instead uses `Samsung`/`LG`/`Apple`. For the same ID `15523`, that version selects `Apple`, consistently with its own output on p.34. Mixing its strings with Lab04's branches would lose source identity. Numerical tracing must follow one identified version at a time.

## `import`: shortening names without changing access

An import allows a type to be used by a short name instead of repeatedly writing its qualified name. These three forms can refer to the same accessible class. [M012 PDF pp.35–37]

| Approach | Declaration or use | Effect |
|---|---|---|
| Qualified name | `computer.Keyboard` | Names the package and class directly. |
| Single-type import | `import computer.Keyboard;` | Allows that class to be named `Keyboard`. |
| Wildcard import | `import computer.*;` | Makes accessible types in that package available for simple-name lookup. |

Importing does not create an object; `new` performs construction. Importing also does not unlock private access. When both packages contain `Keyboard`, avoid an ambiguous simple name and qualify the required type. A wildcard does not recursively import types from subpackages.

A top-level `public class` can be used from another package; in the source-file organization shown, it belongs in a `.java` file with the same name. A top-level class without a modifier can serve as a helper within its package. Do not transfer the member modifiers `private` and `protected` to these top-level declarations. The shortened `new computer.Keyboard()` on M012 p.36 illustrates name notation, not a supplied no-argument constructor. The earlier constructor requires an `int` and a `String`.

### Locating built-in packages

The material uses `String`, `System`, and `Math` from `java.lang` without explicit imports. `java.util` contains types such as `Arrays`, `Calendar`, `Date`, `Random`, and `StringTokenizer`; `java.io` supplies I/O classes and interfaces. Lab04 contrasts the single-type import `import java.util.Scanner;` with `import java.time.*;`, which enables lookup of types in that package. [M012 PDF p.46; NM003 PDF p.18]

```java
import java.util.Scanner;
import java.time.*;
```

These declarations do not yet read input or calculate a time. After resolving a name, the programmer must understand the relevant constructor or method's parameters and result. API documentation is where that contract is located.

## Reading a member's contract in API documentation

An API, or Application Programming Interface, is a contract for using functionality supplied by other code. Instead of implementing everything, a program can use `Scanner` for input and facilities such as `Math.random()`. Knowing the name is not enough to call a method correctly. Different parameter lists can give methods with the same name different uses.

Lab04 v4 shows a four-step path through Java 11 documentation. The following describes **the supplied screenshots**, not a claim about the current documentation UI or software state. [NM003 PDF pp.19–24]

| Stage | What the screen shows | Question to answer next |
|---|---|---|
| Module list, p.21 | Names such as `java.base` | Which broad group contains the facility? |
| Package list, p.22 | Packages in `java.base` | Which package contains the needed type? |
| Class list, p.23 | Classes in `java.math` | Which class is relevant? |
| Member summary, p.24 | `Modifier and Type`, `Method`, `Description` | Do the result type, parameter form, and explanation match the intended use? |

On [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-024), connect a method name with the type to its left and the description on the same row. If the name repeats, compare the parameter lists as well. Seeing `BigDecimal` and other entries in the screenshots does not establish coverage of every numerical API they expose.

This documentation path already appears in v2 pp.17–22. V4 adds earlier explanations defining encapsulation and packages; it does not introduce the API navigation topic for the first time. The inner-class and `Calculator` material in M012 pp.38–45 remains outside the selected package scope. Resolving precise names and reading accessible operations' contracts leads directly to distinguishing `Platform.Platform` from `Platform.Games` in [Lab applications](lab-applications.md).

## Key Takeaways

- A package supplies a namespace and an access boundary; the two qualified `Keyboard` names denote different types.
- Imports shorten names without constructing objects or granting access. Subpackages remain separate packages.
- Lab04 code selects `Realforce` for ID 15523 although its output box says `Razor`; the older M012 branch selects `Apple`.
- Navigate module → package → class → member, checking parameters, result type, and description together.

## Recall and Practice

### Names and contracts

#### Recall Q01 · Qualified names and package boundaries

What do packages resolve in the `Tools` collision and two-`Keyboard` examples? Explain the Default label for `Mart` and subpackage access.

<details><summary>Show solution</summary>

Merging File I/O and UI copies of `Tools.class` creates a short-name collision; package membership distinguishes them. Likewise, `computer.Keyboard` and `instrument.Keyboard` retain the same final name but are different types. A package groups related classes/interfaces and defines an access boundary. Default for `Mart` means no package declaration, not `package default;`. The example maps `package computer;` to its computer source directory. A subpackage is separate and does not inherit package-private access.

**Checking points:** Check both qualified names, the unnamed package, and separate access boundaries.

</details>

#### Recall Q02 · Version-specific branches

Each keyboard stores private `id` and `name` through its constructor, then branches on `id%10`. List the Lab04 branches and trace computer ID 15523 and instrument ID 131511. Compare the output box and M012.

<details><summary>Show solution</summary>

The computer branches are 1→`Corsair`, 2→`Razor`, otherwise→`Realforce`; instrument branches are 1→`Samick`, 2→`Yamaha`, otherwise→the source spelling `Gipson`. Remainders 3 and 1 yield Realforce and Samick. The v2 p.13/v4 p.15 Razor output conflicts with that code. M012 instead uses Samsung/LG/Apple, yielding Apple for 15523. A shared method name creates no inheritance relationship; use each constructed type's own version.

**Checking points:** Check the remainders, all six branches, and the version-specific discrepancy.

</details>

#### Recall Q03 · Imports and access

Compare qualified naming, single-type import, and wildcard import. Address the two-`Keyboard` ambiguity, top-level access, built-in packages, and the abbreviated constructor call.

<details><summary>Show solution</summary>

`computer.Keyboard`, a single-type import followed by `Keyboard`, and a package wildcard are naming alternatives for accessible types. Qualify names when the two keyboards would be ambiguous. A wildcard neither imports subpackages recursively nor unlocks private members. Top-level classes use public or omitted access here, not private/protected; the public class uses a matching .java filename. String/System/Math come from automatically available `java.lang`; `java.util` supplies Scanner/Arrays/Random, `java.io` I/O types, and `java.time.*` enables lookup in that package. None constructs an object. M012's shortened no-argument notation does not supply the actual keyboard's required int/String constructor.

**Checking points:** Separate name resolution, accessibility, and construction.

</details>

#### Recall Q04 · Finding an API contract

Give the four navigation stages in the supplied Java 11 screenshots and the information to inspect in the last table. Is matching the method name enough?

<details><summary>Show solution</summary>

Navigate module list → package list → class list → member summary. The screenshots pass through java.base packages and the java.math class list. In the last table, connect Modifier and Type, Method, and Description to inspect result type, parameters, and behavior. Same-named methods may have different parameter lists. APIs provide existing functionality's usage contract; imports merely shorten names. This navigation already appears in v2 and does not imply studying every numerical API visible on screen.

**Checking points:** Include all four stages and the input/result/description checks.

</details>

### Application practice

#### Practice P01 · After locating the name

New materials-based general practice. No indexed question directly combines namespaces with API navigation; the midterm's inheritance access table is not treated as this unit's style evidence. A colleague imports two packages with a same-named type and assumes that this also creates objects and grants private access. Give an ordered diagnostic procedure.

<details><summary>Show solution</summary>

Identify the two intended types by qualified names, check class/member accessibility from the caller, then consult the member contract for the constructor parameters and behavior. Construction still requires a separate `new` operation. Wildcards do not resolve an ambiguous simple name, enlarge access, or create objects. Check any subpackage's distinct name explicitly.

**Checking points:** Explain the sequence qualified name → access → contract → construction.

</details>

#### Practice P02 · Auditing an output box

New materials-based general practice; no indexed question establishes a direct style match for this version audit. A reviewer proposes changing Lab04's else branch to Razor to match its output box, and applying the same edit to M012. Evaluate the proposal without changing the source.

<details><summary>Show solution</summary>

Forcing code to match the screenshot conceals the discrepancy. Lab04's remainder 3 selects Realforce, while Razor remains a conflicting printed result. M012 has a separate Samsung/LG/Apple mapping, with Apple consistent with both its code and output. There is no basis for one shared edit; explain each version independently.

**Checking points:** Distinguish identical input from different branch tables without claiming an execution test.

</details>

### Short review plan

Recalculate Q02 for each version, then explain Q03 from memory. Next day, apply P01's diagnostic order while locating input/output contracts in the supplied API screenshots.

## Sources

This detailed chapter is materials-only. The September 15 recording reaches Encapsulation p.23 and postpones packages at 01:30:43; the dated links establish that boundary. Retain Lab04's conflicting Razor output separately from M012's Apple version, and read the API screens as supplied Java 11 examples. M012 inner-class/Calculator pp.38–45 remain outside scope.

### Dated notes and transcripts

- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · lecture notes]]

- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 · corrected transcript · 01:30:43]]

### Materials and relevant pages

- [5 encapsulation · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-037), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-046)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-013), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-022)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-024)

Without a direct indexed exam-style match, P questions are presented as lecture/material-based general practice.
