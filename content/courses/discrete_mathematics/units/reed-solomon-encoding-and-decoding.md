---
title: "Reed–Solomon 부호화와 다항식 Decoding"
description: "Reed–Solomon의 소실·오류 복구 조건과 Berlekamp–Welch의 선형화·몫 유일성을 계산과 증명으로 점검한다."
course: "discrete_mathematics"
unit_id: "reed-solomon-encoding-and-decoding"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["04. Number Theory Applications.pdf", "03. Number Theory.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-28-lecture-06"]
---

메시지 계수를 여러 좌표의 다항식 값으로 바꾸면 일부 값이 사라지거나 바뀌어도 구조를 이용해 복구할 수 있다. 소실과 값 변경의 조건을 나눈 뒤 보조 다항식의 선형식에서 원래 메시지가 유일하게 돌아오는 이유를 확인한다.

## Reed–Solomon encoding: Message를 Polynomial에 담기

Reed–Solomon code의 아이디어는 메시지를 polynomial의 coefficients로 담고, 그 polynomial을 여러 좌표에서 계산한 값들을 보내는 것이다. 일부 값이 손상되어도 남은 구조로 원래 polynomial을 복구한다. 슬라이드 제목에 이름이 없더라도 강의에서는 이를 Reed–Solomon이라고 명시했다. [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: Reed–Solomon과 Decoding]], [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 42:21]]

이 단원은 field 위 interpolation을 사용한다. 서로 다른 $n$개 좌표의 올바른 값은 degree $<n$인 polynomial 하나를 정한다. 필요한 분모의 inverse와 degree에 따른 root 수가 그 이유다. 이 선수 개념은 같은 [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: Lagrange interpolation]]에서 연결할 수 있다.

### Coefficients와 전송하는 Evaluations의 구별

메시지 symbols $a_0,\ldots,a_{n-1}$을 prime $q$의 $\mathbb Z_q$ 원소로 표현하고

$$P(X)=a_0+a_1X+\cdots+a_{n-1}X^{n-1},\qquad\deg P<n$$

을 만든다. 전송하는 것은 coefficients 자체가 아니라 서로 다른 좌표 $\beta_i$에서 얻은 evaluations $c_i=P(\beta_i)$다. Receiver는 각 값이 어느 좌표에 속하는지 알아야 한다. Secret Sharing에서는 secret 하나를 constant term에 두고 나머지 coefficients를 random하게 만들었지만, 여기서는 **전체 메시지가 coefficients**다. [NM002 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-013), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 44:09–45:56]]

이하에서는 자료의 $n$을 원래 message symbol 수로 쓴다. 녹취의 $m/n$ 혼용과 일부 빠진 subscripts를 완전한 발화로 복원한 표기는 아니다.

## Erasure와 General error: 위치를 아는가가 바꾸는 추가량

### 알려진 소실 위치에는 $n+k$개 evaluations

Erasure(소실)에서는 값이 없지만 receiver가 어느 위치가 비었는지 알고, 남은 값들은 올바르다. Sender가 미리 어느 packet이 없어질지 모르는 것과 receiver가 수신 뒤 빈 좌표를 식별하는 것은 별개다. 강의의 100개 중 2개 소실 예도 이 구별로 읽는다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 40:30–41:28]]

Degree $<n$인 $P$를 서로 다른 $n+k$개 좌표에서 계산해 보내면, 최대 $k$개 erasures 뒤에도 적어도 $n$개의 올바른 coordinate-value pairs가 남는다. 그중 임의의 $n$개로 interpolation하여 $P$를 복구한 뒤 coefficients를 읽으면 된다. 추가량은 $k$ symbols다. [NM002 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-013), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 46:41–47:40]]

예를 들어 $\mathbb Z_7$에서 message $(2,3)$은 $P(X)=2+3X$다. $n=2,k=1$로 좌표 $1,2,3$의 값 $5,1,4$를 보낸다. 좌표 2의 packet을 잃어도 $(1,5),(3,4)$에서 slope는 $(4-5)/(3-1)=6\cdot4\equiv3\pmod7$이고, constant term은 $5-3=2$다. 이 계산은 강의의 구성을 보여 주는 해설용 예다. 남은 두 값 중 하나가 거짓이면 이 보장은 적용되지 않는다.

### 위치를 모르는 corruption에는 $n+2k$개 evaluations

General error에서는 packet이 도착했지만 값이 바뀌었을 수 있어 어느 값이 옳은지 모른다. 최대 $k$개의 unknown-position corruptions를 고치는 설정에서는 같은 $P$를 서로 다른 $n+2k$개 좌표에서 평가한다. 전송값을 $c_i$, 수신값을 $c'_i$라 하자. Prime 기호는 derivative가 아니라 수신값을 표시한다. 적어도 $n+k$개는 $c_i=c'_i$지만 receiver는 그 위치를 모른다. [NM002 pp.14–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 49:35–52:16]]

따라서 아무 $n$개를 골라 interpolation하는 방법은 안전하지 않다. 잘못된 값이 섞인 점들도 어떤 degree $<n$의 polynomial을 정할 수 있지만 그것이 원래 메시지일 이유가 없다. 대신 찾으려는 후보 $Q$에 다음 조건을 요구한다.

$$\deg Q<n,\qquad Q(\beta_i)=c'_i\text{인 좌표가 적어도 }n+k\text{개}.$$

그 일치 좌표들 중 최대 $k$개만 오류일 수 있으므로 적어도 $n$개에서는 $Q(\beta_i)=c_i=P(\beta_i)$다. Degree $<n$인 $P-Q$가 서로 다른 $n$개의 roots를 가지므로 zero polynomial이고, $Q=P$다. 이것이 이 조건을 만족하는 정답의 유일성이다. **정답이 유일하다는 것과 그 정답을 빠르게 찾는 것은 다른 문제**다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 53:12–55:55]]

## Berlekamp–Welch decoding: 오류 위치를 다항식의 Roots로 표현하기

### Error-locator polynomial이 잘못된 식을 0으로 만든다

오류가 난 좌표들의 조합을 일일이 추측하는 대신 error-locator polynomial(오류 위치 다항식) $E$를 도입한다. 실제 오류 좌표를 모두 포함하도록 $e_1,\ldots,e_k$를 잡고

$$E(X)=\prod_{j=1}^{k}(X-e_j)$$

로 생각한다. Monic은 최고차 coefficient가 1이라는 뜻이다. 실제 오류가 $k$개보다 적으면 다른 좌표를 더해 degree $k$로 만들 수 있다. 아직 receiver가 이 좌표들을 안다는 뜻은 아니다. [NM002 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-016), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 56:45–58:32]]

이렇게 생각한 $E$는 모든 $i$에서

$$P(\beta_i)E(\beta_i)=c'_iE(\beta_i)$$

를 만족한다. 오류 위치에서는 $E(\beta_i)=0$이라 양변이 0이다. 정상 위치에서는 원래 $P(\beta_i)=c'_i$라 양변이 같다. 어느 위치가 정상인지 몰라도 하나의 등식으로 두 경우를 표현하게 된 것이다.

### $R=PE$로 바꾸면 미지 coefficients에 대한 Linear system이 된다

$P$와 $E$의 coefficients를 동시에 직접 풀려고 하면 그 곱에서 미지수끼리 곱해진다. 대신 새로운 polynomial $R(X)=P(X)E(X)$를 두고 $R$과 $E$의 coefficients를 구한다. Degree 조건은

$$\deg R<n+k,\qquad E(X)=X^k+\sum_{j=0}^{k-1}f_jX^j.$$

$R(X)=\sum_{j=0}^{n+k-1}r_jX^j$에는 $n+k$개의 unknown coefficients가 있다. Monic $E$에는 leading coefficient를 제외한 $k$개가 unknown이므로 총 $n+2k$개다. 각 수신 좌표의 식을 전개하면

$$
\sum_{j=0}^{n+k-1}r_j\beta_i^j
-c'_i\sum_{j=0}^{k-1}f_j\beta_i^j
=c'_i\beta_i^k.
$$

$\beta_i,c'_i$는 known이므로 이는 $r_j,f_j$에 대한 linear equation이다. 총 $n+2k$개 좌표에서 linear system을 얻는다. Error coordinates $e_j$ 자체를 unknown으로 놓으면 일반적으로 nonlinear한 관계가 되는 것과 대비된다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 59:31–01:06:21]]

NM002 p.16의 첫 등식에는 $c'_i$가 있지만 뒤 linear-system bullet에는 prime이 빠진 $c_i$가 인쇄되어 있다. Decoder가 아는 값은 **수신값 $c'_i$**이므로 여기서는 그 표기를 사용한다. 원본의 표기 누락을 숨기거나 전송값을 이미 아는 것으로 계산해서는 안 된다. 또한 식과 미지수 수가 같다는 사실만으로 consistent하거나 해가 유일하다고 결론낼 수 없다.

## 작은 Decoding 계산: $E,R$에서 Message로 돌아가기

이전 강의 노트의 해설 예를 이어 $\mathbb Z_7$에서 $n=2,k=1$, 좌표 $1,2,3,4$를 사용하자. $P(X)=2+3X$의 전송값은 $(5,1,4,0)$인데 수신값이 $(5,6,4,0)$이라고 하자. Decoder에게는 원래 $P$와 오류 위치가 알려져 있지 않다. 아래는 받은 네 값에서 시작하는 새 설명용 계산이며 실제 강의 문제를 옮긴 것이 아니다.

$$E(X)=X+f_0,\qquad R(X)=r_0+r_1X+r_2X^2$$

로 놓고 $R(\beta_i)=c'_iE(\beta_i)$를 modulo 7에서 쓰면

$$
\begin{aligned}
r_0+r_1+r_2-5f_0&=5,\\
r_0+2r_1+4r_2-6f_0&=5,\\
r_0+3r_1+2r_2-4f_0&=5,\\
r_0+4r_1+2r_2&=0.
\end{aligned}
$$

두 번째 식에서 첫 번째 식을 빼면 $r_1+3r_2-f_0=0$이다. 세 번째 식에서 첫 번째 식을 빼면 $2r_1+r_2+f_0=0$이다. 합치면 $3r_1+4r_2=0$이므로 $r_1=r_2$다. 이어 $f_0=4r_2$, 마지막 식에서 $r_0=r_2$를 얻는다. 첫 식에 대입하면 $4r_2=5$여서 $r_2=3$이다.

결과는 $r_0=r_1=r_2=3,f_0=5$이며

$$
E(X)=X+5,\qquad R(X)=3+3X+3X^2=(X+5)(2+3X)\pmod7.
$$

따라서 polynomial division으로 $R/E=2+3X$를 얻고 coefficients $(2,3)$을 message로 복구한다. 오류가 있던 좌표 2에서는 $E(2)=0$이고, 나머지 좌표에서는 복구한 $P$가 수신값과 같다. 모든 좌표에서 $R(\beta_i)=c'_iE(\beta_i)$가 성립하는지 대입해 검산할 수 있다. 강의의 마지막 복구 단계가 이 quotient 계산이다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:05:26]]

## 해의 존재와 최종 Quotient의 유일성

### 실제 오류 구조가 적어도 하나의 해를 만든다

최대 $k$개 오류라는 가정 아래에서는 실제 message polynomial $P_{\mathrm{true}}$가 존재한다. 실제 오류 좌표를 모두 roots로 포함하는 monic degree $k$의 $E$를 만들고 $R=P_{\mathrm{true}}E$로 두면 모든 식을 만족한다. 이것이 linear system의 consistency를 보장하는 이유다. 식의 개수만 세는 논증과 다르다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:07:19]]

오류 수가 $k$보다 작으면 $E$의 남는 roots를 다른 방식으로 채울 수 있다. 식들 사이에 dependence가 생길 수도 있다. 따라서 $(E,R)$ 자체는 유일하지 않을 수 있다. 하지만 우리가 복구하려는 것은 이 보조 pair가 아니라 message polynomial이다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:08:09]]

### 어떤 해를 골라도 같은 $P$가 나오는 이유

강의는 quotient가 같다는 세부 증명을 스스로 확인하도록 남겼다. 다음은 그 질문에 대한 노트 측 전개다. 임의의 해 $(R,E)$를 고르고

$$D(X)=R(X)-P_{\mathrm{true}}(X)E(X)$$

를 보자. Degree는 $n+k$보다 작다. 적어도 $n+k$개의 정상 좌표에서는 $c'_i=P_{\mathrm{true}}(\beta_i)$이므로

$$
D(\beta_i)=c'_iE(\beta_i)-P_{\mathrm{true}}(\beta_i)E(\beta_i)=0.
$$

Degree $<n+k$인 polynomial이 서로 다른 $n+k$개 이상의 roots를 가지므로 $D$는 zero polynomial이다. 따라서 $R=P_{\mathrm{true}}E$다. $E$는 monic이어서 zero polynomial이 아니므로 나눗셈의 나머지는 0이고 quotient는 항상 $P_{\mathrm{true}}$다. 보조 해가 여러 개라는 사실과 복구 결과가 하나라는 사실은 양립한다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:09:01]]

이 증명에는 field, distinct coordinates, degree 제한, 최대 $k$개 corruption이라는 조건이 모두 쓰였다. 오류가 그보다 많을 때도 같은 성공 보장을 적용하거나, 해를 얻었다는 이유만으로 모든 가정이 검증되었다고 말할 수 없다. 일반 linear-system 구현과 전체 bit complexity까지 이 강의에서 전개한 것은 아니다.

## Binary finite field: 원소 수와 연산 구조는 다르다

Encoding과 decoding에는 충분히 많은 서로 다른 field elements가 필요하다. 일반 오류 설정에서는 $n+2k$개 좌표가 필요하다. 좌표 0도 허용한다면 field size가 적어도 $n+2k$이면 된다. Prime field에서 $1,\ldots,n+2k$를 모두 nonzero 좌표로 택하려면 $q>n+2k$가 충분하다. 강의의 엄격한 부등식은 이런 선택과 연결해 읽을 수 있다. Secret Sharing에서는 $P(0)$가 secret이어서 0 share를 피하지만, coefficients 전체를 message로 쓰는 여기서는 평가 좌표 0 자체가 금지되지 않는다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:09:50]]

강의는 prime modulus 연산의 비용을 동기로 binary finite field(이진 유한체) $\mathrm{GF}(2^d)$를 소개하며 원소 수 $2^{32},2^{64}$를 언급했다. 정확히 복원되지 않은 GF 지수의 발화 조각은 이 표기의 근거로 덧붙이지 않는다. $\mathrm{GF}(2^d)$와 정수 나머지 ring $\mathbb Z/(2^d)$는 원소 수가 같아도 다른 연산 구조다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:10:48–01:11:47]]

예를 들어 $d\ge2$일 때 $\mathbb Z/(2^d)$의 2는 nonzero이지만 inverse가 없다. 반면 $\mathrm{GF}(2^d)$의 모든 nonzero 원소는 inverse를 갖는다. 따라서 이 단원의 field interpolation을 정수 modulo $2^d$로 그대로 옮길 수 없다. 모든 nonzero 정수 residue가 inverse를 갖지 않는다는 뜻은 아니며, 특히 짝수 nonunits가 문제다. [M008 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

Binary field의 원소는 0/1 coefficients를 가진 polynomial로 표현할 수 있다. 여기에는 **field element 하나의 표현**과 **field elements를 coefficients로 갖는 message polynomial $P$**라는 두 층위가 있다. 둘을 같은 polynomial로 읽으면 안 된다. 강의는 이런 표현이 컴퓨터 연산에 유리하다는 동기를 설명했지만 특정 irreducible polynomial, basis, 구현이나 모든 hardware에서의 성능 순위는 제공하지 않았다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 01:12:40]]

## 핵심 정리

- **메시지와 전송값을 구별한다.** 메시지는 $\deg P<n$인 $P$의 $n$개 계수이며 전송값은 좌표가 알려진 evaluations다. Secret Sharing의 무작위 계수와 역할이 다르다.
- **소실에는 $n+k$, 위치를 모르는 최대 $k$개 값 변경에는 $n+2k$개 좌표를 사용한다.** 전자는 정상 값 $n$개를 남기고 후자는 잘못된 값의 위치를 모르는 상황에서도 정답의 유일성을 확보한다.
- **오류 위치를 $E$의 roots에 담고 $R=PE$로 선형화한다.** Decoder가 아는 수신값 $c'_i$로 $R(\beta_i)=c'_iE(\beta_i)$를 푼다. 식과 미지수 개수가 같다는 사실만으로 성공을 증명할 수는 없다.
- **복구 대상의 유일성과 보조 해의 유일성은 다르다.** $R-P_{\mathrm{true}}E$의 차수와 정상 좌표의 root 수를 비교하면 모든 유효한 해의 몫이 같은 메시지임을 알 수 있다.
- **원소 수만 같다고 같은 연산 공간은 아니다.** 충분한 distinct coordinates와 field의 역원이 필요하다. $\mathrm{GF}(2^d)$를 정수 modulo $2^d$로 바꾸거나 field element 표현을 message polynomial과 혼동하지 않는다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 계수 메시지에서 소실 복구까지

Field $\mathbb Z_7$에서 메시지 $(2,3)$를 좌표 1,2,3에 encoding하고 좌표 2가 소실되었을 때 복구하라. 일반적인 $n$-symbol 메시지에서 $n+k$개 evaluations가 최대 $k$개 erasures를 견디는 이유와 Secret Sharing과의 차이도 설명하라.

<details><summary>해설 보기</summary>

메시지는 $P(X)=2+3X$의 계수이고 전송값은 $P(1)=5,P(2)=1,P(3)=4$다. 좌표 2가 사라지고 다른 값이 정확하면 남은 점은 $(1,5),(3,4)$다. 기울기는 $(4-5)(3-1)^{-1}=6\cdot4\equiv3\pmod7$이고 상수항은 $5-3=2$이므로 메시지 $(2,3)$를 복구한다.

일반적으로 degree $<n$인 polynomial은 서로 다른 정상 점 $n$개로 유일하게 정해진다. 서로 다른 $n+k$개 좌표에서 최대 $k$개가 없어져도 $n$개 이상이 남는다. 빈 좌표를 식별할 수 있고 남은 값이 정확해야 한다. Sender가 미리 소실 위치를 모르는 것과 receiver가 수신 후 빈 위치를 아는 것은 양립한다. 값이 틀린 점이 섞이면 임의의 $n$개를 고르는 이 보장은 적용되지 않는다.

Secret Sharing은 secret을 상수항에 두고 다른 계수를 무작위로 골랐다. 여기서는 전체 메시지가 계수이며 좌표와 evaluation 값의 대응을 receiver가 알아야 한다.

**채점·확인:** 전송값 (5,1,4), inverse 4, 복구 계수 (2,3)을 구하고 알려진 소실·정상 생존값·distinct coordinates의 가정을 밝힌다.

</details>

#### 확인 Q02 · 일치 좌표 수가 정답을 유일하게 하는 이유

서로 다른 $n+2k$개 좌표에서 최대 $k$개 값이 바뀌었다. Degree $<n$인 후보 $Q$가 수신값 $c'_i$와 적어도 $n+k$개 좌표에서 일치하면 $Q=P$임을 증명하라. 왜 임의의 $n$개 수신값을 바로 interpolation하면 안 되는가?

<details><summary>해설 보기</summary>

실제 전송값은 $c_i=P(\beta_i)$이고 $c'_i$는 수신값이다. Prime은 미분 기호가 아니다. 정상 좌표는 적어도 $n+k$개지만 그 위치는 receiver에게 알려져 있지 않다.

후보 $Q$의 $n+k$개 이상 일치 좌표 중 오류는 최대 $k$개뿐이므로 적어도 $n$개에서는 $Q(\beta_i)=c'_i=P(\beta_i)$다. 따라서 degree $<n$인 $P-Q$에 서로 다른 roots가 $n$개 이상 있다. Field 위에서 nonzero polynomial의 root 수는 degree 이하이므로 $P-Q=0$, 즉 $Q=P$다.

임의로 고른 $n$점에는 잘못된 값이 들어갈 수 있고 그 점들을 지나는 polynomial이 실제 $P$라는 보장은 없다. 이 증명은 일치 조건을 만족하는 정답의 유일성을 보이며 그런 후보를 효율적으로 찾는 알고리즘 자체를 제공한 것은 아니다.

**채점·확인:** 공통 정상점 수의 하한 (n+k)−k=n을 구하고 차수와 root 수를 연결한다. 유일성과 탐색 방법을 구분한다.

</details>

#### 확인 Q03 · Error locator가 두 종류의 좌표를 묶는 원리

최대 $k$개 오류 좌표를 roots에 포함하는 monic degree $k$ polynomial $E(X)=\prod_{j=1}^k(X-e_j)$를 생각하자. 왜 모든 좌표에서 $P(\beta_i)E(\beta_i)=c'_iE(\beta_i)$인가? 실제 오류가 $k$개보다 적은 경우와 decoder가 오류 위치를 모른다는 조건도 설명하라.

<details><summary>해설 보기</summary>

정상 좌표에서는 $P(\beta_i)=c'_i$여서 양변이 같다. 오류 좌표에서는 $E(\beta_i)=0$이므로 원래 값과 받은 값이 달라도 양변 모두 0이다. 두 경우를 같은 식으로 표현한 것이다.

실제 오류 수가 $t<k$이면 모든 오류 좌표를 roots로 잡은 뒤 다른 좌표 $k-t$개를 더해 degree $k$를 맞출 수 있다. 정상 좌표를 추가 root로 골라도 등식은 계속 성립한다. 곱의 각 인자가 monic이므로 $E$의 최고차 계수는 1이다.

이는 올바른 $E$가 존재하는 이유를 설명한 것이다. Decoder가 실제 오류 위치를 이미 안다고 가정하지 않는다. 실제 계산은 roots를 사전에 맞히는 대신 $E$와 보조 polynomial의 계수를 구한다.

**채점·확인:** 정상/오류 좌표에서 등식이 성립하는 서로 다른 이유와 부족한 roots를 채워도 되는 이유를 쓴다.

</details>

#### 확인 Q04 · R과 E의 계수에 대한 선형식

$R=PE$, $\deg P<n$, monic $\deg E=k$에서 $R$의 차수 제한과 미지수 수를 구하라. $E=X^k+\sum_{j=0}^{k-1}f_jX^j$로 놓고 한 수신 좌표의 선형식을 유도하라. 왜 미지 roots나 $P,E$를 직접 곱하는 방식과 다른가?

<details><summary>해설 보기</summary>

$\deg R<n+k$이므로 $R=\sum_{j=0}^{n+k-1}r_jX^j$의 미지 계수는 $n+k$개다. $E$는 leading coefficient 1이 고정되어 나머지 $k$개만 미지수다. 총 $n+2k$개이며 각 수신 좌표에서
$$
\sum_{j=0}^{n+k-1}r_j\beta_i^j
-c'_i\sum_{j=0}^{k-1}f_j\beta_i^j
=c'_i\beta_i^k
$$
를 얻는다. $\beta_i,c'_i$가 알려져 있으므로 $r_j,f_j$는 알려진 수의 배수로만 등장하고 미지수끼리 곱하지 않는다.

$P$와 $E$의 미지 계수를 직접 곱하거나 roots $e_j$를 미지수로 전개하면 일반적으로 미지수 곱이 생긴다. $R$를 별도로 두는 것이 선형화의 핵심이다.

자료 p.16의 뒤 bullet에는 prime이 빠진 $c_i$가 있지만 decoder가 아는 수신값 $c'_i$를 사용해야 한다. $n+2k$개 식과 미지수가 있다는 개수만으로 해의 존재나 유일성까지 결론내릴 수 없다. 해를 구한 뒤 $R/E$의 계수를 메시지로 읽는다.

**채점·확인:** 차수 <n+k, 미지수 (n+k)+k, 수신값을 사용한 선형식을 정확히 쓰고 식 개수만으로 결론낼 수 없는 것을 설명한다.

</details>

#### 확인 Q05 · 받은 네 값에서 실제로 decoding하기

$\mathbb Z_7$, $n=2,k=1$, 좌표 $(1,2,3,4)$와 수신값 $(5,6,4,0)$만 주어졌다. $E=X+f_0,\ R=r_0+r_1X+r_2X^2$의 식을 세우고 계수를 구한 뒤 메시지를 복구하라. 최대 한 값 변경이라는 가정을 사용한다.

<details><summary>해설 보기</summary>

모든 식을 mod 7에서 계산하면
$$
\begin{aligned}
r_0+r_1+r_2-5f_0&=5,\\
r_0+2r_1+4r_2-6f_0&=5,\\
r_0+3r_1+2r_2-4f_0&=5,\\
r_0+4r_1+2r_2&=0.
\end{aligned}
$$
둘째−첫째 식은 $r_1+3r_2-f_0=0$, 셋째−첫째 식은 $2r_1+r_2+f_0=0$이다. 더하면 $3r_1+4r_2=0$, 즉 $r_1=r_2$다. 따라서 $f_0=4r_2$, 마지막 식에서는 $r_0=r_2$다. 첫 식에 대입하면 $4r_2=5$이고 $4^{-1}=2$여서 $r_2=3$이다. 결과는 $r_0=r_1=r_2=3,\ f_0=5$다.

따라서 $E=X+5,\ R=3+3X+3X^2$다. Leading term 나눗셈으로 먼저 $3X$를 몫에 놓으면 $R-3X(X+5)=3+2X$이고 이는 $2(X+5)$와 같으므로 몫은 $2+3X$, 나머지는 0이다. 메시지는 계수 $(2,3)$다.

검산하면 좌표 1,…,4에서 $E$의 값은 $(6,0,1,2)$, $R$의 값은 $(2,0,4,0)$다. 수신값과 $E$를 곱해도 $(2,0,4,0)$이다. 복구한 $P$의 값 $(5,1,4,0)$은 수신값과 좌표 2에서만 다르며 $E(2)=0$이다.

**채점·확인:** 전송값을 미리 아는 것으로 풀지 않고 네 수신식을 만든다. 계수·몫·나머지와 모든 좌표의 등식을 검산한다.

</details>

#### 확인 Q06 · 해가 존재하지만 하나일 필요는 없는 이유

최대 $k$개 오류 가정이 선형계의 consistency를 어떻게 보장하는가? 실제 오류가 더 적을 때 보조 해 $(R,E)$가 여러 개일 수 있는 이유도 설명하라.

<details><summary>해설 보기</summary>

실제 메시지 $P_{\mathrm{true}}$와 실제 오류 위치를 논증에 사용한다. 모든 오류 좌표를 roots로 포함하고 필요한 만큼 다른 roots를 더한 monic degree $k$의 $E$를 잡을 수 있다. $R=P_{\mathrm{true}}E$로 두면 $\deg R<n+k$이고 정상 좌표에서는 값의 일치로, 오류 좌표에서는 $E=0$으로 모든 식을 만족한다. 따라서 적어도 하나의 해가 존재한다. Decoder가 이 구성에 쓰인 실제 메시지나 오류 위치를 안다는 가정은 아니다.

오류가 $k$개보다 적으면 남는 roots를 채우는 선택이 달라질 수 있고 식들에 dependence가 있을 수도 있다. 그 결과 $(R,E)$ 자체는 유일하지 않을 수 있다. 미지수 수와 식 수가 같다는 사실로 이 가능성을 배제할 수 없다. 복구하려는 메시지는 보조 해가 아니라 그 몫이므로 몫의 유일성은 별도로 증명해야 한다.

**채점·확인:** 실제 오류로 한 해를 구성하고 degree·monic·모든 좌표의 조건을 확인한다. 보조 해 비유일성과 메시지 비유일성을 구분한다.

</details>

#### 확인 Q07 · 임의의 해에서 같은 메시지가 나오는 증명

선형계를 만족하는 임의의 $(R,E)$를 잡고 $D=R-P_{\mathrm{true}}E$를 사용해 $R/E=P_{\mathrm{true}}$임을 증명하라. 필요한 가정과 원 강의에서 스스로 확인하도록 남긴 부분을 구별하라.

<details><summary>해설 보기</summary>

$\deg R<n+k$, $\deg P_{\mathrm{true}}<n$, $\deg E=k$이므로 $\deg D<n+k$다. 정상 좌표는 적어도 $n+k$개이고 그곳에서는
$$
D(\beta_i)=c'_iE(\beta_i)-P_{\mathrm{true}}(\beta_i)E(\beta_i)=0.
$$
서로 다른 $n+k$개 이상의 roots를 가진 degree $<n+k$ polynomial은 field 위에서 zero polynomial이다. 따라서 $R=P_{\mathrm{true}}E$다. $E$는 monic이어서 zero polynomial이 아니므로 나눗셈의 나머지는 0, 몫은 $P_{\mathrm{true}}$다.

Field, distinct coordinates, degree 제한, 최대 $k$개 값 변경을 모두 사용했다. 오류가 더 많거나 좌표 정보가 틀리면 이 보장은 적용되지 않는다. 강의는 모든 보조 해의 몫이 같다는 세부 증명을 자율 확인으로 남겼고 위 차수·root 논증은 완성된 본문의 해설을 회상한 것이다. 원 발화에서 이 전개 전체를 직접 증명했다고 바꾸어 말하지 않는다.

**채점·확인:** D의 차수와 정상 roots 수를 각각 적고 E가 nonzero라는 이유까지 써서 나머지 0·같은 몫을 결론낸다.

</details>

#### 확인 Q08 · 필요한 좌표 수와 0의 역할

일반 오류 복구에 필요한 서로 다른 evaluation 좌표 수와 field 크기의 조건은 무엇인가? 좌표 0을 허용하는 경우, prime field에서 $1,\ldots,n+2k$를 쓰는 경우, Secret Sharing을 비교하라.

<details><summary>해설 보기</summary>

이 설정에는 서로 다른 $n+2k$개 field elements가 필요하다. 0을 좌표로 허용하는 일반 evaluation에서는 field size가 적어도 $n+2k$이면 좌표 수를 확보한다. Prime field에서 정수 $1,\ldots,n+2k$를 모두 서로 다른 nonzero 좌표로 쓰려면 $q>n+2k$가 충분하다. $q=n+2k$일 때 마지막 정수는 0 residue가 되므로 “모두 nonzero” 조건을 만족하지 못한다.

Reed–Solomon에서는 전체 메시지를 계수로 담으므로 0 평가 좌표 자체가 금지되지 않는다. Secret Sharing은 $P(0)$ 자체가 secret이어서 0 share를 배포하면 secret을 바로 드러낸다. 같은 interpolation 도구를 쓴다는 이유로 0 좌표의 역할까지 같다고 볼 수 없다.

**채점·확인:** n+2k distinct coordinates, 0 허용 시 size≥n+2k, 주어진 nonzero 정수 좌표 선택 시 prime q>n+2k를 구분한다.

</details>

#### 확인 Q09 · Binary field와 두 종류의 polynomial

$d\ge2$에서 $\mathrm{GF}(2^d)$와 $\mathbb Z/(2^d)$를 구분하라. Field element의 binary polynomial 표현과 message polynomial $P$는 어떻게 다른가? 이 강의만으로 특정 구현이나 모든 장치의 성능 순위를 정할 수 있는가?

<details><summary>해설 보기</summary>

$\mathrm{GF}(2^d)$에서는 모든 nonzero 원소가 inverse를 갖는다. 정수 나머지 ring $\mathbb Z/(2^d)$에서는 2가 nonzero이지만 $\gcd(2,2^d)=2$여서 inverse가 없다. 예를 들어 $2x$는 modulo $2^d$에서 1이 될 수 없다. 모든 nonzero residue가 비가역이라는 뜻은 아니고 홀수 residue는 gcd가 1이다. 원소 수가 같아도 이 두 구조의 연산은 같지 않다.

Binary polynomial의 0/1 계수는 field element 하나를 표현한다. 그 field elements 여러 개를 계수로 쓰는 message polynomial $P$는 다른 층위다. 표현용 polynomial의 계수와 메시지 계수를 섞으면 안 된다.

강의는 prime modulus 연산 비용과 binary 표현의 효율을 동기로 소개했다. 손상된 GF 지수나 polynomial 발화를 복원하지 않으며 특정 irreducible polynomial·basis·구현 또는 모든 hardware에서의 성능 우열을 제공한 것으로 확장하지 않는다.

**채점·확인:** inverse의 차이를 원소 2와 gcd로 확인하고 field element 표현과 message polynomial의 두 층위를 구분한다.

</details>

### 적용 연습

#### 연습 P01 · 서로 다른 보조 해를 직접 비교하기

**새로 작성한 강의 기반 일반 연습.** 해당 decoding 구조를 직접 다루는 제공된 기출 문항이 없어 기출형으로 부르지 않는다. $\mathbb Z_7$, $n=2,k=1$, 좌표 1,…,4에서 수신값이 $(5,1,4,0)$이고 실제로 오류가 없다. $P=2+3X$에 대해 $E_1=X-1,\ E_2=X-2$를 각각 사용하여 $R_1,R_2$를 구하라. 두 쌍이 모두 선형계를 만족하는지, 몫은 무엇인지 설명하라. $E_j$의 root가 반드시 실제 오류라는 주장도 판단하라.

<details><summary>해설 보기</summary>

$E_1=X+6$이므로
$$
R_1=(2+3X)(X+6)=5+6X+3X^2\pmod7.
$$
$E_2=X+5$에 대해서는
$$
R_2=(2+3X)(X+5)=3+3X+3X^2\pmod7.
$$
둘 다 $E$는 monic degree 1, $R$는 degree $<3$ 조건을 만족한다.

수신값이 모든 좌표에서 $P(\beta_i)$와 같으므로 $R_j(\beta_i)=P(\beta_i)E_j(\beta_i)=c'_iE_j(\beta_i)$다. 구체적으로 $E_1$의 값 $(0,1,2,3)$에 수신값을 곱하면 $(0,1,1,0)$이고 $R_1$도 같다. $E_2$에서는 $(6,0,1,2)$를 곱해 $(2,0,4,0)$이며 $R_2$도 같다. 두 쌍은 다르지만 각각 나누면 몫은 $2+3X$, 나머지는 0이다.

오류 수가 허용 한계 $k$보다 적어 남는 root를 정상 위치에 채웠다. 따라서 locator의 root가 언제나 실제 오류 위치라고 단정할 수 없다. 보조 해 비유일성과 메시지 유일성이 동시에 가능한 예다.

**채점·확인:** 두 R의 계수와 수신식 대입을 확인하고 몫의 일치와 여분 root의 의미를 설명한다.

</details>

#### 연습 P02 · 소실용 추가량을 값 변경에 썼을 때

**새로 작성한 강의 기반 일반 연습.** 직접 연결할 제공된 Reed–Solomon 기출 문항은 없다. $\mathbb Z_7$, degree $<2$, 좌표 1,2,3에서 수신값이 $(5,6,4)$이고 “최대 한 값이 변경되었다”는 정보만 있다. $(1,5),(3,4)$를 지나는 후보와 $(1,5),(2,6)$를 지나는 후보를 각각 구해 모호함을 보여라. 반면 좌표 2가 알려진 소실이고 생존값 $(1,5),(3,4)$가 정확하다면 어떻게 달라지는가?

<details><summary>해설 보기</summary>

첫 후보는 기울기 $(4-5)/(3-1)=6\cdot4=3$, 상수항 2여서 $P_1=2+3X$다. 세 좌표 값은 $(5,1,4)$이고 수신값과 좌표 2에서만 다르다.

둘째 후보는 기울기 $(6-5)/(2-1)=1$, 상수항 4여서 $P_2=4+X$다. 세 좌표 값은 $(5,6,0)$이고 수신값과 좌표 3에서만 다르다. 둘 다 degree $<2$이며 최대 한 변경과 양립하므로 메시지 $(2,3)$와 $(4,1)$를 구별할 수 없다.

여기서는 $n+k=3$개만 보내 위치 미상의 한 변경에 필요한 $n+2k=4$개 좌표 보장을 충족하지 않았다. Field $\mathbb Z_7$에는 네 distinct coordinates를 고를 여유가 있지만 실제 전송 좌표 수가 부족하다.

좌표 2가 알려진 소실이고 다른 값은 맞다면 정상 두 점을 interpolation하여 $P_1$을 유일하게 복구한다. 같은 추가량이라도 수신 후 오류 위치를 아는지에 따라 결론이 달라진다.

**채점·확인:** 두 후보의 계수·세 평가값·각각 한 불일치를 확인하고 field 크기와 실제 좌표 수의 부족을 구분한다.

</details>

### 복습 순서

Q01–Q02를 풀 때 오류 위치를 아는지 먼저 표시한다. Q03–Q05에서는 차수·미지수·수신값을 적고 식에 대입해 검산한다. Q06–Q07의 존재와 몫 유일성 증명을 나누어 복원한 뒤 Q08–Q09로 field 가정을 점검한다. P01–P02에서는 보조 해가 여러 개인 경우와 메시지가 여러 개인 경우를 구별한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 40:30–47:40 소실·encoding, 49:35–55:55 일반 오류·유일성, 56:45–01:09:01 locator·선형계·복구, 01:09:50–01:12:40 field와 표현. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - 문제 설정·소실과 일반 오류: [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-015)
  - Berlekamp–Welch 선형계와 몫: [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-016)
- [03. Number Theory.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)
  - 역원의 gcd 조건: [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

### 읽을 때의 범위

- 2026-09-28 강의의 field 기반 Reed–Solomon 구성에 한정한다. Number Theory 자료 p.24는 inverse의 선수 개념을 보완하는 자료 근거이며 그 페이지 전체가 이날 다시 발화되었다는 뜻은 아니다.
- 자료의 n을 원래 message symbol 수로 쓴다. 녹취의 m/n 혼용과 빠진 subscripts를 완전한 발화로 복원한 표기는 아니다. 수신값 c′의 prime은 미분이 아니다.
- 자료 p.16 첫 등식의 c′와 뒤 linear-system bullet의 c 표기가 다르다. Decoder가 알고 있는 수신값 c′로 식을 세우며 원본의 prime 누락을 숨기지 않는다.
- Erasure는 빈 위치를 알고 생존값이 정확한 모형, 일반 오류는 최대 k개의 위치 미상 값 변경 모형이다. 가정 밖의 오류 수·틀린 좌표 정보에는 같은 복구 보장을 적용하지 않는다.
- 모든 해의 quotient가 같다는 세부 증명은 강의에서 자율 확인으로 남겼고 본문이 전개한 차수·root 해설을 여기서 회상한다. 완성된 linear-system 구현이나 전체 bit complexity까지 가르쳤다는 뜻은 아니다.
- 마지막 GF 지수와 binary polynomial의 손상된 발화는 복원하지 않는다. GF(2^d)와 정수 modulo 2^d를 구분하며 특정 irreducible polynomial·basis·구현 또는 모든 hardware의 성능 순위를 추가하지 않는다.
