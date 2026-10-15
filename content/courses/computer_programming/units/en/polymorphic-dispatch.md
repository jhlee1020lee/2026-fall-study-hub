---
title: "Overriding, Dispatch, and Casting"
description: "Separate declared-type selection from receiver overrides while tracing fields, operators, and casts."
course: "computer_programming"
unit_id: "polymorphic-dispatch"
lang: "en"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["8 polymorphism.pdf", "Lecture 2 Java Basics 1.pdf", "Lab 6 Polymorphism.pdf", "7 inheritance 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/en/2026-09-01-lecture-01", "courses/computer_programming/lectures/en/2026-09-08-lecture-03", "courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

## Overriding and dispatch through the receiver

### Giving an instance method contract a different implementation

[Method overloading](method-overloading.md) distinguished signatures by the number and types of inputs. Overriding addresses a different need: request the same operation through a common type while executing the implementation appropriate to the actual object. In NM004, `Employee` and `Manager` provide different bodies for the same `getSalary()` contract. [computer_programming:NM004, PDF pp.25-26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
class Employee {
    public double getSalary() { return 180; }
}

class Manager extends Employee {
    @Override
    public double getSalary() { return 250; }
}
~~~

The calls on `new Employee()` and `new Manager()` produce `180.0` and `250.0`, respectively. Both methods return `double`, so their integer literals are converted to that return type. `@Override` expresses the intent for the compiler to check that an inherited method is being overridden. The annotation neither creates another signature nor turns a method with different parameters into an override.

Distinguish the declared return type from the type of the returned expression. The first `Laidoff` alternative is `public double getSalary() { return 0; }`. Its expression `0` can be converted to the declared `double` return type. The second alternative, `public int getSalary() { return 0; }`, changes the declaration's return type. Its name and empty parameter list remain the same, so it is not a separate overload. It is an override with a return type incompatible with the parent's `double`. The diagnostic on p.28 specifically says that `int` is not compatible with `double`. Read p.27's “return type must also be the same” in this primitive-return comparison; this example does not establish that every possible reference return must always have exactly the same type. [computer_programming:NM004, PDF pp.27-28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 55:45]]

The two declarations named `Laidoff` on p.27 are alternatives for comparison. The print statements on pp.26 and 28 also contain malformed closing quotation marks. Reading the central class declarations above does not establish that every line of those pages forms an executable program without changes. The broken diagnostic discussion at 55:45–56:45 in the undated transcript is not silently completed into a new quotation.

Constructors are not overridden in this way. Initialization inside `Manager` is declared with its own class name, as `Manager()`, and connects parent initialization through `super(...)` when needed. A return-type-free declaration `Employee()` inside `Manager` cannot override the parent's constructor. Constructors are not inherited instance methods. [computer_programming:NM004, PDF p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The Object-method exercise on NM005 p.6 can be read with the same distinction. Its lowercase `string` should not be adopted as the exact Java type name `String`. Explaining the proper return type of `toString()` is separate from silently correcting a quotation. The detailed conditions of the Object contract are developed in the [Object contracts and interfaces unit](object-contracts-interfaces.md). [computer_programming:NM005, PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Inspecting types outside an object versus delegating behavior to it

An external helper can select values by inspecting types without using overriding. The source's `HumanResources.getSalary(Employee e)` is a `static` method using these branches. The printed numbers 960, 250, and 180 have no established currency unit. [computer_programming:NM004, PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
if (e instanceof Executive) {
    return 960;
} else if (e instanceof Manager) {
    return 250;
} else {
    return 180;
}
~~~

This helper does not obtain its result by invoking an override of `e.getSalary()`. It checks each type itself and selects a constant in its own body. `instanceof Manager` can be true for a Manager object or an object of a Manager subtype. Consequently, branch order can matter when the tested types are related by inheritance. Handling a broader type first may prevent a later, more specific case from being reached. This observation does not invent a precise Executive–Manager inheritance relationship that the example has not supplied.

Another version examines `e.getClass().getName()` and compares it with `"personnelpkg.Executive"` or `"personnelpkg.Manager"`. This obtains the **exact name of the actual class**, not the name of its superclass. A new Manager subtype can satisfy `instanceof Manager` without having the class-name string `"personnelpkg.Manager"`. These are different tests. There is also a null distinction: `null instanceof Manager` is false, whereas calling the instance method `getClass()` through a null reference cannot succeed. [computer_programming:NM004, PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:00:18]]

When types such as CEO, Cleaner, and Researcher are added, an external branch list must be updated. If several helpers duplicate those branches, an omission can send a new kind of object to the default value. Overriding offers an alternative: each class owns the behavior, and callers use the shared method. The undated transcript's discussion concerns maintenance responsibilities. It does not establish that every use of `instanceof` or `getClass()` is wrong, or that all class dependencies disappear. The helper's own usage still constructs concrete classes. The malformed punctuation in p.31's `else { return 180 };` is not presented as successful source code. [computer_programming:NM004, PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:01:17]]

### RealPoint: tracking fields, overloads, and overrides separately

A repeated name does not make every selection a runtime dispatch. Start with field hiding. On p.34, `Point` declares `static int x = 2`, while subclass `Test` declares `static double x = 4.7`. Inside a `Test` instance method, reading `x`, `super.x`, and `((Point)this).x` gives `4.7`, `2`, and `2`. Both fields remain separate declarations. The cast does not turn the object into another object. Field selection must be distinguished from overriding an instance method. [computer_programming:NM004, PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The RealPoint example combines three selection mechanisms. Parent `Point` supplies integer coordinate fields, a basic movement method, and two `show` overloads. [computer_programming:NM004, PDF p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
class Point {
    int x = 0, y = 0;
    int color;

    int getX() { return x; }
    int getY() { return y; }
    void move(int dx, int dy) { x += dx; y += dy; }

    static void show(int x, int y) {
        System.out.println("(" + x + ", " + y + ")");
    }

    static void show(float x, float y) {
        System.out.println("(" + x + ", " + y + ")");
    }
}
~~~

The subclass declares distinct `float` fields with the same names and changes movement and coordinate access. [computer_programming:NM004, PDF p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
class RealPoint extends Point {
    float x = 0.0f, y = 0.0f;

    void move(int dx, int dy) {
        move((float)dx, (float)dy);
    }

    void move(float dx, float dy) {
        x += dx;
        y += dy;
    }

    int getX() { return (int)Math.floor(x); }
    int getY() { return (int)Math.floor(y); }
}
~~~

`move(int, int)` has the parent's signature and overrides it. `move(float, float)` has a different parameter list and is an overload. The overriding getters return the floor of the actual floating-point coordinates as integers. For example, mathematically `floor(-1.2) = -2`, which differs from a simple integer cast's truncation toward zero.

There is one object in the following calls. Assigning `p = rp` does not create another Point; it stores a reference to the same RealPoint through a parent type. [computer_programming:NM004, PDF p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
RealPoint rp = new RealPoint();
Point p = rp;
rp.move(1.71828f, 4.14159f);
p.move(1, -1);

Point.show(p.x, p.y);
Point.show(rp.x, rp.y);
Point.show(p.getX(), p.getY());
Point.show(rp.getX(), rp.getY());
~~~

Initially, the parent's `int x, y` and the child's `float x, y` are all zero. Follow the changes in separate steps.

1. The declared type of `rp` and the two `float` arguments select `move(float, float)`.
2. Its `x, y` are the RealPoint fields, so only the child coordinates change.
3. The second call, `p.move(1, -1)`, selects the `move(int, int)` signature available through the declared type Point.
4. The actual receiver is RealPoint, so its override of that signature executes.
5. That body delegates to the `float` overload, adding `1.0f, -1.0f` to the child coordinates.

The `Point.move` body that increments the parent fields is not executed along this path. Those integer fields remain `0, 0`. The child coordinates are displayed in the source as `2.7182798, 3.14159`. A `float` representation does not guarantee the same printed form as ideal decimal addition yielding `2.71828`. These displayed values are the material's values, not measurements from a new execution.

| Output call | Type or field selected first | Body or value used | Source output |
|---|---|---|---|
| `Point.show(p.x, p.y)` | Point's `int` fields | 0, 0 passed to `show(int, int)` | `(0, 0)` |
| `Point.show(rp.x, rp.y)` | RealPoint's `float` fields | Child coordinates passed to `show(float, float)` | `(2.7182798, 3.14159)` |
| `Point.show(p.getX(), p.getY())` | Calls with declared return type `int` | Floors returned by RealPoint getters | `(2, 3)` |
| `Point.show(rp.getX(), rp.getY())` | Calls with declared return type `int` | The same RealPoint getters | `(2, 3)` |

This explains how the same object can give `p.x = 0` and `p.getX() = 2`. The former reads the parent field selected through the reference's declared type. The latter dispatches to an actual-receiver method body that reads the child field. The `show` overload is selected from the **types of its argument expressions**. It is not selected because a getter happens to return the value 2; its declared `int` return type determines that part of the selection.

The undated transcript at 01:03:10–01:09:54 explains the mechanisms but skips the complete four-call trace. The detailed calculation above is material-based supplementation from NM004 pp.35–37. The spoken `double` at 01:07:58 is not silently turned into a quotation saying the printed `float`. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:03:10]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:07:58]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:09:54]]

The unofficial recalled final from a different instructor connects parent references, static methods, fields, and overrides through the same separation. First establish that changing the type through which an object is viewed does not remove the same receiver's instance override. This connection does not reproduce the original full code or its output answers. [EX:cp_2026_1_final_q02 p.2]

### Compile-time selection followed by runtime implementation selection

The course material calls compile-time overloading static/syntactic polymorphism and receiver-dependent overriding dynamic/pure polymorphism. Here, the classification word “static” is separate from the `static` method modifier. An instance method's overload signature can also be selected at compile time. [computer_programming:NM004, PDF pp.39-40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The three Polynomial calls have the following argument lists.

| Argument form | Selected parameter list |
|---|---|
| `poly.times(9)` | `int` |
| `poly.times(85.2f)` | `float` |
| `poly.times(new Polynomial(...), 3)` | `Polynomial, int` |

In the complete p.41 figure, signatures from four `times` declarations correspond to method-table entries, and the three calls connect to entries matching their argument lists. `times(Polynomial)` is another candidate, but the two-argument call corresponds to `times(Polynomial, int)`. The figure explains overload selection. It does not mean that every unselected method body disappears from the binary. Neither the Polynomial bodies nor the constructor's string interpretation is supplied, so this table does not establish any resulting polynomial calculation. [computer_programming:NM004, PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

For `Employee e = new Manager(); e.getSalary();`, answer two different questions in sequence. First, does the declared type Employee permit the `getSalary()` call? Second, which implementation of that instance-method signature belongs to the actual Manager receiver? The compiler does know the variable's declared type. What differs is the check made through that type and the implementation selected for the actual object.

The pp.42–43 figures depict the second selection in stages: start with the current class's method, follow direct superclasses toward Object if needed, refer from the selected method data to its code location, and execute the method code. Read the Method Area, RT constant pool, Heap Memory boxes, and their arrows as a schematic of this process. They do not establish one exact storage layout for every JVM, a mandatory linear hierarchy search on every invocation, or a universal performance penalty for runtime dispatch. The uncertain compiler, binary-deletion, and search-cost statements at 01:15:28–01:18:07 in the undated transcript do not justify those stronger conclusions. [computer_programming:NM004, PDF pp.42-43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:15:28]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:18:07]]

A numeric-argument item in the unofficial recalled final from a different instructor combines overloads and overrides. Its transferable reasoning is the same two-stage procedure: use the methods visible at the call site and the argument types to select a signature, then, for an instance method, locate that signature's override for the receiver. Runtime dispatch does not restart selection across all other overloads. [EX:cp_2026_1_final_q09 p.6]

### Operator meanings depend on operand types

The idea of a shared notation with several meanings also appears in operators. The material introduces this as operator overloading, while distinguishing it from user-defined operator overloads, which Java does not provide. The task here is to read the meanings the language already assigns to different operand types. [computer_programming:NM004, PDF pp.44-46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| Expression | Meaning | Result |
|---|---|---|
| `10 + 20` | Integer addition | `30` |
| `1.5 + 2.0` | Floating-point addition | `3.5` |
| `"10" + "20"` | String concatenation | `"1020"` |
| `"sum = " + 30` | Concatenation of a String and a value | `"sum = 30"` |

The embedded illustration on p.44 contains `String s = "Dog" + " barks.";` followed by `s += "Too Loud!";`. After the first statement, the value is `"Dog barks."`; after the second, it is `"Dog barks.Too Loud!"`. Neither the end of the first value nor the beginning of the added text supplies a space, so none appears between the period and `Too`. The `+=` concatenates and assigns the result back to `s`. It does not mutate an immutable String's contents; the variable's reference is updated to the concatenated result. [computer_programming:NM004, PDF p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

The same illustration's `float f = 0.5 % 0.3;` is not a valid assignment as printed. Applying M002's literal and conversion rules, unsuffixed `0.5` and `0.3` are `double` literals, making the remainder expression `double` as well. It cannot be assigned to `float` without an explicit conversion. A separately written teaching repair, `double f = 0.5 % 0.3;`, aligns the variable type. It is neither the original quotation nor an execution record. Binary representation also prevents a guarantee of exactly decimal 0.2. The undated transcript's floating-point `%` comment at 01:19:07 is distinct from this material-based type analysis. [computer_programming:M002, PDF pp.40-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:19:07]]

For integers, `&` and `|` operate on individual bits. The source's 6 and 3 have relevant low three bits `110` and `011`. Keeping positions where both bits are 1 gives `010 = 2`; keeping positions where either bit is 1 gives `111 = 7`. [computer_programming:NM004, PDF p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
  110          110
& 011        | 011
-----        -----
  010          111
~~~

For boolean operands, `true & false` is false and `true | false` is true. Distinguish logical combination of whole boolean values from bitwise operations on integers. Also distinguish boolean `&`/`|`, which evaluate both operands, from short-circuit `&&`/`||`. The latter can omit the right operand: `&&` when the left is false, and `||` when the left is true. Even if the final truth values agree, the evaluation process need not.

For example, with integer `denominator = 0` and `numerator = 100`, `denominator != 0 && numerator / denominator > 2` does not evaluate the division because the left side is false. Replacing `&&` with `&` evaluates the right side too, causing an integer division-by-zero problem. This applies the earlier short-circuit principle to the current operator distinction. The explanation at 24:17 in the 2026-09-08 transcript is evidence from that earlier lecture; it is not a new statement in undated NT001. The uncertain operator sounds at NT001 01:20:06 are not used to reconstruct exact tokens. [computer_programming:M002, PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) [[courses/computer_programming/transcripts/2026-09-08|T007 · 2026-09-08 · 24:17]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:20:06]]

### A cast changes the expression's view, not the actual object

The material uses the hierarchy `Animal → Mammal → Dog → Beagle`. Only one new object, a Beagle, appears in this example. [computer_programming:NM004, PDF p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
Dog dog = new Beagle();
Mammal mammal = (Mammal)dog;
Animal animal = (Animal)dog;
Beagle beagle = (Beagle)dog;
~~~

Upcasting to Mammal or Animal uses the same object through a broader contract. The downcast to Beagle is also compatible with the actual object here. A cast neither transforms the object into a new class nor changes the original variable declaration. It specifies **the type through which that reference is used in this expression**. Read the undated transcript's variable-type-change wording at 01:22:07 with this distinction. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:22:07]]

Upcasts can be implicit. The source compares `Employee e = (Employee)(new Executive());` with `Employee e = new Executive();`. Both allow code to use an Employee contract without depending on every detail of the derived implementation. Casting to the parent does not stop instance-method dispatch to the receiver's override. Declared types still matter for the field and static-method distinctions already studied, however, and casting does not bypass access restrictions. [computer_programming:NM004, PDF p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

A downcast requires the actual object to be compatible with the target type. The following source situations differ in the stage at which they fail. [computer_programming:NM004, PDF pp.49-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| Declaration and use | Problem or reason it is allowed |
|---|---|
| `Life mylife = new Life();` followed by `((Animal)mylife).move()` | The related-type cast expression is possible, but the actual object is not an Animal; it is subject to `ClassCastException` |
| `Life mylife = new Animal();` followed by `mylife.move()` | The Life contract lacks `move`, so the call is not permitted at compile time |
| `((Animal)mylife).move()` using the second reference, which holds an actual Animal | The Animal expression exposes the method, and the actual object fits the target type |

The disallowed `mylife.move()` line and the allowed cast line are alternatives for comparison. They do not describe leaving an erroneous line in a program and then normally executing the next line. “A method unavailable through the parent type” and “an actual object incompatible with the cast's subtype” are not both runtime errors. The printed material distinguishes them without reconstructing the unclear error name spoken at NT001 01:23:53. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:23:53]]

Null has a separate boundary. The reference cast `(Animal)null` remains null. Immediately using it as an instance-method receiver fails because there is no object; that is different from incorrectly casting an actual Life object to Animal and encountering `ClassCastException`. Since `mylife instanceof Animal` is false for null, it can check compatibility before a needed subtype operation. This does not require replacing every design with type branches. Use overrides for a shared contract, and check both the declared type and actual object where a subtype's extended operation is genuinely needed.

## Recall and Practice

### Concept recall

#### Recall Q01 · Override return contracts

Employee's `public double getSalary()` returns 180, and Manager's matching declaration returns 250. Give both results and the role of `@Override`. Compare separate Laidoff alternatives `double getSalary(){return 0;}` and `int getSalary(){return 0;}`. Is a return-type-free `Employee()` inside Manager a constructor override?

<details><summary>Show solution</summary>

The results are 180.0 and 250.0. Converting an integer return expression to declared double differs from changing the method declaration's return type. The double alternative can return 0 as double; the int alternative has the same name and empty parameters, so it is not a new overload and has a return incompatible with the parent's double. `@Override` expresses intent to check an actual inherited override; it cannot turn different parameters into an override. This primitive example does not establish that all reference return types must always be identical.

Constructors are neither inherited nor overridden. Manager declares Manager() and connects needed parent initialization with super(...). Employee() inside Manager is not a parent-constructor override. NM005's lowercase string differs from exact type String. Malformed source quotation marks and duplicated alternative classes do not support claiming success for the unchanged whole program.

**Checking points:** Distinguish both results, expression/declaration types, incompatible returns, annotation, and constructors.

</details>

#### Recall Q02 · Type tests and responsibility

A static helper returns 960 for Executive, 250 for Manager, and 180 otherwise; another checks the exact `getClass().getName()` string. Are the tests equivalent for a new Manager subtype? Explain branch order for related types, null, maintenance on adding classes, and an overriding alternative.

<details><summary>Show solution</summary>

`instanceof Manager` includes Manager subtypes, whereas the exact class name is that of the new concrete subtype and can differ from the Manager string. It is not a superclass-name query. For related tested types, a broad first branch can mask a specific one; do not invent an Executive/Manager relationship absent from the source.

`null` makes the instanceof tests false, so these branches alone fall through to 180, without making null a meaningful employee. The getClass alternative fails on a null receiver. No currency unit is established for 960/250/180.

The helper chooses constants through its own tests rather than invoking `e.getSalary()` overrides. More types require updating potentially duplicated helper lists, where omissions can select a wrong default. Placing the behavior in class-specific overrides lets callers use the shared contract and reduces central updates. It does not make all instanceof/getClass uses wrong or eliminate class dependencies.

**Checking points:** Justify subtype/exact-name, branch-order, null, and maintenance distinctions.

</details>

#### Recall Q03 · Field hiding preserves separate declarations

Point declares `static int x=2`, and Test extends Point with `static double x=4.7`. What do x, super.x, and ((Point)this).x read inside a Test instance method? Does the cast transform the object or erase a parent field? Also distinguish floor(-1.2) from an integer cast.

<details><summary>Show solution</summary>

The reads give 4.7,2,2: unqualified x selects Test's declaration, super.x selects the parent declaration, and viewing the expression as Point likewise selects Point.x. Both field declarations remain; the cast creates no new Point object. Field hiding is not receiver-based instance overriding.

Mathematically floor(-1.2) is -2, while plain `(int)-1.2` truncates toward zero to -1. Reading RealPoint's floor-then-int getter as a plain cast would therefore change its meaning for negative coordinates.

**Checking points:** Check all three field values and selectors, plus both negative floor/cast results.

</details>

#### Recall Q04 · All four RealPoint outputs

Point has initially zero int x,y and move(int,int); RealPoint adds separate float x,y, overrides int move by delegating to float move, and returns int floors through its getters. After `RealPoint rp=new RealPoint(); Point p=rp; rp.move(1.71828f,4.14159f); p.move(1,-1);`, trace show(p.x,p.y), show(rp.x,rp.y), show(p.getX(),p.getY()), and show(rp.getX(),rp.getY()). `show` has static int/int and float/float overloads.

<details><summary>Show solution</summary>

There is one RealPoint object and p/rp are aliases. The first float arguments select RealPoint's float overload and update child fields. The second call selects the int signature visible through Point, but dispatches to the actual RealPoint override. That body delegates to float move, again changing only child fields; Point.move's body never runs along this path.

Parent int fields remain 0,0; the material displays the child float values as 2.7182798,3.14159. The four calls are:

1. p's int fields→show(int,int)→`(0, 0)`.
2. rp's float fields→show(float,float)→`(2.7182798, 3.14159)`.
3. RealPoint getters dispatch, floor to int 2,3→show(int,int)→`(2, 3)`.
4. The same getter overrides and return types→`(2, 3)`.

Thus p.x can be 0 while p.getX() is 2. `show` selection uses the getters' declared int return type, not a value that happens to be integral. The decimal display is the source's float representation, not a guarantee of ideal decimal formatting or a new execution measurement.

**Checking points:** Trace each move's signature, body, and changed fields; supply all four outputs and show types.

</details>

#### Recall Q05 · Instance dispatch after overload selection

Polynomial offers times(int), times(float), times(Polynomial), and times(Polynomial,int). Select signatures for times(9), times(85.2f), and times(new Polynomial(...),3). Explain both selection stages for Employee e=new Manager(); e.getSalary(), and the diagram's method-to-code connection. Can the figure establish polynomial results, deleted overload bodies, or universally slower dispatch?

<details><summary>Show solution</summary>

Argument types/counts select times(int), times(float), and times(Polynomial,int), respectively. The two-argument call is not the one-Polynomial overload. The term static/syntactic polymorphism names this compile-time selection and does not require the static method modifier.

First check that Employee's declared contract permits getSalary(); then select that instance signature's override for the actual Manager receiver. Runtime does not restart overload selection across other signatures. The schematic starts at the current class, follows superclasses toward Object if needed, and refers from selected method data to a code location before executing code.

No Polynomial bodies or string-constructor interpretation are supplied, so actual polynomial results cannot be determined. The diagram proves no universal JVM layout, repeated linear search, deletion of every overloaded body, or universal cost comparison.

**Checking points:** Give all signatures, both stages, and the code connection without inventing results, implementation, or cost.

</details>

#### Recall Q06 · Operator values and evaluation

(a) Compare 10+20, 1.5+2.0, `"10"+"20"`, and `"sum = "+30`. (b) Find s after `String s="Dog"+" barks."; s+="Too Loud!";` and assess String mutation. (c) Identify the type problem in `float f=0.5 % 0.3;`. (d) Explain 6&3,6|3,true&false,true|false, eager versus &&/|| evaluation, and a denominator=0 guard.

<details><summary>Show solution</summary>

Numeric addition gives 30 and 3.5; String concatenation gives `"1020"` and `"sum = 30"`. These are language-defined operand-dependent meanings, not a facility for user-defined Java operator overloads.

Initially s is `"Dog barks."`, then `"Dog barks.Too Loud!"` after +=. No extra space is inserted. Concatenation assigns a result back to the variable rather than mutating an immutable String. Unsuffixed 0.5 and 0.3 are double literals, so % is double and cannot be assigned directly to float. A separately identified teaching repair, `double f=0.5 % 0.3;`, aligns the type without guaranteeing exactly decimal 0.2 under binary representation.

Bitwise AND of 110 and 011 gives 010=2; OR gives 111=7. `boolean` true&false is false and true|false is true. `boolean` &/| evaluate both operands; && can skip the right when the left is false, and || when it is true. With integer denominator=0,numerator=100, `denominator != 0 && numerator / denominator > 2` skips division after the false left side. Replacing && by & evaluates integer division by zero. The historical guard evidence is T007 on 2026-09-08 at 24:17, separate from new undated NT001 speech.

**Checking points:** Check four plus results, both s values, double-to-float, all AND/OR values, skipping conditions, and the guard.

</details>

#### Recall Q07 · Cast views and failure stages

For Animal→Mammal→Dog→Beagle, what remains unchanged when `Dog dog=new Beagle()` is cast to Mammal, Animal, or Beagle? Life lacks move and Animal extends Life adds it. Distinguish alternatives: (a) calling move through Life holding an Animal, (b) casting that reference to Animal then calling, (c) casting an actual Life to Animal, and (d) casting null and invoking an instance method. Include instanceof, access, and overrides.

<details><summary>Show solution</summary>

The actual object remains one Beagle. Mammal/Animal casts are broader upcast views and may also be implicit; the Beagle downcast fits the actual object. A cast sets the expression's usable type, not the original variable declaration or object's class.

(a) fails compile-time call availability because Life lacks move. (b) exposes move through an Animal expression and fits the actual Animal. (c) is a possible related-type cast expression but the actual Life is not Animal, causing `ClassCastException`. Judge the alternatives separately rather than assuming normal progress beyond an erroneous line. (d) permits `(Animal)null` and leaves it null, but an ensuing instance call lacks a receiver and raises `NullPointerException`.

`x instanceof Animal` is false for null and can check actual compatibility where a subtype extension is needed. Casting cannot bypass access restrictions, and an upcast does not stop receiver-based instance overrides. Use the common override contract when available, and appropriate type checks where an actual extension is needed.

**Checking points:** Separate the same object, expression type, and failures of call availability, incompatible cast, and null invocation.

</details>

### Practice

#### Practice P01 · Different state paths in one object

Newly written synthetic practice. Connect only field/static/instance separation from [EX:cp_2026_1_final_q02 p.2] and overload→override order from [EX:cp_2026_1_final_q09 p.6]. Prerequisites are binding, method signatures, field hiding, and aliases. Classes share a package; call statements are inside an appropriate method.

~~~text
class Device {
    int state = 3;
    static String kind() { return "device"; }
    void step(int n) { state += n; }
    void step(float n) { state += 10; }
    String report() { return "" + state; }
}
class Sensor extends Device {
    int state = 20;
    static String kind() { return "sensor"; }
    @Override void step(int n) { state += 2 * n; }
    @Override String report() { return state + "/" + super.state; }
}
Sensor s = new Sensor();
Device d = s;
d.step(1);
d.step(1.0f);
~~~

Find `d.state`, `s.state`, `d.report()`, `((Device)s).report()`, `d.kind()`, and `s.kind()`, with reasons. First state which step body changes which field.

<details><summary>Show solution</summary>

s and d alias one Sensor. `d.step(1)` selects Device's visible int signature and dispatches to Sensor's override, changing Sensor.state to 20+2×1=22. `d.step(1.0f)` selects the float signature. Sensor does not override it, so Device's body runs; state inside that body denotes Device's field, changing 3+10=13.

Thus d.state=13 and s.state=22. Both report calls dispatch to Sensor's override and return `"22/13"`; the Device cast does not change the receiver. `static` kind follows expression type: d.kind()=`"device"`, s.kind()=`"sensor"`. One object does not make every field selection or static body identical.

**Checking points:** Check each step's signature/body/field, all six results, and retained dispatch after the cast.

</details>

#### Practice P02 · A boundary needing a subtype operation

Newly written lecture-based general practice. The index has no directly matching item for this null/extension classification. Life has only breed; Animal extends Life and adds move. Evaluate the alternatives independently.

If a Life reference x holds (a) new Animal(), (b) new Life(), or (c) null, classify x.move() and ((Animal)x).move(). In which case does `if (x instanceof Animal) { ((Animal)x).move(); }` enter its body? Is such a guard needed around every shared method?

<details><summary>Show solution</summary>

In all three cases x has declared type Life, so x.move() fails call-availability checking, including case a with an actual Animal. After the cast, case a fits the actual object and accesses move; b raises ClassCastException because actual Life is not Animal; c preserves null through the cast and then raises NullPointerException at the call.

The instanceof guard is true only in a. It is false in b and c, so neither enters the cast/call body. Compatibility checks are useful where Animal's actual extension is needed. Operations already declared by a shared contract can use that contract and receiver overrides, so there is no reason to replace every shared-method invocation with type branches.

**Checking points:** Check the shared direct-call failure, three post-cast outcomes, all guard results, and its design scope.

</details>

## Sources

### Lecture notes and transcripts

- [[courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2|Date unconfirmed · Object contracts, polymorphism, and generic introduction]]
- [[courses/computer_programming/lectures/en/2026-09-01-lecture-01|2026-09-01 · literal types and conversion foundations]]
- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · operators and short-circuiting]]
- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · object, constructor, static, and reference prerequisites]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · object, initialization, and reference recap]]

Dated notes link the stated prerequisites; they do not establish that detailed inheritance/dispatch was completed on those dates.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · undated transcript]] — 54:47, 55:45, 56:45, 57:38, 59:24, 01:00:18, 01:01:17, 01:03:10, 01:06:05, 01:07:58, 01:09:54, 01:11:50, 01:15:28, 01:18:07, 01:19:07, 01:20:06, 01:22:07, 01:23:53, 01:24:50.
- [[courses/computer_programming/transcripts/2026-09-08|T007 · 2026-09-08 전사 / transcript]] — 24:17.

### Materials and physical PDF pages

Page numbers count physical PDF pages; each page link includes the original page.

- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-032), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-037), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-050).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-006), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042), [p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-069).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007).

### Scope and uncertainties

NT001 is undated. Its 95 utterances retain 124 literal uncertainty markers and 76 additional limits; unclear speech, negation, and missing words are not reconstructed from printed material. Printed examples are material evidence, not evidence that every example was newly spoken. Times below locate transcript passages and are not timestamp anchors.

NM005 has 36 physical PDF pages. Its registered Lab 6 title conflicts with the printed Lab 1 cover; TODOs and the unavailable ZIP referenced on p.19 remain unresolved. It is used for concepts, without supplying a completed graded implementation or transferring attendance/submission rules.

Malformed closing quotation marks, duplicate Laidoff alternatives and p.31 punctuation in NM004, plus lowercase string in NM005, are not treated as complete valid code. The primitive int/double return example does not establish identical types for all reference returns. No currency unit for 960/250/180, unstated Executive/Manager relationship, or claim that getClass returns a superclass name is adopted. The four RealPoint results supplement the speech from material; printed float is not replaced by uncertain spoken double. Diagrams explain the method-data/code connection, not a universal JVM layout, binary deletion, mandatory linear search, or universal cost. Polynomial bodies and the string constructor's meaning are absent.

The short-circuit example is on M002 physical p.69. Its T007 explanation at 24:17 on 2026-09-08 is separate from undated NT001. NM004 p.44's float f=0.5 % 0.3 cannot be assigned as printed because of its double literals. Unclear operator sounds, error names, and downcast-frequency remarks are neither reconstructed nor generalized into statistics.

### Qualified connections to unofficial recalls

These are unofficial recalled documents with no verified official keys supplied. The filenames alone associate the 2025-spring midterm with Kim Sanghan (김상한) and the 2026-spring final with Yoo Youngjae (유영재), different from current instructor Jaemin Yoo (유재민). Connections concern only the concepts or reasoning below and establish no current style, scope, frequency, or probability. New questions are general or synthetic practice.

- [EX:cp_2026_1_final_q02 p.2] — Connect declared-type field/static selection versus instance overrides to P01. Prerequisites are binding, method signatures, and field hiding. [[exam_questions/cp_2026_1_final_q02|Existing question preview]]
- [EX:cp_2026_1_final_q09 p.6] — Connect overload-signature selection followed by receiver override dispatch to P01. Overloading/overriding are prerequisites; the primary RealPoint calculation is not replaced by the recalled numbers. [[exam_questions/cp_2026_1_final_q09|Existing question preview]]

No indexed item directly matches the HR maintenance example, RealPoint’s four outputs, Polynomial schematic, exact operator examples, or the complete Life-cast classification. P02 is general practice. Unrelated collections, exception, and C++ questions are excluded.
