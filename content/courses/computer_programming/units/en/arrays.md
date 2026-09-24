---
title: "Array Creation, References, and Multidimensional Data"
description: "Check array creation, defaults, indices, ragged rows, and String-reference replacement."
course: "computer_programming"
unit_id: "arrays"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["3 java basics 2.pdf", "Lab02 v4.pdf", "Lecture 2 Java Basics 1.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-08-lecture-03", "courses/computer_programming/lectures/en/2026-09-10-lecture-04"]
---

Separate array variables, array objects, and components in your storage model. Following each row's length makes multidimensional access and String-slot replacement predictable.

## Declaring an array and creating its storage

Giving every related value a separate variable name makes storage and traversal awkward. An array groups values of one component type and lets an index select an element. Applying [[courses/computer_programming/units/en/types-expressions|types and references]] also separates an array variable from the array object itself.

```java
int[] arr = new int[4];
```

`int[]` is the variable's type, `arr` is its name, and `new int[4]` creates an array of length four. By contrast, a local declaration `int[] arr;` alone neither creates an array nor assigns a readable reference. Declaration and allocation are different stages. [Computer Programming M006, PDF pp.3–6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf)

Components of a newly created array receive default values: 0 for `int`, 0.0 for `double`, `false` for `boolean`, and `null` for reference components. This is a factual correction to the wording about unguaranteed values at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 37:38–41:21]]. It does not make an unassigned local variable readable.

### An initializer determines values and length

Use an initializer when particular starting values are required:

```java
int[] ages = new int[]{21, 17, 43, 56, 34};
int[] studentAges = {21, 22, 24, 20, 25};
```

Each initializer contains five elements, so each array has length five. The second form is the shortened syntax permitted in a declaration. The material's `new int[3]{14, 13, 12}` is an **invalid example** combining a dimension expression with an initializer. The lecturer's speculation about the design reason for this restriction is not an established language-design explanation.

An `int[]` or `double[]` contains primitive component values; a `String[]` contains String references. Describing array storage as contiguous does not imply that all the Strings' character contents are stored together in that array.

## Indices, length, and element assignment

M006 pp.7–10 introduces indexing with four car names:

```java
String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};
System.out.println(cars[0]); // Volvo
cars[0] = "Opel";
System.out.println(cars[0]); // Opel
System.out.println(cars.length); // 4
```

Indices begin at zero, so the final index of this four-element array is three. Assigning `cars[0]` replaces the reference in its first slot. It neither adds an element nor edits the old String's characters, so the length remains four. An array created with `new int[3]` has length three. Array `length` takes no parentheses, unlike String `length()`.

The separate example in [Lab02 M008, PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) replaces the first slot with `"Hyundai"`. Its outputs are therefore `Volvo`, `Hyundai`, and `4`. Substituting the theory example's `Opel` would change the trace. The relationship between indexing and length is explained at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 42:20]]; the unclear replacement word in the September 10 recording is resolved from the Lab02 material, not from recovered speech.

This traversal visits indices 0, 1, 2, and 3. The strict comparison `i < cars.length` matters: `i == cars.length` is already outside the array.

```java
for (int i = 0; i < cars.length; i++) {
    System.out.println(cars[i]);
}
```

For now, read the loop as starting at zero, increasing by one, and reading while the index is within range. The precise order of checking and updating follows in [[courses/computer_programming/units/en/control-flow|Control flow]].

## Arrays of arrays and two-stage indexing

A Java two-dimensional array is an array whose components refer to other arrays. It need not be rectangular.

```java
int[][] myNumbers = {{1, 2}, {3, 4, 5}};
System.out.println(myNumbers[1][2]); // 5
myNumbers[0][1] = 0;
```

`myNumbers[1]` selects the second inner array, `{3, 4, 5}`. Applying `[2]` selects its third element, 5. The last assignment changes only the first row's second element, from 2 to 0. The first index chooses a row array; the second chooses a component within it. A `char[][] ticTacToe` has the same structure, with outer components referring to `char[]` arrays.

In the diagram on Lab02 M008 p.8, first follow `arr` to the outer array, then follow its three reference slots to the row arrays. Its values are `{{2,7,9},{3,6,1},{7,4,2}}`, making `arr[0][0]` equal to 2 and `arr[1][2]` equal to 1. The arrows show logical reference relationships, not measurable physical address spacing. The explanation at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 48:09]] likewise follows the access one stage at a time.

### Traversal uses each row's own length

M006 p.14 supplies a **different example**. Here the first row has length three and the second has length two:

```java
int[][] myNumbers = {{1, 2, 3}, {4, 5}};
for (int i = 0; i < myNumbers.length; ++i) {
    for (int j = 0; j < myNumbers[i].length; ++j) {
        System.out.println(myNumbers[i][j]);
    }
}
```

The outer length is the number of rows, two. The inner loop uses the length of the current `myNumbers[i]`, printing 1, 2, 3 from the first row and then 4, 5 from the second. A fixed inner bound of two misses 3; a fixed bound of three oversteps the second row. Additional dimensions repeat the same principle of following a reference to the next array.

## Replacing a String-array slot preserves String immutability

Two stages of indexing into a String array select a slot holding a String reference. Changing that slot differs from changing the referenced String's character contents.

```java
String[][] names = {{"Volvo"}};
String old = names[0][0];
names[0][0] = "Opel";
```

This is a **pedagogical reconstruction** connecting the String model on M002 p.48 with array indexing. After the final line, `names[0][0]` refers to `"Opel"`, while `old` still refers to `"Volvo"`. Only the array slot received a new reference; Volvo's characters were not modified.

The exchange at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 52:15–52:47]] concerns this area, but the exact question and the full intention of “String itself to the memory address” remain uncertain. The code above is not a recovered classroom question. The object and memory details deferred there are developed in [[courses/computer_programming/units/en/objects-references|Objects and reference passing]].

## Key Takeaways

- A declaration alone creates no array. Component defaults differ from assignment of a local reference.
- Length n permits indices 0…n−1; slot assignment does not grow an array.
- A 2D array contains row references; use the current row's length for inner bounds.
- Replacing a String slot leaves other references to the old String unchanged.

## Recall and Practice

### Explain and trace

#### Recall Q01 · Declaration, creation, initializer

Distinguish local `int[] a;`, `int[] b=new int[4];`, and `int[] c={21,17,43,56,34};`. Explain why `new int[3]{14,13,12}` is invalid and give other component defaults.

<details><summary>Show solution</summary>

a only declares a reference and needs assignment before reading. b creates four int components, all zero. c creates a length-five array using the five values. Combining a dimension expression with an initializer is invalid; `new int[]{14,13,12}` is a valid form. New double, boolean, and reference components default to 0.0, false, and null. A String[] stores references rather than all character contents. None of these defaults assigns local a.

**Checking points:** Explain creation, lengths/defaults, and why the initializer fix works.

</details>

#### Recall Q02 · Slot changes and length

Starting with the four car names Volvo/BMW/Ford/Mazda, theory replaces slot zero with Opel and Lab02 with Hyundai. Give each before/after value, length, final index, and traversal bound.

<details><summary>Show solution</summary>

Theory gives Volvo→Opel; Lab02 gives Volvo→Hyundai. Both keep length four and final index three; starting at zero with `i<cars.length` visits every slot. Array length has no parentheses, unlike String.length(). Assignment replaces a reference rather than adding an element or editing the old String. A <= bound attempts invalid index four.

**Checking points:** Keep the source replacements distinct and separate length four from index three.

</details>

#### Recall Q03 · Two-stage indexing

For A=`{{1,2},{3,4,5}}`, read A[1][2], then assign A[0][1]=0. Separately, for Lab02 B=`{{2,7,9},{3,6,1},{7,4,2}}`, find B[0][0] and B[1][2]. Explain each indexing stage.

<details><summary>Show solution</summary>

A[1] selects row {3,4,5}, whose element [2] is 5. Assignment leaves A={{1,0},{3,4,5}}. The B reads are 2 and 1. An outer component refers to a row array; the inner index selects that row's value. A char[][] similarly holds char[] references outside, without guaranteeing equal row lengths. Arrows are logical references, not physical spacing.

**Checking points:** Give all reads, the changed component, and the row-reference model.

</details>

#### Recall Q04 · Row lengths and visit order

Traverse `{{1,2,3},{4,5}}` with outer i and inner j. Give both bounds, output order, and the failures caused by fixed inner bounds of two or three.

<details><summary>Show solution</summary>

Use `i<myNumbers.length` for two rows and `j<myNumbers[i].length` for the current row. Restart j at zero per row: visit 1,2,3, then 4,5. Fixed two misses the first row's 3; fixed three attempts nonexistent index two of the second row. Select a row before using its length rather than assuming a rectangle.

**Checking points:** Distinguish a missed value from an out-of-range access.

</details>

#### Recall Q05 · A String slot and an old reference

After `String[][] names={{"Volvo"}}; String old=names[0][0]; names[0][0]="Opel";`, what do the two references reach? Explain immutability and the example's source limit.

<details><summary>Show solution</summary>

names[0][0] reaches Opel and old still reaches Volvo. Two-stage indexing selects a slot that receives a new reference; Volvo's characters are untouched. This is consistent with immutability. The teaching uses a pedagogical reconstruction, not a recovery of the unclear original exchange at 52:15–52:47.

**Checking points:** Separate slot/reference/contents and retain the uncertainty.

</details>

### Apply the ideas

#### Practice P01 · Track only changed slots

**Newly written lecture-based general practice; no direct indexed style match.**
```java
String[][] labels = {{"red", "blue"}, {"green"}};
String old = labels[0][1];
labels[0][1] = labels[1][0];
labels[1][0] = "gold";
```
Give both final rows, old, outer/inner lengths, and the problem with a fixed inner bound of two.

<details><summary>Show solution</summary>

Final rows are {red,green} and {gold}; old remains blue. The first assignment copies the green reference into row zero's second slot. The next changes only row one's first slot, leaving the earlier green reference intact. Outer length two and row lengths two/one are unchanged. A fixed inner bound two accesses missing row-one index one; use that row's length. No String characters were edited.

**Checking points:** Check assignment targets, unchanged lengths, and the invalid index.

</details>

### Review plan

Use Q01–Q02 for creation and length, then draw references and visit order for Q03–Q04. In Q05 and P01, mark only the slots that change.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 37:38, 41:21, 42:20, 48:09, 52:15, 52:47.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 corrected transcript]] — 01:35–03:25.

### Materials and page views

- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-003), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-006), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-010), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-014).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-008).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048).

The theory example replaces the first element with Opel; Lab02 uses Hyundai. The unclear September 10 word remains distinct from the PDF-confirmed value. The exact September 8 question/answer at 52:15–52:47 remains uncertain; the String-slot example is a pedagogical reconstruction.


---

[[courses/computer_programming/units/en/types-expressions|← Previous: Variables, Types, Operators, and Strings]] · [[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/control-flow|Next: Boolean Conditions, Branching, Loops, and Execution Tracing →]]
