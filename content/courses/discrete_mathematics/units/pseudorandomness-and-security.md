---
title: "Pseudorandom Generation과 Cryptographic 요구"
description: "Seed expansion의 한계, LCG trace·LSB·cycle과 cryptographic 요구를 확인한다."
course: "discrete_mathematics"
unit_id: "pseudorandomness-and-security"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: []
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05"]
---

Seed에서 긴 출력을 만들 때 재현성·출력 종류·state 반복을 함께 본다. 실험용 품질과 공격자를 고려한 요구가 어떻게 다른지 구분하자.

## Seed에서 시작하는 pseudorandom generation

Simulation(모의실험), 통계 계산, machine learning 실험에서는 다양한 random-looking data(무작위처럼 보이는 데이터)가 필요하다. 실제 관측을 항상 충분히 수집할 수 없거나 같은 실험을 재현하고 싶을 때 생성된 데이터를 사용한다. 하지만 [[courses/discrete_mathematics/units/paradigms-greedy-and-computability|Deterministic computation]]에 아무 입력 조건도 없이 무작위 문자열을 만들라고 하는 것은 충분한 명세가 아니다. 같은 상태에서 같은 규칙을 실행하면 같은 결과가 나오기 때문이다.

Seed(초기값)는 이 계산을 시작하는 짧은 입력이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 51:13–53:02]]에서는 물리적 관측이나 timestamp(시각 정보)의 작은 자리에서 seed를 얻는 동기를 소개했다. 분 단위처럼 천천히 바뀌는 값보다 작은 단위가 다양해 보일 수 있지만, 시계의 정밀도와 관측 가능한 정보는 유한하다. 어떤 시간 자리가 균등해 보인다는 인상은 uniform distribution이나 secure entropy(보안에 필요한 불확실성)의 검증이 아니다. 구체적인 시간 추출 algorithm이나 entropy 수치는 제공되지 않았다.

Pseudorandom generator(의사난수 생성기, PRG) 또는 pseudorandom number generator(PRNG)는 이 짧은 seed를 긴 출력으로 확장하는 계산으로 이해할 수 있다. 길이만 늘리는 것은 쉽다. Seed를 여러 번 복사해 이어 붙이면 된다. 하지만 반복 구조가 곧 드러나므로 필요한 random-looking 성질을 얻었다고 할 수 없다.

## Deterministic expansion과 가능한 output 수

강의의 확장 관점을 기호로 정리하여

$$G:\{0,1\}^{s}\to\{0,1\}^{L},\qquad L>s$$

인 deterministic function을 생각하자. 가능한 seeds는 $2^s$개이므로 가능한 outputs도 많아야 $2^s$개다. 반면 모든 $L$-bit strings는 $2^L$개다. 그러므로 고정된 seed 길이에서 deterministic하게 만든 출력 분포가 전체 $L$-bit strings의 uniform distribution과 정확히 같을 수는 없다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 54:51]]은 입력 종류가 적으면 출력 종류도 그 수를 넘지 못한다는 이유를 설명했다.

숫자로 보기 위한 해설용 예로 $s=2,L=4$이면 네 seeds에서 나오는 outputs는 최대 네 개다. 전체 4-bit strings는 열여섯 개이므로 적어도 열두 개는 나오지 않는다. 출력 길이가 늘었다고 독립적인 무작위 정보가 저절로 생긴 것은 아니다. 목표는 이 정보이론적 차이가 없어지는 것이 아니라, 정한 용도나 계산 능력에서 원하는 분포와 쉽게 구별되지 않는 성질이다.

### 같은 seed와 연속 호출의 구별

같은 initial seed와 state에서 시작하는 deterministic generator는 같은 sequence를 만든다. 이는 실험 재현에 유용하다. 그러나 generator를 연속 두 번 호출할 때 state가 갱신된다면 서로 다른 값이 나올 수 있다. 같은 seed로 다시 시작하는 것, 실행을 이어 가는 것, re-seeding(초기값 재설정)을 하는 것은 다르다.

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 55:47]]의 자동 seeding과 두 번 호출 설명은 특정 API의 동작을 확정하기에 불명확하다. 따라서 여기서는 API 이름별 동작을 단정하지 않고 초기화와 state progression(상태 진행)을 나누어 이해한다.

## Linear Congruential Method의 계산과 cycle

Linear Congruential Method(선형 합동법)는 [[courses/discrete_mathematics/units/modular-arithmetic-and-inverses|modular arithmetic]]으로 state를 갱신한다. Parameters(매개변수) $a,c,m$과 initial state $x_0$를 정하고

$$x_{n+1}=(ax_n+c)\bmod m$$

을 반복한다. 식은 다음 state가 현재 state 하나로 결정되는 [[courses/discrete_mathematics/units/sets-functions-sequences|recurrence relation]]이다. 출력에는 state 자체를 쓰거나 그 일부를 추출할 수 있다.

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 56:47–58:40]]의 예에서 $a=3,c=7,x_0=9$는 읽히지만 modulus는 14와 13이 섞인다. 다음은 보고된 수열과 일치하는 $m=13$을 명시적으로 선택한 해설이다.

| 단계 | 나머지를 취하기 전 | Modulo 13 state |
|---|---:|---:|
| $x_0$ | 초기값 | 9 |
| $x_1$ | $3\cdot9+7=34$ | 8 |
| $x_2$ | $3\cdot8+7=31$ | 5 |
| $x_3$ | $3\cdot5+7=22$ | 9 |

따라서 $9\to8\to5\to9\to\cdots$이고 cycle(순환)의 길이는 3이다. $m=14$를 사용하면 첫 값부터 $34\bmod14=6$이므로 같은 trace가 아니다. 산술이 13에서 일치한다는 사실이 강사가 내내 13이라고 말했다는 증거는 아니다.

Least significant bit(최하위 비트, LSB)를 추출하면 정수의 홀짝만 남는다. 위 trace의 $x_0$부터의 LSB는 $1,0,1,1,0,1,\ldots$다. 원래 state의 반복이 output의 반복을 만들어 낸다. 일부 bit만 출력한다고 반복 구조가 자동으로 사라지지 않는다.

### 유한 state가 period를 제한하는 이유

가능한 states가 $m$개이므로 $m+1$번의 state 관측 중에는 같은 값이 적어도 두 번 나타난다. 같은 state에서는 다음 state가 결정적으로 같으므로 그 이후도 반복된다. 따라서 eventual cycle의 길이는 $m$을 넘을 수 없다. 하지만 처음부터 cycle에 들어 있는지, cycle 전에 transient(과도 구간)가 있는지, 얼마나 긴 period(주기)를 얻는지는 parameters와 seed에 달려 있다.

위 예에서는 처음 state 9로 돌아와 바로 길이 3의 cycle이다. 이것을 모든 Linear Congruential Method가 처음부터 최대 period $m$으로 돈다고 일반화할 수 없다. $m$을 크게 잡거나 $a$를 홀수로 잡는 것만으로 full period나 좋은 통계적 성질, 보안성을 모두 얻는 것도 아니다. 별도의 full-period 정리는 이번 설명에서 유도되지 않았다.

## 일반용 품질과 cryptographic 요구

[[courses/discrete_mathematics/units/hashing-and-data-distribution|Hash function]]과 PRNG는 용도에 따라 요구가 달라진다. Lookup에서는 보통 들어오는 key들의 적절한 분산이 중요하고, simulation에서는 실험에 필요한 random-looking 품질과 재현성이 중요하다. Cryptographic(암호학적) 용도에서는 구조를 일부러 분석하고 약점을 찾으려는 adversary(공격자)를 고려한다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 01:00:30–01:02:24]]의 구별은 이 요구의 차이다.

| 대상 | 일반적인 목적의 예 | Cryptographic 요구의 예 |
|---|---|---|
| Hash | 실제 key를 여러 bucket에 분산 | 의도적으로 collision을 찾는 계산이 어렵다. |
| PRNG | 재현 가능한 실험용 sequence | 효율적인 계산으로 uniform output과 구별하기 어렵다. |

Collision resistance(충돌 저항성)는 collision이 수학적으로 없다는 뜻이 아니다. 무한 입력과 유한 출력의 hash에는 collision이 존재하지만, 제한된 계산 자원으로 찾아내기 어려워야 한다는 요구다. 마찬가지로 cryptographic pseudorandomness가 앞서 계산한 output 종류 수의 차이를 없애지는 않는다. 요구하는 것은 효율적인 구별에 대한 어려움이다.

Modulo hash에서는 $x$와 $x+m$으로 collision을 쉽게 만들 수 있다. Linear Congruential Method 역시 긴 period만으로 cryptographic 성질이 생기지 않는다. 강의는 패턴을 구별하거나 parameters를 복구할 가능성을 지적했지만 구체적인 복구 algorithm을 전개한 것은 아니다. 단지 “random”이나 “hash”라는 이름이 붙었다고 같은 요구를 만족한다고 볼 수 없다.

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 01:03:15–01:04:14]]는 목적에 맞는 library·OS의 기능을 선택하고 계산 비용도 고려해야 한다고 설명했다. 특정 API, 불명확한 알고리즘 이름, platform별 성능 수치는 이 설명에서 확정되지 않았다. 따라서 구현을 선택할 때는 필요한 성질을 실제로 제공하는 interface인지 확인해야 한다. 일반용 실험의 재현성, 데이터 분산, 공격자에 대한 저항성은 서로 다른 조건이며, 하나의 긴 출력이나 긴 period만으로 모두 보장되지 않는다.

## 핵심 정리

- Deterministic expansion은 가능한 seed보다 많은 종류의 전체 output을 만들지 못한다.
- 같은 초기 seed의 재시작과 state가 진행하는 연속 호출은 다르다.
- 반복 state는 이후 반복을 강제하지만 최대 period와 초기 transient는 parameters에 달려 있다.
- Collision resistance와 pseudorandomness는 제한된 계산 자원을 고려한 요구이며 collision의 부재나 정확한 uniformity가 아니다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Seed의 동기와 관측 한계

Simulation·통계·machine learning 실험에서 random-looking data가 필요한 이유를 말하라. Deterministic computer에 조건 없이 무작위 출력을 요구하거나 timestamp의 낮은 자릿수를 안전한 seed라고 단정할 수 없는 이유는 무엇인가?

<details><summary>해설 보기</summary>

관측 데이터를 충분히 모으기 어렵거나 실험을 재현하려는 경우 생성 데이터를 쓸 수 있다. Deterministic 계산은 같은 입력·상태에서 같은 결과를 내므로 seed 등 시작 조건 없이 '무작위로 만들라'는 말만으로는 충분한 명세가 아니다. Timestamp의 작은 자리가 다양해 보여도 clock precision·가능한 값·편향·예측 가능성과 관측 정보가 제한된다. 그런 인상만으로 uniform distribution이나 secure entropy를 검증한 것이 아니며 구체 entropy 수치는 공급되지 않았다.

**점검 기준:** 생성의 용도·deterministic 재현성과 seed 역할·관측의 유한성·미검증 entropy를 구분한다.

</details>

#### 확인 Q02 · Output support의 상한

G:{0,1}ˢ→{0,1}ᴸ, L>s가 deterministic일 때 가능한 output 수를 설명하라. s=2,L=4와 s=8,L=100을 계산하고 seed를 여러 번 이어 붙이면 무엇이 해결되지 않는지 말하라.

<details><summary>해설 보기</summary>

Seed가 2ˢ개라 output은 최대 2ˢ종류다. s=2,L=4에서는 최대 4종류뿐이며 전체 16개 중 적어도 12개는 나오지 않는다. s=8,L=100에서는 최대 256개로 2¹⁰⁰개 전체 strings에 확률을 주는 uniform과 같을 수 없다. Seed를 복사해 이어 붙이면 길이는 늘지만 반복 패턴이 드러나며 새로운 독립 무작위 정보가 자동 생성되지 않는다. 어떤 용도나 계산 능력에서 쉽게 구별되지 않는지는 이 종류 수의 상한과 별도의 문제다.

**점검 기준:** '최대'와 전체 strings 수를 구별하고 길이·정보량·구별 가능성을 나눈다.

</details>

#### 확인 Q03 · 재시작과 연속 호출

같은 seed에서 시작하면 같은 sequence라는 말이 한 실행에서 두 번 호출하면 같은 값이라는 뜻인가? Re-seeding과 state progression을 구별하여 설명하라.

<details><summary>해설 보기</summary>

같은 initial seed와 state로 다시 시작하면 같은 sequence를 재현한다. 하지만 연속 호출은 앞선 호출이 state를 바꾼 뒤 다음 state에서 실행할 수 있어 다른 값을 낸다. 예를 들어 본문의 state 9에서 진행하면 8,5가 차례로 나오지만 매번 9로 재시작하면 첫 값 8을 반복한다. 이는 명시한 recurrence의 설명이며 특정 API의 자동 seeding 규칙을 확정한 것은 아니다.

**점검 기준:** 초기화·연속 state 갱신·다시 seeding의 차이를 실제 순서로 설명한다.

</details>

#### 확인 Q04 · LCG의 modulus 충돌과 LSB

xₙ₊₁=(3xₙ+7) mod m, x₀=9에서 m=13으로 세 단계를 계산하고 x₀부터 LSB를 쓰라. m=14의 첫 state와 비교하면 발화에 관해 무엇까지 말할 수 있는가?

<details><summary>해설 보기</summary>

m=13에서는 34 mod 13=8,31 mod 13=5,22 mod 13=9이므로 9→8→5→9다. 처음 state로 돌아와 cycle 길이는 3이다. LSB는 홀짝이므로 1,0,1,1,0,1,…다. m=14라면 첫 값은 34 mod 14=6이라 같은 trace가 아니다. 보고된 8과 산술이 맞는 선택은 m=13이지만 이것으로 14라는 발화가 없었다거나 강사가 내내 13을 사용했다고 확정할 수 없다.

**점검 기준:** 세 나머지·cycle·LSB·다른 modulus의 첫 값과 남은 출처 충돌을 모두 기록한다.

</details>

#### 확인 Q05 · Finite state와 eventual period

Modulo m state가 m개일 때 왜 결국 cycle이 생기고 그 길이가 m을 넘지 않는가? 처음 state부터 cycle에 있어야 하는가? 큰 m이나 odd multiplier가 maximal period를 보장하는가?

<details><summary>해설 보기</summary>

m+1번의 state 관측에는 같은 state가 적어도 두 번 등장한다. 같은 state에서는 다음 state가 결정적으로 같아 그 뒤 전체도 반복된다. Cycle에 있는 서로 다른 states는 최대 m개다. 하지만 처음에는 cycle에 들어가기 전 transient가 있을 수 있어 처음부터 돌아온다고 보장할 수 없다. Parameters와 seed에 따라 더 짧은 cycle을 가질 수 있고 큰 m이나 odd multiplier만으로 maximal period·좋은 통계적 성질·보안을 모두 보장하지 않는다. 별도의 full-period 정리는 여기서 배운 범위가 아니다.

**점검 기준:** 반복 state에서 이후 반복으로 가는 논리, 길이 상한, transient와 최대 period의 차이를 설명한다.

</details>

#### 확인 Q06 · 일반용 품질과 공격자

Lookup용 hash·실험용 PRNG와 cryptographic 요구의 차이를 설명하라. Collision이 필연적이라는 사실이 collision resistance와 모순인가? Output 종류 수가 적다는 사실은 pseudorandomness와 어떻게 구별되는가?

<details><summary>해설 보기</summary>

Lookup에서는 실제 key의 적절한 분산, 실험에서는 필요한 random-looking 품질과 재현성을 본다. Cryptographic 요구는 의도적으로 collision을 찾거나 uniform과 구별하려는 adversary의 제한된 계산 자원을 고려한다. Collision resistance는 collision이 없다는 뜻이 아니라 찾아내는 계산이 어려워야 한다는 뜻이라 유한 출력의 collision 존재와 모순되지 않는다. 마찬가지로 PRNG의 output support 차이는 남아도 효율적 구별의 어려움은 별도의 요구다. Modulo hash는 x,x+m으로 collision을 쉽게 만들고 긴 LCG period도 보안을 보장하지 않는다. 목적에 맞는 기능과 비용을 확인해야 하지만 이 자료는 특정 API의 안전성이나 모든 platform의 속도 우열을 제공하지 않는다.

**점검 기준:** 존재와 찾기의 어려움·정확한 uniform과 효율적 구별·목적과 비용을 분리한다.

</details>

### 적용 연습

#### 연습 P01 · Transient와 seed가 합쳐지는 경우

**새로 만든 강의 기반 일반 연습.** LCG·seed support를 직접 다룬 기출 후보가 없어 기출형으로 표시하지 않는다. 선수내용은 modular recurrence와 finite state다.

xₙ₊₁=2xₙ mod 8에서 seed 1과 seed 3의 states를 반복이 보일 때까지 계산하라. 각 transient·cycle과 seed 1의 x₀부터 LSB를 적고, 'seed가 다르면 이후 sequence도 영원히 다르다' 및 'modulus가 8이면 period가 8이다'를 검토하라.

<details><summary>해설 보기</summary>

Seed 1은 1→2→4→0→0…, seed 3은 3→6→4→0→0…다. 각각 처음 세 states가 transient이며 cycle은 0 하나라 길이 1이다. Seed 1의 LSB는 1,0,0,0,…다. 두 실행은 4에 도달한 시점부터 같은 state와 같은 후속 sequence를 공유하므로 다른 seed가 영구히 다른 tail을 보장하지 않는다. Modulus 8은 가능한 state 수와 period 상한일 뿐 실제 period 8의 보장이 아니다. 일부 bit만 출력해도 이 반복을 없애지 못하며 보안성 역시 이런 크기만으로 주장할 수 없다.

**점검 기준:** 두 traces·세 transient states·cycle 1·LSB를 계산하고 두 잘못된 일반화를 각각 반박한다.

</details>

### 짧은 복습 계획

Q01–Q03으로 생성 목적·출력 종류·호출 상태를 나눈다. Q04의 두 modulus 첫 계산을 비교하고 Q05의 반복 논증을 말로 재현한다. P01에서 transient를 표시한 뒤 Q06의 품질·보안 구분으로 결론을 제한한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 이산수학 강의·자료 연결]]

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 STT]] · 51:13, 53:02, 54:51, 55:47, 56:47, 57:39, 58:40, 01:02:24, 01:03:15, 01:04:14, 53:59, 01:00:30.

2026-09-23 51:13 이후 STT에 근거한 응용이며 추가 PDF·판서·code는 공급되지 않았다. LCG의 modulus 발화에는 14와 13이 충돌한다. 본문의 m=13 계산은 9→8→5→9와 일치하지만 발화를 확정하지 않는다. Timestamp entropy, bit·byte 수치, 자동 seeding과 특정 API, 불명확한 암호 알고리즘 이름은 확정하지 않는다. 이후 applications와 다음 chapter는 미래 예고로 남는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

Seed expansion·output support·LCG/LSB/cycle·계산 자원을 고려한 보안 요구를 직접 평가하는 기출 후보가 없다. 같은 암호 분야라는 이유로 affine cipher·RSA 문항을 PRNG 유형의 근거로 쓰지 않고 강의 기반 일반 연습으로 한정한다.


---

[[courses/discrete_mathematics/units/hashing-and-data-distribution|← 이전: Hash Function과 데이터 분산]] · [[courses/discrete_mathematics/units/index|단원 목차]]
