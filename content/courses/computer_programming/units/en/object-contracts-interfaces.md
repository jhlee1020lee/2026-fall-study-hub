---
title: "Dynamic Binding, Object Contracts, Interfaces, and Abstract Classes"
description: "Check Object equality and ordering contracts alongside interface and abstract-class design."
course: "computer_programming"
unit_id: "object-contracts-interfaces"
lang: "en"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["7 inheritance 2.pdf", "6 inheritance 1.pdf", "8 polymorphism.pdf", "Lab 6 Polymorphism.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/en/2026-09-10-lecture-04", "courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

## Binding and shared Object contracts

### Selection by declared type and by receiver

To apply one operation to different objects, separate the contract known to the caller from the implementation supplied by the object. A reference variable stores a value referring to an object. In `Parent child = new Child();`, the declared type is Parent and the object's actual class is Child. Assignment does not copy the object into a new Parent. The optional Inheritance 1 prerequisite supplies the Child-extends-Parent subtype relationship; inheritance does not grant subclass code direct access to a parent's private state. [computer_programming:RM001, PDF pp.20-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

Binding connects a method call to an operation. The following static-method definition and the instance-method alternative below are independent examples from NM001.

~~~text
class Parent {
    static void print() {
        System.out.println("Parent.print()");
    }
}
class Child extends Parent {
    static void print() {
        System.out.println("Child.print()");
    }
}

Parent parent = new Parent();
Parent child = new Child();
parent.print();
child.print();
~~~

Both reference expressions have declared type Parent, so the two selected bodies print `Parent.print()` and `Parent.print()`. Child's static print hides Parent's static print. A Child object does not make the second call select Child's static body. Writing `Parent.print()` makes its class ownership clearer. [computer_programming:NM001, PDF pp.4-5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Now remove static from both print declarations and annotate the child's `void print()` with `@Override`. The first call prints `Parent.print()`; the second prints `Child.print()`. The compiler first checks that Parent permits the call. Within that contract, dynamic dispatch selects the overriding body for the actual receiver, the object receiving the call. A private method is not an inherited override target, and a final method cannot be overridden. These cases differ from both ordinary instance overriding and static hiding. [computer_programming:NM001, PDF pp.3-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

NM001 p.3 says “Types of variables are unknown during the compilation.” This cannot mean that the compiler does not know declared types. What may vary is the receiver's actual class and therefore its implementation. The date-unconfirmed NT001 transcript at 00:48 recalls binding; the precise two-output comparison above is supplied by the material examples. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 00:48]]

### A Shape array: one call, different implementations

If Shape provides draw and Circle and Square override it, a caller can request drawing without testing each object's individual kind. In the material, `Shape.randShape()` returns `new Circle()` when `(int)(Math.random() * 2)` is 0 and `new Square()` when it is 1. Its return type is Shape, while the returned object belongs to one of the two subclasses. [computer_programming:NM001, PDF pp.8-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

~~~text
Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();
~~~

Allocation creates four reference slots, initially all null. It does not create four shape objects. The first loop stores an actual shape reference in each slot, from index 0 through 3. The second loop repeats the same expression, `shapes[i].draw()`, but a Circle receiver uses Circle.draw and a Square receiver uses Square.draw.

The material's four lines, `Circle.draw(), Square.draw(), Circle.draw(), Circle.draw()`, are one possible sequence, not a promised random outcome. If the population loop is omitted, calling draw on a null slot has no receiver and raises NullPointerException. Keep the common element type, actual object, and population step distinct.

### toString: giving objects responsibility for their representation

Object's `public String toString()` returns a String describing an object. If every caller assembles the fields separately, changing the format requires editing several places. Giving the object responsibility for its representation lets different callers share that definition. NT001, date unconfirmed, 00:48 and 01:48 explains this motivation. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 00:48,01:48]]

NM001's MyClass supplies this representation:

~~~text
class MyClass {
    @Override
    public String toString() {
        return "MyClass";
    }
}
MyClass myClass = new MyClass();
System.out.println("String = " + myClass);
~~~

The concatenated result is `String = MyClass`. The original object's class does not change into String. The p.14 phrase “casts the object to the String class” is not an accurate reference-cast explanation: concatenation obtains a string representation. Returning a String from toString and printing through println are also different responsibilities. A void method that only prints does not satisfy this return contract. [computer_programming:NM001, PDF pp.12-14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

On p.13, a String and its explicit toString result have the same text; the File example likewise displays the same path representation in both forms. It is not an example of reading file contents. A separate Student example formats name fields and id using `String.format("%s %s (%d)", fName, lName, id)`. Two String placeholders and one integer placeholder centralize the format, instead of making callers repeatedly join the names and parentheses. This Student is a different definition from the later GPA-comparison Student. Matching string representations do not by themselves establish equals equality. [computer_programming:NM001, PDF pp.13-16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### equals: identity and content equality

Reference `==` tests identity: whether two references refer to the same object. Object's default equals has that meaning too. To treat distinct objects as the same meaningful value, a class chooses relevant fields and defines content equality. NT001, date unconfirmed, 01:48 emphasizes comparing contents rather than references. This does not require exposing or comparing physical address numbers. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:48]]

Two calls to `new String("abc")` create distinct objects, so reference equality is false, while String.equals returns true because String already supplies content comparison. Primitive values themselves have no instance equals method. The p.17 claim equating the two operations for primitives must be read with this correction; primitive values and wrapper objects are different. [computer_programming:NM001, PDF pp.17-18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The material's Shoes stores `String company, model` and `int size`. Its equals body is:

~~~text
public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Shoes) {
        Shoes shoes = (Shoes) o;
        return this.company.equals(shoes.company)
            && this.model.equals(shoes.model)
            && this.size == shoes.size;
    }
    return false;
}
~~~

The first check immediately accepts the same object. Otherwise instanceof verifies a compatible type before the cast. The two String fields are compared by contents; the primitive size is compared by value. All three conditions must hold because they are combined with `&&`. An unconditional cast before checking the type could fail when comparing an unrelated object. [computer_programming:NM001, PDF pp.19-20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

~~~text
Shoes s1 = new Shoes("Nice", "AirMax", 265);
Shoes s2 = new Shoes("Nice", "AirMax", 265);
Shoes s3 = s1;
~~~

| Comparison | Result | Reason |
| --- | --- | --- |
| `s1 == s2` | false | Distinct objects |
| `s1.equals(s2)` | true | Matching values in all three fields |
| `s1 == s3` | true | Aliases of one object |
| `s1.equals(s3)` | true | The initial identity check succeeds |

[computer_programming:NM001, PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

For `s1.equals(null)`, null fails instanceof Shoes, so the result is false. A null company field is a different boundary: on the path comparing different objects, `this.company.equals(...)` has a null receiver and is unsafe. Self-comparison may still stop at the first line. Follow the actual branch rather than treating all null situations as equivalent.

For non-null objects, equality must be reflexive, symmetric, and transitive: an object equals itself, reversing the comparison preserves the result, and a=b together with b=c implies a=c. Results must remain consistent while the comparison information is unchanged, and a non-null receiver's equals(null) must be false. These are conditions for making content comparison a coherent relation.

The separate Point2D material example first checks instanceof Point2D, then compares its two double coordinates with `==`. Distinct objects with the same finite coordinates (2.0, 3.0) compare true by that equals and false by reference equality. A differing coordinate or null argument produces false. However, a NaN coordinate is not `==` to itself, so this implementation cannot be generalized to equality over all double values. The `(2.0,3.0)` string produced by toString is a separate representation responsibility. [computer_programming:NM004, PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

### Collection equality and the hashCode contract

Collection is an interface; Collections is the class of static collection utilities. Distinguish the names when reading NM001 p.22. The full structure of the p.23 frequency example counts occurrences equal to target o:

~~~text
public static int frequency(Collection<?> c, Object o) {
    int result = 0;
    if (o == null) {
        for (Object e : c)
            if (e == null)
                result++;
    } else {
        for (Object e : c)
            if (o.equals(e))
                result++;
    }
    return result;
}
~~~

A null target cannot receive equals, so its branch counts `e == null` directly. A non-null target uses `o.equals(e)`. As a teaching application, suppose the collection contains the earlier `s1, s2, null`, with their non-null fields unchanged. Searching for s1 counts 2; searching for null counts 1. Different Shoes objects count as the same value when their content equality succeeds. Read `Collection<?>` here as leaving the particular element type unnamed, not as permission to add arbitrary values safely. [computer_programming:NM001, PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The method `hashCode()` returns an int. Its actual spelling has uppercase C, unlike the material's hashcode. If `a.equals(b)` is true, their hash codes must be equal. The converse does not hold: different values can have the same hash code, a collision. Hash results must also remain consistent while information relevant to equality is unchanged.

Classifying equal contents by inconsistent hashes conflicts with the contract used by hash-based storage and lookup. Consequently, a content-based equals must be accompanied by a compatible hashCode definition. The supplied Shoes and Point2D examples do not show hashCode implementations and therefore do not complete the entire hash contract. This is not a requirement to reimplement every Object method. [computer_programming:NM001, PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

When applying this distinction, separate “one lookup returned true” from “the equality and hash contracts justify consistent lookup of equal values.” That guarantee analysis is the qualified connection to the unofficial recalled questions. It requires neither reconstructing their full implementations nor teaching HashSet's internal algorithms here. [EX:cp_2026_1_final_q01d p.1] [EX:cp_2026_1_final_q03 p.3]

### Interfaces: a contract usable without knowing its implementation

An interface is a type contract specifying available operations. An abstract method declares its name, parameter types, and return type without a body. A concrete class accepts the contract with implements and must satisfy the remaining abstract methods. It can use a suitable inherited implementation; an abstract class can leave some obligations to a later subclass.

A class can extend one superclass while implementing several interfaces. An interface can extend other interfaces. The public contract lets callers use an operation without knowing the hidden implementation, connecting interfaces to encapsulation. NT001, date unconfirmed, 02:48-04:25 supplies this motivation. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 02:48,03:33,04:25]]

The RamenCooker material declares both constants and operations:

~~~text
interface RamenCooker {
    int numSteps = 5;
    int amountWater = 500;
    int boilTime = 3;
    public void boilWater();
    public boolean noodleFirst();
}
~~~

Interface fields are public static final even when those modifiers are omitted. The values 5, 500, and 3 are initialized constants, not per-object mutable state. Leaving them uninitialized or choosing conflicting modifiers is invalid. boilWater requests an operation with no return value, while noodleFirst requires a boolean result; these declarations do not determine the cooking procedure. [computer_programming:NM001, PDF pp.26-29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

To implement MyInterface's `void printNum(int i);`, MyClass supplies `public void printNum(int i)`. The p.30 call is printed as `myClass.func(123);`, which does not match the declared method. A separately identified teaching correction, `myClass.printNum(123);`, would print 123 through the supplied implementation. Keep that correction distinct from the printed call. [computer_programming:NM001, PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

PizzaStore promises `Pizza bakePizza()` and `void deliver()`. PizzaHut sketches adding cheese and finding a delivery location; MrPizza sketches adding pepperoni and finding a delivery person. Their internal strategies differ while callers depend on the same signatures and return contracts. In particular, bakePizza must return Pizza. The supplied bodies omit return statements and helper definitions, so these are design sketches rather than complete programs. [computer_programming:NM001, PDF pp.31-32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

A useful explanation of an interface identifies what input the caller provides and what result and behavior it expects, beyond merely saying that implementations differ. This is the conceptual demand connected to the unofficial recalled interface question. [EX:cp_2025_1_midterm_q02 p.1]

### List: replacing an implementation while preserving operations

`List<E>` is an interface for ordered elements. E is the element-type placeholder; ArrayList and LinkedList are example implementations. NM001 gives this sequence:

~~~text
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
~~~

After the three add calls, the list is [10, 20, 30]. Indices begin at zero, so get(2) returns 30 without changing the list. In this call, remove(1) takes the int index 1 and removes 20. The list becomes [10, 30] and size returns 2. Do not confuse this with searching for and removing the numeric value 1. The listed set operation replaces an element at a position, but is not called in this trace.

Integer is a wrapper class, not primitive int. The example's add(10) uses boxing to supply an Integer element; `List<Integer>` does not mean `List<int>`. Replacing the construction with `new LinkedList<>()` preserves the meaning of this sequence when using the same supported List operations. It does not make storage layout or speed identical. MyFavoriteList and MyOwnList are placeholders assuming user-defined classes that implement List; their bodies are not supplied. [computer_programming:NM001, PDF pp.33-35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### Comparable: choosing an ordering attribute

Every object has a basic equality meaning, but not every kind of object has a useful natural ordering. `Comparable<T>` is a contract chosen by classes that need an order. The sign of `int compareTo(T obj)` expresses the relation: positive means the receiver is greater, negative means the argument is greater, and zero means the same position in the chosen ordering. The result need not be exactly 1 or -1. NT001, date unconfirmed, 05:25-07:23 contrasts Object equality with this optional ordering contract. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 05:25,06:23,07:23]]

NM001's `Seagull implements Comparable<Seagull>` stores flyingHeight and numFriend, but compares height alone:

~~~text
public int compareTo(Seagull seagull) {
    if (this.flyingHeight > seagull.flyingHeight)
        return 1;
    else if (this.flyingHeight == seagull.flyingHeight)
        return 0;
    else
        return -1;
}
~~~

For height/friend pairs (10, 1) and (3, 100), the first object's compareTo returns 1. Friend count has no effect. Different objects with equal height may compare as zero without having the same identity, all fields, or equals result. This example supplies no equals override. Implementing Comparable does not prevent extending a superclass or implementing other interfaces, but it does not establish compatibility with every requirement of every collection. [computer_programming:NM001, PDF pp.36-39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [computer_programming:NM001, PDF p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### Lexicographic String comparison

Lexicographic comparison determines order at the first differing character. The supplied String implementation excerpt compares equal-index characters up to the shorter length, lim. At the first difference it returns `c1 - c2`; if the whole common range matches, it returns `len1 - len2`. It does not sum character codes or compare lengths first. [computer_programming:NM001, PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

| Comparison | Deciding position | Result |
| --- | --- | --- |
| `"aaaaaa".compareTo("bbbbbb")` | First a and b | -1 |
| `"bbbbbb".compareTo("aaaaaa")` | First b and a | 1 |
| `"aaaaaa".compareTo("aaaaaa")` | No difference; equal lengths | 0 |
| `"bbbbbb".compareTo("bccccc")` | Second b and c | -1 |
| `"bbbbbb".compareTo("BBBBBB")` | First b and B | 32 |

[computer_programming:NM001, PDF p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The last result still expresses order through its positive sign. If one String is a complete prefix of the other, no character differs in the common range and the shorter String comes first by the length difference. For the teaching example "ab" versus "abcd", the result is 2-4=-2. The source's ASCII description fits these English-character examples; it is not a description of every culture's dictionary order. Its char[] value is the representation in the supplied implementation excerpt, not a claim about String storage in every Java version.

### GPA sorting: separating comparison from display

A different Student example stores GPA and implements Comparable. It is independent of the earlier name/id Student.

~~~text
class Student implements Comparable<Student> {
    double gpa;
    Student(double gpa) { this.gpa = gpa; }

    public int compareTo(Student anotherStudent) {
        double diff = gpa - anotherStudent.gpa;
        return diff > 0 ? 1 : diff < 0 ? -1 : 0;
    }

    @Override
    public String toString() {
        return Double.toString(gpa);
    }
}
~~~

Adding 3.3, 4.2, and 3.1 in that order initially gives [3.3, 4.2, 3.1]. Collections.sort(sList) rearranges the existing elements according to compareTo, producing [3.1, 3.3, 4.2]. Adding stores an additional element; sorting changes their order. toString makes each GPA readable but does not define the ordering. [computer_programming:NM001, PDF pp.43-45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Read the subtraction-based implementation under the finite-value conditions of the example. If diff is NaN, both `diff > 0` and `diff < 0` are false, so the method can return zero. It is not a complete ordering implementation for every double value. This limitation follows from analyzing the material code.

### Interface default and static bodies

Introducing interfaces through bodyless abstract methods does not establish a universal ban on bodies. NM001 p.47 explicitly permits default and static method bodies from Java 8:

~~~text
interface RamenCooker {
    void boilWater();
    default void clean() {
        System.out.println("Rinsing with water");
    }
}
~~~

boilWater remains an abstract obligation. clean provides a common instance body that implementing classes can use. A static method belongs to the interface itself and differs from receiver-based selection of an instance override. The default keyword here provides a method body; it is unrelated to package access obtained by omitting an access modifier. [computer_programming:NM001, PDF p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The earlier summaries on pp.26-27 and 54, and NT001 at date-unconfirmed 08:22 and 14:45, need this qualification. Keep the transcript wording intact and apply the explicit exception from p.47 in the explanation. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 08:22,14:45]]

### Abstract classes: common state and meaningful unimplemented behavior

An abstract class can share instance state and implementations while leaving some operations abstract. Declaring an abstract method requires an abstract class, and direct construction such as new Person() is forbidden. The converse is not that every abstract class must contain at least one abstract method and at least one concrete method. [computer_programming:NM001, PDF p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The material's Person has package-access description and name, and private age. printName and ageOneYear have common implementations, while work and play are left as obligations:

~~~text
abstract void work();
abstract void play();
~~~

NT001, date unconfirmed, 10:13 explains why: without knowing the kind of Person, assigning arbitrary work/play behavior would conceal the design gap. Student and BusinessMan reuse common state and operations while defining their own behavior. Person's method manages private age; subclass code does not gain direct access to it. The unmodified description and name fields are not public either. [computer_programming:NM001, PDF pp.50-52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 09:13,10:13,13:48]]

| Kind | work | play | Intended ageOneYear transition |
| --- | --- | --- | --- |
| Student | `Study hard` | `Drink hard` | 25 → 26 |
| BusinessMan | `Meeting all day` | `Go to the movies` | 34 → 35 |

These are fictional class behaviors and state examples. Pages 51-52 invoke `super(description, name, age)`, but p.50 does not declare that three-argument Person constructor. The table describes the intended trace assuming the required initialization is present; the printed pages are not complete program source as supplied. The source comment "non-field field" does not define a Java field category. [computer_programming:NM001, PDF pp.50-53](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Supplying concrete work/play bodies and removing the abstract restrictions permits an ordinary class design. Subclasses can then inherit those default behaviors unchanged. Leaving the methods abstract prevents direct construction and makes concrete classes supply the intended operations. The recorded answer at NT001 20:24-23:03 explains this choice; the original unrecorded student's question need not be reconstructed. An abstract class is still a class, distinguished from a concrete class. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 20:24,21:11,22:06,23:03]]

Use an interface when unrelated kinds should support the same operations, or when a class already extends another superclass and needs more contracts. Use an abstract class when related classes share instance fields, common constructor initialization, protected helpers, and implementations. [computer_programming:NM001, PDF pp.54-55](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The optional List example shows why contract and common implementation occupy separate layers:

~~~text
public abstract class AbstractList<E> implements List<E> { ... }
public class ArrayList<E> extends AbstractList<E> { ... }
~~~

This is a relationship skeleton, not a completed collection algorithm. List specifies the contract, AbstractList shares implementation, and ArrayList is concrete. Extending AbstractList does not remove ArrayList's List relationship: `implements List<E>` continues through inheritance. NT001, date unconfirmed, 16:41-19:24 explains how this reduces repeated implementation. E is a named type parameter, distinct from the ? wildcard. The brief generic motivation continues at the end of method-overloading. [computer_programming:NM001, PDF p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 16:41,17:36,18:29,19:24]]

## Recall and Practice

### Concept recall

#### Recall Q01 · Declared type and receiver

Both `print()` bodies print their declaring class name. Given `Parent parent = new Parent(); Parent child = new Child();`, compare the two calls (a) when both methods are `static`, and (b) when Child overrides the instance method. What type does the compiler know? Are `private` and `final` methods equivalent override targets?

<details><summary>Show solution</summary>

The static calls select `Parent.print()` twice because both expressions have declared type Parent; Child's static hiding body is not selected by receiver dispatch. In the instance alternative, the receivers are Parent and Child, so the bodies print `Parent.print()` and `Child.print()`.

The compiler knows the declared type Parent and checks that its contract permits `print()`. Only the overriding implementation of that instance signature depends on the actual receiver. Assignment does not copy a Child into a Parent object. A `private` method is not an inherited override target; a `final` method cannot be overridden.

**Checking points:** Give all four results and distinguish declared-type checking from instance implementation selection.

</details>

#### Recall Q02 · Two stages of a Shape array

An array `Shape[] shapes = new Shape[4];` is populated with Circle or Square references from `randShape()`, then traversed with `draw()`. Explain its state before and after population, how the four bodies are chosen, and what happens if population is omitted. Is the source's Circle/Square/Circle/Circle sequence fixed?

<details><summary>Show solution</summary>

Allocation creates four null reference slots, not four shape objects. The population loop stores actual Circle/Square references at indices 0–3. Traversal uses the common Shape contract while selecting each actual object's overriding `draw()` body. If the stored kinds are Circle/Square/Circle/Circle, those four messages follow in that order; random selection does not guarantee that sample on every use.

Without population, the first `shapes[0].draw()` has a null receiver and raises `NullPointerException`. Array length and the number of created shape objects are different.

**Checking points:** Separate slots, objects, and calls; include both the nonfixed sample and null failure.

</details>

#### Recall Q03 · Returning a representation

If `MyClass.toString()` returns `"MyClass"`, explain `"String = " + myClass` and the object's type. What responsibility is centralized by `String.format("%s %s (%d)", fName, lName, id)` in Student? Distinguish it from a printing `void` method, a File representation, and equality.

<details><summary>Show solution</summary>

The result is `String = MyClass`. Concatenation uses the representation supplied by `public String toString()`; it neither casts the original object to a String instance nor changes its class. A returned String can be reused or printed by the caller. A `void` method that merely prints does not fulfill this return contract.

Student centralizes two `%s` name fields and one `%d` integer id in one format, reducing duplicated formatting at call sites. A File's `toString()` represents its path; it does not read file contents. Equal representations also do not establish `equals` equality.

**Checking points:** Check the exact result, return/print/cast distinctions, all three placeholders, and independence from equality.

</details>

#### Recall Q04 · Shoes identity, contents, and null

Shoes.equals first accepts `this == o`; otherwise it checks `o instanceof Shoes`, then ANDs company/model `equals` with size `==`. For distinct s1 and s2 with matching non-null fields and `s3 = s1`, explain `s1 == s2`, `s1.equals(s2)`, `s1 == s3`, and `s1.equals(s3)`. Also distinguish another type, a null argument, a null company, String objects, and primitives.

<details><summary>Show solution</summary>

The results are false, true, true, true. s1 and s2 are different objects with matching contents in all three fields; s3 aliases s1, so the initial identity check already succeeds. An unrelated type or a null argument fails `instanceof Shoes` and returns false. Checking the type before casting avoids treating an unrelated object as Shoes.

A null s1.company is different: comparison with another Shoes can reach `this.company.equals(...)` with a null receiver. Self-comparison can still return at the first line. Two `new String("abc")` objects likewise have different identities (`==` false), but String's content `equals` returns true. Primitive values themselves have no instance `equals`; size uses value `==`.

For non-null objects, equality must be reflexive, symmetric, transitive, and consistent while comparison information is unchanged; `equals(null)` must be false.

**Checking points:** Justify each result; include both null paths, the type guard, and equality conditions.

</details>

#### Recall Q05 · Finite Point2D coordinates and NaN

Point2D.equals checks the type and then `x == other.x && y == other.y`, with no identity shortcut. Compare distinct objects at (2.0,3.0), an object with one differing coordinate, and null. What does self-comparison when x is NaN reveal? Do `toString()` and the shown code complete the hash contract?

<details><summary>Show solution</summary>

Matching finite coordinates make both coordinate comparisons true, so content `equals` is true while reference `==` remains false for distinct objects. One differing coordinate makes the conjunction false; null fails the type guard. If x is NaN, even `x == x` is false, so this body's self-comparison is false. It therefore cannot be generalized to a reflexive equality implementation over every double value.

The `(2.0,3.0)` representation from `toString()` concerns display, separately from equality. No `hashCode` implementation is shown, so the code does not complete the hash contract required by its content equality.

**Checking points:** Trace the finite condition and NaN self-comparison; do not assume an unseen hashCode.

</details>

#### Recall Q06 · Frequency and hash guarantees

A Collection contains s1, s2, null, where s1 and s2 are distinct Shoes with equal non-null fields. Frequency counts `e == null` when the target is null and `o.equals(e)` otherwise. Find the counts for s1 and null. Explain Collection versus Collections, the direction of the equals/hashCode implication, and what one successful lookup proves.

<details><summary>Show solution</summary>

The s1 target matches the first element by identity and the second by all three field contents, but not null, giving 2. The null target counts the single null element with `e == null`, giving 1. A null target cannot receive `o.equals(e)`, which explains the separate branch. Collection is an interface; Collections is the class supplying static utilities of this kind.

If `a.equals(b)` is true, `a.hashCode() == b.hashCode()` is required. The converse fails because collisions can give equal hashes to unequal values. Consistency is required while relevant comparison information is unchanged. Shoes/Point2D examples showing only content equals cannot be assumed to complete hash compatibility. One successful lookup does not prove a guarantee for all equal values. Traversing `Collection<?>` also does not authorize arbitrary element insertion.

**Checking points:** Account for every element in 2 and 1, reject the converse, and distinguish observation from a contract.

</details>

#### Recall Q07 · Interface obligations

Explain RamenCooker's constants 5,500,3 and its `void boilWater()`/`boolean noodleFirst()` operations. Must every concrete class write every body afresh? Identify the limits in MyInterface's `printNum(int)` versus the printed `func(123)` call and PizzaStore's `Pizza bakePizza()`/`void deliver()` sketches.

<details><summary>Show solution</summary>

An interface gives callers a contract for inputs, returns, and behavior. The three initialized fields are implicitly `public static final`, rather than mutable state for each instance. They need initialization and cannot use conflicting modifiers. `boilWater` requests behavior without a return value; `noodleFirst` requires a boolean while leaving the cooking strategy to implementations. A class may extend one superclass and implement several interfaces; an interface may extend other interfaces.

A concrete class must satisfy remaining abstract obligations but can reuse suitable inherited implementations. An abstract class can leave some obligations to a later subclass. `default`/static bodies are the separate exception in Q12. The `printNum(int)` implementation must be public. The printed `func(123)` call does not match that method; the explicitly identified correction `printNum(123)` would print 123.

Both PizzaStore implementations must preserve the Pizza return from `bakePizza()` and void `deliver()` despite different preparation strategies: PizzaHut sketches adding cheese and finding a location, while MrPizza sketches adding pepperoni and finding a delivery person. Missing returns and helpers make the source a sketch, not a complete program. Hiding implementation behind a public contract connects this design to encapsulation.

**Checking points:** Explain the constant modifiers, qualified implementation obligation, and both source defects.

</details>

#### Recall Q08 · List index trace

Start with `List<Integer> list = new ArrayList<>();`, add 10,20,30, then call `get(2)`, `remove(1)`, and `size()`. Give the results and states, explain set, distinguish Integer from int, and assess replacement by LinkedList.

<details><summary>Show solution</summary>

The adds give [10,20,30]. Zero-based `get(2)` returns 30 without mutation. Here `remove(1)` takes the int index 1, removes 20, and leaves [10,30]; size is 2. It is not deletion by searching for value 1. `set` replaces a value at a position and is not called in this sequence.

Integer is a wrapper reference type and adding these numbers uses boxing; `List<int>` is not a substitute notation. For the same supported operations, constructing LinkedList lets the caller retain the List contract. Storage and performance need not match. MyFavoriteList/MyOwnList assume real List implementations whose bodies are not supplied.

**Checking points:** Give each result and state; check boxing and the contract/implementation distinction.

</details>

#### Recall Q09 · Ordering signs and equality

For Seagull comparing height only, let a=(10,1), b=(3,100), c=(10,99), written as (height,friends). Explain `a.compareTo(b)`, `b.compareTo(a)`, and `a.compareTo(c)`. Does zero establish identity or equals? Is every object Comparable?

<details><summary>Show solution</summary>

The source body returns 1 for greater height, 0 for equal height, and -1 for smaller height, giving 1,-1,0. Friend counts are not consulted. The general compareTo convention specifies positive, negative, or zero; it does not require exactly ±1.

Zero means a tie in the chosen height ordering. The distinct a and c do not share identity, and this class supplies no equals override, so neither all-field equality nor equals equality follows. Object gives a default equality meaning, whereas useful ordering is an optional Comparable contract. Implementing it allows other superclass/interface relationships and does not establish automatic suitability for every collection.

**Checking points:** Check all three sign directions, the chosen attribute, zero versus equals, and optional ordering.

</details>

#### Recall Q10 · First difference and prefix

The supplied String excerpt returns the first differing character-code difference, or the length difference if the common range matches. Find the result and deciding position for: `aaaaaa` versus `bbbbbb`, the reverse, `aaaaaa` versus itself, `bbbbbb` versus `bccccc`, `bbbbbb` versus `BBBBBB`, and `ab` versus `abcd`.

<details><summary>Show solution</summary>

The results are -1,1,0,-1,32,-2. The first two use the first a/b difference and its reverse. The third has identical characters and length. In the fourth, the first b matches and the second position gives b-c=-1. The fifth immediately gives b-B=32. The last matches the two common characters and then returns the length difference 2-4=-2.

Thus neither length nor a sum of all codes is compared first. A value such as 32 still expresses order through its sign. These English-character comparisons establish neither locale-sensitive dictionary ordering nor one internal String representation across all Java versions.

**Checking points:** Give all six numbers and first deciding positions; explain the absence of a differing character in the prefix case.

</details>

#### Recall Q11 · Storing, sorting, and displaying GPA

Student.compareTo uses `diff = gpa - other.gpa; return diff > 0 ? 1 : diff < 0 ? -1 : 0;`, while toString returns `Double.toString(gpa)`. What changes when sorting after adding 3.3,4.2,3.1? Explain the two methods and the boundary when diff is NaN.

<details><summary>Show solution</summary>

Immediately after adding, the list is [3.3,4.2,3.1]; sorting by compareTo for these finite values gives [3.1,3.3,4.2]. `add` increases stored elements; sort rearranges elements already stored. `compareTo` determines order, whereas toString only makes each GPA readable. Changing display alone does not change order. This Student is independent of the name/id example.

If diff is NaN, both >0 and <0 are false, so the expression returns its final zero. This cannot be guaranteed to express a correct ordering tie over every double value; the result is read under the stated finite-value conditions.

**Checking points:** Check both orders, the roles of both methods and add/sort, and both false NaN comparisons.

</details>

#### Recall Q12 · `default` bodies and package access

In `interface RamenCooker { void boilWater(); default void clean() { System.out.println("Rinsing with water"); } }`, separate the implementation obligation from the shared body. Compare an interface static body and the meaning of default when an access modifier is omitted.

<details><summary>Show solution</summary>

`boilWater` is an abstract obligation that a concrete implementation must satisfy. `clean` supplies a usable common instance body printing `Rinsing with water`. The source explicitly permits default/static interface bodies from Java 8, so a universal statement that interfaces have no bodies is incorrect.

A static body belongs to the interface rather than receiver-dependent instance override selection. The `default` keyword providing a body is unrelated to package access obtained by omitting an access modifier. This distinction does not establish all later interface syntax or conflict-resolution rules.

**Checking points:** Distinguish abstract/default/static and avoid conflating default with package access.

</details>

#### Recall Q13 · Person's common state and unimplemented behavior

Person has package-access description/name, private age, common printName/ageOneYear, and abstract work/play. (a) Compare leaving work/play abstract with supplying default bodies. (b) Assuming the needed initialization exists, trace Student aged 25 and BusinessMan aged 34 through ageOneYear and work/play. (c) What omission is exposed by the original `super(description,name,age)` calls?

<details><summary>Show solution</summary>

Leaving the methods abstract prevents direct Person construction and makes concrete subclasses supply the remaining behaviors, exposing the design gap instead of inventing arbitrary parent work/play. Supplying concrete bodies and removing abstract restrictions permits an ordinary class whose defaults subclasses can inherit. An abstract class need not contain at least one method of each abstract/concrete kind.

Assuming the required initialization, the shared ageOneYear changes 25→26 and 34→35. Student work/play gives `Study hard`/`Drink hard`; BusinessMan gives `Meeting all day`/`Go to the movies`. `printName` and aging reuse parent implementations. The parent's method manages private age; subclasses do not gain direct access, and description/name are not public either.

The Person page, however, omits the three-argument constructor invoked by the child pages. This is an intended state trace, not a claim that the printed whole executes successfully. The `non-field field` comment also defines no new Java field category.

**Checking points:** Include the design alternative, access levels, both ages, all four behaviors, and the missing constructor.

</details>

#### Recall Q14 · Contract, shared implementation, concrete implementation

What would you choose when unrelated objects need the same operations, versus related classes sharing state, initialization, and helpers? Explain the three layers in `AbstractList<E> implements List<E>` and `ArrayList<E> extends AbstractList<E>`, and why the List relationship remains.

<details><summary>Show solution</summary>

The first calls for an interface defining the shared operation contract; it is also useful for adding a contract to a class that already has a superclass. The second calls for an abstract class sharing instance fields, constructor initialization, protected helpers, and common implementation.

List supplies the operation contract, AbstractList shares part of its implementation, and ArrayList is concrete. Extending AbstractList carries its implemented List relationship forward rather than discarding List. The layering avoids rewriting common parts across implementations. The source is a relationship skeleton, not a complete collection algorithm. `E` names a repeated type position and is not the `?` wildcard.

**Checking points:** Explain both choices, all three layers, and the inherited relationship without assuming detailed generics.

</details>

### Practice

#### Practice P01 · Auditing equality records

Newly written synthetic practice. Prerequisites are identity/content equality and the hashCode contract. Only observation-versus-guarantee reasoning is connected to [EX:cp_2026_1_final_q01d p.1] and [EX:cp_2026_1_final_q03 p.3] (3-(a); implementation repair excluded).

Hypothetical record A reports `a.equals(b)=true` with hashes 17/23. Record B reports `a.equals(c)=false` with hashes 17/17. An analyst rejects B but accepts A because one lookup succeeded. Explain both errors and what remains unchecked. Do not implement a new hash function.

<details><summary>Show solution</summary>

A violates the required equal→same-hash implication; one successful lookup does not remove the 17≠23 inconsistency. B can be a legitimate collision: unequal values may share a hash. Rejecting it reverses the implication incorrectly.

These two records do not establish reflexivity, symmetry, transitivity, consistency of equals while comparison information is unchanged, or hash consistency in all relevant cases. They also determine neither one particular contains outcome nor compatibility with every library.

**Checking points:** Identify A's required violation, B's possible valid collision, the limited observation, and unchecked conditions.

</details>

#### Practice P02 · Separating a contract from shared state

Newly written lecture-based general practice. The index contains an interface-definition item but no direct format evidence for this design task.

An external device already has another superclass. Related internal devices share name, counter, initialization, and helpers. All must provide `String report()`. Assign interface/abstract/concrete roles in a minimal design. Does availability of a default body let an interface store an instance counter? Do identical reports imply equals equality?

<details><summary>Show solution</summary>

Put the common report input/String-return contract in an interface. The external device can implement it while retaining its superclass. Related internal devices can reuse name/counter, initialization, and helpers in an abstract class implementing that interface; concrete subclasses satisfy remaining meaningful behavior. This mirrors the roles in AbstractList→ArrayList.

A default body can provide shared instance behavior but does not change interface fields from `public static final` into per-object mutable state. The varying counter is a reason to use abstract-class instance state. Matching reports establish neither identity nor equals equality; an equality criterion is separate. No complete device implementation is needed.

**Checking points:** Check external inheritance, internal shared state, interface field limits, and representation/equality separation.

</details>

## Sources

### Lecture notes and transcripts

- [[courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2|Date unconfirmed · Object contracts, polymorphism, and generic introduction]]
- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · array and traversal prerequisites]]
- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · object, constructor, static, and reference prerequisites]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · object, initialization, and reference recap]]

Dated notes link the stated prerequisites; they do not establish that detailed inheritance/dispatch was completed on those dates.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · undated transcript]] — 00:48, 01:48, 02:48, 03:33, 04:25, 05:25, 06:23, 07:23, 08:22, 09:13, 10:13, 13:48, 14:45, 16:41, 17:36, 18:29, 19:24, 20:24, 21:11, 22:06, 23:03.

### Materials and physical PDF pages

Page numbers count physical PDF pages; each page link includes the original page.

- [6 inheritance 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-023).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-009), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-024), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-047), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-053), [p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-054), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056).
- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-033).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-004), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-006), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).

### Scope and uncertainties

NT001 is undated. Its 95 utterances retain 124 literal uncertainty markers and 76 additional limits; unclear speech, negation, and missing words are not reconstructed from printed material. Printed examples are material evidence, not evidence that every example was newly spoken. Times below locate transcript passages and are not timestamp anchors.

NM005 has 36 physical PDF pages. Its registered Lab 6 title conflicts with the printed Lab 1 cover; TODOs and the unavailable ZIP referenced on p.19 remain unresolved. It is used for concepts, without supplying a completed graded implementation or transferring attendance/submission rules.

NM001 p.3's claim that variable types are unknown at compilation, p.14's String-cast wording, and p.17's primitive-equals wording are not adopted as Java rules. Distinguish Collection/Collections on p.22, func/printNum on p.30, omitted Pizza returns, and Person's absent constructor and unusual comment. The early interface-body ban is qualified by the Java 8 default/static exception on p.47. Compatible hashCode bodies are not supplied for Shoes/Point2D; NaN limits the coordinate-equality and GPA comparisons. The String excerpt supports its shown implementation and character examples, not every version or locale. NT001's E/wildcard wording at 16:41 and uncertain abstract-instantiation/performance statements remain separate from material evidence. Complete List/Comparable algorithms, all contracts, and detailed generics are outside this scope.

### Qualified connections to unofficial recalls

These are unofficial recalled documents with no verified official keys supplied. The filenames alone associate the 2025-spring midterm with Kim Sanghan (김상한) and the 2026-spring final with Yoo Youngjae (유영재), different from current instructor Jaemin Yoo (유재민). Connections concern only the concepts or reasoning below and establish no current style, scope, frequency, or probability. New questions are general or synthetic practice.

- [EX:cp_2025_1_midterm_q02 p.1] — A concept connection on an interface’s inputs, returns, and behavior. Class/method foundations suffice; anonymous-class and lambda implementations are not imported.
- [EX:cp_2026_1_final_q01d p.1] — Connect the one-way equal-implies-equal-hashCode requirement. Identity/content and Object contracts are prerequisites; no hash implementation is requested.
- [EX:cp_2026_1_final_q03 p.3] — Use only 3-(a)’s distinction between one observation and a contractual guarantee. Equality/overriding are prerequisites; 3-(b)’s implementation repair and HashSet internals are excluded.

No indexed item directly matches the Shape array, toString formats, List indices, Seagull/String/GPA calculations, or Person/List layering. P02 is general design practice based on these materials. Tree collections, lambdas, anonymous classes, and generic bounds would add prerequisites.
