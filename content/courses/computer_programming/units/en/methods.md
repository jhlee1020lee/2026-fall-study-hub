---
title: "Method Contracts, Calls, Returns, and Reuse"
description: "Review reusable averages, method contracts/signatures, and call/return flow."
course: "computer_programming"
unit_id: "methods"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["3 java basics 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-08-lecture-03"]
---

Read method declarations as input/result contracts and trace calls through use of the returned value. Explain reuse while separating printing, returning, and casting.

## Methods give calculations a named responsibility

Even after learning to compute an average with [[courses/computer_programming/units/en/arrays|arrays]] and [[courses/computer_programming/units/en/control-flow|loops]], copying the calculation creates more places to maintain. A function is a callable block that performs meaningful work on inputs; Java calls it a method. Modularity gives smaller pieces clear responsibilities that can be managed and checked. Reusability lets callers invoke that responsibility again.

The picture on M006 p.43 sends apples through function `h` and produces sliced apples. Separating input, processing, and output helps distinguish the caller's preparation of input from the calculation assigned to the method.

[Computer Programming M006, PDF pp.44–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) declares three arrays together:

```java
double[] arr1 = {1.2, 3.4, 2.5, 6.4},
         arr2 = {5.2, 6.7, 8.2, 3.6},
         arr3 = {0.2, 3.4, 4.5, 4.2};
```

The leading `double[]` type applies to all three comma-separated declarators. Each variable refers to a separate array created by its own initializer; the final semicolon ends one declaration. The commas do not combine them into a two-dimensional array. At [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:28:34]], the lecturer explains the syntax and then discourages the compressed style. That is a readability preference, not a syntax prohibition.

### Defining the average calculation once

The repeated version resets `sum = 0` for each array, accumulates its elements, and divides by its length. M006 p.46 extracts that work into a method, giving each call its own local sum:

```java
static double average(double[] arr) {
    double sum = 0;
    for (double f : arr) {
        sum += f;
    }
    return sum / arr.length;
}
```

This method definition belongs inside a class. When a caller invokes `average(arr1)`, the reference value from arr1 becomes the parameter `arr`, and the method returns the calculation's result. `System.out.println(average(arr1));` is a separate caller action that prints the returned value.

| Input array | Mathematical sum | Sum ÷ length |
| --- | ---: | ---: |
| `arr1` | 13.5 | 3.375 |
| `arr2` | 23.7 | 5.925 |
| `arr3` | 12.3 | 3.075 |

All three arrays have length four. These are mathematical values; floating-point representation can introduce small discrepancies. The original method provides no validation contract for null or empty input. Its use with the supplied non-null, nonempty arrays is not a safety guarantee for every input.

The emphasis at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:30:30–01:33:21]] is on meaningful responsibilities and names such as `average` or `sum`, not arbitrary bundles of statements. The meaning of `static` was deferred there and is developed in [[courses/computer_programming/units/en/objects-references|class and instance membership]].

## Reading a declaration as an input and result contract

A method declaration tells its user what inputs and result to expect:

```java
public static int intPlusFloat(int i, float f) {
    return i + (int) f;
}
```

On M006 p.49, `public` specifies access, `static` associates the method with the class, `int` is the return type, and `intPlusFloat` is the name. The parentheses contain parameter types and names, `int i` and `float f`. The name alone does not promise a sum preserving the fractional part.

The return expression first casts `f` to `int`, then adds integers. For explanatory inputs `i = 2, f = 3.7f`, the cast yields 3 and the method returns 5, not 5.7. The cast changes the value used in the expression, not the declared type of `f`. This calculation expands the declaration/body connection discussed at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:34:19]].

### Four combinations of parameters and returns

| Source method | Input | Value delivered to caller | Observable action |
| --- | --- | --- | --- |
| `add(int i, int j)` | Two `int` values | Their `int` sum | Returns the sum |
| `printInt(int i)` | One `int` | None: `void` | Prints the input |
| `getSpecialValue()` | None | `int` value 777 | Returns a fixed value |
| `printMyName()` | None | None: `void` | Prints a fixed String |

The personal-name literal in the last example is unnecessary to explain its role. **Output and return are different channels**: a void method may still have observable effects. M006 pp.50–51 and [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:35:20]] distinguish these four forms.

A return ends the current method's execution. A path that returns a value normally must provide a value compatible with the declared return type. A void method may reach its end or exit earlier through `return;`. The introductory demand for a return should not be treated as a complete rule for every possible flow, including infinite loops and abnormal termination.

Optional exam enrichment sharpens the distinction between the whole declaration and the method signature. For the non-generic methods here, a signature consists of the name and **ordered parameter types**. In `intPlusFloat(int, float)`, parameter names `i` and `f` and actual argument values are not signature components; neither is the return type `int`. The return type nevertheless remains essential to the method's contract. The 2026-1 source is a recollection with explicit order/accuracy limitations and no official answer key, not evidence of a current lecture exam promise or a complete verified paper. [EX:cp_2026_1_final_q01a p.1]

## Following arguments to a returned value

An argument is a value supplied at a call; a parameter is the variable receiving it inside the method. M006 p.52 shows a returned value being stored and then printed:

```java
class Main {
    static float interpolate(float x1, float x2, float r1, float r2) {
        return (r2 * x1 + r1 * x2) / (r1 + r2);
    }

    public static void main(String[] args) {
        float intrp = interpolate(0f, 3f, 1.5f, 2.5f);
        System.out.println(intrp);
    }
}
```

Matching arguments in order gives `x1 = 0f`, `x2 = 3f`, `r1 = 1.5f`, and `r2 = 2.5f`. The expression becomes (2.5×0 + 1.5×3)/(1.5+2.5)=4.5/4=1.125. That float is returned, stored in `intrp`, and printed. The lecturer skips the formula's meaning and derivation at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 01:38:59]], so this is a **materials-based arithmetic trace**. It does not establish a valid-input contract covering a zero denominator.

### Declaration order differs from call order

On M006 p.53, `first()` calls `second()` declared below it, and `second()` calls `third()`:

```java
class Main {
    void first() { second(); }
    void second() { third(); }
    void third() { System.out.println("third"); }
}
```

Declaring this class alone prints nothing. When `first()` is called on an appropriate object, execution follows first → second → third, prints `third`, and returns through its callers. A method's later textual position in the same class does not prevent the call. The lecture's use of “nested” concerns calls between methods, not syntax for declaring another Java method inside a method body.

## Key Takeaways

- Several declarators in one declaration may still refer to separate arrays.
- A method provides a reusable responsibility; its caller may print or further use the result.
- Return type matters to the contract, while current non-generic signatures contain the name and ordered parameter types.
- Read cast positions and actual calls; declaration order is not execution order.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Three arrays and reuse

Explain the type, commas, semicolon, and arrays in `double[] arr1={1.2,3.4,2.5,6.4}, arr2={5.2,6.7,8.2,3.6}, arr3={0.2,3.4,4.5,4.2};`. Why extract average calculation?

<details><summary>Show solution</summary>

The double[] type applies to all three declarators; commas separate names/initializers and the semicolon closes one declaration. Each variable refers to its own array, not one 2D array. Disliking this compact style is not a syntax prohibition. Extracting average gives one body to maintain/test and reuse for different inputs. Modularity separates meaningful responsibilities; reusability invokes that responsibility again.

**Checking points:** Explain multiple declarators as well as the reason for reuse.

</details>

#### Recall Q02 · Returning averages and caller output

For each Q01 array, accumulate from sum=0 and return sum/arr.length. Give sums/mathematical means, per-call initialization, who prints, and input limits.

<details><summary>Show solution</summary>

The sums are 13.5,23.7,12.3 and division by four gives 3.375,5.925,3.075. A fresh local sum starts at zero each call, preventing cross-call accumulation. The method returns; the caller's println prints, leaving the value reusable elsewhere. Floating-point representation may differ slightly from the mathematical values. The examples assume non-null, nonempty inputs without a validation contract for others.

**Checking points:** Check all sums/means, reset, return/printing, and input assumptions.

</details>

#### Recall Q03 · Four input/return combinations

Classify add(int,int), printInt(int), getSpecialValue(), and printMyName() by inputs, return type, and behavior. Explain public/static and termination by return.

<details><summary>Show solution</summary>

`add` accepts two ints and returns their int sum; printInt accepts an int and prints with void return; getSpecialValue takes no input and returns int 777; printMyName takes no input and prints a fixed String with no return value. `public` specifies access and static class membership. `return` ends the current method; value-returning paths must match its declared type. `void` methods may reach their end or use return;. Printing is separate, and the introductory rule is not a blanket statement about infinite/abnormal paths.

**Checking points:** Separate all four forms and printing from return.

</details>

#### Recall Q04 · The effect of cast position

Evaluate `public static int intPlusFloat(int i,float f){return i+(int)f;}` at i=2,f=3.7f. How do name, return type, and body inform the result?

<details><summary>Show solution</summary>

Cast f to int 3 first, then add int 2 to return 5. The name alone does not promise 5.7; int return type and the cast show that the fraction is not preserved. The declared type of f remains float; only the expression's value is converted.

**Checking points:** Keep cast→addition→return order and f's declared type.

</details>

#### Recall Q05 · Arguments and result flow

Trace interpolate(0f,3f,1.5f,2.5f), returning `(r2*x1+r1*x2)/(r1+r2)` into intrp. Explain parameter matching, calculation, storage/output, and scope.

<details><summary>Show solution</summary>

Ordered matching gives x1=0,x2=3,r1=1.5,r2=2.5. Numerator 2.5×0+1.5×3=4.5 and denominator four yield float 1.125, stored in intrp and printed afterward. Arguments are supplied values; parameters receive them inside the method. This is materials-based arithmetic, not the skipped interpolation derivation or a contract permitting a zero denominator.

**Checking points:** Check all four bindings, 4.5/4, and return/storage/output.

</details>

#### Recall Q06 · Declaration versus call order

A class defines first→second→third calls and only third prints "third". Compare declaring the class with invoking first on an appropriate object. May second be declared later?

<details><summary>Show solution</summary>

Declaration alone prints nothing. Calling first follows first→second→third, prints third once, and returns through the callers. Later declarations in the same class can be called, so textual order is not execution order. The lecture's nested wording concerns calls, not declaring a method inside another method body.

**Checking points:** Distinguish declaration from invocation and explain call/return order.

</details>

### Apply the ideas

#### Practice P01 · Compare signature and computation

**Newly written synthetic exam-style practice.** Transfer signature-component reasoning from [EX:cp_2026_1_final_q01a p.1]. Prerequisites are the current non-generic declaration, parameter, return, and cast concepts. The recollection has no official key; overload selection is not asked.

Compare independent examples A `int blend(int i,float f){return i+(int)f;}` and B `double blend(int count,float amount){return count+amount;}` in signature and computational contract. Also evaluate A with (2,3.7f).

<details><summary>Show solution</summary>

Both signatures are `blend(int,float)`: parameter names and return type are not signature components, though they matter to the contract. A casts f before addition and returns 5. B returns a mixed numeric sum without that cast as double, so its computation differs and floating-point approximation matters. These are independent comparison examples, not instructions to combine both in one class. Matching signature information does not establish identical bodies or results.

**Checking points:** Explain same signature, different body contract, and A's result five.

</details>

### Review plan

Explain declaration/average behavior in Q01–Q02, then compare Q03's four contracts. Trace Q04–Q06 and use P01 to separate signature identity from body meaning.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 01:30:30, 01:28:34, 01:33:21, 01:35:20, 01:34:19, 01:38:59.

### Materials and page views

- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-044), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-053).

The average example supplies no validation contract for null/empty inputs. Interpolation's derivation was skipped; only the given arithmetic is traced here. Detailed static semantics were deferred on September 8 and follow in the objects unit.

Exam connection: P01 extends signature-component reasoning from [EX:cp_2026_1_final_q01a p.1] into comparing declarations and bodies. This recollection warns about order/accuracy and has no official key. Its duplicated (f), incomplete queue statement, and empty (i) are not reconstructed.


---

[[courses/computer_programming/units/en/control-flow|← Previous: Boolean Conditions, Branching, Loops, and Execution Tracing]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/objects-references|Next: Objects, Constructors, Static Members, and Reference Passing →]]
