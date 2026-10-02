---
title: "Multi-cycle CPU의 datapath·제어와 성능"
description: "50 ps microcycle의 FSM·MasterEn·성능 계산을 연결한다."
course: "computer_architecture"
unit_id: "multicycle-datapath-control"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 06.pdf", "lec 03.pdf", "lec 05 typo fixed.pdf", "lec 04.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-29-lecture-05", "courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-10-lecture-04", "courses/computer_architecture/lectures/2026-09-15-lecture-05"]
---

명령마다 필요한 경로를 세고 그 경로에 맞는 완료 경계를 찾자. Clock을 짧게 만드는 효과는 CPI와 instruction mix까지 계산해야 판단할 수 있다.

## Instruction마다 다른 작업량과 공통 clock

Programmer-visible state(PVS, 프로그램에 보이는 상태)는 PC, architectural registers, memory처럼 프로그램 의미를 결정하는 상태이다. Single-cycle 구현은 현재 상태와 instruction에서 다음 상태를 계산하고 한 clock 경계에서 필요한 갱신을 끝낸다. 따라서 지원하는 instruction 중 가장 긴 경로를 감당할 만큼 공통 cycle이 길어야 한다. 9월 29일의 multi-cycle 설명은 짧은 instruction까지 그 경계를 기다리는 비효율에서 출발한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 04:01]] [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]

[CA NM002 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-003)–[CA NM002 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-004)의 회로를 읽을 때 PC의 **주소**, instruction의 **bits**, register가 담은 **data**를 나눈다. Instruction은 32 bits이며 `rs1=[19:15]`, `rs2=[24:20]`, `rd=[11:7]`, `opcode=[6:0]`이다. 선택된 register data와 주요 연산 경로는 64 bits이다. STT 04:01의 PC가 instruction을 저장한다는 표현은 이 배선과 맞지 않는다. PC는 instruction memory의 주소를 제공한다는 것이 그림에 근거한 해설이다.

| 단계 | 무엇을 하는가 | Instruction에 따른 차이 |
|---|---|---|
| IF | Instruction bits를 읽음 | 산술도 fetch는 필요 |
| ID | Decode와 register operand read | 자료의 JAL timing 예는 register read 생략 |
| EX | ALU 연산 | 산술 결과 또는 load/store 주소를 계산 |
| MEM | Data-memory read/write | R/I arithmetic에는 필요 없음 |
| WB | Destination register write | Load는 읽은 data, 산술은 ALU 결과를 기록 |

R/I-type **arithmetic**은 IF → ID → EX → WB를, `lw`는 다섯 작업을 모두 사용한다. I-type이라는 encoding만으로 MEM이 없다고 할 수는 없다. Load도 I-type일 수 있다. 04:56의 반복된 R-type 표현은 06:49의 보충과 자료를 함께 읽어 산술 R/I형으로 구분한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 04:56]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 06:49]]

ALU의 register/immediate 입력 선택, ALU/memory 결과의 write-back 선택, PC+4/target의 next-PC 선택은 서로 다른 mux 역할이다. Branch displacement의 shift-left-1도 encoding 단위에 관한 규칙이며 모든 immediate를 두 배로 만드는 연산이 아니다. 이 회로는 기본 subset을 설명하며 모든 jump 변형의 완성 구현은 아니다. [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034) 필요한 ISA 표현은 [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]], branch·link 의미는 [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트]]와 연결된다.

## Component delay로 가장 긴 경로 계산하기

[CA NM002 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005)는 memory read/write 200 ps, ALU add 100 ps, register file read/write 50 ps, 그 밖의 combinational logic 0 ps를 가정한다. 9월 29일 07:50도 이를 단순화한 예로 설명한다. Memory 크기에 관한 06:49의 상충 발언과 실제 memory의 지연은 이 가정과 구별한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 07:50]]

| 자료의 instruction 종류 | IF | ID | EX | MEM | WB | 합계 |
|---|---:|---:|---:|---:|---:|---:|
| R/I arithmetic | 200 | 50 | 100 | — | 50 | 400 ps |
| `lw` | 200 | 50 | 100 | 200 | 50 | 600 ps |
| `sw` | 200 | 50 | 100 | 200 | — | 550 ps |
| Bxx / JALR, WB 생략 조건 | 200 | 50 | 100 | — | — | 350 ps |
| JAL, ID·WB 생략 조건 | 200 | — | 100 | — | — | 300 ps |

Load의 600 ps에는 instruction fetch와 data-memory read가 각각 200 ps씩 들어간다. 이 subset의 single-cycle period는 최소 600 ps여야 하므로 이상적인 최대 frequency는

$$
f_{single}=\frac{1}{600\times10^{-12}\text{ s}}
\approx1.667\text{ GHz}.
$$

R-type의 유용한 경로는 400 ps여도 다음 공통 경계는 600 ps 뒤이다. 차이 200 ps는 timing 여유이며 산술 instruction이 실제 data memory를 반드시 읽었다는 뜻이 아니다.

### Jump의 link를 버려도 되는 경우와 보존해야 하는 경우

위 표의 취소된 WB는 모든 branch/jump의 보편 규칙이 아니다. Conditional branch는 PC 갱신만으로 끝날 수 있지만 `jal/jalr`가 `x0` 이외의 destination에 return address를 남긴다면 그 register 갱신을 빼면 instruction 의미가 사라진다. 9월 29일 08:47–09:40도 WB 생략을 조건부로 설명한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 08:47]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 09:40]]

따라서 표의 350/300 ps는 link를 보존하지 않아도 되는 표시된 경로의 값이다. Link-write가 필요한 경우의 완전한 추가 state schedule은 자료가 제공하지 않는다. 또한 0 ps mux·wire·control은 현실의 timing 보장이 아니라 계산을 단순화한 가정이다.

## 50 ps micro-cycle과 MasterEn

Multi-cycle의 첫 모형은 600 ps를 50 ps micro-cycle로 나누고 각 instruction에 필요한 개수만 사용한다. IF 200 ps는 4개, ID 50 ps는 1개, EX 100 ps는 2개, MEM 200 ps는 4개, WB 50 ps는 1개에 대응한다. R-type은 8개로 400 ps, load는 12개로 600 ps가 된다. [CA NM002 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-006) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 12:25]]

Clock을 빠르게 넣는 것만으로는 충분하지 않다. 계산이 아직 안정되지 않은 중간 clock에서 register나 memory에 쓰면 잘못된 결과가 남는다. MasterEn(master enable, 최종 상태 갱신 허용 신호)은 instruction의 sequence가 끝나는 경계에서 PVS 갱신을 허용한다. Controller의 state register는 그 사이에도 매 micro-cycle마다 진행한다.

MasterEn은 RegWrite나 MemWrite를 대신하지 않는다. Instruction별 신호는 **어떤 상태를 쓸지**, MasterEn은 이 초기 모형에서 **언제 완료된 효과를 허용할지**를 정한다. MasterEn=1이라고 모든 register와 memory를 쓰는 것도 아니다. [CA NM002 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-007) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 14:04]] 13:11에는 MasterEn=1에서도 갱신할 수 없다는 상충된 부정 표현이 있다. 여기서는 뒤 설명과 figure의 완료 전이를 따른다. 그 불명확한 발화를 새로 복원한 것은 아니다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 13:11]]

## FSM 경로에서 CPI 읽기

Finite-state machine(FSM, 유한 상태 기계)은 현재 state와 입력으로 다음 state와 control을 정한다. 이 예의 12개 state는 IF1–IF4, ID, EX1–EX2, MEM1–MEM4, WB이다. 네 IF state는 한 instruction의 200 ps fetch를 배분한 것이며 서로 다른 네 instruction을 뜻하지 않는다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 15:55]]

![CA NM002 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.06/page-008.png)

그림에서 대부분의 화살표는 다음 state로 진행하지만 IF4, EX2, MEM4에서는 instruction 종류에 따라 경로가 갈린다. 빨간 MasterEn=1 표시는 완료 뒤 IF1으로 돌아가는 **전이**에 붙어 있다. IF1에 머무는 동안 임의로 계속 쓴다는 뜻이 아니다.

| 종류 | 경로에서 세는 micro-cycle | CPI | 완료 전이 |
|---|---|---:|---|
| R/I arithmetic | 4 IF + 1 ID + 2 EX + 1 WB | 8 | WB → IF1 |
| `lw` | 4 IF + 1 ID + 2 EX + 4 MEM + 1 WB | 12 | WB → IF1 |
| `sw` | 4 IF + 1 ID + 2 EX + 4 MEM | 11 | MEM4 → IF1 |
| Bxx / JALR, WB 생략 조건 | 4 IF + 1 ID + 2 EX | 7 | EX2 → IF1 |
| JAL, ID·WB 생략 조건 | 4 IF + 2 EX | 6 | EX2 → IF1 |

JAL은 IF4에서 ID를 건너뛰어 EX1으로 간다. EX2 뒤 산술은 WB로, load/store는 MEM1로, 표의 branch/jump는 IF1으로 간다. MEM4에서는 load만 WB로 더 진행하고 store는 끝난다. [CA NM002 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-009)의 표는 같은 FSM을 표 형식으로 표현한 것이다. 전체 state가 12개라는 사실과 모든 instruction이 12개를 방문한다는 주장은 다르다. 다음 instruction의 IF1을 이전 instruction의 CPI에 하나 더 세지도 않는다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 18:48]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 22:23]]

이 초기 모형은 PVS에서 다음 PVS까지의 조합 경로와 최종 갱신을 다룬다. 이후 IR 등 중간 저장소를 추가하는 resource-reuse 설계의 PC 갱신 시점을 여기에 그대로 합쳐서는 안 된다.

## ROM microsequencer의 입력과 출력

FSM을 lookup table로 구현하면 current state와 instruction class가 입력이고, datapath control과 next state가 출력이다. 12개 state에는 $\lceil\log_2 12\rceil=4$ bits가 필요하다. NS3–NS0라는 네 next-state bit가 다음 clock의 state register로 돌아가 controller의 진행을 정한다. 이는 ALU의 계산 결과와 다른 출력이다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 20:43]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 21:41]]

[CA NM002 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-010)의 generic diagram에는 opcode 6 bits와 state 4 bits가 들어간다. 출력은 PCWrite, PCWriteCond, IorD, MemRead, MemWrite, IRWrite, MemtoReg, PCSource, ALUOp, ALUSrcA/B, RegWrite, RegDst와 next state 등이다. 이 명칭은 controller가 mux·ALU·write timing을 지시함을 보여 주지만 현재 Lab1의 signal 정의로 그대로 옮길 수는 없다.

RISC-V의 실제 opcode field는 `[6:0]`, 즉 7 bits이다. Generic figure의 6-bit opcode와 9월 29일 20:43의 “RISC-V opcode는 6”이라는 말을 혼합하면 안 된다. 그림 그대로는 입력 10 bits, $2^{10}=1024$ rows이다. 가상으로 raw RISC-V opcode 7 bits와 state 4 bits를 모두 주소로 쓰면 $2^{11}=2048$ rows이다. Instruction class로 먼저 decode하는 설계라면 폭은 다시 달라진다. [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034)

완전한 ROM 표의 저장량은 입력 $n$ bits, 출력 $m$ bits일 때 $m2^n$ bits이다. 설명용으로 $n=10,m=20$이면 20,480 bits, 입력 하나를 추가하면 40,960 bits, 출력 하나만 추가하면 21,504 bits이다. 행 수와 각 행의 폭을 구분해야 한다. 34:04의 $n2^n$ 구두 표기는 이 둘을 구분한 계산과 충돌하므로 그대로 일반식으로 채택하지 않는다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 34:04]] 이 수치는 최적화된 PLA의 gate 수나 지연을 직접 계산한 값도 아니다. 큰 table이 차지하는 면적과 반복되는 next-state 정보가 microcode 분리의 동기가 된다.

## Instruction mix로 비교하는 평균 실행시간

같은 binary와 실행 경로, 또는 명시적으로 같은 IC를 비교하면 $T=IC\times CPI_{avg}\times T_{clk}$이다. 같은 ISA라는 사실만으로 임의 프로그램의 IC가 같아지는 것은 아니다. 9월 29일 24:33은 한 program이 모든 cycle을 사용하는 조건에서 이를 wall-clock time이라 불렀다. 일반적인 I/O·대기·동시 작업 상황에서는 [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트]]의 CPU time과 elapsed time 구분을 유지한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 24:33]] [CA M006 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006)

Instruction-count 비중 $w_i$에 대해

$$
\sum_i w_i=1,\qquad
CPI_{avg}=\sum_iw_iCPI_i,
\qquad
IPC_{avg}=\frac{1}{\sum_i(w_i/IPC_i)}
$$

이며 각 종류의 rate는 $IPC_i=1/CPI_i$이다. 따라서 마지막 식은 같은 instruction-count weight의 weighted harmonic mean이다. Time 비중을 대신 넣거나 IPC의 arithmetic mean을 쓰면 총 instructions/총 cycles와 달라진다. [CA M006 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-018) 복기 Q5도 어떤 quantity와 weight를 평균하는지 먼저 밝혀야 하는 요구로 연결된다. [EX:ca_2025_2_midterm_q05 p.2] 공식 원문·정답이 검증되지 않은 복기 문장을 보편 평균 규칙으로 외우지 않는다.

### 자료의 두 mix를 각각 계산하기

[CA NM002 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-012)–[CA NM002 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-013)의 머리말은 SW 15%, ALU 40%인데 실제 식은 SW 10%, ALU 45%이다. 나머지는 같다. 이 충돌을 하나의 확정 입력으로 섞지 않는다.

| 종류 | CPI | 머리말 mix | 계산식 mix |
|---|---:|---:|---:|
| LW | 12 | 25% | 25% |
| SW | 11 | 15% | 10% |
| ALU | 8 | 40% | 45% |
| Branch | 7 | 15% | 15% |
| Jumps | 6 | 5% | 5% |

마지막 행의 6은 이 표의 JAL 경로이다. CPI 7인 JALR나 link-write가 필요한 jump에 같은 비용을 쓰는 일반화가 아니다.

계산식 mix는 $0.25(12)+0.10(11)+0.45(8)+0.15(7)+0.05(6)=9.05$이다. 머리말 mix는 $0.25(12)+0.15(11)+0.40(8)+0.15(7)+0.05(6)=9.20$이다. 50 ps micro-clock은 **20 GHz**이고, single-cycle의 600 ps는 약 1.667 GHz이다.

| 지표 | Single-cycle | 계산식 mix | 머리말 mix |
|---|---:|---:|---:|
| CPI | 1 | 9.05 | 9.20 |
| IPC | 1 | 0.110497 | 0.108696 |
| 평균 instruction 시간 | 600 ps | 452.5 ps | 460 ps |
| MIPS | 1666.667 | 2209.945 | 2173.913 |
| 같은 IC에서 speedup | 1 | 1.325967 | 1.304348 |

MIPS는 $IPC\times f_{MHz}$이다. 자료에 표시된 IPC 0.1104를 사용하면 $0.1104\times20000=2208$ MIPS라는 근사값이 나온다. 이를 정확한 $1/9.05$ 계산과 구분한다. STT의 26:18 수치, 28:07의 0.114, 29:06의 208, 31:04의 2.2 GHz는 일관된 단위 계산으로 확정된 발화가 아니다. 여기서는 식으로 재계산하며 **약 2.2 billion instructions/s와 20 billion cycles/s를 구별**한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 26:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 28:07]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 29:06]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 31:04]]

두 mix 모두 평균 CPI가 12보다 작아 이 이상적 모형에서 빨라진다. 모두 load라면 $12\times50=600$ ps로 같은 latency이다. 복기 Q8과 연결되는 판단도 “multi-cycle이면 항상 크게 빠르다”가 아니라 period, 필요한 cycle 수, workload와 overhead를 함께 비교하는 것이다. [EX:ca_2025_2_midterm_q08 p.2] 실제 control·latch overhead를 0으로 놓은 이 계산이 모든 구현의 성능 우위를 보장하지는 않는다.

## 핵심 정리

- R/I 산술의 ALU 결과는 data이고 load의 ALU 결과는 주소이다.
- MasterEn은 완료 경계의 PVS 갱신을 허용하며 controller 진행을 멈추지 않는다.
- CPI는 전체 state 수가 아니라 해당 instruction이 방문한 microcycle 수다.
- 50 ps는 20 GHz이고, 두 원자료 mix는 CPI 9.05와 9.20으로 따로 계산해야 한다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · 단계와 데이터 폭

R/I arithmetic과 `lw`의 IF·ID·EX·MEM·WB 경로를 비교하라. PC, 32-bit instruction의 세 register field와 opcode, 64-bit data, 세 종류 mux를 구분하라.

<details><summary>해설 보기</summary>

PC는 주소이고 IF가 instruction bits를 읽는다. `rs1=[19:15]`, `rs2=[24:20]`, `rd=[11:7]`, opcode=`[6:0]`이며 선택된 register data는 64 bits이다. 산술은 IF→ID→EX→WB, load는 EX의 EA 뒤 MEM에서 값을 읽어 WB한다. I-type이라는 format만으로 MEM이 없다고 하면 load를 놓친다. ALU register/immediate 입력, ALU/memory write-back 결과, PC+4/target 선택 mux는 역할이 다르다. Branch의 shift는 displacement 단위용이지 모든 immediate를 두 배로 만드는 규칙이 아니다.

**채점·확인:** PC와 instruction·index와 data, 산술 결과와 주소를 구별한다.

</details>

#### 확인 Q02 · 지연 합과 link 조건

Memory 200 ps, ALU 100 ps, register read/write 각각 50 ps, 기타 0 ps에서 산술·`lw`·`sw`·WB 없는 Bxx/JALR·ID/WB 없는 JAL의 경로 시간을 구하라. 공통 clock과 JAL link 조건도 답하라.

<details><summary>해설 보기</summary>

산술 200+50+100+50=400 ps, load는 MEM 200을 더해 600 ps, store는 WB 없이 550 ps, 표시된 Bxx/JALR는 350 ps, JAL은 300 ps이다. Load가 가장 길어 single-cycle≥600 ps, 최대 약 1.667 GHz이다. 산술의 200 ps 여유는 실제 memory read를 했다는 뜻이 아니다. `jal/jalr`가 `rd≠x0`에 link를 쓰면 register 갱신을 보존해야 한다. 표는 그 추가 schedule을 주지 않으므로 생략 경로의 수치를 모든 jump로 확대하지 않는다.

**채점·확인:** IF와 MEM을 둘 다 세고 조건부 jump 수치를 표시한다.

</details>

#### 확인 Q03 · MasterEn과 제어 진행

50 ps clock에서 IF·ID·EX·MEM·WB의 microcycle 수를 구하라. MasterEn=0이면 어떤 상태가 억제되고 무엇은 진행하는가? MasterEn=1이 모든 곳에 쓰라는 뜻인가?

<details><summary>해설 보기</summary>

각각 4·1·2·4·1이다. 초기 모형은 instruction sequence 끝에서만 architectural PVS 효과를 확정하고 controller state는 중간에도 IF1→IF2처럼 진행한다. 그렇지 않으면 완료 경계에 도달할 수 없다. MasterEn과 해당 RegWrite/MemWrite 등이 함께 어떤 쓰기를 허용하며 모든 위치에 쓰는 것은 아니다. 완료 전이의 신호이지 IF1에 있는 동안 계속 쓰는 신호가 아니다. 13:11의 상충 부정 표현은 14:04와 도식에 따른 해설과 구별한다.

**채점·확인:** 제어 state와 architectural state 및 when/what을 구분한다.

</details>

#### 확인 Q04 · FSM 경로와 CPI

12-state 모형의 각 instruction class CPI와 완료 전이를 구하고 IF4·EX2·MEM4의 분기 이유를 설명하라. 다음 IF1을 이전 CPI에 더하는가?

<details><summary>해설 보기</summary>

산술은 IF4개+ID+EX2개+WB=8, `lw`는 여기에 MEM4개로 12, `sw`는 WB 없이 11이다. Bxx/JALR 생략 경로는 7, JAL 생략 경로는 ID도 없어 6이다. IF4에서 JAL만 EX1로 바로 가며 EX2에서 산술→WB, load/store→MEM1, 표시된 branch/jump→IF1이다. MEM4에서 load→WB, store→IF1이다. MasterEn=1은 산술/load의 WB→IF1, store의 MEM4→IF1, 해당 branch/jump의 EX2→IF1에 붙는다. Next IF1은 다음 instruction의 첫 cycle이라 더하지 않는다. 12개 state를 모두 방문하는 것은 아니다.

**채점·확인:** 다섯 비용과 세 완료 전이를 실제 방문 수로 설명한다.

</details>

#### 확인 Q05 · ROM 행 수와 출력 폭

12-state controller의 state 폭, generic 6-bit opcode 입력 및 실제 7-bit RISC-V 입력의 ROM 행 수를 구하라. 10-input/20-output ROM에 입력 또는 출력 1 bit를 더한 용량과 control·NS 출력을 설명하라.

<details><summary>해설 보기</summary>

12개는 ceil(log2 12)=4 bits다. Generic 그림은 6+4=10 inputs→1024 rows, raw RISC-V라면 7+4=11→2048 rows다. Class predecode를 하면 다른 폭일 수 있다. n-input/m-output ROM 용량은 m×2^n: 20×1024=20,480 bits, 입력 추가는 40,960, 출력만 추가는 21,504 bits이다. Datapath control은 ALU·mux·read/write를 선택하고 NS3–NS0는 다음 state register 입력이다. `n×2^n` 구두 일반식이나 6-bit RISC-V 주장을 채택하지 않는다. 이 용량은 최적화된 PLA gate 수·delay와 같지 않다.

**채점·확인:** 입력은 행 수, 출력은 행 폭이라는 근거로 계산한다.

</details>

#### 확인 Q06 · 두 mix의 CPI와 시간

LW/SW/ALU/Branch/JAL CPI=(12,11,8,7,6)이다. 자료 머리말 mix=(25,15,40,15,5)%, 계산식 mix=(25,10,45,15,5)%를 각각 적용해 CPI·IPC·평균 시간·MIPS·600 ps 대비 speedup을 구하라. Microclock은 50 ps다.

<details><summary>해설 보기</summary>

계산식은 .25×12+.10×11+.45×8+.15×7+.05×6=9.05, 머리말은 .25×12+.15×11+.40×8+.15×7+.05×6=9.20이다.

|Mix|IPC|시간|MIPS|Speedup|
|---|---:|---:|---:|---:|
|계산식|1/9.05≈0.110497|452.5 ps|2209.945|1.325967|
|머리말|1/9.20≈0.108696|460 ps|2173.913|1.304348|

Clock은 1/(50×10^-12)=20 GHz=20000 MHz이고 MIPS=IPC×20000이다. 600 ps single-cycle은 CPI=1, 약1666.667 MIPS다. 자료의 rounded IPC .1104는 2208 MIPS를 주며 정확한 역수 계산과 구별한다. 두 비중 충돌을 섞지 않고 Jumps의 6은 WB 생략 JAL 경로로 한정한다.

**채점·확인:** 두 weight 합=1, 시간=CPI×50, speedup=600/시간을 확인한다.

</details>

#### 확인 Q07 · 평균 IPC와 비교 조건

Instruction-count weight w_i에서 CPI·IPC 식을 유도하고 IPC arithmetic mean의 함정을 설명하라. 모두 load인 경우와 같은 ISA지만 IC가 다른 경우도 평가하라.

<details><summary>해설 보기</summary>

총 cycles=IC Σw_i CPI_i, 따라서 CPI_avg=Σw_i CPI_i이고 IPC_avg=1/Σ(w_i/IPC_i)이다. 같은 count weight의 harmonic mean이며 time weight나 IPC arithmetic mean을 대신 넣지 않는다. 모두 load면 12×50=600 ps라 single-cycle과 같은 이상적 latency다. 일반 비교는 IC×CPI×period이며 같은 ISA만으로 IC가 같지 않다. 한 program이 모든 cycles를 사용하는 특수 조건 밖에서는 CPU time과 elapsed time도 구별한다. 약 2.2 billion instructions/s는 clock 2.2 GHz가 아니고 실제 overhead를 생략한 계산이 보편 우열을 보장하지 않는다.

**채점·확인:** 총 instructions/총 cycles로 검산하고 비교 전제를 명시한다.

</details>

### 적용 연습

#### 연습 P01 · Overhead가 결론을 바꾸는 경계

새로 만든 합성 연습이다. 동일 IC의 실행이 산술 50%·load 50%로 구성되고 CPI는 8·12다. Single-cycle은 600 ps, multi-cycle은 처음 50 ps다. 평균 CPI·IPC와 speedup을 구한 뒤 구현 overhead로 microperiod가 65 ps가 되면 다시 비교하라. 두 설계가 같아지는 microperiod는 얼마인가?

연결: [EX:ca_2025_2_midterm_q05 p.2]의 평균량·weight 판별과 [EX:ca_2025_2_midterm_q08 p.2]의 조건 없는 처리량 주장 검토를 결론이 뒤집히는 경계 문제로 옮겼다. 선수는 Q02·Q04·Q06·Q07이며 overhead 수치는 새 가정이다.

<details><summary>해설 보기</summary>

CPI=.5×8+.5×12=10, IPC=1/10=.1이다. 종류별 IPC의 산술 평균은 .5/8+.5/12≈.104167이라 총 cycles와 맞지 않는다. 50 ps에서는 명령당 500 ps, speedup=600/500=1.2다. 65 ps에서는 650 ps, speedup=600/650=12/13≈.9231로 더 느리다. 같아지는 period는 600/10=60 ps이다. Clock이 single-cycle보다 훨씬 빨라도 명령당 여러 cycles와 overhead를 곱해야 한다.

**채점·확인:** 같은 IC, harmonic 평균, 60 ps 경계와 우열 반전을 확인한다.

</details>

### 짧은 복습 계획

Q02–Q04에서 각 경로와 완료 전이를 다시 그린 뒤 Q05의 ROM 행·폭을 구하자. Q06–Q07의 두 mix를 분리 계산하고 P01에서 overhead 경계를 먼저 예측해 보자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트]]
- [lec 06.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-013)
- [lec 05 typo fixed.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf) — [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063)
- [lec 04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-018)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 보정 STT]] — 04:01, 04:56, 06:49, 07:50, 08:47, 09:40, 12:25, 13:11, 14:04, 15:55, 16:57, 18:48, 20:43, 21:41, 22:23, 24:33, 26:18, 28:07, 29:06, 31:04, 34:04 (페이지 안의 시간 표기)

9월 29일 설명은 제공되지 않은 이전 수업의 날짜·전체 진도를 확정하지 않는다. 0 ps 기타 logic·50 ps microclock은 이상적 수업 가정이다. JAL/JALR의 WB 생략은 link를 보존하지 않는 표시된 경로에만 적용한다. 6-bit generic opcode와 7-bit RISC-V opcode, 두 mix, MIPS·GHz의 상충 수치는 각각 구분한다. 초기 MasterEn 모형과 뒤의 IR 자원 공유 모형은 동일한 갱신 schedule이 아니다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q05 p.2], [EX:ca_2025_2_midterm_q08 p.2].
