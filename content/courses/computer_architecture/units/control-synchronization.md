---
title: "Bitwise operation·분기·Synchronization"
description: "Mask·분기·array loop·signed 비교와 LR/SC의 두 가지 검사를 연결한다."
course: "computer_architecture"
unit_id: "control-synchronization"
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

Bit 조작에서 분기·반복으로 진행하며 실행되는 경로와 바뀌는 값을 함께 추적한다. 공유 memory에서는 읽은 data의 조건과 conditional store의 성공 여부를 따로 판단해야 재시도 오류를 막을 수 있다.

## Logical shift와 고정 폭 Bit pattern

Bitwise operation(비트별 연산)은 숫자를 하나의 크기로만 보지 않고 각 bit를 옮기거나 선택하거나 뒤집는다. 주소 계산에서 index를 원소 크기만큼 배율 조정하고, bit 집합에서 필요한 부분을 추출할 때 유용하다. [데이터 표현](data-register-memory.md)의 폭·signedness와 [instruction encoding](instruction-encoding.md)의 field를 구분한 상태에서 읽으면 각 연산의 경계가 명확해진다.

`slli`는 왼쪽으로, `srli`는 오른쪽으로 logical shift(논리 이동)하고 빈자리에 0을 채운다. 자료의 작은 pattern은 `0001 → 0010`과 `0010 → 0001`이다. 왼쪽으로 `i`칸 이동하면 `2^i`를 곱한 pattern과 연결되지만 register 밖으로 나간 bit는 버린다. 오른쪽 logical shift는 unsigned 정수의 `2^i`에 대한 내림 나눗셈에 해당하며 음수의 sign을 보존하지 않는다. 설명용 8-bit `11110000`을 오른쪽 한 칸 이동하면 `01111000`이다.

[[page_cache/computer_architecture/lec.03/page-031|CA M003 p.31]]의 RV64 immediate shift 형식은 `funct6(6) | shamt(6) | rs1(5) | funct3(3) | rd(5) | opcode(7)`다. 괄호의 폭을 합하면 32이고, I-format의 12-bit 영역을 기능 구분과 이동량으로 나눈다. `shamt` 6 bits는 64-bit register에서 0–63의 이동량을 표현한다. 강의도 처음의 R-type 표현을 I-type으로 정정했다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 12:50]] 9월 8일에는 이 주제를 예고했고 실제 상세 설명은 9월 10일에 이어졌다.

## AND·OR·XOR와 Mask

Mask(마스크)는 원하는 bit 위치를 선택하는 pattern이다. AND는 두 입력이 모두 1일 때, OR는 하나라도 1일 때, XOR는 서로 다를 때 1이다.

| 입력 A,B | AND | OR | XOR |
|---|---|---|---|
| 0,0 | 0 | 0 | 0 |
| 0,1 | 0 | 1 | 1 |
| 1,0 | 0 | 1 | 1 |
| 1,1 | 1 | 1 | 0 |

AND mask가 1인 위치는 원래 bit를 유지하고 0인 위치는 지운다. OR mask가 1인 위치는 켜고, XOR mask가 1인 위치는 **뒤집는다**. 자료의 `x10=0x0DC0`, `x11=0x3C00`에 적용하면 AND는 `0x0C00`, OR는 `0x3DC0`이다. [[page_cache/computer_architecture/lec.03/page-032|CA M003 pp.32–33]]

```asm
and x9, x10, x11
or  x9, x10, x11
xor x9, x10, x12
```

앞의 두 줄은 각 결과를 따로 확인하는 예다. 세 번째 줄의 자료 예제는 `x12`의 모든 bit가 1이므로 `x10`을 반전한다. M003 p.34의 “Set some bits to 1”은 XOR의 일반 정의로는 틀리다. 위 truth table과 그림의 반전 결과에 따라 **선택한 bit를 toggle한다**고 정정한다.

C/Java의 `&`, `|`, `^`, `~`는 각각 bitwise AND, OR, XOR, NOT에 대응한다. RISC-V에는 `andi`·`ori`·`xori` immediate형도 있다. −1을 sign-extend하면 all-ones이므로 `xori rd,rs1,-1`은 전체 bit 반전에 사용할 수 있다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 16:27]] 자료의 Java logical right shift 표기는 `>>>`다. C의 `>>`를 type 조건 없이 항상 `srli`와 같은 의미라고 읽지는 않는다.

## Conditional branch로 If/Else를 나누기

`beq rs1,rs2,L1`은 두 register 값이 같을 때 `L1`으로, `bne`는 다를 때 `L1`으로 간다. 조건이 거짓이면 다음 instruction으로 진행한다. 마지막 operand는 결과를 받는 register가 아니라 branch target이다.

자료는 `if (i==j) f=g+h; else f=g-h;`를 다음처럼 번역한다. `f,g,h,i,j`는 각각 `x19,x20,x21,x22,x23`이다. [[page_cache/computer_architecture/lec.03/page-036|CA M003 p.36]]

```asm
      bne x22, x23, Else
      add x19, x20, x21
      beq x0, x0, Exit
Else: sub x19, x20, x21
Exit:
```

같은 경우에는 첫 branch를 통과하여 덧셈하고 `Exit`로 간다. 다른 경우에는 `Else`로 직접 가서 뺄셈한다. `x0`는 언제나 0이므로 `beq x0,x0,Exit`는 unconditional branch(무조건 분기)다. 이를 빼면 덧셈 뒤에 뺄셈까지 실행되어 결과를 덮어쓴다. 두 경로를 나누는 것뿐 아니라 **다시 합쳐질 때 다른 경로로 흘러들지 않게 하는 것**도 필요하다. Label의 실제 배치는 assembler가 처리한다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 22:49]]

## Array loop와 Basic block

반복문에서도 주소 계산, 조건 판단, 갱신, 되돌아가기를 나누어 보면 된다. 자료의 `while (save[i] == k) i += 1;`은 `i=x22`, `k=x24`, `save` base=`x25`, 원소 크기=8 bytes다. [[page_cache/computer_architecture/lec.03/page-037|CA M003 p.37]]

```asm
Loop: slli x10, x22, 3
      add  x10, x10, x25
      ld   x9, 0(x10)
      bne  x9, x24, Exit
      addi x22, x22, 1
      beq  x0, x0, Loop
Exit:
```

첫 줄이 `8i`를 만들고 두 번째 줄이 `base+8i`를 만든다. `ld`는 주소가 아니라 **그 주소에 든 원소**를 가져온다. 값이 다르면 종료하고, 같으면 `i`를 1 늘린 뒤 새로운 주소를 계산하러 돌아간다. 설명용 `save={7,7,9}`, `k=7`, 시작 `i=0`이면 다음과 같다.

| 검사한 i | 읽은 값 | 조건 결과 | 다음 동작 |
|---|---|---|---|
| 0 | 7 | 같음 | i를 1로 증가 |
| 1 | 7 | 같음 | i를 2로 증가 |
| 2 | 9 | 다름 | i=2인 채 종료 |

이 코드는 array 경계를 검사하지 않으므로 모든 유효 원소가 `k`인 경우의 안전성까지 제공하지 않는다.

Basic block(기본 블록)은 중간에 branch도 branch target도 없는 instruction sequence다. Branch는 마지막, 진입 target은 처음에만 올 수 있다. 이 loop에서 `slli`부터 `bne`까지 네 instruction이 한 block인 이유는 정상적인 제어 흐름이 그 중간에서 갈라지거나 들어오지 않기 때문이다. 다른 곳에서 `ld`로 들어오는 target을 추가하면 그 위치에서 block을 나눠야 한다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 27:52]] Compiler와 processor는 이런 실행 구간의 성질을 활용하되 의미를 보존한다. Exception이나 interrupt가 불가능하다는 뜻은 아니다.

## Signed 비교와 조건 반전

같은 bit pattern도 비교 instruction이 선택하는 해석에 따라 결과가 다르다. `blt`·`bge`는 signed 비교, `bltu`·`bgeu`는 unsigned 비교다. [[page_cache/computer_architecture/lec.03/page-040|CA M003 p.40]]의 32-bit all-ones와 1은 signed로 `−1<1`이지만 unsigned로 `4,294,967,295>1`이다. RV64 register 전체가 all-ones이면 unsigned 값은 `2^64−1`이며, 32-bit 그림의 숫자를 그대로 쓰면 안 된다.

`if (a>b) a+=1;`에서 `a=x22`, `b=x23`라면 조건을 반대로 검사하여 본문을 건너뛸 수 있다.

```asm
      bge  x23, x22, Exit
      addi x22, x22, 1
Exit:
```

여기서는 `b>=a`일 때 증가를 건너뛴다. “`bge`니까 원래 조건도 ≥일 것”이라고 instruction 이름만 보면 operand 순서를 놓친다. [[page_cache/computer_architecture/lec.03/page-039|CA M003 p.39]]

복기 Q12의 조건부 array store에 적용할 사고 순서도 같다. 먼저 어느 비교가 본문을 실행하거나 건너뛰게 하는지 정하고, 그 경로에서 쓸 값과 array 주소를 구분한 뒤, data width에 맞는 store를 고른다. 특히 8-byte lecture array 예제를 모든 `int` array에 그대로 적용해서는 안 된다. 비교의 의미, 유효한 주소, 저장 폭을 차례로 확정하면 branch·address·store를 일관되게 결합할 수 있다. [EX:ca_2025_2_midterm_q12 p.4]

## LR/SC와 Atomic update의 재시도

여러 processor가 공유 memory를 수정할 때 단순한 load 뒤에 store를 놓는 것만으로는 중간 간섭을 감지할 수 없다. Read-modify-write(읽기·수정·쓰기)를 하나의 atomic effect(원자적 효과)로 만들려면 hardware 지원이 필요하다.

`lr.d`는 값을 읽고 reservation(예약)을 남긴다. `sc.d`는 그 reservation에 따른 조건이 만족될 때만 쓰기를 수행하고, 성공하면 status 0, 실패하면 nonzero를 destination에 돌려준다. 자료가 설명한 대표 실패 상황은 그 사이 location이 바뀌는 경우다. Reservation 자체가 다른 processor의 쓰기를 막는 lock은 아니며 모든 실패 조건을 이 한 가지로 단정할 수도 없다. [[page_cache/computer_architecture/lec.03/page-065|CA M003 p.65]]

자료 첫 예제의 atomic swap은 다음과 같다. 아래 `sc.d`의 operand 순서는 **강의자료의 표기**인 `status,(address),data`를 유지한 것으로, assembler 입력 문법을 새로 검증한 코드는 아니다.

```text
again: lr.d x10,(x20)
       sc.d x11,(x20),x23
       bne x11,x0,again
       addi x23,x10,0
```

`x10`은 읽은 **data**, `x11`은 쓰기 성공 여부를 나타내는 **status**다. 실패하면 이미 완료한 것처럼 진행하지 않고 `lr.d`부터 다시 시작한다. 설명용으로 memory=7, `x23=9`인 시도가 성공하면 memory는 9가 되고 마지막 복사로 `x23=7`이 된다. 실패한 시도에서는 이 교환이 완료된 것이 아니다. [[page_cache/computer_architecture/lec.03/page-066|CA M003 p.66]]

같은 페이지의 두 번째 lock 예제는 자율 복습으로 남긴 자료 기반 설명이다. 1을 준비하고 lock 값이 0인지 읽어 확인한 뒤 SC로 1을 쓰려 한다. 이미 잠겼거나 SC가 실패하면 재시도하며, unlock은 0을 store한다. 강의는 첫 swap의 설명과 두 번째 예제의 자율 복습을 구분했다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 01:15:16–01:16:49]]

복기 Q18은 word 단위 `lr.w`·`sc.w`를 사용하는 더 확장된 조건부 갱신을 요구한다. 여기서 가져올 핵심은 **data 조건이 맞는지**와 **SC가 성공했는지**를 서로 다른 검사로 다루고, 실패 뒤에는 새로 읽은 값으로 조건도 다시 평가해야 한다는 점이다. [EX:ca_2025_2_midterm_q18 p.9] Counting semaphore 전체의 정확성을 판단하려면 추가 조건이 필요하다. 특히 이 입문 reservation 설명만으로 실전 lock의 memory ordering까지 해결되지는 않는다.

## 핵심 정리

- Logical shift는 0을 채우고 고정 폭 밖의 bits를 버린다.
- AND는 선택·clear, OR는 set, XOR는 toggle을 한다.
- If/else에서는 다른 경로의 결과로 덮어쓰지 않도록 합류 전 jump도 필요하다.
- Loop는 주소 계산·값 읽기·조건·갱신·되돌아가기를 따로 확인한다.
- Signedness는 비교 의미를 정하고, LR data와 SC status는 서로 다른 질문에 답한다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · 고정 폭 Shift

8-bit `11110000`의 logical right shift 1칸과 left shift 1칸을 구하라. 부호 보존·곱셈 해석의 한계와 RV64 immediate shift의 field 폭을 설명하라.

<details><summary>해설 보기</summary>

오른쪽은 `01111000`(120), 왼쪽은 높은 bit를 버려 `11100000`(224)다. 오른쪽은 0을 채워 signed 음수를 보존하지 않으며 왼쪽도 무한 정밀도 240×2=480을 그대로 저장하지 못한다. RV64 형식은 `funct6(6)|shamt(6)|rs1(5)|funct3(3)|rd(5)|opcode(7)`=32 bits이고 6-bit shamt는 0…63이다. I-format의 immediate 영역을 나눈 형태다.

**채점·확인 기준:** 두 pattern·고정 폭·zero fill·32-bit field 합계를 확인한다.

</details>

#### 확인 Q02 · Mask와 Toggle

`a=1010`, mask=`1100`의 AND·OR·XOR를 구하고 각 mask의 역할을 말하라. `0x0DC0`과 `0x3C00`의 AND/OR, `xori rd,rs1,-1`의 효과와 C/Java 표기상의 주의점도 설명하라.

<details><summary>해설 보기</summary>

결과는 `1000`, `1110`, `0110`이다. AND는 mask=1인 자리 보존, OR는 set, XOR는 toggle이므로 이미 1인 자리도 0이 될 수 있다. Hex 결과는 AND `0x0C00`, OR `0x3DC0`이다. −1은 sign extension 뒤 all-ones여서 `xori`가 모든 bit를 반전한다. `& | ^ ~`는 bitwise 연산, 자료의 Java logical right shift는 `>>>`이며 C `>>`를 type 조건 없이 `srli`와 같다고 할 수 없다.

**채점·확인 기준:** 수치 결과와 toggle/set 차이, immediate −1의 이유를 확인한다.

</details>

#### 확인 Q03 · If/Else의 두 경로

본문의 `if(i==j) f=g+h; else f=g-h;` 번역에서 `g=9,h=4`라 하자. `i==j`와 `i!=j` 경로의 결과를 구하고 덧셈 뒤 `beq x0,x0,Exit`를 지웠을 때를 설명하라.

<details><summary>해설 보기</summary>

첫 `bne`는 같으면 통과하여 13을 계산하고 unconditional branch로 subtraction을 건너뛴다. 다르면 `Else`로 가서 5를 계산한다. Skip을 지우면 같은 경우에도 subtraction으로 흘러 13이 5로 덮인다. `x0` 두 값은 항상 같고 label은 이동할 target이며 결과 register가 아니다.

**채점·확인 기준:** 두 정상 결과와 오류 경로의 덮어쓰기 원인을 설명한다.

</details>

#### 확인 Q04 · Array loop의 매 반복

8-byte `save={7,7,9}`, base=`0x1000`, `k=7`, 초기 `i=0`이다. 본문의 loop가 읽는 주소·값·최종 `i`와 load 횟수를 추적하라. 모든 유효 원소가 7이면 종료와 안전성을 보장하는가?

<details><summary>해설 보기</summary>

`slli`와 `add`로 `base+8i`를 매번 새로 만든다. 주소 `0x1000`, `0x1008`, `0x1010`에서 7·7·9를 읽는다. 앞 두 번은 일치하여 increment하고 셋째는 `bne`로 나가 `i=2`, load 3회, increment 2회다. Bounds check가 없으므로 전부 7이면 유효 영역 밖을 읽을 수 있어 안전한 종료가 보장되지 않는다.

**채점·확인 기준:** 주소/data 분리, 조건·increment 순서, mismatch load까지 센다.

</details>

#### 확인 Q05 · Basic block의 경계

Loop의 `slli; add; ld; bne`가 한 basic block인 이유를 말하라. 다른 branch가 `ld`로 직접 들어오면 어디에서 나누며, block이라는 말이 interrupt 불가능성도 보장하는가?

<details><summary>해설 보기</summary>

중간 branch나 진입 target이 없고 끝의 `bne`에서만 제어가 나뉜다. `ld`가 새 target이면 앞의 `slli; add`와 뒤의 `ld; bne`로 나누어 중간 진입을 반영한다. 이 정상 흐름의 구조를 compiler·processor가 최적화에 이용할 수 있지만 의미 보존이 필요하다. Interrupt·exception이 없다는 주장은 아니다.

**채점·확인 기준:** 끝 branch/첫 target 조건과 새로운 분할 지점을 명시한다.

</details>

#### 확인 Q06 · Signedness와 반대 조건

같은 폭의 all-ones와 1을 `blt`·`bltu`로 비교하라. 이어 `if(a>b) a+=1`을 `bge x23,x22,Exit`로 구현할 때 operand 순서와 `a=b`, `a=-1,b=1`인 경우를 확인하라. `a=x22,b=x23`다.

<details><summary>해설 보기</summary>

Signed all-ones는 −1이므로 `blt`는 branch한다. Unsigned는 `2^n−1`로 1보다 크므로 `bltu`는 branch하지 않는다. `bge x23,x22`는 `b>=a`를 검사하므로 원래 조건이 거짓인 경우를 건너뛴다. 동등일 때도 skip, −1과 1에서도 `1>=−1`로 skip하여 a는 그대로다. 32-bit all-ones의 4,294,967,295를 RV64 전체 all-ones 값으로 쓰지 않는다.

**채점·확인 기준:** 두 comparison 의미와 equality·negative 사례, operand 방향을 확인한다.

</details>

#### 확인 Q07 · LR Data와 SC Status

단순 load/store가 atomic swap을 보장하지 않는 이유를 설명하라. 자료의 성공 시도에서 memory=7, 새 data=9라면 memory와 반환된 옛값은 무엇인가? SC가 nonzero이면 무엇을 다시 해야 하며, 두 번째 lock 예제는 어떤 두 검사를 하는가?

<details><summary>해설 보기</summary>

두 접근 사이 다른 processor가 값을 바꿀 수 있다. LR은 data를 읽고 reservation을 두며 SC는 조건부 store와 status를 돌려준다. 성공 status=0이면 memory=9, 옛 data=7이 swap의 마지막 복사로 반환된다. 실패 status는 data가 아니며 swap이 완료되지 않았으므로 LR부터 다시 읽는다. Lock은 읽은 data가 0인지와 SC status가 0인지 따로 확인하며 실패하면 재시도하고 unlock은 0을 쓴다. Reservation이 다른 쓰기를 막지는 않는다.

**채점·확인 기준:** Data/status 분리, 성공·실패 경로, 두 lock 검사와 unlock을 설명한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · 조건부 Array 결과 저장

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q12 p.4]의 경로·주소·store 선택 추론을 옮기되 variable index와 산술을 추가했다. 선수는 현재 단원의 shift·signed branch와 앞 단원의 8-byte 주소 계산이다. Signed 64-bit `a=x20,b=x21`, 유효한 index `i=x22`, 8-byte array base=`x25`이고 overflow는 없다고 가정한다. `a>b`면 `A[i]=a-b`, 아니면 `A[i]=a+b`를 구현하라. `x5,x6`은 scratch다. `(a,b)=(7,2),(2,2),(-3,1)`을 확인하라.

<details><summary>해설 보기</summary>

주소를 먼저 계산하고 false 조건에서 Else로 간다.

```asm
slli x5, x22, 3
add  x5, x25, x5
bge  x21, x20, Else
sub  x6, x20, x21
beq  x0, x0, Store
Else: add x6, x20, x21
Store: sd x6, 0(x5)
```

`b>=a`는 false arm을 선택한다. 세 결과는 차 5, 동등의 합 4, 음수 사례의 합 −2다. 두 경로 모두 `base+8i`에 정확히 한 번 `sd`하며 첫 경로는 Else를 건너뛴다. 이 8-byte 선택은 새 문제의 명시 조건이지 원복기의 모든 `int`에 대한 가정이 아니다.

**채점·확인 기준:** Signed 비교·동등 처리·8i·두 결과 경로·단일 store를 모두 확인한다.

</details>

#### 연습 P02 · 실패 뒤 조건을 다시 읽기

새로 만든 synthetic 연습이며 [EX:ca_2025_2_midterm_q18 p.9]의 data 조건/SC status 구분만 적용한다. 선수는 본문의 자료 기반 lock 예제다. 한 시도에서 LR은 0을 읽었지만 SC는 실패했다. 다음 LR은 1을 읽고, 더 나중 LR은 0을 읽어 그때의 SC가 성공한다. 매 시점에 lock 획득 여부와 다음 동작을 설명하라. 첫 실패 뒤 예전 0만 믿고 성공 경로로 가면 왜 틀리는가?

<details><summary>해설 보기</summary>

첫 0은 시도 가능성을 보였을 뿐이고 SC 실패로 획득하지 못했으므로 LR부터 재시도한다. 다음 값 1은 이미 잠긴 상태여서 그 시도는 SC를 진행하지 않고 다시 읽어야 한다. 더 나중 0을 읽고 SC가 status 0으로 1을 저장한 뒤에야 이 모형에서 획득했다. 예전 data 조건은 현재 값도 쓰기 성공도 보장하지 않는다. 이 추적은 완전한 counting semaphore나 실전 lock의 ordering·fairness 증명이 아니다.

**채점·확인 기준:** Data=0과 status=0을 구분하고 모든 실패가 fresh LR로 돌아가게 설명한다.

</details>

### 복습 순서

Q01–Q02는 bit별로 계산하고 Q03–Q06은 실제로 실행되는 instruction만 표시한다. Q07과 P02에서는 data 조건과 status를 서로 다른 칸에 쓴 뒤, P01을 두 경로·동등·음수 입력으로 확인하고 [[courses/computer_architecture/units/procedures-stack|Procedure와 stack]]으로 이어 간다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 · 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 · 강의 노트]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-030|p.30]], [[page_cache/computer_architecture/lec.03/page-031|p.31]], [[page_cache/computer_architecture/lec.03/page-032|p.32]], [[page_cache/computer_architecture/lec.03/page-034|p.34]], [[page_cache/computer_architecture/lec.03/page-035|p.35]], [[page_cache/computer_architecture/lec.03/page-036|p.36]], [[page_cache/computer_architecture/lec.03/page-037|p.37]], [[page_cache/computer_architecture/lec.03/page-038|p.38]], [[page_cache/computer_architecture/lec.03/page-039|p.39]], [[page_cache/computer_architecture/lec.03/page-040|p.40]], [[page_cache/computer_architecture/lec.03/page-064|p.64]], [[page_cache/computer_architecture/lec.03/page-065|p.65]], [[page_cache/computer_architecture/lec.03/page-066|p.66]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 01:05:42 · preview]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 12:50, 16:27, 22:49, 27:52, 01:15:16–01:16:49]]

- 9월 8일은 logical operation 예고이며 상세 shift·control 설명은 9월 10일에 확인된다. XOR의 'set' 문구는 truth table과 inversion 예에 따라 toggle로 구분한다.
- Basic block은 정상 제어 흐름의 구분이며 exception·interrupt 불가능성을 뜻하지 않는다. Array loop에는 bounds check가 없다.
- Atomic swap 설명과 달리 두 번째 lock의 전체 흐름은 자료 기반 자율 복습이다. 슬라이드 SC operand 순서는 assembler 입력으로 검증한 문법이 아니다.
- Reservation은 다른 쓰기를 막는 lock이 아니며 SC 실패 조건 전체가 열거되지 않았다. Q18 연결은 data 조건·status·재시도에 한정하고 완전한 semaphore·memory ordering·fairness는 다루지 않는다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.

- [[exam_questions/ca_2025_2_midterm_q12|기존 문제 미리보기 · Q12]]
- [[exam_questions/ca_2025_2_midterm_q18|기존 문제 미리보기 · Q18]]


---

[[courses/computer_architecture/units/instruction-encoding|← 이전: Instruction의 비트 표현과 주소 구성]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/procedures-stack|다음: Procedure 호출·Calling convention·Stack →]]
