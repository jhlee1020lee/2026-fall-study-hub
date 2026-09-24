---
title: "Higher-Order Functions와 계산 구조의 재사용"
description: "함수 인자로 계산을 재사용하고 mapReduce의 종료값·결합 순서·정보 보존을 분석합니다."
course: "principles_of_programming"
unit_id: "higher-order-functions"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-17-lecture-05"]
---

계산 방법을 함수 값으로 전달하면 항 생성과 공통 재귀 구조를 분리할 수 있습니다. 구간의 끝·빈 경우·결합 순서를 함께 추적하며 재사용과 분산 결합에 필요한 조건을 확인합니다.

## Function value(함수 값): 계산 방법을 입력으로 전달하기

정수 `3`을 다른 함수에 전달하듯 계산 방법 자체도 전달할 수 있다면, 같은 계산 구조를 여러 목적에 재사용할 수 있다. Function value는 복사하거나 argument(인자)로 넘기거나 결과로 반환할 수 있는 값이다. Function type(함수 타입)은 어떤 입력을 받아 어떤 결과를 내는지를 나타낸다. 예를 들어 `Int => Int`는 정수 하나를 받아 정수를 내는 함수의 type이고, `(Int, Int) => Int`는 정수 둘을 받아 정수를 내는 함수의 type이다.

함수를 입력으로 받거나 결과로 반환하는 함수가 Higher-order function(고차 함수)이다. 이 기준에서 중요한 것은 함수 body(본문)의 길이나 재귀 여부가 아니라, 입력과 결과에 함수 값이 있는가다. 9월 17일 강의는 이 성질을 코드 재사용의 동기로 연결했다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 00:21–02:15]] [POP M002 p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### 합·제곱합·세제곱합에서 달라지는 부분 찾기

[[courses/principles_of_programming/units/expressions-functions|함수 적용과 기본 재귀]]를 이용하면 자료의 세 합을 다음과 같이 표현할 수 있다.

```scala
def sumLinear(n: Int): Int =
  if (n <= 0) 0 else n + sumLinear(n - 1)

def sumSquare(n: Int): Int =
  if (n <= 0) 0 else n * n + sumSquare(n - 1)

def sumCubes(n: Int): Int =
  if (n <= 0) 0 else n * n * n + sumCubes(n - 1)
```

세 함수는 `n<=0`에서 끝나고, 한 항을 만든 뒤 `n-1`까지의 결과에 더한다. 달라지는 것은 현재 항을 만드는 `n`, `n*n`, `n*n*n`뿐이다. 이 차이를 하나의 고정된 `Int`로 전달하면 다음 단계의 `n`에 맞춰 항을 바꿀 수 없다. `n`을 받아 항을 계산하는 `Int => Int` 함수가 필요하다. [POP M002 pp.46–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def sum(f: Int => Int, n: Int): Int =
  if (n <= 0) 0 else f(n) + sum(f, n - 1)

def linear(n: Int) = n
def square(n: Int) = n * n
def cube(n: Int) = n * n * n

def sumLinear(n: Int) = sum(linear, n)
def sumSquare(n: Int) = sum(square, n)
def sumCubes(n: Int) = sum(cube, n)
```

위 코드는 앞의 세 정의를 대체하는 별도 버전이다. `sum(square,3)`은 `square(3)+square(2)+square(1)+0=9+4+1=14`다. 같은 재귀 구조에 `linear`를 주면 `6`, `cube`를 주면 `27+8+1=36`이다. 재귀의 경계와 진행 방식은 한 곳에 남고 항 계산만 바뀐다. 9월 17일 07:08의 설명이 말하는 “바뀌는 부분을 인자로 받는다”는 것이 이 과정이다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 07:08–10:56]]

## Anonymous function(익명 함수)과 Type inference(타입 추론)

한 번 전달할 간단한 함수를 위해 늘 별도 이름을 만들 필요는 없다. Anonymous function은 함수 값을 사용 위치에 바로 표현한다. 자료의 일반 형식은 `(x1: T1, ..., xn: Tn) => e`다. 왼쪽은 parameter(매개변수), 오른쪽은 입력을 받았을 때 계산할 body다. 함수 값을 만드는 것과 그 body를 실제 argument로 평가하는 것은 구분한다.

```scala
def sumLinear(n: Int) = sum((x: Int) => x, n)
def sumSquare(n: Int) = sum((x: Int) => x * x, n)
def sumCubes(n: Int) = sum((x: Int) => x * x * x, n)
```

여기서 `sum`의 첫 parameter type이 `Int => Int`이므로 입력 type을 알 수 있는 문맥이 있다. 자료는 이를 이용한 `sum((x) => x * x, n)` 같은 생략형도 제시한다. Type annotation(타입 명시)을 생략할 수 있다는 것과, 명시할 이유가 없다는 것은 다르다. `(x: Int)`라고 쓰면 독자가 호출 문맥을 거슬러 올라가지 않고도 입력 의도를 읽을 수 있고 잘못 추론된 type도 알아차리기 쉽다. [POP M002 p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

9월 17일 13:53–17:05에서는 이 가독성의 이유와, IDE가 type을 보여 줄 때 달라지는 점을 함께 논의했다. STT의 “무조건 쓰게 한다”는 표현은 바로 이어지는 생략 예와 맞지 않으므로 모든 anonymous parameter에 적용하는 규칙으로 읽지 않는다. 여기서 쓰는 문법과 변환은 제공된 자료의 Scala 문맥이다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 13:53–17:05]]

## Inclusive range(양 끝을 포함하는 구간)와 빈 구간의 값

이번에는 1부터 `n`까지가 아니라 `a`부터 `b`까지 처리한다고 하자. 자료의 다음 `sum`과 `product`는 앞의 두 인자 `sum`과 구분되는 범위 버전이다. [POP M002 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def sum(f: Int => Int, a: Int, b: Int): Int =
  if (a <= b) f(a) + sum(f, a + 1, b) else 0

def product(f: Int => Int, a: Int, b: Int): Int =
  if (a <= b) f(a) * product(f, a + 1, b) else 1
```

조건이 `a <= b`이므로 `a=b`인 마지막 항도 처리한다. 다음 호출에서 `a+1>b`가 되면 빈 구간의 결과를 반환한다. 처음부터 `a>b`이면 `f`를 한 번도 적용하지 않는다.

`f(x)=x`를 `2..4` 구간에 적용하면 합은 `2+(3+(4+0))=9`, 곱은 `2*(3*(4*1))=24`다. 합의 빈 구간 결과 `0`과 곱의 빈 구간 결과 `1`은 각각 identity element(항등원)다. 끝에서 아무 항도 더하거나 곱하지 않았다는 의미를 보존한다. 곱의 종료값을 `0`으로 바꾸면 빈 구간뿐 아니라 모든 비어 있지 않은 곱도 마지막 0 때문에 0이 된다.

따라서 재귀의 base case(기저 경우)는 단지 멈추기 위한 장치가 아니다. 전체 계산의 뜻을 결정한다. 구간 끝을 포함하는지, 빈 경우 무엇을 반환하는지까지 함수의 계약에 들어간다. 이 예의 계산은 `a+1`의 진행과 결과가 `Int` 범위 안에 있는 작은 구간을 사용한다.

## `mapReduce`: 항 생성·결합·종료값을 분리하기

범위 `sum`과 `product`에는 여전히 같은 진행 구조가 반복된다. 이번에는 항을 만드는 `f`뿐 아니라 결과를 결합하는 연산과 빈 구간의 값도 parameter로 만들 수 있다. 자료 p.50은 p.49의 DRY 연습에 다음 구성을 제공한다.

```scala
def mapReduce(
  reduce: (Int, Int) => Int,
  inival: Int,
  f: Int => Int,
  a: Int,
  b: Int
): Int = {
  if (a <= b)
    reduce(f(a), mapReduce(reduce, inival, f, a + 1, b))
  else inival
}

def sum(f: Int => Int, a: Int, b: Int): Int =
  mapReduce((x, y) => x + y, 0, f, a, b)

def product(f: Int => Int, a: Int, b: Int): Int =
  mapReduce((x, y) => x * y, 1, f, a, b)
```

`f`는 현재 위치의 항을 만들고, `reduce`는 현재 항과 뒤 구간의 결과를 결합한다. `inival`은 원본의 parameter 이름으로, 빈 구간의 결과다. `a,b`는 어디를 처리할지 정한다. 따라서 `product`를 `sum`으로 바꾸려면 곱셈을 덧셈으로 바꾸는 것뿐 아니라 `inival`도 `1`에서 `0`으로 바꾸어야 한다. 덧셈에 `1`을 그대로 주면 원하는 합보다 1이 크고, 빈 구간의 결과도 달라진다. [POP M002 pp.49–50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

`a=2,b=4`에서 결과의 결합 구조는 다음과 같다.

```text
reduce(f(2),
  reduce(f(3),
    reduce(f(4), inival)))
```

현재 항과 뒤쪽 결과를 이 순서로 결합한다. 임의의 `reduce`를 전달할 수 있다는 사실이 그 연산을 마음대로 재배열해도 된다는 뜻은 아니다. 자료의 결합 구조에 뺄셈을 넣어 보는 설명용 계산에서는 `2 - (3 - (4 - 0)) = 3`이다. 반면 같은 시작값 `0`에 항 `2,3,4`를 왼쪽부터 누적하면 `((0 - 2) - 3) - 4 = -9`다. 시작값 없이 세 항만 왼쪽부터 결합한 `(2 - 3) - 4`는 `-5`로 또 다르다. 따라서 누적 방식으로 바꿀 때는 결합 방향뿐 아니라 시작값의 위치와 인자 순서도 보존해야 한다. 합에서 눈에 띄지 않던 차이가 다른 연산에서는 결과를 바꾼다. 재사용 가능한 함수를 만들수록 전달한 연산에 어떤 성질을 요구하는지도 분명히 해야 한다.

### 함수의 type에서 역할과 결합 방향 읽기

과거의 list 처리 문항에서도 종료값과 결합 함수를 분리하는 사고가 사용된다. 지금의 `inival`·`reduce`를 이해하면, 입력 값과 “현재 항 + 나머지 결과를 결합하는 규칙”이 왜 서로 다른 역할인지 설명할 수 있다. 다만 그 문항 전체에는 사용자 정의 list와 타입 매개변수가 필요하므로 이 단원만으로 구현 준비가 끝났다고 볼 수 없다. [EX:pop_2024_mid_q01_s01 L.50-53]

또 다른 과거 문항은 산술 연산 자체를 함수 입력으로 받아 평가 구조를 재사용한다. 여기서 가져올 연결은 “계산의 공통 구조와 연산의 구체적 의미를 분리한다”는 점이다. 완전한 evaluator 구현에 필요한 `Expr`·`Result` 자료형, 다형성과 예외 처리는 후속 전제다. [EX:pop_2024_mid_q03_s04 L.77-81]

두 연결 모두 기존 강의의 `sum`·`mapReduce`를 더 정확히 읽기 위한 것이다. 예를 들어 결과 type이 `Int`이면 현재 계산의 수치 결과를 받고, 결과 type이 함수 type이면 아직 남은 입력을 받아야 한다. 이 차이가 함수 반환과 currying으로 이어진다.

## Map과 Reduce로 큰 데이터를 나누어 계산하기

9월 17일의 강의는 매우 많은 사용자의 나이 통계처럼 한 컴퓨터에 담기 어려운 데이터를 동기로 든다. 전체를 여러 서버로 나누고, 각 서버에서 데이터별 계산인 map을 수행한 뒤 부분 결과를 reduce로 결합하는 개략 구조다. 앞의 재귀 함수는 이 사고를 작은 구간에서 보여 주지만, 분산 처리는 부분 결과를 어떻게 보존하고 합칠지까지 요구한다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 22:33–27:04]]

평균을 예로 들면 정보 보존의 필요성이 드러난다. 다음은 강의의 통계 동기를 설명하기 위해 만든 계산이다. 한 묶음에 값 `10` 하나, 다른 묶음에 `20` 세 개가 있다고 하자. 두 묶음의 평균은 각각 `10`, `20`이지만, 이 평균 두 개를 단순히 평균내면 `15`다. 전체 자료의 평균은

$$
\frac{10+20+20+20}{4}=\frac{70}{4}=17.5
$$

로 다르다. 묶음의 크기가 다르기 때문이다. 부분 결과를 평균 하나 대신 `(합계, 개수)`로 보존하면 `(10,1)`과 `(60,3)`을 `(70,4)`로 합쳐 올바르게 계산할 수 있다.

분할한 계산을 다시 합칠 때는 이처럼 필요한 정보가 남아 있어야 한다. 또한 묶음의 결합 순서를 바꾸려면 결과가 보존되는 조건을 확인해야 한다. 여기의 평균 계산과 순서 조건은 설명을 위한 분석이며 STT의 손상된 표현을 복원한 발화가 아니다. 강의는 27:04에서 모든 작업을 이 단순한 구조에 그대로 맞출 수는 없다는 한정도 두었다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 25:31, 27:04]]

계산 방법을 값으로 주고받게 되면 또 하나의 문제가 생긴다. 함수가 원래 정의된 곳을 떠나 다른 곳에서 사용되어도 내부 이름의 의미는 유지되어야 한다. 그 요구가 [[courses/principles_of_programming/units/closures-currying|Closure와 environment의 보존]]으로 이어진다.

## 핵심 정리

- Higher-order function(고차 함수)은 함수를 인자로 받거나 반환한다. 긴 함수나 재귀 함수라는 뜻이 아니다.
- 항을 만드는 `f:Int=>Int`를 받으면 현재 위치에 따라 항을 바꾸면서 공통 진행 구조를 유지할 수 있다.
- Anonymous function(익명 함수)의 type은 문맥에서 추론할 수 있다. 명시적 annotation은 사람이 읽을 때 입력 의도를 드러낸다.
- Inclusive range(양 끝 포함 구간)는 `a=b`도 한 항 처리한다. 빈 합의 0과 빈 곱의 1은 전체 계산 의미의 일부다.
- `mapReduce`의 `f`·`reduce`·`inival`은 항 생성·결합·빈 결과를 각각 맡는다. 임의의 결합 함수를 받는다고 순서를 마음대로 바꿀 수는 없다.
- 큰 데이터를 나눈 뒤 결합하려면 부분 결과에 필요한 정보가 남아 있어야 한다. 부분 평균만으로는 묶음 크기를 잃는다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Function value와 공통 합산 구조

Function value와 higher-order function의 기준을 설명하라. 1..n의 합·제곱합·세제곱합을 공통화할 때 고정된 정수 대신 `Int=>Int`를 받는 이유, 공통 재귀식, n=3의 세 값을 적어라.

<details><summary>해설 보기</summary>

함수 값은 복사·인자 전달·반환할 수 있으며 function type은 입력과 결과를 나타낸다. 함수를 인자로 받거나 반환하면 higher-order function이다. 세 합은 `n<=0`이면 0, 아니면 현재 항과 n-1까지의 결과를 더한다. 달라지는 항을 `f(n)`으로 만들면 `sum(f,n)=if(n<=0)0 else f(n)+sum(f,n-1)`이다. 고정 정수는 위치마다 바뀌는 n, n*n, n*n*n을 표현하지 못한다. n=3에서 각각 `3+2+1=6`, `9+4+1=14`, `27+8+1=36`이다.

**채점·확인:** 함수 값의 세 사용, higher-order 기준, 함수 인자 필요성과 공통식·세 계산을 설명한다.

</details>

#### 확인 Q02 · 익명 함수와 type 문맥

이름을 미리 정의하지 않고 `sum`에 제곱항을 전달하라. `(x)=>x*x`에서 x의 type을 알 수 있는 이유와 annotation을 유지할 이유는? 함수 값을 만드는 때와 body 실행은 같은가?

<details><summary>해설 보기</summary>

`sum((x: Int)=>x*x,n)`으로 함수 값을 직접 전달한다. sum이 `Int=>Int`를 요구하므로 이 예의 `(x)=>x*x`에서도 x가 Int인 문맥을 얻는다. Annotation은 독자가 호출 문맥을 추적하지 않고 의도를 읽고 잘못된 추론을 알아차리는 데 도움을 준다. IDE의 type 표시도 이를 보완할 수 있다. 함수 값을 표현하는 것과 실제 argument로 body를 계산하는 것은 별개다. 이 생략 예를 모든 문맥·버전에 대한 규칙으로 확대하지 않는다.

**채점·확인:** 익명 전달 코드, 추론 문맥, 사람을 위한 annotation 이유와 실행 시점의 차이를 포함한다.

</details>

#### 확인 Q03 · 구간의 끝과 빈 결과

`f(x)=x`에 대한 범위 sum·product를 2..4, 4..4, 5..4에서 구하라. `a<=b`와 각 종료값의 의미를 설명하고 product의 빈 결과를 0으로 바꾸면 어떻게 되는지 보여라.

<details><summary>해설 보기</summary>

2..4에서는 sum이 `2+(3+(4+0))=9`, product가 `2*(3*(4*1))=24`다. 4..4는 마지막 한 항도 포함하여 각각 4다. 5..4는 처음부터 비어 f를 쓰지 않고 각각 0과 1을 반환한다. 0은 덧셈, 1은 곱셈의 identity element다. `product`의 종료값이 0이면 `2*(3*(4*0))=0`이 되어 비어 있지 않은 곱까지 모두 망가진다.

**채점·확인:** 세 구간의 여섯 결과, 끝 포함과 빈 경우 f 미호출, 항등원의 이유를 제시한다.

</details>

#### 확인 Q04 · mapReduce 인자들의 역할

`mapReduce(reduce,inival,f,a,b)`에서 다섯 인자의 역할과 2..4의 중첩 구조를 적어라. `product`를 `sum`으로 바꾸려면 무엇을 함께 바꾸어야 하며 초기값 1을 남기면 어떤 결과인가?

<details><summary>해설 보기</summary>

f는 위치에서 항을 만들고 reduce는 현재 항과 뒤쪽 결과를 결합한다. inival은 빈 구간의 결과, a,b는 처리 범위다. 구조는 `reduce(f(2),reduce(f(3),reduce(f(4),inival)))`이다. 곱은 `reduce=(x,y)=>x*y`와 inival=1, 합은 `reduce=(x,y)=>x+y`와 inival=0을 쓴다. f가 identity이면 덧셈만 바꾸고 1을 남긴 2..4 결과는 `2+3+4+1=10`으로 원하는 9와 다르다. 빈 경우도 0 대신 1을 반환한다.

**채점·확인:** 항·결합·종료값의 구별, 정확한 인자 순서와 10의 잘못된 결과를 설명한다.

</details>

#### 확인 Q05 · 임의의 reduce를 재배열할 수 있는가

f가 identity, inival=0, 구간이 2..4이고 reduce가 뺄셈일 때 자료의 중첩 계산, 0부터 왼쪽 누적, 시작값 없는 왼쪽 결합을 각각 계산하라. 이 비교가 경고하는 것은?

<details><summary>해설 보기</summary>

자료 구조는 `2-(3-(4-0))=3`이다. 0부터 왼쪽 누적하면 `((0-2)-3)-4=-9`다. 시작값 없는 왼쪽 결합은 `(2-3)-4=-5`다. 같은 항과 뺄셈을 썼어도 결합 방향·초기값 위치·argument 순서가 달라 결과가 바뀐다. 덧셈 예에서 차이가 안 보였다고 임의의 reduce에도 재배열이 안전하다고 결론 내릴 수 없다.

**채점·확인:** 3/-9/-5를 괄호 구조와 함께 보이고 결과가 달라진 원인을 설명한다.

</details>

#### 확인 Q06 · 부분 평균이 잃는 정보

많은 사용자의 나이 통계라는 강의 동기에서 서버별 map·reduce는 어떤 역할인가? 한 묶음 `[10]`과 다른 묶음 `[20,20,20]`의 평균을 합칠 때 부분 평균의 단순 평균과 전체 평균을 비교하고 필요한 정보를 적어라.

<details><summary>해설 보기</summary>

데이터를 여러 서버에 나누고 각 서버에서 데이터별 계산인 map을 수행한 뒤 부분 결과를 reduce로 결합한다. 예의 부분 평균 10,20을 똑같이 평균내면 15다. 실제 전체는 `(10+20+20+20)/4=17.5`다. 묶음 크기가 다른데 같은 가중치를 주었기 때문이다. `(합계,개수)`로 `(10,1)`과 `(60,3)`을 보존하면 `(70,4)`로 합쳐 17.5를 얻는다. 순서를 바꾸려면 결과 보존 조건도 확인해야 한다. 이는 강의 동기의 설명 계산이며 모든 작업이 이런 단순 구조에 맞는 것은 아니다.

**채점·확인:** 15/17.5의 차이, 합계·개수의 충분한 정보, 적용 한계를 포함한다.

</details>

### 적용 연습

#### 연습 P01 · 누적 방향을 바꾼 리팩터링 검토

**새로 만든 synthetic(합성) 연습이며 실제 기출이 아니다.** 2024 중간 Q1-1 Main.scala [EX:pop_2024_mid_q01_s01 L.50-53]의 종료값·결합 함수 역할을 옮겼다. 현재 전제는 inclusive range·함수 인자·재귀·산술이다. 원문의 generic IList 구현은 추가 전제가 필요하다.

f가 identity, reduce가 `(x,y)=>x-y`, inival=0일 때 원래 범위 `mapReduce`를 '왼쪽부터 `acc-f(a)`로 누적'하게 바꾸어도 같은 결과라는 제안을 검토하라. 1..3, 2..2, 3..2를 모두 검사하고 동등성 판단에 필요한 조건을 설명하라.

<details><summary>해설 보기</summary>

| 구간 | 원래 오른쪽 중첩 | 0부터 왼쪽 누적 |
|---|---|---|
| 1..3 | `1-(2-(3-0))=2` | `((0-1)-2)-3=-6` |
| 2..2 | `2-0=2` | `0-2=-2` |
| 3..2 | 0 | 0 |

빈 경우만 같다고 변환이 옳지는 않다. 비어 있지 않은 경우 초기값 위치와 항의 argument 역할·결합 방향이 달라진다. 주어진 뺄셈은 위 반례로 제안을 거부할 수 있다. 다른 reduce에서는 그 연산과 초기값의 성질이 해당 재배열을 허용하는지 별도로 확인해야 한다. 테스트 몇 개에서 우연히 일치하는 것만으로 임의 연산의 동등성을 얻지는 않는다.

**채점·확인:** 세 구간의 양쪽 결과와 구조적 차이를 설명한다. 숫자 대입만 적지 말고 제안을 거부하는 반례의 역할을 적는다.

</details>

#### 연습 P02 · 연산의 의미만 함수로 바꾸기

**새로 만든 synthetic(합성) 연습이며 실제 기출이 아니다.** 2024 중간 Q3-4 Main.scala [EX:pop_2024_mid_q03_s04 L.77-81]에서 산술 연산을 함수 인자로 분리하는 요구를 가져왔다. 현재는 `Int` 함수 값·산술·적용만 사용한다. 원문의 Expr/Result·다형성·예외 처리는 후속 전제다.

`combine(op,x,y)`가 x+1과 y*2를 이 순서로 op에 전달하도록 작성하라. x=2,y=4에서 덧셈·곱셈·뺄셈 함수를 각각 주어 검산하고, 인자 순서를 뒤집은 오류를 왜 뺄셈이 드러내는지 설명하라.

<details><summary>해설 보기</summary>

~~~scala
def combine(op: (Int, Int) => Int, x: Int, y: Int): Int =
  op(x + 1, y * 2)
~~~

두 argument는 3과 8이다. `(a,b)=>a+b`이면 11, `(a,b)=>a*b`이면 24, `(a,b)=>a-b`이면 -5다. 뒤집으면 앞 둘은 여전히 11과 24라서 오류를 놓칠 수 있지만 뺄셈은 `8-3=5`로 바뀐다. 공통 구조는 두 입력을 준비하고 op에 적용하는 부분이며 op의 의미만 교체한다. 원문 evaluator를 구현하거나 원문의 예외 동작을 이 연습에 추가한 것은 아니다.

**채점·확인:** 함수 type·적용 순서·11/24/-5와 뒤집힌 5, 공통 구조와 교체 부분을 모두 확인한다.

</details>

### 복습 순서

Q01–Q02로 공통 구조와 항 함수를 분리한 뒤 Q03에서 빈 구간·한 항을 먼저 검사한다. Q04–Q05의 괄호를 직접 쓰고 P01·P02로 순서 오류를 찾는다. 끝으로 Q06에서 부분 결과에 빠진 정보가 없는지 설명한다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-17-lecture-05|2026-09-17 강의 노트 · 함수 값과 재사용]] / [[courses/principles_of_programming/transcripts/2026-09-17|보정 STT · 00:21–02:15, 07:08–10:56, 13:53–17:05, 20:11, 22:33–27:04]].
- [Lecture Part 1 · pp.45–50 함수 값·익명 함수·범위와 mapReduce](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).
- 과거 평가의 부분 연결: 2024 중간 Q1-1 Main.scala [EX:pop_2024_mid_q01_s01 L.50-53]의 종료값·결합 규칙, Q3-4 Main.scala [EX:pop_2024_mid_q03_s04 L.77-81]의 연산 함수 전달. P01·P02는 그 사고를 사용하는 새 합성 연습이다.

원문의 generic list·Expr/Result·예외 처리는 현재 단원만으로 다루지 않는다. Q3 제목의 40점과 소문항 합 35점은 원문에 남은 불일치이며 현 학기 배점으로 사용하지 않는다. 큰 데이터의 평균 계산은 강의 동기를 설명하는 분석이고 손상된 발화의 복원이 아니다.


---

[[courses/principles_of_programming/units/recursion|← 이전: Newton's Method, Recursion과 Tail Call]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/closures-currying|다음: Closures, 환경 보존과 Currying →]]
