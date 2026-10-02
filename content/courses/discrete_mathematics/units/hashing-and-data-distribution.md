---
title: "Hash Function과 데이터 분산"
description: "Modulo hash, collision과 데이터 분포를 작은 bucket 예제로 복습한다."
course: "discrete_mathematics"
unit_id: "hashing-and-data-distribution"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["04. Number Theory Applications.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05"]
---

Key로 저장 위치와 조회 위치를 함께 계산하는 규칙을 이해한다. 충돌의 존재와 분산의 품질을 구별하고 평균 load만으로 알 수 없는 것을 확인한다.

## Hash function: 저장과 검색이 공유하는 위치 계산

데이터를 효율적으로 저장한다는 말에는 나중에 원하는 데이터를 찾는 비용도 포함된다. 긴 목록에 메뉴 이름과 가격을 차례로 적으면 query마다 처음부터 linear search해야 할 수 있다. 메뉴를 section별로 나누면 먼저 해당 section으로 간 뒤 그 안에서 찾는다. 이 비유는 실제 메뉴판이 hash table이라는 뜻이 아니라, 저장할 때와 찾을 때 같은 규칙을 사용한다는 생각을 보여 준다. [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: Hash와 데이터 분산]], [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 44:59–46:56]]

Hash function(해시 함수)은 강의의 모델에서 임의 길이의 input을 고정 길이의 output으로 보내는 함수다. 대표적인 정수 예는

$$h:\mathbb Z\to\mathbb Z_m,\qquad h(x)=x\bmod m$$

이다. Key(검색 기준값) $x$에 대해 $h(x)=j$이면 record를 bucket(저장 구획) $j$에 둔다. 나중에 같은 key와 같은 함수·parameters로 $j$를 다시 계산하면 전체 목록부터 찾을 필요가 줄어든다. 함수나 modulus를 바꾸고 기존 위치 그대로 검색하면 다른 bucket으로 갈 수 있다. [NM002 p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-002)

### 고정된 output 길이와 key의 식별은 다르다

$m\ge2$개의 residue를 같은 bit width로 표현하려면 $\lceil\log_2m\rceil$ bits면 된다. 예를 들어 $m=10$이면 3 bits의 8개 patterns로는 부족하고 4 bits의 16개 patterns면 충분하다. 이 경우 사용하지 않는 patterns도 있다. 강의의 $\log m$ 표현을 정수 길이로 정확히 읽기 위해 ceiling을 붙인 계산이다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 43:07–44:07]]

고정 길이 output은 record 전체를 유일하게 나타내는 식별자라는 뜻이 아니다. 서로 다른 $x,y$에 대해 $h(x)=h(y)$일 수 있다. 이런 collision(충돌)이 있으면 bucket 위치를 찾은 뒤에도 어떤 record인지를 구분해야 한다.

## Collision과 입력 분포: 평균 load만으로는 부족하다

### 충돌의 존재와 좋은 분산을 구별하기

무한한 input domain에서 유한한 output 집합으로 가는 함수는 injective일 수 없다. 따라서 이 모델에서는 collision이 반드시 존재한다. 목표는 모든 collision을 제거하는 것이 아니라 다루는 데이터가 한쪽에 지나치게 몰리지 않게 하는 것이다. Constant function $h(x)=0$도 형식적인 hash 정의는 만족하지만 모든 record가 같은 bucket에 쌓여 검색상 이점을 잃는다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 47:55–48:43]]

Modulo hash도 입력의 구조에 민감하다. $h(x)=x\bmod10$을 명시적으로 택한 해설 예에서 $1,11,21$은 모두 bucket 1로 간다. 강의에 등장한 다양한 값들을 같은 modulus에 넣으면 다음과 같다.

| Key | 13 | 27 | 45 | 127 | 4 |
|---|---:|---:|---:|---:|---:|
| Bucket | 3 | 7 | 5 | 7 | 4 |

여러 bucket에 분산되지만 27과 127은 여전히 충돌한다. 녹취의 앞쪽 숫자열은 불명확하므로 $1,11,21$은 이를 복원한 인용이 아니라 조건을 정한 설명용 예다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 49:28]]

NM002 p.2의 실제 그림도 서로 다른 두 key의 화살표가 같은 output 02에 도착하고, 다른 key는 01과 04로 간다. 읽어야 할 핵심은 모든 화살표가 서로 다른 곳으로 향한다는 것이 아니라, **분산과 collision이 함께 존재한다**는 점이다.

### Bucket 평균과 확률적 보장의 차이

$B$개 bucket에 $N$개 items를 넣으면 bucket당 평균 load(저장 항목 수)는 언제나 $N/B$다. 이것은 전체 수를 bucket 수로 나눈 항등식이다. 예를 들어 10개 bucket에 20개 items를 모두 첫 bucket에 넣어도 평균은 2다. 따라서 평균만으로 각 bucket에 대략 두 개씩 들어갔다고 말할 수 없다.

특정 bucket이 과부하될 확률이 작다고 말하려면 배치가 어떤 probability model을 따르는지 알아야 한다. Uniform·independent 배치 같은 가정은 정당화해야 하며, 단순히 modulo를 계산했다는 이유로 성립하지 않는다. 강의의 load-balancing 설명도 분포를 고려하는 동기이고 정량적인 확률 bound를 유도한 것은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 48:43–50:15]]

자료의 “constant lookup time을 가능하게 한다”는 소개 역시 모든 입력의 worst-case가 무조건 $O(1)$이라는 뜻은 아니다. Collision 처리, load, 입력 분포와 함수 계산 비용을 따로 보아야 한다. 구체적인 collision-resolution 구현은 이 범위에서 주어지지 않았다. 이 단원에서 확실히 연결할 수 있는 것은 key에서 위치로 가는 공통 규칙과, 그 규칙의 유용성이 실제 분포에 달린다는 사실이다.

## 핵심 정리

- Fixed-width output은 작은 위치 번호를 표현한다는 뜻이며 key를 유일하게 식별한다는 뜻은 아니다.
- 저장과 검색은 같은 hash 함수와 parameters를 사용해야 한다.
- 무한한 입력을 유한한 bucket으로 보내면 collision은 불가피하다.
- 평균 load $N/B$는 산술 항등식이다. 좋은 분산이나 무조건 일정한 lookup 시간을 보장하지 않는다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Fixed-width의 정확한 의미

강의의 hash function 모델과 $h:\mathbb Z\to\mathbb Z_m$의 modulo 예를 설명하라. $m=10$의 bucket 번호는 왜 4 bits가 필요하며, 출력이 fixed-width이면 모든 bit pattern을 사용하는가?

<details><summary>해설 보기</summary>

임의 길이 입력을 정해진 길이 출력에 대응시키는 함수다. 정수 예는 $h(x)=x\bmod m$으로 가능한 output은 $m$개다. $b$ bits는 $2^b$개 patterns를 표현하므로 최소 고정 폭은 $\lceil\log_2m\rceil$이다.

$m=10$에서 3 bits는 8개뿐이라 부족하고 4 bits의 16개 중 10개를 쓰면 된다. 사용하지 않는 patterns가 있어도 fixed-width다. 출력의 길이가 고정되었다고 원래 입력까지 유일하게 복원할 수 있는 것은 아니다.

**채점·확인:** 함수의 방향, ceiling의 이유, 8/16 patterns 및 미사용 pattern을 확인한다.

</details>

#### 확인 Q02 · 저장과 조회의 약속

메뉴를 section별로 나누는 비유는 hash에서 어떤 원리를 설명하는가? Key 27을 modulo 10으로 저장한 뒤 같은 record를 찾는 절차와, bucket을 찾은 뒤에도 남는 일을 설명하라.

<details><summary>해설 보기</summary>

긴 목록 전체를 매번 읽는 대신 저장할 때 정한 위치 규칙을 조회에도 재사용한다는 원리다. 메뉴판 자체가 실제 hash table이라는 뜻은 아니다. 27 mod 10=7이므로 bucket 7에 저장하고 조회 때도 같은 계산으로 7에 간다.

다른 key 127도 bucket 7에 갈 수 있으므로 위치를 알았다는 사실만으로 원하는 record가 유일해지지 않는다. Key를 구별하는 처리가 더 필요하다. 함수나 modulus만 바꾸고 기존 위치를 그대로 두면 조회가 실패할 수 있다.

**채점·확인:** 공통 함수·parameters, bucket 계산, key 식별의 필요성을 설명한다.

</details>

#### 확인 Q03 · 불가피한 충돌과 나쁜 분산

왜 무한 입력·유한 output의 hash는 injective일 수 없는가? Constant hash와 modulo 10에서 $1,11,21$ 및 $13,27,45,127,4$의 위치를 비교하라.

<details><summary>해설 보기</summary>

서로 다른 모든 입력에 다른 output을 주려면 무한히 많은 output이 필요하지만 output은 유한하므로 충돌이 존재한다. Constant hash는 모든 입력을 한 곳에 보내 정의는 만족해도 분산에 도움이 되지 않는다.

Modulo 10에서 첫 집합은 모두 bucket 1이다. 둘째는 $3,7,5,7,4$로 여러 곳에 가지만 27과 127이 충돌한다. 일반적으로 $x$와 $x+10$도 충돌한다. 충돌을 완전히 없애는 목표와 실제 입력이 지나치게 몰리지 않게 하는 목표는 다르다. 자료의 그림도 두 key가 같은 02로 가며 다른 key는 01·04로 가는 구조다.

**채점·확인:** cardinality 논증, 두 위치열, constant hash와 그림의 분산/충돌 공존을 확인한다.

</details>

#### 확인 Q04 · 평균 load와 확률

10개 bucket에 20개 items를 넣으면 평균 2다. 전부 한 곳에 넣어도 이 말이 성립하는가? 이 평균에서 낮은 과부하 확률이나 모든 lookup의 worst-case O(1)을 결론낼 수 있는가?

<details><summary>해설 보기</summary>

성립한다. (20,0,0,0,0,0,0,0,0,0)의 총합도 20이라 평균은 2다. 평균은 총 items 수를 bucket 수로 나눈 값이지 각 bucket이 평균에 가깝다는 보장이 아니다.

과부하 확률을 계산하려면 어떤 확률 모델로 배치하는지 알아야 한다. Uniform·independent 가정은 modulo 연산만으로 얻어지지 않는다. Lookup에는 collision 처리와 load, 함수 계산 비용도 관여하므로 자료의 constant lookup 소개를 무조건적인 worst-case 보장으로 읽지 않는다.

**채점·확인:** 극단적 분배 반례와 필요한 분포·구현 조건을 분리한다.

</details>

### 적용 연습

#### 연습 P01 · 같은 평균, 다른 집중도

**새로 만든 강의 기반 일반 연습.** Hash·bucket lookup의 직접 대응 기출은 없다. 빈 상자 기대값 기출은 별도의 확률 도구를 요구하므로 여기서는 사용하지 않는다.

Modulo 5로 A=(0,5,10,15,20), B=(0,1,2,3,4)를 저장한다. 각 bucket의 load, 평균, 최대 load, 번호의 고정 bit 폭을 구하라. 평균으로 함수 품질을 판정하자는 주장을 평가하라.

<details><summary>해설 보기</summary>

A의 loads는 $(5,0,0,0,0)$, B는 $(1,1,1,1,1)$이다. 둘 다 평균 $5/5=1$이지만 최대 load는 각각 5와 1이다. 번호는 0부터 4까지 5개이므로 $\lceil\log_2 5\rceil=3$ bits가 필요하다.

같은 함수와 같은 평균도 입력 분포가 다르면 집중도가 달라진다. 이 관측은 B의 다섯 key에 관한 것이지 모든 입력의 균등 분산을 증명하지 않는다. 함수 선택과 실제 데이터 구조를 함께 보아야 한다.

**채점·확인:** 두 load 벡터·평균·최댓값·3 bits와 일반화의 한계를 확인한다.

</details>

#### 연습 P02 · 함수만 바꾼 조회

**새로 만든 강의 기반 일반 연습.** 저장·조회 규칙 변경의 직접 기출 근거는 없다.

Key 12,22를 modulo 10으로 저장한 뒤 레코드를 옮기지 않고 조회만 modulo 7로 바꿨다. 각 조회 위치를 계산하고, 실패 원인과 안전하게 바꾸기 위해 필요한 조건을 설명하라. “두 key가 다른 bucket으로 나뉘었으니 해결됐다”는 말도 평가하라.

<details><summary>해설 보기</summary>

저장 위치는 둘 다 2다. 새 조회는 12 mod 7=5, 22 mod 7=1로 가므로 원래 위치 2를 찾지 않는다. 새 함수로 저장 위치도 일치하게 바꾸거나 기존 규칙으로 조회해야 한다.

이 두 key가 새 함수에서 충돌하지 않는 것은 한 예일 뿐이다. 다른 key 12,19는 둘 다 5로 간다. 함수 변경이 모든 충돌을 없애거나 모든 lookup을 일정 시간에 끝내 준다는 결론은 아니다. 구체적인 충돌 처리 구현은 이 연습의 범위 밖이다.

**채점·확인:** 2·2와 5·1, 위치 규칙의 일치, 새 충돌 예를 확인한다.

</details>

### 복습 순서

Q01–Q02로 위치 계산을 확인한 뒤 Q03–Q04에서 충돌과 평균의 반례를 만든다. P01의 두 데이터 집합을 직접 분류하고 P02의 함수 변경 오류를 설명한다. 다음 날 숫자 없이도 조건의 차이를 말해 본다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트 · 2026-09-23 · 이산수학 5강]]
- [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 녹취]] — 43:07–44:07 fixed-width; 44:59–46:56 저장·조회; 47:55–50:15 충돌·분포. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - Hash model과 collision 그림: [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-002)

### 읽을 때의 범위

- 9월 23일의 실제 hash 설명을 따른다. 해당 응용 자료는 이후 확보된 보충 자료이며 당시 자료 가용성을 소급하지 않는다.
- 녹취의 log m을 정수 폭으로 읽을 때 ceiling이 필요하다. Modulo 10의 1,11,21은 불명확한 숫자열을 복원한 인용이 아니라 조건을 정한 예다.
- Constant lookup은 조건부로 가능한 소개다. Collision-resolution 구현, 무조건적인 O(1) 보장, 과부하의 정량 확률 bound는 제공되지 않았다.
- 평균 load와 uniform·independent 배치 가정은 다르다. 공개 보정 녹취의 불명확한 표현을 새 음성 확인으로 해소한 것은 아니다.
