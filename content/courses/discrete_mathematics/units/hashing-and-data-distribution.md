---
title: "Hash Function과 데이터 분산"
description: "Hash의 고정 길이 출력과 저장·조회 규칙, collision과 분포 의존성을 복습한다."
course: "discrete_mathematics"
unit_id: "hashing-and-data-distribution"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: []
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-23-lecture-05"]
---

Hash가 정하는 것은 record 자체가 아니라 먼저 찾아볼 위치다. 출력의 bit width, 실제 key의 분포, bucket의 load를 구분하며 lookup의 한계를 확인하자.

## Hash function과 fixed-length output

긴 key(키)를 그대로 비교하며 매번 모든 record(레코드)를 찾으면 저장한 데이터가 많아질수록 검색이 부담스러워진다. Hash function(해시 함수)은 입력을 정해진 크기의 출력으로 보내어 저장 위치를 선택하는 데 사용할 수 있다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 43:07–44:07]]에서 소개한 모델은 임의 길이 입력을 fixed-length output(고정 길이 출력)으로 보내는 function이다. 이 응용은 공급된 Number Theory PDF의 끝 이후에 설명된 STT 내용이다.

정수 입력의 간단한 예는

$$h:\mathbb Z\to\mathbb Z_m,\qquad h(x)=x\bmod m$$

이다. [[courses/discrete_mathematics/units/modular-arithmetic-and-inverses|Residue system]] $\mathbb Z_m=\{0,1,\ldots,m-1\}$을 출력으로 사용하므로 가능한 값이 $m$개다. 무한히 많은 정수 입력을 유한한 위치로 보내는 셈이다.

Fixed length는 출력을 모두 같은 bit width(비트 폭)로 표현할 수 있다는 뜻이다. $m\ge2$이면 필요한 최소 폭은 $\lceil\log_2m\rceil$ bits다. 설명용 $m=10$에서는 0부터 9까지를 표현해야 하므로 4 bits가 필요하다. 3 bits는 8개 값밖에 표현하지 못하고, 4 bits의 16개 patterns 중에는 사용하지 않는 것도 있다. $\log_2m$을 그대로 정수 길이라고 쓰기보다 ceiling을 확인해야 한다.

## Bucket을 통한 저장과 lookup

Bucket(버킷)을 $0,1,\ldots,m-1$로 번호 매겨 놓고 key $x$의 record를 bucket $h(x)$에 저장한다고 하자. 나중의 lookup(조회)에서도 같은 key에 같은 $h$를 적용하면 같은 bucket으로 갈 수 있다. 저장 규칙과 검색 규칙이 연결되어 전체 list를 항상 처음부터 훑을 필요를 줄이는 것이다.

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 45:58–46:56]]에서는 메뉴 이름과 가격이 긴 목록에 있을 때, 관련 section부터 찾는 비유로 이 동기를 설명했다. 실제 메뉴판이 hash table을 구현한다는 뜻은 아니다. 또한 hash의 output은 record 자체가 아니라 찾아볼 위치를 좁히는 정보다.

설명용으로 $m=10$에서 key 27의 record를 넣으면 $h(27)=7$이므로 bucket 7에 둔다. 다시 27을 찾을 때도 bucket 7로 간다. 그러나 그 안에 여러 key가 있으면 원래 key를 추가로 확인해야 한다. 위치를 계산했다는 사실만으로 record가 유일하게 정해지지 않는다. 충돌 처리 방식의 구현이나 언제나 $O(1)$이라는 보장은 이 강의 설명에 포함되어 있지 않다.

## Collision과 실제 데이터의 분포

서로 다른 $x,y$가 $h(x)=h(y)$를 만족하면 collision(충돌)이다. [[courses/discrete_mathematics/units/sets-functions-sequences|Injection]]의 정의로 보면, 입력이 무한하고 출력이 유한한 위 모델은 injection이 될 수 없다. 따라서 collision은 반드시 존재한다. 좋은 분산이란 모든 collision이 없다는 뜻이 아니라 실제로 들어오는 데이터가 일부 bucket에 지나치게 몰리지 않는다는 뜻이다.

Constant hash(상수 해시) $h(x)=0$도 형식적으로 고정 길이 출력을 만들지만 모든 record가 bucket 0에 모인다. [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 47:55]]은 정의를 만족하는 function과 유용한 hash를 이 예로 구별했다. 모든 record가 한곳에 있으면 bucket을 계산하는 이점이 거의 사라진다.

Modulo hash도 입력 분포에 따라 크게 달라진다. 비교를 위해 $m=10$을 명시적으로 정하자.

| 입력 key | $h(x)=x\bmod10$ |
|---|---:|
| 1, 11, 21 | 모두 1 |
| 13 | 3 |
| 27 | 7 |
| 45 | 5 |
| 127 | 7 |
| 4 | 4 |

첫 줄은 집중을 보여 주는 해설용 입력이다. 나머지 key들은 [[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 49:28]]에 등장하는 예를 명시한 modulus 아래에서 계산했다. 27과 127은 여전히 충돌하지만 다른 값들은 여러 bucket으로 흩어진다. STT의 불명확한 modulus와 첫 숫자열을 정확한 발화로 복원한 것은 아니다.

일반적으로 $x$와 $x+m$은 언제나 같은 bucket으로 가므로 의도적인 collision을 만들기 쉽다. 다양한 값이 들어올 것이라는 기대만으로 나쁜 입력이 배제되는 것은 아니다. [[courses/discrete_mathematics/units/asymptotic-analysis-and-cost-models|Average-case와 input distribution]]의 구별이 여기에도 적용된다.

### 평균 load와 과부하 확률

Bucket 수를 $B$, item 수를 $N$이라 쓰면 bucket당 산술 평균 load(적재량)는 $N/B$다. 이는 각 bucket의 item 수를 모두 더하면 $N$이라는 사실에서 나온다. 그러나 어떤 bucket이 이 평균보다 훨씬 클 가능성이 작다는 결론은 평균값만으로 나오지 않는다. 모든 item이 한 bucket에 들어가도 평균은 여전히 $N/B$다.

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 STT 50:15]]의 과부하 가능성 분석은 배치에 대한 probability model(확률 모형)이 필요하다는 전제 아래 읽어야 한다. 예를 들어 각 item이 독립적으로 각 bucket에 균등하게 간다고 가정하면 특정 bucket의 expected load도 $N/B$지만, 실제 데이터가 그 가정을 만족하는지는 별도다. 강의에서는 정량적인 과부하 확률 bound를 유도하지 않았다. 저장 위치의 개수, key의 구조, 필요한 분산 특성을 함께 봐야 hash 선택의 의미가 생긴다.

## 핵심 정리

- m개의 bucket 번호에는 ceil(log₂m) bits가 필요하며 모든 bit pattern을 사용할 필요는 없다.
- 저장과 lookup은 같은 hash 규칙과 parameters를 공유해야 한다.
- 무한 입력을 유한 출력으로 보내면 collision은 존재한다. 좋은 분산과 collision의 부재는 다르다.
- 산술 평균 load N/B만으로 개별 bucket의 최대 load나 과부하 확률을 알 수 없다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · Fixed-width output

강의의 hash model과 h(x)=x mod m의 domain·output을 설명하라. m=10의 bucket 번호를 fixed width로 쓰려면 몇 bits이며 log₂10을 그대로 길이라고 쓸 수 있는가?

<details><summary>해설 보기</summary>

강의 모델은 임의 길이 입력을 고정 길이 출력으로 보내는 함수다. 정수 예는 ℤ→ℤₘ으로 무한한 정수 입력을 0,…,m−1의 m개 output에 보낸다. w bits는 2ʷ patterns이므로 m≥2에서 최소 정수 w=ceil(log₂m)이다. 3 bits는 8개라 10개를 담지 못하고 4 bits면 16개 중 10개를 사용할 수 있다. Log₂10은 정수 길이가 아니므로 ceiling이 필요하다.

**점검 기준:** 입력 집합·출력 수·2ʷ≥m의 조건과 사용하지 않는 patterns를 구분한다.

</details>

#### 확인 Q02 · 저장과 lookup의 공통 규칙

Modulo 10 hash로 key 27을 저장하고 다시 조회하는 과정을 말하라. 저장과 조회에서 규칙을 바꾸거나 bucket 번호를 곧 record라고 생각하면 왜 문제가 되는가?

<details><summary>해설 보기</summary>

27 mod 10=7이므로 record를 bucket 7에 둔다. 같은 key와 같은 hash·parameters로 조회하면 다시 7로 가서 원래 key가 맞는지 확인한다. 규칙을 달리 쓰면 다른 bucket으로 가서 저장된 값을 놓칠 수 있다. 127도 bucket 7이므로 위치가 같다고 key나 record가 같은 것은 아니다. Bucket은 후보 위치를 좁힐 뿐이다. 구체적인 collision-resolution 방식이나 항상 O(1)이라는 보장은 여기서 주어지지 않았다.

**점검 기준:** 동일 규칙·원래 key 확인·bucket과 record의 차이를 설명한다.

</details>

#### 확인 Q03 · Collision·분포·평균 load

Collision이 필연적인 이유와 constant hash의 문제를 설명하라. Modulo 10에서 1,11,21 및 13,27,45,127,4의 분포를 계산하라. N items, B buckets의 평균 load가 모든 bucket의 load를 보장하는가?

<details><summary>해설 보기</summary>

무한 입력을 유한 출력에 injection으로 대응시킬 수 없으므로 서로 다른 입력이 같은 output으로 가는 collision이 있다. h(x)=0은 형식상 고정 출력을 주지만 모든 record를 한 bucket에 모은다. Modulo 10에서 1,11,21은 모두 1, 뒤의 다섯 key는 3,7,5,7,4로 가서 일부 분산되지만 27과 127은 충돌한다. 일반적으로 x와 x+10은 쉽게 같은 bucket을 만든다.

모든 load를 더하면 N이므로 산술 평균은 N/B다. 그러나 전부 한 bucket에 있어도 같은 평균이다. 특정 bucket의 expected load나 과부하 확률을 말하려면 배치의 확률 모형이 필요하다. 균등·독립 가정을 실제 데이터가 만족하는지는 별도이며 여기서 정량 overload bound를 얻은 것은 아니다.

**점검 기준:** Collision의 존재와 유용한 분산을 구별하고 모든 residues·평균의 한계를 계산한다.

</details>

### 적용 연습

#### 연습 P01 · 평균이 같아도 다른 bucket

**새로 만든 강의 기반 일반 연습.** 직접 대응하는 hash 기출 후보가 없어 기출형이라고 부르지 않는다. 선수내용은 modulo hash·load·lookup이다.

4 buckets에 h(x)=x mod 4로 저장한다. 데이터 A={0,4,8,12}와 B={0,1,2,3}의 bucket별 load, 평균, 필요한 출력 bits를 비교하라. '평균 1이므로 hash output만으로 record를 유일하게 알 수 있다'는 결론을 검토하라.

<details><summary>해설 보기</summary>

A의 load는 (4,0,0,0), B는 (1,1,1,1)이며 둘 다 평균 4/4=1이다. Bucket 번호는 0,…,3이라 두 경우 모두 2 bits다. A에서는 네 key가 output 0을 공유하므로 hash output만으로 record를 구별하지 못한다. B의 현재 네 key는 충돌하지 않지만 이후 key 4가 들어오면 0과 충돌한다. 평균과 출력 폭은 현재나 미래의 record 유일성을 보장하지 않으며 원래 key 확인이 필요하다.

**점검 기준:** 두 load vectors·동일 평균·bit width·현재와 추가 입력의 collision을 각각 확인한다.

</details>

### 짧은 복습 계획

Q01에서 출력 개수와 bit patterns를 구분하고 Q02는 저장부터 조회까지 같은 key를 따라간다. Q03의 collision 예를 계산한 뒤 P01에서 평균 load와 실제 배치를 나란히 그려 비교한다. 다음으로 [[courses/discrete_mathematics/units/pseudorandomness-and-security|PRNG와 보안 요구]]를 읽는다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 이산수학 강의·자료 연결]]

[[courses/discrete_mathematics/transcripts/2026-09-23|2026-09-23 보정 STT]] · 43:07, 44:07, 45:58, 46:56, 47:55, 48:43, 50:15.

2026-09-23 43:07 이후 STT로 확인한 응용이며 해당 instructor PDF page는 공급되지 않았다. Key·record와 n/m 표기의 혼동은 분리해 읽는다. Modulo 10의 예와 ceiling 계산은 명시한 설명용 계산이며 49:28의 불명확한 modulus·숫자열을 복원한 발화가 아니다. Collision 처리 구현과 정량 overload bound는 공급되지 않았다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

기출 후보에 hash·bucket·lookup을 직접 다루는 문항은 없다. 빈 상자의 expected value 문항은 indicator와 별도 확률 모형이 더 필요하여 현재의 load 설명을 그 기출 유형으로 확대하지 않는다.


---

[[courses/discrete_mathematics/units/modular-arithmetic-and-inverses|← 이전: Congruence Classes와 Modular Inverse]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/pseudorandomness-and-security|다음: Pseudorandom Generation과 Cryptographic 요구 →]]
