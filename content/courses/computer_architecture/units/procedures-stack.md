---
title: "Procedure 호출·Calling convention·Stack"
description: "Calling convention, frame 배치, leaf·factorial·string copy의 보존과 복귀를 추적한다."
course: "computer_architecture"
unit_id: "procedures-stack"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-10-lecture-04"]
---

함수 호출을 인자·결과·복귀 주소와 보존해야 할 값의 이동으로 읽는다. Stack frame의 생성과 복원을 별개 동작으로 추적하면 leaf·재귀·string copy가 caller의 상태를 어떻게 유지하는지 확인할 수 있다.

## Procedure call의 인자·결과·복귀 주소

Procedure(프로시저, 함수)를 호출하려면 target으로 이동하는 것 이상이 필요하다. Caller(호출하는 쪽)는 인자를 전달하고 callee(호출받는 쪽)는 필요한 local storage를 확보해 계산하고 결과를 전달한 뒤 원래 실행 흐름으로 돌아가야 한다. [분기와 제어 흐름](control-synchronization.md)이 다음 실행 위치를 고르는 법을 설명했다면, procedure call은 **어디로 돌아갈지와 무엇을 보존할지**를 더한다.

수업의 정수 인자 예제에서는 `x10`–`x17`에 인자를 놓고 결과는 `x10`에 돌려준다. Register 표는 `x10`–`x11`을 return value에도 쓰는 자리로 표시한다. 반면 `x1`은 return address(복귀 주소)다. Return value(반환값)는 계산 결과이고 return address는 caller에서 계속 실행할 위치다. 결과가 7이라면 그 예제의 `x10`에 7을 두며, `x1`을 7로 바꾸는 것이 아니다. [[page_cache/computer_architecture/lec.03/page-041|CA M003 p.41]]

```asm
jal  x1, ProcedureLabel
jalr x0, 0(x1)
```

두 줄은 각각 call과 return의 전형적인 형태다. `jal x1,ProcedureLabel`은 다음 instruction의 주소를 `x1`에 남기고 target으로 이동한다. 기본 32-bit instruction 예에서는 다음 주소가 `PC+4`다. `jalr x0,0(x1)`은 `x1`을 바탕으로 복귀하며 새 link를 `x0`으로 보내 보관하지 않는다. `jalr`는 return 전용 instruction이 아니라 register로 계산한 주소에 가는 jump이며, 자료는 `switch`의 computed jump도 용도로 든다. [[page_cache/computer_architecture/lec.03/page-042|CA M003 p.42]]

9월 10일 39:39에서는 계산 결과를 `x10`에 전달하며, 일반적인 결과용 자리로 `x10`·`x11`을 사용한다고 설명한다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 39:39 · 결과 전달]] 반면 40:28의 “return value … register s one” 구절은 STT에서도 불명확하게 남아 있다. 이를 `x1`이라고 명확히 말한 것으로 복원하거나 반환값을 `x1`에 둔다는 규칙으로 읽으면 안 된다. 여기서는 자료 pp.41–42의 구분에 따라 계산 결과와 caller로 돌아갈 주소를 서로 다른 값으로 이해한다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 40:28 · 복귀 설명의 불명확한 구절]] 복기 Q3에 연결되는 판단도 instruction 이름을 “호출 전용/복귀 전용”으로 외우기보다 **target을 만드는 방법과 link를 저장할 위치**를 확인하는 것이다. [EX:ca_2025_2_midterm_q03 p.2]

## Calling convention과 보존 책임

Caller와 callee는 같은 register file을 사용한다. 별도로 만든 함수끼리 통신하려면 calling convention(호출 규약)이 필요하다. Callee-saved register는 callee가 바꾸려면 원래 값을 저장했다가 복귀 전에 복원해야 한다. Caller-saved register는 호출 뒤 값이 유지된다고 기대할 수 없으므로 caller가 이후 필요한 값만 보관한다. 매번 모든 register를 무조건 저장하라는 규칙이 아니다.

[[page_cache/computer_architecture/lec.03/page-048|CA M003 p.48]]의 표를 역할과 책임으로 읽으면 다음과 같다.

| Register | Alias/용도 | 필요한 값의 보존 책임 |
|---|---|---|
| `x0` | `zero` | 고정된 0 |
| `x1` | `ra`, return address | Caller |
| `x2` | `sp`, stack pointer | Callee |
| `x3`, `x4` | `gp`, `tp` | 표의 대시는 일반 temporary라는 뜻이 아님 |
| `x5`–`x7` | `t0`–`t2` | Caller |
| `x8`–`x9` | `s0/fp`, `s1` | Callee |
| `x10`–`x17` | `a0`–`a7`, 인자/일부 결과 | Caller |
| `x18`–`x27` | `s2`–`s11` | Callee |
| `x28`–`x31` | `t3`–`t6` | Caller |

Caller가 호출 전의 `x5`를 나중에도 필요로 한다면 자신이 보관해야 한다. 반대로 callee가 `x18`을 작업 공간으로 쓰면 자신이 원래 값으로 되돌려야 한다. 계산에 잠깐 쓰는 register라는 일상적 의미와 표의 Temporary 분류는 다르다. `x18`을 임시 계산에 사용해도 callee-saved 의무는 남는다.

Compiler와 library가 같은 규약을 지키면 서로 다른 시점에 번역된 함수도 인자와 결과를 교환할 수 있다. 강의는 library 연결을 이 약속의 실용적인 이유로 설명했다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 45:52]] `gp`와 `tp`의 세부 runtime 규칙은 여기서 설명되지 않았으므로 표의 빈 보존 항목을 자유로운 덮어쓰기 허가로 읽지 않는다.

## Stack frame과 Memory layout

Memory layout(메모리 배치)의 개념 그림은 낮은 주소부터 reserved, text, static data, dynamic data, stack을 놓는다. Text는 program code, static data는 global·static 변수와 자료가 예로 든 상수 배열·문자열, heap은 `malloc`/`new` 등으로 사용하는 dynamic data다. Stack은 procedure 호출에 필요한 저장공간을 제공한다. `gp=x3`은 static 영역을 offset으로 참조할 기준과 연결된다. 이 그림은 모든 OS의 정확한 주소 배치를 정하지 않는다. [[page_cache/computer_architecture/lec.03/page-055|CA M003 p.55]]

그림에서 heap은 높은 주소로, stack은 낮은 주소로 자란다. 따라서 stack의 top은 가장 높은 주소가 아니라 현재 push/pop하는 끝이다. Stack pointer(SP, 스택 포인터)는 `x2`이며 이 끝을 가리킨다. Procedure frame 또는 activation record(활성 레코드)는 한 호출이 사용하는 영역으로, 필요한 경우 저장한 인자 register, return address, saved register, local array·structure를 담는다.

Frame pointer(FP, 프레임 포인터) `x8`은 frame을 참조할 기준으로 쓸 수 있다. 일부 compiler가 사용하는 방식이지 모든 함수에 반드시 필요한 별도 값은 아니다. 단순한 정수 인자 모형에서 여덟 register 자리를 넘는 인자는 stack으로 전달할 수 있다. [[page_cache/computer_architecture/lec.03/page-056|CA M003 p.56]] [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 57:36]] 함수가 새 frame을 얻는다는 것이 프로그램 전체 stack이 비어 있다는 뜻은 아니며, 모든 C local variable이 반드시 memory에 놓인다는 뜻도 아니다.

## Leaf procedure의 저장·계산·복원

Leaf procedure(말단 프로시저)는 다른 procedure를 호출하지 않는다. 자료의 `leaf_example`은 `g,h,i,j`를 `x10,x11,x12,x13`으로 받고 `(g+h)−(i+j)`를 계산한다. 두 합에 `x18`·`x19`, 차에 `x20`을 사용하므로 이 세 callee-saved register를 보존해야 한다.

원자료 pp.44–46은 두 번째 합을 `add x19,x12,x1`로 인쇄하지만 p.43의 `j=x13` 및 `i+j` 주석과 맞지 않는다. 아래에서는 **그 operand를 `x13`으로 정정**했다. 이것은 자료 내부 근거에 따른 정정이며 강사가 그 값을 명확히 발화했다는 주장은 아니다.

```asm
leaf_example:
    addi sp, sp, -24
    sd   x18, 16(sp)
    sd   x19, 8(sp)
    sd   x20, 0(sp)
    add  x18, x10, x11
    add  x19, x12, x13
    sub  x20, x18, x19
    addi x10, x20, 0
    ld   x20, 0(sp)
    ld   x19, 8(sp)
    ld   x18, 16(sp)
    addi sp, sp, 24
    jalr x0, 0(x1)
```

세 64-bit 값을 보관하므로 그림상 공간은 `3×8=24 bytes`다. 진입 전 SP를 `S`라고 하면 새 SP는 `S−24`이고 낮은 주소부터 원래 `x20`, `x19`, `x18`이 각각 `S−24`, `S−16`, `S−8`에 놓인다. [[page_cache/computer_architecture/lec.03/page-047|CA M003 p.47]]의 세 그림은 할당 전, 저장 중, 복귀 후를 보여 준다. 가운데 그림의 SP가 내려가고 마지막 그림에서 원위치로 돌아오는 것을 읽으면 된다.

결과를 `x10`에 먼저 복사해야 `x20`을 원래 값으로 복원해도 반환값을 잃지 않는다. 또한 SP를 올리는 것만으로 register 값이 복구되지는 않는다. 세 `ld`가 값을 복원하고 마지막 `addi`가 frame 공간을 해제하는 서로 다른 일을 한다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 42:58]] 이 24-byte sequence는 수업의 저장·복원 모형이며 외부 ABI의 모든 정렬·호출 요구를 만족하는 구현이라는 인증은 아니다.

## Non-leaf recursion에서 n과 Return address 보존

Non-leaf procedure(비말단 프로시저)는 다른 procedure를 호출한다. 자료의 `fact(n)`은 `n<1`이면 1, 아니면 `n×fact(n−1)`을 반환한다. 이때 `x10`에는 처음의 `n`도, 재귀 호출이 반환한 결과도 들어간다. 곱셈에 원래 `n`이 필요하므로 보관해야 한다. 다음 `jal`은 `x1`도 덮어쓰므로 현재 호출의 return address 역시 보관해야 한다. [[page_cache/computer_architecture/lec.03/page-052|CA M003 p.52]]

자료의 prologue는 SP를 16 줄이고 `8(sp)`에 `x1`, `0(sp)`에 `n`을 저장한다. `x5=n−1`을 만든 뒤 `bge x5,x0,L1`으로 재귀 경로를 고른다. 작은 정상 입력의 base case에서는 `x10=1`로 만들고 SP를 복구한 뒤 return한다. 추가 call을 하지 않았으므로 기존 `x1`은 그대로 남아 있다.

재귀 경로에서는 `x10=n−1`로 호출한다. 돌아온 결과를 `x6`으로 옮긴 다음 stack에서 원래 `n`과 `x1`을 복구하고 SP를 되돌린다. 마지막으로 `x10=n×x6`를 계산해 caller로 돌아간다. 이 순서에서 반환 결과를 먼저 옮기는 이유는 원래 `n`을 `x10`으로 복원할 때 그 결과를 덮어쓰지 않기 위해서다.

설명용 `fact(2)`의 작은 추적은 다음과 같다.

| 호출 | 보존하는 값 | 하위 호출/계산 | 반환값 |
|---|---|---|---|
| `fact(2)` | n=2, 자기 caller로 돌아갈 주소 | `fact(1)` 결과에 2를 곱함 | 2 |
| `fact(1)` | n=1, `fact(2)`로 돌아갈 주소 | `fact(0)` 결과에 1을 곱함 | 1 |
| `fact(0)` | 자료의 prologue가 공간 확보 | Base case | 1 |

호출은 `2→1→0`, 반환은 `1→1→2` 순이다. 보존 필요성과 base case는 강의에서 설명했고, `n>=1`의 줄별 추적은 자율 복습으로 남겼다. 위 전체 재귀 흐름은 자료 기반 해설이다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 51:55]] `n−1`이나 곱셈의 overflow, stack 고갈까지 처리하는 범용 구현은 아니다.

## String copy에서 종료 Byte까지 저장하기

자료의 `strcpy` 예제는 `while ((x[i]=y[i])!='\0') i+=1;`이라는 순서를 사용한다. **먼저 대입하고 나중에 종료를 검사**하므로 zero terminator(종료용 0 byte)도 destination에 복사된다. `x10`은 destination base, `x11`은 source base, `x19`는 `i`다. Byte 원소이므로 주소는 `base+i`이며 doubleword array처럼 `8i`가 아니다. [[page_cache/computer_architecture/lec.03/page-058|CA M003 p.58]]

다음은 자료 p.59의 loop 부분이다.

```asm
L1: add  x5, x19, x11
    lbu  x6, 0(x5)
    add  x7, x19, x10
    sb   x6, 0(x7)
    beq  x6, x0, L2
    addi x19, x19, 1
    jal  x0, L1
```

Source가 설명용 `{'A','B',0}`이면 loop의 byte load와 store는 각각 세 번, `i` 증가는 두 번이다. `beq`를 `sb`보다 앞으로 옮기면 종료 byte를 쓰지 않은 채 끝나는 오류가 생긴다. 이 횟수에는 loop 밖의 stack 저장·복원은 포함하지 않았다.

`x19`는 callee-saved이므로 자료는 진입 때 8-byte 공간에 저장하고 `i=0`으로 시작하며, `L2`에서 원래 값을 복원하고 SP를 되돌려 return한다. `lb`와 `lbu`의 64-bit 결과는 다를 수 있지만 바로 뒤의 `sb`가 쓰는 하위 byte와 zero 여부는 이 사용법에서 같을 수 있다. 그래서도 두 load가 일반적으로 같은 instruction이 되는 것은 아니다. 강의는 특히 `lbu`와 `sb`를 설명하고 나머지 추적을 자율 복습으로 안내했다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 01:01:31–01:03:52]]

이 전체 loop 해설은 자료 기반이며, destination의 충분한 용량과 유효하게 끝나는 source가 필요하다. 코드에는 길이 검사가 없다. 반환값·보존 규약·memory 접근의 정당성은 서로 따로 확인해야 한다는 점이 procedure와 data access를 연결한다.

## 핵심 정리

- Return value는 계산 결과, return address는 계속 실행할 위치다.
- Caller는 필요한 caller-saved 값을 보관하고 callee는 변경한 callee-saved 값을 복원한다.
- SP 복구는 공간 해제이며 저장한 register를 읽는 복원과 다르다.
- 재귀에서는 원래 인자와 현재 복귀 주소가 다음 call을 넘어 살아 있어야 한다.
- String copy는 대입 후 종료를 검사하므로 0 byte까지 복사한다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · Call의 결과와 복귀 위치

기본 32-bit instruction에서 주소 `0x400`의 `jal x1,F`로 호출하여 F가 정수 7을 반환한다. 인자·결과 register, `x1`의 값, `jalr x0,0(x1)`의 목적을 말하라. `jalr`는 return 전용인가?

<details><summary>해설 보기</summary>

정수 인자는 `x10`–`x17`, 이 결과 7은 `x10`에 둔다. `x1=0x404`는 caller의 다음 instruction 주소이고 결과와 다르다. Return은 `x1`을 이용해 그 위치로 가며 새 link는 `x0`으로 버린다. `jalr`는 register로 계산한 target을 쓰므로 computed jump에도 사용할 수 있다. Procedure에는 이 제어 이전 외에 local storage 확보·계산·보존·결과 전달이 필요하다.

**채점·확인 기준:** 7과 0x404를 분리하고 link를 버리는 이유와 `jalr`의 일반성을 설명한다.

</details>

#### 확인 Q02 · 누가 무엇을 보존하는가

Caller가 호출 뒤 `x5`와 `x18`의 옛값을 필요로 하고 callee가 둘 다 바꾼다. 책임을 구분한 뒤 `ra`, `sp`, temporary·saved·argument register 범주와 `gp/tp`의 대시를 설명하라.

<details><summary>해설 보기</summary>

Caller는 필요한 `x5`를 미리 보관한다. Callee는 변경할 `x18`을 저장하고 반환 전에 복원한다. 표에서 caller 책임은 `x1/ra`, `x5`–`x7`, `x28`–`x31`, `x10`–`x17`이며 callee 책임은 `x2/sp`, `x8`–`x9`, `x18`–`x27`이다. `x0`는 고정 0이고 `x3/gp`, `x4/tp`의 대시는 자유로운 temporary라는 허가가 아니다. `x18`을 잠깐 써도 의무는 바뀌지 않으며 필요한 값·변경하는 값만 조건에 따라 보존한다. 같은 규약이 별도 compiler/library의 통신을 가능하게 한다.

**채점·확인 기준:** 두 값의 책임, 표의 범주, 조건부 보존과 library 동기를 확인한다.

</details>

#### 확인 Q03 · Frame과 Memory layout

Text·static data·heap·stack의 역할과 그림의 성장 방향을 설명하라. Frame에 들어갈 수 있는 값, SP/FP/gp의 역할, 8개를 넘는 정수 인자와 'stack top'의 의미를 말하라.

<details><summary>해설 보기</summary>

Text는 code, static data는 global/static 객체, heap은 dynamic data, stack은 호출 저장공간이다. 그림에서 heap은 위 주소로, stack은 낮은 주소로 자라므로 frame 확보는 SP 감소다. Frame에는 필요한 saved arguments·return address·saved registers·local arrays가 들어갈 수 있다. `sp=x2`는 활성 끝, 선택적으로 쓰는 `fp=x8`은 frame 기준이고 `gp=x3`은 static 영역 offset의 기준과 연결된다. 단순 정수 모형의 나머지 인자는 stack으로 전달할 수 있다. Top은 최고 주소가 아니며 새 frame을 만든다고 caller frame이 없어지거나 모든 local이 memory에 놓이는 것은 아니다.

**채점·확인 기준:** 역할·방향·SP/FP·frame 내용과 모든 layout을 일반화하지 않는 한계를 확인한다.

</details>

#### 확인 Q04 · Leaf의 Frame과 반환값

본문의 leaf에서 진입 `sp=0x1000`, 옛 `x18,x19,x20=100,200,300`, 인자 `g,h,i,j=9,4,5,2`다. 세 저장 주소, 계산 결과와 복귀 후 register/SP를 추적하라. 둘째 합의 `x1` 인쇄 오류와 결과 복사·load·SP 복구의 순서를 설명하라.

<details><summary>해설 보기</summary>

24 bytes를 확보하면 SP=`0xFE8`이다. 옛 `x20=300`은 `0xFE8`, `x19=200`은 `0xFF0`, `x18=100`은 `0xFF8`에 저장된다. 합은 13과 7, 차는 6이다. `j`가 `x13`에 있으므로 둘째 합은 `x12+x13`이며 return address인 `x1`을 더하면 틀린다. 결과 6을 `x10`에 복사한 뒤 세 `ld`로 100·200·300을 복원하고 SP를 `0x1000`으로 되돌린다. SP만 올리면 register 값이 남고, `x20` 복원 뒤 결과를 복사하면 300을 반환하므로 순서가 중요하다.

**채점·확인 기준:** 세 주소·정정 operand·결과 6·복원 값·SP를 모두 확인한다. Frame은 수업 모형이다.

</details>

#### 확인 Q05 · 재귀의 인자와 Return address

자료의 `fact(2)`가 `fact(0)`까지 들어가고 돌아오는 값과 최대 frame 공간을 계산하라. 왜 n과 `x1`을 둘 다 저장하며, 재귀 결과를 `x6`에 옮기는가? Base case가 `x1`을 reload하지 않아도 되는 이유도 설명하라.

<details><summary>해설 보기</summary>

호출은 2→1→0, 반환은 1→1→2다. 매 진입에서 16 bytes를 확보하며 base도 포함하므로 최대 48 bytes, 처음 SP=S이면 가장 깊은 SP=S−48이다. 각 frame의 `0(sp)`는 원래 n, `8(sp)`는 기존 복귀 주소다. 재귀 call은 `x10`을 결과로, `jal`은 `x1`을 새 link로 바꾸므로 둘 다 필요하다. 결과를 `x6`에 먼저 옮겨야 n을 `x10`에 복원할 때 잃지 않는다. Base는 nested call이 없어 `x1`이 변하지 않았으므로 SP를 복구하고 돌아갈 수 있다. 모든 return 뒤 SP는 S로 복구된다.

**채점·확인 기준:** 세 호출·세 반환·48 bytes·두 보존 이유·base 경로를 확인한다.

</details>

#### 확인 Q06 · 종료 Byte와 String copy

본문 `strcpy`가 `{'A','B',0}`을 복사할 때 loop의 load·store·increment 횟수와 주소식을 구하라. 종료 검사를 `sb` 앞으로 옮긴 경우, `x19` 보존, `lb`와 `lbu`의 제한적인 동등성을 설명하라.

<details><summary>해설 보기</summary>

Byte 원소여서 source/destination 주소는 각 base+i다. 0도 대입한 뒤 검사하므로 load 3회·store 3회·increment 2회다. 검사를 먼저 하면 마지막 0을 쓰지 않아 destination의 종료가 보장되지 않는다. `x19`는 callee-saved이므로 진입의 옛값을 8-byte slot에 저장하고 종료 때 reload한 뒤 SP를 복구한다. `lb/lbu`의 상위 bits는 달라도 이 코드의 즉시 `sb`와 zero test에서는 같은 하위 byte와 zero 여부를 낼 수 있다. 일반적인 register 계산에서 같은 값은 아니며 충분한 destination과 유효한 terminated source가 필요하다.

**채점·확인 기준:** Terminator 포함 횟수·byte offset·register 복원과 load 차이의 한계를 모두 확인한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · Nested call 뒤 잘못된 복귀

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q03 p.2]의 target/link 구분에 본문의 보존 규약을 결합한다. Caller의 `0x400: jal x1,F` 뒤 F는 `0x810: jal x1,G`로 G를 호출한다. F는 자기 return address를 저장하지 않았고 G 호출 뒤에도 필요한 `x5=9`도 저장하지 않았다. 나중에는 반환값 7을 `x1`에 넣으려 한다. 두 call 직후 link와 세 결함을 설명하고 필요한 보존·반환 위치를 제시하라. 기본 32-bit instruction 모형이다.

<details><summary>해설 보기</summary>

첫 link는 `0x404`, nested call의 link는 `0x814`다. F가 옛 `x1`을 보관하지 않으면 G에서 돌아온 뒤 원래 caller의 `0x404`를 잃는다. `x5`는 caller-saved이므로 G가 그대로 둘 것이라고 가정할 수 없고, F가 G의 caller로서 필요한 9를 보관해야 한다. 반환값 7은 `x10`에 두고, 저장한 outer link를 `x1`에 복원한 뒤 return해야 한다. 이때 필요한 stack 공간·저장 register도 복구한다. `x1=7`은 계산 결과를 복귀 target으로 오용한 것이다.

**채점·확인 기준:** 0x404/0x814를 구분하고 RA·live caller-saved·return value의 세 문제를 각각 해결한다.

</details>

### 복습 순서

Q01–Q03에서 register 역할과 frame 그림을 먼저 복원한다. Q04–Q06은 호출 전·계산 중·복귀 뒤 상태를 표로 비교하고 P01의 누락된 보존을 찾은 뒤 [[courses/computer_architecture/units/performance-model|실행시간 모형]]으로 연결한다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 · 강의 노트]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-041|p.41]], [[page_cache/computer_architecture/lec.03/page-042|p.42]], [[page_cache/computer_architecture/lec.03/page-043|p.43]], [[page_cache/computer_architecture/lec.03/page-044|p.44]], [[page_cache/computer_architecture/lec.03/page-047|p.47]], [[page_cache/computer_architecture/lec.03/page-048|p.48]], [[page_cache/computer_architecture/lec.03/page-049|p.49]], [[page_cache/computer_architecture/lec.03/page-050|p.50]], [[page_cache/computer_architecture/lec.03/page-052|p.52]], [[page_cache/computer_architecture/lec.03/page-055|p.55]], [[page_cache/computer_architecture/lec.03/page-056|p.56]], [[page_cache/computer_architecture/lec.03/page-058|p.58]], [[page_cache/computer_architecture/lec.03/page-059|p.59]]

- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 39:39 · result transfer; 40:28 · unclear return wording; 42:58, 45:52, 51:55, 57:36, 01:01:31–01:03:52]]

- 9월 10일 39:39는 `x10`/`x11` 결과 전달, 40:28은 불명확한 'return value … register s one' 구절의 위치다. 뒤 구절에서 `x1`을 명확한 발화로 복원하지 않는다.
- Leaf 예제의 `x1` operand 인쇄는 인자 배치에 따라 `x13`으로 구분해 바로잡는다. 24-byte·8-byte frame은 수업의 저장/복원 모형이며 전체 ABI 정렬 준수의 인증은 아니다.
- Factorial의 재귀 경로와 string copy의 전체 추적은 자율 복습으로 남긴 자료 기반 설명이다. Factorial은 overflow·stack 고갈을 처리하는 범용 구현이 아니다.
- String copy에는 길이 검사가 없으며 source가 유효하게 끝나고 destination 용량이 충분해야 한다. Memory layout은 개념 그림이고 FP는 모든 함수에 필수인 별도 값이 아니다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.


---

[[courses/computer_architecture/units/control-synchronization|← 이전: Bitwise operation·분기·Synchronization]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/performance-model|다음: 실행시간과 Performance 모형 →]]
