---
title: "Algorithmic Paradigms·Greedy와 계산 가능성"
description: "Greedy의 계산·교환 논증과 Turing machine·Halting Problem의 한계를 복습한다."
course: "discrete_mathematics"
unit_id: "paradigms-greedy-and-computability"
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

설계 방식과 최적화의 목적을 분리하고, 선택 규칙이 무엇을 보존하는지 확인한다. Greedy의 정당성과 계산 자체의 가능성은 각각 증명과 반례로 따져 보자.

## Algorithmic paradigm과 optimization model

[[courses/discrete_mathematics/units/algorithms-search-and-sort|검색·정렬 algorithm]]의 구체적인 지시에서 한 단계 물러나면 여러 문제에 재사용되는 설계 방식이 보인다. Algorithmic paradigm(알고리즘 설계 패러다임)은 그런 일반적인 접근이다. Brute-force(직접 탐색)는 특별한 구조를 활용하지 않고 후보를 직접 확인하며 Linear Search가 한 예다. Divide-and-conquer(분할 정복)는 문제를 작은 문제들로 나누는 관점이다. [이산수학 M005 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)는 Greedy, Probabilistic, Dynamic programming, Backtracking도 소개한다. 이름이 소개된 모든 방식의 구체 algorithm을 여기서 배운 것은 아니다.

이 분류는 서로 겹치지 않는 칸들이 아니다. Deterministic algorithm(결정적 알고리즘)은 입력과 초기 상태가 같으면 같은 실행을 한다. Probabilistic algorithm(확률적 알고리즘)은 random choices(무작위 선택)에 따라 실행 경로나 결과가 달라질 수 있다. 따라서 divide-and-conquer이면서 probabilistic일 수도 있다. Random choices가 있다는 이유만으로 답이 틀린다는 뜻은 아니며 correctness(정확성)는 별도로 따진다.

Optimization problem(최적화 문제)은 resource constraint(자원 제약)를 지키는 feasible solution(가능해) 중 objective function(목적함수)을 가장 좋게 만드는 것을 찾는다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 32:08–32:57]]은 100시간을 다섯 과목에 배분하여 결과를 최대화하는 예를 들었다. 이를 수식으로 정리하면

$$t_i\ge0,\qquad \sum_{i=1}^{5}t_i\le100,\qquad \text{maximize }G(t_1,\ldots,t_5)$$

처럼 쓸 수 있다. 하지만 각 과목에서 시간에 따라 결과가 어떻게 달라지는지, 전체 목표에 어떻게 반영되는지를 알아야 최적 배분을 계산할 수 있다. 총시간과 과목 수만으로 20시간씩 나누는 방법의 최적성을 보장할 수 없다. 이 수식은 강의의 동기를 정리한 것이며, 구체적인 $G$나 Dynamic programming의 recurrence가 제공된 예는 아니다.

## Greedy choice와 전체 최적해

Greedy algorithm(탐욕 알고리즘)은 현재 단계에서 가장 좋다고 정한 선택을 반복한다. 어떤 의미에서 “좋은가”가 명확해야 하며, local optimum(국소 최적)과 global optimum(전역 최적)은 다르다. 첫 선택이 좋아 보여도 나중의 좋은 선택을 막을 수 있다.

Greedy-choice property(탐욕 선택 성질)는 해당 선택과 양립하는 최적해가 있음을 보이는 데 쓰인다. Optimal substructure(최적 부분구조)는 선택 뒤에 남은 문제도 적절히 최적으로 풀어 전체 해로 이어갈 수 있다는 성질이다. 이산수학 M005 PDF pp.19,25의 두 조건을 말하는 것만으로는 증명이 끝나지 않는다. 실제 문제에서 왜 성립하는지 보여야 한다.

### Coin change의 계산과 반례

Coin change(동전 거스름돈)의 목표를 동전 개수 최소화로 두자. Greedy rule은 남은 금액을 넘지 않는 가장 큰 동전을 고르는 것이다. M005 PDF p.20의 액면가 25, 10, 5, 1 cents에서 67 cents를 처리하면

$$67\to42\to17\to7\to2\to1\to0$$

이므로 $25+25+10+5+1+1$의 여섯 동전을 사용한다. 자료는 이 체계와 50, 100을 추가한 체계의 최적성을 진술한다. 그러나 액면가가 바뀌면 결론도 달라진다. 25, 10, 1만 있을 때 31 cents에 Greedy를 적용하면 25 하나와 1 여섯 개로 일곱 동전이 필요하다. 반면 $10+10+10+1$은 네 동전이므로 Greedy가 최적이 아니다. 한 반례만으로도 “모든 액면가 체계에서 최적”이라는 주장은 무너진다.

[[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 38:45]]는 원래 체계에서 Greedy보다 quarter를 적게 쓰는 경쟁 조합과 비교하라는 exchange argument(교환 논증)의 방향을 제시했다. 작은 동전들을 같은 금액의 더 적은 동전으로 바꿀 수 있다면 그 경쟁 조합은 최적일 수 없다. 예를 들어 자료의 액면가를 사용한 해설용 교환 $10+10+5\to25$는 금액을 유지하면서 세 동전을 하나로 줄인다.

다만 이 한 교환이 모든 경쟁 조합을 처리한다는 증명은 아니다. 어떤 조합에서도 필요한 교환이 가능한지와 다음 액면가에서의 비교가 더 필요하다. 실제 발화는 그 단계별 비교를 완성하지 않았고 액면가에도 25,15,1처럼 읽히는 불확실성이 있다. 위 계산은 명확한 자료의 25,10,5,1을 사용한 것이며, 생략된 증명을 실제 강의로 덧붙인 것은 아니다.

## Interval scheduling과 earliest finish

Interval scheduling(구간 일정 배정)에서는 한 강의실에 가능한 한 많은 talks를 넣는다. 각 talk는 시작부터 끝까지 중단 없이 진행하고 서로 겹치면 안 된다. 한 talk가 끝나는 시각에 다음 talk가 시작하는 것은 허용한다. 목표는 총 사용 시간이나 가중치 합이 아니라 talk의 개수다.

Earliest-start(가장 이른 시작) rule은 긴 talk 하나가 이후 여러 talk를 막을 수 있어 실패한다. Shortest-duration(가장 짧은 길이) rule도 충분하지 않다. 이산수학 M005 PDF p.23의 세 구간을 보자.

| Talk | 시작 | 종료 | 길이 |
|---|---|---|---:|
| 1 | 8:00 | 9:45 | 105분 |
| 2 | 9:00 | 10:00 | 60분 |
| 3 | 9:45 | 11:00 | 75분 |

가장 짧은 Talk 2를 고르면 다른 두 구간과 모두 겹쳐 한 개만 넣는다. Talk 1과 3을 고르면 9:45 경계에서 이어져 두 개를 넣는다. 원본 그림은 세 talk의 시작·종료 시각을 적은 상자들로 이 충돌을 보여 준다. 길이만 최소화해서는 이후 남는 기회를 판단할 수 없다.

올바른 rule은 earliest finish(가장 이른 종료)다. M005 PDF p.24의 절차는 종료 시각으로 정렬한 뒤 compatible(양립 가능한) talk를 차례로 추가한다.

```text
procedure schedule(s1, ..., sn: start times, e1, ..., en: end times)
    sort talks by finish time so that e1 <= ... <= en
    S := empty set
    for j := 1 to n
        if talk j is compatible with S then
            S := S union {j}
    return S
```

선택한 마지막 talk의 종료 이후에 시작하는지 확인하면 다음 후보의 compatibility를 판단할 수 있다. 위 예에서는 Talk 1이 가장 먼저 끝나고, 그 뒤 Talk 3이 가능하다.

왜 종료 시각이 중요한지 exchange로 설명할 수 있다. 어떤 최적 일정의 첫 talk를 전체에서 가장 일찍 끝나는 talk로 바꾸자. 새 첫 talk가 더 늦게 끝나지 않으므로 기존 뒤쪽 talk들을 그대로 둘 수 있다. 첫 선택을 이렇게 맞춘 뒤 남은 구간에도 같은 논리를 적용한다. 이것은 이해를 위해 전개한 논증이다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 47:58]]에서는 formal proof를 생각해 보도록 미뤘고, [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 01:57]]에는 최적성의 복습이 확인된다. 목적을 가중치 합으로 바꾸거나 방을 두 개로 늘리면 이 증명이 그대로 적용되는지 다시 검토해야 한다.

## Turing machine과 유한한 계산의 기술

Algorithm을 수학적으로 논하려면 “컴퓨터가 할 수 있는 일”도 모델로 표현해야 한다. Turing machine(튜링 기계)은 tape(테이프)에 적힌 기호를 읽고 쓰며, 현재 위치를 왼쪽 또는 오른쪽으로 옮기고, state(상태)와 읽은 기호에 따라 정해진 규칙을 실행하는 모델이다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 51:32–54:37]]의 설명은 이 구성요소들이 계산을 단순한 기계적 단계로 표현한다는 데 초점이 있다.

각 정수를 64 bits로 표현할 수 있다고 가정하면 $n$개의 정수는 $64n$ bits로 encoding(부호화)할 수 있다. Sorting의 출력은 같은 수들을 정렬한 encoding이다. 64 bits는 이 예의 고정 폭 가정이지 모든 정수의 길이가 아니다. 더 큰 정수를 허용하면 표현 길이도 늘어난다.

유한한 규칙 집합이 있다고 실행 단계 수도 유한한 것은 아니다. 같은 규칙을 끝없이 반복할 수 있기 때문이다. Probabilistic computation은 별도의 random tape에서 기호를 읽어 선택에 사용하는 것으로 설명할 수 있다. 일반 입력이 같아도 random tape가 달라지면 실행이 달라진다. 반대로 일반 입력, 초기 상태, random tape까지 고정하면 다음 행동은 규칙에 따라 결정된다. 실제 판서 배치나 formal machine tuple을 가정하지 않아도 이 차이는 이해할 수 있다.

## Halting Problem과 solvability의 한계

Solvability(계산 가능성)는 허용된 모든 입력에 대해 유한 시간 안에 정답을 내는 algorithm이 존재하는지를 묻는다. Efficiency(효율성)는 그런 algorithm이 얼마나 많은 자원을 쓰는지를 묻는다. 오래 걸리는 문제와 일반적인 해결 algorithm이 없는 문제는 다르다.

Halting Problem(정지 문제)은 program $P$와 input $I$를 받아 $P(I)$가 언젠가 종료하는지 항상 판정하는 문제다. 직접 실행해 기다리면 종료하는 경우는 알아낼 수 있다. 하지만 끝없이 실행되는 경우에는 “아직 안 끝났다”는 관찰만 계속될 뿐, 유한 시간 안에 결론을 얻지 못한다.

이산수학 M005 PDF p.27의 [[courses/discrete_mathematics/units/logic-and-proof|contradiction 논증]]을 따라가자. 항상 종료하면서 정확하게 판정하는 $H(P,I)$가 있다고 가정한다. Program도 문자열로 encoding할 수 있으므로 $H(P,P)$라는 입력을 줄 수 있다. 이 가정 아래 다음 $K$를 만든다.

```text
procedure K(P)
    if H(P, P) outputs "loops forever" then halt
    else loop forever
```

이제 $K(K)$를 생각한다.

| $H(K,K)$의 예측 | $K(K)$의 정의에 따른 행동 | 결과 |
|---|---|---|
| 종료한다 | 무한히 반복한다 | 예측과 모순 |
| 무한히 반복한다 | 종료한다 | 예측과 모순 |

가능한 예측 둘 다 실패하므로 그런 보편적인 $H$는 없다. 여기서 `"loops forever"`는 $H$가 유한 시간 안에 내는 판정 문구다. $H$ 자신이 멈추지 않는다는 뜻으로 읽으면 가정이 달라진다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 01:01:50]]의 논증과 [[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 STT 02:24]]의 복습이 다루는 한계도 이것이다. 특정 program의 종료를 전혀 증명할 수 없다는 결론이 아니라, 모든 program과 input을 처리하는 판정기의 불가능성이다.

## 핵심 정리

- Paradigm은 겹칠 수 있는 설계 관점이며 random choice와 correctness는 별개의 문제다.
- Greedy의 local choice가 전체 최적이라는 결론에는 해당 목적·제약에서의 논증이 필요하다.
- Earliest finish는 한 방에서 무가중치 talk 개수를 최대화하는 목적에 맞춘다.
- 유한 규칙은 무한 실행을 만들 수 있다. Halting 불가능성은 모든 program-input을 처리하는 보편 판정기에 관한 주장이다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Paradigm과 optimization 명세

Brute-force·divide-and-conquer·probabilistic이라는 말이 서로 배타적인가? Deterministic 실행과 random choices를 구별하라. 100시간을 다섯 과목에 배분한다는 정보만으로 최적 배분을 계산할 수 있는가?

<details><summary>해설 보기</summary>

Brute-force는 후보를 직접 확인하는 방식이고 Linear Search가 예다. Divide-and-conquer는 문제를 나누는 방식이며 probabilistic은 random choices를 쓰는지에 관한 관점이라 함께 적용될 수 있다. Deterministic 실행은 입력·초기 상태가 같으면 같고, probabilistic 실행은 random choice에 따라 달라질 수 있다. Random을 쓴다고 정답이 반드시 틀리는 것은 아니다.

시간 배분은 tᵢ≥0,Σᵢ₌₁⁵tᵢ≤100이라는 제약만 준다. 최대화할 G(t₁,…,t₅), 즉 과목별 시간–결과 관계와 합산 방식이 있어야 배분을 비교한다. 이를 모르면 균등 20시간씩이 최적이라는 보장도 없고 구체 DP 해법도 정해지지 않는다.

**점검 기준:** 설계 관점의 중첩, 실행 재현성, constraint와 objective function의 역할을 모두 설명한다.

</details>

#### 확인 Q02 · Coin Greedy와 반례

남은 금액 이하의 가장 큰 coin을 고르는 규칙으로 25,10,5,1에서 67 cents를 처리하라. 25,10,1만 있을 때 31 cents는 왜 반례인가? Greedy-choice property와 optimal substructure의 역할도 말하라.

<details><summary>해설 보기</summary>

67→42→17→7→2→1→0으로 25,25,10,5,1,1의 여섯 개를 쓴다. 25,10,1에서 31은 25 뒤에 1 여섯 개를 써 일곱 개지만, 10+10+10+1은 네 개라 Greedy가 최적이 아니다. Greedy-choice property는 최적해와 양립하는 첫 선택을 정당화하고 optimal substructure는 남은 문제의 최적해를 전체에 이어 주는 데 쓰인다. 이름만 제시해서는 그 체계에서 두 성질이 성립한다는 증명이 되지 않는다.

**점검 기준:** 잔액 trace·동전 수를 계산하고 액면가 조건과 global optimum의 차이를 설명한다.

</details>

#### 확인 Q03 · Coin exchange가 아직 증명이 아닌 이유

원래 25,10,5,1 체계에 대한 부분적 exchange 제안은 어떤 경쟁 조합을 비교하는가? 10+10+5→25가 보존·감소시키는 것을 말하고, 이 교환 하나로 전체 최적성이 증명되는지 판정하라.

<details><summary>해설 보기</summary>

Greedy가 쓰는 최대 quarter 수보다 quarter를 적게 쓴 경쟁 조합을 생각하고 작은 동전을 더 적은 수로 바꿀 수 있는지 비교한다. 10+10+5→25는 금액 25를 보존하며 동전 수를 3에서 1로 줄인다. 그런 개선이 가능한 경쟁 해는 최적이 아니다. 하지만 모든 경쟁 조합에서 필요한 교환이 가능한지, 남은 액면가 단계도 처리되는지는 별도로 보여야 한다. 따라서 한 예나 강의의 부분적 제안만으로 모든 경우의 최적성 증명이 완성되지는 않는다.

**점검 기준:** 비교 대상, 보존량, 감소량, 남은 경우 분석을 명시한다.

</details>

#### 확인 Q04 · Earliest-finish의 실행과 교환

Talk 1=8:00–9:45, Talk 2=9:00–10:00, Talk 3=9:45–11:00에서 earliest-finish를 실행하라. Shortest-duration과 earliest-start가 일반적으로 실패하는 이유, earliest-finish의 교환 논증을 설명하라.

<details><summary>해설 보기</summary>

종료 순서 1,2,3에서 1을 고르고 2는 겹쳐 건너뛰며 3은 9:45에 바로 이어지므로 고른다. 끝과 다음 시작이 같아도 compatible하다. 가장 짧은 2를 고르면 다른 둘을 모두 막아 하나만 남는다. Earliest-start도 예컨대 0–10의 긴 talk를 먼저 택하면 1–2와 2–3을 함께 택할 기회를 잃는다.

어떤 최적 일정의 첫 talk를 가장 먼저 끝나는 talk로 바꿔도 종료가 늦어지지 않아 뒤의 talks를 유지할 수 있다. 첫 선택 후 남은 구간에도 같은 논리를 적용한다. 목표는 한 방의 talk 개수이므로 가중치나 총 사용시간에 같은 결론을 옮길 수 없다.

**점검 기준:** 실제 선택과 경계 equality, 두 실패 규칙, 첫 talk 교환이 뒤를 보존하는 이유를 설명한다.

</details>

#### 확인 Q05 · Turing machine의 한 step

Tape·state·read/write·movement가 한 step에서 어떻게 연결되는가? n개의 정수를 64n bits로 표현한다는 가정과 random tape의 역할을 설명하고, 유한 규칙이면 실행도 유한한지 말하라.

<details><summary>해설 보기</summary>

현재 state와 읽은 symbol에 맞는 규칙이 쓸 symbol, 다음 state, 이동 방향을 정한다. 이 규칙들을 반복해 계산한다. 각 정수가 64 bits에 표현된다는 고정 폭 가정 아래 n개가 64n bits이며 임의 크기 정수가 항상 64 bits라는 뜻은 아니다. Random tape는 random choices를 공급하여 일반 input이 같아도 실행을 달라지게 할 수 있다. Input·초기 상태·random tape까지 고정하면 실행은 규칙대로 정해진다. 같은 규칙으로 계속 돌아갈 수 있어 유한한 description도 무한 실행을 만들 수 있다.

**점검 기준:** 기계의 구성요소를 행동과 연결하고 64-bit 가정·random tape 고정 여부·종료의 차이를 구분한다.

</details>

#### 확인 Q06 · Halting 판정기의 자기입력

Solvability와 efficiency의 차이를 말하라. 항상 종료하며 정확히 판정하는 H(P,I)를 가정하고 H(P,P)의 예측을 반대로 수행하는 K를 만들었을 때 K(K)의 두 경우를 설명하라. 단순히 실행해 기다리면 왜 해결되지 않는가?

<details><summary>해설 보기</summary>

Solvability는 모든 허용 입력에 유한 시간 안에 정답을 주는 algorithm의 존재, efficiency는 그 자원 요구량이다. H가 K(K)를 종료한다고 예측하면 K는 정의상 무한 반복한다. H가 무한 반복한다고 판정하면 K는 종료한다. 두 경우 모두 정확성 가정과 모순이다. Program도 문자열로 표현할 수 있어 자기입력이 가능하다. H의 '무한 반복'은 유한 시간에 낸 판정이지 H 자신이 멈추지 않는다는 뜻이 아니다.

직접 실행은 종료하는 경우를 발견하지만 끝나지 않는 경우 '아직 안 끝남'만 관찰하여 항상 유한 시간에 판정하지 못한다. 결론은 보편 판정기의 부재이며 특정 program의 종료를 증명할 수 없다는 뜻은 아니다.

**점검 기준:** 두 예측을 모두 뒤집어 모순을 보이고, 보편성·H의 종료 가정·기다리기의 한계를 보존한다.

</details>

### 적용 연습

#### 연습 P01 · 목적을 바꾼 일정

**새로 만든 강의 기반 일반 연습.** 한 방의 earliest-finish에 직접 맞는 기출 후보가 없고 두 방 weighted DP는 추가 내용이므로 그 유형을 주장하지 않는다. 선수내용은 interval compatibility와 objective function이다.

A=[0,6], B=[0,2], C=[2,4], D=[4,6]이며 끝과 시작이 같은 것은 허용한다. 개수를 최대화하는 일정과, A의 가중치 10·나머지 각각 3일 때 합을 최대화하는 일정을 비교하라. 기존 교환 논증의 어느 부분으로 두 번째 최적성을 보장할 수 없는가?

<details><summary>해설 보기</summary>

Earliest finish는 B,C,D를 택해 3개를 얻는다. A는 다른 세 talk와 모두 겹쳐 A를 택하면 하나뿐이다. 개수 목적에서는 B,C,D가 최적이다. 가중치 목적에서는 B,C,D의 합은 9이고 A 하나가 10이므로 A가 최적이다. A가 없는 모든 일정은 세 짧은 talk의 일부라 9 이하이므로 이 비교로 충분하다. 첫 talk를 더 일찍 끝나는 것으로 바꾸면 뒤의 자리는 보존해도 가중치가 보존되지는 않는다.

**점검 기준:** 두 목적의 최적해·값·다른 경우의 상한을 제시하고 교환 시 가중치 손실을 설명한다.

</details>

### 짧은 복습 계획

Q01에서 목적과 제약을 분리한 뒤 Q02–Q04의 성공·실패 예를 그린다. Q05의 유한 기술과 Q06의 보편 판정 불가능성을 연결하되 혼동하지 않는다. P01에서는 목적만 바꿨을 때 기존 증명의 어느 전제가 사라지는지 표시한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 이산수학 강의·자료 연결]] · [[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 이산수학 강의·자료 연결]]

[02. Algorithms.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf) · 페이지별 보기: [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-027)

[[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 보정 STT]] · 31:12, 32:08, 32:57, 37:48, 38:45, 40:32, 47:58, 51:32, 54:37, 01:01:50.

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 보정 STT]] · 02:24, 01:57.

2026-09-09의 설명과 2026-09-14의 짧은 복습을 연결한다. Coin 체계는 자료의 25,10,5,1을 사용하되 불명확한 액면가 발화를 없애지 않는다. Coin exchange는 부분적 제안이고 interval scheduling의 formal proof도 강의에서는 미뤘다. 여기서 쓰는 교환 논증은 본문의 해설이다. 실제 tape 판서, 완전한 machine tuple, DP recurrence는 공급되지 않았다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

현재 coin exchange, 한 방의 earliest-finish, tape/random tape, Halting contradiction에 직접 일치하는 기출 후보가 없다. 두 방의 weighted scheduling은 DP state가 더 필요하고 P/NP·recursive tiling 역시 별도 선수내용이므로 일반 연습으로 한정한다.


---

[[courses/discrete_mathematics/units/algorithms-search-and-sort|← 이전: Algorithm 명세와 Searching·Sorting의 실행]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|다음: Asymptotic Analysis와 Cost Model →]]
