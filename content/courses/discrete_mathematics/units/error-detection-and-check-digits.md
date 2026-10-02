---
title: "오류 검출·복구와 Check Digits"
description: "오류 위치와 개수에 따라 parity, repetition, UPC, ISBN-10이 보장하는 검출·복구를 비교한다."
course: "discrete_mathematics"
unit_id: "error-detection-and-check-digits"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["04. Number Theory Applications.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-28-lecture-06"]
---

먼저 수신값에서 무엇을 알고 있는지 따져야 검출과 복구의 보장을 구분할 수 있다. Parity·반복 전송·UPC·ISBN-10의 계산을 통해 오류 모형과 추가 정보의 역할을 비교한다.

## Error detection과 Correction: 추가 정보가 필요한 이유

통신 중에는 packet이 사라지거나 도착한 값이 바뀔 수 있다. 작은 반도체 소자에서는 신호와 전기적 간섭, 전송·관측 과정도 오류의 동기가 된다. Error detection(오류 검출)은 잘못되었음을 알아내는 일이고, error correction(오류 정정)은 원래 값으로 되돌리는 일이다. 오류가 있다는 사실을 아는 것과 어느 값으로 고쳐야 하는지 아는 것은 다르다. [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: 오류 검출과 복구]], [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 19:40–22:12]]

추가 구조 없이 임의의 1MB를 보냈다고 하자. 수신한 bit string 자체만 보고는 이것이 원래 메시지인지, 다른 메시지가 손상된 결과인지 보편적으로 구분할 수 없다. Redundancy(중복 정보)는 허용되는 전송값 사이에 제약을 만들어 이 구분을 돕는다. 그 대가는 원래 정보보다 더 많은 양을 보내는 overhead다. 모든 특별한 데이터 모델에서 무조건 같은 추가량이 필요하다는 주장이 아니라, 임의 데이터의 오류를 복구하려는 상황의 동기다.

Error-correcting code(ECC)는 메시지를 packets로 나누고 일부가 소실·변조되어도 복구할 수 있게 encoding한다. 원래 정보량, 전송 code의 크기, 고칠 수 있는 오류 수에는 trade-off가 있다. 강의는 이론적 bound와 추가 성질을 연구한다고 소개했지만 특정 bound 식이나 최적성 증명은 제시하지 않았다. 높은 화질의 영상이 끊기는 예도 요구 전송량과 실제 전달량을 설명하는 동기이며, buffering 자체가 bit corruption이나 특정 ECC의 결과임을 확정하지 않는다. [NM002 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-012), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 37:48–39:37, 48:35]]

## Parity와 Repetition: 이상을 감지하는 것과 위치를 고치는 것

### Even parity가 알려 주는 한 가지 조건

Hamming weight(해밍 무게)는 bit string에서 1의 개수다. Even parity(짝수 패리티)는 마지막 check bit를 정해 전체 Hamming weight를 짝수로 만든다. [NM002 p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-010)의 예는 다음과 같다.

| 상태 | Bit string | 1의 개수 |
|---|---|---:|
| 원래 데이터 | `1011001` | 4 |
| Check bit 0을 붙인 전송값 | `10110010` | 4 |
| 오류가 난 수신값 | `10110011` | 5 |

한 bit가 뒤집히면 1의 개수가 하나 늘거나 줄어 홀짝이 바뀐다. 따라서 single bit flip은 검출한다. 그러나 홀수 parity만으로는 어느 bit가 틀렸는지 알 수 없다. 어느 한 자리를 뒤집어도 짝수 parity가 되는 후보가 여럿이기 때문이다. 일반적으로 홀수 개의 bit flip은 검출하고 짝수 개는 놓칠 수 있다.

녹취에는 parity를 correction이라고 부르는 표현과 곧바로 “고치는 게 안 된다”는 설명이 함께 있다. 여기서는 slide의 detection과 위치를 알 수 없다는 이유에 따라 **검출만 보장한다**고 구별한다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 22:12–24:06]]

### Majority vote가 사용하는 더 많은 복사본

같은 bit를 세 번 보내고 majority vote(다수결)를 취하면, 같은 bit의 세 copies 중 최대 하나가 flip된 경우 복구할 수 있다. 수신값 $0,1,0$에서는 0이 원래 값이다. 다섯 번 반복하면 같은 위치의 다섯 copies 중 최대 두 flips를 견딘다. 대신 전송량은 각각 3배, 5배가 된다. 이 보장은 원래 bit별로 정한 오류 수 조건에 대한 것이다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 31:10–32:09]]

Erasure(소실)에서는 어느 copy가 비었는지 알고 남은 값은 올바르다. 따라서 세 copies 중 두 개가 소실되어도 하나가 남으면 복구할 수 있다. 반면 세 값이 도착했는데 두 값이 잘못되면 majority가 틀릴 수 있다. 강의 후반에 repetition, bit flip, erasure 표현이 섞여 정정되는 부분은 이 두 모델로 나누어 읽어야 한다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 43:12–44:09]]

## UPC: Decimal digits의 가중합으로 한 자리 오류 검출하기

Universal Product Code(범용 상품 코드, UPC)의 여기서 다루는 방식은 11개의 decimal digits 뒤에 check digit $x_{12}$를 붙인다. 홀수 위치에는 weight 3, 짝수 위치에는 weight 1을 주어

$$
3x_1+x_2+3x_3+x_4+\cdots+3x_{11}+x_{12}\equiv0\pmod{10}
$$

을 맞춘다. Bit가 아니라 decimal digit를 다루는 식이다. [NM002 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-011), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 33:07–34:02]]

자료의 앞 11자리 `03600029145`에 weights를 곱하면

$$3\cdot0+3+3\cdot6+0+3\cdot0+0+3\cdot2+9+3\cdot1+4+3\cdot5=58.$$

따라서 $58+x_{12}\equiv0\pmod{10}$에서 $x_{12}=2$이고 최종 code는 `036000291452`다. Leading zero도 자리의 일부이므로 잃어버리면 안 된다.

### 단일 변경을 잡는 이유와 알려진 빈 자리의 복구

어느 한 digit가 $\Delta\ne0\pmod{10}$만큼 바뀌면 checksum은 $w\Delta$만큼 바뀐다. Weight $w$는 1 또는 3이며 둘 다 modulo 10에서 invertible이다. 따라서 $w\Delta\not\equiv0$여서 single-digit error를 검출한다. 이는 자료의 보장을 풀어 쓴 수학적 설명이다.

반대로 **어느 자리가 비었는지 알고** 나머지가 올바르면

$$wx\equiv-(\text{나머지 weighted sum})\pmod{10}$$

을 풀어 그 digit를 복구할 수 있다. $3^{-1}\equiv7\pmod{10}$이므로 weight 3인 자리도 유일하게 정해진다. 앞 예의 세 번째 자리 6을 지웠다고 하자. 나머지 weighted sum은 전체 합 60에서 $3\cdot6$을 뺀 42다. 따라서 $3x+42\equiv0$, $3x\equiv8$, $x\equiv7\cdot8\equiv6\pmod{10}$이다. 이 빈 자리 계산은 새 해설 예다.

위치가 미지인 값 변경에는 같은 논리를 바로 적용할 수 없다. 강의의 deletion 설명은 알려진 빈 자리를 복구하는 상황으로 한정해야 한다. 어디서 문자가 삭제되어 이후 위치까지 밀렸는지 모르는 일반 deletion은 다른 문제다. 또한 둘 이상의 오류가 서로 상쇄되면 checksum을 통과할 수 있다. 검사를 통과했다는 사실이 무오류의 증명은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 35:03–35:49]]

## ISBN-10: 서로 다른 Weights로 자리 교환까지 검출하기

ISBN-10은 열 자리 중 마지막 digit를

$$x_{10}\equiv\sum_{i=1}^{9}ix_i\pmod{11}$$

로 정한다. 나머지 10은 `X`로 표시한다. 이 식은 $\sum_{i=1}^{9}ix_i-x_{10}\equiv0$이고, $-1\equiv10\pmod{11}$이므로 열 자리 weights를 $1,2,\ldots,10$으로 읽을 수 있다. 다른 길이의 ISBN 방식과 혼동하지 않는다. [NM002 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-011), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 35:49–36:48]]

Single error는 한 자리 값 변경이고 transposition error(자리 교환 오류)는 두 자리의 값을 맞바꾸는 것이다. Modulo 11은 field이고 모든 weight가 nonzero다. 한 자리의 nonzero 변경 $\Delta$는 $i\Delta\ne0\pmod{11}$이므로 검출된다.

서로 다른 위치 $i,j$에 서로 다른 값 $a,b$가 있다가 교환되면 weighted sum의 변화는

$$ib+ja-(ia+jb)=(i-j)(b-a)\pmod{11}$$

이다. 두 인수 모두 nonzero이므로 곱도 nonzero다. 이것이 서로 다른 digits의 transposition을 검출하는 이유다. 같은 값끼리 바꾸면 문자열 자체가 달라지지 않는다. 이 논증은 slide의 검출 보장을 풀어 쓴 해설이다.

UPC에서는 같은 weight를 가진 위치가 반복된다. 강의의 $x_6,x_8$은 둘 다 weight 1이므로 바꾸어도 합이 같다. 같은 `036000291452`에서 6번 자리 0과 8번 자리 9를 교환해도 checksum은 변하지 않는다. 따라서 UPC가 모든 transposition을 검출한다고 하면 틀린다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 36:48]]

ISBN-10의 더 강한 검출 능력도 오류 위치를 항상 알아내거나 임의의 손상을 correction한다는 뜻은 아니다. Correction에는 여러 후보 중 원래 메시지를 하나로 정할 수 있을 만큼의 구조가 필요하다. 그 구조를 polynomial의 evaluations로 만드는 방법이 Reed–Solomon encoding으로 이어진다.

## 핵심 정리

- **검출과 복구는 다르다.** 검사식의 실패는 오류를 알리지만 원래 값이나 오류 위치까지 정하지는 않는다. 검사를 통과해도 여러 오류가 상쇄되었을 수 있다.
- **오류 모형이 보장을 결정한다.** 위치가 알려진 소실과 위치를 모르는 값 변경을 구분한다. 반복 전송의 majority 조건을 소실 개수의 한계로 옮기지 않는다.
- **추가량의 비용을 함께 센다.** Parity는 한 check bit를 더하고, 3회·5회 반복은 전체 전송량이 각각 3배·5배가 된다. 보낼 정보량, 허용 오류, code 크기는 함께 고려해야 한다.
- **검산식의 보장은 역원에서 나온다.** UPC의 weights 1·3은 mod 10에서 가역이고 ISBN-10의 weights 1,…,10은 mod 11에서 서로 다른 nonzero 원소다. 이 차이가 단일 변경과 자리 교환의 검출 범위를 설명한다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 추가 정보가 해결하는 문제

위치가 표시된 packet 소실, 도착한 packet의 값 변경, 오류 검출, 원래 값 복구를 구별하라. 추가 구조 없이 임의의 1MB만 보낼 때 보편적인 복구가 어려운 이유와 ECC의 설계 목표를 설명하라. 영상 buffering만으로 bit corruption이 있었다고 결론낼 수 있는가?

<details><summary>해설 보기</summary>

소실은 어느 좌표의 값이 없는 상황이고 값 변경은 값은 도착했지만 틀렸을 수 있는 상황이다. 검출은 오류의 존재를 알아내는 일, 복구는 올바른 원래 값을 정하는 일이다. 수신한 임의의 bit string만으로는 그것이 원래 메시지인지 다른 메시지가 손상된 결과인지 항상 구별할 수 없다. Redundancy는 전송값에 제약을 더해 이 구별에 쓸 정보를 제공한다.

설계에서는 원래 정보량, 전송 overhead와 code 크기, 허용할 소실·값 변경 수, 복구 효율을 함께 본다. 강의는 이 trade-off와 이론적 한계의 존재를 소개했지만 특정 bound를 증명하지 않았다. 전기적 간섭 등의 설명은 오류 동기이지 장치별 측정 오류율이 아니다. Buffering은 필요한 전송량과 실제 전달량 차이로도 생길 수 있으므로 그 현상만으로 bit corruption이나 특정 ECC 구현을 확정할 수 없다.

**채점·확인:** 소실과 값 변경, 검출과 복구를 각각 구분하고, 추가 정보의 필요를 “임의 데이터의 보편적 복구”라는 조건과 함께 설명한다.

</details>

#### 확인 Q02 · Even parity의 계산과 한계

데이터 `1011001`에 even-parity check bit를 붙여라. 수신값 `10110011`을 검사하고, 홀수·짝수 개 bit flip에 대한 보장과 오류 위치를 알아낼 수 있는지를 설명하라.

<details><summary>해설 보기</summary>

Hamming weight는 1의 개수다. 데이터의 weight가 4이므로 check bit는 0이고 전송 문자열은 `10110010`이다. 수신값 `10110011`의 weight는 5여서 even-parity 규칙을 어긴다.

한 번 뒤집을 때마다 weight의 짝·홀이 바뀌므로 홀수 개의 서로 다른 bit flip은 검출된다. 짝수 개가 뒤집히면 짝·홀이 유지되어 놓친다. 오류가 있다고 해도 어느 bit를 고칠지는 알 수 없다. 예를 들어 이 수신값의 서로 다른 한 bit를 각각 뒤집어도 여러 even-parity 문자열이 생긴다. 따라서 한 bit 오류 검출과 한 bit 오류 복구를 같은 보장으로 말하면 안 된다.

**채점·확인:** 4→check bit 0, 수신 weight 5를 계산하고, 홀수 flip 검출·짝수 flip 누락·위치 미식별을 모두 설명한다.

</details>

#### 확인 Q03 · Repetition에서 값 변경과 소실

같은 bit를 3회 또는 5회 전송할 때 majority가 보장하는 bit-flip 허용 수와 비용은 무엇인가? 수신 `0,1,0`과 세 복사본 중 두 개가 소실된 `?,0,?`를 각각 해석하라.

<details><summary>해설 보기</summary>

3회 반복은 같은 원본 bit의 세 복사본 중 최대 한 개가 뒤집혀도 두 개의 정상 값이 다수여서 복구한다. 따라서 `0,1,0`은 이 가정 아래 원래 0이다. 5회 반복은 최대 두 개가 뒤집혀도 정상 세 개가 다수다. 전체 전송량은 각각 원래의 3배·5배이고 추가량은 2배·4배다.

소실 위치가 표시되고 남은 복사본은 정확하다는 별도 가정에서는 `?,0,?`의 한 정상 복사본만으로 0을 복구한다. 반면 세 복사본 중 두 개의 값이 뒤집히면 틀린 값이 다수가 될 수 있다. “두 개까지는 복구할 수 없다”를 두 소실의 보편적 한계로 옮기면 이 두 모형을 섞게 된다.

**채점·확인:** 3회/1 flip, 5회/2 flips와 비용을 맞히고, 알려진 소실에서는 한 정상 복사본으로 충분하다는 조건을 명시한다.

</details>

#### 확인 Q04 · UPC를 계산하고 단일 변경을 검출하기

11자리 데이터 `03600029145`에 UPC check digit을 붙여라. 홀수 위치 weight 3, 짝수 위치 weight 1을 쓰는 mod 10 식으로 단일 자리 변경이 반드시 검출되는 이유도 증명하라.

<details><summary>해설 보기</summary>

앞 11자리 가중합은
$$
3\cdot0+3+3\cdot6+0+3\cdot0+0+3\cdot2+9+3\cdot1+4+3\cdot5=58.
$$
따라서 $58+x_{12}\equiv0\pmod {10}$에서 $x_{12}=2$, 완성 문자열은 `036000291452`다. 맨 앞 0도 한 자리이므로 지우면 안 된다.

한 자리만 서로 다른 decimal digit으로 바뀌면 변화량 $\Delta\not\equiv0\pmod {10}$이다. Checksum 변화는 $w\Delta$이고 $w=1$ 또는 3이다. 둘 다 mod 10에서 역원을 가지므로 $w\Delta=0$이라면 $\Delta=0$이어야 해 모순이다. Check digit 변경도 weight 1인 같은 논증으로 검출한다. 이 증명은 변경 위치를 찾아 주지는 않는다.

**채점·확인:** 가중합 58·check digit 2·선행 0을 보존하고, weight의 가역성을 이용해 단일 변경 검출을 보인다.

</details>

#### 확인 Q05 · 알려진 빈 자리의 복구

유효한 UPC `03?000291452`에서 세 번째 자리 하나만 소실되었고 다른 자리는 정확하다. 빈 자리를 복구하라. 위치를 모르는 삭제나 두 자리 오류에도 같은 보장을 적용할 수 있는가?

<details><summary>해설 보기</summary>

빈 자리의 weight는 3이다. 나머지 가중합은 $3+6+9+3+4+15+2=42$이므로
$$
3x+42\equiv0\pmod {10},\qquad 3x\equiv8\pmod {10}.
$$
$3^{-1}\equiv7$을 곱하면 $x\equiv56\equiv6\pmod {10}$이다. Decimal digit 0,…,9 중 유일한 값은 6이다.

이 복구는 빈 위치가 정확히 알려져 weights를 올바르게 배정하고, 나머지 값은 맞다는 가정에 의존한다. 위치 미상의 삭제는 자리 이동까지 생길 수 있어 같은 식의 보장으로 다룰 수 없다. 두 미지 값에는 이 한 검사식만으로 일반적으로 유일한 복구를 보장하지 못하고, 두 변경은 서로 상쇄될 수도 있다.

**채점·확인:** 합 42, 역원 7, 복구값 6을 검산하고 “알려진 한 자리·나머지 정확”의 조건을 함께 쓴다.

</details>

#### 확인 Q06 · ISBN-10의 X와 단일 변경

ISBN-10의 $x_{10}\equiv\sum_{i=1}^9 i x_i\pmod {11}$에서 나머지 10은 어떻게 표시하는가? 계산용 앞 9자리 `100000001`의 check symbol을 구하고, 열 자리의 weights로 다시 써서 단일 변경 검출을 설명하라.

<details><summary>해설 보기</summary>

나머지 10은 대문자 `X`다. 주어진 계산용 문자열의 합은 $1\cdot1+9\cdot1=10$이므로 check symbol은 `X`다. 이는 검사식을 연습하기 위한 문자열이며 실제 도서 식별번호라고 주장하는 예가 아니다.

식을 $\sum_{i=1}^9 i x_i-x_{10}\equiv0\pmod {11}$로 쓰면 $-1\equiv10$이므로 열 자리 weights는 1,…,10이다. 실제로 예제는 $1+9+10\cdot10=110\equiv0$이다. 한 자리의 다른 허용 symbol로의 변경 $\Delta\ne0\pmod {11}$에 대해 weight $i\ne0$이고, mod 11은 field여서 $i\Delta\ne0$이다. 따라서 단일 변경이 검출된다.

**채점·확인:** X=10을 명시하고, weight −1과 10의 동치를 이용해 예제와 단일 변경 증명을 모두 확인한다.

</details>

#### 확인 Q07 · 서로 다른 두 자리의 교환

ISBN-10에서 서로 다른 위치 $i,j$의 서로 다른 값 $a,b$를 교환하면 왜 검출되는가? UPC 예제 `036000291452`의 6번째와 8번째 자리를 바꾸는 경우와 비교하라.

<details><summary>해설 보기</summary>

교환 전 해당 합은 $ia+jb$, 후에는 $ib+ja$이므로 변화는 $(i-j)(b-a)\pmod {11}$이다. 위치 1,…,10에서 서로 다른 weights의 차이와 서로 다른 허용 symbol의 차이는 모두 mod 11에서 nonzero다. Field에서는 두 nonzero 원소의 곱도 nonzero이므로 ISBN-10 검사가 실패한다. 같은 값끼리의 교환은 문자열 변화 자체가 없다.

UPC의 6번째 값 0과 8번째 값 9는 둘 다 weight 1을 가진다. 두 값을 바꾸면 기존 $0+9$가 $9+0$이 되어 가중합이 그대로라 검출되지 않는다. ISBN-10의 검출 보장도 어느 위치가 잘못되었는지 알아내는 일반 복구 보장은 아니다. 다른 길이의 ISBN에 이 식을 그대로 적용하지 않는다.

**채점·확인:** 변화량을 직접 유도하고, ISBN의 prime modulus·서로 다른 weights와 UPC의 같은 weights를 대조한다.

</details>

### 적용 연습

#### 연습 P01 · 검사 통과가 무오류를 뜻하지 않는 사례

**새로 작성한 강의 기반 일반 연습.** 이 checksum 주제와 직접 대응하는 제공된 기출 문항이 없어 기출 형식으로 분류하지 않는다. UPC `036000291452`에서 (a) 첫 자리만 0→1로, (b) 첫 자리 0→1과 두 번째 자리 3→0을 함께 바꾼다. 두 경우의 checksum과 검출 여부를 계산하고, (b)가 ISBN-10의 “서로 다른 두 자리 교환” 정리에 대한 반례인지 판단하라.

<details><summary>해설 보기</summary>

원래 가중합은 $58+2=60$이다.

(a) 첫 자리의 weight는 3이므로 변화는 $3(1-0)=3$이다. 새 합 63은 mod 10에서 3이어서 오류가 검출된다.

(b) 두 번째 자리의 변화는 $1(0-3)=-3$이다. 두 변화가 합쳐 0이므로 문자열 `106000291452`의 합은 여전히 60이다. 오류 두 개가 있지만 검사를 통과한다. 이는 검사 통과가 무오류 증명이 아님을 보여 준다.

이 사례는 UPC 식이며, 바뀐 값 쌍 $(0,3)\to(1,0)$도 단순 교환이 아니다. 따라서 ISBN-10의 서로 다른 두 symbol 교환 검출 정리와 모순되지 않는다.

**채점·확인:** 63과 60을 구하고, 오류의 개수뿐 아니라 검사 체계와 변경 종류까지 정리의 가정과 비교한다.

</details>

#### 연습 P02 · 전송 비용을 내고 얻는 보장

**새로 작성한 강의 기반 일반 연습.** 직접 대응하는 제공된 기출 근거가 없어 기출형으로 부르지 않는다. 100 data bits를 (A) 한 even-parity bit를 추가해 보내거나 (B) 각 bit를 3회, (C) 각 bit를 5회 반복한다. 추가 framing 비용은 무시한다. 전송량을 계산하고, “각 원본 bit의 복사본 그룹에서 최대 두 bit flip”과 “각 3-copy 그룹에서 두 known-position erasures, 나머지는 정확”을 각각 어느 보장으로 처리할지 설명하라.

<details><summary>해설 보기</summary>

전송량은 A가 101 bits, B가 300 bits, C가 500 bits다. A의 parity는 한 flip 같은 홀수 flip의 검출을 제공하지만 위치를 정하지 못해 복구하지 못하며, 짝수 flip은 놓칠 수 있다.

각 복사본 그룹의 최대 두 flip에는 C가 정상 세 개를 유지하므로 majority 복구를 보장한다. B에서는 원래 0의 `000`이 `110`으로 바뀌면 틀린 1이 다수가 되므로 보장하지 못한다.

두 소실이 위치와 함께 표시되고 남은 복사본은 정확한 B 그룹은 한 값만 남아도 복구한다. 이는 두 flip의 사례와 다르다. 더 많은 추가량은 이 사례에서 더 강한 flip 허용량을 주지만, 이 비교만으로 모든 code의 최적 overhead나 일반 bound를 구한 것은 아니다.

**채점·확인:** 101·300·500을 계산하고, 두 flip에는 5회 반복, 두 알려진 소실에는 3회 반복의 한 정상 복사본을 근거로 든다.

</details>

### 복습 순서

Q01에서 소실·값 변경과 검출·복구를 먼저 구분한다. Q02–Q03의 보장을 오류 모형별로 표 없이 말해 본 뒤 Q04–Q07의 checksum 계산과 증명을 가리고 다시 푼다. 마지막에는 P01의 상쇄 예와 P02의 전송 비용을 이용해 “검사 통과”와 “복구 보장”을 구별한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 19:40–24:06 오류 동기·parity, 31:10–39:37 repetition·UPC·ISBN·trade-off, 43:12–44:09 혼재한 오류 모형, 48:35 통신량 예. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - Parity와 check digits: [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-011)
  - Packet 복구의 동기: [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-012)

### 읽을 때의 범위

- 2026-09-28 녹취와 해당 강의자료의 범위를 사용한다. 소자의 오류 원인은 일반 동기이며 특정 장치의 측정 오류율이나 coding bound는 제시되지 않았다.
- 녹취에서 parity를 correction이라고 부른 대목은 뒤의 “고칠 수 없다”는 설명 및 자료 p.10의 detection과 구별한다. 손상된 token을 보충하거나 불확실한 발화를 복원한 것으로 제시하지 않는다.
- Repetition의 bit-flip majority와 알려진 위치의 erasure를 분리한다. 43:12–44:09의 혼재한 표현을 두 소실 복구 불가능이라는 일반 명세로 채택하지 않는다.
- UPC는 decimal digit과 알려진 한 빈 자리의 모형이다. bit·우편 시스템·deletion이라는 발화를 위치 미상 삭제 복구, 두 자리 오류 복구 또는 모든 자리 교환 검출로 확대하지 않는다.
- ISBN 증명은 ISBN-10의 mod 11 식에 한정한다. 검사식의 성공은 무오류나 일반 correction의 증명이 아니다.
- Video buffering은 통신량의 동기일 뿐 특정 bit corruption이나 ECC 구현을 입증하지 않는다. 계산·검출 증명은 완성된 본문의 해설을 회상하는 내용이다.
