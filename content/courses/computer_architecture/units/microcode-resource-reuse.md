---
title: "Microcode controller와 하드웨어 자원 공유"
description: "μPC·dispatch·공유 ALU·IR의 역할과 설계 절충을 연결한다."
course: "computer_architecture"
unit_id: "microcode-resource-reuse"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 06.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-29-lecture-05"]
---

Microcode는 반복되는 control 진행을 작은 program으로 표현한다. 자원 공유가 줄이는 회로와 그 대신 보존해야 하는 중간 값을 함께 살펴보자.

## 반복되는 next-state를 microprogram으로 표현하기

Multi-cycle controller는 instruction 종류와 현재 state를 보고 control output과 next state를 정한다. 모든 opcode·state 조합을 한 ROM에 저장하면, 여러 instruction이 같은 다음 state로 가는 정보도 반복해서 들어간다. 예를 들어 IF의 중간 state나 EX1에서 단순히 다음 state로 진행하는 규칙을 instruction마다 다시 저장할 필요가 있는지 생각할 수 있다. 9월 29일 35:59–39:27은 이 반복을 분리하는 발상으로 microcode controller를 소개한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 35:59]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 39:27]] [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]

Microprogram counter(마이크로프로그램 카운터, μPC)는 현재 **micro-state의 주소**이다. 사용자 프로그램에서 instruction 주소를 나타내는 PC와는 다른 상태이다. μPC로 μprogram ROM을 인덱싱하면 선택된 μinstruction의 field가 datapath control과 next-address 선택을 지정한다. 연속 state는 incrementer가 μPC+1을 계산하고, opcode에 따라 분기할 때는 작은 dispatch ROM의 target을 선택한다. [CA NM002 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014) 37:51의 lookup table 입력을 “micro instruction”이라 부르는 구절은 이 μPC-indexed 구조와 구분해 읽는다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 37:51]]

### AddrCtl과 두 dispatch ROM

![CA NM002 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-015.png)

그림에서 위쪽 state register가 현재 μPC를 보관하고, adder는 증가한 state를 만든다. Mux는 0으로 돌아가기, Dispatch ROM 1, Dispatch ROM 2, 증가한 state 중 하나를 골라 다음 μPC로 보낸다. μprogram의 control 출력이 AddrCtl을 정하므로, 데이터 처리뿐 아니라 다음 제어 위치를 고르는 것까지 작은 program처럼 동작한다.

| AddrCtl | 다음 state의 출처 |
|---:|---|
| 0 | State 0 |
| 1 | Dispatch ROM 1 |
| 2 | Dispatch ROM 2 |
| 3 | 현재 state + 1 |

설명용으로 현재 μPC=5, AddrCtl=3이면 다음 μPC는 6이다. 이 덧셈은 사용자 PC를 4 bytes 늘리는 것과 다르다. 이 그림에서는 microinstruction 주소의 다음 위치를 선택한다.

| 그림의 instruction 이름 | 그림의 6-bit opcode | Dispatch ROM 1 target | Dispatch ROM 2 target |
|---|---|---|---|
| R-format | 000000 | 0110 | — |
| jmp | 000010 | 1001 | — |
| beq | 000100 | 1000 | — |
| lw | 100011 | 0010 | 0011 |
| sw | 101011 | 0010 | 0101 |

첫 dispatch에서 lw와 sw는 같은 target으로 들어가 공통 부분을 사용할 수 있고, 두 번째 dispatch에서는 서로 다른 후속 경로로 갈라진다. 한편 대부분의 단순 next-state는 큰 opcode별 table 대신 incrementer로 표현된다. 이 분리가 반복을 줄이는 원리이며 정확한 면적·지연 감소량을 측정한 결과는 아니다.

**이 표의 opcode와 target 번호는 앞의 12-state RISC-V timing FSM과 다른 illustrative machine에 속한다.** 9월 29일 43:18과 44:26은 이전 FSM을 구현하는 예가 아니라고 명시한다. 따라서 `0110`을 앞 FSM의 특정 state에 임의 대응시키거나 `000000`을 실제 RISC-V R-type opcode로 외우면 안 된다. 41:27의 R-type target 구두 표현도 인쇄된 `0110`과 맞지 않으며, 여기서는 그림을 읽어 설명한 것이다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 41:27]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 43:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 44:26]]

## 한 ALU를 시간에 따라 재사용하기

Control 저장량뿐 아니라 datapath의 물리적 자원도 줄일 수 있다. Single-cycle 그림에서는 PC+4를 계산하는 adder와 register 산술을 하는 ALU가 따로 있어 같은 cycle에 일할 수 있다. Instruction을 여러 시점으로 나누면 PC+4가 필요한 시점과 EX 연산 시점이 달라져, 같은 ALU를 순차적으로 사용할 여지가 생긴다. [CA NM002 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-017) [CA NM002 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-018) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 45:27]]

[CA NM002 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020)에서는 ALU 입력 앞의 mux가 핵심이다.

| 필요한 작업 | ALU 입력의 출처 | 결과의 용도 |
|---|---|---|
| Sequential PC 계산 | PC와 상수 4 | 다음 순차 instruction 주소 |
| Register 산술 | Register file의 두 값 | 산술 결과 |
| Immediate를 쓰는 연산 | Register 값과 필요한 immediate | 해당 연산의 결과 또는 주소 |

9월 29일 47:25는 PC와 4를 고르는 시점과 register 값을 고르는 EX 시점을 대비한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 47:25]] ALU를 없애는 것이 아니라 **입력 출처와 사용 시점**을 바꾸어 재사용한다는 점이 중요하다.

Single-cycle도 서로 다른 instruction 사이에서는 같은 ALU를 사용한다. 여기서 추가한 아이디어는 **한 instruction의 서로 다른 단계** 사이에서도 같은 물리 자원을 쓰는 것이다. Adder 수를 줄이면 면적·제조 비용을 줄일 수 있지만, mux와 control, 중간 값 보존이 필요하고 원래의 동시 계산을 포기한다. 따라서 자원 절약만으로 항상 더 빠르다고 말할 수 없다.

이 예의 PC+4는 32-bit, 4-byte instruction 모형에 한정된다. “RISC-V instruction은 항상 4”라는 말을 제공되지 않은 모든 extension의 길이 규칙으로 확대하지 않는다. 또한 p.18의 16→32-bit immediate label은 older-style illustrative diagram의 폭이다. 앞의 RV64 32-bit instruction/64-bit datapath와 합쳐 하나의 구현 사양으로 만들면 안 된다.

## PC가 바뀌어도 현재 instruction을 보존하는 IR

PC가 instruction memory의 address input에 직접 연결되어 있으면 PC가 바뀔 때 조합 경로를 따라 instruction memory output도 바뀐다. Resource-reuse 설계에서 현재 instruction이 끝나기 전에 PC+4를 저장하면, 뒤 단계가 다음 instruction의 opcode와 register field를 잘못 읽을 수 있다. 9월 29일 48:04가 설명한 timing 문제이다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 48:04]]

![CA NM002 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-022.png)

그림의 Instruction Register(IR, 명령어 레지스터)는 **instruction memory의 output과 decode/register-file 쪽 사이**에 있다. 따라서 보존하는 것은 fetch한 instruction bits이다. 예를 들어 PC=A일 때 instruction $I_A$를 IR에 잡아 두면, PC가 A+4로 바뀌더라도 decode와 EX는 IR의 $I_A$를 계속 사용하여 현재 명령을 끝낼 수 있다. IR의 capture 시점을 제어하고 필요한 동안 유지하는 것이 해결의 핵심이다. [CA NM002 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021)

49:03과 49:43에는 IR가 previous instruction counter 또는 PC를 저장한다는 말과 위치·갱신 시점에 대한 망설임이 있다. 위의 **instruction bits 저장** 설명은 실제 배선에 근거한 note-side correction이며 그 발화를 복원한 것이 아니다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 49:03]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 49:43]]

강의의 “latch-based control”은 필요한 정보를 저장해 전파·갱신 경계를 만든다는 개념이다. 특정 latch의 active level, setup/hold, 두 phase 회로까지 이 그림이 정한 것은 아니다. 또한 초기 MasterEn 모형의 최종 PVS 갱신과 이 IR 도입 모형의 PC timing은 설계의 서로 다른 단계이므로 같은 micro-state에서 항상 갱신한다고 단정하지 않는다.

## Shared memory와 중간 실행 상태

9월 29일 52:36은 instruction memory와 data memory도 재사용할 수 있다고 짧게 소개하고 세부 내용은 다음 주로 미룬다. 따라서 다음 [CA NM002 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023)의 block reading은 **자료 기반 보충**이다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 52:36]]

단일 memory를 IF와 data access에 서로 다른 시점에 쓰려면 해당 시점의 주소를 선택해야 한다. 한 작업에서 읽은 값을 다음 작업까지 유지하는 내부 저장소도 필요하다.

| 내부 저장소 | 그림에서 보존하는 정보 | 필요한 이유 |
|---|---|---|
| IR | Fetch한 instruction bits | 이후 decode·실행 중 field 유지 |
| Memory Data Register(MDR) | Memory에서 읽은 data | Load 결과를 WB까지 보존 |
| A, B | Register file의 두 read 값 | 이후 단계에서 operand 사용 |
| ALUOut | ALU 계산 결과 | 주소·결과를 다음 단계까지 유지 |

Load를 따라 생각하면 instruction을 IR에 보관한 뒤 base와 immediate로 EA를 계산하고, 그 주소를 memory 접근까지 유지해야 한다. Memory에서 읽은 data도 WB 때까지 남아 있어야 한다. Store에서는 주소와 함께 저장할 operand도 memory 단계까지 필요하다. 이것은 block의 정보 보존 목적을 설명하며 IR/MDR enable이나 모든 instruction의 완전한 control schedule을 만들어 낸 것은 아니다.

이 내부 register들은 software가 직접 지정하는 architectural general-purpose register와 구별된다. 한 instruction의 IF와 data access가 단일 memory를 시간차로 쓰는 것과 여러 instruction이 겹쳐 진행하는 pipeline도 다른 문제이다. 50:46–51:38의 pipeline 예고는 앞 instruction이 EX를 쓰는 동안 비어 있는 IF/ID에서 다음 작업을 진행할 수 있다는 동기까지이다. Hazard, forwarding, flush와 실제 pipeline CPI는 여기서 전개되지 않았다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 50:46]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 51:38]]

## Datapath와 microcode 사이에 복잡성을 배분하기

Microcontroller는 state를 세기만 하는 장치에서 더 나아가 sequence와 분기를 수행하는 작은 processor처럼 볼 수 있다. 여러 단순 동작을 μprogram으로 배열하면 더 복잡한 instruction이나 처음 예상하지 않은 동작을 지원할 수 있는지 생각할 수 있다. 긴 sequence와 반복에는 loop counter 같은 μISA 내부 상태가 더 필요할 수 있다. 이 상태를 늘리는 것은 사용자에게 보이는 register를 늘리는 것과 다르다. [CA NM002 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)

| 자료의 설계 방향 | 자원을 배분하는 방식 | 원리에서 따라오는 고려 사항 |
|---|---|---|
| Complex datapath + simple microcoding | 필요한 일을 회로에 직접 많이 배치 | Sequence를 단순하게 할 여지, 회로 면적·설계 부담 |
| Simple datapath + complex microcoding | 단순 자원을 여러 micro-operation으로 재사용 | Sequence 길이, control 저장량, 내부 상태 부담 |
| Simple datapath + simple microcoding | 단순한 instruction과 datapath/control을 함께 유지 | 지원 기능과 단순성 사이의 선택 |

세 방향의 장단점은 자원과 순차 실행 원리에서 도출한 해설이며 어느 방식이 항상 더 빠르거나 싸다는 측정 결론이 아니다. Loop counter와 정식 비교 문구는 slide detail이고, main processor와 microcontroller 중 어디에 일을 둘지 선택한다는 질문은 9월 29일 53:36–54:28에서 직접 확인된다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 53:36]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 54:28]]

복기 Q16(a)의 microcoded multi-cycle 쪽도 이런 방식으로 접근할 수 있다. 먼저 instruction을 어떤 sequence로 실행하고 자원을 언제 재사용하는지 설명한 뒤, 그 sequence 길이와 clock period가 latency에 주는 영향을 따진다. [EX:ca_2025_2_midterm_q16 p.8] 같은 문항의 hardwired pipeline 쪽 완전한 비교는 이후 pipeline 학습이 필요하다. 이 복기 자료는 공식 원문·정답이 검증된 것이 아니며, “microcoded”라는 이름만으로 보편적인 성능 우열을 결정할 수 없다. 자료의 x86/CISC 예시 역시 특정 현대 제품의 microcode 구조나 update 절차를 확인한 설명은 아니다.

## 핵심 정리

- μPC는 microinstruction 주소이고 사용자 PC와 다른 상태다.
- Incrementer는 공통 순차 진행을, dispatch ROM은 종류별 분기를 맡는다.
- 한 ALU를 PC+4와 EX에 공유하려면 입력 선택과 중간 값 보존이 필요하다.
- IR는 instruction bits, MDR는 load data를 보존하며 pipeline overlap과 시간 공유는 다르다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · μPC와 AddrCtl

Monolithic ROM의 반복을 어떻게 나누는가? μPC·μprogram ROM·μinstruction·incrementer·dispatch와 AddrCtl 0–3의 역할을 설명하고 μPC=5, AddrCtl=3을 추적하라.

<details><summary>해설 보기</summary>

여러 opcode에서 같은 next-state를 반복 저장하는 대신 μPC가 μprogram ROM의 μinstruction을 고르고 그 field가 datapath control과 다음 주소 선택을 지정한다. 공통 진행은 incrementer, opcode별 분기는 작은 dispatch ROM이다. AddrCtl 0=state0, 1=dispatch1, 2=dispatch2, 3=현재+1이므로 예의 다음 μPC는 6이다. 사용자 PC의 instruction 주소·4-byte 증가와 다르다. 중복 감소 원리는 있지만 정확한 면적·delay 절감량은 측정되지 않았다.

**채점·확인:** ROM 주소 입력과 선택된 instruction 출력, PC와 μPC를 구별한다.

</details>

#### 확인 Q02 · 두 dispatch table

그림의 dispatch1에서 R-format·jmp·beq·lw·sw target과 dispatch2의 lw·sw target을 써라. 두 memory 명령이 처음 같고 나중 다른 이유와 이전 FSM 번호로 옮길 수 없는 이유는 무엇인가?

<details><summary>해설 보기</summary>

그림의 (opcode→target)은 R `000000→0110`, jmp `000010→1001`, beq `000100→1000`, lw `100011→0010`, sw `101011→0010`이다. Dispatch2는 lw→`0011`, sw→`0101`이다. 공통 작업은 공유하고 후속 load/store 경로는 분리한다. 이 예는 별도 machine이므로 target `0110`을 앞 FSM의 EX1 등에 대응시키거나 6-bit R opcode를 실제 RISC-V로 외우면 안 된다. 41:27 구두 target과 인쇄값의 차이도 유지한다.

**채점·확인:** 두 표의 차이와 state 번호의 해당 예제 한정을 설명한다.

</details>

#### 확인 Q03 · ALU의 시간 공유

PC+4와 register EX 연산을 한 ALU로 수행하려면 입력과 사용 시점을 어떻게 바꾸는가? Single-cycle도 ALU를 공유한다는 말과 여기서의 추가 공유를 구별하라.

<details><summary>해설 보기</summary>

PC 계산 때 PC와 상수4, EX 때 register 둘 또는 register와 immediate를 mux로 선택한다. Single-cycle의 서로 다른 instruction 간 공유에 더해 한 instruction의 단계 사이에서 순차 공유한다. Adder 수·면적을 줄일 수 있지만 mux·단계별 control·결과 보존이 필요하고 동시 계산을 포기한다. PC+4는 여기의 4-byte instruction 가정이다. Older diagram의 16→32 immediate를 앞 RV64 data 폭과 합쳐 사양으로 만들지 않는다.

**채점·확인:** 어떤 입력이 언제 필요한지와 공유 비용을 모두 답한다.

</details>

#### 확인 Q04 · IR가 막는 잘못된 decode

현재 instruction을 끝내기 전에 PC가 A→A+4로 변한다. Instruction memory에 직접 연결된 decode의 문제와 IR의 위치·내용·capture 조건을 설명하라.

<details><summary>해설 보기</summary>

조합 memory output이 A+4의 다른 instruction으로 바뀌어 남은 단계가 잘못된 opcode·register field를 볼 수 있다. Instruction-memory output과 decode 사이의 IR에 A에서 fetch한 instruction bits를 저장하고 필요한 동안 유지한다. 저장하는 것은 A 자체가 아니다. Capture 시점을 제어해야 하지만 그림은 latch active level·setup/hold·two-phase 구현을 지정하지 않는다. 49:03·49:43의 PC 저장 표현은 배선과 구분한 해설 정정이며 초기 MasterEn 모델의 PC timing과도 섞지 않는다.

**채점·확인:** 문제의 전파 경로와 보존할 정보, unspecified timing을 구별한다.

</details>

#### 확인 Q05 · 중간 register의 정보

IR·MDR·A·B·ALUOut에 보존하는 것과 load/store에서 필요한 이유를 답하라. 하나의 memory를 시간 공유하는 것이 pipeline overlap과 같은가?

<details><summary>해설 보기</summary>

IR는 instruction bits, MDR는 memory read data, A·B는 두 register read 값, ALUOut은 계산 결과·주소를 보존한다. Load는 EA를 memory 접근까지, 읽은 값을 WB까지 유지해야 하며 store는 주소와 저장 data를 둘 다 유지해야 한다. IF와 data 접근에 단일 memory를 번갈아 쓰므로 주소 선택도 필요하다. 이들은 내부 실행 상태로 software가 직접 지정하는 GPR와 다르다. Pipeline은 여러 instruction의 중첩이므로 한 instruction 안의 시간 공유와 다르다. 상세 block reading은 자료 보충이며 enable schedule·hazard·forwarding·flush·pipeline CPI는 아직 주어지지 않았다.

**채점·확인:** 다섯 저장소의 역할과 load/store 값의 생존 기간을 설명한다.

</details>

#### 확인 Q06 · 복잡성을 어디에 둘 것인가

Complex datapath/simple microcoding, simple datapath/complex microcoding, simple/simple 세 방향을 비교하라. Loop counter 같은 μISA state는 왜 필요하며 architectural register와 같은가?

<details><summary>해설 보기</summary>

전용 회로에 일을 두면 sequence를 짧고 단순하게 할 여지가 있지만 회로 면적·설계 비용이 든다. 단순 자원을 μprogram으로 반복하면 공유가 가능하나 sequence 길이·control memory·내부 상태 비용이 생긴다. Simple/simple은 지원 instruction과 datapath/control을 함께 단순화하는 방향이다. 반복 작업 진행을 위해 loop counter 같은 내부 상태가 필요할 수 있지만 software에 노출된 register를 늘리는 것과 다르다. 설계 방향이지 RISC/CISC 전체의 속도·비용 순위나 현대 x86 구현 사실은 아니다.

**채점·확인:** 세 방향과 sequence·면적·내부 상태의 교환을 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 공유 설계의 비교 조건

새로 만든 합성 연습이다. 같은 architectural 효과를 내는 설계 A는 전용 adder와 짧은 μsequence, B는 공유 ALU와 더 긴 μsequence를 사용한다. B의 clock은 더 빠르다고만 알려져 있다. B가 반드시 latency가 짧다는 결론을 평가하고, 비교에 필요한 수치와 PC 조기 갱신 시 보존할 정보를 제시하라.

연결: [EX:ca_2025_2_midterm_q16 p.8] (a)의 microcoded multi-cycle reasoning을 자원·시간·정확성 조건의 비교로 옮겼다. 선수는 앞 단원의 CPI×period와 Q03·Q04·Q06이다. (b)의 hardwired pipeline 비교는 후속 선수학습이 필요해 유보한다.

<details><summary>해설 보기</summary>

Latency는 필요한 microcycle 수×period이므로 빠른 clock만으로는 더 긴 sequence의 비용을 상쇄했는지 알 수 없다. 각 instruction 경로의 count·period·overhead와 workload를 알아야 한다. 면적도 없앤 adder뿐 아니라 mux·control·저장소를 함께 본다. PC가 먼저 바뀌면 IR로 현재 instruction bits를 유지하고 중간 결과도 다음 소비 시점까지 보존해야 한다. 정확한 capture schedule은 자료 밖이라 임의로 정하지 않는다. 따라서 B의 resource reuse는 설명할 수 있어도 보편적인 latency/throughput 우위는 결론낼 수 없다.

**채점·확인:** 부족한 수치를 명시하고 정확성 조건을 성능 비교와 함께 점검한다.

</details>

### 짧은 복습 계획

Q01–Q02에서 μPC와 두 dispatch를 손으로 trace하고 Q03–Q05에서 값이 살아 있어야 할 기간을 표시하자. Q06과 P01은 시간·면적·내부 상태를 함께 비교해 답하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]
- [lec 06.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf) — [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-018), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 보정 STT]] — 35:59, 37:51, 39:27, 41:27, 43:18, 44:26, 45:27, 47:25, 48:04, 49:03, 49:43, 50:46, 51:38, 52:36, 53:36, 54:28 (페이지 안의 시간 표기)

Dispatch의 6-bit opcode와 state 번호는 앞의 12-state RISC-V FSM과 다른 예다. 구두 target 및 ROM 입력 표현의 충돌을 그림으로 해설하되 발화를 복원하지 않는다. IR는 PC가 아니라 instruction bits를 담는다. Shared memory의 IR·MDR·A·B·ALUOut 상세와 loop counter는 자료 보충이며 9월 29일은 pipeline 동기만 예고했다. Latch의 세부 timing, 전체 control schedule, 현대 제품의 microcode/update는 범위 밖이다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q16 p.8].
- [[exam_questions/ca_2025_2_midterm_q16|2025-2 중간 복기 Q16 · 기존 문제 미리보기]]
Q16은 (a)의 microcoded 측면만 연결하며 (b)의 hardwired pipeline 비교는 후속 학습이 필요하다.
