---
title: "다항식 보간과 Secret Sharing"
description: "Field 위 보간, threshold 복구와 균등·독립 계수의 privacy 논증을 복습한다."
course: "discrete_mathematics"
unit_id: "polynomial-secret-sharing"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["04. Number Theory Applications.pdf", "03. Number Theory.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-28-lecture-06", "courses/discrete_mathematics/lectures/2026-09-23-lecture-05"]
---

Secret을 다항식의 상수항에 두고 서로 다른 좌표의 값으로 나누어 보관한다. 충분한 shares의 복구와 적은 shares의 정보 비노출을 각각 증명한다.

## Secret Sharing: 충분한 Share로만 비밀을 복구하는 구성

Secret Sharing(비밀 분산)은 secret 하나를 여러 사람이 나누어 보관하게 한다. $k$-out-of-$n$ 방식에서 $1\le k\le n$이고, 요구는 두 가지다. 올바른 shares를 가진 임의의 $k$명은 secret을 복구해야 한다. 반면 $k-1$명 이하는 shares를 모두 모아도 secret에 관한 정보를 얻지 못해야 한다. “정확한 값은 모르지만 홀짝은 안다”면 복구는 못했어도 정보가 샌 것이므로 두 번째 요구를 만족하지 않는다. [NM002 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-009)

[[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: Secret Sharing]]에서는 100명이 정보를 나누고 honest한 50명이 모이면 복구하되 49명까지는 알 수 없는 예로 이 threshold를 설명했다. 여러 열쇠를 함께 사용하는 핵미사일 발사 비유도 공동 승인의 동기다. 특정 실제 장치의 구현을 검증한 사례는 아니다. 녹취의 손상된 임계 인원 표현은 슬라이드의 $k-1$ 조건과 이 50/49 예를 근거로 읽는다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 24:06–25:54]]

### Secret을 constant term에 넣고 나머지 coefficients를 무작위화하기

Prime $q>n$을 고르고 secret $s$를 $\mathbb Z_q$의 원소로 표현한다. 모든 addition과 multiplication은 modulo $q$에서 한다. 다음 polynomial(다항식)을 만든다.

$$P(X)=s+r_1X+\cdots+r_{k-1}X^{k-1}.$$

Coefficients(계수) $r_1,\ldots,r_{k-1}$은 $\mathbb Z_q$ 전체에서 **서로 독립이고 secret과도 독립인 uniform distribution**으로 선택한다. 0도 허용한다. 따라서 degree(차수)는 항상 $k-1$인 것이 아니라 $\deg P<k$다. 최고차 coefficient가 0이 될 수 있다는 사실은 오류가 아니라 이 random choice의 일부다. 녹취의 “degree $k-1$”보다 슬라이드의 degree bound를 정확히 사용하는 이유다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 25:54–27:19]]

사람 $i$에게는 share $s_i=P(i)$를 준다. Share는 **좌표 $i$와 그 값**을 함께 알아야 의미가 있다. $q>n$이면 $1,\ldots,n$은 field 안에서 서로 다른 nonzero 좌표다. 좌표를 modulo $q$에서 중복시키면 안 된다. 특히 0을 일반 share의 좌표로 주면 $P(0)=s$를 그대로 넘겨주므로 비밀성이 사라진다.

구성을 이해하기 위한 작은 예로 $q=7,k=2,s=3$에서 이번에 뽑힌 coefficient가 $r_1=2$라고 하자. 그러면 $P(X)=3+2X$이고 shares $(1,5)$, $(2,0)$을 만든다. Share 값 0은 허용된다. 피해야 하는 것은 **좌표 0**이다. 이 예와 다음 계산은 강의 원리를 풀어 쓴 pedagogical examples이며 강의에서 그대로 낸 문제는 아니다.

## Lagrange interpolation: 서로 다른 점으로 Polynomial 복구하기

### Field와 degree bound가 필요한 이유

두 점으로 직선을, 세 점으로 degree 2 이하의 polynomial을 정한다는 직관을 일반화하면, 서로 다른 $k$개 좌표의 값이 degree $<k$인 polynomial을 정한다. 정확히 $k-1$차여야 하는 것은 아니다. 또한 식의 개수와 미지수 개수가 같다는 사실만으로 유일성을 얻는 것도 아니다. 좌표가 서로 달라야 하고, 필요한 나눗셈이 가능한 field(체)에서 계산해야 한다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 28:11–30:11]]

Prime $q$의 $\mathbb Z_q$에서는 모든 nonzero 원소가 $q$와 서로소이므로 multiplicative inverse를 갖는다. 이 선수 개념은 [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: Modular inverse의 조건]]과 [M008 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)를 연결하면 된다. Composite modulus에서는 서로 다른 좌표의 차이가 nonzero여도 inverse가 없을 수 있다.

### 보간식의 각 항은 한 점만 선택한다

서로 다른 $x_1,\ldots,x_k$와 값 $y_i=P(x_i)$가 있다고 하자. Lagrange interpolation(라그랑주 보간)을 식으로 전개하면

$$
\ell_i(X)=\prod_{j\ne i}\frac{X-x_j}{x_i-x_j},\qquad
P(X)=\sum_{i=1}^{k}y_i\ell_i(X).
$$

여기서 division은 field inverse를 곱한다는 뜻이다. $x_i-x_j\ne0$이므로 모든 분모가 invertible이다. $X=x_i$에서는 $\ell_i=1$이고 다른 좌표 $x_j$에서는 분자에 0이 생겨 $\ell_i=0$이다. 따라서 합에 $X=x_i$를 넣으면 $y_i$ 하나만 남는다. 각 항의 degree는 $k-1$ 이하이므로 요구한 degree bound도 만족한다. 이는 자료가 이름으로 제시한 보간 원리를 풀어 쓴 유도다.

유일성에는 field 위 polynomial의 root 수 성질을 사용한다. Nonzero degree $d$ polynomial은 서로 다른 roots를 최대 $d$개만 갖는다. Root $a$ 하나마다 factor $X-a$를 분리할 수 있고 degree가 하나 줄어들기 때문이다. 다른 $Q$도 같은 $k$개 값을 주면 $P-Q$는 degree $<k$인데 roots가 $k$개이므로 zero polynomial이어야 한다. 따라서 $P=Q$다.

앞의 $\mathbb Z_7$ 예에서는 두 shares $(1,5),(2,0)$으로 slope를 구하면

$$r_1=\frac{0-5}{2-1}\equiv2\pmod7,\qquad s=5-2=3.$$

복구한 뒤 secret은 constant term $P(0)$이다. $X$의 coefficient를 읽는 것이 아니다. 녹취의 일차항·상수항을 둘러싼 손상된 표현은 위 식으로 수학적 의미를 명확히 하되, 발화를 복원했다고 주장하지 않는다.

### 세 share의 복구와 같은 값의 의미

이전 강의 노트의 해설 예를 이어서 $\mathbb Z_{17}$에서 $n=5,k=3,s=5$, 이번 random coefficients를 $r_1=2,r_2=3$으로 두면

$$P(X)=5+2X+3X^2\pmod{17}.$$

| 좌표 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| Share | 10 | 4 | 4 | 10 | 5 |

서로 다른 좌표에 같은 share 값이 나와도 괜찮다. 필요한 것은 값들의 distinctness가 아니라 좌표들의 distinctness다. 좌표 1, 2, 3을 모으면

$$
s+r_1+r_2=10,\quad
s+2r_1+4r_2=4,\quad
s+3r_1+9r_2=4
\pmod{17}.
$$

인접한 식을 빼면 $r_1+3r_2=11$, $r_1+5r_2=0$이다. 다시 빼면 $2r_2=6$이고, $2^{-1}=9\pmod{17}$을 곱해 $r_2=3$, 이어서 $r_1=2,s=5$를 얻는다. 여기까지는 올바른 shares의 reconstruction(복구)을 보인 것이다. Threshold 미만의 privacy(비밀성)는 다음의 별도 논증이 필요하다.

## Uniform·independent coefficients가 보장하는 정보 비공개성

### 여러 후보가 남는 것보다 강한 주장

두 shares $(1,10),(2,4)$만 아는 위 예에서는 $5+2X+3X^2$와 $6+9X+12X^2$가 모두 그 점들을 통과한다. 그러나 이 사실만으로 “아무 정보도 없다”고 결론낼 수는 없다. 서로 다른 secret이 여전히 가능하더라도 관측 뒤 특정 secret의 가능성이 높아졌다면 정보가 생겼기 때문이다.

그래서 각 후보 secret에 대해 **같은 관측이 일어날 확률**을 비교한다. 아래 counting argument(경우의 수 논증)는 NM002 p.9의 마지막 “왜 정보가 없는가”를 설명하는 노트 측 증명이며, 강사가 전체를 발화한 것으로 제시하지 않는다.

### 고정된 관측과 양립하는 Polynomial 수 세기

$t<k$개의 서로 다른 nonzero 좌표 $x_1,\ldots,x_t$에서 임의의 share 값 $y_1,\ldots,y_t$를 관측했다고 하자. 후보 secret $s$ 하나를 고정한다.

1. $P(0)=s$와 관측한 $t$개의 값은 고정되어 있다.
2. 0 및 관측 좌표와 다른 nonzero 좌표 $k-1-t$개를 미리 정한다. $q>n\ge k$이므로 필요한 좌표가 존재한다.
3. 이 추가 좌표들의 값을 각각 자유롭게 고르면 $q^{k-1-t}$가지 선택이 있다.
4. 이제 서로 다른 좌표의 $k$개 점이 되었으므로, 앞의 interpolation에 따라 각 선택마다 degree $<k$인 polynomial이 정확히 하나 생긴다.

반대로 고정된 secret과 관측을 만족하는 모든 polynomial은 추가 좌표들의 값을 유일하게 정한다. 따라서 이 세기는 중복도 빠짐도 없다. **어떤 $s$에 대해서도 관측과 양립하는 polynomial 수는 정확히 $q^{k-1-t}$개**다.

Secret $s$를 고정하면 가능한 random coefficient 벡터는 $q^{k-1}$개다. 모든 coefficient가 독립·균등하게 선택되고 secret과도 독립이므로 각 벡터의 조건부 확률은 $q^{-(k-1)}$이다. 따라서

$$
\Pr[Y=(y_1,\ldots,y_t)\mid S=s]
=\frac{q^{k-1-t}}{q^{k-1}}
=q^{-t}.
$$

이 값은 $s$와 무관하다. Secret의 prior distribution이 어떤 것이든 $\Pr[Y=y]=\sum_s\Pr[S=s]q^{-t}=q^{-t}$이고, 가능한 secret에 대해

$$\Pr[S=s\mid Y=y]=\Pr[S=s]$$

가 된다. 관측이 secret의 상대적 가능성을 전혀 바꾸지 않는다. **Secret 자체가 uniform일 필요는 없다.** 필요한 uniformity와 independence는 random coefficients에 대한 조건이다.

$\mathbb Z_7,k=2$의 한 share $(1,5)$에서는 모든 후보 $s$마다 $r_1=5-s$가 하나씩 있으므로 관측 확률이 모두 $1/7$이다. $\mathbb Z_{17},k=3$에서 두 shares를 관측하면 각 secret마다 coefficient pair가 하나씩이고 확률은 $1/17^2$다. $t=0$에서는 빈 관측의 확률이 1이며, $k=1$에서는 threshold 미만인 경우가 이것뿐이다.

Coefficients를 편향되거나 종속되게 선택하면 벡터들이 같은 확률을 갖는다는 단계가 무너진다. 최고차 coefficient 0을 임의로 금지하는 것도 다른 분포다. 좌표 0을 share로 주는 경우는 secret 자체를 보여 주므로 이 증명을 적용할 수 없다.

## Byzantine fault와 올바른 Share라는 전제

강의는 일곱 성 사이로 명령을 전달하는데 일부 성이 점령되어 전달된 명령을 그대로 믿을 수 없는 상황을 동기로 들었다. Byzantine fault(비잔틴 장애)는 불완전한 분산 상황에서 서로 다른 관찰자가 서로 다른 증상을 볼 수 있다는 문제다. 출처가 맞는 명령인지, 전달 중 변조되었는지, 다른 참여자도 같은 정보를 받았는지의 질문이 생긴다. [NM002 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-008), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 17:51–18:47]]

NM002 p.8의 왼쪽 패널에서는 주변 참여자들의 화살표가 모두 중앙 성을 향해 안쪽으로 모인다. 이는 공통 전략에 맞춰 함께 행동하는 상황이다. 오른쪽 패널에는 중앙 성을 향하는 빨간 화살표와 성에서 멀어지는 파란 화살표가 함께 있어, 안쪽으로 향하는 행동과 바깥쪽으로 향하는 행동이 충돌한다. 이 대비는 참여자나 전달 정보를 신뢰할 수 없을 때 행동을 조정하지 못해 공동 전략이 실패할 수 있음을 보여 준다. 녹취의 일곱 성 이야기는 성 사이의 명령 전달을 설명한 별도 비유이므로, 그림을 그 이야기와 같은 배치로 보거나 참여자 수를 성의 수에 대응시키지 않는다. 이 그림은 합의가 필요한 이유를 보여 줄 뿐이며, Secret Sharing이나 ECC만으로 명령의 authentication과 참여자들의 agreement가 보장된다는 뜻은 아니다.

앞의 construction이 보장한 것은 honest한 $k$개 shares의 복구와 그보다 적은 shares의 정보 비공개성이다. 거짓 share가 섞였을 때 누가 거짓말했는지 알아내거나, 명령의 origin을 authentication하거나, 모든 참여자가 agreement에 도달하게 만드는 protocol까지 포함하지 않는다. 같은 좌표를 여러 번 내는 것도 새로운 점을 제공하지 않는다. Polynomial을 쓴다는 공통점 때문에 뒤의 오류 정정과 연결할 수는 있지만, 각 기술이 어떤 오류와 어떤 공격자에 대해 무엇을 보장하는지는 따로 구별해야 한다.

## 핵심 정리

- Threshold의 두 요구는 올바른 $k$개 shares의 복구와 $t<k$개 shares의 정보 비노출이다.
- $P(0)$은 secret이고 일반 share는 서로 다른 nonzero 좌표의 값이다. 값 0은 허용하지만 좌표 0은 secret을 드러낸다.
- Degree는 정확히 $k-1$이 아니라 $<k$다. 무작위 계수는 0을 포함해 field 전체에서 선택한다.
- 보간의 유일성은 field·서로 다른 좌표·degree bound에서 나온다.
- Privacy에는 모든 secret에서 같은 관측의 확률이 같다는 논증이 필요하다. 후보가 여럿이라는 말만으로는 부족하다.
- 이 구성은 거짓 share 식별이나 authentication·Byzantine agreement까지 제공하지 않는다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 불신 참여자와 보장의 경계

일곱 성 사이의 명령 전달과 방향이 엇갈리는 Byzantine 그림은 어떤 문제를 보여 주는가? Secret Sharing이나 ECC가 그 문제를 모두 해결한다고 할 수 있는가?

<details><summary>해설 보기</summary>

일부 참여자·통신을 신뢰할 수 없으면 관찰자마다 다른 메시지를 받아 일관성과 진위를 확신하기 어렵다. 명령이 원래 발신자의 것인지, 변조되었는지, 다른 참여자도 같은 정보를 받았는지의 문제가 생긴다. 일곱 성의 비유와 자료 그림을 정확히 같은 배치로 간주할 필요는 없다.

자료 p.8의 왼쪽은 모든 화살표가 중앙 성으로 모여 하나의 전략에 따른 행동을 나타낸다. 오른쪽은 성을 향하는 빨간 화살표와 반대로 멀어지는 파란 화살표가 섞여 행동이 충돌한다. 따라서 불신 참여자나 불완전한 정보 때문에 공동 전략을 조정하지 못할 수 있다는 대비다. 그림의 참여자 수를 녹취의 일곱 성에 대응시키지 않는다.

Secret Sharing의 threshold 복구·privacy와 ECC의 정해진 오류 모델 아래 복구는 각자의 보장이다. 그것만으로 명령의 origin을 인증하거나 모두의 agreement를 만드는 protocol까지 얻지는 않는다.

**채점·확인:** 왼쪽의 공동 방향과 오른쪽의 충돌을 설명하고 그림과 일곱 성 비유를 구별한다. 동기의 세 질문과 construction의 제한된 보장도 구별한다.

</details>

#### 확인 Q02 · Shares를 만드는 정확한 조건

$k$-out-of-$n$의 두 요구를 적고 prime $q>n$, secret $s\in\mathbb Z_q$로 다항식·shares를 구성하라. 왜 계수 0을 허용하고 좌표 0을 피하는가? 같은 share 값과 같은 좌표도 구별하라.

<details><summary>해설 보기</summary>

임의의 honest한 $k$개 서로 다른 shares로 복구해야 하며 $t<k$개 관측은 secret에 관한 정보를 주지 않아야 한다. 완전 복구가 어렵더라도 홀짝이 드러나면 두 번째 요구는 실패다.

$P(X)=s+\sum_{j=1}^{k-1}r_jX^j$로 두고 $r_j$를 secret과 독립이며 서로 독립인 uniform $\mathbb Z_q$ 값으로 고른다. Share는 $(i,P(i))$, $i=1,\ldots,n$이다. $q>n$이면 좌표가 서로 다른 nonzero field elements다. 0 계수도 허용하므로 $\deg P<k$이며 항상 정확히 $k-1$차일 필요는 없다. $P(0)=s$여서 좌표 0을 주면 secret이 노출된다. 반면 값 0이나 서로 다른 좌표의 같은 값은 괜찮다. 같은 좌표를 반복해도 새 점은 늘지 않는다.

**채점·확인:** 두 요구, randomness의 세 조건, degree bound, 좌표/값의 차이를 모두 확인한다.

</details>

#### 확인 Q03 · Lagrange 식과 유일성

서로 다른 field 좌표 $(x_i,y_i)$, $i=1,\ldots,k$에서 $\deg P<k$인 보간식을 쓰고 왜 존재·유일한지 설명하라. “식과 미지수가 k개라서”만으로 충분한가?

<details><summary>해설 보기</summary>

$\ell_i(X)=\prod_{j\ne i}(X-x_j)/(x_i-x_j)$로 두면 $P(X)=\sum_i y_i\ell_i(X)$다. 서로 다른 좌표와 field 조건 때문에 분모는 nonzero이고 역원이 존재한다. $\ell_i(x_i)=1$, $\ell_i(x_j)=0$이어서 각 점의 값을 재현하며 degree도 $<k$다.

다른 $Q$도 같은 값을 주면 $P-Q$는 degree $<k$이고 서로 다른 roots $k$개를 갖는다. Field 위 nonzero degree $d$ polynomial의 root 수는 최대 $d$이므로 $P-Q=0$이다. Root 하나마다 $X-a$를 분리하면 degree가 줄어드는 것이 이 성질의 이유다. 식 개수만으로는 충분하지 않으며 중복 좌표나 noninvertible 분모가 있으면 논증이 깨진다. 이 전개는 강의 원리를 풀어 쓴 해설이다.

**채점·확인:** 보간식·역원·값 재현·degree와 root-count uniqueness를 모두 제시한다.

</details>

#### 확인 Q04 · 두 share와 한 share

$\mathbb Z_7$에서 degree $<2$인 $P$의 shares가 $(1,5),(2,0)$이면 $P$와 secret을 복구하라. $(1,5)$만 관측한 경우 각 후보 secret의 가능성과, uniform slope일 때 그 관측 확률을 구하라.

<details><summary>해설 보기</summary>

$P=s+rX$라 두면 $r=(0-5)/(2-1)\equiv2$, $s=5-2=3$이다. 따라서 $P=3+2X$이고 secret은 $P(0)=3$이며 coefficient 2가 아니다.

한 share에서는 각 $s\in\mathbb Z_7$마다 $r=5-s$가 정확히 하나씩 있다. Slope를 전체 7개 값에서 균등하게 고르면 $\Pr[Y=5\mid S=s]=1/7$로 모든 secret에서 같다. 후보가 전부 가능하다는 사실에 이 동등한 likelihood를 더해야 정보 비노출을 설명할 수 있다.

**채점·확인:** slope·상수항 검산과 각 s의 유일한 r·1/7을 확인한다.

</details>

#### 확인 Q05 · 세 share의 복구

$\mathbb Z_{17}$에서 degree $<3$인 $P$가 $(1,10),(2,4),(3,4)$를 지난다. 계수를 구하고 같은 share 값이 두 번 나온 것이 왜 문제가 아닌지 설명하라.

<details><summary>해설 보기</summary>

$P=s+r_1X+r_2X^2$라 두면 $s+r_1+r_2=10$, $s+2r_1+4r_2=4$, $s+3r_1+9r_2=4$다. 인접한 식을 빼서 $r_1+3r_2=11$, $r_1+5r_2=0$을 얻는다. 다시 빼면 $2r_2=6$이다. $2^{-1}=9$ modulo 17이므로 $r_2=3$, 이어서 $r_1=2,s=5$다.

검산하면 $P(1)=10$, $P(2)=21\equiv4$, $P(3)=38\equiv4$다. 필요한 distinctness는 좌표에 대한 것이므로 두 값이 4로 같은 것은 문제가 아니다. 복구의 성공 자체가 threshold 미만 privacy의 증명은 아니다.

**채점·확인:** 역원을 사용한 소거·세 값 검산·좌표 distinctness를 확인한다.

</details>

#### 확인 Q06 · Threshold 미만 privacy의 개수 증명

서로 다른 nonzero 좌표에서 $t<k$개의 고정 관측 $y$가 주어졌다. 각 후보 secret $s$와 양립하는 polynomial 수를 세고 $\Pr[Y=y\mid S=s]$를 구하라. Secret 자체가 uniform이 아니어도 posterior가 prior와 같은 이유까지 설명하라.

<details><summary>해설 보기</summary>

$P(0)=s$와 $t$개 관측은 $t+1$개 점을 고정한다. 나머지 $k-1-t$개 서로 다른 nonzero 좌표를 관측 좌표 밖에서 미리 고른다. $q>n\ge k$라 필요한 좌표가 있다. 추가 값의 선택은 $q^{k-1-t}$가지이고 각 선택은 서로 다른 $k$개 점의 보간으로 정확히 한 degree $<k$ polynomial을 정한다. 반대로 조건을 만족하는 polynomial은 추가 값들을 유일하게 정하므로 중복·누락이 없다.

고정 $s$에서 random coefficient 벡터는 $q^{k-1}$개이며 균등·독립 조건에 의해 같은 확률이다. 따라서
$$\Pr[Y=y\mid S=s]=q^{k-1-t}/q^{k-1}=q^{-t}.$$
이 값이 $s$와 무관하므로 임의 prior에 대해서도 $\Pr[Y=y]=\sum_s\Pr[S=s]q^{-t}=q^{-t}$이다. Bayes 식에 넣으면 $\Pr[S=s\mid Y=y]=\Pr[S=s]$다. Secret 자체의 uniformity가 아니라 계수의 uniformity와 independence를 사용했다. 이 counting proof는 본문의 해설 유도다.

**채점·확인:** 추가 좌표 수·일대일 세기·분모·조건부 확률·posterior까지 이어서 설명한다.

</details>

#### 확인 Q07 · 증명의 경계와 random choice

Q06에서 $t=0$ 또는 $k=1$은 어떻게 되는가? 최고차 계수의 0을 금지하거나 계수들이 secret에 의존하도록 바꾸면 왜 같은 privacy 증명을 쓸 수 없는가?

<details><summary>해설 보기</summary>

$t=0$이면 관측과 양립하는 수는 $q^{k-1}$이며 빈 관측 확률은 1이다. $k=1$에서는 threshold 미만인 경우가 $t=0$뿐이다. 이때 $P=s$이고 한 share로 복구한다.

최고차 계수의 0을 금지하면 전체 coefficient 벡터가 $q^{k-1}$개라는 설정을 바꾼다. 편향·종속 선택이나 secret 의존이 있으면 고정 secret에서 벡터들이 같은 확률을 갖는다는 단계가 깨진다. 후보 secret이 여러 개 남는 것만으로 posterior가 유지된다고 할 수 없다. 좌표 0을 관측하면 secret 자체를 알므로 nonzero 조건도 필수다.

**채점·확인:** 두 경계값, 개수와 확률 단계, 좌표 조건을 각각 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 정확한 차수를 강제한 대가

**새로 만든 강의 기반 일반 연습.** Polynomial secret sharing·privacy의 직접 기출 근거는 없다.

$\mathbb Z_7,k=2$에서 “항상 직선이어야 한다”며 $P(X)=s+rX$의 $r$을 $1,\ldots,6$에서만 균등하게 고른다. Share $(1,5)$를 관측했을 때 secret에 관한 정보가 생기는지 계산하라. $r=0$도 허용하는 원래 구성과 비교하라.

<details><summary>해설 보기</summary>

관측 조건은 $r=5-s$다. $s=5$면 $r=0$이 필요하지만 금지되어 관측 확률은 0이다. 다른 여섯 secret에는 허용된 $r$ 하나씩이 대응하므로 관측 확률은 각각 $1/6$이다. 따라서 관측은 secret 5를 배제해 정보를 준다. 예를 들어 원래 secret이 uniform이었다면 posterior는 5에 0, 나머지에 $1/6$으로 바뀐다.

$r=0,\ldots,6$ 모두에서 uniform하게 고르면 모든 secret에 관측 확률 $1/7$이 된다. Degree를 정확히 1로 강제하는 변경은 단순 표기 문제가 아니라 randomness와 privacy를 바꾸는 일이다.

**채점·확인:** s=5의 배제, 0 대 1/6, 원래 1/7과 posterior의 변화를 검산한다.

</details>

#### 연습 P02 · 서로 맞지 않는 shares

**새로 만든 강의 기반 일반 연습.** 거짓 share와 reconstruction 조건을 직접 다루는 기출 근거는 없다.

$\mathbb Z_7,k=2$에서 $(1,5),(2,0),(3,1)$을 받았다. 첫 두 점과 첫째·셋째 점으로 각각 secret을 구하고, “세 사람이 모였으므로 모두 믿고 같은 답을 낸다”는 주장을 평가하라. 어느 사람이 거짓말했는지 이 구성만으로 확정할 수 있는가?

<details><summary>해설 보기</summary>

첫 두 점은 Q04처럼 $P=3+2X$를 주어 secret 3이다. 이 다항식은 좌표 3에서 $9\equiv2$를 주므로 수신값 1과 불일치한다.

첫째·셋째로 구한 slope는 $(1-5)/(3-1)\equiv3\cdot4\equiv5$, 상수항은 $5-5=0$이다. 따라서 $P=5X$, secret 0이며 좌표 2의 예측값은 3이라 수신값 0과 다르다. 서로 다른 두 점의 보간은 각각 가능하지만 모두가 올바른 shares라는 전제가 깨졌다.

여러 값이 일관되지 않음을 확인할 수는 있어도 이 threshold construction만으로 원래 secret이나 거짓 참여자를 확정할 수 없다. Honest한 shares의 복구 보장과 인증·오류 정정은 별개의 요구다.

**채점·확인:** 두 slope·secret·불일치 값, honest 가정과 식별 한계를 확인한다.

</details>

### 복습 순서

Q02–Q05로 구성과 보간을 먼저 확인한 다음 Q06의 개수 비율을 스스로 유도한다. Q07·P01에서 randomness 조건이 빠진 경우를 점검하고 P02에서 honest-share 전제를 검사한다. 다음 날 복구와 privacy의 근거를 각각 한 문단으로 써 본다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트 · 2026-09-23 · 이산수학 5강]]
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 17:51–18:47 불신 참여자; 24:06–27:19 threshold·구성; 28:11–30:11 보간. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - Byzantine 동기와 threshold 구성: [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-009)
- [03. Number Theory.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)
  - Field 계산의 합동·역원 선수 복습: [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-005), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

### 읽을 때의 범위

- 9월 28일의 구성과 보간을 중심으로 하며 9월 23일 modular inverse가 선수 내용이다. 보간식·root-count·uniform-independent 계수의 counting privacy proof는 강의의 원리를 풀어 쓴 해설이다.
- 1≤k≤n, prime q>n, 서로 다른 nonzero 좌표, secret과 독립인 균등·독립 계수를 전제한다. 최고차 계수 0을 허용해 degree<k를 쓴다.
- 복구에는 honest한 shares가 필요하다. 거짓 share의 식별·authentication·Byzantine agreement protocol을 이 구성에 포함하지 않는다.
- 녹취의 k−1·상수항·방정식 일부는 손상되어 있다. 정돈한 식을 정확한 음성 복원으로 주장하지 않으며 핵미사일·성의 비유는 실제 구현 검증이 아니다.
- 직접 대응하는 기출이 없어 일반 연습으로 구성했다. 보정 녹취의 불확실성과 음성 누락 가능성을 새로 해소한 것은 아니다.
