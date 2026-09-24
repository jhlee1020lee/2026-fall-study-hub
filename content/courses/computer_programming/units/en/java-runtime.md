---
title: "Programming Goals and the Java Execution Environment"
description: "Review programming verification and the path from Java source to IDE execution."
course: "computer_programming"
unit_id: "java-runtime"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 1 Introduction.pdf", "Lecture 2 Java Basics 1.pdf", "Lab01.pdf", "Lab02 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/en/2026-09-01-lecture-01", "courses/computer_programming/lectures/en/2026-09-03-lecture-02", "courses/computer_programming/lectures/en/2026-09-08-lecture-03", "courses/computer_programming/lectures/en/2026-09-10-lecture-04", "courses/computer_programming/lectures/en/2026-09-15-lecture-05"]
---

Turn programming goals into checkable requirements and distinguish Java compilation from execution. Diagnose failures through tool paths, filenames, and launch targets.

## Programming and verifiable behavior

Programming turns a desired outcome into executable work and checks whether that work meets its purpose. Start by defining inputs, outputs, and constraints. Decompose the work, implement it, and compare its behavior with those requirements. Terminating successfully or producing one correct answer does not by itself establish reliable computational behavior. Boundary inputs, execution time, memory and CPU use, errors, and unintended behavior also matter.

In the [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 transcript]], 12:22–13:03, the lecturer separates implementation from verification: even when another programmer or an AI helps produce code, checking that it satisfies the goal remains necessary. Asking a precise question about a function or an overall design can help, but the resulting code still needs to be read and explained.

Maintenance concerns the ease of later changes; efficiency concerns resource use; readability concerns how readily a reader can understand intent. Meaningful names and useful divisions of responsibility support all three. The emphasis on memory, CPU, and compiler behavior at [[courses/computer_programming/transcripts/2026-09-08|2026-09-08, 53:25]] serves the same purpose: understand what changes when a statement executes, rather than recognizing only its surface syntax.

## From Java source to JVM execution

Java source and its executable representation are different. The compiler `javac` translates a `.java` source file into Java bytecode stored in a `.class` file. The JVM, or Java Virtual Machine, executes that bytecode. The two commands therefore perform different stages:

```text
javac HelloWorld.java
java HelloWorld
```

The first compiles the source; the second requests execution of the `HelloWorld` class. A `.class` file is not an operating-system-native executable. A JVM for the target platform handles platform-specific execution, giving the course's model of common bytecode running on different systems. Lab01's introductory description of an “executable file” must be read within this bytecode model. [Java Basics 1, PDF pp.7–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)

Distinguishing the JVM, JRE, and JDK explains why development requires more than execution support.

| Component | Role in the course's model |
| --- | --- |
| JVM | Executes bytecode |
| JRE, Java Runtime Environment | Combines the JVM with Java package classes |
| JDK, Java Development Kit | Adds development tools to the execution environment |

The [[courses/computer_programming/transcripts/2026-09-03|2026-09-03 transcript]], 02:20, explains this containment relationship. A developer needs compilation tools as well as the ability to run a program. This is a conceptual distinction, not a claim that every present-day distribution packages these components identically. Mobile and web applications, servers, games, and database connections are introductory examples of Java's uses.

## The structure and entry point of `HelloWorld`

Java Basics 1 begins with this program:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
```

The `class` keyword begins a class definition, and `HelloWorld` is its name. Save this public class in `HelloWorld.java`. Saving it in `Hello.java` produces the filename diagnostic shown in the material. PascalCase is a naming convention; matching this public class name to its filename is an enforced rule in the supplied compilation model.

Here `main` is the entry point of the standalone example. `public` permits access, `static` associates the method with the class, `void` declares no return value, and `String[] args` declares a String-array parameter. Braces delimit the class and method bodies; a semicolon ends the printing statement. This does not mean every class must have its own `main`. The relationship between static members and objects is developed in [[courses/computer_programming/units/en/objects-references|Objects and references]].

`System.out.println` calls `println` through `System.out`, prints its argument, and ends the line. Console output and returning a value to a caller are separate actions, so a `void` method can print. The explanation at [[courses/computer_programming/transcripts/2026-09-15|2026-09-15, 40:13]] likewise separates `void`, the method name, and the String-array input.

Comments separate explanatory text from executable statements. `//` starts a comment extending to the end of the line; `/*` and `*/` delimit a block comment. Comments can explain intent or constraints that names alone do not convey. When a comment and a literal differ, the literal determines what the program prints. The program above prints `Hello, world!`, including that capitalization and comma.

## Connecting the JDK to an IDE

Understanding the execution stages makes environment problems easier to isolate. [Lab01](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf) presents selecting a JDK for the OS and CPU architecture, checking installation, writing source, compiling, and running. `java -version` identifies the Java command resolved by the current shell; it does not also establish that the source and compiler configuration are correct.

For a command that cannot be found on Windows, the material adds the JDK's `bin` directory to `Path` and reopens PowerShell. On Mac, installation is followed by a version check in Terminal. Showing filename extensions helps avoid saving `HelloWorld.java.txt`. Compilation is performed from the directory containing the source. The command discussed at [[courses/computer_programming/transcripts/2026-09-03|2026-09-03, 08:06]] belongs to this sequence. These are historical course procedures: the specified 11.0.32.1 and the Mac screenshots showing 16.0.2 and 11.0.16.1 are different version evidence, not one consistent installation state.

An IDE, or Integrated Development Environment, combines an editor, compilation support, and a debugger. The IntelliJ example creates a Java project, selects a JDK, places a `HelloWorld` class under `src`, and selects its main class in an Application run configuration. The Run window displays the result. A configuration's display name is separate from the selected main class. The IDE connects compilation and execution conveniently; it does not replace their underlying meaning.

| Observed problem | Stage to distinguish first |
| --- | --- |
| `java` cannot be found | Installed tools and the shell's search path |
| Filename ends in `.java.txt` | Source filename and extension |
| Public class and filename differ | Compilation and name checking |
| A different main class runs | IDE launch target |
| Expected output is not visible | Execution status and the Run output window |

Lab02 also supplies a license-activation correction without requiring reinstallation. Its historical menu sequence is Help → Manage Subscriptions… → Log in to JetBrains Account → Activate → restart. Account registration, software installation, and license activation are separate checks. [Lab02, PDF pp.3–5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf)

## Key Takeaways

- One correct output does not verify boundary inputs, resources, or error behavior.
- `javac` produces bytecode; a platform-specific JVM executes it.
- Distinguish return values from output, and naming conventions from filename rules.
- An IDE connects the JDK, source, and main class for compilation and execution.

## Recall and Practice

### Explain and trace

#### Recall Q01 · One correct result

AI-generated code passes an example. Explain three programming stages, further verification, and the roles of readability, maintenance, and efficiency.

<details><summary>Show solution</summary>

Define inputs, outputs, and constraints; decompose and implement; compare behavior with requirements. Check other and boundary inputs, time/memory/CPU limits, errors, and unintended behavior. Readability helps explain state changes, maintenance concerns later changes, and efficiency concerns resources. AI authorship removes none of these checks.

**Checking points:** Distinguish the three stages, input/resource checks, and three quality criteria.

</details>

#### Recall Q02 · Compiler and JVM

Explain compilation/run commands and results for `HelloWorld.java`; distinguish JVM/JRE/JDK and `.class` from a native executable.

<details><summary>Show solution</summary>

`javac HelloWorld.java` produces `.class` bytecode; `java HelloWorld` requests execution through the target JVM. The file is not an OS-native executable. In the course model, the JRE contains the JVM and Java package classes, while the JDK adds development tools. Platform-specific JVMs handle execution differences; this model does not fix current distribution packaging.

**Checking points:** Explain each command's stage and each component's role.

</details>

#### Recall Q03 · Reading main and output

What happens if `public class HelloWorld` is saved in `Hello.java`? Explain `public static void main(String[] args)`, `System.out.println("Hello, world!");`, comments/braces, and conventions versus rules.

<details><summary>Show solution</summary>

The filename mismatch causes a compilation error; use `HelloWorld.java`. PascalCase is a separate convention. `public` specifies access, `static` class membership, `void` no return value, `main` this example's entry point, and `String[] args` a String-array parameter. Braces delimit class/method bodies; the semicolon ends the statement. `//` comments to line end; `/* ... */` encloses a comment. `println` through `System.out` prints `Hello, world!` and a newline. Output is separate from return, and not every class needs main.

**Checking points:** Preserve capitalization/comma and distinguish output from return.

</details>

#### Recall Q04 · Classifying setup problems

Distinguish missing `java`, a `.java.txt` file, a wrong main class, and inactive licensing. How does an IDE connect manual execution stages?

<details><summary>Show solution</summary>

The first concerns installation/shell lookup; the historical procedure adds JDK bin to Path and reopens the shell. The second concerns extension, the third the run configuration's target rather than display name, and the fourth account/license activation separately from installation. Lab02 describes activation and restart. Manual work compiles in the source directory and executes the class. An IDE connects the project JDK, source class, and main class and shows output in Run. A successful version check alone does not verify source/compiler settings.

**Checking points:** Separate all four problems and retain compile/run stages inside the IDE.

</details>

### Apply the ideas

#### Practice P01 · Design a diagnostic sequence

**Newly written lecture-based general practice; no direct indexed exam match.** A version check works, but the file is `HelloWorld.java.txt` and the IDE runs another class. Explain checks and their evidence before accepting a colleague's reinstall proposal.

<details><summary>Show solution</summary>

Show extensions and verify `HelloWorld.java` matches the public class. In the source directory, use the result of `javac HelloWorld.java` to assess compilation and `java HelloWorld` to assess that class's execution. Check the IDE's project JDK and main class, then compare Run output. Finally verify literal output and input/boundary requirements. Version lookup, translation, execution, and behavior each establish different facts. The evidence does not show that reinstallation fixes the filename and target errors.

**Checking points:** Address both observed causes and what each check can establish.

</details>

### Review plan

State the criteria in Q01, then explain Q02–Q03 without notes. For Q04 and P01, mark which stage each observation actually checks.

## Sources

### Dated lectures and transcripts

- [[courses/computer_programming/lectures/en/2026-09-01-lecture-01|2026-09-01 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-03-lecture-02|2026-09-03 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-08-lecture-03|2026-09-08 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-10-lecture-04|2026-09-10 · Computer Programming lecture and sources]]
- [[courses/computer_programming/lectures/en/2026-09-15-lecture-05|2026-09-15 · Computer Programming lecture and sources]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 corrected transcript]] — 12:22–13:03.
- [[courses/computer_programming/transcripts/2026-09-03|2026-09-03 corrected transcript]] — 02:20, 08:06.
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 corrected transcript]] — 53:25.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 corrected transcript]] — 00:47.
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 corrected transcript]] — 40:13.

### Materials and page views

- [Lecture 1 Introduction.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/1.intro.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-004), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-008).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-009), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-013), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-015), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-020), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-024).
- [Lab01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf) — [PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=8), [PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=29), [PDF p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=63).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-005).

The specified 11.0.32.1 and Mac screenshots showing 16.0.2/11.0.16.1 are distinct historical evidence. Installation, account, and license steps are historical examples, not verified current instructions. Transcript uncertainties remain.


---

[[courses/computer_programming/units/index|Unit contents]] · [[courses/computer_programming/units/en/types-expressions|Next: Variables, Types, Operators, and Strings →]]
