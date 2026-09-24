---
title: "Sets·Functions·Sequences로 구조 표현하기"
description: "Set 연산, 함수의 성질과 역함수, countability, 수열과 합의 조건을 함께 점검한다."
course: "discrete_mathematics"
unit_id: "sets-functions-sequences"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00. Introduction.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-02-lecture-01"]
---

원소와 집합, 함수의 입력과 출력, 수열의 index를 구분하며 구조를 읽는다. 계산 뒤에는 domain·codomain과 공식의 적용 조건을 확인하자.

## Set과 원소의 구별

Set(집합)은 서로 구별되는 대상들의 순서 없는 모임이다. 목록의 순서를 바꾸거나 같은 원소를 다시 써도 set은 달라지지 않는다. $a\in A$는 $a$가 $A$의 원소라는 뜻이고, $A\subseteq B$는 $A$의 모든 원소가 $B$에도 있다는 뜻이다. [[courses/discrete_mathematics/units/logic-and-proof|Quantifier]]로 쓰면 $A\subseteq B$는 $\forall x(x\in A\to x\in B)$다. 예를 들어 $1\in\{1,2\}$와 $\{1\}\subseteq\{1,2\}$는 서로 다른 종류의 관계를 말한다.

Universal set(전체집합) $U$는 현재 논의하는 전체 범위이고, empty set(공집합) $\varnothing$에는 원소가 없다. Singleton(단일원소집합)은 원소가 하나인 set이다. 따라서 $\varnothing$와 $\{\varnothing\}$는 다르다. 두 번째 set에는 empty set이라는 원소가 하나 있다. Finite set(유한집합)의 cardinality(원소 수) $|A|$는 서로 다른 원소의 수이므로 $|\{1,3,5,7\}|=4$이고 $|\varnothing|=0$이다.

[이산수학 M002 PDF pp.16–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/00.Introduction.pdf)는 수 집합을 다음 convention으로 사용한다.

| 기호 | 의미 |
|---|---|
| $\mathbb N$ | $\{0,1,2,\ldots\}$ |
| $\mathbb Z$ | 정수 전체 |
| $\mathbb Q$ | $p/q$ 꼴의 수, $p,q\in\mathbb Z$, $q\ne0$ |
| $\mathbb R$ | 실수 전체 |
| $\mathbb Z^+,\mathbb Q^+,\mathbb R^+$ | 각각의 양수 부분 |

여기서는 $0\in\mathbb N$이다. 자연수의 시작점을 다르게 정한 글을 읽을 때는 이 convention부터 확인해야 한다. Infinite set(무한집합)은 finite하지 않은 set이지만, 무한한 set들이 모두 같은 크기인 것은 아니다.

### Russell’s paradox와 정의의 경계

조건을 적기만 하면 언제나 새로운 set이 만들어지는지 생각해 보자. $S$를 “자기 자신을 원소로 갖지 않는 모든 set $u$의 모임”이라고 가정한다. 그러면 다음 두 경우가 모두 막힌다.

* $S\in S$라면 $S$의 정의상 $S\notin S$여야 한다.
* $S\notin S$라면 그 정의의 조건을 만족하므로 $S\in S$여야 한다.

이것이 Russell’s paradox(러셀의 역설)다. 문제가 되는 것은 임의의 조건을 만족하는 모든 set을 모은 것이 다시 하나의 set이라고 허용한 가정이다. 보통의 union이나 intersection 자체가 모순이라는 뜻은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 43:19]]도 이 모임을 일반적인 set으로 볼 수 없다는 취지로 설명했다. 이를 해소하는 공리적 집합론 전체까지 여기서 전개한 것은 아니다.

## Cartesian product와 set operations

Cartesian product(데카르트 곱) $A\times B$는 $a\in A$, $b\in B$인 ordered pair(순서쌍) $(a,b)$의 set이다. $A=\{1,2\}$, $B=\{a,b,c\}$이면

$$A\times B=\{(1,a),(1,b),(1,c),(2,a),(2,b),(2,c)\}.$$

Set 자체의 나열 순서는 중요하지 않지만 각 pair 안의 순서는 중요하다. 첫째 성분은 $A$에서, 둘째 성분은 $B$에서 온다. 자료의 이 예에는 $2\cdot3=6$개의 pair가 있다.

Union(합집합) $A\cup B$는 적어도 한쪽에 속하는 원소, intersection(교집합) $A\cap B$는 양쪽에 속하는 원소를 모은다. $A\cap B=\varnothing$이면 두 set은 disjoint(서로소)다. Complement(여집합) $A^c$는 $U$ 안에서 $A$ 밖에 있는 원소이며, difference(차집합) $A-B$는 $A$에는 있고 $B$에는 없는 원소다. 따라서

$$A-B=A\cap B^c.$$

설명용으로 $U=\{1,2,3,4\}$, $A=\{1,2\}$, $B=\{2,3\}$를 놓으면 $A\cup B=\{1,2,3\}$, $A\cap B=\{2\}$, $A^c=\{3,4\}$, $A-B=\{1\}$이다. Complement는 $U$에 의존한다. $U$가 바뀌면 $A$가 그대로여도 $A^c$는 달라질 수 있다.

이산수학 M002 PDF pp.24–27의 Venn diagram(벤 다이어그램)을 볼 때는 색칠된 영역을 원소 조건으로 읽으면 된다. Union 그림은 두 원 전체, intersection은 겹친 부분, complement는 사각형 $U$ 안의 원 바깥, difference는 $A$의 겹치지 않는 부분이 칠해져 있다. 그림의 넓이가 cardinality를 표시하는 것은 아니다.

### Set identities를 논리로 확인하기

원소 하나 $x$를 잡고 “왼쪽에 속한다”와 “오른쪽에 속한다”의 조건이 같은지 확인하면 set identity(집합 항등식)를 증명할 수 있다. 이산수학 M002 PDF p.28의 기본 법칙은 다음과 같다.

| 법칙 | Union | Intersection |
|---|---|---|
| Identity | $A\cup\varnothing=A$ | $A\cap U=A$ |
| Domination | $A\cup U=U$ | $A\cap\varnothing=\varnothing$ |
| Idempotent | $A\cup A=A$ | $A\cap A=A$ |
| Commutative | $A\cup B=B\cup A$ | $A\cap B=B\cap A$ |
| Associative | $A\cup(B\cup C)=(A\cup B)\cup C$ | $A\cap(B\cap C)=(A\cap B)\cap C$ |

Complement를 두 번 취하면 $(A^c)^c=A$이다. Distributive laws(분배법칙)는

$$A\cup(B\cap C)=(A\cup B)\cap(A\cup C),$$
$$A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$$

이다. 두 번째 식에서 왼쪽 원소 조건은 “$A$에 속하고, $B$ 또는 $C$에 속한다”다. 이를 두 경우로 나누면 오른쪽 조건이 된다. M002 p.15에는 첫 번째 분배식의 안쪽 기호가 p.28과 충돌하는 오기가 있으므로 위 식은 p.28과 원소 조건에 맞추어 썼다.

De Morgan’s law(드모르간 법칙) $(A\cap B)^c=A^c\cup B^c$도 같은 방식이다. 양쪽 조건을 모두 만족하지 못한다는 것은 적어도 한쪽 조건이 실패한다는 뜻이다. Difference가 반복된 긴 식도 먼저 $A-B=A\cap B^c$로 풀면 괄호의 의미를 놓치지 않는다. 2021년 중간의 set identity 항목 (f)은 이런 검토를 요구한다. 이 자료의 학기는 확인되지 않았으며, 원소 조건을 비교하는 방법을 연결한 것이다. [EX:dm_2021_mid_q01 p.1]

## Function과 대응의 성질

Function(함수) $f:A\to B$는 $A$의 각 원소에 $B$의 원소를 정확히 하나 대응시킨다. $A$는 domain(정의역), $B$는 codomain(공역)이다. $f(a)=b$일 때 $b$는 $a$의 image(상), $a$는 $b$의 preimage(원상)다. 전체 image $f[A]$는 실제 도달한 값들의 set으로, codomain보다 작을 수 있다.

이산수학 M002 PDF p.29의 도형 대응에서는 triangle이 3으로, square와 rhombus가 모두 4로, hexagon이 6으로 간다. 각 도형의 출력은 하나이므로 function이다. 하지만 서로 다른 입력 두 개가 같은 출력 4에 도달한다. 이처럼 입력당 출력 하나라는 조건과 출력당 입력 하나라는 조건은 다르다.

| 성질 | 조건 | 화살표를 읽는 기준 |
|---|---|---|
| Injection(단사) | $f(a)=f(b)\Rightarrow a=b$ | 서로 다른 입력이 같은 출력에 모이지 않는다. |
| Surjection(전사) | 모든 $b\in B$에 $f(a)=b$인 $a$가 있다. | codomain에 도달하지 못한 원소가 없다. |
| Bijection(전단사) | Injection이면서 surjection이다. | 모든 출력에 정확히 하나의 입력이 대응한다. |

M002 p.31의 그림은 입력들이 서로 다른 값으로 가지만 codomain의 4가 비어 있어 injection만 만족한다. p.32는 모든 목표가 사용되지만 3으로 두 화살표가 모여 surjection만 만족한다. p.33에서는 모든 목표에 정확히 하나의 화살표가 도달한다. Codomain을 바꾸면 surjection 여부가 달라질 수 있으므로 화살표만이 아니라 양쪽 set도 함께 봐야 한다.

### Inverse와 composition

Inverse function(역함수) $f^{-1}:B\to A$는 $b$에서 출발해 $f(a)=b$인 $a$로 돌아간다. 이 $a$가 존재해야 하므로 surjection이 필요하고, 하나로 정해져야 하므로 injection이 필요하다. 따라서 전체 codomain에서 inverse를 갖는 조건은 bijection이다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 49:12]]도 존재와 유일성을 함께 강조했다. Preimage라는 말은 inverse가 없어도 쓸 수 있지만, 여러 preimage 중 하나를 임의로 고르는 것은 전체 inverse를 정의한 것과 다르다.

$g:A\to B$, $f:B\to C$이면 composition(합성)은

$$(f\circ g)(a)=f(g(a))$$

이다. 오른쪽 $g$를 먼저 적용하고 그 결과에 $f$를 적용한다. M002 p.35의 그림도 $A\to B\to C$ 순서로 이어진다. 중간 출력이 다음 function의 domain에 들어가야 하며 순서를 바꾼 합성은 정의되지 않을 수도 있다.

Injection과 composition을 함께 다루는 2021년 중간 Q5는 이 정의를 논증에 사용하는 유형이다. 합성의 성질을 판단할 때는 임의의 두 입력을 잡고, 그 입력의 image가 같다는 가정이 합성 전후에 어떻게 전달되는지 추적한다. 어떤 전제가 실제로 쓰였는지도 구분해야 한다. [EX:dm_2021_mid_q05 p.2] 이 원문의 학기는 미확인이다.

## Countability와 무한한 목록

Countable(가산)이라는 말은 이 자료에서 finite set과 자연수로 빠짐없이 나열할 수 있는 infinite set을 모두 포함한다. Countably infinite(가산무한) set의 cardinality는 $\aleph_0$로 쓴다. 짝수 자연수는 $0,2,4,\ldots$로, 정수는 $0,1,-1,2,-2,\ldots$로 나열할 수 있다. 후자의 목록에서는 양수와 음수를 번갈아 넣으므로 어느 정수도 영원히 뒤로 밀려나지 않는다.

Hilbert’s Grand Hotel(힐베르트의 호텔)은 이런 대응의 의미를 보여 준다. 방이 $1,2,3,\ldots$이고 모두 차 있어도 방 $n$의 손님을 $n+1$로 보내면 1번 방이 빈다. 서로 다른 손님이 같은 방으로 가지 않고, 기존 손님도 모두 방을 갖는다. 두 countable 호텔을 합칠 때는 첫 호텔의 손님 $n$을 $2n-1$번 방에, 둘째 호텔의 손님 $n$을 $2n$번 방에 보내면 된다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 45:50–46:43]]에서 소개한 이동과 합치기는 유한한 방의 직관을 그대로 적용할 수 없음을 보여 준다.

### Diagonal argument로 빠진 실수 만들기

모든 infinite set이 이런 목록을 갖는 것은 아니다. 이산수학 M002 PDF p.21은 $(0,1)$의 모든 실수를 $r_1,r_2,\ldots$로 나열했다고 가정한다. $r_i$의 소수점 아래 $j$번째 자리를 $a_{ij}$라 쓰고, 대각선 자리 $a_{ii}$와 다른 $b_i$를 다음처럼 선택한다.

$$b_i=\begin{cases}1,&a_{ii}\ne1,\\2,&a_{ii}=1.\end{cases}$$

새 수 $x=0.b_1b_2b_3\ldots$는 $r_1$과 첫째 자리, $r_2$와 둘째 자리, 일반적으로 $r_i$와 $i$번째 자리에서 다르다. 따라서 목록의 어느 항도 $x$가 아니다. 모든 실수를 나열했다는 가정과 모순이므로 $(0,1)$은 uncountable(비가산)이다.

여기서 대각선이 하는 일은 항을 더하는 것이 아니라 각 행에서 다른 자리를 하나씩 확보하는 것이다. 1과 2만 쓰는 선택은 $x$가 끝없이 0 또는 9로 이어지는 소수 표현의 중복 문제도 피한다. 목록을 아무리 길게 늘여도 이 구성은 모든 행에 대해 작동한다.

## Sequence와 recurrence relation

Sequence(수열)는 정수 index의 집합에서 값들의 set $S$로 가는 function이다. $a_n$은 index $n$에 대응하는 term(항)이다. Set과 달리 순서와 같은 값의 반복이 중요하다. 유한한 alphabet(기호 집합)에서 만든 유한 sequence를 string(문자열)이라 하며, 자료에서는 empty string을 $\lambda$로, `abcd`의 길이를 4로 쓴다.

Arithmetic progression(등차수열)은 $a,a+d,a+2d,\ldots$처럼 common difference(공차) $d$가 일정하다. $a=-1,d=4$이면 $-1,3,7,11,\ldots$이다. Geometric progression(등비수열)은 $a,ar,ar^2,\ldots$처럼 common ratio(공비) $r$가 일정하다. $a=2,r=5$이면 $2,10,50,250,1250,\ldots$이다. 이 숫자 예와 string 표기는 M002 PDF pp.36–38의 복습 내용이다.

Recurrence relation(점화식)은 현재 term을 이전 terms로 정한다. Fibonacci sequence는

$$f_0=0,\quad f_1=1,\quad f_n=f_{n-1}+f_{n-2}\quad(n\ge2)$$

로 정의되어 $0,1,1,2,3,5,\ldots$를 만든다. Initial conditions(초기조건)가 없으면 같은 recurrence를 만족하는 여러 sequence가 가능하다. 이 정의와 그 값을 실제로 계산하는 절차는 구별해야 한다. 후자는 [[courses/discrete_mathematics/units/algorithms-search-and-sort|Fibonacci algorithm]]에서 다룬다.

### Summation과 product의 자료 기반 복습

다음 합 공식은 M002 PDF pp.39–41의 선택적 복습이다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 50:04]]에서는 세부 공식을 모두 알아야 한다고 요구하지 않았다.

$$\sum_{j=m}^{n}a_j=a_m+a_{m+1}+\cdots+a_n$$

이고 $\sum_{j\in S}a_j$는 index set $S$의 항을 더한다. $\prod$는 같은 방식으로 곱한다. 예를 들어 $\sum_{j=1}^{3}j=6$이고 $\prod_{j=1}^{3}j=6$이지만, 두 기호가 같은 연산을 뜻하는 것은 아니다.

유한 geometric sum $S_n=1+r+\cdots+r^n$에 $r$를 곱한 뒤 원래 식을 빼면 중간 항이 사라져

$$rS_n-S_n=r^{n+1}-1,\qquad S_n=\frac{r^{n+1}-1}{r-1}$$

을 얻는다. 자료는 $r\notin\{0,1\}$에서 이를 제시한다. $r=1$이면 직접 세어 $S_n=n+1$이고, $r=0$을 포함하려면 0제곱 표기의 convention부터 정해야 한다. M002 p.40의 중간 소거 줄에는 오기가 있어 위 전개는 항별 소거와 마지막 식으로 확인한 것이다.

| 합 | 값 |
|---|---|
| $\sum_{k=1}^{n}k$ | $n(n+1)/2$ |
| $\sum_{k=1}^{n}k^2$ | $n(n+1)(2n+1)/6$ |
| $\sum_{k=1}^{n}k^3$ | $n^2(n+1)^2/4$ |

Infinite sum(무한합)에는 수렴 조건이 더 필요하다. 자료의

$$\sum_{k=0}^{\infty}x^k=\frac1{1-x},\qquad
\sum_{k=1}^{\infty}kx^{k-1}=\frac1{(1-x)^2}$$

는 모두 $|x|<1$에서의 식이다. $x=1/2$인 첫 합은 2지만, $x=2$를 대입하여 합이 $-1$이라고 읽을 수는 없다. 실제 부분합이 계속 증가해 유한한 값으로 수렴하지 않기 때문이다.

## 핵심 정리

- 원소 관계와 부분집합 관계는 다르며, complement는 universal set에 의존한다.
- Inverse에는 출력마다 preimage가 존재하고 유일해야 하므로 bijection이 필요하다.
- Countability는 빠짐없는 listing의 문제다. Diagonal argument는 임의의 목록에 빠진 수를 만든다.
- Sequence는 index별 값과 반복을 보존한다. Recurrence에는 초기조건, 무한합에는 수렴 조건이 필요하다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · 원소·부분집합·수 집합

∅와 {∅}의 cardinality를 구하고, 1∈{1,2}와 {1}⊆{1,2}의 뜻을 구분하라. {1,1,2}의 cardinality와 이 자료의 ℕ,ℤ,ℚ,ℝ,ℤ⁺ 표기를 설명하라.

<details><summary>해설 보기</summary>

∅에는 원소가 없어 0, {∅}에는 empty set이라는 원소 하나가 있어 1이다. 1∈{1,2}는 수 1의 소속이고 {1}⊆{1,2}는 왼쪽 집합의 모든 원소가 오른쪽에도 있다는 뜻이다. 반복 기재는 새 원소가 아니므로 |{1,1,2}|=2다. ℕ={0,1,2,…}, ℤ는 정수, ℚ는 정수 p,q와 q≠0에 대한 p/q, ℝ은 실수, ℤ⁺는 양의 정수다. ℚ⁺·ℝ⁺도 각 집합의 양수 부분이다.

**점검 기준:** 중괄호의 층위를 구별하고 자연수에 0을 포함하는 convention과 분모 조건을 보존한다.

</details>

#### 확인 Q02 · Russell’s paradox의 두 경우

S를 자신을 원소로 갖지 않는 모든 집합의 집합이라 하자. S∈S와 S∉S를 각각 가정하면 무엇이 생기는가?

<details><summary>해설 보기</summary>

S∈S이면 정의상 자신을 원소로 갖지 않아 S∉S다. S∉S이면 S의 수집 조건을 만족하므로 S∈S다. 두 선택 모두 반대 결론으로 이어진다. 문제는 임의 조건에 맞는 모든 집합의 모임을 언제나 하나의 집합으로 허용한 가정에 있다. 보통의 union이나 intersection이 모두 모순이라는 결론은 아니다.

**점검 기준:** 양쪽 경우와 문제가 된 가정을 각각 말한다.

</details>

#### 확인 Q03 · Cartesian product와 네 set operations

U={1,2,3,4}, A={1,2}, B={2,3}에서 A∪B, A∩B, Aᶜ, A−B, B−A를 구하라. A×{a,b,c}를 나열하고 Venn diagram에서 difference 영역을 설명하라.

<details><summary>해설 보기</summary>

합집합은 {1,2,3}, 교집합은 {2}, Aᶜ={3,4}, A−B={1}, B−A={3}이다. 교집합이 비지 않았으므로 disjoint가 아니다. A×{a,b,c}={(1,a),(1,b),(1,c),(2,a),(2,b),(2,c)}로 6개다. 각 pair의 순서는 보존한다. Venn diagram의 A−B는 A 안에서 B와 겹치지 않는 부분이며 B−A와 일반적으로 다르다. 그림의 넓이가 cardinality는 아니다.

**점검 기준:** 모든 계산과 ordered pair의 순서, complement의 U 의존성을 확인한다.

</details>

#### 확인 Q04 · Set identities를 원소 조건으로 설명하기

A∩U, A∪∅, A∪U, A∩∅, A∪A, (Aᶜ)ᶜ를 정리하라. Union·intersection의 교환·결합법칙과 두 분배법칙을 쓰고, (A∩B)ᶜ=Aᶜ∪Bᶜ의 이유를 설명하라.

<details><summary>해설 보기</summary>

앞의 값은 A,A,U,∅,A,A다. A∩A도 A다. A∪B=B∪A, A∩B=B∩A이고, 각 연산에서 괄호를 바꿔도 같다: A∪(B∪C)=(A∪B)∪C, A∩(B∩C)=(A∩B)∩C.

분배식은 A∪(B∩C)=(A∪B)∩(A∪C), A∩(B∪C)=(A∩B)∪(A∩C)다. 첫 식의 원소는 A에 있거나 B,C에 모두 있으므로 A 또는 B이면서 A 또는 C이다. 둘째 식은 A이면서 B 또는 C인 조건을 두 경우로 나눈다. De Morgan 식은 두 조건을 모두 만족하지 않는 것이 적어도 하나의 실패와 같다는 뜻이다. Difference는 A∩Bᶜ로 바꿔 같은 방법으로 확인한다.

**점검 기준:** 항등식을 이름만 적지 말고 분배와 부정의 원소 조건을 설명한다.

</details>

#### 확인 Q05 · Function의 image와 codomain

도형 집합 {triangle,square,rhombus,hexagon}에서 {3,4,5,6}으로 각 변의 수를 보내자. Function·injection·surjection·bijection 여부와 image를 판정하고, codomain을 image로 바꾸면 어떤 성질이 달라지는지 설명하라.

<details><summary>해설 보기</summary>

각 도형은 출력 하나를 가지므로 function이다. Image는 {3,4,6}이다. Square와 rhombus가 모두 4로 가므로 injection이 아니고, 5에는 preimage가 없으므로 surjection도 아니다. 따라서 bijection도 아니다. Codomain을 {3,4,6}으로 제한하면 surjection은 되지만 두 입력의 collision은 남아 injection·bijection은 여전히 아니다.

**점검 기준:** 입력당 출력 하나와 출력당 입력 하나를 구분하고, codomain 변경은 collision을 없애지 못함을 설명한다.

</details>

#### 확인 Q06 · Inverse의 존재와 composition 순서

Injection만인 f:A→B는 왜 B 전체에서 inverse를 갖지 못하는가? Surjection만이면 무엇이 문제인가? g:A→B, f:B→C의 합성을 쓰고 preimage와 inverse를 구별하라.

<details><summary>해설 보기</summary>

Injection만이면 일부 b∈B에 preimage가 없어 inverse의 출력을 정할 수 없다. Surjection만이면 한 b에 여러 preimages가 있을 수 있어 inverse 값이 유일하지 않다. 두 조건이 모두 있어야 bijection이고 B 전체의 inverse가 존재한다. 합성은 (f∘g)(a)=f(g(a))로 g부터 적용하며 중간 값이 f의 domain에 속해야 한다. Preimage는 inverse가 없어도 특정 출력으로 가는 입력을 뜻할 수 있다.

**점검 기준:** 존재와 유일성의 역할, 합성의 오른쪽 우선 순서를 각각 설명한다.

</details>

#### 확인 Q07 · Countable 목록과 호텔 배치

이 자료의 countable에는 finite set도 들어가는가? 정수의 listing을 쓰고, 만실인 countably infinite 호텔에 한 손님을 추가하거나 두 호텔의 손님을 한 호텔에 합치는 배치를 설명하라.

<details><summary>해설 보기</summary>

Finite도 countable에 포함한다. 정수는 0,1,−1,2,−2,…로 나열하며 모든 정수는 유한한 위치에 등장한다. 방 번호가 1부터 시작하면 기존 손님 n을 n+1로 옮겨 1번 방을 비운다. 두 호텔은 첫 호텔 손님 n을 2n−1, 둘째를 2n에 보낸다. 각 호텔 내부와 두 호텔 사이 모두 방 번호가 겹치지 않고 모든 손님에게 유한한 방 번호가 있다.

**점검 기준:** 빠짐없음과 충돌 없음을 확인하며, 무한히 많은 버스의 별도 배치를 이미 증명했다고 확대하지 않는다.

</details>

#### 확인 Q08 · Diagonal argument의 핵심

(0,1)의 모든 실수가 r₁,r₂,…로 나열되었다고 가정하자. 대각 자리 aᵢᵢ가 1이면 bᵢ=2, 아니면 bᵢ=1로 정할 때 어떤 모순이 생기는가? 왜 1과 2를 쓰는가?

<details><summary>해설 보기</summary>

x=0.b₁b₂…는 (0,1)에 있으며 임의의 i에서 rᵢ와 i번째 자리가 다르다. 따라서 어느 rᵢ도 x일 수 없어 전체 목록이라는 가정과 모순이다. 1과 2만 쓰면 새 수는 결국 0 또는 9만 이어지는 소수의 중복 표현이 되지 않아 자리 차이로 서로 다른 수를 보일 수 있다. 유한 개 행만 비교한 것이 아니라 임의의 행 i에 작동한다.

**점검 기준:** 임의의 i에서 달라지는 자리와 소수 표현의 중복 회피를 설명한다.

</details>

#### 확인 Q09 · Sequence·string·초기조건

Set과 sequence가 반복과 순서를 다루는 차이를 설명하라. Empty string과 `abcd`의 길이, a=−1,d=4인 arithmetic progression과 a=2,r=5인 geometric progression의 처음 네 항을 쓰라. Fibonacci의 초기조건 없이 recurrence만으로 수열이 정해지는가?

<details><summary>해설 보기</summary>

Sequence는 정수 index마다 값을 주는 function이므로 같은 값의 반복과 순서를 유지한다. Set은 같은 원소를 중복 세지 않고 순서도 없다. Empty string λ의 길이는 0, `abcd`는 4다. 두 progression은 각각 −1,3,7,11과 2,10,50,250이다. fₙ=fₙ₋₁+fₙ₋₂만으로는 시작값을 정할 수 없다. f₀=0,f₁=1을 더 주면 0,1,1,2,3,5,…로 정해진다.

**점검 기준:** Index·공차·공비·초기조건을 분리하며 string과 progression 숫자는 자료 기반 복습임을 유지한다.

</details>

#### 확인 Q10 · 유한 합과 곱, geometric sum

Σⱼ₌₂⁴j와 Πⱼ₌₂⁴j를 계산하라. Sₙ=1+r+⋯+rⁿ의 소거식을 유도하고 1+2+4+8, r=1인 경우를 구하라. Σk, Σk², Σk³ 공식을 n=3에서 확인하라.

<details><summary>해설 보기</summary>

합은 2+3+4=9, 곱은 2·3·4=24다. rSₙ−Sₙ에서는 중간 항이 소거되어 rⁿ⁺¹−1만 남으므로 r≠1에서 Sₙ=(rⁿ⁺¹−1)/(r−1)이다. r=2,n=3에서는 15이고, r=1에서는 1이 n+1개여서 n+1이다. 자료는 r∉{0,1}로 제시하므로 r=0은 0제곱 convention을 먼저 정해야 한다.

Σₖ₌₁ⁿk=n(n+1)/2, Σk²=n(n+1)(2n+1)/6, Σk³=n²(n+1)²/4다. n=3이면 각각 6,14,36이며 직접 1+2+3, 1+4+9, 1+8+27과 맞는다.

**점검 기준:** Σ와 Π를 구분하고 소거 부호·끝항·r=1 예외 및 세 공식의 값을 확인한다.

</details>

#### 확인 Q11 · 무한합의 적용 조건

Σₖ₌₀∞xᵏ와 Σₖ₌₁∞kxᵏ⁻¹의 공식을 조건과 함께 쓰라. x=1/2의 값은 무엇이며 x=2에 첫 식을 대입해 −1을 얻어도 되는가?

<details><summary>해설 보기</summary>

|x|<1에서 각각 1/(1−x), 1/(1−x)²다. x=1/2이면 2와 4다. x=2에서는 첫 합의 부분합 1+2+⋯+2ⁿ=2ⁿ⁺¹−1이 끝없이 커지므로 유한한 합 −1이 될 수 없다. 유한 geometric sum의 대수식과 무한합의 수렴 조건은 별개다.

**점검 기준:** 두 공식의 index와 |x|<1을 보존하고 x=2의 부분합으로 잘못된 적용을 반박한다.

</details>

### 적용 연습

#### 연습 P01 · Difference 식 고치기

**새로 만든 synthetic 연습.** [EX:dm_2021_mid_q01 p.1] (f)의 원소별 set identity 검토를 옮겼다. Set operations와 논리 연산이 선수내용이다.

(A∪B)−C=(A−C)∩(B−C)라는 주장을 작은 반례로 반박하고, 오른쪽 연산 하나를 고쳐 원소 조건으로 증명하라.

<details><summary>해설 보기</summary>

A={1}, B=∅, C=∅이면 왼쪽은 {1}, 오른쪽은 ∅여서 반례다. 올바른 식은 (A∪B)−C=(A−C)∪(B−C)다. 왼쪽 원소는 A 또는 B에 속하면서 C에는 속하지 않으므로, A에 속하고 C 밖이거나 B에 속하고 C 밖인 원소다. 이는 수정한 오른쪽과 양방향으로 같다.

**점검 기준:** 직접 계산한 반례, 수정된 union, 양방향 원소 조건을 제시한다.

</details>

#### 연습 P02 · 전체 함수와 제한된 합성

**새로 만든 synthetic 연습.** [EX:dm_2021_mid_q05 p.2]의 합성 전후 injection 추적을 옮겼다. Domain·codomain·image와 composition만 필요하다.

A={a,b}, B={1,2,3}, C={u,v}이고 g(a)=1,g(b)=2, f(1)=u,f(2)=v,f(3)=u다. f와 f∘g의 injection 여부가 다른 이유를 설명하라. A에 c를 추가하고 g(c)=3으로 확장하면 무엇이 달라지는가?

<details><summary>해설 보기</summary>

f는 1과 3을 같은 u로 보내므로 injection이 아니다. 하지만 합성은 a→u,b→v여서 injection이다. g[A]={1,2}에서는 f의 collision을 만드는 3을 사용하지 않기 때문이다. c를 추가하면 합성에서 a와 c가 u로 만나 injection이 깨진다. f 전체의 성질과 실제로 들어오는 image 위의 작용을 구별해야 한다.

**점검 기준:** 합성 값을 모두 쓰고, 처음에는 사용되지 않은 입력 3이 왜 확장 후 문제를 만드는지 설명한다.

</details>

### 짧은 복습 계획

Q01–Q04는 작은 집합을 그려 답하고, Q05–Q06은 화살표 방향을 표시한다. Q07–Q08의 무한집합 논증을 말로 재현한 뒤 Q09–Q11의 초기조건·수렴 조건을 확인한다. P01–P02에서 틀린 식은 반례와 수정식을 나란히 남긴다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-02-lecture-01|2026-09-02 이산수학 강의·자료 연결]]

[00. Introduction.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/00.Introduction.pdf) · 페이지별 보기: [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-041)

[[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 보정 STT]] · 44:09, 43:19, 47:41, 48:32, 49:12, 45:50, 46:43, 40:48, 50:04.

2026-09-02의 개념 복습과 Introduction 자료를 함께 읽는다. String·개별 progression 예와 상세 합 공식은 자료 기반 보충이며, 특히 pp.39–41은 선택적 복습이다. 자연수는 0을 포함한다. p.15의 분배식과 p.40 중간 소거식에는 오기가 있어 p.28의 원소 조건과 p.40의 최종 식으로 확인한다. 두 호텔보다 깊은 무한 버스 배치나 recurrence 해법은 여기서 요구하지 않는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

[[exam_questions/dm_2021_mid_q01|2021 학기 미확인 중간 Q1]]에서는 (f)의 set identity 검토만 연결한다. [EX:dm_2021_mid_q01 p.1] [[exam_questions/dm_2021_mid_q05|같은 시험 Q5]]에서는 injection의 정의를 합성 전후로 적용하는 논증을 연결한다. [EX:dm_2021_mid_q05 p.2] 선수내용은 원소 조건, domain·codomain과 composition이며 onto 함수의 개수를 세는 inclusion-exclusion이나 characteristic equation은 포함하지 않는다.


---

[[courses/discrete_mathematics/units/logic-and-proof|← 이전: Discrete Mathematics의 언어와 Logic·Proof]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/matrices-and-linear-maps|다음: Matrices와 Linear Maps의 대응 →]]
