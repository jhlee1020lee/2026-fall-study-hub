---
title: "Pseudorandom Generation과 Cryptographic 요구"
description: "Seed support·LCG·암호학적 요구와 공유 prime의 GCD 위험을 복습한다."
course: "discrete_mathematics"
unit_id: "pseudorandomness-and-security"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["04. Number Theory Applications.pdf", "03. Number Theory.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05", "courses/discrete_mathematics/lectures/2026-09-28-lecture-06"]
---

짧은 seed에서 긴 출력을 만드는 과정의 재현성과 한계를 확인한다. LCG의 주기와 공격 저항성을 구별하고 편향된 prime 선택이 남기는 공통인수를 계산한다.

## Pseudorandom generation: 짧은 Seed에서 긴 출력을 만들기

Computer simulation이나 통계·machine learning 실험에서는 실제 데이터를 충분히 수집하기 어렵거나 생성 데이터로 실험해도 되는 경우가 있다. 이때 random-looking data가 필요하다. 그러나 deterministic computer에 “아무렇게나 긴 문자열을 만들어라”라고만 말하면 어떤 분포에서 무엇을 뽑을지 정해지지 않는다. 계산 절차와 초기 정보가 필요하다. [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: PRG·PRNG]], [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 51:13–53:02]]

Seed(초기 입력)는 생성기의 출발 정보를 제공한다. 직접 입력받거나 physical observation에서 얻을 수 있다. 강의의 timestamp 소수 자리 예는 분 단위보다 자주 변하는 값을 얻으려는 동기다. 하지만 clock의 precision과 관측 정보량은 유한하다. 자주 변하거나 겉으로 고르게 보인다는 것만으로 uniform distribution이나 공격자가 예측하기 어려운 entropy를 입증하지는 못한다.

### Deterministic expansion이 uniform distribution과 다른 이유

PRG·PRNG의 seed expansion을

$$G:\{0,1\}^s\to\{0,1\}^{L},\qquad L>s$$

인 deterministic function으로 정리해 보자. 가능한 seeds는 $2^s$개이므로 outputs도 많아야 $2^s$개다. 전체 $L$-bit strings는 $2^L$개이므로, 모든 문자열에 같은 확률을 주는 uniform distribution과 같을 수 없다. 새 계산 예로 8-bit seed에서 100-bit output을 만들더라도 가능한 output은 많아야 256개이며, $2^{100}$개 전체를 고르게 생성하지 못한다. 강의의 불명확한 bit·byte 숫자를 복원하지 않아도 이 개수 논증은 성립한다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 53:59–54:51]]

그러면 목표는 “출력이 길어졌다”에서 끝나지 않는다. Seed를 여러 번 concatenation하면 길이는 늘지만 반복 패턴이 쉽게 드러난다. 필요한 사용 환경과 관찰 능력에서 random output과 쉽게 구별되지 않는 성질을 요구하는 것이다. 정보이론적으로 가능한 출력의 종류가 제한된다는 사실과 계산 자원이 제한된 관찰자가 쉽게 구별할 수 있느냐는 질문은 다르다.

같은 초기 seed와 state(내부 상태)로 시작하면 deterministic generator는 같은 sequence를 재현한다. 그러나 연속 호출마다 state가 갱신될 수 있으므로 “두 번 호출하면 같은 값”이라는 결론은 아니다. Re-seeding, 새 실행, 같은 실행의 다음 호출을 구분해야 한다. 녹취의 자동 seed 설명은 특정 API의 정확한 동작을 확정할 정도로 명확하지 않다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 55:47]]

## Linear Congruential Method: 유한한 State가 만드는 주기

Linear Congruential Method(선형 합동 방법)는 multiplier $a$, increment $c$, modulus $m$, initial state $x_0$를 정하고

$$x_{n+1}=(ax_n+c)\bmod m$$

으로 갱신한다. [NM002 p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-003)의 recurrence다. State를 그대로 output으로 쓰거나 least significant bit(최하위 비트, LSB), 즉 state의 홀짝을 추출할 수 있다.

강의 예에서 $a=3,c=7,x_0=9$는 읽히지만 modulus는 14와 13이 섞여 있다. 첫 계산부터 $34\bmod14=6$과 $34\bmod13=8$은 다르다. 다음 표는 **$m=13$을 선택한 일관된 해설 계산**이며, 강의자가 처음부터 끝까지 13이라고 말했다는 뜻은 아니다. 새로 공급된 NM002의 일반식도 그 발화 충돌 자체를 해결해 주지는 않는다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 56:47–58:40]]

| 단계 | State | 다음 state 계산 | 현재 LSB |
|---|---:|---|---:|
| 0 | 9 | $34\bmod13=8$ | 1 |
| 1 | 8 | $31\bmod13=5$ | 0 |
| 2 | 5 | $22\bmod13=9$ | 1 |
| 3 | 9 | 처음 state로 복귀 | 1 |

따라서 state는 $9\to8\to5\to9\to\cdots$이고 LSB는 $1,0,1,1,0,1,\ldots$다. 같은 state가 다시 나타나면 같은 transition을 따르므로 이후도 반복된다. Modulo $m$에서 state가 $m$개뿐이므로 eventual cycle의 길이는 $m$을 넘지 않는다. 그렇다고 모든 seed에서 처음부터 주기 $m$이 되는 것은 아니다. 반복 구간 전에 transient가 있을 수 있고, 이 예처럼 period가 3일 수도 있다. Multiplier가 홀수라는 조건 하나만으로 최대 period를 보장하지 않는다.

## Cryptographic 요구: 긴 주기와 공격 저항성을 구별하기

일반적인 hash table은 실제 데이터의 분산과 lookup 성능을, simulation용 PRNG는 필요한 통계적 품질과 재현성을 중시한다. Cryptographic(암호학적) 사용에서는 의도적으로 약점을 찾는 adversary(공격자)를 고려한다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 01:00:30–01:04:14]]

| 대상 | 일반 사용에서 살피는 성질 | 공격자를 고려할 때 추가로 필요한 구별 |
|---|---|---|
| Hash | 실제 입력이 적절히 분산되는가 | Collision이 존재하는 것과 효율적으로 찾아내는 것은 다름 |
| PRNG | 필요한 분포·주기·재현성을 제공하는가 | 출력 패턴을 구별하거나 다음 값을 예측하기 쉬운지 별도 문제 |

Collision resistance(충돌 저항성)는 collision이 수학적으로 없다는 뜻이 아니다. 제한된 계산 자원으로 collision을 찾아내기 어렵다는 요구다. Pseudorandomness 역시 짧은 seed의 output support를 전체 공간으로 바꾸는 성질이 아니라 효율적인 구별에 대한 요구다. 강의의 “찾을 수 없다”는 표현은 이런 자원 제한의 의미로 읽어야 한다.

LCG의 period가 길어도 이 요구들이 자동으로 성립하지 않는다. 강의는 구조적 패턴의 구별과 parameters 복구 가능성을 지적한다. 목적에 맞는 cryptographic library·OS 기능을 선택해야 한다는 설명도 있었지만 특정 API, 불명확한 알고리즘 이름, platform별 비용 순위까지 확정할 근거는 주어지지 않았다. 복잡한 계산을 사용한다는 소개를 모든 구현에서 언제나 더 느리다는 실측 결론으로 일반화하지 않는다.

## Prime 선택의 편향이 Public modulus에 남기는 흔적

Randomness의 품질이 실제 수학적 구조와 연결되는 예가 RSA의 prime 선택이다. 전체 RSA 절차에 앞서 여기서는 서로 다른 primes의 곱 $N=pq$를 공개한다는 설정만 사용한다. Prime Number Theorem의 $\pi(x)\approx x/\ln x$는 큰 범위에 prime 후보가 많다는 설명을 돕는다. 그러나 가능한 후보가 많다는 것과 구현이 그 후보를 고르게, 예측하기 어렵게 선택한다는 것은 다르다. [M008 p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-017)

[[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: PRNG와 공통 prime]]에서는 서로 다른 public moduli라도 같은 prime을 공유할 수 있다는 점을 설명했다. $N_1=pq$, $N_2=pr$이고 서로 다른 prime cofactors $q,r$를 쓰면

$$\gcd(N_1,N_2)=p.$$

전체 modulus가 같을 필요가 없다. 공통인수를 GCD로 찾은 뒤 나눗셈하면 남은 인수들도 구한다. 해설용 $N_1=55=5\cdot11$, $N_2=65=5\cdot13$에서는 GCD가 5이고, 나머지 인수가 각각 11과 13이다. $N_1=N_2$여서 GCD가 modulus 전체가 되는 상황과는 다르다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 15:06–17:51]]

강의의 규모 계산처럼 천만 개 중 0.1%라고 **가정**하면 만 개다. 이는 작은 비율도 큰 집단에서 큰 수가 된다는 산술 예이며, 특정 사건의 실제 비율을 확인한 통계는 아니다. 또한 후보 prime이 많다는 설명을 충돌확률이 정확히 0이라는 주장으로 바꾸면 안 된다. 녹취의 prime 후보군 지수와 bit 수 일부는 손상되어 있으므로 임의의 수치로 채우지 않는다. 핵심은 큰 후보 공간을 확보하는 것과 좋은 sampling을 구현하는 것 모두가 필요하다는 점이다.

## 핵심 정리

- 길이를 늘리는 deterministic 계산은 가능한 seed보다 많은 output 종류를 만들지 못한다.
- 동일 초기 seed·state는 동일 sequence를 주지만 연속 호출의 값이 항상 같은 것은 아니다.
- 유한 state는 eventual cycle을 만들며 긴 period 하나로 cryptographic 품질을 증명하지 못한다.
- Collision의 존재와 효율적인 발견, support의 차이와 효율적인 구별은 각각 다른 질문이다.
- 큰 prime 후보군과 편향 없는 예측하기 어려운 sampling은 별개의 조건이다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 짧은 physical seed

Simulation·통계·machine learning 실험에서 random-looking data를 쓰는 이유는 무엇인가? Timestamp의 낮은 자릿수가 자주 변하면 uniform하고 안전한 seed라는 결론을 낼 수 있는가?

<details><summary>해설 보기</summary>

실제 데이터를 충분히 모으기 어렵거나 생성 데이터로 실험할 수 있을 때 random-looking 입력이 도움이 된다. Deterministic computer에는 분포와 생성 절차를 명시해야 한다.

Timestamp는 짧은 초기 정보를 얻는 동기지만 clock precision과 관측 정보는 유한하다. 자주 변하는 값이라도 가능한 값 수, 편향, 공격자의 예측 가능성은 별도다. 겉으로 다양해 보인다는 사실만으로 uniformity나 secure entropy가 검증되지는 않는다.

**채점·확인:** 용도·명세 필요성·유한 정보와 예측 가능성을 설명한다.

</details>

#### 확인 Q02 · Support와 state

8-bit seed를 100-bit로 늘리는 deterministic generator의 가능한 output 수는 최대 얼마인가? Seed 반복 연결이 좋은 방법이 아닌 이유와 재시작·re-seeding·연속 호출의 차이를 설명하라.

<details><summary>해설 보기</summary>

Seeds가 $2^8=256$개이므로 서로 다른 outputs도 최대 256개다. 100-bit uniform은 $2^{100}$개 전체에 확률을 주므로 같은 분포가 아니다. Seed를 반복 연결하면 길이만 늘고 눈에 띄는 반복 패턴이 생긴다. 이 support 한계와 제한된 계산 자원의 관찰자가 쉽게 구별할 수 있는지는 다른 질문이다.

같은 초기 seed·state로 재시작하면 같은 sequence가 나온다. 연속 호출은 state를 갱신하므로 보통 sequence의 다음 항을 읽는 상황이다. Re-seeding은 초기 정보를 다시 설정하는 일이며 특정 API가 언제 이를 하는지는 따로 확인해야 한다.

**채점·확인:** 256 대 전체 공간, 반복 패턴, 재현성의 정확한 조건을 확인한다.

</details>

#### 확인 Q03 · LCG의 두 modulus와 cycle

$x_{n+1}=(3x_n+7)\bmod m$, $x_0=9$에서 $m=14,13$의 첫 값을 비교하라. $m=13$을 선택한 계산의 state·LSB 여섯 항과 period를 구하고 최대 cycle·transient·홀수 multiplier의 한계를 설명하라.

<details><summary>해설 보기</summary>

첫 계산은 34다. Modulo 14에서는 6, modulo 13에서는 8이므로 기록된 8은 후자와 맞는다. 그러나 이것이 녹취에 14가 없었다는 증거는 아니다.

$m=13$에서는 $9\to8\to5\to9$로 반복하고 처음 여섯 state는 9,8,5,9,8,5다. 해당 LSB는 1,0,1,1,0,1이며 state period는 3이다. 같은 state부터 같은 transition이 이어진다. State가 $m$개뿐이므로 eventual cycle 길이는 $m$ 이하지만 처음부터 cycle일 필요는 없어 transient가 있을 수 있다. 홀수 multiplier라는 조건 하나로 최대 period나 보안을 보장하지 않는다.

**채점·확인:** 6/8의 분기, 세 단계 산술, LSB와 cycle 상한·한계를 확인한다.

</details>

#### 확인 Q04 · 일반용과 암호용 요구

일반 hash·simulation PRNG의 요구를 cryptographic 사용과 비교하라. Collision이 존재하는데 collision resistance를 요구하는 것은 모순인가? 긴 period만으로 충분하며 비용 순위는 항상 같은가?

<details><summary>해설 보기</summary>

일반 hash는 실제 데이터의 분산·lookup을, simulation PRNG는 필요한 통계 품질과 재현성을 본다. Cryptographic 사용은 일부러 collision을 찾거나 출력을 구별·예측하려는 공격자를 고려한다.

Collision이 존재한다는 수학적 사실과 제한된 자원으로 찾기 어렵다는 요구는 양립한다. 마찬가지로 작은 support가 계산적으로 쉽게 구별된다는 자동 결론은 아니다. LCG의 긴 period만으로 구조적 패턴이나 parameters 복구 위험이 사라지지 않는다. 용도에 맞는 cryptographic 기능을 선택해야 하지만 특정 API·알고리즘 이름이나 모든 platform의 속도·energy 순위는 이 강의에서 확정하지 않았다.

**채점·확인:** 존재/계산 구별, adversary, LCG와 목적·비용의 조건을 포함한다.

</details>

#### 확인 Q05 · 공개 modulus의 공통인수

서로 다른 primes $p,q,r$에 대해 $N_1=pq,N_2=pr$의 GCD가 무엇인지 설명하고 55와 65로 검산하라. $N_1=N_2$인 경우와 prime 후보가 많다는 사실의 한계도 구별하라.

<details><summary>해설 보기</summary>

두 수가 공유하는 prime은 $p$뿐이므로 $\gcd(N_1,N_2)=p$다. $65=55+10$, $55=5\cdot10+5$, $10=2\cdot5$여서 GCD는 5다. 나머지 인수는 $55/5=11$, $65/5=13$이다. 전체 modulus가 달라도 공통 prime이 드러난다.

두 modulus가 같으면 GCD가 modulus 전체이므로 이 계산만으로 한 prime을 분리한 것은 아니다. Prime Number Theorem의 $\pi(x)\approx x/\ln x$는 큰 후보군을 설명하지만 실제 sampling이 일부 prime에 치우치지 않는다는 뜻은 아니다. 작은 충돌확률도 정확히 0이라는 뜻은 아니다.

**채점·확인:** 공유 prime 조건, Euclidean 검산과 cofactor, 동일 modulus 및 후보군/분포 차이를 확인한다.

</details>

#### 확인 Q06 · 비율과 검증된 사건의 차이

천만 개 중 0.1%가 취약하다고 가정하면 몇 개인가? 이 산술로 강의에서 언급한 사건의 실제 지역·시기·피해 규모까지 확인되는가?

<details><summary>해설 보기</summary>

0.1%=0.001이므로 10,000,000×0.001=10,000개다. 작은 비율도 큰 모집단에서 상당한 수가 된다는 계산이다.

이는 주어진 가정의 산술이지 사건의 실측 비율이나 지역·시기의 검증이 아니다. 녹취의 손상된 prime 후보군 지수·bit 수를 이 계산으로 복원할 수도 없다. 핵심은 sampling의 편향이 후보군 규모와 별개로 위험할 수 있다는 점이다.

**채점·확인:** 만 개라는 값과 가정 계산/실증 주장 구별을 명시한다.

</details>

### 적용 연습

#### 연습 P01 · 반복 호출과 초기화 구별

**새로 만든 강의 기반 일반 연습.** Seed·LCG·LSB의 직접 대응 기출은 없다.

Q03의 명시적 $m=13$ 모델에서 호출은 먼저 state를 갱신한 뒤 그 LSB를 내보낸다고 정한다. (A) 한 번 9로 초기화하고 세 번 호출, (B) 매번 9로 다시 초기화하고 한 번씩 호출할 때 출력을 비교하라. 둘 중 어느 쪽도 이 결과만으로 cryptographic 품질을 입증하지 못하는 이유는?

<details><summary>해설 보기</summary>

A는 갱신 state가 8,5,9이므로 출력은 0,1,1이다. B는 매번 첫 갱신 $9\to8$만 수행하여 0,0,0이다. Q03이 initial state의 LSB부터 적은 것과 달리 여기서는 갱신 후 출력이라는 계약을 먼저 정했다.

같은 seed는 같은 전체 sequence를 재현한다는 뜻이지 state가 전진해도 모든 호출값이 같다는 뜻이 아니다. A의 변화나 B의 반복만으로 통계 품질·효율적인 구별 저항성을 증명할 수 없다. 이미 이 모델은 짧은 cycle이라는 한계도 갖는다.

**채점·확인:** 갱신 후 계약, 두 출력열, state progression과 보안 해석을 확인한다.

</details>

#### 연습 P02 · 많은 후보라는 설명의 빈틈

**새로 만든 강의 기반 일반 연습.** 편향된 prime sampling과 공유 인수의 직접 기출은 없다.

한 설명이 “후보 prime이 많고 공개 modulus 55와 65가 다르므로 prime 선택은 안전하다”고 주장한다. 계산으로 반박한 뒤, 서로 다른 두 modulus의 GCD가 1이었던 다른 관측만으로 generator의 안전성을 증명할 수 있는지도 답하라.

<details><summary>해설 보기</summary>

gcd(55,65)=5이므로 두 modulus는 서로 달라도 인수를 공유한다. 55=5×11, 65=5×13을 얻는다. 따라서 큰 후보군과 다른 최종 값은 편향 없는 sampling을 보장하지 않는다.

GCD가 1인 한 쌍은 그 두 수에 공통인수가 없다는 사실만 보인다. 다른 출력에서의 편향, 예측 가능성, 구조적 구별 가능성까지 배제하지 않는다. Cryptographic 요구는 목적과 공격 모델을 포함하며 한두 표본으로 보증할 수 없다.

**채점·확인:** 수학적 반박과 GCD 검사의 확인 범위·미확인 범위를 구별한다.

</details>

### 복습 순서

Q01–Q02에서 seed와 분포를 설명하고 Q03의 state·LSB를 따로 적는다. Q04–Q06과 P02에서는 수학적 계산과 보안 주장에 필요한 가정을 나눈다. 다음 날 P01의 재시작·연속 호출 차이를 다시 계산한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트 · 2026-09-23 · 이산수학 5강]]
- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 녹취]] — 51:13–55:47 seed·support; 56:47–59:38 LCG; 01:00:30–01:04:14 cryptographic 요구. 시간 표시는 녹취 본문에서 찾는다.
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 15:06–17:51 prime sampling과 공유 인수. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - LCG의 일반식: [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-003)
- [03. Number Theory.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)
  - Prime 후보군·GCD 선수 복습: [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-017), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-019)

### 읽을 때의 범위

- 9월 23일 PRNG 설명과 9월 28일 공유 prime 예를 연결한다. 응용 slide의 일반 LCG 식은 이후 확보된 보충이며 녹취의 modulus 13/14 충돌을 해결하지 않는다.
- LCG 수치 계산은 m=13을 명시적으로 선택한 예다. 처음부터 내내 13이라고 발화했다는 주장이 아니며 큰 modulus의 손상된 지수도 추정하지 않는다.
- Bit·byte 숫자와 자동 seed·두 번 호출 발화는 불명확하다. 특정 API를 검증하거나 보편적 호출 동작으로 확정하지 않는다.
- Collision resistance와 pseudorandomness는 계산 자원을 제한한 요구다. 긴 period만으로 보안·uniformity를 증명하지 않으며 현재 알고리즘 보안 상태나 platform별 비용을 보증하지 않는다.
- Prime 후보군의 손상된 수식·사건의 지역·시기·실제 비율은 복원하지 않는다. 0.1%×천만은 가정의 산술이며 최신 실증 통계가 아니다.
- 보정 녹취의 불확실성과 음성 누락 가능성은 남는다. 다음 장 induction·recursion은 이 복습에 포함하지 않는다.
