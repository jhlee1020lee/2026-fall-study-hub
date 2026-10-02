---
title: "데이터 표현·Register·Memory"
description: "RV64의 register, byte 주소, 정수 표현과 값 보존을 연습한다."
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
source_lectures: ["courses/computer_architecture/lectures/2026-09-08-lecture-03", "courses/computer_architecture/lectures/2026-09-03-lecture-02", "courses/computer_architecture/lectures/2026-09-10-lecture-04"]
---

Register 이름, 주소, 그 주소의 값을 따로 추적해 보자. Byte 배치와 signed 해석을 나누면 load·계산·store의 실수를 찾기 쉽다.

## Register file과 연산의 작업 공간

Register(레지스터)는 processor가 자주 쓰는 값을 가까이 두는 작은 저장소이다. 수업의 RV64 모형에는 `x0`–`x31`의 32개 general-purpose register가 있고 각각의 data 폭은 64 bits이다. 64-bit data를 doubleword, 32-bit data를 word라고 부른다. 따라서 register 수와 data 폭의 명목 합은

$$
32\times64\text{ bits}=2048\text{ bits}=256\text{ bytes}
$$

이다. 다만 `x0`은 hard-wired zero이므로 항상 0을 읽으며 저장용으로 바꿀 수 없다. 위의 256 bytes 전체가 자유롭게 쓸 수 있는 공간이라는 뜻은 아니다. `x1=ra`, `x2=sp` 등의 나머지 역할은 주로 calling convention의 사용 약속이다. [CA M003 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-009) [CA M003 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-010) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 23:03]]

9월 8일 20:16과 24:24의 “128 bytes”는 같은 설명의 `32 × 8 bytes`와 맞지 않는다. 256 bytes는 여기서 산술로 바로잡은 값이며 STT가 그렇게 말했다는 인용은 아니다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 20:16]] [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 24:24]] Register → cache → main memory → SSD/HDD라는 전형적 hierarchy에서는 뒤로 갈수록 용량이 커지고 접근이 느려지는 관계를 생각한다. “Smaller is faster”는 설계 직관이며 항상 성립하는 법칙은 아니다. [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]

### 두 입력과 한 출력으로 식을 나누기

기본 register 산술의 `add a,b,c`는 `b`와 `c`의 값을 더해 `a`에 쓴다는 표기이다. 일정한 operand 형식은 같은 처리 logic을 재사용하기 쉽게 한다. 그 대신 `f=(g+h)-(i+j)`처럼 복합적인 식은 여러 instruction으로 나눈다. [CA M003 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-007) [CA M003 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-008)

자료의 가상 register 표기로는 먼저 `t0=g+h`, 다음 `t1=i+j`, 마지막 `f=t0-t1`이다. 첫 합을 두 번째 합으로 덮어쓰면 마지막 뺄셈에 필요한 값이 사라진다. 여기의 `t0`, `t1`, `f` 등은 해당 설명의 가상 이름이다. 9월 8일 17:48도 이 점을 강조한다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 17:48]]

Compiler가 `f,g,h,i,j`를 각각 `x19,x20,x21,x22,x23`에 배정한 자료 예는 다음과 같다.

```asm
add x5,  x20, x21
add x6,  x22, x23
sub x19, x5,  x6
```

예를 들어 이 식에 설명용 값 `g=7,h=5,i=3,j=2`를 넣으면 `x5=12`, `x6=5`, `x19=7` 순서가 된다. C 변수마다 항상 같은 register가 정해진 것은 아니다. 이것은 compiler가 선택한 배정이다. 두 번째 destination의 불확실한 구두 표현은 자료 p.8의 서로 다른 temporary로 해설하며 복원된 발화로 취급하지 않는다. [CA M003 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-011)

## Byte address와 endianness

Array, structure, dynamic data를 register file만으로 담을 수는 없다. Load-store architecture는 memory의 값을 register에 load하고 register에서 계산한 뒤 결과를 store한다. 따라서 instruction을 fetch한다는 이유만으로 ALU instruction이 data-memory operand를 직접 사용한다고 볼 수 없다. [CA M003 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-012) 과거 복기 문항에서 요구하는 구분도 바로 이 operand의 출처이다. [EX:ca_2025_2_midterm_q02 p.2] 여기서 시험 연결은 공식 원문·정답이 독립 확인되지 않은 2025-2 복기본을 사용한다.

Byte-addressable memory에서는 주소 하나가 8-bit byte 하나를 식별한다. 32-bit integer 하나는 연속된 네 byte를 차지한다. Endianness(바이트 저장 순서)는 그 네 byte를 주소 증가 순서로 어떻게 배치하는지 정한다.

| 32-bit 값 | Big endian: 낮은 주소 → 높은 주소 | Little endian: 낮은 주소 → 높은 주소 |
|---|---|---|
| `0xFF000000` | `FF 00 00 00` | `00 00 00 FF` |
| `0x00000001` | `00 00 00 01` | `01 00 00 00` |

[CA M003 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-013)의 빨간 첫 행과 오른쪽으로 향하는 주소 화살표를 보면 byte의 수치적 중요도와 주소 순서가 서로 다른 개념임을 알 수 있다. Little endian은 least-significant byte를 가장 낮은 주소에, big endian은 most-significant byte를 그곳에 둔다. 수업의 실행 모형은 little endian이다.

설명용으로 주소 증가 순서의 byte가 `01 00 00 00`이면 little endian 해석은 1, big endian 해석은 $2^{24}=16,777,216$이다. Byte들은 같아도 해석 규칙이 다르면 값이 달라진다. 9월 8일 30:44는 서로 다른 machine이 network로 데이터를 교환할 때 순서를 맞추어야 하는 이유를 설명한다. 특정 network API나 모든 ISA 실행 모드까지 일반화할 필요는 없다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 30:44]]

## Effective address와 array offset

주소 계산을 명확히 하려면 register 이름, register의 값, memory의 값을 분리해야 한다. `GPR[x5]`는 `x5`의 값이고 `MEM[a]`는 주소 `a`에서 읽은 값이다. [CA M008 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-015)의 일반적인 addressing mode 비교는 다음과 같다.

| Mode | 값을 읽는 표현 |
|---|---|
| Absolute | `MEM[10000]` |
| Register indirect | `MEM[GPR[rbase]]` |
| Displaced/based | `MEM[offset + GPR[rbase]]` |
| Indexed | `MEM[GPR[rbase] + GPR[rindex]]` |
| Memory indirect | `MEM[MEM[GPR[rbase]]]` |

이 목록은 ISA 일반을 비교하는 9월 3일 자료 기반 설명이다. 모든 mode가 RISC-V instruction 하나로 제공된다는 뜻은 아니다. 특히 마지막 행은 register에서 얻은 주소의 memory 내용을 다시 주소로 쓰므로 한 번의 주소 계산과 구별된다. [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]

### `A[12] = h + A[8]`를 byte 단위로 옮기기

[CA M003 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-014)에서는 `h`가 `x21`, 배열 base가 `x22`, 원소 크기가 8 bytes이다. Zero-based index이므로 `A[8]`은 아홉 번째 원소이며 byte offset은 $8\times8=64$이다. `A[12]`는 열세 번째 원소로 offset이 $12\times8=96$이다.

```asm
ld  x9, 64(x22)
add x9, x21, x9
sd  x9, 96(x22)
```

첫 줄은 주소 `GPR[x22]+64`에서 값을 읽고, 둘째 줄은 그 값에 `h`를 더하며, 셋째 줄은 합을 주소 `GPR[x22]+96`에 쓴다. Offset 64와 96은 원소 수가 아니라 byte 수이다. 이를 array 전체의 크기와도 혼동하면 안 된다. STT 33:54의 “64 bytes array”는 `A[12]` 접근과 맞지 않으므로 전체 배열 크기로 채택하지 않는다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 33:54]]

### Register allocation과 immediate

Memory 값을 계산에 쓰려면 load/store가 추가되므로 compiler는 자주 쓰는 값을 register에 배정하려 한다. Register가 부족하면 일부 값을 memory에 spill한다. 이 code 생성의 선택은 같은 instruction sequence를 더 효율적으로 실행하는 microarchitecture 최적화와 구분된다. [CA M003 PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-015) [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 39:47]]

Immediate(즉시값)는 instruction에 직접 포함된 constant이다.

```asm
addi x22, x22, 4
```

이는 `x22`의 값에 4를 더해 다시 `x22`에 쓴다. Loop index의 +1, pointer의 +4·+8 같은 작은 상수가 흔하므로 표현 가능한 immediate를 사용하면 그 상수를 가져오는 별도 memory load를 피할 수 있다. 모든 상수가 한 immediate에 들어가는 것은 아니므로 폭의 조건이 중요하다. 이것이 “Make the common case fast”의 예이다. [CA M003 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-016) 9월 10일 compiler 시연의 손상된 flag·기본 옵션은 이 원리로 추정해 채우지 않는다. [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 05:12]]

## Unsigned와 two's complement

Endianness가 byte의 **배치** 문제라면 signedness는 bit pattern의 **수치 의미** 문제이다. $n$-bit unsigned integer는

$$
x=\sum_{i=0}^{n-1}b_i2^i,\qquad 0\leq x\leq2^n-1
$$

로 읽는다. `00001011`은 $8+2+1=11$이고, 8-bit 최댓값은 255이다. 64-bit unsigned 최댓값은 정확히 **18,446,744,073,709,551,615**이다. [CA M003 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-017)에 인쇄된 **18,446,774,073,709,551,615**는 같은 페이지의 $2^{64}-1$과 맞지 않는 오기이며 과거 노트·baseline에도 이어져 있었다. 여기의 값은 식을 정수 산술로 계산한 정정이고 원자료나 발화의 인용을 바꾼 것이 아니다.

범위가 커도 bit 수가 고정되어 있으면 무한히 큰 정수를 한 register로 표현할 수 없다. 9월 8일 44:22는 Python이나 scientific application의 더 큰 정수 표현이 ISA 위의 software에서 구현된다는 층위 차이를 설명한다. 그 library의 내부 알고리즘까지 제시된 것은 아니다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 44:22]]

### 최상위 bit에 음수 가중치를 주기

Two's complement(2의 보수)의 signed 값은 가장 높은 bit의 가중치를 음수로 바꾼다.

$$
x=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i,
\qquad -2^{n-1}\leq x\leq2^{n-1}-1.
$$

64-bit 범위는 −9,223,372,036,854,775,808부터 9,223,372,036,854,775,807이다. 최상위 bit 1은 negative, 0은 non-negative를 뜻한다.

| Pattern | Signed 의미 |
|---|---|
| `000…0` | 0 |
| `111…1` | −1 |
| `100…0` | 최솟값 |
| `011…1` | 최댓값 |

자료의 32-bit `11111111 11111111 11111111 11111100`은 $-2,147,483,648+2,147,483,644=-4$이다. 더 작은 폭으로 같은 원리를 보면 8-bit `0xFE`는 unsigned로 254, signed로 $-128+126=-2$이다. Bit pattern 자체가 바뀌는 것이 아니라 해석이 바뀐다. [CA M003 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-018) [CA M003 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-019)

Negation은 모든 bit를 뒤집고 1을 더해서 구한다. 8-bit +2는 `00000010`, 반전하면 `11111101`, 1을 더하면 −2의 `11111110`이다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 48:31]] [CA M003 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-020) 고정 폭에서 $x+\mathord{\sim}x$는 모든 bit가 1이므로 modulo $2^n$에서 −1이다. 따라서 $\mathord{\sim}x+1$은 $-x$와 같은 $n$-bit pattern을 준다. 그러나 signed 최솟값의 양의 대응값은 같은 폭으로 표현되지 않는다. Pattern 계산이 가능하다는 것과 원하는 signed 결과가 범위 안에 있다는 것은 따로 확인해야 한다.

## 폭을 바꾸어도 값을 보존하는 extension

Signed two's complement의 폭을 늘릴 때는 sign bit를 복제하고, unsigned 값에는 왼쪽을 0으로 채운다. Sign extension(부호 확장)은 원래 음수 가중치와 추가된 높은 bit들의 가중치가 함께 작용하여 numeric value를 보존하게 한다.

| 8-bit 값 | 16-bit로 값을 보존한 결과 |
|---|---|
| +2: `0000 0010` | `0000 0000 0000 0010` |
| −2: `1111 1110` | `1111 1111 1111 1110` |

12-bit signed immediate도 같은 원리로 64 bits까지 확장한다. 원래 bit 11을 위의 52자리에 복제한다. 이 reasoning이 복기 Q4의 extension 요구와 연결된다. [EX:ca_2025_2_midterm_q04 p.2] Zero extension을 대신하면 negative immediate의 값이 보존되지 않는다. [CA M003 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021)

RV64의 subword load/store에서는 memory access 폭과 destination register 폭을 구분해야 한다.

| Memory 폭 | Signed load | Unsigned load | Store |
|---:|---|---|---|
| 8 bits | `lb` | `lbu` | `sb` |
| 16 bits | `lh` | `lhu` | `sh` |
| 32 bits | `lw` | `lwu` | `sw` |

Signed load는 64-bit destination으로 sign-extend하고 unsigned load는 zero-extend한다. Memory byte `0x80`을 `lb`로 읽으면 `0xFFFFFFFFFFFFFF80`, `lbu`로 읽으면 `0x0000000000000080`이 된다. Signed 수로는 각각 −128과 128이다. 반대로 store는 source register의 하위 8/16/32 bits만 쓰므로 이런 signed/unsigned 확장 구분이 필요 없다. 두 결과를 각각 `sb`로 저장하면 모두 `0x80`을 쓴다. [CA M003 PDF p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057)

9월 8일의 byte 확장 설명과 9월 10일의 여러 load/store 폭 설명이 여기서 만난다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 53:56]] [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 STT 58:31]] [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트]] C type과 signedness는 compiler의 instruction 선택에 영향을 준다. 수업의 `char`·`short`·`int`·`long long` 크기 예를 모든 C 구현의 보편 규칙으로 바꾸면 안 된다. 잘못된 폭이나 signedness는 값의 해석을 바꾸어 오류를 만들 수 있지만, 9월 8일 52:03의 불명확한 vulnerability 설명이나 9월 10일의 손상된 byte 수 발언으로 구체적인 exploit 또는 새 폭 규칙을 확정하지 않는다. [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 STT 52:03]]

## 핵심 정리

- RV64의 32×64 bits는 명목 256 bytes이며 `x0`은 변경할 수 없다.
- Array offset은 index×원소 byte 크기이고 ALU 계산과 memory 변경은 별개다.
- Endianness는 배치, signedness는 bit의 가중치, extension은 폭을 늘릴 때의 값 보존이다.
- Unsigned 64-bit 최댓값은 18,446,744,073,709,551,615이다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Register 폭과 역할

32개 64-bit register의 명목 용량을 구하고 `x0`, `x1=ra`, `x2=sp`를 비교하라. Storage hierarchy에서 작다는 말은 무엇을 설명하고 무엇을 보장하지 않는가?

<details><summary>해설 보기</summary>

32×64/8=256 bytes이다. STT의 128 bytes와 다른 산술 정정이며 `x0`의 8 bytes까지 자유롭게 쓸 수 있다는 뜻은 아니다. `x0`은 항상 0이고 나머지의 `ra/sp` 역할은 주로 calling convention이다. 32-bit word와 64-bit doubleword도 구분한다. Register→cache→main memory→SSD/HDD는 전형적으로 용량 증가·접근 속도 저하 관계이지만 'smaller is faster'는 예외 없는 법칙이 아니다.

**채점·확인:** 단위 환산, `x0` 예외, convention과 hardware 차이를 확인한다.

</details>

#### 확인 Q02 · 중간 합을 보존하기

`f=(g+h)-(i+j)`에서 `f,g,h,i,j=x19,x20,x21,x22,x23`이고 값은 7,5,3,2 (`g,h,i,j`)이다. 두 temporary로 instruction sequence와 결과를 쓰고 한 temporary를 덮어쓸 때의 오류를 설명하라.

<details><summary>해설 보기</summary>

`add x5,x20,x21`은 12, `add x6,x22,x23`은 5, `sub x19,x5,x6`은 7을 만든다. 둘째 합으로 첫 temporary를 덮으면 마지막 뺄셈의 첫 operand를 잃는다. 두 입력·한 출력이라는 규칙성으로 hardware를 공유하지만 복합 식은 여러 instruction이 필요하다. `t0/t1`은 자료의 virtual 이름이며 C 변수의 실제 register 배정은 compiler 선택이다.

**채점·확인:** 세 결과와 값의 생존 기간을 검산한다.

</details>

#### 확인 Q03 · Byte 순서와 operand 출처

주소 증가 순서로 `0xFF000000`과 `0x00000001`의 big/little-endian byte 배열을 쓰고 `01 00 00 00`의 두 해석을 구하라. Instruction fetch가 ALU의 직접 memory operand를 뜻하는가?

<details><summary>해설 보기</summary>

첫 값은 big `FF 00 00 00`, little `00 00 00 FF`; 둘째는 big `00 00 00 01`, little `01 00 00 00`이다. 주어진 bytes는 little에서 1, big에서 2^24=16,777,216이다. 주소 하나는 8-bit byte라 32-bit 값은 네 주소를 차지한다. Load-store는 큰 array 등의 값을 load→register 연산→store로 처리한다. Instruction을 가져오는 IF와 data operand의 출처는 별개다. 통신 시 순서를 합의해야 같은 값을 읽는다.

**채점·확인:** 낮은 주소와 낮은 수치 자릿수를 구별한다.

</details>

#### 확인 Q04 · 주소 모드와 array offset

Absolute·register indirect·based·indexed·memory indirect를 `MEM`과 `GPR`로 써라. 이어 `h=x21`, `base(A)=x22`, 원소 8 bytes인 `A[12]=h+A[8]`을 추적하라.

<details><summary>해설 보기</summary>

순서대로 `MEM[10000]`, `MEM[GPR[rbase]]`, `MEM[GPR[rbase]+offset]`, `MEM[GPR[rbase]+GPR[rindex]]`, `MEM[MEM[GPR[rbase]]]`이다. 마지막은 memory 값 자체를 다시 주소로 쓴다. Array에서는 `ld x9,64(x22); add x9,x21,x9; sd x9,96(x22)`이다. 64=8×8, 96=12×8 bytes이며 `A[8]`은 아홉째, `A[12]`는 열세째다. Offset은 총 배열 크기가 아니다. 일반 addressing 목록을 모두 RISC-V 단일 instruction이라고 읽지 않는다.

**채점·확인:** 다섯 주소 식과 세 instruction의 data 방향을 확인한다.

</details>

#### 확인 Q05 · Allocation·spill·immediate

Register가 부족할 때 spill이 필요한 이유와 비용을 설명하라. `addi x22,x22,4`의 장점은 무엇이며 compiler 최적화와 microarchitecture 최적화는 어떻게 다른가?

<details><summary>해설 보기</summary>

보관해야 할 값이 register 수를 넘으면 일부를 memory에 두고 필요할 때 load/store하므로 instruction과 접근 비용이 추가된다. Compiler는 자주 쓰는 값의 배정과 sequence를 바꾸고 microarchitecture는 주어진 sequence의 실행 방식을 개선한다. `addi`는 4를 instruction 안에 담아 별도 constant load 없이 `x22`를 4 증가시킨다. 흔한 작은 상수에 유용하지만 immediate 폭에 들어가는 경우만 해당한다.

**채점·확인:** Spill의 추가 접근과 immediate의 표현 범위 조건을 포함한다.

</details>

#### 확인 Q06 · Unsigned 값과 고정 폭

`00001011`과 8-bit unsigned 최댓값을 계산하고 64-bit 최댓값을 정확히 써라. Endianness를 바꾸거나 큰 정수 software를 사용하면 하나의 고정폭 register 범위가 늘어나는가?

<details><summary>해설 보기</summary>

양의 가중치 합으로 8+2+1=11, 최댓값은 2^8−1=255이다. 2^64−1=18,446,744,073,709,551,615이며 M003 p.17의 18,446,774,073,709,551,615와 과거 노트의 해당 수치는 오기다. 이 해설은 식을 계산한 정정이며 원문 인용을 바꾼 것이 아니다. Endianness는 byte 배치만 바꾸고 고정 bit 수의 범위는 그대로다. 큰 정수는 ISA 위의 software 표현으로 처리하며 한 register가 무한한 정수를 담는다는 뜻은 아니다.

**채점·확인:** 정확한 십진수와 정정의 출처, width 한계를 확인한다.

</details>

#### 확인 Q07 · Two's complement와 negation

8-bit `0xFE`의 signed/unsigned 값, signed 범위, 0·−1·최소·최대 pattern을 구하라. 32-bit `0xFFFFFFFC`, +2의 negation, 최솟값 negation의 한계도 설명하라.

<details><summary>해설 보기</summary>

8-bit unsigned는 254, signed는 −128+126=−2이다. n-bit signed 범위는 −2^(n−1)부터 2^(n−1)−1, 64-bit는 −9,223,372,036,854,775,808부터 9,223,372,036,854,775,807이다. Pattern은 `000…0`, `111…1`, `100…0`, `011…1` 순이다. 32-bit 예는 −2,147,483,648+2,147,483,644=−4이다. 8-bit +2의 `00000010`을 뒤집어 `11111101`에 1을 더하면 `11111110`이다. `x+~x`는 모든 bit 1이므로 modulo 2^n에서 −1, 따라서 `~x+1`이 −x의 pattern이다. 최솟값의 양의 대응값은 signed 범위 밖이라 pattern 계산과 표현 가능성을 분리한다.

**채점·확인:** 음수 최상위 가중치와 modular 증명·범위 예외를 모두 확인한다.

</details>

#### 확인 Q08 · 폭을 늘릴 때 값 보존

8-bit +2와 −2를 16 bits로 확장하라. Signed 12-bit immediate를 64 bits로 만들 때 복제할 bit와 새 자리 수는 무엇이며 zero extension은 언제 다른 결과를 내는가?

<details><summary>해설 보기</summary>

+2는 `0000000000000010`, −2는 `1111111111111110`이다. Sign bit를 복제하면 새 음수 최상위 가중치와 추가 양의 가중치가 원래 값을 보존한다. 12-bit에서는 bit 11을 위의 52자리에 복제한다. 음수에 zero extension을 쓰면 양의 값이 되어 의미가 바뀐다. Unsigned widening에는 zero extension이 맞다.

**채점·확인:** Bit 11·52자리, 양수·음수 두 결과와 값 보존 이유를 확인한다.

</details>

#### 확인 Q09 · Subword load와 store

`lb/lbu`, `lh/lhu`, `lw/lwu`, `sb/sh/sw`의 폭과 확장 규칙을 비교하라. `0x80`을 `lb`와 `lbu`로 읽은 결과 및 다시 `sb`로 저장한 byte는 무엇인가?

<details><summary>해설 보기</summary>

Load 폭은 8/16/32 bits이며 signed 계열은 64-bit destination으로 sign-extend, unsigned 계열은 zero-extend한다. `lb` 결과는 `0xFFFFFFFFFFFFFF80`(−128), `lbu`는 `0x0000000000000080`(128)이다. Store는 각각 하위 8/16/32 bits만 쓰므로 둘 다 `sb` 결과는 `0x80`이다. 따라서 register 결과가 달라도 좁은 store 결과는 같을 수 있다. C type·signedness가 instruction 선택에 영향을 주지만 자료의 type 크기는 모든 C 구현의 법칙이 아니며 불확실한 발화로 특정 exploit을 확정하지 않는다.

**채점·확인:** Access 폭과 destination 폭을 구별하고 signed store가 따로 필요 없는 이유를 답한다.

</details>

### 적용 연습

#### 연습 P01 · 같은 byte에서 다른 값

새로 만든 합성 연습이다. `x10=0x3000`, `MEM byte[0x3003]=0xFE`이다. A는 `lb x5,3(x10); addi x5,x5,1; sb x5,4(x10)`, B는 첫 instruction만 `lbu`로 바꾼다. 두 실행의 register 값과 저장 byte를 비교하고 “저장 byte가 같으면 계산 의미도 같다”, “ALU가 memory byte를 직접 더했다”를 평가하라.

연결: [EX:ca_2025_2_midterm_q02 p.2]의 operand 출처와 [EX:ca_2025_2_midterm_q04 p.2]의 값 보존을 결과 관찰·오류 진단으로 결합했다. 선수는 Q03·Q04·Q08·Q09이며 byte 확장은 수업 개념을 옮긴 새 상황이다.

<details><summary>해설 보기</summary>

A는 load 뒤 −2, 덧셈 뒤 −1(`0xFFFFFFFFFFFFFFFF`)이다. B는 254→255(`0x00000000000000FF`)이다. 둘 다 `0x3004`에 하위 byte `FF`를 쓰지만 64-bit 결과는 다르므로 같은 저장 byte가 같은 signed 의미를 보장하지 않는다. EA는 0x3000+3이고 load가 먼저 register를 채운다. `addi`는 register 값과 immediate 1을 더하며 memory를 직접 operand로 사용하지 않는다.

**채점·확인:** 두 64-bit 결과, 동일한 하위 byte, 두 유효 주소와 operand 출처를 모두 확인한다.

</details>

### 짧은 복습 계획

Q02·Q04를 손으로 trace하고 Q06–Q09는 bit 계산으로 검산하자. 다음 복습에서는 P01의 잘못된 설명을 먼저 고친 뒤 해설과 비교하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]
- [[courses/computer_architecture/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트]]
- [lec 03.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf) — [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-021), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.03/page-057)
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-015)
- [[courses/computer_architecture/transcripts/2026-09-08|2026-09-08 보정 STT]] — 17:48, 20:16, 23:03, 24:24, 30:44, 33:54, 39:47, 44:22, 48:31, 52:03, 53:56 (페이지 안의 시간 표기)
- [[courses/computer_architecture/transcripts/2026-09-10|2026-09-10 보정 STT]] — 05:12, 58:31 (페이지 안의 시간 표기)

9월 3일 addressing mode 비교는 자료 기반이며 모든 mode가 RISC-V 한 instruction인 것은 아니다. 9월 8일 STT의 128 bytes, 배열 전체 크기 표현과 임시 register 이름의 불확실성을 자료·산술로 구분했다. M003 p.17 및 과거 노트의 unsigned64 숫자 오기는 식 2^64−1로 바로잡은 해설이다. 9월 10일의 compiler flag·byte 수 불확실성을 복원하지 않으며 C type 크기를 모든 구현에 일반화하지 않는다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q02 p.2], [EX:ca_2025_2_midterm_q04 p.2].
