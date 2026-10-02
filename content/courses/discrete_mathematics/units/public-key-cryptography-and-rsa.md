---
title: "공개키 암호와 RSA"
description: "키의 역할·RSA 계산·Euler 조건과 자료 시점의 한계를 복습한다."
course: "discrete_mathematics"
unit_id: "public-key-cryptography-and-rsa"
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

공개키와 비밀키의 역할을 나누어 사전 비밀 공유의 문제를 이해한다. RSA의 두 modulus를 구별해 계산하고 짧은 복호화 증명과 보안 설명의 범위를 확인한다.

## Public-key cryptography: 처음 만난 상대에게 비밀을 보내기

Encryption(암호화)은 통신을 지켜보는 제3자가 있어도 메시지를 보호하려는 방법이다. Symmetric-key cryptography(대칭키 암호)에서는 sender와 receiver가 같은 비밀 key $K$를 미리 공유한다. Sender가 $C=E_K(M)$을 보내면 receiver는 $M=D_K(C)$를 계산한다. 계산 자체와 별개로, 처음 만난 상대와 **어떻게 $K$를 먼저 안전하게 공유할 것인가**라는 문제가 남는다. [NM002 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-004), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 03:57–04:55]]

Public-key cryptography(공개키 암호)는 공개할 key와 감출 key를 분리한다. Receiver가 public key와 private key의 pair를 만들고 public key를 공개한다. Sender는 receiver의 public key로 encrypt하고, receiver는 자신만 가진 private key로 decrypt한다. 암호화 방법을 안다는 것이 복호화 방법까지 쉽게 알아낼 수 있다는 뜻은 아니다. 이 역할 구별은 [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트: Public-key와 RSA]]의 출발점이다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 05:54–06:48]]

강의는 처음 통신을 시작하는 public-key 방식의 장점과 symmetric-key 방식의 효율을 결합하는 hybrid 사용을 소개했다. 구체적인 메시지 교환·인증·구현 protocol까지 제공한 것은 아니다. 공개 encryption key와 비밀 decryption key를 구별하는 사고는 2021년 학기 미확인 기출 (j)의 개념 요구에도 연결된다. 공개할 것으로 설계된 값의 공개 여부와 private key의 노출을 같은 사건으로 취급하면 안 된다. [EX:dm_2021_mid_q01 p.1]

### Discrete logarithm과 Integer factorization

[NM002 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-005)는 자료상의 연혁으로 공개키 아이디어의 출발을 1974년, Diffie–Hellman을 1976년, RSA를 1977년으로 적는다. 이 연혁은 materials-only 보충이며 독립적으로 확인한 역사 서술은 아니다. 여기서 학습에 필요한 것은 연결되는 계산 문제의 차이다.

Discrete logarithm(이산 로그)은 $g,h,p$를 알 때 $g^x\equiv h\pmod p$를 만족하는 exponent $x$를 찾는 문제다. 알려진 $x$로 $g^x\bmod p$를 계산하는 forward operation과 다르다. Integer factorization(정수 인수분해)은 $N=pq$라는 곱에서 큰 prime factors $p,q$를 찾는 문제다. 하나는 지수를, 다른 하나는 곱의 인수를 찾는다. 자료는 각각을 key exchange와 RSA encryption에 연결하지만 Diffie–Hellman protocol의 전체 절차와 보안 증명은 이 범위에 포함하지 않는다.

## RSA key generation: 두 Modulus의 역할

RSA는 이전 정수론 도구들이 함께 쓰이는 예다. GCD로 서로소 조건을 검사하고, Extended Euclidean algorithm으로 inverse를 구하며, modular exponentiation으로 암호문을 계산한다. 강의의 이전 도구 복습은 이 연결을 위한 것이지 각 도구의 모든 코드와 증명을 다시 강의했다는 뜻은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 03:03, 12:40]]

Textbook RSA의 식을 정확히 읽으려면 서로 다른 primes $p,q$를 사용한다. 그러면

$$N=pq,\qquad\varphi(N)=(p-1)(q-1).$$

여기서 $\varphi(N)$은 $N$과 서로소인 residue의 수를 나타내는 totient다. $\gcd(e,\varphi(N))=1$인 양의 정수 $e$를 선택하고

$$d=e^{-1}\pmod{\varphi(N)}$$

를 구한다. Public key는 $(N,e)$, private key는 $(N,d)$다. 메시지는 $0\le m<N$의 정수 대표원으로 두고 다음처럼 계산한다. [NM002 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-006)

| 단계 | 계산 | 사용하는 modulus |
|---|---|---|
| Private exponent 구성 | $ed\equiv1$ | $\varphi(N)$ |
| Encryption | $c=m^e\bmod N$ | $N$ |
| Decryption | $c^d\bmod N$ | $N$ |

특히 $d$를 $e^{-1}\bmod N$으로 구하는 것이 아니다. Bézout 관계 $ue+v\varphi(N)=1$에서 $u\bmod\varphi(N)$이 $d$가 된다. 이 inverse 연결의 선수 개념은 [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트: Bézout과 Modular inverse]]에서 확인할 수 있다. [M008 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

### 작은 수로 key와 ciphertext 계산하기

다음은 식을 확인하기 위한 작은 해설 예이며 실제 강의의 수치 문제나 보안용 parameters가 아니다. $p=5,q=11$이면 $N=55$, $\varphi(N)=40$이다. $e=3$은 40과 서로소이고

$$40=13\cdot3+1,\qquad1=40-13\cdot3$$

이므로 $d=-13\bmod40=27$이다. $3\cdot27=81\equiv1\pmod{40}$으로 검산한다. 메시지 $m=2$의 암호문은 $c=2^3\bmod55=8$이다.

복호화도 큰 정수를 끝까지 만들 필요가 없다. Modulo 55에서

$$8^2\equiv9,\quad8^4\equiv26,\quad8^8\equiv16,\quad8^{16}\equiv36.$$

$27=16+8+2+1$이므로 $8^{27}\equiv36\cdot16\cdot9\cdot8\equiv2\pmod{55}$다. 처음 메시지로 돌아온다. Binary representation과 squaring의 재사용은 [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 12:40]]에서 연결한 계산 도구다.

## Euler’s theorem으로 보는 복호화의 이유와 조건

계산 예 하나가 모든 메시지에 대한 증명은 아니다. 강의는 RSA의 전체 correctness proof를 생략하고 Euler’s theorem과의 연결을 소개했다. 아래는 그 연결을 정돈한 노트 측 유도다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 09:59–11:48]]

Euler’s theorem의 여기서 필요한 조건은 $\gcd(m,N)=1$이다. 이때

$$m^{\varphi(N)}\equiv1\pmod N.$$

또한 $ed\equiv1\pmod{\varphi(N)}$이므로 $ed=1+t\varphi(N)$인 정수 $t$가 있다. 양의 대표원 $e,d$를 사용하는 설정에서 이 식을 넣으면

$$
c^d\equiv(m^e)^d=m^{ed}
=m\bigl(m^{\varphi(N)}\bigr)^t
\equiv m\pmod N.
$$

결과를 $0,\ldots,N-1$의 대표원으로 반환하므로 원래 메시지를 얻는다. $\gcd(m,N)\ne1$인 메시지에 Euler 식을 바로 대입해서는 안 된다. 이는 **지금 제시한 짧은 증명의 범위**이며, RSA가 그런 메시지에서 반드시 실패한다는 뜻은 아니다. 전체 메시지에 대한 별도 증명을 여기서 완료한 것으로 읽지 않는다.

## Primality test와 Factoring 난이도는 다른 질문이다

Key generation에는 큰 prime이 필요하므로 큰 integer 후보를 무작위로 뽑고 prime인지 검사하는 과정이 필요하다. Primality test(소수 판정)는 “이 수가 prime인가”를 결정한다. Integer factorization처럼 실제 인수들을 찾아내는 일과는 다르다. 강의는 이 도구가 필요하다는 연결까지 설명했고, M008 p.13도 두 질문을 구분한다. [M008 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-013), [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 11:48–12:40]]

Fermat·Miller–Rabin·AKS의 상세 절차와 오류 확률은 이 연결만으로 학습한 범위가 되지 않는다. 또한 prime 후보가 많아도 PRNG가 편향되면 공통인수를 가진 moduli가 나올 수 있으므로 후보 공간의 크기만으로 sampling의 품질을 판단할 수 없다.

### Key size를 읽을 때 어느 수의 길이인지 확인하기

$N$을 factor하면 $p,q$에서 $\varphi(N)$을 구하고 $d$를 계산할 수 있다. 따라서 factorization의 어려움은 자료가 설명하는 RSA security의 필요한 배경이다. 이것만으로 textbook 식이 모든 실제 공격에 안전하다는 충분조건을 얻지는 않는다. 실제 사용에서는 더 안전한 형태로 바꾼다는 강의 설명이 있지만, 구체적인 padding·인증 방식은 공급되지 않았다.

[NM002 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-007)은 **자료에 적힌 당시 설명**으로 RSA-250의 250 decimal digits, 829 bits, 2020년 2월 factorization 기록을 제시한다. 또한 RSA-1024를 309 digits로 표시하고 2048-bit 권고를 적는다. 이 수치와 기록은 현재 보안 권고나 최신 기록을 확인한 결과가 아니다.

녹취의 약 830 bits·약 310 digits는 반올림 표현과 구분할 수 있지만, “1024-bit prime”과 modulus 길이를 섞는 부분은 그대로 불확실하다. $p,q$ 각각의 길이와 곱 $N$의 길이는 같은 값이 아니다. Bit 수 증가가 공격 비용의 단순 비례 증가를 뜻하지 않는다는 동기는 보존하되, 여기서 factorization의 정확한 exponential complexity가 증명된 것은 아니다. [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 STT 10:50, 13:40–14:28]]

## 핵심 정리

- 대칭키는 같은 비밀을 미리 공유해야 한다. 공개키 방식은 수신자의 공개 encryption key와 비밀 decryption key를 분리한다.
- RSA의 $d$는 modulo $\varphi(N)$에서 구하고 메시지·암호문은 modulo $N$에서 계산한다.
- GCD·Bézout·binary exponentiation은 서로 다른 계산 단계를 담당한다.
- Euler를 이용한 짧은 논증에는 $\gcd(m,N)=1$이 필요하다. 그 조건 밖에서 증명을 못 쓴다는 것과 RSA 실패는 다르다.
- Primality testing은 소수 여부, factoring은 인수 찾기다. 자료의 기록·key size 언급은 현재 보안 권고가 아니다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 키 전달 문제와 도구의 역할

Symmetric-key 방식의 송수신 과정과 사전 key distribution 문제를 설명하라. Public/private key는 누가 만들고 누가 쓰며 hybrid의 동기는 무엇인가? 앞서 배운 정수론·Hash·PRNG 도구와의 연결도 설명하라.

<details><summary>해설 보기</summary>

대칭키에서는 양쪽이 비밀 $K$를 공유해 $C=E_K(M)$, $M=D_K(C)$를 계산한다. 처음 만난 상대와 그 $K$를 먼저 안전하게 공유하는 일이 남는다. 공개키 방식에서는 receiver가 key pair를 만들고 public key를 공개한다. Sender는 receiver의 public key로 암호화하고 receiver는 자신의 private key로 복호화한다.

Hybrid는 통신을 시작하는 공개키 방식의 장점과 대칭키 방식의 효율을 함께 쓰려는 동기다. 구체 protocol은 여기서 주어지지 않았다. Integer·prime·modular arithmetic 위에서 GCD는 서로소·공통인수를 검사하고 Extended Euclid는 역원을 구한다. Hash의 저장·검색, PRNG의 생성 데이터라는 이전 응용과 달리 암호에서는 공격자를 고려하는 요구가 필요하다.

**채점·확인:** 송수신자의 key 선택, 사전 공유 문제, hybrid의 동기와 도구별 역할을 확인한다.

</details>

#### 확인 Q02 · 지수 찾기와 인수 찾기

자료가 제시한 공개키 출발·Diffie–Hellman·RSA의 연도를 출처의 주장으로 적어라. Discrete logarithm과 integer factorization에서 아는 값·찾는 값을 구별하고 forward 계산과 비교하라.

<details><summary>해설 보기</summary>

자료는 공개키 아이디어의 출발을 1974년, Diffie–Hellman을 1976년, RSA를 1977년으로 적는다. 이것은 자료의 연혁 보충이며 별도로 확인한 역사적 연대라는 뜻은 아니다.

Discrete logarithm은 $g,h,p$를 알고 $g^x\equiv h\pmod p$의 지수 $x$를 찾는다. 알려진 $x$로 $g^x\bmod p$를 계산하는 방향과 다르다. Factoring은 $N$을 알고 $N=pq$의 prime factors를 찾으며 알려진 두 인수를 곱하는 방향과 다르다. 자료의 대응은 key exchange와 RSA의 배경 계산 문제까지이며 Diffie–Hellman 전체 절차·보안 증명은 포함하지 않는다.

**채점·확인:** 자료 귀속의 세 연도, known/unknown과 forward/reverse 계산을 구별한다.

</details>

#### 확인 Q03 · RSA의 두 modulus

서로 다른 primes $p=5,q=11$, $e=3$에서 $N,\varphi(N),d$와 두 key를 구하라. $0\le m<N$인 메시지 $m=2$의 암호문도 구하고 어떤 modulus에서 역원을 구했는지 명시하라.

<details><summary>해설 보기</summary>

$N=55$, $\varphi(N)=4\cdot10=40$이다. $\gcd(3,40)=1$이고 $1=40-13\cdot3$이므로 $d=-13\bmod40=27$이다. 검산은 $3\cdot27=81\equiv1\pmod{40}$이다.

Public key는 $(55,3)$, private key는 $(55,27)$이고 $c=2^3\bmod55=8$이다. $d$는 $e^{-1}\bmod N$이 아니라 $e^{-1}\bmod\varphi(N)$이다. $(p-1)(q-1)$ 식은 서로 다른 primes라는 조건을 사용한다.

**채점·확인:** 55·40·27·두 key·8, Bézout 계수와 modulus 구별을 확인한다.

</details>

#### 확인 Q04 · 복호화의 수치 검산

Q03의 $8^{27}\bmod55$를 반복 제곱과 $27=16+8+2+1$로 계산하라. 중간마다 modulo를 취해도 되는 이유와 큰 수를 전부 먼저 만들지 않는 이유를 설명하라.

<details><summary>해설 보기</summary>

Modulo 55에서 $8^2=64\equiv9$, $8^4\equiv81\equiv26$, $8^8\equiv676\equiv16$, $8^{16}\equiv256\equiv36$이다. 따라서 $8^{27}\equiv36\cdot16\cdot9\cdot8$이다. 차례로 $36\cdot16\equiv26$, $26\cdot9\equiv14$, $14\cdot8\equiv2$여서 메시지 2로 돌아온다.

같은 residue의 대표원으로 바꾸어 곱해도 결과 class가 같으므로 매번 줄일 수 있다. Binary exponent의 1 bit 위치만 결합하면 큰 중간 정수를 전부 유지할 필요가 없다. 이 작은 계산은 수식 확인용이지 보안용 parameter 예가 아니다.

**채점·확인:** 네 제곱 residue, 누적곱, 원래 메시지와의 일치를 검산한다.

</details>

#### 확인 Q05 · Euler 논증의 조건

$\gcd(m,N)=1$, $ed=1+t\varphi(N)$에서 $c^d\equiv m$을 유도하라. $\gcd(m,N)\ne1$인 경우 이 유도를 사용할 수 있는가? 그것이 곧 복호화 실패를 뜻하는가?

<details><summary>해설 보기</summary>

서로소일 때 Euler 식 $m^{\varphi(N)}\equiv1\pmod N$을 쓸 수 있다. 그러면
$$c^d\equiv(m^e)^d=m^{ed}=m(m^{\varphi(N)})^t\equiv m\pmod N.$$
복호화 결과를 $0,\ldots,N-1$의 대표원으로 돌려주므로 원래 대표 메시지를 얻는다.

비서로소이면 이 Euler 식을 그대로 적용할 수 없다. 이는 지금의 증명 방식이 그 경우를 다루지 못한다는 뜻이며 RSA가 반드시 실패한다는 결론이 아니다. 강의는 전체 correctness proof를 생략했고 위 유도는 본문에서 풀어 쓴 조건부 설명이다.

**채점·확인:** Euler의 가정, exponent 대입, 대표원, 증명 범위와 실패 판정의 차이를 설명한다.

</details>

#### 확인 Q06 · Prime을 고르는 단계

큰 prime을 key generation에 사용할 때 random sampling과 primality test는 어떤 순서로 쓰는가? Composite라고 판단하면 그 인수까지 알게 되는가?

<details><summary>해설 보기</summary>

큰 integer 후보를 뽑고 prime인지 검사해 p 또는 q로 쓸 수 있는지 판단한다. Primality test의 질문은 소수 여부이며 실제 인수를 구하는 factorization과 다르다. Composite 판정만으로 그 factors를 얻었다고 할 수 없다.

Prime 후보가 많아도 sampling이 편향될 수 있으므로 PRNG 품질은 별도다. Fermat·Miller–Rabin·AKS의 상세 절차나 오류 확률은 이 연결만으로 배운 내용이 되지 않는다.

**채점·확인:** sampling→판정의 순서, 판정/인수 산출 차이, 상세 검사법 범위를 확인한다.

</details>

#### 확인 Q07 · 자료의 기록과 길이의 대상

자료의 RSA-250·RSA-1024·2048-bit 언급을 시점과 함께 요약하라. N과 p,q의 bit length를 왜 구별하며 factoring이 어렵다는 설명만으로 textbook RSA의 실제 안전성이 보장되는가?

<details><summary>해설 보기</summary>

자료는 RSA-250을 250 decimal digits·829 bits, 2020년 2월의 factorization 기록으로 제시한다. RSA-1024는 309 digits로 적고 2048-bit 권고를 소개한다. 이는 자료에 적힌 당시 주장이지 현재 기록·권고·보급률을 확인한 결과가 아니다. 약 830 bits·약 310 digits라는 반올림과도 구별한다.

N은 p와 q의 곱이므로 modulus 길이와 각 prime의 길이는 같은 대상이 아니다. N을 factor하면 φ(N)과 d를 구할 수 있으므로 factoring 난이도는 필요한 배경이지만 이것만으로 모든 실제 공격에 안전하다는 충분조건은 아니다. 정확한 exponential 복잡도나 구체 padding·인증 방식도 이 설명에서 증명되지 않았다.

**채점·확인:** 날짜·수치의 자료 귀속, prime/modulus 구별, 필요 배경과 충분 보장의 차이를 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 공개값과 비밀값을 나누기

**새로 만든 기출 연결 합성 연습.** [EX:dm_2021_mid_q01 p.1]의 (j)에서 key 역할을 구분하는 요구를 값의 분류와 인수 유출의 결과로 옮겼다. Q01·Q03의 도구가 선수 내용이며 현재 보안 권고를 판단하는 문제가 아니다. 2021년 자료의 학기는 미확인이다. [[exam_questions/dm_2021_mid_q01|2021 중간 Q1 미리보기]]

수신자가 $(N,e)=(55,3)$을 공개했고 별도로 p=5가 노출되었다. 의도된 공개값과 추가로 드러난 비밀 정보를 구분하고, sender·receiver가 쓸 key 및 p 노출 후 계산 가능한 값을 설명하라.

<details><summary>해설 보기</summary>

$(55,3)$은 공개 encryption key다. Sender는 그것으로 암호화하고 receiver는 private exponent $d$로 복호화한다. $p=5$의 노출은 public key의 정상 공개와 다른 사건이다.

$p$를 알면 $q=55/5=11$, $\varphi(N)=40$, $d=3^{-1}\bmod40=27$을 계산한다. 즉 factoring 정보를 얻으면 비밀 exponent를 구성할 수 있다. 공개키가 공개되었다는 사실과 그 인수를 얻었다는 사실을 혼동하면 안 된다. 작은 수는 역할 확인용이며 실제 보안 수준의 예가 아니다.

**채점·확인:** 공개 목적·두 사용자의 key·5→11→40→27의 추론을 확인한다.

</details>

#### 연습 P02 · 짧은 증명이 적용되지 않는 메시지

**새로 만든 강의 기반 일반 연습.** 조건부 Euler 증명의 적용 범위를 직접 묻는 선정 기출은 없다.

$N=55,e=3,d=27$에서 $m=5$를 생각하라. “$5^{40}\equiv1$이므로 복호화된다”는 설명의 문제를 찾고, $c=5^3\bmod55$와 $c^{27}\bmod55$를 직접 계산해 증명 실패와 계산 결과를 비교하라.

<details><summary>해설 보기</summary>

$\gcd(5,55)=5$라 Euler의 서로소 조건이 없다. 실제 $5^{40}$은 5의 배수여서 modulo 55의 residue 1일 수 없다. 그 문장은 사용할 수 없다.

$c=125\bmod55=15$다. $15^2\equiv5$, $15^4\equiv25$, $15^8\equiv20$, $15^{16}\equiv15$이고 $27=16+8+2+1$이다. 누적곱은 $15\cdot20\equiv25$, $25\cdot5\equiv15$, $15\cdot15\equiv5$이므로 복호화 결과는 5다. 이 한 예는 짧은 증명의 가정이 깨져도 계산이 실패한다고 단정할 수 없음을 보여 준다. 모든 비서로소 메시지에 대한 일반 증명을 대신하지는 않는다.

**채점·확인:** gcd 조건 실패, c=15, 제곱·누적 결과 5 및 예제/일반 증명의 차이를 확인한다.

</details>

### 복습 순서

Q01–Q02로 역할과 계산 문제를 구별한 뒤 Q03–Q05를 종이에 계산한다. P01에서 공개값과 유출값을 구분하고 P02에서 Euler 증명의 조건을 검사한다. Q06–Q07은 각 문장의 확인 범위를 한 줄씩 적어 복습한다.

## 출처

### 강의 노트와 녹취

- [[courses/discrete_mathematics/lectures/2026-09-28-lecture-06|2026-09-28 강의 노트 · 2026-09-28 · 이산수학 6강]]
- [[courses/discrete_mathematics/lectures/2026-09-23-lecture-05|2026-09-23 강의 노트 · 2026-09-23 · 이산수학 5강]]
- [[courses/discrete_mathematics/transcripts/2026-09-28|2026-09-28 보정 녹취]] — 03:03–06:48 복습과 key 역할; 09:59–12:40 RSA와 계산 도구; 13:40–14:28 크기·기록. 시간 표시는 녹취 본문에서 찾는다.

### 강의자료의 해당 쪽

- [04. Number Theory Applications.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf)
  - 대칭키·공개키·자료상의 연혁: [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-005)
  - RSA 식과 자료 시점의 기록: [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/04.number.theory.applications/page-007)
- [03. Number Theory.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf)
  - Primality의 정의: [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-013)
  - Bézout와 inverse 선수 복습: [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/03.number.theory/page-024)

### 읽을 때의 범위

- 9월 28일의 RSA 소개와 9월 23일 inverse 선수 내용을 연결한다. 공개키 연혁·계산 문제 대응과 factoring 기록은 자료로 보충한 설명이다.
- RSA 전체 correctness proof는 강의에서 생략되었다. 본문의 Euler 유도는 gcd(m,N)=1인 경우이며 비서로소 메시지의 실패를 주장하지 않는다.
- φ(N)=(p−1)(q−1)은 서로 다른 primes를 전제한다. 역원 modulus φ(N)과 메시지 modulus N을 구별하며 작은 수 예는 보안용이 아니다.
- Hybrid·실제 RSA 변형은 동기 수준이며 구체 protocol·padding·인증·primality-test 절차를 제공한 것으로 확대하지 않는다.
- 2020년 기록과 1024·2048-bit 언급은 자료 시점의 주장이다. Prime/modulus 길이가 섞인 녹취는 미해결이며 현재 권고·보급률·정확한 factoring complexity를 확인하지 않는다.
- 2021 기출은 학기 미확인 Q1(j)의 역할 구별에 한정한다. 공개 녹취의 불명확한 발화·가림을 복원하거나 과거 시험 정책을 현재로 옮기지 않는다.
