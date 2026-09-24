---
title: "Objects, Constructors, Static Members, and Reference Passing"
description: "Review OOP responsibilities, initialization, static sharing, reference passing, and GC through state traces."
course: "computer_programming"
unit_id: "objects-references"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 1 Introduction.pdf", "Lecture 2 Java Basics 1.pdf", "4 oop.pdf", "Lab03 v2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-01-lecture-01", "courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

Mark whether each assignment changes a variable's reference or a shared object's field. Connect classes, constructors, static members, and calls to that model to explain what callers observe.

## Objects organize state and behavior

A [[courses/computer_programming/units/en/methods|method]] groups work. Object-oriented programming, or OOP, goes further by viewing software as **interacting objects with state and behavior**. An object may represent a physical car, a conceptual bank account, or a software entity such as a linked list. This does not require implementing linked lists now. The person/house/car model on M011 p.3 connects the person to the house through `lives in` and to the car through `drives`. A model includes relationships between objects, not only an inventory of entities.

The coffee example on [Computer Programming M011, PDF pp.3–6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) contrasts two organizations. The procedural account lists preparing beans, grinding, preparing water, boiling, adding beans, and mixing. The object-oriented account groups grind, boil, and mix capabilities inside a Coffee Machine and lets a user supply ingredients and request operations. A capability list is not itself the user's recipe: the object offers functions, while the caller chooses their sequence.

The explanation at [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 03:38]] concerns making large programs easier to understand, extend, and maintain, rather than enabling computations impossible procedurally. Java and C++ are introduced as vehicles for these principles; C++ implementation is not added here.

### Classes, instances, and reference variables

A class is an object's blueprint. An instance is an object created from that class; instantiate names the act of creating it. Attributes describe appearance or state, while methods define behavior. Together they are members.

```java
class Car {
    int width = 10;
    String color = "red";
}
```

Executing `Car car = new Car();` inside a method distinguishes a reference variable `car` of type `Car` from the new Car object. `new Car()` creates the object; `car` stores a value referring to it. Reading `car.width` gives 10, then `car.width = 5;` makes it 5. Attributes can describe state such as fuel, speed, and color without corresponding to physical components.

`Car car = new Car(), newCar = new Car();` creates two objects. After `newCar.color = "blue";`, `car.color` remains red. Sharing a class definition does not mean sharing instance fields. See [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 13:45]] and M011 pp.7–14. The recalled 2025-1 definition item provides an optional connection: distinguish the class definition, actual instances, and variables referring to them when explaining their relationship. It is recalled material without an official answer key. [EX:cp_2025_1_midterm_q01 p.1]

Fields not explicitly initialized receive defaults: false for `boolean`, 0 for `int`, 0.0 for `float`, and null for a String reference. The default char is `'\u0000'`; the slide's apparently empty notation is not a valid empty char literal. Field defaults differ from the requirement to assign a local variable before reading it.

## An instance method reads its receiver's state

M011 p.15 makes the type-name/variable-name distinction concrete:

```java
class Car {
    void printHello() {
        System.out.println("Hello World!");
    }
}
```

In this separate example, create an object with `Car car = new Car();` and call `car.printHello();`. The expression before the dot, `car`, selects the receiver; the method name and parentheses select its action. Because `printHello` is a non-static instance method, the type name `Car` cannot replace that receiver. The method prints `Hello World!` despite returning void.

On M011 p.16, `getSpeed()` contains `return speed;`. If `myCar.speed = 100` and `yourCar.speed = 90`, their calls return 100 and 90. One method definition reads different state depending on its receiver.

The materials-based example on [Lab03 M014, PDF pp.6–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf), acquired September 19, instead sets `speed = 10` and returns `10 * speed`. Reading the field gives 10; calling the method gives 100. The name `getSpeed` does not guarantee a plain field return, and these two source bodies must not be merged.

## Constructors and this establish initial state

A constructor is a special initialization construct used during object creation. It has the class's name and no return type, including no `void`. The `Car()` example on M011 p.20 prints `A car is created.` during creation. Parameters allow different initialization paths:

```java
public class Car {
    int weight;
    String color = "unknown";

    Car(int w) { weight = w; }
    Car(int w, String c) {
        weight = w;
        color = c;
    }

    void printInfo() {
        System.out.println(weight + " kg, " + color);
    }
}
```

On M011 p.22, `new Car(1500, "red").printInfo();` prints `1500 kg, red`; `new Car(2000).printInfo();` prints `2000 kg, unknown`. The second creation path leaves the color initializer intact. This class declares those two parameter lists, not a no-argument constructor. Centralizing initialization reduces missed field assignments after creation.

The supplemental Lab03 p.8 example initializes carNumber and model to 1234 and Sonata and prints `Car initialized.`. However, its declaration uses `myCar` while the later expression says `mayCar.model`. The intended `1234 Sonata` output and the validity of the literally printed code are different claims.

### this under shadowing

`this` refers to the current object. When a parameter shadows a field with the same name, it makes the distinction explicit:

```java
class Car {
    int speed = 30;

    void cantChangeSpeed(int speed) {
        speed = speed;
    }

    void changeSpeed(int speed) {
        this.speed = speed;
    }
}
```

The first method on M011 p.26 assigns the parameter to itself. The second assigns the parameter value to the receiver's field. But omitting this does not always mean referring to a local. On p.24, `changeColor()` has no local color; `this.color = "red";` followed by `color = "blue";` changes the same field twice. The outputs are red and blue, and the final field is blue. The explanation at [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 24:11]] that the second assignment changes only a local conflicts with the printed code and is explicitly corrected here.

This class-body fragment from M011 p.25 shows another use:

```java
int speed = 100;
String speedAndUnit() {
    return speed + " km/h";
}
void printSpeedAndUnit() {
    System.out.println(this.speedAndUnit());
}
```

Calling `car.printSpeedAndUnit()` prints `100 km/h`. Here omitting this from `this.speedAndUnit()` retains the same receiver. The capitalization in `printSpeedAndUnit` is part of the identifier.

Lab03 p.9 adds a **materials-based constructor-chaining example**. The `Car()` body uses `this(55, "blue")` to invoke the two-parameter constructor. Although field initializers start at 100/red, this creation path ends at 55/blue. `this.printSpeed()` is a method call; `this(...)` connects constructors. A constructor is not an ordinary method to call again arbitrarily, and chaining also prevents a blanket claim that exactly one constructor body executes per creation. Detailed chaining was deferred on September 15.

## Shared static state and the receiver restriction

A static member belongs with the class rather than an individual object. `Car.num` and `Car.printNum()` can be used without first creating an instance. The per-car versus total-state contrast on M011 pp.27–30 becomes:

```java
class Car {
    static int num;
    static int totalMile;
    int mile;

    Car() { num++; }

    void setMile(int mile) {
        this.mile = mile;
        totalMile += mile;
    }
}
```

The two class-owned integer fields start at zero. Constructing three objects and calling `setMile(20)`, `setMile(30)`, and `setMile(40)` once on the respective objects gives `num = 3` and `totalMile = 90`. Each mile field is separate, while totalMile is shared. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 33:33]]

Names alone do not guarantee intended meanings. Another setter call adds the new input again, so totalMile may cease to equal the sum of current instance mile fields. Num counts constructions; it does not automatically track surviving objects.

Lab03 p.10's static owner example assigns one shared String field through two constructors, changes it through one instance, reads it through the other, then changes it through the class name. Replacing the personal-name literals with ordinal labels for explanation, the field holds the second value after the two constructions; the first observed output is the third value and the final output is the fourth. All accesses concern the same field.

### A static context has no implicit instance

```java
class Car {
    float fuel;
    static float totalFuel() {
        return fuel; // invalid unqualified instance access
    }
}
```

This **invalid example** on M011 p.32 and M014 p.11 does not identify which Car's fuel to read. A static method has no implicit `this` object. Adding one `new Car()` elsewhere cannot repair the method definition. The message `non-static variable fuel cannot be referenced from a static context` is a compilation diagnostic, not runtime output.

The restriction concerns direct access without a receiver. Static code can use an explicit object reference to access an instance member; an instance method can also use a static member. The reversed static/non-static wording around [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 36:24]] is not adopted as a rule.

## Reference assignment and object identity

Reference assignment does not copy an object:

```java
String str1 = new String("hey");
String str2 = new String("hey");
String str3 = str1;
```

On M011 p.35, `str1 == str2` is false and `str1 == str3` is true. The first two refer to distinct objects; the last assignment copies str1's reference value. Equal contents and identical objects are different relationships.

```java
Car myCar = new Car();
Car car1 = myCar;
Car car2 = myCar;
Car car3 = car1;
```

There is only one new expression here, so four variables refer to one object. A field change through one reference is visible through the others. By contrast, the first two `new Car()` expressions on Lab03 p.12 create distinct objects and compare false; after `car2 = car1` the comparison is true. The phrase “We don't get false” at [[courses/computer_programming/transcripts/2026-09-17|2026-09-17, 08:32]] conflicts with the printed false/true results and is not turned into a reliable identity rule.

## Arguments are copied by value, including references

Java argument passing **always copies values**: primitive values for primitive arguments and reference values for reference arguments. Caller variables and callee parameters are separate storage locations.

### Swapping primitive parameters changes local copies

Inside `swap(int a, int b)` on M011 pp.37–39:

```java
int temp = a;
a = b;
b = temp;
```

Starting with copied values 2 and 3, the callee ends with local a=3, b=2, temp=2. The caller retains 2,3. Identical names do not make parameters aliases for caller variable storage. Lab03 p.13 similarly sets the parameter of `changeNumber(int number)` to 100, but the caller's number remains 10 and prints 10.

The later source example on M011 pp.49–50 instead prints `a = temp` as its final line. Tracing those bytes restores local a to 2 while b remains 3, conflicting with p.50's local 3/2 diagram. Do not silently repair the printed line when attributing it to the source. Both versions leave caller x=2, y=3 unchanged.

### Copied references can mutate shared fields

Suppose `IntHolder` has an integer value field initialized by its constructor. When the caller supplies holders containing 2 and 3, callee a and b receive copied references to those same objects. The targets on M011 p.41 are the fields:

```java
int temp = a.value;
a.value = b.value;
b.value = temp;
```

Now the caller also reads 3,2 from the shared objects. In the supplemental M014 p.14 example, car1 refers to a Car with speed=50 and is passed to `changeSpeed(car1)`. The copied argument is **car1's reference value**, not the integer 50 or an entire Car copy. The callee's `car.speed = 100` changes the shared object, so `car1.speed` later reads 100. Assigning a different reference to local car, however, does not reassign caller car1.

The lecture and slides also call this effect call-by-reference. The precise Java rule is call-by-value for reference values too, a qualification present on M011 p.42. Accessing one shared object without copying its entire contents differs from changing the caller's reference variable itself.

### A String swap differs from a Wrapper-field swap

On M011 pp.52–53, `temp = a; a = b; b = temp;` changes only **callee reference variables**. Caller s1=`"Hi"` and s2=`"all"` remain unchanged. Read the diagram's caller connections separately from the values stored in callee a and b: crossed reference paths do not establish that caller variables were exchanged.

The course's `Wrapper` is a separate class containing a String field s. There are now two stages: caller → Wrapper object → String. This method-body fragment on pp.55–56 changes shared Wrapper fields:

```java
String temp = a.s;
a.s = b.s;
b.s = temp;
```

The caller consequently reads all and Hi through `s1.s` and `s2.s`. Neither the Strings' characters nor the caller's Wrapper reference variables were modified. In the diagram, look for the extra reference stage from the Wrapper field to its String.

The source's p.51 ends with `a = temp` and does not even complete a local swap; p.54 similarly ends with `a.s = temp` rather than the intended field exchange. The explanation uses the actual sequences on pp.52–53 and pp.55–56 without converting the source's whole Wrapper structure into a finished executable program. The claim around [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 54:55–55:51]] that the plain String swap eventually works is not adopted as caller-swap success. These detailed examples are not established as having all been repeated on September 17.

## Object lifetime and garbage collection

A primitive variable's stored value may directly be 2; a reference variable stores a reference that must be followed to the object. The symbol-table model on M011 pp.46–48 connects names with storage locations. It does not guarantee a particular JVM's table placement or literal physical addresses.

New object creation allocates the required memory; the garbage collector reclaims memory used by objects no longer in use. The September 15 example creates `new IntHolder(4)` inside swap and leaves no reference elsewhere after returning. This illustrates becoming eligible for collection, not a guarantee of immediate collection at method return. Automatic memory management is also discussed at [[courses/computer_programming/transcripts/2026-09-17|2026-09-17, 12:50]].

The recalled 2025-1 GC item offers an optional connection: distinguish creation, reachability, eligibility, and actual collection time. The recollection neither guarantees immediate collection nor supplies an official answer key. [EX:cp_2025_1_midterm_q03 p.2]

The contrast with explicit allocation/free in C concerns responsibility for memory management. Automatic management does not eliminate creation expressions such as new, nor establish a universal performance multiplier between languages. Health reaching zero, simulation termination, and GC eligibility concern application state, control flow, and object lifetime respectively. Who may change such state is the next concern in [[courses/computer_programming/units/en/encapsulation|Encapsulation and access control]].

## Key Takeaways

- A class is a definition, an instance a created object, and a reference variable storage for a referring value.
- Instance methods need receivers; whether this may be omitted depends on shadowing.
- Static fields are shared, but update code determines what counters and totals mean.
- Java copies reference values too. Parameter reassignment differs from shared-field mutation.
- Eligibility for GC does not determine collection timing.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Capabilities versus a procedure

Are a Coffee Machine's grind/boil/mix capabilities the same as a user's coffee procedure? Must OOP objects/interactions represent only physical things?

<details><summary>Show solution</summary>

Capabilities are offered operations; a procedure is the caller's sequence of preparation and requests. OOP assigns responsibilities to interacting objects with state/behavior. Cars, conceptual bank accounts, and software entities such as linked lists can all be modeled. Relationships such as lives in and drives matter too. This organization aids understanding/extensibility/maintenance rather than enabling otherwise impossible computation; linked-list implementation is not a prerequisite here.

**Checking points:** Distinguish capabilities/order, state/behavior, and entities/relationships.

</details>

#### Recall Q02 · Class, instance, defaults

Car has width=10,color="red". After two separate new expressions followed by car.width=5 and newCar.color="blue", give object count and both states. Explain uninitialized fields versus locals.

<details><summary>Show solution</summary>

There are two objects. Car is the class/type; car/newCar are reference variables for separate instances. Their states are 5/red and 10/blue. Attributes and methods are members; sharing a definition does not share instance fields. Uninitialized fields receive false, zero, 0.0, null, and char `'\u0000'` for the stated types, while locals require assignment before reading. An empty char literal is not that default.

**Checking points:** Include two objects, both states, references, and field defaults.

</details>

#### Recall Q03 · Receiver and method body

In `Car car=new Car(); car.printHello();`, distinguish `Car` and `car`. Non-static `void printHello` prints `Hello World!`. Find the results of a `return speed` method for receivers with `speed` values 100 and 90; contrast Lab03’s `speed = 10` and `return 10*speed`.

<details><summary>Show solution</summary>

Car is the type; car supplies the receiver reference. `Car.printHello()` cannot replace the instance call; void still permits Hello World! output. A return-speed body yields 100/90 for receivers with those fields. The separate Lab03 body reads field ten and returns one hundred, so field output ten differs from method result one hundred. A getter-like name does not replace reading the body.

**Checking points:** Preserve identifier case, receiver distinction, and the different source bodies.

</details>

#### Recall Q04 · Constructor initialization

`color` defaults to unknown; Car(int w) sets weight, while Car(int w,String c) sets both fields. Explain results of new Car(1500,"red") and new Car(2000), no-arg availability, and the Lab03 myCar/mayCar discrepancy.

<details><summary>Show solution</summary>

States are 1500/red and 2000/unknown; printInfo prints `1500 kg, red` and `2000 kg, unknown`. The second path preserves the initializer. These two parameterized constructors do not provide a no-arg constructor. A constructor has the class name and no return type, including void, and centralizes initialization during creation. Lab03 declares myCar but later uses mayCar.model; intended 1234 Sonata output is distinct from literal code validity.

**Checking points:** Explain both paths, preserved initializer, no return type, and source typo.

</details>

#### Recall Q05 · With and without shadowing

Independently start field speed=30 with parameter speed=80 and execute speed=speed or this.speed=speed. Then trace this.color="red"; color="blue"; in a method with no local color.

<details><summary>Show solution</summary>

The first self-assigns the parameter and leaves field thirty; the second assigns receiver field eighty. With no shadowing local color, both color forms refer to the same field, producing red then blue and ending blue. Missing this does not automatically mean local. The color result corrects conflicting speech by reading the printed code, rather than rewriting that speech as correct.

**Checking points:** Identify the parameter or field targeted by each assignment.

</details>

#### Recall Q06 · this in methods and constructors

At speed100, speedAndUnit returns speed+" km/h" and printSpeedAndUnit prints this.speedAndUnit(). Give call/output. Separately, Lab03 Car() chains to this(55,"blue") that sets both fields after initial 100/red.

<details><summary>Show solution</summary>

`car.printSpeedAndUnit()` prints `100 km/h`; omitting this here keeps the same receiver. The Lab03 chain finishes at 55/blue. A method call such as this.printSpeed() differs from constructor chaining this(...). This neither makes constructors arbitrarily callable ordinary methods nor guarantees one constructor body per creation. Detailed chaining is a later-acquired materials supplement, not recovered deferred speech.

**Checking points:** Preserve printSpeedAndUnit spelling/output and distinguish both this uses.

</details>

#### Recall Q07 · Shared counters and actual totals

Static num,totalMile start zero; constructors increment num and setMile(v) assigns this.mile=v then adds v to totalMile. Set three objects to20,30,40, then set the first to20 again. Also explain successive first/second/third/fourth assignments to static owner.

<details><summary>Show solution</summary>

Initially num=3,totalMile=90 and miles20,30,40. Repeating the first setter leaves num3 and those miles but totalMile110, while current miles sum90. `num` counts constructions, not surviving objects; totalMile accumulates inputs. Static owner is one shared field: after two constructions it holds the second value, another instance observes the third assignment, and class-name assignment stores the fourth. Personal-name literals are unnecessary.

**Checking points:** Explain 3/90→3/110, current sum90, and shared owner state.

</details>

#### Recall Q08 · A receiver in static context

Why is `float fuel; static float totalFuel(){return fuel;}` invalid? Would creating a Car elsewhere repair it? Explain permitted static/instance access.

<details><summary>Show solution</summary>

`fuel` exists, but the static method has no implicit receiver identifying which Car owns it. This is a compilation diagnostic, not normal runtime output. Creating an object elsewhere does not supply a receiver to the definition. Static code can access instance members through an explicit object reference, and instance methods may use static members.

**Checking points:** Identify missing receiver selection, not merely object existence.

</details>

#### Recall Q09 · Reference count versus object count

Give == results for separate new String("hey") values str1/str2 and str3=str1. Count objects in one new Car assigned through myCar/car1/car2/car3 and explain a field change through an alias.

<details><summary>Show solution</summary>

str1==str2 is false and str1==str3 true. Assignment copies a reference value, not an object. One new Car means one object reached by four variables; all observe changes to its field. Two separately created Cars compare false, then true after car2=car1. The September17 'don't get false' wording conflicts with this and is not adopted as an identity rule.

**Checking points:** Separate creations, aliases, identity, and content equality.

</details>

#### Recall Q10 · Separate storage in primitive swap

Copy caller x2,y3 into a,b, then run temp=a; a=b; b=temp;. Give caller and local states. If the last line is a=temp as printed elsewhere, does it match a3/b2? What if changeNumber assigns its copied10 parameter to100?

<details><summary>Show solution</summary>

The correct local swap ends temp2,a3,b2, while caller x2,y3 remains. With final a=temp, locals instead end a2,b3, conflicting with the diagram. Neither version assigns caller storage. changeNumber similarly sets only its parameter100; caller10 remains and prints10. Matching names do not alias caller variables.

**Checking points:** Give correct/erroneous local traces and unchanged caller state.

</details>

#### Recall Q11 · Copied references and field mutation

Pass car1 with speed50 into changeSpeed(Car car), which sets car.speed=100. What is copied and observed? Compare reassigning local car and swapping fields of IntHolders with values2/3.

<details><summary>Show solution</summary>

The copied value is the reference, not integer50 or the whole Car. Both variables reach the same object, so car1.speed becomes100. Reassigning local car does not reassign caller car1. For holders, temp=a.value; a.value=b.value; b.value=temp changes shared fields to3/2, visible to callers. Java passes reference values by value; source 'call-by-reference' wording must not imply caller-variable replacement.

**Checking points:** Distinguish the copied value, shared mutation, and parameter rebinding.

</details>

#### Recall Q12 · Targets in a String swap

Pass caller s1="Hi",s2="all" to a,b and execute temp=a; a=b; b=temp;. Describe callee/caller references and String contents.

<details><summary>Show solution</summary>

Callee a reaches all and b Hi, while caller s1 stays Hi and s2 all. Only copied parameter references were rebound; neither caller slots nor String characters were changed. Crossed local arrows do not prove caller-swap success. The source p51 final a=temp does not even complete a local swap.

**Checking points:** Track all caller/callee references and unchanged characters.

</details>

#### Recall Q13 · An extra Wrapper field slot

Two Wrapper objects have String field s set to Hi/all. Trace temp=a.s; a.s=b.s; b.s=temp and what callers observe. What if the final line is a.s=temp as on p54?

<details><summary>Show solution</summary>

The correct swap changes shared Wrapper.s fields to all/Hi, visible to callers. It changes the second link in caller→Wrapper→String, not caller Wrapper references or String characters. Final a.s=temp instead restores the first field to Hi and leaves the second all. Distinguish the correct pp55–56 sequence from p54's printed line; do not treat the whole original structure as a finished executable program.

**Checking points:** Explain two reference stages, both traces, and untouched locations.

</details>

#### Recall Q14 · Eligibility versus collection time

A new IntHolder(4) created in a method is referenced nowhere after return. Has GC necessarily run? Distinguish primitive/reference storage, health zero, and simulation termination.

<details><summary>Show solution</summary>

It may become eligible, but immediate collection is not guaranteed. Primitive storage holds a value; reference storage holds a reference leading to an object. Symbol-table drawings are logical models, not physical-address guarantees. Automatic management reclaims unused objects without removing creation through new. Health zero is application state and simulation termination control flow; neither establishes reachability. Contrasting C's explicit free proves no universal performance multiplier.

**Checking points:** Separate reachability, eligibility, actual collection, and application state.

</details>

### Apply the ideas

#### Practice P01 · Creation and remaining references

**Newly written synthetic exam-style practice.** Transfer class/instance reasoning from [EX:cp_2025_1_midterm_q01 p.1] and GC conditions from [EX:cp_2025_1_midterm_q03 p.2] into creation/alias/rebinding traces. Prerequisites are taught new/references/GC; the recollections have no official key.
```java
Car a = new Car();
Car b = a;
a = new Car();
b = null;
```
Assume no other references. Count creations after each line and identify final reachability. Can the number actually collected immediately afterward be fixed?

<details><summary>Show solution</summary>

Cumulative creations are1,1,2,2. After line two, a/b share the first object. Line three rebinds only a, so b still reaches the first. Line four removes that path, making the first eligible; a reaches the second. Two creations differ from one currently reachable object. The code does not determine whether collection has already occurred or how many objects were collected immediately.

**Checking points:** Give counts, distinguish lines three/four, and qualify actual GC timing.

</details>

#### Practice P02 · Rebinding after a field change

**Newly written lecture-based general practice; no direct indexed style match for this combination.** Car's instance speed starts zero. A static helper executes `car.speed=40; car=new Car(); car.speed=90;`. The caller passes a with speed10. What does the caller read, and why may static code access these fields?

<details><summary>Show solution</summary>

Caller a reads40. The first write changes the original shared object. After new, local car points to another object;90 is stored there without rebinding a. The static helper uses an explicit car receiver, unlike unqualified fuel access. This trace does not determine collection timing for either object.

**Checking points:** Assign40/90 to the right objects and explain explicit receivers.

</details>

### Review plan

Explain definitions/creation with Q01–Q04, then trace receivers/shared state in Q05–Q08. Draw caller/parameter/object locations for Q09–Q13 before checking reachability in Q14 and P01–P02.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-01-lecture-01|2026-09-01 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 corrected transcript]] — 01:15:24.
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 corrected transcript]] — 03:38, 13:45, 33:33, 36:24, 54:55–55:51 (plain `String` swap success claim; caller references remain unchanged), 57:33 (shared `Wrapper.s` field mutation).
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 corrected transcript]] — 08:32, 12:50.

### Materials and page views

- [Lecture 1 Introduction.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/1.intro.pdf) — [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-012).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048).
- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-003), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-007), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-016), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-020), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-022), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-026), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-030), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-032), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-036), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-039), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-042), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-044), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-053), [p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-054), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-056).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-015).

Distinguish September 15 teaching from September 17 recap. Lab03 was acquired September 19 and does not recover speech after the 17:39 cutoff. Retain the color/static/identity speech conflicts and swap code/diagram discrepancies. The myCar/mayCar constructor typo and erroneous final swap assignments are not silently repaired as source quotations.

Connections: class/object relationships [EX:cp_2025_1_midterm_q01 p.1] and GC conditions [EX:cp_2025_1_midterm_q03 p.2]. Existing [[exam_questions/cp_2025_1_midterm_q01|class/object question preview]] and [[exam_questions/cp_2025_1_midterm_q03|GC question preview]] are available. Both are recollections without official keys; neither guarantees collection timing or exam likelihood.


---

[[courses/computer_programming/units/en/methods|← Previous: Method Contracts, Calls, Returns, and Reuse]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/encapsulation|Next: Encapsulation, Access Control, and State Design →]]
