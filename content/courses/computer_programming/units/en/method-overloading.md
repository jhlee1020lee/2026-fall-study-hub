---
title: "Method Signatures and Overloading Design"
description: "Trace signatures, overload selection, and constructor delegation, then distinguish the reuse motivation for generics."
course: "computer_programming"
unit_id: "method-overloading"
lang: "en"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["8 polymorphism.pdf", "Lab 6 Polymorphism.pdf", "6 inheritance 1.pdf", "Lecture 2 Java Basics 1.pdf", "7 inheritance 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/en/2026-09-01-lecture-01", "courses/computer_programming/lectures/en/2026-09-10-lecture-04", "courses/computer_programming/lectures/en/2026-09-15-lecture-05", "courses/computer_programming/lectures/en/2026-09-17-lecture-06"]
---

## Method signatures and overload selection

### Giving related operations a shared name

If printing requires separate names such as `printInt`, `printFloat`, and `printString`, callers must remember several names for the same general purpose. Polymorphism provides a common name or contract for different forms of behavior. Overloading is one way to do this: methods share a name but have different parameter lists. Similar meaning alone does not establish a Java method relationship. For example, `Animal.move()` and `Fish.swim()` may both describe movement, but their different names mean that one does not override the other. [computer_programming:NM004, PDF pp.4-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

For the non-generic methods in this section, compare signatures using the **method name and the ordered list of parameter types**. Parameter variable names and the return type do not distinguish these signatures.

| Declaration form | Distinguishing signature |
|---|---|
| `int add(int a, int b)` | `add(int, int)` |
| `int add(int x, int y, int z)` | `add(int, int, int)` |
| `float add(float a, float b)` | `add(float, float)` |
| `double add(int x, int y)` | The same `add(int, int)` as the first row |

The first three forms can coexist because their parameter counts or types differ. The last cannot coexist with the first by relying on the return type alone. A caller's input form, such as `add(1, 2)`, would be the same. Renaming parameters from `a, b` to `x, y` does not create another signature. The general signature notation on p.7 displays a return type, whereas the Java explanation on p.8 and the undated transcript at 27:51 explicitly exclude it from this distinction. These contexts should be read separately. [computer_programming:NM004, PDF pp.7-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 27:51]]

Overloading **adds a different signature**. Overriding **changes the implementation of an inherited instance method with the same signature**. Calling a return-type-only change an overload would obscure this distinction. An unofficial recalled examination from a different instructor offers a secondary signature comparison, rather than evidence of the current course's examination scope. [EX:cp_2026_1_final_q01a p.1]

### Type-specific movement and a sum of absolute values

A straightforward use of overloading is the same operation on different input types. The `Point.move` example has `float` coordinate fields and two methods whose input types differ. These are the relevant bodies from the material. [computer_programming:NM004, PDF pp.11-12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
void move(int dx, int dy) {
    x += dx;
    y += dy;
}

void move(float dx, float dy) {
    x += dx;
    y += dy;
}
~~~

Starting at the origin, `move(3, 0)` selects the overload with two `int` parameters and reaches `(3.0, 0.0)`. Then `move(0.0f, 4.0f)` selects the overload with two `float` parameters and reaches `(3.0, 4.0)`. The suffix `f` determines the literal's type; it is not decorative notation.

Closely related calculations can also share a name when their input shapes differ. The scalar `abs_add(double a, double b)` returns the sum of two absolute values. The array overload `abs_add(double[] arr)` calls that scalar operation repeatedly. The following excerpt places their central bodies together. [computer_programming:NM004, PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
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
~~~

For ordinary finite inputs, the accumulated `sum` is nonnegative. Thus `abs_add(sum, arr[index])` adds the next element's absolute value to the absolute-value sum already obtained. The source array from `1.0` through `10.0` gives `1 + 2 + … + 10 = 55.0`. A newly chosen small teaching example, `{-2.0, 3.0, -4.0}`, makes the same accumulation visible.

| Element processed | Calculation | New `sum` |
|---|---|---:|
| None | Initial value | 0.0 |
| -2.0 | `abs_add(0.0, -2.0)` | 2.0 |
| 3.0 | `abs_add(2.0, 3.0)` | 5.0 |
| -4.0 | `abs_add(5.0, -4.0)` | 9.0 |

This reuse is a **call from one overload to another**, not inheritance through `extends`. Keeping the central calculation in one place makes its dependent array calculation easier to maintain. It also means that changing the scalar operation requires reconsidering what the array operation now means. The undated transcript's comment about call cost at 34:41 does not establish a performance rule for every call. The supported design lesson is reduced duplication and coordinated maintenance. The example does not provide a complete numerical-library contract for NaN, infinity, or overflow. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 34:41]]

### Adding information: where a search starts

Another overload retains a basic operation while accepting additional information. The DNA example uses the second parameter of `String.indexOf` to specify a **starting index**, rather than an ordinal such as “the second match.” [computer_programming:NM004, PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
String dna = new String("TACGAAGTTACTCGCTGTCAGATCGTAAGCGACGCGATCGTAATGTGAAT");
int first = dna.indexOf("CGC");
int second = dna.indexOf("CGC", first + "CGC".length());
~~~

Indices start at zero. The first `CGC` starts at 12 and has length 3. The second search therefore begins at `12 + 3 = 15` and finds the next match at 32. Passing 12 again would leave the first match within the search range and find it again. Rather than adding a new name such as `indexOfSecond`, the overload supplies an optional piece of information to the same search operation.

This code demonstrates a second search under the assumption that the first match exists. It does not handle a first result of `-1`. Skipping the entire first match also means that it is not a general enumeration of all overlapping matches. The undated transcript has an uncertain `CCT` search term at 35:41 and appears to omit the offset in its explanation at 36:41. The `CGC` and `+ length()` above come from the printed code; they are not reconstructed speech. The printed `indexof` on NM005 p.5 must likewise be distinguished from the exact Java identifier `indexOf`. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 35:41]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 36:41]] [computer_programming:NM005, PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Default wrappers and delegation to a common body

An overload can supply a default for an omitted parameter. In the material's `power` example, the method that accepts an exponent performs the calculation, while the shorter method supplies the default exponent 2. [computer_programming:NM004, PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
static double power(double input, int n) {
    if (n <= 0)
        return 1;
    return input * power(input, n - 1);
}

static double power(double input) {
    return power(input, 2);
}
~~~

`power(2)` delegates to `power(2, 2)`. The calculation becomes `2 × power(2, 1)`, then `2 × 2 × power(2, 0)`. The last call returns 1, giving `4.0`. Similarly, `power(2, 10)` multiplies ten factors of 2 and gives `1024.0`. The base case's integer literal `1` is converted to the method's `double` return type.

The condition is `n <= 0`, not just `n == 0`. For `n = -1`, the printed method immediately returns `1.0`. It does not implement reciprocal powers for negative exponents. The example teaches the relationship between a default wrapper and a recursive body, rather than a complete mathematical and resource contract for every input.

The same delegation principle appears in `debug`. The basic `debug()` prints the field `var1`. One proposed `debug(String s)` copies that field-output expression; another prints the additional message and then calls the basic method. The following are **alternative bodies**. They cannot both be declared with this same signature in one class. [computer_programming:NM004, PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
// Alternative A: copy the field-output expression
void debug(String s) {
    System.out.println(s + "var 1 : " + this.var1);
}

// Alternative B: delegate the common field output
void debug(String s) {
    System.out.print("Output : " + s);
    debug();
}
~~~

With `var1 = 0` and `s = "state: "`, the first alternative prints `state: var 1 : 0`. In the second, the basic `debug()` supplies `var 1 : 0`, so the whole line is `Output : state: var 1 : 0`. Only the second includes the `"Output : "` prefix, so the complete output strings are not identical. Its structural advantage is that a change to the basic field-output format is reused by the delegating method. The undated transcript at 41:23 presents this as a design principle, rather than a mandatory syntactic rule. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 41:23]]

### Constructor overloads and consistent initialization meanings

Constructors can provide several initialization paths with different parameter lists. The `Point` on NM004 p.17 has `double x, y` and compares four paths. This is a separate class example from the earlier `move` example with `float` fields. [computer_programming:NM004, PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| Constructor | Meaning of its inputs | Stored coordinates |
|---|---|---|
| `Point()` | Origin | `x = y = 0` |
| `Point(int x, int y)` | Cartesian coordinates | Supplied `x, y` |
| `Point(float x, float y)` | Cartesian coordinates | Supplied `x, y` |
| `Point(double radius, double theta)` | Polar coordinates | `radius * Math.cos(theta)`, `radius * Math.sin(theta)` |

For the last path, mathematically `radius = 2` and `theta = 0` give `x = 2 cos 0 = 2` and `y = 2 sin 0 = 0`. Initialization can transform a representation rather than merely copy input fields.

Distinct signatures nevertheless do not guarantee a predictable API. `new Point(2.0f, 0.0f)` interprets the two numbers as Cartesian coordinates, while `new Point(2.0, 0.0)` interprets them as radius and theta. A caller who expects only a change of numerical precision may overlook the change in coordinate meaning. At 44:12, the undated transcript criticizes this design and proposes an explicit distinction such as a coordinate-system indicator. That suggestion does not supply an exact implementation of a new required constructor. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 44:12]]

The source line `import Math;` does not establish a valid import. The useful evidence here is the constructor list and the printed conversion expressions. Silently repairing that line would not justify presenting the whole page as a complete executable program. Uncertain spoken radius/radians wording is likewise separate from the printed identifiers and formulas.

### Connecting initialization with this and super

When several constructors repeat the same assignments, one can provide the common initialization. NM004 p.18 delegates that work to `Point(float, float)`. Its fields are again `double`, but its constructor list differs from p.17. In particular, the previous page's two-`double` constructor must not be merged into this example. [computer_programming:NM004, PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
Point(float x, float y) {
    this.x = x;
    this.y = y;
}

Point(int x, int y) {
    this((float)x, (float)y);
}

Point() {
    this(0, 0);
}
~~~

Following `new Point()` requires following the argument types as well as the names.

| Stage | Why it is selected | Next operation |
|---|---|---|
| `Point()` | No arguments | `this(0, 0)` |
| `Point(int, int)` | Both `0` literals are `int` | Cast both values to `float` and delegate |
| `Point(float, float)` | Both arguments are explicitly converted to `float` | Assign the fields |

These are not three newly created objects. Multiple constructor bodies participate in the initialization of **one object**. The inner delegated initialization finishes before control returns to the outer constructor.

At 46:08, the undated transcript suggests using `0.0`. An unsuffixed `0.0` is a `double`, however, so it cannot be passed directly to either of the displayed `int`/`float` constructors. A separately written teaching alternative, `this(0.0f, 0.0f)`, would pass two `float` arguments directly. This makes the type distinction explicit; it does not change the recorded suggestion into a quotation containing `0.0f`. [computer_programming:NM004, PDF pp.18-19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 46:08]]

`this(...)` delegates to another constructor of the same class. `super(...)` delegates initialization to a constructor of the direct superclass. A constructor is not an inherited instance method that a subclass overrides. A subclass constructor uses its own class name and connects necessary parent initialization with `super(...)`. An implicit `super()`, when no explicit constructor invocation is supplied, still requires an accessible no-argument parent constructor. [computer_programming:RM001, PDF pp.49-51](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

Constructor exercises Q06 and P02 assume JDK 11. Under that assumption, the basic rule places an explicit `this(...)` or `super(...)` first so that delegated initialization precedes the remaining work. NM004 p.19 and the undated transcript at 48:59–49:57 separately mention restricted work before the call in Java 25. That mention should neither be erased by claiming one absolute rule for all versions nor expanded into detailed permission rules that the supplied source does not establish. [computer_programming:NM004, PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 48:59]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 49:57]]

The unofficial recalled midterm from a different instructor provides a secondary `this`/`super` connection: distinguish delegation within one object's initialization from the parent initialization it requires. It does not turn a constructor into an inherited method. [EX:cp_2025_1_midterm_q05 p.3]

### When several overloads are applicable

Inheritance allows an argument to fit more than one parameter type. If `ColoredPoint extends Point`, a `ColoredPoint` can also be passed to a `Point` parameter. Consequently, having different signatures does not guarantee that every call selects exactly one of them. [computer_programming:NM004, PDF pp.20-21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
static void test(ColoredPoint p, Point q) {
    System.out.println("(ColoredPoint, Point)");
}

static void test(Point p, ColoredPoint q) {
    System.out.println("(Point, ColoredPoint)");
}
~~~

Consider `test(cp, cp)` where `cp` is declared as `ColoredPoint`.

| Candidate | First argument | Second argument |
|---|---|---|
| `test(ColoredPoint, Point)` | Exactly `ColoredPoint` | Can be viewed as `Point` |
| `test(Point, ColoredPoint)` | Can be viewed as `Point` | Exactly `ColoredPoint` |

Both are applicable. The first is more specific in the first position, and the second is more specific in the second position. Neither parameter list is more specific overall. The call is ambiguous. Choosing whichever declaration appears first, or examining the actual object later at runtime, does not resolve this overload-selection problem.

On pp.22–23, the second declaration is **replaced** by `test(ColoredPoint, ColoredPoint)`. This candidate matches the first candidate's first position and is more specific in the second. It is therefore the most-specific candidate for `test(cp, cp)`, and its body prints `(ColoredPoint, ColoredPoint)`. The undated transcript's “matches first” wording at 52:44 should be read as an abbreviated discussion of this type relationship, rather than textual declaration order. [computer_programming:NM004, PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 52:44]]

`null` provides another way to examine reference-parameter selection. It can be passed to several reference types, but two unrelated parameter types need not have a most-specific relationship. A cast that gives the argument expression an explicit type can change which candidates apply. This is not a change to the actual class of a `null` object. The unofficial recalled final from a different instructor offers a secondary connection between applicability, specificity, and casts. The transferable procedure is to collect applicable candidates and ask whether their type relationships determine one winner; reproducing the original question and its option-by-option answers is unnecessary. [EX:cp_2026_1_final_q08 p.5]

### Why generics help: naming the type in a repeated structure

Overloading is useful for different input forms such as `move(int, int)` and `move(float, float)`. If changing the element type instead leads to copying the same list structure and operations, adding overload after overload does not express the common structure well. Generics place type variables in methods, classes, or interfaces so that a common structure can be applied to several types. The material calls this parametric polymorphism; reuse across repeated structure motivates its introduction. The [Object contracts and interfaces unit](object-contracts-interfaces.md) established the `List<E>` contract and `AbstractList<E>`, which provides part of its common implementation. The repeated name `E` is a **named type parameter** connecting positions that use the same element type. [computer_programming:NM001, PDF pp.55-56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [computer_programming:NM004, PDF p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [computer_programming:NM004, PDF p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

`List<Integer>` and `List<String>` use the same list contract with different element types. `Integer` and `String` are concrete type arguments; `E` is the named position in the declaration. These examples use reference types, so the primitive `int` cannot simply replace `Integer` to form `List<int>`. Expressing permitted elements through types reduces the burden of storing everything as `Object` and repeatedly casting it to an expected type at use. It does not eliminate every possible program error. The explanations on NM005 pp.7–8 are material-based support; they do not imply that every example on those pages was newly explained aloud. [computer_programming:NM005, PDF pp.7-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

The wildcard `?` is different: it denotes an unnamed unknown type. `List<?>` does not mean the same thing as a named `List<E>`, and neither notation means “a box into which any chosen type can be inserted.” A caller cannot arbitrarily decide which element type the unknown represents. Nor does `?` name a relationship across several positions as `E` can. [computer_programming:NM004, PDF p.66](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) The earlier `Collection<?>` example traversed elements and compared them with an `Object`; that observation and comparison do not justify arbitrary insertion. This motivation also does not establish a free conversion from `List<Subtype>` to `List<Supertype>`.

The undated transcript calls `E` a wildcard at 16:41. At 01:25:47, `[[unclear: can take arbitrary type during runtime]]` is uncertain wording about when a type placeholder takes an arbitrary type. Distinguish that wording from the materials' compile-time typing account and from the named-parameter versus wildcard distinction. They are not quotations silently rewritten to agree with the explanation. This section covers the motivation for reuse and the initial notation distinction. Detailed generic classes, methods, constructors, bounds, and ProducerConsumer remain later material-based topics; this discussion does not complete them. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 16:41]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:25:47]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:26:45]]

**Concept check.** (a) Why does a type parameter help with repeated list implementations that differ only in element type? (b) What are `E` in `List<E>`, `Integer` in `List<Integer>`, and `?` in `List<?>`? (c) Does this motivation guarantee arbitrary insertion or conversion from `List<Subtype>` to `List<Supertype>`?

**Reasoning.** (a) Naming the changing type lets common operations and storage structure preserve relationships between several type positions. This addresses a different kind of repetition from adding a separate overload for each input form. (b) `E` is a named parameter in a declaration, `Integer` is a concrete reference type argument, and `?` is an unnamed unknown type. (c) An unknown type cannot be chosen arbitrarily by the caller, and relationships between parameterized types require their own rules. Neither guarantee follows from the motivation; detailed permitted operations and generic relationships require later study.

## Recall and Practice

### Concept recall

#### Recall Q01 · Signatures and related behavior

Which pair cannot coexist among `int add(int a,int b)`, `double add(int x,int y)`, `int add(int x,int y,int z)`, and `float add(float a,float b)`? Does renaming parameters create an overload? Does `Fish.swim()` override `Animal.move()`?

<details><summary>Show solution</summary>

The first two both have signature `add(int,int)` and cannot coexist on return type alone. Three ints and two floats give different parameter counts or types and therefore separate overloads. For these non-generic methods, compare the name and ordered parameter types; variable names and return type do not distinguish them. The caller's name and inputs in `add(1,2)` are the same, so the result cannot separate those declarations.

Overloading adds a different signature; overriding changes the implementation of an inherited instance signature. Different names `swim` and `move` cannot form an override merely because their meanings are related. Sharing a purpose-specific name can reduce the burden of remembering names such as printInt, but that motivation differs from the signature rules.

**Checking points:** Identify the conflicting pair, both distinct forms, excluded parameter names/return type, and swim/move.

</details>

#### Recall Q02 · Point movement and abs_add reuse

A Point with initially zero float fields has `move(int,int)` and `move(float,float)` adding dx,dy. Trace `move(3,0)` then `move(0.0f,4.0f)`. An array abs_add starts sum at zero and calls scalar `abs_add(a,b)=|a|+|b|` as `sum=abs_add(sum,arr[i])`. Trace arrays 1.0–10.0 and {-2.0,3.0,-4.0}, and explain the reuse.

<details><summary>Show solution</summary>

The first call selects int/int and reaches (3.0,0.0); the f-suffixed second call selects float/float and reaches (3.0,4.0). The same movement is offered for different input types.

For ordinary finite inputs within the represented range, accumulated sum is nonnegative, so `|sum|+|next|=sum+|next|`. The 1–10 sum is 10×11/2=55.0. The smaller array traces 0.0→2.0→5.0→9.0. Scalar and array input shapes serve closely related calculations. The array body calls the scalar body for reuse; it does not inherit it through extends. Changing scalar meaning requires rechecking array meaning. This reduces duplicated maintenance without establishing that every call is necessarily expensive. No complete NaN/infinity/overflow contract is supplied.

**Checking points:** Check both selected types, both positions, 55 and 2/5/9, and reuse by a call.

</details>

#### Recall Q03 · Additional information in indexOf

In the source DNA, the first CGC starts at index 12, has length 3, and the following start is 32. Where does `indexOf("CGC", first + "CGC".length())` begin searching? What if its start is first? Why is this not a match ordinal, and what are the missing-match and overlap limits?

<details><summary>Show solution</summary>

The starting index is 12+3=15, and the first match from there is 32. Passing 12 again leaves the original CGC in range, so it is found again at 12. The second parameter is a zero-based starting position, not an ordinal requesting match number 2. It is an overload adding information to the same search.

The example assumes the first search succeeds and supplies no first=-1 handling. Skipping the full match length also misses potential overlaps starting inside that match.

**Checking points:** Explain 15→32 and rediscovery at 12, with both missing-match and overlap limits.

</details>

#### Recall Q04 · Wrappers with default values and debug alternatives

`power(input,n)` returns 1 if n<=0 and otherwise input×power(input,n-1); the one-argument overload delegates with n=2. Find `power(2)`, `power(2,10)`, and `power(2,-1)`. Basic debug prints `var 1 : 0`. The copied debug(s) prints `s+"var 1 : "+var1`; the delegating alternative uses `print("Output : "+s); debug();`. For s=`"state: "`, explain both outputs and the design difference.

<details><summary>Show solution</summary>

`power(2)` delegates to power(2,2), giving 2×power(2,1)=2×2×power(2,0)=4.0. `power(2,10)` multiplies ten twos for 1024.0; `power(2,-1)` immediately satisfies n<=0 and returns 1.0. The base-case literal 1 is returned as double. This is not a reciprocal-power implementation for negative exponents.

The copied alternative prints `state: var 1 : 0`; delegation prints `Output : state: var 1 : 0`. Their prefixes differ. Delegation follows future changes to the basic debug field-output format. The debug(String) bodies are alternatives with one signature and cannot both be declared together. Concentrating work in a common body is a maintenance principle here, not a syntactic requirement for every overload.

**Checking points:** Check all three values, the negative base case, both exact outputs, and propagation of changes.

</details>

#### Recall Q05 · Legal overloads and predictable APIs

In the independent p.17 Point example, fields are double: Point() gives the origin, int/int and float/float use Cartesian coordinates, and double radius/theta performs a polar conversion. Explain all four paths, radius=2/theta=0, and the risk in changing `new Point(2.0f,0.0f)` to `new Point(2.0,0.0)`.

<details><summary>Show solution</summary>

No arguments gives (0,0); int/int and float/float store the supplied Cartesian x,y. `double`/`double` uses x=r cos(theta), y=r sin(theta), giving (2,0) mathematically for r=2,theta=0. Although these particular calls may give the same coordinates, the first interprets Cartesian inputs and the second polar inputs.

A caller intending only a precision change can accidentally change meaning. Distinct signatures and a predictable API are different criteria. An explicit coordinate-system indicator is a design suggestion, not a supplied implementation of another required constructor. The original `import Math;` also does not establish a valid whole program; do not merge this example with the next page's different constructor list.

**Checking points:** Explain all four paths, formulas, and semantic change without merging the two Point definitions.

</details>

#### Recall Q06 · One-object initialization with this and super

In the separate p.18 example, Point(float,float) assigns fields, Point(int,int) calls `this((float)x,(float)y)`, and Point() calls `this(0,0)`. Trace initialization of one object. Do 0,0.0,0.0f select the same path? Explain this versus super, the condition for implicit super(), and the version scope of the first-action rule.

<details><summary>Show solution</summary>

The path is Point()→Point(int,int)→Point(float,float). Both zeros are int literals, selecting the middle path, which casts them to float and delegates the common assignments. Inner initialization finishes before returning outward; three objects are not created. `this(0.0f,0.0f)` directly fits float/float, but unsuffixed `this(0.0,0.0)` supplies doubles that do not directly fit this int/float constructor list. Importing the previous page's double constructor would merge different examples.

`this(...)` delegates to another constructor of the same class; super connects to the direct superclass constructor. Implicit super() still needs an accessible no-argument parent constructor. Constructors are not inherited or overridden. Here, assume the JDK 11 context and apply its explicit this/super-first rule. Source p.19 separately mentions restricted prior work in Java 25, which neither establishes an absolute rule for every version nor supplies detailed permission syntax.

**Checking points:** Explain every argument type, one object, accessibility, and the version qualification.

</details>

#### Recall Q07 · Most-specific selection across two positions

ColoredPoint extends Point. Why is passing cp,cp (both declared ColoredPoint) ambiguous between `test(ColoredPoint,Point)` and `test(Point,ColoredPoint)`? What changes if the second declaration is replaced by `test(ColoredPoint,ColoredPoint)`? Can declaration order or the runtime receiver settle it?

<details><summary>Show solution</summary>

Initially cp can also fit Point, so both candidates apply. One is more specific in the first position and the other in the second; neither whole list is uniquely most specific. The invocation is ambiguous during overload selection.

After replacement, (ColoredPoint,ColoredPoint) matches the first candidate in the first position and is more specific in the second. It is selected and prints `(ColoredPoint, ColoredPoint)`. Different signatures do not guarantee a unique selection for every call. Textual declaration order and deferring overload choice until runtime do not resolve it. `null`/cast cases likewise begin with applicable candidates and expression types.

**Checking points:** Judge both versions by type relationships in each position, not declaration order.

</details>

### Practice

#### Practice P01 · Two-position candidates and casts

Newly written synthetic practice. Transfer only reference-overload applicability, null, and cast reasoning from [EX:cp_2026_1_final_q08 p.5]. Prerequisites are sibling subclasses Circle/Square of Shape, overloads, and upcasts.

Candidates are `choose(Shape,Shape)`, `choose(Circle,Shape)`, and `choose(Shape,Square)`. Circle c and Square s are non-null. Explain (a) choose(c,s), (b) choose((Shape)c,s), and (c) choose(null,null). (d) What changes for a,c after adding `choose(Circle,Square)`? Bodies only display the selected signature without inspecting values.

<details><summary>Show solution</summary>

(a) has three applicable candidates, but Circle/Shape and Shape/Square are more specific in different positions, so it is ambiguous. Both dominating Shape/Shape does not order them against each other.

(b) gives the first expression type Shape, excluding Circle/Shape. Of the remaining two, Shape/Square is more specific in the second position and wins; c's actual object is unchanged. In (c), both nulls fit all reference lists, leaving the same incomparable pair and ambiguity.

(d) adds Circle/Square, equal in one position and more specific in the other relative to each cross candidate. It wins for both a and c. `null` has not become a Circle/Square object; the premise that bodies do not dereference it matters.

**Checking points:** Explain candidate inclusion/exclusion and both positions; treat neither casts nor null as object transformation.

</details>

#### Practice P02 · Checking changes to initialization delegation

Newly written lecture-based general practice. The indexed this/super concept item does not directly establish the format of this change-checking task. Assume the JDK 11 initialization context.

In the p.18-style int→float constructor chain, add one hypothetical check to the common float body. Compare paths and check counts with `this(0,0)` versus `this(0.0f,0.0f)`. Why not `this(0.0,0.0)`? Connect common-body reuse and accessible parent-constructor requirements.

<details><summary>Show solution</summary>

The first path is no-argument→int/int→float/float; the second is no-argument→float/float. Each reaches the common float body once for one object, so the added check occurs once. More constructor bodies do not automatically mean more objects or repeated checks. Central assignments/checks make both paths follow the same change.

Unsuffixed 0.0 is double, and this list has no double/double constructor, so it cannot be passed directly to the int/float forms. A seemingly simple default change still needs literal-type analysis. Same-class this delegation does not replace superclass initialization or remove access conditions. The actual chain needs an accessible parent constructor, including implicit super(). Read the hypothetical check after delegation in this JDK 11 context.

**Checking points:** Include both paths, one check, double literals, and parent accessibility.

</details>

### Generics introduction supplement

#### Recall Q08 · The reuse motivation for generics

(a) When list implementations differ only by element type, what different repetition is addressed by overloads versus type parameters? (b) Distinguish E, Integer/String, and ? in `List<E>`, `List<Integer>`, `List<String>`, and `List<?>`. (c) Compare storing Object then casting, and state the limits on arbitrary insertion, subtype conversion, and elimination of errors.

<details><summary>Show solution</summary>

Overloads offer related behavior for different input forms under one name. Generics name the changing type in a repeated common structure, reusing relationships among several type positions. On the established List contract→shared AbstractList implementation→concrete ArrayList foundation, this motivates avoiding a copy of the structure for every element type.

E is a named type parameter in a declaration; Integer and String are concrete reference type arguments. Integer is not primitive int, so `List<int>` is not a replacement. ? denotes an unnamed unknown type, rather than naming the same type across positions as E can.

Exposing element types can reduce storing Object and repeatedly casting to the expected type. It does not let a caller choose the unknown type of List<?> for arbitrary insertion, imply free conversion of `List<Subtype>` to `List<Supertype>`, or eliminate all program errors. This answer covers reuse motivation and notation only; detailed generic classes/methods/constructors, bounds, and ProducerConsumer remain later material-based topics.

**Checking points:** Cover reuse, E/argument/?, and all three nonguarantees without adding detailed generic implementations.

</details>

## Sources

### Lecture notes and transcripts

- [[courses/computer_programming/lectures/en/undated-inheritance-polymorphism-vemyed7m83v2ejw2|Date unconfirmed · Object contracts, polymorphism, and generic introduction]]
- [[courses/computer_programming/lectures/en/2026-09-01-lecture-01|2026-09-01 · literal types and conversion foundations]]
- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · array and traversal prerequisites]]
- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · object, constructor, static, and reference prerequisites]]
- [[courses/computer_programming/lectures/en/2026-09-17-lecture-06|2026-09-17 · object, initialization, and reference recap]]

Dated notes link the stated prerequisites; they do not establish that detailed inheritance/dispatch was completed on those dates.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · undated transcript]] — 26:53, 27:51, 33:13, 34:41, 35:41, 36:41, 41:23, 44:12, 46:08, 48:59, 49:57, 50:55, 52:44, 16:41, 01:25:47, 01:26:45.

### Materials and physical PDF pages

Page numbers count physical PDF pages; each page link includes the original page.

- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-008), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-023), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-052), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-059), [p.66](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-066).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-003), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-005), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-008), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).
- [6 inheritance 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042).

### Scope and uncertainties

NT001 is undated. Its 95 utterances retain 124 literal uncertainty markers and 76 additional limits; unclear speech, negation, and missing words are not reconstructed from printed material. Printed examples are material evidence, not evidence that every example was newly spoken. Times below locate transcript passages and are not timestamp anchors.

NM005 has 36 physical PDF pages. Its registered Lab 6 title conflicts with the printed Lab 1 cover; TODOs and the unavailable ZIP referenced on p.19 remain unresolved. It is used for concepts, without supplying a completed graded implementation or transferring attendance/submission rules.

Although NM004 p.7 displays a return type in its signature notation, return type does not distinguish these overloads. NT001's uncertain CCT, offset, radius/radians, and 0.0 wording is separate from printed CGC, +length, and identifiers. The Cartesian/polar Point on p.17 differs from the this-delegation Point on p.18. Original import Math; does not establish complete valid source. No measurement supports universal call costs or recursion limits.

Q06 and P02 explicitly assume JDK 11, distinguishing NM004 p.19's first-action rule from its separate Java 25 mention. This does not claim verification of later-version specifications. The generics supplement covers reuse motivation, named E versus ?, and nonguarantees only. Detailed generic classes/methods/constructors, bounds, and ProducerConsumer remain later material topics.

### Qualified connections to unofficial recalls

These are unofficial recalled documents with no verified official keys supplied. The filenames alone associate the 2025-spring midterm with Kim Sanghan (김상한) and the 2026-spring final with Yoo Youngjae (유영재), different from current instructor Jaemin Yoo (유재민). Connections concern only the concepts or reasoning below and establish no current style, scope, frequency, or probability. New questions are general or synthetic practice.

- [EX:cp_2026_1_final_q01a p.1] — Compare a non-generic method’s name and ordered parameter types, excluding parameter names/return type and detailed generic-signature rules.
- [EX:cp_2025_1_midterm_q05 p.3] — Connect only the this(...)/super(...) concepts after object/inheritance prerequisites. This does not classify the whole recalled question as a constructor exercise.
- [EX:cp_2026_1_final_q08 p.5] — Connect reference-overload applicability and unique specificity under null/casts to P01. Inheritance, reference types, and Q07 are prerequisites; original option-by-option answers are not supplied. [[exam_questions/cp_2026_1_final_q08|Existing question preview]]

No indexed item directly matches Point movement, abs_add, the exact DNA search, power/debug, polar-coordinate design, or a complete constructor-delegation trace. P02 is general change-checking practice; generic implementation and bounds questions exceed this introductory supplement.
