---
title: "2026-09-10 · 프로그래밍의 원리 · Blocks 자료 복습"
course: principles_of_programming
date: 2026-09-10
lecture_no: 4
tags:
  - principles_of_programming
  - lecture
  - detailed
lang: ko
concepts: []
review_status: approved
draft: false
note_layout: content_first_v1
source_basis: materials_only
actual_lecture_scope: unconfirmed
source_assets: []
---

Blocks와 이름의 Scope를 자료의 코드 예제로 복습합니다.
9월 10일 녹음이 없어 당일 진도를 확정하지 않고, lecture-part1.pdf p.27–35를 선택한 보충 노트입니다.

## 강의 내용과 설명

### Blocks: 여러 정의를 묶어 하나의 값으로 평가하기

Block(블록)은 `{ ... }` 안에 정의와 표현식을 묶는 구조이며, Scala 자료에서는 Block 자체도 Expression(표현식)이다. 여러 이름을 정의하고 계산하더라도 마지막 Expression의 값이 Block의 결과가 된다. 이번 복습은 **lecture-part1.pdf p.27–35의 Blocks and Name Scoping**을 골라 읽는 자료 기반 보충이다. 9월 10일 녹음·STT가 없으므로 이 페이지들이 그날 실제 진도였다고 확정하지 않는다. [M01 p.27] [M01 p.28]

설명용으로 `{ val a = 2; val b = 3; a + b }`는 5다. 앞의 `val` 두 개가 각각 끝나는 것과 Block 전체의 반환 값을 구별한다. Block 안에 다른 Block을 넣으면 내부에서만 쓰는 이름을 만들 수 있어, 계산의 보조 이름이 바깥 코드에 퍼지지 않게 한다. [M01 p.28]

### Scope of Names: 안쪽 이름과 바깥 이름의 관계

Scope(이름의 유효 범위)는 그 이름을 사용할 수 있는 영역이다. Block 안에서 정의한 이름은 그 Block 안에서만 보인다. 안쪽 Block은 바깥 이름을 사용할 수 있지만 같은 이름을 새로 정의하면 바깥 이름을 Shadow(가리기)한다. 같은 Block 안에서 같은 이름을 중복 정의하는 것과, 안쪽 Block에서 새 이름을 정의하는 것은 다르다. [M01 p.29]

자료의 바깥 `t=0`과 안쪽 `t=10`은 서로 다른 정의다. 안쪽에서 직접 `t`를 읽으면 10이지만 안쪽 Block을 나왔다고 바깥 t가 10으로 바뀌지는 않는다. 설명용 `{ val t=0; val r={ val t=10; t+1 }; t+r }`는 r=11, 최종 결과=11이다. 가림은 바깥 값에 대입하여 변경하는 동작이 아니다. [M01 p.29]

자료의 모델에서는 **동일한 Block 안의 중복 정의는 허용하지 않는다.** 새로 중첩한 Block에서 바깥 이름을 Shadow하는 것은 허용된다. 따라서 이 둘을 “같은 이름이 두 번 나왔다”는 이유만으로 같은 경우로 판단하면 안 된다. [M01 p.29]

### Function과 Environment: 호출 위치보다 정의 위치를 기준으로 읽기

Environment(환경)는 이름과 그 의미를 연결하는 문맥이다. 이 자료의 핵심 규칙은 Function(함수)을 **정의한 Environment**를 기준으로 본문을 평가한다는 것이다. 호출한 곳에 같은 이름의 다른 값이 있어도 그 값을 함수의 자유로운 이름에 자동으로 끼워 넣지 않는다. [M01 p.29]

```scala
{ val t = 0
  def f(x: Int) = t + g(x+1)
  def g(y: Int) = y*y
  val x = f(5)
  val r = {
    val t = 10
    val s = f(5)
    s - t
  }
  t + r
}
```

f는 바깥 t=0이 보이는 곳에서 정의되었다. 따라서 바깥의 f(5)도 안쪽의 f(5)도 `0+g(6)=36`이다. 안쪽 s=36에서 직접 읽는 t는 그 Block의 10이므로 r=26, 바깥 `t+r`는 0+26=26이다. 안쪽 호출의 t=10을 함수 본문의 t에 넣어 46이라고 계산하면 정의 환경 규칙을 놓친 것이다. [M01 p.29]

### def와 val의 순서: 정의를 묶는 것과 즉시 값을 구하는 것

자료 p.28은 def들의 순서는 허용할 수 있지만 val들의 순서는 같게 취급할 수 없다고 지적한다. `def f(x:Int)=g(x)` 뒤에 `def g(x:Int)=10`을 두고 그 뒤에 `val x=f(10)`을 두는 p.30의 첫 예시는 허용 대상이다. 반면 f와 g 사이에 `val x=f(10)`이 오면 g가 준비되기 전에 값을 구하려 하므로 허용하지 않는 예로 제시된다. [M01 p.28] [M01 p.30]

이 차이는 “파일 아래에 이름이 한 번 나타나기만 하면 언제나 괜찮다”는 규칙이 아님을 보여 준다. 함수 정의를 연결할 여유와, 값을 평가하는 지점에서 필요한 이름이 이미 준비되어야 한다는 조건을 함께 읽는다. 다음 Safety Checking 규칙은 이 수업 자료가 채택한 설명 모델이며 모든 Scala 버전의 전체 컴파일러 규칙을 대신하는 설명은 아니다. [M01 p.30] [M01 p.31]

### Safety Checking: 다음 val을 경계로 이름의 준비 상태 확인하기

Safety Checking(안전성 검사)은 아직 정의되지 않은 이름의 사용을 배제하려는 검사다. 자료 p.31의 두 규칙은 `val x=e`의 e에 필요한 이름은 **그 val 이전**, `def x=e`의 e에 필요한 이름은 **다음 val 이전**에 정의되어 있어야 한다는 것이다. 함수 인자처럼 본문 안에서 새로 바인딩되는 이름은 그 해당 범위에서 읽는다. [M01 p.31]

```scala
// 자료에서 통과하는 배치
{ def f(x:Int) = g(x)
  def g(x:Int) = 10
  val a = 10
  f(10)
}

// 자료에서 실패하는 배치
{ def f(x:Int) = g(x)
  val a = 10
  def g(x:Int) = 10
  f(10)
}
```

두 번째의 val a는 f를 호출하지도 않지만, 자료의 검사에서는 이미 f 다음의 val 경계를 넘었다. 그래서 “어차피 f(10)은 g 정의 뒤에서 실행되니 이 검사도 통과한다”는 답은 자료 규칙과 다르다. 첫 번째는 g가 다음 val 전에 정의되어 통과한다. 동작을 머릿속에서 실행하는 것과 주어진 정적 검사 규칙을 적용하는 것을 구별한다. [M01 p.31]

### Evaluation for Blocks: Environment별 값을 표로 추적하기

자료 p.32는 p.29와 닮았지만 바깥 정의가 **`val x=f(5)+7`**이다. 따라서 이 페이지에서 x는 43이다. p.29의 x=36과 혼합하지 않는다. 두 예제 모두 최종 값이 26이라서 중간 값의 차이를 놓치기 쉽다. [M01 p.29] [M01 p.32]

| 평가 위치 | 참고하는 Environment | 결과 |
|---|---|---|
| 바깥 t 정의 | E0 | t=0 |
| 바깥 f(5)+7 | f의 정의 환경 E0와 인자 x=5 | g(6)=36, x=43 |
| 안쪽 t 정의 | E0 안의 새 Block E3 | 안쪽 t=10 |
| 안쪽에서 f(5) 호출 | f의 정의 환경 E0와 새 인자 x=5 | s=36 |
| 안쪽 s-t | E3의 s=36, t=10 | r=26 |
| 바깥 t+r | E0의 t=0, r=26 | 26 |

그림에서 f와 g의 각 호출은 별도의 인자 Environment를 만들지만 바깥 이름을 찾을 기준은 정의 Environment E0다. 함수 인자 x=5와 바깥 val x=43은 이름이 같아도 같은 바인딩이 아니다. 자료의 Environment 요약 일부는 `f=(x)t+g(x)`로 적혀 있으나, 실제 코드와 전개 줄은 `g(x+1)`을 사용한다. 이 노트는 코드와 실제 전개에 맞추어 g(6)=36으로 읽으며 원자료의 생략·불일치를 조용히 고쳐 원본이라고 제시하지 않는다. [M01 p.32]

### Semi-colons and Parenthesis: 줄바꿈이 식을 끊는 위치

Semi-colon(세미콜론) `;`은 같은 줄에 여러 정의·Expression을 구분해 적을 때 사용한다. 한 Expression을 여러 줄에 나눌 때는 Parenthesis(괄호)가 묶음 범위를 분명히 해 준다. 자료 p.33에서는 줄 끝이 `t +`이면 뒤의 s가 이어지는 형태를 허용하고, `t` 뒤에서 줄을 끝낸 다음 새 줄에 `+ s`를 쓰는 형태는 의도한 덧셈 표현으로 허용하지 않는 예로 둔다. [M01 p.33]

```scala
// 자료의 허용 예: 연산자가 앞줄 끝에 남음
val r = { val t=10; val s=square(5); t +
s }

// 자료의 비허용 예
val r = { val t=10; val s=square(5); t
+ s }

// 자료의 허용 예: 괄호로 한 식임을 표시
val r = { val t=10; val s=square(5); (t
+ s) }
```

핵심은 줄 수를 외우는 것이 아니라 내가 의도한 **하나의 Expression**이 어디서 끝나는지 명확히 쓰는 것이다. 위 허용·비허용 표시는 강의자료의 해당 구문 해석 예시를 따른다. 다른 Scala 버전의 모든 줄바꿈·연산자 규칙을 여기서 새로 단정하지 않는다. [M01 p.33]

### sqrt를 Blocks로 정리하기: 보조 정의의 범위와 중복 계산

자료 p.34의 기존 sqrt 코드는 `isGoodEnough`, `improve`, `sqrtIter`를 함께 사용한다. p.35의 개선 예시는 그 보조 함수들을 `sqrt(x:Double)={...}` 안에 넣고 마지막에 `sqrtIter(1,x)`를 호출한다. sqrt 계산에만 필요한 이름을 내부에 두어 외부에서 보조 함수 이름을 따로 다루지 않아도 되게 한다. 이전의 개선식 `(guess+x/guess)/2`와 반복 구조 자체는 유지한다. [M01 p.34] [M01 p.35]

또한 `isGoodEnough` 안에 `val ratio=guess*guess/x`를 두어 같은 식을 두 번 적지 않고 `ratio>0.999 && ratio<1.001`로 사용한다. 경계는 **엄격한 부등식**이므로 ratio가 정확히 0.999 또는 1.001이면 통과하지 않는다. 반복 한 번에서 ratio를 이름 붙여 사용하는 것과, 모든 재귀 호출에서 영원히 같은 ratio를 쓰는 것은 다르다. [M01 p.35]

자료의 개선 코드에도 세 보조 함수의 **x 매개변수는 그대로 남아 있다**. 내부 함수로 옮겼으므로 모든 x 인자를 제거했다고 설명하지 않는다. 마지막 `sqrtIter(1,x)`의 결과가 sqrt Block 전체의 값이 되는 점에서 처음 배운 Block의 Expression 성질로 돌아온다. 이번 복습에서는 자료의 sqrt(2) 같은 양수 사례를 사용하며, 0·음수 등 모든 입력에 대한 종료와 정확성을 증명한 수치 라이브러리라고 확대하지 않는다. [M01 p.35]

## 강의 흐름과 연결

[지난 노트의 함수 평가와 sqrt](./2026-09-08-lecture-03.md)에서 여러 보조 함수를 사용했다면, 이번 보충은 그 정의를 어디에 두고 어떤 이름을 읽는지 정리한다. 선택한 p.27–35가 9월 10일 실제 진도라는 뜻은 아니다.

`Block의 마지막 값 → 이름의 Scope → Function의 정의 Environment → def/val 경계 검사 → Environment별 실행 추적 → sqrt의 내부 정의`

| 학습목표 | 본문에서 설명한 연결 | 회상·적용 |
|---|---|---|
| LO01–LO02 | Block의 값과 중첩 Scope·Shadow | Q1–Q2, P01 |
| LO03·LO06 | 정의 Environment와 실제 값 추적 | Q3·Q6, P01 |
| LO04–LO05 | def/val 순서와 다음 val 경계 | Q4–Q5, P02 |
| LO07 | 줄바꿈과 Parenthesis | Q7, P03 |
| LO08 | sqrt 보조 함수의 내부화 | Q8, P04 |

## 핵심 요약

- Block의 결과는 마지막 Expression의 값이다. 내부 이름을 만드는 것과 바깥 값을 변경하는 것은 다르다.
- Function은 정의 Environment를 사용한다. 호출 위치의 같은 이름을 함수 본문에 대신 넣지 않는다.
- 자료의 Safety Checking은 def의 이름 준비를 **다음 val 이전**에서 검사한다. 실행 시점만 보고 판단하지 않는다.
- p.29의 x=36과 p.32의 x=43은 서로 다른 코드의 결과다. 두 페이지의 최종 값 26만 외우면 중간 차이를 놓친다.
- sqrt의 개선은 보조 정의를 Block 안에 묶고 ratio를 이름 붙이는 것이다. 자료에는 x 매개변수가 남아 있다.

## 회상·연습문제

### 개념 회상

**Q1. Block의 결과는 무엇이며 이름을 안에 묶는 이유는?**

<details><summary>확인 답안</summary>

Block은 Expression이며 마지막 Expression의 값을 준다. `{ val a = 2; val b = 3; a + b }`의 결과는 5다. 내부의 보조 이름을 그 Block 안에서만 사용하도록 범위를 한정한다.

</details>

**Q2. 안쪽 t=10은 바깥 t=0을 바꾸는가? 동일 Block의 중복 정의와 어떻게 다른가?**

<details><summary>확인 답안</summary>

바깥 t를 바꾸지 않고 새로운 안쪽 바인딩으로 가린다. 자료의 모델에서는 동일 Block 안의 중복 정의는 금지하지만, 중첩 Block에서 바깥 이름을 Shadow하는 것은 허용한다. 안쪽을 나온 뒤 바깥 t는 여전히 0이다.

</details>

**Q3. p.29의 안쪽 f(5)가 46이 아니라 36인 이유와 최종 값은?**

<details><summary>확인 답안</summary>

f를 정의한 바깥 환경의 t=0과 g를 사용하므로 0+g(6)=36이다. 안쪽 s=36에서 안쪽 t=10을 빼 r=26이 되고, 바깥 t+r는 0+26=26이다.

</details>

**Q4. p.30에서 def g가 val x=f(10)의 앞 또는 뒤에 올 때 무엇이 다른가?**

<details><summary>확인 답안</summary>

두 def 뒤에 val 평가가 오면 필요한 g가 준비되어 있다. val 평가 뒤에 def g가 오면 값을 구할 때 필요한 이름이 준비되지 않는 예시다. 아래쪽에 정의가 존재하기만 하면 항상 허용되는 규칙은 아니다.

</details>

**Q5. 자료의 Safety Checking에서 val a=10이 f를 호출하지 않아도 중간에 오면 실패하는 이유는?**

<details><summary>확인 답안</summary>

def 본문에 필요한 g가 다음 val 이전에 있어야 한다는 정적 검사 경계 때문이다. val 본문의 이름은 그 val 이전에 정의되어야 한다. 이는 이 수업의 검사 모델이며 Scala 전체 규칙을 대신하는 주장은 아니다.

</details>

**Q6. p.29와 p.32의 x 및 Environment 추적의 차이는?**

<details><summary>확인 답안</summary>

p.29는 x=f(5)=36, p.32는 x=f(5)+7=43이다. 두 경우 모두 안쪽 f(5)는 정의 환경의 t=0으로 계산되어 s=36, r=26, 최종 값=26이다. 함수 인자 x=5와 바깥 val x=43은 다른 바인딩이다.

</details>

**Q7. t 뒤 줄바꿈, t+ 뒤 줄바꿈과 괄호를 사용하는 경우를 설명하라.**

<details><summary>확인 답안</summary>

자료는 t+ 뒤의 줄바꿈을 이어지는 식으로 허용하며 t 뒤에서 끊고 다음 줄에 +s를 쓰는 예는 비허용으로 표시한다. (t와 +s)를 괄호로 묶으면 하나의 식인 범위가 분명하다. 세미콜론은 같은 줄의 정의나 식을 구분한다.

</details>

**Q8. sqrt 개선에서 바뀐 것과 남은 것은? ratio 경계값은 통과하는가?**

<details><summary>확인 답안</summary>

보조 def를 sqrt Block 안에 두고 ratio를 val로 계산하여 재사용한다. 보조 함수들의 x 매개변수와 sqrtIter(1,x)는 남아 있다. ratio가 정확히 0.999 또는 1.001이면 엄격한 부등식 때문에 통과하지 않는다. 마지막 호출 값이 전체 Block의 값이다.

</details>

### 기출 스타일 기반 예상·변형 문제

이 과목은 제공된 기출이 없어 아래 네 문제 모두 강의자료에 근거한 일반 연습이다. 교수의 출제 방식이나 실제 시험 출제를 주장하지 않는다.

#### 연습 P01

**새로 만든 연습. 일반 연습 — 관련 기출 근거 없음.** 제공된 POP 기출이 없으므로 자료의 중첩 Block 평가를 변형했다.

범위: LO01·LO02·LO03·LO06의 Block 값, Shadow, 정의 Environment 추적. [M01 p.28] [M01 p.29] [M01 p.32]
선수 개념: val/def, 기본 산술, Function의 정의 Environment. 현재 본문으로 접근 가능하다.

다음 코드에서 s, r, 최종 값과 두 t의 관계를 설명하라. 같은 Block에 `val t=9`를 하나 더 추가하는 경우도 자료 규칙으로 판단하라.

```scala
{ val t = 2
  def f(x: Int) = t + x*x
  val r = { val t = 7; val s = f(3); s - t }
  t + r
}
```

<details><summary>풀이와 채점 포인트</summary>

f는 바깥 t=2의 Environment에서 정의되었으므로 f(3)=2+9=11이고 s=11이다. 안쪽에서 직접 읽는 t는 7이어서 r=11−7=4다. 마지막 식은 바깥 t+r=2+4=6이다. 안쪽 t는 바깥 t를 바꾸지 않는다. 기존 t와 **동일한 Block**에 또 val t를 정의하면 자료의 중복 정의 금지 규칙에 걸린다.

채점 포인트: s=11과 정의 환경 이유 2점, r=4와 안쪽 t 1점, 최종 값 6과 바깥 t 보존 2점, 동일 Block 중복과 중첩 Shadow 구별 1점. 총 6점.

</details>

#### 연습 P02

**새로 만든 연습. 일반 연습 — 관련 기출 근거 없음.** POP 기출이 없어 자료의 Safety Checking에 배치 변경을 적용한다.

범위: LO04·LO05의 def/val 순서와 다음 val 경계. [M01 p.30] [M01 p.31]
선수 개념: def 본문의 이름과 val 평가 구별. 현재 접근 가능하며 강의자료의 검사 모델만 적용한다.

배치 A와 B의 통과 여부를 판정하고 실패 배치를 최소한으로 고쳐라. val a가 f를 호출하지 않는다는 사실이 판정을 바꾸는가? 수정한 통과 배치에서 마지막 f(2)의 값도 구하라.

```scala
// A
{ def f(x:Int)=g(x); def g(x:Int)=x+1; val a=0; f(2) }
// B
{ def f(x:Int)=g(x); val a=0; def g(x:Int)=x+1; f(2) }
```

<details><summary>풀이와 채점 포인트</summary>

A는 f가 요구하는 g가 다음 val a 이전에 정의되어 통과한다. B는 다음 val a가 g보다 먼저 있어 실패한다. a의 우변이 0이라 f를 호출하지 않아도 자료의 정적 검사 경계는 그대로다. B에서 g 정의를 val a 앞에 옮기면 A와 같은 통과 배치가 된다. 통과 배치의 마지막 f(2)는 3이다.

채점 포인트: A 통과 이유 1점, B 실패와 다음 val 경계 2점, a의 호출 여부와 검사 구별 1점, 올바른 수정 1점·마지막 값 1점. 총 6점.

</details>

#### 연습 P03

**새로 만든 연습. 일반 연습 — 관련 기출 근거 없음.** POP 기출이 없어 자료의 줄바꿈 예시를 숫자 식으로 바꾸었다.

범위: LO07의 Semi-colon과 Parenthesis. [M01 p.33]
선수 개념: 하나의 Expression과 Block의 마지막 값. 현재 접근 가능하다.

자료의 구문 예시를 따라 아래 두 형태 중 의도한 4+6을 분명하게 하나의 식으로 묶는 형태를 고르고, 다른 형태를 괄호를 쓰지 않고 고쳐라. 같은 줄에서 두 val을 나눌 때 쓰는 구분자도 적어라.

```scala
// A
{ val t=4; val s=6; t
+ s }
// B
{ val t=4; val s=6; (t
+ s) }
```

<details><summary>풀이와 채점 포인트</summary>

B는 괄호로 한 Expression임을 표시해 자료의 허용 형태이고 결과는 10이다. A는 자료가 비허용 예로 제시하는 줄바꿈 형태다. `t +`를 첫 줄 끝에 두고 다음 줄을 `s`로 쓰면 자료의 다른 허용 형태가 된다. 같은 줄의 두 val은 `;`로 구분한다. 이는 자료의 예시 규칙이며 모든 Scala 버전의 구문 판정으로 일반화하지 않는다.

채점 포인트: B 선택과 괄호 이유 2점, A를 연산자가 앞줄 끝에 남게 수정 1점, 결과 10 및 세미콜론 1점. 총 4점.

</details>

#### 연습 P04

**새로 만든 연습. 일반 연습 — 관련 기출 근거 없음.** 제공 기출 없이 자료의 sqrt 개선을 설명하고 경계값을 적용하는 문제다.

범위: LO08의 보조 함수 Scope, ratio, Block 마지막 값. [M01 p.34] [M01 p.35]
선수 개념: 이전 sqrt의 improve·sqrtIter, 곱셈·나눗셈·엄격 부등식. 현재 본문과 지난 노트로 접근 가능하다.

① 보조 함수를 sqrt 안으로 옮긴 효과와 x 매개변수의 상태를 설명하라. ② guess=1.5, x=2일 때 ratio와 검사 결과, improve의 다음 guess를 구하라. ③ ratio가 0.999, 1, 1.001일 때 각각 통과하는가? ④ sqrt Block 전체의 값을 결정하는 마지막 호출은?

<details><summary>풀이와 채점 포인트</summary>

① 보조 이름의 Scope를 sqrt 내부에 한정한다. 자료의 개선 코드에도 x 매개변수는 남아 있다. ② ratio=1.5²/2=1.125로 1.001보다 커서 실패한다. 다음 guess=(1.5+2/1.5)/2=17/12≈1.416667이다. ③ 두 경계는 엄격한 부등식이라 실패하고 1만 통과한다. ④ 마지막 `sqrtIter(1,x)`가 돌려주는 값이 Block 전체의 값이다. 이 한 단계 계산은 모든 입력의 종료 증명이 아니다.

채점 포인트: 내부 Scope와 매개변수 보존 2점, ratio·판정·개선값 3점, 세 경계 판정 1점, 마지막 호출의 역할 1점. 총 7점.

</details>

### 다음 복습

먼저 Q1–Q8을 코드 없이 말하고, P01·P02는 이름을 찾는 Environment와 val 경계를 직접 표시하며 푼다. 다음에는 P01의 바깥 t만 바꾸어 함수 결과와 최종 결과가 어떻게 달라지는지 다시 추적한다. 실제 수업 진도가 확인되면 이 보충 범위와 비교해 추가 범위를 정리한다.

## 출처와 검증 상태

M01은 공식 lecture-part1.pdf의 실제 PDF p.27–35다. **9월 10일 녹음·STT는 없고 실제 강의 진도도 미확인**이므로 이 문서는 선택한 자료 범위의 복습 보충이다. 교수 발언이나 당일 강조를 복원하지 않았다.

p.32의 Environment 요약과 실제 코드의 g 인자 차이는 본문에 구분했다. Safety Checking과 줄바꿈 판정은 해당 강의자료의 모델을 따른다. 이 과목의 제공 기출은 없으며 모든 새 문제는 일반 연습이다. 해설의 계산과 이름 참조는 별도로 검산했고, 문서는 사용자 요청으로 공개한 학습노트다.

<details><summary>자료 페이지 바로가기</summary>

M01: [[page_cache/principles_of_programming/lecture-part1/page-027|p.27]], [[page_cache/principles_of_programming/lecture-part1/page-028|p.28]], [[page_cache/principles_of_programming/lecture-part1/page-029|p.29]], [[page_cache/principles_of_programming/lecture-part1/page-030|p.30]], [[page_cache/principles_of_programming/lecture-part1/page-031|p.31]], [[page_cache/principles_of_programming/lecture-part1/page-032|p.32]], [[page_cache/principles_of_programming/lecture-part1/page-033|p.33]], [[page_cache/principles_of_programming/lecture-part1/page-034|p.34]], [[page_cache/principles_of_programming/lecture-part1/page-035|p.35]]

</details>

2026-09-14 공개 안내: 작성 후 별도 의미 검토를 완료한 노트를 사용자 요청으로 공개했다. 발화의 미복원 구간과 자료 기반 보충의 구분은 그대로 유지한다.
