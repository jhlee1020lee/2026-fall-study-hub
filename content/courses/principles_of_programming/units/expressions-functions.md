---
title: "Expression·Value·Function과 Evaluation"
description: "이름 치환·함수 적용·조건 선택을 이용해 expression의 계산과 종료를 추적합니다."
course: "principles_of_programming"
unit_id: "expressions-functions"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-03-lecture-02", "courses/principles_of_programming/lectures/2026-09-08-lecture-03"]
---

Expression이 value가 되는 과정을 이름 치환과 함수 적용 규칙으로 추적합니다. 조건 선택과 재귀를 같은 규칙으로 읽으며 종료와 타입의 차이를 확인합니다.

## Expression(표현식), Value(값), Type(타입)

프로그램을 읽을 때 “무슨 값이 나오는가”만 보면 아직 실행하지 않은 계산과 이미 얻은 결과를 혼동하기 쉽다. Expression은 계산을 기술하고, value는 더 계산할 것이 없는 결과다. `3`은 이미 value인 expression이고, `3 + 4`는 덧셈을 해야 `7`이라는 value가 된다. 모든 expression이 결국 value에 도달하는 것은 아니다. 이 차이는 뒤에서 종료를 논할 때 중요해진다.

자료는 type을 값의 집합으로 소개한다. 이 도입 모델에서 `Boolean`은 두 값 `true`, `false`를 포함한다. `Int`는 32-bit 정수이며 범위가 정해져 있고, `Double`은 64-bit floating-point(부동소수점) 값이다. [POP M002 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| Type | 값의 범위 또는 의미 | 읽을 때 주의할 점 |
|---|---|---|
| `Int` | −2147483648부터 2147483647까지 | 수학적 정수 전체가 아님 |
| `Double` | 64-bit floating-point 값 | 모든 실수를 정확히 나타내는 것은 아님 |
| `Boolean` | `true`, `false` | 조건 선택에 사용 |

Name binding(이름 연결)은 expression에 이름을 붙이는 것이다. 자료의 다음 정의에서 `a`와 `b`는 긴 expression을 다시 쓸 수 있게 한다.

```scala
def a = 1 + (2 + 3)
def b = 3 + a * 4
```

여기서 `def`로 이름을 정의했다는 사실은 이미 결과를 계산하여 저장했다는 뜻이 아니다. 우선 이름과 expression을 연결하고, 그 이름의 값이 필요할 때 expression을 평가한다. 이 구분을 유지해야 이후 `val`과 `def`의 차이도 이해할 수 있다.

## Evaluation(평가): 구조를 따라 expression을 줄이기

Expression을 value로 줄이는 과정이 evaluation이다. Abstract Syntax Tree(AST, 추상 구문 트리)는 expression의 구조를 드러낸다. 예를 들어 `5 + b`의 바깥 구조는 덧셈이고, 두 operand(피연산자)는 `5`와 `b`다. 연산자 종류를 먼저 확인하더라도 덧셈 자체를 먼저 계산할 수는 없다. 피연산자의 값부터 필요하다.

자료의 규칙은 이름을 만나면 연결된 expression으로 바꾸고, primitive operator(기본 연산자)를 만나면 operand를 왼쪽부터 평가한 다음 연산을 적용하는 것이다. 아래는 앞의 두 정의로 `5 + b`를 계산한 과정이다. [POP M002 pp.12–13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```text
5 + b
→ 5 + (3 + a * 4)
→ 5 + (3 + (1 + (2 + 3)) * 4)
→ 5 + (3 + (1 + 5) * 4)
→ 5 + (3 + 6 * 4)
→ 5 + (3 + 24)
→ 5 + 27
→ 32
```

바깥 왼쪽의 `5`는 이미 값이므로 멈춘다. 오른쪽 `b`는 아직 이름이고, 이를 펼치면 다시 `a`의 값이 필요하다. 그 안의 `2 + 3`부터 끝나면서 바깥 연산도 차례로 끝난다. “바깥에서 안쪽으로 노드를 확인한다”와 “안쪽의 필요한 계산이 먼저 완료된다”는 모순이 아니다. 전자는 구조를 읽는 순서이고 후자는 연산의 입력이 준비되는 순서다.

9월 3일 38:01–45:52의 AST 설명도 이 구별을 따른다. 현재 노드가 이름인지 연산자인지를 판별하고, 그 규칙을 필요한 부분식에 반복해서 적용하면 된다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 38:01–45:52]]

## Function application(함수 적용)과 Substitution(치환)

이름이 이미 있는 expression의 약칭으로만 쓰인다면 새로운 입력마다 식을 다시 작성해야 한다. Function(함수)은 parameter(매개변수)를 가진 expression으로, 아직 주어지지 않은 값에 대한 계산을 미리 표현한다.

```scala
def f(x: Int): Int = x + a
```

`x`는 나중에 받을 입력의 이름이다. 반면 `f(10)`의 `10`은 실제로 공급한 argument(인자)다. 9월 3일 50:27에서는 이 점을 이름의 더 본질적인 역할로 설명했다. 이름은 긴 식을 짧게 쓰는 수단인 동시에 미래의 입력을 사용해 계산을 작성하는 수단이다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 50:27]]

현재 사용할 call-by-value(값에 의한 호출) 규칙에서는 argument를 왼쪽부터 value로 만들고, function application을 함수의 body(본문)로 바꾸며, body의 parameter를 실제 argument value로 치환한다. 앞서 정의한 `a`가 `6`으로 평가되는 경우를 보자. [POP M002 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 단계 | 계산 | 얻은 값 |
|---|---|---|
| 안쪽 호출 | `f(3) → 3 + a → 3 + 6` | `9` |
| 바깥 호출의 argument | `f(3) + 1 → 9 + 1` | `10` |
| 바깥 호출 | `f(10) → 10 + a → 10 + 6` | `16` |
| 전체 expression | `5 + 16` | `21` |

따라서 `5 + f(f(3) + 1)`은 `21`이다. 안쪽 `f`가 `9`를 반환했다고 곧바로 바깥 `f`에 `9`를 넣으면 안 된다. 바깥 argument는 `f(3) + 1` 전체이므로 `10`까지 평가해야 한다. 9월 3일 54:12의 설명 역시 argument를 먼저 value로 만든 뒤 body의 parameter를 바꾸는 순서를 강조한다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 54:12]]

이 단순한 치환 예에는 이름 충돌이 없다. 중첩된 범위에서 같은 이름을 다시 정의하는 경우에는 어느 binding을 가리키는지까지 보존해야 하며, 그 문제는 [[courses/principles_of_programming/units/blocks-scope|Block과 environment]]의 정의 환경 규칙으로 이어진다.

## Conditional expression(조건식): 선택한 branch만 평가하기

조건식은 조건에 따라 다른 expression을 결과로 고른다. `if (b) e1 else e2`에서 먼저 `b`를 `Boolean` 값으로 평가한다. `true`이면 `e1`, `false`이면 `e2`만 평가한다. 선택하지 않은 branch(분기)는 평가하지 않는다. 자료는 두 branch가 같은 type인 설정을 사용하며, 전체 조건식도 그 type의 값을 낸다. [POP M002 p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def abs(x: Int) = if (x >= 0) x else -x
```

`abs(-3)`에서는 `-3 >= 0`이 `false`라서 `-(-3)=3`을 얻는다. `abs(0)`에서는 조건이 `true`라서 그대로 `0`을 얻는다. 어느 경우든 두 결과를 미리 계산한 뒤 하나를 선택하는 방식이 아니다. 이 점이 재귀의 종료 조건과 단락 평가를 가능하게 한다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 18:34]]

단, 이 코드를 모든 `Int`에 대해 비음수 결과를 보장하는 수학적 절댓값 구현으로 확대하면 안 된다. `Int`의 최솟값 −2147483648의 양의 대응값 2147483648은 같은 type의 범위 밖이다. 이는 자료의 정수 범위에서 도출한 경계 조건이다. 또한 여기의 같은-type branch 설명은 자료의 도입 규칙이지 모든 Scala 버전의 type inference 전체를 설명하는 규칙은 아니다.

## Recursion(재귀): 같은 body에 다른 입력을 전달하기

반복 계산을 함수로 표현하려면 정의 안에서 그 정의를 다시 사용할 수 있어야 한다. 다음은 자료의 합 함수다. [POP M002 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def sum(n: Int): Int =
  if (n <= 0) 0
  else n + sum(n - 1)
```

재귀에 별도의 마법 같은 평가 규칙이 생기는 것은 아니다. 앞서 배운 function application과 조건 선택을 반복하면 된다.

```text
sum(2)
→ if (2 <= 0) 0 else 2 + sum(2 - 1)
→ 2 + sum(1)
→ 2 + (1 + sum(0))
→ 2 + (1 + 0)
→ 3
```

반복되는 것은 함수 body이고, 달라지는 정보는 `n=2,1,0`이다. `n=0`에서 조건이 `true`가 되면 재귀 호출이 없는 branch `0`을 고른다. 이 base case(기저 경우)에 도달한 뒤 기다리던 덧셈이 끝난다. `sum(0)`을 펼친 식의 다른 branch에 `sum(-1)`이 보이더라도 그 branch를 선택하지 않았으므로 실행하지 않는다. 양의 입력에서 `n`이 하나씩 줄어드는 사실과 base case가 함께 종료의 근거가 된다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 59:47–01:01:42]]

이 정의는 0 이하의 입력에도 `0`을 반환한다. 다만 수학적 전개가 끝난다는 설명과 실제 실행에서 필요한 call stack이나 정수 범위는 별도로 따져야 한다. 여기서는 `2`처럼 작은 입력의 평가 구조를 확인한 것이다.

## Termination(종료)과 Divergence(발산)

평가가 value에 도달하면 termination이고, 계속 expression만 바꾸며 끝나지 않으면 divergence다. 다음 자료의 정의를 펼치면 진행 상황이 바뀌지 않는다. [POP M002 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```scala
def loop: Int = loop
```

```text
loop → loop → loop → …
```

`Int`라고 결과 type을 적어 두었어도 value를 얻는다는 보장은 없다. `sum`에서는 입력이 줄어 base case로 향하지만, `loop`에는 그런 진전이 없다. 9월 3일에 설명한 `g(x)`가 같은 `g(x)`를 다시 호출하는 예도 같은 입력으로 되돌아간다는 문제가 있다.

강의에서 보고된 timeout은 실행 환경이 계산을 중단한 것이지 expression이 정상적인 `Int`를 반환한 것이 아니다. Type의 일관성, 수학적 종료, 실행 환경의 자원 제한을 구분해야 한다. 다음 [[courses/principles_of_programming/units/evaluation-strategies|evaluation strategy]]에서 argument를 “먼저 평가할지, 필요할 때 평가할지” 비교하면 이 차이가 실제로 어떤 호출은 끝나고 어떤 호출은 끝나지 않는 차이로 나타난다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 01:05:32, 01:08:01]]

## 핵심 정리

- Expression(표현식)은 계산을 기술하고 value(값)는 더 계산할 것이 없는 결과다. Name binding(이름 연결)은 이름과 식을 연결한다.
- AST(추상 구문 트리)의 바깥 연산을 알아보는 것과 그 연산을 실행할 준비가 된 것은 다르다. 필요한 operand(피연산자)를 왼쪽부터 평가한다.
- CBV 함수 적용은 argument(인자) 전체를 value로 만든 뒤 parameter(매개변수)를 치환한다.
- 조건식은 선택한 branch(분기)만 평가한다. 재귀에서는 base case(기저 경우)를 고르는 순간 추가 재귀가 멈춘다.
- 결과 type이 `Int`여도 종료가 보장되지는 않는다. Timeout은 정상적인 값 반환이 아니다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · Value·Expression·Type·이름

`3`, `3+4`, `def a=3+4`를 구분하라. 자료의 `Int`·`Double`·`Boolean`은 어떤 값을 나타내며, `def` 선언은 계산 결과를 즉시 저장하는가?

<details><summary>해설 보기</summary>

`3`은 이미 value인 expression이다. `3+4`는 덧셈 뒤 `7`이 되는 expression이다. `def a=3+4`는 `a`에 식을 연결하며 사용할 때 평가한다. 선언만으로 결과를 계산해 저장한 것은 아니다. Type을 값의 집합으로 보는 도입에서 `Int`는 −2147483648..2147483647의 32-bit 정수, `Boolean`은 `true,false`, `Double`은 64-bit floating-point 값이다. `Int`는 수학적 정수 전체가 아니고 `Double`은 모든 실수를 정확히 표현하지 않는다.

**채점·확인:** 값도 식임을 인정하고 정의와 평가를 나누며 세 type의 범위·한정을 적는다.

</details>

#### 확인 Q02 · AST와 primitive operation

`def a=1+(2+3)`, `def b=3+a*4`일 때 `5+b`를 평가하라. 바깥 덧셈 노드를 먼저 확인하면서도 그 덧셈을 마지막에 계산하는 이유는?

<details><summary>해설 보기</summary>

바깥 왼쪽 `5`는 값이지만 `b`는 아직 이름이다. `b`를 `3+a*4`로 펼치고 `a`를 `1+(2+3)`으로 바꾼다. 필요한 안쪽 연산부터 `2+3=5`, `1+5=6`, `6*4=24`, `3+24=27`을 얻은 뒤 `5+27=32`다. 연산자 노드의 종류를 확인하는 것은 적용할 규칙을 고르는 일이다. 실제 연산에는 값인 operand가 필요하므로 부분식 계산을 먼저 끝낸다.

**채점·확인:** 32라는 결과 외에 두 이름 치환과 피연산자의 준비 순서를 보인다.

</details>

#### 확인 Q03 · 미래의 입력과 중첩 함수 적용

`a=6`, `def f(x: Int): Int=x+a`라 하자. Parameter와 argument를 구분하고 `5+f(f(3)+1)`을 CBV로 전개하라. 이름은 긴 식의 약칭 외에 어떤 역할을 하는가?

<details><summary>해설 보기</summary>

정의의 `x`는 아직 받지 않은 입력의 이름인 parameter이고 `f(3)`의 `3`은 실제 argument다. `f(3)→3+6=9`, 바깥 argument 전체 `f(3)+1→10`, `f(10)→10+6=16`, 마지막으로 `5+16=21`이다. 안쪽 결과 9를 바깥 함수에 바로 넣으면 `+1`을 누락한다. Parameter 이름은 미래에 받을 값을 사용한 계산을 미리 기술하게 한다.

**채점·확인:** 9→10→16→21의 구분과 parameter·argument의 역할을 설명한다.

</details>

#### 확인 Q04 · 조건식의 선택과 정수 경계

`def abs(x: Int)=if(x>=0)x else -x`에서 `abs(-3)`과 `abs(0)`를 구하라. 두 branch를 미리 평가하는가? 자료의 type 조건과 `Int` 최솟값의 한계도 설명하라.

<details><summary>해설 보기</summary>

`-3>=0`은 `false`이므로 `-(-3)=3`만 계산한다. `0>=0`은 `true`이므로 `0`을 고른다. 조건은 `Boolean`으로 평가하고 선택하지 않은 branch는 계산하지 않는다. 자료의 도입은 두 branch가 같은 type을 갖는 설정이며 이 경우 결과는 `Int`다. 최솟값 −2147483648의 양수 2147483648은 `Int` 범위 밖이므로 모든 `Int`에 대한 비음수 절댓값 보장으로 확대할 수 없다.

**채점·확인:** 각 branch 선택, 미선택 branch 생략, 같은-type 규칙의 자료 범위와 최솟값 한계를 포함한다.

</details>

#### 확인 Q05 · 재귀와 base case

`sum(n)=if(n<=0)0 else n+sum(n-1)`에서 `sum(2)`를 전개하라. 무엇이 반복되고 무엇이 바뀌는가? `sum(0)`의 다른 branch에 있는 호출도 평가하는가?

<details><summary>해설 보기</summary>

`sum(2)→2+sum(1)→2+(1+sum(0))→2+(1+0)→3`이다. 같은 body와 적용 규칙을 반복하고 `n`은 2,1,0으로 바뀐다. 양의 `n`이 감소하여 0에 도달하면 재귀 호출이 없는 branch `0`을 고른다. 그때 미선택 branch의 `sum(-1)`은 실행하지 않는다. 처음부터 `n<=0`이면 바로 0이며, 작은 입력의 종료 전개와 실제 큰 입력의 stack·정수 범위는 별개다.

**채점·확인:** 감소와 base case를 함께 제시하고 미선택 재귀를 실행하지 않는다.

</details>

#### 확인 Q06 · 타입과 종료의 차이

`def loop: Int=loop`는 왜 `Int` 값을 주지 못하는가? 같은 입력으로 자신을 다시 부르는 함수나 timeout 보고를 종료와 연결하여 설명하라.

<details><summary>해설 보기</summary>

`loop→loop→loop→…`로 식을 바꾸어도 진행이 없다. 같은 입력을 그대로 자기 호출에 전달하고 base case로 향하지 않는 함수도 이와 같은 문제가 있다. `Int`라는 type은 결과의 종류를 기술하지만 값에 도달하는 감소 과정의 증명은 아니다. Timeout이나 자원 오류는 실행 환경의 중단이며 정상적인 `Int` value 반환이 아니다.

**채점·확인:** 같은 식으로 돌아가는 원인과 type·정상 종료·환경 중단을 구분한다.

</details>

### 적용 연습

#### 연습 P01 · 미선택 재귀와 중첩 입력 추적

**새로 만든 강의 기반 일반 연습.** 기본 치환·조건 선택을 직접 묻는 기출 형식 근거가 없어 일반 연습으로 제시한다. CBV와 작은 `Int` 계산만 사용한다.

~~~scala
def loop: Int = loop
def f(x: Int): Int = x + 2
def walk(n: Int): Int =
  if (n <= 0) 0 else f(n) + walk(n - 1)
~~~

① `f(walk(2)+1)`의 값을 trace로 구하라. ② `if(true) f(1) else loop`와 `f(loop)`가 각각 종료하는지 설명하라.

<details><summary>해설 보기</summary>

① `walk(2)=f(2)+walk(1)=4+(f(1)+walk(0))=4+(3+0)=7`이다. 바깥 argument 전체는 `7+1=8`이며 `f(8)=10`이다. `walk`는 `n`을 줄여 0에서 멈춘다.

② 조건식은 `true` branch만 골라 `f(1)=3`을 낸다. `loop`가 사라진 것이 아니라 선택되지 않았다. `f(loop)`는 argument를 먼저 value로 만들려다 발산하므로 body의 `x+2`를 시작하지 못한다.

**채점·확인:** 중간값 7과 argument 8을 구분하고, branch 선택 이전/이후의 요구 차이를 설명한다.

</details>

### 복습 순서

Q01–Q03을 닫힌 해설 상태에서 풀어 '식→인자 값→body→결과'를 적는다. 이어 Q04–Q06의 종료 판단을 문장으로 쓰고 P01에서 실제 평가되는 호출에만 표시한다. 평가 시점이 헷갈리면 [[courses/principles_of_programming/units/evaluation-strategies|평가 전략]]으로 이어 간다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 식·함수·재귀]] / [[courses/principles_of_programming/transcripts/2026-09-03|보정 STT · 31:07, 34:00, 38:01–45:52, 50:27, 54:12, 59:47–01:08:01]].
- [[courses/principles_of_programming/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · 조건식과 앞선 내용 복습]] / [[courses/principles_of_programming/transcripts/2026-09-08|보정 STT · 18:34]].
- [Lecture Part 1 · pp.12–16 식·함수·재귀, p.21 조건식](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).

AST 판서 원본은 제공되지 않았으며 trace는 자료의 규칙을 적용한 계산이다. 조건식의 같은-type 설명은 해당 자료의 도입 모델로 읽는다. 보정 STT의 불명확한 발화와 timeout 보고를 새 실행 결과로 해석하지 않는다.


---

[[courses/principles_of_programming/units/principles-specification|← 이전: 프로그래밍 원리, Specification과 Abstraction]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/evaluation-strategies|다음: Call-by-value·Call-by-name과 Lazy Evaluation →]]
