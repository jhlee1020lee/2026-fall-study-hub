---
title: "Inheritance, Casting, Overriding, and Construction"
description: "Review inheritance design, overloads, overrides, hiding, casts, initialization, and access."
course: "computer_programming"
unit_id: "inheritance"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["6 inheritance 1.pdf"]
private_source_assets: []
source_lectures: []
---

Check whether a reuse relationship preserves both parent operations and the child's meaning. Trace calls, fields, casts, and construction using their separate selection rules.

## Inheritance and composition: choosing a relationship for reuse

Copying similar classes makes a common change require edits to several copies. Inheritance defines a more specific class from an existing one, reusing common functionality and adding differences. Parent, superclass, and base class describe one side of this relationship; child, subclass, and derived class describe the other. The detailed rules here are **materials-only study from RM001, Inheritance 1**. They do not establish a new recording or a particular taught date. The access boundaries in [Encapsulation](encapsulation.md) and [Packages](packages.md) provide the foundation.

RM001 pp.4–5 begin with repeated declarations of `Lecture`'s `hasTA = true`, `hasExams = true`, and `hasAssignments = false`. `CSLecture extends Lecture` adds `isHard = true`; `CPLecture extends CSLecture` adds `isExciting = true`. Common definitions can now reside in one place. However, redeclaring `hasAssignments = true` in the child creates a separate field that hides the parent's field; it does not globally change the inherited declaration. These fictional class names and boolean values are not facts about this semester's assignments, exams, or difficulty.

The diagrams on [RM001 PDF pp.7–9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-009) compare three expansion strategies. Replacing `A` with `A′` can break the connections of existing users. Copying `A` creates similar but separate implementations to maintain. The final diagram retains `A` and its users, adding a dotted inheritance connection from `A′` to `A`. This motivates incremental extension. Maintainability, consistency, development efficiency, and reliability are design aims of reuse, not automatic consequences of writing an inheritance declaration.

### Checking behavior behind “is-a” and “has-a”

A `CarOwner` is a `Person`, so inheritance can express that is-a relationship. Owning a car is a has-a relationship, represented by composition: keeping a `Car` in a field. It does not require `CarOwner extends Car`. [RM001 PDF pp.17–18]

Even mathematical inclusion is insufficient. The `Circle extends Ellipse` example on p.19 initializes both axes to the radius but inherits independent `stretchX()` and `stretchY()` operations. In an **explanatory calculation**, a circle with axes `(2, 2)` stretched by a factor of two on X alone becomes `(4, 2)`, violating the circle's invariant. A subtype must retain its meaning while supporting the operations exposed by the parent. Merely having similar fields can conceal this problem.

## `extends` and one direct superclass

`class Child extends Parent` declares a relationship through which accessible parent members can be inherited. In RM001 p.15, `Parent` contains `int var = 123;` and `func()`, which prints `Parent`. `Child` extends it with an empty body. Within this same-package example, both `parent.func()` and `child.func()` print `Parent`, and each object's `var` reads as `123`. An empty child declaration can therefore still expose inherited behavior. It does not grant direct access to private members.

| Hierarchy | Meaning | Number of direct parents |
|---|---|---|
| Single: `A → B` | B extends A | One for B |
| Multilevel: `A → B → C` | B is both a child and a parent | One at each step |
| Hierarchical: B, C, D below A | One parent has several children | One for each child |

Several levels or several children are different from several direct parents for one class. An ordinary class without an explicit superclass connects to `Object`; `Object` itself has no superclass. `toString()` provides a string representation, and `getClass()` returns the `Class` object representing the actual class. The next chapter develops `equals()` and `hashCode()`. Not every method listed on RM001 p.21 can be overridden: `getClass()`, for example, cannot. Detailed use of `wait`, `notify`, `finalize`, and `clone` remains outside this scope.

`class C extends A, B` on RM001 pp.26–28 is a deliberately invalid Java example. In that example, `D.f()` sets `var` to `1`, `A.f()` sets it to `2`, and `B.f()` sets it to `3`. It illustrates conflicting parent implementations, but the declaration of `C` itself is illegal. Neither `2` nor `3` can be selected as an actual execution result of that source. Implementing several interfaces is a separate mechanism. The classification diagram places `Character` under `Object`, then `Digit` and `Letter`, and `Vowel` and `Consonant` under `Letter`. This is a classification analogy, not a listing of Java library inheritance.

## Overloading and overriding ask different questions

Overloading supplies different parameter lists under one method name. Overriding replaces an inherited instance method's implementation in a child class. `Point.move(int dx, int dy)` and `Point3d.move(int dx, int dy, int dz)` on RM001 p.16 have different numbers of arguments. The latter adds a three-coordinate operation; it does not replace the two-argument operation with the same signature.

### Limiting movement with `SlowPoint`

`SlowPoint` on RM001 p.31 defines the same two-argument `move(int,int)` as its parent. It limits the requested displacement, then delegates the actual coordinate update to `super.move()`. This is the child portion of that general teaching example:

```java
class SlowPoint extends Point {
    int xLimit = 10, yLimit = 10;
    void move(int dx, int dy) {
        super.move(limit(dx, xLimit), limit(dy, yLimit));
    }
    static int limit(int d, int limit) {
        return d > limit ? limit : d < -limit ? -limit : d;
    }
}
```

`limit(20,10)` is `10`, and `limit(-12,10)` is `-10`. Consequently, an **explanatory trace** requesting `move(20,-12)` from the origin ends at `(10,-10)`. The boundary values `10` and `-10` remain unchanged. These results follow from the printed expression; they are not additional recovered speech or an execution receipt.

`@Override` tells the compiler that the programmer intends to override a method, helping expose an incorrect signature. The annotation does not create an object or call the method. In RM001 p.33, calling `printName()` on separate `Parent` and `Child` objects prints `Parent` and `Child`. Sharing a name alone does not establish compliance with all return-type and access rules; the full declarations matter.

Separate **which signature is selected** from **which overriding body executes for that signature**. The recalled 2026-1 final question 9 combines these decisions with `int` and `double` arguments. First inspect the overloads available through the reference's declared type and the argument types. Then find the actual object's override of the selected instance method. Field access does not enter that second step. This transfers the question's reasoning demand without reproducing its private program or answer. [EX:cp_2026_1_final_q09 p.6]

## Field and static hiding versus dynamic dispatch

Treating hiding and dynamic dispatch as one rule makes casts particularly confusing. RM001 pp.34–39 distinguish them:

| Target | Selection basis | Does a child object always select the child's declaration? |
|---|---|---|
| Field | The access expression's compile-time type | No. |
| `static` method | Type-based name resolution | No. |
| Overridden instance method | The actual receiver, for the selected signature | The applicable child override executes. |

With `Super s = new Sub();`, a static `s.greeting()` selects `Super`'s `Goodnight`, while the instance call `s.name()` uses `Sub`'s override. Sharing one reference does not make those selection rules identical. Reading a static call using its class name helps make its ownership clear. [RM001 PDF p.35]

For fields, suppose `Point.x` is `int 2` and `Test.x` is `double 4.7`. Inside `Test`, `x`, `super.x`, and `((Point)this).x` produce `4.7`, `2`, and `2`. The cast changes the expression's type; it neither changes the object nor removes the child field. By contrast, in `T1 → T2 → T3`, where instance `s()` methods return Strings `"1"`, `"2"`, and `"3"`, calls to `s()`, `((T2)this).s()`, and `((T1)this).s()` on a `T3` receiver all return `"3"`. **Casting to a parent type does not undo an override.**

The “Hiding Variables” sketch on RM001 p.36 omits `extends Parent` from `Child`. As printed, it shows independent classes with values `123` and `456`, not an executed inheritance-hiding example. Page 38's `Test extends Point` supplies the actual inheritance relationship used in the field trace.

## Upcasts and downcasts preserve the object

An upcast treats a child object through a parent-typed reference. `Parent p = new Child();` does this implicitly; an explicit `(Parent)` does not create another object. The declared type limits which members are available, while overridden instance behavior still follows the actual `Child`. [RM001 PDF pp.40–42]

A downcast explicitly asks to use an object through a more specific type. The actual object must belong to that type or one of its subclasses. In RM001 p.44, a `Parent` reference points to a `Sister`: `print()` therefore prints `Sister`, and a `Sister` cast is appropriate. A `Brother` cast does not match that object and is a `ClassCastException` case. Independently, the printed source names both local variables `sister`, so the unchanged block also has a duplicate-declaration error. The runtime lesson must be separated from that compilation defect.

`instanceof` checks whether an object is an instance of the tested type. [RM001 PDF pp.22–23]

| Actual object | `instanceof Parent` | `instanceof Child` |
|---|---|---|
| `new Parent()` | `true` | `false` |
| `new Child()` | `true` | `true` |
| `null` | `false` | `false` |

The same class also satisfies the test; the rule is not restricted to strict descendants. A `MyClass` instance satisfies both `MyClass` and `Object`, and the example's `String` and `Integer` references also satisfy `Object`. `Integer integer = 3` introduces a wrapper reference, rather than applying `instanceof` to the primitive value `3`. Runtime checking does not mean that compilation performs no type checking: the compiler also checks whether the cast is type-compatible in principle.

## `super`: selecting parent behavior and initialization

`this` refers to the current object. `super` provides a context for selecting a parent-side declaration or implementation for that object. It neither creates a separate parent object nor unlocks private access.

On RM001 p.45, the parent declares `var = 123` and the child declares `var = 456`. `child.var` is `456`, while the child's `getParentVar()` returns `super.var`, or `123`. On p.46, `Child.printName()` prints only `Child`; a separate `printParentName()` invokes `super.printName()`. Calling those two methods in order prints `Child`, then `Parent`. Do not merge them into an override that originally contained both operations.

In the earlier `T3` example, `s()` returns `"3"`, `super.s()` invokes immediate parent `T2` and returns `"2"`, while `((T2)this).s()` still returns `"3"`. Ordinary dispatch differs from an explicit parent-body call. Java does not support `super.super.Print()`. In RM001 p.53, `Child.Print()` calls `super.Print()`, and `Parent.Print()` in turn calls `super.Print()`, producing `Grand` followed by `Child`. This is a path provided by the parent, not a prohibition on using every member inherited from a grandparent. Preserve the source identifier's capital `Print`.

When applying this distinction to recalled 2025-1 midterm question 5, separate **the current-object expression**, **parent field/body selection**, and **constructor delegation**, rather than merely listing keyword definitions. [EX:cp_2025_1_midterm_q05 p.3]

### Constructor order and the conflicting `color` values

Constructing a child initializes its parent portion first in the displayed examples. RM001 p.48 prints `Parent` from the parent constructor before `Child` from the child. Page 49's `Geometry` supplies both a parameterized constructor and a no-argument constructor setting `dimension = 3`. The empty `Point()` in that example implicitly invokes the accessible no-argument constructor through `super()`. Such a constructor does not automatically exist in every possible parent class. `this(...)` delegates to another constructor of the same class, whereas `super(...)` connects to parent initialization.

The code on RM001 p.50 has `Point()` assign `x = 1; y = 1;` and `ColoredPoint` declare `int color = 0;`. The chain reaches `Object`, then returns through parent initialization before the child field initializer. **The final state of the p.50 code is `(x,y,color) = (1,1,0)`.** The [order explanation on p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051) instead prints `color = 0xFF00FF`. Preserve the order lesson and disclose the conflicting value; the p.50 initializer does not somehow transform itself into `0xFF00FF`.

Recalled 2026-1 final subquestion 1-(c) uses this constructor distinction. Within the supplied material's language context, check both whether `this(...)`/`super(...)` is explicit and whether an accessible parent no-argument constructor exists. This is not a claim about every constructor syntax in current Java. [EX:cp_2026_1_final_q01c p.1]

## Access boundaries continue through inheritance

The example where `Rectangle.getArea()` multiplies `Shape`'s protected `height` and `width` shares state without exposing it to every caller. An override must not narrow access: a public method remains public, while a protected method can remain protected or become public. A package-access method can be overridden with the same or wider access where it is actually inherited. [RM001 PDF pp.55–56]

In the counter example, `Point.move()` adds to the coordinates and increments `useCount` and `totalUseCount`; `PointBack.moveBack()` subtracts from the coordinates and increments both counters. `useCount` belongs to each instance, while `static protected totalUseCount` accumulates calls across instances. An individual object's count need not equal the shared total. [RM001 PDF p.57]

Across packages, `ComplexAlgebra.C` declares protected `real`, `add`, and `multiply`, but package-access `imag`, `angle`, and `radius`. `RealAlgebra.R extends C` initializes with `super(value, 0)` and uses inherited `real` to represent the real component; it cannot directly use the package-access members. The `...` in `multiply` is an omitted implementation. Cross-package protected access belongs to the subclass's inheritance context, not unrestricted access through arbitrary parent receivers. [RM001 PDF pp.59–60]

Recalled 2025-1 midterm question 4 uses a diagram spanning two packages and a subclass. Analyze the declaration location, the accessing code's package, the subclass relationship, and the receiver type in turn. “A child can always access protected members” is not a sufficient table entry. This is historical recalled material, not a verified official paper or answer key. [EX:cp_2025_1_midterm_q04 p.2]

### Parent methods can still change private state

Inaccessibility of a parent's private field does not make that state disappear. `Point.move()` on RM001 p.61 can increment its own private static `totalMoves`. When `Point3d` invokes `super.move(dx,dy)`, parent code legally updates the counter, but a direct `totalMoves++` in the child is an access error. On p.63, a parent method similarly updates private `x` and `y`, while the child updates its own private `z`.

The two private `makeMoney()` methods in `Parent` and `Child` on p.64 return `100` and `0` respectively. They are independent private methods, not overrides. Reusing an accessible parent operation is different from directly accessing the parent's private implementation.

## `final`: restricting extension, overriding, or reassignment

The meaning of `final` depends on its target. [RM001 PDF pp.65–68]

| Target | Change it forbids | What can still happen |
|---|---|---|
| `final class ColoredPoint` | Extending that class again | Its objects can be used. |
| A final instance method | Overriding it in a child | It can be inherited and called. |
| A static final method | Hiding it with the same signature | It can be called where accessible. |
| An initialized final variable | Reassigning another value | For a reference, separately mutable object state can still change. |

The declaration `static final Point origin = new Point(0, 0);` fixes a shared reference. `p.origin = new Point(-1,-2)` tries to assign another reference and is invalid. A fixed reference does not make all of the pointed-to `Point`'s mutable `x`, `y`, and `useCount` state immutable. Distinguishing object identity, object state, and class extension prevents treating `final` as a universal protection mechanism.

## Key Takeaways

- An is-a design must preserve the child's meaning under parent operations; has-a is represented by composition.
- Selecting an overload signature and dispatching an instance override are separate steps. Fields and static methods use type-based selection.
- Casts preserve the object. A `super` body call differs from an ordinary call through a parent cast.
- Trace parent initialization before child initialization and check whether the needed parent constructor is accessible.
- Inheritance retains access boundaries; overrides cannot narrow access. A final reference does not make an entire object immutable.

## Recall and Practice

### Relationships and call selection

#### Recall Q01 · Reuse and invariants

(a) Compare modifying, copying, and extending A, including parent/child terminology. (b) Distinguish CarOwner's is-a and has-a relationships. (c) Explain the Lecture field redeclaration and the Circle single-axis counterexample.

<details><summary>Show solution</summary>

(a) Replacing A may break existing users; copying creates similar implementations to maintain; keeping A and extending it supports incremental reuse without automatically guaranteeing safety. Parent/superclass/base and child/subclass/derived name the relationship's sides. 

(b) A CarOwner is a Person but has a Car, so distinguish inheritance from a Car field. 

(c) The Lecture hierarchy shares common fields, but redeclaring `hasAssignments=true` hides a separate parent field rather than changing it globally. These fictional values are not semester policy. Stretching only X of a `(2,2)` Circle by two gives `(4,2)`, breaking its equal-axis invariant.

**Checking points:** Check the three extension choices, both relationships, field hiding, and the axis calculation.

</details>

#### Recall Q02 · Direct superclass and hierarchy

Can an empty `Child extends Parent` use the same-package `var=123` and `func()`? Compare single, multilevel, and hierarchical inheritance, Object, and invalid `extends A,B`.

<details><summary>Show solution</summary>

Accessible inherited members remain usable: each object's var is 123 and both func calls print Parent. Single is A→B; multilevel is A→B→C; hierarchical branches below A, still with one direct parent per child. Ordinary classes connect to Object, which itself has no superclass. `toString()` provides a representation and `getClass()` the actual class's Class object; `getClass()` cannot be overridden. Although the diamond sketch assigns 1/2/3 in D/A/B, C's `extends A,B` declaration is illegal, so 2 or 3 is not an actual output. Multiple interfaces are separate. The Character classification is an analogy, not a library hierarchy.

**Checking points:** Check inherited access, direct-parent count, the illegal declaration, and the Object qualification.

</details>

#### Recall Q03 · Overloading and limited movement

Distinguish `Point3d.move(int,int,int)` from `SlowPoint.move(int,int)`. Trace `(20,-12)` from the origin and check ±10 boundaries. What does `@Override` do?

<details><summary>Show solution</summary>

The three-argument method adds an overload distinct from the parent's two-argument signature. SlowPoint overrides the same two-argument instance method, limits each displacement to [-10,10], and passes it to `super.move`. Thus 20→10 and -12→-10 yield `(10,-10)`; ±10 stay unchanged. `@Override` asks the compiler to check overriding intent, not to create or call anything. The separate Parent/Child printName example prints Parent then Child. A matching name alone does not establish valid return and access rules.

**Checking points:** Check signatures, both limits, parent updating, and annotation purpose.

</details>

#### Recall Q04 · Field, static, and instance selection

For `Super s=new Sub()`, which declaration supplies static `greeting()` and overridden `name()`? Trace Test's `x=4.7`, Point's `x=2`, and parent casts of a T3 receiver.

<details><summary>Show solution</summary>

`static` greeting uses Super and returns Goodnight; instance name uses the actual Sub override. Inside Test, `x`, `super.x`, and `((Point)this).x` give `4.7,2,2`. Field selection follows expression type; a cast does not remove the child field or change the object. With T1/T2/T3 instance s methods returning strings 1/2/3, direct and T2/T1-cast calls on a T3 object all return `"3"`. Casting cannot cancel overriding. RM001 p.36 omits extends in Child, so it shows independent classes rather than executable inheritance hiding.

**Checking points:** Explain all three selection rules and why field and instance casts differ.

</details>

### Casts and initialization

#### Recall Q05 · Casts and the actual object

For `Parent p=new Sister()`, assess Parent/Sister tests and a Brother cast. Explain the four Parent/Child `instanceof` combinations, null, wrappers, and compile/runtime checks.

<details><summary>Show solution</summary>

Both Parent and Sister tests are true. A Brother cast cannot transform a Sister and is a runtime ClassCastException case; the printed p.44 block additionally has a duplicate local name, so it is not an unchanged execution trace. A new Parent tests true for Parent and false for Child; a new Child tests true for both. Null tests false. Upcasting can be implicit, preserves identity, and restricts visible members. A downcast requires the actual object to match the target or its subclass; compilation also checks type compatibility in principle. MyClass/String/Integer objects are Objects; `Integer integer=3` denotes a wrapper reference, not primitive instanceof.

**Checking points:** Distinguish actual type, null, same-type tests, compilation defects, and runtime failure.

</details>

#### Recall Q06 · super and parent bodies

Compare parent var 123/child var 456, separate printName/printParentName, and T3's direct/super/parent-cast s calls. How does the material connect the grandparent instead of using `super.super.Print()`?

<details><summary>Show solution</summary>

Child's field is 456; getParentVar selects `super.var=123`. Child.printName prints only Child, while the separate printParentName calls the parent body and prints Parent. T3's direct, super, and parent-cast calls give `"3","2","3"`. `this` denotes the current object; super selects a parent-side context for it, without creating another object or unlocking private access. `super.super.Print()` is unsupported. The explicit Child.Print → Parent.Print → Grandparent.Print path prints Grand then Child; it does not prohibit every inherited grandparent member.

**Checking points:** Separate fields, bodies, the current object, and the immediate-parent path.

</details>

#### Recall Q07 · Initialization order and discrepancy

When can Point's empty constructor call Geometry successfully, and how do `this(...)` and `super(...)` differ? Give Parent/Child output order and compare p.50's ColoredPoint final state with p.51.

<details><summary>Show solution</summary>

Geometry supplies an accessible no-argument constructor setting dimension to 3, so the empty Point constructor can use implicit super(). Not every parent automatically has such a constructor. `this(...)` delegates within the same class; `super(...)` delegates parent initialization. The simple example prints Parent before Child. In p.50, the chain reaches Object, returns through Point setting x=y=1, then sets the child color to 0: `(1,1,0)`. Page 51's 0xFF00FF is a conflicting printed value, not a transformation caused by initialization order.

**Checking points:** Check parent-constructor existence/access, order, all three final values, and the discrepancy.

</details>

### Access boundaries

#### Recall Q08 · Access, counters, and overrides

(a) Explain Shape/Rectangle's protected state and override access. (b) Starting with a shared count of zero, find the counts after PointBack A moves twice and B once. (c) Explain cross-package C/R access and initialization.

<details><summary>Show solution</summary>

(a) Rectangle can multiply inherited protected height and width. A public override stays public; protected may stay protected or become public; a package method must actually be inherited before overriding with equal/wider access. 

(b) Instance useCount values are A=2 and B=1, while static totalUseCount=3. move adds coordinates and moveBack subtracts, but both increment counts. 

(c) Cross-package R can use C's protected real/add/multiply in its inheritance context, not package-access imag/angle/radius. `super(value,0)` initializes the parent portion. `protected` access is not unrestricted through arbitrary parent receivers; multiply's ellipsis omits implementation.

**Checking points:** Check per-object/shared counts, non-narrowing overrides, and protected versus package access.

</details>

#### Recall Q09 · Parent-private state

Why can Point3d change parent-private x/y or totalMoves through `super.move` but not directly? Are the two same-named private makeMoney methods overrides?

<details><summary>Show solution</summary>

The accessible parent method body may access its own private state. The child delegates x/y and parent-counter updates to it, while directly updating only its own private z. A child-side totalMoves++ is an access error. Privacy does not erase parent-managed state or forbid normal operations. Parent's private makeMoney returning 100 and Child's private method returning 0 are independent methods, not dynamic overrides.

**Checking points:** Check legal operation calls versus direct access and the absence of private overriding.

</details>

#### Recall Q10 · Targets of final

What does final prohibit on a class, instance method, static method, and initialized reference variable? Are reassignment and state mutation equivalent for static final Point origin?

<details><summary>Show solution</summary>

A final class cannot be extended; a final instance method cannot be overridden; a static final method cannot be hidden with the same signature. Inheriting and calling an accessible method remains possible. An initialized final variable cannot be reassigned, so assigning a new Point to origin is invalid. The reference's final status does not itself forbid modifying the existing object's mutable x/y/useCount. `static` ownership and final reassignment restrictions are separate.

**Checking points:** Judge extension, overriding, hiding, reassignment, and mutation separately.

</details>

### Application practice

#### Practice P01 · Signature before body

New synthetic practice transfers overload→override reasoning from [EX:cp_2026_1_final_q09 p.6] and explicit parent-body reasoning from [EX:cp_2025_1_midterm_q05 p.3]. Prerequisites Q03–Q06 are current. In one package, Base.f(int) returns `"I"`, Base.f(double) returns `"D"`, and Sub overrides only the double version to return `"S"`. Sub.parentValue() returns super.f(2.0). For `Base b=new Sub()`, trace b.f(2), b.f(2.0), ((Base)b).f(2.0), and ((Sub)b).parentValue().

<details><summary>Show solution</summary>

Results: `I,S,S,D`. The int argument selects the int signature, whose inherited Base body remains. The double argument selects double, then dispatches to the Sub override. The Base cast preserves the object, giving S again. The actual Sub makes the downcast valid; parentValue's explicit super call selects Base's double body and returns D. The exercise changes the overridden signature and combines it with parent delegation rather than merely replacing constants.

**Checking points:** For each value, identify the selected signature and executed body.

</details>

#### Practice P02 · A subclass moved across packages

New synthetic practice combines package/inheritance access from [EX:cp_2025_1_midterm_q04 p.2] with constructor prerequisites from [EX:cp_2026_1_final_q01c p.1]. Prerequisites Q07–Q09, within the material's Java context. `public` Base supplies only public Base(int n), a protected value field, package-access helper(), and private hidden. In Sub extends Base in another package, assess an empty constructor, this.value, helper(), and direct hidden access. Explain the minimal direction for constructor delegation.

<details><summary>Show solution</summary>

The empty constructor needs an accessible Base(), which does not exist. Delegate a suitable int through `super(n)` rather than assuming an unseen no-argument constructor. Access to this.value inside Sub is allowed in the protected inheritance context. helper() is not accessible across packages and hidden remains private. Fixing constructor delegation does not fix these independent access failures. Do not generalize this.value access to arbitrary Base receivers.

**Checking points:** Separate constructor and three member judgments and explain the package boundary.

</details>

### Short review plan

Compare casts with super in Q04/Q06, then solve P01. Next day, use Q07/Q08 and P02 to check constructibility separately from accessibility.

## Sources

This is materials-only study of Inheritance 1, without a new recording or assigned taught date. Preserve missing extends on p.36, duplicate local naming on p.44, and the pp.50–51 color discrepancy. Keep protected receiver limits and the supplied constructor context; detailed Object concurrency/cleanup APIs remain outside scope.

### Materials and relevant pages

- [6 inheritance 1 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-005), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-009), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-017), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-028), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-036), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-053), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-056), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-057), [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-061), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-063), [p.64](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-064), [p.65](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-065), [p.66](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-066), [p.67](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-067), [p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-068)

### Scope of exam connections

These are historical recalls, not verified official papers, answer keys, or predictions for this term. No official answer key is supplied; check the new solutions using their stated reasoning. The final recall's order, accuracy, and missing-question limits remain.

- [EX:cp_2026_1_final_q09 p.6] · [[exam_questions/cp_2026_1_final_q09|existing question preview]]

- [EX:cp_2025_1_midterm_q05 p.3]

- [EX:cp_2026_1_final_q01c p.1]

- [EX:cp_2025_1_midterm_q04 p.2]
