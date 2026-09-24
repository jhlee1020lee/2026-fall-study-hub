---
title: "Call-by-value·Call-by-name과 Lazy Evaluation"
description: "CBV·CBN·val·def·lazy val을 평가 시점, 반복, 종료와 출력으로 비교합니다."
course: "principles_of_programming"
unit_id: "evaluation-strategies"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-08-lecture-03", "courses/principles_of_programming/lectures/2026-09-15-lecture-04"]
---

인자를 언제 평가하고 그 결과를 재사용하는지에 따라 같은 식의 계산량과 종료가 달라집니다. CBV·CBN·lazy val을 trace와 출력 횟수로 구분하고 조건 선택의 동작을 보존해 봅니다.

## Call-by-value와 Call-by-name: argument를 언제 평가하는가

[[courses/principles_of_programming/units/expressions-functions|Expression과 function application]]에서 argument(인자)를 먼저 value(값)로 만든 뒤 body(본문)에 전달했다. 이 전략이 Call-by-value(값에 의한 호출, CBV)다. Call-by-name(이름에 의한 호출, CBN)은 argument expression(인자 식)의 평가를 미루고, body가 그 값을 요구할 때 평가한다. 평가 시점이 달라지면 불필요한 계산을 생략할 수 있지만, 같은 expression을 반복해서 계산할 수도 있다.

자료의 제곱 함수 body `x * x`에 `1 + 1`을 전달하는 계산을 두 전략으로 비교해 보자. 아래 CBN 전개는 그 body에 CBN 규칙을 적용한 비교이며, 기본 Scala 선언 `def square(x: Int)`가 CBN이라는 뜻은 아니다. [POP M002 pp.17–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```text
CBV: square(1 + 1) → square(2) → 2 * 2 → 4

CBN: square(1 + 1) → (1 + 1) * (1 + 1)
                  → 2 * (1 + 1) → 2 * 2 → 4
```

CBV에서는 덧셈을 한 번 계산한 값 `2`를 body의 두 위치에서 쓴다. CBN에서는 `x`를 두 번 요구하므로 `1 + 1`을 두 번 계산한다. 반대로 실행한 경로에서 `x`를 전혀 쓰지 않는다면 CBN은 그 계산을 생략할 수 있고, CBV는 함수에 진입하기 전에 계산한다. 따라서 한 예의 연산 횟수만으로 어느 전략이 항상 낫다고 판단할 수 없다.

9월 8일 03:43의 핵심 설명은 CBV가 argument 평가를 먼저 하고 CBN은 그 평가를 미룬 채 body를 시작한다는 것이다. STT의 일부 전략 명칭·횟수에는 혼선이 남아 있으므로, 위의 정확한 전개는 자료의 규칙으로 구분해 읽는다. CBN은 계산 결과를 자동으로 저장하는 전략이 아니다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 03:43]]

### 평가 전략은 종료와 관찰 가능한 동작도 바꾼다

순수하고 결정적인 작은 산술식에서는 두 전략이 같은 값에 도달하면서 계산량만 달라질 수 있다. 그러나 출력이나 매번 결과가 달라지는 계산을 반복하면 관찰 가능한 동작도 달라진다. 9월 8일 09:31에서는 random 계산이 이런 차이의 예로 논의되었다. 종료하지 않는 식을 평가하는지의 차이도 크다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 09:31]]

Scala 자료에서는 기본 parameter가 CBV이고 `=>`를 붙인 parameter가 CBN이다.

```scala
def loop: Int = loop
def one(x: Int, y: => Int) = 1
```

| 호출 | Body 진입 전에 필요한 계산 | 결과 |
|---|---|---|
| `one(1 + 2, loop)` | 첫 argument를 `3`으로 평가 | `y`를 쓰지 않아 `1` |
| `one(loop, 1 + 2)` | 첫 argument인 `loop`를 평가 | 끝나지 않아 body에 진입하지 못함 |

`one`의 body가 상수 `1`이라는 사실만으로 두 호출이 모두 끝나지는 않는다. 첫 parameter의 CBV 규칙이 body보다 먼저 적용되기 때문이다. 반대로 첫 호출에서 두 번째 argument를 한 번도 평가하지 않는 것은 `loop`가 종료 가능한 식으로 변했기 때문이 아니라, 그 식을 요구하지 않았기 때문이다. [POP M002 p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

## `val`과 `def`: 결과에 이름을 붙이는가, 계산에 이름을 붙이는가

평가 시점의 차이는 이름을 정의할 때도 나타난다. 아래 두 선언은 비교를 위한 별도 예다. [POP M002 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
val a = 1 + 2 + 3
```

```scala
def a = 1 + 2 + 3
```

`val`은 정의를 평가할 때 오른쪽을 계산하여 `6`에 이름을 연결한다. 인자 없는 `def`는 아직 평가하지 않은 expression을 정의하며, `a`를 사용할 때 그 식을 평가한다. 한 번 계산한 결과를 자동으로 저장한다고 이해하면 안 된다. 그래서 `def b = loop`는 정의만으로 `loop`의 값을 요구하지 않지만, `val b = loop`는 초기값을 구하려다 끝나지 않는다.

자료는 `val`을 field, `def`를 method라고도 부른다. `def f(a: Int, b: Int): Int = a * b - 2`처럼 parameter가 있는 경우도 아직 평가하지 않은 expression을 정의한다는 점에서 같다. 차이는 계산을 시작하려면 `a,b`에 줄 실제 argument가 더 필요하다는 것이다. 9월 8일 16:04의 설명은 인자 없는 `def`와 인자 있는 `def`를 이 관점에서 연결했다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 16:04]]

## Conditional expression과 Short-circuit(단락 평가)

`if (b) e1 else e2`는 `b`의 값에 따라 branch(분기) 하나만 평가한다. 이것을 세 입력을 받는 함수로 추상화한다고 생각해 보자. 세 입력을 모두 CBV로 받으면 함수 진입 전에 `e1,e2`가 모두 평가된다. 선택하지 않을 branch에 출력이나 `loop`가 있으면 불필요한 출력이 발생하거나, 원하는 branch를 고르기도 전에 발산한다.

따라서 조건 `b`는 먼저 평가하되 branch expression 둘은 평가를 미뤄야 한다. 9월 8일 23:28에서는 이를 “조건은 CBV, 두 branch는 CBN으로 받는 관점”으로 설명했다. 27:10에는 한 branch의 A만 출력되고 B는 출력되지 않았다는 시연 보고가 있다. 이는 선택 평가를 설명하는 관찰이며, 제공되지 않은 완전한 시연 코드를 복원한 것은 아니다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 23:28, 27:10]]

### Boolean 연산에서 오른쪽 식이 필요한 조건

Boolean expression에는 `true`, `false`, 부정 `!`, 논리 연산 `&&`, `||`와 비교 `<=`, `>=`, `<`, `>`, `==`, `!=`가 있다. `!true`는 `false`, `!false`는 `true`다. 논리 연산은 다음 규칙으로 오른쪽의 필요 여부를 정한다. [POP M002 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 식 | 줄어든 식 또는 값 | 오른쪽 `b`의 평가 |
|---|---|---|
| `true && b` | `b` | 필요 |
| `false && b` | `false` | 생략 |
| `true \|\| b` | `true` | 생략 |
| `false \|\| b` | `b` | 필요 |

`true && (loop == 1)`은 비교 결과가 필요하므로 `loop`를 평가하다 발산한다. `false && (loop == 1)`은 오른쪽에 손대지 않고 `false`가 된다. 단락 평가는 이미 구한 두 Boolean 값을 조합하는 것 이상이다. 어느 expression을 실제로 실행할지도 정한다.

### `and`와 `or`에 평가 행동까지 보존하기

자료 pp.23–24의 기존 연습은 `and(x,y)`가 `x && y`와, `or(x,y)`가 `x || y`와 같은 동작을 하되, **함수 body에서 `&&`와 `||`를 사용하지 않는 것**이다. 제공된 해답은 조건식으로 선택을 표현한다.

```scala
def and(x: Boolean, y: => Boolean) =
  if (x) y else false

def or(x: Boolean, y: => Boolean) =
  if (x) true else y
```

`and(false, loop == 1)`은 `if (false) loop == 1 else false`로 줄어 `false`다. `and(true, loop == 1)`은 오른쪽을 요구하여 발산한다. `or(true, loop == 1)`은 `true`를 반환한다. `y`를 strict한 `Boolean` parameter로 바꾸면 함수 진입 전에 `loop == 1`을 평가하므로 이 행동을 보존하지 못한다. 9월 8일 33:12의 보충도 두 번째 입력을 CBN으로 받아야 한다는 점이다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 33:12]] [POP M002 pp.23–24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

## Lazy call-by-value: 최초 사용까지 미루고 결과를 재사용하기

CBN은 쓰지 않는 계산을 피하지만 여러 번 쓰면 반복할 수 있다. `val`은 한 번 얻은 값을 재사용하지만 사용하지 않을 경로에서도 정의에 도달하면 초기화한다. 자료의 Lazy call-by-value(지연 값 평가)는 `lazy val`로 두 성질을 결합한다. 최초로 값이 필요할 때 expression을 평가하고, 성공적으로 얻은 값을 이후 사용에서 재사용한다.

여기서 필요한 block 규칙은 간단하다. `{ ... }`에 정의와 expression을 묶으면 마지막 expression의 값이 block 전체의 결과다. 따라서 `{ println("ok"); 100+100+100+100 }`은 실행될 때 `ok`를 출력한 뒤 `400`을 낸다. 이 block을 자료의 함수에 by-name argument로 전달한다. [POP M002 p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def f(c: Boolean, i: => Int): Int = {
  lazy val iv = i
  if (c) 0
  else iv * iv * iv
}

f(true,  { println("ok"); 100 + 100 + 100 + 100 })
f(false, { println("ok"); 100 + 100 + 100 + 100 })
```

첫 호출은 `0`을 고르고 `iv`를 요구하지 않는다. 그래서 `i`도 평가하지 않고 출력도 없다. 두 번째 호출은 곱셈의 첫 `iv`가 필요할 때 `i`를 평가한다. `ok`를 한 번 출력하고 얻은 `400`을 저장하므로 나머지 두 `iv`는 저장된 값을 쓴다. 결과는 `400 * 400 * 400 = 64000000`이다.

같은 코드의 local 선언만 바꾸면 차이가 선명해진다. 아래는 정상 종료하는 이 argument에 대한 코드 분석이다.

| Local 선언 | `c=true`의 `i` 평가 횟수 | `c=false`의 `i` 평가 횟수 | 평가 시점 |
|---|---:|---:|---|
| `val iv = i` | 1 | 1 | Local 정의에 도달하자마자 |
| `def iv = i` | 0 | 3 | 실제 `iv` 사용마다 |
| `lazy val iv = i` | 0 | 1 | 최초 사용 시, 이후 값 재사용 |

9월 15일 15:05의 끝부분은 “쓰이지 않으면 0번, 쓰이면 한 번”이라는 의도를 설명한다. 같은 구간의 부정 표현과 전략 명칭에는 모순이 남아 있어 위 표는 원본 코드에 근거해 정확히 구분한 것이다. 예외 발생이나 동시 초기화의 추가 규칙까지 이 예로 일반화하지는 않는다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 15:05]]

평가를 미룬다는 규칙만으로 이름의 의미까지 설명되지는 않는다. By-name argument 안에 바깥 이름이 있다면 그 이름을 어느 environment(환경)에서 찾을지도 보존해야 한다. 이 문제는 [[courses/principles_of_programming/units/blocks-scope|Block과 environment]]를 익힌 뒤 [[courses/principles_of_programming/units/closures-currying|Closure를 이용한 CBN 설명]]에서 코드와 환경을 함께 전달하는 방식으로 해결한다.

## 핵심 정리

- CBV는 함수 진입 전에 argument를 평가하고 CBN은 실제로 필요할 때 평가한다. CBN에는 결과 저장이 자동으로 따라오지 않는다.
- 순수한 산술식의 같은 결과가 출력·random·발산까지 포함한 동작의 동일성을 뜻하지는 않는다.
- `val`은 정의에서 값을 구하고 `def`는 사용할 때 식을 평가하며, `lazy val`은 최초 사용까지 미룬 뒤 성공한 결과를 재사용한다.
- 조건식과 short-circuit(단락 평가)은 미선택 식을 실행하지 않는다. 이를 함수로 옮길 때 branch 인자를 strict하게 받으면 뜻이 바뀐다.
- `and`·`or`의 동등성에는 Boolean 결과뿐 아니라 오른쪽 평가 여부와 종료도 포함된다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 같은 인자를 두 번 쓰는 경우

Body가 `x*x`인 `square(1+1)`을 CBV와 CBN으로 각각 전개하고 덧셈 횟수를 세어라. 어느 전략이 항상 더 적게 계산하는가? 기본 `x: Int` 선언과 전략 비교도 구분하라.

<details><summary>해설 보기</summary>

CBV는 `square(2)→2*2→4`로 `1+1`을 한 번 계산한다. CBN은 `(1+1)*(1+1)→2*(1+1)→2*2→4`로 두 번 계산한다. 같은 body에 두 전략을 적용한 비교이며 기본 Scala의 `x: Int`를 CBN으로 읽는 것은 아니다. 실행 경로에서 `x`를 쓰지 않으면 CBN은 0번, CBV는 진입 전에 한 번 평가하므로 항상 우수한 전략을 이 예로 정할 수 없다.

**채점·확인:** CBV 1회·CBN 2회 및 미사용 경로의 반대 이점을 모두 설명한다.

</details>

#### 확인 Q02 · 평가 시점이 종료와 effect를 바꾼다

`def loop: Int=loop`, `def one(x: Int,y: => Int)=1`에서 두 호출 `one(1+2,loop)`, `one(loop,1+2)`를 비교하라. 출력·random 인자에서는 무엇을 추가로 확인해야 하는가?

<details><summary>해설 보기</summary>

첫 호출은 strict한 첫 argument를 3으로 만든 후 body로 들어가고 `y`를 쓰지 않아 1을 반환한다. 둘째 호출은 첫 argument `loop`를 평가하다 끝나지 않아 body의 1에 도달하지 못한다. `loop`의 종료 성질이 바뀐 것이 아니라 필요 여부가 다른 것이다. 출력은 평가 횟수만큼 출력할 수 있고 random은 반복 평가마다 다른 값을 낼 수 있으므로 최종 값 외에 평가 여부·횟수·관찰 가능한 행동을 비교한다.

**채점·확인:** 두 호출의 body 진입 여부를 구분하고 effect 비교를 단순 속도 문제로 축소하지 않는다.

</details>

#### 확인 Q03 · 값과 식에 이름 붙이기

`val a=1+2+3`과 인자 없는 `def a=1+2+3`의 정의·사용 시점을 비교하라. `def b=loop`와 `val b=loop`, parameter가 있는 `def f(a: Int,b: Int)=a*b-2`와의 관계도 설명하라.

<details><summary>해설 보기</summary>

`val a`는 정의를 평가할 때 6을 구해 연결하고 이후 그 값을 쓴다. 인자 없는 `def a`는 식을 정의하고 사용할 때마다 평가하며 결과를 자동 저장하지 않는다. 그래서 `def b=loop`는 정의만으로 발산하지 않지만 `val b=loop`는 초기값을 구하다 끝나지 않는다. 인자가 있는 `def f`도 정의 시 body를 실행하지 않는다는 점은 같고, 추가로 실제 `a,b`를 받아야 계산할 수 있다.

**채점·확인:** 정의 시 평가·사용 시 평가·parameter 공급을 구분하며 def를 memoization으로 설명하지 않는다.

</details>

#### 확인 Q04 · 조건식을 함수로 옮기는 조건

`if(b)e1 else e2`를 세 인자 함수로 옮길 때 모두 CBV로 받으면 왜 동작이 달라지는가? 미선택 branch에 print 또는 `loop`가 있다고 하자. 강의의 A/B 시연에서 확인된 범위도 구분하라.

<details><summary>해설 보기</summary>

모두 CBV이면 함수에 들어가기 전에 `e1,e2`까지 계산한다. 선택하지 않을 print가 실행되거나 `loop` 때문에 선택 자체에 도달하지 못한다. 조건 `b`는 먼저 평가하되 두 branch를 by-name으로 받고 고른 branch만 요구해야 선택 실행을 보존한다. STT는 한 branch의 A만 출력되고 B는 출력되지 않았다고 보고하지만 전체 시연 코드나 반환값까지 제공한 것은 아니다.

**채점·확인:** 조건과 branch의 서로 다른 평가 역할, 미선택 식의 effect·발산을 설명한다.

</details>

#### 확인 Q05 · Boolean reduction 네 경우

정수 비교와 `!`의 결과 type·역할을 설명하고 `true&&b`, `false&&b`, `true||b`, `false||b`에서 오른쪽이 필요한지 적어라. `b=(loop==1)`이면 어떻게 되는가?

<details><summary>해설 보기</summary>

정수의 `<=,>=,<,>,==,!=` 비교는 Boolean 값을 만든다. `!true=false`, `!false=true`다. 네 식은 각각 `b,false,true,b`로 줄어든다. 첫째와 넷째는 오른쪽 값이 필요하고 둘째와 셋째는 필요 없다. 따라서 `b=(loop==1)`이면 첫째·넷째는 발산하고 둘째는 false, 셋째는 true다. 오른쪽은 먼저 계산된 Boolean이 아니라 아직 실행하지 않은 식일 수 있다.

**채점·확인:** 네 경우의 결과와 요구 여부를 모두 맞추고 비교·부정도 설명한다.

</details>

#### 확인 Q06 · and/or 연습의 제약과 동작

자료의 기존 `and/or` 연습이 금지한 연산자를 밝히고 제공된 해결 방식을 설명하라. `and(false,loop==1)`, `and(true,loop==1)`, `or(true,loop==1)`의 결과와 strict한 `y:Boolean`의 문제를 적어라.

<details><summary>해설 보기</summary>

기존 강의 연습은 body에서 `&&`와 `||`를 쓰지 않고 같은 동작을 만드는 것이다. 자료의 제공 해답은 다음과 같다.

~~~scala
def and(x: Boolean, y: => Boolean) = if (x) y else false
def or(x: Boolean, y: => Boolean) = if (x) true else y
~~~

순서대로 false, 발산, true다. 첫째와 셋째는 `y`를 요구하지 않고 둘째만 요구한다. `y:Boolean`으로 바꾸면 함수 진입 전에 `loop==1`을 평가하므로 생략 동작을 잃는다. 금지 연산자 회피뿐 아니라 값·평가 여부·종료를 함께 보존해야 한다.

**채점·확인:** 기존 자료 해답임을 구분하고 두 금지 연산자, by-name 표기, 세 결과를 모두 맞춘다.

</details>

#### 확인 Q07 · val·def·lazy val의 횟수 표

By-name `i`를 받는 함수가 local `iv=i`를 정의하고 `if(c)0 else iv*iv*iv`를 계산한다. `i={println("ok");100+100+100+100}`일 때 local 선언을 `val`, `def`, `lazy val`로 바꾼 세 경우의 `c=true/false` 평가 횟수와 반환값을 비교하라.

<details><summary>해설 보기</summary>

Block의 마지막 산술식 값은 400이며 한 번 평가할 때 ok를 한 번 출력한다.

| local 선언 | true일 때 횟수·값 | false일 때 횟수·값 |
|---|---|---|
| `val iv=i` | 1회·0 | 1회·64000000 |
| `def iv=i` | 0회·0 | 3회·64000000 |
| `lazy val iv=i` | 0회·0 | 1회·64000000 |

`val`은 정의에 도달하자마자, `def`는 세 사용마다, `lazy val`은 첫 필요 시 평가한다. 마지막은 성공한 400을 나머지 사용에서 재사용한다. 정상 종료하는 이 코드의 분석이며 예외·동시 초기화 규칙까지 설명하는 표가 아니다.

**채점·확인:** 6개 횟수와 반환값을 모두 맞추고 lazy의 지연과 재사용을 각각 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 두 번 쓰는 지연 입력의 재사용 설계

**새로 만든 강의 기반 일반 연습.** 제공된 기출에 CBV/CBN·lazy 평가 횟수를 직접 요구하는 근거는 없다. 본문의 조건식·block·by-name·local binding만 사용한다.

`def choose(c:Boolean, i: => Int):Int`를 완성하라. `c=true`이면 i를 실행하지 않고 0을 반환하며, false이면 i를 한 번만 평가해 그 값을 두 번 곱한다. 입력 `{println("go"); 2+3}`으로 두 경우를 검산하고 local `def`와 strict parameter로의 변경이 각각 어떤 요구를 깨는지 설명하라.

<details><summary>해설 보기</summary>

~~~scala
def choose(c: Boolean, i: => Int): Int = {
  lazy val v = i
  if (c) 0 else v * v
}
~~~

`true` 경로는 v를 쓰지 않아 출력 0회·결과 0이다. `false` 경로는 첫 v에서 go를 한 번 출력하여 5를 저장하고 두 번째 v는 그 값으로 `5*5=25`를 계산한다. `def v=i`로 바꾸면 false에서 두 번 출력한다. `i:Int`로 바꾸면 함수 진입 전에 입력을 평가하여 true에서도 출력한다. By-name 입력과 lazy local의 역할이 둘 다 필요하다.

**채점·확인:** 두 경로의 횟수·값과 두 변경의 실패 이유를 제시한다. 값 25만 맞으면 충분하지 않다.

</details>

### 복습 순서

Q01–Q03에서 '정의·진입·사용'의 시점을 먼저 표시한다. Q04–Q06은 실행되지 않는 오른쪽·branch를 지우며 풀고, Q07의 표를 빈 종이에 다시 만든 뒤 P01의 두 변경안을 반례로 검토한다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · 평가 전략·조건식]] / [[courses/principles_of_programming/transcripts/2026-09-08|보정 STT · 03:43, 09:31, 12:19, 16:04, 23:28, 27:10, 33:12]].
- [[courses/principles_of_programming/lectures/2026-09-15-lecture-04|2026-09-15 강의 노트 · lazy val 복습과 확장]] / [[courses/principles_of_programming/transcripts/2026-09-15|보정 STT · 15:05, 16:59]].
- [Lecture Part 1 · pp.17–24 호출·정의·단락 평가, p.37 lazy val](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).

전략 명칭·평가 횟수·부정 표현에 남은 STT 혼선은 PDF 코드로 발화를 복원했다는 뜻 없이 구분했다. Q06은 기존 강의 연습의 제약과 제공 해답 확인이고 P01은 새 일반 연습이다. By-name의 이름 찾기는 [[courses/principles_of_programming/units/closures-currying|Closure와 호출 환경]]에서 이어진다.


---

[[courses/principles_of_programming/units/expressions-functions|← 이전: Expression·Value·Function과 Evaluation]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/blocks-scope|다음: Blocks, Scope와 Environment →]]
