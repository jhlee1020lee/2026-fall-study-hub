---
title: "Algorithm 명세와 Searching·Sorting의 실행"
description: "Pseudocode, 검색과 두 정렬 절차를 명세·상태·불변식으로 복습한다."
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
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-09-lecture-03"]
---

입력·출력의 약속을 먼저 적고 검색·정렬의 상태 변화를 추적한다. 각 반복이 무엇을 보존하며 언제 끝나는지 설명해 구현 사이의 차이를 확인한다.

## Algorithm과 Pseudocode: 입력을 결과로 바꾸는 정확한 절차

Algorithm(알고리즘)을 읽을 때는 먼저 **어떤 입력에 대해 무엇을 반환해야 하는가**를 정한다. 정수 두 개의 합, 두 matrix의 곱, 유한한 sequence의 maximum, 학습 데이터로 만드는 model은 출력의 종류부터 서로 다르다. 절차가 길고 정교해도 원하는 출력 조건을 만족하지 않으면 그 문제의 해법이 아니다. Algorithm은 이런 문제를 풀기 위한 precise instructions의 유한한 기술이다. 다만 기술된 명령 수가 유한하다는 사실과 모든 입력에서 실행이 끝난다는 사실은 별개다. 반복문 하나도 끝없이 실행될 수 있다. 이 관점은 [[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트: Algorithm의 명세]]와 [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 09:50–10:49]]에서 출발한다.

Pseudocode(의사코드)는 자연어와 실제 programming language 사이에서 절차를 드러낸다. 특정 언어의 문법을 모두 구현하지 않아도 반복 범위, 조건, 대입 순서와 반환값은 명확해야 한다. [M005 pp.4–8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)의 세 표기는 같은 Fibonacci 절차를 다음처럼 달리 적는다.

| 의미 | Rosen style | CLRS style | Programming style |
|---|---|---|---|
| 대입 | `:=` | `←` | `=` |
| 동등 비교 | 수학적 등호 | 수학적 등호 | `==` |
| 콜론의 예 | `n : integer`의 type 표시 | 문맥에 따라 읽음 | 조건문·반복문의 block 시작 |

따라서 `f1 = f2`를 읽는 의미는 표기 관례에 달려 있다. 대입문이라면 두 값이 같다는 명제를 주장하는 것이 아니라, 오른쪽의 현재 값을 왼쪽 변수에 저장하는 명령이다.

### Fibonacci: 이전 두 값을 보존하는 갱신 순서

Fibonacci sequence는 $F_0=0$, $F_1=1$, $F_n=F_{n-1}+F_{n-2}$로 정한다. 다음은 [M005 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-006)의 절차다. 입력은 nonnegative integer다.

```text
procedure fibonacci(n : integer)
    if n <= 1 then
        return n
    f1 := 0
    f2 := 1
    for i := 2 to n
        temp := f1 + f2
        f1 := f2
        f2 := temp
    return f2
```

반복 직전에 `f1`과 `f2`가 바로 앞의 두 항을 담는다고 생각하면 코드가 자연스럽다. 먼저 두 **이전 값**의 합을 `temp`에 보관하고, 두 변수의 역할을 한 칸 앞으로 옮긴다. 합을 저장하기 전에 `f1 := f2`를 실행하면 원래 `f1`을 잃어버린다.

| 처리한 단계 | `f1` | `f2` |
|---|---:|---:|
| 초기 상태 | 0 | 1 |
| `i = 2` | 1 | 1 |
| `i = 3` | 1 | 2 |
| `i = 4` | 2 | 3 |
| `i = 5` | 3 | 5 |

따라서 입력 4의 결과는 3이고, 입력 5에서는 한 번 더 갱신해 5를 반환한다. 강의도 최근 두 값을 유지하는 방식을 설명한다. 녹취의 초기값 일부에는 `0/1` 불확실성이 남아 있어, 위 초기값과 trace는 슬라이드에 맞춘 계산이다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 11:48–12:44]]

값을 계산하는 일과 계산의 비용을 세는 일도 구별해야 한다. 위 코드에서 수열의 두 값을 더하는 명령은 $n\ge2$일 때 $n-1$번 실행된다. $F_n$의 값 자체가 덧셈 횟수인 것은 아니다. 이 구별은 iterative 부분과 정수 덧셈 수를 연결하는 기출 요구에도 쓰인다. Recursive 부분의 호출 분석은 별도 선수 학습이므로 여기의 loop count와 섞지 않는다. [EX:dm_2022_2_mid_q10 p.2]

## Maximum과 Linear search: 읽은 구간에 대해 무엇을 아는가

### Maximum을 유지하는 Loop invariant

Nonempty sequence $a_1,\ldots,a_n$의 maximum을 찾으려면 첫 원소를 후보로 잡고 나머지를 비교한다. [M005 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-005)

```text
max := a1
for i := 2 to n
    if max < ai then max := ai
return max
```

Loop invariant(반복 불변식)는 “$i$번째 원소까지 처리하면 `max`는 $a_1,\ldots,a_i$의 maximum이다”이다. 처음에는 원소가 하나이므로 성립한다. 다음 원소가 현재 maximum보다 크면 교체하고, 아니면 유지하므로 성질이 계속된다. 유한한 $n$개를 모두 처리했을 때 원하는 결과를 얻는다.

예를 들어 $(3,1,7,4)$에서는 후보가 $3\to3\to7\to7$이다. 음수만 있는 $(-5,-2,-9)$에서도 $-5\to-2\to-2$로 올바르게 작동한다. 무조건 0에서 시작하면 두 번째 예에서 입력에 없는 0을 반환하므로 잘못이다. Empty sequence에는 첫 원소 자체가 없으므로 이 코드의 계약을 그대로 적용할 수 없다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 11:48]]

### Linear search의 성공 위치와 실패 표지

Searching problem은 주어진 $x$와 같은 원소의 위치를 찾거나 없음을 판정하는 문제다. 자료는 서로 다른 정수, 1-based index를 사용하며 성공하면 위치를, 실패하면 0을 반환한다. 이 반환 규약에서 0은 배열의 첫 위치가 아니다. [M005 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-009)

```text
i := 1
while i <= n and x != ai
    i := i + 1
if i <= n then location := i
else location := 0
return location
```

조건은 먼저 범위를 확인한 뒤, 범위 안일 때만 `ai`를 읽는 것으로 해석한다. 반복 중 $i$보다 앞선 원소들은 이미 $x$가 아님을 확인했다. 일치하는 값이 있으면 그 자리에서 멈추고, 없으면 $i=n+1$에 도달해 0을 반환한다. 끝난 cursor $n+1$을 발견 위치로 반환하거나 $a_{n+1}$을 데이터처럼 읽으면 안 된다.

예를 들어 네 원소가 모두 $x$와 다르면 네 번의 data comparison 뒤 $i=5$가 되고, 최종 결과는 0이다. 최악에는 모든 원소를 한 번씩 비교하므로 data comparison은 $n$회다. 강의의 $O(n)$ 예고는 이 증가 양상을 가리킨다. 반복 제어 비교까지 셀지는 cost model에서 별도로 정한다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 14:19–15:10]]

## Binary search: 정렬된 구간을 안전하게 줄이기

Binary search(이진 탐색)는 increasing order로 정렬된 목록을 이용한다. 중간값 $a_m$보다 $x$가 크면 그 왼쪽 값들도 전부 너무 작다. 이 논리로 후보의 절반을 버릴 수 있다. 정렬되지 않았다면 중간값 하나로 왼쪽 전체를 판단할 근거가 없다. 정렬에 드는 preprocessing 비용은 검색 자체의 비용과 별도다.

[M005 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-012)의 구현은 nonempty list의 inclusive interval $[i,j]$를 유지한다.

```text
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

원하는 값이 존재한다면 항상 남겨 둔 구간에 있다. $i<j$이면 $i\le m<j$이므로 어느 분기든 구간이 작아지고, 마지막에는 한 원소만 남는다. **이 구현에서는 $x=a_m$이어도 즉시 반환하지 않는다.** 같은 경우도 `j := m`으로 간다.

자료의 목록 $1,2,3,5,6,7,8,10,12,13,15,16,18,19,20,22$에서 19를 찾으면 다음과 같다. [M005 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-011)

| 현재 구간 | 중간 위치 $m$ | $a_m$ | 다음 구간 |
|---|---:|---:|---|
| $[1,16]$ | 8 | 10 | $[9,16]$ |
| $[9,16]$ | 12 | 16 | $[13,16]$ |
| $[13,16]$ | 14 | 19 | $[13,14]$ |
| $[13,14]$ | 13 | 18 | $[14,14]$ |

마지막 $a_{14}=19$를 확인해 14를 반환한다. 강의의 “길이가 1이 된 뒤 확인한다”는 설명이 이 마지막 검사에 해당한다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 19:07]]

종료 조건을 바꾸면 비교 횟수도 다시 세야 한다. 2021년 학기 미확인 기출의 관련 요구는 equality에서 즉시 종료하는 변형을 다룬다. 위 예에서는 세 번째 midpoint에서 equality를 만나지만, 슬라이드 코드는 거기서 끝나지 않는다. 그 기출의 평균 분석에는 성공 검색, 균등한 위치 분포, 특정 목록 크기, equality test까지 세는 조건이 붙는다. 그 조건을 이 trace에 소급 적용하면 안 된다. [EX:dm_2021_mid_q09 p.2]

## Sorting: 확정된 구간을 늘리는 두 가지 방법

Sorting(정렬)은 비교 순서가 정의된 objects를 그 순서에 맞게 재배열한다. 숫자 크기뿐 아니라 alphabetic order나 database의 key 순서도 가능하다. 같은 문제를 풀더라도 입력 크기, 이미 정렬된 정도, input distribution, hardware·software 환경이 다르면 적합한 방법도 달라질 수 있다. 무작위 permutation에서 좋은 방법이 특정 구조의 데이터에서도 항상 최선인 것은 아니다. 강의는 이 점을 average-case analysis와 연결했다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 20:54–23:13]]

### Bubble sort: 오른쪽에 maximum을 하나씩 확정하기

Bubble sort(버블 정렬)는 인접한 두 값의 순서가 뒤집혔으면 교환한다. 왼쪽에서 오른쪽으로 지나가면 아직 처리 중인 구간의 maximum이 오른쪽 끝까지 이동한다. [M005 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-014)의 코드는 다음과 같다.

```text
for i := 1 to n - 1
    for j := 1 to n - i
        if aj > a(j+1) then interchange aj and a(j+1)
```

Pass $i$를 시작할 때 오른쪽 $i-1$개는 이미 제자리에 있다. 남은 $n-i+1$개의 원소 사이를 $n-i$번 비교하면 다음 maximum도 확정된다. 여기서 `a(j+1)`은 배열의 $j+1$번째 원소를 나타내는 pseudocode 표기다.

| 단계 | 배열 | 이번 pass의 비교 수 |
|---|---|---:|
| 시작 | $7,3,5,2,6$ | — |
| 1 | $3,5,2,6,7$ | 4 |
| 2 | $3,2,5,6,7$ | 3 |
| 3 | $2,3,5,6,7$ | 2 |
| 4 | $2,3,5,6,7$ | 1 |

이것은 M005 p.15의 배열을 끝까지 추적한 것이다. 세 번째 pass 뒤 이미 정렬되어 보여도 코드에 조기 종료 검사가 없으므로 네 번째 pass가 남는다. 총 비교는 $4+3+2+1=10$회이며 실제 swap 수와 다르다. 뒤쪽 확정 구간을 제외한다는 설명은 [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 25:08]]에서도 강조된다.

### Insertion sort: 정렬된 prefix에 새 값을 끼워 넣기

Insertion sort(삽입 정렬)는 앞쪽의 sorted prefix를 유지한다. 한 원소만 있는 prefix는 이미 정렬되어 있다. $j$번째 단계에서는 $a_1,\ldots,a_{j-1}$이 정렬되어 있으므로, 새 값 $a_j$의 자리를 찾고 필요한 값들을 한 칸씩 밀면 된다. [M005 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-016)의 비교·이동 순서를 그대로 쓰면 다음과 같다.

```text
for j := 2 to n
    i := 1
    while aj > ai
        i := i + 1
    m := aj
    for k := 0 to j - i - 1
        a(j-k) := a(j-k-1)
    ai := m
```

첫 번째 loop는 앞에서부터 삽입 위치를 찾는다. 늦어도 $i=j$에서 자기 자신과의 strict comparison이 거짓이 되어 멈춘다. `m`에 새 값을 보존한 다음, **뒤에서부터** shift해야 아직 옮기지 않은 원소를 덮어쓰지 않는다. $i=j$라면 shift loop는 비어 있다.

앞의 배열에서 sorted prefix는 $[7]\to[3,7]\to[3,5,7]\to[2,3,5,7]\to[2,3,5,6,7]$이다. 특히 2를 넣을 때는 7, 5, 3을 뒤에서부터 옮겨 첫 자리를 비운다. 이것이 강의의 “알맞은 곳에 넣고 뒤쪽을 한 칸씩 민다”는 설명이다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 26:57–28:46]]

비교 연산자 하나도 성질을 바꾼다. `aj > ai`는 같은 값 앞에서 멈추므로, 이 구현은 나중에 들어온 equal key를 앞에 놓을 수 있다. 같은 key들의 원래 순서를 유지하는 stability(안정성)는 이 코드에 자동으로 따라오지 않는다. Bubble sort의 오른쪽 suffix와 Insertion sort의 왼쪽 prefix를 구별하되, 그 진행 방향 자체를 모든 변형이 공유하는 정의로 외우지는 말아야 한다.

## 핵심 정리

- 입력의 허용 범위와 성공·실패 출력부터 정한다.
- 대입은 현재 값을 바꾼다. Fibonacci의 이전 두 값, 삽입할 원소처럼 잃으면 안 되는 값은 먼저 보존한다.
- Maximum은 읽은 prefix의 최댓값, Bubble sort는 확정된 suffix, Insertion sort는 정렬된 prefix를 유지한다.
- Binary search는 정렬과 구간 축소 규칙을 함께 사용한다. Equality에서 멈추는 구현과 한 원소를 남기는 구현의 trace를 구별한다.
- 반환값, 비교 횟수, swap·shift 수는 서로 다른 질문이다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 명세와 표기

Nonempty integer list의 maximum 문제에서 유효 입력·출력·절차를 정하라. 유한한 명령문만으로 종료가 보장되는가? Pseudocode의 대입 표기와 동등 비교, colon의 두 용도도 구별하라.

<details><summary>해설 보기</summary>

유효 입력은 원소가 하나 이상인 유한 정수 목록이고, 출력은 그 목록의 최댓값이다. 첫 원소를 후보로 두고 나머지를 순서대로 비교해 더 클 때 갱신한 후 반환한다. 이 scan은 유한 목록을 끝까지 읽어 종료하지만, 짧은 무한 반복문도 작성할 수 있으므로 기술의 유한성과 실행의 종료는 별개다.

`:=`, `←`, programming style의 `=`는 대입이며 `==`는 동등 비교다. `n : integer`의 colon은 type, programming style 조건문 뒤의 colon은 block 시작을 나타낸다. 표기 관례를 먼저 확인해야 대입을 명제로 잘못 읽지 않는다.

**채점·확인:** 입력·출력·절차, 종료의 별도 근거, 대입/비교 및 type/block을 모두 구별한다.

</details>

#### 확인 Q02 · Fibonacci의 이전 상태

초기 상태 `(f1,f2)=(0,1)`에서 입력 5의 갱신과 반환값, 수열 값 덧셈 횟수를 구하라. 입력 0·1은 어떻게 처리하며, `f1 := f2`를 합 계산보다 먼저 두면 왜 틀리는가?

<details><summary>해설 보기</summary>

`i=2,3,4,5` 뒤의 상태는 `(1,1)`, `(1,2)`, `(2,3)`, `(3,5)`다. 반환값은 5이고 두 수열 값을 더하는 명령은 4번 실행된다. 일반적으로 $n\ge2$에서 이 덧셈은 $n-1$회다. 입력 0·1은 반복 전에 각각 0·1을 반환해 해당 덧셈을 하지 않는다.

먼저 `f1 := f2`를 하면 이전 `f1`이 사라져 첫 단계부터 $1+1=2$를 만들 수 있다. `temp`에는 갱신 전 두 값의 합을 저장해야 한다. 수열의 값과 연산 수는 다르다.

**채점·확인:** 네 상태, base cases, 값 5와 횟수 4, 덮어쓰기의 원인을 확인한다.

</details>

#### 확인 Q03 · Maximum의 불변식

목록 (−5,−2,−9)의 maximum scan을 추적하고 초기·유지·종료의 근거를 설명하라. 초기값을 0으로 바꾸거나 empty list를 넣으면 어떻게 되는가?

<details><summary>해설 보기</summary>

후보는 $-5\to-2\to-2$다. 첫 원소는 처음 읽은 구간의 maximum이다. 새 원소가 후보보다 클 때만 교체하면 처리한 prefix의 maximum이라는 성질이 유지된다. 마지막에는 prefix가 전체 목록이므로 $-2$가 정답이다.

0으로 시작하면 갱신하지 않아 목록에 없는 0을 반환한다. Empty list에는 첫 원소가 없어 제시 초기화가 정의되지 않으며 별도 처리가 필요하다.

**채점·확인:** 결과, 세 단계의 불변식 논증, 음수·빈 입력의 한계를 설명한다.

</details>

#### 확인 Q04 · 검색 cursor와 반환값

1-based 목록 (4,9,2,7)에서 linear search로 2와 5를 찾을 때 종료 cursor·반환값·data comparison 수를 구하라. 범위 검사와 이미 지나간 구간은 어떤 역할을 하는가?

<details><summary>해설 보기</summary>

2는 세 번째에서 일치하므로 cursor 3, 반환값 3, 데이터 비교 3회다. 5는 네 값 모두와 달라 cursor 5로 끝나지만 반환값은 실패 표지 0이며 데이터 비교는 4회다.

반복 중 cursor 앞의 값들은 모두 목표와 다르다. `i <= n`을 먼저 확인해 범위를 벗어난 값을 읽지 않는다. 성공 위치는 1부터 시작하므로 0은 첫 원소가 아니다. 최악에는 $n$개의 데이터를 비교하며 반복 제어 검사 수는 이 수에 포함하지 않는다.

**채점·확인:** 성공/실패의 cursor·반환·비교 수, 범위 검사 및 비용 기준을 명시한다.

</details>

#### 확인 Q05 · Binary search의 마지막 한 칸

정렬 목록 1,2,3,5,6,7,8,10,12,13,15,16,18,19,20,22에서 19의 검색 구간과 midpoint를 적어라. 왜 equality를 만난 뒤에도 계속하며, 왜 정렬·nonempty 조건이 필요한가?

<details><summary>해설 보기</summary>

구간은 $[1,16]\to[9,16]\to[13,16]\to[13,14]\to[14,14]$, midpoint는 $8,12,14,13$이다. 본문 구현은 `x > am`이면 왼쪽을 버리고 나머지는 `j := m`으로 처리하므로 같은 값을 보아도 바로 반환하지 않는다. 마지막 equality로 위치 14를 확인한다.

정렬되어 있어야 버린 구간에 목표가 없다고 추론할 수 있다. $i<j$에서 $i\le m<j$여서 두 분기 모두 구간을 줄이며, 목표가 있다면 남은 구간에 있다는 성질을 유지한다. 빈 목록은 마지막 원소 검사를 할 수 없어 별도 계약이 필요하다. 정렬 preprocessing 비용은 검색 자체와 따로 센다.

**채점·확인:** 모든 구간과 midpoint, equality 분기, 축소·보존 근거와 전제를 확인한다.

</details>

#### 확인 Q06 · Sorting 선택의 조건

숫자 외의 sorting 예를 들고, 무작위 permutation에서 유리한 방법이 반쯤 정렬된 자료에서도 항상 최선인지 설명하라.

<details><summary>해설 보기</summary>

문자열의 alphabetic order나 record의 key 순서도 비교 규칙을 정하면 sorting 대상이며 결과는 그 순서에 맞춘 재배열이다.

항상 최선이라고 할 수 없다. 입력 크기, 기존 정렬 정도의 정확한 의미, 입력 분포, 비교·이동 비용과 hardware·software 환경이 달라질 수 있다. 모든 입력의 균등 분포를 현실 분포로 자동 간주할 수 없다. 여기서 실행을 배운 것은 Bubble/Insertion이며 다른 정렬의 상세 절차까지 배웠다고 보지 않는다.

**채점·확인:** 비교 순서, 분포·비용·환경 의존성과 학습 범위를 설명한다.

</details>

#### 확인 Q07 · Bubble sort의 네 pass

(7,3,5,2,6)을 본문의 고정 loop로 정렬하라. Pass별 배열과 비교 수, 총 swap 수를 적고 정렬되어 보인 뒤에도 남은 pass가 있는 이유를 설명하라.

<details><summary>해설 보기</summary>

Pass 1은 (3,5,2,6,7): 비교 4, swap 4다. Pass 2는 (3,2,5,6,7): 비교 3, swap 1이다. Pass 3은 (2,3,5,6,7): 비교 2, swap 1이다. Pass 4는 같은 배열: 비교 1, swap 0이다. 총 비교 10회와 swap 6회를 구별한다.

매 pass의 인접 비교로 남은 구간의 maximum이 끝에 도착한다. 따라서 확정 suffix는 다음 pass에서 제외한다. 조기 종료 조건이 없으므로 세 번째 pass 후 정렬되어도 네 번째 비교를 수행한다.

**채점·확인:** 네 pass, 비교/swap의 구별, suffix 및 조기 종료 부재를 확인한다.

</details>

#### 확인 Q08 · Insertion sort의 보존과 이동

Prefix [3,5,7] 뒤의 새 값 2를 삽입하는 순서를 설명하라. 앞에서 `aj > ai`를 검사할 때 자기 자신까지 가면 어떻게 멈추는가? 같은 key 두 개의 순서는 반드시 보존되는가?

<details><summary>해설 보기</summary>

2를 `m`에 보관하고 삽입 위치 $i=1$을 정한다. 7, 5, 3 순으로 오른쪽에 복사한 다음 첫 자리에 2를 놓아 [2,3,5,7]을 얻는다. 뒤에서부터 이동해야 아직 복사하지 않은 값을 덮지 않는다. 매 단계 뒤에는 새 원소를 포함한 prefix가 정렬된다.

새 값이 가장 크면 $i=j$에서 자기 자신보다 큰지 묻는 조건이 거짓이 되어 멈추고 shift는 없다. 같은 값 앞에서도 strict comparison이 거짓이므로 새 equal key가 먼저 들어갈 수 있다. Key만 비교하는 $[3_A,3_B]$는 $[3_B,3_A]$가 될 수 있어 이 구현의 stability는 보장되지 않는다.

**채점·확인:** 값 보존, 역방향 shift, prefix, 자기 비교와 동등 key를 모두 다룬다.

</details>

### 적용 연습

#### 연습 P01 · 반환값과 연산 수를 따로 검증하기

**새로 만든 기출 연결 합성 연습.** [EX:dm_2022_2_mid_q10 p.2]에서 반복 절차와 정수 덧셈 수를 구별하는 요구만 옮겼다. 선수 개념은 Q01–Q02이며 재귀 호출 분석은 다루지 않는다. [[exam_questions/dm_2022_2_mid_q10|2022-2 중간 Q10 미리보기]]

한 구현이 base case 뒤 매 반복에서 `f1 := f2` 다음 `f2 := f1 + f2`를 실행한다. 입력 4에서 출력과 덧셈 횟수를 찾고, 올바른 절차로 고쳐 비교하라. 횟수가 같으면 correctness도 같은가?

<details><summary>해설 보기</summary>

초기 (0,1)에서 잘못된 갱신 후 상태는 $(1,2)\to(2,4)\to(4,8)$이다. 출력 8, 덧셈 3회다. 이전 두 값의 합을 `temp`에 먼저 보관한 뒤 `f1 := f2`, `f2 := temp`로 바꾸면 $(1,1)\to(1,2)\to(2,3)$이므로 출력 3, 덧셈 3회다.

Loop 수가 같아도 계산하는 식이 다르면 결과가 다르다. 명세를 만족하는지 확인한 뒤 비용을 비교해야 한다. 입력 0·1은 고친 구현에서도 반복 전에 반환한다.

**채점·확인:** 잘못된 trace·수정 trace·동일 횟수와 상이한 결과를 모두 제시한다.

</details>

#### 연습 P02 · 종료 규칙이 바꾸는 비용

**새로 만든 기출 연결 합성 연습.** [EX:dm_2021_mid_q09 p.2]의 equality 즉시 종료 요구를 구현 비교로 옮겼다. 2021년 자료의 학기는 미확인이다. Q05의 구간 추적이 선수 내용이며, 원문의 성공 검색·균등 위치·$n=2^k-1$ 평균 분석 전체는 요구하지 않는다.

목록 (2,4,6,8,10,12,14)에서 (A) 본문 구현과 (B) 매 반복에서 `x == am`을 먼저 검사해 같으면 반환하고 다르면 A의 갱신을 하는 변형을 비교하라. 목표 8과 9의 midpoint·반환값을 구하고 equality/대소 비교만 세어라. B도 한 원소가 남으면 마지막 equality를 한다.

<details><summary>해설 보기</summary>

목표 8에서 A의 midpoint는 4,2,3이다. 구간은 $[1,7]\to[1,4]\to[3,4]\to[4,4]$이며 위치 4를 반환한다. 대소 비교 3회와 마지막 equality 1회로 총 4회다. B는 첫 midpoint에서 equality 1회로 4를 반환한다.

목표 9에서 두 방법의 midpoint는 4,6,5다. $[1,7]\to[5,7]\to[5,6]\to[5,5]$에서 마지막 값 10과 다르므로 0을 반환한다. A는 $3+1=4$회, B는 각 반복의 equality와 대소 비교 $6+1=7$회다. 반복 제어는 세지 않았다.

조기 종료 검사는 일부 성공 입력을 줄이지만 검사 비용도 더한다. 두 trace만으로 평균 우열을 결론낼 수 없고 입력 분포와 비교 규약이 필요하다.

**채점·확인:** 두 경로·출력·4/1 및 4/7 비교 수, 평균 해석의 한계를 확인한다.

</details>

### 복습 순서

Q01–Q04로 명세와 갱신을 설명한 뒤 Q05·Q07·Q08을 종이에 추적한다. P01에서 잘못된 갱신을 고치고 P02에서 종료 조건을 비교한 다음, 틀린 단계만 다음 날 해설을 닫고 다시 계산한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트 · 2026-09-09 · 이산수학 3강]]
- [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 보정 녹취]] — 09:50–19:07 명세와 검색; 20:07–28:46 정렬. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [02. Algorithms.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf)
  - 명세·표기·Fibonacci: [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-008)
  - 검색: [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-012)
  - 정렬: [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/02.algorithms/page-017)

### 읽을 때의 범위

- 9월 9일 강의를 중심으로 한다. Fibonacci 초기값의 불명확한 발화는 자료의 0·1 초기화로 설명하며 음성을 복원했다고 보지 않는다.
- Maximum과 제시 Binary search는 nonempty 입력을 전제한다. 실패 표지 0과 종료 cursor를 구별하고 equality 즉시 반환 변형의 횟수를 본문 코드에 섞지 않는다.
- Insertion sort의 stability 판단은 strict comparison을 해석한 설명이다. Merge·Quick·재귀 및 중복 개수용 경계 탐색은 여기의 신규 학습 범위가 아니다.
- 기출 연결은 선정 소부분에 한정한다. 2021 중간은 학기 미확인이며 안내문의 Q8–Q11과 실제 Q1–Q10의 차이로 보이지 않는 Q11을 추정하지 않는다. 과거 배점·시험 규칙은 현재 규칙이 아니다.
- 공개 보정 녹취에도 불명확한 말과 가림이 남아 있다. 이 복습은 추가 청취나 음성 누락 확인이 아니다.
