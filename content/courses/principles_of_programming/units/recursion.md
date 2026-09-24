---
title: "Newton's Method, Recursion과 Tail Call"
description: "Newton 반복·call stack·accumulator·tail call을 계산과 자원 조건으로 설명합니다."
course: "principles_of_programming"
unit_id: "recursion"
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

Newton 갱신의 수치 조건과 재귀 호출이 남기는 작업을 함께 분석합니다. Tail position, 실제 최적화 지원, 정수 범위를 나누어 계산의 정확성과 자원 사용을 판단해 봅니다.

## Newton’s method(뉴턴 방법): 제곱근을 root 탐색으로 바꾸기

제곱근을 구하려면 아직 모르는 정답에 점점 가까워지는 계산을 만들 수 있다. 양의 target(목표값) $n$에 대해 $h(t)=t^2-n$으로 두면, 찾는 양의 제곱근은 $h(t)=0$을 만족하는 root(근)다. 현재 guess(추정값) $g$가 있을 때 그 위치의 접선이 가로축과 만나는 곳을 다음 guess로 삼는 관점이 Newton’s method다.

다음 대수 전개는 자료의 갱신식을 이해하기 위한 설명이다. $h'(g)=2g$이므로, $g>0$일 때

$$
g_{\text{next}}
= g-\frac{h(g)}{h'(g)}
= g-\frac{g^2-n}{2g}
= \frac{g+n/g}{2}.
$$

자료의 `improve(guess, x)`에서는 같은 target을 `x`라고 부른다. `x`는 유지하고 `guess`만 바꾼다. “0으로 가까워진다”는 대상은 $h(g)$이지 양의 제곱근을 찾는 guess 자체가 아니다. 9월 8일 38:19의 강의도 target과 guess가 혼동되지 않도록 target을 `n`으로 구분해 설명한다. 34:49의 “x값이 점점 0으로”라는 표현은 target·guess·함숫값이 혼동된 설명으로 읽어야 한다. 위에서는 자료의 갱신식과 $h(t)=t^2-n$에 따라, 0으로 가야 하는 대상과 구하려는 root를 구분했다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 33:59–40:35]] [POP M002 pp.25–26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### `isGoodEnough`: 모르는 정답 대신 계산 가능한 잔차 검사하기

현재 guess가 $\sqrt{x}$와 얼마나 가까운지 직접 비교하려면 이미 정답을 알아야 한다. 대신 계산 가능한 `guess * guess`가 target `x`에 얼마나 가까운지 본다. 자료의 검사는

$$
0.999 < \frac{\text{guess}^2}{x} < 1.001
$$

이다. $x>0$에서 이는 $|\text{guess}^2-x|/x<0.001$과 같다. **제곱값의 상대 잔차**를 검사하는 것이며, $|\text{guess}-\sqrt{x}|<0.001$이라는 제곱근의 절대오차 조건과는 다르다. 경계가 엄격하므로 비율이 정확히 0.999 또는 1.001이면 실패한다. 이 해석은 자료의 조건식에서 도출한 것이다.

### 검사·개선·반복을 함수로 나누기

자료 p.25는 검사와 반복 부분을 채우는 연습이고 p.26은 다음 해답을 제공한다.

```scala
def isGoodEnough(guess: Double, x: Double) =
  guess * guess / x > 0.999 && guess * guess / x < 1.001

def improve(guess: Double, x: Double) =
  (guess + x / guess) / 2

def sqrtIter(guess: Double, x: Double): Double =
  if (isGoodEnough(guess, x)) guess
  else sqrtIter(improve(guess, x), x)

def sqrt(x: Double) =
  sqrtIter(1, x)
```

`isGoodEnough`는 현재 결과를 받아들일지 정한다. `improve`는 다음 guess를 만든다. `sqrtIter`는 검사에 실패하면 개선된 guess로 자신을 다시 호출하며 target `x`는 그대로 넘긴다. `sqrt`는 초기 guess `1`에서 이 과정을 시작하는 인터페이스다. 9월 8일 41:32의 설명처럼 `sqrtIter`의 목적을 “현재 guess에서 충분히 좋은 근사를 얻는다”로 읽으면 각 함수의 역할이 분명해진다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 38:19, 41:32]]

아래는 `sqrt(2)`의 식을 유리수로 직접 전개한 설명용 계산이다. 실제 `Double` 실행의 출력 자릿수를 복원한 표가 아니다.

| 현재 guess $g$ | $g^2/2$ | 검사 |
|---|---:|---|
| $1$ | $1/2=0.5$ | 실패 |
| $3/2=1.5$ | $9/8=1.125$ | 실패 |
| $17/12\approx1.416667$ | $289/288\approx1.003472$ | 실패 |
| $577/408\approx1.414216$ | $332929/332928\approx1.000003$ | 통과 |

첫 개선은 $(1+2/1)/2=3/2$, 두 번째는 $(3/2+4/3)/2=17/12$다. 두 번째 값이 이미 익숙한 제곱근에 가까워 보여도 자료의 비율 조건은 아직 만족하지 않는다. 다음 개선 후에야 이 정확한 산술 전개에서는 검사를 통과한다.

이 예는 양의 target과 양의 guess에서 읽는다. `x=0`에서는 비율의 분모가 0이고, 음수 target에는 이 실수 제곱근 목표가 맞지 않는다. 유한 정밀도의 모든 입력과 모든 초기값에 대한 종료·수렴 보장은 여기서 얻지 않았다. 다른 문제에 반복 구조를 재사용할 때도 개선식뿐 아니라 정의역과 종료 검사를 함께 맞춰야 한다. STT의 불명확한 소수 출력이나 넓은 수렴 발언을 모든 `Double` 입력의 보장으로 사용하지 않는다.

## Recursion(재귀)이 남기는 continuation(후속 계산)

수학적으로 간결한 정의가 실행 자원도 적게 쓰는 것은 아니다. [[courses/principles_of_programming/units/expressions-functions|기본 재귀 합]]을 작은 입력으로 펼쳐 보면 그 이유를 볼 수 있다.

```text
sum(3)
→ 3 + sum(2)
→ 3 + (2 + sum(1))
→ 3 + (2 + (1 + sum(0)))
→ 3 + (2 + (1 + 0))
→ 6
```

아래로 내려가는 동안 덧셈은 완료되지 않는다. `sum(2)`가 끝나면 3을 더해야 하고, `sum(1)`이 끝나면 2를 더해야 한다. 호출 결과를 받은 뒤 해야 할 일이 continuation이다. Caller(호출자)는 callee(피호출자)가 돌아올 위치, 필요한 environment(환경), 남은 계산에 관한 정보를 유지해야 한다. 이런 호출 정보가 call stack(호출 스택)에 쌓인다.

9월 15일 28:55의 종이 비유는 미뤄 둔 식을 적을 공간을 설명한다. 시간이 충분해도 계속 늘어나는 식을 적을 종이가 부족할 수 있다. 33:56에서는 이를 호출 정보와 stack에 연결한다. 손상된 발화의 용량 단위는 실제 메모리 수치로 해석하지 않는다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 28:55, 33:56]]

Stack overflow(호출 스택 용량 초과)는 미완료 호출이 사용 가능한 stack 공간보다 깊어질 때 생길 수 있다. 전체 RAM이 모두 소진되었다는 뜻과 같지 않다. 자료 p.39의 큰 입력 목록은 실험을 제안하지만 특정 입력부터 항상 실패한다는 보편적 한도를 제공하지는 않는다. `BigInt`처럼 큰 정수를 담는 표현을 사용해도 기다리는 덧셈과 호출 깊이 자체는 그대로 남는다. [POP M002 pp.39–40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### Ordinary recursion(일반 재귀)을 유지할 수 있는 조건

일반 재귀를 사용할지 판단할 때는 **가능한 입력과 프로그램의 호출 경로 전체에서 미완료 호출 깊이가 얼마나 커질 수 있는지** 먼저 확인한다. 그 깊이가 실제 실행 환경의 사용 가능한 stack 안에 충분히 제한된다는 근거가 있다면, 계산 관계를 직접 드러내는 일반 재귀를 유지할 수 있다. 반대로 입력이 커질 수 있거나 깊이의 상한을 모른다면, 짧은 코드라는 이유만으로 안전하다고 판단하지 말고 호출 깊이와 필요한 저장 공간을 따로 분석해야 한다. 다른 함수들이 이미 사용 중인 stack도 있으므로 이 함수 하나의 입력 크기만 보아서는 부족하다.

9월 15일 37:27에서 강사는 프로그램 전체의 상황을 보아 호출이 충분히 작게 제한된다고 확신할 때 간단한 재귀를 그대로 쓸 수 있다고 설명했다. 여기서 “작다”는 실행 환경에 상대적인 조건이다. 발화의 천·10만 같은 숫자는 설명을 위한 예이며 모든 runtime(실행 환경)에 통하는 안전 한도가 아니다. 앞의 `sum(3)`은 대기하는 계산을 보여 주는 작은 예일 뿐, 임의의 큰 `n`도 안전하다는 근거가 되지 않는다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 37:27]]

36:30의 “stack overflow가 없어요”라는 구절은 바로 이어지는 발생 설명과 모순된다. 그 발화를 바꾸어 확정하지 않고, 여기서는 35:32의 깊이 증가 설명과 미완료 호출의 저장 구조를 근거로 **사용 가능한 stack을 넘으면 실패할 수 있다**고 설명한다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 35:32, 36:30]]

## Tail call(꼬리 호출): 반환 뒤에 남은 계산 없애기

호출 결과가 그대로 현재 함수의 결과가 된다면 중간 호출자로 돌아와 추가 계산을 할 필요가 없다. 이 위치에 있는 호출이 tail call이다. `n + sum(n - 1)`은 반환된 값에 `n`을 더해야 하므로 tail call이 아니다. 반면 `sqrtIter(improve(guess,x),x)`는 새 argument를 계산한 뒤 재귀 호출의 결과를 그대로 반환하므로 tail position(꼬리 위치)에 있다. Tail position은 소스의 마지막 줄인지보다 **호출이 돌아온 뒤 할 일이 있는지**로 판별한다.

9월 15일 51:21의 설명은 중간 호출자가 결과를 그대로 전달하기만 한다면 그 복귀 단계를 제거할 수 있다는 것이다. 다만 이런 구조와 실행 구현이 실제로 최적화를 지원하는지는 나누어 판단해야 한다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 51:21]]

### Accumulator(누적값)에 이미 끝낸 계산 담기

합을 tail-recursive하게 만들려면 덧셈을 반환 뒤에 남기는 대신 다음 호출 전에 끝내야 한다. 자료는 `sumItr(res,m)`에서 `res`에 이미 더한 합을, `m`에 아직 처리하지 않은 범위를 담는다. [POP M002 p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
import scala.annotation.tailrec

def sum(n: Int): Int = {
  @tailrec
  def sumItr(res: Int, m: Int): Int =
    if (m <= 0) res
    else sumItr(m + res, m - 1)
  sumItr(0, n)
}
```

`sum(3)`의 상태는 다음과 같다.

| 호출 상태 `(res,m)` | 이미 계산한 합 | 남은 합 | 다음 단계 |
|---|---:|---|---|
| `(0,3)` | 0 | `1+2+3` | `(3,2)` |
| `(3,2)` | 3 | `1+2` | `(5,1)` |
| `(5,1)` | 5 | `1` | `(6,0)` |
| `(6,0)` | 6 | 없음 | `6` 반환 |

정수 범위 안에서 `res + (1 + … + m)`이 원래 구하려던 합이라는 관계가 유지된다. 이것이 상태의 뜻을 확인하는 invariant(불변 관계)다. 한 단계에서 `m`을 `res`에 더하고 남은 범위를 하나 줄여도 전체 합은 변하지 않는다. 마지막에는 남은 범위가 없으므로 `res`가 답이다.

`sumItr(m + res, m - 1)`에 덧셈이 있다고 tail call이 아닌 것은 아니다. CBV 규칙으로 새 argument를 **호출 전에** 계산하며, 호출이 돌아온 뒤에는 덧셈이 없다. 강의의 지우개 비유는 이전 상태를 새 상태로 바꾸어 대기식 목록을 늘리지 않는다는 뜻이다. “두 칸”이라는 비유가 전체 runtime의 메모리가 두 word뿐이라는 뜻은 아니다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 38:27–40:49]]

이 관점은 과거 평가에서도 결과가 맞는 것과 요구한 재귀 구조를 지키는 것을 구분하는 데 쓰인다. 2024년 중간고사의 해당 부분은 tail recursion이라는 구현 조건을 별도로 요구한다. 지금 가져올 핵심은 상태의 의미와 반환 뒤의 남은 작업을 설명하는 능력이다. 그 문항 전체를 풀려면 아직 이 단원에서 다루지 않은 사용자 정의 list와 타입 매개변수도 필요하다. [EX:pop_2024_mid_q02_s01 L.36-42]

### `@tailrec`은 알고리즘을 대신 고쳐 주지 않는다

자료의 `@tailrec`은 compiler(컴파일러)에 tail recursion의 의도를 알리고 지원 조건을 만족하지 못하면 오류로 드러내도록 하는 표기다. `n + sum(n-1)`에 annotation만 붙여도 accumulator 알고리즘으로 자동 변환된다고 생각하면 안 된다. 먼저 호출 뒤의 일을 없애는 구조로 작성해야 한다. 9월 15일 01:05:32에서는 이 의도를 명시하여 실수를 오류로 발견하는 용도로 설명했다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 01:05:32]]

Tail-call optimization(꼬리 호출 최적화)이 적용되면 이 호출 사슬의 stack 증가를 줄일 수 있다. 그렇다고 계산 시간이 사라지거나, 다른 데이터 할당과 수치 범위 문제가 모두 해결되는 것은 아니다. 언어와 구현에 따라 지원 범위가 다르므로 tail position이라는 구조적 사실과 실제 최적화 여부를 따로 확인해야 한다.

이 차이를 보여 주려고 강사는 9월 15일 43:09에 Python을 예로 들어, tail-call 형태로 작성해도 그 최적화를 해 주지 않는다고 설명했다. 여기서 가져올 핵심은 호출 뒤 할 일이 없다는 구조만으로 실행 환경이 중간 호출 정보를 없애 준다고 단정할 수 없다는 것이다. Python에 관한 설명은 강의에서 전달된 사례로 읽으며, 모든 Python 구현의 정책을 독립적으로 확인한 결론으로 확대하지 않는다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 43:09]]

이어 44:09에서는 accumulator를 전달하는 tail-recursive 표현보다 `while`이 읽기 쉽고, 일반 재귀는 깊이가 작은 경우에 쓰게 하고 싶다는 설계 취향을 전달했다. 이는 **가독성에 관한 평가**이며 최적화가 가능한 구조인지, 실제로 지원되는지와는 다른 판단이다. 강사가 전달한 견해를 특정 설계자의 확인된 직접 인용으로 받아들일 필요도 없다. 45:53에서는 두 상태를 갱신하는 반복과 인자를 넘기는 tail-recursive 표현의 본질적 연결을 짚고, 표현이 읽기 좋은지는 학습자가 비교해 판단하도록 했다. 앞의 `sumItr(res,m)`도 누적값과 남은 범위라는 상태를 다음 호출의 인자로 전달하므로 이 연결을 보여 준다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 44:09, 45:53]]

따라서 tail position은 반환 뒤의 계산 유무로, 최적화 지원은 실제 언어·구현의 조건으로, 가독성은 상태의 의미와 흐름이 독자에게 얼마나 명확한지로 판단한다. 읽기 편하다는 평가가 stack 사용 감소를 보장하지 않고, 최적화되지 않는 구현이 있다는 사실도 tail position이라는 개념을 바꾸지 않는다.

## Integer overflow(정수 범위 초과)와 Stack overflow의 구분

큰 입력의 합에서 숫자가 이상하게 나오는 문제와 호출 깊이 때문에 중단되는 문제는 다르다. `Int`의 최대값은 2147483647이다. 수학적으로

$$
1+\cdots+100000
=\frac{100000\times100001}{2}
=5000050000
$$

이므로 같은 `Int`에 이 합을 그대로 담을 수 없다. 이 값은 자료의 정수 범위에 근거한 설명용 계산이며 STT의 불명확한 실시간 출력을 복원한 것이 아니다. [POP M002 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 문제 | 부족하거나 넘치는 대상 | 바꾸어야 할 관점 |
|---|---|---|
| Stack overflow | 미완료 호출을 저장할 공간 | 호출 구조·깊이·최적화 지원 |
| Integer overflow | 정수를 표현할 범위 | 숫자 type과 중간 계산 범위 |
| 긴 계산 시간 | 필요한 연산량 | 알고리즘과 입력 크기 |

Tail recursion으로 바꾸어 stack 문제를 줄여도 `Int` 범위는 그대로다. `BigInt`로 숫자 범위를 넓혀도 ordinary recursion의 호출 깊이는 그대로일 수 있다. 9월 15일 01:00:39에서는 숫자 결과의 이상을 integer overflow와 연결했지만, 정확한 화면 입력·출력과 시간 수치는 불명확하다. 그 보고를 다른 언어나 모든 실행의 동일한 결과로 일반화하지 않는다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 01:00:39]]

## Mutual recursion(상호 재귀)과 일반 Tail call

Tail call은 자기 자신을 부르는 경우에만 생기지 않는다. 함수 F가 G의 결과를 그대로 반환해도 tail call이다. Tail recursion은 그중 자기 재귀가 tail position에 놓인 경우다. 자료 p.42의 다음 두 함수는 서로를 tail call로 호출한다.

```scala
def sum(acc: Int, n: Int): Int =
  if (n <= 0) acc else sum2(n + acc, n - 1)

def sum2(acc: Int, n: Int): Int =
  if (n <= 0) acc else sum(2 * n + acc, n - 1)
```

이 코드의 이름이 `sum`이라고 앞의 일반 합과 같은 계산은 아니다. 한 함수는 `n`을, 다른 함수는 `2*n`을 더한다. 작은 입력으로 추적하면

```text
sum(0,3)
→ sum2(3,2)
→ sum(7,1)
→ sum2(8,0)
→ 8
```

이다. 일반적인 `1+2+3=6`과 다르다. 호출 뒤에 더할 것은 없지만 자료는 직접 `sum(0,20000)`을 실행하는 예에 stack overflow 주석을 둔다. 그 주석은 자료의 실행 설명이며 여기서 새로 재현한 결과는 아니다. [POP M002 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### `TailCalls`: 완료값과 다음 계산 구분하기

자료 p.43은 같은 상호 재귀를 다음과 같이 표현한다.

```scala
import scala.util.control.TailCalls._

{
  def sum(acc: Int, n: Int): TailRec[Int] =
    if (n <= 0) done(acc)
    else tailcall(sum2(n + acc, n - 1))

  def sum2(acc: Int, n: Int): TailRec[Int] =
    if (n <= 0) done(acc)
    else tailcall(sum(2 * n + acc, n - 1))

  sum(0, 20000).result
}
```

`TailRec[Int]`는 최종적으로 `Int`를 얻을 계산을 표현한다. `done(acc)`는 이미 끝난 결과이고, `tailcall(...)`은 계속 진행할 다음 계산을 나타낸다. 마지막 `.result`로 그 계산의 결과를 얻는다. 직접 상호 호출의 깊이를 쌓는 것과 다른 표현으로 실행을 진행시키되, `n`과 `2*n`을 번갈아 더한다는 계산 의미는 유지한다. [POP M002 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

9월 15일 후반 강의는 자기 tail recursion과 일반 tail call의 구현 지원 차이를 논의한다. Java로 옮기는 과정 때문일 것이라는 설명은 강사의 가설로 제시되었으므로 compiler 내부의 확정 사실로 쓰지 않는다. 남는 원리는 명확하다. 호출이 tail position에 있다는 성질, 그 성질을 실행 환경이 지원하는 방식, 계산이 요구하는 다른 자원은 각각 구분해서 읽어야 한다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 01:05:32–01:12:25]]

## 핵심 정리

- Newton 갱신은 target을 유지하고 guess를 바꾼다. 0으로 가려는 것은 `h(g)=g*g-n`이며 guess 자체가 아니다.
- `0.999 < guess*guess/x < 1.001`은 제곱값의 상대 잔차 검사다. 엄격한 경계·양의 정의역·초기값을 함께 확인한다.
- Ordinary recursion(일반 재귀)은 반환 후의 continuation(후속 계산)을 쌓을 수 있다. 가능한 전체 호출 깊이가 실제 stack 안에 제한되는지 판단해야 한다.
- Tail call(꼬리 호출)은 반환 뒤에 일이 없는 호출이다. Accumulator(누적값)의 의미와 불변 관계를 설명하면 변환을 검산할 수 있다.
- `@tailrec`은 임의의 알고리즘을 고쳐 주지 않는다. 구조·최적화 지원·가독성은 다른 판단이며 stack 감소가 integer overflow·시간 비용까지 해결하지는 않는다.
- 상호 tail call도 존재한다. 자료의 `TailCalls`는 완료값과 다음 계산을 구분하지만 원래 계산의 의미는 유지한다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Newton의 target·guess·root

양의 target n의 제곱근을 찾는 함수 `h(t)`와 root 조건을 적어라. 양의 guess g에서 다음 guess의 식을 설명하고 n=2,g=1을 한 번 갱신하라. 무엇이 0에 가까워지는가?

<details><summary>해설 보기</summary>

`h(t)=t*t-n`에서 `h(t)=0`인 양의 t를 찾는다. 접선의 가로축 교점은 `g-h(g)/h'(g)`이고 `h'(g)=2g`이므로 `g-(g*g-n)/(2g)=(g+n/g)/2`다. 미분 전개는 본문의 선택적 설명이며 갱신식 자체로도 계산할 수 있다. n=2,g=1이면 새 guess는 `(1+2/1)/2=1.5`, target은 2로 유지된다. 0에 접근하는 것은 h(g)이고 guess의 목표는 √2다.

**채점·확인:** target 유지·guess 개선·h(g)의 0과 양의 root를 구분하며 1.5를 얻는다.

</details>

#### 확인 Q02 · 잔차 기준과 sqrt(2)의 trace

`0.999<guess*guess/x<1.001`은 무엇의 오차인가? 경계 0.999/1.001과 `sqrt(2)`의 guess `1,3/2,17/12,577/408`을 판정하라. 임의의 시작점과 모든 Double에 대한 보장인가?

<details><summary>해설 보기</summary>

x>0에서 `|guess*guess-x|/x<0.001`인 제곱값의 상대 잔차다. `|guess-sqrt(x)|<0.001`인 근의 절대오차와 같지 않다. 두 경계는 엄격한 부등식 때문에 실패한다. 나열한 guess의 비율은 각각 `1/2`, `9/8`, `289/288≈1.003472`, `332929/332928≈1.000003`이다. 앞 세 개는 실패, 마지막은 통과한다. 자료 초기값은 1이다. x=0은 분모 문제, 음수 x는 이 실수 제곱근 목표와 맞지 않으며 모든 유한 정밀도 입력·초기값의 수렴을 보장하지 않는다. 이 유리수 trace는 실시간 Double 출력의 복원이 아니다.

**채점·확인:** 잔차 의미·두 엄격 경계·네 판정·정의역 한정을 모두 제시한다.

</details>

#### 확인 Q03 · 검사·개선·반복의 역할

`isGoodEnough`, `improve`, `sqrtIter`, `sqrt`가 각각 하는 일과 재귀 호출에서 바뀌는 인자를 설명하라. `improve`만 바꾸면 어떤 root 문제든 해결되는가?

<details><summary>해설 보기</summary>

isGoodEnough는 현재 guess를 받아들일지 검사하고 improve는 `(guess+x/guess)/2`로 다음 guess를 만든다. sqrtIter는 검사 성공 시 현재 guess를 반환하고 실패 시 개선한 guess와 같은 x로 다시 호출한다. sqrt는 `sqrtIter(1,x)`로 시작한다. 반복 구조를 재사용할 수 있어도 새 문제에 맞는 정의역·충분함 기준·진행 조건까지 필요하다. 갱신식만 바꿔 모든 문제의 종료·수렴이 확보되는 것은 아니다.

**채점·확인:** 네 역할과 guess/x의 변화 여부, 재사용에 필요한 조건을 설명한다.

</details>

#### 확인 Q04 · Continuation과 일반 재귀를 남길 조건

`sum(3)`에서 기다리는 일을 적고 caller가 보존하는 정보를 설명하라. BigInt나 더 긴 실행 시간이 깊은 호출을 해결하는가? 일반 재귀를 그대로 사용할 판단 기준도 제시하라.

<details><summary>해설 보기</summary>

`3+(2+(1+sum(0)))`까지 내려가면서 반환 뒤 더해야 할 1,2,3이 남는다. Caller는 돌아올 위치, 필요한 environment, 남은 계산인 continuation 정보를 유지하며 call stack이 이를 저장한다. Stack overflow는 미완료 호출이 사용 가능한 stack을 넘어서는 문제이지 전체 RAM 고갈과 같은 뜻이 아니다. BigInt는 수치 범위를 바꾸고 긴 시간은 실행 시간 여유를 줄 뿐 이 대기 정보를 없애지 않는다.

가능한 입력과 프로그램 전체의 호출 경로에서 최대 미완료 깊이가 실제 실행 환경의 stack 안에 충분히 제한된다는 근거가 있으면 일반 재귀를 유지할 수 있다. 다른 함수가 이미 쓰는 stack도 고려한다. 상한을 모르거나 커질 수 있으면 깊이·공간 분석이 필요하다. 강의의 작은 입력 숫자는 예시이며 보편적 안전 한도가 아니다.

**채점·확인:** 대기 덧셈과 저장 정보, 세 자원의 차이, 프로그램 전체 깊이와 실제 stack 기준을 모두 설명한다.

</details>

#### 확인 Q05 · Tail position과 accumulator 불변 관계

`n+sum(n-1)`, `sqrtIter(improve(guess,x),x)`, `sumItr(m+res,m-1)` 중 tail call을 판별하라. `sumItr(res,m)`의 종료 규칙을 쓰고 초기 `(0,3)`의 trace와 invariant를 적어라.

<details><summary>해설 보기</summary>

첫 식은 호출 뒤 n을 더하므로 tail call이 아니다. 나머지는 새 argument를 호출 전에 계산하고 반환값을 그대로 넘기므로 tail position이다. 합의 helper는 `m<=0`이면 res를 반환하고 아니면 다음 상태 `(m+res,m-1)`로 간다. `(0,3)→(3,2)→(5,1)→(6,0)→6`이다. 정수 범위 내에서 `res+(1+…+m)`은 원래 합으로 유지된다. 현재 m을 res에 옮기면서 남은 합에서 빼므로 전체가 변하지 않는다. 0에서 남은 항이 없으면 res가 답이다.

**채점·확인:** 마지막 줄 여부 대신 반환 뒤의 일을 보고, 인자 덧셈과 invariant 보존을 설명한다.

</details>

#### 확인 Q06 · Annotation·구현 지원·가독성

`@tailrec`은 `n+sum(n-1)`을 자동으로 고쳐 주는가? Tail-call 최적화의 효과를 한정하고, 9월 15일 Python 사례와 while 선호를 구조·지원·가독성으로 나누어 설명하라.

<details><summary>해설 보기</summary>

Annotation은 지원되는 tail-recursive 형태를 의도했음을 표시하고 조건을 충족하지 못할 때 오류로 드러내는 장치다. 반환 뒤 덧셈을 accumulator로 재설계하는 일은 작성자가 해야 한다. 최적화가 적용되면 해당 호출 사슬의 stack 증가를 줄일 수 있지만 계산량·다른 할당·숫자 범위까지 없애지는 않는다.

강사는 Python을 tail 형태로 써도 최적화가 자동 적용되지 않는 사례로 전달했다. 이는 구조가 곧 지원 보장이 아니라는 설명이며 모든 Python 구현을 독립 확인한 결론은 아니다. 이어 accumulator 표현보다 while이 읽기 쉽고 일반 재귀는 얕은 경우에 쓰고 싶다는 설계 취향을 소개했다. 가독성 평가는 최적화 가능 구조·실제 지원과 별개다. While의 상태 갱신과 tail recursion의 인자 전달은 누적값·남은 범위를 다음 단계로 넘기는 연결이 있지만, 무엇이 읽기 좋은지는 상태의 의미와 흐름을 보고 판단한다.

**채점·확인:** annotation의 한계, stack 효과의 범위, Python의 귀속, while 가독성 평가를 각각 설명한다.

</details>

#### 확인 Q07 · 정수 범위와 호출 공간

1부터 100000까지의 수학적 합과 `Int` 최대값을 비교하라. Tail-recursive 구현에서 예상과 다른 숫자가 나왔다면 최적화 실패라고 단정할 수 있는가? BigInt와 tail 변환이 해결하는 대상을 나누어라.

<details><summary>해설 보기</summary>

수학적 합은 `100000*100001/2=5000050000`이며 `Int` 최대값 2147483647보다 크다. 이 산술은 수학적 정수 계산이지 중간 곱을 Int에서 실행하라는 코드가 아니다. Stack 증가를 줄여도 Int 범위는 그대로라 예상 수를 담지 못할 수 있다. BigInt는 큰 수 표현을 다루지만 일반 재귀의 깊이는 줄이지 않는다. 긴 시간, 깊은 호출, 수치 범위를 각각 검사해야 하며 강의의 불명확한 음수·0 출력으로 정확한 실행을 복원하지 않는다.

**채점·확인:** 5000050000과 범위 비교, 중간 계산 주의, 수치·stack 원인의 독립성을 설명한다.

</details>

#### 확인 Q08 · 상호 tail call의 계산 의미

자료의 `sum(acc,n)`은 n>0에서 `sum2(n+acc,n-1)`, `sum2(acc,n)`는 `sum(2*n+acc,n-1)`을 호출하며 n<=0이면 acc를 반환한다. `sum(0,3)`을 전개하고 일반 합인지, 자기 tail recursion인지 판정하라.

<details><summary>해설 보기</summary>

`sum(0,3)→sum2(3,2)→sum(7,1)→sum2(8,0)→8`이다. 두 함수가 n과 2*n을 번갈아 더하므로 일반 합 6과 다르다. 호출 결과를 추가 계산 없이 반환하여 둘 다 tail call이지만 서로 다른 함수를 부르는 상호 재귀다. Tail recursion이라는 자기 호출의 경우와 일반 tail call을 구분해야 한다. Tail position만으로 해당 구현의 stack 감소를 보장하지 않는다.

**채점·확인:** 8의 각 상태와 n/2*n 교대, tail call과 자기 재귀 구별을 포함한다.

</details>

#### 확인 Q09 · TailCalls의 완료값과 다음 계산

자료 p.43의 `TailRec[Int]`, `done(acc)`, `tailcall(...)`, `.result`는 각각 무엇인가? 직접 상호 호출과의 관계 및 Java 변환에 관한 강사의 설명은 어느 범위로 읽어야 하는가?

<details><summary>해설 보기</summary>

`TailRec[Int]`는 최종 Int를 얻을 계산의 표현이다. `done(acc)`는 이미 완료된 값, `tailcall(...)`은 계속할 다음 계산이고 바깥 `.result`가 그 계산을 진행해 결과를 얻는다. p.42의 n·2*n 교대 계산을 유지하면서 직접 상호 호출의 깊이를 쌓는 것과 다른 실행 표현을 제공한다. p.42의 20000 입력 stack overflow 주석은 자료의 보고이며 새로 측정한 보편 한도가 아니다. Scala에서 Java로 변환하며 일이 남을 수 있다는 설명은 강사의 가설로 명시되었으므로 compiler 내부의 확인된 사실로 쓰지 않는다.

**채점·확인:** 네 표기·원래 계산 의미의 보존·자료 실행 주석과 구현 가설의 한정을 적는다.

</details>

### 적용 연습

#### 연습 P01 · 결과와 tail 구조를 함께 만족시키기

**새로 만든 synthetic(합성) 연습이며 실제 기출 문항이 아니다.** 2024 중간 Q2-1의 '결과뿐 아니라 tail-recursive 구조를 만족해야 한다'는 요구를 옮겼다. 근거는 Main.scala의 [EX:pop_2024_mid_q02_s01 L.36-42]이다. 이 연습의 전제는 조건 재귀·정수 곱셈·accumulator이며, 원문 전체에 필요한 generic list와 타입 매개변수는 아직 별도 학습이 필요하다.

`0<=n<=20`에 대해 `S(0)=0`, `S(n)=n*n+S(n-1)`을 계산하는 tail-recursive `squares(n:Int):Int`를 작성하라. 초기·종료 상태, invariant, n=3·0·5의 결과를 설명하고 기존 비꼬리 재귀에 annotation만 붙이는 제안이 충분한지도 판정하라.

<details><summary>해설 보기</summary>

~~~scala
import scala.annotation.tailrec
def squares(n: Int): Int = {
  @tailrec
  def go(res: Int, m: Int): Int =
    if (m <= 0) res
    else go(res + m * m, m - 1)
  go(0, n)
}
~~~

Invariant는 `res+S(m)=S(n)`이다. 시작에서는 `0+S(n)`이고, 한 단계의 `res'=res+m*m`와 `m'=m-1`는 문제의 정의 `S(m)=m*m+S(m-1)` 때문에 합을 보존한다. m=0이면 res가 답이다.

n=3의 상태는 `(0,3)→(9,2)→(13,1)→(14,0)`이다. n=0은 0, n=5는 `25+16+9+4+1=55`다. n<=20에서 최댓값은 `S(20)=2870`이며 중간 값도 이 범위 안이다. 재귀 호출 전에 곱셈·덧셈을 마치고 반환 뒤에는 일이 없다. `n*n+squares(n-1)`에 annotation만 붙여도 남은 덧셈은 사라지지 않는다. 이 숫자 범위 확인과 실제 최적화 지원은 별도 판단이다.

**채점·확인:** 코드·초기/종료 상태·invariant 보존·14/0/55·tail 판정이 모두 있어야 한다. 원문 list 구현이나 제공 테스트를 이 해답의 검증으로 대신하지 않는다.

</details>

### 복습 순서

Q01–Q03에서 target·guess·잔차를 먼저 분리한다. Q04의 대기식을 Q05의 두 상태로 바꾸고, Q06–Q07로 최적화와 수치 문제를 따로 검사한다. P01을 해설 없이 작성한 뒤 Q08–Q09로 자기 재귀와 일반 tail call을 비교한다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · Newton 반복]] / [[courses/principles_of_programming/transcripts/2026-09-08|보정 STT · 33:59–46:31]].
- [[courses/principles_of_programming/lectures/2026-09-15-lecture-04|2026-09-15 강의 노트 · 재귀·stack·tail call]] / [[courses/principles_of_programming/transcripts/2026-09-15|보정 STT · 22:39, 28:55, 33:56, 35:32–37:27, 38:27–40:49, 43:09, 44:09, 45:53, 51:21, 01:00:39–01:12:25]].
- [Lecture Part 1 · p.12 정수 범위, pp.25–26 Newton, pp.39–43 재귀와 TailCalls](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).
- 과거 평가의 제한된 연결: 2024 중간 Q2-1 Main.scala [EX:pop_2024_mid_q02_s01 L.36-42]. 원문은 generic list 전제가 추가로 필요하며 P01은 새 합성 연습이다.

접선 판서와 정확한 실시간 소수·정수 출력은 제공 자료만으로 복원하지 않았다. Python 사례·while 가독성은 강사가 전달한 설명이며 보편적 구현 검증이 아니다. 제공된 과거 자료는 전체 시험을 뜻하지 않으며 역사적 제약을 현 학기 규정으로 옮기지 않는다.


---

[[courses/principles_of_programming/units/blocks-scope|← 이전: Blocks, Scope와 Environment]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/higher-order-functions|다음: Higher-Order Functions와 계산 구조의 재사용 →]]
