---
title: "컴퓨터의 구성과 ISA: 명세에서 구현까지"
description: "ISA의 계약, 컴퓨터 구성, RISC의 선택과 multicore의 동기를 연결한다."
course: "computer_architecture"
unit_id: "architecture-contract"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 01.pdf", "lec 02.pdf", "lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-01-lecture-01", "courses/computer_architecture/lectures/2026-09-03-lecture-02", "courses/computer_architecture/lectures/2026-09-08-lecture-03"]
---

ISA(명령어 집합 구조)가 정하는 동작과 그 동작을 실현하는 설계를 구분한다. 상태 변화, compiler와 OS의 요구, 소자 scaling의 한계를 연결하면 같은 instruction을 실행하는 컴퓨터도 성능이 다른 이유를 설명할 수 있다.

## ISA와 Microarchitecture가 나누는 책임

Computer(컴퓨터)는 데이터를 저장하고 검색하고 처리하는 programmable device(프로그램 가능한 장치)다. 휴대전화, desktop, server, data center의 규모는 달라도 프로그램이 요구하는 계산을 수행한다는 역할은 같다. 여기서 프로그램이 기대하는 **동작의 의미**와 그 동작을 실현하는 **구현 방법**을 나누면 컴퓨터의 여러 층을 이해하기 쉬워진다.

Instruction Set Architecture(명령어 집합 구조, ISA)는 software에서 관찰하고 제어할 수 있는 동작의 명세다. Microarchitecture(마이크로아키텍처)는 그 명세를 만족시키는 processor의 실제 설계다. Circuit(회로)은 그 설계를 gate, wire, transistor로 구현하는 층이다. 두 processor가 같은 덧셈 instruction을 이해하더라도 datapath(데이터 경로), control logic(제어 논리), cache(캐시)가 다르면 실행시간과 전력은 달라질 수 있다. 속도가 다르다는 이유만으로 ISA도 다르다고 결론내릴 수 없다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 03:13]]

[[page_cache/computer_architecture/lec.01/page-016|CA M001 p.16]]의 계층 그림은 applications, compilers, OS 아래에 ISA와 microarchitecture를 놓고 그 아래에 digital design, circuits, devices/physics를 배치한다. ISA는 software와 hardware 사이의 접점이며 그 아래에서는 같은 의미를 여러 방식으로 실현한다. 자동차의 사용 설명서가 정하는 조작법, 특정 자동차의 설계, 실제 부품을 구분하는 것과 비슷하다. 같은 ISA는 machine instruction 의미의 호환 기반이지 모든 library와 실행 환경까지 같다는 보장은 아니다.

## Stored-program과 Architectural state

Stored-program(프로그램 내장) 방식에서는 instruction(명령어)과 data(데이터)를 모두 memory(메모리)에 표현한다. Processor는 프로그램을 바꾸어 다른 일을 할 수 있으며, 가져온 bit pattern을 ISA에 따라 instruction으로 해석한다. [[page_cache/computer_architecture/lec.01/page-014|CA M001 p.14]]는 processing 안의 control과 datapath, program과 data를 저장하는 storage, 외부와 연결되는 I/O(입출력)를 보여 준다. 다음 페이지에서는 CPU의 ALU(산술 논리 장치), register file(레지스터 파일), cache가 main memory와 I/O 쪽으로 연결된다. 이는 구성요소의 역할을 읽는 모형이지 모든 컴퓨터의 배선도는 아니다.

Architectural state(아키텍처 상태)는 실행의 의미를 나타내는 programmer-visible state(프로그래머 가시 상태)다. Register(레지스터)는 processor 안의 작은 저장 위치이고, memory는 더 많은 instruction과 data를 담는다. Program Counter(프로그램 카운터, PC)는 실행할 instruction의 주소를 나타낸다. 순차 실행 모형에서는 PC가 가리키는 instruction을 fetch(가져오기)하고 execute(실행하기)한 뒤, 그 의미에 따라 PC를 갱신한다. 이 명시적인 상태 전이 설명은 녹음이 없는 9월 3일의 자료 기반 복습이다. [[page_cache/computer_architecture/lec.02/page-007|CA M008 p.7]] [[page_cache/computer_architecture/lec.02/page-010|CA M008 p.10]]

| Instruction 범주 | 주된 상태 변화 | 다음 실행 위치 |
|---|---|---|
| Arithmetic/logical | 입력값을 계산해 destination에 결과 저장 | 보통 다음 순차 instruction |
| Data movement | Register와 memory 등 사이에서 값 이동 | 보통 다음 순차 instruction |
| Control flow | 조건과 target에 따라 실행 순서 결정 | Target 또는 순차 위치 |

`add`는 두 입력값을 더해 destination register에 쓰지만 conditional branch(조건 분기)는 조건에 따라 PC를 바꾼다. Branch의 target은 결과를 받을 register가 아니다. ISA는 숫자의 format과 size, binary encoding(이진 부호화), visible state, I/O interface, protection·privilege 및 software convention도 다룬다. 이 항목들을 소개한 것과 상세 구현을 배운 것은 구분해야 한다.

9월 1일에는 program과 data가 통로를 공유하는 설명을 Harvard architecture의 분리된 통로와 대비했다. 저장의 개념, 접근 통로, 구체적인 cache 구성은 서로 다른 질문이다. 어느 구조가 항상 빠르다는 결론에는 별도 조건이 필요하다. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 22:25–23:07]] 2025-2 복기 Q1도 이 저장 개념을 구분하도록 요구하지만, 복기 문항은 현재 강의의 발화 근거나 공식 정답이 아니다. [EX:ca_2025_2_midterm_q01 p.2]

## Compiler와 Context switching이 ISA를 필요로 하는 이유

Compiler(컴파일러)는 C의 expression(식)을 실제 instruction sequence(명령어 열)로 바꾼다. 덧셈에 어떤 operand(피연산자)를 줄 수 있는지, register가 몇 개이고 data format은 무엇인지 알아야 올바른 코드를 만든다. 고수준 언어가 이 세부를 감추더라도 hardware와의 약속이 사라지지는 않는다.

Operating system(OS, 운영체제)의 context switching(실행 문맥 전환)은 같은 계약을 다른 방향에서 보여 준다. Process A의 계산값이 register에 남은 상태에서 process B를 실행하면 B가 같은 실제 register를 덮어쓸 수 있다. A를 이어 실행하려면 그 상태를 memory 등에 보관했다가 복원해야 한다. 강의는 현재 register 값을 저장하고 다른 process의 값을 register로 가져오는 동작을 설명했다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 04:46–05:32]] 무엇을 어떻게 보존할 수 있는지는 ISA와 연결되지만, 이 예가 완전한 OS context 구조나 scheduling 정책까지 정하지는 않는다.

## Transistor에서 Gate로 이어지는 구현

명세를 실제 동작으로 만들려면 binary value(이진값)를 물리적으로 표현해야 한다. 강의의 간략 모형에서 transistor(트랜지스터)는 control에 따라 전류 경로를 연결하거나 끊는 switch(스위치)다. [[page_cache/computer_architecture/lec.01/page-019|CA M001 p.19]]의 위쪽 유형은 control이 1일 때 연결되고 아래쪽 유형은 0일 때 연결된다. 모든 transistor의 control polarity가 같다는 그림이 아니다.

Gate(논리 게이트)는 binary input으로 binary output을 만든다. Inverter(반전기)는 입력을 뒤집고 NAND는 AND 결과를 뒤집는다. 따라서 NAND는 두 입력이 모두 1일 때만 0이다.

| A | B | AND | NAND |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

이 규칙은 [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 30:22]]와 일치한다. M001 p.20의 NOR 라벨 도형은 NAND와 비슷한 외곽으로 그려져 있으므로 도형만으로 NOR 기능을 추론하지 않는다. Gate를 조합하면 현재 입력으로 출력을 정하는 combinational circuit(조합 회로)과 상태를 보존하는 sequential circuit(순차 회로), 나아가 memory와 CPU를 만들 수 있다. 여기서는 이 연결을 이해하며, transistor 수준의 상세 설계는 별도 선수학습이다.

## Operand 형식과 RISC의 단순화

Instruction set(명령어 집합)은 컴퓨터가 제공하는 operation의 목록이다. x86-64, ARM, RISC-V는 다르지만 arithmetic, data movement, control flow라는 공통 요구를 해결한다. 강의는 RISC-V를 UC Berkeley에서 개발된 open ISA로 소개하고 embedded processor와 accelerator에도 쓰이는 수업 예제로 선택했다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 07:20–11:44]]

M008은 `OP in2`인 monadic, `OP inout,in2`인 binatic, `OP out,in1,in2`인 triadic operand 형식을 비교한다. 첫 형식은 일부 입력·결과 위치가 암묵적이고, 두 번째는 한 위치가 입력과 출력을 겸하며, 세 번째는 결과와 두 입력을 따로 명시한다. RISC-V의 기본 register arithmetic는 세 번째 방식이다. [[page_cache/computer_architecture/lec.02/page-013|CA M008 p.13]]

RISC의 load-store(적재·저장) 방식은 ALU 연산과 memory 접근을 분리하고 비교적 적은 format을 사용한다. 복잡한 expression도 여러 단순 instruction으로 나누면 계산할 수 있다. 대신 compiler가 중간 결과를 보관하고 register를 배정하며 sequence를 구성해야 한다. 단순한 ISA가 모든 일을 한 instruction으로 처리한다는 뜻은 아니다.

9월 3일 자료는 초기 ISA의 단순함, assembly programming·microprogramming과 관련된 CISC의 복잡화, cache와 compiler의 발전을 배경으로 한 RISC의 단순화를 구분한다. x86의 지속성에는 호환 생태계와 경제적 요인도 관련된다. 이것은 자료 기반 역사 설명이며 9월 8일의 불명확한 trade-off 발화를 복원한 내용은 아니다. [[page_cache/computer_architecture/lec.02/page-016|CA M008 pp.16–17]]

## ISA의 확장성과 General purpose

ISA는 이후 프로그램과 구현도 의존하는 장기 계약이다. 즉각적인 최적성이 미래의 compatibility(호환성)와 scalability(확장성)에는 불리할 수 있다. M008은 storage capacity, CPU 수, I/O 수를 parameter화하고 instruction encoding에 spare bits(여분 비트)를 남기는 방법을 소개한다. 여유 공간이 있으면 기존 pattern의 의미를 바꾸지 않고 확장할 가능성이 생긴다. 이것만으로 모든 호환 문제가 해결되는 것은 아니다. [[page_cache/computer_architecture/lec.02/page-026|CA M008 p.26]]

General purpose(범용성)는 크기와 종류가 다른 application을 지원한다는 뜻이다. 일반 data의 bit pattern에 임의의 특별한 의미를 강요하지 않고, 필요한 numeric operation과 bit manipulation, 세밀한 memory addressing을 제공하는 방향이다. 문자로 쓰인 bit들을 processor가 언제나 문자로만 취급할 필요는 없다. 반면 ML accelerator는 범용성 일부를 줄여 특정 계산의 성능을 얻는 대비 사례다. 자료의 asynchronous operation(비동기 동작)은 구성요소를 하나의 고정 속도에 지나치게 묶지 않으려는 설계 항목이며, 구체적인 회로 protocol까지 주어진 것은 아니다. [[page_cache/computer_architecture/lec.02/page-027|CA M008 p.27]]

## Moore's Law와 Multicore의 동기

Moore's Law(무어의 법칙)는 chip의 transistor 수가 대략 2년마다 두 배가 되는 역사적 추세로 소개된다. M001 p.23의 세로축은 logarithmic scale(로그 척도)이므로 같은 높이 차이는 일정한 개수가 아니라 일정한 배수의 증가다. Transistor 수가 늘었다고 프로그램이 같은 배수로 빨라지지는 않는다.

[[page_cache/computer_architecture/lec.01/page-024|CA M001 p.24]]의 표에는 1970년대 10K–100K transistors와 0.2–2 MHz, 1980년대 100K–1M과 2–20 MHz, 1990년대 1M–100M과 20 MHz–1 GHz가 놓여 있다. 마지막 2010 열의 1B transistors, 10 GHz, IPC 10(?), MIPS/MFLOPS 100,000은 **extrapolated(외삽한)** 값이다. 강의에서도 명시했듯 실제 측정 결과로 읽으면 안 된다. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 36:16]]

Dennard Scaling(데나드 스케일링)은 소자가 작아질 때 더 빠르게 switch하면서 전력 밀도를 유지할 수 있다는 scaling 배경이다. 자료는 leakage와 overheating을 한계로 든다. [[page_cache/computer_architecture/lec.01/page-026|CA M001 p.26]]에서는 transistor 수가 계속 늘어도 frequency와 single-thread performance가 같은 비율로 따라가지 않는다. Frequency의 둔화와 logical core 수 증가를 함께 보아야 하며 single-thread performance가 완전히 정지했다는 그림도 아니다.

Multicore(다중 코어)는 독립 작업을 동시에 수행하여 throughput(처리량)을 높일 수 있다. 그러나 한 작업의 latency(지연시간)를 줄이려면 그 작업을 나눌 수 있어야 한다. 설명용으로 같은 길이의 독립 작업 두 개를 두 core에 하나씩 주면 이상적으로 함께 끝낼 수 있지만, 나눌 수 없는 작업 하나가 자동으로 절반 시간에 끝나지는 않는다. 선형 throughput 향상에도 충분한 작업과 병목이 없다는 조건이 필요하다. 이 구분은 [실행시간과 성능 모형](performance-model.md)의 출발점이다.

## 핵심 정리

- ISA는 관찰 가능한 의미를 정하고 microarchitecture는 그것을 구현한다.
- PC·register·memory의 변화로 instruction의 효과를 설명하면 계산 결과와 다음 실행 위치를 혼동하지 않는다.
- Compiler의 번역과 OS의 context switching은 같은 architectural state에 의존한다.
- 단순한 operand 형식, 확장 공간, 범용성은 서로 다른 설계 요구를 조정하는 선택이다.
- Transistor 증가·frequency·단일 작업 latency·여러 작업 throughput은 별개다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · 명세와 구현

같은 `add`를 실행하는 두 processor의 속도와 전력이 다르다. ISA·microarchitecture·circuit 중 어느 층의 차이로 설명할 수 있으며, 같은 ISA만으로 전체 프로그램 실행을 보장할 수 있는가?

<details><summary>해설 보기</summary>

ISA는 `add`가 만드는 결과처럼 software에서 관찰할 동작을 정한다. Datapath·control·cache 선택은 microarchitecture, gate·wire·transistor로 만드는 일은 circuit 층이므로 같은 의미를 다른 비용으로 구현할 수 있다. 프로그램은 library와 실행 환경도 요구하므로 instruction 의미의 호환만으로 모든 실행 조건이 충족되지는 않는다.

**채점·확인 기준:** 세 층의 책임, 성능 차이의 가능성, 실행 환경 조건을 모두 설명한다.

</details>

#### 확인 Q02 · 구성요소와 저장

Stored-program에서 memory에 놓이는 두 종류의 내용을 말하고 control·datapath·storage·I/O의 역할을 연결하라. Harvard의 분리 통로와 비교하면 한 구조가 항상 더 빠르다는 결론도 나오는가?

<details><summary>해설 보기</summary>

Memory에는 instruction과 data가 있다. Control은 실행을 지시하고 datapath는 값을 처리하며 storage는 프로그램·값을 보관하고 I/O는 외부와 교환한다. ALU·register file·cache와 main memory의 구성 그림은 역할 모형이다. 저장되는 내용과 접근 통로의 공유 여부는 구분해야 하며, 실제 workload와 구현 조건 없이 보편적인 속도 우위를 정할 수 없다.

**채점·확인 기준:** Instruction/data와 네 역할을 설명하고 통로 수만으로 성능을 단정하지 않는다.

</details>

#### 확인 Q03 · Instruction이 바꾸는 상태

`add`, data movement, conditional branch를 register·memory·PC 관점으로 비교하라. ISA가 정하는 항목은 이 세 instruction 이름 외에 무엇이 있는가?

<details><summary>해설 보기</summary>

`add`는 source register 값으로 destination 값을 만들고 보통 PC를 다음 순차 위치로 옮긴다. Data movement는 저장 위치 사이 값을 옮기며, branch는 조건에 따라 target 또는 순차 PC를 선택한다. Target은 산술 결과 register가 아니다. ISA는 data 크기·format, visible state, encoding, I/O interface, protection·privilege, software convention도 다룬다. 이 목록은 상세 I/O나 privilege 구현을 학습했다는 뜻은 아니다.

**채점·확인 기준:** 계산 결과와 제어 흐름을 구분하고, PC 중심 fetch/execute 흐름 및 ISA의 더 넓은 계약을 설명한다.

</details>

#### 확인 Q04 · Compiler와 실행 문맥

Compiler가 C의 덧셈을 번역할 때 ISA에서 알아야 할 것을 두 가지 이상 들라. Process B가 A의 register를 덮어쓴 뒤 A를 재개하려면 무엇이 필요한가?

<details><summary>해설 보기</summary>

Compiler는 사용할 연산, operand와 register, data format·encoding을 알아야 한다. A의 중간값은 B가 실행되기 전에 memory 등에 보관하고 A를 재개할 때 복원해야 한다. 그렇지 않으면 A가 B의 값으로 이어 계산한다. 고수준 언어가 세부를 숨겨도 번역과 상태 보존에 필요한 계약은 사라지지 않는다.

**채점·확인 기준:** Compiler 요구와 save/restore의 인과관계를 둘 다 설명한다.

</details>

#### 확인 Q05 · Switch와 NAND

두 transistor 유형의 control polarity가 같다고 해도 되는가? NAND의 입력 00·01·10·11의 출력과 inverter의 역할을 쓰고, combinational과 sequential circuit을 구분하라.

<details><summary>해설 보기</summary>

위 유형은 control 1에서, 아래 유형은 0에서 연결되므로 polarity가 다르다. NAND는 AND의 반대여서 출력이 1·1·1·0이며 inverter는 입력을 뒤집는다. Combinational circuit은 현재 입력으로 출력을 정하고 sequential circuit은 상태를 보존한다. Gate에서 memory·CPU로 이어지는 연결을 이해하는 설명이며 NOR 라벨의 부정확한 도형이나 상세 transistor 회로를 추측하지 않는다.

**채점·확인 기준:** Polarity, 네 출력, 상태 보존 차이를 모두 맞힌다.

</details>

#### 확인 Q06 · Operand와 RISC의 선택

Monadic·binatic·triadic 표기의 implicit/shared/separate operand 차이를 설명하라. 단순한 RISC 연산으로 복잡한 식을 처리하는 방법과 자료가 제시한 CISC→RISC 변화의 배경을 연결하라. 서로 다른 ISA의 공통 범주와 RISC-V를 수업 예제로 쓰는 이유도 설명하라.

<details><summary>해설 보기</summary>

`OP in2`는 일부 입력·결과가 암묵적이고 `OP inout,in2`는 한 위치를 입력·출력으로 공유하며 `OP out,in1,in2`는 결과와 두 입력을 구분한다. RISC-V 기본 register arithmetic는 마지막 방식이다. Compiler가 복합 식을 여러 instruction으로 나누고 중간값·register를 관리한다. 자료는 assembly programming·microprogramming과 CISC의 복잡화를, cache·compiler 발전과 RISC 단순화를 연결하며 x86의 지속성에는 호환 생태계·경제적 요인도 든다. x86-64·ARM·RISC-V는 서로 다른 ISA이지만 arithmetic·data movement·control flow 범주를 공유한다. Berkeley에서 개발한 open ISA인 RISC-V는 교육뿐 아니라 embedded processor·accelerator에도 쓰여, 이 공통 개념을 실제 processor 예제와 연결해 배우게 한다.

**채점·확인 기준:** 세 형식·compiler의 역할·역사 설명·ISA 공통 범주와 RISC-V의 선택 이유를 구분하고 단순함을 instruction 한 개로 오해하지 않는다.

</details>

#### 확인 Q07 · 확장성과 범용성

Spare encoding bits와 storage·CPU·I/O 수의 parameter화는 왜 유용한가? General-purpose 설계와 ML accelerator의 선택, 자료의 asynchronous operation을 설명하라.

<details><summary>해설 보기</summary>

현재 pattern의 의미를 보존하면서 미래 기능·규모를 늘릴 여지를 만든다. 즉각적인 최적성과 장기 호환성이 항상 일치하지 않기 때문이다. 범용 설계는 일반 data pattern에 임의의 특수 의미를 강요하지 않고 여러 numeric·bit operation과 세밀한 addressing을 제공한다. Accelerator는 특정 계산을 위해 범용성 일부를 줄일 수 있다. Asynchronous는 구성요소를 한 고정 속도에 지나치게 묶지 않으려는 소개이며 구체적인 회로 protocol은 아니다.

**채점·확인 기준:** 확장 공간의 목적과 한계, 범용성·특화의 선택, asynchronous의 범위를 설명한다.

</details>

#### 확인 Q08 · Scaling 도표와 Multicore

Log 축에서 같은 높이 증가와 2010 열은 어떻게 읽는가? Transistor 수가 늘어도 frequency와 단일 작업 성능이 비례하지 않는 이유, multicore의 latency·throughput 조건을 설명하라.

<details><summary>해설 보기</summary>

Log 축의 같은 차이는 같은 배수이며 2010 열은 외삽값이다. Moore의 transistor 증가 추세와 Dennard의 전력 밀도·속도 scaling 기대는 다르고 leakage·발열은 frequency 향상을 제한한다. 그림은 single-thread 성능의 완전 정지가 아니라 증가 둔화를 보여 준다. 독립 작업이 충분하고 병목이 없다면 core를 늘려 처리량을 높일 수 있지만 한 작업 시간은 병렬화 가능성에 달린다.

**채점·확인 기준:** 외삽/측정 구분, 두 scaling 개념, 단일 작업과 독립 작업 조건을 모두 포함한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · 세 주장에 필요한 근거

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q01 p.2]의 저장 개념을 구분하는 추론을 옮겼으며 선수는 이 단원의 ISA·stored-program·multicore 설명이다. 두 processor가 같은 ISA를 구현하고 instruction과 data를 memory에 저장한다. B에는 core가 두 개다. (a) 두 processor의 실행시간이 같아야 하는가? (b) 이 정보로 접근 통로 구성을 알 수 있는가? (c) 나눌 수 없는 1초 작업 한 개와 독립적인 1초 작업 두 개에 대해 B의 이득을 구분하라. 각 core의 속도는 같고 추가 병목은 없다고 가정한다.

<details><summary>해설 보기</summary>

(a) 아니다. 같은 의미를 다른 microarchitecture로 구현할 수 있다. (b) 아니다. Memory에 표현된다는 사실만으로 접근 통로나 cache 구성이 정해지지 않는다. (c) 한 작업을 나눌 수 없다면 여전히 1초다. 독립 작업 두 개는 두 core에 하나씩 주어 이상적으로 1초에 함께 끝낼 수 있으며, 한 core에서 순차 실행한 2초와 비교해 전체 완료시간이 절반이다. 각 작업 자체의 service latency는 1초로 유지된다.

**채점·확인 기준:** 각 결론의 근거를 따로 쓰고, 두 작업의 총 완료시간 감소를 한 작업의 latency 감소로 바꾸지 않는다.

</details>

### 복습 순서

Q01–Q04로 계약과 상태 변화를 말로 설명하고, Q05–Q08은 표·그림 없이 재구성한다. P01에서 주장마다 필요한 근거를 분리한 뒤 [[courses/computer_architecture/units/program-translation-loading|프로그램 번역과 적재]]로 이어 간다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-01-lecture-01|2026-09-01 · 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 · 자료 기반 복습]]
- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 · 강의 노트]]

- [lec.01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.01.pdf): [[page_cache/computer_architecture/lec.01/page-011|p.11]], [[page_cache/computer_architecture/lec.01/page-014|p.14]], [[page_cache/computer_architecture/lec.01/page-015|p.15]], [[page_cache/computer_architecture/lec.01/page-016|p.16]], [[page_cache/computer_architecture/lec.01/page-019|p.19]], [[page_cache/computer_architecture/lec.01/page-020|p.20]], [[page_cache/computer_architecture/lec.01/page-021|p.21]], [[page_cache/computer_architecture/lec.01/page-023|p.23]], [[page_cache/computer_architecture/lec.01/page-024|p.24]], [[page_cache/computer_architecture/lec.01/page-025|p.25]], [[page_cache/computer_architecture/lec.01/page-026|p.26]], [[page_cache/computer_architecture/lec.01/page-027|p.27]]
- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-005|p.5]], [[page_cache/computer_architecture/lec.02/page-007|p.7]], [[page_cache/computer_architecture/lec.02/page-009|p.9]], [[page_cache/computer_architecture/lec.02/page-010|p.10]], [[page_cache/computer_architecture/lec.02/page-013|p.13]], [[page_cache/computer_architecture/lec.02/page-016|p.16]], [[page_cache/computer_architecture/lec.02/page-017|p.17]], [[page_cache/computer_architecture/lec.02/page-026|p.26]], [[page_cache/computer_architecture/lec.02/page-027|p.27]]
- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-006|p.6]]

- [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT · 22:25–23:07, 30:22, 36:16]]
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 03:13, 04:46–05:32, 07:20–11:44]]

- 9월 3일 lec.02는 녹음 없는 자료 기반 복습이다. Operand 분류·ISA 역사·확장 설계와 명시적인 상태 모형이 그날 실제로 설명된 진도를 뜻하지 않는다.
- 9월 8일 03:55·08:20의 불명확한 구절은 복원하지 않는다. Context switching은 register 보존의 동기이며 완전한 OS 정책 설명은 아니다.
- Gate 그림은 간략 모형이며 p.20의 NOR 외곽으로 기능을 판단하지 않는다. 상세 transistor 회로는 범위 밖이다.
- 2010 표의 수치는 외삽값이며 현대 제품 기록이 아니다. Multicore의 이상적 처리량 향상에는 독립 작업과 병목 부재가 필요하다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.

- [[exam_questions/ca_2025_2_midterm_q01|기존 문제 미리보기 · Q01]]


---

[[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/program-translation-loading|다음: 프로그램 번역·Linking·Loading →]]
