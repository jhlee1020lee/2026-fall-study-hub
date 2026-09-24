---
title: "Instruction의 비트 표현과 주소 구성"
description: "R/I/S field, PC-relative 변위와 signed immediate를 이용한 큰 상수 구성을 확인한다."
course: "computer_architecture"
unit_id: "instruction-encoding"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-10-lecture-04"]
---

Instruction의 각 field가 연산·register 번호·상수·변위를 어떻게 나타내는지 해독한다. 값의 부호와 byte 단위를 끝까지 유지하면 format 선택, branch 거리, 큰 상수 구성의 오류를 같은 원리로 점검할 수 있다.

## Machine code와 Hexadecimal

Instruction도 memory에서는 bit pattern이다. 그 bit를 연산과 operand로 해석하려면 instruction encoding(명령어 부호화) 규칙이 필요하다. Binary로 표현된 instruction을 machine code(기계어), 사람이 읽는 이름과 operand 표기를 assembly code(어셈블리 코드)라고 한다. [Register와 데이터 표현](data-register-memory.md)을 이해했다면 이제 **값을 계산하는 instruction 자체를 어떤 bit로 표현하는가**를 살펴볼 수 있다.

수업은 적은 수의 format을 갖는 기본 32-bit RISC-V instruction을 다룬다. 일정한 길이와 반복되는 field 위치는 decode(해독)의 규칙성을 높인다. 이는 모든 RISC-V 확장이나 다른 ISA의 instruction 길이가 항상 32 bits라는 주장은 아니다. Hexadecimal(16진법)은 한 digit으로 4 bits를 나타내어 긴 pattern을 간결하게 쓴다. [[page_cache/computer_architecture/lec.03/page-023|CA M003 p.23]]의 예는 다음과 같다.

```text
hex:     e    c    a    8    6    4    2    0
binary: 1110 1100 1010 1000 0110 0100 0010 0000
```

이 표기는 bit를 바꾸지 않고 묶어 읽는 방법만 바꾼다. 또 프로그램도 data로 표현되므로 한 프로그램이 다른 프로그램을 읽고 바꿀 수 있다. M003 p.29는 memory 안에 accounting program, editor, C compiler의 machine code와 payroll data, book text, editor의 C source를 함께 놓는다. Compiler가 source를 처리하고 linker가 object를 처리하는 일이 가능한 이유다. Standardized ISA는 같은 binary instruction의 의미를 공유하게 해 binary compatibility(이진 호환성)의 기반이 되지만 프로그램 전체에는 실행 환경 조건도 필요하다. 이 그림의 compiler/linker 해설은 자료 기반 보충이다.

## R-format: Register 번호와 Operation을 담는 Field

R-format(레지스터 형식)은 두 register를 읽어 하나에 결과를 쓰는 연산에 필요한 정보를 담는다. 상위 bit에서 하위 bit로 읽으면 다음과 같다. [[page_cache/computer_architecture/lec.03/page-025|CA M003 p.25]]

| Bits | Field | 폭 | 의미 |
|---|---|---|---|
| 31:25 | `funct7` | 7 | 연산을 더 세분하는 code |
| 24:20 | `rs2` | 5 | 두 번째 source register 번호 |
| 19:15 | `rs1` | 5 | 첫 번째 source register 번호 |
| 14:12 | `funct3` | 3 | 연산을 더 세분하는 code |
| 11:7 | `rd` | 5 | Destination register 번호 |
| 6:0 | `opcode` | 7 | Operation code |

폭의 합은 `7+5+5+3+5+7=32`다. Register가 32개이므로 번호를 고르는 데 5 bits가 필요하다. Field에 들어가는 것은 register의 현재 **값**이 아니라 **번호**다. `rs1=20`이면 실행할 때 `x20`의 값을 읽는다는 뜻이다. 연산은 `opcode` 하나만이 아니라 `funct3`·`funct7`과 함께 구분한다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 59:09]]

자료의 `add x9,x20,x21`을 구성해 보자. `rd=9`, `rs1=20`, `rs2=21`이고 `funct7=0`, `funct3=0`, `opcode=51=0x33`이다.

```text
funct7   rs2   rs1  funct3  rd   opcode
0000000 10101 10100   000  01001 0110011

0000 0001 0101 1010 0000 0100 1011 0011
= 0x015A04B3
```

Field의 경계를 기준으로 조립한 뒤 4 bits씩 다시 묶으면 [[page_cache/computer_architecture/lec.03/page-026|CA M003 p.26]]의 hex 값이 나온다. Assembly의 operand 순서인 `rd,rs1,rs2`와 word 안에서 보이는 field 순서는 같지 않으므로 위치를 따로 확인해야 한다.

## I-format과 S-format의 공통 위치

Immediate arithmetic와 load는 두 번째 source register 대신 immediate(즉시값)를 필요로 한다. I-format은 상위부터 `imm[11:0] | rs1 | funct3 | rd | opcode`이며 폭은 `12+5+3+5+7`이다. `addi`에서는 `rs1`의 값과 constant로 계산하고, load에서는 `GPR[rs1]+sign_extend(immediate)`가 memory 주소이며 읽은 값이 `rd`에 간다. I-format은 load 전용이 아니다. [[page_cache/computer_architecture/lec.03/page-027|CA M003 p.27]]

일반 signed 12-bit immediate의 범위는 `−2048…2047`이다. RV64에서 이를 값으로 사용하려면 sign bit인 `imm[11]`을 위쪽 52 bits에 복제한다. 예를 들어 12-bit `111111111100`은 −4이므로 base에서 네 bytes 뒤가 아니라 **네 bytes 앞**을 나타낼 수 있다. Zero extension을 하면 4092로 바뀐다. 이 보존 원리가 복기 Q4와 Q13(c)의 연결점이다. [EX:ca_2025_2_midterm_q04 p.2] [EX:ca_2025_2_midterm_q13 p.5]

Store에는 base address와 저장할 data라는 두 register 입력이 필요하지만 결과 register는 필요 없다. S-format은 다음처럼 바뀐다.

```text
I: imm[11:0]       | rs1 | funct3 | rd       | opcode
S: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
```

`sd x9,96(x22)`에서는 `x22`가 base, `x9`가 data다. 둘 다 읽는 입력이며 memory가 목적지다. S-format은 R-format의 `rs1` 위치인 bits 19:15와 `rs2` 위치인 bits 24:20을 유지하면서 남은 공간에 immediate를 7+5 bits로 나눈다. R/I-format의 `rd` 위치는 bits 11:7로 같지만 S-format의 그 자리는 immediate 하위 부분이다. [[page_cache/computer_architecture/lec.03/page-028|CA M003 p.28]]

이 배치는 operand 요구가 달라져도 register 선택 위치와 전체 길이를 최대한 규칙적으로 유지하는 절충이다. 9월 8일 01:03:54–01:04:49에서도 두 source 위치를 유지하려 immediate를 나눈다고 설명했다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 01:03:54–01:04:49]] 복기 Q13(a)에서는 field 이름을 외우는 것보다 이 설계 이유를 설명하는 깊이가 필요하다. [EX:ca_2025_2_midterm_q13 p.5]

## PC-relative Branch와 Jump의 거리

Label은 사람이 읽기 위한 이름이고 assembler가 실제 배치에 맞는 주소·변위로 바꾼다. PC-relative addressing(PC 기준 상대 주소 지정)은 target의 절대 주소 대신 현재 instruction과의 거리를 쓴다. Branch target이 대개 가깝기 때문에 짧은 field로 유용한 범위를 표현할 수 있다. 또한 함께 이동한 코드에서 source와 target에 같은 값 `k`를 더하면 `(target+k)−(PC+k)=target−PC`라서 내부 거리는 변하지 않는다. 두 번째 성질은 주소식에서 도출한 설명이며 복기 Q13(b)의 절대 주소와 상대 주소 비교에 연결된다. [EX:ca_2025_2_midterm_q13 p.5]

M003 p.62는 `target = PC + immediate × 2`라고 표현한다. 여기서 immediate는 **2-byte 단위의 거리**다. 9월 10일의 `PC=100`, `target=200` 예에서는 byte 차이가 100이고 그 단위 값은 50이다. 반대로 200에서 100으로 가면 −100 bytes, 즉 −50 단위다. 기준 PC는 branch 자신의 주소다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 01:05:39]]

[[page_cache/computer_architecture/lec.03/page-062|CA M003 p.62]]의 SB-format에서는 immediate 조각들이 word 안에 흩어져 있다. 그림에서 왼쪽의 `imm[12]`와 오른쪽의 `imm[11]`을 놓치지 않고 다음 순서로 재조립한다.

```text
SB byte displacement: imm[12] | imm[11] | imm[10:5] | imm[4:1] | 0
UJ byte displacement: imm[20] | imm[19:12] | imm[11] | imm[10:1] | 0
```

재조립한 결과를 sign-extend하면 이미 **byte 변위**다. 여기에 다시 2를 곱하면 거리가 두 배가 된다. SB의 저장된 12 bits와 생략된 최하위 0으로부터 표현 범위는 −4096…4094 bytes, 간격은 2 bytes다. 표현 가능한 변위와 실행 가능한 instruction의 정렬 조건은 별개다. 여기의 기본 32-bit instruction 예에서는 instruction 시작 주소가 4-byte 간격이다.

`jal`의 UJ-format은 더 많은 immediate bits로 더 넓은 PC-relative 범위를 표현한다. 실제 field 배치는 `imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode`이며, 위의 수치 복원 순서와 구분해야 한다. [[page_cache/computer_architecture/lec.03/page-063|CA M003 p.63]]

## LUI와 Signed immediate를 이용한 큰 상수

12-bit immediate로 표현되지 않는 상수는 여러 instruction으로 만든다. `lui`는 **20-bit constant**를 destination의 bits 31:12에 놓고 bits 11:0을 0으로 만든다. RV64에서는 bit 31을 bits 63:32로 확장한다. `31−12+1=20`이므로 9월 10일 01:08:10–01:09:07의 “12-bit” 표현과 충돌하는 부분은 자료의 20 bits로 정정한다. [[page_cache/computer_architecture/lec.03/page-061|CA M003 p.61]] [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 01:08:10–01:09:07]]

자료의 규칙을 적용한 설명용 계산은 다음과 같다.

```asm
lui  x5, 0x12345
addi x5, x5, 0x678
```

첫 줄 뒤 `x5=0x0000000012345000`이고 `0x678`을 더하면 `0x0000000012345678`이다. 그러나 원하는 하위 12-bit pattern이 `0x800` 이상이면 `addi`가 그 pattern을 음수로 해석한다. 단순히 상위·하위를 잘라 쓰는 방식은 실패할 수 있다.

`0x12345ABC`를 만들 때 `0xABC`의 signed 12-bit 값은 `0xABC−0x1000=−0x544`다. 따라서 상위 부분을 하나 올려 다음처럼 계산한다.

```asm
lui  x5, 0x12346
addi x5, x5, -1348
```

`1348=0x544`이며 `0x12346000−0x544=0x12345ABC`다. 이 값들은 강의 발화를 복원한 것이 아니라 signed-immediate 규칙을 적용해 확인한 예다. M003 p.63의 먼 jump도 상위 주소를 `lui`로 만들고 `jalr`에 register와 하위 offset을 주는 생각을 사용한다. 그때도 하위 offset의 부호를 고려해야 한다. 이 입문 구성법이 임의의 64-bit 상수나 주소를 언제나 두 instruction으로 만든다는 뜻은 아니다.

## 핵심 정리

- Register field는 현재 값이 아닌 register 번호를 담는다.
- I-format은 immediate 연산과 load, S-format은 base와 data라는 두 입력을 갖는 store를 표현한다.
- S immediate 분할은 source register 위치의 규칙성을 보존한다.
- Branch의 2-byte 단위 값과 이미 복원된 byte 변위를 구분한다.
- `lui`는 20 bits를 놓으며 뒤의 signed `addi` 때문에 상위 부분 보정이 필요할 수 있다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · Bit 표기와 프로그램 표현

`0xECA86420`을 binary로 바꾸고 32 bits인지 확인하라. Compiler나 linker가 다른 프로그램을 처리할 수 있는 이유와 ISA 표준화가 보장하는 범위를 설명하라.

<details><summary>해설 보기</summary>

각 hex digit은 4 bits이므로 `1110 1100 1010 1000 0110 0100 0010 0000`, 총 8×4=32 bits다. 표기만 달라진 같은 pattern이다. Source·machine code·object도 data 표현이므로 실행 중인 프로그램이 이를 읽어 변환할 수 있다. ISA 표준화는 binary instruction 의미를 공유하게 하지만 library·실행 환경까지 자동으로 맞추지는 않는다.

**채점·확인 기준:** 8개 nibble, 32-bit 합계, programs-as-data와 호환성 한계를 확인한다.

</details>

#### 확인 Q02 · R-format 조립

`add x9,x20,x21`에서 `funct7=0`, `funct3=0`, `opcode=0x33`이다. 여섯 field를 상위부터 폭·값으로 쓰고 hex를 조립하라. `x20`의 현재 값이 바뀌면 encoding도 바뀌는가?

<details><summary>해설 보기</summary>

순서는 `funct7(7)|rs2(5)|rs1(5)|funct3(3)|rd(5)|opcode(7)`다. 값은 `0000000|10101|10100|000|01001|0110011`이며 합계 32 bits, hex는 `0x015A04B3`다. 수치 조립도 `21×2^20+20×2^15+9×2^7+0x33`으로 확인된다. Field의 20은 register 번호이므로 내용이 바뀌어도 encoding은 그대로다. 연산은 opcode·funct3·funct7을 함께 해석한다.

**채점·확인 기준:** Field와 assembly operand 순서 차이, 5-bit 번호, 최종 hex를 맞힌다.

</details>

#### 확인 Q03 · I/S의 입력과 목적지

`addi`, load, `sd x9,96(x22)`의 operand 역할을 비교하라. I/S-format의 폭과 공통 register 위치, store에 `rd`가 없는 이유, 96의 split immediate를 설명하라.

<details><summary>해설 보기</summary>

I는 `imm12|rs1(5)|funct3(3)|rd(5)|opcode(7)`이며 `addi`의 immediate는 값, load에서는 주소 offset이다. S는 `imm[11:5](7)|rs2(5)|rs1(5)|funct3(3)|imm[4:0](5)|opcode(7)`다. Store는 `x22`의 base와 `x9`의 data를 둘 다 읽고 memory에 쓰므로 `rd`가 없다. `rs1=19:15`, `rs2=24:20` 위치를 유지하며 96=`000001100000`을 `0000011|00000`으로 나눈다. R/I의 `rd` 자리 11:7이 S에서는 low immediate다.

**채점·확인 기준:** 값/offset 구별, 두 source와 memory 목적지, field 위치·split을 확인한다.

</details>

#### 확인 Q04 · 음수 Immediate의 보존

12-bit `111111111100`을 signed로 해석하고 RV64로 확장할 bit를 말하라. Base=100일 때 주소 계산을 sign/zero extension으로 각각 수행하고 signed 12-bit 범위를 도출하라.

<details><summary>해설 보기</summary>

Unsigned pattern은 4092지만 signed는 `4092−4096=−4`다. `imm[11]=1`을 위 52 bits에 채워야 −4를 유지하므로 주소는 96이다. Zero extension은 +4092로 만들어 4192가 된다. 최고 bit의 가중치 −2048과 나머지 합 2047에서 범위 −2048…2047이 나온다. 확장하는 것은 register 번호가 아니라 immediate 값이다.

**채점·확인 기준:** −4·96·4192, sign bit 위치, 52 bits와 범위를 검산한다.

</details>

#### 확인 Q05 · Branch 단위와 재조립

PC 100→target 200과 반대 방향의 byte 차이·2-byte 단위 값을 구하라. SB/UJ의 저장된 field와 byte 변위 복원 순서를 구분하고 SB 범위와 정렬 조건을 구분하라. PC-relative의 설계 이유도 두 가지 설명하라.

<details><summary>해설 보기</summary>

Assembler는 실제 instruction 배치에 따라 label의 주소와 변위를 정한다. 앞으로는 +100 bytes/+50 units, 뒤로는 −100 bytes/−50 units이며 기준은 branch 자신의 PC다. SB의 저장된 immediate 조각은 `imm12`, `imm10:5`, `imm4:1`, `imm11`로 흩어져 있고, UJ의 상위→하위 field는 `imm20|imm10:1|imm11|imm19:12|rd|opcode`다. SB는 `imm12|imm11|imm10:5|imm4:1|0`, UJ는 `imm20|imm19:12|imm11|imm10:1|0`으로 수치 순서대로 복원하고 sign-extend한다. 복원 후에는 byte 변위이므로 ×2를 반복하지 않는다. SB는 −4096…4094 bytes, 간격 2지만 기본 32-bit instruction 시작 주소는 여기서 4-byte 간격이다. 가까운 target에 짧은 field가 유용하고, PC와 target을 함께 k만큼 옮겨도 차이는 같다는 두 이유가 있다.

**채점·확인 기준:** 양방향 부호·수치 복원 순서·단위·범위/정렬 구별·두 설계 이유를 확인한다.

</details>

#### 확인 Q06 · LUI와 하위 Signed 값

`lui x5,0x12345; addi x5,x5,0x678`의 중간값과 결과를 구하라. `0x12345ABC`는 왜 upper `0x12346`과 immediate −1348을 쓰는가? LUI의 폭·zero fill·sign extension과 먼 jump 연결도 설명하라.

<details><summary>해설 보기</summary>

LUI는 20 bits를 31:12에 놓고 11:0을 0, 63:32를 bit31로 채워 `0x0000000012345000`을 만든다. +`0x678` 뒤는 `0x12345678`이다. `0xABC`는 12-bit signed에서 `0xABC−0x1000=−0x544=−1348`이므로 upper를 올려 `0x12346000−0x544=0x12345ABC`로 맞춘다. 먼 jump도 upper 주소와 register+low offset을 이용한 `jalr`를 결합하며 low 부호를 고려한다. 임의의 64-bit 값을 두 instruction으로 모두 만드는 법은 아니다.

**채점·확인 기준:** 20-bit 폭과 상·하위 처리, 두 수치 결과와 upper 보정 이유를 설명한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · Format 변경과 코드 이동

새로 만든 synthetic 연습이며 [EX:ca_2025_2_midterm_q13 p.5] (a,b)의 설계 이유를 전이한다. 선수는 I/S field와 PC-relative 설명이다. (a) “S immediate를 bits 31:20에 연속 배치하면서 R-format의 두 source 위치도 그대로 둔다”는 제안의 충돌을 찾아라. (b) PC=`0x400`, target=`0x3E0`인 branch를 둘 다 `0x1000`만큼 이동하면 encoded 거리와 target은 어떻게 되는가? 두배를 다시 곱하는 오류도 설명하라.

<details><summary>해설 보기</summary>

(a) `rs2`의 24:20이 31:20에 포함되므로 그 자리에서 data register 번호와 immediate를 동시에 보존할 수 없다. S는 7+5로 나누어 source 위치를 유지한다. (b) 원래 변위는 −`0x20`=−32 bytes, −16 units이며 이동 후 PC=`0x1400`, target=`0x13E0`에서도 그대로다. 복원된 −32에 다시 ×2하면 `0x1400−64=0x13C0`으로 잘못 간다.

**채점·확인 기준:** 실제 충돌 bit 위치와 relocation 후 불변 거리, 올바른/잘못된 target을 확인한다.

</details>

#### 연습 P02 · Low pattern이 음수일 때

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q04 p.2], [EX:ca_2025_2_midterm_q13 p.5] (c)의 sign extension 추론만 본문의 LUI 구성에 적용한다. 목표는 `0x2468ABCD`인데 제안은 upper `0x2468A`와 low pattern `0xBCD`를 그대로 조합한다. Low의 signed 값, 잘못된 결과, 수정한 두 instruction을 구하라.

<details><summary>해설 보기</summary>

`0xBCD−0x1000=−0x433=−1075`다. 잘못된 합은 `0x2468A000−0x433=0x24689BCD`로 목표보다 `0x1000` 작다. `lui x5,0x2468B` 뒤 `addi x5,x5,-1075`이면 `0x2468B000−0x433=0x2468ABCD`다. Low pattern이 signed operand라는 점을 보존하기 위해 upper를 보정한 것이다.

**채점·확인 기준:** −1075, 오차 0x1000, 수정 upper와 최종 값을 모두 검산한다.

</details>

### 복습 순서

Q01–Q04는 field 경계를 그려 풀고 Q05–Q06은 주소와 상수의 중간값을 쓴다. P01에서 설계 이유, P02에서 signed immediate 오류를 점검한 뒤 [[courses/computer_architecture/units/control-synchronization|분기와 동기화]]의 실행 경로를 추적한다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 · 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 · 강의 노트]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-022|p.22]], [[page_cache/computer_architecture/lec.03/page-023|p.23]], [[page_cache/computer_architecture/lec.03/page-025|p.25]], [[page_cache/computer_architecture/lec.03/page-026|p.26]], [[page_cache/computer_architecture/lec.03/page-027|p.27]], [[page_cache/computer_architecture/lec.03/page-028|p.28]], [[page_cache/computer_architecture/lec.03/page-029|p.29]], [[page_cache/computer_architecture/lec.03/page-061|p.61]], [[page_cache/computer_architecture/lec.03/page-062|p.62]], [[page_cache/computer_architecture/lec.03/page-063|p.63]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 56:21, 59:09, 01:03:54–01:04:49]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 01:05:39, 01:08:10–01:09:07]]

- 기본 32-bit instruction 부분집합을 다루며 모든 ISA 확장의 길이에 대한 주장은 아니다. Hex 변환과 프로그램을 처리하는 프로그램의 상세는 자료 보충이다.
- 9월 8일 field 수와 9월 10일 LUI 폭의 불명확한 발화는 그대로 불확실하다. 자료에서 R의 여섯 field와 LUI의 20 bits를 확인한다.
- SB의 표현 범위와 instruction 정렬은 별개다. 여기의 예는 4-byte instruction 시작 주소를 쓰며 LUI/ADDI 두 개가 임의의 64-bit 값을 모두 구성하지는 않는다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.


---

[[courses/computer_architecture/units/data-register-memory|← 이전: 데이터 표현·Register·Memory]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/control-synchronization|다음: Bitwise operation·분기·Synchronization →]]
