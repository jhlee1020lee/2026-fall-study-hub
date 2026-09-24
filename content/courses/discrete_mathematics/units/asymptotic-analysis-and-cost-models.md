---
title: "Asymptotic Analysis와 Cost Model"
description: "Big-O·Ω·Θ의 증명과 시간·공간·데이터 이동·평균 분석의 조건을 점검한다."
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
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-09-lecture-03", "courses/discrete_mathematics/lectures/2026-09-14-lecture-04"]
---

무엇을 한 번의 연산으로 셀지 정하고, 증가율 주장을 고정된 상수와 부등식으로 확인한다. 같은 차수, 같은 실제 시간, 같은 입력 분포를 서로 구별하자.

## Operation count와 asymptotic growth

같은 문제를 푸는 [[courses/discrete_mathematics/units/algorithms-search-and-sort|algorithm]]들을 비교하려면 입력 크기에 따라 얼마나 많은 일을 하는지 알아야 한다. Concrete analysis(구체적 분석)는 정한 operation(연산)을 정확히 몇 번 수행하는지 세고, asymptotic analysis(점근 분석)는 입력이 커질 때 그 수의 growth(증가율)를 비교한다. 예를 들어 $3n+5$와 $6n+10$은 모든 $n$에서 두 배 차이가 나지만 같은 linear growth를 갖는다. 증가율이 같다는 것은 실행시간이 같다는 뜻이 아니다.

Big-O는 eventual upper bound(충분히 큰 입력에서의 상한)를 표현한다. [이산수학 M005 PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)의 정의는

$$f(x)=O(g(x))\quad\Longleftrightarrow\quad
\exists C>0,\exists k>0,\ \forall x>k:\ |f(x)|\le C|g(x)|$$

이다. $C,k$를 witnesses(증명 상수)라고 부른다. $C$를 먼저 고정한 뒤 모든 충분히 큰 $x$에 적용해야 한다. $x$가 커질 때마다 $C$도 바꾸면 이 정의를 만족시킨 것이 아니다. 작은 $x$에서 부등식이 실패해도 괜찮고, $f(x)\le g(x)$ 자체가 성립할 필요도 없다.

자료 그림에서는 $f$가 $g$보다 위에 있어도 threshold $k$ 이후에는 배율을 곱한 $Cg$ 아래에 놓인다. 핵심은 곡선 사이의 정확한 간격이 아니라 한 고정된 배율이 이후 구간을 모두 덮는다는 점이다.

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 09:15]]는 $O(g)$를 function들의 collection으로 읽으라고 설명했다. $f=O(g)$는 실질적으로 $f\in O(g)$라는 관계다. $f_1=O(g)$이고 $f_2=O(g)$라고 해서 $f_1=f_2$가 되는 일반적인 등식이 아니다. 또한 $n=O(n^2)$도 맞으므로 Big-O만으로 가장 정확한 증가율을 얻었다고 할 수 없다.

## Witness를 만드는 부등식

Polynomial(다항식) $f(x)=\sum_{i=0}^{d}a_ix^i$, $a_d\ne0$를 보자. $x>1$이면 모든 $i\le d$에서 $x^i\le x^d$이므로

$$|f(x)|\le\sum_{i=0}^{d}|a_i|x^i
\le\left(\sum_{i=0}^{d}|a_i|\right)x^d.$$

따라서 $k=1$, $C=\sum_i|a_i|$가 $O(x^d)$의 witnesses다. 계수에 음수가 있을 수 있으므로 절댓값 없이 더하면 안 된다. 설명용 $f(x)=2x^2-3x+4$에서는 $x>1$일 때 $|f(x)|\le9x^2$로 잡을 수 있다. 가장 작은 $C$를 찾아야 하는 것은 아니다.

M005 PDF p.31의 다른 예도 각 항을 더 큰 값으로 덮으면 된다.

$$1+2+\cdots+n\le n\cdot n=n^2,$$
$$n!=1\cdot2\cdots n\le n^n,$$
$$\log(n!)\le\log(n^n)=n\log n.$$

각각 $O(n^2)$, $O(n^n)$, $O(n\log n)$라는 상한이다. 마지막 식은 logarithm이 증가함을 사용한다. 상한을 증명하는 것과 그 상한이 tight(정확한 증가 차수)함을 증명하는 것은 다르다.

자료의 growth graph에는 $1,\log n,n,n\log n,n^2,2^n,n!$가 등장한다. 충분히 큰 $n$에서는 이 순서로 빠르게 증가하지만 작은 입력에서도 항상 엄격한 순서는 아니다. 예를 들어 $4^2=2^4$다. 원본 세로 눈금이 $1,2,4,8,\ldots$처럼 배증하므로 직선 눈금에서의 기울기로 읽어서도 안 된다.

### Sum과 product의 bound

$f_i=O(g_i)$의 witnesses를 $C_i,k_i$라 하자. 두 부등식을 동시에 쓰려면 $x>\max(k_1,k_2)$로 잡는다. 그러면

$$|f_1+f_2|\le|f_1|+|f_2|
\le C_1|g_1|+C_2|g_2|
\le(C_1+C_2)\max\{|g_1|,|g_2|\}.$$

따라서 $f_1+f_2=O(\max\{|g_1|,|g_2|\})$이고, 같은 $g$로 bound되면 sum도 $O(g)$다. Product에는

$$|f_1f_2|\le C_1C_2|g_1g_2|$$

를 사용하므로 $f_1f_2=O(g_1g_2)$다. M005 PDF p.32와 [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 13:16]]의 규칙은 이렇게 공통 threshold와 새 상수를 만들어 확인할 수 있다. $g_1,g_2$가 nonnegative이면 sum 형태의 bound도 편리하지만, 부호가 있는 function에 절댓값 없는 $g_1+g_2$를 쓰면 상쇄로 0이 될 수 있다.

## Big-Omega와 Big-Theta

Big-Omega $f=\Omega(g)$는 어떤 $C>0,k>0$에 대해 모든 $x>k$에서 $|f(x)|\ge C|g(x)|$인 eventual lower bound(충분히 큰 입력에서의 하한)다. 부등식을 다시 쓰면 $|g(x)|\le(1/C)|f(x)|$이므로

$$f=\Omega(g)\quad\Longleftrightarrow\quad g=O(f).$$

Big-Theta $f=\Theta(g)$는 $f=O(g)$와 $f=\Omega(g)$를 함께 만족한다는 뜻이다. 즉 충분히 큰 입력에서 양쪽 상수 배율 사이에 끼인다. Upper bound와 lower bound의 상수가 같을 필요는 없다. 두 threshold 중 큰 것을 택하면 두 조건을 함께 쓸 수 있다. M005 PDF pp.33–34는 이 방향을 구분한다. STT에서 lower bound를 Big-O처럼 부르는 불명확한 대목은 위 정의로 구별해 읽는다.

$\Theta$는 대칭이지만 $O$는 일반적으로 대칭이 아니다. $n=O(n^2)$여도 $n^2=O(n)$은 아니다. 후자가 맞다면 충분히 큰 모든 $n$에서 $n^2\le Cn$, 즉 $n\le C$여야 하므로 고정된 $C$와 양립하지 않는다.

상한만 증명하고 $\Theta$라고 쓰는 오류를 피하려면 하한을 만드는 부분을 따로 찾아야 한다. 2022-2 중간의 power sum 문항도 이 두 방향을 요구한다. [EX:dm_2022_2_mid_q03 p.1] 그 사고방식을 일반적인 고정 정수 $d\ge1$에 적용하면 $\sum_{j=1}^{n}j^d\le n^{d+1}$이고, 뒤쪽 절반에는 각각 $(n/2)^d$ 이상인 항이 적어도 $n/2$개 있으므로

$$\sum_{j=1}^{n}j^d\ge\frac n2\left(\frac n2\right)^d
=\frac{n^{d+1}}{2^{d+1}}.$$

양쪽 bound가 같은 차수여서 $\Theta(n^{d+1})$가 된다. 이는 특정 기출의 원문이나 제공 답안을 옮긴 것이 아니라, 필요한 하한 논증을 일반적인 식으로 전개한 보충이다.

## Cost model이 정하는 시간과 공간

Performance(성능)는 하나의 숫자보다 넓은 개념이다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 19:03]]은 code simplicity(코드의 단순성)도 한 관점이라고 설명한 뒤 time complexity와 space complexity를 구분했다. 코드가 짧다는 이유만으로 실행도 빠르다고 결론 내릴 수는 없다.

Time complexity(시간 복잡도)는 보통 실제 seconds 대신 정한 basic operation(기본 연산)의 횟수를 input size의 function으로 센다. 이를 실제 latency(지연시간)로 바꾸려면 operation의 비용과 hardware·software 조건이 필요하다. Integer multiplication을 한 번으로 셀 수도 있고, 각 digit multiplication과 addition을 나누어 셀 수도 있다. 무엇을 세는지 먼저 정하는 것이 cost model(비용 모형)이다.

Linear Search의 `x != ai`는 데이터 비교이고 `i <= n`은 loop-control housekeeping(반복 제어를 위한 부수 연산)이다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 34:07]]에서는 main operation 위주로 분석해도 된다고 안내했다. 그래도 구체 count를 제시할 때는 포함한 항목을 밝혀야 한다. 둘 다 comparison이라도 index와 데이터의 bit length가 다르면 실제 비용까지 같지는 않다. Fixed-word 연산을 상수 비용으로 보는 모델을 임의 길이 정수의 bit cost에 그대로 적용하지 않는다.

Space complexity(공간 복잡도)는 계산에 필요한 memory의 양이다. [[courses/discrete_mathematics/units/paradigms-greedy-and-computability|Turing machine]]에서는 사용하는 tape 공간으로 이해할 수 있다. 필요한 memory를 확보하지 못하면 시간이 충분해도 같은 계산을 그대로 실행할 수 없다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 24:16]]은 context가 커질 때의 memory 요구를 동기로 들었다. 다른 algorithm이나 저장 전략을 쓰는 것은 별도의 변경이며, 단순히 기다리는 것과 다르다.

같은 강의 22:38의 qubit 예도 자원의 종류를 생각하게 한다. 1,000-qubit 장치 두 개를 따로 갖는 것과 2,000 qubits가 함께 계산하는 장치 하나는 같은 구성이라고 할 수 없다. 이는 자원의 개수와 공동 사용 가능한 구조를 구별하는 비유이며, 모든 연결 방식의 불가능성을 증명한 것은 아니다.

### Arithmetic과 data movement

Arithmetic(산술 연산)만 빨라져도 전체 계산이 같은 비율로 빨라지는 것은 아니다. 데이터를 보관하고 이동하는 data movement(데이터 이동)가 큰 비용이면 그 부분이 bottleneck(병목)이 된다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 26:02–29:27]]은 GPU의 병렬 행렬 연산과 FPGA 등 hardware 선택을 시간·에너지 비용과 연결하면서, 수업에서는 operation count라는 추상화를 사용한다고 설명했다.

해설용으로 전체 비용을 arithmetic 10, transfer 90으로 가정하자. Arithmetic을 10% 줄이면 10이 9가 되어 전체는 100에서 99로 줄어든다. 전체 감소율은 1%다. 이 숫자는 특정 장치에서 측정한 비율이 아니라 부분 개선과 전체 개선의 차이를 보여 주는 계산이다. Asymptotic notation이 상수 배율을 숨긴다고 현실의 두 배 차이가 사라지는 것도 아니다.

## Worst-case와 distribution-dependent average

입력 크기가 같아도 내용에 따라 비용은 달라질 수 있다. Worst-case analysis(최악 경우 분석)는 그 크기의 허용 입력 전체에서 최대 비용을 본다. 따라서 모든 입력에 적용되는 보장이 되지만, 실제로 드문 입력이 최대를 만들면 일상적인 사용에서는 느슨할 수 있다.

Average-case analysis(평균 경우 분석)는 input distribution(입력 분포) $D$를 정하고

$$\mathbb E_D[T(X)]=\sum_x\Pr_D[X=x]T(x)$$

를 계산한다. 모든 입력을 똑같이 평균내는 것은 uniform distribution(균등분포)이라는 특정한 가정이다. 어떤 분포를 썼는지 없으면 평균 비용도 정해지지 않는다.

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 38:35]]의 feature vector(특징 벡터) 예를 일반적인 데이터 모델로 읽어 보자. 데이터가 벡터로 표현된다고 가능한 모든 벡터가 같은 확률로 나타나지는 않는다. 실제 분포를 모르는 경우도 많다. Worst-case가 매우 커도 특정 분포에서는 빠를 수 있지만, 그 주장을 하려면 그 분포와 계산을 제시해야 한다. 이 차이는 [[courses/discrete_mathematics/units/search-and-matrix-complexity|Linear Search의 성공·실패 확률별 평균]]에서 수치로 확인할 수 있다.

## 핵심 정리

- Big-O의 C와 threshold는 입력이 커져도 고정되어야 하며 upper bound만으로 tightness는 얻지 못한다.
- 합과 곱의 규칙은 공통 threshold에서 부등식을 결합하여 증명한다.
- Operation count를 latency로 바꾸려면 실제 연산 비용과 data movement를 알아야 한다.
- Average-case에는 distribution이 필요하고, 공간 부족은 더 오래 기다리는 것만으로 해소되지 않는다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Big-O의 정확한 의미

f=O(g)의 quantifier와 절댓값 조건을 쓰라. 3n과 100n이 모두 O(n)이라는 사실은 equality인가? C=n을 골라 n²=O(n)이라고 할 수 있는가?

<details><summary>해설 보기</summary>

고정된 C>0,k>0가 존재하여 모든 x>k에서 |f(x)|≤C|g(x)|여야 한다. 3n과 100n은 각각 C=3,100과 k=1로 bound되지만 같은 함수가 아니다. O(n)은 이런 함수의 collection이어서 = 표기는 소속 관계처럼 읽는다. C=n은 입력에 따라 변하므로 witness가 아니다. n²≤Cn이면 n≤C가 필요해 임의로 큰 n을 고정 C가 덮지 못한다. 작은 입력에서의 실패나 f>g 자체는 허용된다.

**점검 기준:** 상수 선택 뒤 모든 큰 입력이라는 순서, 함수 equality와 bound, concrete count와 growth를 구별한다.

</details>

#### 확인 Q02 · Polynomial·sum·factorial bound

f(x)=2x²−7x+3의 x>1에 대한 witness를 구하라. Σⱼ₌₁ⁿj, n!, log(n!)의 본문 upper bound도 부등식으로 보이라.

<details><summary>해설 보기</summary>

|f(x)|≤2x²+7x+3≤12x²이므로 C=12,k=1이다. 일반 차수 d에서는 xⁱ≤xᵈ를 이용하여 C=Σ|aᵢ|로 잡는다. Σj≤n·n=n², n!=Πj≤Πn=nⁿ이다. 고정된 밑이 1보다 큰 log는 증가하므로 log(n!)≤log(nⁿ)=n log n이다. 이로써 각각 O(n²),O(nⁿ),O(n log n)를 얻지만 상한만으로 tightness까지 증명한 것은 아니다.

**점검 기준:** 절댓값 합을 쓰고 각 상한의 중간 부등식과 logarithm의 증가 조건을 밝힌다.

</details>

#### 확인 Q03 · Growth graph의 축과 범위

1, log n, n, n log n, n², 2ⁿ, n!의 eventual 증가 순서를 쓰라. 작은 n에서도 늘 엄격한 순서인가? 세로축 눈금이 1,2,4,8,…인 그림의 기울기를 어떻게 읽어야 하는가?

<details><summary>해설 보기</summary>

충분히 큰 n에서는 제시한 순서로 증가 속도가 빨라진다. 하지만 n=4에서는 n²=2ⁿ=16이고 n=2에서는 n!=2<2²이므로 작은 n까지 엄격한 부등식이 성립하지 않는다. 세로축이 배증하면 같은 눈금 간격은 같은 차이가 아니라 같은 배율을 나타낸다. 선형 축의 기울기처럼 수치 증가량을 읽으면 안 된다.

**점검 기준:** Eventually라는 범위, 작은 입력 반례, 축의 배율 의미를 모두 확인한다.

</details>

#### 확인 Q04 · Sum·product의 witnesses

f₁=O(n²),f₂=O(n³)의 합과 곱을 witnesses로 정당화하라. Signed g₁,g₂에 절댓값 없는 g₁+g₂를 무조건 bound로 쓰면 무엇이 문제인가?

<details><summary>해설 보기</summary>

각 Cᵢ,kᵢ를 잡고 n>max(k₁,k₂,1)에서 |f₁+f₂|≤C₁n²+C₂n³≤(C₁+C₂)n³이므로 합은 O(n³)다. |f₁f₂|≤C₁C₂n⁵이므로 곱은 O(n⁵)다. 일반 sum은 max(|g₁|,|g₂|)로 bound한다. g₁=n,g₂=−n이면 g₁+g₂=0으로 상쇄된다. 예컨대 f₁=f₂=n은 각각 O(gᵢ)이지만 합 2n은 O(0)이 아니므로 절댓값 없는 합 규칙은 일반적으로 실패한다.

**점검 기준:** 공통 threshold와 새 상수를 쓰고 signed 함수의 상쇄 반례를 계산한다.

</details>

#### 확인 Q05 · Ω·Θ와 방향

Ω와 Θ를 정의하고 f=Ω(g) iff g=O(f)를 설명하라. Θ는 대칭인데 O가 대칭이 아닌 예를 들고, upper bound만 얻었을 때 같은 order라고 할 수 있는지 말하라.

<details><summary>해설 보기</summary>

Ω는 고정된 C>0,k>0에 대해 모든 x>k에서 |f(x)|≥C|g(x)|인 하한이다. 이를 |g|≤(1/C)|f|로 바꾸면 g=O(f)다. Θ는 upper와 lower bound를 동시에 만족하는 관계이며 두 상수와 threshold는 달라도 된다. 각각의 큰 threshold 이후에 양쪽을 쓰면 되고, 부등식을 뒤집어도 상수배 비교가 되어 Θ는 대칭이다. n=O(n²)이지만 n²=O(n)은 아니므로 O는 대칭이 아니다. Upper bound만으로는 같은 order를 말할 수 없다.

**점검 기준:** 방향·상수의 역수·공통 threshold와 양방향 필요성을 설명한다.

</details>

#### 확인 Q06 · Code simplicity와 time cost

소스 코드가 짧으면 operation count도 줄어드는가? Linear Search에서 n과 2n+2라는 count가 공존하는 이유와 index comparison·data comparison의 실제 비용 차이를 설명하라.

<details><summary>해설 보기</summary>

Code simplicity는 기술의 단순성이고 time complexity는 선택한 operation이 몇 번 수행되는지다. 짧은 loop도 많이 반복할 수 있어 같은 평가가 아니다. 실패하는 Linear Search에서 n은 data comparison만, 2n+2는 n번의 범위·data 비교와 종료 범위 검사·마지막 if까지 셀 수 있다. 따라서 count가 다르더라도 모순은 아니다. Data의 bit length가 index보다 클 수 있어 같은 '비교'라도 실제 비용은 다르다. Fixed-word 상수 비용과 임의 길이 정수 bit cost, count와 seconds를 구분해야 한다.

**점검 기준:** 줄 수·operation 종류·housekeeping 포함 여부·bit length·latency를 각각 분리한다.

</details>

#### 확인 Q07 · Space와 함께 쓸 수 있는 자원

Memory 요구량이 가용 공간을 넘을 때 시간을 두 배 주면 반드시 실행되는가? 1,000-qubit 장치 두 개와 2,000 qubits가 함께 연산하는 장치를 같은 것으로 세어도 되는가?

<details><summary>해설 보기</summary>

같은 algorithm의 필요한 memory가 그대로라면 더 오래 기다려도 공간이 생기지 않는다. 다른 저장 전략이나 algorithm을 쓰는 것은 별도 변경이다. Space는 Turing machine의 사용 tape 공간처럼 이해할 수 있다. 독립 장치 두 개의 총량과 공동 계산 가능한 한 장치의 구성은 같다고 단정할 수 없다. 이 비유는 자원의 구조를 구별하라는 뜻이며 모든 연결 방식의 불가능성을 증명한 것은 아니다.

**점검 기준:** 시간과 공간의 독립 조건, 자원 총량과 공동 사용 구조, 비유의 한계를 말한다.

</details>

#### 확인 Q08 · 부분 개선의 전체 효과

전체 비용을 arithmetic 10, transfer 90으로 가정하자. Arithmetic 비용을 10% 줄이면 전체 감소율은 얼마인가? GPU 등에서 operation count만으로 전체 시간·에너지 개선을 정할 수 없는 이유는 무엇인가?

<details><summary>해설 보기</summary>

Arithmetic은 10에서 9가 되므로 합은 100에서 99, 감소율은 1%다. Data movement가 그대로인 상황에서는 산술 부분 개선율 10%가 전체로 그대로 전달되지 않는다. Hardware의 병렬성, 데이터 이동, 저장, 입력 크기에 따라 지배 비용이 달라지므로 count의 감소를 전체 latency·energy로 환산하려면 더 많은 비용 정보가 필요하다. 10과 90은 예의 가정이지 모든 장치의 측정치가 아니다.

**점검 기준:** 분모를 전체 100으로 두어 계산하고 고정된 비용과 개선된 비용을 나눈다.

</details>

#### 확인 Q09 · Worst-case와 평균의 distribution

같은 크기의 입력 비용이 1 또는 9라면 평균을 크기만으로 알 수 있는가? 두 경우 확률이 1/2씩일 때와 9가 나올 확률이 1/10일 때를 비교하라. Feature vector로 표현하면 실제 입력이 uniform해지는가?

<details><summary>해설 보기</summary>

Worst-case는 허용 입력 중 최대인 9다. 균등한 두 경우의 평균은 5이고, 9의 확률이 1/10이면 0.9·1+0.1·9=1.8이다. 일반 평균은 ΣₓPr_D[X=x]T(x)여서 D가 필요하다. Vector로 encoding하는 것은 표현을 정할 뿐 실제 발생 확률을 균등하게 만들지 않는다. 드문 최악 입력과 현실 평균은 다를 수 있지만 분포를 모르면 어느 평균도 확정하지 못한다.

**점검 기준:** 확률 합 1, 두 평균과 최댓값, encoding과 실제 distribution의 차이를 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 항을 줄여도 차수가 같은가

**새로 만든 synthetic 연습.** [EX:dm_2022_2_mid_q03 p.1]의 양방향 bound 요구를 옮겼다. 선수내용은 고정 정수 d≥1의 power와 유한 합·Θ다.

짝수 n에서 S(n)=Σⱼ₌₁ⁿjᵈ를 계산하던 작업을 바꾼다. A는 뒤쪽 절반의 항만 계산하여 A(n)=Σⱼ₌ₙ⁄₂₊₁ⁿjᵈ이고, B는 마지막 항만 계산하여 B(n)=nᵈ다. A와 B가 모두 S와 같은 order라는 주장을 검토하라. 수치 대입 대신 항의 수와 크기로 상·하한을 써라.

<details><summary>해설 보기</summary>

S는 n개 항 각각이 nᵈ 이하라 S≤nᵈ⁺¹이다. 뒤쪽 n/2개는 각각 (n/2)ᵈ 이상이므로 S≥nᵈ⁺¹/2ᵈ⁺¹이다. 따라서 S=Θ(nᵈ⁺¹)다. A도 같은 뒤쪽 항들을 모두 포함하므로 nᵈ⁺¹/2ᵈ⁺¹≤A≤nᵈ⁺¹/2여서 같은 order다. B는 정확히 nᵈ이므로 Θ(nᵈ)다. B/S≤2ᵈ⁺¹/n→0이어서 같은 order가 아니다. 고정 비율의 항을 남기는 경우와 단 한 항을 남기는 경우는 다르다.

**점검 기준:** 짝수 n의 항 수, 고정된 d에 따른 상수, 각 경우의 upper·lower bound를 확인한다.

</details>

### 짧은 복습 계획

Q01–Q05에서 부등식마다 C와 threshold를 표시한다. Q06–Q09는 count·time·space·distribution 중 빠진 조건을 찾는 방식으로 복습한다. P01을 푼 뒤 [[courses/discrete_mathematics/units/search-and-matrix-complexity|실제 검색·행렬곱 count]]에 같은 기준을 적용한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 이산수학 강의·자료 연결]] · [[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 이산수학 강의·자료 연결]]

[02. Algorithms.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf) · 페이지별 보기: [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-034), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-038)

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 보정 STT]] · 34:07, 09:15, 04:07, 08:24, 13:16, 32:05, 33:19, 19:03, 24:16, 22:38, 26:02, 29:27, 35:53, 38:35.

[[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 보정 STT]] · 15:10.

2026-09-09의 검색 비용 예고를 2026-09-14의 본격 분석과 연결한다. 불명확한 Big-O 상수·bit 수·lower-bound 발화는 자료 정의와 구분한다. Hardware·qubit·데이터 이동 사례는 동기이며 보편적인 측정치나 불가능 정리가 아니다. 10+90 비용 예도 명시적으로 가정한 계산이다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

2022-2 중간 Q3에서 upper와 lower bound를 함께 만들어 Θ를 정당화하는 요구를 연결한다. [EX:dm_2022_2_mid_q03 p.1] 선수내용은 유한 합과 고정 차수 polynomial bound이며 제공 원문의 지수·문장을 옮기지 않는다. Space·code simplicity·data movement·현실 distribution을 직접 평가하는 후보는 없어도 본문과 회상에 포함한다.


---

[[courses/discrete_mathematics/units/paradigms-greedy-and-computability|← 이전: Algorithmic Paradigms·Greedy와 계산 가능성]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/search-and-matrix-complexity|다음: Searching·Matrix Multiplication의 Complexity →]]
