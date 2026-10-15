---
title: "Docker Lab Environment and CPU Assignment Specifications"
description: "Questions and worked answers distinguish environment checks from CPU assignment scope, port roles, and bit-width specifications."
course: "computer_architecture"
unit_id: "lab-environment-specification"
lang: "en"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["Docker Install.pdf", "Lab 0 1.pdf", "lab2-slides.pdf"]
private_source_assets: ["lab2-slides.pdf"]
source_lectures: ["courses/computer_architecture/lectures/en/2026-09-29-lecture-05"]
---

## Docker containers and the lab project

CPU design work first requires distinguishing the files being edited from the environment in which the tools run. A **Docker container** provides the lab execution environment. The **dinocpu project** is the collection of design files used in that environment. **VSCode Dev Containers** helps connect the editor to the container. Opening a folder, preparing and connecting to a container, and implementing the CPU are separate steps.

The [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] at 56:40–58:36 describes using Docker containers for the labs, recommends the VSCode path, and allows a CLI path for those familiar with Docker. The preparation and single-cycle discussion connect to the [[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 Computer Architecture lecture notes]]. The detailed sequence below explains the supplied installation and Lab0 materials; it does not certify current product procedures or a successful installation.

The material proceeds from Docker installation to archive extraction, opening the resulting `dinocpu/` folder, and connecting to the container. Its archive-extraction example is: [computer_architecture:NM004 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004).

```sh
tar -xzf dinocpu-lab1.tar.gz
```

This command extracts project files. It does not itself install Docker or run the CPU. After opening `dinocpu/` in VSCode, the next step is **Reopen in Container**, shown at the bottom right of the screenshot in [computer_architecture:NM004 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005). The material explains that VSCode then builds the container and connects to it. Merely seeing files in the editor is therefore not evidence that the container connection has been established.

The CLI details are delegated to `assignment-0.md`. Lab0 covers environment preparation and an introduction to **Chisel**, the language used in the lab. The `first-hardware.md` tutorial is optional preparation for students unfamiliar with Chisel, and the Lab0 tutorial requires no submission. This does not make the subsequent CPU implementation optional. [computer_architecture:NM004 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006). The bodies of those two Markdown documents are not supplied here, so their filenames do not establish build/test commands or particular Chisel syntax.

## Operating-system paths and verification steps

### From Windows through WSL into Ubuntu

The Windows path in the installation material enables **WSL**, Windows Subsystem for Linux, to enter a Linux environment. It first enables Windows Subsystem for Linux in Windows Features and restarts the machine, then uses the following commands in administrator PowerShell. The installation step and the default-WSL-version setting are distinct. [computer_architecture:NM003 p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002).

```powershell
wsl --install
wsl --set-default-version 2
```

The material then enables **Dev › Containers: Execute In WSL** in the VSCode Dev Containers extension settings. Running `wsl` from PowerShell enters the Ubuntu shell, where the Ubuntu procedure continues. [computer_architecture:NM003 p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003). PowerShell and the Ubuntu shell are different command contexts; the presence of a terminal window alone does not identify where a command belongs.

### Ubuntu Engine installation and group membership

The Ubuntu material gives these commands for installing Docker Engine and adding the current user to the docker group. [computer_architecture:NM003 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004).

```sh
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

The first receives a script and passes it to `sudo sh` for installation. The second changes the current user's group membership rather than repeating the installation. The material notes that the script may show a warning and wait approximately 20 seconds under WSL. It then closes and reopens the shell to use the changed environment; the WSL path enters again with `wsl`.

The supplied verification example is:

```sh
docker run hello-world
```

This runs an example container. It checks a different step from simply displaying a version string, but it does not establish that dinocpu builds or that all assignment tests pass.

### Two Mac alternatives and the version example

The first Mac path selects Docker Desktop for Apple or Intel hardware, moves `Docker.app` from the `.dmg` into Applications, and starts the app. It checks the Docker menu-bar icon and then displays version information using the following command. [computer_architecture:NM003 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005); [computer_architecture:NM003 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006).

```sh
docker --version
```

The second path is a Homebrew alternative, not an additional installation step to perform after the first path:

```sh
brew install --cask docker
```

Starting the app and checking the icon and version follow this alternative as well. The displayed `Docker version 28.0.1, build xxxxxxx` illustrates the output format; it does not designate a required or latest version. Page 7 prints `docker —version` with an em dash, whereas page 6 prints `docker --version` with two hyphens. The code above follows page 6. Visually similar characters are not identical command-line option bytes. [computer_architecture:NM003 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007).

Keeping the OS paths separate also clarifies what each check establishes. The version command displays version information, `hello-world` runs that example, and Reopen in Container builds and connects to the project container. None of those observations alone establishes a correct CPU implementation or a successful complete test suite.

## Lab1 instruction scope and the control contract

### Instruction format versus the implemented instruction set

The detailed Lab1 briefing specifies **R-type and I-type arithmetic/logic instructions**, refining the earlier R-type-centered introduction. Read the [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 lecture (computer_architecture:NT001)]] at 58:36 together with [computer_architecture:NM004 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008). Sharing an I-type instruction format does not put every such instruction in the assignment's arithmetic/logic scope. For example, the fact that a load has an I-type format does not include all loads in Lab1.

A **contract** is a concrete agreement the implementation must satisfy: supported instructions, module interfaces, and control meanings. The material explicitly directs students to `assignment-1.md` because some control definitions differ from those in class. The lecture at 59:36 likewise emphasizes implementing to that specification. Remembering that a select value was zero in a lecture diagram does not establish the assignment's encoding. This separates ISA operation semantics from the particular control representation used by the assignment datapath.

### Reading the blank worksheet

[computer_architecture:NM004 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009) is a worksheet for drawing required connections, not a finished datapath. It separately shows PC, Next PC, Control Unit, ALU Control, Instruction Memory, Register File, ALU, and Immediate Generator, as well as a supplied `select 32 bits` block. Before connecting names, identify whether each port represents an **index, a value, or an operation selection**.

| Port or module | Meaning to identify |
|---|---|
| `readreg1`, `readreg2`, `writereg` | Indices selecting registers to read or write |
| `readdata1`, `readdata2`, `writedata` | Values moving into or out of registers |
| `wen` | Permission to perform a register write |
| ALU `inputx`, `inputy`, `operation`, `result` | Operands, operation selection, and result |
| Immediate Generator `instruction→sextImm` | The immediate interpreted from the instruction |
| Next PC | Selection of the next address using current PC and control-flow information |

The Control Unit exposes names including `itype`, `aluop`, `src1`, `src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, and `wordinst`. ALU Control receives `aluop`, `itype`, `funct7`, `funct3`, and `wordinst` and produces `operation`. Next PC lists `pc`, `imm`, `inputx`, `inputy`, `funct3`, `branch`, and `jumptype`. These names identify meanings that need checking; they are not themselves bit encodings or truth tables.

### Label both width and meaning

The worksheet asks for necessary wires and muxes, a width on every wire, and a bit slice where only part of a value is carried. For example, `instruction[19:15]` includes both endpoints, so its width is 19−15+1=5 bits. A five-bit index represents 2^5=32 register numbers. It is neither the entire 32-bit instruction word nor the entire 64-bit value held in an RV64 datapath register.

Even if two ports both concern registers, a five-bit register-number wire differs in width and meaning from a register-data wire. A width mismatch requires determining from the specification whether to select, truncate, or extend; it does not justify arbitrarily making 32 and 64 match. Conversely, equal widths do not make an address and an arithmetic operand interchangeable.

The worksheet also says that not every module or port may be needed. The task is to provide the connections required by supported instructions, not to fill every empty port. Since the actual `assignment-1.md`, starter code, and tests are absent, the worksheet alone cannot determine exact control encodings, completed wiring, or a Chisel implementation.

## Lab2 data memory, control flow, and specification reading

### Architectural effects beyond an arithmetic result

The Lab2 briefing extends Lab1's single-cycle CPU to RV64I integer instructions including loads, stores, branches, `lui`, `auipc`, `jal`, and `jalr`. Read the introduction at 42:57 in the [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|undated lecture (computer_architecture:NT002)]] alongside computer_architecture:NM008 p.2. The explanation here is bounded to general instruction concepts and reading the specification.

This undated transcript is text compared with the materials without verified original audio, not a complete verbatim recovery. Missing speech, the actual class date, and speaker identities have not been recovered.

Arithmetic/logic work centers on obtaining operands and writing a result to a register. A load separates **which address is read** from **where the returned data goes**. A store separates **the address**, **the value**, and **permission to write**. A conditional branch combines a condition and target to select next PC. `lui` forms an upper-immediate value; `auipc` forms a PC-relative value; `jal` and `jalr` combine control transfer with a link value. Reusing an ALU or mux does not make these architectural effects equivalent.

The briefing's statement that the template includes a Lab1 R/I solution describes what is to be provided. It is not a finding from examining that code or checking its correctness. Lab2 again warns of control definitions that can differ from the class model, so its `assignment-2.md` contract must govern. The undated lecture's discussion at 43:54 reinforces the need to consult that document.

### Data Memory ports and the boundary of a wiring solution

The blank worksheet in private lab source computer_architecture:NM008 p.3 adds Data Memory with ports named `address`, `writedata`, `valid`, `memread`, `memwrite`, `maskmode`, `sext`, and `readdata`. These names support distinguishing the questions to ask, without reproducing the original diagram or supplying its connections.

`address` denotes the location, `writedata` the value to store, and `readdata` the returned value. `valid` and the read/write controls distinguish whether an access is valid and which operation is requested. `maskmode` and `sext` identify where access width and extension behavior need to be checked, but their names do not supply exact encodings or a width table. The fundamental requirement is that the memory control and transferred data belong to the same instruction.

The worksheet calls for necessary control wires as well as data wires, muxes, widths, and partial-bit slices. The five-bit calculation for `instruction[19:15]` still applies; it remains distinct from a 32-bit instruction word and 64-bit register data. The width discussion at 44:10 in the undated lecture, computer_architecture:NT002, connects to this requirement. Uncertain wording such as “full/four” at 45:07 must not be converted into an exact quotation of submission rules.

The material directs students through Parts I–IX in order, with tests for each part, and lists a worksheet and four code files as submission items. This encourages checking successive parts against their contracts. Without `assignment-2.md`, the template, and the tests themselves, the individual part contents, permitted I/O changes, test commands, and pass conditions cannot be reconstructed. Instruction scope, control definitions, interface widths, and submission items each need confirmation in the actual specification; a lecture diagram does not replace a complete wiring or implementation solution.

## Recall and Practice

### Review sequence

After Q01–Q03, use P01 to state exactly what each observation establishes. In Q04–Q07, distinguish instruction effects from port roles and check the five/32/64-bit calculation; then correct the specification-reading mistakes in P02.

### Environment and the scope of checks

#### Recall Q01 · Files, environment, and preparation

Distinguish Docker containers, dinocpu, VSCode Dev Containers, and Lab0/Chisel preparation. Give the material’s sequence from extraction to container connection. Does an optional tutorial make Lab1 optional?

<details><summary>Show solution</summary>

A container is the tool-execution environment; dinocpu is the design-file project; Dev Containers connects the editor to that environment. The material’s sequence is Docker preparation→extract with `tar -xzf dinocpu-lab1.tar.gz`→open `dinocpu/`→Reopen in Container to build/connect. Extracting or opening files alone neither establishes connection nor runs the CPU. Lab0 introduces setup and Chisel; `first-hardware.md` is optional preparation and Lab0 has no submission. This does not make CPU implementation optional. CLI details are delegated to `assignment-0.md`, whose absent body cannot establish build/test commands.

Checking points: Check distinct roles, sequence, and optional preparation versus the implementation assignment.

Sources: [Lab0·Lab1 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004) · [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005) · [Lab0·Lab1 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006)

</details>

#### Recall Q02 · Reading the Windows-to-Ubuntu path

Explain the material’s Windows→WSL→Ubuntu sequence with shell context. What do `wsl --install`, `wsl --set-default-version 2`, the Docker installation script, group change, shell reopening, and `hello-world` each do? Do not execute them.

<details><summary>Show solution</summary>

After enabling WSL in Windows Features and restarting, administrator PowerShell runs `wsl --install` for installation and `wsl --set-default-version 2` to set the default WSL version. Enable Execute In WSL in Dev Containers, then run `wsl` in PowerShell to enter Ubuntu and continue the Ubuntu steps. The supplied `curl -fsSL https://get.docker.com | sudo sh` example executes a downloaded installation script; `sudo usermod -aG docker $USER` changes current-user group membership. The described WSL warning and approximately 20-second pause are not CPU tests. Close/reopen the shell, entering `wsl` again on that path. `docker run hello-world` checks that example’s container execution, not a dinocpu build or assignment pass.

Checking points: Check PowerShell versus Ubuntu and the distinct installation, setting, group, and example-execution steps.

Sources: [Docker Install p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001) · [Docker Install p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002) · [Docker Install p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003) · [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004)

</details>

#### Recall Q03 · Mac alternatives and what checks establish

Distinguish the two Mac paths and their follow-up checks. How should `Docker version 28.0.1` and `docker —version` versus `docker --version` be interpreted? What do version output, `hello-world`, and Reopen in Container fail to establish?

<details><summary>Show solution</summary>

The first path selects chip-appropriate Docker Desktop, moves `Docker.app` from its `.dmg` into Applications, starts it, then checks the menu-bar icon and version. The second uses `brew install --cask docker` as an alternative, followed by app startup and the same checks. They are not consecutive mandatory installations. Version 28.0.1 is an output example, not a required/latest release. Page 7’s em dash `—` differs from page 6’s two hyphens `--`; code follows page 6’s `docker --version`. Version output reports information; `hello-world` runs that example; Reopen in Container handles the project container’s build/connection. None alone certifies CPU implementation or full-test correctness.

Checking points: Check alternatives, app startup/checks, example version and literal dash difference, and the limits of each observation.

Sources: [Docker Install p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005) · [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006) · [Docker Install p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)

</details>

### Assignment scope and specification reading

#### Recall Q04 · Format versus implementation scope

Why can remembering Lab1 merely as an I-type assignment incorrectly include loads? If a lecture mux-select value differs from the assignment document, which governs and why?

<details><summary>Show solution</summary>

The detailed briefing specifies R-type and I-type arithmetic/logic instructions. I-type describes encoding format; not every I-type instruction is arithmetic/logic, so format alone cannot add loads. Implementation must follow `assignment-1.md` control definitions. ISA operation meaning and a particular datapath’s select encoding are different contracts; zero in a lecture diagram does not establish zero in the assignment. The absent document, starter, and tests prevent deriving its exact truth table or completed code here.

Checking points: Check format versus R/I arithmetic/logic scope and the reason assignment-specific control definitions govern.

Sources: [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008)

</details>

#### Recall Q05 · Port meaning and width

Classify `readreg1`/`writereg`, `readdata1`/`writedata`, `wen`, ALU `operation`, and `instruction→sextImm` on the blank worksheet. Calculate the width of `instruction[19:15]` and register count, contrasting instruction-word and RV64-data widths. Can Control Unit, ALU Control, and Next PC names determine all wiring?

<details><summary>Show solution</summary>

`readreg1`/`writereg` are indices; `readdata1`/`writedata` are data; `wen` is write enable; `operation` selects the ALU function. Immediate Generator interprets instruction immediate fields into `sextImm`. The inclusive slice is 19−15+1=5 bits, selecting 2^5=32 registers; it is distinct from a 32-bit instruction and 64-bit register data. Control Unit outputs include `itype`, `aluop`, `src1`, `src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, `wordinst`. ALU Control uses `aluop`, `itype`, `funct7`, `funct3`, `wordinst` to determine `operation`. Next PC’s `pc`, `imm`, `inputx`, `inputy`, `funct3`, `branch`, `jumptype` indicate roles to inspect. Names do not provide encoding tables: necessary wires, muxes, widths, and slices follow the specification. The given `select 32 bits` block is not an arbitrary 64-bit data wire, and every port need not be used. Equal widths also do not equate an address with an operand.

Checking points: Distinguish the five/32/64-bit levels, indices/data/enables/selections, required width/slice labels, and the specification boundary.

Sources: [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009)

</details>

#### Recall Q06 · Lab2 architectural effects

List the newly introduced instruction classes and distinguish the effects of loads, stores, branches, `lui`, `auipc`, `jal`, and `jalr`. How should the statement that the template contains a Lab1 solution be interpreted?

<details><summary>Show solution</summary>

The briefing extends Lab1 to RV64I integer instructions including loads, stores, branches, `lui`, `auipc`, `jal`, and `jalr`. A load distinguishes read address from returned-data destination; a store distinguishes address, data, and write permission. A branch selects next PC using condition and target. `lui` forms an upper-immediate value, `auipc` a PC-relative value, and `jal`/`jalr` combine transfer with a link. Sharing an ALU does not equate these effects. The included Lab1 R/I solution is a statement about provision, not an inspection or correctness finding. Control follows `assignment-2.md`, but its body, template, and tests are absent, so complete implementation cannot be determined.

Checking points: Check every listed class, distinct effects, and promised provision versus actual verification.

Sources: computer_architecture:NM008 p.2

</details>

#### Recall Q07 · Memory ports and missing specifications

What distinctions are required for Data Memory’s `address`, `writedata`, `readdata`, `valid`, `memread`, `memwrite`, `maskmode`, and `sext`? Explain what worksheet labels, Parts I–IX, per-part tests, and submission guidance establish and what they do not.

<details><summary>Show solution</summary>

`address` is a location, `writedata` a stored value, and `readdata` a returned value. `valid` and read/write signals distinguish access validity and operation; `maskmode` and `sext` identify access-width/extension meanings to check in the specification. Names do not define bit encodings. Data and control must describe the same instruction’s effects; label required data/control wires, muxes, widths, and partial-bit slices. Keep five-bit indices, 32-bit instructions, and 64-bit data separate. The briefing gives Parts I–IX in order, per-part tests, and four code files plus a worksheet, but not each part’s implementation, test commands/pass criteria, or permitted I/O changes. Undated 45:07’s uncertain full/four wording does not become exact speech merely by comparison with the material.

Checking points: Check location/value/control roles, widths/slices, and workflow guidance versus the missing implementation contract.

Sources: computer_architecture:NM008 p.2 · computer_architecture:NM008 p.3 · computer_architecture:NM008 p.4

</details>

### Newly written general practice

#### Practice P01 · Avoid overstating verification

Newly written lecture/material-based general practice. No indexed candidate directly tests Docker/Dev Containers preparation status. Prerequisites: Q01–Q03.

A student (1) sees a version string, (2) sees `hello-world` run, and (3) opens extracted project files in the editor, then reports that the CPU assignment tests are finished. State what each observation supports and what still needs checking. Do not invent installation or test commands.

<details><summary>Show solution</summary>

Observation (1) establishes version information, (2) the example container’s execution, and (3) open project files. None establishes this project’s Reopen in Container connection, dinocpu build, or assignment test results. Check the project-container connection separately and consult the actual assignment for build/test procedures and success criteria. Since that document is absent here, neither guessed commands nor a pass claim are justified.

Checking points: Match each claim to its observation and distinguish container connection, project build, and assignment success.

Sources: [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004) · [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006) · [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005)

</details>

#### Practice P02 · Three errors in a design note

Newly written material-based general practice. No candidate in the complete recalled-exam index directly assesses this Lab worksheet’s specification-reading contract, so this is not labeled an exam variation. Prerequisites: Q04–Q07.

A note says: “Every I-type instruction belongs in Lab1. `instruction[19:15]` concerns registers, so it is 64 bits. Lab2 names `maskmode`, so its encoding may be chosen arbitrarily.” Correct each statement, then provide a specification-reading checklist that can be written now without supplying completed wiring.

<details><summary>Show solution</summary>

First, Lab1 is limited to R/I arithmetic/logic; format alone does not include loads. Second, the inclusive slice is 19−15+1=5 bits of register index, distinct from 64-bit register data. Third, `maskmode` identifies width-related behavior to inspect; its encoding follows `assignment-2.md`. A justified checklist records supported instruction effects, each port’s index/data/control role, required wire/mux widths and slices, authoritative control definitions, and the supplied part/test/submission guidance versus matters still requiring the actual specification. Do not fill missing truth tables, TODOs, or complete connections.

Checking points: Correct all three with reasons and separate specification questions from implementation answers.

Sources: [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008) · [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009) · computer_architecture:NM008 p.2 · computer_architecture:NM008 p.3

</details>

## Sources

### Lectures and materials

[[courses/computer_architecture/lectures/en/2026-09-29-lecture-05|2026-09-29 · Microcode, resource reuse, and lab briefing]]

- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 (computer_architecture:NT001)]] 56:40, 57:31, 58:36, 59:36 — Transcript of the dated lecture.

- [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|Undated lecture (computer_architecture:NT002)]] 42:57, 43:54, 44:10, 45:07 — Lecture date unknown; uncertain speech remains distinct from material-based explanation. This TXT transcript was compared with the materials; original audio is unverified. It is not a complete verbatim transcript and does not recover missing speech, the actual class date, or speaker identities.

- [Lab0·Lab1 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Lab.0.1.pdf): [Lab0·Lab1 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004), [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005), [Lab0·Lab1 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006), [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008), [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009). Lab0/Lab1 briefing and blank worksheet, not a replacement for detailed assignment documents.

- [Docker Install PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Docker.Install.pdf): [Docker Install p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001), [Docker Install p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002), [Docker Install p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003), [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004), [Docker Install p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005), [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006), [Docker Install p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007). Installation examples from the material, not verification of current products or execution.

- Lab2 briefing, pp.2–4: private material with no public original or page link. Used only for its stated scope and port meanings; assignment2, templates, and tests are not supplied.

No candidate in the complete recalled-exam index directly tests these Docker/WSL/container checks or the particular Lab1/Lab2 worksheet-reading contract. Related CPU-design questions do not authenticate this lab’s exam style; P01–P02 are general practice.


---

[[courses/computer_architecture/units/en/microcode-resource-reuse|← Previous: Microcode, Resource Reuse, Pipelining, and Hazards]] · [[courses/computer_architecture/units/index|Unit contents]]
