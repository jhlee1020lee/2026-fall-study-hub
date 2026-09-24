---
title: "Closures, 환경 보존과 Currying"
description: "Closure의 환경 보존과 by-name을 이해하고 currying·부분 적용의 호출 단계를 추적합니다."
course: "principles_of_programming"
unit_id: "closures-currying"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-15-lecture-04", "courses/principles_of_programming/lectures/2026-09-17-lecture-05"]
---

함수 값이 이동해도 이름의 뜻이 유지되는 이유를 코드와 정의 환경의 쌍으로 설명합니다. By-name의 두 환경과 함수 반환의 단계별 타입을 추적하여 currying과 partial application을 정확히 읽어 봅니다.

## Closure(클로저): 함수가 이동해도 이름의 의미 유지하기

[[courses/principles_of_programming/units/blocks-scope|Block과 environment]]에서는 함수 body(본문)의 바깥 이름을 정의 위치에서 찾았다. 이제 function value(함수 값)를 다른 곳에 저장하거나 반환해 보자. 코드만 옮기면 어느 environment(환경)에서 이름을 찾아야 하는지 잃을 수 있다. Closure는 **함수 코드와 definition environment(정의 환경)를 함께 보존하는 값**이다.

자료 pp.51–52는 같은 코드에 두 실행 모델을 적용하여 이 필요성을 보여 준다. 아래의 `g _`는 자료에서 parameter가 있는 정의를 함수 값으로 변환하는 표기다. [POP M002 pp.51–52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
{
  val t = 0
  val f: Int => Int = {
    val t = 10
    def g(x: Int): Int = x + t
    g _
  }
  f(20)
}
```

바깥 environment를 `E0`, 안쪽을 `E1`이라고 하자. `g`의 parameter `x`는 호출 때 받지만, body의 `t`는 `g`가 정의된 `E1`의 `10`을 뜻한다. Parameter로 받지 않고 바깥 binding(이름 연결)을 찾는 이런 이름의 의미까지 보존해야 한다.

### 함수 코드만 저장한 모델의 20과 Closure 모델의 30

원본 p.51의 “without Closures” 실행표에서 볼 것은 `f`에 `(x)x+t`라는 코드만 저장한다는 점이다. 이 실패 모델은 `f`가 저장된 바깥 `E0`를 호출 환경의 부모로 삼는다. 그러면 `t=0`을 찾아 `f(20)=20`이 된다. **20은 올바른 closure 평가의 또 다른 정답이 아니라, 정보가 빠진 모델의 잘못된 결과**다.

p.52에서는 `f`에 `(E1, (x)x+t)`를 저장한다. 호출할 때 `x=20`인 새 environment `E2`를 만들고 그 부모를 보존된 `E1`로 연결한다.

| 단계 | 보존하거나 찾는 정보 | 결과 |
|---|---|---|
| 안쪽 함수 값 생성 | 코드 `x+t`와 정의 환경 `E1` | `(E1,(x)x+t)` |
| 바깥 `f`에 저장 | 같은 closure 값 | 정의 환경은 여전히 `E1` |
| `f(20)` 호출 | `E2: x=20`, 부모 `E1` | `x`는 `E2`에서 20 |
| Body의 `t` 찾기 | `E2`에 없으므로 `E1`로 이동 | 10 |
| 덧셈 | `20+10` | 30 |

원본 두 실행표에서 중요한 차이는 호출의 `E0::[E2|x=20]`와 `E1::[E2|x=20]`다. 함수 값을 어느 이름에 저장했는지가 아니라, 그 값이 보존한 정의 환경이 바깥 이름의 뜻을 정한다. 9월 17일 27:04의 질문도 함수 값이 여러 곳으로 이동해도 의미가 달라지면 안 된다는 요구에서 출발한다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 27:04, 35:09–41:04]]

## Scope와 Lifetime(수명): block이 끝나도 필요한 정보는 남는다

안쪽 block이 끝난 뒤에는 바깥 코드에서 안쪽 이름 `t`를 직접 사용할 수 없다. 그런데 반환된 closure는 여전히 그 binding을 필요로 한다. Block을 나왔다는 이유만으로 `t=10` 정보를 지워 버리면 이후 `f(20)`의 뜻을 보존할 수 없다.

Scope(유효 범위)는 소스에서 이름을 직접 사용할 수 있는 범위이고, lifetime은 실행 중 필요한 정보가 유지되는 기간이다. 두 개념을 구분하면 “안쪽 이름은 밖에서 보이지 않는데 반환된 함수는 그 값을 어떻게 쓰는가”라는 의문이 풀린다. 바깥 코드가 안쪽 이름을 직접 읽는 것이 아니라 closure가 보존한 환경을 통해 body가 그 binding을 찾는 것이다.

9월 17일 41:04–42:00에서는 closure의 참조가 남아 있으면 필요한 환경을 유지해야 한다는 점을 Garbage Collection(자동 메모리 회수)과 연결했다. 이는 의미를 설명하는 환경 모델이다. 모든 Scala local value가 반드시 특정 heap 구조에 할당된다는 구현 주장으로 확대하지 않는다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 41:04–42:00]]

## Parameterized expression(매개변수화된 식)과 Closure value의 구분

자료 p.53은 `def`로 정의한 함수를 parameterized expression으로, 그것을 환경과 함께 전달 가능한 값으로 바꾼 것을 closure value로 구분한다. `f _`는 이 변환의 명시적 표기이며 compiler가 문맥에서 필요한 변환을 삽입하기도 한다고 설명한다. 반면 anonymous function(익명 함수)은 함수 값을 직접 표현한다. [POP M002 p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

이 구분과 `val`·`def`의 평가 시점은 함께 보되 혼동하면 안 된다. 앞의 `val f`는 오른쪽 block을 한 번 평가해 closure를 저장한다. 같은 오른쪽을 인자 없는 `def f`로 정의하면 `f`를 사용할 때 그 block을 다시 평가한다. 순수한 이 예에서는 어느 쪽도 내부 `t=10`을 잃지 않으므로 `f(20)`의 값은 모두 30이다. 달라지는 것은 block을 평가하는 시점과 반복 여부다. 여기서 말하는 인자 없는 `def f`와 빈 argument 목록을 가진 `def f()`는 구분한다.

### Anonymous syntax와 재귀 함수 값

자료는 `(x: T) => e`를 다음과 같은 구성으로 설명한다.

```scala
{ def noname(x: T) = e; noname _ }
```

이는 그대로 실행할 코드가 아니라 문법 대응을 나타낸 일반 형식이며, `T`, `e`는 해당 type과 expression의 자리다. 이 대응에는 **`e`가 `noname`을 사용하지 않는다**는 조건이 있다. Anonymous syntax에는 body가 직접 부를 자기 이름이 없기 때문이다.

그렇다고 재귀 함수 값을 만들 수 없다는 뜻은 아니다. Block 안에서 자기 이름을 부르는 named `def`를 정의하고, 그 함수 값을 반환하는 별도 구성을 사용할 수 있다. 이때에는 `noname`을 사용하지 않는다는 위 단순 대응의 조건과, 자기 이름을 도입한 재귀 구성을 구분해야 한다. 뒤의 `sumF`가 실제로 그 방식으로 재귀하면서 반환된다. 9월 17일 말미의 anonymous syntax 논의도 이런 직접 자기 참조의 제약을 다룬다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 01:11:14–01:12:37]]

## Call-by-name에서도 argument의 environment가 필요하다

[[courses/principles_of_programming/units/evaluation-strategies|CBN 평가 규칙]]은 argument expression의 평가를 미룬다. 그러나 그 식을 body에 옮겨 적기만 하면 식 안의 이름을 잘못 찾을 수 있다. 함수 body는 함수의 정의 환경에서, argument expression은 호출 위치의 환경에서 읽어야 한다.

9월 15일 16:59에서는 단순한 식 교체만으로 원하는 실행을 설명할 수 없다고 지적하고 해결을 뒤로 미뤘다. 9월 17일 42:57의 해결은 지연된 argument도 호출 환경과 짝지은 closure로 전달하는 것이다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 16:59]] [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 42:57]]

```scala
{
  val t = 0
  def f(x: => Int) = t + x
  val r = {
    val t = 10
    f(t * t)
  }
  r
}
```

자료 p.54의 environment 번호를 사용하면 `f`의 정의 환경은 바깥 `E0`, 호출 위치는 안쪽 `E1`이다. 호출의 새 parameter environment `E2`는 `E0`를 부모로 삼되, `x`에는 지연된 식과 호출 환경의 쌍 `(E1,t*t)`를 둔다. [POP M002 p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 평가 대상 | 이름을 찾는 환경 | 값 |
|---|---|---:|
| Body `t + x`의 `t` | `E2`에서 부모 `E0`로 | 0 |
| `x`가 요구한 argument `t*t` | 보존한 호출 환경 `E1` | `10*10=100` |
| Body 전체 | 서로 다른 출처의 두 결과 결합 | `0+100=100` |
| 바깥 `r` | 안쪽 block이 반환한 값 | 100 |

원본 실행표에서 `E0::[E2|x=(E1,t*t)]`를 읽으면 두 환경의 역할이 동시에 드러난다. Body의 부모가 `E0`라는 사실과 argument가 `E1`을 보존한다는 사실을 모두 따라야 한다. 모든 `t`를 같은 곳에서 읽으면 잘못된 계산이 된다.

이 지연 closure는 입력 parameter 없이 필요할 때 실행할 식을 보존한다. CBN 자체가 결과를 저장하는 것은 아니다. 여러 번 요구하면 그 식을 다시 평가할 수 있으며, 최초 결과의 재사용은 `lazy val`에서 따로 배운 성질이다. STT의 칠판 환경 번호나 불명확한 횟수 표현을 위 PDF의 환경 번호·평가 횟수로 억지로 맞추지는 않는다.

## Currying(커링): 일부 입력을 받아 나머지 함수를 반환하기

앞의 [[courses/principles_of_programming/units/higher-order-functions|Higher-order function 단원]]에서 만든 범위 합 `sum(f,a,b)`에서 `f`는 어떤 항을 만들지 정하고 `a,b`는 처리 범위를 정한다. 여러 계산에서 제곱합만 반복한다면 매번 `f`와 범위를 함께 지정하는 대신, 먼저 제곱합 함수를 얻고 나중에 범위를 줄 수 있다.

자료 p.56의 기존 wrapper(감싸는 함수)는 `sumSquare(a,b)=sum(square,a,b)`처럼 `a,b`를 받아 그대로 넘긴다. 원하는 형태는 `sum(square)`만으로 범위를 받을 함수를 얻는 것이다. 따라서 첫 호출의 결과는 정수 합이 아니라 `(Int,Int) => Int`인 함수여야 한다. [POP M002 pp.56–58](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

Currying은 여러 입력을 한 번에 받는 함수를 입력을 나누어 받는 함수 반환 구조로 바꾸는 방식이다. 완전히 한 인자씩 나눈 type은

```text
(T1, T2, ..., Tn) => T
→ T1 => (T2 => (... => (Tn => T)))
```

이다. Uncurrying(언커링)은 반대 방향이다. 합의 예는 `f`와 `(a,b)`라는 두 묶음 사이를 나눈다. 세 인자를 모두 하나씩 받는 완전한 형태와 묶음 구조가 다르다는 점도 읽어야 한다. 이 type 대응만으로 효과가 있는 프로그램의 모든 평가 시점까지 같다고 결론 내리지는 않는다. [POP M002 p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### `sumF`가 바깥 `f`를 보존하는 과정

자료 p.57은 내부에 named recursive function `sumF`를 만들고 그 값을 반환한다. 마지막 `sumF _`는 같은 페이지의 명시적 변환 표기를 사용했다.

```scala
def sum(f: Int => Int): (Int, Int) => Int = {
  def sumF(a: Int, b: Int): Int =
    if (a <= b) f(a) + sumF(a + 1, b) else 0
  sumF _
}

def sumLinear = sum((n) => n)
def sumSquare = sum((n) => n * n)
def sumCubes = sum((n) => n * n * n)
```

바깥 `sum`은 `f`를 받고 내부 `sumF`는 `a,b`를 받는다. `sumF`가 반환되어도 그 closure는 정의 환경과 바깥 `sum` 호출의 parameter 환경을 잇는 연결을 보존한다. 나중에 `sumF`의 body에서 `f`를 찾으면 그 연결을 따라 처음 전달한 함수를 찾는다. 제곱 함수를 전달했다면 계속 제곱 함수를 사용한다. `f`를 `sumF`의 세 번째 parameter로 다시 받지 않아도 되는 이유다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 58:45, 01:03:39]]

이것은 단순히 “이전 값을 기억한다”는 구호보다 구체적이다. `sumF`의 새 호출에는 새로운 `a,b`가 있고, `f`는 closure의 부모 연결에서 찾는다. 처리 범위는 바뀌어도 항 계산 규칙은 보존된다. 또한 직접 자기 이름 `sumF`로 재귀하므로 anonymous syntax의 자기 이름 문제도 피한다.

과거 문항의 함수 type에서도 “규칙을 먼저 받고 데이터 처리 함수를 결과로 돌려준다”는 두 단계를 읽을 수 있다. 현재 단원에서는 이 함수 반환 관계만 연결한다. 그 문항의 전체 구현에는 사용자 정의 list와 타입 매개변수가 추가로 필요하며 closure 환경을 묻는 직접 문항이라고 확대하지 않는다. [EX:pop_2024_mid_q01_s01 L.50-53]

### Successive application(연속 적용)의 두 단계

자료 p.58의 다음 두 식은 같은 합을 표현한다.

```scala
sumSquare(3, 10) + sumCubes(5, 20)

sum((n) => n * n)(3, 10) + sum((n) => n * n * n)(5, 20)
```

`sum((n)=>n*n)`은 첫 단계에서 제곱항을 사용할 함수를 만든다. 이어 `(3,10)`이 그 함수에 구간을 주면 수치 계산이 진행된다. 같은 이유로 `sum((n)=>n*n*n)(5,20)`은 5부터 20까지의 세제곱합이다.

자료 식을 직접 계산하면 제곱합은 `385-(1+4)=380`, 세제곱합은 `44100-(1+8+27+64)=44000`이다. 따라서 둘을 더한 값은 44380이다. 이는 자료의 정확한 구간을 검산한 값이며 불명확한 실시간 출력의 복원이 아니다. Wrapper를 쓰든 함수를 바로 적용하든 첫 단계에서 고른 항 함수와 두 번째 단계의 범위를 같게 유지해야 한다.

## Multiple parameter lists(여러 매개변수 목록)와 변환 표기

자료 p.59는 인자 목록을 다음처럼 나누는 형태도 제시한다. [POP M002 pp.59–60](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def sum(f: Int => Int)(a: Int, b: Int): Int =
  if (a <= b) f(a) + sum(f)(a + 1, b)
  else 0
```

겉으로 `sum(f)(a,b)`라고 쓴다고 앞의 내부 closure 반환 정의와 모든 중간 표현이 같은 것은 아니다. 자료의 구분에서 multiple-list 정의의 `sum(f)`는 아직 parameterized expression이고, `sum(f) _`로 함수 값에 변환한다. 내부 `sumF`를 반환하는 정의에서는 `sum(f)` 자체가 이미 closure 값이다.

| `sum`의 정의 형태 | 자료 p.60의 `sumLinear` |
|---|---|
| `def sum(f)(a,b): Int = ...` | `def sumLinear = sum((n)=>n) _` |
| `def sum(f): (Int,Int)=>Int = { ...; sumF _ }` | `def sumLinear = sum((n)=>n)` |

원본 p.60은 두 block에서 underscore가 필요한 위치를 대비한다. 이 표는 그 Scala 자료의 변환 모델을 설명하며, 원본의 “incorrect” 표시를 모든 버전의 compiler 판정으로 일반화하지 않는다. 중요한 것은 남은 parameter를 가진 정의와 전달 가능한 함수 값을 구별하는 일이다.

### 재귀에서 함수 값을 다시 만드는 구조의 비용

다음은 p.59의 다른 표현이다.

```scala
def sum(f: Int => Int): (Int, Int) => Int =
  (a, b) =>
    if (a <= b) f(a) + sum(f)(a + 1, b)
    else 0
```

여기서는 재귀 단계마다 `sum(f)`를 다시 거쳐 함수 값을 얻고 그 함수를 `(a+1,b)`에 적용하는 구조다. 앞의 nested `sumF`는 이미 정의한 `sumF`를 직접 재귀 호출한다. 함수 값을 만드는 지점이 달라지므로 가능한 비용 차이를 분석할 이유가 생긴다.

다만 소스에 그런 구조가 보인다는 사실만으로 실제 heap 할당 횟수나 실행 시간의 차이를 확정할 수는 없다. 최적화가 무엇을 제거하는지는 구현에 달려 있다. 9월 17일 01:06:55의 설명은 유연한 currying 경계와 가능한 효율 차이를 비교하는 맥락으로 읽는다. [[courses/principles_of_programming/transcripts/2026-09-17|2026-09-17 STT 01:06:55–01:08:46]]

## Partial application(부분 적용): 값을 고정하고 남은 입력 묶기

Currying이 입력을 받는 단계를 나누는 방법이라면, partial application은 일부 입력값을 정해 나머지 입력을 받을 함수를 만드는 것이다. Anonymous wrapper를 사용하면 어느 자리를 고정하고 남은 인자를 어떤 순서와 묶음으로 받을지도 드러낼 수 있다. 자료 p.62의 예는 `y=1`, `a=2`를 고정한다. [POP M002 p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def foo(x: Int, y: Int, z: Int)(a: Int, b: Int) =
  x + y + z + a + b

val f1 = (x: Int, z: Int, b: Int) => foo(x, 1, z)(2, b)
val f2 = foo(_: Int, 1, _: Int)(2, _: Int)
val f3 = (x: Int, z: Int) => ((b: Int) => foo(x, 1, z)(2, b))
```

`f1`은 남은 `x,z,b`를 한 번에 받는다. `f2`는 같은 남은 세 자리를 자료의 placeholder(자리 표시자) `_`로 나타낸다. `f3`는 `x,z`를 먼저 받고, `b`를 받을 함수를 반환한다.

| 적용 | 실제로 이어지는 호출 | 결과 |
|---|---|---:|
| `f1(1,2,3)` | `foo(1,1,2)(2,3)` | 9 |
| `f2(1,2,3)` | `foo(1,1,2)(2,3)` | 9 |
| `f3(1,2)(3)` | `foo(1,1,2)(2,3)` | 9 |

고정값이 같고 최종 덧셈이 같아도 인자를 받는 단계는 다를 수 있다. `f3(1,2)`는 아직 정수 9가 아니라 `b`를 기다리는 함수다. Wrapper의 parameter 목록과 body에서의 배치를 바꾸면 인자 순서의 재배열도 표현할 수 있다. 따라서 짧은 표기를 읽을 때는 생략된 입력이 무엇인지, 지금 결과가 값인지 함수인지, 그 함수가 어느 binding을 보존하는지를 차례로 확인해야 한다.

## 핵심 정리

- Closure(클로저)는 함수 코드와 정의 environment(환경)를 함께 보존한다. 저장 위치나 호출 위치가 정의 환경을 대신하지 않는다.
- Scope(유효 범위)와 lifetime(수명)은 다르다. 밖에서 local 이름을 직접 쓸 수 없어도 반환된 closure는 필요한 binding을 유지한다.
- `val`과 인자 없는 `def`는 평가·재사용 시점이 다르다. 같은 순수한 closure 식을 사용하면서 정의 환경을 잃는 차이가 생기는 것은 아니다.
- CBN의 body는 함수 정의 환경을, 지연 argument는 호출 환경을 사용한다. 지연 closure 자체는 계산 결과의 자동 저장이 아니다.
- Currying(커링)은 입력 단계를 함수 반환으로 나누고 partial application(부분 적용)은 일부 값을 고정한다. 현재 결과가 숫자인지 남은 입력을 받을 함수인지 확인한다.
- Multiple parameter lists와 이미 closure를 반환하는 정의의 변환 표기는 자료에서 구별된다. 소스상 함수 생성 지점이 달라도 실제 할당·성능은 별도 문제다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Code-only의 20과 Closure의 30

바깥 E0의 t=0, 안쪽 E1의 t=10에서 `g(x)=x+t`를 함수 값으로 반환하여 바깥 f에 저장하고 `f(20)`을 호출한다. 코드만 보존한 p.51의 실패 모델과 p.52의 closure 모델을 각각 trace로 설명하라.

<details><summary>해설 보기</summary>

코드만 `(x)x+t`로 저장하고 호출의 부모를 f가 저장된 E0로 잡으면 x=20에 바깥 t=0을 더해 20이다. 이는 올바른 closure 평가의 대안 정답이 아니라 정의 환경을 잃은 모델의 실패다. Closure는 `(E1,(x)x+t)`를 보존한다. 호출 시 E2에 x=20을 넣고 부모를 E1로 연결하므로 body의 t는 10이고 결과는 30이다. f를 E0에 저장해도 값이 보존한 E1은 바뀌지 않는다.

**채점·확인:** 코드 외의 환경 정보, E2의 부모 E1, 20의 실패 성격과 30의 계산을 설명한다.

</details>

#### 확인 Q02 · Scope와 lifetime

안쪽 block이 끝나 t라는 이름이 바깥 코드에 보이지 않는데 반환된 f가 t=10을 사용하는 것은 왜 가능한가? GC 설명을 모든 local의 특정 메모리 배치 주장으로 읽어도 되는가?

<details><summary>해설 보기</summary>

Scope는 소스에서 이름을 직접 사용할 수 있는 범위이고 lifetime은 실행 중 정보가 필요한 기간이다. 바깥 코드가 안쪽 t를 직접 읽는 것이 아니라 f의 closure가 보존한 환경을 통해 body가 t를 찾는다. 이후 호출에서 필요하므로 block 종료만으로 그 binding을 없앨 수 없다. 강의는 참조가 남은 환경을 유지하는 일을 GC와 연결하지만 이는 의미 모델이며 모든 local이 반드시 특정 heap 구조에 놓인다는 결론은 아니다.

**채점·확인:** 접근 범위와 보존 기간을 구분하고 closure의 참조 및 구현 한계를 설명한다.

</details>

#### 확인 Q03 · Parameterized expression·val f·def f

자료가 구별하는 parameterized expression과 closure value, `f _`의 역할을 말하라. Q01에서 같은 오른쪽 block을 `val f` 대신 괄호 없는 `def f`로 정의하면 두 번 사용 시 평가 시점과 결과 30이 어떻게 되는가?

<details><summary>해설 보기</summary>

자료의 def는 parameterized expression이고 이를 정의 환경과 함께 전달 가능한 함수 값으로 바꾼 것이 closure다. `f _`는 명시적 변환 표기이며 문맥에 따른 compiler의 변환도 설명한다. `val f`는 오른쪽 block을 초기화 때 한 번 평가해 closure 값을 저장한다. 인자 없는 `def f`는 f를 사용할 때마다 그 block을 다시 평가한다. 순수한 이 예에서는 각각 얻은 closure가 내부 t=10을 보존하므로 `f(20)`은 모두 30이다. 재평가는 정의 환경의 폐기가 아니며 `def f`와 `def f()`도 구분한다.

**채점·확인:** 표현식/값 변환과 val/def의 시점을 나누고 30이 20으로 바뀐다고 답하지 않는다.

</details>

#### 확인 Q04 · 익명 표면 문법과 재귀 함수 값

`(x:T)=>e`를 `{def noname(x:T)=e; noname _}`로 설명할 때 e에 필요한 조건은 무엇인가? 이 조건이 재귀 closure를 만들 수 없다는 뜻인가?

<details><summary>해설 보기</summary>

단순 문법 대응에서는 e가 noname을 사용하지 않아야 한다. 익명 표면 문법 자체에는 body가 직접 부를 자기 이름이 없기 때문이다. 그러나 block 안에 자기 이름을 부르는 named def를 정의하고 그 함수 값을 반환할 수 있다. 본문의 sumF가 자기 이름으로 재귀하고 closure로 반환되는 예다. 자기 참조가 없는 익명 문법의 대응 조건과 이름을 도입한 별도 재귀 구성은 다르다.

**채점·확인:** noname 미사용 조건과 named def를 통한 재귀 값 구성을 둘 다 설명한다.

</details>

#### 확인 Q05 · CBN에서 보존하는 두 환경

바깥 E0에 t=0과 `def f(x: => Int)=t+x`가 있고 안쪽 E1에 t=10이 있다. `f(t*t)`에서 새 E2의 부모와 x에 저장할 쌍을 적고 결과를 구하라. 지연 식을 body에 문자 그대로 넣거나 자동 저장으로 읽으면 무엇이 틀리는가?

<details><summary>해설 보기</summary>

Body의 E2는 f의 정의 환경 E0를 부모로 하고, x에는 호출 환경을 붙인 `(E1,t*t)`를 보존한다. Body의 t는 E0의 0이고 x가 필요해지면 E1에서 `10*10=100`을 계산하여 결과는 100이다. 모든 t를 E0에서 읽으면 인자의 뜻을 잃고, 모든 t를 E1에서 읽으면 body의 뜻을 잃는다. CBN은 요구마다 지연 식을 다시 평가할 수 있으며 최초 결과를 저장하는 lazy val과 다르다. 9월 15일은 이 환경 문제를 제기하고 9월 17일에 closure를 통한 해결을 설명했다.

**채점·확인:** E2→E0와 x→(E1,t*t), 0+100, 두 오해 및 강의 시점의 구별을 포함한다.

</details>

#### 확인 Q06 · Currying·uncurrying의 타입과 동기

`sum(f,a,b)`의 반복 wrapper를 `sum(square)`로 바꾸려면 첫 호출의 결과 type이 무엇이어야 하는가? 완전한 세 인자 currying과 f/(a,b)의 묶음 분리, uncurrying을 타입으로 구별하라.

<details><summary>해설 보기</summary>

항 규칙 square는 정했지만 범위 a,b가 남았으므로 `sum(square)`의 결과는 `(Int,Int)=>Int`인 함수다. 일반적으로 `(T1,T2,T3)=>T`를 완전히 curry하면 `T1=>(T2=>(T3=>T))`이고 반대가 uncurrying이다. 범위 합은 `(Int=>Int)=>((Int,Int)=>Int)`로 f와 (a,b) 두 묶음을 나눈 예여서 범위 둘도 하나씩 받는 완전 분리와 다르다. 반복해서 a,b를 넘기는 wrapper 대신 규칙을 고른 함수를 반환하려는 동기다. 이 type 관계가 효과가 있는 모든 프로그램의 평가 시점 동일성을 보장하지는 않는다.

**채점·확인:** 남은 함수 type·두 묶음·완전 분리·역변환을 설명한다.

</details>

#### 확인 Q07 · sumF의 포획과 연속 적용

`sum(f)` 안의 `sumF(a,b)`는 `a<=b`일 때 `f(a)+sumF(a+1,b)`, 아니면 0이다. f를 다시 받지 않고도 어떻게 찾는가? `sum(square)(3,10)+sum(cube)(5,20)`의 두 적용 단계와 수치 결과를 확인하라.

<details><summary>해설 보기</summary>

바깥 sum 호출의 parameter 환경에 f가 있고 내부 sumF의 closure가 그 환경으로 이어지는 부모 연결을 보존한다. 각 sumF 호출의 새 a,b 환경에서 부모를 따라 원래 f를 찾으므로 sum 호출이 끝나도 규칙을 사용할 수 있다. 첫 적용 `sum(square)` 또는 `sum(cube)`는 규칙을 포획한 함수를 만들고, 두 번째 적용은 해당 범위를 계산한다. 제곱합은 `9+16+25+36+49+64+81+100=380`, 세제곱합은 1..20의 44100에서 1..4의 100을 뺀 44000이다. 합은 44380이다. 이 값은 자료 구간을 산술 검산한 것이며 불명확한 live 출력을 복원한 것은 아니다.

**채점·확인:** 새 a,b와 포획된 f의 위치, 첫 함수/둘째 수치 단계, 380+44000=44380을 설명한다.

</details>

#### 확인 Q08 · Multiple lists와 변환 위치

A는 `def sum(f:Int=>Int)(a:Int,b:Int):Int=...`이고 B는 `def sum(f:Int=>Int):(Int,Int)=>Int={...;sumF _}`이다. 자료 p.60에서 `def sumLinear=...`의 오른쪽 underscore 표기가 다른 이유는?

<details><summary>해설 보기</summary>

자료의 A에서 `sum((n)=>n)`은 남은 a,b를 가진 parameterized expression이므로 `sum((n)=>n) _`로 함수 값으로 변환한다. B의 `sum((n)=>n)`은 이미 내부 sumF closure를 반환하므로 같은 변환을 다시 붙이는 경우가 아니다. 겉으로 둘 다 `sum(f)(a,b)`를 사용할 수 있어도 중간 표현의 종류는 구별해야 한다. 이는 원본 Scala 자료의 표기 설명이며 최신 모든 compiler의 판정으로 확대하지 않는다.

**채점·확인:** A의 남은 표현식과 B의 이미 반환된 함수 값, 자료 문맥의 한계를 명시한다.

</details>

#### 확인 Q09 · 함수 값 재생성과 가능한 비용

내부 named `sumF`를 직접 재귀 호출하는 형태와 `sum(f)=(a,b)=>...sum(f)(a+1,b)...` 형태는 소스상 어떤 차이가 있는가? 실제 할당 횟수·시간이나 모든 지점에서 currying을 쓰라는 결론이 나오는가?

<details><summary>해설 보기</summary>

Named sumF는 이미 정의된 자기 함수를 직접 부른다. 둘째는 각 재귀 단계에서 sum(f)를 다시 거쳐 함수 값을 얻고 이를 나머지 범위에 적용하는 구조다. 함수 값을 만드는 지점이 다르므로 비용 차이를 분석할 이유가 있지만 compiler가 제거하는 작업은 구현에 달려 있어 실제 heap 할당 횟수나 속도를 단정할 수 없다. 필요한 함수 값을 꺼내 사용할 경계에서 인자 목록을 나누는 유연성과 가능한 비용을 함께 고려한다.

**채점·확인:** 두 소스 구조와 최적화·측정의 한계를 구분하고 필요한 currying 경계를 설명한다.

</details>

#### 확인 Q10 · Partial application의 고정값과 입력 묶음

`foo(x:Int,y:Int,z:Int)(a:Int,b:Int)=x+y+z+a+b`에서 y=1,a=2를 고정한다. `f1=(x:Int,z:Int,b:Int)=>foo(x,1,z)(2,b)`, `f2=foo(_:Int,1,_:Int)(2,_:Int)`, `f3=(x:Int,z:Int)=>((b:Int)=>foo(x,1,z)(2,b))`의 남은 입력과 `f1(1,2,3)`·`f2(1,2,3)`·`f3(1,2)(3)`의 결과를 적어라. `f3(1,2)` 자체는 어떤 값인가? 남은 입력을 b,x,z 순서로 받는 wrapper도 작성하라.

<details><summary>해설 보기</summary>

f1과 자료의 placeholder 표기 f2는 x,z,b 세 입력을 한 번에 받는다. f3는 x,z를 받은 뒤 b를 받을 함수를 반환한다. 셋 다 최종적으로 `foo(1,1,2)(2,3)`이 되어 `1+1+2+2+3=9`다. `f3(1,2)` 자체는 아직 9가 아니라 `(b:Int)=>1+1+2+2+b`에 해당하는 함수다. 입력을 b,x,z 순서로 받으려면 `(b: Int, x: Int, z: Int) => foo(x,1,z)(2,b)`로 쓸 수 있다. 이 함수에 `(3,1,2)`를 주면 같은 `foo(1,1,2)(2,3)`으로 이어져 9다. Parameter 목록은 받는 순서, body의 배치는 원래 함수에 전달하는 순서를 각각 정한다.

**채점·확인:** 고정 y/a·남은 x/z/b·한 단계/두 단계·중간 함수와 최종 9를 구분하고 b,x,z 입력을 올바른 foo 자리에 다시 배치한다.

</details>

### 적용 연습

#### 연습 P01 · 연산과 왼쪽 인자를 고정한 함수

**새로 만든 synthetic(합성) 연습이며 실제 기출이 아니다.** 2024 중간 Q1-1 Main.scala [EX:pop_2024_mid_q01_s01 L.50-53]의 '규칙을 먼저 받아 데이터 처리 함수를 반환한다'는 인터페이스 사고를 옮겼다. 원문이 closure 환경 추적을 직접 묻는다고 확대하지 않는다. 현재 전제는 함수 값·환경 보존·부분 적용이며 원문의 generic list·타입 매개변수는 후속 전제다.

`bindLeft(op:(Int,Int)=>Int,a:Int):Int=>Int`가 나중의 b에 `op(a,b)`를 적용하도록 작성하라. `leftSub=bindLeft((x,y)=>x-y,9)`와 `leftAdd=bindLeft((x,y)=>x+y,2)`를 만든 뒤 다음 block을 계산하라. 각 함수가 보존하는 것을 적고 값을 뒤집어 고정한 오류도 판별하라.

~~~scala
{
  val a = 100
  val op: (Int, Int) => Int = (x, y) => x * y
  leftSub(4) + leftAdd(4)
}
~~~

<details><summary>해설 보기</summary>

~~~scala
def bindLeft(op: (Int, Int) => Int, a: Int): Int => Int =
  (b: Int) => op(a, b)
~~~

leftSub의 closure는 그 생성 호출의 op=뺄셈, a=9를 보존한다. leftAdd는 별도 호출의 op=덧셈, a=2를 보존한다. 이후 b=4가 각각 새 호출 입력으로 주어져 `9-4=5`와 `2+4=6`, 합 11이다. 호출 block의 a=100·곱셈 op는 closure의 정의 환경을 교체하지 않는다. 생성 호출은 끝났어도 이 binding이 필요하므로 보존된다.

잘못 `op(b,a)`로 작성하면 leftSub(4)가 `4-9=-5`이고 leftAdd(4)는 여전히 6이라 합은 1이 된다. 덧셈만 검사하면 고정 위치 오류가 드러나지 않는다. Currying/함수 반환은 남은 b를 기다리는 단계, partial application은 op와 a를 정한 것이라는 역할도 구분한다.

**채점·확인:** 정확한 반환 type·환경별 op/a·5+6=11·뒤집힌 1·caller shadowing 무관성을 모두 설명한다.

</details>

### 복습 순서

Q01–Q05에서 각 식 옆에 '정의 환경' 또는 '호출 환경'을 표시한다. Q06–Q08은 첫 적용의 결과 type을 쓰고 Q09로 소스 구조와 실제 비용을 나눈다. Q10과 P01은 고정값·남은 입력·보존 환경을 먼저 적은 뒤 계산한다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-15-lecture-04|2026-09-15 강의 노트 · by-name 환경 문제 제기]] / [[courses/principles_of_programming/transcripts/2026-09-15|보정 STT · 07:07, 16:59]]: 해결을 뒤로 미룬 맥락이다.
- [[courses/principles_of_programming/lectures/2026-09-17-lecture-05|2026-09-17 강의 노트 · Closure·currying·부분 적용]] / [[courses/principles_of_programming/transcripts/2026-09-17|보정 STT · 27:04, 35:09–42:57, 52:27, 58:45–01:03:39, 01:06:55–01:12:37]].
- [Lecture Part 1 · pp.51–54 환경·Closure, pp.56–62 함수 반환·currying](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).
- 과거 평가의 부분 연결: 2024 중간 Q1-1 Main.scala [EX:pop_2024_mid_q01_s01 L.50-53]의 함수 반환 인터페이스. 원문 list 구현이나 제공 해답을 옮긴 것이 아니며 P01은 새 합성 연습이다.

p.51의 20은 실패 모델, p.52의 30은 정의 환경을 보존한 모델의 결과다. By-name은 body와 argument가 서로 다른 환경을 보존한다. Underscore·multiple-list 표기는 원본 자료의 문맥이며 할당 횟수·최신 compiler 동작을 새로 확인했다는 뜻이 아니다. 9월 17일 마지막 제공 segment 이후나 p.63부터의 내용을 이 단원의 진도로 확정하지 않는다.


---

[[courses/principles_of_programming/units/higher-order-functions|← 이전: Higher-Order Functions와 계산 구조의 재사용]] · [[courses/principles_of_programming/units/index|단원 목차]]
