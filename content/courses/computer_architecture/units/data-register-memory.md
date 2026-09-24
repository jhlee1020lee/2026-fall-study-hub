---
title: "데이터 표현·Register·Memory"
description: "Register 계산, byte 주소, endianness, 정수 표현과 load/store 폭을 함께 확인한다."
course: "computer_architecture"
unit_id: "data-register-memory"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 03.pdf", "lec 02.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-03-lecture-02", "courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-10-lecture-04"]
---

같은 bit pattern이 register 값·memory의 byte·주소 중 무엇을 뜻하는지 구분하며 코드를 추적한다. 원소 크기와 signedness를 명시하면 offset과 load/store 선택에서 생기는 오류를 찾아낼 수 있다.

## Register file과 Storage hierarchy

계산할 값을 어디에 두는지는 instruction의 모양과 실행 비용을 함께 결정한다. [ISA의 상태 모형](architecture-contract.md)에서 소개한 register는 processor 안의 작은 저장 공간이다. 수업의 RV64 모델은 `x0`–`x31`이라는 **32개의 64-bit general-purpose register**를 갖는다. 64-bit data는 doubleword(더블워드), 32-bit data는 word(워드)다. Register 폭이 64 bits라는 사실은 모든 memory 접근이나 instruction도 64 bits라는 뜻이 아니다. [[page_cache/computer_architecture/lec.03/page-009|CA M003 p.9]]

명목 register 폭의 합은 `32 × 64 / 8 = 256 bytes`다. 9월 8일 20:16의 “32 times 8 bytes”와 “128 bytes”는 서로 충돌한다. 여기서는 명시된 구성으로 계산한 **256 bytes로 정정**하며, 발화를 고쳐 인용하지 않는다. 또한 `x0`는 hard-wired zero(고정된 0)이므로 쓰려고 해도 이후 읽는 값은 0이다. 256 bytes 전부가 자유롭게 값을 보존하는 공간은 아니다. `x1=ra`, `x2=sp` 같은 다른 역할은 주로 calling convention(호출 규약)의 약속이다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 20:16–23:03]]

전형적인 storage hierarchy(저장 계층)는 register, cache, main memory, SSD/HDD 순으로 용량이 커지고 접근이 느려지는 관계다. 그래서 자주 쓰는 작은 집합을 register에 둔다. “Smaller is faster”는 이 설계 직관을 표현하지만 강의에서도 항상 성립하는 법칙은 아니라고 한정했다. Cache의 구체적 구현은 이 직관과 별개의 후속 내용이다.

## Arithmetic와 중간 결과의 보존

`add a,b,c`는 `b`와 `c`의 register 값을 더해 `a`에 쓴다. 두 source(입력)와 한 destination(결과 위치)을 일정하게 쓰면 hardware의 처리 logic을 공유하기 쉽다. 이것이 “Simplicity favors regularity”의 의미다. 복합 expression은 그 규칙적인 작은 계산들로 나눈다.

`f = (g + h) - (i + j)`를 예로 들면 먼저 두 합을 만들고 마지막에 뺀다. 추상적인 표기는 `add t0,g,h; add t1,i,j; sub f,t0,t1`이다. 여기서 `t0`·`t1`은 중간값을 나타내는 예제의 virtual register 이름이다. 첫 합을 두 번째 합으로 덮어쓰면 마지막 뺄셈에 필요한 정보가 사라진다. M003 p.8의 두 번째 destination은 `t1`이며, STT의 불명확한 `t0`/`t1` 표현 대신 이 자료를 따라 설명한다.

`f,g,h,i,j`를 각각 `x19,x20,x21,x22,x23`에 배정한 자료의 실제 sequence는 다음과 같다. [[page_cache/computer_architecture/lec.03/page-011|CA M003 p.11]]

```asm
add x5,  x20, x21
add x6,  x22, x23
sub x19, x5,  x6
```

설명용으로 `g=8,h=3,i=4,j=2`라면 `x5=11`, `x6=6`, 최종 `x19=5`다. C 변수 이름에 특정 register가 고정되는 것은 아니다. 이 배정은 compiler가 선택한 것이며, 단순한 instruction 형식을 유지하는 대신 복합 계산에 여러 instruction이 필요해진다.

## Load-store와 Byte-addressable memory

큰 array(배열), structure(구조체), dynamic data(동적 데이터)는 작은 register file에 모두 들어가지 않는다. Load-store architecture에서는 memory의 값을 register로 load(읽기)하고 register에서 계산한 뒤 store(쓰기)한다. ALU instruction이 memory operand를 직접 사용하지 않는다는 원칙과, address 계산에 register 값을 쓴다는 사실은 양립한다. 2025-2 복기 Q2가 요구하는 구분도 여기에 있다. [EX:ca_2025_2_midterm_q02 p.2]

Byte-addressable memory(바이트 단위 주소 지정 메모리)는 주소 하나가 8-bit byte 하나를 식별한다는 뜻이다. 32-bit integer 하나는 연속된 네 주소를 사용한다. Endianness(바이트 순서)는 그 네 byte의 중요도와 주소 증가 순서를 연결하는 규칙이다.

| 32-bit 값 | Big endian: 낮은 주소 → 높은 주소 | Little endian: 낮은 주소 → 높은 주소 |
|---|---|---|
| `0xFF000000` | `FF 00 00 00` | `00 00 00 FF` |
| `0x00000001` | `00 00 00 01` | `01 00 00 00` |

[[page_cache/computer_architecture/lec.03/page-013|CA M003 p.13]]의 주소 화살표는 오른쪽으로 향한다. Big endian에서는 첫 주소에 most-significant byte, little endian에서는 least-significant byte가 놓인다. Byte 안의 bit를 뒤집는 연산은 아니다. 같은 주소 순서의 `01 00 00 00`도 little endian에서는 1, big endian에서는 `1 × 256³ = 16,777,216`이다.

수업은 little endian 모델을 사용하지만 모든 실행 환경을 그 순서로 일반화하지 않는다. 강의는 서로 다른 machine이 값을 교환할 때 byte 순서를 맞춰야 한다는 network 맥락을 덧붙였다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 30:44]] Endianness는 저장 순서이고, 뒤에서 다룰 signedness는 저장된 pattern의 숫자 해석이다.

## Addressing mode와 Array의 Byte offset

`GPR[x5]`는 register의 값, `MEM[a]`는 주소 `a`의 memory 값이다. Addressing mode(주소 지정 방식)는 원하는 값의 주소를 어떻게 표현하는지 정한다. 9월 3일 자료의 일반 비교는 다음과 같다. 모두가 RISC-V instruction 하나로 제공된다는 뜻은 아니다. [[page_cache/computer_architecture/lec.02/page-015|CA M008 p.15]]

| Mode | 읽을 값의 표현 |
|---|---|
| Absolute | `MEM[10000]` |
| Register indirect | `MEM[GPR[rbase]]` |
| Displaced/based | `MEM[GPR[rbase] + offset]` |
| Indexed | `MEM[GPR[rbase] + GPR[rindex]]` |
| Memory indirect | `MEM[MEM[GPR[rbase]]]` |

RISC-V 자료의 `ld x9,64(x22)`는 `x22`의 값에 64 **bytes**를 더한 주소에서 doubleword를 읽는다. `A[12] = h + A[8]`에서 `h=x21`, `A`의 base address(시작 주소)=`x22`, 원소 크기=8 bytes라면:

```asm
ld  x9, 64(x22)
add x9, x21, x9
sd  x9, 96(x22)
```

Index가 0부터 시작하므로 `A[8]`은 아홉 번째 원소이며 offset은 `8×8=64`다. `A[12]`는 열세 번째 원소이고 offset은 `12×8=96`이다. 설명용 base가 `0x1000`이면 읽는 주소는 `0x1040`, 쓰는 주소는 `0x1060`이다. Index에 바로 12를 더하는 오류는 원소 수와 byte 수를 혼동한 결과다. [[page_cache/computer_architecture/lec.03/page-014|CA M003 p.14]] 강의의 “64 bytes array”라는 표현은 이 예제의 전체 array 크기로 채택할 수 없다. `A[12]`가 존재하려면 그 위치까지 유효한 공간이 필요하다.

## Register allocation과 Immediate

Compiler는 자주 쓰는 값을 register에 배정하는 register allocation(레지스터 할당)을 수행한다. 동시에 필요한 값이 register 수를 넘으면 일부를 memory에 spill(내보내기)하며, 다시 사용할 때 load가 필요해진다. 이는 instruction sequence를 만드는 최적화다. 같은 sequence를 더 효율적으로 실행하는 microarchitecture 최적화와 구분해야 한다.

Immediate(즉시값)는 instruction 안에 직접 표현한 constant다. `addi x22,x22,4`는 `x22`에 4를 더해 같은 register에 쓴다. Loop index의 +1이나 pointer의 +4·+8은 흔하므로, 표현 범위 안의 constant를 별도로 memory에서 읽지 않는 것이 “Make the common case fast”의 사례다. [[page_cache/computer_architecture/lec.03/page-016|CA M003 p.16]] [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 39:47]]

같은 C source라도 compiler 선택에 따라 instruction 수와 memory 접근이 달라진다. 다만 9월 10일 05:12–06:12의 시연 명령·옵션은 불명확하므로 특정 flag나 보편적인 몇 배 향상으로 바꾸어 말할 수 없다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 05:12–06:12]] Immediate도 크기에 제한이 있으며 큰 상수는 [instruction encoding과 주소 구성](instruction-encoding.md)에서 다룬다.

## Unsigned와 Two's complement

숫자의 의미는 bit pattern에 적용하는 가중치에서 나온다. `b_i`가 0 또는 1인 n-bit unsigned integer(부호 없는 정수)는 다음과 같다.

$$
x=\sum_{i=0}^{n-1}b_i2^i,\qquad 0\le x\le 2^n-1.
$$

M003 p.17의 `00001011`은 `8+2+1=11`이다. 마지막 표기의 아래첨자 10은 십진법 표시이지 답이 1110이라는 뜻이 아니다. 64-bit unsigned 최댓값은 **`2^64−1 = 18,446,744,073,709,551,615`**다. `2^64 = 18,446,744,073,709,551,616`에서 1을 빼면 이 값을 얻는다. [[page_cache/computer_architecture/lec.03/page-017|CA M003 p.17]]에 인쇄되어 이전 baseline에도 옮겨진 최댓값의 십진수 표기는 산술 오기이므로 이 계산값으로 정정한다. 큰 수이지만 여전히 유한한 범위다. 강의가 언급한 Python이나 scientific application의 더 큰 정수는 ISA 위에서 software가 여러 저장 위치를 사용해 표현하는 별도 층이다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 44:22]]

Two's complement(2의 보수)는 최상위 bit의 가중치를 음수로 바꾼 signed integer(부호 있는 정수) 해석이다.

$$
x=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i,\qquad
-2^{n-1}\le x\le 2^{n-1}-1.
$$

| Pattern | Signed 의미 |
|---|---|
| `000…0` | 0 |
| `111…1` | −1 |
| `100…0` | 최솟값 `−2^(n−1)` |
| `011…1` | 최댓값 `2^(n−1)−1` |

따라서 최상위 bit가 1이면 negative, 0이면 non-negative다. 64-bit 범위는 −9,223,372,036,854,775,808부터 9,223,372,036,854,775,807이다. M003 p.18의 32-bit `111…1100`은 `−2,147,483,648+2,147,483,644=−4`다. 8-bit `11111110`은 unsigned로 254, signed로 `−128+126=−2`다. Bit 자체에 signed 표지가 붙는 것이 아니라 해석 규칙이 다른 것이다.

Negation(부호 반전)은 bit를 모두 뒤집고 1을 더하는 방식으로 만들 수 있다. 8-bit +2인 `00000010`을 뒤집으면 `11111101`, 1을 더하면 −2인 `11111110`이다. [[page_cache/computer_architecture/lec.03/page-020|CA M003 p.20]] 고정 폭에서는 결과의 표현 가능성도 확인해야 한다. 최솟값의 양의 대응값은 같은 signed 폭의 최댓값보다 하나 크므로 표현되지 않는다.

## Sign extension과 Load/Store width

폭을 늘리면서 값을 보존하려면 signed 값에는 sign extension(부호 확장), unsigned 값에는 zero extension(0 확장)을 적용한다. 8→16-bit에서 +2는 `0000 0010 → 0000 0000 0000 0010`, −2는 `1111 1110 → 1111 1111 1111 1110`이다. −2의 왼쪽을 0으로 채우면 254가 되므로 원래 값이 보존되지 않는다. [[page_cache/computer_architecture/lec.03/page-021|CA M003 p.21]]

RV64에서는 읽은 data가 destination register보다 좁을 수 있으므로 load instruction이 나머지 상위 bit를 정해야 한다.

| 읽기 폭 | Sign-extended load | Zero-extended load | 같은 폭의 store |
|---|---|---|---|
| Byte, 8 bits | `lb` | `lbu` | `sb` |
| Halfword, 16 bits | `lh` | `lhu` | `sh` |
| Word, 32 bits | `lw` | `lwu` | `sw` |

Memory byte `0x80`을 `lb`로 읽으면 `0xFFFFFFFFFFFFFF80`, `lbu`로 읽으면 `0x0000000000000080`이다. Signed 해석은 각각 −128과 128이다. 반면 `sb`·`sh`·`sw`는 source register의 하위 8·16·32 bits만 쓰므로 signed/unsigned에 따라 상위 bit를 채우는 store 구분은 필요하지 않다. [[page_cache/computer_architecture/lec.03/page-057|CA M003 p.57]]

C type의 width와 signedness는 compiler가 어떤 load를 고르는지에 영향을 준다. 의도와 다른 확장은 잘못된 값과 오류, 경우에 따라 vulnerability로 이어질 수 있다는 경고가 있었다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 53:56]] 불명확한 exploit 설명을 보충해 만들거나 수업의 C 크기 예시를 모든 구현의 규칙으로 일반화하지 않는다. 이 원리는 음수 immediate를 큰 register 폭으로 옮길 때도 적용된다. 그때 확장할 대상은 register 번호가 아니라 **immediate가 나타내는 값**이다.

## 핵심 정리

- RV64의 32×64-bit register 폭은 명목상 256 bytes이며 `x0`는 항상 0이다.
- 복합 식의 중간값은 마지막 사용까지 보존해야 한다.
- Array offset은 index×원소 byte 크기다. 주소와 그 주소에 저장된 값은 다르다.
- Endianness는 byte 순서, signedness는 bit pattern의 수치 해석이다.
- 좁은 load는 상위 bits를 정하지만 store는 지정된 하위 bits만 쓴다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · Register 용량과 폭

RV64의 register 수·폭으로 명목 byte 용량을 계산하고 `x0` 때문에 생기는 한계를 설명하라. Word·doubleword·instruction 길이와 전형적인 storage hierarchy도 구분하라.

<details><summary>해설 보기</summary>

`32×64/8=256 bytes`다. `x0` 쓰기는 보존되지 않고 읽으면 0이므로 전부 자유로운 저장공간은 아니다. Word는 32-bit data, doubleword는 64-bit data이며 register 폭이 모든 접근이나 instruction 길이를 정하지 않는다. Register→cache→main memory→SSD/HDD는 보통 용량이 커지고 느려지는 순서다. `ra`·`sp` 같은 역할은 convention이며 '작으면 빠르다'도 절대 법칙이 아니다.

**채점·확인 기준:** 256 계산, `x0`, 세 종류의 폭과 hierarchy의 한정을 모두 확인한다.

</details>

#### 확인 Q02 · 중간 합을 보존하기

`g,h,i,j=8,3,4,2`가 `x20`–`x23`에 있다. `f=(g+h)-(i+j)`를 `x5`·`x6`을 써서 계산하고 두 번째 합도 `x5`에 쓰는 오류를 설명하라. 이 register 배정은 C 변수의 고정 속성인가?

<details><summary>해설 보기</summary>

`add x5,x20,x21`로 11, `add x6,x22,x23`로 6을 만든 뒤 `sub x19,x5,x6`로 5를 얻는다. 첫 합을 덮어쓰면 뺄셈에 필요한 11을 잃는다. 두 source·한 destination의 규칙적 형식을 여러 번 사용하며 register 배정은 compiler의 선택이다.

**채점·확인 기준:** 세 연산의 값과 first-sum 보존 이유, register 배정의 성격을 설명한다.

</details>

#### 확인 Q03 · Memory byte의 해석

왜 큰 array에 load-store가 필요한가? 낮은 주소부터 `01 00 00 00`인 네 byte를 little/big endian unsigned 값으로 읽고, `0xFF000000`의 두 저장 순서와 machine 간 통신의 주의점을 설명하라.

<details><summary>해설 보기</summary>

Array 전체는 작은 register file에 담기 어렵고 ALU 계산은 load한 register 값으로 한다. 주어진 byte는 little endian에서 1, big endian에서 `1×256³=16,777,216`이다. `0xFF000000`은 big endian에서 `FF 00 00 00`, little endian에서 `00 00 00 FF`다. 주소 하나는 byte 하나이며 byte 내부 bits를 뒤집는 것이 아니다. 송수신 machine은 multibyte 해석 순서를 맞춰야 한다.

**채점·확인 기준:** 두 수치·두 byte 순서·load-store 필요성·network 동기를 모두 설명한다.

</details>

#### 확인 Q04 · Addressing mode를 식으로 읽기

`rbase=100`, `rindex=8`, offset=4라고 하자. Absolute `MEM[10000]`, register indirect, based, indexed, memory indirect가 무엇을 읽는지 식으로 쓰라. `MEM[100]=500`이라면 memory indirect의 최종 주소는?

<details><summary>해설 보기</summary>

각각 `MEM[10000]`, `MEM[100]`, `MEM[104]`, `MEM[108]`, `MEM[MEM[100]]=MEM[500]`이다. 마지막은 주소 100에서 읽은 500을 다시 주소로 사용하므로 register 값·첫 memory 값·최종 data를 구분해야 한다. 자료는 일반 mode 비교이며 모든 식이 RISC-V instruction 하나라는 뜻은 아니다.

**채점·확인 기준:** 다섯 식과 memory indirect의 두 번 참조를 맞힌다.

</details>

#### 확인 Q05 · Array index를 Byte offset으로

8-byte 원소의 `A`, base=`0x1000`, `h=5`, `A[8]=7`일 때 본문의 `A[12]=h+A[8]`을 추적하라. 읽기·쓰기 주소, 결과, 필요한 최소 array 공간을 말하라.

<details><summary>해설 보기</summary>

`ld` offset은 `8×8=64`, 주소는 `0x1040`이다. 7을 읽어 5와 더한 12를 `sd` offset `12×8=96`, 주소 `0x1060`에 쓴다. `A[8]`은 아홉째, `A[12]`는 열세째이며 최소 13개 원소, 104 bytes가 필요하다. 64 bytes 전체 array라는 표현은 이 접근을 수용하지 못한다.

**채점·확인 기준:** 주소와 data를 분리하고 index×8 및 마지막 원소의 공간까지 확인한다.

</details>

#### 확인 Q06 · Spill과 Immediate

Register가 부족하면 compiler가 무엇을 하며 microarchitecture 최적화와 어떻게 다른가? `addi x22,x22,4`에서 4를 immediate로 쓰는 이점과 한계를 설명하라.

<details><summary>해설 보기</summary>

일부 값을 memory에 spill하고 필요할 때 다시 load하도록 sequence를 바꾼다. Compiler는 실행할 instruction과 접근 수를 바꾸지만 microarchitecture는 주어진 sequence의 실행 방법을 개선할 수 있다. 4는 instruction에 들어 있어 별도 constant load가 필요 없다. 흔한 작은 증가량에 유용하지만 immediate field 안에 표현 가능해야 하며 불명확한 시연에서 특정 옵션이나 보편적 speedup을 추론할 수 없다.

**채점·확인 기준:** Spill/reload, 최적화 층위, constant load 제거와 범위 조건을 설명한다.

</details>

#### 확인 Q07 · Unsigned의 유한 범위

8-bit `00001011`과 all-ones의 값을 가중치로 계산하라. Unsigned 64-bit 최댓값을 정확히 쓰고 더 큰 Python 정수가 한 register의 무한 폭을 뜻하지 않는 이유를 설명하라.

<details><summary>해설 보기</summary>

`00001011=8+2+1=11`, 8-bit all-ones는 `Σ(2^i), i=0…7=255`다. 일반 최댓값은 `2^n−1`이므로 64-bit는 `18,446,744,073,709,551,615`다. 이는 `2^64=18,446,744,073,709,551,616`에서 1을 뺀 값이며 p.17의 잘못된 십진수와 구분한다. 더 큰 정수는 software가 여러 저장 위치로 표현할 수 있다. Endianness는 이런 가중치 규칙 자체가 아니라 byte 배치 문제다.

**채점·확인 기준:** 11·255·정확한 64-bit 값, 유한 폭과 software 표현을 모두 확인한다.

</details>

#### 확인 Q08 · Two's complement와 Negation

8-bit `11111110`을 unsigned와 signed로 읽고 +2를 negate하는 과정을 보이라. 8-bit signed의 0·−1·최소·최대 pattern과 범위를 쓰고 최솟값을 negate할 때의 문제를 설명하라.

<details><summary>해설 보기</summary>

Unsigned는 254, signed는 최상위 가중치가 −128이므로 `−128+126=−2`다. +2의 `00000010`을 complement한 `11111101`에 1을 더하면 `11111110`이다. `00000000=0`, `11111111=−1`, `10000000=−128`, `01111111=127`이며 범위는 −128…127이다. 최소의 양의 대응값 +128은 이 폭에 없어서 bit 절차가 수학적 양수 결과를 표현하지 못한다. 64-bit에도 범위 `−2^63…2^63−1`의 같은 비대칭이 있다.

**채점·확인 기준:** 가중치·negation 두 단계·네 pattern·표현 불가능한 경계를 확인한다.

</details>

#### 확인 Q09 · 확장과 저장 폭

−2를 8→16 bits로 sign/zero extend한 결과를 비교하라. RV64에서 `lb/lbu`, `lh/lhu`, `lw/lwu`, `sb/sh/sw`의 폭을 쓰고 byte `0x80`을 읽은 뒤 `sb`하면 무엇이 같고 다른지 설명하라.

<details><summary>해설 보기</summary>

`11111110`의 sign extension은 `1111111111111110`으로 −2를 보존하고 zero extension은 `0000000011111110`으로 254다. Signed/unsigned load 쌍은 각각 8·16·32 bits를 읽어 sign/zero extend한다. `lb 0x80` 결과는 `0xFFFFFFFFFFFFFF80`(−128), `lbu`는 `0x0000000000000080`(128)이다. `sb/sh/sw`는 하위 8·16·32 bits만 쓰므로 두 결과에 `sb`를 적용하면 모두 `0x80`이다. 값 해석을 보존할 load는 type·width에 따라 골라야 하며 store에는 상위 bit 확장이 없다.

**채점·확인 기준:** 폭 표 전체와 두 extension 결과, 같은 store byte가 같은 register 값은 아니라는 점을 확인한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · 같은 Byte가 숨기는 차이

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q02 p.2]의 load-store operand 구분을 확장하며 선수는 본문의 immediate·확장·store 폭이다. 유효한 주소 `x10=0x2000`의 byte가 `0x80`이고 출력 주소 `0x2001`도 유효하다. 두 실행은 각각 `lb x5,0(x10)` 또는 `lbu x5,0(x10)` 뒤 `addi x5,x5,1; sb x5,1(x10)`을 수행한다. 최종 `x5`와 출력 byte를 비교하고 출력 byte만 같으면 두 계산도 같다는 주장을 평가하라.

<details><summary>해설 보기</summary>

`lb` 경로는 −128+1=−127, `x5=0xFFFFFFFFFFFFFF81`이고 `lbu` 경로는 128+1=129, `x5=0x0000000000000081`이다. 두 `sb` 모두 하위 byte `0x81`만 쓴다. `addi`는 register 값과 immediate를 계산하며 주소 `x10` 자체나 memory byte를 직접 operand로 더하지 않는다. 최종 register 값은 다르므로 같은 byte만으로 계산 의미가 같다고 판단할 수 없다.

**채점·확인 기준:** 두 full-width 결과와 출력 주소·byte, register operand의 의미를 각각 확인한다.

</details>

### 복습 순서

Q01–Q06을 storage→계산→주소 순으로 풀고 Q07–Q09는 bit 가중치와 확장 결과를 직접 계산한다. P01에서 store 결과만 보고 두 load를 같다고 판단했는지 확인한 뒤 [[courses/computer_architecture/units/instruction-encoding|Instruction encoding]]으로 넘어간다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 · 자료 기반 복습]]
- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 · 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 · 강의 노트]]

- [lec.03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf): [[page_cache/computer_architecture/lec.03/page-007|p.7]], [[page_cache/computer_architecture/lec.03/page-008|p.8]], [[page_cache/computer_architecture/lec.03/page-009|p.9]], [[page_cache/computer_architecture/lec.03/page-011|p.11]], [[page_cache/computer_architecture/lec.03/page-012|p.12]], [[page_cache/computer_architecture/lec.03/page-013|p.13]], [[page_cache/computer_architecture/lec.03/page-014|p.14]], [[page_cache/computer_architecture/lec.03/page-015|p.15]], [[page_cache/computer_architecture/lec.03/page-016|p.16]], [[page_cache/computer_architecture/lec.03/page-017|p.17]], [[page_cache/computer_architecture/lec.03/page-019|p.19]], [[page_cache/computer_architecture/lec.03/page-020|p.20]], [[page_cache/computer_architecture/lec.03/page-021|p.21]], [[page_cache/computer_architecture/lec.03/page-057|p.57]]
- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-015|p.15]]

- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT · 20:16–23:03, 30:44, 39:47, 44:22, 53:56]]
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT · 05:12–06:12, 58:31–01:03:52]]

- 일반 addressing mode 분류는 녹음 없는 9월 3일 자료 보충이다. 모든 mode가 RISC-V instruction 하나로 제공되는 것은 아니다.
- 9월 8일의 128 bytes 발언은 32×8=256 bytes와 충돌한다. 두 번째 합의 destination과 전체 array 크기에 관한 불명확한 표현은 자료로 구분하며 복원된 발화로 제시하지 않는다.
- lec.03 p.17의 unsigned 64-bit 십진수는 산술 오기이며 올바른 최댓값은 18,446,744,073,709,551,615다.
- 9월 10일 compiler 옵션 시연과 9월 8일 취약점 관련 불명확한 발화는 확정하지 않는다. Load/store 폭의 상세는 두 날짜의 설명을 합친 것으로 C type 크기의 보편 규칙은 아니다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.


---

[[courses/computer_architecture/units/program-translation-loading|← 이전: 프로그램 번역·Linking·Loading]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/instruction-encoding|다음: Instruction의 비트 표현과 주소 구성 →]]
