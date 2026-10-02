---
title: "Congruence Classes와 Modular Inverse"
description: "합동류·역원의 증명과 binary modular exponentiation의 상태를 복습한다."
course: "discrete_mathematics"
unit_id: "modular-arithmetic-and-inverses"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["03. Number Theory.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05", "courses/discrete_mathematics/lectures/2026-09-28-lecture-06"]
---

같은 나머지의 정수들을 하나의 class로 보고 연산이 대표원에 의존하지 않는 이유를 확인한다. 역원으로 나눗셈의 조건을 정한 뒤 binary digits로 거듭제곱을 계산한다.

## Congruence class: 같은 나머지를 하나의 대상으로 다루기

Modular arithmetic(모듈러 산술)은 정수의 크기 전체보다 나머지가 중요한 계산을 표현한다. 양의 modulus $m$에 대해

$$a\equiv b\pmod m\quad\Longleftrightarrow\quad m\mid(a-b)$$

로 정의한다. 같은 나머지를 가진 정수들의 모임이 congruence class(합동류)다. 예를 들어 modulo 6에서 2와 8은 같은 class에 속하지만 같은 정수는 아니다. 모든 정수는 정확히 하나의 class에 속하므로 $\mathbb Z$는 서로 겹치지 않는 $m$개의 class로 나뉜다. $\mathbb Z_m=\{0,1,\ldots,m-1\}$은 각 class에서 대표원을 하나씩 선택한 residue system이다. [M008 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-005)

[[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: Congruence class와 Modular inverse]]의 설명을 따라, “대표원을 바꾸어도 계산 결과의 class가 같다”는 사실을 확인해 보자. $a,c$ 대신 $a+km,c+\ell m$을 써도 합의 차이는 $m(k+\ell)$이고, 곱의 차이는

$$
(a+km)(c+\ell m)-ac=m(kc+\ell a+k\ell m)
$$

이므로 둘 다 $m$의 배수다. 그래서 class 위의 addition과 multiplication이 대표원 선택과 무관하게 정의된다. Modulo 6에서 $2+5=7$과 $8+5=13$은 둘 다 대표원 1로 돌아온다. 이것이 단순히 작은 숫자만 기억해도 계속 계산할 수 있는 이유다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 34:50–35:50]]

## Modular inverse: 나눗셈이 가능한 정확한 조건

이제 $m\ge2$로 두자. $ab\equiv1\pmod m$인 $b$가 존재하면 이를 $a$의 multiplicative inverse(곱셈 역원)라고 하고 $a^{-1}$로 적는다. Modular division은 이 inverse를 곱하는 연산으로 이해한다. Subtraction은 additive inverse를 더하는 것이다. 녹취에서 subtraction을 multiplication의 역으로 설명한 부분은 이 구별과 맞지 않으므로 그대로 수학적 정의로 채택하지 않는다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 36:34–38:32]]

$\mathbb Q,\mathbb R,\mathbb C$에서는 모든 nonzero 원소에 multiplicative inverse가 있지만, $\mathbb Z_m$에서는 nonzero만으로 부족하다. $\mathbb Z_6$의 2에 무엇을 곱해도 나머지는 $0,2,4$ 중 하나다. 결코 1이 되지 않으므로 $2^{-1}$은 없다.

Inverse가 존재할 때 유일하다는 말도 **modulo $m$에서 유일하다**는 뜻이다. $b,c$가 둘 다 $a$의 inverse이면

$$b\equiv b(ac)\equiv(ba)c\equiv c\pmod m.$$

예를 들어 modulo 6에서 5의 inverse로 5와 11을 적을 수 있지만 $5\equiv11\pmod6$이므로 같은 inverse class다. [M008 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

### GCD와 Bézout identity로 필요충분조건 증명하기

정확한 조건은

$$a^{-1}\pmod m\text{이 존재한다}\quad\Longleftrightarrow\quad\gcd(a,m)=1$$

이다. 먼저 inverse $b$가 있으면 어떤 정수 $k$에 대해 $ab-km=1$이다. $g=\gcd(a,m)$는 $ab$와 $km$을 모두 나누므로 1도 나누어야 한다. 따라서 $g=1$이다.

반대로 $\gcd(a,m)=1$이면 Bézout identity(베주 항등식)에 의해 정수 $s,t$가 존재해 $as+mt=1$이 된다. Modulo $m$을 취하면 $as\equiv1$이므로 $s\bmod m$이 inverse다. Extended Euclidean algorithm은 이 $s,t$를 실제로 구한다. 존재한다는 주장에 계산 방법까지 붙는 constructive proof다. Bézout의 역대입이 낯설다면 [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: GCD에서 Bézout 계수로]]를 먼저 연결해서 읽을 수 있다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 39:30–42:08]]

해설용 작은 계산으로 $7=2\cdot3+1$을 $1=7-2\cdot3$으로 고치면, modulo 7에서 3의 inverse는 $-2\equiv5$다. 검산은 $3\cdot5=15\equiv1$이다. 음수인 Bézout 계수도 올바른 inverse를 주며, 필요하면 $0,\ldots,m-1$의 대표원으로 바꾸면 된다.

### 소거는 inverse가 있을 때 가능하다

정수나 실수에서 하던 나눗셈을 합동식에 무조건 옮기면 위험하다. $ac\equiv bc\pmod m$에서 $c$에 inverse가 있으면 양쪽에 곱해 $a\equiv b$를 얻는다. 그러나 modulo 6에서 $1\cdot2\equiv4\cdot2$여도 $1\not\equiv4$다. 이 새 설명용 반례에서 소거하려던 2에는 inverse가 없다. 기출의 소거 조건 판정에 필요한 사고도 “곱해진 수가 0이 아닌가”에서 멈추지 않고 modulus와 서로소인지 검사하는 것이다. [EX:dm_2021_mid_q01 p.1]의 (i)에 연결되며, 해당 2021년 자료의 학기는 미확인이다.

## Binary modular exponentiation: 필요한 제곱만 조합하기

RSA처럼 큰 exponent를 쓰는 계산에서 $b^n$ 전체를 먼저 만들면 불필요하게 큰 중간 정수를 다루게 된다. 대신 각 multiplication 뒤에 modulo를 취하고, exponent의 binary digits를 이용하면 적은 단계로 결과를 구할 수 있다. [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: RSA의 거듭제곱 계산]]에서는 이 방법을 이전 도구의 재사용으로 연결했다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 12:40]]

먼저 필요한 positional representation(위치 기수법)을 자료로 보충하자. Base $B>1$의 digit는 $0,\ldots,B-1$이고, 양의 정수는 leading digit가 0이 아닌 $\sum_j a_jB^j$로 유일하게 표현된다. $965=9\cdot10^2+6\cdot10+5$가 익숙한 예다. Computing에서는 binary(2), octal(8), hexadecimal(16)을 사용한다. [M008 pp.6–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)의 이 보충을 전체 binary arithmetic 코드가 당일 새로 강의되었다는 뜻으로 읽지는 않는다.

$n=\sum_{i=0}^{k-1}a_i2^i$이면

$$b^n=\prod_{i:a_i=1}b^{2^i}.$$

따라서 $b,b^2,b^4,b^8,\ldots$를 차례로 squaring(제곱)하고 bit가 1인 항만 누적하면 된다. 아래는 [M008 p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-010)의 loop를 읽기 쉽게 적은 것이다. $n>0$, $m\ge2$이며 낮은 bit부터 처리한다.

```text
x := 1
power := b mod m
for i := 0 to k - 1
    if ai = 1 then
        x := (x * power) mod m
    power := (power * power) mod m
return x
```

Bit $i$ 처리 직전에는 $power\equiv b^{2^i}$이고 $x$는 이미 처리한 낮은 bit들의 exponent에 해당하는 곱이다. Bit가 1이면 현재 `power`를 포함하고, 어느 경우든 square해서 다음 자릿값으로 넘어간다. **0 bit에서 생략하는 것은 누적 곱셈뿐이며 squaring은 생략하지 않는다.**

자료의 방법을 적용한 새 계산으로 $3^{13}\bmod7$을 보자. $13=(1101)_2$이므로 처리 순서는 $1,0,1,1$이다.

| Bit 위치 $i$ | $a_i$ | 처리 직전 `power` | 누적 후 `x` | 제곱 후 `power` |
|---|---:|---:|---:|---:|
| 0 | 1 | 3 | 3 | 2 |
| 1 | 0 | 2 | 3 | 4 |
| 2 | 1 | 4 | $12\bmod7=5$ | 2 |
| 3 | 1 | 2 | $10\bmod7=3$ | 4 |

답은 3이다. 마지막 `power`는 다음 bit가 없으므로 더 쓰이지 않는다. Loop는 exponent의 bit 수만큼 돌아 $O(\log n)$번의 modular multiplications를 사용한다. 이는 각 multiplication 자체의 bit cost까지 포함한 복잡도는 아니다. $n=0$에서는 빈 exponent의 관례에 따라 $b^0\bmod m=1\bmod m$을 별도로 반환한다.

## 핵심 정리

- Congruence는 정수 equality가 아니며 residue는 class의 대표원이다.
- 덧셈·곱셈은 대표원을 바꾸어도 같은 class를 준다. 나눗셈은 divisor의 역원이 있어야 한다.
- $a^{-1}\pmod m$의 존재 조건은 $\gcd(a,m)=1$이고, Bézout에서 $a$의 계수를 취해 구한다.
- 역원의 유일성은 정수 하나가 아니라 modulo $m$의 class에 관한 것이다.
- Binary exponentiation에서는 0 bit에서도 squaring을 한다. Modular multiplication 횟수와 bit cost는 구별한다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 대표원을 바꾸어도 되는 이유

$a\equiv b\pmod m$을 divisibility로 정의하고 class와 대표원을 구별하라. Modulo 6에서 2 대신 8로 5를 더하고 곱해 비교한 뒤, 일반적인 대표원 교체에서 addition·multiplication이 well-defined임을 보이라.

<details><summary>해설 보기</summary>

정의는 $m\mid(a-b)$다. 같은 나머지의 정수들이 한 class이며 정수 전체는 $m$개의 겹치지 않는 class로 나뉜다. $0,\ldots,m-1$은 그 대표원 선택이다. 2와 8은 다른 정수지만 같은 class다. 합 7과 13은 residue 1, 곱 10과 40은 residue 4로 일치한다.

$a,c$ 대신 $a+km,c+\ell m$을 쓰면 합의 차이는 $m(k+\ell)$, 곱의 차이는 $m(kc+\ell a+k\ell m)$이다. 모두 $m$의 배수이므로 결과 class는 같다.

**채점·확인:** 정의·partition·대표원·합과 곱의 두 일반식까지 확인한다.

</details>

#### 확인 Q02 · 곱셈 역원과 유일성

$m\ge2$에서 역원을 정의하고 subtraction과 division을 구별하라. Modulo 6의 2는 왜 역원이 없으며, 5의 역원으로 5와 11을 함께 쓸 수 있는가? 역원의 modulo 유일성도 증명하라.

<details><summary>해설 보기</summary>

$ab\equiv1\pmod m$인 $b$가 $a$의 곱셈 역원이다. Subtraction은 덧셈 역원을 더하는 일이고 division은 곱셈 역원을 곱하는 일이다. $\mathbb Q,\mathbb R,\mathbb C$와 달리 residue에서 nonzero만으로 나눗셈이 가능한 것은 아니다.

Modulo 6에서 $2b$의 residue는 0,2,4뿐이라 1이 될 수 없다. 반면 $5\cdot5=25$, $5\cdot11=55$는 모두 1 modulo 6이며 $5\equiv11$이므로 같은 inverse class다. 일반적으로 $ab\equiv ac\equiv1$이면 $b\equiv b(ac)\equiv(ba)c\equiv c$다.

**채점·확인:** 정의·두 역연산·nonzero 반례·class 유일성의 계산을 모두 제시한다.

</details>

#### 확인 Q03 · GCD 조건의 양방향 증명

역원이 존재할 필요충분조건이 $\gcd(a,m)=1$인 이유를 양방향으로 보이라. $1=7-2\cdot3$에서 3의 modulo 7 역원을 찾고 검산하라.

<details><summary>해설 보기</summary>

역원 $b$가 있으면 $ab-km=1$인 정수 $k$가 있다. $\gcd(a,m)$는 좌변 두 항을 나누므로 1도 나누어야 하여 GCD가 1이다.

반대로 GCD가 1이면 Bézout의 $as+mt=1$을 얻는다. Modulo $m$에서 $mt$가 사라지므로 $s\bmod m$이 역원이다. Extended Euclidean 계산은 이 계수를 실제로 제공한다. 예에서는 3에 곱한 계수가 $-2$이므로 역원은 $-2\equiv5\pmod7$이고 $3\cdot5=15\equiv1$로 확인된다. $m$의 계수와 혼동하지 않는다.

**채점·확인:** 필요성의 공약수 논증, 충분성의 Bézout, 계수 선택과 검산을 확인한다.

</details>

#### 확인 Q04 · 위치 기수법과 지수의 분해

Base $B>1$ 표현의 digit 범위와 leading digit 조건을 적고 965의 십진 표현, 13의 이진 표현을 설명하라. 왜 $b^{13}$에 $b,b^4,b^8$을 쓰며 computing의 base 2·8·16은 무엇인가?

<details><summary>해설 보기</summary>

양의 정수는 $0\le a_j<B$, 최고 digit는 0이 아닌 $\sum_j a_jB^j$로 유일하게 표현한다. $965=9\cdot10^2+6\cdot10+5$다. $13=8+4+1=(1101)_2$이므로 $b^{13}=b^8b^4b$다. Base 2는 binary, 8은 octal, 16은 hexadecimal이다.

일반적으로 $n=\sum a_i2^i$를 지수법칙에 넣으면 1 bit 위치의 $b^{2^i}$만 곱하면 된다. 이 자리값·구체 loop는 자료로 보충한 내용이며 9월 28일에는 RSA에서 squaring을 재사용한다는 연결이 있었다.

**채점·확인:** digit·leading 조건, 두 위치표현과 지수 분해를 확인한다.

</details>

#### 확인 Q05 · 0 bit에서도 제곱하는 이유

$3^{13}\bmod7$을 낮은 bit부터 추적하라. 각 단계의 누적값과 다음 power를 적고 두 변수의 invariant, $n=0$ 처리, $O(\log n)$의 비용 단위를 설명하라.

<details><summary>해설 보기</summary>

초기 $(x,power)=(1,3)$이고 처리 bit는 $1,0,1,1$이다. 누적·제곱까지 한 상태는 $(3,2),(3,4),(5,2),(3,4)$이므로 답은 3이다. 두 번째 bit에서 누적은 그대로지만 power는 $2^2\bmod7=4$로 바뀐다.

Bit $i$ 직전 power는 $b^{2^i}$의 residue이고 $x$는 이미 처리한 낮은 bit의 지수 합에 해당하는 residue다. 0 bit는 누적 곱만 생략하며 제곱은 다음 자리로 이동하기 위해 필요하다. $n=0$은 빈 곱으로 $1\bmod m$을 반환한다. $n>0$에서 bit 수에 비례한 modular multiplication 횟수가 $O(\log n)$이며 각 큰 정수 곱의 bit cost까지 센 것은 아니다.

**채점·확인:** 네 상태·두 invariant·0 bit·0 exponent·연산 단위를 모두 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 소거를 허용하는 조건 고치기

**새로 만든 기출 연결 합성 연습.** [EX:dm_2021_mid_q01 p.1]의 (i)에서 소거 조건을 검토하는 추론을 옮겼다. Q02–Q03이 선수 내용이며 같은 문항의 다른 소문항은 포함하지 않는다. 2021년 자료의 학기는 미확인이다. [[exam_questions/dm_2021_mid_q01|2021 중간 Q1 미리보기]]

Modulo 8에서 두 식 $2x\equiv6$과 $3x\equiv6$을 받았다. 모든 residue 해를 비교하고 “0이 아닌 계수는 약분할 수 있다”는 규칙을 올바른 충분조건으로 고쳐라.

<details><summary>해설 보기</summary>

첫 식은 $x=3,7$에서 성립한다. 실제로 $2\cdot3=6$, $2\cdot7=14\equiv6$이다. $x=0,\ldots,7$의 곱 residue는 $0,2,4,6,0,2,4,6$이므로 다른 해는 없다. 2는 nonzero지만 GCD가 2여서 역원이 없다.

3은 $\gcd(3,8)=1$이고 $3\cdot3\equiv1$이다. 역원 3을 곱하면 $x\equiv18\equiv2$로 유일하다. 올바른 충분조건은 계수와 modulus가 서로소라는 것이다. 역원이 있으면 양변에 곱해 소거할 수 있다. 두 식의 해 수 차이가 nonzero만으로 부족함을 드러낸다.

**채점·확인:** 첫 식의 두 해와 완전성, 둘째 역원·유일해, GCD 조건을 제시한다.

</details>

#### 연습 P02 · 조건문 안에 들어간 squaring

**새로 만든 강의 기반 일반 연습.** Binary modular exponentiation 자체의 직접 기출 문항은 없다.

13의 낮은 bit 순서 $1,0,1,1$에서 power의 squaring도 1 bit일 때만 실행하도록 잘못 고쳤다고 하자. 초기 $(1,3)$, modulus 7로 네 단계를 계산해 올바른 Q05와 비교하고, 어느 invariant가 처음 깨지는지 설명하라.

<details><summary>해설 보기</summary>

잘못된 상태는 $(3,2),(3,2),(6,4),(3,2)$다. 마지막 누적값 3은 우연히 정답과 같다. 하지만 0 bit인 두 번째 단계 뒤 power가 4로 바뀌어야 하는데 2에 머무르므로 다음 bit에서 $3^4\bmod7=4$라는 invariant가 이미 깨졌다.

정답 하나의 일치는 correctness 증명이 아니다. Squaring을 조건문 밖으로 옮기면 Q05의 상태열이 복구된다. 특히 세 번째 단계의 누적값도 올바른 값 5 대신 6이므로 과정의 오류를 직접 확인할 수 있다.

**채점·확인:** 잘못된 네 상태, 우연한 최종 일치, 최초 invariant 실패와 수정 위치를 확인한다.

</details>

### 복습 순서

Q01–Q03의 증명을 식으로 재현한 뒤 Q04–Q05의 자리값·상태표를 손으로 계산한다. P01에서 소거의 전제를 찾고 P02에서 0 bit 처리 오류를 고친다. 다음 날 곱셈 검산으로 역원과 최종 residue를 확인한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트 · 2026-09-23 · 이산수학 5강]]
- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 녹취]] — 34:50–42:08 합동류·역원. 시간 표시는 녹취 본문에서 찾는다.
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 12:40 RSA에서 inverse·binary squaring 재사용. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [03. Number Theory.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)
  - 합동과 역원: [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-005), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)
  - 자료로 보충한 자리값·거듭제곱: [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-007), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-010)

### 읽을 때의 범위

- 9월 23일의 합동류·역원 설명과 9월 28일의 RSA 계산 도구 복습을 연결한다. 위치 기수법과 구체 exponentiation loop는 자료로 보충한 범위다.
- Subtraction을 multiplication의 역으로 말한 녹취와 s/x 기호 충돌은 미해결 발화다. 정돈한 정의·증명을 정확한 발화 복원으로 보지 않는다.
- 역원·나눗셈 예는 m≥2로 한정한다. 소거는 invertible한 계수에만 적용하며 유일성은 modulo class에 관한 것이다.
- Binary full-adder·multiplication 전체 코드와 상세 primality-test 강의까지 확장하지 않는다. O(log n)은 modular multiplication 횟수다.
- 기출은 2021년 학기 미확인 Q1(i)에만 연결한다. 과거 배점·규칙을 현재 학기에 옮기지 않으며 제공 답안을 정답 근거로 사용하지 않는다.
- 공개 보정 녹취의 불명확한 말·가림과 음성 누락 가능성을 이 복습에서 해소한 것은 아니다.
