---
title: "Encapsulation, Access Control, and State Design"
description: "Review consistent state, access scope, failure behavior, and accessor validation/tracing."
course: "computer_programming"
unit_id: "encapsulation"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["4 oop.pdf", "5 encapsulation.pdf", "Lab03 v2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

Separate permission to read state from permission to change it, and explain the relationships a method must preserve. Combine access control, validation, and logging to find errors that private alone cannot prevent.

## Encapsulation defines permitted interactions

After [[courses/computer_programming/units/en/objects-references|objects and references]] organize state, the next question is who may change it and through which paths. Encapsulation exposes useful interactions while hiding internal complexity and disallowed access. A driver uses a steering wheel and accelerator without understanding the entire engine.

Abstraction simplifies use through an interface; defensive programming limits unexpected changes to state. Here interface first means an object's agreed point of use, without assuming the later Java `interface` declaration syntax. The objective is to design permitted programmatic access, not to make the existence of the source code secret. [Computer Programming M012, PDF pp.2–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf)

The robot arm/head/chest collaboration analogy after [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:08:56]] illustrates this division. Each contributor can connect agreed functionality without reading every implementation detail elsewhere. This does not mean trusting code without checking it: cooperation depends on agreed inputs, results, and state guarantees.

### Inheritance and polymorphism describe other relationships

The OOP introduction connects abstraction with encapsulation, code reuse with inheritance, and varied behavior with polymorphism. The Organisms → Animals/Plants → Duck/Cat/Tree/Grass hierarchy on M011 pp.58–61 concerns **relationships between classes**. A child class can inherit its parent's characteristics, reuse its code, and add characteristics of its own. Defining a Cat class and creating several cat objects from it is a different relationship.

The introductory polymorphism example has dogs, cats, and ducks provide different sounds through the common behavior `animalSound`. A caller uses a shared agreement while concrete classes implement behavior differently. Two objects of the same Car class merely holding speed=100 and speed=90 are not that implementation distinction. See [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:04:10]] and [M011 PDF pp.58–61](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf).

The present goal is to distinguish motivations. Concrete inheritance syntax, overriding, and method dispatch remain later topics rather than hidden prerequisites for the examples here.

## One sale should change related state together

Suppose FruitStore starts with balance=10000 and stock=30, and each fruit costs 2000. Selling three requires two coordinated changes:

| State | Balance | Stock |
| --- | ---: | ---: |
| Before sale | 10000 | 30 |
| Change | +2000×3 = +6000 | −3 |
| After sale | 16000 | 27 |

If external code reduces stock but leaves balance untouched, it violates the sale relationship. M012 pp.4–6 groups both changes in `sell(int num)`, so callers need not repeat the internal calculation. Adding the method alone, however, does not prevent direct assignments while the fields remain exposed.

The following AppleStore example makes balance and stock private, uses `getBalance()` and `getStock()` for reading, and uses sell for changes. A getter can reveal a value without granting arbitrary writes. Reading state and choosing its next value are separate permissions. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:16:32]]; M012 pp.11–12.

These source methods omit public and therefore have package access. Their calls assume the same package; the lecturer's informal description of them as public is not the literal declaration. The example teaches responsibility for consistent state changes, not every validation or concurrency requirement of a real commercial system.

## Access modifiers restrict paths to members

An access modifier specifies permitted access to a member. The introduction on M012 pp.9–10 can be read as follows:

| Member declaration | Introductory meaning |
| --- | --- |
| `private` | Access centered on the declaring class |
| Modifier omitted | Package-private access within the same package |
| `protected` | Same-package access and access through inheritance under its rules |
| `public` | A public member permitting access from external classes |

For now, a package is a grouping of classes. “Default access” describes omission; it is not an instruction to insert the keyword `default`. Protected does not allow unrestricted access through any receiver in another package. Nor are all four forms equally valid for every kind of class declaration.

The `private int weight = 80;` example on M012 p.10 produces a private-access diagnostic when separate-class code reads it directly. The failure concerns the access path, not whether someone already knows the value 80. Following the introduction at [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:14:06]], the detailed Packages chapter was deferred after the material through p.23. This introductory table does not replace those later rules.

## Private helpers and preserving state on failure

Centralizing sales also provides a place to validate them. Subtracting an order larger than stock would make stock negative, so M012 p.14 introduces this helper. These methods are fragments inside AppleStore:

```java
private boolean inStock(int num) {
    int shortage = num - stock;
    if (shortage > 0) {
        return false;
    } else {
        return true;
    }
}

boolean sell(int num) {
    if (inStock(num)) {
        balance += 2000 * num;
        stock -= num;
        return true;
    } else {
        return false;
    }
}
```

The private helper hides how the check is performed. Callers request a sale and receive success or failure. Changing sell's return type from void to boolean changes its contract because the caller now needs to learn whether it succeeded.

With initial balance=10000 and stock=30, `sell(50)` produces shortage=20. The helper returns false and both assignments are skipped: **the result is false and state remains 10000/30**. The caller prints `Not enough apples in stock`. Returning false after already reducing stock would violate this demonstrated behavior. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:21:14]]; M012 pp.15–16.

The printed check does not reject negative quantities. From the same initial state, `sell(-1)` gives shortage=−31, passes, and changes balance to 8000 and stock to 31. This is **boundary analysis derived from the source code**, not a claim that the lecturer spoke those numbers. Encapsulation provides a place for validation; it does not automatically make that validation complete.

## Choosing getters, setters, and validation

Getters and setters are ordinary methods following a naming and design convention, not special Java syntax.

```java
private int age;

public int getAge() {
    return age;
}

public void setAge(int age) {
    this.age = age;
}
```

The fragment on M012 p.18 returns the field through the getter and assigns the parameter through the setter. Exposing only a getter makes that interface read-only; exposing only a setter makes it write-only. Every private field need not receive both. Neither must code inside the class always use accessors, nor must every setter return void.

Validation can live in a setter. The discussion of negative or excessively large ages motivates checking inputs without establishing a precise permitted age range. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:24:58]]

### Why the null check comes first

M012 p.21 uses [[courses/computer_programming/units/en/control-flow|short-circuiting]] to protect a setter:

```java
public void setName(String name) {
    if (name == null || name.equals("")) {
        System.out.println("Name cannot be null or empty");
    } else {
        this.name = name;
    }
}
```

`name == null` checks for an absent reference; `name.equals("")` checks the contents of an existing String. For null, the true left operand skips the method call on the right. Reversing the order attempts equals on a null receiver before a later check could protect it. Assignment occurs only for a non-null, nonempty String. The clarification is at [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:28:49]]. It requires no claim that null is a guaranteed physical address zero.

## Access tracing observes how state is used

Methods controlling access can also record reads and writes. The original class name on M012 p.22 is `ChangableVar`. Its `setValue` assigns valueToBeWatched, increments countOfChange, and prints a change number. Its `getValue` increments readHistory before returning the value. A getter can therefore have an observable side effect.

The intended material-based sequence on p.23 is:

| Step | Operation | Trace |
| --- | --- | --- |
| 1 | First `getValue()` | Default value 0, readHistory=1 |
| 2 | `setValue(52)` | value=52, change #1 |
| 3 | `setValue(53)` | value=53, change #2 |
| 4 | Second `getValue()` | Value 53, readHistory=2 |

Assigning the same value again would still increment the count because the setter never compares old and new values. It counts **setter calls**, not necessarily distinct changes of value.

However, p.23 calls `getReadHistory()` without its definition appearing on p.22. The table follows the material's intended readable-history behavior; it does not claim those two pages are a complete executable program. At [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 01:29:46]], the lecturer explains the debugging/logging motivation but skips the long trace. This materials-based analysis leaves the missing implementation unfilled while showing how controlled access supports observation.

## Key Takeaways

- Encapsulation designs usable interfaces and permitted changes; readable state need not allow arbitrary writes.
- A sale coordinates balance/stock and preserves both on failure.
- Omitted access means package-private, not public or a default keyword.
- A setter centralizes validation but does not automatically make it complete.
- A getter can update a counter; its name does not guarantee absence of side effects.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Protection despite readable values

Why can a private field remain encapsulated when a getter reveals its value? Explain abstraction, defensive programming, and agreed interfaces in the robot-work analogy.

<details><summary>Show solution</summary>

Read permission differs from arbitrary write permission. Methods can expose usable operations while restricting disallowed state changes without requiring callers to know internals. Abstraction reduces usage complexity; defensive programming limits invalid changes. Robot-part collaborators rely on agreed inputs/results/state, not unverified trust. Interface here means a point of use, not the whole later Java interface syntax.

**Checking points:** Do not confuse source secrecy with controlled access paths.

</details>

#### Recall Q02 · Hierarchy, instances, behavior

Is Organisms→Animals→Cat the same relationship as several Cat objects? Contrast class-specific animalSound behavior with two Cars having different speeds.

<details><summary>Show solution</summary>

The hierarchy relates parent/child classes for reuse and added characteristics; several Cat objects instantiate one class. Different concrete implementations of common animalSound introduce polymorphism, while the same Car method reading different speed fields is an instance-state difference. This is a motivational distinction, not a detailed dispatch/override task.

**Checking points:** Separate class relationships, instantiation, implementation differences, and state differences.

</details>

#### Recall Q03 · Two states in one sale

With balance10000,stock30,price2000, sell three. Explain the problem with externally changing only stock, what merely adding sell leaves unresolved, and getter permissions.

<details><summary>Show solution</summary>

Balance becomes16000 and stock27. Reducing only stock breaks the sale relationship between revenue and inventory. Grouping writes in sell does not prevent bypass while fields remain exposed, so access design matters. Getters permit reading without arbitrary writing. The source sell/getters omit public and assume same-package callers.

**Checking points:** Explain both calculations, bypass risk, and read/write permissions.

</details>

#### Recall Q04 · What access declarations mean

Give the introductory meanings of private, omitted modifier, protected, and public. Do you insert default for omitted access? What happens when a separate class reads private weight80?

<details><summary>Show solution</summary>

`private` centers access on the declaring class; omission gives same-package access; protected includes same-package and inheritance-based access under its rules; public exposes the member externally. No default keyword is inserted, and omission is not public. Separate-class direct access to weight produces a private-access diagnostic. The introductory table is not a complete rule for every class declaration or arbitrary cross-package receiver.

**Checking points:** Explain all levels, omission, and the table's limits.

</details>

#### Recall Q05 · Successful, failed, and negative orders

Use independent balance10000,stock30. inStock rejects only num-stock>0. On acceptance, sell adds2000*num to balance, subtracts num from stock, and returns true; otherwise false. Trace3,50,−1 and explain the helper/boolean contract.

<details><summary>Show solution</summary>

Three passes with shortage−27, returning true and state16000/27. Fifty fails with shortage20, returning false and preserving10000/30. Minus one passes with shortage−31, returning true and state8000/31. The private helper centralizes checking; boolean lets the caller observe failure. Failure must preserve both states, and the missing negative-quantity check shows validation is incomplete.

**Checking points:** Check every shortage, return, state, and failure-preservation condition.

</details>

#### Recall Q06 · Optional getters and setters

getAge returns the field and setAge assigns this.age=age. Must every private field expose both? What age bounds and setter return-type rules does the material establish?

<details><summary>Show solution</summary>

They are ordinary methods following a convention. Getter-only access can be read-only and setter-only write-only, so both are not mandatory. Validation may live in a setter, but no precise permitted age range is specified. `void` is this example's choice, not a universal setter rule; internal class code need not always go through accessors.

**Checking points:** Distinguish convention/syntax, optional permissions, and unspecified age bounds.

</details>

#### Recall Q07 · `null` guard ordering

The setter prints a message for `name==null || name.equals("")`, otherwise stores the value. Trace null, empty String, and Code; explain reversing the tests.

<details><summary>Show solution</summary>

`null` makes the left true, skipping equals and storage. Empty String makes the left false and equals true, also preventing storage. Code makes both false and is stored. Reversal calls equals on null before the guard can protect it. Reference absence and String contents are different tests; no physical-address-zero claim is needed.

**Checking points:** Explain all paths, preservation of old state, and guard order.

</details>

#### Recall Q08 · Read and write counters

ChangableVar increments readHistory per getValue and assigns/increments countOfChange per setValue. From default zero, trace get,set52,set53,get, then another set53. Explain the source's execution limit.

<details><summary>Show solution</summary>

The first get returns0/history1; set52 gives value52/change1; set53 gives53/change2; the second get returns53/history2. Another set53 increments change to3 because no equality comparison exists. Getters can have side effects, and the change counter counts calls rather than distinct values. P23 calls an undefined getReadHistory absent from p22, so this is the intended material trace, not proof of an executable complete program.

**Checking points:** Track both counters, repeated-set counting, and the missing-method limitation.

</details>

### Apply the ideas

#### Practice P01 · Sequential requests after validation

**Newly written lecture-based general practice; no direct indexed style match.** A new contract rejects num<=0 or num>stock with false and unchanged state; otherwise it sells at price2000. From balance10000,stock3, call sell(0),sell(2),sell(2) sequentially. Give returns/states and explain checking before mutation.

<details><summary>Show solution</summary>

Zero fails the new positivity condition: false,10000/3. The next two succeeds: true,14000/1. The final two exceeds current stock one: false,14000/1. Each call checks the current state. Checking after writes could alter state even for rejected requests, violating the failure contract. Positivity validation is the practice's explicit change, not a claim that the original source already implemented it.

**Checking points:** Check sequential states, the newly stipulated condition, and unchanged failure state.

</details>

### Review plan

Explain purpose/access with Q01–Q04. Calculate success/failure/negative-input states in Q05, trace validation/counters in Q06–Q08, then check each P01 call.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 corrected transcript]] — 01:08:56, 01:04:10, 01:16:32, 01:14:06, 01:21:14, 01:24:58, 01:29:46.
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 corrected transcript]] — 00:55–01:51.

### Materials and page views

- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-061).
- [5 encapsulation.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-003), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-012), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-014), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-018), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-023).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-004).

Inheritance/polymorphism are motivational introductions; detailed overriding/dispatch and cross-package protected receiver rules remain later scope. AppleStore's unmodified methods assume the same package. ChangableVar omits getReadHistory implementation, so its intended trace is analyzed without treating it as a complete program; the lecture skipped its detailed walk-through.


---

[[courses/computer_programming/units/en/objects-references|← Previous: Objects, Constructors, Static Members, and Reference Passing]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/lab-applications|Next: Input Validation, Board Evaluation, and Object Interaction Labs →]]
