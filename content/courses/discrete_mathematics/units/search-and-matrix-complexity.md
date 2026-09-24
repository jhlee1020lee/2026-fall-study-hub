---
title: "Searching·Matrix Multiplication의 Complexity"
description: "검색 count와 분포, 행렬곱·Strassen 비용, AI 계산식의 domain과 검증을 연결한다."
course: "discrete_mathematics"
unit_id: "search-and-matrix-complexity"
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

검색의 비교 횟수와 행렬곱의 산술 횟수를 실제 구현에서 센다. 더 작은 exponent나 kernel 개선을 해석할 때는 연산 환경·상수·전체 비용까지 확인하자.

## Linear Search의 비교 횟수와 평균

[[courses/discrete_mathematics/units/algorithms-search-and-sort|Linear Search]]는 앞에서부터 목표를 확인한다. 먼저 [[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|Cost model]]을 정하자. 목표 $x$와 원소 $a_i$의 main data comparison만 세면 위치 $i$에서 성공할 때 $i$회이고, 실패할 때 $n$회다. 첫 원소에서 성공하는 best case(최선 경우)는 1회이고, 마지막에서 성공하거나 끝까지 실패하는 worst case는 $n$회다. 따라서 worst-case는 $\Theta(n)$이다.

[이산수학 M005 PDF pp.39–40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)는 loop-control comparison과 마지막 `if`까지 함께 센다. 두 convention을 나란히 놓으면 숫자의 차이가 설명된다.

| 경우 | Main data comparison | 자료의 넓은 comparison count |
|---|---:|---:|
| 위치 $i$에서 성공 | $i$ | $2i+1$ |
| 실패 | $n$ | $2n+2$ |

성공할 때 각 방문 위치에서 범위 검사와 데이터 비교를 하고, loop 밖에서 범위를 한 번 더 확인하므로 $2i+1$이다. 실패할 때는 $n$회의 두 비교에, 실패로 loop를 끝내는 범위 검사와 마지막 `if`가 더해져 $2n+2$다. 실패 뒤 존재하지 않는 $a_{n+1}$을 비교한 수가 아니다.

목표가 반드시 존재하고 위치가 uniform하다고 가정하면 main comparison의 평균은

$$\frac1n\sum_{i=1}^{n}i=\frac{n+1}{2}$$

이다. 같은 가정에서 자료의 평균은

$$\frac1n\sum_{i=1}^{n}(2i+1)=n+2.$$

두 답은 모두 $\Theta(n)$이며 세는 대상이 다르다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 34:07]]에서는 main operation 중심 분석을 허용했지만, 어느 count를 택했는지는 명시해야 한다.

### 성공 확률이 달라질 때

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 42:03]]은 존재 확률 0.3, 부재 확률 0.7인 경우도 생각할 수 있다고 설명했다. 성공했을 때 위치가 uniform하다는 가정을 추가하면 main 평균은

$$0.3\frac{n+1}{2}+0.7n.$$

설명용 $n=10$에서는 $0.3\cdot5.5+0.7\cdot10=8.65$회다. 항상 성공한다고 가정한 5.5회와 다르다. 성공 위치까지 비균등하면 $p_i=\Pr(x=a_i)$, $p_{\varnothing}=\Pr(x\text{가 없음})$로 놓고

$$\mathbb E[T]=\sum_{i=1}^{n}p_i i+p_{\varnothing}n$$

으로 계산한다. 이 확률들의 합은 1이어야 한다. 평균이 “대략 절반을 본다”는 직관은 특정 성공·위치 분포에서 나온 결과다.

## Binary Search의 반감과 구현 차이

여기서 분석하는 것은 interval이 하나가 될 때까지 줄인 뒤 equality를 검사하는 [[courses/discrete_mathematics/units/algorithms-search-and-sort|자료의 Binary Search]]다. List는 미리 정렬되어 있고 비어 있지 않다. M005 PDF p.41의 가정은 $n=2^k$이며 $2k$가 아니다.

길이가 $2^k$이면 매 iteration(반복)마다 남는 길이가 정확히 절반이므로 $k$회 후 하나가 남는다. Loop 안의 `x > am`이 $k$회이고 마지막 equality가 1회이므로 main comparison은 $k+1$회다. 따라서 $\Theta(\log n)$이다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 46:06]]에는 불명확한 “$k+3$” 조각 뒤에 $k+1$이라고 정리하는 발화가 있다. 여기서는 code에 따라 $k+1$로 계산한다.

일반 $n$에서는 두 반쪽의 길이가 같지 않을 수 있다. $n=11$이면 $m=6$을 기준으로 왼쪽 $[1,6]$은 6개, 오른쪽 $[7,11]$은 5개다. 큰 쪽도 $\lceil n/2\rceil$개 이하라서 반감이 계속된다. 이 구현의 worst-case loop 수는 $\lceil\log_2n\rceil$이고, 마지막 equality를 더하면 $\lceil\log_2n\rceil+1$회다. $n=1$이면 loop는 없고 마지막 검사만 한다. 큰 $n$에서의 증가 차수가 logarithmic이라는 주장과 이 경계 경우는 양립한다.

2021년 중간 Q9는 midpoint와 일치하면 즉시 종료하도록 수정하고, 성공 위치가 균등하며 $n=2^k-1$인 조건에서 평균을 분석하게 한다. [EX:dm_2021_mid_q09 p.2] 이 원문의 학기는 미확인이다. 그 구현에서는 목표가 몇 번째 깊이에서 발견되는지에 따라 비용이 달라지므로, 위 구현의 $k+1$을 그대로 옮길 수 없다. 각 깊이의 위치 수로 가중하고 equality와 방향 비교를 어떻게 세는지 분리해야 한다. 이 연결은 구현과 분포를 먼저 고정해야 한다는 점이며, 별도의 수정 algorithm과 전용 평균 풀이를 이미 강의했다고 뜻하지 않는다.

## Schoolbook matrix multiplication의 연산 수

[[courses/discrete_mathematics/units/matrices-and-linear-maps|Matrix multiplication]]에서 $A$가 $m\times k$, $B$가 $k\times n$이면 $C=AB$는 $m\times n$이다. M005 PDF p.42의 nested loops(중첩 반복문)를 쓰면 다음과 같다.

```text
procedure matrix multiplication(A, B)
    for i := 1 to m
        for j := 1 to n
            cij := 0
            for q := 1 to k
                cij := cij + aiq * bqj
    return C
```

Output entries가 $mn$개이고 각 entry마다 $k$개의 products가 필요하므로 multiplication은 $mnk$회다. 이 code를 그대로 세면 0에 첫 product를 더하는 것까지 포함하여 addition도 $mnk$회다. 반면 M005 PDF p.43은 $k$개 products를 합하는 데 필요한 addition을 $k-1$회로 센다. 첫 product를 초기값으로 삼고 나머지를 더하면 이 count가 된다.

Square case $m=k=n=N$에서는 multiplication $N^3$회, 후자의 addition convention에서는 $N^2(N-1)$회다. 전체가 cubic인 이유는 $N^2$개의 결과마다 길이 $N$인 dot product를 계산하기 때문이다. 이 분석은 arithmetic operation count이며, 임의 길이 정수의 bit complexity나 데이터 이동 비용을 포함한 전체 latency와 같지는 않다.

### 같은 결과여도 괄호에 따라 달라지는 비용

행렬곱의 associativity는 결과의 equality를 보장하지만 중간 행렬 크기와 비용까지 같게 만들지는 않는다. 2021년 중간 Q3는 이 차이를 이용하여 괄호 배치의 비용을 비교하는 유형이다. [EX:dm_2021_mid_q03 p.2] 학기가 확인되지 않은 역사적 문항의 계산 관점을 일반식으로 보충하자.

$A:p\times q$, $B:q\times r$, $C:r\times s$이면 schoolbook multiplication 수는

$$\operatorname{cost}((AB)C)=pqr+prs,$$
$$\operatorname{cost}(A(BC))=qrs+pqs.$$

첫 식은 $AB$가 $p\times r$이라는 사실을, 둘째 식은 $BC$가 $q\times s$라는 사실을 사용한다. 계산 순서를 바꾸어도 원래 행렬의 순서 $A,B,C$는 그대로다. 긴 chain 전체에서 최적 괄호를 찾는 Dynamic programming은 추가 학습이며, 여기서는 dimension과 한 번의 multiplication 비용을 정확히 연결하는 데 초점을 둔다.

## Strassen의 일곱 block products

Schoolbook은 자연스럽지만 multiplication 횟수가 반드시 그만큼 필요한 것은 아니다. 전체 크기가 $N\times N$인 두 행렬을 네 개의 $N/2\times N/2$ blocks로 나누자. M005 PDF p.45의 그림처럼 $A_{11},A_{12}$가 윗줄이고 $A_{21},A_{22}$가 아랫줄이다. $B$도 같은 방식이다. 보통 계산은 네 output blocks 각각에 두 block products를 사용하므로 총 8회다.

Strassen은 덧셈과 뺄셈을 더 사용하여 multiplication을 7회로 줄인다. M005 PDF p.46의 식은 다음과 같다.

$$\begin{aligned}
M_1&=(A_{11}+A_{22})(B_{11}+B_{22}),\\
M_2&=(A_{21}+A_{22})B_{11},\\
M_3&=A_{11}(B_{12}-B_{22}),\\
M_4&=A_{22}(B_{21}-B_{11}),\\
M_5&=(A_{11}+A_{12})B_{22},\\
M_6&=(A_{21}-A_{11})(B_{11}+B_{12}),\\
M_7&=(A_{12}-A_{22})(B_{21}+B_{22}).
\end{aligned}$$

그리고 p.47처럼 재조합한다.

$$\begin{aligned}
C_{11}&=M_1+M_4-M_5+M_7, & C_{12}&=M_3+M_5,\\
C_{21}&=M_2+M_4, & C_{22}&=M_1-M_2+M_3+M_6.
\end{aligned}$$

예를 들어 $C_{12}$는

$$A_{11}(B_{12}-B_{22})+(A_{11}+A_{12})B_{22}
=A_{11}B_{12}+A_{12}B_{22}$$

로, 원하는 block product가 된다. $C_{11}$에서도 전개 후 $A_{11}B_{22}$, $A_{22}B_{11}$, $A_{22}B_{21}$ 등의 항이 소거되어 $A_{11}B_{11}+A_{12}B_{21}$만 남는다. 소거할 때는 $A$ block이 왼쪽, $B$ block이 오른쪽인 곱의 순서를 유지해야 한다. 행렬들이 서로 commute한다고 가정한 계산이 아니다.

### Recursive cost가 줄어드는 이유

각 block multiplication에 같은 방법을 다시 적용하면, $N$이 2의 거듭제곱이고 한계 크기에서 상수 비용으로 끝낸다는 모델에서

$$T(N)=7T(N/2)+cN^2$$

가 된다. $cN^2$는 block additions와 subtractions의 비용이다. 깊이 $\ell$에서는 $7^\ell$개의 문제가 있고 각 문제의 크기가 $N/2^\ell$이므로 그 층의 결합 비용은 $cN^2(7/4)^\ell$이다. 깊이 $\log_2N$까지의 합과 $7^{\log_2N}=N^{\log_27}$개의 말단 계산을 합치면 $\Theta(N^{\log_27})$의 scale을 얻는다.

$\log_27\approx2.8074$이므로 자료는 $O(N^{2.81})$로 반올림한다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 01:01:08]]의 log 밑과 7/8 관련 불명확한 발화는 위 recurrence로 정리해 읽는다. 일곱 식을 어떻게 발견했는지와 일반적인 Master Theorem의 증명은 이 설명의 범위 밖이다.

## 작은 exponent와 실제 crossover

자료는 square multiplication의 upper bound를 $O(n^\omega)$로 비교한다. 이 소문자 $\omega$는 lower-bound notation $\Omega$와 다른 기호다. M005 PDF pp.44,48은 schoolbook의 3, Strassen의 약 2.8074, Coppersmith–Winograd의 2.3755와 이후 작은 개선들을 소개한다. 그래프에서는 초반의 큰 하락에 비해 뒤쪽 변화가 작아 보인다. 이것은 자료가 제시한 연구 흐름이며, 표의 최신 기록을 별도로 확인한 결과가 아니다. p.44의 Strassen 연도 `1696`도 오기이므로 역사적 연도로 채택하지 않는다.

Exponent가 작아도 모든 현실 입력에서 빠른 것은 아니다. 실제 cost가 각각 $An^a$, $Bn^b$이고 $a>b$, $A,B>0$라고 가정하면 두 번째가 더 작아지는 조건은

$$n^{a-b}>\frac BA.$$

$B$가 매우 크면 crossover(성능이 역전되는 크기)가 지나치게 커질 수 있고, $n^2$개의 데이터를 저장하는 공간도 문제가 된다. Big-O upper bounds만 안다면 그것들을 정확한 cost처럼 등식으로 놓고 crossover를 계산할 수도 없다.

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 52:57, 01:01:54]]은 작은 행렬에서는 schoolbook, 큰 행렬에서는 다른 방법을 택할 수 있다는 점과 같은 algorithm의 더 tight한 분석으로도 bound가 개선될 수 있다는 점을 설명했다. Rectangular 행렬을 blocks로 나누거나 padding하는 아이디어, 정수 곱셈에서 naive 방식과 FFT 계열을 크기에 따라 달리 쓰는 아이디어도 이 맥락의 동기다. 구체적인 library나 overhead까지 확정한 분석은 아니다.

## AI-assisted 발견에서 domain과 검증 구별하기

M005 PDF pp.49–50의 사례는 주어진 계산식을 탐색하는 방법도 algorithm 설계의 대상이 된다는 것을 보여 준다. 아래 수치는 공급 자료의 소개이며 현재 기록이나 모든 hardware에서의 속도 보장으로 읽지 않는다.

| 자료의 사례 | 탐색 방식 | 소개된 계산 범위 |
|---|---|---|
| AlphaTensor (2022) | Reinforcement Learning, Monte Carlo Tree Search, neural-network-guided TensorGame | $4\times4$ over $\mathbb Z_2$에서 scalar multiplications $49\to47$ |
| AlphaEvolve (2025) | Gemini LLMs와 evolutionary framework | $4\times4$ complex-valued multiplication에서 $49\to48$ |

$\mathbb Z_2$에서는 $1+1=0$이므로 그 위에서 성립하는 식을 일반적인 실수·복소수 산술에 그대로 옮길 수 없다. 자료는 $5\times5$의 $98\to96$과 후속 95도 소개하지만 모든 결과의 domain이 위 첫 행과 같다고 단정할 수 없다. AlphaEvolve 사례의 real input은 complex input의 특수한 경우다. 후속 rational-coefficient variant라는 말은 식의 계수에 관한 것이지 입력을 유리수로 제한한다는 뜻이 아니다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 01:03:39]]의 소개는 이런 산술 환경의 차이와 함께 읽어야 한다.

새 식을 발견하는 일과 주어진 식을 검증하는 일도 다르다. Strassen에서 했듯 각 output이 $AB$의 해당 성분과 같아지는지 전개하는 것이 correctness 검사이고, scalar multiplications가 실제로 몇 개인지 세는 것은 cost 검사다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 01:06:19]]은 이 차이를 설명한다. 다만 전체 48-product 식은 공급되지 않았으므로 그 식 자체를 여기서 검산한 것은 아니다.

이와 달리 발견을 위한 탐색에는 개선된 식이 존재한다는 사전 보장 없이 상당한 시간과 계산 자원을 투입해야 할 수 있다. [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 01:06:37–01:07:35]]에서 강사는 연구자의 시간이 한정되어 있어 그런 탐색을 선택하기 어렵다는 점을 설명하고, 소개한 AI-assisted 결과에도 탐색 방법을 설계하는 연구자의 작업과 회사의 자원 투입이 함께 있었다고 덧붙였다. 사람이 얼마나 오래 걸렸을지에 관한 발언은 강사의 추정이며, 측정된 탐색 시간이나 인간에게 불가능하다는 결론은 아니다.

49를 48로 줄인 kernel의 multiplication 감소율은 $1/49\approx2.04\%$다. 전체 workload 중 그 kernel이 차지하는 비중, 추가 additions, memory와 transfer 비용이 있으므로 전체 시간이나 전력이 곧바로 2.04% 줄어들지는 않는다. 반복되는 연산의 작은 개선이 큰 누적 가치를 가질 수 있다는 동기와, 실제 시스템 전체의 절감률은 별도의 주장이다.

## 핵심 정리

- 정확한 검색 count는 종료 방식과 housekeeping 포함 여부에 따라 달라진다.
- 행렬곱은 output entries 수와 각 dot product 길이를 곱해 비용을 센다.
- Associativity가 결과를 보존해도 중간 크기와 비용은 달라질 수 있다.
- Strassen의 7개 하위 곱셈과 추가 덧셈을 함께 센다. 작은 exponent와 실제 속도 우위는 별개다.
- 계산식의 correctness, operation count, 적용 가능한 arithmetic domain을 각각 확인한다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Linear Search의 두 count와 평균

성공 위치 i와 실패 시 main comparison 및 넓은 comparison count를 유도하라. 항상 성공하고 위치가 uniform할 때 두 평균, n=10에서 성공 확률 0.3일 때 main 평균, 위치가 비균등한 경우의 식을 쓰라.

<details><summary>해설 보기</summary>

성공 i에서는 data 비교 i회다. 범위 검사도 i회와 마지막 if 1회를 세면 2i+1이다. 실패하면 data n회, 범위 n+1회, 마지막 if 1회로 2n+2다. 실패 뒤 aₙ₊₁을 비교하는 것이 아니다. Main best는 1, worst는 n으로 worst-case Θ(n)이다.

성공 위치 uniform이면 평균은 (Σi)/n=(n+1)/2, 넓은 count는 (Σ(2i+1))/n=n+2다. n=10, 성공 확률 0.3에 성공 위치 uniform이면 0.3·5.5+0.7·10=8.65다. 비균등 확률 pᵢ와 부재 확률 p∅에는 Σpᵢi+p∅n이며 Σpᵢ+p∅=1이다.

**점검 기준:** 범위·data·마지막 검사를 각각 세고 성공·실패 및 조건부 uniform 가정을 명시한다.

</details>

#### 확인 Q02 · Binary Search의 길이 감소

본문 구현에서 n=16의 main comparison 수를 구하라. n=11의 첫 분할 크기와 일반 n의 worst-case, n=1의 경우를 설명하라. 즉시 equality에서 끝나는 구현에도 같은 정확한 수가 적용되는가?

<details><summary>해설 보기</summary>

16=2⁴라 네 번 구간 비교 후 마지막 equality를 더해 5회다. 11에서는 midpoint index 6으로 [1,6]의 6개 또는 [7,11]의 5개가 남는다. 매번 큰 쪽도 ceil(n/2) 이하라 worst-case loop 수는 ceil(log₂n), 최종 비교 포함 ceil(log₂n)+1이다. n=1에서는 loop 없이 마지막 한 번만 한다. 즉시 equality 종료 구현은 발견 깊이에 따라 달라져 같은 exact count를 쓸 수 없다. 본문 비용은 정렬된 nonempty list에서의 검색 비용이다.

**점검 기준:** 정확한 반감과 ceiling bound, 마지막 검사·경계 입력·구현 차이를 함께 확인한다.

</details>

#### 확인 Q03 · Matrix multiplication의 addition 두 방식

2×3과 3×4 행렬을 zero-accumulation code로 곱할 때 output 크기·multiplication·addition 수를 구하라. 첫 product를 초기값으로 쓰면 무엇이 달라지고 square N×N에서는 어떤 식이 되는가?

<details><summary>해설 보기</summary>

Output은 2×4로 8 entries이고 각 entry에서 3 products라 multiplication은 24회다. 0에 더하는 첫 단계까지 포함하면 addition도 24회다. 세 products 자체를 합하는 데에는 entry당 2회만 필요해 첫 product 초기화 방식은 16 additions다. 일반 m×k,k×n에서는 mnk multiplications와 두 방식에 따라 mnk 또는 mn(k−1) additions다. Square N에서는 N³과 N³ 또는 N²(N−1)로 모두 cubic이다. Arithmetic count이지 임의 정밀도 bit cost는 아니다.

**점검 기준:** Output 수×inner dimension을 계산하고 초기화 convention과 bit-cost 경계를 구분한다.

</details>

#### 확인 Q04 · Exponent·crossover·분석 개선

자료의 O(n^ω)에서 ω와 Ω의 차이를 말하라. 정확한 비용이 2n³과 64n²라면 어느 범위에서 후자가 작으며, Big-O 표기만 주어진 때도 이 비교를 할 수 있는가? 새 bound는 항상 새 algorithm인가?

<details><summary>해설 보기</summary>

ω는 행렬곱 upper-bound exponent를 나타내는 소문자이고 Ω는 asymptotic lower bound 기호다. 정확한 비용이라면 64n²<2n³ iff n>32다. 일반 Anᵃ,Bnᵇ에서 a>b이면 nᵃ⁻ᵇ>B/A다. 하지만 Big-O 상한은 정확한 비용식이 아니므로 두 상한을 등식처럼 비교해 실제 crossover를 확정할 수 없다. 상수·memory·data movement 때문에 작은 exponent도 실용 입력에서 불리할 수 있고 더 tight한 분석만으로 같은 algorithm의 bound가 개선되기도 한다. 입력 크기에 따라 schoolbook·Strassen 등을 고르는 맥락이며 표의 숫자는 자료의 소개다.

**점검 기준:** 수치 경계의 strict inequality, upper bound와 exact cost, 분석 변화와 algorithm 변화의 차이를 설명한다.

</details>

#### 확인 Q05 · Strassen의 재조합을 검산하기

본문의 M₁–M₇을 다시 쓰고 네 output blocks의 재조합을 확인하라. 특히 C₁₂를 전개할 때 어떤 항이 없어지며 곱의 순서를 바꿀 필요가 있는가?

<details><summary>해설 보기</summary>

각 block을 A₁₁,A₁₂,A₂₁,A₂₂와 B₁₁,B₁₂,B₂₁,B₂₂라 쓰면 다음 일곱 products다.

M₁=(A₁₁+A₂₂)(B₁₁+B₂₂), M₂=(A₂₁+A₂₂)B₁₁, M₃=A₁₁(B₁₂−B₂₂), M₄=A₂₂(B₂₁−B₁₁), M₅=(A₁₁+A₁₂)B₂₂, M₆=(A₂₁−A₁₁)(B₁₁+B₁₂), M₇=(A₁₂−A₂₂)(B₂₁+B₂₂).

C₁₁=M₁+M₄−M₅+M₇=A₁₁B₁₁+A₁₂B₂₁,
C₁₂=M₃+M₅=A₁₁B₁₂+A₁₂B₂₂,
C₂₁=M₂+M₄=A₂₁B₁₁+A₂₂B₂₁,
C₂₂=M₁−M₂+M₃+M₆=A₂₁B₁₂+A₂₂B₂₂.

예컨대 C₁₂=A₁₁B₁₂−A₁₁B₂₂+A₁₁B₂₂+A₁₂B₂₂로 가운데 두 항이 소거된다. 나머지 재조합도 분배 후 같은 AB 항의 계수를 합하면 오른쪽 두 항만 남는다. 모든 product에서 A block은 왼쪽, B block은 오른쪽이며 commute한다고 가정하지 않는다.

**점검 기준:** 일곱 products와 네 재조합의 부호·factor 순서를 확인하고 실제 C₁₂ 소거를 보인다.

</details>

#### 확인 Q06 · 7개 하위 문제의 recursive cost

전체 dimension N이 2의 거듭제곱일 때 Strassen의 recurrence를 쓰고 log₂7 exponent가 나오는 과정을 level별 비용으로 설명하라. 덧셈 비용이 사라지는가?

<details><summary>해설 보기</summary>

T(N)=7T(N/2)+cN²다. Multiplication은 half-size 7개, 추가 block additions·subtractions는 cN²다. 깊이 ℓ에는 7ℓ개가 아니라 7^ℓ개의 문제, 각각 dimension N/2^ℓ가 있으므로 그 층 결합비용은 cN²(7/4)^ℓ다. 깊이 h=log₂N까지의 geometric sum은 7/4>1이어서 마지막 규모 N²(7/4)^h=N^(log₂7)와 같은 차수다. Leaves도 7^h=N^(log₂7)개다. 따라서 이 모델에서 Θ(N^(log₂7)), log₂7≈2.8074이며 자료는 O(N^2.81)로 반올림한다.

**점검 기준:** 7 하위 곱과 cN²를 둘 다 세고 층별 개수·크기·leaf count를 연결한다.

</details>

#### 확인 Q07 · AI 계산식의 arithmetic domain

자료의 AlphaTensor와 AlphaEvolve 사례를 탐색 방식·4×4 scalar multiplication 수·domain별로 비교하라. ℤ₂의 식을 complex inputs에 바로 적용하거나 rational-coefficient를 rational-input이라는 뜻으로 읽어도 되는가?

<details><summary>해설 보기</summary>

AlphaTensor는 Reinforcement Learning·Monte Carlo Tree Search와 neural-network-guided TensorGame을 사용한 사례이며 자료는 4×4 over ℤ₂의 49→47을 소개한다. AlphaEvolve는 Gemini LLMs와 evolutionary framework의 사례로 4×4 complex-valued의 49→48을 소개한다. ℤ₂에서는 1+1=0이므로 그 domain의 소거식을 일반 실수·복소수에 그대로 옮길 수 없다. Real input은 complex input의 특수한 경우다. Rational-coefficient variant는 계산식의 계수에 관한 말이지 입력을 유리수로 제한한다는 뜻이 아니다. 자료의 5×5 98→96 및 후속 95도 모든 결과가 같은 domain이라는 증거는 아니다.

**점검 기준:** 두 탐색 방식·숫자·domain을 묶어 말하고 계수와 입력의 범위를 구분한다.

</details>

#### 확인 Q08 · Correctness·count·전체 성능

48개의 scalar multiplication을 쓴다는 식을 받았을 때 어떤 검증이 필요한가? 49→48의 감소율과 전체 실행시간·전력 절감률은 왜 다를 수 있는가?

<details><summary>해설 보기</summary>

먼저 모든 허용 입력에서 각 output이 AB의 해당 성분과 같은지 식을 전개하여 correctness를 확인한다. 별도로 multiplication 수를 세어 48회를 확인한다. 짧은 식이 맞는 식이라는 보장도, 맞는 식이 싼 식이라는 보장도 없다. Kernel multiplication 감소율은 (49−48)/49≈2.04%다. 하지만 kernel이 전체에서 차지하는 비중과 추가 additions·memory·transfer가 다르므로 전체 시간·전력도 2.04% 준다고 결론 낼 수 없다. 발견에는 탐색 설계·자원이 필요하며 전체 48-product 식은 공급되지 않아 여기서 검산한 것은 아니다.

**점검 기준:** 검증 두 종류·감소율의 분모·전체 비용의 추가 요인·공급되지 않은 식의 한계를 확인한다.

</details>

### 발견 과정의 조건 확인

#### 확인 Q09 · 검증할 수 있다는 것과 발견할 수 있다는 것

주어진 matrix multiplication 식의 correctness와 multiplication 수를 확인할 수 있어도, 탐색을 시작하면 반드시 더 좋은 식을 찾는다고 말할 수 없는 이유는 무엇인가? 연구자의 한정된 시간과 AI-assisted 탐색의 설계·계산 자원을 연결하고, 사람이 걸렸을 시간에 관한 강사의 추정을 어떻게 읽어야 하는지 설명하라.

<details><summary>해설 보기</summary>

검증은 이미 주어진 후보 식을 전개해 output이 AB와 같은지 확인하고 연산 수를 세는 일이다. 발견은 그 후보 자체를 찾아야 하는 일이며, 탐색을 시작할 때 개선된 식이 존재한다는 보장이나 언제 찾을지에 대한 보장이 주어진 것은 아니다. 따라서 검증 방법을 안다는 사실만으로 발견의 성공이나 필요한 시간을 정할 수 없다.

연구자의 시간은 한정되어 있으므로, 성공이 불확실한 탐색에 오랫동안 시간을 쓰는 선택에는 부담이 있다. 소개된 AI-assisted 사례도 탐색 방법을 설계한 연구자의 작업과 회사의 계산 자원 투입이 함께한 결과다. AI가 탐색했다는 말이 사람의 설계나 자원 비용이 없어졌다는 뜻은 아니다.

사람이 얼마나 오래 걸렸을지에 관한 발언은 강사의 추정으로 읽어야 한다. 실제로 측정한 탐색 시간이나 인간에게 불가능하다는 증명으로 사용하지 않는다. 또한 전체 48-product 식은 공급되지 않았으므로 이 사례의 완전한 식을 여기서 검산했다고 주장하지 않는다.

**점검 기준:** 후보 검증과 후보 발견의 차이, 개선 존재·소요 시간의 사전 불확실성, 한정된 연구 시간, 인간의 탐색 설계와 계산 자원, 추정 발언의 한계를 모두 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 크기에 따라 괄호 선택하기

**새로 만든 synthetic 연습.** [EX:dm_2021_mid_q03 p.2]의 dimension과 괄호 비용 비교를 옮겼다. 선수내용은 associativity와 rectangular schoolbook count이며 chain DP는 필요 없다.

양의 정수 k에 대해 A는 2×k, B는 k×3, C는 3×k다. (AB)C와 A(BC)의 scalar multiplication 수를 구하고 어떤 k에서 각각 유리한지 판정하라. 중간 행렬 크기와 최종 결과의 같음도 설명하라.

<details><summary>해설 보기</summary>

AB는 2×3이고 그 비용은 6k, 이어 (AB)C는 2×k이며 비용 6k라 총 12k다. BC는 k×k이고 비용 3k², A(BC)는 2×k이며 비용 2k²라 총 5k²다. 12k<5k² iff k>12/5이므로 정수 k≥3에서는 (AB)C가 싸고 k=1,2에서는 A(BC)가 싸다. 양의 정수에서 동률은 없다. Associativity로 최종 행렬은 같지만 중간 2×3과 k×k의 크기·연산 수는 다르다. 행렬 순서는 A,B,C 그대로다.

**점검 기준:** 두 단계 비용과 중간 차원, k의 정수 경계, 괄호와 순서의 차이를 확인한다.

</details>

### 짧은 복습 계획

Q01–Q03에서는 먼저 count 대상과 입력 조건을 쓴다. Q05의 block 재조합 한 곳을 손으로 전개하고 Q06으로 비용을 연결한다. Q07–Q08에서 domain과 전체 성능 주장을 점검한 다음 P01의 크기별 선택을 풀어 본다. Q09는 검증과 발견을 두 열로 나누어, 주어진 것과 보장되지 않은 것을 적고 연구 시간·설계·자원의 역할을 덧붙인다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 이산수학 강의·자료 연결]]

[02. Algorithms.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf) · 페이지별 보기: [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-050)

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 보정 STT]] · 34:07, 42:03, 46:06, 47:35, 01:01:08, 52:57, 01:01:54, 01:03:39, 01:06:19, 01:04:28, 01:06:37–01:07:35.

2026-09-14의 검색·행렬곱 분석 범위다. Binary Search 자료의 n=2ᵏ와 code에 따른 k+1을 사용하고 불명확한 발화와 구분한다. Zero accumulation code와 products 합의 addition count는 다르다. AI 사례의 역사·수치는 공급 자료의 소개로 한정하며 최신 기록이나 모든 hardware의 보장으로 쓰지 않는다. Strassen의 발견 과정과 Master Theorem 일반 증명, 전체 48-product 식은 공급되지 않았다. 01:06:37–01:07:35의 탐색 불확실성·한정된 연구 시간·설계와 자원 투입을 함께 읽되, 사람이 걸렸을 시간에 관한 발언은 강사의 추정으로 한정한다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

[[exam_questions/dm_2021_mid_q03|2021 학기 미확인 중간 Q3]]의 차원·괄호별 multiplication 비용 비교를 연결한다. [EX:dm_2021_mid_q03 p.2] 선수내용은 matrix dimension·associativity·schoolbook count이며 chain DP는 제외한다. 같은 시험 Q9는 즉시 equality 종료, n=2ᵏ−1, 성공 위치 uniform이라는 조건을 사용하므로 본문 구현의 k+1을 옮길 수 없다. [EX:dm_2021_mid_q09 p.2] 이 연결은 구현·분포 비교에 한정하며 원문의 수정 code와 전용 평균 풀이를 요구하지 않는다. Strassen·AI domain·crossover를 직접 다룬 기출 후보는 없다.


---

[[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|← 이전: Asymptotic Analysis와 Cost Model]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/prime-distribution|다음: Prime Number Theorem과 소수 분포의 추정 →]]
