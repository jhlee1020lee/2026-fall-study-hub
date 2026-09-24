---
title: "Prime Number Theorem과 소수 분포의 추정"
description: "PNT의 상대 근사·균등 선택 확률과 li 및 조건부 error bound를 구별한다."
course: "discrete_mathematics"
unit_id: "prime-distribution"
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

소수의 개수와 밀도를 구분하고, 근사가 비율과 차이 중 무엇을 말하는지 확인한다. PNT의 확률 해석에는 선택 분포를, 더 정밀한 오차식에는 적용 조건을 붙여 읽자.

## Prime-counting function과 상대적인 근사

Prime(소수)은 1보다 큰 양의 정수 중 양의 약수가 1과 자기 자신뿐인 수다. 1은 prime이 아니고, 1보다 크면서 prime이 아닌 양의 정수는 composite(합성수)다. 이 정의는 [이산수학 M008 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)의 선수 배경이다. 여기서는 소수를 판정하는 개별 algorithm보다 큰 범위에 소수가 얼마나 있는지를 다룬다.

Prime-counting function(소수 계수함수) $\pi(x)$를 $x$ 이하의 primes 개수로 정의하자. 예를 들어 $\pi(10)=4$인 것은 2, 3, 5, 7 때문이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 00:00]]에는 “less than”과 “1부터 $x$까지”가 섞여 있지만, 여기서는 M008 PDF p.17의 “not exceeding”에 맞춰 끝점을 포함한다. 녹음은 이 설명 도중 시작하므로 앞서 어떤 primality test를 얼마나 다뤘는지는 추정하지 않는다.

Prime Number Theorem(소수정리, PNT)은

$$\lim_{x\to\infty}\frac{\pi(x)}{x/\ln x}=1$$

이라고 말한다. 여기서 $\ln$은 natural logarithm(자연로그)이다. $x/\ln x$가 큰 $x$에서 소수 개수의 상대적 scale을 잘 근사한다는 뜻이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 02:38]]은 “비율이 1로 간다”와 “차이가 0으로 간다”를 구별했다.

이 구별을 위한 해설용 예로

$$\frac{x+\sqrt x}{x}=1+\frac1{\sqrt x}\longrightarrow1$$

이지만 $(x+\sqrt x)-x=\sqrt x$는 커진다. 상대적으로 가까워진다는 사실과 절대 오차가 작아진다는 사실은 다르다. 반대로 두 function이 모두 발산한다는 것만으로 차이가 커진다고 증명할 수도 없다. $x+1$과 $x$의 차이는 항상 1이다. 따라서 STT 03:30의 두 값이 커진다는 설명만을 절대 오차에 대한 증명으로 사용하지 않는다.

자료는 Gauss·Legendre의 추측과 Riemann zeta function을 사용한 1896년 증명을 배경으로 소개한다. 이 단원에서 사용하는 내용은 그 해석이며, zeta function이나 해석적 정수론의 증명을 전개한 것은 아니다. [[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|Asymptotic bound]]와 마찬가지로 어떤 의미에서 “가깝다”고 하는지부터 읽어야 한다.

## 소수 밀도와 균등한 선택

양의 정수 $x$에 대해 $1,\ldots,x$ 중 하나를 uniform하게 고르면 prime일 확률은 정확히 $\pi(x)/x$다. PNT를 적용한 근사는

$$\frac{\pi(x)}x\approx\frac1{\ln x}$$

이다. 이 확률 해석에는 균등한 선택이라는 가정이 필요하다. 특정 residue만 고르거나 작은 정수에 더 큰 확률을 주면 같은 식을 자동으로 적용할 수 없다.

M008 PDF p.17과 [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 04:28]]의 $x=10^{22}$ 예를 계산하면

$$\ln(10^{22})=22\ln10\approx50.6569,$$
$$\frac1{\ln(10^{22})}\approx0.0197407\approx1.97\%.$$

따라서 약 2%라는 규모를 얻는다. 자료가 제시한 실제 count의 근삿값 $\pi(10^{22})\approx2.01\times10^{20}$은 약 2.01%의 비율에 해당한다. 이 count는 자료의 수치이며 여기서 모든 소수를 직접 세어 얻은 값은 아니다.

$10^{22}$ 자체는 23자리이고 그보다 작은 양의 정수들이 최대 22자리다. 또한 “정확히 22자리인 수만 고른다”는 실험은 “1부터 $10^{22}$까지 고른다”는 실험과 분포가 다르다. 소수의 상대 밀도 $1/\ln x$가 낮아진다고 소수 개수 자체가 줄어드는 것도 아니다. 분모가 커지는 속도와 개수가 늘어나는 속도를 구분해야 한다.

## Logarithmic integral과 조건부 error bound

더 정밀한 추정은 절대 오차까지 다룬다. 다음은 M008 PDF p.18과 [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 05:25–07:15]]의 선택적 심화 배경이다. Logarithmic integral(로그 적분) $\operatorname{li}(x)$은 자료에서 $x/\ln x$보다 좋은 추정으로 소개된다. 자료가 제시하는 $x=10^{22}$에서의 비교는

$$\pi(x)-\frac{x}{\ln x}\approx4.06\times10^{18},$$
$$\operatorname{li}(x)-\pi(x)\approx1.93\times10^9$$

이다. 상대적으로 좋은 첫 근사에도 큰 절대 오차가 남을 수 있다는 점을 보여 준다.

자료에는 $\operatorname{li}(x)=\int_0^x dt/\log t$라는 표기가 있지만, $t=1$에서 분모가 0이 되므로 보통의 연속함수 적분처럼 무조건 계산할 수 없다. 필요한 적분 convention은 공급 자료에 설명되지 않았다. 따라서 이 식으로 수치 적분 절차를 정하지 않고, 어떤 종류의 추정 함수가 사용되는지를 읽는 수준으로 둔다.

같은 페이지가 2016년 결과로 소개하는 식의 형태는

$$|\pi(x)-\operatorname{li}(x)|
\le0.2593\frac{x}{(\ln x)^{3/4}}
\exp\left(-\sqrt{\frac{\ln x}{6.315}}\right)$$

이다. 계수와 제곱근을 포함한 구조는 원본 페이지에서 확인할 수 있지만, 적용 가능한 $x$의 범위와 증명은 제시되지 않았다. 모든 양수에 대입할 수 있는 공식이나 독립 확인한 최신 최선의 bound로 취급하지 않는다.

별도로 Riemann hypothesis(리만 가설)가 참이면

$$\pi(x)=\operatorname{li}(x)+O(\sqrt x\log x)$$

라는 더 강한 error bound가 따른다고 자료는 설명한다. 이 문장은 가설에 조건부이며, STT의 “square root 수준”이라는 요약에서도 $\log x$ 인자를 빼서는 안 된다. $O(\sqrt x\log x)$는 $O(\sqrt x)$와 다른 bound다. 가설을 가정한 결과와 이미 무조건 성립한다고 제시된 추정을 나누어 읽는 것이 이 심화 내용의 핵심이다.

## 핵심 정리

- π(x)는 x 이하의 소수 개수이며 PNT는 π(x)/(x/ln x)→1이라는 상대적 주장이다.
- Uniform하게 1,…,x에서 고를 때의 정확한 prime 확률은 π(x)/x다.
- 소수의 상대 밀도가 낮아져도 π(x)가 감소한다는 뜻은 아니다.
- Riemann hypothesis에 조건부인 O(√x log x)에서 가설과 log 인자를 모두 보존한다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Prime-counting과 ratio

Prime의 정의와 π(10)을 쓰고 PNT를 수식으로 설명하라. 비율이 1로 가면 차이가 0으로 가는가? 두 함수가 모두 발산하면 차이도 반드시 발산하는가?

<details><summary>해설 보기</summary>

Prime은 1보다 큰 양의 정수로 양의 약수가 1과 자신뿐인 수다. 1은 prime이 아니며 π(10)=4로 2,3,5,7을 센다. PNT는 limₓ→∞π(x)/(x/ln x)=1이다. 이는 상대 scale의 근사다. (x+√x)/x=1+1/√x→1이지만 차이는 √x로 커지므로 ratio에서 절대차 0을 결론낼 수 없다. 또 x+1과 x는 모두 발산해도 차이가 1이라 두 함수의 발산만으로 차이 발산을 증명할 수 없다.

**점검 기준:** Prime의 1 제외·끝점 포함, PNT의 자연로그·비율, 서로 다른 두 잘못된 추론의 반례를 쓴다.

</details>

#### 확인 Q02 · 10²² 예의 확률과 자리 수

Uniform하게 1,…,10²²에서 정수 하나를 고를 때 prime 확률의 정확한 식과 PNT 근삿값을 구하라. 자료의 π(10²²)≈2.01×10²⁰와 비교하고, 정확히 22자리 수만 고르는 것과 같은 실험인지 말하라.

<details><summary>해설 보기</summary>

정확한 확률은 π(10²²)/10²²다. PNT로는 1/ln(10²²)=1/(22 ln10)≈1/50.6569≈0.0197407, 약 1.97%다. 자료의 count를 사용한 비율은 약 2.01%이며 직접 모든 소수를 센 값은 아니다. 10²² 자체는 23자리이고 그보다 작은 양수는 최대 22자리다. 정확히 22자리만 고르면 작은 자리 수를 제외하므로 다른 분포다. x가 커질 때 밀도 약 1/ln x가 낮아져도 포함 구간이 늘어 π(x) 자체는 줄지 않는다.

**점검 기준:** 정확한 비율과 근사, 자연로그, % 환산, 자리 수·분포·개수와 밀도의 차이를 확인한다.

</details>

#### 확인 Q03 · li의 오차와 적분 표기

자료의 x=10²²에서 π(x)−x/ln x와 li(x)−π(x)의 비교는 무엇을 보여 주는가? li(x)=∫₀ˣdt/log t를 보통의 적분처럼 그대로 계산하면 안 되는 이유를 설명하라.

<details><summary>해설 보기</summary>

자료의 두 차이는 각각 약 4.06×10¹⁸과 1.93×10⁹이다. 이 예에서 li 추정의 절대 오차가 훨씬 작고, 상대적으로 좋은 x/ln x에도 큰 절대차가 남을 수 있음을 보여 준다. 그러나 integrand는 t=1에서 log t=0이어서 singularity가 있다. 공급 자료에 처리 convention이 없으므로 보통의 연속함수 적분이나 임의의 수치 적분 절차로 해석하지 않는다.

**점검 기준:** 두 차이의 방향·규모와 singularity 위치, 공급되지 않은 적분 convention을 보존한다.

</details>

#### 확인 Q04 · 오차식의 조건과 빠진 인자

자료가 2016년 결과로 소개하는 오차식의 구조를 쓰고, Riemann hypothesis가 참이면 주어진다는 식과 구분하라. 후자를 무조건 O(√x) 오차라고 요약할 수 있는가?

<details><summary>해설 보기</summary>

자료의 첫 식은 |π(x)−li(x)|≤0.2593·x/(ln x)^(3/4)·exp(−√(ln x/6.315)) 형태다. 적용 x 범위와 증명이 공급되지 않았으므로 모든 양수에 쓰는 공식이나 최신 최선의 bound라고 확정하지 않는다.

별도 조건부 문장은 Riemann hypothesis가 참이면 π(x)=li(x)+O(√x log x)라는 것이다. O(√x)라고 쓰면 log 인자를 버리고, 무조건이라고 쓰면 가설을 버린다. 둘 다 원문의 주장보다 강하므로 허용되지 않는다.

**점검 기준:** 계수·제곱근·분모의 구조를 확인하고 RH 조건과 log factor를 유지한다.

</details>

### 적용 연습

#### 연습 P01 · 추출 규칙이 밀도 해석을 바꿀 때

**새로 만든 강의 기반 일반 연습.** 직접 맞는 PNT 기출 후보가 없어 기출형으로 분류하지 않는다. 선수내용은 prime 정의와 uniform 선택 확률이다.

짝수 정수 x≥4에서 실험 A는 1,…,x 중 uniform하게, 실험 B는 2,4,…,x 중 uniform하게 뽑는다. 두 실험의 prime 확률을 쓰고, B에도 1/ln x를 바로 적용해도 되는지 설명하라.

<details><summary>해설 보기</summary>

A는 π(x)/x이고 큰 x에서 PNT로 약 1/ln x다. B의 가능한 값은 x/2개이고 prime은 2 하나뿐이다. 다른 짝수는 2와 더 작은 양의 약수를 가져 composite이므로 B의 확률은 1/(x/2)=2/x다. B는 전체 정수 구간의 uniform 분포가 아니라 짝수 부분의 uniform 분포여서 A의 PNT 밀도를 그대로 옮길 수 없다.

**점검 기준:** 두 sample set의 크기와 유리한 원소 수를 세고 uniform의 대상 집합이 다름을 설명한다.

</details>

### 짧은 복습 계획

Q01에서 ratio와 difference를 분리하고 Q02의 자연로그 계산을 다시 한다. Q03–Q04는 숫자를 외우기보다 각 식이 말하는 오차와 조건을 표시한다. P01로 분포를 바꾸었을 때 왜 기존 확률 근사를 옮길 수 없는지 확인한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 이산수학 강의·자료 연결]]

[03. Number Theory.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf) · 페이지별 보기: [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-012), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-018)

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 STT]] · 02:38, 04:28, 07:15, 05:25, 00:00, 03:30, 06:20.

2026-09-23 STT는 prime-counting 설명 도중 시작한다. 끝점은 자료 p.17의 'x 이하'를 따르되 발화의 less-than 표현을 복원하지 않는다. Prime 정의 p.12는 선수 배경이고 이전 primality-test 진도를 추정하지 않는다. p.18의 li·오차식은 선택적 심화 자료로, 적분 convention과 bound의 전체 적용 범위·증명은 공급되지 않았다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

공급된 전체 기출 후보에 PNT, prime density, li 또는 Riemann hypothesis의 error bound를 직접 다룬 문항은 없다. Prime divisor가 등장하는 relation 분류는 다른 주제이므로 여기서는 강의 기반 일반 연습을 사용한다.


---

[[courses/discrete_mathematics/units/search-and-matrix-complexity|← 이전: Searching·Matrix Multiplication의 Complexity]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/gcd-euclid-and-bezout|다음: GCD·Euclidean Algorithm·Bézout의 구성 →]]
