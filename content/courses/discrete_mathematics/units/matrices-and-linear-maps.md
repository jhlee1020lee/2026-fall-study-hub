---
title: "Matrices와 Linear Maps의 대응"
description: "Matrix 계산을 linear map의 표현·합성·inverse와 연결하고 neural-network 예를 검산한다."
course: "discrete_mathematics"
unit_id: "matrices-and-linear-maps"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01. Vectors and Matrices.pdf"]
private_source_assets: []
source_lectures: ["courses/discrete_mathematics/lectures/2026-09-07-lecture-02", "courses/discrete_mathematics/lectures/2026-09-09-lecture-03"]
---

행렬의 크기와 기본 입력의 image를 함께 보면 row-column 계산의 의미가 드러난다. Linear map의 조건으로 표현·합성·역변환을 설명하고, bias와 batch가 등장하는 문맥을 구별하자.

## Matrix의 차원과 row-column 계산

Matrix(행렬)는 수를 row(행)와 column(열)에 배열한 것이다. $m$개의 row와 $n$개의 column이 있으면 크기는 $m\times n$이고, $a_{ij}$는 $i$번째 row, $j$번째 column의 entry(성분)다. $m=n$이면 square matrix(정사각행렬)다. 행렬은 데이터를 저장할 수도 있지만, 여기서는 [[courses/discrete_mathematics/units/sets-functions-sequences|Function]]을 유한한 계수로 표현하는 도구로 발전시킨다.

Graph(그래프)의 vertex(정점) 사이의 연결도 matrix로 표현할 수 있다. Row와 column을 각각 vertex에 대응시키면 entry에 두 vertex의 연결 여부를 기록할 수 있기 때문이다. [이산수학 M001 PDF p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/01.Vectors.and.Matrices.pdf)와 [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 07:50]]은 이를 응용 동기로 소개한다. 이 단원에서는 matrix의 arithmetic과 linear map을 공부하며, graph나 communication network의 algorithm까지 다루지는 않는다.

Addition(덧셈)은 같은 크기의 행렬 사이에서 성분별로 정의한다.

$$(A+B)_{ij}=a_{ij}+b_{ij}.$$

Multiplication(곱셈)은 다르다. $A$가 $m\times k$, $B$가 $k\times n$이면 $AB=C$는 $m\times n$이고

$$c_{ij}=\sum_{\ell=1}^{k}a_{i\ell}b_{\ell j}$$

이다. $A$의 row와 $B$의 column을 짝지어 곱한 뒤 더하는 dot product(내적)다. [이산수학 M001 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/01.Vectors.and.Matrices.pdf)의 붉은 성분들은 바로 이 한 row와 한 column이 결과의 $c_{ij}$ 하나를 만드는 것을 보여 준다.

안쪽 차원 $k$가 맞아야 하는 이유는 곱해 더할 항의 수가 같아야 하기 때문이다. $i\in\{1,\ldots,m\}$, $\ell\in\{1,\ldots,k\}$, $j\in\{1,\ldots,n\}$으로 먼저 정하면 남는 index $i,j$와 합산되어 사라지는 $\ell$을 구별할 수 있다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 10:34]]도 크기에 맞춰 index를 고정하라고 설명했다.

$AB$가 정의되어도 $BA$는 정의되지 않거나 크기가 다를 수 있다. 둘 다 정의되어도 일반적으로 $AB\ne BA$다. 예를 들어 설명용으로

$$A=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad B=\begin{pmatrix}1&0\\0&2\end{pmatrix}$$

를 택하면 $AB=\begin{pmatrix}1&2\\0&2\end{pmatrix}$이고 $BA=\begin{pmatrix}1&1\\0&2\end{pmatrix}$다. 곱의 순서를 임의로 바꾸는 scalar 계산 습관을 행렬에 옮겨서는 안 된다.

## Linear map을 결정하는 기본 방향

Linear map(선형사상) $F:\mathbb R^n\to\mathbb R^m$은 모든 $u,v$와 실수 $c$에 대해

$$F(u+v)=F(u)+F(v),\qquad F(cu)=cF(u)$$

를 만족한다. 따라서 linear combination(선형결합)도 보존한다.

$$F\left(\sum_j c_ju_j\right)=\sum_j c_jF(u_j).$$

이산수학 M001 PDF p.9의 두 조건은 단순히 그래프가 직선처럼 보인다는 설명보다 정확하다. 특히 $F(0)=0$이어야 한다. $x\mapsto 2x+1$은 그래프가 직선이지만 이 정의의 linear map은 아니다.

먼저 $F:\mathbb R\to\mathbb R$를 보자. $a=F(1)$로 놓으면

$$F(x)=F(x\cdot1)=xF(1)=ax.$$

한 방향의 기본 입력 1에서의 값만 알면 나머지 값이 모두 결정된다. 이를 $n$차원으로 확장한다. Standard unit vector(표준단위벡터) $e_j$는 $j$번째 성분만 1이고 나머지는 0이다. 모든 $x=(x_1,\ldots,x_n)^T$는 $x=\sum_jx_je_j$이므로, scalar 값을 출력하는 $F:\mathbb R^n\to\mathbb R$에 대해

$$F(x)=\sum_jx_jF(e_j)=\sum_ja_jx_j=a\cdot x,\qquad a_j=F(e_j).$$

반대로 고정된 $a$와의 dot product는 합과 scalar multiplication을 분배하므로 linear하다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 26:21]]의 설명을 요약하면 기본 방향에서의 값만 알면 모든 입력에서의 값을 안다는 뜻이다. 위 식은 그 설명을 정돈한 해설용 표기이며, 실제 판서를 복원한 전사는 아니다.

### Vector 출력을 matrix로 쌓기

이제 $F:\mathbb R^n\to\mathbb R^m$을 $m$개의 coordinate function(좌표함수) $F_i$로 나눈다. 각 $F_i$가 linear이면 $F_i(x)=a_i\cdot x$인 row vector $a_i$가 있다. 이 rows를 쌓아 만든 $m\times n$ 행렬 $A$에 대해

$$F(x)=Ax.$$

같은 결과를 column으로 읽으면 더 직접적이다.

$$A=\begin{bmatrix}F(e_1)&F(e_2)&\cdots&F(e_n)\end{bmatrix}.$$

$j$번째 column은 $j$번째 기본 입력의 전체 출력이다. 예를 들어 설명용으로 $F(e_1)=(1,2)^T$, $F(e_2)=(4,5)^T$이면 $A=\begin{pmatrix}1&4\\2&5\end{pmatrix}$이며 $F((2,3)^T)=2F(e_1)+3F(e_2)=(14,19)^T$다.

이 표현은 고정된 standard coordinates에서 유일하다. $Ax=Bx$가 모든 $x$에 대해 성립하면 $x=e_j$를 대입하여 $A,B$의 $j$번째 columns가 같음을 얻는다. 모든 $j$에 대해 같으므로 $A=B$다. 이것이 M001 PDF p.11의 matrix representation(행렬 표현)이다. [[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 STT 08:54]]의 복습처럼 $a_{ij}$는 $j$번째 입력 성분이 $i$번째 출력에 기여하는 계수다.

## Function 연산이 matrix 연산이 되는 이유

같은 domain과 codomain을 가진 $F_1,F_2$에 대해 새 function의 sum을

$$(F_1+F_2)(u)=F_1(u)+F_2(u)$$

로 정의한다. 이는 한 function의 성질 $F(u+v)=F(u)+F(v)$와 다르다. 앞 식은 function 두 개로 새 function을 만드는 정의이고, 뒤 식은 주어진 function이 만족해야 하는 조건이다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 36:35]]에서 구별한 대목이다.

각각의 linearity를 적용하면

$$(F_1+F_2)(u+v)=F_1(u)+F_1(v)+F_2(u)+F_2(v)
=(F_1+F_2)(u)+(F_1+F_2)(v)$$

이고 scalar 조건도 성립한다. $(cF)(u)=cF(u)$로 정의한 scalar multiple도 같은 두 조건을 보존한다. 행렬로 쓰면 각각 $A_1+A_2$, $cA$가 대응한다.

### Composition에서 곱셈 공식을 유도하기

$G:\mathbb R^n\to\mathbb R^k$, $F:\mathbb R^k\to\mathbb R^m$이면 $H=F\circ G$도 linear하다. 예를 들어

$$H(u+v)=F(G(u)+G(v))=F(G(u))+F(G(v))=H(u)+H(v),$$

$$H(cu)=F(cG(u))=cH(u).$$

$G(x)=Bx$, $F(y)=Ay$로 놓고 성분을 전개하면

$$z_i=\sum_{\ell=1}^{k}a_{i\ell}y_\ell
=\sum_{\ell=1}^{k}a_{i\ell}\sum_{j=1}^{n}b_{\ell j}x_j
=\sum_{j=1}^{n}\left(\sum_{\ell=1}^{k}a_{i\ell}b_{\ell j}\right)x_j.$$

따라서 $H$의 행렬은 $AB$다. Row-column 공식은 두 function을 차례로 적용하는 과정을 하나의 행렬로 표현한 결과다. $B$를 먼저 적용하므로 곱 $AB$에서도 오른쪽이 먼저 작용한다. 이산수학 M001 PDF pp.10–12와 [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 53:55]]의 설명을 일관된 $i,\ell,j$로 정리한 유도이며, 불명확한 판서 index를 그대로 복원한 식은 아니다.

### Associativity와 identity

세 function에 대해 $(F\circ G)\circ H$와 $F\circ(G\circ H)$는 둘 다 $H$, $G$, $F$ 순서로 입력을 처리한다. 같은 function이므로 유일한 matrix representation도 같아

$$(AB)C=A(BC)$$

가 된다. 이 associativity(결합법칙)는 순서를 바꾸는 commutativity(교환법칙)와 다르다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 01:01:27]]은 합성을 이해하면 결합법칙이 자연스럽다고 설명했다.

아무것도 바꾸지 않는 identity map에는 diagonal entries가 1이고 나머지가 0인 identity matrix(항등행렬) $I_n$이 대응한다. $A$가 $m\times n$이면

$$AI_n=I_mA=A.$$

왼쪽과 오른쪽의 identity 크기가 다를 수 있다는 점이 차원 확인의 좋은 예다. Square matrix에는 $A^r=A\cdots A$를 정의하고 $A^0=I_n$으로 정한다. Rectangular matrix에 같은 방식의 거듭제곱을 무조건 쓸 수는 없다.

## Inverse와 되돌릴 수 있는 변환

Square matrix $A$에 대해 $AB=BA=I_n$인 $B$가 존재하면 $A$는 invertible(가역)이며 $B=A^{-1}$라 쓴다. 모든 square matrix가 invertible한 것은 아니다. 예를 들어 zero matrix는 모든 입력을 0으로 보내므로 원래 입력을 구별해 되돌릴 수 없다.

$F(x)=Ax$가 bijective이면 $F^{-1}$도 linear하다. 임의의 출력 $y=F(u)$, $z=F(v)$에 대해

$$F^{-1}(y+z)=F^{-1}(F(u+v))=u+v=F^{-1}(y)+F^{-1}(z)$$

이고 $F^{-1}(cy)=cF^{-1}(y)$도 같다. 그 matrix representation이 $A^{-1}$다. Injection만으로 전체 codomain에서 inverse가 존재하는 것은 아니며, 여기서는 bijection이 필요하다.

Inverse의 유일성도 결합법칙으로 확인할 수 있다. $B,C$가 둘 다 $A$의 inverse이면

$$B=BI=B(AC)=(BA)C=IC=C.$$

이 계산은 단순히 같은 역할의 이름을 붙인 것이 아니라 두 후보가 실제로 같다는 증명이다. 정의와 대응은 이산수학 M001 PDF pp.8,12에 있다.

## Neural-network layer와 batch input

이산수학 M001 PDF p.6의 계산을 보자.

$$W=\begin{pmatrix}1&4\\2&5\end{pmatrix},\quad
X=\begin{pmatrix}2\\3\end{pmatrix},\quad
B=\begin{pmatrix}2\\1\end{pmatrix}.$$

각 row가 입력의 weighted sum(가중합)을 만들므로

$$WX=\begin{pmatrix}1\cdot2+4\cdot3\\2\cdot2+5\cdot3\end{pmatrix}
=\begin{pmatrix}14\\19\end{pmatrix},\qquad
WX+B=\begin{pmatrix}16\\20\end{pmatrix}.$$

$B$는 bias(편향)다. 자료는 이를 neural-network layer의 계산으로 소개하지만, 엄밀한 linearity 정의를 적용하면 $B\ne0$인 $X\mapsto WX+B$는 원점을 보존하지 않는 affine map(아핀사상)이다. 이는 앞의 정의로 구별한 해설이다.

[[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 13:23, 41:57]]에서는 이런 계산 뒤에 ReLU 같은 nonlinear activation(비선형 활성화)을 넣는 이유를 설명했다. ReLU는 성분마다 $\max(0,t)$를 적용한다. Linear map만 합성하면 다시 하나의 linear map이 된다. Bias가 있는 두 affine map도 activation 없이 합성하면

$$W_2(W_1x+b_1)+b_2=(W_2W_1)x+(W_2b_1+b_2)$$

라는 하나의 affine map으로 정리된다. 여러 층의 표현을 단순한 한 번의 affine 계산과 다르게 만드는 데 nonlinear 단계가 중요하다. 위 양수 출력에 ReLU를 적용하면 $(16,20)^T$는 그대로지만, 음수 성분이 있으면 0으로 바뀐다.

이처럼 layer에서 matrix 계산을 반복한다는 점은 hardware의 성능을 비교하는 동기도 된다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 14:22]]에서 강사는 model의 많은 계산이 matrix multiplication에 집중되어 bottleneck(병목)이 되므로 이를 hardware benchmark(성능 비교 기준)로 사용한다고 설명했다. 이는 모든 model의 전력 중 일정 비율을 측정한 결과가 아니라 계산 부담에 관한 동기 설명이다. 해당 STT에 불명확하게 남은 hardware 약어도 특정 장치명으로 확정하지 않는다.

한편 $AX$를 언제나 두 function의 composition으로 읽을 필요는 없다. $X=[x_1\ \cdots\ x_k]$가 여러 입력을 columns로 쌓은 것이라면

$$AX=[Ax_1\ \cdots\ Ax_k]$$

는 동일한 map을 여러 입력에 적용한 batch(묶음) 계산이다. [[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 STT 01:05:20]]은 이 두 용법을 구별했다. 행렬곱이라는 표기는 같지만 한쪽 행렬이 변환을 나타내는지 데이터 묶음인지 문맥을 읽어야 한다.

## 핵심 정리

- m×k와 k×n의 곱은 m×n이며, 합산 index는 공통 차원을 따른다.
- Linear map의 j번째 기본 입력 image는 표현 행렬의 j번째 column이다.
- Composition은 오른쪽 행렬부터 작용한다. Associativity는 순서 교환을 허용하지 않는다.
- Bias가 0이 아니면 affine map이며, batch 행렬의 columns는 여러 입력을 나타낼 수 있다.

## 확인·연습문제

### 개념과 풀이 확인

#### 확인 Q01 · 차원과 성분, 순서

A가 2×3, B가 3×4일 때 AB의 크기와 c₂₄를 쓰라. BA와 A+B는 가능한가? A=[[1,1],[0,1]], B=[[1,0],[0,2]]인 별도 예에서는 AB,BA를 비교하라.

<details><summary>해설 보기</summary>

첫 경우 AB는 2×4이고 c₂₄=a₂₁b₁₄+a₂₂b₂₄+a₂₃b₃₄다. 합산 index는 1부터 3까지 움직이고 row 2와 column 4는 남는다. BA는 안쪽 차원 4와 2가 맞지 않아 정의되지 않고, A+B도 크기가 달라 정의되지 않는다. 두 번째 예는 AB=[[1,2],[0,2]], BA=[[1,1],[0,2]]다. 둘 다 정의되어도 일반적으로 교환되지 않는다.

**점검 기준:** 안쪽·바깥쪽 차원, component-wise addition 조건, 두 곱의 다른 (1,2) 성분을 확인한다.

</details>

#### 확인 Q02 · Identity·power·inverse의 유일성

3×2 행렬 A의 양쪽 identity 크기를 정하라. Square matrix의 A⁰와 inverse 정의를 쓰고, 두 inverse B,C가 같음을 증명하라. 모든 square matrix가 invertible한가?

<details><summary>해설 보기</summary>

I₃A=A, AI₂=A다. Square A의 A⁰=I이며 Aʳ는 r번 곱이다. AB=BA=I인 B가 inverse다. B,C가 inverse라면 B=BI=B(AC)=(BA)C=IC=C로 같다. 결합법칙을 썼지 곱의 순서를 바꾸지 않았다. Zero matrix는 어떤 행렬을 곱해도 zero라 identity를 만들지 못하므로 모든 square matrix가 invertible한 것은 아니다.

**점검 기준:** Identity 차원을 구분하고 두 방향의 inverse 정의, 유일성의 각 등식을 확인한다.

</details>

#### 확인 Q03 · Bias와 activation

W=[[1,4],[2,5]], X=(2,3)ᵀ, B=(2,1)ᵀ에서 WX와 WX+B를 계산하라. F(X)=WX+B의 linearity와 ReLU 적용 결과를 설명하고, activation 없는 두 affine 층을 합쳐 보라.

<details><summary>해설 보기</summary>

WX=(14,19)ᵀ, WX+B=(16,20)ᵀ다. F(0)=B≠0이므로 엄밀한 linear map이 아니라 affine map이다. ReLU는 각 성분에 max(0,t)를 적용하므로 이 출력은 그대로이고, 예를 들어 (−2,3)ᵀ는 (0,3)ᵀ가 된다. 두 층은 W₂(W₁x+b₁)+b₂=(W₂W₁)x+(W₂b₁+b₂)라는 하나의 affine map으로 합쳐진다. Nonlinear activation이 없으면 층을 여러 개 놓아도 이 형태를 벗어나지 않는다.

**점검 기준:** Weighted sum 계산, 원점 검사, 음수에 대한 ReLU, 합성 bias를 모두 확인한다.

</details>

#### 확인 Q04 · 기본 방향으로 scalar 출력 결정

Linearity의 두 조건을 쓰고 F:ℝ→ℝ가 F(x)=ax인 이유를 보이라. F:ℝ²→ℝ에서 F(e₁)=3,F(e₂)=−2이면 F(4,5)를 구하고 일반적인 dot-product 표현도 설명하라.

<details><summary>해설 보기</summary>

조건은 F(u+v)=F(u)+F(v), F(cu)=cF(u)다. a=F(1)이면 F(x)=F(x·1)=xF(1)=ax다. 다변수에서는 x=Σⱼxⱼeⱼ이므로 F(x)=ΣⱼxⱼF(eⱼ)=a·x다. 예에서는 F(4,5)=4·3+5·(−2)=2다. 반대로 고정된 a와의 dot product는 합과 scalar multiplication에 분배되어 두 조건을 만족한다.

**점검 기준:** 한 방향에서 여러 기본 방향으로 확장하는 유도와 역방향 linearity 확인을 포함한다.

</details>

#### 확인 Q05 · Columns로 만드는 유일한 표현

F(e₁)=(1,2)ᵀ,F(e₂)=(4,5)ᵀ인 linear map의 행렬과 F(2,3)을 구하라. Coordinate function의 rows와 image의 columns가 어떻게 연결되며 행렬이 왜 유일한가?

<details><summary>해설 보기</summary>

A=[[1,4],[2,5]]이고 F(2,3)=2F(e₁)+3F(e₂)=(14,19)ᵀ다. i번째 coordinate function은 row aᵢ와 입력의 dot product이고, j번째 column 전체가 F(eⱼ)다. aᵢⱼ는 입력 j가 출력 i에 기여하는 계수다. Ax=Bx가 모든 x에 대해 같으면 x=eⱼ를 대입해 모든 columns가 같으므로 A=B다. 유일성은 고정된 standard coordinates에서의 주장이다.

**점검 기준:** Image를 row로 잘못 놓지 않고, 모든 기본 입력을 대입하는 유일성 논증을 쓴다.

</details>

#### 확인 Q06 · Function sum과 linearity 구분

(F₁+F₂)(u)=F₁(u)+F₂(u)와 F(u+v)=F(u)+F(v)는 무엇이 다른가? Linear maps의 sum과 scalar multiple이 linear임을 두 조건으로 확인하고 대응 행렬을 쓰라.

<details><summary>해설 보기</summary>

첫 식은 두 함수를 더해 새 함수를 만드는 정의이고, 둘째는 한 함수가 만족하는 성질이다. S=F₁+F₂이면 S(u+v)=F₁(u)+F₁(v)+F₂(u)+F₂(v)=S(u)+S(v), S(cu)=cF₁(u)+cF₂(u)=cS(u)다. H=tF이면 H(u+v)=tF(u)+tF(v)=H(u)+H(v), H(cu)=tcF(u)=cH(u)다. 대응 행렬은 A₁+A₂와 tA다.

**점검 기준:** 함수 정의와 성질을 구분하고 sum·scalar multiple 모두에서 두 조건을 확인한다.

</details>

#### 확인 Q07 · Composition에서 row-column 식 유도

G:ℝⁿ→ℝᵏ, F:ℝᵏ→ℝᵐ가 linear이고 G(x)=Bx,F(y)=Ay다. F∘G의 linearity와 표현 행렬의 cᵢⱼ를 유도하라.

<details><summary>해설 보기</summary>

H(u+v)=F(G(u)+G(v))=H(u)+H(v), H(cu)=F(cG(u))=cH(u)다. 성분으로 zᵢ=Σℓaᵢℓyℓ=ΣℓaᵢℓΣⱼbℓⱼxⱼ=Σⱼ(Σℓaᵢℓbℓⱼ)xⱼ이므로 cᵢⱼ=Σℓ₌₁ᵏaᵢℓbℓⱼ다. A는 m×k, B는 k×n이며 H(x)=(AB)x다. 오른쪽 B가 먼저 작용하므로 BA가 아니다.

**점검 기준:** Linearity 두 조건, index 범위, 중간 성분의 소거와 곱의 순서를 확인한다.

</details>

#### 확인 Q08 · Associativity와 inverse map

행렬곱의 associativity를 function composition으로 설명하라. Bijective linear F의 inverse도 linear임을 보이고, 왜 injection만으로 충분하지 않은지 말하라.

<details><summary>해설 보기</summary>

(F∘G)∘H와 F∘(G∘H)는 모두 H,G,F 순서로 작용한다. 같은 함수의 행렬 표현은 유일하므로 (AB)C=A(BC)다. 이는 행렬 순서를 바꾸는 주장이 아니다.

y=F(u),z=F(v)라 두면 F⁻¹(y+z)=F⁻¹(F(u+v))=u+v=F⁻¹(y)+F⁻¹(z)다. 마찬가지로 F⁻¹(cy)=F⁻¹(F(cu))=cu=cF⁻¹(y)다. 따라서 inverse가 linear하고 그 행렬은 A⁻¹이다. Injection만이면 codomain에 도달하지 못한 y의 inverse 값이 없을 수 있다.

**점검 기준:** 동일한 작용 순서와 표현의 유일성, inverse의 두 linear 조건 및 surjection 필요성을 설명한다.

</details>

#### 확인 Q09 · Batch input의 뜻

A가 m×n, X=[x₁ … xₖ]가 n×k이면 AX의 각 column은 무엇인가? X도 반드시 두 번째 transformation인가?

<details><summary>해설 보기</summary>

AX는 m×k이며 j번째 column은 Axⱼ다. 따라서 한 map A를 k개의 입력에 적용한 결과를 묶었다고 해석할 수 있다. 이 문맥의 X는 samples를 columns로 쌓은 데이터다. 같은 행렬곱 표기라도 두 변환의 composition을 의도하는 경우와 구별해야 한다.

**점검 기준:** 입력·출력의 크기와 각 column의 의미를 말하며 X의 역할을 문맥으로 정한다.

</details>

### 응용의 의미 확인

#### 확인 Q10 · Graph의 연결을 matrix로 표현하기

Vertex가 n개인 graph의 연결 여부를 matrix에 기록할 때 row, column, entry는 각각 무엇에 대응하는가? 행렬의 크기를 설명하고, 이 표현을 안다는 것과 graph algorithm을 배웠다는 것을 구별하라.

<details><summary>해설 보기</summary>

각 row와 각 column에 n개의 vertex를 같은 순서로 대응시키면 n×n matrix가 된다. Entry aᵢⱼ는 row의 vertex i와 column의 vertex j가 연결되어 있는지를 기록한다. 따라서 단순한 숫자 배열에도 두 대상 사이의 관계라는 의미를 붙일 수 있다.

이는 연결 관계를 데이터로 표현하는 동기다. 그 표현을 입력으로 받아 어떤 문제를 풀지, 어떤 계산 단계를 사용할지까지 정한 것은 아니므로 graph나 communication network의 algorithm을 배웠다는 결론은 나오지 않는다.

**점검 기준:** 두 index가 각각 vertex를 고른다는 점, n×n의 이유, entry의 의미와 표현·algorithm의 차이를 모두 설명한다.

</details>

#### 확인 Q11 · 반복되는 matrix 계산과 hardware benchmark

Neural-network layer의 matrix multiplication이 hardware benchmark의 동기가 되는 이유를 설명하라. 이 설명만으로 모든 model의 전력 중 일정 비율이 matrix multiplication에 쓰인다고 결론 내릴 수 있는가?

<details><summary>해설 보기</summary>

Layer는 W와 입력 X를 곱하는 계산을 사용하고, 여러 layer와 입력에 이 계산이 반복된다. 따라서 matrix multiplication의 계산 부담이 누적되어 bottleneck이 될 수 있다. 이 workload를 얼마나 잘 처리하는지 비교하는 것은 그 계산이 중요한 model에 사용할 hardware를 평가하는 한 가지 기준이 된다.

이는 반복되는 계산이 성능 비교에 중요한 이유를 설명한 것이다. Model마다 계산 구성과 반복 횟수가 다르고 hardware의 처리 방식도 다르므로, 이 동기 설명이 모든 model에 공통인 전력 비율의 측정값을 주지는 않는다. 한 benchmark에서의 성능을 다른 모든 작업의 성능이나 전력 절감률로 바꿔 말해서도 안 된다.

**점검 기준:** 반복되는 WX 계산에서 부담의 누적·bottleneck·benchmark로 이어지는 이유를 설명하고, 측정하지 않은 보편적 전력 비율을 주장하지 않는다.

</details>

### 적용 연습

#### 연습 P01 · 두 입력을 합쳐 처리해도 되는가

**새로 만든 강의 기반 일반 연습.** 현재 기출 후보에는 basis image·bias·batch를 함께 확인하는 직접 문항이 없어 기출형이라고 부르지 않는다. 선수내용은 본문의 linear combination과 affine map이다.

F(e₁)=(1,0)ᵀ,F(e₂)=(1,1)ᵀ인 linear F와 b=(0,1)ᵀ에 대해 H(x)=F(x)+b라 하자. x=(1,0)ᵀ,y=(0,1)ᵀ를 각각 처리한 H(x),H(y)와 H(x+y)를 구하라. H(x)+H(y)=H(x+y)인가? Batch로 처리할 때 bias는 어디에 더하는가?

<details><summary>해설 보기</summary>

F의 행렬은 A=[[1,1],[0,1]]이다. H(x)=(1,1)ᵀ, H(y)=(1,2)ᵀ여서 합은 (2,3)ᵀ다. 하지만 H(x+y)=(2,2)ᵀ다. 따로 계산해 더하면 bias가 두 번 들어가고, 합친 입력은 한 번만 들어가기 때문이다. X=[x y]에 대해 AX의 각 column에 b를 각각 더해야 [H(x) H(y)]가 된다. H가 affine이라는 점이 합 보존 실패를 설명한다.

**점검 기준:** 행렬 구성·세 출력·bias 횟수를 계산하고 batch의 각 sample에 bias를 적용한다.

</details>

### 짧은 복습 계획

Q01의 차원과 Q05의 column 배치를 먼저 확인한다. Q06–Q08은 함수식으로 증명한 다음 대응하는 행렬식을 쓴다. Q03과 Q09를 비교해 transformation·bias·입력 묶음을 구별한 뒤 P01을 풀어 본다. Q10–Q11에서는 연결 관계의 표현과 반복되는 계산의 부담을 각각 한 문장으로 설명하고, 응용 동기에서 실제로 따라오지 않는 결론을 표시한다.

## 출처

[[courses/discrete_mathematics/lectures/2026-09-07-lecture-02|2026-09-07 이산수학 강의·자료 연결]] · [[courses/discrete_mathematics/lectures/2026-09-09-lecture-03|2026-09-09 이산수학 강의·자료 연결]]

[01. Vectors and Matrices.pdf 원문 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/01.Vectors.and.Matrices.pdf) · 페이지별 보기: [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-002), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/discrete_mathematics/01.vectors.and.matrices/page-012)

[[courses/discrete_mathematics/transcripts/2026-09-07|2026-09-07 보정 STT]] · 07:50, 14:22, 10:34, 23:09, 26:21, 32:22, 36:35, 53:55, 16:05, 01:01:27, 01:05:20, 13:23, 41:57.

[[courses/discrete_mathematics/transcripts/2026-09-09|2026-09-09 보정 STT]] · 08:54.

2026-09-07의 설명과 2026-09-09의 linear-map 복습을 연결한다. p.2와 07:50은 graph의 연결 표현 동기이고, 14:22는 반복되는 matrix 계산과 hardware benchmark의 동기다. 후자는 모든 model에 공통인 전력 비율을 측정한 결과가 아니다. 판서의 불명확한 첨자는 일관된 i,ℓ,j로 정리했으며 정확한 판서 복원은 아니다. Affine 구별은 linearity 정의를 적용한 설명이다. Basis change, 역행렬 계산법과 generalized inverse는 다루지 않는다.

보정 STT에 남은 불명확한 말은 그대로 한계로 남는다. 아래 풀이의 정돈된 수식과 설명용 계산이 그 발화를 복원했다는 뜻은 아니다.

현재 기출 후보에는 unit-vector representation의 유일성, affine/activation, batch 해석을 직접 묻는 문항이 없다. Matrix-chain의 비용은 [[courses/discrete_mathematics/units/search-and-matrix-complexity|검색·행렬곱 비용]]에서 연결한다. Linear dependence 증명과 chain Dynamic programming은 별도 선수내용이므로 여기서는 강의 기반 일반 연습을 한다.


---

[[courses/discrete_mathematics/units/sets-functions-sequences|← 이전: Sets·Functions·Sequences로 구조 표현하기]] · [[courses/discrete_mathematics/units/index|단원 목차]] · [[courses/discrete_mathematics/units/algorithms-search-and-sort|다음: Algorithm 명세와 Searching·Sorting의 실행 →]]
