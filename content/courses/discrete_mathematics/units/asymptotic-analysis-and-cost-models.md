---
title: "Asymptotic Analysis와 Cost Model"
description: "Big-O·Omega·Theta의 증명과 비용 모델·입력 분포의 차이를 복습한다."
course: "discrete_mathematics"
unit_id: "asymptotic-analysis-and-cost-models"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["02. Algorithms.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-14-lecture-04"]
---

무엇을 한 번의 연산으로 세는지 정하고 함수의 성장을 상한·하한으로 비교한다. 평균 비용에는 입력 분포가, 실제 성능에는 메모리와 데이터 이동이 필요함을 확인한다.

## Cost model: 무엇을 세어 Algorithm의 비용으로 삼는가

Algorithm의 performance(성능)는 한 숫자로 끝나지 않는다. Code simplicity는 읽고 유지하기 쉽게 만드는 성질이고, time complexity(시간 복잡도)는 정한 연산의 횟수, space complexity(공간 복잡도)는 실행에 필요한 memory를 다룬다. 코드가 짧다고 반복 횟수까지 적은 것은 아니다. [[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 강의 노트: 성능과 비용 모델]]에서 강조한 출발점도 “어떤 관점의 비용인가”를 구별하는 것이다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 19:03–21:47]]

### Basic operation과 Housekeeping

Time complexity는 보통 seconds를 직접 예측하지 않고 input size에 따른 basic operation의 횟수를 센다. Cost model(비용 모델)은 무엇을 한 번의 연산으로 보고 어떤 작업을 포함할지 정한 약속이다. 실제 latency로 바꾸려면 연산의 실제 비용과 실행 환경을 더 알아야 한다.

Linear search의 `x != ai`는 데이터 비교이고 `i <= n`은 반복 범위를 확인하는 housekeeping이다. 둘 다 comparison이라는 이름을 쓰지만 데이터와 index의 bit length가 다르면 실제 비용도 같지 않을 수 있다. 강의는 main operation 위주로 분석한다고 설명했다. 정수 곱셈에서도 작은 digit의 곱셈과 덧셈을 모두 세는 분석과 핵심 연산 하나를 세는 분석은 다른 약속이다. [M005 p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-038), [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 31:09–34:07]]

따라서 “검색 실패에 $n$회가 든다”는 말에는 data comparison만 센다는 조건을 붙여야 한다. 반복 제어와 마지막 검사를 추가한 수가 달라도 같은 분석을 틀리게 센 것이라고 바로 판단할 수 없다. Fixed-word 연산을 상수 비용으로 세는 것도 하나의 모델이다. 임의로 긴 정수의 비교나 곱셈까지 항상 $O(1)$이라고 주장하는 근거는 되지 않는다.

### Memory와 데이터 이동이 만드는 한계

Space complexity는 실제 memory의 양으로, Turing machine에서는 사용하는 tape 공간으로 이해할 수 있다. 같은 절차에 필요한 memory가 부족하면 더 기다리는 것만으로 실행 가능해지지 않는다. 강의의 긴 context를 처리하는 AI model 예는 이 점을 보여 준다. 특정 model의 정확한 memory 공식까지 제시한 것은 아니다. 또한 독립적인 1,000-qubit 장치 두 개를 보유하는 것과 2,000 qubits가 공동으로 연산하는 장치를 구성하는 것은 서로 다른 자원 조건이다. 이는 자원의 결합 방식에 관한 동기이며 모든 연결 architecture에 대한 불가능 정리는 아니다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 22:38–24:16]]

Accelerator(연산 가속기)의 arithmetic이 빨라도 input·model을 옮기고 결과를 회수하는 data transfer가 bottleneck(병목)이 될 수 있다. GPU의 parallel linear algebra나 FPGA 같은 hardware 선택은 time뿐 아니라 energy와도 관련된다. 강의의 transfer 비중 80–90%는 가능한 상황을 설명하는 말이지 모든 작업의 실측 비율이 아니다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 25:05–29:27]]

이를 명시적인 가정으로 계산해 보자. 전체 시간 100 중 arithmetic이 10, transfer가 90이라고 하자. Arithmetic을 10% 줄이면 $10\to9$이지만 전체는 $100\to99$, 즉 1%만 줄어든다. 이 계산은 불명확한 녹취 숫자의 복원이 아니라 병목을 설명하는 예다. 연산 횟수의 감소율을 전체 latency나 energy의 감소율로 그대로 옮기면 안 되는 이유가 여기 있다.

## Big-O: 충분히 큰 입력에 적용되는 상한

Concrete analysis(구체적 분석)는 정확한 횟수를 세고, asymptotic analysis(점근적 분석)는 input size가 커질 때의 growth를 비교한다. 전자는 상수 차이도 보존하고, 후자는 큰 입력에서 어떤 항이 지배하는지 드러낸다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 04:07–06:27]]

함수 $f,g$에 대해 $f=O(g)$는 고정된 양의 상수 $C$와 threshold $k$가 있어서

$$
|f(x)|\le C|g(x)|\qquad\text{for all }x>k
$$

가 성립한다는 뜻이다. $C,k$를 witnesses라고 부른다. $x$가 바뀔 때마다 $C$를 바꾸는 것은 이 정의를 만족시키지 않는다. 반대로 작은 $x$까지 모두 검사할 필요는 없고, $f(x)\le g(x)$ 자체가 성립할 필요도 없다. [M005 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-030)의 그림에서도 $f$는 $g$보다 높지만, $k$ 뒤에서는 배율을 곱한 $Cg$ 아래에 있다. 그림에서 읽을 것은 두 원래 곡선의 단순한 높이 비교가 아니라 **상수 배율과 시작점**이다.

예를 들어 $3n$과 $100n$은 각각 $C=3$, $C=100$으로 $O(n)$에 속한다. 그래도 두 함수가 같거나 실제 시간이 같은 것은 아니다. $O(g)$를 조건을 만족하는 함수들의 collection으로 보면 $f=O(g)$는 사실상 $f\in O(g)$라는 표기다. $f_1=O(g)$와 $f_2=O(g)$에서 $f_1=f_2$를 끌어낼 수 없다. 강의의 같은 Big-O에 속하는 서로 다른 함수 설명이 이 오해를 짚는다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 09:15–10:47]]

### Polynomial의 모든 항을 하나의 항으로 제어하기

$f(x)=\sum_{i=0}^{d}a_ix^i$, $a_d\ne0$일 때 $x>1$이면

$$
|f(x)|\le\sum_{i=0}^{d}|a_i|x^i
\le\left(\sum_{i=0}^{d}|a_i|\right)x^d.
$$

따라서 $k=1$, $C=\sum|a_i|$를 택하면 $f=O(x^d)$다. 계수에 음수가 있을 수 있으므로 절댓값을 빼면 안 된다. 해설용으로 $2x^2-7x+3$은 $x>1$에서

$$|2x^2-7x+3|\le2x^2+7x+3\le12x^2$$

이므로 $C=12$가 된다. 녹취에서 $C$의 표현 일부가 불명확하지만 이 절댓값 합은 triangle inequality로 직접 확인된다. [M005 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-031), [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 07:26–08:24]]

같은 원리로 복잡한 합이나 곱도 간단히 bound할 수 있다. 양의 정수 $n$에 대해 $1+\cdots+n\le n\cdot n$이므로 $O(n^2)$, $n!\le n^n$이므로 $O(n^n)$다. 고정된 밑 $b>1$의 logarithm은 증가함수이므로

$$\log_b(n!)\le\log_b(n^n)=n\log_b n,$$

즉 $\log(n!)=O(n\log n)$이다. 이들은 유효한 upper bound이며 이 부등식만으로 모두 tight하다고 결론내리지는 않는다.

M005 p.31의 growth graph는 $1,\log n,n,n\log n,n^2,2^n,n!$을 비교한다. 충분히 큰 $n$에서는 이 순서로 성장하지만 작은 값에서 항상 엄격한 순서는 아니다. $2!<2^2$이고 $4^2=2^4$다. 또한 세로 눈금이 $1,2,4,8,\ldots$로 배증하므로 화면의 기울기를 선형 축의 기울기처럼 읽으면 안 된다.

### Sum rule과 Product rule의 공통 threshold

$f_i=O(g_i)$의 witnesses가 $C_i,k_i$라고 하자. 두 bound를 동시에 쓰려면 $x>\max(k_1,k_2)$로 잡는다. 그때

$$
|f_1+f_2|\le|f_1|+|f_2|
\le(C_1+C_2)\max(|g_1|,|g_2|).
$$

따라서 합은 $O(\max(|g_1|,|g_2|))$다. 같은 $g$로 bound되면 $f_1+f_2=O(g)$여서 $O(g)$는 addition에 닫혀 있다. Product는

$$|f_1f_2|\le C_1C_2|g_1g_2|$$

이므로 $O(g_1g_2)$다. 예를 들어 각각 $O(n^2)$, $O(n^3)$인 함수의 합은 $O(n^3)$, 곱은 $O(n^5)$다. 여기서 다루는 것은 upper bound이며 cancellation이 있으면 실제 growth는 더 작을 수도 있다. [M005 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-032), [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 12:23–14:13]]

Nonnegative growth functions에는 $g_1+g_2$를 사용하는 설명도 가능하다. Signed functions에서는 $g_1$과 $g_2$가 상쇄될 수 있으므로 절댓값 없는 합을 보편적인 upper bound로 사용하지 않는다.

## Big-Omega와 Big-Theta: 하한을 더해야 같은 성장률이 된다

$f=\Omega(g)$는 어떤 고정된 $C>0,k$에 대해 모든 $x>k$에서 $|f(x)|\ge C|g(x)|$라는 eventual lower bound다. 부등식을 정리하면 $|g(x)|\le(1/C)|f(x)|$이므로 $g=O(f)$와 동치다. $f=\Theta(g)$는 $f=O(g)$와 $f=\Omega(g)$가 모두 성립하는 경우다. 두 bound의 상수는 달라도 되며 threshold는 둘 중 큰 값을 사용하면 된다. [M005 pp.33–34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)

이때 $f$와 $g$는 same order라고 한다. $\Theta$는 대칭이지만 $O$는 그렇지 않다. $n=O(n^2)$여도 $n^2=O(n)$은 아니다. 후자를 가정하면 충분히 큰 모든 $n$에 대해 $n\le C$여야 해서 불가능하다. 따라서 두 함수는 같은 order가 아니다. 녹취의 lower bound 설명에서 Big-O처럼 들리는 일부 표현은 여기서는 슬라이드의 $\Omega$ 정의에 맞춰 구별한다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 15:12–18:16]]

Upper bound를 구한 뒤에는 그만큼 큰 비용이 정말 필요한지도 따로 보여야 한다. 예를 들어 합의 tight growth를 확인할 때, 모든 항을 가장 큰 항으로 바꾸는 것은 upper bound의 방법이다. Lower bound에서는 뒤쪽의 일정 비율에 해당하는 항들이 모두 충분히 크다는 점을 사용한다. 새 해설 예로 $S(n)=\sum_{i=1}^n i^2$는 $S(n)\le n^3$이고, $i\ge\lceil n/2\rceil$인 적어도 $n/2$개 항만 남겨도 $S(n)\ge(n/2)(n/2)^2=n^3/8$이다. 그러므로 $S(n)=\Theta(n^3)$다. 정확한 합 공식을 외우지 않아도 양쪽 witnesses를 구성할 수 있다. 이런 양방향 bound의 요구를 기출의 합 분석에 연결할 수 있다. [EX:dm_2022_2_mid_q03 p.1]

## Worst-case와 Average-case: 입력의 크기와 분포를 함께 읽기

같은 크기의 입력도 내용이 다르면 다른 시간에 종료될 수 있다. Worst-case는 크기 $n$인 허용 입력 전체에서 비용의 maximum을 본다. Average-case는 입력 분포 $D$를 정하고

$$\mathbb E_D[T(X)]=\sum_x\Pr_D[X=x]T(x)$$

를 계산한다. 가능한 입력을 모두 같은 가중치로 평균내는 것도 uniform distribution이라는 특정 가정이다. Input size만 알면 이 확률들이 자동으로 정해지는 것은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 34:57–38:35]]

간단한 새 예로 어떤 검색의 두 가능한 입력 비용이 1과 5라고 하자. 각각 확률 $1/2$이면 평균은 3이지만, 확률이 $0.9,0.1$이면 $0.9\cdot1+0.1\cdot5=1.4$다. Worst-case는 둘 다 5다. 강의에서 health data를 feature vector로 나타내는 예를 든 이유도 실제 데이터가 가능한 모든 vector에 균등하게 퍼지지 않기 때문이다. 실제 분포를 모르면 평균 분석 자체가 어려워진다.

Worst-case가 큰 algorithm도 특정 분포에서는 훨씬 짧게 실행될 수 있지만, 그 주장을 하려면 어떤 분포인지 밝혀야 한다. “보통 빠르다”는 인상으로 모든 입력에 대한 보장을 대신할 수 없고, 큰 worst-case bound만으로 모든 현실 입력이 느리다고 말할 수도 없다. 정렬 정도가 다른 데이터에 sorting 방법을 선택하거나 검색의 성공·실패 확률을 분석할 때 이 구별이 필요하다.

## 핵심 정리

- $O$는 고정된 상수와 충분히 큰 입력에서의 상한이며 함수값의 equality가 아니다.
- $\Theta$에는 상한과 하한이 모두 필요하다. 합의 뒤쪽 항들을 남기는 방법은 하한을 만드는 데 유용하다.
- 합·곱의 bound를 결합할 때는 원래 부등식들이 동시에 성립하는 threshold를 고른다.
- 코드 길이, basic operation 수, bit cost, memory와 data movement는 서로 다른 성능 정보다.
- Worst-case는 허용 입력 중 최댓값이고 average-case는 명시한 분포로 가중한 평균이다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Witness와 함수 equality

$f=O(g)$의 정의를 $C,k$로 적어라. $3n$과 $100n$이 모두 $O(n)$이면 같은 함수인가? 입력마다 $C=n$을 골라 $n^2=O(n)$을 보였다는 논증은 왜 틀리는가?

<details><summary>해설 보기</summary>

고정된 양의 $C$와 threshold $k$가 존재해 모든 $x>k$에서 $|f(x)|\le C|g(x)|$여야 한다. 작은 입력에서는 성립하지 않아도 되고 $f\le g$ 자체일 필요도 없다.

$3n$과 $100n$은 각각 $C=3,100$, 예를 들어 $k=0$으로 bound되지만 같은 함수는 아니다. $O(n)$은 함수들의 collection으로 읽는다. $C=n$은 고정 상수가 아니며 $n^2\le Cn$은 모든 큰 $n$에 $n\le C$를 요구하므로 불가능하다. 정확한 횟수 차이가 같은 asymptotic class 안에서도 남는다.

**채점·확인:** 양화 순서·절댓값·고정 상수·threshold와 concrete count의 차이를 설명한다.

</details>

#### 확인 Q02 · 부호 있는 polynomial의 상한

$2x^2-7x+3=O(x^2)$의 witnesses를 정하라. 같은 방법으로 일반 degree $d$ polynomial을 bound하고 계수의 부호 있는 합을 쓰면 안 되는 이유를 설명하라.

<details><summary>해설 보기</summary>

$x>1$에서 $|2x^2-7x+3|\le2x^2+7x+3\le12x^2$이므로 $C=12,k=1$이면 된다. 부호 있는 합 $2-7+3=-2$는 양의 상한 상수가 아니다.

일반적으로 $a_d\ne0$인 $f(x)=\sum_{i=0}^{d}a_ix^i$는 $x>1$에서 $|f(x)|\le\sum|a_i|x^i\le(\sum|a_i|)x^d$다. Triangle inequality로 cancellation을 제거한 뒤 각 낮은 차수 항을 최고차 항으로 제어한다.

**채점·확인:** 수치 witnesses와 일반 부등식 두 단계를 제시한다.

</details>

#### 확인 Q03 · 합·factorial·growth graph

정확한 합 공식 없이 $1+\cdots+n$, $n!$, $\log_b(n!)$의 본문 upper bounds를 보이라($b>1$ 고정). $1,\log n,n,n\log n,n^2,2^n,n!$의 growth 순서와 배증하는 세로 눈금을 어떻게 읽는가?

<details><summary>해설 보기</summary>

$1+\cdots+n\le n\cdot n$이므로 $O(n^2)$다. $n!$의 모든 인수가 $n$ 이하이므로 $n!\le n^n$, 즉 $O(n^n)$다. 증가함수 $\log_b$를 적용하면 $\log_b(n!)\le n\log_b n$이므로 $O(n\log n)$이다. 여기서 상한만 보였으므로 tightness는 별도다.

열거한 growth 순서는 충분히 큰 입력에서의 비교다. 작은 값에서는 $2!<2^2$, $4^2=2^4$처럼 달라진다. 세로 눈금 $1,2,4,8,\ldots$는 같은 간격이 같은 증가량이 아니라 배율을 뜻하므로 화면 기울기를 선형 축의 기울기로 해석하면 안 된다.

**채점·확인:** 세 부등식, log 밑 조건, 상한/tightness와 작은 입력·축의 차이를 모두 확인한다.

</details>

#### 확인 Q04 · 합과 곱의 공통 threshold

$f_i=O(g_i)$의 witnesses가 $C_i,k_i$일 때 합·곱의 상한을 증명하라. $g_1+g_2$를 절댓값 없이 쓰는 것과 합이 반드시 tight하다는 주장에는 어떤 함정이 있는가?

<details><summary>해설 보기</summary>

$x>\max(k_1,k_2)$로 두면 두 원래 bound를 함께 쓸 수 있다.
$$|f_1+f_2|\le C_1|g_1|+C_2|g_2|\le(C_1+C_2)\max(|g_1|,|g_2|),$$
$$|f_1f_2|\le C_1C_2|g_1g_2|.$$
같은 $g$로 bound되면 합도 $O(g)$여서 addition에 닫힌다. $O(n^2)$와 $O(n^3)$의 합은 $O(n^3)$, 곱은 $O(n^5)$다.

Signed $g_i$는 합에서 상쇄될 수 있으므로 절댓값 없는 $g_1+g_2$를 보편적 상한으로 쓰지 않는다. 또한 $f_1=n^2,f_2=-n^2$의 합은 0이다. Sum rule은 상한을 주며 반드시 tight한 차수를 주지는 않는다.

**채점·확인:** 공통 threshold, 두 상수 구성, 같은 class의 닫힘과 cancellation을 확인한다.

</details>

#### 확인 Q05 · 하한과 same order

$\Omega,\Theta$를 정의하고 $f=\Omega(g)\iff g=O(f)$를 설명하라. $n=O(n^2)$에서 same order를 결론낼 수 있는가? $\sum_{i=1}^{n}i^2$의 양쪽 bound도 제시하라.

<details><summary>해설 보기</summary>

$\Omega$는 충분히 큰 $x$에서 $|f(x)|\ge C|g(x)|$인 고정 양의 상수가 있다는 뜻이다. 이를 $|g(x)|\le |f(x)|/C$로 바꾸면 $g=O(f)$다. $\Theta$는 $O$와 $\Omega$를 함께 만족한다. 두 상수는 달라도 되고 threshold는 큰 것으로 통일한다. $\Theta$는 대칭이지만 $O$는 아니다.

$n^2=O(n)$은 불가능하므로 $n,n^2$는 same order가 아니다. $S=\sum i^2$는 $S\le n^3$이며, 뒤쪽 적어도 $n/2$개 항은 각각 $(n/2)^2$ 이상이어서 $S\ge n^3/8$이다. 따라서 $\Theta(n^3)$다. Same order도 함수값이나 실제 시간의 equality는 아니다.

**채점·확인:** 정의·역방향 관계·상하한 상수와 후반 항의 개수까지 설명한다.

</details>

#### 확인 Q06 · Performance와 counting convention

코드가 짧아지면 반드시 빨라지는가? Linear search 실패에 대해 $n$과 $2n+2$ comparisons가 나올 수 있는 이유, data comparison과 housekeeping의 차이, fixed-word와 임의 길이 정수 비용의 차이를 설명하라.

<details><summary>해설 보기</summary>

Code simplicity는 기술의 단순성이고 time complexity는 정한 연산의 실행 횟수다. 짧은 loop도 많이 반복될 수 있다. $n$은 데이터 비교만 세는 기준이고, $2n+2$는 $n$회 데이터 비교에 $n+1$회 범위 검사와 마지막 검사 1회를 더한 기준일 수 있다.

데이터 값 비교와 index 범위 검사는 목적도 bit length도 다르다. 무엇을 생략했는지 명시해야 수를 비교할 수 있다. Fixed-word 연산을 상수 비용으로 보는 모델은 가능하지만 임의 길이 정수 비교·곱셈까지 항상 $O(1)$이라고 보장하지 않는다. 초 단위 시간에는 실제 연산 비용과 환경이 필요하다.

**채점·확인:** simplicity/time 구별, 두 횟수의 구성, bit length·실행환경 한계를 적는다.

</details>

#### 확인 Q07 · 시간만 늘려 해결되는가

Space complexity의 의미를 memory·Turing machine 관점에서 설명하라. 메모리가 부족한 긴 context 계산에 시간만 더 주면 되는가? 독립적인 1,000-qubit 장치 두 개 예는 무엇을 말하며 무엇까지 말하지 않는가?

<details><summary>해설 보기</summary>

Space complexity는 실행에 필요한 memory 양이며 Turing machine에서는 사용하는 tape 공간으로 본다. 동일 절차의 memory 요구가 용량을 넘으면 더 기다려도 필요한 공간이 줄어든다는 보장은 없다. 실행 방식이나 자원 조건을 바꾸어야 할 수 있다.

독립 장치 두 개와 2,000 qubits가 함께 연산하는 장치는 자원의 결합 방식이 다르다는 동기다. 모든 연결 architecture가 불가능하다는 정리는 아니다. AI 예도 특정 model의 정확한 memory 공식을 제공하지 않는다.

**채점·확인:** 공간 정의, 실행 가능성, 두 동기 예의 제한을 모두 설명한다.

</details>

#### 확인 Q08 · 부분 개선의 전체 효과

총 시간 100 중 arithmetic 10, transfer 90이라고 가정한다. Arithmetic을 10% 줄이면 전체 감소율은 얼마인가? GPU·FPGA와 energy 논의에 이를 어떻게 연결하며 어떤 일반화는 피해야 하는가?

<details><summary>해설 보기</summary>

Arithmetic은 10에서 9로 줄어 전체는 99다. 감소율은 (100−99)/100=1%다. 연산 단계가 빨라도 입력·model 이동과 결과 회수가 병목이면 전체 효과가 작다.

Accelerator의 parallel 연산, data movement와 energy를 함께 고려해야 한다. 시간 감소율이 그대로 energy 감소율이라는 근거는 없다. 10+90은 명시한 계산 가정이고 녹취의 80–90%를 모든 장치의 실측 비율로 일반화할 수 없다.

**채점·확인:** 산술 9, 전체 99, 1%와 비용별 구별을 확인한다.

</details>

#### 확인 Q09 · 분포가 바꾸는 평균

같은 크기의 두 입력에서 비용이 1과 5다. 확률이 각각 $(1/2,1/2)$ 또는 $(0.9,0.1)$일 때 평균과 worst-case를 비교하라. 실제 feature vector에 uniform model을 자동 적용할 수 있는가?

<details><summary>해설 보기</summary>

평균은 첫 분포에서 $1/2+5/2=3$, 둘째에서 $0.9+0.5=1.4$다. Worst-case는 모두 5다. 일반적으로 평균은 $\sum_x\Pr_D[X=x]T(x)$여서 크기만 아니라 분포 $D$가 필요하다.

현실의 feature vector는 일부 영역에 더 몰릴 수 있고 분포 자체를 모를 수도 있다. 큰 worst-case가 모든 현실 입력의 큰 비용을 뜻하지 않고, 특정 자료에서 빠르다는 관측이 모든 입력의 상한을 대신하지도 않는다.

**채점·확인:** 두 평균·최댓값과 uniform 가정의 근거 필요성을 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 상한뿐인 분석을 고치기

**새로 만든 기출 연결 합성 연습.** [EX:dm_2022_2_mid_q03 p.1]의 양방향 bound 요구를 전체 합과 평균 비용의 구별에 옮겼다. Q02·Q03·Q05의 부등식만 사용하며 원문의 합이나 정답을 재현하지 않는다.

$A(n)=\frac1n\sum_{i=1}^n i^2$를 분석한 보고서가 “각 항이 $n^2$ 이하이므로 $A(n)=\Theta(n^2)$”라고 결론냈다. 결론과 논증을 따로 평가하고 빠진 부분을 보완하라. 총비용 $T(n)=nA(n)$도 구분하라.

<details><summary>해설 보기</summary>

결론은 맞지만 제시 논증은 $A(n)\le n^2$, 즉 상한만 준다. 뒤쪽 적어도 $n/2$개 항이 $(n/2)^2$ 이상이므로
$$A(n)\ge\frac1n\frac n2\left(\frac n2\right)^2=\frac{n^2}{8}.$$
따라서 $n\ge1$에서 $n^2/8\le A(n)\le n^2$라는 양쪽 상수로 $\Theta(n^2)$를 결론낸다. 총비용은 $T=nA$여서 $n^3/8\le T\le n^3$, 즉 $\Theta(n^3)$다. 평균과 총합의 정규화 factor $1/n$을 놓치면 차수가 달라진다.

**채점·확인:** 참인 결론과 불완전한 증명을 구별하고 하한의 항 수·크기·정규화를 모두 제시한다.

</details>

#### 연습 P02 · 최적화 보고서의 가정

**새로 만든 강의 기반 일반 연습.** Memory·transfer·입력 분포를 함께 평가하는 직접 기출 근거는 없다.

두 workload의 전체 시간은 각각 100,200이다. 첫 것은 arithmetic 10·transfer 90, 둘째는 arithmetic 100·transfer 100이며 확률은 0.8,0.2다. Arithmetic만 절반으로 줄이면 평균 시간과 worst-case는 어떻게 바뀌는가? 필요한 memory가 12GB인데 8GB만 있으면 이 시간표로 실행 가능성까지 보장할 수 있는가?

<details><summary>해설 보기</summary>

개선 후 시간은 $5+90=95$, $50+100=150$이다. 평균은 전 $0.8(100)+0.2(200)=120$, 후 $0.8(95)+0.2(150)=106$이므로 14, 약 11.67% 감소한다. 이 두 허용 workload의 worst-case는 200에서 150으로 줄어 25% 감소한다. Arithmetic 50% 개선이 전체 50% 개선은 아니다.

같은 절차가 12GB를 요구하면 8GB에서 이 표의 실행이 가능하다고 보장할 수 없다. 분포가 바뀌면 평균도 다시 계산해야 하고, 초 단위 가정은 단순 operation count와 구별해야 한다.

**채점·확인:** 95·150·120·106·worst-case 25%, 분포와 공간 조건을 확인한다.

</details>

### 복습 순서

Q01–Q05의 부등식을 해설 없이 쓰고 P01에서 상한뿐인 논증을 고친다. Q06–Q09와 P02에서는 먼저 비용 단위·분포를 적는다. 다음 날 수치 답보다 각 결론의 가정을 다시 설명한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 강의 노트 · 2026-09-14 · 이산수학 4강]]
- [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 보정 녹취]] — 04:07–18:16 점근 표기; 19:03–34:07 비용·메모리·전송; 34:57–38:35 입력 분포. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [02. Algorithms.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)
  - 점근 표기와 growth: [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-034)
  - 시간·공간·연산 수: [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-038)

### 읽을 때의 범위

- 9월 14일의 개념·비용 모델 설명을 따른다. 불명확한 polynomial 상수와 lower-bound 발화는 자료의 절댓값·Omega 정의에 맞춘 해설과 구별한다.
- 정수 연산을 상수로 세는 모델과 전체 bit complexity는 다르다. 비교 횟수에는 무엇을 포함했는지 반드시 적는다.
- Memory·quantum 장치·accelerator·feature vector는 동기 설명이다. 특정 제품 공식, 모든 architecture의 불가능성, 모든 작업의 transfer 비율이나 energy 감소를 확정하지 않는다.
- 합성 연습의 부등식은 본문의 해설 방법을 재사용한다. 기출 연결은 상하한 추론에 한정하며 matrix-chain·BFS·DP·분산 계산의 추가 선수내용을 포함하지 않는다.
- 보정 녹취의 불확실성을 새 청취로 해소한 것이 아니다. 과거 기출의 규칙이나 등장 여부는 현재 시험 정책·출제 보장이 아니다.
