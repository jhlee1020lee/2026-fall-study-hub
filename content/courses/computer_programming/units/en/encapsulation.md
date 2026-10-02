---
title: "Encapsulation, Access Control, and State Design"
description: "Review access levels, consistent state changes, null checks, and getter/setter effects."
course: "computer_programming"
unit_id: "encapsulation"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["4 oop.pdf", "5 encapsulation.pdf", "Lab03 v2.pdf", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

Learn to design permitted access together with valid state changes. Trace sales, string validation, and access logging, checking both the result and the state left behind.

## Encapsulation: making an object responsible for its state changes

If using an object requires knowing every internal field and method, a small implementation change can disturb all its callers. Encapsulation bundles state and behavior while exposing the interactions that callers need. A driver needs to use the steering wheel and accelerator without understanding every engine component. Abstraction reduces the complexity of using something; defensive programming restricts unexpected changes to its state. Hiding an implementation primarily means **designing permitted access paths**, rather than keeping the existence of its source code secret. [Computer Programming M012 PDF pp.4–7]

The September 15 lecture extends this idea to people implementing a robot's arm, head, and chest. Each contributor can depend on agreed operations and results instead of understanding every other component's implementation. This motivates cooperation through an interface; it does not remove the need to verify the parts. Here, “interface” means a general interaction boundary, not yet a Java `interface` declaration. The unclear numerical expression in the [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 transcript, 01:08:56–01:09:54]] does not establish a percentage. The related explanation remains available in the [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|September 15 lecture notes · Encapsulation]].

The capsule diagram on M011 p.59 groups variables and methods within a class. M012 p.3 contrasts complicated machinery with a simple control panel. Together, the figures distinguish putting code in one container from exposing only the controls a user needs. A repairer needs different internal information from someone using the normal operation.

### Two values that must change in one sale

`FruitStore` starts with `balance = 10000` and `stock = 30`. Selling three fruits at `2000` each should make both changes:

\[
\text{stock}'=30-3=27,\qquad
\text{balance}'=10000+2000\times3=16000.
\]

If external code writes the two fields directly, it must know the sale rule and can accidentally reduce stock without collecting payment. M012 p.5 gathers the two assignments into one operation. This is the teaching example's sale method, not a complete commercial system.

```java
void sell(int num) {
    balance += 2000 * num;
    stock -= num;
}
```

The caller can now request `sell(3)`. Adding a method alone, however, does not prevent callers from bypassing it while the fields remain exposed. `AppleStore` makes the fields `private`, provides `getBalance()` and `getStock()` for reading, and uses `sell()` for changes. Knowing a value and being allowed to assign any value are different permissions. Getters preserve that distinction. [M012 PDF pp.11–12]

The displayed methods do not have `public` modifiers. They actually have package-private access. The lecture assumes that the example code is in the same package and occasionally calls these operations public for convenience. That spoken shortcut must not become a different declaration in the reader's understanding. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 transcript, 01:16:32–01:18:17]]

## Access control: choosing the permitted paths

An access modifier determines whether a member can be used from a particular location. M012 p.10 declares `private int weight = 80;`. Reading that field directly from a separate external class produces a private-access error. The value exists; the access is not permitted.

| Form | Meaning at this level | Important qualification |
|---|---|---|
| `private` | Access within the declaring class | Knowing the field's name does not authorize external access. |
| No modifier | Access within the same package | There is no written `default` access keyword here. |
| `protected` | Same-package access and access in a subclass's inheritance context | A subclass in another package does not gain unrestricted access through arbitrary parent objects. |
| `public` | The member is exposed externally | Its containing class must also be accessible. |

This is a starting model for member access, not a rule that all four modifiers apply equally to top-level classes. [Packages](packages.md) develops namespaces and top-level class access; [Inheritance](inheritance.md) develops access from subclasses in other packages. [M012 PDF pp.9–10]

### Returning failure while preserving state

Even a permitted method can create an invalid state. Selling `50` items unconditionally from stock `30` would make the stock negative. M012 pp.13–16 introduce the private helper `inStock(int num)`. It computes `shortage = num - stock`, returns `false` if the result is positive, and otherwise returns `true`. The revised sale changes both fields only when the check succeeds.

```java
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

For `sell(50)`, `50 - 30 = 20`, so the sale fails. It returns `false`, leaving `balance = 10000` and `stock = 30`. The source's caller uses that result to print `Not enough apples in stock`. Printing a message in the caller and returning an outcome from the sale method are separate responsibilities. Changing the return type from `void` to `boolean` lets the caller distinguish requesting a sale from successfully completing one. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 transcript, 01:20:14–01:22:07]]

This helper is not complete input validation. As a **boundary case derived from the printed code**, `sell(-1)` from the initial state produces `shortage = -31` and passes the check. The resulting balance is `8000` and stock is `31`. The source has no condition rejecting a negative order. This is an explanatory code trace, not an additional statement recovered from the lecture. Encapsulation concentrates responsibility for validation; it does not automatically supply the correct validation rules.

## Getters and setters: separating reading, validation, and tracing

A getter and a setter are ordinary methods named and designed for particular roles, not special Java syntax. In M012 p.18, `getAge()` returns `age`; `setAge(int age)` uses `this.age = age` to assign its parameter to the current object's field. Every private field does not need both methods. Exposing only a getter creates a read-only path; exposing only a setter creates a write-only path. These descriptions concern the external interface, not a prohibition on changes within the class. The earlier `sell()` directly updates its own class's private fields.

A setter can validate before assignment, and either kind of method can record access. The age example at September 15 01:24:58–01:25:52 motivates rejecting inappropriate values. Mentioning negative or extremely large ages does not define an official numerical acceptance interval. [[courses/computer_programming/transcripts/2026-09-15|September 15 transcript · selective access and validation]]

### Why a null check precedes the empty-string check

`Person.setName` in M012 p.21 tests `name == null || name.equals("")`. A `null` reference does not designate an object; `""` is an empty String. The first expression checks the reference, while the second compares string content. With short-circuit evaluation, `||` skips its right operand when the left is true. Consequently, it does not call `equals()` on a null receiver. Reversing the tests is unsafe: a later null check cannot prevent an earlier failing call. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 transcript, 01:26:50–01:28:49]]

The lecture's address-zero description is a simplified model. The relevant meaning is that there is no object to receive the call; Java's `null` is not being specified as a guaranteed physical address.

Lab04 applies the same idea to a `Book` title. The following general instructional example appears on [NM003 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-009), with the same code in NM002 v2 p.8. This Lab04 extension is **materials-only study**, with no new recording or assigned taught date.

```java
class Book {
    private String title;

    public void setTitle(String title) {
        if (title == null || title.equals("")) {
            System.out.println("Title cannot be null or empty");
        } else {
            this.title = title;
        }
    }

    public String getTitle() {
        return title;
    }
}
```

Because the new object's field has no explicit initializer, `title` initially contains `null`. This explanatory trace follows the exact predicate:

| Step | Input or operation | Subsequent `title` | Reason |
|---|---|---|---|
| Immediately after creation | `getTitle()` | `null` | No title has been stored. |
| First assignment | `setTitle("Java")` | `"Java"` | Both rejection tests are false. |
| Rejected assignment | `setTitle("")` | `"Java"` | The error branch does not assign the field. |
| Another rejection | `setTitle(null)` | `"Java"` | Short-circuit evaluation leads to rejection and preserves the old value. |
| A space | `setTitle(" ")` | `" "` | One space is not an empty string. |

Automatically trimming or rejecting whitespace would introduce a stronger rule than this code contains. `getTitle()` itself does not change state here. Nevertheless, a getter's name alone does not guarantee that every getter is free of side effects.

### Reading can also update a history

The source class in M012 pp.22–23 is spelled `ChangableVar`. Its `setValue()` assigns the value, increments `countOfChange`, and prints the change number. Its `getValue()` increments `readHistory` before returning the value. Reading therefore changes the history state even though it does not change the watched value.

The intended trace is: first read `0` with history `1`; `setValue(52)` produces change `#1`; `setValue(53)` produces change `#2`; the second read returns `53` with history `2`. Setting the same value twice also increments twice because the setter never compares the old and new values. The counter measures **method calls**, which need not equal the number of actual value changes.

Page 23 calls `getReadHistory()`, but page 22 does not define it. The displayed trace describes the intended example, not a complete program that those pages form unchanged. At September 15 01:29:46, the lecturer motivates logging and debugging and skips the detailed traversal of the long example. [[courses/computer_programming/transcripts/2026-09-15|September 15 transcript · tracing access]]

## Reusing common state and providing different behavior

Encapsulation sets interaction boundaries. Inheritance reuses and extends characteristics across classes. Polymorphism provides different behavior behind a common operation. M011 pp.58–61 and M014 p.4 connect these ideas to abstraction, code reuse, and behavioral diversity respectively.

The diagram on M011 p.60 places `Animals` and `Plants` below `Organisms`, then `Duck`/`Cat` and `Tree`/`Grass` below those branches. Read this as more specific classes inheriting common characteristics. The lecture similarly uses adding a tail to `Cat` to explain extension; uncertain biological wording or method names are not reconstructed as verified facts.

For example, defining a `Cat` class using animal characteristics and adding another characteristic is different from creating several cat objects from that class. Dogs, cats, and ducks can provide different sounds through `animalSound()`. The caller relies on the common operation without having to know each sound in advance. This concerns different implementations, rather than merely two objects of one class holding different speed values. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 transcript, 01:03:16–01:04:10]]

The [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|September 17 lecture notes · OOP review]] and [[courses/computer_programming/transcripts/2026-09-17|September 17 transcript, 00:55–01:51]] also introduce these three features. That introductory recorded scope remains distinct from the later detailed syntax. The reuse, access, and construction rules in [Inheritance](inheritance.md), followed by call selection in [Object contracts and interfaces](object-contracts-interfaces.md), extend this foundation through supplied materials.

## Key Takeaways

- Encapsulation distinguishes permission to read from permission to assign arbitrary state, supporting abstraction and data protection.
- A successful sale changes related state together; failure preserves it. `private` alone does not validate input.
- Omitting an access modifier gives package access. Getters and setters are ordinary methods and can validate or log calls.
- Trace the exact predicate: null-first `||` protects the receiver, and an empty string differs from a space.
- Inheritance concerns class reuse; polymorphism concerns different implementations of a common request.

## Recall and Practice

### Access and state

#### Recall Q01 · Design boundary

Use the controls and robot-team analogies to distinguish abstraction from defensive programming. Does a getter destroy encapsulation by revealing a value?

<details><summary>Show solution</summary>

Controls expose the operations needed for use while hiding implementation complexity. Robot contributors likewise depend on agreed operations. Defensive programming restricts changes to permitted paths. Reading through a getter does not grant arbitrary assignment, so encapsulation remains. Neither analogy means keeping source code secret or skipping verification of collaborators' work.

**Checking points:** Explain reduced complexity, controlled changes, and the distinction between read and write permission.

</details>

#### Recall Q02 · Class relationships and objects

Distinguish reusing animal traits in `Cat` and adding a tail, constructing two cat objects, and providing different `animalSound()` behavior across animal classes.

<details><summary>Show solution</summary>

The first is inheritance: reusing and extending parent characteristics. The second creates distinct objects from one class. The third introduces polymorphism through class-specific implementations of a common operation. Two objects merely having different speed values is not the same explanation. The recordings introduce these motivations; detailed dispatch syntax belongs to the later materials.

**Checking points:** Distinguish class extension, object creation, and implementation diversity.

</details>

#### Recall Q03 · Related state changes

From `balance=10000`, `stock=30`, and price 2000, trace a sale of three items. Is adding `sell()` sufficient to prevent inconsistent external changes?

<details><summary>Show solution</summary>

`stock=27` and `balance=16000`: both updates belong to one sale. Collecting them in `sell()` prevents callers from having to repeat the rule, but exposed fields still permit bypassing that method. `private` state and controlled operations work together; getters provide observation. The printed sale/getter methods omit `public`, so their external calls rely on the same-package context.

**Checking points:** Check both values, the bypass risk, and the original package access.

</details>

#### Recall Q04 · Access levels

Explain the four member access levels. Why can a separate class not read `private int weight=80`, and should package access be written with `default`?

<details><summary>Show solution</summary>

`private` restricts access to the declaring class at this level; no modifier permits the same package; `protected` also supports the subclass inheritance context; `public` exposes the member externally. The weight exists but the read is forbidden. Package access has no written `default` keyword. Cross-package protected access is not unrestricted through arbitrary parent receivers, and a public member still needs an accessible containing class. Top-level classes do not accept all four member modifiers.

**Checking points:** Separate existence from permission and retain the protected-access qualification.

</details>

#### Recall Q05 · Failure and the negative boundary

The original helper fails only when `num-stock>0`. Starting independently from `(balance,stock)=(10000,30)`, trace `sell(50)` and `sell(-1)`, and explain the boolean result.

<details><summary>Show solution</summary>

`50-30=20` makes the first call return `false` and preserve `(10000,30)`; the caller can then print the failure message. For `-1`, the shortage is `-31`, so the printed check succeeds: return `true`, balance `8000`, stock `31`. A boolean replaces `void` to communicate success. Keeping the helper private hides its implementation, but does not supply the missing negative-order check. This boundary is derived from the code.

**Checking points:** Check preservation of both fields on failure and the calculation explaining negative-order acceptance.

</details>

### Validation and logging

#### Recall Q06 · Selective access and short-circuiting

Are getters/setters special syntax? Distinguish the two sides of `this.age=age` and explain why reversing `name==null || name.equals("")` is unsafe.

<details><summary>Show solution</summary>

They are ordinary methods named by convention. `this.age` is the current object's field; `age` is the parameter. Exposing only a getter or setter controls the external path, while internal methods can still access private state. With null first, a true left operand makes `||` skip `equals()`. Reversing the order calls a method on a missing object before the later test can help. Null is neither an empty String nor a guaranteed physical address zero. The age example motivates validation without defining an official interval.

**Checking points:** Check convention, parameter versus field, selective exposure, and evaluation order.

</details>

#### Recall Q07 · Logging side effects

Trace the first read, `setValue(52)`, `setValue(53)`, and second read in `ChangableVar`. What if the same value is set twice, and are the displayed pages a complete runnable program?

<details><summary>Show solution</summary>

The first read returns 0 with history 1; the setters report changes #1 and #2; the second read returns 53 with history 2. The getter changes logging state. Two same-value setter calls still increment twice because the body does not compare values. Thus the count measures calls, not necessarily actual changes. Page 23 calls `getReadHistory()`, absent from p.22, so this is an intended trace rather than evidence that the pages run unchanged. The recorded explanation skipped the long traversal.

**Checking points:** Separate value, read count, and setter-call count; identify the missing method.

</details>

#### Recall Q08 · Book rejection paths

Read a new `Book` title, then call `setTitle("Java")`, `setTitle("")`, `setTitle(null)`, and `setTitle(" ")`. Explain the value at every stage and the rejection rule.

<details><summary>Show solution</summary>

The initial field is `null`, then the values are `"Java"`, `"Java"`, `"Java"`, and `" "`. Empty and null inputs take the error branch, which does not assign; null is safely rejected by short-circuiting. A space does not equal the empty String, so it is accepted. This getter does not mutate the title. Do not infer trimming or whitespace rejection. This Lab04 extension is materials-only study.

**Checking points:** Check the initial value, preservation on rejection, and acceptance of a space.

</details>

### Application practice

#### Practice P01 · Is the change accessible?

New lecture-based general practice. The candidate involving package/subclass access is treated in Inheritance, not as direct style evidence for this state-preservation exercise. Prerequisites: Q03–Q05. A separate same-package `Cashier` tries to assign the original `AppleStore.stock` directly and to call `sell(50)`. Which access is allowed, and what remains after the permitted call fails?

<details><summary>Show solution</summary>

Direct field assignment is forbidden by `private`. The unmodified `sell(50)` is callable from the same package, but with stock 30 it returns `false` and leaves balance 10000 and stock 30. Accessibility and successful execution are separate decisions. This does not solve the historical question's full cross-package subclass table.

**Checking points:** Give separate access and state judgments and check both fields.

</details>

#### Practice P02 · Validation and logging

New lecture/material-based general practice; the candidate index does not establish this combined validation/logging style. A colleague claims that getters always preserve all state and that a null/empty check also rejects whitespace. Refute each claim using the different examples in Q06–Q08 and name the observations to check.

<details><summary>Show solution</summary>

`ChangableVar.getValue()` increments `readHistory` even if the watched value stays unchanged. `Book.setTitle(" ")` stores the space because it is not empty. Observe history in the first case and the returned title in the second. Method names and reassuring descriptions cannot replace tracing the actual fields and predicate.

**Checking points:** Connect each counterexample to its observable state and its code-level reason.

</details>

### Short review plan

Retrace Q03, Q05, and Q08 without the tables, then explain access using Q04. Next day, revisit Q07 and P02 to check that method names are not substituting for side-effect analysis.

## Sources

Connect the September 15 access/validation explanation with September 17's OOP introduction. The Lab04 Book extension is materials-only, without a recording. Unclear proportions and biological wording remain uncertain; retain ChangableVar's missing method and AppleStore's negative-order limitation.

### Dated notes and transcripts

- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · lecture notes]]

- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · lecture notes]]

- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 · corrected transcript · 01:03:16–01:04:10; 01:08:56–01:09:54; 01:16:32–01:18:17; 01:20:14–01:22:07; 01:24:58–01:29:46]]

- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 · corrected transcript · 00:55–01:51]]

### Materials and relevant pages

- [4 oop · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-061)

- [5 encapsulation · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-018), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-023)

- [Lab03 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-004)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-008)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-004), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-009)

Without a direct indexed exam-style match, P questions are presented as lecture/material-based general practice.
