---
title: "Algorithm 명세와 Searching·Sorting의 실행"
description: "Fibonacci, maximum, 검색과 정렬을 상태 추적과 invariant로 확인한다."
course: "discrete_mathematics"
unit_id: "algorithms-search-and-sort"
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

Input과 반환 규약을 정한 뒤 변수와 구간이 어떻게 변하는지 추적한다. 알고리즘 이름보다 실제 comparison·assignment 순서를 기준으로 실행과 정확성을 설명하자.

## Algorithm 명세와 pseudocode의 상태

Algorithm(알고리즘)을 읽기 전에 input(입력)과 output(출력)을 정해야 한다. 정수 덧셈은 두 정수에서 합을, 행렬곱은 크기가 맞는 두 행렬에서 그 곱을, maximum 문제는 비어 있지 않은 sequence에서 가장 큰 값을 요구한다. [이산수학 M005 PDF pp.3–5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)는 이런 유효한 입력을 원하는 출력으로 바꾸는 정확한 지시를 algorithm으로 소개한다. 유한한 길이로 절차를 적을 수 있다는 사실과 모든 입력에서 실행이 끝난다는 사실은 따로 확인해야 한다.

Pseudocode(의사코드)는 구현 언어보다 계산의 순서를 드러내기 위한 표기다. 자료의 Rosen style `:=`, CLRS style `←`, programming style `=`는 assignment(대입)다. Programming style의 `==`는 equality comparison(동등 비교)이며, `:`도 type 표시인지 block 시작인지 표기법에 따라 다르다. 기호가 익숙한 언어와 비슷하다고 의미까지 자동으로 옮기지 않는다.

### Fibonacci에서 이전 값을 보존하기

[[courses/discrete_mathematics/units/sets-functions-sequences|Fibonacci recurrence]]의 $f_0=0,f_1=1$과 $f_n=f_{n-1}+f_{n-2}$를 계산하는 M005 PDF p.6의 절차는 다음과 같다. 입력 $n$은 nonnegative integer다.

```text
procedure fibonacci(n: nonnegative integer)
    if n <= 1 then return n
    f1 := 0
    f2 := 1
    for i := 2 to n
        temp := f1 + f2
        f1 := f2
        f2 := temp
    return f2
```

`f1`, `f2`는 이름이 고정되어 있지만 담기는 값은 계속 바뀐다. 반복 직전에 최근 두 Fibonacci 값을 담고, `temp`에 다음 값을 보존한 뒤 한 칸씩 전진한다. $n=5$일 때 상태를 직접 추적하면 다음과 같다.

| 처리 단계 | `f1` | `f2` |
|---|---:|---:|
| 초기 | 0 | 1 |
| $i=2$ | 1 | 1 |
| $i=3$ | 1 | 2 |
| $i=4$ | 2 | 3 |
| $i=5$ | 3 | 5 |

`f1 := f2`부터 실행하고 나서 새 `f1`과 `f2`를 더하면 이전 값 하나를 잃는다. `temp`가 필요한 이유다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 12:44]]에도 최근 두 값을 갱신한다는 설명이 있다. 초기값을 0/1로 말한 불명확한 조각은 자료 pp.6–8의 `f1 := 0`, `f2 := 1`과 구분한다.

2022-2 중간 Q10 중 iterative algorithm 부분은 이런 상태 관리와 정수 덧셈 횟수를 함께 요구한다. 이 code에서 Fibonacci 값끼리 더하는 연산은 $n\ge2$일 때 $n-1$회다. Sequence를 정의하는 recurrence와 algorithm의 연산 횟수를 나타내는 식은 서로 다른 대상이다. Recursive 방식의 별도 분석은 이 연결만으로 배웠다고 간주하지 않는다. [EX:dm_2022_2_mid_q10 p.2]

## Maximum scan과 loop invariant

비어 있지 않은 sequence $a_1,\ldots,a_n$의 maximum을 구할 때는 처음 값을 기준으로 시작한다. M005 PDF p.5의 절차다.

```text
procedure max(a1, ..., an: integers, n >= 1)
    max := a1
    for i := 2 to n
        if max < ai then max := ai
    return max
```

Loop invariant(반복 불변식)는 “$i$번째 원소까지 처리하면 `max`는 $a_1,\ldots,a_i$의 maximum”이다. 첫 원소만 처리했을 때 성립한다. 다음 원소가 기존 maximum보다 크면 교체하고, 그렇지 않으면 유지하므로 한 단계 뒤에도 성립한다. 마지막에는 모든 원소를 처리했으므로 원하는 결과다.

설명용 입력 $(-5,-2,-9)$에서는 `max`가 $-5\to-2\to-2$로 바뀐다. 무조건 0으로 초기화하면 입력에 없는 0을 답으로 남길 수 있다. 초기화는 편의적인 상수가 아니라 invariant의 첫 경우를 만족시키는 선택이어야 한다.

## Linear Search와 반환 규약

Searching(검색)은 목표 $x$와 같은 원소의 위치를 찾거나 없음을 판정한다. 자료는 서로 다른 정수들의 list에 1부터 시작하는 index를 쓰고, 성공하면 위치를, 실패하면 0을 반환한다. Linear Search(선형 검색)는 앞에서부터 하나씩 확인한다.

```text
procedure linear search(x: integer, a1, ..., an: distinct integers)
    i := 1
    while i <= n and x != ai
        i := i + 1
    if i <= n then location := i
    else location := 0
    return location
```

M005 PDF p.9의 조건은 범위를 먼저 검사하는 것으로 읽는다. `i <= n`이 거짓이면 `ai`를 읽지 않아야 한다. 반복 중에는 이미 지나간 위치에 $x$가 없다는 성질을 유지한다. $x=a_i$이면 해당 위치에서 멈추고, 끝까지 없으면 $i=n+1$이 되어 0을 반환한다. 실패 후 $a_{n+1}$을 정상 원소처럼 읽는 해석은 잘못이다.

예를 들어 설명용 list $(4,9,2)$에서 9를 찾으면 첫 비교를 통과한 뒤 $i=2$에서 멈춘다. 7을 찾으면 세 원소가 모두 다르므로 $i=4$에서 범위 조건이 거짓이 된다. Main data comparison만 세면 최악에 $n$회다. Loop-control까지 세는 convention과의 차이는 [[courses/discrete_mathematics/units/search-and-matrix-complexity|검색의 complexity]]에서 계산한다.

## Binary Search와 줄어드는 interval

Binary Search(이진 검색)는 정렬 순서가 있어야 비교 하나로 많은 후보를 버릴 수 있다. $a_1<\cdots<a_n$이고 $n\ge1$이라고 하자. M005 PDF p.12는 inclusive interval(양 끝 포함 구간) $[i,j]$를 남기는 다음 구현을 사용한다.

```text
procedure binary search(x: integer, a1, ..., an: increasing integers)
    i := 1
    j := n
    while i < j
        m := floor((i + j) / 2)
        if x > am then i := m + 1
        else j := m
    if x = ai then location := i
    else location := 0
    return location
```

$x>a_m$이면 $a_1,\ldots,a_m$ 중 어느 것도 답이 아니므로 왼쪽을 버린다. 그렇지 않으면 오른쪽의 $m+1$ 이후를 버리고 $m$은 남긴다. 이 구현은 $x=a_m$이어도 즉시 반환하지 않는다. 끝까지 interval을 하나로 줄인 뒤 마지막 equality를 검사한다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 19:07]]의 설명도 이 반환 방식이다.

M005 PDF p.11의 list는

$$1,2,3,5,6,7,8,10,12,13,15,16,18,19,20,22$$

이다. 여기서 19를 찾는 trace는 다음과 같다.

| 현재 $[i,j]$ | $m$ | $a_m$ | 남기는 interval |
|---|---:|---:|---|
| $[1,16]$ | 8 | 10 | $[9,16]$ |
| $[9,16]$ | 12 | 16 | $[13,16]$ |
| $[13,16]$ | 14 | 19 | $[13,14]$ |
| $[13,14]$ | 13 | 18 | $[14,14]$ |

마지막 $a_{14}=19$를 확인하여 14를 반환한다. 목표와 midpoint가 일치한 셋째 단계에서도 끝나지 않는다는 점을 주의해서 보자. 자료 그림의 붉은 원소들은 각 단계에서 남은 후보 구간이다.

정렬되지 않은 list에는 이런 버리기가 정당하지 않다. 또한 이 code에는 empty list 처리가 별도로 없다. 입력의 전제와 반환 규약을 유지해야 trace와 이후 비용 분석이 일치한다. 검색 전에 필요한 sorting 비용도 검색 자체의 비용과 분리한다.

## Sorting과 정렬되는 구간

Sorting(정렬)은 비교 순서가 정해진 원소들을 그 순서대로 재배열하는 문제다. 숫자뿐 아니라 문자열의 alphabetic order나 record의 key도 기준이 될 수 있다. 입력 크기, 기존 정렬 정도, input distribution, hardware와 software 조건에 따라 적합한 방법이 달라진다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 21:39]]의 선택 논의는 특정 algorithm이 모든 환경에서 최선이라는 주장이 아니다.

### Bubble Sort의 확정된 suffix

Bubble Sort(버블 정렬)는 인접한 원소의 순서가 틀렸으면 서로 바꾼다. M005 PDF p.14의 구현은 왼쪽에서 오른쪽으로 이동한다.

```text
procedure bubblesort(a1, ..., an: real numbers, n >= 2)
    for i := 1 to n - 1
        for j := 1 to n - i
            if aj > a(j+1) then interchange aj and a(j+1)
```

한 pass(순회) 동안 아직 정렬되지 않은 구간의 maximum이 오른쪽 끝까지 이동한다. 따라서 다음 pass에서는 이미 제자리에 있는 suffix(뒷부분)를 제외한다. M005 PDF p.15의 예를 끝까지 따라가면 다음과 같다.

| 단계 | 배열 | 새로 확정되는 값 |
|---|---|---:|
| 시작 | $7,3,5,2,6$ | — |
| Pass 1 | $3,5,2,6,7$ | 7 |
| Pass 2 | $3,2,5,6,7$ | 6 |
| Pass 3 | $2,3,5,6,7$ | 5 |
| Pass 4 | $2,3,5,6,7$ | 3 |

셋째 pass 뒤 이미 정렬되었어도 이 code에는 조기 종료 검사가 없다. 넷째 pass에서 2와 3을 비교한다. Comparisons는 $4+3+2+1=10$회이며 swaps의 횟수와 같지 않다. “정렬되어 보인다”와 “제시된 code가 종료한다”를 구분해야 한다.

### Insertion Sort의 확장되는 prefix

Insertion Sort(삽입 정렬)는 앞부분이 이미 정렬되어 있다는 성질을 유지하며 새 원소를 넣는다. M005 PDF p.16의 구현은 삽입 위치를 앞에서부터 찾는다.

```text
procedure insertion sort(a1, ..., an: real numbers, n >= 2)
    for j := 2 to n
        i := 1
        while aj > ai
            i := i + 1
        m := aj
        for k := 0 to j - i - 1
            a(j-k) := a(j-k-1)
        ai := m
```

마지막 `for`는 상한이 음수이면 실행하지 않는 counting-loop convention이다. $j$번째 단계 직전에 $a_1,\ldots,a_{j-1}$은 sorted prefix(정렬된 앞부분)다. `while`은 새 값보다 작지 않은 첫 원소에서 멈춘다. 새 값이 가장 크면 $i=j$에서 자기 자신과 비교하여 멈춘다. 이후 `m`에 새 값을 저장하고, 삽입할 자리 뒤의 값들을 오른쪽으로 민다. 뒤에서부터 이동해야 아직 옮기지 않은 값이 덮어써지지 않는다.

M005 PDF p.17의 붉은 테두리는 $[7]\to[3,7]\to[3,5,7]\to[2,3,5,7]\to[2,3,5,6,7]$로 커지는 prefix다. 예를 들어 $[3,5,7]$ 앞부분에 2를 넣을 때 7, 5, 3 순서로 오른쪽에 옮긴 뒤 첫 자리에 2를 넣는다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 28:46]]의 설명도 위치 탐색과 shift(이동)를 나눈다.

이 code의 strict comparison `aj > ai`는 같은 값 앞에서 멈춘다. 따라서 동일 key를 가진 record의 원래 순서를 보존하는 stable(안정적인) variant와 자동으로 같다고 볼 수 없다. 같은 이름의 sorting algorithm이라도 비교 부호와 순회 방향을 확인해야 실제 동작을 알 수 있다.

## 핵심 정리

- 유한한 program description과 모든 입력에서의 종료는 다른 조건이다.
- 덮어쓰기 전의 값을 보존해야 recurrence의 다음 상태를 올바르게 만든다.
- Binary Search의 정렬 전제와 equality 검사 위치가 trace를 결정한다.
- Bubble Sort는 확정된 suffix, Insertion Sort는 확장되는 sorted prefix를 유지한다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · 문제 명세와 pseudocode

유한한 nonempty integer list의 maximum을 구하는 문제의 유효 input, output, 정확한 지시를 말하라. :=, ←, =, ==와 colon은 pseudocode style에 따라 어떻게 읽는가? 유한한 기술이면 항상 종료하는가?

<details><summary>해설 보기</summary>

Input은 적어도 한 원소가 있는 유한 정수 list, output은 그 list의 가장 큰 값이다. 첫 원소를 후보로 놓고 나머지를 순서대로 비교해 더 클 때만 갱신한 뒤 반환한다. Rosen의 :=, CLRS의 ←, programming style의 =는 대입이고 ==는 동등 비교다. Colon은 type 표시 또는 block 시작일 수 있어 해당 style을 확인한다. 이 scan은 유한 list를 끝까지 지나므로 종료하지만, 유한 지시도 무한 반복을 기술할 수 있어 기술 길이만으로 종료는 보장되지 않는다.

**점검 기준:** Input·output·procedure를 구분하고 대입과 비교, 기술의 유한성과 실행의 유한성을 분리한다.

</details>

#### 확인 Q02 · Fibonacci 갱신 순서

자료의 iterative Fibonacci에서 n=0,1의 반환값과 n=5일 때 (f1,f2)의 모든 상태를 쓰라. 왜 temp가 필요하며 Fibonacci 값의 덧셈은 몇 번인가?

<details><summary>해설 보기</summary>

n≤1이면 n을 그대로 반환하므로 0과 1이다. n=5에서는 (0,1)→(1,1)→(1,2)→(2,3)→(3,5)이고 f2=5를 반환한다. 먼저 temp에 이전 두 값의 합을 저장하고 f1을 이전 f2로, f2를 temp로 바꾼다. f1을 먼저 덮어쓰면 이전 f1을 잃는다. i=2,3,4,5의 네 번, 일반 n≥2에는 n−1번의 Fibonacci 값 덧셈이 있다. 이는 loop index 갱신까지 포함한 총 연산 수가 아니다.

**점검 기준:** 기저 입력·네 상태 전이·보존할 이전 값·덧셈의 범위를 정확히 확인한다.

</details>

#### 확인 Q03 · Maximum scan의 invariant

입력 (−5,−2,−9)를 추적하고 max=0 초기화가 실패하는 이유를 말하라. Invariant의 초기·유지·종료 논증과 empty input의 한계도 설명하라.

<details><summary>해설 보기</summary>

첫 원소로 초기화하면 max는 −5→−2→−2로 움직여 −2를 반환한다. max=0이면 모두 0보다 작아 갱신되지 않고 입력에도 없는 0이 남는다. Invariant는 i번째 원소까지 처리한 뒤 max가 그 prefix의 maximum이라는 것이다. 첫 원소에서는 참이고, 새 원소와 비교해 더 큰 것만 남기면 유지된다. 모든 원소를 처리하면 전체 maximum이다. Empty list에는 a₁이 없어 별도 계약이 필요하다.

**점검 기준:** 추적값과 실제 입력 원소 초기화의 이유, invariant의 세 단계 및 빈 입력 한계를 포함한다.

</details>

#### 확인 Q04 · Linear Search의 실패 상태

길이 4의 distinct list에서 목표가 없을 때 loop 종료 i와 반환값은 무엇인가? 범위 검사를 먼저 해야 하는 이유와 성공 위치 2인 경우를 설명하라.

<details><summary>해설 보기</summary>

실패하면 i가 1부터 5까지 증가한 뒤 i≤4가 거짓이 되어 loop를 나온다. 반환값은 0이며 i=5를 성공 index로 반환하지 않는다. 범위가 거짓일 때 a₅를 읽지 않아야 한다. 성공 위치가 2라면 a₁과 다름을 확인하고 i=2에서 match로 멈춰 2를 반환한다. 지나간 위치에는 목표가 없다는 invariant가 유지된다. Main comparison은 실패에 4회다.

**점검 기준:** 종료 상태와 반환 규약을 구분하고 short-circuit 해석과 지나간 구간의 성질을 설명한다.

</details>

#### 확인 Q05 · Binary Search가 남기는 interval

자료의 list (1,2,3,5,6,7,8,10,12,13,15,16,18,19,20,22)에서 19를 찾는 interval과 midpoint를 추적하라. 이미 a₁₄=19를 만났는데 왜 즉시 끝나지 않는가?

<details><summary>해설 보기</summary>

[1,16]의 m=8,a₈=10에서 [9,16]을 남긴다. m=12,a₁₂=16이면 [13,16], m=14,a₁₄=19이면 [13,14], m=13,a₁₃=18이면 [14,14]다. 이 구현은 x>aₘ이면 i=m+1, 아니면 j=m으로 갱신하므로 equality에서도 구간만 줄인다. 마지막 x=a₁₄를 확인해 14를 반환한다. 정렬되어 있어야 버린 쪽에 답이 없음을 보장한다. 비어 있지 않은 list가 전제이며 sorting의 선행 비용은 별도다.

**점검 기준:** 네 midpoint와 구간, 마지막 equality, 정렬·nonempty 전제를 함께 기록한다.

</details>

#### 확인 Q06 · Sorting의 목표와 선택

Sorting은 숫자에만 쓰이는가? 같은 문제를 푸는 한 algorithm이 모든 실제 데이터와 환경에서도 가장 좋다고 할 수 없는 이유를 설명하라.

<details><summary>해설 보기</summary>

숫자, 문자열의 alphabetic order, record key처럼 비교 순서가 정해진 대상을 그 순서로 재배열한다. 기존 정렬 정도, 크기, input distribution, hardware·software와 세는 operation이 달라지면 장점도 달라질 수 있다. 일반 입력에서의 분석이 일부 정렬된 실제 데이터의 최선 선택을 자동으로 정하지 않는다.

**점검 기준:** 비교 기준을 정하고 입력 구조·분포·환경을 근거로 선택이 달라짐을 설명한다.

</details>

#### 확인 Q07 · Bubble Sort의 마지막 pass

자료의 7,3,5,2,6을 pass별로 적고 확정되는 구간을 설명하라. 이미 정렬된 뒤에도 비교가 남는가? 전체 adjacent comparison 수와 swaps가 같은가?

<details><summary>해설 보기</summary>

Pass 뒤 배열은 차례로 3,5,2,6,7 → 3,2,5,6,7 → 2,3,5,6,7 → 2,3,5,6,7이다. 각 pass에서 남은 prefix의 maximum이 오른쪽 끝으로 이동하여 suffix가 하나씩 확정된다. 이 code에는 조기 종료가 없어 네 번째 pass의 2,3 비교도 한다. 비교 수는 4+3+2+1=10이고, swaps는 4+1+1+0=6이다. 비교가 참일 때만 swap하기 때문이다.

**점검 기준:** 확정 suffix와 네 번째 pass, 비교 10회와 swap 6회를 구별한다.

</details>

#### 확인 Q08 · Insertion Sort의 이동과 동률

Sorted prefix [3,5,7]에 새 값 2를 넣는 순서를 말하라. 자료의 while `aj > ai`는 새 값이 가장 크거나 같은 key가 있을 때 어디서 멈추며 stability를 보장하는가?

<details><summary>해설 보기</summary>

먼저 위치 i=1을 찾고 2를 m에 보존한다. 7,5,3 순서로 뒤에서부터 오른쪽으로 옮긴 뒤 a₁=2를 써 [2,3,5,7]을 만든다. 앞에서부터 옮기면 아직 이동하지 않은 값을 덮을 수 있다. 새 값이 가장 크면 i=j에서 자기 자신과의 strict comparison이 거짓이 되어 멈추고 shift는 없다. 같은 key에서는 기존 같은 값 앞에서 멈춰 새 record가 먼저 들어가므로 원래 순서를 보존하는 stable variant라고 할 수 없다. 매 단계 후 prefix가 정렬된다는 성질은 유지된다.

**점검 기준:** 저장·뒤쪽부터 shift·자기 비교 종료·동일 key 순서의 네 사항을 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 상태를 잃는 구현 고치기

**새로 만든 synthetic 연습.** [EX:dm_2022_2_mid_q10 p.2]의 iterative 상태 관리와 덧셈 count를 옮겼다. 선수내용은 본문의 recurrence·대입 순서이며 recursive 분석은 요구하지 않는다.

초기값 f1=0,f2=1 뒤 i=2,…,n에서 `f1 := f2` 다음 `f2 := f1 + f2`를 실행하는 구현이 있다. n=4의 반환값을 구하고 올바른 Fibonacci와 비교하라. 변수 하나를 추가하여 고친 뒤, 덧셈 횟수가 원래 잘못된 code와 같아도 correctness가 달라지는 이유를 설명하라.

<details><summary>해설 보기</summary>

잘못된 전이는 (0,1)→(1,2)→(2,4)→(4,8)이므로 8을 반환하며 f₄=3과 다르다. 갱신 전에 `temp := f1 + f2`를 계산하고 `f1 := f2`, `f2 := temp` 순서로 바꾸면 (0,1)→(1,1)→(1,2)→(2,3)이 된다. 두 구현 모두 이 입력에서 값의 덧셈을 세 번 하지만, 잘못된 구현은 이전 f1을 버리고 이전 f2를 두 번 더한다. 같은 operation count는 같은 값을 계산한다는 증거가 아니다.

**점검 기준:** 오류 trace와 수정 trace를 모두 계산하고, count와 correctness의 독립성을 설명한다.

</details>

### 짧은 복습 계획

Q01에서 명세를 쓰고 Q02·Q03의 변수값을 표로 추적한다. Q04·Q05는 실패 입력도 확인한 뒤 Q07·Q08의 suffix와 prefix를 표시한다. P01에서 수정한 갱신 순서를 다시 실행하고 [[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|비용 모형]]으로 넘어간다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 이산수학 강의·자료 연결]] · [[courses/discrete_mathematics/lectures/2026-09-14-lecture-04|2026-09-14 이산수학 강의·자료 연결]]

[02. Algorithms.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf) · 페이지별 보기: [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-017)

[[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 보정 STT]] · 12:44, 11:48, 15:10, 19:07, 21:39, 25:08, 28:46.

[[courses/discrete_mathematics/transcripts/2026-09-14|2026-09-14 보정 STT]] · 00:58.

2026-09-09의 실제 절차 설명과 2026-09-14의 recap을 함께 연결한다. Fibonacci의 불명확한 초기값 발화는 자료의 f1=0,f2=1과 구분한다. 자료의 Bubble Sort에는 조기 종료가 없고, Insertion Sort는 strict comparison으로 앞에서 삽입 위치를 찾는다. 다른 이름의 정렬 절차나 recursive Fibonacci 분석까지 학습한 것으로 확대하지 않는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

[[exam_questions/dm_2022_2_mid_q10|2022-2 중간 Q10]]의 iterative Fibonacci 부분에서 상태 보존과 정수 덧셈 count를 연결한다. [EX:dm_2022_2_mid_q10 p.2] 현재 필요한 선수내용은 Fibonacci 초기조건·반복문이며, 원문의 recursive 방식과 memoization 비교는 유보한다. Maximum invariant와 현재 Bubble/Insertion 구현에 직접 일치하는 기출 후보는 없다.


---

[[courses/discrete_mathematics/units/matrices-and-linear-maps|← 이전: Matrices와 Linear Maps의 대응]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/paradigms-greedy-and-computability|다음: Algorithmic Paradigms·Greedy와 계산 가능성 →]]
