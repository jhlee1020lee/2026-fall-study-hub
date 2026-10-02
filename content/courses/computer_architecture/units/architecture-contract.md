---
title: "컴퓨터의 구성과 ISA: 명세에서 구현까지"
description: "ISA와 구현의 차이를 상태 변화와 설계 절충으로 정리한다."
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
source_lectures: ["courses/computer_architecture/lectures/2026-09-01-lecture-01", "courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-03-lecture-02"]
---

ISA가 약속하는 동작과 이를 실현하는 회로를 구분해 보자. 상태 변화에서 출발해 호환성, 확장성, 성능의 한계를 연결한다.

## ISA와 구현을 나누는 이유

Computer(컴퓨터)는 데이터를 저장·검색·처리하는 programmable device이다. 휴대 장치, desktop, server, data center는 크기와 목적이 달라도 프로그램에 따라 일을 한다는 점을 공유한다. 같은 프로그램을 서로 다른 회로에서 실행하려면, 프로그램이 요구하는 **동작의 의미**와 그 동작을 만드는 **구현 방식**을 구분해야 한다.

Instruction Set Architecture(명령어 집합 구조, ISA)는 소프트웨어가 관찰하고 제어할 수 있는 기능의 명세이다. Microarchitecture(마이크로아키텍처)는 그 명세를 만족시키는 processor 설계이며, circuit(회로)은 이를 gate, wire, transistor로 실현한다. 자동차의 사용 설명서, 특정 차량의 설계, 실제 부품을 구분하는 비유가 유용하다. 같은 ISA의 두 processor가 같은 덧셈 instruction을 이해해도 datapath, control, cache 구성이 다르면 속도와 전력 특성은 달라진다. 같은 ISA라는 조건만으로 운영체제와 실행 환경까지 모두 호환된다는 뜻은 아니다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 03:13]] [CA M008 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-005)

[CA M001 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-016)의 계층 그림은 applications, compilers, OS 아래에 ISA와 microarchitecture를, 그 아래에 digital design, circuits, devices/physics를 둔다. 위층은 아래층의 모든 세부 사항 대신 필요한 계약을 사용한다. 예를 들어 compiler는 C의 덧셈을 어떤 instruction과 operand 형식으로 표현할 수 있는지 알아야 하지만, 각각의 transistor를 배치할 필요는 없다. [[courses/computer_architecture/lectures/2026-09-01-lecture-01|2026-09-01 강의 노트]]

### Compiler와 context switching이 사용하는 계약

Compiler(컴파일러)는 operation, register, 데이터 크기와 instruction encoding을 알고 C 연산을 machine instruction으로 옮긴다. 고수준 언어가 이런 사항을 사용자에게 감추어도 system software에는 필요한 정보이다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 04:46]]

OS의 context switching(실행 문맥 전환)은 같은 실제 register를 여러 process가 번갈아 쓰게 한다. Process A를 멈추고 B를 실행하면 B의 계산이 register 값을 바꿀 수 있다. A를 이어 실행하려면 A의 값을 memory에 보관했다가 복원해야 한다. 9월 8일 설명은 이 저장·복원을 ISA가 software와 hardware 사이의 계약인 이유로 연결한다. Scheduling 정책이나 완전한 OS 문맥 구조까지 정한 설명은 아니다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 05:32]] [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]

## Stored-program과 architectural state

Stored-program(프로그램 내장) 구조에서는 instruction과 data를 모두 memory에 저장한다. [CA M001 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-014)의 processing block 안에는 연산을 하는 datapath와 순서를 정하는 control이 있고, storage에는 program과 data가 함께 표시된다. I/O는 외부와 정보를 주고받는다. 이어지는 [CA M001 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-015)에서는 CPU 내부의 ALU, register file, cache가 memory bus를 통해 main memory에 연결되고, I/O bridge가 disk·video·keyboard/mouse·network 쪽으로 이어진다. 이것은 구성요소의 관계를 설명하는 모형이며 모든 컴퓨터의 실제 배선을 고정하는 설계도는 아니다.

9월 1일에는 program/data 통로를 공유하는 설명과 Harvard architecture의 분리된 통로를 대비했다. 분리하면 동시 접근 기회가 생기지만, 통로 수만으로 모든 workload의 처리량 우위를 보장하지는 않는다. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 23:07]] 과거 복기 문항과 연결할 때도 핵심은 저장 대상과 통로를 구분하는 것이다. 시험 문장의 참·거짓을 외우기보다 instruction과 data가 어디에 놓이는지 설명할 수 있어야 한다. [EX:ca_2025_2_midterm_q01 p.2] 이 시험 연결은 2025-2 복기본에 근거하며 공식 원문·정답이 독립 확인된 자료는 아니다.

Architectural state(아키텍처 상태)는 프로그램 실행의 의미를 나타내는 memory, registers, Program Counter(프로그램 카운터, PC) 등의 상태이다. PC는 다음에 해석할 instruction의 **주소**를 지정한다. [CA M008 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-007)의 순차 모형은 그 주소에서 instruction을 fetch하고 실행한 뒤, instruction의 규칙에 따라 PC를 갱신한다.

| Instruction 종류 | 읽는 정보 | 바꾸는 상태 |
|---|---|---|
| Arithmetic/logical | Source operand | 계산 결과를 destination에 기록하고 보통 순차 PC로 진행 |
| Data movement | 옮길 값과 위치 | Register 또는 memory의 지정 위치 |
| Control flow | 조건과 target | 다음 PC를 target 또는 순차 주소로 선택 |

설명용으로 두 register의 값이 7과 5라면 덧셈은 destination에 12를 남긴다. Branch는 두 값을 비교해 다음 instruction의 위치를 결정한다. 이 차이가 ISA를 단순한 명령 이름 목록보다 넓은 계약으로 만든다. ISA는 숫자의 format·size, visible state, instruction과 encoding뿐 아니라 I/O interface, protection/privilege, software conventions도 다룬다. 여기서는 뒤 세 항목의 상세 구현까지 전개하지 않는다. [CA M008 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-010)

자료가 instruction을 추상적으로 atomic한 상태 전이라고 설명하는 것은 실행 전후의 의미를 정의하는 관점이다. 모든 instruction이 한 clock에 끝난다거나 다른 processor의 모든 memory 접근을 차단한다는 뜻으로 확대하면 안 된다. 이 명시적인 실행 모형은 녹음이 없는 9월 3일의 자료 기반 복습이다. [CA M008 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-011) [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]

## Operand 형식과 RISC의 단순화

Instruction set은 제공되는 operation의 repertoire이다. x86-64, ARM, RISC-V는 서로 다른 ISA이지만 arithmetic, data movement, control flow를 공통 범주로 갖는다. 강의에서는 UC Berkeley에서 개발된 open ISA인 RISC-V를 embedded processor와 accelerator에도 쓰이는 예로 소개했다. 이는 수업의 선택 동기이며 개별 라이선스 계약에 대한 법적 판단은 아니다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 07:20]] [CA M003 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-006)

[CA M008 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-013)의 operand 표기는 입력과 출력을 얼마나 명시하는지 비교한다.

| 자료의 분류 | 표기 | 읽는 방법 |
|---|---|---|
| Monadic | `OP in2` | 한 operand를 명시하며 나머지 의미는 operation 규칙에 의존 |
| Binatic | `OP inout,in2` | 한 위치를 입력과 출력으로 함께 사용 |
| Triadic | `OP out,in1,in2` | 출력 하나와 입력 둘을 각각 명시 |

RISC-V의 기본 register 산술은 마지막 형태를 따른다. Load-store 방식은 memory 접근과 ALU 연산을 분리한다. 복잡한 식도 여러 단순 instruction으로 구성할 수 있으며 compiler가 중간 결과와 register 배치를 관리한다.

자료의 역사 설명은 초기의 단순한 ISA, assembly programming·microprogramming과 함께 복잡해진 CISC, cache와 compiler의 발전을 배경으로 단순화를 추구한 RISC를 연결한다. 적은 format과 규칙성은 구현과 compiler 최적화에 도움이 된다. x86의 지속성을 기술적 우열 하나로 설명할 수 없고 호환 생태계와 경제적 요인도 고려해야 한다. 이 상세 역사 비교는 자료 기반이다. 9월 8일 08:20의 trade-off에 관한 불명확한 구절은 이 설명으로 복원된 발화가 아니다. [CA M008 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-016) [CA M008 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-017) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 08:20]]

### 확장성과 generality를 남기는 설계

ISA는 현재 한 processor만의 내부 약속이 아니다. 이후의 프로그램과 구현도 의존하므로 현재의 최적성 일부를 future scalability와 compatibility를 위해 양보할 수 있다. Storage capacity, CPU 수, I/O 수를 parameter화하고 instruction encoding에 spare bits를 남기면 나중에 확장할 여지가 생긴다. 모든 bit를 당장 소비하면 그 공간을 다시 확보하기 어렵다. 자료의 asynchronous component operation도 고정된 속도 관계에 과도하게 묶이지 않으려는 설계 항목이며 구체적인 회로 프로토콜은 제시되지 않는다. [CA M008 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-009) [CA M008 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-026)

Generality(범용성)는 여러 종류와 크기의 application을 지원하는 성질이다. 일반 data bit pattern에 임의의 특별한 의미를 강제하지 않고, numeric operation·bit manipulation·세밀한 memory addressing을 제공하는 방향과 연결된다. 반대로 ML accelerator는 범용성 일부를 줄여 특정 계산에 자원을 집중할 수 있다. 어느 쪽이 무조건 좋은지가 아니라 지원할 작업과 장기 호환성의 요구가 무엇인지가 설계 질문이다. [CA M008 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-027)

## Transistor에서 성능 확장의 한계까지

Transistor(트랜지스터)의 간략한 switch 모형은 control 값에 따라 전류 경로를 연결하거나 끊는다. [CA M001 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-019) 위 그림은 control=1일 때 연결되는 유형, 아래 그림은 control=0일 때 연결되는 유형을 보여 준다. 이런 switch로 binary input을 binary output으로 바꾸는 gate를 만든다. Inverter는 입력을 뒤집고 NAND는 AND 결과를 뒤집는다.

| 입력 A | 입력 B | NAND 출력 |
|---:|---:|---:|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

이 규칙은 9월 1일의 설명과 일치한다. Gate를 조합하면 combinational circuit을, 상태 보존 요소와 결합하면 sequential circuit·memory·CPU를 구성할 수 있다. 여기서 목적은 층위 사이의 연결을 이해하는 것이며 상세 transistor 설계는 범위 밖이다. 자료 p.20의 NOR 라벨 도형만으로 gate 기능을 추론하지 않는다. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 30:22]] [CA M001 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-021)

### Moore's Law와 Dennard Scaling은 다른 주장이다

Moore's Law는 chip의 transistor 수가 대략 2년마다 두 배가 되는 역사적 추세로 소개된다. [CA M001 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-023)의 세로축은 logarithmic scale이므로 그래프의 직선 같은 상승은 매번 같은 **개수**가 더해진다는 뜻이 아니다. [CA M001 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-024)의 역사 표는 다음 규모를 대비한다.

| 시기 | Transistors | Clock frequency | IPC | MIPS/MFLOPS |
|---|---:|---:|---:|---:|
| 1970년대 | 10K–100K | 0.2–2 MHz | <0.1 | <0.2 |
| 1980년대 | 100K–1M | 2–20 MHz | 0.1–0.9 | 0.2–20 |
| 1990년대 | 1M–100M | 20 MHz–1 GHz | 0.9–2 | 20–2000 |
| 2010 **외삽** | 1B | 10 GHz | 10(?) | 100,000 |

이 표의 2010년 행은 측정 결과가 아니라 외삽이다. 원본 M001 PDF p.24의 오른쪽 끝 2010년 열을 여기서는 행으로 옮겼다. 9월 1일 36:16에서도 이 점을 강조했다. MIPS/MFLOPS 역시 서로 다른 workload의 성능을 무조건 같은 기준으로 만드는 숫자는 아니다. [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 36:16]]

Dennard Scaling은 소자가 작아질 때 더 빨리 switch하면서 전력 밀도를 유지할 수 있다는 scaling 배경이다. 자료는 leakage와 overheating을 그 한계로 제시한다. [CA M001 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-025) [CA M001 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-026)의 추세 그림에서는 transistor 수가 늘어나는 동안 frequency와 single-thread performance가 같은 비율로 따라가지 않고 logical core 수가 증가한다. Single-thread performance가 완전히 멈춘 그림으로 읽으면 안 된다.

여러 core는 독립 작업을 함께 처리해 throughput(처리량)을 높일 수 있다. 그러나 한 작업의 latency(지연시간)를 줄이려면 그 작업 자체를 병렬화해야 한다. 설명용으로 독립 작업 둘을 core 둘에 하나씩 맡기면 두 작업을 함께 끝낼 수 있지만, 한 작업의 순차 부분이 자동으로 절반이 되지는 않는다. 충분한 독립 작업과 병목 없는 자원이 있어야 선형 처리량 증가도 기대할 수 있다. 이는 역사적 scaling 자료가 던지는 설계 동기이며 현재 제품의 기록이나 미래 예측은 아니다. [CA M001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-027) [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 STT 40:38]]

## 핵심 정리

- 같은 ISA도 datapath·cache·control 구현에 따라 속도와 전력이 달라진다.
- PC는 instruction의 주소이며 instruction 종류에 따라 다음 상태가 달라진다.
- 규칙적인 instruction은 compiler가 복잡한 계산을 여러 단계로 구성하도록 한다.
- Transistor 수 증가, 전력 밀도 유지, 단일 작업 가속은 서로 다른 주장이다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · 명세와 구현

같은 machine instruction의 의미를 지원하지만 속도가 다른 두 processor를 ISA·microarchitecture·circuit 층위로 설명하라. 같은 ISA면 어떤 프로그램 환경도 자동 호환되는가?

<details><summary>해설 보기</summary>

ISA는 software가 관찰·제어하는 기능의 계약이다. Microarchitecture는 datapath·control·cache로 그 계약을 구현하고 circuit은 gate·wire·transistor로 실현한다. 따라서 같은 연산 결과를 내면서도 실행시간·전력이 다를 수 있다. Compiler·OS는 위층에서 ISA를 이용하지만 운영체제와 실행 환경 조건까지 ISA 하나로 보장되지는 않는다. Computer의 저장·검색·처리 역할은 mobile부터 server까지 공유된다.

**채점·확인:** 세 층위의 역할과 성능 차이의 원인, 환경 호환성 한계를 모두 설명한다.

</details>

#### 확인 Q02 · 저장 구조와 상태 전이

Stored-program의 저장 대상과 Harvard의 통로 구분을 설명하라. CPU·memory·I/O의 역할을 연결하고 add, data movement, branch가 PC·register·memory에 주는 효과를 비교하라.

<details><summary>해설 보기</summary>

Instruction과 data를 memory에 저장한다. CPU의 datapath는 계산하고 control은 순서를 정하며 ALU·register file·cache는 main memory와 연결된다. I/O는 외부 장치와 정보를 주고받는다. Harvard의 분리된 program/data 통로는 동시 접근 기회를 주지만 항상 높은 처리량을 보장하지 않는다. PC의 주소에서 fetch한 뒤 add는 operand 합을 destination에 쓰고 보통 순차 PC로, data movement는 지정 register/memory로 값을 옮기고 순차 PC로, branch는 조건에 따라 target 또는 순차 PC로 진행한다. 추상적인 atomic 전이는 한 clock이나 다른 CPU의 모든 memory 접근 차단을 뜻하지 않는다.

**채점·확인:** PC를 instruction bits와 구별하고 세 instruction class의 상태 효과를 나눈다.

</details>

#### 확인 Q03 · Compiler와 문맥 복원

Compiler는 ISA에서 무엇을 알아야 하는가? Process A의 register를 저장하지 않고 B를 실행한 뒤 A로 돌아오면 어떤 문제가 생기는가? ISA가 instruction 이름 목록보다 넓은 이유도 답하라.

<details><summary>해설 보기</summary>

Compiler는 operation, operand 위치, register, 숫자 format·폭과 encoding을 알아야 한다. B가 같은 실제 register를 덮어쓰므로 A의 계산을 이어 가려면 A의 상태를 저장하고 복원해야 한다. ISA는 이 visible state와 변화 규칙 외에도 I/O interface, protection·privilege, software convention을 다룬다. 여기서 완전한 OS 문맥 구조나 scheduling 정책까지 정한 것은 아니다.

**채점·확인:** 정보가 사라지는 원인과 save/restore의 목적을 연결한다.

</details>

#### 확인 Q04 · Switch에서 NAND까지

Control=1에서 연결되는 transistor와 반대 유형을 구분하고 NAND의 네 입력 조합 출력을 써라. Inverter와 상태를 보존하는 회로의 역할도 설명하라.

<details><summary>해설 보기</summary>

첫 유형은 1에서 연결·0에서 차단하고 반대 유형은 0에서 연결·1에서 차단한다. NAND는 AND를 뒤집으므로 (00,01,10,11)에 (1,1,1,0)을 낸다. Inverter는 0↔1을 바꾼다. Gate 조합은 combinational 계산을 만들고 저장 요소는 sequential 상태·memory를 가능하게 한다. 애매한 NOR 도형의 외곽만으로 기능을 결정하거나 상세 transistor 설계를 배웠다고 확대하지 않는다.

**채점·확인:** 네 NAND 값과 combinational/sequential 차이를 확인한다.

</details>

#### 확인 Q05 · Operand 형식과 compiler

`OP in2`, `OP inout,in2`, `OP out,in1,in2`를 비교하라. RISC의 단순한 instruction으로 복잡한 식을 실행하는 방법과 load-store의 뜻은 무엇인가?

<details><summary>해설 보기</summary>

각각 한 operand 명시, 입력·출력 위치 공유, 출력 하나·입력 둘 명시이다. 기본 RISC-V register 산술은 마지막 형식이다. Compiler가 복잡한 식을 여러 단순 instruction으로 나누고 중간 값과 register 배정을 관리한다. Load-store는 memory 접근과 ALU 계산을 분리한다. 규칙적이고 적은 format은 구현·최적화를 돕지만 복잡한 일을 한 instruction에 모두 담는다는 뜻은 아니다.

**채점·확인:** 표기 수와 입력·출력 역할을 함께 해석한다.

</details>

#### 확인 Q06 · ISA 역사와 선택

x86-64·ARM·RISC-V의 공통 범주, 자료의 CISC→RISC 변화 배경, RISC-V를 수업 예로 고른 이유를 설명하라. x86의 지속성을 기술적 우열 하나로 설명할 수 있는가?

<details><summary>해설 보기</summary>

세 ISA는 arithmetic·data movement·control flow 범주를 공유한다. 자료는 초기 단순 ISA, assembly programming·microprogramming과 관련된 복잡화, cache·compiler 발전에 힘입은 단순화를 대비한다. RISC-V는 Berkeley의 open ISA이자 embedded·accelerator에도 쓰이는 예로 소개된다. x86의 지속성에는 호환 생태계와 경제적 요인도 있어 단일 성능 순위로 설명되지 않는다. 이는 역사·선택 동기이며 최신 시장 조사나 라이선스 판정은 아니다.

**채점·확인:** Compiler·cache 배경과 호환 생태계를 모두 포함한다.

</details>

#### 확인 Q07 · 확장성과 범용성

Unused encoding bits, capacity parameterization, asynchronous components가 어떤 장기 목적을 갖는가? 범용 설계와 ML accelerator의 절충을 비교하라.

<details><summary>해설 보기</summary>

Spare bits는 향후 기능을 위한 공간을, storage·CPU·I/O 수의 parameter화는 규모 변화 여지를 남긴다. Asynchronous operation은 고정된 속도 관계에 과도하게 묶이지 않으려는 항목이며 구체 protocol은 없다. 범용성은 여러 종류·크기의 작업을 지원하며 일반 data pattern에 임의 의미를 강제하지 않고 numeric·bit operation과 세밀한 주소 지정을 제공하는 방향이다. Accelerator는 일부 범용성을 양보해 특정 계산에 집중할 수 있다. 현재 최적성, 미래 호환성, 지원 workload를 함께 비교해야 한다.

**채점·확인:** 각 방법의 목적과 특화가 양보하는 성질을 설명한다.

</details>

#### 확인 Q08 · Scaling 그래프의 한계

Logarithmic transistor 그래프의 직선 상승, 이 단원 표의 2010년 행에 있는 10 GHz·IPC 10(?) 외삽, Dennard Scaling의 한계를 각각 해석하라. Core가 두 배이면 한 순차 작업도 두 배 빨라지는가?

<details><summary>해설 보기</summary>

Log 축의 비슷한 상승은 일정량 덧셈보다 곱셈적 성장을 나타낸다. Moore의 추세는 transistor 수이고 이 단원 표의 2010년 행은 측정 성과가 아닌 외삽이다. 원본 M001 PDF p.24의 오른쪽 끝 2010년 열을 행으로 옮긴 것이다. 역사 표의 IPC는 <0.1→0.1–0.9→0.9–2, MIPS/MFLOPS는 <0.2→0.2–20→20–2000으로 규모 변화를 보이지만 서로 다른 작업의 보편 점수는 아니다. Dennard는 더 작은 소자의 속도·전력 밀도 관계이며 leakage·overheating이 제약이다. Frequency·single-thread 성능의 증가 둔화는 완전 정지가 아니다. 여러 core는 독립 작업 처리량을 높일 수 있지만 한 작업의 latency 개선에는 내부 병렬화가 필요하며 공유 병목도 없어야 한다.

**채점·확인:** 측정·외삽, transistor·frequency, latency·throughput을 각각 구분한다.

</details>

### 적용 연습

#### 연습 P01 · 설계 설명의 오류 진단

새로 만든 합성 연습이다. Instruction과 data가 같은 memory에 있고 PC가 주소를 공급하는 두 설계 A·B가 같은 ISA를 구현한다. B에는 core가 더 많다. 한 설명자가 “같은 memory이므로 ISA도 구현도 동일하고, B의 모든 프로그램은 core 수만큼 빨라진다”고 한다. 이 설명을 저장 구조·구현·작업 병렬성으로 나누어 고쳐라.

연결: [EX:ca_2025_2_midterm_q01 p.2]의 저장 구조 판별을 근거 설명과 성능 주장 진단으로 확장했다. 선수 개념은 Q01·Q02·Q08이며 공식 원문이 확인되지 않은 복기본의 reasoning만 사용한다.

<details><summary>해설 보기</summary>

같은 memory에 두 종류를 저장한다는 조건은 stored-program 구성을 말한다. 그것만으로 두 ISA가 같아지는 것은 아니며 이 문제에서는 ISA가 같다는 조건을 따로 주었다. 같은 ISA도 core 수·cache·datapath가 다를 수 있다. B의 추가 core는 독립 작업이나 분할 가능한 작업에 유용하지만 순차 부분을 자동으로 나누지 않는다. 따라서 workload의 병렬성과 병목을 알아야 성능 비율을 주장할 수 있다.

**채점·확인:** 저장 특성에서 ISA 동일성을 추론하지 않고, 문제의 별도 조건과 구현 차이를 구별한다.

</details>

### 짧은 복습 계획

Q01–Q03으로 층위와 상태를 말로 설명한 뒤 Q05–Q07의 설계 절충을 비교하자. 다음 복습에서는 Q08의 그래프 해석과 P01의 오류 진단을 해설 없이 다시 해 보자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-01-lecture-01|2026-09-01 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]
- [lec 01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.01.pdf) — [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-011), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-016), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-019), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-021), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.01/page-027)
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-005), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-011), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-013), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-017), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-027)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-006)
- [[courses/computer_architecture/transcripts/2026-09-01|2026-09-01 보정 STT]] — 23:07, 30:22, 36:16, 40:38 (페이지 안의 시간 표기)
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 보정 STT]] — 03:13, 04:46, 05:32, 07:20, 08:20 (페이지 안의 시간 표기)

9월 3일의 실행 모형·operand 분류·ISA 역사와 확장성은 녹음 없는 자료 기반 복습이다. 9월 1일·8일 STT의 불확실한 말은 해설로 복원되지 않으며 상세 transistor 설계·OS scheduling·현행 제품 비교는 범위 밖이다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q01 p.2].
- [[exam_questions/ca_2025_2_midterm_q01|2025-2 중간 복기 Q1 · 기존 문제 미리보기]]
