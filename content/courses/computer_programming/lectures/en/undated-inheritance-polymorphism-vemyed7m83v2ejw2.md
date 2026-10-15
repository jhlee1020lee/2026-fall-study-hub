---
title: "Object Contracts, Polymorphism, and a Generics Introduction · Lecture Notes · Date Unconfirmed"
course: "computer_programming"
lang: "en"
term: "2026_Fall"
date: null
lecture_date: null
date_confidence: "unknown"
source_kind: "lecture_note"
note_layout: "content_first_v1"
reader_layout: "content_first"
review_status: "approved"
draft: false
cssclasses: ["plain-document"]
source_mode: "text_only_practical"
audio_verified: false
verbatim_complete: false
source_assets: ["6 inheritance 1.pdf", "7 inheritance 2.pdf", "8 polymorphism.pdf", "Lab 6 Polymorphism.pdf", "Lecture 2 Java Basics 1.pdf"]
source_basis: "privacy_reviewed_corrected_text_and_official_materials"
---

## Lecture Content and Explanation

### References, inheritance, and the receiver

A reference variable has a declared type, and its value can refer to an object whose class is that type or a permitted subtype. In `Parent p = new Child();`, the declaration tells the compiler that expressions using `p` must obey the `Parent` contract. The object created by `new Child()` is still a `Child`. Assigning its reference to `p` creates neither a second object nor a change to that object's class. The object receiving an instance-method call is its receiver.

Optional material prerequisite: `class Child extends Parent` expresses an is-a relationship. Every `Child` can be used as a `Parent`, whereas owning a `Parent` object as a field expresses has-a composition. Java classes have one direct superclass; interfaces allow additional type contracts. A class with no explicit superclass extends `Object`, whose own superclass does not exist. This is why otherwise unrelated classes share methods such as `toString`, `equals`, and `hashCode`. It does not make every listed `Object` method overridable. [RM001, physical PDF pp.14,17-23,26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

An instance field belongs to an object; a static member belongs to a class. Access is a separate question: a superclass's private state is not directly accessible merely because a subclass extends it. A superclass method can manipulate its own private state on a subclass object. Omitting an access modifier gives package access, rather than public access. These distinctions matter when a subclass inherits common behavior, overrides an instance method, or declares a field with the same name. [RM001, physical PDF pp.34,55-64](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

### Static hiding and overridden instance methods

Binding connects a method call to the method it denotes. Material supplement: NM001 first gives `Parent` and `Child` separate static methods named `print()`, then repeats the example with instance methods. The two versions must be reasoned about separately.

```
Parent parent = new Parent();
Parent child = new Child();
parent.print();
child.print();
```

When both declarations of `print` are static, `Child.print` hides `Parent.print`. Both expressions above have declared type `Parent`, so both calls denote `Parent.print()`. The two output lines are therefore `Parent.print()` and `Parent.print()`. Calling a static method through a variable does not make it dynamically dispatched; writing `Parent.print()` makes the class association clearer. [NM001, physical PDF pp.4-5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

When `print` is an instance method and `Child` overrides it, the same declarations and calls instead yield `Parent.print()` followed by `Child.print()`. The compiler first checks that `Parent` permits a zero-argument `print` call. At runtime, the first receiver is a `Parent`; the second is a `Child`, so its override supplies the body. A private method is not an inherited override target, and a final instance method cannot be overridden. [NM001, physical PDF pp.6-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

NM001 p.3 says that variable types are unknown during compilation. That is inaccurate if it means declared types: the compiler knows them and checks member access against them. What can vary with execution is the class of the receiver and thus the overriding body selected for an instance call. NT001 briefly recalls static and dynamic binding before discussing `Object`; this does not establish that every printed example was newly explained aloud. [NM001, physical PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 00:48](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### A Shape array and object-specific drawing

Material supplement: `Shape.randShape()` returns a `Shape` reference. Its switch uses `(int)(Math.random() * 2)`: case 0 constructs a `Circle`, and case 1 constructs a `Square`. Each class provides its own `draw()` body. The common return type allows callers to store either kind through the same declared type. [NM001, physical PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

```
Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();
```

An array is an indexed collection with indices from 0 through `length - 1`. Here, creating `Shape[4]` creates four reference slots, initially null; it does not construct four shapes. The first loop fills each slot with the reference returned by `randShape`. The second loop invokes `draw` on each stored receiver. A `Circle` produces `Circle.draw()`; a `Square` produces `Square.draw()`. The caller needs the common `Shape` operation rather than a branch for each concrete class. [NM001, physical PDF pp.8-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The printed sequence Circle, Square, Circle, Circle is one possible sample, not a sequence guaranteed on every execution. If a slot remains null, invoking `draw()` on that slot has no receiver and would raise `NullPointerException`. This follows from reference-array initialization and instance-call semantics; it is not an additional observed run. The array's element type and each stored object's actual class answer different questions.

### toString supplies a representation

The inherited method `public String toString()` supplies a String representation of an object. A useful override centralizes how the object is described, so callers do not repeatedly assemble its fields. This is the reason emphasized in the opening recap. Returning a String differs from printing a message: a `void` printing method produces output but returns no representation to its caller. [NM001, physical PDF pp.11-12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 00:48](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement: a String printed directly and through its `toString()` has the same textual content. The File example similarly displays its path representation through either form; a representation is not evidence that a file was opened or created. In the separate `MyClass` example, the override returns `"MyClass"`, so `"String = " + myClass` gives `"String = MyClass"`. NM001 p.14 calls this casting the object to the String class. The correct explanation is string conversion for concatenation: the original object remains a `MyClass`, and a String representation is obtained. This does not demonstrate a reference cast from `MyClass` to `String`. [NM001, physical PDF pp.13-14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The material's name-and-identifier `Student` example uses:

```
return String.format("%s %s (%d)", fName, lName, id);
```

The two `%s` conversions place textual fields, and `%d` places the integer identifier. Both explicit field concatenation and printing the object can display that format, but the override puts the formatting responsibility in one method. A readable representation is not a definition of equality: two different objects can print identical text without their class treating them as equal. [NM001, physical PDF pp.15-16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### Identity, content equality, and guards

For references, `a == b` tests whether they refer to the same object, or are both null. It does not expose a physical memory address. The inherited `Object.equals` uses identity; an override of `public boolean equals(Object o)` can define meaningful content equality. Primitive values such as `int` have no instance `equals` method. NM001 p.17's claim that primitive `==` and `equals` are the same therefore confuses primitive operations with methods on objects. [NM001, physical PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Material supplement: two separate evaluations of `new String("abc")` construct distinct objects. Their reference comparison is false, but `equals` is true because String already defines content comparison. Historical prerequisite material likewise contrasts separately constructed Strings with shared String literals. Literal sharing can make `==` true in that particular case; it does not make `==` a general String-content test. [NM001, physical PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [M002, physical PDF pp.61-62](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf), (T007, 15:58, 16:54, 17:48)

The `Shoes` material example compares company, model, and size:

```
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
```

First, an alias of the same receiver returns true immediately. Otherwise, `instanceof Shoes` checks the argument's type before the cast. Null fails that test, so a null argument returns false. After a successful test, the cast permits access to Shoes fields; it does not change the argument object. String fields use content `equals`, whereas the primitive size uses `==`. All three comparisons must succeed. [NM001, physical PDF pp.19-20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

For distinct `s1` and `s2` containing `"Nice"`, `"AirMax"`, and 265, with `s3 = s1`, the four tests `s1 == s2`, `s1.equals(s2)`, `s1 == s3`, and `s1.equals(s3)` yield false, true, true, true. A null argument and a null field are different cases. If the receiver's company or model field is null, invoking that field's `equals` can fail; the argument guard does not protect every field. The printed implementation consequently needs its non-null field assumption. [NM001, physical PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The separate `Point2D` example checks `o instanceof Point2D`, then compares `x` and `y` using `==`. Two distinct points with finite coordinates (2.0, 3.0) satisfy both coordinate tests, so this `equals` returns true while reference identity remains false. Changing one coordinate makes the conjunction false; null does not pass the type guard. Its `toString` separately creates coordinate text. Direct double comparisons do not define every useful numerical notion of equality: for example, NaN does not equal itself with `==`, so this particular Point2D body can fail reflexivity for NaN coordinates. Neither this page nor the Shoes code supplies a matching `hashCode` implementation. [NM004, physical PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

A content-equality definition must be reflexive, symmetric, transitive, and consistent while the relevant information is unchanged; for a non-null receiver, `equals(null)` must be false. These conditions explain why equality needs a deliberate class-level definition rather than whichever fields happen to print nicely. The recap's distinction is content versus identity, not a requirement to reimplement every method inherited from Object. [STT NT001, 01:48](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Equality in collections and the hashCode contract

Material supplement: the frequency example counts elements equal to a target. It initializes `result` to zero and chooses a null-specific path:

```
if (o == null) {
    for (Object e : c)
        if (e == null) result++;
} else {
    for (Object e : c)
        if (o.equals(e)) result++;
}
```

If the target `o` is null, `o.equals(e)` would invoke an instance method without a receiver. The first branch instead counts null elements directly. With a non-null target, the second branch uses that target's equality definition. Thus separately constructed Shoes objects can contribute to the same content-frequency count. As an illustrative trace, a collection containing two matching Shoes values and one null gives a count of two for a matching non-null Shoes target, and one for the null target, assuming the Shoes fields satisfy the preceding non-null requirement. [NM001, physical PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

`Collection` is the interface; `Collections` is the utility class containing operations such as `frequency` and `sort`. NM001 p.22 blurs those names. In `Collection<?>`, the question mark denotes an unknown element type; this frequency example can examine elements as Objects without establishing the full rules of generic types.

The actual Java spelling is `hashCode()`, with a capital C, rather than the material's `hashcode()`. It returns an int used in hash-based operations. If `a.equals(b)` is true, `a.hashCode()` and `b.hashCode()` must be equal. The converse is false: different values can share a hash code, so the hash alone cannot prove equality. Repeated calls must remain consistent within an execution while the information used for equality is unchanged. If a class changes equality from identity to content, its hash-code behavior must agree with that choice; otherwise equal values can be treated inconsistently by hash-based uses. The printed Shoes example illustrates equality but leaves that matching implementation unspecified. No hash function or collision-handling algorithm follows from the example. [NM001, physical PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### Interfaces specify shared operations

An interface is a type contract describing operations that implementations must support. An abstract method declares its name, parameter types, and return type without a body. A concrete implementing class must satisfy the required abstract methods, using its own bodies or suitable inherited implementations. An abstract implementing class may leave some obligations to concrete subclasses. A class can extend one superclass while implementing several interfaces. This lets unrelated kinds of object support a common operation without requiring them to share one concrete implementation. The lecture connects this public contract with encapsulation: callers use the exposed operations while implementation details can remain hidden. [NM001, physical PDF pp.26-27,32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 02:48, 03:33, 04:25](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement: the RamenCooker interface declares constants `numSteps = 5`, `amountWater = 500`, and `boilTime = 3`. Interface fields are implicitly `public static final` and require initializers. These values are shared constants, not per-object mutable settings. Its `void boilWater()` and `boolean noodleFirst()` declarations specify behavior: one returns no value, and the other returns a boolean. An implementation determines the actual boiling behavior and the boolean result while preserving those call forms. [NM001, physical PDF pp.28-29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The next example declares `MyInterface.printNum(int i)` and implements it publicly in `MyClass` by printing `i`. Public access is required when implementing this public interface method; reducing access would break the public contract. However, the source then calls `myClass.func(123)`, although it has declared `printNum`, not `func`. That printed call does not demonstrate successful invocation of the implementation. The separately corrected illustrative call is `myClass.printNum(123)`, whose body would print 123. The correction concerns the example's method name, not an alternate quotation of the source. [NM001, physical PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

PizzaStore similarly promises `Pizza bakePizza()` and `void deliver()`. PizzaHut and MrPizza can choose different preparation helpers and delivery strategies. Callers still expect a Pizza return from baking and no return value from delivery. The printed baking bodies call cheese or pepperoni helpers but omit a Pizza return, and the helpers themselves are not supplied. They are design sketches, not complete programs. Their lesson is that shared signatures constrain callers' expectations while allowing implementation differences. [NM001, physical PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### List operations through a common type

Material supplement: `List<E>` represents an ordered collection with a common set of operations. `E` names the element type. ArrayList and LinkedList are examples of implementations; their internal representations need not be the same.

```
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
```

After the three additions, the order is [10, 20, 30]. With zero-based indexing, `get(2)` returns 30 without changing the list. Here, the literal `1` is an int index, so `remove(1)` removes the element at index 1, which is 20. The remaining list is [10, 30], and `size()` returns 2. This is not a request to remove the value 1. Although `set` is another listed updating operation, the displayed sequence never calls it. [NM001, physical PDF pp.33-35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

`Integer` is a reference wrapper type, not the primitive type `int`. In this example, adding numeric literals uses boxing to supply Integer values. This small amount of generic notation identifies what the list stores; it does not mean any related type argument can be substituted automatically.

Changing construction to `new LinkedList<>()` can preserve these supported operations and their meaning because callers use the List contract. The material's MyFavoriteList and MyOwnList are placeholders for hypothetical classes that actually implement that contract, not supplied working implementations. A common API does not imply identical storage, timing, or every possible optional-operation behavior.

### Comparable defines an ordering criterion

`Comparable<T>` provides the method `int compareTo(T other)`. A negative result puts the receiver before the argument, a positive result puts it after the argument, and zero places them together under the chosen ordering. The contract uses the sign, not an obligation to return exactly -1 or 1. In the lecture's comparison, `equals` belongs to Object's common foundation, whereas useful ordering is an additional property that some kinds of object choose to provide. Implementing Comparable does not prevent a class from extending a superclass or implementing other interfaces. [NM001, physical PDF pp.36-37,46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 05:25, 06:23, 07:23](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement: Seagull stores both `flyingHeight` and `numFriend`, but its `compareTo` examines only flyingHeight. The code returns 1 when the receiver's height is greater, 0 when heights are equal, and -1 otherwise. It directly reads the argument's flyingHeight, so that argument must be non-null; null does not denote an equal-height value. Comparing (height 10, friends 1) with (height 3, friends 100) therefore returns 1: the larger friend count does not participate in this ordering. [NM001, physical PDF pp.38-39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Two distinct Seagulls with the same height compare as zero even if their friend counts differ. Zero here does not establish reference identity or equality of all fields. This example does not override `equals`, so inherited identity equality can differ from ordering equivalence. A class designer must understand that distinction when choosing an ordering for library use; implementing Comparable alone does not guarantee compatibility with every collection or every desired equality convention.

### Lexicographic String comparison

Material supplement: the supplied String implementation excerpt compares corresponding characters from left to right. It sets `lim` to the smaller string length, examines positions below `lim`, returns `c1 - c2` at the first unequal pair, and returns `len1 - len2` only if all shared positions match. Thus a later difference never overrides an earlier one. Length decides a prefix case, not every comparison. [NM001, physical PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

For the printed examples:

- `"aaaaaa".compareTo("bbbbbb")` returns -1 from the first `a - b`.
- Reversing those operands gives 1, and comparing `"aaaaaa"` with itself gives 0.
- `"bbbbbb".compareTo("bccccc")` skips the equal first b, then returns -1 from the second-position `b - c`.
- `"bbbbbb".compareTo("BBBBBB")` returns 32 immediately from `b - B`, whose codes are 98 and 66.

These results show why positive does not mean exactly 1. [NM001, physical PDF p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

As an illustrative prefix calculation, `"ab"` versus `"abc"` finds no unequal character in the two shared positions and returns `2 - 3 = -1`; the shorter prefix comes first. Summing all character codes, or comparing length before characters, would implement different rules. The supplied `char[] value` is the representation used in this excerpt, not a promise about every Java implementation. The English-letter examples involve character-code order rather than a complete locale-sensitive dictionary ordering.

### Ordering students and displaying their values

Material supplement: the GPA Student class is a separate example from the earlier Student holding names and an identifier. It stores a double GPA and defines:

```
public int compareTo(Student anotherStudent) {
    double diff = gpa - anotherStudent.gpa;
    return diff > 0 ? 1 : diff < 0 ? -1 : 0;
}
public String toString() {
    return Double.toString(gpa);
}
```

For the supplied ordinary finite values 3.3, 4.2, and 3.1, the comparisons establish `3.1 < 3.3 < 4.2`. Adding the three objects first makes them elements of the list. `Collections.sort(sList)` then rearranges the existing elements into ascending order. The output representation is [3.1, 3.3, 4.2] because each element's `toString` supplies its GPA text. The comparison determines order; the representation determines what is displayed. Changing a display format alone does not change the comparison criterion. [NM001, physical PDF pp.43-45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

NM001 p.43 loosely describes storing objects using sort. Adding stores an element in the list; sorting changes its order. Also, the subtraction-based comparison is not a complete ordering solution for all double values. If the difference is NaN, both `diff > 0` and `diff < 0` are false, so this body returns zero. Its finite GPA trace should not be generalized to unrestricted floating-point data.

### Interface default methods and static methods

Material supplement: an interface need not consist exclusively of bodyless methods. NM001 explicitly introduces Java 8 default and static methods with bodies:

```
interface RamenCooker {
    void boilWater();
    default void clean() {
        System.out.println("Rinsing with water");
    }
}
```

`boilWater` remains an abstract obligation, while `clean` supplies a common instance-method body that an implementing class can use or override. A static interface method instead belongs to the interface and is called through that interface's name; it is not an instance override selected from a receiver. The keyword `default` in this declaration supplies behavior. It does not mean package access obtained by omitting an access modifier. [NM001, physical PDF p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

NM001 pp.26-27 and p.54, and the lecture's statements at 08:22 and 14:45, describe interfaces as having no implementation bodies. That blanket statement conflicts with the same material's p.47. The accurate introductory distinction is that an interface can require abstract operations and can also provide the default/static bodies just illustrated. A concrete implementation must satisfy outstanding abstract obligations, not rewrite every method body regardless of what is already provided. [STT NT001, 08:22, 14:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Abstract classes share state and leave meaningful obligations

An abstract class is a class that cannot be instantiated directly. If a class declares an abstract method, it must be abstract; declaring a class abstract does not require it to contain both an abstract method and a concrete method. It can share instance state, constructors, and implemented behavior while leaving some operations for subclasses. This gives more than a collection of method names: it allows related subclasses to reuse a common implementation. [NM001, physical PDF pp.49-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The lecture's Person has description, name, and private age, with implemented `printName()` and `ageOneYear()`, plus abstract `work()` and `play()`. The reason to leave those last two abstract is substantive: an unspecified Person has no meaningful universal work or play body. A concrete subclass must provide those behaviors, while reusing common name printing and aging. Private age remains controlled by Person's code; description and name have package access in the displayed declaration, not public access. The source comments calling them “non-field” do not establish a Java category of non-field fields. [NM001, physical PDF p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 09:13, 10:13, 13:48](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement: Student supplies `Study hard` for work and `Drink hard` for play; BusinessMan supplies `Meeting all day` and `Go to the movies`. These are fictional class behaviors. With the intended common initialization, the two Person-typed references print their respective descriptions and names, and `ageOneYear` changes ages 25 to 26 and 34 to 35. Calls to `work` and `play` select the concrete subclasses' bodies. The printed subclasses call `super(description, name, age)`, but the Person declaration supplies no such constructor. The intended state changes and messages can be explained conditionally, yet these pages do not together form a complete working program. [NM001, physical PDF pp.51-53](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

If meaningful work/play implementations were added to Person and the abstract restrictions removed, it could instead be an ordinary concrete class. Subclasses could inherit those defaults unchanged or override them. Keeping the methods abstract makes the missing behavior an explicit obligation and prevents direct construction of an underspecified Person. The recorded answer develops that design rationale; an abstract class is still a class, and “actual class” in the source should not be read as denying that fact. The uncertain affirmative wording about creating an abstract instance at 08:22 is inconsistent with the non-instantiation rule stated in the material. [STT NT001, 08:22, 20:24, 21:11, 22:06](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2), [NM001, physical PDF p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The choice between interface and abstract class concerns the relationship and the reusable implementation:

| Design question | Interface | Abstract class |
| --- | --- | --- |
| What does the type primarily provide? | A shared operation contract, with possible default/static bodies | A class abstraction with shared implementation and optional abstract operations |
| Can it hold per-object mutable state? | Its fields are public static final, not instance state | It can hold instance fields with suitable access |
| Can it initialize common instance state through constructors? | It has no instance constructors | Its constructors participate in subclass construction |
| How does it combine with other types? | A class can implement several interfaces while extending a class | A subclass extends one direct superclass; that superclass can implement interfaces |
| When is it useful here? | Different kinds of object support the same operations | Related classes reuse state, common initialization, or protected helpers |

The default/static qualification comes from p.47 and is needed when reading the simplified comparison on p.54. [NM001, physical PDF pp.47,54-55](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

The List example combines both approaches:

```
abstract class AbstractList<E> implements List<E> { ... }
class ArrayList<E> extends AbstractList<E> { ... }
```

List supplies the contract, AbstractList shares part of the implementation, and ArrayList supplies a concrete implementation. Extending AbstractList does not remove the List relationship: it carries that relationship onward. The lecture discusses why this extra layer avoids rewriting common behavior across many implementations. Here `E` is a named type parameter, not the wildcard `?`; the notation can express a common structure without yet supplying collection algorithms or a full generics treatment. [NM001, physical PDF p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [STT NT001, 16:41, 17:36, 18:29, 19:24](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Method signatures and return types

Polymorphism allows related actions to appear through a shared operation name. The motivation is visible in `printInt`, `printFloat`, and `printString`: all print, but type-specific names burden the caller with remembering several names for the same role. Similar meaning alone, however, does not create a Java override. In the material, Fish adds `swim()` while Animal defines `move()`; the different names mean that `swim` does not override `move`. With `Animal a = new Fish()`, `a.move()` calls the inherited Animal operation, and a suitable Fish cast is needed to access the separately named `swim()`. [NM004, physical PDF pp.4-6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 24:54, 25:54, 26:53](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

For these non-generic examples, a Java method signature consists of its name and ordered parameter-type list. For example, `String substring(int beginIndex, int endIndex)` has the signature `substring(int, int)`; the displayed return type and parameter names do not distinguish it. Parameter variable names do not distinguish signatures. The return type is part of a declaration's information but does not distinguish overloads. Thus `add(int, int)`, `add(int, int, int)`, and `add(float, float)` are different signatures: one changes the number of parameters, and another changes their types. By contrast, these two declarations cannot coexist in one class:

```
int add(int a, int b) { ... }
double add(int a, int b) { ... }
```

They have the same name and parameter types. Assigning a result to a double variable would not authorize a second method distinguished only by its return type. NM004 p.7 includes a return type in a general signature display; p.8 and the lecture explicitly exclude it for Java overload identity. [NM004, physical PDF pp.7-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 27:51, 28:51, 29:34](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Overloading supplies the same name with different signatures. Overriding supplies a new implementation of an inherited instance method with the matching signature and other required compatibility conditions. The NM005 recap uses the same int/float move overloads and a toString representation of the Point. [NM005, physical PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Overloads for different input types and related input shapes

The Point example stores float `x` and `y`. Its `move(int dx, int dy)` and `move(float dx, float dy)` perform the same operation: add the supplied displacement to the fields. Starting from the zero-initialized fields, `move(3, 0)` selects the int-parameter form and produces (3.0, 0.0). The next call, `move(0.0f, 4.0f)`, selects the float-parameter form and produces (3.0, 4.0). The `f` suffix makes those literals float. Overloading lets the caller express the same movement using either supplied numeric input form. [NM004, physical PDF pp.11-12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 31:21, 32:15](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

A related use keeps the operation's meaning while changing its input shape:

```
static double abs_add(double a, double b) {
    return Math.abs(a) + Math.abs(b);
}
static double abs_add(double[] arr) {
    double sum = 0;
    for (int index = 0; index < arr.length; ++index) {
        sum = abs_add(sum, arr[index]);
    }
    return sum;
}
```

The scalar overload returns the sum of two absolute values. In the array overload, `sum` begins at zero. For ordinary finite inputs, each iteration takes the nonnegative accumulated sum and adds the absolute value of the next element. An illustrative trace on [-2.0, 3.0, -4.0] gives `0 -> 2 -> 5 -> 9`; an empty array makes no iterations and returns 0.0. For the supplied array 1.0 through 10.0, the accumulation is `1 + 2 + ... + 10 = 55.0`. The loop condition stops before `arr.length`, so the last visited index is `arr.length - 1`. [NM004, physical PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 33:13, 34:10, 35:41](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The array overload reuses the scalar overload instead of maintaining a separate copy of its core operation. If that common operation changes intentionally, its caller changes with it. This is delegation through a method call, not class inheritance. The lecture's assertion at 34:41 that calling the function necessarily increases time is not established by these semantics; this example supports a maintenance rationale, not a measured performance conclusion. It also supplies no complete policy for null arrays or unrestricted exceptional floating-point values.

### An added parameter controls the search start

An overload can supply additional information to the same operation. The printed DNA example is:

```
String dna =
    "TACGAAGTTACTCGCTGTCAGATCGTAAGCGACGCGATCGTAATGTGAAT";
int first = dna.indexOf("CGC");
int second = dna.indexOf("CGC", first + "CGC".length());
```

The one-argument call finds the first occurrence beginning at zero-based index 12. The substring has length 3, so the second call starts searching at `12 + 3 = 15`. The next occurrence from there starts at 32. The two values are therefore 12 and 32. The second parameter is a starting index, not the number of the occurrence requested. If it were 12 again, the same first occurrence would still be eligible and would be found again. [NM004, physical PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

This code skips past the complete first match; it does not enumerate all overlapping matches. It also assumes the initial search succeeds. If a general search returns -1, that failure needs separate handling before using the result to plan a subsequent search. The source's example illustrates the added-start-position overload, rather than a complete occurrence-search algorithm.

The lecture correctly identifies the role of the second argument but has an uncertain reference to passing the first result alone, and the preceding utterance has an uncertain CCT/CGC discrepancy. The exact CGC literal and `+ "CGC".length()` offset above come from the printed code. The later lab recap prints `indexof`; Java's method name in this explanation is `indexOf`, with capital O. These are source discrepancies, not alternate valid spellings or repaired quotations of the utterance. [STT NT001, 35:41, 36:41, 37:41](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2), [NM005, physical PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Default arguments through delegation

The supplied power example uses a short overload to choose a default exponent:

```
static double power(double input, int n) {
    if (n <= 0) return 1;
    return input * power(input, n - 1);
}
static double power(double input) {
    return power(input, 2);
}
```

The call `power(2)` selects the one-parameter form, which delegates to `power(2, 2)`. That expands to `2 * power(2, 1)`, then `2 * 2 * power(2, 0)`, yielding 4.0. The two-parameter call `power(2, 10)` makes ten multiplications before the zero-exponent base case and yields 1024.0. The returned integer literal 1 is converted to the method's double return type. With `n = -1`, the printed `n <= 0` condition also immediately returns 1.0. This code therefore does not implement negative powers as reciprocals. [NM004, physical PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 38:38, 39:33](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Delegation gives the default-argument form the same central implementation as the explicitly parameterized form. The design principle is to put the substantial common work in one place, rather than let similar methods drift into inconsistent copies. It is a design recommendation, not a rule that every legal overloaded method must invoke another overload.

The debug example makes the same distinction. Its `debug()` prints `"var 1 : "` followed by var1. One proposed `debug(String s)` copies that field-printing expression after the supplied message; the other prints `"Output : " + s` and then calls `debug()`. In the delegating alternative, changing the basic field display changes both uses. The two bodies are alternatives for one signature, not declarations that can simultaneously occupy the same class. Also, the extra `"Output : "` prefix means their exact output text is not identical. With var1 equal to zero and the illustrative message `"state: "`, the delegating form would produce `Output : state: var 1 : 0` followed by a newline. [NM004, physical PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 40:30, 41:23](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Constructor overloads and coordinate meaning

Constructors initialize new objects and use the class's name without a return type. Different parameter lists can provide different initialization paths. In NM004's Point example, `Point()` stores zero in both coordinates; `Point(int, int)` and `Point(float, float)` store Cartesian x and y. A separate `Point(double radius, double theta)` interprets the two numbers as polar data and computes:

```
this.x = radius * Math.cos(theta);
this.y = radius * Math.sin(theta);
```

For radius 2 and angle 0, the mathematical conversion gives `x = 2 * 1 = 2` and `y = 2 * 0 = 0`. The parameter names and these equations establish radius and angle, rather than two Cartesian coordinates. [NM004, physical PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The parameter types make those overloads distinguishable, but they make a surprising API. A caller changing `new Point(2.0f, 0.0f)` to `new Point(2.0, 0.0)` may expect only a precision change, yet the source changes the meaning from x/y to radius/angle. The lecture recommends making such a semantic distinction explicit, suggesting an additional indicator. That suggestion is not a supplied new constructor implementation. Technical distinguishability and a predictable API are separate design criteria. [STT NT001, 42:21, 43:12, 44:12](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The printed `import Math;` is not a valid Java import of a Math package. The `Math` class used here is available as `java.lang.Math`; these equations do not require that malformed line. This explanation identifies the source defect without presenting the complete printed page as successful executable code. It also distinguishes the source's radius identifier from the uncertain spoken “radians and theta” wording.

### Constructor chaining and initialization order

The next Point definition concentrates the shared assignments in `Point(float, float)`:

```
class Point {
    private double x, y;

    Point(float x, float y) {
        this.x = x;
        this.y = y;
    }
    Point(int x, int y) {
        this((float) x, (float) y);
    }
    Point() {
        this(0, 0);
    }
}
```

This is a material-based excerpt of the constructor declarations; it omits the source's invalid import. The invocation `this(...)` delegates to another constructor of the same class. In `Point()`, both zeros are int literals, so overload selection chooses `Point(int, int)`. That constructor explicitly converts the values to float and delegates to `Point(float, float)`, which performs the assignments. Control returns through the delegating constructors only after the delegated initialization finishes. The path is `Point() -> Point(int, int) -> Point(float, float)`. [NM004, physical PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The utterance proposing `0.0` must not be silently read as `0.0f`. An unsuffixed decimal literal is double. With only the int and float constructors displayed above, `this(0.0, 0.0)` cannot implicitly narrow its arguments to either candidate and is not a valid shortcut to the float constructor. By contrast, `0.0f` is a float literal and would directly select that constructor in a separately changed example. The material's actual `this(0, 0)` remains the three-constructor chain just traced. [STT NT001, 45:08, 46:08](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2), [M002, physical PDF pp.40-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)

For the earlier-Java constructor form used in this material, the explicit `this(...)` invocation must come first in the constructor body. This ensures delegated initialization precedes the remainder of that constructor's work. NM004 p.19 and the lecture separately mention restricted work before such a call in Java 25, so “first” should not be asserted as an unqualified rule for every version; the detailed newer syntax is not developed here. [NM004, physical PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 47:08, 47:59, 48:59, 49:57](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Optional material prerequisite: `super(...)` instead invokes a superclass constructor. In the ordinary constructor form, a constructor without an explicit same-class or superclass constructor invocation implicitly invokes `super()`, which requires an accessible no-argument superclass constructor. Superclass initialization proceeds before the remaining subclass initialization; constructors are not overridden methods selected by the runtime receiver. This is why Person's missing three-argument constructor cannot be supplied by merely overriding work/play. [RM001, physical PDF pp.48-51](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

### Applicable overloads and the most specific candidate

Inheritance can make several overloads applicable to one call. Let `ColoredPoint extends Point`, and consider the material's static declarations:

```
static void test(ColoredPoint p, Point q) { ... }
static void test(Point p, ColoredPoint q) { ... }
```

For `ColoredPoint cp = new ColoredPoint(); Test.test(cp, cp);`, both arguments have declared type ColoredPoint. The first candidate accepts the first argument directly and the second as a Point. The second candidate accepts the first as a Point and the second directly. Each candidate is more specific in one position, and neither is more specific across the whole parameter list. The call is ambiguous at compile time. A different signature permits the declarations to coexist, but does not guarantee every possible call has one winner. [NM004, physical PDF pp.20-21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 50:55, 51:49](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The second example instead declares:

```
static void test(ColoredPoint p, Point q) { ... }
static void test(ColoredPoint p, ColoredPoint q) { ... }
```

For the same call, the second candidate is as specific in its first position and more specific in its second. It is the uniquely more specific choice and prints `(ColoredPoint, ColoredPoint)`. Neither the order of declaration nor a search for the first textual match decides this result. The lecture's “matches first” wording should be understood through this type-specificity relationship, not as a declaration-order rule. [NM004, physical PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 52:44](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Overriding, compatible returns, and constructors

An override redefines an inherited instance method so that a subclass can change or extend its behavior through the same call contract. In the material, Employee's `public double getSalary()` returns 180, while Manager's matching method returns 250. For those receivers, the resulting values are 180.0 and 250.0. `@Override` asks the compiler to check the declared overriding intent; the annotation does not itself create a different signature or perform dispatch. The source's mismatched quotation mark in its output statement is a printing-code defect, separate from this method-selection reasoning. [NM004, physical PDF pp.25-26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 53:49, 54:47](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The Laidoff alternatives test a return-type constraint. A subclass's `double getSalary()` returning zero can override the inherited double-returning method. A subclass's `int getSalary()` with the same zero-argument signature cannot. This is not a return-type overload: the signature is still `getSalary()`, and the primitive return type is incompatible with the overridden double return. The printed diagnostic specifically identifies int as incompatible with double. The slide's and utterance's broader “same return type” wording should be confined to this primitive case; it does not establish that every legal reference-return override must spell exactly the same reference type. [NM004, physical PDF pp.27-28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 55:45, 56:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Constructors are not inherited and cannot be overridden. A constructor in Manager must be named `Manager`. A return-type-free declaration named `Employee()` inside Manager is not a way to override Employee's constructor. Calling `super(...)` asks a superclass constructor to initialize its part of a newly created object; it does not turn that constructor into a polymorphic instance method. Likewise, a constructor's overload is chosen from its parameter list, rather than by a later receiver override. [NM004, physical PDF p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:02:14](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The lab's overriding recap uses lowercase `string` in a toString declaration. The Java return type is `String`; the recap's spelling should not be adopted as valid Java. Overriding Object methods such as toString and equals also differs from implementing Comparable's compareTo, which is not an Object method. [NM005, physical PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Type branches compared with object-owned behavior

The HumanResources example imitates class-dependent salary behavior through a static helper taking an Employee. It returns 960 if the argument is an Executive, 250 if it is a Manager, and 180 otherwise. These are the material's example numbers without a specified currency. The helper inspects a type and chooses a branch; it does not call an overridden salary method on the receiver. [NM004, physical PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 57:38, 58:34](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

An `instanceof Manager` test includes compatible subtype objects, so branch order matters if several tested types lie in the same inheritance chain. In an illustrative hierarchy where Executive extends Manager, checking Manager first would also catch an Executive and prevent reaching a later Executive branch. A first-match conditional is different from the most-specific overload rule: these are explicit program branches.

The alternative helper switches on `e.getClass().getName()`, matching the exact strings `"personnelpkg.Executive"` and `"personnelpkg.Manager"`. `getClass()` describes the actual class, not merely the reference's declared type or its superclass. A newly introduced subclass of Manager may satisfy `instanceof Manager` but has its own actual class name, so the exact Manager-name branch need not match it. Renaming or moving classes can also affect string-based tests. With a null argument, instanceof tests are false, whereas invoking getClass on null has no receiver; this further shows that the helpers are not universally interchangeable. [NM004, physical PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:00:18](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

If CEO, Cleaner, Researcher, or other employee kinds are added, centralized branch lists must be updated wherever their behavior is encoded. Missing a case can silently use the fallback. With overriding, each class owns its salary behavior and callers use `e.getSalary()`, reducing the need to maintain parallel type lists. This is the maintenance point of the lecture, not a claim that every instanceof/getClass use is wrong or that constructing named classes removes all dependencies on them. The source's malformed fallback punctuation and broad no-import wording do not alter that reasoning. [NM004, physical PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 59:24, 01:01:17](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Field hiding, overloading, and the RealPoint trace

Field hiding leaves two distinct declarations; it does not override one field with a new runtime-selected field. Material supplement: when Point declares `static int x = 2` and Test extends Point with `static double x = 4.7`, a Test instance method evaluating `x`, `super.x`, and `((Point)this).x` reads 4.7, 2, and 2. The cast changes the type of the expression used for field selection, not the object. The same name is being hidden, despite the lecture's uncertain “new name” wording. [NM004, physical PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:03:10, 01:04:09](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

In the more detailed example, Point has instance int fields x and y initially zero, int-returning getters, `move(int, int)`, and two static `show` overloads, one taking ints and one taking floats. RealPoint extends Point and separately declares float fields x and y. Its important declarations are:

```
void move(int dx, int dy) {
    move((float) dx, (float) dy);
}
void move(float dx, float dy) {
    x += dx;
    y += dy;
}
int getX() {
    return (int) Math.floor(x);
}
int getY() {
    return (int) Math.floor(y);
}
```

The int move overrides Point's int move. The float move overloads it with another parameter list. The getters override Point's getters and read the RealPoint float fields, then floor the values and return ints. These are three different mechanisms in the same class. [NM004, physical PDF pp.35-36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The source then uses:

```
RealPoint rp = new RealPoint();
Point p = rp;
rp.move(1.71828f, 4.14159f);
p.move(1, -1);
```

There is one object, referenced through both Point and RealPoint. The first call has float arguments and a RealPoint-typed receiver expression, so it selects the float move overload and updates the subclass fields. In the second call, the compiler selects `move(int, int)` through Point. Because that is an overridable instance method and the receiver is a RealPoint, execution enters RealPoint's int override, which converts the two arguments to float and delegates to its float move. Both moves consequently update the subclass fields; Point's int x and y remain zero. [STT NT001, 01:06:05, 01:07:02, 01:07:58, 01:08:57, 01:09:54](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement to the four-call calculation skipped in the transcript: float arithmetic rounds the represented inputs and the updated results. After the second move, the float values are approximately 2.7182798385620117 and 3.141590118408203; the source displays them as 2.7182798 and 3.14159. Flooring gives ints 2 and 3. The rounded values explain the material's displayed decimal strings.

| Source call | Selected argument types and behavior | Resulting output |
| --- | --- | --- |
| `Point.show(p.x, p.y)` | Point's int fields; int show overload | `(0, 0)` |
| `Point.show(rp.x, rp.y)` | RealPoint's float fields; float show overload | `(2.7182798, 3.14159)` |
| `Point.show(p.getX(), p.getY())` | RealPoint getter overrides return ints; int show overload | `(2, 3)` |
| `Point.show(rp.getX(), rp.getY())` | The same getter overrides return ints; int show overload | `(2, 3)` |

The apparently surprising pair `p.x == 0` and `p.getX() == 2` is therefore consistent: field access selects the Point declaration, while the instance method dispatches to RealPoint's body. The source code uses float, despite the utterance's uncertain reference to double. [NM004, physical PDF pp.35-37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

### Compile-time overload selection and runtime receiver dispatch

Static or syntactic polymorphism in the material refers to selection resolved at compile time, such as overloading. Dynamic or pure polymorphism refers to the runtime choice of an overriding instance body. An overloaded method need not itself be static: overload selection is a compile-time decision for instance methods too. In either case, declared types remain available to the compiler. [NM004, physical PDF p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:11:50, 01:12:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement: the Polynomial example offers `times(Polynomial)`, `times(int)`, `times(float)`, and `times(Polynomial, int)`. The calls `poly.times(9)`, `poly.times(85.2f)`, and `poly.times(new Polynomial(...), 3)` select the int, float, and (Polynomial, int) parameter lists respectively. The diagram extracts these signatures, registers entries in a method table, and connects each call's argument types to an entry. It explains call selection, not removal of all overloaded bodies from compiled code. The abbreviated constructor and method bodies do not supply a polynomial parser or numerical results to calculate. [NM004, physical PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:13:39, 01:14:31, 01:15:28, 01:16:18](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

For `Employee e = new Manager(); e.getSalary();`, the compiler first checks the getSalary call against Employee. At runtime, Manager's override supplies the body and returns 250.0. The next diagrams depict searching the current class and, if necessary, its superclasses up to Object, locating method data, following its code location, and executing that code. These arrows explain the semantic selection in stages. They are not a universal physical JVM memory map or a guarantee that each invocation performs a fresh linear search. The lecture's binary-body-deletion and unavoidable-cost generalizations exceed what the diagrams establish. [NM004, physical PDF pp.42-43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:17:13, 01:18:07](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The following illustrative Java example combines static Animal overloads with a dynamically selected Dog body. It is a constructed example of these rules, not a transcription of a supplied source program.

```
class Animal {
    String sound() {
        return "Animal body";
    }

    static String describe(Animal x) {
        return "Animal parameter: " + x.sound();
    }

    static String describe(Dog x) {
        return "Dog parameter: " + x.sound();
    }
}

class Dog extends Animal {
    @Override
    String sound() {
        return "Dog body";
    }
}

class DispatchExample {
    public static void main(String[] args) {
        Animal a = new Dog();
        Dog d = new Dog();
        System.out.println(Animal.describe(a));
        System.out.println(Animal.describe(d));
        System.out.println(a.sound());
        System.out.println(Animal.describe((Dog) a));
    }
}
```

The first call's argument expression has declared type Animal. It selects the static `describe(Animal)`, even though `a` refers to a Dog. Inside that selected body, `x.sound()` is an instance call on a Dog receiver, so it invokes Dog's override. The complete first line is `Animal parameter: Dog body`. Runtime dispatch does not go back and reselect `describe(Dog)`.

The second argument expression has type Dog, so the more-specific static `describe(Dog)` is selected and returns `Dog parameter: Dog body`. The third call directly uses the overridden sound signature and returns `Dog body`. In the fourth call, the successful cast gives the argument expression type Dog, so overload selection chooses `describe(Dog)`; its line is again `Dog parameter: Dog body`. The cast succeeds because that actual object was created as a Dog. It does not create or convert an object.

The calculated four-line output is:

```
Animal parameter: Dog body
Dog parameter: Dog body
Dog body
Dog parameter: Dog body
```

Static methods have no runtime receiver override. They can nevertheless contain instance calls whose receivers do undergo overriding, as these two describe bodies demonstrate. The distinction follows the same declared-type and receiver rules used in the material's Parent and Employee examples. [NM001, physical PDF pp.4-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), [NM004, physical PDF pp.39-43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

### Built-in operators and operand types

Java defines the meanings of its operators for the permitted operand types; it does not allow a class author to invent arbitrary user-defined operator overloads. Numeric addition gives `10 + 20 == 30` and `1.5 + 2.0 == 3.5`. String concatenation gives `"10" + "20"` as `"1020"`, and `"sum = " + 30` as `"sum = 30"`. These different meanings of the same symbol are built into the language, not methods the example's class can redefine. [NM004, physical PDF pp.44-45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:19:07](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

Material supplement from the inserted image on physical p.44:

```
String s = "Dog" + " barks.";
s += "Too Loud!";
```

After the first statement, s refers to `"Dog barks."`. The second concatenates the additional text and assigns the result back to s, giving `"Dog barks.Too Loud!"`. There is no inserted space before Too because neither adjoining string supplies one. String immutability is preserved: the variable is updated to refer to the concatenated value rather than modifying the existing String object.

The same original image prints `float f = 0.5 % 0.3;`. Floating-point remainder is permitted, but both unsuffixed literals are double, so that expression has type double and cannot directly initialize a float. A separately corrected illustrative declaration is `double f = 0.5 % 0.3;`. This fixes the assignment type; it does not make a guarantee of an exactly represented decimal 0.2. The distinction follows the supplied literal and narrowing-conversion rules. [NM004, physical PDF p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [M002, physical PDF pp.38-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)

For integer operands, single `&` and `|` work on corresponding bits. For 6 and 3, the relevant binary digits are 110 and 011. AND gives 010, which is 2; OR gives 111, which is 7. On boolean operands, `true & false` is false and `true | false` is true. These boolean forms evaluate both operands. [NM004, physical PDF p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

Historical prerequisite recap: `&&` and `||` differ in evaluation, not just spelling. With `left && right`, a false left operand skips right; with `left || right`, a true left operand skips right. For the supplied integer condition `denominator != 0 && num / denominator == 1`, denominator zero makes the left test false, so integer division by zero is avoided. Replacing `&&` with `&` would evaluate the division as well. Similarly, `true | condition()` evaluates condition(), while `true || condition()` skips it; side effects or exceptions can consequently differ even when the final boolean agrees. The exact tokens here come from the printed operators and the historical short-circuit explanation, not a repair of the unclear operator words in NT001. [M002, physical PDF pp.66-70](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf), (T007, 23:27, 24:17, 25:11, 26:11), [STT NT001, 01:20:06](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

### Upcasts, downcasts, and failure stages

A reference cast changes the type of an expression used to view an existing object. It never changes the actual object's class or rewrites the type in an existing variable declaration. In the material's hierarchy, Beagle extends Dog, Dog extends Mammal, and Mammal extends Animal:

```
Dog dog = new Beagle();
Mammal mammal = (Mammal) dog;
Animal animal = (Animal) dog;
Beagle beagle = (Beagle) dog;
```

All four references denote the same Beagle. Viewing it as Mammal or Animal is an upcast; viewing the Dog-typed expression as Beagle is a downcast that succeeds because the actual object is a Beagle. An implicit upcast, as in `Animal a = new Beagle();`, needs no explicit cast. The Employee/Executive example illustrates the same equivalence between explicit and implicit upcasting. This allows code to depend on a general contract without knowing the concrete implementation. [NM004, physical PDF pp.47-48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:22:07, 01:23:05](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

A cast expression must first be permitted by the compile-time type relationship. For a permitted reference downcast of a non-null value, the actual object must be an instance of the target type or one of its subtypes. Merely wishing to use the target's extra methods cannot satisfy that condition.

The Life/Animal examples isolate two different failure stages. Life supplies `breed()`; its subclass Animal adds `move()`.

```
Life mylife = new Animal();
mylife.move();                 // unavailable through declared type Life
((Animal) mylife).move();      // actual object is compatible
```

The first call is rejected at compile time because Life has no move method. The compiler does not permit a missing member merely because this particular initializer creates an Animal. The cast in the second call supplies an Animal-typed expression, and the actual object satisfies that cast, so move is accessible. [NM004, physical PDF p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:24:50](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

In a separate example:

```
Life mylife = new Life();
((Animal) mylife).move();
```

The related-class cast can pass compile-time checking, but the actual Life object is not an Animal. Evaluating the cast raises `ClassCastException` before move can be invoked. This differs from the previous missing-member error, and it is not explained solely by whether some behavior is absent from the superclass. Actual object compatibility is decisive. [NM004, physical PDF p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:23:53](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

An illustrative guarded use is `if (mylife instanceof Animal) { ((Animal) mylife).move(); }`. The type test excludes incompatible objects and null. Casting null itself to a reference type is allowed, but invoking an instance method on the resulting null reference still has no receiver and fails. Finally, casting a Dog receiver to Animal does not force Animal's overridden instance body: `((Animal) dog).sound()` in the preceding illustrative program still chooses Dog's sound. A subclass's explicit `super` method call has a different role. Optional prerequisite material makes this distinction with superclass casts that retain the most-derived instance method and an explicit super call that selects the parent implementation. [RM001, physical PDF pp.37-47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

### Generics as a type placeholder

Generics introduce a named type variable into a class, interface, or method so that the same structure can be used with different type arguments. The material calls this parametric polymorphism. Its motivation differs from writing separate overload bodies for each concrete input type: a type placeholder can express which uses of the type must agree throughout one reusable structure. [NM004, physical PDF p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), [STT NT001, 01:25:47](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2)

The already encountered `List<E>` and `AbstractList<E>` use E as a named type parameter. Choosing `List<Integer>` preserves Integer as the element type for that use; it does not silently become a list of primitive ints or a `List<Number>`. Any boxing or unboxing occurs at specific expressions that require such a conversion, rather than being the meaning of the type parameter itself. Subtyping between possible element types does not automatically make their parameterized List types covariant. [NM001, physical PDF pp.33-35,56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

A question mark, as in `Collection<?>`, is a wildcard standing for an unknown element type. It is distinct from declaring a named E that can be referred to consistently elsewhere. Unknown does not mean that every value can safely be inserted or that every operation is allowed. The lecture's informal wildcard wording and “arbitrary type during runtime” phrase do not establish a rule that a generic parameter freely changes at runtime. The material's later compile-time explanation corrects that implication, although its accompanying claim that all runtime type errors disappear is also too broad: the downcast examples already show why runtime compatibility can still matter. The brief introduction motivates type reuse and distinguishes these notations; the transcript explicitly leaves detailed generics for the next time. [STT NT001, 16:41, 01:25:47, 01:26:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2), [NM004, physical PDF pp.59,66](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

## Recall and Practice

### Recall

#### Recall Q01 Static hiding and receiver overriding

Consider these independent declarations in one package.

~~~
class Base {
    static String tag() { return "base"; }
    String speak() { return "base voice"; }
}
class Branch extends Base {
    static String tag() { return "branch"; }
    @Override String speak() { return "branch voice"; }
}
Base first = new Branch();
Base second = new Base();
~~~

Determine first.tag(), second.tag(), ((Branch)first).tag(), first.speak(), and second.speak(). Identify the expression types and actual receivers. Would ((Base)first).speak() force the Base body? Explain the private/final restrictions and assess the source claim that variable types are unknown during compilation.

[NM001, physical PDF pp.3-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [RM001, physical PDF pp.34,39,65-67](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf).

<details><summary>Answer</summary>

The five values are `"base"`, `"base"`, `"branch"`, `"branch voice"`, and `"base voice"`. Both variables are declared Base. Static tag selection follows that declared expression type; Branch.tag hides rather than overrides Base.tag. The successful cast makes the third qualifier expression Branch-typed without changing its object.

For speak(), the compiler checks the zero-argument signature through Base. The actual Branch receiver selects Branch.speak and the actual Base selects Base.speak. ((Base)first).speak() still uses Branch.speak. A superclass cast does not suppress an instance override.

A private method is not inherited as an override target; a same-named subclass declaration is separate. A final instance method can be inherited but cannot be overridden. The compiler knows declared types: NM001 p.3's contrary blanket wording is inaccurate. What may vary with execution is the actual receiver and its overriding body.

Checking points: distinguish declared type, actual receiver, static hiding, and instance overriding; infer no timing cost.

</details>

#### Recall Q02 An array of references before drawing

Assume Shape declares void draw(), Circle overrides it to print C, and Square overrides it to print S.

~~~
Shape[] figures = new Shape[3];
figures[0] = new Square();
figures[2] = new Circle();
for (int i = 0; i < figures.length; i++)
    figures[i].draw();
~~~

Describe the slots after creation and assignment. Trace the loop until it stops, including the unreached draw. Give a null-guarded loop and its output. If a random Circle-or-Square factory instead fills every slot, explain its Shape return type, receiver-specific output, and why a printed random sample fixes no future order.

[NM001, physical PDF pp.8-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf).

<details><summary>Answer</summary>

Array creation makes three reference slots, initially [null,null,null], rather than three shape objects. The assignments make them [Square reference,null,Circle reference]. The loop prints S at index 0, then raises NullPointerException at index 1. Index 2 is never reached, so it does not print C.

~~~
for (int i = 0; i < figures.length; i++) {
    if (figures[i] != null) figures[i].draw();
}
~~~

This prints S and then C. The element expression has type Shape; its non-null actual object supplies the draw override. A factory can return either subtype through the shared Shape type, allowing the same traversal without a per-class branch. Once all slots are filled, each message follows the actual stored object. A sample sequence is only one possibility, not a guaranteed order, seed-specific run, or probability measurement.

Checking points: separate slot allocation, object construction, assignment, null failure, and runtime dispatch.

</details>

#### Recall Q03 A returned representation is not equality

A fictional Label has String text, int count, and this override:

~~~
public String toString() {
    return String.format("%s [%d]", text, count);
}
~~~

For text "oak" and count 6, find the text printed by println("item=" + label) and println(label). Explain %s/%d, returning String versus printing through void, centralized formatting, and the effect of changing only toString. Does identical printed text imply equality or a cast to String? What does the material's File representation establish?

[NM001, physical PDF pp.12-16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 00:48](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The lines are `item=oak [6]` and `oak [6]`. %s supplies the text and %d the integer count. One override centralizes formatting instead of requiring every caller to assemble fields.

toString returns a String value; it need not print. A void print method emits output but supplies no representation to another expression. Reformatting toString changes display, not automatically equality or ordering. Distinct objects can print the same representation while Object.equals still distinguishes their identities.

Concatenation obtains a string representation without changing the Label into a String. NM001 p.14's casting-to-String wording is misleading: it is string conversion, not a demonstrated reference cast. Similarly, a File's displayed path is a representation, not evidence that a file was opened or created.

Checking points: preserve spaces/brackets and distinguish output, return value, object type, and equality.

</details>

#### Recall Q04 Identity, contents, type guards, and null fields

Use the Shoes algorithm: return true for this == o; otherwise require o instanceof Shoes, cast, and compare company/model by String.equals and size by ==. Assume those fields are non-null except in the separate case below. a and b are distinct Shoes("Pine","Trail",240), c=a, and d has size 245. Determine a==b, a.equals(b), a==c, a.equals(c), a.equals(d), a.equals(null), and a.equals("Pine"). Explain guard order and what happens if a.company is null when comparing to b. Can int call equals?

Compare == and equals for two separate new String("same") objects and for references initialized to the same literal. Separately, Point2D.equals tests instanceof and compares both doubles with ==, without an identity shortcut. Compare two distinct finite points (1.5,-2.0), a point differing only in y=-1.0, null, and an object with a NaN coordinate compared with itself. State the equals obligations, the missing hashCode condition, and whether toString determines equality.

[NM001, physical PDF pp.17-21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NM004, physical PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [M002, physical PDF pp.61-62](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf).

<details><summary>Answer</summary>

The Shoes results are false, true, true, true, false, false, false. a and b differ in identity but match all compared contents; c aliases a. d fails the size test. Null and String fail instanceof, preventing the cast and field comparisons. The identity shortcut succeeds before field inspection for an alias.

A null argument differs from a null field: for distinct a and b, a.company.equals(...) invokes a method on null and can raise NullPointerException. The type guard does not protect every field. An alias still returns true at the first check. This implementation needs its non-null-field assumption.

Primitive int has no instance equals method; NM001 p.17's primitive-equals statement is inaccurate. The separately constructed Strings have == false and equals true. Shared identical literals can instead make == true through sharing; that special case is not a general content test. Reference identity does not disclose a physical memory address.

The two finite Point2D objects compare true by their two coordinates but have reference == false. Changing y gives false; null fails the type guard. In the exact body, a NaN coordinate makes its self-test false because NaN == NaN is false, and there is no identity shortcut. Direct double equality therefore is not a universally suitable numerical-equivalence definition.

Equals must be reflexive, symmetric, transitive, and consistent while relevant information is unchanged; a non-null receiver's equals(null) is false. The NaN self-case violates reflexivity. Equal objects also require equal hash codes; neither printed Shoes nor Point2D supplies a matching hashCode implementation. toString describes objects rather than deciding equality.

Checking points: distinguish argument guards, field assumptions, identity, content, and numerical boundaries.

</details>

#### Recall Q05 Frequency and the direction of the hash implication

A collection is [a,b,null,c,null], where a and b are distinct content-equal Shoes with non-null fields and c differs in size. A fresh non-null t equals a and b. The frequency algorithm counts e==null for a null target, otherwise target.equals(e). Find counts for t, null, and c, explaining the branches.

For unchanged equality-relevant state, assess: equals true requires equal hashCode values; equal hashes prove equals; differing hashes permit equals true; repeated hashCode calls may vary arbitrarily. What is missing from the Shoes code? Distinguish Collection/Collections and interpret ? in Collection<?> without developing full generics.

[NM001, physical PDF pp.22-24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf).

<details><summary>Answer</summary>

The counts are 2, 2, and 1. The non-null target's equality counts a and b as contents rather than identities. The null-target branch counts the two null references directly, avoiding an invalid null.equals invocation. The stipulated non-null Shoes fields make these particular comparisons safe.

Equals true requires equal hashes; equal hashes do not require equals true because collisions are permitted. Different hashes therefore contradict equality for a valid unchanged pair. Repeated hashCode calls must be consistent within an execution while information used by equality stays unchanged; this does not require equal hashes across different executions.

The printed Shoes class supplies content equality without the corresponding hashCode. A frequency trace uses equality, not hashing, so it cannot establish the missing hash-based contract. No hash function or collision-resolution implementation is required here.

Collection is an interface; Collections is the utility class with operations such as frequency and sort. NM001 p.22 blurs their names, and p.24's hashcode must not replace the actual spelling hashCode. ? denotes an unknown element type, not permission for arbitrary insertion or every generic operation.

Checking points: count null without a null receiver, retain target.equals direction, and do not reverse the implication.

</details>

#### Recall Q06 Interface operations and implementation obligations

Consider:

~~~
interface Gauge {
    int LIMIT = 8;
    double read();
    void clear();
}
~~~

Explain LIMIT's implicit modifiers and initializer requirement, the methods' input/output contracts, and what a concrete implementing class must provide. Can inherited implementations satisfy them? What may an abstract implementation defer? Why would package-access double read() returning 2.5 fail to implement this method? Compare two hidden implementation strategies used through Gauge; can one class extend another while implementing multiple interfaces? May Gauge.LIMIT be reassigned? Finally identify the source's printNum/func mismatch and missing Pizza return/helpers without completing the original sketch.

[NM001, physical PDF pp.26-32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 03:33, 04:25](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

LIMIT is implicitly public static final and needs an initializer. It is a shared constant, not per-object mutable state. Reassigning Gauge.LIMIT is forbidden; a separately declared class field would not mutate it.

read takes no arguments and returns double; clear takes none and returns no value. A concrete class must satisfy both public abstract operations through suitable public compatible implementations, including inherited methods where appropriate. An abstract implementing class may defer outstanding obligations. A package-access read improperly narrows the public interface contract.

One implementation could calculate a reading and another retrieve stored data. Callers rely on signatures while details remain encapsulated. A class can extend one superclass and implement several interfaces. This basic abstract-method form does not forbid the default/static bodies introduced separately.

NM001 p.30 declares printNum but calls an undeclared func, so that call is not successful implementation evidence. Page 31's bakePizza promises Pizza but omits a return and relies on undefined helpers. It is an incomplete design sketch, not a complete program.

Checking points: preserve public access and return obligations; distinguish a required behavior from mandatory duplicated bodies.

</details>

#### Recall Q07 List state and implementation substitution

Assume the java.util types are available. Trace:

~~~
List<Integer> values = new ArrayList<>();
values.add(40);
values.add(10);
values.add(40);
values.get(2);
values.remove(1);
values.size();
~~~

Give each get/remove/size return and every changed list. Why is remove(1) index removal rather than removal of the value 1? Explain zero-based indexing, E, Integer, and boxing. Would LinkedList construction preserve these operations? Does the example establish identical storage/speed, a working hypothetical MyList, automatic covariance, or that set was called?

[NM001, physical PDF pp.33-35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf).

<details><summary>Answer</summary>

The successive list states are [40], [40,10], and [40,10,40]. get(2) returns 40 without mutation. remove(1) uses its int argument as the zero-based index, returns the removed Integer 10, and leaves [40,40]. size() returns 2. Index 1 denotes the second element, not the content value 1.

ArrayList and LinkedList support this sequence through the List contract. Substitution can preserve these calls and meanings without identical internal storage or performance. A hypothetical MyList must actually implement the required contract; its name proves nothing. set is a listed operation but is never called here.

E is a named element type parameter. Integer is a reference wrapper, not primitive int; add's numeric arguments undergo boxing at those expressions. The type parameter itself does not perform automatic unboxing or make related parameterized list types covariant.

Checking points: record state only on mutation and choose remove using the argument type.

</details>

#### Recall Q08 One chosen ordering attribute

Use Seagull's height-only compareTo, returning 1/0/-1 for greater/equal/lower height. a=(height4,friends90), b=(height11,friends1), and distinct c=(height4,friends2). Compute a.compareTo(b), b.compareTo(a), a.compareTo(c), a==c, and a.equals(c), assuming no equals override. What does this body do with a null argument? Must every compareTo return exactly -1/0/1? Does zero prove equal fields or identity? Explain optional Comparable versus Object.equals and whether another superclass/interface remains possible.

[NM001, physical PDF pp.36-39,46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 05:25, 07:23](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The results are -1, 1, 0, false, false. The criterion ignores friend counts. a and c have equal heights but differ in friends and identity; inherited Object.equals remains identity-based. The body directly reads the argument's height, so a null argument raises NullPointerException.

The sign is what matters: negative means before, positive after, and zero equivalent under the chosen ordering. Other signed values are valid; -1 and 1 are just this implementation's choices. Zero does not prove identity, all-field equality, or equals true.

Equals is available through Object's common foundation. Useful ordering is an additional property a class elects to support with `Comparable<T>` and int compareTo(T). It may still extend one superclass and implement other interfaces. Implementing Comparable alone establishes no guarantee for every collection operation.

Checking points: use only height, preserve the non-null argument condition, and distinguish ordering equivalence from equality.

</details>

#### Recall Q09 First character difference and prefix length

Apply the supplied String excerpt: scan corresponding characters, return the first unequal code difference, otherwise len1-len2. Use b=98, c=99, d=100, D=68 as needed. Compute "cab".compareTo("cad"), "car".compareTo("ca"), "d".compareTo("D"), "ca".compareTo("car"), and "cab".compareTo("cab"). State the deciding index or length calculation. Why are length-first or code-sum comparisons wrong? Distinguish return sign, locale ordering, and the supplied char[] implementation representation.

[NM001, physical PDF pp.40-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf).

<details><summary>Answer</summary>

The results are -2, 1, 32, -1, and 0. cab/cad matches at indices 0 and 1, then returns b-d=98-100=-2 at index 2. car/ca matches all shared positions and returns 3-2=1. d/D differs immediately: 100-68=32. The reversed prefix gives 2-3=-1, and identical cab strings give 3-3=0 after scanning all shared positions.

An earlier unequal character decides before later characters or length. Length matters only after the shorter prefix matches completely. Summing codes loses positional information and implements a different rule. A positive result need not be 1.

These English examples use character-code order, not complete locale-sensitive dictionary collation. The char[] excerpt explains its algorithm, not every Java version's internal String storage.

Checking points: identify the deciding position and retain exact differences, not just their signs.

</details>

#### Recall Q10 Sorting and display have different responsibilities

A fictional GradeValue uses:

~~~
public int compareTo(GradeValue other) {
    double diff = gpa - other.gpa;
    return diff > 0 ? 1 : diff < 0 ? -1 : 0;
}
public String toString() { return "g=" + Double.toString(gpa); }
~~~

A list receives 2.5, 4.0, 3.25, is sorted with Collections.sort, then printed. Give its orders and displayed text; assign storage, reordering, comparison, and formatting to add/sort/compareTo/toString. Does reformatting reverse the order? Test a NaN difference and state the boundary of this numerical example.

[NM001, physical PDF pp.43-45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf).

<details><summary>Answer</summary>

Insertion leaves [2.5,4.0,3.25]. For these ordinary finite values, 2.5<3.25<4.0, so sorting gives that ascending order and printing yields `[g=2.5, g=3.25, g=4.0]`.

add stores elements, sort rearranges existing elements, compareTo specifies their ordering criterion, and toString supplies their displayed representations. Reformatting does not change the criterion. NM001 p.43's storing-through-sort wording confuses insertion with sorting. This fictional class, like the material's GPA Student, is separate from its name/identifier Student definition.

A NaN difference makes both >0 and <0 false, causing this body to return 0 even against a finite value. The finite trace is not a complete ordering policy for unrestricted doubles or an implementation of a sorting algorithm.

Checking points: derive order from comparison rather than display, and retain the NaN limitation.

</details>

#### Recall Q11 Default body, static body, and package access

Consider:

~~~
interface Switchable {
    void on();
    default String state() { return "available"; }
    static String family() { return "switch"; }
}
class Lamp implements Switchable {
    public void on() { System.out.println("lit"); }
}
~~~

For Switchable s=new Lamp(), explain calls obtaining state, performing on, and obtaining family. Which method remains abstract in the interface; which bodies are instance/static? Must Lamp reimplement state? Does default mean package-only access? Reconcile the source's no-interface-bodies claim with its later example without extending to further interface features.

[NM001, physical PDF pp.26-27,47,54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 08:22, 14:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

s.state() returns "available" and s.on() prints lit. Switchable.family() returns "switch", called through the interface name. on is abstract in Switchable and implemented publicly in Lamp. state is a common default instance body that Lamp may use or override. family is a static interface body, not a receiver-selected override inherited for instance dispatch.

The default keyword supplies a body; it does not mean package access obtained by omitting an access modifier. These interface methods remain public. A concrete class satisfies outstanding abstract obligations rather than rewriting every provided body.

NM001 pp.26-27,54 and the cited NT001 statements give a simplified no-bodies rule, contradicted by NM001 p.47's explicit Java 8 default/static methods. The blanket claim is inaccurate; bodyless abstract methods and the shown body-bearing forms must be distinguished. Later feature/conflict rules are unnecessary here.

Checking points: distinguish access, method-body provision, and static versus instance calls.

</details>

#### Recall Q12 Abstract behavior and common state

Assume abstract Person has package-access name/description, private age, a constructor setting these, implemented printName/ageOneYear, and abstract work/play. A fictional Learner starts at 18 and prints practice/walk for work/play; a Builder starts at 40 and prints build/music. Each receives ageOneYear once. Through Person references, call Learner work/play then Builder work/play.

Give four messages and new ages. Explain private access, direct instantiation, concrete-subclass obligations, and whether an abstract class must have an abstract method. What changes if meaningful work/play bodies are added and Person becomes concrete? Choose interface versus abstract class for unrelated operation-sharing objects with other superclasses, and related objects sharing mutable state, constructors, and protected helpers. Explain `List<E>` -> `AbstractList<E>` -> `ArrayList<E>`, including the meaning of E, and distinguish the printed Person constructor gap from this question's explicit assumption.

[NM001, physical PDF pp.49-56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 10:13, 16:41, 17:36, 19:24, 20:24, 22:06](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2); [RM001, physical PDF pp.48-51,61-63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf).

<details><summary>Answer</summary>

The work/play messages are practice, walk, build, music: Person-typed calls select the actual subclass overrides. The ages become 19 and 41 through Person's common ageOneYear. Person code may manipulate its own private age on subclass objects, but subclasses do not gain direct field access. Name/description follow package access, not automatic public access.

An abstract Person cannot be directly instantiated. Concrete subclasses must satisfy outstanding work/play obligations, potentially through suitable inherited implementations, while reusing common methods/state. Abstract classes may have no abstract methods; NM001 p.49's both-kinds introduction is not a necessary-and-sufficient definition.

Adding meaningful bodies and removing the abstract restrictions would permit a concrete Person and inherited defaults. Leaving the methods abstract instead expresses missing behavior deliberately and prevents an underspecified general instance. It remains a class; NT001 08:22's uncertain instantiation affirmation does not change the material's prohibition.

Use an interface for a common operation contract across unrelated types, including classes already extending another superclass. Use an abstract class for related classes sharing instance state, initialization, or protected helpers. Interface default methods do not supply mutable instance fields.

List supplies the contract, AbstractList implements reusable partial behavior, and ArrayList supplies a concrete implementation through inheritance. ArrayList remains a List. E is a named type parameter, distinct from ?, without supplying all collection algorithms.

NM001 p.50 omits the three-argument constructor invoked by pp.51-52. Those original pages are incomplete as a combined executable program. This question expressly provides the initialization assumption, so its changed age trace is conditional on that sufficient contract.

Checking points: separate private state, inherited behavior, abstract obligations, construction, and the continuing interface relationship.

</details>

#### Recall Q13 Same signature or different overload?

Group equal signatures among these candidate declarations and choose a set that can coexist in one class. Bodies are omitted only for this comparison.

~~~
int combine(int left, int right)
double combine(int x, int y)
int combine(int x, int y, int z)
float combine(float x, float y)
int combine(String text, int count)
int combine(int count, String text)
~~~

Explain the effects of changing parameter names, parameter order/types/count, and return type. Would assigning the first two results to different destination types make both declarations legal? Distinguish overload from inherited instance override and explain why Fish.swim is not Animal.move's override merely because swimming is movement.

[NM004, physical PDF pp.5-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NM005, physical PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf); [NT001, 27:51, 28:51](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The first two both have combine(int,int); they cannot coexist. Keep either one plus combine(int,int,int), combine(float,float), combine(String,int), and combine(int,String). The others differ by parameter count, types, or ordered type sequence.

Parameter names do not distinguish signatures; return type alone also does not. Assignment to a double destination cannot license the duplicate declaration. For these non-generic Java examples, signature identity uses method name and ordered parameter types. NM004 p.7 displays returns in a general notation, but p.8 and NT001 explicitly exclude them for this Java distinction.

Overloading supplies different signatures under one name. Overriding changes an inherited instance implementation through the matching signature and compatible conditions. swim and move differ in name, so similar intent does not make them an override pair.

Checking points: retain parameter order/types, ignore parameter names for identity, and reject return-only overloads.

</details>

#### Recall Q14 Different numeric inputs and related input shapes

A Point has zero-initialized float x,y and move(int,int)/move(float,float), both adding the displacement. Trace move(-2,1) then move(0.5f,-3.5f), selecting signatures and coordinates.

Separately, abs_add(double,double) returns abs(a)+abs(b); abs_add(double[]) starts sum=0 and uses sum=abs_add(sum,arr[index]) for each element. Trace [-4.0,1.5,-2.0], an empty array, and abs_add(-3.0,-2.0). Explain nonnegative accumulation, loop termination, and reuse. What does the source 1-through-10 array sum to? State input assumptions and distinguish delegation, inheritance, maintenance, and a performance claim.

[NM004, physical PDF pp.11-13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NM005, physical PDF pp.4-5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf); [NT001, 33:13, 34:41](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The int arguments select move(int,int), changing (0.0,0.0) to (-2.0,1.0). The f-suffixed arguments select move(float,float), producing (-1.5,-2.5). These are the same movement task supported for two numeric input types.

The array's sum evolves 0.0 -> 4.0 -> 5.5 -> 7.5. The prior sum is nonnegative and its absolute value is itself, so each update adds the next absolute value. Indices 0,1,2 are visited, then index equals length 3 and the strict loop condition stops. Empty input makes no updates and returns 0.0. The scalar call gives 3+2=5.0. The source's positive 1-through-10 array yields 1+2+...+10=55.0.

The related scalar/array overloads share a meaningful name. The array body delegates the core operation to the scalar body, keeping a change in one implementation rather than independent copies. This is method-call reuse, not an extends relationship. NT001 34:41's universal call-cost claim is not a measured conclusion here.

These traces assume a non-null array, ordinary finite values, and a representable finite sum. They do not provide complete NaN/infinity/overflow or null-array policies.

Checking points: select by argument types before execution and show every accumulator value.

</details>

#### Recall Q15 A starting index is not an occurrence number

For text="ABABA--ABA" and pattern="ABA", show character indices and compute:

~~~
int first = text.indexOf("ABA");
int again = text.indexOf("ABA", first);
int next = text.indexOf("ABA", first + "ABA".length());
~~~

Explain the repeated result, the later match, and the skipped overlapping match. Is the extra parameter an occurrence number? What must be checked if the first search returns -1? Distinguish the printed spelling/offset from the uncertain spoken account.

[NM004, physical PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NM005, physical PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf); [NT001, 35:41, 36:41](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

Indices are 0:A,1:B,2:A,3:B,4:A,5:-,6:-,7:A,8:B,9:A. first is 0. again searches inclusively from 0 and returns 0 again. next starts at 0+3=3 and returns 7. The overlapping match at 2 is skipped because it precedes that start.

The second argument specifies a starting position, not the requested occurrence number. Advancing by the whole pattern length skips past the first full match but does not enumerate all overlaps. A -1 first result requires separate failure handling before planning another search; adding length to a failure marker proves no earlier match. In the source DNA, the analogous printed calculation is first=12, start=15, next=32.

The literal CGC and +length offset are printed NM004 evidence, not repaired speech. NT001 has uncertain CCT/CGC wording and an offset-omitting account. NM005's indexof spelling is also a source error; the method name is indexOf.

Checking points: use inclusive zero-based starts and separate successful matching from failure handling.

</details>

#### Recall Q16 Defaults delegate to a central body

Use:

~~~
static double power(double value, int exponent) {
    if (exponent <= 0) return 1;
    return value * power(value, exponent - 1);
}
static double power(double value) { return power(value, 2); }
~~~

Expand power(3), power(3,4), power(3,0), and power(3,-2). Explain the default, repeated work, and negative-exponent boundary.

Separately, var1=7; debug() prints "var 1 : "+var1 with a newline. One debug(String s) alternative prints s+"var 1 : "+var1; another prints "Output : "+s without a newline, then invokes debug(). Compare exact output for s="state: ", the effect of changing debug(), coexistence of both alternatives, and whether delegation is forced syntax.

[NM004, physical PDF pp.15-16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 39:33, 40:30, 41:23](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

power(3) delegates to power(3,2), expands to 3*3*power(3,0), and returns 9.0. power(3,4) expands through exponents 4,3,2,1,0 and gives 3*3*3*3*1=81.0. Both zero and -2 satisfy exponent<=0 and return 1.0 immediately. The base-case literal becomes double. This is not reciprocal-power behavior: power(3,-2) does not return 1/9.

The debug alternatives print `state: var 1 : 7` and `Output : state: var 1 : 7`, each with one newline. Their exact strings differ. The second delegates the shared field display, so changing debug() changes both entry paths. The first copied expression may need a separate edit.

Both alternatives have debug(String), so they cannot coexist in one class. Delegation is a maintenance principle, not a Java requirement for every overload. No stack-capacity, overflow, or runtime-cost conclusion is established.

Checking points: expose the default argument, retain the <=0 condition, and distinguish common behavior from identical output.

</details>

#### Recall Q17 Different constructor signatures can hide different meanings

The Point constructor set uses no arguments for origin, int/int and float/float for Cartesian x,y, and double/double for radius,theta with x=radius*cos(theta), y=radius*sin(theta). Angles are radians. Explain paths and results for new Point(), new Point(2,1), new Point(2.0f,1.0f), and new Point(2.0,1.0). Give the last coordinates as mathematical expressions and calculate the radius 4/theta 0 case. Why is changing float to double surprising despite legal signatures? Explain how an explicit coordinate-system indicator could clarify intent without implementing it. Assess import Math and the radius/radians wording.

[NM004, physical PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 42:21, 43:12, 44:12](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The paths initialize origin (0,0), Cartesian (2,1), Cartesian (2.0,1.0), and polar-derived (2*cos(1),2*sin(1)), respectively. For radius 4/theta 0, the mathematical conversion is (4*1,4*0)=(4,0). This is an equation-based calculation, not an observed trigonometric run or exact general floating-point guarantee.

The signatures differ by numeric types, but the API changes coordinate meaning where a caller may expect only more precision. Signature legality and predictable semantics are separate criteria. A clearly documented extra coordinate-system indicator could expose that choice; the lecture's proposal is not a supplied required constructor implementation.

The printed import Math is malformed, not proof of a Math package containing Point. The expressions refer to java.lang.Math. radius denotes distance; radians describe angle units. The uncertain spoken substitution is not a corrected quotation.

Checking points: derive selection from literal types and explain the semantic change, not merely legality.

</details>

#### Recall Q18 Delegation entry and return order

Use the earlier-Java constructor form in the supplied teaching:

~~~
class Coordinate {
    private double x, y;
    Coordinate(float x, float y) {
        this.x = x; this.y = y;
        System.out.print("F ");
    }
    Coordinate(int x, int y) {
        this((float)x, (float)y);
        System.out.print("I ");
    }
    Coordinate() {
        this(2, -1);
        System.out.print("N ");
    }
}
~~~

Trace new Coordinate(): constructor entry, stored coordinates, and printed order. Independently replace this(2,-1) with this(2.0,-1.0), then this(2.0f,-1.0f). Explain the first-invocation rule and its initialization purpose, this versus super, implicit super() accessibility, and why constructors are not dynamically overridden. Retain the source's Java 25 qualification without adding newer syntax.

[NM004, physical PDF pp.18-19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [M002, physical PDF pp.40-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf); [RM001, physical PDF pp.48-51](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf); [NT001, 46:08, 48:59, 49:57](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The path is Coordinate() -> Coordinate(int,int) -> Coordinate(float,float). Int literals select the middle overload; its explicit casts select the float constructor. That body stores (2.0,-1.0) and prints F. Returning through the int body prints I, then the no-argument body prints N: `F I N ` including its trailing space.

The unsuffixed decimal replacement has double arguments. Neither the int nor float constructor accepts implicit narrowing from double, so it fails at compile time. The f-suffixed replacement directly selects the float constructor, skips the int body, and prints `F N `. NT001's proposed 0.0 must likewise not be silently read as 0.0f.

In this earlier-Java form, this(...) must be first so delegated initialization finishes before the remaining work. It calls another constructor in the same class; super(...) invokes a superclass constructor. If neither invocation is written, the ordinary form implicitly invokes super(), requiring an accessible no-argument superclass constructor. Constructors are not inherited or overridden receiver methods.

NM004 p.19 and NT001 separately mention restricted prior work in Java 25. Thus the first-call rule is version-bounded, not universal across every version; that mention does not supply newer syntax here.

Checking points: separate entry from completion order, preserve literal types, and check the superclass initialization precondition.

</details>

#### Recall Q19 More than one applicable method

TaggedPoint extends Point. Set A contains static choose(TaggedPoint,Point) and choose(Point,TaggedPoint). For TaggedPoint t=new TaggedPoint(), list applicable candidates and classify choose(t,t), choose(t,(Point)t), and choose((Point)t,t). Independent set B instead has choose(TaggedPoint,Point) and choose(TaggedPoint,TaggedPoint): classify choose(t,t).

A separate one-argument set contains select(Object), select(Circle), and select(Square), where Circle/Square are unrelated Object subclasses. Bodies return their parameter-type names without dereferencing. Classify select(null), select((Circle)null), select((Object)null). Explain declaration legality versus call ambiguity, declaration order, and whether a cast creates an object.

[NM004, physical PDF pp.20-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 50:55, 52:44](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

Set A's choose(t,t) makes both candidates applicable. The first is more specific in parameter one, the second in parameter two; neither dominates across the whole list, making the call ambiguous at compile time.

choose(t,(Point)t) has argument types TaggedPoint,Point, so only choose(TaggedPoint,Point) applies: a Point-typed expression cannot implicitly downcast to the other's TaggedPoint parameter. The reversed cast arrangement selects only choose(Point,TaggedPoint). These upcasts leave the objects unchanged.

Set B's two candidates both apply, but choose(TaggedPoint,TaggedPoint) is equally specific in the first position and more specific in the second, so it uniquely wins. Distinct signatures allow declarations to coexist without guaranteeing a unique method for every call.

Null fits all three reference parameters in the separate set. Circle and Square are incomparable most-specific candidates, so select(null) is ambiguous. A Circle-typed null selects Circle; an Object-typed null selects Object. Their stipulated bodies return the type names without dereferencing, so typed null need not itself cause failure. Casting null to a reference type creates no object.

Applicability and specificity determine selection, not textual order. NT001's matches-first wording is not a declaration-order rule.

Checking points: write expression types before comparing candidates and distinguish selection from body null safety.

</details>

#### Recall Q20 Override compatibility and constructor identity

Use:

~~~
class Staff {
    public double pay() { return 120; }
}
class Lead extends Staff {
    @Override public double pay() { return 190; }
}
Staff a = new Staff();
Staff b = new Lead();
~~~

Determine a.pay()/b.pay() and the two selection stages. Independently replace Lead's method by public int pay() returning 0: overload, valid override, or error at what stage? What does @Override check? May the public access become protected? Distinguish Lead(), a return-type-free Staff() declared inside Lead, and super(). Are constructors inherited? Why does the source int/double example not establish a same-spelling rule for every reference return? Assess the lab's lowercase string.

[NM004, physical PDF pp.25-28,32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [RM001, physical PDF pp.32,56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf); [NM005, physical PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf).

<details><summary>Answer</summary>

The values are 120.0 and 190.0. The compiler checks the available Staff.pay() signature and its double result; the actual Staff or Lead receiver selects the body. @Override asks the compiler to verify overriding intent, rather than creating a signature or performing dispatch.

int pay() has the same zero-argument signature, so it is not a return-only overload. Its primitive return is incompatible with the inherited double return, producing a compile-time error rather than a runtime choice. Narrowing public to protected also breaks the inherited public access contract.

Lead() names Lead's constructor. A return-type-free Staff() inside Lead cannot be a constructor override; constructor names must match their declaring classes. super() instead invokes an accessible superclass constructor for initialization. Constructors are neither inherited nor overridden; default-constructor provision and implicit super calls are separate rules.

The material's same-return wording is bounded by this incompatible primitive example, not a complete rule prohibiting every covariant reference return. No full reference-return treatment is required. NM005 p.6's lowercase string is not the Java String type. Alternative Laidoff class definitions and malformed source output quotes are not one successful program.

Checking points: separate signature matching, return/access compatibility, annotation, initialization, and runtime body selection.

</details>

#### Recall Q21 Subtype tests versus exact class names

Assume demo.Staff, Manager extends Staff, Executive extends Manager, and Specialist extends Manager. One static helper tests instanceof Executive -> 35, then instanceof Manager -> 20, else 12. Another calls getClass().getName(), recognizes only "demo.Executive"/"demo.Manager" with those values, otherwise 12.

Compare results for Executive, Specialist, and null. What changes if Manager is tested first? What does getClass identify? Compare maintaining several such helpers when Researcher is added with class-owned pay overrides and a shared caller. What happens on a direct null.pay() instance call? Does this reasoning ban every type inspection or remove every class dependency?

[NM004, physical PDF pp.29-31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 59:24, 01:00:18, 01:01:17](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The instanceof helper yields 35 for Executive, 20 for Specialist, 12 for null. Executive matches both tested types but uses the first branch; Specialist is a Manager subtype. Null satisfies no instanceof test.

The exact-name helper yields 35 for Executive but 12 for Specialist, whose actual class name is demo.Specialist. Null.getClass() raises NullPointerException before a fallback. getClass describes the actual receiver class, not merely the Staff declaration or a superclass. If Manager is tested first in the first helper, it also catches Executive and returns 20, preventing its later branch.

These are explicit first-true program branches, unlike most-specific overload selection. New employee kinds can require updating each central behavior list; omissions can silently choose the fallback. Overrides place pay behavior in the classes and let callers use a common method, reducing parallel lists. A direct instance pay call still requires a non-null receiver.

This is a maintenance comparison, not a prohibition on every instanceof/getClass use or proof of no class dependencies. The original numeric values have no verified currency; the lecture's superclass/no-import wording and source punctuation defect do not establish other Java rules.

Checking points: distinguish subtype inclusion, exact identity, null fallback/invocation, and branch order.

</details>

#### Recall Q22 Hidden fields, overloads, and dynamic getters

Use these fragments in one package:

~~~
class Point {
    int x = 0, y = 0;
    void move(int dx, int dy) { x += dx; y += dy; }
    int getX() { return x; }
    int getY() { return y; }
    static void show(int x, int y) {
        System.out.println("(" + x + ", " + y + ")");
    }
    static void show(float x, float y) {
        System.out.println("(" + x + ", " + y + ")");
    }
}
class RealPoint extends Point {
    float x = 0.0f, y = 0.0f;
    @Override void move(int dx, int dy) {
        move((float)dx, (float)dy);
    }
    void move(float dx, float dy) { x += dx; y += dy; }
    @Override int getX() { return (int)Math.floor(x); }
    @Override int getY() { return (int)Math.floor(y); }
}
RealPoint r = new RealPoint();
Point p = r;
r.move(-1.5f, 2.25f);
p.move(1, -3);
Point.show(p.x, p.y);
Point.show(r.x, r.y);
Point.show(p.getX(), p.getY());
Point.show(r.getX(), r.getY());
~~~

Track both field pairs after each move, selected signatures/bodies, and all four outputs. Explain floor for negative fractions. Independently, inside a Child instance method, a Parent static int count=3 is hidden by Child static double count=6.5. What do count, super.count, and ((Parent)this).count read? Is the parent declaration removed?

[NM004, physical PDF pp.34-37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 01:06:05, 01:07:58, 01:09:54](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

One object contains distinct Point int fields and RealPoint float fields. The first call selects move(float,float) through RealPoint, changing only its floats to (-1.5,2.25). The second selects move(int,int) through Point at compile time, dispatches to RealPoint's int override, and delegates via float casts. The float pair becomes (-0.5,-0.75); the parent int pair stays(0,0). These chosen binary fractions are exact.

~~~
(0, 0)
(-0.5, -0.75)
(-1, -1)
(-1, -1)
~~~

p.x/p.y select Point's fields and show(int,int); r.x/r.y select RealPoint's fields and show(float,float). Both getter pairs dispatch to RealPoint, whose floors are -1.0 and -1.0, then int -1. Their int results select show(int,int). Truncating negative fractions toward zero would instead give 0 and would not implement these getters.

The independent static-field reads are 6.5, 3, 3. Hiding leaves separate declarations selected through the relevant expression type/qualifier. It does not replace one runtime-dispatched field. The cast changes expression type, not the object.

The source's complete four-show calculation supplements the portion explicitly skipped at NT001 01:09:54. The printed type is float despite an uncertain spoken double reference.

Checking points: separate field selection, overload signature, receiver body, and each field's actual mutation.

</details>

#### Recall Q23 Static overload selection with a dynamic call inside

Analyze this independent illustration:

~~~
class Animal {
    String sound() { return "base"; }
    static String describe(Animal x) {
        return "A[" + x.sound() + "]";
    }
    static String describe(Dog x) {
        return "D[" + x.sound() + "]";
    }
}
class Dog extends Animal {
    @Override String sound() { return "woof"; }
}
Animal a = new Dog();
Animal plain = new Animal();
Dog d = new Dog();
~~~

Find Animal.describe(a), Animal.describe(d), Animal.describe(plain), Animal.describe((Dog)a), and ((Animal)d).sound(). Give each selected describe signature and inner sound body. Does runtime sound selection reselect describe(Dog)?

Separately, Polynomial declares times(Polynomial), times(int), times(float), times(Polynomial,int), with unspecified bodies. Match arguments 4, 2.5f, and(anotherPolynomial,2), where anotherPolynomial has that declared type. Explain the diagram's signature-to-table and actual-class-to-superclass, method-data-to-code stages. Can it establish numerical products, erased overload bodies, universal memory layout, repeated linear search, or performance bounds?

[NM001, physical PDF pp.4-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NM004, physical PDF pp.39-43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NT001, 01:15:28, 01:16:18, 01:18:07](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The values are `A[woof]`, `D[woof]`, `A[base]`, `D[woof]`, and `woof`.

The Animal-typed a selects describe(Animal); inside, x refers to a Dog and sound uses Dog.sound. Dog-typed d selects the more-specific describe(Dog), again using Dog.sound. Animal-typed plain selects describe(Animal) and its actual Animal uses Animal.sound. The permitted (Dog)a cast succeeds and gives a Dog-typed argument for describe(Dog), without changing the object. Casting d to Animal does not suppress Dog.sound.

Static methods have no runtime receiver override, but their bodies may contain instance calls that do dispatch. Choosing the sound body does not restart outer overload selection. The changed complete program is synthetic, not a supplied exact source program.

The Polynomial arguments select times(int), times(float), and times(Polynomial,int). The schematic extracts signatures, registers table entries, and maps argument types to a selected entry. For an overridden instance signature, the later diagrams depict starting at the actual class, following superclasses if necessary, locating method data/code, and executing. Declared types and legal signatures are still checked by the compiler.

No missing Polynomial bodies or parser support numerical outputs. Resolving calls does not imply deletion of overloaded implementations, contrary to NT001's overbroad binary wording. The diagrams are not a universal physical JVM layout, mandated repeated linear traversal, or timing evidence.

Checking points: resolve the outer signature before the inner receiver; preserve the distinction between semantics and schematic implementation.

</details>

#### Recall Q24 Types and evaluation determine operator behavior

Evaluate or classify these independent snippets:

~~~
9 + 5
1.25 + 2.5
"score=" + 2 + 5
2 + 5 + " points"
9 & 5
9 | 5
true & false
true | false
String s = "Cat" + " sleeps.";
s += "Quiet!";
float rem = 0.75 % 0.5;
~~~

Show integer bits, exact strings/spacing, and whether += mutates a String. Fix only the remainder variable type and delimit floating-point exactness, comparing the source p.44 declaration.

For int denominator=0,num=12, compare denominator!=0 && num/denominator==1 with single &. Compare true||check() with true|check(), where check returns boolean and may have a side effect. Explain results, skipped/evaluated operands, and failures. Can a class define its own + overload?

[NM004, physical PDF pp.44-46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [M002, physical PDF pp.38-42,48,66-70](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf); (T007,24:17,25:11,26:11); [NT001, 01:19:07, 01:20:06](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The additions give 14 and 3.75. The strings are `score=25` and `7 points`: left-associated + concatenates once a String is reached, whereas the second first adds the integers.

~~~
9:   1001
5:   0101
AND: 0001 = 1
OR:  1101 = 13
~~~

Boolean true&false is false; true|false is true. Those single-symbol boolean forms evaluate both operands rather than applying integer bit patterns.

s first denotes `Cat sleeps.`, then `Cat sleeps.Quiet!`. Neither adjacent string supplies an extra space. += assigns the concatenated result back to the variable without mutating the old immutable String.

The decimal literals are double, so the remainder is double and cannot implicitly narrow into float. The separate fix is `double rem = 0.75 % 0.5;`. These particular binary-exact inputs give 0.25. General decimal floating arithmetic may round: the source `float f = 0.5 % 0.3;` both has the same invalid assignment type and promises no exact decimal 0.2. The repaired declaration is distinct from the original and not an observed run.

For denominator 0, && sees a false left test and skips division, giving false. Single & evaluates the integer division and raises ArithmeticException before completing a boolean result. true||check() skips check; true|check() evaluates it, so side effects or exceptions matter despite the same possible truth result. M002/T007 provide this historical short-circuit distinction rather than a repaired NT001 operator sequence.

Java defines these built-in meanings; class authors cannot invent arbitrary + overloads.

Checking points: retain operand types, exact text, literal-conversion conditions, and evaluation order.

</details>

#### Recall Q25 Cast compatibility and failure stages

Life declares breed(); Animal extends Life, adding move() and sound(); Mammal extends Animal; Dog extends Mammal and overrides sound(); Beagle extends Dog without another override.

~~~
Dog dog = new Beagle();
Life a = new Animal();
Life b = new Life();
Life absent = null;
~~~

Independently classify Mammal m=dog, Animal x=(Animal)dog, Beagle y=(Beagle)dog, a.move(), ((Animal)a).move(), ((Animal)b).move(), and ((Animal)absent).move(). Separate member availability, cast compatibility, and null invocation. How many extra Beagles do the first assignments create; does dog's declaration change? Give a guarded Life-to-Animal move call, explain upcasting's purpose, and compare ((Animal)dog).sound() with an explicit super method call.

[NM004, physical PDF pp.47-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [RM001, physical PDF pp.37-47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf); [NT001, 01:22:07, 01:23:53, 01:24:50](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

The Mammal assignment is implicit upcasting and the Animal cast explicit upcasting, both retaining the Beagle. The Beagle downcast is permitted and succeeds for that actual object. They create no extra Beagle beyond new Beagle(), and dog stays declared Dog.

a.move() fails at compile time: Life has no move signature. ((Animal)a).move() has a permitted typed expression and compatible actual Animal, so move is callable. ((Animal)b).move() passes the related-type compile-time cast check but raises ClassCastException on the actual Life before move. Casting absent to Animal succeeds and yields null, but its move invocation raises NullPointerException.

~~~
if (a instanceof Animal) {
    ((Animal)a).move();
}
~~~

The guard rejects incompatible objects and null for this stable local reference. Upcasting lets callers depend on a general contract without concrete implementation details. Casts change an expression's reference type, never an object's class or a variable declaration.

((Animal)dog).sound() still uses Dog's override on the Beagle receiver because Beagle supplies no further override. A suitable super.sound() inside a subclass instead directly invokes its parent implementation; a superclass cast is not that operation.

Checking points: identify the first failure stage and use actual compatibility rather than missing behavior as the downcast criterion.

</details>

#### Recall Q26 A type placeholder preserves a relationship

At the brief introductory level, explain reuse in `List<E>`/`AbstractList<E>`, what repeated E preserves, and how ? in Collection<?> differs. Assess with reasons: `List<Integer>` stores primitive int as its type argument; it automatically becomes `List<Number>`; every element is automatically unboxed merely by being in the list; ? permits any value and operation; a generic parameter freely changes at runtime; generics remove every runtime type error. Distinguish choosing a type argument from expression-specific boxing/unboxing and from separate overloads. Why are detailed generic classes, static members, methods/constructors, bounds/wildcard algorithms, and Producer-Consumer not required here?

[NM004, physical PDF pp.52,59,66](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NM001, physical PDF pp.33-35,56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NT001, 16:41, 01:25:47, 01:26:45](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2).

<details><summary>Answer</summary>

A named type parameter lets one reusable structure consistently relate the types of its operations rather than duplicate it for each concrete type. E names that element type; choosing Integer supplies the corresponding reference type. ? denotes an unknown element type at a use rather than a declared name reusable elsewhere. Unknown does not license arbitrary insertion or operations.

All six claims are false. Integer is a reference wrapper. Its subtype relation to Number does not automatically make `List<Integer>` a `List<Number>`; the parameterized lists are not automatically covariant. Boxing or unboxing occurs at specific expressions needing the conversion, not because E itself means primitive int. A type argument is not free runtime type mutation. Generic checks do not eliminate all cast/null runtime errors.

Overloads offer distinct signatures and possibly bodies for particular inputs. A placeholder instead preserves related uses of a type within a shared structure, the motivation called parametric polymorphism. NT001's E-as-wildcard and arbitrary-runtime-type wording must be qualified. NM004 p.59 supports compile-time type reasoning, but its complete-runtime-error-immunity generalization is also too broad. These are attributed source errors, not silently repaired quotations.

NT001 explicitly leaves detailed generics for next time. Later printed implementation pages and the Producer-Consumer lab do not turn the brief introduction into those full topics. No bounded algorithm, generic class, or scheduler implementation is required.

Checking points: preserve named parameters and wrapper types, distinguish conversions at expressions, and respect the future boundary.

</details>

### Integrated Practice

#### Practice P01 Representation, equality, hashing, and ordering

Use this fictional immutable value class. Labels and comparison arguments are non-null.

~~~
final class Parcel implements Comparable<Parcel> {
    private final String label;
    private final int rank;
    Parcel(String label, int rank) {
        this.label = label; this.rank = rank;
    }
    @Override public String toString() { return label; }
    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Parcel)) return false;
        Parcel p = (Parcel)o;
        return rank == p.rank && label.equals(p.label);
    }
    @Override public int hashCode() { return 7; }
    @Override public int compareTo(Parcel p) {
        return rank > p.rank ? 1 : rank < p.rank ? -1 : 0;
    }
}
Parcel a = new Parcel("oak", 4);
Parcel b = new Parcel("oak", 4);
Parcel c = new Parcel("oak", 1);
Parcel d = new Parcel("elm", 4);
~~~

1. Compute a==b, a.equals(b), a.equals(c), a.equals(null), a.compareTo(c), and a.compareTo(d). What do identical representations and the shared hash prove?
2. A collection is [a,null,c,b,d,null]. Frequency counts e==null for a null target, otherwise target.equals(e). Find counts for a fresh Parcel("oak",4) and null, naming contributing positions. Does the argument type guard protect nullable fields too?
3. A separate `List<Parcel>` contains [a,c,b,d], without null. After ascending sort, which element must be first and which comparison-equivalence group follows? No tie-order rule is required. Explain why printed labels cannot establish the comparison criterion and what compareTo(null) does.
4. Assess the constant hash's equality implication, compare ordering equivalence with equals, and explain ArrayList-to-LinkedList substitution for these supported List operations.

[NM001, physical PDF pp.17-24,33-46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [NM004, physical PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf).

<details><summary>Answer</summary>

The six results are false, true, false, false, 1, and 0. a and b are distinct but match label and rank. c prints the same oak representation but has different rank, so equals is false. Null fails instanceof. a ranks above c, while a and d tie in rank despite different labels. Neither equal representations nor comparison zero proves equals true.

The fresh target matches positions 0 and 3, a and b, so frequency is 2. c fails on rank, d on label, and the two null arguments fail the type guard. A null target takes the separate branch and counts positions 1 and 5, also 2. Null.equals would be invalid. Argument guarding allows a safe cast but does not protect a null label receiver: if the stipulated non-null-label condition were removed, comparing distinct objects could fail at label.equals.

For sorting, c must precede every rank-4 object. The following comparison-equivalence group is {a,b,d}; the task needs no order inside it. The representations show oak first and two oak/one elm in the following group, concealing rank. Passing null to compareTo directly dereferences p.rank and raises NullPointerException. Null-target frequency handling does not make comparison null-safe.

With final class, fixed fields, and the non-null-label condition, equality by label contents and rank is reflexive, symmetric, transitive, consistent, and rejects null. Every equal pair returns the constant hash 7, satisfying the required implication. Unequal objects also return 7, which is a permitted collision rather than proof of equality. It establishes neither unique hashes nor measured performance. This new illustrative constant is not a missing original Shoes implementation or a recalled set-repair answer.

List construction can be changed from ArrayList to LinkedList while preserving these supported add/get/remove/size and sort operations under their contracts. It does not make storage or speed identical.

Checking points: show each counting contribution; distinguish null target, nullable field, null comparison argument, representation, equality, hashing, and ordering.

</details>

#### Practice P02 Shared initialization and abstract behavior

Analyze this small counter model, independent of the supplied lab.

~~~
interface Reportable {
    String report();
    default String heading() { return "value"; }
    static String family() { return "counter"; }
}
abstract class Counter implements Reportable {
    private int ticks;
    protected int value;
    Counter(int start) { value = start; }
    public final void tick() { ticks++; change(); }
    protected int ticks() { return ticks; }
    protected abstract void change();
}
class StepCounter extends Counter {
    private int delta;
    StepCounter() { this(4, 2); }
    StepCounter(int start, int delta) {
        super(start); this.delta = delta;
    }
    @Override protected void change() { value += delta; }
    @Override public String report() {
        return value + " after " + ticks();
    }
}
class DownCounter extends Counter {
    private int delta;
    DownCounter(int start, int delta) {
        super(start); this.delta = delta;
    }
    @Override protected void change() { value -= delta; }
    @Override public String report() {
        return value + " after " + ticks();
    }
}
Counter[] counters = new Counter[3];
counters[0] = new StepCounter();
counters[2] = new DownCounter(10, 3);
for (int round = 0; round < 2; round++) {
    for (Counter counter : counters) {
        if (counter != null) counter.tick();
    }
}
for (Counter counter : counters) {
    if (counter != null)
        System.out.println(counter.heading() + ": " + counter.report());
}
~~~

1. Trace StepCounter's constructor delegation and common/subclass initialization. Distinguish constructor invocations from instance overriding.
2. Track both objects after each round and give the output. Explain the null slot and the effect of removing either guard.
3. Identify the relevant abstract/default/static/final/private/protected members. Why can Counter defer report; why must implementations be public? How do subclasses use ticks without direct private-field access?
4. For Reportable r=counters[0], independently classify r.report(), r.tick(), and ((Counter)r).tick(). Explain why both an interface and abstract class are useful and whether a new counter subtype needs a caller type branch.

[NM001, physical PDF pp.8-9,26-32,47,49-56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [RM001, physical PDF pp.48-51,55-67](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf); [NM004, physical PDF pp.18-19,32,47-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf).

<details><summary>Answer</summary>

StepCounter() selects this(4,2), then StepCounter(int,int) invokes Counter(int) with 4. Counter's ordinary implicit super() initializes Object before its body. Common value is assigned 4 and private ticks begins at zero. Returning to StepCounter assigns delta=2. DownCounter similarly receives value=10 and delta=3. These initialize one new object per construction; constructors are not dynamically overridden.

Slot 1 remains null. Each non-null counter receives one tick per round. After round one, StepCounter is (value 6, ticks 1), DownCounter (value 7, ticks 1). After round two, they are (8,2) and (4,2). The lines are:

~~~
value: 8 after 2
value: 4 after 2
~~~

Counter.tick increments its private count and then calls change on the actual receiver, selecting the StepCounter addition or DownCounter subtraction. report similarly uses the concrete receiver body. Removing the first guard invokes tick on the null slot and stops that loop; removing the second can invoke heading/report on null and stop printing. Array allocation creates reference slots, not a third counter.

The inherited concrete tick is final and cannot be overridden, yet its call to abstract change is dynamically dispatched. change is a protected superclass obligation; report is a public interface obligation. Abstract Counter may defer report, but concrete subclasses must satisfy outstanding methods with appropriate access. The protected ticks() method allows reading the private count through Counter code. heading is an inherited default instance body; family is an interface static called as Reportable.family(), not receiver-dispatched.

r.report() is permitted through Reportable and uses StepCounter.report. r.tick() fails at compile time because the interface has no tick signature. ((Counter)r).tick() succeeds for this actual StepCounter and would advance its state; this diagnostic is independent of the completed two-round trace. The cast neither changes the object nor r's declaration.

The interface offers a reporting contract even for unrelated types. Counter shares mutable state, common construction, and tick behavior while requiring meaningful change behavior. A new subtype can provide its change/report without a type branch in the caller loops.

Checking points: trace each object and construction path, separate private-state access from inherited behavior, and check declared member access before runtime compatibility.

</details>

#### Practice P03 Separate four selection mechanisms

Use these class fragments. Treat the later diagnostic cases independently from the main sequence.

~~~
class Vehicle {
    int load = 6;
    static String kind() { return "vehicle"; }
    String sound() { return "roll"; }
    void carry(int n) { System.out.println("V-int:" + n); }
    void carry(double n) { System.out.println("V-double:" + n); }
    static String inspect(Vehicle v) { return "V/" + v.sound(); }
    static String inspect(Cart c) { return "C/" + c.sound(); }
}
class Cart extends Vehicle {
    int load = 9;
    static String kind() { return "cart"; }
    @Override String sound() { return "rattle"; }
    @Override void carry(int n) { System.out.println("C-int:" + n); }
    String extra() { return "basket"; }
}
Vehicle v = new Cart();
Cart c = new Cart();
Vehicle plain = new Vehicle();
System.out.println(v.load + " " + c.load);
System.out.println(v.kind() + " " + c.kind());
System.out.println(Vehicle.inspect(v));
System.out.println(Vehicle.inspect(c));
System.out.println(Vehicle.inspect(plain));
v.carry(2);
v.carry(2.0);
System.out.println(((Vehicle)c).sound());
System.out.println(((Cart)v).extra());
~~~

Give all nine output lines. For each, identify expression types, selected fields/signatures, and any runtime receiver body. Independently classify v.extra(), ((Cart)plain).extra(), and ((Cart)(Vehicle)null).extra(). If only v's initializer changes to new Vehicle(), explain changes to inspect(v), v.carry(2), and the explicit Cart cast; do its declared type and compile-time overload choices change? Explain why this is not declaration-order lookup or object-class mutation by casting.

[NM004, physical PDF pp.20-23,34-43,47-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf); [NM001, physical PDF pp.4-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf); [RM001, physical PDF pp.37-47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf).

<details><summary>Answer</summary>

The nine lines are:

~~~
6 9
vehicle cart
V/rattle
C/rattle
V/roll
C-int:2
V-double:2.0
rattle
basket
~~~

v.load reads Vehicle's field through its declared Vehicle expression; c.load reads Cart's separate hidden declaration. v.kind() selects Vehicle's static declaration and c.kind() Cart's; actual objects do not override static calls.

Vehicle.inspect(v) selects inspect(Vehicle) using v's declared type. Inside, its actual Cart receiver selects Cart.sound, so it returns V/rattle. The Cart-typed c selects inspect(Cart), yielding C/rattle through that same sound override. plain selects inspect(Vehicle) with an actual Vehicle body, giving V/roll. Inner receiver dispatch never restarts outer overload selection.

v.carry(2) selects carry(int) at compile time and dispatches to Cart's override. v.carry(2.0) selects carry(double); Cart supplies no override, so Vehicle's inherited body prints V-double:2.0. Casting c to Vehicle leaves Cart.sound selected. Casting v to Cart succeeds for the actual Cart and permits extra, yielding basket.

Independently, v.extra() is a compile-time unavailable-member error through Vehicle. ((Cart)plain).extra() has a permitted related-type cast but raises ClassCastException on the actual Vehicle before extra. The null cast succeeds but its extra invocation raises NullPointerException.

If v instead starts with new Vehicle(), its declaration and selected inspect(Vehicle)/carry(int) signatures remain unchanged. The actual body gives V/roll and V-int:2. Its Cart downcast now fails. Expression type, hidden-member selection, overload signature, and actual receiver body are distinct decisions. Textual declaration order does not choose the winner; a cast never changes the object's class.

Checking points: list all selection stages and check actual downcast compatibility before attempting subclass behavior.

</details>

## Sources

[NT001, Inheritance and Polymorphism transcript](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2) supports the Object/interface recap, abstract classes, overloads, dispatch, casts, and brief generics introduction. The lecture date is unconfirmed; upload/title/timetable and relative exam/lab references do not date it. Timestamps are supplied utterance starts, not endpoints. The text and its source qualifications leave audio, gaps, speaker identity, omitted turns, and board/live code unverified.

[NM001, Inheritance 2](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), physical PDF pp.3-56, supplies detailed Object/interface/comparison and abstract-class examples. [NM004, Polymorphism](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), physical PDF pp.4-50,52, supports the selected polymorphism topics; pp.59,66 only qualify introductory type claims. Printed examples are material supplements, not all newly spoken. Detailed generic implementations and Producer-Consumer remain outside this note.

[NM005, Lab 6 Polymorphism](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf), physical PDF pp.4-6, corroborates only the selected recap. The source has 36 pages. Its Lab 1 cover conflicts with the Lab 6 designation; session-local announcements establish neither this lecture date nor current policy.

[RM001, Inheritance 1](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf), physical PDF pp.14,17-23,26,30-35,37-51,55-68, and [M002, Java Basics 1](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf), physical PDF pp.38-42,47-49,61-62,66-70, provide optional prerequisites. T007, 2026-09-08, supplied starts 15:04,15:58,16:54,17:48,18:44,19:41,23:27,24:17,25:11,26:11,27:10,28:06, is the separate historical reference/short-circuit recap.

The unofficial recalled references cp_2025_1_midterm_recall (2025 spring midterm, filename-only instructor 김상한) and cp_2026_1_final_recall (2026 spring final, filename-only instructor 유영재) have no verified official answers. Their filename attributions differ from current instructor Jaemin Yoo. Connections are limited to interface meaning (midterm Q2, physical p.1), this/super (Q5,p.3), signature/private-method/constructor/hash conditions (final Q1(a-d),p.1), selection traces (Q2,p.2; Q9,p.6), equality/hash consistency (Q3,p.3), and overload ambiguity (Q8,p.5). They establish no current style, frequency, or scope. The final warns of uncertain order/content; duplicate (f), incomplete queue wording, and blank 1-(i) are not repaired or reconstructed.

PDF page views: [Java Basics 1, physical p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-038); [Inheritance 2, physical p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004); [Polymorphism, physical p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-004); [Lab 6 Polymorphism, physical p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-004); [Inheritance 1, physical p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-037).
