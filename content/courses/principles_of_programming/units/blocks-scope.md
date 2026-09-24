---
title: "Blocks, Scope와 Environment"
description: "Block 결과·shadowing·정의 환경·정적 검사와 local helper 구성을 추적합니다."
course: "principles_of_programming"
unit_id: "blocks-scope"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-08-lecture-03", "courses/principles_of_programming/lectures/2026-09-10-materials-blocks", "courses/principles_of_programming/lectures/2026-09-15-lecture-04"]
---

Block의 마지막 식과 각 이름이 연결된 환경을 따라 계산합니다. 이름의 가림, 정의 순서의 검사, 보조 함수 은닉을 구분하여 같은 이름이 있어도 의미를 정확히 읽어 봅니다.

## Block(블록): 여러 정의를 하나의 expression으로 묶기

계산을 설명하기 위해 붙인 보조 이름이 모두 바깥으로 드러날 필요는 없다. Block은 `{ ... }` 안에 정의와 expression(표현식)을 묶어, 필요한 범위 안에서 이름을 쓰게 한다. 앞의 [[courses/principles_of_programming/units/expressions-functions|expression 평가 규칙]]을 그대로 이어서, block 자체도 expression이며 **마지막 expression의 값이 block 전체의 결과**다. 이 원리로 여러 단계의 계산을 하나의 값으로 사용할 수 있다.

설명용으로 `{ val a = 2; val b = 3; a + b }`를 읽으면, 두 local value(지역값)를 정의한 뒤 마지막 `a + b`를 평가하므로 전체 결과는 `5`다. 마지막 정의의 이름을 자동으로 반환하는 것이 아니라, 마지막 expression을 평가한다. [POP M002 p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

이 단원의 Blocks·Safety Checking·줄바꿈 예는 [[courses/principles_of_programming/lectures/2026-09-10-materials-blocks|9월 10일자로 정리된 pp.27–35 자료 복습]]을 포함한다. 그날 녹음이나 STT가 없어 이 범위를 실제 수업 진도로 확정하지 않는다. 9월 15일의 도입에는 block과 보조 함수 은닉에 대한 복습 발화가 따로 있다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 01:42–03:06]]

### Scope(유효 범위)와 Shadowing(이름 가림)

Block 안에서 정의한 이름은 그 범위 안에서 사용한다. 안쪽 block은 바깥 이름을 사용할 수 있지만, 같은 이름을 안쪽에서 새로 정의하면 가까운 정의가 바깥 정의를 가린다. 이것이 shadowing이다. 자료의 모델에서는 한 block 안의 중복 정의를 허용하지 않는 것과 중첩된 block의 shadowing을 구분한다. [POP M002 p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

다음은 shadowing을 따로 보기 위해 만든 설명용 예다.

```scala
{
  val t = 0
  val r = {
    val t = 10
    t + 1
  }
  t + r
}
```

안쪽의 `t + 1`은 안쪽 binding(이름 연결)의 `10`을 읽어 `11`이 된다. 그 값이 `r`에 연결된다. 바깥의 `t + r`는 바깥 `t=0`을 읽으므로 최종 값도 `11`이다. 안쪽 `val t = 10`은 바깥 `t`를 바꾸는 대입이 아니다. 같은 철자의 이름을 가진 서로 다른 binding을 만든 것이다.

## Environment(환경)와 정의 위치에 따른 이름 찾기

Environment는 이름과 그 의미를 연결하는 문맥이다. Function(함수)의 body(본문)를 평가할 때는 **함수가 정의된 environment**를 기준으로 바깥 이름을 찾는다. 호출 위치에 같은 이름이 있다고 함수 안의 이름이 그쪽으로 바뀌지는 않는다. 다음은 자료 p.29의 예다.

```scala
{
  val t = 0
  def f(x: Int) = t + g(x + 1)
  def g(y: Int) = y * y
  val x = f(5)
  val r = {
    val t = 10
    val s = f(5)
    s - t
  }
  t + r
}
```

`f`와 `g`는 바깥 environment에서 정의되었다. 바깥의 `f(5)`는 `0 + g(6) = 36`이므로 바깥 `x`는 `36`이다. 안쪽 block에서 `t=10`을 정의한 뒤 `f(5)`를 호출해도 `f`의 body가 찾는 `t`는 여전히 바깥의 `0`이다. 따라서 `s=36`이다. 다만 안쪽 block에 직접 쓰인 `s - t`의 `t`는 안쪽의 `10`이므로 `r=26`이 된다. 최종 `t + r`는 바깥에서 평가하여 `0+26=26`이다.

### 호출별 environment를 구분한 실행표

자료 p.32의 실행표는 위 예와 닮았지만 바깥 정의가 `val x = f(5) + 7`이다. 따라서 **p.29의 바깥 `x`는 36, p.32의 바깥 `x`는 43**이다. 두 예의 최종 값은 모두 26이라 중간 차이를 놓치기 쉽다. [POP M002 pp.29, 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

원본 p.32에서 볼 핵심은 각 함수 호출 앞에 표시된 부모 environment와, 안쪽 block의 별도 binding이다. `E0::[E1|x=5]`는 새 `E1`에 parameter `x=5`를 두고 바깥 이름은 `E0`를 따라 찾는다는 표기다.

| p.32의 계산 위치 | 새 environment와 부모 | 계산 |
|---|---|---|
| 첫 `f(5)` | `E1: x=5`, 부모 `E0` | `t=0`, `g(6)` 요구 |
| 첫 `g(6)` | `E2: y=6`, 부모 `E0` | `6*6=36` |
| 바깥 `x` 초기화 | `E0` | `36+7=43` |
| 안쪽 block | `E3: t=10`, 부모 `E0` | `s`를 위해 `f(5)` 호출 |
| 두 번째 `f(5)` | `E4: x=5`, 부모 `E0` | 다시 `0+g(6)` |
| 두 번째 `g(6)` | `E5: y=6`, 부모 `E0` | 다시 `36` |
| 안쪽 마지막 식 | `E3: t=10, s=36` | `s-t=26` |
| 바깥 마지막 식 | `E0: t=0, r=26` | `t+r=26` |

함수 parameter `x=5`와 바깥 `val x=43`도 서로 다른 binding이다. 또한 `E4`의 부모를 호출한 block인 `E3`로 연결하면 `f` 안에서 잘못된 `t`를 찾게 된다. 부모는 정의 위치의 `E0`다.

원본 p.32의 저장 환경 요약에는 `f=(x)t+g(x)`라고 적힌 부분이 있지만, 위쪽 코드와 호출 전개는 `g(x+1)`이다. 여기서는 서로 일치하는 코드와 호출 전개를 따라 `g(6)=36`으로 계산했다. 이 표기 불일치를 결과가 25라는 별도의 규칙으로 해석하면 안 된다.

## Safety Checking(안전성 검사): 이름이 준비되어야 하는 시점

앞서 본 [[courses/principles_of_programming/units/evaluation-strategies|`def`와 `val`의 평가 시점]]을 떠올려 보자. `def`는 계산을 정의하고 `val`은 정의 위치에서 값을 요구한다. 그래서 소스의 아래쪽에 필요한 이름이 언젠가 등장한다는 것만으로 충분하지 않다. 값이 필요한 시점에 그 이름이 준비되어 있어야 한다.

자료 p.30은 `def f(x: Int) = g(x)`, `def g(x: Int) = 10`, `val x = f(10)`의 순서는 허용 대상으로 제시한다. 반면 `f`와 `g`의 정의 사이에 `val x = f(10)`을 넣으면 `g`가 준비되기 전에 계산을 시작하려 한다. 자료 p.31은 이를 다음과 같은 정적 규칙으로 정리한다. [POP M002 pp.30–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 정의 | 오른쪽 expression에서 필요한 외부 이름의 준비 기한 |
|---|---|
| `val x = e` | 해당 `val` 정의 전 |
| `def x = e` | 다음 `val` 정의 전 |

Parameter처럼 body 안에서 도입되는 이름은 자신의 범위에서 읽는다. 아래는 원본의 통과·실패 배치다.

```scala
// 자료의 검사에서 통과
{
  def f(x: Int) = g(x)
  def g(x: Int) = 10
  val a = 10
  f(10)
}
```

```scala
// 자료의 검사에서 실패
{
  def f(x: Int) = g(x)
  val a = 10
  def g(x: Int) = 10
  f(10)
}
```

두 번째의 `val a`는 `f`를 호출하지도 않는다. 그래도 `f`가 필요로 하는 `g`가 **다음 `val` 경계 뒤**에 있으므로 자료의 검사는 실패한다. 실제로 마지막 호출만 머릿속에서 실행해 보는 것과 보수적인 정적 규칙을 적용하는 것은 다른 판단이다. 여기의 통과·실패는 강의자료의 모델이며, 모든 Scala 버전의 compiler가 사용하는 전체 규칙을 대신하지 않는다.

## Semi-colon(세미콜론)과 Parenthesis(괄호): expression 경계 드러내기

`;`는 같은 줄의 여러 정의나 expression을 구분한다. 한 expression을 여러 줄로 나누려면 이어지는 범위도 분명해야 한다. 자료 p.33은 아래 세 배치를 대비한다. 각 예는 별도 block이며 `square`는 제곱 함수라고 둔다. [POP M002 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
// 자료의 허용 예
val r = {
  val t = 10; val s = square(5); t +
  s
}
```

```scala
// 자료의 비허용 예
val r = {
  val t = 10; val s = square(5); t
  + s
}
```

```scala
// 자료의 허용 예
val r = {
  val t = 10; val s = square(5); (t
  + s)
}
```

첫 예에서는 줄 끝의 `+`가 아직 오른쪽 operand를 기다리고 있다. 두 번째는 `t`만으로 식이 끝난 것으로 읽힐 수 있어 의도한 덧셈의 경계가 불분명하다. 세 번째는 괄호가 `t + s` 전체를 한 식으로 묶는다. 이 자료의 허용·비허용 표기를 읽는 목적은 줄 수를 외우는 것이 아니라 expression이 어디까지인지 명확히 표현하는 데 있다.

## 보조 함수를 block 안에 숨겨 `sqrt`의 인터페이스 정리하기

Block은 보조 이름을 숨기는 데도 쓰인다. 제곱근 계산을 외부에서 사용하는 사람에게는 `sqrt`가 필요하지만, 내부에서 검사·개선·반복을 맡는 이름까지 모두 드러낼 필요는 없다. 자료 pp.34–35는 기존 계산을 아래처럼 `sqrt` 안에 묶는다. [POP M002 pp.34–35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def sqrt(x: Double) = {
  def sqrtIter(guess: Double, x: Double): Double = {
    if (isGoodEnough(guess, x)) guess
    else sqrtIter(improve(guess, x), x)
  }
  def isGoodEnough(guess: Double, x: Double) = {
    val ratio = guess * guess / x
    ratio > 0.999 && ratio < 1.001
  }
  def improve(guess: Double, x: Double) =
    (guess + x / guess) / 2
  sqrtIter(1, x)
}
```

이 계산에서 `x`는 양의 target(목표값), `guess`는 현재 추정값이다. `isGoodEnough`가 충분히 좋다고 판단하면 `guess`를 반환하고, 아니면 `improve`로 새 추정값을 만들어 반복한다. Block의 마지막 `sqrtIter(1,x)`가 그 계산을 시작하며, 얻은 값이 `sqrt` 전체의 결과다. 수치 갱신의 이유와 정의역은 [[courses/principles_of_programming/units/recursion|Newton’s method와 재귀 계산]]과 연결된다.

원본 p.35에서 볼 두 변화는 helper를 내부로 옮긴 것과 `ratio`에 중복 계산을 모은 것이다. `ratio`는 한 번의 `isGoodEnough` 호출 안에서 계산하여 두 비교에 재사용한다. 다음 반복에서 `guess`가 달라지면 새 호출의 `ratio`도 다시 계산한다. 경계는 엄격한 부등식이므로 정확히 0.999나 1.001인 경우는 통과하지 않는다.

내부로 옮겼다고 helper의 `x` parameter를 제거한 것은 아니다. 원본 코드에는 그대로 남아 있다. 바뀐 것은 이름을 드러내는 범위와 local 계산의 조직이고, 갱신식과 반복의 목적은 유지된다. 9월 15일 03:06의 강의도 외부에서는 `sqrt`만 보이고 보조 함수들은 내부에 숨는다는 점을 설명한다. [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 03:06]]

## 핵심 정리

- Block(블록)은 마지막 expression의 값을 내는 expression이다. 안쪽 이름은 바깥 binding을 갱신하지 않고 shadowing(이름 가림)할 수 있다.
- 함수 body의 바깥 이름은 함수의 정의 environment(환경)에서 찾는다. 호출자의 같은 철자 이름과 섞지 않는다.
- 자료의 Safety Checking(안전성 검사)은 실제 마지막 실행 시점만 보는 규칙이 아니다. `def`의 외부 이름은 다음 `val` 전에 준비되어야 한다.
- 세미콜론과 괄호는 expression의 경계를 드러낸다. 줄바꿈 예의 허용 여부는 자료의 문맥으로 읽는다.
- Helper를 `sqrt` 안에 두면 이름의 공개 범위를 줄인다. `ratio`는 각 검사 호출 안에서 재사용하며 모든 반복의 공통 상수가 아니다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Block 결과와 shadowing

`{val t=0; val r={val t=10; t+1}; t+r}`에서 `r`과 최종 값을 구하라. 안쪽 선언은 대입인가? 같은 block의 중복 정의와 비교하라.

<details><summary>해설 보기</summary>

안쪽 마지막 식은 안쪽 `t=10`을 읽어 11이고 그 값이 `r`이 된다. 바깥 마지막 식은 바깥 `t=0`을 읽어 `0+11=11`이다. Block은 마지막 정의의 이름을 자동 반환하지 않고 마지막 식을 계산한다. 안쪽 `val t`는 새 binding으로 바깥 이름을 가릴 뿐 기존 값을 바꾸지 않는다. 자료는 같은 block의 중복 정의를 허용하지 않는 것과 중첩 block의 shadowing을 구분한다.

**채점·확인:** r=11·전체=11과 두 t의 독립성을 설명한다.

</details>

#### 확인 Q02 · 정의 환경과 호출 환경

자료 p.29의 바깥 `t=0`, `f(x)=t+g(x+1)`, `g(y)=y*y`를 사용한다. 안쪽 block은 `t=10`, `s=f(5)`를 정의한 뒤 `s-t`를 반환한다. `s,r`과 바깥 `t+r`를 구하고 `f`·`g` 호출 환경의 부모를 적어라.

<details><summary>해설 보기</summary>

`f(5)`의 새 parameter binding은 `x=5`이고 부모는 f의 정의 환경 E0다. `t`는 0, `g(6)`은 g의 정의 환경 E0를 부모로 하는 새 `y=6` 환경에서 36을 만든다. 안쪽에서 불러도 `s=0+36=36`이다. 안쪽 마지막 `s-t`만 안쪽 t=10을 읽어 `r=26`이고 바깥 결과는 `0+26=26`이다. p.32 번호로 두 번째 f 환경 E4와 g 환경 E5의 부모는 E0이며 호출한 안쪽 block E3가 아니다.

**채점·확인:** 36·26·26뿐 아니라 함수 호출의 E0 부모와 안쪽 식의 E3 lookup을 구분한다.

</details>

#### 확인 Q03 · 비슷한 두 표의 x와 원본 불일치

p.29의 `val x=f(5)`와 p.32의 `val x=f(5)+7`의 차이를 설명하라. 바깥 x가 호출 parameter x를 바꾸는가? p.32 환경 요약의 `g(x)`와 위 코드의 `g(x+1)`는 어떻게 읽어야 하는가?

<details><summary>해설 보기</summary>

`f(5)=36`이므로 바깥 x는 p.29에서 36, p.32에서 43이다. 호출 때 생기는 `x=5`는 별도 parameter binding이며 바깥 x와 다르다. 최종 결과가 둘 다 26이라고 중간 binding까지 같지는 않다. p.32 저장 환경 요약에는 `g(x)`가 있지만 상단 코드와 호출 전개는 `g(x+1)`로 일치한다. 그 코드·전개에 따라 `g(6)=36`으로 읽고 원본 요약의 불일치를 남겨야 한다. 25를 별도 정답으로 만들지 않는다.

**채점·확인:** 36/43/5의 세 역할과 계산 근거·원본 불일치를 명시한다.

</details>

#### 확인 Q04 · 다음 val 경계의 정적 검사

자료의 검사 규칙으로 다음 A·B를 판정하고 val 자체에 적용되는 규칙도 말하라. B의 `val a`는 f를 부르지 않는다.

~~~scala
// A
def f(x: Int) = g(x)
def g(x: Int) = 10
val a = 10
f(10)
// B
def f(x: Int) = g(x)
val a = 10
def g(x: Int) = 10
f(10)
~~~

각 예는 별도 block이다. B의 마지막 호출 때 g가 있다는 사실은 충분한가?

<details><summary>해설 보기</summary>

A는 f가 필요로 하는 g가 다음 val 이전에 있어 자료의 검사를 통과한다. B는 g가 다음 `val a` 경계 뒤에 있으므로 실패한다. a가 f를 부르는지와 무관하게 적용되는 보수적인 정적 규칙이다. `val x=e`에서는 e가 필요로 하는 외부 이름이 그 val 정의 전에 준비되어야 한다. 따라서 `val x=f(10)`을 f와 g 사이에 놓는 배치도 허용되지 않는다. 마지막 실행 경로의 계산 가능성과 자료의 검사 통과는 다른 판단이며 모든 Scala compiler 규칙으로 일반화하지 않는다.

**채점·확인:** A 통과·B 실패, def의 다음-val 경계와 val의 자기 정의 전 경계를 모두 설명한다.

</details>

#### 확인 Q05 · 줄바꿈과 expression 경계

자료 p.33은 `t +` 뒤에서 줄을 바꾸는 경우, `t` 뒤에서 끊고 다음 줄에 `+ s`를 쓰는 경우, `(t`와 `+ s)`로 묶는 경우를 어떻게 구분하는가? 세미콜론의 역할도 적어라.

<details><summary>해설 보기</summary>

자료에서 첫째는 `+`가 오른쪽 operand를 기다리므로 이어지는 식으로 허용한다. 둘째는 `t`가 완성된 식으로 끝난 것으로 읽힐 수 있어 의도한 덧셈의 비허용 예다. 셋째는 괄호가 여러 줄을 한 expression으로 묶어 허용한다. 세미콜론은 같은 줄의 여러 정의·식을 구분한다. 이 판정은 자료의 예이며 모든 버전의 줄바꿈 문법에 대한 일반 판정은 아니다.

**채점·확인:** 세 배치의 차이를 문장 경계로 설명하고 괄호·세미콜론을 구분한다.

</details>

#### 확인 Q06 · sqrt helper 은닉과 ratio의 수명

p.35가 `isGoodEnough`·`improve`·`sqrtIter`를 `sqrt` 내부에 둔 이유와 마지막 `sqrtIter(1,x)`의 역할을 설명하라. Helper의 `x` parameter, `ratio`의 재사용 범위와 경계값 0.999/1.001은 어떻게 되는가?

<details><summary>해설 보기</summary>

외부에는 sqrt라는 인터페이스를 드러내고 내부 보조 이름을 그 block에 제한한다. 마지막 `sqrtIter(1,x)`가 초기 guess 1로 계산을 시작하고 반환값이 sqrt block의 결과가 된다. 충분하면 guess를 반환하고 아니면 `(guess+x/guess)/2`로 개선해 같은 target을 넘기는 계산은 유지된다. Helper의 x parameter도 원본에 남아 있다. `val ratio=guess*guess/x`는 한 검사 호출에서 두 비교에 재사용하지만 새 guess의 다음 검사에서는 새로 구한다. 엄격한 `>0.999`와 `<1.001`이므로 두 경계 모두 실패한다.

**채점·확인:** 공개 범위와 수치 계산의 보존, x 유지, 호출별 ratio, 두 경계를 모두 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 호출 위치에 속지 않는 lookup

**새로 만든 강의 기반 일반 연습.** Block lookup·next-val 검사를 직접 묻는 기출 형식 근거가 없다. 현재 단원의 정의 환경 규칙과 자료의 검사 모델만 사용한다.

~~~scala
{
  val t = 2
  def f(x: Int) = t + g(x)
  def g(y: Int) = y * y
  val r = {
    val t = 9
    f(3) - t
  }
  t + r
}
~~~

결과와 두 t의 lookup 경로를 적어라. 이어 `def f`와 `def g` 사이에 `val marker=0`을 넣으면 자료의 정적 검사를 통과하는지 설명하라.

<details><summary>해설 보기</summary>

f와 g는 t=2인 바깥 환경에서 정의된다. 안쪽 `f(3)`도 `2+g(3)=2+9=11`이다. 안쪽 직접 식은 t=9를 사용하여 `r=11-9=2`이고 바깥 결과는 `2+2=4`다. marker를 사이에 넣으면 f가 필요로 하는 g가 다음 val 뒤로 넘어가 자료의 검사에 실패한다. marker가 f를 호출하지 않고 수치적으로 0이라는 사실은 그 정적 경계를 없애지 않는다.

**채점·확인:** 결과 4와 정의/호출 환경의 차이, marker 삽입 후 검사 실패를 각각 근거로 설명한다.

</details>

### 복습 순서

Q01–Q03을 풀 때 같은 철자의 이름에도 별도 환경 표시를 붙인다. Q04는 코드 실행 전에 다음 val 경계를 먼저 표시하고 Q05–Q06으로 식과 helper의 범위를 확인한다. 마지막으로 P01에서 수치 trace와 정적 검사 판정을 따로 적는다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · Blocks 다음 주제 예고]] / [[courses/principles_of_programming/transcripts/2026-09-08|보정 STT · 55:43]]: p.27 제목의 예고이며 세부 규칙의 강의 확인은 아니다.
- [[courses/principles_of_programming/lectures/2026-09-10-materials-blocks|2026-09-10 Blocks 자료 복습 · 녹음 없음]]: pp.27–35를 선택한 자료 기반 복습이며 그날의 실제 진도를 확정하지 않는다.
- [[courses/principles_of_programming/lectures/2026-09-15-lecture-04|2026-09-15 강의 노트 · 환경·helper 은닉 복습]] / [[courses/principles_of_programming/transcripts/2026-09-15|보정 STT · 01:42–03:06]].
- [Lecture Part 1 · pp.27–35 Block·scope·검사·sqrt 조직](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).

p.32의 환경 요약에는 `g(x)`가 있으나 상단 코드와 trace는 `g(x+1)`이며 후자를 따라 계산한다. p.29의 x=36과 p.32의 x=43도 구분한다. 정적 검사·줄바꿈 판정은 자료의 모델이고 9월 15일 회고가 9월 10일의 녹음을 대신하지 않는다.


---

[[courses/principles_of_programming/units/evaluation-strategies|← 이전: Call-by-value·Call-by-name과 Lazy Evaluation]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/recursion|다음: Newton's Method, Recursion과 Tail Call →]]
