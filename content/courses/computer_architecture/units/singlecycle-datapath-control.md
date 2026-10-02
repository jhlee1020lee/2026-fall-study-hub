---
title: "Single-cycle CPU의 상태·Datapath·Control"
description: "Single-cycle의 operand·주소·제어 경로와 clock 한계를 정리한다."
course: "computer_architecture"
unit_id: "singlecycle-datapath-control"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 05 typo fixed.pdf", "lec 05.pdf", "lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-10-lecture-04"]
---

Instruction의 상태 변화가 한 clock 안의 data·control 경로로 어떻게 구현되는지 보자. 값과 주소, mux 선택과 write enable을 나누어 회로를 추적한다.

## Architectural state를 다음 상태로 바꾸는 회로

ISA를 abstract finite-state machine(FSM, 유한 상태 기계)으로 보면, instruction 하나는 현재 program-visible state(PVS, 프로그램에 보이는 상태)를 다음 상태로 바꾸는 규칙이다. PC, architectural register, memory의 실행 전후 값이 그 규칙을 표현한다. 이 추상적인 “한 instruction당 한 상태 전이”는 물리적으로 한 clock을 써야 한다는 뜻도, 다른 processor의 memory 접근을 모두 차단한다는 뜻도 아니다. [CA RM001 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-006)

Single-cycle CPU는 이 상태 전이를 한 clock cycle 안에 구현한다. 현재 상태를 읽어 다음 값을 계산하는 combinational logic과, clock 경계에서 그 값을 받아들이는 저장소를 연결한다. 이 상세 회로 설명은 single-cycle instructor 자료를 읽는 선수 복습이다. 녹음이 없는 수업의 날짜나 전체 구두 진도를 추정하지 않는다. 관련 register·표현 규칙은 [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]], branch·procedure 의미는 [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트]]에서 연결할 수 있다.

### Combinational read와 synchronous write

[CA RM001 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-007)에서 register를 고르는 두 read select와 한 write select는 각각 5 bits이다. $2^5=32$이므로 32개 register 중 하나를 지정할 수 있다. Register **번호**가 5 bits인 것과 그 안의 **data**가 64 bits인 것은 다른 문제이다.

[CA RM001 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-008)의 교육용 “magic” memory/register file은 combinational read를 가정한다. Read select나 저장된 내용이 바뀌면 read data가 조합 경로를 따라 바뀐다. 반면 synchronous write는 positive clock edge에서 write enable이 켜져 있어야 선택된 저장소를 바꾼다. 설명용으로 현재 `x5=7`이고 write-data input에 10이 준비되어도 enable이 꺼져 있으면 `x5`는 7로 남는다. Control은 계산 결과뿐 아니라 **어디에, 언제 쓸지**도 정해야 한다.

이것은 단순한 timing 모형이다. 실제 DRAM·cache의 latency, port 수, clock 조건까지 같은 것으로 일반화하지 않는다. 원본 RM002의 해당 기술 설명과도 일치하지만 두 자료의 공지 버전과 원본 ID는 구별한다. [CA RM002 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-008)

## Instruction fetch와 register 산술의 경로

Datapath(데이터 경로)는 값과 주소를 처리하는 register, ALU, multiplexer(mux, 선택기), memory의 연결이다. IF, ID, EX, MEM, WB는 그 작업을 나누는 이름이다.

| 단계 | 역할 |
|---|---|
| IF | PC가 가리키는 instruction을 fetch |
| ID | Instruction을 decode하고 register operand를 읽음 |
| EX | ALU 연산 또는 effective address 계산 |
| MEM | 필요한 data-memory 접근 |
| WB | 결과를 register file로 write back |

Single-cycle에서는 이 이름들이 다섯 clock을 뜻하지 않는다. 한 cycle 안의 기능적 구분이다. [CA RM001 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-009) PC는 instruction memory의 read address이며 출력되는 32-bit instruction과 다르다. 별도 adder가 PC+4를 계산하여 이 자료의 4-byte instruction 다음 주소를 준비한다. [CA RM001 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-012)

`add rd,rs1,rs2`에서는 instruction의 `[19:15]`가 `rs1`, `[24:20]`이 `rs2`, `[11:7]`이 `rd`를 지정한다. 앞의 두 field가 고른 64-bit 값은 read port를 거쳐 ALU로 가고, 합이 `rd`의 write data로 돌아간다. 설명용으로 PC=100, source 값이 7과 5이면 destination에 12를 쓰고 PC는 104가 된다. `rd=x0`이라면 기존의 고정 zero 규칙을 유지한다. [CA RM001 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-013) [CA RM001 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-015)

이 instruction에는 data-memory read/write가 필요 없다. 그러나 **instruction fetch를 위한 memory 접근**은 여전히 필요하다. 같은 memory라는 단어 때문에 IF와 MEM을 하나로 합치면 유용한 실행 경로를 잘못 세게 된다.

## Immediate와 ALU 입력 선택

`addi rd,rs1,immediate12`는 source register에 signed immediate를 더해 destination에 쓰고 PC+4로 진행한다. Immediate Generator는 instruction 전체를 하나의 signed 수로 확장하는 장치가 아니다. Format에 필요한 field를 뽑거나 재조립해서 64-bit immediate 값을 만든다. [CA RM001 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-016) [CA RM001 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-017)

예를 들어 12-bit pattern `0xFFC`는 unsigned로 4092이지만 signed immediate로는 $4092-4096=-4$이다. Sign extension은 그 −4를 보존한다. 설명용 `x5=10`에 이 immediate를 더하면 결과는 6이다. Zero extension으로 4092를 더하는 것은 다른 instruction 의미를 만든다. 과거 복기 Q13(c)와 연결되는 reasoning도 “형식적으로 위를 채운다”에서 끝나지 않고 negative operand의 **값 보존**을 설명하는 것이다. [EX:ca_2025_2_midterm_q13 p.5] 이 연결은 공식 원문·정답이 독립 확인되지 않은 2025-2 복기 자료를 사용한다.

R-type은 ALU의 두 번째 입력에 register file의 Read data2를, immediate 산술은 immediate를 사용한다. 그 자리에 mux를 두고 ALUSrc로 고르면 첫 입력과 결과의 write-back 경로를 공유할 수 있다. Load/store도 base+offset을 계산하므로 같은 immediate 입력 경로를 쓴다. [CA RM001 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-018) [CA RM001 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-019)

다만 모든 format의 immediate를 같은 연속 12-bit field로 취급하면 안 된다. Store는 나뉜 두 조각을 재조립하며, branch는 흩어진 displacement bit와 생략된 low zero를 고려한다. RM001 p.17의 “selected 12 bits”는 개요이고, 정확한 branch 배치는 [CA M003 PDF p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062)를 함께 읽어야 한다. Sign extension은 sign-bit wire 복제, 고정 한 칸 shift는 wire 재배치로 표현할 수 있다. 이것은 임의 shift 양을 처리하는 일반 shifter 설계와 다르다. [CA RM001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027)

## Load와 store에서 주소와 data를 분리하기

Load의 ALU 결과는 가져올 **값**이 아니라 그 값의 **주소**이다. `lw`는 base register와 sign-extended offset을 더해 effective address(EA, 유효 주소)를 만들고, 그곳의 word를 읽어 destination으로 보낸다. `sw`도 같은 주소 계산을 하지만 memory에 쓸 data는 `rs2`에서 가져오며 일반 register를 쓰지 않는다. 설명용 base=1000, offset=12이면 두 경우의 EA는 모두 1012이지만 data의 이동 방향은 반대이다. [CA RM001 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-021) [CA RM001 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-022)

[CA RM001 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-023)에서는 register file의 두 번째 read data가 memory의 write-data input으로 별도로 이어진다. ALUSrc가 immediate를 선택해도 store data는 이 별도 경로로 전달될 수 있다. 또한 register로 돌아올 값은 ALU 결과일 수도, memory read 결과일 수도 있으므로 write-back mux가 필요하다.

| 신호 | 선택 또는 허용하는 것 |
|---|---|
| ALUSrc | ALU 두 번째 입력: Read data2 또는 immediate |
| MemtoReg | Register에 쓸 값: ALU result 또는 memory read data |
| MemRead | Data-memory read |
| MemWrite | Data-memory write |
| RegWrite | Register file write |

ALUSrc와 MemtoReg는 위치와 목적이 다르다. 하나는 **계산의 입력**, 다른 하나는 **저장할 결과의 출처**를 고른다.

여기의 `lw/sw`는 4-byte word 예이다. RV64의 `lw`는 word를 64 bits로 sign-extend하고 `sw`는 source의 하위 32 bits를 쓴다. 뒤의 control 표는 `ld/sd`라는 8-byte doubleword 예를 쓰므로 폭까지 같은 예로 합치지 않는다. [CA M003 PDF p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057) RM001 p.22의 남아 있는 “load 4-byte word” caption은 SW heading·mnemonic·상태 전이와 충돌하는 오기이다. 또한 `translate(EA)` 표기는 주소 변환의 추상 경계일 뿐, 여기서 virtual memory·exception·alignment 처리 회로를 완성한 것은 아니다.

## BEQ의 조건과 다음 PC

`beq`는 두 source register가 같으면 PC-relative target으로, 다르면 PC+4로 진행한다. 자료 회로는 ALU에서 두 값을 빼고 Zero 출력으로 같음을 판정한다. 별도 adder는 현재 PC에 signed branch displacement를 더한다. 이 BEQ 하위집합에서는 $PCSrc=Branch\land Zero$이므로 branch opcode라는 사실만으로 항상 target을 고르는 것은 아니다. [CA RM001 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-025) [CA RM001 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-026)

[CA RM001 PDF p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027)의 shift-left-1은 2-byte 단위 immediate를 byte displacement로 바꾸는 표시이다. 설명용 PC=100, target=200이면 차이는 100 bytes, 2-byte 단위 immediate는 50이다. 반면 SB field를 재조립할 때 low zero까지 붙여 이미 100을 만들었다면 다시 shift하면 안 된다. Immediate Generator가 어느 convention의 값을 내는지 일관되게 읽어야 한다.

`jal`은 조건 비교 없이 target으로 이동하면서 `rd`에 PC+4를 link로 남긴다. `rd=x0`이면 그 저장 결과를 버린다. RM001 p.28은 JAL 아래에 “branch if equal” caption과 `PC + (immediate20 << 2)`를 인쇄하지만, 조건 없는 JAL 의미와 그 페이지의 UJ field, [CA M003 PDF p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063)의 low-zero 규칙에 맞지 않는다. Target은 $\{imm[20],imm[19:12],imm[11],imm[10:1],0\}$를 signed byte displacement로 복원해 현재 PC에 더한다. 이는 source bit 배치에 근거한 명시적 해설 정정이다. 아래의 기본 datapath가 JAL/JALR의 link·target 경로까지 완성했다고 읽어서는 안 된다. [CA RM001 PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-028)

## Opcode에서 ALU control과 write enable까지

Single-cycle control은 현재 instruction의 combinational function이다. Decoder는 읽고 쓸 위치, ALU operation, mux 선택을 정한다. Opcode와 내부 control encoding은 서로 다른 층위이다. [CA RM001 PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-030) [CA RM001 PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-031)

[CA RM001 PDF p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-032)의 교육용 ALU에는 4-bit control이 있고 `0000=AND`, `0001=OR`, `0010=add`, `0110=subtract`이다. Main control이 opcode로 만든 2-bit ALUOp를 ALU control이 funct field와 함께 해석한다.

| Instruction | ALUOp | funct7 | funct3 | ALU action | 내부 ALU control |
|---|---|---|---|---|---|
| `ld/sd` | 00 | X | X | 주소 덧셈 | 0010 |
| `beq` | 01 | X | X | 비교용 뺄셈 | 0110 |
| R-type `add` | 10 | 0000000 | 000 | 덧셈 | 0010 |
| R-type `sub` | 10 | 0100000 | 000 | 뺄셈 | 0110 |
| R-type `and` | 10 | 0000000 | 111 | AND | 0000 |
| R-type `or` | 10 | 0000000 | 110 | OR | 0001 |

여기서 X는 해당 경우의 결과를 정하는 데 그 field를 보지 않는다는 뜻이다. 임의의 불명확한 hardware 값이 언제나 안전하다는 뜻은 아니다. [CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034)의 main control은 instruction `[6:0]`을 받고, ALU control은 ALUOp와 instruction `[30,14:12]`를 받는다. 이 제한된 합법 instruction 집합에서는 나머지 funct7 bits가 고정되어 필요한 구분 bit만 드러난다. ISA 전체의 instruction 검증을 이 선 몇 개로 모두 해결했다는 뜻은 아니다. p.31의 여러 branch/jump 표기도 모든 이름이 독립적인 canonical opcode라는 증거로 쓰지 않는다.

### Control 표를 값의 흐름으로 읽기

[CA RM001 PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-033)의 single-bit 신호를 함께 읽으면 다음과 같다.

| 종류 | ALUSrc | MemtoReg | RegWrite | MemRead | MemWrite | Branch | ALUOp |
|---|---:|---:|---:|---:|---:|---:|---|
| R-format | 0 | 0 | 1 | 0 | 0 | 0 | 10 |
| `ld` | 1 | 1 | 1 | 1 | 0 | 0 | 00 |
| `sd` | 1 | X | 0 | 0 | 1 | 0 | 00 |
| `beq` | 0 | X | 0 | 0 | 0 | 1 | 01 |

Store와 branch에서는 RegWrite=0이므로 MemtoReg가 무엇을 골라도 register를 바꾸지 않는다. 그래서 그 칸은 X이다. 그러나 store의 MemWrite는 memory 효과를 만드는 데 필요하므로 1이어야 한다.

![CA RM001 PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.05.typo.fixed/page-034.png)

이 그림을 볼 때 instruction에서 나오는 **field 선택선**, register·ALU·memory 사이의 **data 경로**, 파란색 **control 선**을 구별하자. R-type은 두 register → ALU → destination을 사용한다. Load는 base와 immediate → 주소 → memory → destination, store는 주소 계산과 별도로 `rs2` → memory write-data를 사용한다. BEQ는 두 register의 비교 결과와 PC-relative adder를 next-PC mux에서 결합한다. 다음 세 페이지의 highlight도 이 흐름을 구별해 보여 준다. [CA RM001 PDF p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-035) [CA RM001 PDF p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-036) [CA RM001 PDF p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-037)

Single-cycle에서는 fetch부터 필요한 최종 값까지 한 cycle 안에 안정되어야 한다. 따라서 가장 긴 load 경로를 기다릴 수 있는 공통 clock이 짧은 ALU instruction에도 적용된다. 복기 Q7을 검토할 때의 핵심은 가장 빠른 경로를 고르는 것이 아니라 **지원하는 모든 경로가 끝날 수 있는 경계**를 찾는 것이다. [EX:ca_2025_2_midterm_q07 p.2] 이것이 multi-cycle로 넘어가는 동기이다. [CA RM001 PDF p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-038) 실제 성능 우열은 다음 설계의 cycle 길이와 CPI를 함께 계산해야 하며, 이 교육용 control 표는 control 정의가 다른 현재 Lab1의 구현 정답으로 옮길 수 없다.

## 핵심 정리

- 조합 read와 clock edge에서의 허용된 write는 다르다.
- ALUSrc는 ALU 입력, MemtoReg는 register write-back 출처를 고른다.
- Branch는 조건과 target을 따로 계산하며 byte displacement를 두 번 shift하면 안 된다.
- 공통 clock은 가장 긴 지원 경로를 감당해야 한다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · 읽기와 쓰기의 경계

Register selector가 바뀔 때와 write data만 바뀔 때를 비교하라. 32개 register의 index 폭과 data 폭은 무엇이며 추상 FSM의 한 전이가 반드시 한 clock인가?

<details><summary>해설 보기</summary>

Index는 2^5=32이므로 5 bits, data는 64 bits이다. 조합 read는 selector·현재 내용에 따라 출력이 바뀐다. Write는 positive edge와 write enable이 있어야 저장 내용을 바꾼다. `x5=7`, write data=10이어도 enable=0이면 7이다. ISA는 PC·register·memory의 관찰 가능한 전후 의미를 정하고 한 clock/microcycles 선택은 구현이다. 다른 CPU의 모든 memory 접근 차단도 이 추상 전이에서 따르지 않는다.

**채점·확인:** Selector·data·enable·edge를 따로 설명한다.

</details>

#### 확인 Q02 · ADD의 정보 흐름

`add rd,rs1,rs2`에서 PC, 32-bit instruction, `[19:15]`, `[24:20]`, `[11:7]`, register data의 역할을 추적하라. PC=100, operand=7·5일 때 결과와 IF/ID/EX/MEM/WB의 의미는 무엇인가?

<details><summary>해설 보기</summary>

PC의 주소로 IF가 instruction을 읽고 ID에서 각 field가 `rs1`, `rs2`, `rd` 번호를 고른다. 두 64-bit read 값이 EX의 ALU에서 12가 되고 WB에서 `rd`로 돌아간다. PC는 104이다. `rd=x0`이면 쓰기 결과를 버린다. Data-memory MEM은 필요 없지만 instruction fetch는 필요하다. 다섯 이름은 single-cycle 안의 기능 구분이지 다섯 clock이나 완료된 pipeline이 아니다.

**채점·확인:** Instruction bits·register 번호·값을 섞지 않는다.

</details>

#### 확인 Q03 · Immediate와 ALUSrc

12-bit `0xFFC`를 signed로 확장해 10에 더하라. Immediate Generator가 instruction 전체를 확장하는가? R/I 산술과 load/store가 ALU를 공유하는 방법, store/branch field 및 고정 shift의 주의점도 설명하라.

<details><summary>해설 보기</summary>

4092−4096=−4이므로 64-bit로 늘려도 −4, 결과 6이다. Generator는 필요한 field를 뽑고 재조립한다. ALUSrc mux가 register Read data2 또는 immediate를 골라 같은 ALU·write-back을 쓴다. Load/store도 base+offset에 이 경로를 쓴다. Store immediate는 두 조각, branch displacement는 흩어진 bits와 low zero를 고려한다. Sign bit 복제와 고정 shift는 배선으로 표현할 수 있지만 일반 variable shifter와 다르다. 이미 byte displacement면 추가 shift하지 않는다.

**채점·확인:** 값 보존·입력 mux·format별 조립을 모두 답한다.

</details>

#### 확인 Q04 · Load와 store의 쓰기 대상

Base=1000, offset=12에서 `lw`와 `sw`의 EA·data 출처·write 대상을 비교하라. ALUSrc·MemtoReg·MemRead·MemWrite·RegWrite와 word/doubleword 폭도 구별하라.

<details><summary>해설 보기</summary>

둘의 EA는 1012이다. `lw`는 memory의 32-bit word를 읽어 64-bit로 sign-extend하여 `rd`에 쓰고 `sw`는 `rs2` 하위 32 bits를 memory에 쓰며 일반 register는 안 쓴다. ALUSrc는 주소 덧셈의 offset 입력, MemtoReg는 register로 돌아갈 ALU/memory 결과 선택이다. Store data는 Read data2에서 memory로 별도로 간다. MemRead/MemWrite/RegWrite는 해당 읽기·쓰기 허용이다. 뒤의 `ld/sd`는 8-byte라 word 예와 폭을 섞지 않는다. `translate(EA)`는 추상 경계이지 완전한 주소 변환 구현이 아니다.

**채점·확인:** EA를 load 값으로 오인하지 않고 input/result mux를 구별한다.

</details>

#### 확인 Q05 · BEQ와 JAL의 PC

PC=100, branch target=200에서 equality·Branch·Zero·PCSrc와 displacement 단위를 설명하라. Operand가 다르면 어디로 가는가? `jal`의 link·target과 자료 p.28의 오류는 무엇인가?

<details><summary>해설 보기</summary>

ALU 뺄셈의 Zero가 equality를 나타내며 BEQ subset에서 PCSrc=Branch AND Zero이다. 다르면 Branch=1이어도 PC=104이다. Target 차이는 100 bytes=50개의 2-byte 단위이고 low zero를 붙여 이미 100으로 복원했다면 다시 ×2하지 않는다. `jal`은 조건 없이 target으로 가며 `rd`에 PC+4=104를 남긴다(`x0`이면 버림). UJ displacement는 `{imm[20],imm[19:12],imm[11],imm[10:1],0}`를 signed byte 값으로 복원한다. p.28의 'branch if equal'과 `<<2`는 이 의미·layout과 충돌하는 원자료 표기다. 기본 datapath는 완전한 jump 구현이 아니다.

**채점·확인:** 조건·target·link를 따로 계산하고 원문 오류를 숨기지 않는다.

</details>

#### 확인 Q06 · 두 단계 ALU decoding

Main control과 ALU control의 입력·출력을 구분하라. `ld/sd`, `beq`, R-type `add/sub/and/or`의 ALUOp·funct 구분·내부 ALU control을 복원하라.

<details><summary>해설 보기</summary>

Main control은 opcode `[6:0]`에서 2-bit ALUOp 등을 만든다. ALU control은 ALUOp와 funct 정보(제한된 그림의 `[30,14:12]`)에서 4-bit 동작을 만든다. `ld/sd`: 00→add `0010`, `beq`: 01→sub `0110`, funct는 X이다. R형 ALUOp=10에서 `add`는 funct7/funct3=`0000000/000`→`0010`, `sub`는 `0100000/000`→`0110`, `and`는 `0000000/111`→`0000`, `or`는 `0000000/110`→`0001`이다. 내부 encoding은 ISA opcode와 다르고 제한된 합법 집합에서는 다른 funct7 bits가 고정되어 있다. X는 그 행을 결정할 때 안 보는 정보이지 임의 hardware unknown의 안전 보장이 아니다.

**채점·확인:** Class 선택과 funct 선택, 2-bit와 4-bit를 구별한다.

</details>

#### 확인 Q07 · Control 표를 경로로 읽기

(ALUSrc,MemtoReg,RegWrite,MemRead,MemWrite,Branch,ALUOp) 순서로 R형·`ld`·`sd`·`beq`를 쓰고 `sd/beq`의 X 이유를 설명하라. 각 경로의 활성 data 이동도 답하라.

<details><summary>해설 보기</summary>

R=(0,0,1,0,0,0,10), `ld`=(1,1,1,1,0,0,00), `sd`=(1,X,0,0,1,0,00), `beq`=(0,X,0,0,0,1,01)이다. R은 두 register→ALU→rd, load는 base+immediate→주소→memory→rd, store는 주소 계산과 별도 rs2→memory, BEQ는 비교 Zero와 PC-relative adder→next-PC mux이다. `sd/beq`는 RegWrite=0이라 MemtoReg가 register를 바꾸지 않아 X다. `sd`의 MemWrite는 실제 memory 효과를 내므로 1이어야 한다.

**채점·확인:** 모든 신호와 data 경로를 맞추고 X를 무조건 0으로 외우지 않는다.

</details>

#### 확인 Q08 · 공통 clock의 제약

짧은 ALU 경로에 맞춰 clock을 정하면 긴 load에 무슨 문제가 생기는가? Multi-cycle로 바꾸었다는 이름만으로 성능 향상이 확정되는가?

<details><summary>해설 보기</summary>

Load는 fetch·주소 계산·memory 읽기·write-back의 필요한 값이 경계까지 안정되어야 한다. 짧은 경로만 기다리면 유효한 값이 준비되기 전 저장할 수 있다. 공통 clock은 가장 긴 지원 경로를 감당하므로 짧은 명령에도 그 주기가 적용된다. Multi-cycle은 명령별 필요한 시간 분배를 허용하지만 실제 비교에는 cycle period×CPI, workload와 overhead가 필요하다.

**채점·확인:** 가장 빠른 경로가 아닌 가장 긴 필요한 경로를 기준으로 답한다.

</details>

### 적용 연습

#### 연습 P01 · 서로 독립된 두 결함

새로 만든 합성 연습이다. 한 교육용 single-cycle 설계의 R형 경로는 350 ps, load 경로는 570 ps이며 다른 경로는 더 짧다. 설계자는 350 ps clock을 선택하고 `addi`의 12-bit `0xFFC`를 zero-extend한다. `x5=10`에서 기대 결과와 잘못 계산한 값을 구하고 두 결함의 수정이 서로를 대신할 수 있는지 설명하라.

연결: [EX:ca_2025_2_midterm_q07 p.2]의 최장 경로 판단과 [EX:ca_2025_2_midterm_q13 p.5] (c)의 signed 값 보존을 기능·timing 결함의 분리로 확장했다. 선수는 Q01·Q03·Q08이며 Q13(a,b)의 전체 encoding 설계는 선택하지 않았다.

<details><summary>해설 보기</summary>

Signed `0xFFC`는 −4라 기대 합은 6이지만 zero extension은 4092를 만들어 4102를 계산한다. Sign extension을 고쳐도 350 ps clock은 570 ps load를 감당하지 못한다. 이 가정에서는 공통 period≥570 ps가 필요하다. 반대로 주기만 늘리면 틀린 operand 의미가 그대로다. 의미 보존과 경계까지 값의 안정은 별개의 조건이며 실제 회로 overhead는 따로 고려해야 한다.

**채점·확인:** 6·4102·570 ps와 두 결함의 독립성을 확인한다.

</details>

### 짧은 복습 계획

Q02–Q05는 data의 출발·도착을 그려 답하고 Q06–Q08의 control 표를 이유와 함께 복원하자. 다음 복습에서 P01의 두 오류를 별도로 진단하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · 관련 선수 개념]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트 · 관련 선수 개념]]
- [lec 05 typo fixed.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-009), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-013), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-019), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-023), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-028), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05.typo.fixed/page-038)
- [lec 05.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-006), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-008), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.05/page-038)
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-063)

상세 회로는 single-cycle 자료 기반 선수 복습이다. 연결된 9월 8일·10일 노트가 이 회로 전체의 당시 구두 진도를 증명하지 않는다. 'Magic' memory는 교육용 timing 모형이며 RM001과 RM002는 별도 버전이다. RM001 p.22의 load caption 및 p.28의 JAL 조건·shift 표기는 다른 의미·bit 배치와 충돌한다. Control encoding은 현재 Lab1 사양으로 옮길 수 없고 완전한 JAL/JALR·주소 변환 회로도 제시되지 않는다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q07 p.2], [EX:ca_2025_2_midterm_q13 p.5].
Q13은 (c)만 연결한다. (b)의 immediate×2 표기는 encoded 단위인지 복원된 byte displacement인지 구분해야 하며 (a,b) 전체 풀이를 제공한 것은 아니다.
