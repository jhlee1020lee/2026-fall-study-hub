---
title: "Congruence Classes와 Modular Inverse"
description: "대표원 독립성, inverse의 modulo 유일성과 GCD 조건을 계산·증명으로 확인한다."
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
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05"]
---

같은 remainder를 갖는 정수들을 하나의 class로 보고 연산의 의미를 확인한다. 나눗셈이나 소거 전에는 GCD로 inverse의 존재를 검사하고 Bézout 계수로 실제 값을 찾자.

## Congruence class와 대표원

Modular arithmetic(모듈러 산술)은 정수 전체를 같은 remainder끼리 묶어 계산하는 방법이다. 양의 modulus(법) $m$에 대해

$$a\equiv b\pmod m\quad\Longleftrightarrow\quad m\mid(a-b).$$

즉 두 수의 차이가 $m$의 배수다. [이산수학 M008 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)의 이 정의에서, $m=6$일 때 2와 8은 congruent(합동)이지만 정수로서 같은 수는 아니다.

Congruence class(합동류)는 한 정수와 합동인 정수들의 모임이다. Modulo 6의 2에 해당하는 class는 $\ldots,-10,-4,2,8,14,\ldots$다. 정수 전체는 서로 겹치지 않는 $m$개 classes로 partition(분할)된다. $\mathbb Z_m=\{0,1,\ldots,m-1\}$은 각 class에서 대표원 하나씩을 고른 residue system(잉여계)이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 34:50–35:50]]에서는 이를 앞서 사용한 연산의 복습으로 설명했다. 이 복습만으로 기록되지 않은 날의 정확한 진도를 역으로 정할 수는 없다.

### Addition과 multiplication이 대표원에 의존하지 않는 이유

대표원을 바꿀 때 결과의 class까지 바뀐다면 class 위의 계산이 잘 정의되지 않는다. $a,c$ 대신 같은 classes의 $a+km,c+\ell m$을 택해 보자. 두 합의 차이는

$$(a+km+c+\ell m)-(a+c)=m(k+\ell),$$

두 곱의 차이는

$$(a+km)(c+\ell m)-ac=m(kc+\ell a+k\ell m)$$

이다. 둘 다 $m$의 배수이므로 합과 곱의 결과 class는 바뀌지 않는다. 이것이 modular addition과 multiplication이 가능한 이유다.

해설용 modulo 6 계산에서 $2+5=7\equiv1$, $2\cdot5=10\equiv4$이다. 2 대신 8을 사용해도 $8+5=13\equiv1$, $8\cdot5=40\equiv4$가 된다. 계산 중 편한 대표원을 써도 마지막 residue가 같은 이유를 숫자로 확인할 수 있다.

## Multiplicative inverse와 division의 조건

이제 $m\ge2$로 두자. $ab\equiv1\pmod m$을 만족하는 $b$를 $a$의 multiplicative inverse(곱셈 역원) modulo $m$이라 한다. Division은 해당 inverse를 곱하는 것으로 이해한다. 따라서 $a$가 0이 아니라고 항상 inverse가 있는 것은 아니다.

$\mathbb Q,\mathbb R,\mathbb C$에서는 nonzero 원소가 inverse를 갖지만, $\mathbb Z_6$의 2에 정수를 곱한 remainder는 0, 2, 4 중 하나다. 1이 나올 수 없어 2의 inverse가 없다. “0이 아니므로 나누어 없앤다”는 실수 계산 습관이 modular arithmetic에서 실패하는 예다. 정의와 존재 조건은 M008 PDF p.24에 있다.

Subtraction은 additive inverse(덧셈 역원)를 더하는 연산이고, division은 multiplicative inverse를 곱하는 연산이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 36:34]]에는 subtraction을 multiplication의 역으로 표현한 대목이 있지만, 여기서는 두 연산을 수학적으로 바로잡아 구분한다. 두 종류의 inverse는 같은 것이 아니다.

### 유일하다는 말의 의미

Inverse가 존재할 때 유일하다는 것은 정수 하나만 가능하다는 뜻이 아니라 modulo $m$에서 하나의 class라는 뜻이다. $b,c$가 둘 다 inverse라면

$$b\equiv b(ac)\equiv(ba)c\equiv c\pmod m.$$

따라서 같은 class다. 예를 들어 5가 어떤 inverse이면 $5+m$도 같은 inverse class의 대표원이다. $\mathbb Z_m$에서 대표원을 하나로 정했을 때만 하나의 숫자로 나타난다.

## Bézout로 증명하는 존재 조건과 계산

Inverse의 정확한 조건은

$$a^{-1}\pmod m\text{가 존재한다}\quad\Longleftrightarrow\quad\gcd(a,m)=1$$

이다. 이를 양방향으로 보자. 먼저 $ab\equiv1\pmod m$이면 어떤 정수 $k$에 대해 $ab-km=1$이다. $g=\gcd(a,m)$는 $ab$와 $km$을 모두 나누므로 1도 나눈다. 따라서 $g=1$이다.

반대로 $\gcd(a,m)=1$이면 [[courses/discrete_mathematics/units/gcd-euclid-and-bezout|Bézout identity]]로 정수 $s,t$가 존재하여

$$as+mt=1.$$

Modulo $m$을 취하면 $as\equiv1$이므로 $s\bmod m$이 inverse다. $a$가 음수인 경우에도 $|a|$에 대한 Bézout 계수의 부호를 조정하여 같은 정수 선형결합을 얻는다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 41:10]]은 이 증명이 존재뿐 아니라 실제로 찾는 방법도 준다고 설명했다.

정의를 적용한 해설용 예로 modulo 7에서 3의 inverse를 구하자. $7=2\cdot3+1$이므로

$$1=7-2\cdot3.$$

따라서 3의 계수 $-2$가 inverse이고, 표준 대표원으로 바꾸면 $-2\equiv5\pmod7$이다. 직접 곱하면 $3\cdot5=15\equiv1$로 확인된다. 음수 계수를 잘못된 답으로 버릴 이유는 없으며 같은 class의 대표원으로 정리하면 된다.

### Congruence에서 cancellation이 가능한 때

$ac\equiv bc\pmod m$에서 $c$의 inverse가 있으면 양변에 이를 곱하여 $a\equiv b\pmod m$을 얻는다. 반대로 $\gcd(c,m)\ne1$이면 그런 cancellation(소거)을 보장할 수 없다. 해설용 modulo 6에서 $2\cdot1\equiv2\cdot4$이지만 $1\not\equiv4$다. 두 곱은 각각 2와 8이라 같은 residue가 되지만, 2는 inverse가 없다.

2021년 중간 Q1의 (i)는 바로 이런 소거 조건을 점검하는 연결이다. [EX:dm_2021_mid_q01 p.1] 이 자료의 학기는 미확인이며, RSA 등 같은 문항의 다른 항목까지 이 단원의 진도로 포함하지 않는다. 계산의 핵심은 양변에 무엇을 곱해 원래 연산을 되돌릴 수 있는지이며, 그 가능성을 GCD가 정확히 판정해 준다는 점이다.

## 핵심 정리

- Congruence는 정수 equality가 아니라 차이가 modulus의 배수라는 관계다.
- Addition·multiplication의 결과 class는 대표원을 바꿔도 같다.
- m≥2에서 inverse는 gcd(a,m)=1일 때만 존재하고 하나의 class로 유일하다.
- Inverse 없는 인수를 무조건 소거하면 서로 다른 residues를 같은 것으로 만들 수 있다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Congruence와 대표원

a≡b mod m의 뜻을 쓰고 modulo 6의 2에 해당하는 class를 설명하라. ℤₘ={0,…,m−1}과 정수 전체의 partition은 어떻게 연결되는가?

<details><summary>해설 보기</summary>

m>0에서 m|(a−b)라는 뜻이다. Modulo 6의 2 class는 …,−10,−4,2,8,14,…처럼 2+6k인 모든 정수다. 2와 8은 같은 class지만 같은 정수는 아니다. 모든 정수는 유일한 remainder 0,…,m−1 중 하나를 가지므로 m개의 서로 겹치지 않는 classes로 나뉜다. ℤₘ 표기는 각 class에서 하나씩 고른 대표원으로 계산하는 방식이다.

**점검 기준:** 차이의 divisibility·정수 equality와의 차이·유일 remainder에 따른 partition을 설명한다.

</details>

#### 확인 Q02 · 연산이 대표원에 무관한 이유

a,c를 a+km,c+ℓm으로 바꿀 때 합과 곱의 결과가 같은 class임을 보이라. Modulo 6에서 2 대신 8을 써 5와 더하고 곱하여 확인하라.

<details><summary>해설 보기</summary>

합의 차이는 m(k+ℓ), 곱의 차이는 m(kc+ℓa+kℓm)으로 모두 m의 배수다. 따라서 연산의 결과 class는 대표원 선택에 의존하지 않는다. 2+5=7≡1,8+5=13≡1이고 2·5=10≡4,8·5=40≡4다. 단지 한 예가 맞아서가 아니라 일반 차이가 m의 배수임을 보였기 때문에 well-defined하다.

**점검 기준:** 합·곱의 두 전개와 숫자 검산을 각각 수행한다.

</details>

#### 확인 Q03 · Inverse의 의미와 유일성

m≥2에서 multiplicative inverse를 정의하고 modulo 6의 2와 5를 비교하라. 5의 inverse가 5라면 11도 inverse인가? 두 inverse가 같은 class임을 증명하고 subtraction과 division을 구별하라.

<details><summary>해설 보기</summary>

ab≡1 mod m인 b가 a의 multiplicative inverse다. Modulo 6에서 2의 곱은 0,2,4만 되어 inverse가 없다. 5·5=25≡1이고 5·11=55≡1이므로 5와 11 모두 inverse의 대표원이다. b,c가 모두 inverse라면 b≡b(ac)≡(ba)c≡c이므로 하나의 class로 유일하다. Subtraction은 additive inverse를 더하는 것, division은 multiplicative inverse를 곱하는 것이다. Nonzero만으로 modular division이 가능하지는 않다.

**점검 기준:** 2의 불가능성·5와 11의 검산·class 유일성·두 종류 inverse를 설명한다.

</details>

#### 확인 Q04 · GCD 조건과 Bézout coefficient

Inverse가 존재할 필요충분조건을 양방향으로 증명하라. 7=2·3+1을 이용해 3 modulo 7의 inverse를 구하고 어떤 Bézout coefficient를 택하는지 설명하라.

<details><summary>해설 보기</summary>

Inverse가 있으면 ab−km=1이다. g=gcd(a,m)는 ab와 km을 모두 나누어 1도 나누므로 g=1이다. 반대로 gcd(a,m)=1이면 Bézout로 as+mt=1인 정수 s,t가 있고 modulo m에서 as≡1이므로 a의 계수 s가 inverse다. 1=7−2·3에서는 3의 계수 −2를 택해 −2≡5 mod 7이고 3·5=15≡1로 확인한다. m의 계수 t를 고르는 것이 아니다.

**점검 기준:** 양방향 divisibility·정수 계수의 존재·정확한 계수 선택과 대표원 정규화·검산을 포함한다.

</details>

#### 확인 Q05 · Cancellation의 조건

ac≡bc mod m에서 언제 a≡b mod m를 결론낼 수 있는가? 본문의 modulo 6 반례를 계산하라.

<details><summary>해설 보기</summary>

gcd(c,m)=1이면 c의 inverse를 양변에 곱해 ac·c⁻¹≡bc·c⁻¹, 즉 a≡b를 얻는다. Inverse가 없으면 일반적인 소거 보장은 없다. Modulo 6에서 2·1=2,2·4=8은 같은 residue 2이지만 1과 4의 차이 3은 6의 배수가 아니다. 2가 nonzero여도 inverse가 없어 이 소거는 실패한다.

**점검 기준:** 소거를 정당화하는 실제 inverse 연산과 반례의 두 합동 판정을 보인다.

</details>

### 적용 연습

#### 연습 P01 · Nonzero만 검사하는 나눗셈 규칙

**새로 만든 synthetic 연습.** [EX:dm_2021_mid_q01 p.1] (i)의 소거 전제 점검을 옮겼다. 선수내용은 residue·GCD·inverse이며 cipher 지식은 사용하지 않는다.

cx≡y mod m에서 'c≠0이면 x를 하나로 정할 수 있다'는 규칙을 검토하라. c=2,y=4에서 m=8의 residues를 직접 점검하고 m=9와 비교하라. 유일한 해를 inverse로 구하려는 규칙에는 어떤 검사가 필요한가?

<details><summary>해설 보기</summary>

Modulo 8에서 x=0,…,7의 2x residues는 0,2,4,6,0,2,4,6이다. 따라서 y=4의 해는 2와 6으로 둘이며 gcd(2,8)=2라 inverse가 없다. Modulo 9에서는 gcd(2,9)=1이고 2·5=10≡1이므로 inverse 5를 곱해 x≡5·4=20≡2다. 두 해가 있다면 inverse를 곱해 같은 class가 되어 유일하다. 필요한 검사는 c의 nonzero 여부가 아니라 gcd(c,m)=1이다. 이 조건 실패는 어떤 특정 y에도 해가 없다는 뜻이 아니라 inverse에 의한 일반적인 유일해 규칙을 사용할 수 없다는 뜻이다.

**점검 기준:** m=8의 두 해를 실제 계산하고 m=9의 inverse·유일성을 검산하며 조건 실패의 의미를 과장하지 않는다.

</details>

### 짧은 복습 계획

Q01–Q02에서 정수·class·대표원을 구분해 적는다. Q03–Q04를 양방향 증명과 곱셈 검산으로 확인한 뒤 Q05·P01에서 소거가 가능한 인수인지 먼저 검사한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 이산수학 강의·자료 연결]]

[03. Number Theory.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf) · 페이지별 보기: [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-005), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 STT]] · 35:50, 38:32, 41:10, 34:50, 36:34.

2026-09-23의 modular arithmetic 복습을 연결한다. 대표원 나열과 subtraction에 관한 불명확하거나 잘못된 발화는 수학적 정의와 구분한다. Inverse 설명은 m≥2로 한정하고, 음수 계수는 같은 class의 대표원으로 정리한다. 기록되지 않은 수업 날짜의 진도와 affine cipher·RSA까지 이 복습으로 추정하지 않는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

[[exam_questions/dm_2021_mid_q01|2021 학기 미확인 중간 Q1]]의 (i)에 있는 congruence cancellation 조건만 연결한다. [EX:dm_2021_mid_q01 p.1] 선수내용은 본문의 inverse 조건과 [[courses/discrete_mathematics/units/gcd-euclid-and-bezout|Bézout identity]]다. 같은 문항의 RSA·P/NP 및 다른 cipher 문항의 frequency analysis는 포함하지 않는다.


---

[[courses/discrete_mathematics/units/gcd-euclid-and-bezout|← 이전: GCD·Euclidean Algorithm·Bézout의 구성]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/hashing-and-data-distribution|다음: Hash Function과 데이터 분산 →]]
