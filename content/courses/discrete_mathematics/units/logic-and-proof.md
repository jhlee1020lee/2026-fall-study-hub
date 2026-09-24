---
title: "Discrete Mathematics의 언어와 Logic·Proof"
description: "Proposition과 quantifier를 계산하고 귀류법의 가정과 모순을 확인한다."
course: "discrete_mathematics"
unit_id: "logic-and-proof"
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

참·거짓을 판정하는 조건을 먼저 정하고, 정의에서 결론을 끌어내는 연습을 한다. Truth table(진리표), domain(논의 영역), 모순의 근거를 직접 써 보며 뒤 단원의 증명 언어를 준비하자.

## Discrete Mathematics와 수학적 표현

Discrete Mathematics(이산수학)는 서로 구별되는 대상과 그 사이의 관계를 다룬다. 컴퓨터가 처리하는 bit, 데이터 항목, 프로그램의 단계는 이런 대상이다. 온도처럼 연속적으로 변하는 현상을 계산할 때도 측정값을 유한한 정밀도의 수로 표현하는 discretization(이산화)이 필요하다. 무엇을 데이터로 표현하고 어떤 관계를 보존할지 정하는 순간부터 수학적 모델이 개입한다. [이산수학 M002 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/00.Introduction.pdf)

Logic(논리)은 프로그램의 조건과 정당성을, set(집합)은 데이터의 모임을, graph(그래프)는 연결 관계를 표현한다. Number Theory(정수론)는 암호의 수학적 기반에, combinatorics(조합론)는 경우의 수와 알고리즘 비용 분석에 연결된다. 이는 각 응용을 이미 다 배웠다는 뜻이 아니라 같은 수학적 언어가 쓰이는 방향이다. [이산수학 M002 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/00.Introduction.pdf)의 이 연결을 이해하면 정의를 배우는 이유가 분명해진다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 31:01]]에서도 정의로부터 결과를 이끌어 내는 사고방식이 학습의 목적이라고 설명했다.

## Proposition과 logical operations

Proposition(명제)은 참 또는 거짓 중 하나의 truth value(진리값)를 갖는 선언문이다. 참인 문장만 proposition인 것은 아니다. 자료의 예에서 $1+1=2$는 참인 proposition이고, $2\pi=6.28$은 정확한 등식으로 읽으면 거짓인 proposition이다. 근삿값을 말하려면 등호 대신 근사임을 표시해야 한다.

두 proposition $p,q$를 결합하는 연산은 다음처럼 정의한다. Negation(부정) $\neg p$는 진리값을 뒤집고, conjunction(논리곱) $p\land q$는 둘 다 참일 때만 참이다. Disjunction(논리합) $p\lor q$는 적어도 하나가 참일 때 참이므로 둘 다 참인 경우도 포함한다. Implication(함의) $p\to q$는 $p$가 참인데 $q$가 거짓인 경우만 배제한다. Biconditional(동치 연결사) $p\leftrightarrow q$는 두 진리값이 같을 때 참이다.

| $p$ | $q$ | $\neg p$ | $p\land q$ | $p\lor q$ | $p\to q$ | $p\leftrightarrow q$ |
|---|---|---|---|---|---|---|
| T | T | F | T | T | T | T |
| T | F | F | F | T | F | F |
| F | T | T | F | T | T | F |
| F | F | T | F | F | T | T |

Implication을 일상적인 인과관계와 동일시하면 마지막 두 행이 낯설어진다. 여기서는 약속한 조건 $p$가 성립했는데 결론 $q$가 실패한 경우만 거짓으로 정한다. 따라서 $p\to q$와 $\neg p\lor q$의 표는 일치한다. 반대로 $q\to p$는 별개의 식이다. 표의 둘째 행에서 $p\to q$는 거짓이고 $q\to p$는 참이므로 방향을 뒤집을 수 없다. 정의와 표는 이산수학 M002 PDF pp.10–12에 해당한다.

복합식은 안쪽 연산부터 열을 만들어 계산하면 된다. 예를 들어 설명용 식 $\neg(p\land q)$는 $p\land q$ 열을 뒤집어 F, T, T, T를 얻는다. 이는 $\neg p\lor\neg q$와 같다. 모든 입력에서 같은 진리값을 갖는다는 것이 logical equivalence(논리적 동치)다. 한두 행이 일치하는 것만으로는 충분하지 않다. 2022-2 중간의 논리 문항 (a)–(b)도 이런 식 평가와 조건의 표현을 요구한다. 특히 “최대”라는 조건은 경계인 0개를 포함하는지 먼저 확인해야 한다. [EX:dm_2022_2_mid_q01 p.1]

### Boolean 값과 modulo 2의 대응

T를 1, F를 0으로 표현하면 AND는 modulo 2에서의 곱셈과 대응한다. XOR(배타적 논리합)는 두 값이 다를 때 1이므로 modulo 2의 덧셈과 대응한다. NOT은 1과 XOR하는 것으로 표현할 수 있다. [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 36:32]]의 설명에서도 덧셈에 대응시킨 것은 OR가 아니라 XOR였다.

이 구별은 $1+1\equiv0\pmod2$에서 바로 드러난다. $1\operatorname{XOR}1=0$이지만 $1\operatorname{OR}1=1$이다. 같은 두 원소 $\{0,1\}$를 사용한다고 모든 논리 연산이 이름이 비슷한 산술 연산과 같아지는 것은 아니다.

## Quantifier와 domain

Predicate(술어) $P(x)$는 $x$에 따라 진리값이 달라질 수 있는 조건이다. Universal quantifier(전칭기호) $\forall x\,P(x)$는 지정된 domain(논의 영역)의 모든 $x$에서 조건이 참임을 뜻한다. Existential quantifier(존재기호) $\exists x\,P(x)$는 그 domain에 조건을 만족하는 원소가 적어도 하나 있음을 뜻한다. 기호만 쓰고 domain을 빠뜨리면 문장의 의미를 확정할 수 없다. 이산수학 M002 PDF p.13과 [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 37:59]]의 핵심도 이 구별이다.

정수 domain에서 $\exists x(x^2=4)$는 $x=2$라는 witness(증인)로 확인한다. 그러나 $\forall x(x^2=4)$는 $x=0$이라는 counterexample(반례)로 무너진다. 하나의 witness는 존재를 보이기에 충분하고, 하나의 counterexample은 전칭 주장을 반박하기에 충분하다. 전칭 주장을 증명하려면 특정한 몇 값을 확인하는 데서 멈추지 않고 임의의 원소에 적용되는 논증이 필요하다.

Domain의 효과를 보기 위한 설명용 예로 $\exists x(x^2=2)$는 실수에서 참이지만 정수에서는 거짓이다. 방정식의 실수해를 찾았다고 정수해의 존재를 보인 것은 아니다. 2022-2 중간의 quantified statement 문항도 정수 domain을 명시한다. 식을 변형해 분모가 생긴다면 그 분모가 0인 경우를 먼저 나누어야 하며, 구한 값이 실제 domain 안에 있는지도 확인해야 한다. [EX:dm_2022_2_mid_q02 p.1]

Quantifier가 중첩되면 선택 순서도 중요하다. $\forall x\exists y\,P(x,y)$에서는 $x$를 정한 뒤 그에 맞는 $y$를 고를 수 있다. $\exists y\forall x\,P(x,y)$에서는 하나의 $y$가 모든 $x$에 통해야 한다. 이는 앞의 정의를 두 번 적용한 해석이다. 정수에서 $P(x,y)$를 $y=x+1$로 잡으면 첫 문장은 참이지만 둘째 문장은 거짓이어서 순서를 바꿀 수 없음을 볼 수 있다.

## Proof by contradiction과 기약분수

Proof by contradiction(귀류법)은 보이려는 proposition의 부정을 가정한 뒤, 어떤 $r$과 $\neg r$을 함께 도출하는 방법이다. 모순이 생겼다는 사실만 적는 대신 무엇과 무엇이 양립할 수 없는지 밝혀야 한다. 이산수학 M002 PDF p.14의 구조를 [[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 STT 39:54]]에서 짧게 언급한 $\sqrt2$ 예에 적용해 전개해 보자. 다음 계산은 그 예를 완성한 해설이다.

$\sqrt2$가 rational(유리수)이라고 가정하고 기약분수 $p/q$로 쓰되 $p,q$는 정수이고 $q\ne0$라 하자. 제곱하면

$$p^2=2q^2.$$

$p^2$가 짝수이므로 $p$도 짝수다. 홀수 $2k+1$의 제곱은 $4k(k+1)+1$로 홀수이기 때문이다. 따라서 $p=2k$라고 쓰면 $4k^2=2q^2$, 즉 $q^2=2k^2$이고 $q$도 짝수가 된다.

그러면 $p,q$가 공통인수 2를 갖는다. 이는 처음에 기약분수로 골랐다는 조건과 모순이다. 따라서 $\sqrt2$는 irrational(무리수)이다. 처음부터 기약이라는 조건을 두지 않았다면 두 수가 짝수라는 사실만으로 모순을 얻지 못한다. 증명은 결론뿐 아니라 처음 선택한 조건에 의존한다.

## 핵심 정리

- Implication은 전제가 참인데 결론이 거짓인 경우에만 거짓이며, 역방향 implication과 다르다.
- Boolean 값의 modulo 2 덧셈은 XOR에 대응한다. OR는 두 입력이 모두 참일 때 구별된다.
- 존재에는 witness 하나가 충분하지만 전칭에는 임의의 원소에 적용되는 논증이 필요하다.
- 귀류법에서는 처음 가정과 충돌하는 조건을 끝까지 명시한다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Discrete structure의 역할

온도처럼 연속적인 현상도 컴퓨터로 다룰 때 discrete structure가 필요한 이유를 설명하고, Logic·Set·Graph가 표현하는 대상을 하나씩 말하라.

<details><summary>해설 보기</summary>

컴퓨터에는 관측값을 유한 정밀도의 bit와 구별되는 데이터 항목으로 표현해야 한다. 그 표현과 연산 단계는 이산적으로 다룰 수 있다. Logic은 조건과 정당성, Set은 데이터의 모임, Graph는 연결 관계를 표현한다. 이런 응용 방향을 안다고 각 응용 algorithm까지 이미 배운 것은 아니다.

**점검 기준:** 연속 현상과 계산에 쓰는 유한 표현을 구분하고, 정의에서 관계를 분석한다는 목적을 설명한다.

</details>

#### 확인 Q02 · Proposition과 다섯 연산

1+1=2와 정확한 등식 2π=6.28은 각각 proposition인가? (p,q)=(T,T),(T,F),(F,T),(F,F) 순서로 ¬p, p∧q, p∨q, p→q, p↔q의 값을 구하고 implication의 역방향도 같은지 판정하라.

<details><summary>해설 보기</summary>

두 문장 모두 진리값을 갖는 proposition이며 각각 참, 거짓이다. π의 근삿값을 정확한 등식과 혼동하면 안 된다.

| (p,q) | ¬p | p∧q | p∨q | p→q | p↔q |
|---|---|---|---|---|---|
| T,T | F | T | T | T | T |
| T,F | F | F | T | F | F |
| F,T | T | F | T | T | F |
| F,F | T | F | F | T | T |

p→q는 약속한 전제 p가 참인데 q가 실패할 때만 거짓이다. (T,F)에서 q→p는 참이므로 방향을 뒤집으면 다른 식이다. 모든 행이 같은지 확인해야 logical equivalence를 말할 수 있다.

**점검 기준:** 거짓 문장도 proposition이며, 전제가 거짓인 두 행의 implication은 참이다.

</details>

#### 확인 Q03 · Boolean 값과 modulo 2

T=1,F=0으로 놓을 때 AND, XOR, NOT을 modulo 2 연산으로 표현하라. OR까지 덧셈으로 바꾸는 주장을 반례로 검토하라.

<details><summary>해설 보기</summary>

AND는 pq mod 2, XOR는 (p+q) mod 2, NOT은 (1+p) mod 2다. 특히 p=q=1이면 modulo 2 합은 0이지만 OR는 1이다. 같은 두 값 {0,1}을 쓴다는 사실만으로 모든 연산이 일치하지 않는다.

**점검 기준:** 각 대응을 구분하고 1,1에서 OR와 XOR의 결과를 모두 쓴다.

</details>

#### 확인 Q04 · Witness·counterexample·선택 순서

정수에서 ∃x(x²=4), ∀x(x²=4)의 진리값을 근거와 함께 말하라. ∃x(x²=2)는 실수와 정수에서 어떻게 다른가? 정수에서 ∀x∃y(y=x+1)과 ∃y∀x(y=x+1)는 같은가?

<details><summary>해설 보기</summary>

첫 존재문은 x=2로 참이고 전칭문은 x=0에서 실패하여 거짓이다. 한 witness가 전체 domain의 증명이 되지는 않는다. x²=2는 실수에서 √2를 택할 수 있지만 정수에서는 1²<2<2²이고 음수 제곱도 같으므로 해가 없다.

∀x∃y에서는 x를 받은 뒤 y=x+1을 고르므로 참이다. ∃y∀x에서는 하나의 y가 x=0일 때 1, x=1일 때 2여야 하므로 불가능하다. 선택 순서와 domain이 모두 의미를 바꾼다.

**점검 기준:** 존재와 전칭을 각각 확인하고, 고정된 y와 x에 따라 달라지는 y를 구별한다.

</details>

#### 확인 Q05 · √2의 귀류법

√2=p/q가 기약분수라고 가정한 증명을 완성하라. p²가 짝수이면 p도 짝수인 이유와 마지막 모순을 포함하라.

<details><summary>해설 보기</summary>

q≠0인 기약분수를 가정하면 p²=2q²다. 홀수 2k+1의 제곱은 4k(k+1)+1로 홀수이므로 p²가 짝수일 때 p는 짝수다. p=2k를 대입하면 q²=2k²여서 같은 이유로 q도 짝수다. 따라서 p,q가 공통인수 2를 갖는데, 이는 기약이라는 처음 조건과 모순이다. 가정을 버려 √2가 무리수임을 얻는다. 임의의 분수였다면 둘 다 짝수라는 사실만으로는 모순이 아니다.

**점검 기준:** 기약·q≠0 조건, 홀수 제곱 논증, p와 q의 짝수성, 기약 조건과의 충돌을 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 조건식의 오류를 경계에서 찾기

**새로 만든 synthetic 연습.** [EX:dm_2022_2_mid_q01 p.1] (a)–(b)의 식 평가·경계 확인을 옮겼다. 선수내용은 본문의 AND·OR·NOT뿐이며 원문 문항을 재현하지 않는다.

세 경보 p,q,r 중 정확히 두 개가 켜질 때 참인 식을 만들라. 후보 E=(p∧q)∨(q∧r)∨(r∧p)가 충분한지 검토하고, 켜진 개수 0,1,2,3별로 수정한 식을 확인하라.

<details><summary>해설 보기</summary>

E는 적어도 한 쌍이 함께 켜졌는지를 검사하므로 셋 다 켜진 경우에도 참이다. 따라서 F=E∧¬(p∧q∧r)로 수정한다. 켜진 수 0 또는 1에서는 E가 거짓, 2에서는 E가 참이고 세 변수의 AND가 거짓, 3에서는 뒤의 NOT 항이 거짓이다. 결과는 차례로 F,F,T,F다. 개수별로 묶어도 모든 배치를 포괄하는 이유는 식이 세 변수에 대칭이기 때문이다.

**점검 기준:** 셋 다 참인 반례와 수정 조건을 제시하고 네 경계 경우를 모두 확인한다.

</details>

#### 연습 P02 · Domain을 바꿨을 때의 존재

**새로 만든 synthetic 연습.** [EX:dm_2022_2_mid_q02 p.1]의 domain·witness·예외 확인을 옮겼다. 기초 정수 곱셈과 quantifier만 사용한다.

x,y가 정수일 때 ∀x∃y(xy=0)를 판정하라. y만 홀수 정수로 제한하면 어떻게 바뀌는가? 이를 풀면서 양변을 x로 나누어도 되는지 설명하라.

<details><summary>해설 보기</summary>

원래 문장은 모든 정수 x에 y=0을 택하면 xy=0이므로 참이다. y를 홀수로 제한하면 x=1에 대해 1·y=0을 만족하는 홀수 y가 없어 거짓이다. x=0에서는 어떤 y도 곱이 0이므로, 모든 x를 다루는 풀이에서 x로 무조건 나누면 바로 이 경우를 잃는다.

**점검 기준:** 원래의 모든 x에 통하는 witness, 변경된 domain의 반례, x=0의 소거 금지를 각각 적는다.

</details>

### 짧은 복습 계획

먼저 Q02의 표와 Q04의 witness·counterexample을 해설 없이 작성한다. 다음에 Q05에서 모순이 되는 두 조건을 표시하고 P01–P02를 푼다. 다음 복습에서는 틀린 진리표 행이나 빠뜨린 domain 조건만 다시 설명한 뒤 [[courses/discrete_mathematics/units/sets-functions-sequences|Sets와 Functions]]로 이어 간다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-02-lecture-01|2026-09-02 이산수학 강의·자료 연결]]

[00. Introduction.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/00.Introduction.pdf) · 페이지별 보기: [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-007), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/00.introduction/page-014)

[[courses/discrete_mathematics/transcripts/2026-09-02|2026-09-02 보정 STT]] · 31:01, 36:32, 37:59, 39:54.

2026-09-02의 빠른 개념 복습에 해당한다. √2 증명의 상세 계산은 강의에서 짧게 언급한 예를 풀어 쓴 해설이며, rules of inference의 전체 체계를 강의한 것으로 확대하지 않는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

기출 연결: [[exam_questions/dm_2022_2_mid_q01|2022-2 중간 Q1]]의 (a)–(b)는 식 평가와 경계 조건 확인에 연결한다. [EX:dm_2022_2_mid_q01 p.1] [[exam_questions/dm_2022_2_mid_q02|2022-2 중간 Q2]]는 정수 domain과 quantifier 순서, 소거 전 예외 확인에 연결한다. [EX:dm_2022_2_mid_q02 p.1] 두 연결에는 본문의 논리 연산과 기초 정수식만 사용하며, 원문의 floor 항목이나 별도 추론규칙 증명은 포함하지 않는다.


---

[[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/sets-functions-sequences|다음: Sets·Functions·Sequences로 구조 표현하기 →]]
