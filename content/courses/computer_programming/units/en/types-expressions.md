---
title: "Variables, Types, Operators, and Strings"
description: "Check conversions, evaluation, Strings, and line input through calculation and tracing."
course: "computer_programming"
unit_id: "types-expressions"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 2 Java Basics 1.pdf", "3 java basics 2.pdf", "4 oop.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-01-lecture-01", "courses/computer_programming/lectures/en/2026-09-08-lecture-03"]
---

Track an expression's type, result, and final variable state separately. Distinguishing String contents from references resolves common operator and input mistakes.

## Variables and types define storage and computation

After [[courses/computer_programming/units/en/java-runtime|the Java execution environment]], the next task is to explain what each statement reads and changes. A variable is named storage for a value of a specified type. A declaration introduces its name and type; initialization supplies its initial value; assignment stores a value.

```java
int x;        // declaration
x = 10;       // assignment before the first read
x = 15;       // later assignment
int sum = 0;  // declaration with initialization
```

This expands the distinctions in [Computer Programming M002, PDF pp.27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf). Identifiers are case-sensitive: `myVar` and `myvar` differ. The introductory naming rules permit letters, digits, underscores, and dollar signs, but not a leading digit. Names such as `age`, `sum`, and `totalVolume` reveal purpose. Starting variable names with lowercase is a convention. `String` is a class name, not a keyword, and a lone `_` is not a valid identifier in the course's JDK 11.

A local variable must be assigned before it is read. Merely writing `int x;` does not give it a readable value. The wording at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 12:10]] about an uncertain JVM-selected initial value needs a factual qualification: **definite assignment of locals differs from default initialization of fields and array components**. This correction does not claim that the recorded speech itself was corrected.

### Primitive values and reference values

The eight primitive types are `boolean`, `char`, `byte`, `short`, `int`, `long`, `float`, and `double`. A `boolean` is `true` or `false`; a `char` is a character value written with single quotes, such as `'A'`. The signed integer types have these sizes:

| Type | Bits | Signed range |
| --- | ---: | --- |
| `byte` | 8 | −128 … 127 |
| `short` | 16 | −32,768 … 32,767 |
| `int` | 32 | −2,147,483,648 … 2,147,483,647 |
| `long` | 64 | −2⁶³ … 2⁶³−1 |

An N-bit signed integer has 2ᴺ possible values, from −2⁽ᴺ⁻¹⁾ through 2⁽ᴺ⁻¹⁾−1. For a `byte`, −128 through 127 gives 256 values. Including 128 as well would incorrectly give 257.

The floating-point types `float` and `double` use 32 and 64 bits. The material compares roughly 6–7 digits of precision with roughly 15. These are approximate **significant digits**, not a fixed guarantee about digits after the decimal point; the wording on M002 p.33 needs that correction. The diagrams on M002 p.31 and M011 p.46 also incorrectly place floating-point under Integral Value. Greater precision motivates using `double` for ordinary calculations, while large data sets make memory cost relevant. The discussion at [[courses/computer_programming/transcripts/2026-09-01|2026-09-01, 01:01:31]] connects type selection to this tradeoff.

A reference variable stores a value referring to an object, rather than the whole object. The storage occupied by a long String's characters is therefore a different issue from the storage for its reference variable. A reference is not a guarantee of a particular physical address representation, and different objects need not have equal sizes. Detailed binary encodings and endianness are beyond this treatment.

## Conversions and the types of literals

The material introduces widening along `byte → short → int → long → float → double`. Narrowing in the opposite direction may lose information and requires an explicit cast in the examples.

```java
double testDouble = 1.0;
float testFloat = (float) testDouble;
```

The cast converts this expression's value; it does not change the declared type of `testDouble`. M002 pp.38–42 and [[courses/computer_programming/transcripts/2026-09-01|2026-09-01, 01:08:40]] make the type of the assigned value central.

| Assignment | Result and reason |
| --- | --- |
| `float f = 3.72;` | Invalid as written: the unsuffixed literal is `double` and requires narrowing. |
| `double d = 3.72f;` | The `f` suffix makes a `float` literal, which widens to `double`. |
| `int i = 1000L;` | Invalid as written: the value is small, but the literal's type is `long`. |
| `long l = 1000;` | The `int` literal widens to `long`. |

The material's `13243` versus `13243L` illustrates the same distinction. Automatic widening is not a universal promise of exact preservation: an integer converted to floating-point may be rounded because of limited precision. The introductory chain is not a complete conversion table covering `char` and `boolean`.

## Operator results and the next variable state

In `x + 10`, `x` and `10` are operands and `+` is the operator. Arithmetic operators `+`, `-`, `*`, `/`, and `%` compute sum, difference, product, quotient, and remainder; `++` and `--` change a value by one. Classifications can overlap: increment is both unary and arithmetic.

| Expression | Result | Reason |
| --- | --- | --- |
| `5 / 2` | `int` value `2` | Integer division discards the fractional part. |
| `5 % 2` | `int` value `1` | This is the remainder, not the quotient. |
| `15 / 3.0` | `double` value `5.0` | Mixed numeric operands undergo conversion. |
| `2 << 3` | `int` value `16` | Binary `10` shifted three positions becomes `10000` in this example. |
| `0b1 & 0b0` | `0` | AND is applied to corresponding bits. |
| `true && false` | `false` | Boolean conditions are combined. |

Integer `5 / 0` is an error; that statement should not be generalized to all floating-point division. Read the operator introduction at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 04:33–09:18]] together with the mixed-type example: operators do not universally preserve an input type. The bitwise operators `&`, `|`, and `^` perform AND, OR, and XOR; shifts change bit positions.

### Prefix, postfix, and compound assignment

M002 pp.57–58 starts these two examples from separate initial states:

```java
int x1 = 1, y1 = 1;
int prefixResult = x1 + ++y1;  // 3; y1 is now 2

int x2 = 1, y2 = 1;
int postfixResult = x2 + y2++; // 2; y2 is now 2
```

Prefix `++y1` supplies the updated value, 2. Postfix `y2++` supplies the old value, 1, while also changing the stored value to 2. Equal final values of `y1` and `y2` therefore coexist with different expression results.

Compound assignment reads the left variable, performs an operation, and stores the result back there. After `x = 10; x += 5;`, `x` is 15. For the demonstrated `int` cases, `x -= 3`, `x *= 3`, `x /= 3`, and `x %= 3` store the corresponding arithmetic results. The same update structure applies to `x &= 3`, `x |= 3`, `x ^= 3`, `x >>= 3`, and `x <<= 3`. In particular, `x <<= 3` uses `x` as the left operand, not `3`. This is not an unrestricted textual-substitution rule for all types. The lecture's description of compound assignment as unary also conflicts with its two-operand syntax.

Starting from `x = 1, y = 2, z = 3`, `x = y = z` groups as `x = (y = z)`. The inner assignment stores 3 in `y` and yields 3; the outer assignment stores that in `x`. Understanding this does not require routinely writing compressed expressions: the readability warning at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 29:09–30:09]] still applies.

### Precedence, associativity, and evaluation order

Precedence determines grouping; associativity determines grouping among operators at the same level. Operand evaluation order describes when the computations actually occur.

```java
int x = 5;
int y = 10;
int z = ++x + y * 3;
```

The grouping is `(++x) + (y * 3)`. Java evaluates the left operand first: `++x` changes `x` to 6 and yields 6. The right operand yields 30 without changing `y`. Thus `z = 36`, with final `x = 6` and `y = 10`. Higher multiplication precedence does not mean that this right operand must execute before the left operand.

The Java-relevant groups in the supplied table descend through access/grouping, unary/casts/prefix operations, `* / %`, `+ -`, shifts, relational comparison, equality, bitwise AND, XOR, OR, logical AND, logical OR, `?:`, and assignment. Relational `< <= > >=` and equality `== !=` occupy distinct levels. M002 p.74 also contains C/C++ entries such as `sizeof`, pointer meanings of `*` and `&`, and the comma operator; these are not Java rules. At [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 32:03–33:02]], the lecturer was uncertain about increment's position, although the table contains prefix increment. The lecturer did not require memorizing the whole table. Parentheses make intent explicit without turning that uncertainty into a newly certain statement.

## Separating String contents from references

`String` is a reference type with methods such as `length()`, `toUpperCase()`, `toLowerCase()`, and `concat()`. As an explanatory substitution for the personal-name literal on M002 pp.43–45, take `"Java"`: its length is 4, its uppercase form is `"JAVA"`, and its lowercase form is `"java"`. Both `"Java".concat("Code")` and `"Java" + "Code"` yield `"JavaCode"`. As in the source, no space is inserted automatically.

The meaning of `+` depends on the preceding result in its left-associated chain:

```java
System.out.println(1 + "2");                        // 12
System.out.println("The answer is: " + 2 + 3 + "!"); // The answer is: 23!
System.out.println(2 + 3 + " is the answer!");       // 5 is the answer!
```

The second line appends 2 and then 3 to a String; the third first computes the integer sum 5. The colon in the actual literal is part of the output. String conversion here is not primitive numeric widening, and `println` is not restricted to String arguments.

### Immutability and equality

String immutability prevents changing an object's character contents. It does not prevent reassigning a variable's reference.

```java
String appleOne = "Apple";
String appleTwo = "Apple";
appleTwo = "Pear";
```

Afterward, `appleOne` still refers to `"Apple"`. The original Apple did not turn into Pear; the reference stored in `appleTwo` changed. This is the distinction in [[courses/computer_programming/transcripts/2026-09-01|2026-09-01, 01:15:24]] and [M002 PDF pp.47–48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf). The String Pool model explains sharing, not a guaranteed physical layout in every JVM.

Two calls to `new String("Apple")` create distinct objects: `==` is `false` even though `String.equals()` is `true`. Two variables using the same pooled `"Apple"` literal refer to one object, so both comparisons are `true`. Even there, `==` succeeds because of identity, not because it compares contents.

Primitive comparisons `== != > < >= <=` yield booleans; `=` assigns. Do not replace the valid symbols with `=>`, `=<`, or `<>`. To ask whether a non-null String `a` differs in content from `b`, negate the boolean result with `!a.equals(b)`, as discussed at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 19:41–21:36]]. A potentially null receiver first needs a [[courses/computer_programming/units/en/control-flow|short-circuit guard]]. Other classes do not necessarily implement `equals` like String.

## Scanner: input, return, storage, and output

The Scanner example connects Strings to external input. In the code from M002 pp.21–22, the import belongs at the start of the file and the remaining statements inside a method body.

```java
import java.util.*;
```

```java
Scanner scanner = new Scanner(System.in);
System.out.println("Enter username");
String userName = scanner.nextLine();
System.out.println("Username is: " + userName);
```

`scanner.nextLine()` waits for a line and Enter, then returns that line as a String. Assignment stores the returned value in `userName`; the following statement prints it. Reading, returning, assigning, and printing are separate stages. When the required input is a whole line, spaces do not justify discarding the remainder. The explanation at [[courses/computer_programming/transcripts/2026-09-01|2026-09-01, 54:38]] follows this flow. This bounded use of imports and Scanner does not establish completion of the later, deferred Packages chapter.

## Key Takeaways

- Locals require assignment before reading; field/array defaults are a different rule.
- Read literal types and cast positions first. Widening need not preserve every numeric detail.
- Precedence groups expressions; evaluation order sequences them. Track increment results separately from stored values.
- String reassignment does not edit characters. Identity and content equality answer different questions.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Declaration, assignment, names

Distinguish local `int x;`, `int x=10;`, and later `x=15;`. Explain `myVar`/`myvar`, `String`, `_`, and field defaults.

<details><summary>Show solution</summary>

The first only declares a local and needs assignment before reading; the second declares and initializes; the third assigns an existing variable. `myVar` and `myvar` are different identifiers. `String` is a class name, not a keyword; a lone `_` is invalid in the course's JDK 11. Meaningful lowercase-start names are a convention. Field/new-array defaults do not make unassigned locals readable.

**Checking points:** Separate declaration/initialization/reassignment and identifier rules/conventions.

</details>

#### Recall Q02 · Primitive ranges and references

Classify all eight primitive types and give integer widths. Explain why byte cannot span −128 through 128, how float/double precision differs, and what a reference to a long String stores.

<details><summary>Show solution</summary>

`boolean` stores true/false; `char` a character; byte/short/int/long are signed integers of 8/16/32/64 bits; float/double are floating-point types of 32/64 bits. An N-bit signed range is −2^(N−1) through 2^(N−1)−1. `byte` has 256 states, so −128…127 fits; including +128 would require 257. Roughly 6–7 versus 15 digits means significant digits, not guaranteed decimal places. `double` trades more memory for greater precision. A String reference stores a reference value, not all characters. The source diagram placing floating-point under integral is incorrect.

**Checking points:** Include all eight types, widths, the 256-value count, significant digits, and reference storage.

</details>

#### Recall Q03 · Literal types and casts

Judge `float f=3.72;`, `double d=3.72f;`, `int i=1000L;`, and `long l=1000;`. Does `(float)testDouble` change its declared type, and is every widening exact?

<details><summary>Show solution</summary>

The first and third are invalid as written because they narrow double→float and long→int. The second and fourth widen float→double and int→long. Literal type matters even when the value looks small. A cast converts the expression's value; testDouble remains declared double. Integer-to-floating widening may round due to precision limits. The introductory chain is not a complete char/boolean conversion table.

**Checking points:** Give all four judgments, the cast target, and the precision qualification.

</details>

#### Recall Q04 · Division, remainder, mixed types

Evaluate `5/2`, `5%2`, `15/3.0`, `2<<3`, `0b1&0b0`, and `true&&false`, explaining types or operation kinds. Identify operands/operator in `x+10` and classify `++`.

<details><summary>Show solution</summary>

The results are int 2, int 1, double 5.0, int 16, int 0, and boolean false. Integer division discards the fraction; remainder is separate. The double operand makes the mixed division double. Shifting binary 10 three positions gives 10000. Bitwise AND and boolean AND operate on different kinds of values. x and 10 are operands, + the operator; increment is both unary and arithmetic. Integer division by zero fails, without establishing the same rule for floating-point.

**Checking points:** Explain quotient/remainder and bit/boolean distinctions, not just values.

</details>

#### Recall Q05 · Increment result versus state

From independent initial states x=1,y=1, evaluate `x + ++y` and `x + y++` and give final x,y.

<details><summary>Show solution</summary>

Prefix changes y to 2 and uses it, producing 3; postfix uses old y=1, producing 2. Both finish at x=1,y=2. Postfix still changes the stored y, so the result 2 does not leave y at 1.

**Checking points:** Separate both expression results from final variable states.

</details>

#### Recall Q06 · Compound and chained assignment

Trace `int x=10; x+=5; x<<=3;`. Independently group and evaluate `x=y=z` from x=1,y=2,z=3, and classify the operations in the compound-assignment table.

<details><summary>Show solution</summary>

x changes 10→15→120. In this int example, `x<<=3` shifts x left by three and stores it; it is not `3<<x`. Chaining groups as `x=(y=z)`, leaving all three at 3. `+= -= *= /= %=` store arithmetic results, `&= |= ^=` bitwise results, and `>>= <<=` shift results into the left variable. These two-operand forms are not unary and are not unrestricted textual substitutions for all types.

**Checking points:** Identify the left shift operand, right-associative grouping, and update targets.

</details>

#### Recall Q07 · Grouping and evaluation order

From x=5,y=10, parenthesize `int z=++x+y*3;` and explain evaluation and final values. May the table's sizeof, pointer *, and comma entries be used as Java rules?

<details><summary>Show solution</summary>

The grouping is `(++x)+(y*3)`. The left increment first sets x=6 and yields 6; the right product yields 30 without changing y. Final z=36,x=6,y=10. Precedence controls grouping, associativity grouping at one level, and evaluation order the sequence. Relational/equality, bitwise AND/XOR/OR, and logical AND/OR occupy distinct levels. C/C++ table entries are not Java rules; parentheses clarify intent.

**Checking points:** Do not mistake higher multiplication precedence for evaluating the right operand first.

</details>

#### Recall Q08 · String operations and output

Give the length, upper/lowercase forms, and concat("Code") result for "Java". Evaluate `1+"2"`, `"The answer is: "+2+3+"!"`, and `2+3+" is the answer!"`.

<details><summary>Show solution</summary>

The results are 4, JAVA, java, and JavaCode, with no automatic space. The expressions produce Strings `12`, `The answer is: 23!`, and `5 is the answer!`. Left-associated addition appends 2 and 3 separately after a String, whereas the last expression first adds integers to get 5. The colon belongs to the literal. String conversion is not primitive widening; println can also print numbers.

**Checking points:** Preserve spaces/colon and distinguish numeric addition from concatenation.

</details>

#### Recall Q09 · Immutability and reassignment

After `String a="Apple", b="Apple"; b="Pear";`, explain the contents reached through each reference. Does assigning b violate immutability?

<details><summary>Show solution</summary>

a still refers to Apple; b refers to Pear. The assignment changes b's reference value, not Apple's characters, so a remains unchanged. Pool sharing explains this relationship without guaranteeing physical memory layout.

**Checking points:** Identify b's reference storage as the changed location.

</details>

#### Recall Q10 · Identity and content equality

Compare separate `new String("Apple")` objects and two uses of the same literal using == and equals(). Give a content-inequality test for non-null a and the primitive comparison symbols.

<details><summary>Show solution</summary>

Separate objects give false for == and true for String.equals. Shared pooled literals give true for both, but == still tests identity. For non-null a, `!a.equals(b)` tests unequal contents. Comparison symbols are `== != > < >= <=`; `=` assigns, and `=> =< <>` are not alternatives. A null receiver requires protection, and other classes need not implement equals like String.

**Checking points:** Give all four results, their reasons, and the non-null assumption.

</details>

#### Recall Q11 · Input, return, storage, output

Scanner reads the line `Computer Programming` into `String userName=scanner.nextLine();`, followed by `println("Username is: "+userName)`. Explain each stage and the output.

<details><summary>Show solution</summary>

After the import makes the names available, `new Scanner(System.in)` creates the input object inside a method. nextLine waits for a line and Enter and returns a String including the space. Assignment stores it in userName; println prints `Username is: Computer Programming` and a newline. Reading, return, and assignment are not themselves output. This example does not cover all package or input-error behavior.

**Checking points:** Preserve the space and identify each stage's responsibility.

</details>

#### Recall Q12 · Associativity within a level

Compare grouping for `10-3-2` and `x=y=z` from x=1,y=2,z=3. What purpose do parentheses serve?

<details><summary>Show solution</summary>

Subtraction groups `(10-3)-2`, giving 5 rather than 9 from `10-(3-2)`. Assignment groups right as `x=(y=z)`, leaving all at 3. Associativity specifies grouping at one precedence level, not operand evaluation order itself. Parentheses make intended grouping explicit.

**Checking points:** Explain 5 versus 9 and right-associative assignment.

</details>

### Apply the ideas

#### Practice P01 · Equal output, equal state?

**Newly written lecture-based general practice; no direct indexed style match.**
```java
int n = 2;
String a = "n=" + n++ + (n * 2);
String b = "n=" + (n + n * 2);
```
Find a, b, and final n. Explain what the parenthesized parts change.

<details><summary>Show solution</summary>

For a, postfix appends old n=2 and changes n to 3. The product is then 6, yielding `n=26`. For b, the parenthesized sum is 3+3×2=9, yielding `n=9`; final n=3. The first parentheses compute the product numerically but do not add it to the 2 already appended to a String. The second computes the entire sum before concatenation.

**Checking points:** Mark the mutation point and the String/numeric role of each +.

</details>

#### Practice P02 · Two different proposed fixes

**Newly written lecture-based general practice; no direct indexed style match.** Consider `float f=3.72;` and separately `String a=new String("Code"), b=new String("Code");`. Correct both claims: “the small value makes the first line valid” and “false from a==b means different text.”

<details><summary>Show solution</summary>

The first ignores literal type: 3.72 is double, so use a float literal such as 3.72f or an explicit cast for that value. The second confuses identity and contents: separate new expressions make == false, while a.equals(b) is true. Casting transforms a numeric expression; equals compares String contents, so these fixes address different causes.

**Checking points:** Separate the type error from the identity/content error.

</details>

### Review plan

Use Q01–Q04 for types/conversions and make intermediate-value tables for Q05–Q08. Explain Q09–Q12, then solve P01–P02 and retrace only the failed steps.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-01-lecture-01|2026-09-01 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 corrected transcript]] — 57:48, 01:01:31 (`float`/`double` precision–memory tradeoff), 01:03:31 (integer range), 01:08:40, 01:15:24, 54:38.
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 12:10, 04:33, 09:18, 14:06 (compound-assignment operand order), 29:09–30:09 (chained-assignment readability), 32:03, 33:02, 19:41, 21:36.

### Materials and page views

- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-021), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-027), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-033), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-039), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-045), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-057), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-061), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-062), [p.64](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-064), [p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-071), [p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-073), [p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-074).
- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-018).
- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-048).

Keep the corrections to integer ranges, significant digits, and local initialization distinct from inaccurate source wording. Do not import C/C++ entries from the precedence table into Java. The String Pool diagram explains sharing, not physical layout; Scanner/import use does not complete the Packages topic.


---

[[courses/computer_programming/units/en/java-runtime|← Previous: Programming Goals and the Java Execution Environment]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/arrays|Next: Array Creation, References, and Multidimensional Data →]]
