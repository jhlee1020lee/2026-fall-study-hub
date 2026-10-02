---
title: "Dynamic Binding, Object Contracts, Interfaces, and Abstract Classes"
description: "Review binding, Object contracts, List and Comparable, and interface/abstract-class design."
course: "computer_programming"
unit_id: "object-contracts-interfaces"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["7 inheritance 2.pdf", "6 inheritance 1.pdf"]
private_source_assets: []
source_lectures: []
---

Distinguish implementation selection from contracts for representation, equality, and ordering. Recall how interfaces and abstract classes divide common operations and shared state.

## Binding: distinguishing the callable method from its executed body

Using different objects through one reference type requires a common calling contract while allowing behavior to follow the actual object. Binding describes how a method call connects to an operation. The distinction between declared type and actual object from [Inheritance](inheritance.md) is the starting point. This chapter is **materials-only study** from NM001, Inheritance 2, with the necessary RM001 prerequisites. It does not establish a new recording or a particular taught date.

NM001 pp.4–7 retain these reference declarations while changing the method declarations:

```java
Parent parent = new Parent();
Parent child = new Child();
```

| Declaration of `print()` | `parent.print()` | `child.print()` | Explanation |
|---|---|---|---|
| A `static` method in each class | `Parent.print()` | `Parent.print()` | Both expressions have declared type `Parent`. |
| Parent instance method and child override | `Parent.print()` | `Child.print()` | The actual receiver classes differ. |

The compiler knows the reference's declared type and checks available signatures. Runtime selection then finds the actual object's override for the selected instance signature. NM001 p.3's statement about types being unknown during compilation cannot mean that declared types are unknown; this explanation qualifies that wording. Private methods are not overridden by children, and final methods cannot be overridden. These rules do not by themselves establish JVM optimizations or physical call costs.

For a mixed trace such as recalled 2026-1 final question 2, classify each expression before evaluating it. Fields and static calls follow declared types; overridden instance calls follow actual receivers. A cast to a parent type leaves instance overriding in effect. Explaining these three paths matters more than merely listing output. The recalled question is historical supplementary evidence, and its complete private program or supplied answer is not reproduced here. [EX:cp_2026_1_final_q02 p.2]

### Sending a common request through `Shape[]`

`Shape.randShape()` on NM001 pp.8–9 returns a `Circle` or `Square` according to `(int)(Math.random() * 2)`. Its return type is `Shape`, although the actual object has a more specific class. The two source loops perform different jobs:

```java
Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();
```

Array allocation initially creates four reference slots containing `null`; it does not create four shape objects. The first loop fills each slot with a shape reference, and the second requests the common `draw()` operation. Actual circles execute `Circle.draw()`, and squares execute `Square.draw()`. Calling before filling a slot would leave no object to receive the call, a boundary obtained by combining array initialization with invocation rules.

The displayed sequence Circle, Square, Circle, Circle is one possible output. A fixed array length does not make the random selection sequence fixed. The example explains why different concrete types can be traversed through a common type; it does not impose the same inheritance design on Lab04.

## `toString()`: providing a representation without changing the object

Concatenating individual fields at every output location repeats a representation rule. Overriding Object's `public String toString()` centralizes that rule. Its String return also distinguishes it from a void method that directly prints something. [NM001 PDF pp.12–16]

```java
class MyClass {
    @Override
    public String toString() {
        return "MyClass";
    }
}
```

In this material example, `"String = " + myClass` produces `String = MyClass`. Page 14 describes this as casting to String, but the object's actual class does not become `String`, and this is not a reference cast. The operation **obtains a String representation and concatenates it**.

The source's String example displays the same content through direct output and `toString()`. Its File example likewise shows the same path representation through both forms. That represents a path; it does not open a file. A separate `Student` example formats `fName`, `lName`, and `id` with `String.format("%s %s (%d)", ...)`. The incidental person's name and identifier are unnecessary to the lesson. Centralizing the format lets different output locations use one consistent representation.

## `equals()`: distinguishing identity from content equality

Reference `==` checks identity: whether two references designate the same object. Object's default `equals()` makes that distinction too, but a class can override it to define equality through meaningful fields. Two separately constructed `new String("abc")` objects on NM001 p.18 compare `false` with `==` and `true` with `equals()`, because String already supplies content equality. This does not require treating references as exposed physical memory addresses.

Primitive values themselves have no instance `equals()` method. The p.17 claim equating `==` and `equals()` for primitives is therefore inaccurate. Primitive value comparison must be distinguished from invoking a method on a wrapper object.

### `Shoes`: the checking sequence and two null boundaries

The `Shoes` example on NM001 pp.19–21 defines equality using `company`, `model`, and `size`:

1. If `this == o`, it immediately returns `true`.
2. Otherwise, it checks `o instanceof Shoes`.
3. If that succeeds, it casts to `Shoes` and requires both String-field `equals()` comparisons and the size `==` comparison to succeed.
4. An object that is not a `Shoes` yields `false`.

Let `s1` and `s2` be separate objects with the source values `Nice`, `AirMax`, and `265`, and let `s3 = s1`:

| Comparison | Result | Reason |
|---|---|---|
| `s1 == s2` | `false` | They were constructed separately. |
| `s1.equals(s2)` | `true` | All three selected fields match. |
| `s1 == s3` | `true` | Assignment copied a reference to the same object. |
| `s1.equals(s3)` | `true` | The first identity check succeeds. |

A null argument fails `instanceof`, so this method returns `false`. That does not make its internal fields null-safe. When comparing different shoes, a null `company` or `model` field in the receiver can make the direct field-level `equals()` call fail. This is a limitation of the printed code, not a complete general equality implementation. [NM001 PDF p.20]

## Equality in collections and the `hashCode()` contract

A collection can use the equality meaning supplied by its elements. The `frequency` example on NM001 p.23 starts at `result = 0`. If the search object `o` is null, it counts elements satisfying `e == null`; otherwise it counts those for which `o.equals(e)` succeeds. The separate path prevents a method call on a null search receiver. Distinct `Shoes` objects can therefore count as occurrences of the same value under their content equality.

`Collection<?>` here denotes a collection whose particular element type is not fixed by the example. It does not introduce the entire generic type system. Also distinguish the names: `Collection` is an interface, while `Collections` is the utility class supplying such static operations. The abbreviated explanation on p.22 must not merge them.

`hashCode()` provides an `int` associated with an object. The necessary implication is:

\[
a.equals(b)=\text{true}\quad\Longrightarrow\quad
a.hashCode()=b.hashCode().
\]

The converse is not guaranteed. Different objects can share a hash value, so matching hashes do not prove equality. Overriding `equals()` without satisfying the corresponding hash contract can make hash-based use inconsistent. The actual identifier has a capital C: `hashCode()`, despite the source's `hashcode()` headings. The `Shoes` pages do not provide a hashCode implementation, so their equality example is not a completed example of hash-based use. [NM001 PDF p.24]

Recalled 2026-1 final subquestion 1-(d) connects to this **direction of implication**. Explain whether the contract holds for equal objects, rather than relying on one observed output. No additional internal hash algorithm is needed to make that argument. [EX:cp_2026_1_final_q01d p.1]

## `interface`: a contract implementations must satisfy

An interface specifies operations that implementing classes must provide. An abstract method declares input and result types without a body; a concrete implementing class must supply the required implementations. A class can extend only one direct class while implementing several interfaces. [NM001 PDF pp.26–32]

```java
interface MyInterface {
    void printNum(int i);
}

class MyClass implements MyInterface {
    public void printNum(int i) {
        System.out.println(i);
    }
}
```

These declarations appear on NM001 p.30. The following source call, however, uses the undeclared `myClass.func(123)`. It is not evidence that the shown program executes successfully. The intended connection is between `printNum(int)` and its public implementation; the missing `func` must not silently become a newly invented source method.

Interface fields are implicitly `public static final` and require initial values. `RamenCooker`'s `numSteps = 5`, `amountWater = 500`, and `boilTime = 3` are shared constants, not per-object state to be changed by setters. `void boilWater()` and `boolean noodleFirst()` describe behavior for implementations to provide. [NM001 PDF pp.28–29]

`PizzaStore` specifies `Pizza bakePizza()` and `void deliver()`. Its `PizzaHut` and `MrPizza` implementations vary the internal cheese/pepperoni steps and the preparation for delivery. Callers depend on the common result type and calling contract rather than those internal steps. Nevertheless, the `bakePizza()` bodies on p.31 omit the required Pizza return, and helper definitions are absent. These are **incomplete design sketches**, not finished runnable code.

Recalled 2025-1 midterm question 2 asks for the interface concept. Connect “defines a common contract” with “a concrete class implements that contract.” Memorizing only “methods have no bodies” would fail to account for the later default/static examples. [EX:cp_2025_1_midterm_q02 p.1]

### Common operations and replaceable `List<Integer>` implementations

`List<E>` on NM001 pp.33–35 is an interface for ordered collections, with `E` identifying the element type. `ArrayList` and `LinkedList` are implementations. The sequence in the material shows what using an object through the interface means:

```java
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
```

After the three additions, the order is `[10,20,30]`. Reading zero-based index `2` gives `30` without changing the list. Here, `remove(1)` uses int index `1`, removing `20`; the remaining list is `[10,30]`, and `size()` is `2`. `Integer` is a wrapper type, not the primitive type `int`; adding the numbers uses boxing.

Replacing the construction with `new LinkedList<>()` still supports this common operation sequence. It does not imply identical performance or internal storage. The source names `MyFavoriteList` and `MyOwnList` assume user-defined classes actually implementing List; their implementations were not supplied. `set()` is also listed as a common operation but is not called in this trace. Detailed generic rules and collection internals remain later topics.

## `Comparable<T>`: choosing an ordering attribute

Objects requiring an order can implement `Comparable<T>` and its `int compareTo(T obj)`. The **sign** matters: positive means the receiver is greater, negative means the argument is greater, and zero means the objects occupy the same position under the selected ordering. The result need not be exactly `1` or `-1`. [NM001 PDF pp.36–39]

`Seagull` has `flyingHeight` and `numFriend`, but compares only height. Comparing `(10,1)` with `(3,100)` gives `1` because `10 > 3`; the friend counts do not affect it. Equal heights give zero even for different objects, so comparison equality does not establish identity or equality of every field. This example does not supply an `equals()` override.

Every object has an equality operation through Object, but a useful total ordering does not arise naturally for every kind of entity. Implementing Comparable is a deliberate choice of ordering contract. This explains the distinction made on NM001 p.46.

### Lexicographic comparison of Strings

Lexicographic comparison uses the first differing character. The supplied implementation excerpt on NM001 pp.40–41 compares positions up to the smaller length. At the first unequal pair `c1`, `c2`, it returns `c1 - c2`; if that entire common range matches, it returns `len1 - len2`. It does not compare lengths first or sum all character codes.

| Source comparison | Deciding position | Result |
|---|---|---|
| `"aaaaaa".compareTo("bbbbbb")` | First `a - b` | `-1` |
| The reverse comparison | First `b - a` | `1` |
| `"aaaaaa"` with itself | No differing character; equal lengths | `0` |
| `"bbbbbb".compareTo("bccccc")` | The second characters, `b - c` | `-1` |
| `"bbbbbb".compareTo("BBBBBB")` | First `b - B` | `32` |

The last result directly shows why positive does not necessarily mean one. When one string is the entire shared prefix of another, length difference decides. For the explanatory pair `"ab"` and `"abc"`, this yields `2 - 3 = -1`. [NM001 PDF p.42]

The source's ASCII wording fits these English-character code examples; it does not describe every culture's dictionary order. Likewise, `char[] value` belongs to the supplied implementation excerpt, not a claim about the current internal String representation in every Java version.

### Sorting and display have separate responsibilities

A different `Student` class on NM001 pp.44–45 returns `1`, `-1`, or `0` according to the sign of the GPA difference. After adding the fictional example values `3.3`, `4.2`, and `3.1`, `Collections.sort(sList)` orders them as `[3.1,3.3,4.2]`. `add()` inserts elements; `sort()` rearranges elements already present. Page 43's wording about storing with sort must not turn sorting into insertion.

This class's `toString()` returns `Double.toString(gpa)` for convenient display. **`compareTo()` supplies the ordering; `toString()` supplies the representation.** This is a separate class definition from the earlier Student with name/id formatting, and these are instructional numbers, not actual students' grades.

The subtraction implementation also does not establish a complete order for every double value. If the difference is `NaN`, both `diff > 0` and `diff < 0` are false, so the printed expression can return zero. This code-derived boundary distinguishes the supplied ordinary finite examples from a universal floating-point ordering rule.

## Interface bodies and abstract classes with shared state

### A `default` body is not package-default access

NM001 p.47 states that interface default/static methods can have bodies starting with Java 8. The earlier “no method bodies” wording must therefore be restricted to the basic abstract-method form. The source gives:

```java
interface RamenCooker {
    void boilWater();
    default void clean() {
        System.out.println("Rinsing with water");
    }
}
```

`boilWater()` still needs an implementation, but `clean()` supplies common behavior. A static method body is instead associated with the interface itself. This written `default` keyword provides implementation; it is unrelated to omitting an access modifier for package access. The example does not establish the complete interface feature set of later Java versions.

### Shared state, initialization, and abstract behavior

An abstract class can contain common instance state and implementation while leaving selected operations abstract. A class declaring an abstract method must be abstract, and an abstract class cannot be instantiated directly with `new`. Conversely, an abstract class need not contain at least one abstract and one concrete method. [NM001 PDF pp.49–55]

The source's `Person` contains `description`, `name`, private `age`, and common `printName()` and `ageOneYear()` methods. Children implement `work()` and `play()`. `Student` supplies `Study hard`/`Drink hard`, while `BusinessMan` supplies `Meeting all day`/`Go to the movies`. The common aging method is intended to change the sample ages `25 → 26` and `34 → 35`. These strings distinguish fictional class behavior, not facts about identifiable people's lives.

However, the child constructors call `super(description,name,age)`, while the printed `Person` on p.50 has no matching constructor. These pages do not form complete executable code unchanged. Read the intended state and behavior relationship while preserving the missing initialization definition.

| Design need | Choice suggested by the material | Why |
|---|---|---|
| The same operation across unrelated kinds of objects | Interface | Supplies a common calling contract. |
| An additional contract for a class already extending another class | Interface | Multiple interfaces can be implemented. |
| Shared instance fields and implementations among related classes | Abstract class | Provides common state and behavior. |
| Common initialization constructors and protected helpers | Abstract class | Shares responsibility for state management. |

The optional structure on NM001 p.56 declares `AbstractList<E> implements List<E>` and then `ArrayList<E> extends AbstractList<E>`. List supplies the contract, and AbstractList supplies a layer for common implementation. ArrayList does not lose its List relationship; it inherits that relationship through AbstractList. Understanding this structure does not require inventing all the collection framework's internal method implementations.

## Key Takeaways

- The compiler checks declared types and signatures; actual receivers select overridden instance bodies.
- `toString()` supplies representation, `equals()` equality, and `compareTo()` a chosen ordering; these meanings differ.
- Equal objects require equal `hashCode()` values, but matching hashes do not prove equality.
- Interfaces provide calling contracts; abstract classes can share instance state, initialization, and implementation.
- Separate null arguments from null fields, possible random output from fixed output, and source sketches from complete programs.

## Recall and Practice

### Binding and Object contracts

#### Recall Q01 · Two stages of binding

Compare static print methods with an instance print overridden by Child for `Parent parent=new Parent(); Parent child=new Child();`. Does the compiler lack the declared types?

<details><summary>Show solution</summary>

`static` calls both select Parent.print. Instance calls select Parent.print then Child.print because the actual receivers differ. The compiler knows both declared Parent types and checks available signatures; runtime selection chooses the overriding body. Page 3's wording cannot mean ignorance of declared types. `private` methods are not overrides and final methods cannot be overridden. These language distinctions do not establish JVM optimizations or physical call costs.

**Checking points:** Explain both output sequences and the compile/runtime roles.

</details>

#### Recall Q02 · Array slots and shapes

Distinguish the state immediately after new Shape[4], after filling from randShape, and during the draw loop. Is the sample Circle/Square/Circle/Circle sequence fixed?

<details><summary>Show solution</summary>

Allocation creates four null reference slots, not four shapes. The first loop stores Circle/Square references selected through `(int)(Math.random()*2)`. The second invokes the common draw operation, dispatching to each actual shape's override. Calling before filling leaves no receiver. The four-line sample is one possible sequence, not something fixed by array length. This illustration does not impose the same inheritance design on Lab04.

**Checking points:** Distinguish slot allocation from object creation and explain both loops.

</details>

#### Recall Q03 · String representation

If MyClass.toString returns `"MyClass"`, what does `"String = "+myClass` produce? Explain the common lesson from the String/File and Student-format examples.

<details><summary>Show solution</summary>

It produces `String = MyClass`. `public String toString()` returns a representation; it does not cast the object's actual class into String, nor is it a void printing method. The String/File examples show the same representation through direct output and toString; they do not open a file. Student's `%s %s (%d)` format centralizes field formatting so callers avoid repeating it. Incidental personal names and paths are unnecessary.

**Checking points:** Check return versus printing, representation, preserved object type, and reusable formatting.

</details>

#### Recall Q04 · Identity, content, and null

(a) Give four comparisons and the check sequence for separate equal-field Shoes s1/s2 and s3=s1. (b) Contrast a null argument and null receiver fields. (c) Compare two new String("abc") objects and primitive equals.

<details><summary>Show solution</summary>

(a) The results are false,true,true,true for `s1==s2`, `s1.equals(s2)`, `s1==s3`, and `s1.equals(s3)`. Shoes checks identity first, then instanceof Shoes, casts, and requires both String-field equals comparisons plus size ==; other types return false. 

(b) A null argument fails instanceof, but a null company/model receiver field can still fail during comparison of distinct objects. 

(c) Two new String("abc") objects likewise have distinct identity but equal content. Object's default equals uses identity; content equality comes from overrides. Primitives have no instance equals method and must not be confused with wrappers.

**Checking points:** Explain the four results, check order, and both null boundaries.

</details>

#### Recall Q05 · Frequency and the hash contract

For `[null, s1, s2, null]`, with matching non-null Shoes fields, what are the frequencies of null and s1? Explain Collection/Collections and the direction of the equals/hashCode contract.

<details><summary>Show solution</summary>

Null occurs twice through e==null checks; s1 occurs twice through s1.equals(e) for s1 and s2. The null-search branch avoids a method call on a null receiver. Collection is the interface; Collections is the utility class. Here `Collection<?>` does not fix a particular element type. If equals is true, the int hashCode results must agree; equal hashes alone may be collisions and do not prove equality. The Shoes source omits hashCode, so it is not a completed hash-use example. Preserve the identifier `hashCode()`.

**Checking points:** Check why both counts are 2, null handling, the one-way implication, and the source limitation.

</details>

### Interfaces and ordering

#### Recall Q06 · Interface contracts and sketches

Explain RamenCooker's constants/abstract methods and the obligations of MyInterface/PizzaStore implementations. Where are the source examples incomplete?

<details><summary>Show solution</summary>

An interface gives a common input/result signature contract. Concrete classes supply required abstract methods and may implement several interfaces while extending one class. Fields are initialized public static final constants: numSteps=5, amountWater=500, and boilTime=3 are not per-instance settings. boilWater/noodleFirst describe behavior. MyInterface's printNum(int) has a public implementation, but p.30 calls undeclared func(123). PizzaStore implementations must preserve a Pizza-returning bakePizza and void deliver despite different internal steps. Missing returns/helpers make the sketches incomplete. The no-body description applies only to the basic abstract-method form.

**Checking points:** Check the contract, constants, multiple interfaces, and missing call/return definitions.

</details>

#### Recall Q07 · Tracing List operations

Add 10,20,30 to a List<Integer>, then call get(2), remove(1), and size(). What results, and what does replacing ArrayList with LinkedList preserve or not guarantee?

<details><summary>Show solution</summary>

The list becomes [10,20,30]; get(2) returns 30 without mutation. With its int argument, remove(1) removes index 1's 20, leaving [10,30], and size is 2. List<E> supplies an ordered-element contract; E is the element type, and Integer is a wrapper used through boxing. LinkedList supports this sequence, but matching operations do not imply identical storage or performance. MyFavoriteList/MyOwnList assume actual List implementations. `set()` is introduced as an update operation but is not called in this trace.

**Checking points:** Distinguish index from value, observation from mutation, and contract from implementation.

</details>

#### Recall Q08 · Comparable's chosen criterion

Compare Seagulls with (height,friends)=(10,1) and (3,100). What about separate objects of equal height? Explain zero from compareTo versus equals.

<details><summary>Show solution</summary>

The source compares only flyingHeight, so the first result is 1; friend counts do not matter. Equal heights yield zero without establishing identity or equality of all fields. Positive/negative/zero compareTo results mean greater/less/equivalent under the selected ordering and need not be ±1. All objects have equals through Object, but not every entity has a useful natural total order, motivating optional Comparable<T>. The Seagull example provides no equals override.

**Checking points:** Check the selected attribute, sign, limited meaning of zero, and distinction from equals.

</details>

#### Recall Q09 · Deciding a String comparison

Using the supplied algorithm, compare aaaaaa/bbbbbb, the reverse, self, bbbbbb/bccccc, bbbbbb/BBBBBB, and ab/abc. Is length the first criterion?

<details><summary>Show solution</summary>

Results are -1,1,0,-1,32,-1. Compare corresponding positions up to the shorter length and return the first character-code difference. bbbbbb/bccccc differs at the second b-c=-1; lowercase versus uppercase differs at the first b-B=32. For ab/abc the shared prefix matches, so 2-3=-1 decides. Length is not the first criterion, nor is the sum of codes. Positive 32 is valid. This is the supplied char[] excerpt and English-character example, not a claim about every current JDK or locale's dictionary order.

**Checking points:** Explain the first differing position, prefix boundary, and meaning of 32.

</details>

#### Recall Q10 · Sorting and display

For the fictional Student GPA list 3.3,4.2,3.1, distinguish add, sort, compareTo, and toString. Does the difference-based comparison handle NaN as a complete ordering?

<details><summary>Show solution</summary>

add inserts elements; Collections.sort rearranges them using compareTo's GPA order to obtain [3.1,3.3,4.2]. toString merely displays Double.toString(gpa). Sorting does not insert, and representation does not define order. This Student is separate from the earlier name/id class. If diff is NaN, both >0 and <0 are false, so the expression can return zero; ordinary finite examples do not establish a complete order for all doubles.

**Checking points:** Check all four responsibilities and the two false comparisons for NaN.

</details>

### Shared implementation and state

#### Recall Q11 · Interface bodies and default

boilWater() lacks a body but default clean() has one. Explain implementation obligations, the ownership of a static body, and the difference from package-default access.

<details><summary>Show solution</summary>

A concrete implementation must supply the abstract boilWater operation. `default clean()` supplies the shared Rinsing with water body; a static body belongs to the interface itself. The material explicitly allows default/static bodies from Java 8, qualifying its earlier abstract-method summary. Here default is an actual keyword providing implementation, unlike omitted access modifiers giving package access. This does not cover every later interface feature or conflict rule.

**Checking points:** Check the abstract obligation, shared default body, static ownership, and access terminology.

</details>

#### Recall Q12 · Shared state and abstract classes

(a) Explain shared/specialized Person-family responsibilities and intended age/action traces. (b) State the missing-constructor limitation and abstract-class rules. (c) Compare interface/abstract-class choices and the List relationship through AbstractList.

<details><summary>Show solution</summary>

(a) Person shares description/name/private age plus printName/ageOneYear; children implement work/play. Assuming the intended initialization, ages become 25→26 and 34→35; Student provides Study hard/Drink hard and BusinessMan Meeting all day/Go to the movies. 

(b) Yet the matching Person constructor for super(description,name,age) is absent, so this is not an unchanged execution result. A class declaring an abstract method must be abstract and cannot be instantiated directly, but need not contain one method of each kind. 

(c) Use an abstract class to share related state/constructors/protected helpers; use an interface for common operations across kinds or an extra contract alongside another superclass. ArrayList retains List through AbstractList.

**Checking points:** Separate intended behavior from the missing constructor and explain design choice and contract inheritance.

</details>

### Application practice

#### Practice P01 · Three selections on one object

New synthetic practice transfers classification of field/static/instance selection from [EX:cp_2026_1_final_q02 p.2]. Prerequisites: Inheritance's hiding/casts and Q01. Meter has value=4, static kind()→`"base"`, and instance read()→its value. FastMeter has a separate value=9, static kind()→`"fast"`, and an overriding read()→super.value+value. With `Meter a=new FastMeter(); Meter b=a;`, trace b.value, b.kind(), b.read(), and the FastMeter field after a.value=6.

<details><summary>Show solution</summary>

Results: `6,"base",15,9`. a and b alias one object; a.value assigns the Meter field selected by the declared type. b reads that field and its static kind selects Meter. Only read dispatches to FastMeter, adding parent 6 and child 9. The assignment leaves the child field at 9. The new alias-and-mutation step requires more than substituting constants.

**Checking points:** State the alias, separate fields, static type, and instance override reasons.

</details>

#### Practice P02 · Hash observations and guarantees

New synthetic practice transfers the equals→hashCode implication from [EX:cp_2026_1_final_q01d p.1] to comparison of two observations. Prerequisites Q04–Q05; no hash internals. Experiment A finds equal objects with hashes 12 and 15. Experiment B finds hashes both 12 but equals false. Which violates the contract, and can one matching observation certify an implementation?

<details><summary>Show solution</summary>

A violates the required direction: equal objects must share a hash. B alone is not a violation because collisions are permitted. One successful observation cannot prove the requirement for all equal pairs. No specific hash function or collection output is needed for this conclusion.

**Checking points:** Check the direction of necessity and distinguish an observation from a general guarantee.

</details>

#### Practice P03 · Common operations and shared state

New synthetic practice extends the interface-contract demand of [EX:cp_2025_1_midterm_q02 p.1] into design selection. Prerequisites Q06/Q11/Q12 are current. Two unrelated classes already extend different parents but need a shared output operation. A separate related family also needs shared instance state and initialization. Propose a mechanism for each, and qualify 'interfaces have no bodies.'

<details><summary>Show solution</summary>

Use an interface for the first common operation alongside the existing superclass relationships. Use an abstract class for the related family's state, constructors, and common implementation, leaving required behavior abstract. Basic interface abstract methods lack bodies, but the material's default/static forms have them. A common signature alone does not repair missing source constructors or returns.

**Checking points:** Connect each choice to its need and qualify the basic no-body form.

</details>

### Short review plan

Start with identity/equality/hash in Q04–Q05, then compare ordering and representation in Q08–Q10. Next day, trace P01 and explain P03's design choices in sentences.

## Sources

This is materials-only study of Inheritance 2 with necessary Inheritance 1 foundations. The printNum/func mismatch, missing Pizza returns/helpers, and absent Person constructor remain incomplete sketches. Preserve Shoes' null-field/hashCode limits, the source-version String excerpt, and fictional GPA/NaN qualifications. Default/static interface bodies are included without implying full generic/collection internals.

### Materials and relevant pages

- [7 inheritance 2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-009), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-024), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-053), [p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-054), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056)

- [6 inheritance 1 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-034), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-039), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-047)

### Scope of exam connections

These are historical recalls, not verified official papers, answer keys, or predictions for this term. No official answer key is supplied; check the new solutions using their stated reasoning. The final recall's order, accuracy, and missing-question limits remain.

- [EX:cp_2026_1_final_q02 p.2] · [[exam_questions/cp_2026_1_final_q02|existing question preview]]

- [EX:cp_2026_1_final_q01d p.1]

- [EX:cp_2025_1_midterm_q02 p.1]
