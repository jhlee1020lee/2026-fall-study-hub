---
title: "Docker Lab Environment and CPU Assignment Specifications"
description: "Interpret Docker preparation and Lab1 specifications without filling missing implementation details."
course: "computer_architecture"
unit_id: "lab-environment-specification"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Docker Install.pdf", "Lab 0 1.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-29-lecture-05"]
---

Read environment preparation, instruction implementation, and submission requirements separately. Identify the setup stages and the information the worksheet asks you to express.

## Docker containers and the lab-environment boundary

Preparing the lab environment differs from implementing CPU instructions. Lab0 prepares tools and the project environment; Lab1 implements instruction behavior according to a specification. The September 29 briefing says all labs use Docker containers and recommends VSCode with the Dev Containers extension. A CLI route is also available for users familiar with Docker, with details referred to `assignment-0.md`. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 56:40]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 57:31]] [CA NM004 PDF p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-002) [CA NM004 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-003) [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]

Opening files in an editor does not itself establish a connection to the container environment. The material's progression is Docker preparation → archive extraction → opening the resulting folder → container build and connection.

The archive in [CA NM004 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004) is named `dinocpu-lab1.tar.gz`, with this extraction example. Commands below are examples read from instructor documentation, not commands executed while producing this text.

```sh
tar -xzf dinocpu-lab1.tar.gz
```

The material says extraction creates `dinocpu/`. The screenshot in [CA NM004 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005) highlights **Reopen in Container** in VSCode's lower-right corner. After opening the `dinocpu` folder, that choice lets VSCode build and connect to the container. Distinguish opening a folder, building a container, and connecting to its environment when interpreting setup state.

Lab0 is described as introducing Chisel and linking to the `first-hardware.md` tutorial. Following the tutorial is optional preparation for students unfamiliar with Chisel, and Assignment0 requires no submission. [CA NM004 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006) The supplied material does not include the archive contents, `assignment-0.md`, or `first-hardware.md`. It therefore does not establish specific Chisel syntax, build/test commands, or successful installation. Archive names and “Chisel” use the document's spelling rather than silently reconstructing unclear spoken names.

## Reading the operating-system routes separately

The detailed sequences below are **materials-based review of Docker Install**. They are not a claim that every OS-specific command was explained orally on September 29, nor newly verified instructions for current product UI, the latest version, or the reader's installed state. The different OS routes are alternatives, not one sequence to execute in full.

### Moving from Windows through WSL to Ubuntu

[CA NM003 PDF p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001)–[CA NM003 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003) first enable **Windows Subsystem for Linux** through Windows features, then reboot and use administrator PowerShell for:

```powershell
wsl --install
wsl --set-default-version 2
```

The first installs WSL; the second selects version 2 as the default. The material next enables **Dev › Containers: Execute In WSL** in the VSCode Dev Containers extension's Settings. The following PowerShell command enters an Ubuntu shell, where the document's Ubuntu steps continue:

```powershell
wsl
```

The subsequent context is an Ubuntu shell. Beginning in Windows PowerShell does not make every later Linux command part of the same shell syntax.

### Docker Engine and execution checking on Ubuntu

[CA NM003 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004) places a Docker Engine installation-script pipeline beside a command adding the current user to the docker group.

```sh
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

The first is the source document's download-and-install pipeline; the second changes user-group membership. The document says the script can print a warning and wait about twenty seconds under WSL. After the group change, close and reopen the shell; on the WSL route, enter again with `wsl`, then check container execution:

```sh
docker run hello-world
```

This final command checks whether a container can run in the environment. Here, only the source sequence and command roles have been read; no download, installation, execution, or successful result is claimed.

### Two Mac alternatives and version output

Option 1 in [CA NM003 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005)–[CA NM003 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006) selects Docker Desktop for the appropriate Apple or Intel chip, moves `Docker.app` from the `.dmg` into Applications, launches it, and checks the menu-bar whale icon. It then reads the version with:

```sh
docker --version
```

The example output, `Docker version 28.0.1, build xxxxxxx`, illustrates output form. It does not designate the current latest or required lab version.

Option 2 is an alternative Homebrew installation route, followed by launching the app, checking the icon, and checking the version. [CA NM003 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)

```sh
brew install --cask docker
```

Page 7 visibly uses an em dash in `docker —version`, whereas page 6 uses two ASCII hyphens in `docker --version`. Distinguish these characters. The command block above uses page 6's spelling rather than silently rewriting page 7 as a quotation.

## R/I arithmetic and the assignment specification

The actual Lab1 notice specifies **only R-type and I-type arithmetic/logic instructions**. This is more specific than the R-type description in the September 1 plan. It does not require every instruction with an I-type encoding, such as all loads. [CA NM004 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-007) [CA NM004 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 58:36]]

Some CPU control signals are defined differently from the classroom examples, so the specification in `assignment-1.md` governs the implementation. Understanding the concept of selecting an ALU input differs from choosing the assignment's exact control bit pattern. Copying a classroom truth table can produce the wrong behavior even when names look familiar. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 59:36]]

The supplied bundle lacks `assignment-1.md`, the starter archive, and tests. Exact signal encodings, TODOs, permitted implementation-file changes, and a completed implementation cannot be inferred from this briefing. The original worksheet does, however, establish the kinds of information the drawing must express.

### Classifying worksheet ports as indices, data, and control

[CA NM004 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009) is an unwired worksheet, not a completed circuit. It places PC, Next PC, Control Unit, ALU Control, Instruction Memory, Register File, ALU, and Immediate Generator separately, with a supplied `select 32 bits` block.

| Port or block in the figure | Information to distinguish |
|---|---|
| Register File `readreg1/readreg2`, `writereg` | Indices identifying registers |
| `readdata1/readdata2`, `writedata` | Values produced or accepted by selected registers |
| `wen` | Control permitting a register update |
| ALU `inputx/inputy`, `operation`, `result` | Two operands, operation selection, and result |
| Immediate Generator `instruction → sextImm` | Extended immediate derived from instruction fields |
| Next PC `pc`, `imm`, `inputx/inputy`, `funct3`, `branch`, `jumptype` | Address, condition, and selection information |

Control Unit receives the opcode and exposes `itype`, `aluop`, `src1/src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, and `wordinst`. ALU Control receives `aluop/itype/funct7/funct3/wordinst` and selects `operation`. These names help identify information roles; they do not by themselves specify encodings or truth tables.

The worksheet requires drawing the wires and any muxes needed for R/I execution, labeling every wire's width and any partial bit slice. For example, `instruction[19:15]` contains $19-15+1=5$ bits. It differs from the full 32-bit instruction and from the data width of the register selected by that index. A slice label communicates **which information and how many bits flow**, beyond merely showing a connection. The worksheet also says not every module or port may be needed. This explains how to read the diagram without supplying the completed wiring or mux solution.

[CA NM004 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008) and September 29 59:36 require submitting the completed worksheet. [CA NM004 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-010) records the then-issued deadline as 10/12 23:59 at eTL and describes one compressed file, code-only submission, and exclusion of debugging/test files from grading. This is the source-dated notice, not a live schedule check. The exact packaging relationship between the mandatory worksheet and code-only archive is not supplied, so it should not be invented. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 01:00:30]] Distinguishing concepts, environment preparation, and submission specifications prevents a working tool setup from being mistaken for a finished implementation or completed submission.

## Key Takeaways

- Opening a folder, building a container, and connecting to it are different states.
- Windows/WSL, Ubuntu, and Mac routes are alternatives, not one combined installation sequence.
- Lab1 covers R/I arithmetic/logic; exact control encodings come from its specification.
- Read register indices, data, control, and bit slices as distinct information.

## Recall and Practice

### Recall the reasoning

#### Recall Q01 · Lab0 preparation stages

Explain Docker, Dev Containers, `dinocpu-lab1.tar.gz`, `dinocpu/`, Reopen in Container, and the Chisel tutorial in sequence. Does Lab0 require submission?

<details><summary>Show solution</summary>

The material prepares Docker, extracts `dinocpu-lab1.tar.gz` with the documented `tar -xzf` example, opens resulting `dinocpu/` in VSCode, then uses Dev Containers' Reopen in Container to build/connect. Opening the folder alone does not prove connection. Experienced Docker users have a CLI alternative referenced in `assignment-0.md`. Lab0 introduces Chisel and optional `first-hardware.md`, with no submission. Those documents/archive contents are absent, so specific syntax, build/test commands, and actual success are not established. This explains documented command roles.

**Checking points:** Check optional tutorial/no submission and distinguish folder, build, connection.

</details>

#### Recall Q02 · From Windows to Ubuntu

Explain the WSL feature, reboot, administrator PowerShell, VSCode setting, and `wsl` in the Windows route. What roles do Ubuntu installation, group changes, reopening the shell, and the execution check serve? Interpret the document; do not execute commands.

<details><summary>Show solution</summary>

The sequence is enable Windows Subsystem for Linux→reboot→administrator PowerShell `wsl --install` and `wsl --set-default-version 2`→Dev Containers setting Dev › Containers: Execute In WSL→enter Ubuntu with `wsl`. The Docker Engine script pipeline installs; `sudo usermod -aG docker $USER` changes group membership; reopening the shell uses the updated environment; `docker run hello-world` checks container execution. A warning/~20-second wait under WSL is documented behavior in the material. Subsequent Linux commands are not all PowerShell commands, and reading this sequence proves no installation success.

**Checking points:** Check the shell transition and distinct roles of all four Ubuntu stages.

</details>

#### Recall Q03 · Mac alternatives and version examples

Compare Mac options 1 and 2 through installation, launch, and checks. Interpret example version 28.0.1 and `docker —version` versus `docker --version`.

<details><summary>Show solution</summary>

Option1 selects Docker Desktop for Apple/Intel, moves `Docker.app` from `.dmg` to Applications, launches it, checks the whale icon, then version output. Option2 uses `brew install --cask docker` as an alternative, followed by app/icon/version checks. They are not consecutive required installations. Version 28.0.1 illustrates output form, not a latest/required version. The p.7 em dash differs from p.6's two ASCII hyphens; distinguish the source spellings.

**Checking points:** Include alternative routes, example-version status, and the dash discrepancy.

</details>

#### Recall Q04 · Lab1 scope and specification

Does R/I arithmetic/logic mean every I-type instruction? Explain the roles of classroom control tables, `assignment-1.md`, and the required worksheet, including missing information.

<details><summary>Show solution</summary>

Loads can be I-type, so format alone cannot expand assignment scope. The notice specifies R/I arithmetic/logic and warns that some controls differ; the assignment specification governs implementation. The worksheet is required, but absent `assignment-1.md`, starter, and tests leave exact control bits, TODOs, allowed files, and implementation unspecified. Page10's 10/12 23:59, one archive, code-only submission, and exclusion of debug/test files are source-dated notices. The worksheet/archive packaging relationship is not resolved by the supplied material.

**Checking points:** Respect the scope and worksheet requirement without inventing missing specifications.

</details>

#### Recall Q05 · Port information and bit slices

Classify Register File, ALU, Immediate Generator, and Next PC ports by information role. Explain Control Unit/ALU Control, the width of `instruction[19:15]`, and worksheet wire/mux requirements.

<details><summary>Show solution</summary>

`readreg1/readreg2/writereg` are indices; `readdata1/readdata2/writedata` are data; `wen` enables writing. ALU `inputx/inputy` are operands, `operation` a selection, `result` the computed value. The generator maps instruction→`sextImm`; Next PC's `pc/imm/inputx/inputy/funct3/branch/jumptype` distinguish addresses, conditions, and selection. Control Unit maps opcode to `itype/aluop/src1/src2/branch/jumptype/resultselect/memop/toreg/regwrite/validinst/wordinst`; ALU Control uses `aluop/itype/funct7/funct3/wordinst` to choose operation. Names alone do not specify encodings. `[19:15]` has five bits, distinct from the full 32-bit instruction or selected data width. The worksheet requires necessary wires/muxes and all widths/partial slices, not mandatory use of every port. Its `select 32 bits` block is part of the blank diagram.

**Checking points:** Check 5=19−15+1 and distinguish information roles from a completed wiring solution.

</details>

### Apply the ideas

#### Practice P01 · Evidence needed for completion claims

Newly written lecture/material-based general practice. A student claims: 'The folder opens and a version string appears, so Lab1 inside the container is finished. I can copy classroom control bits and connect every port.' Evaluate environment and specification claims separately and identify the evidence still needed.

None of the 18 exam candidates tests Docker/WSL, Dev Containers, current lab scope, or worksheet reading. Q14's hypothetical ISA extension provides no authority for a current-lab implementation.

<details><summary>Show solution</summary>

An open folder and version output establish file access and version information, not container build/connection, implementation, validation, or submission. Assignment controls may differ, and the worksheet explicitly permits unused ports. The actual specification, starter, and tests are needed to establish scope, encoding, and validation criteria; the present material cannot fill those gaps. Keep the required worksheet distinct from the unresolved archive-packaging detail.

**Checking points:** Separate environment, implementation, validation, and submission, naming the missing specification evidence.

</details>

### Short review plan

Explain the documented route relevant to your OS using Q01–Q03, then check specification scope with Q04–Q05. In P01, separate established state from evidence still needed.

## Sources

- [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 lecture notes]]
- [Docker Install.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Docker.Install.pdf) — [p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001), [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)
- [Lab 0 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Lab.0.1.pdf) — [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-002), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-010)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 corrected transcript]] — 56:40, 57:31, 58:36, 59:36, 01:00:30 (plain timestamps within the page)

September 29 confirms Docker, VSCode/CLI options, and lab scope. OS-specific installation details are materials-only, not current UI or installation-success verification. `assignment-0.md`, `first-hardware.md`, `assignment-1.md`, the starter archive, and tests are absent. Exact TODOs, control encodings, completed wiring, and implementations therefore remain unspecified. The deadline is source-dated; the packaging relationship between the required worksheet and code-only archive is unresolved.

Exam connections are limited to a Fall 2025 reconstruction whose official wording and answers are not independently verified. No supplied answer is adopted as verified, and historical grading rules or appearance predictions are not transferred to this term.
