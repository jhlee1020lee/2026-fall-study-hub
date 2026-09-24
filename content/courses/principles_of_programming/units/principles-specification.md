---
title: "프로그래밍 원리, Specification과 Abstraction"
description: "Specification과 검증의 범위를 이해하고 계산·추상화·언어 선택을 구분하는 단원입니다."
course: "principles_of_programming"
unit_id: "principles-specification"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/2026-09-01-lecture-01", "courses/principles_of_programming/lectures/2026-09-03-lecture-02", "courses/principles_of_programming/lectures/2026-09-08-lecture-03", "courses/principles_of_programming/lectures/2026-09-15-lecture-04"]
---

원하는 조건을 정하는 일과 구현이 그 조건을 만족하는지 확인하는 일을 구분합니다. 계산 방식과 프로그램 조직을 비교하며 검증 결과와 설계 품질을 각각 판단해 봅니다.

## Specification(명세): 프로그램이 만족해야 할 조건

프로그램을 만든다는 일에는 서로 다른 판단이 들어 있다. 무엇을 만들 가치가 있는지 고르고, 원하는 동작을 정확히 적고, 구현이 그 조건을 만족하는지 확인해야 한다. 코드 생성이 빨라져도 이 판단들이 자동으로 해결되지는 않는다. 정해진 문제를 완수하는 일과 다음에 풀 문제를 정하는 일도 다르다. 9월 1일 강의는 원리를 배우는 이유를 생성된 결과를 이해하고 방향을 정하는 능력에서 찾았다. [[courses/principles_of_programming/transcripts/2026-09-01|2026-09-01 STT 08:55, 01:08:59]]

Specification은 구현이 만족해야 할 성질을 표현한다. 코드는 그 성질을 달성하는 구체적인 계산이고, specification은 무엇을 달성해야 하는지 판단하는 기준이다. 사람이 코드를 직접 모두 작성하지 않더라도 이 둘의 대응을 읽을 수 있어야 한다.

강의의 로봇 동기를 단순화한 설명용 사례를 생각해 보자. “물체를 A에서 B로 옮긴다”는 조건만 만족하는 동작이 사람과의 충돌까지 피하는 것은 아니다. 이동 성공과 이동 중의 안전을 모두 원한다면 둘 다 조건에 들어 있어야 한다. 여기에 센서가 실제 상태를 얼마나 정확히 나타내는지도 구분해야 한다. **불완전한 specification을 완벽히 만족하는 구현도 실제 목적에는 실패할 수 있다.** 이 사례는 특정 로봇의 검증 결과가 아니라, 조건을 적는 일과 조건을 만족하는 일을 구분하기 위한 예다.

### Proof generation(증명 생성)과 proof checking(증명 검사)

코드를 읽는 사람도 실수할 수 있다. Formal verification(형식 검증)은 구현과 specification의 관계를 수학적으로 다루어 검토를 보완한다. 여기서는 증명을 찾는 일과 주어진 증명이 타당한지 검사하는 일을 나눈다.

프로그램을 $P$, specification을 $S$, 증명을 $π$라고 부르면, 생성기는 “$P$가 $S$를 만족한다”는 근거 $π$를 만들고 proof checker(증명 검사기)는 그 근거가 허용된 규칙에 맞는지 검사한다. 이 기호는 역할을 구분하기 위한 설명용 표기다. 9월 1일 30:05의 C 코드 사례에서도 복잡한 증명 생성과 작은 검사기를 분리하는 생각이 제시되었다. [[courses/principles_of_programming/transcripts/2026-09-01|2026-09-01 STT 30:05, 36:05]]

| 역할 | 확인하는 대상 | 별도로 남는 판단 |
|---|---|---|
| Specification 작성 | 원하는 입력·출력·제약의 표현 | 빠뜨린 요구가 없는가 |
| 구현과 증명 생성 | 주어진 조건을 만족하는 계산과 근거 | 제출된 근거가 타당한가 |
| Proof checker | 정해진 규칙에 따른 증명의 타당성 | 논리·모델·가정과 검사기를 신뢰할 수 있는가 |
| 사람의 검토 | 조건과 실제 목적의 관계 | 현실의 변화가 모델 밖에 있지 않은가 |

선택한 입력 몇 개의 테스트가 성공하면 그 사례에서의 동작을 확인한 것이다. 증명은 명시한 전제와 모델 아래의 성질을 다룬다. 따라서 검사 통과를 “모든 현실 상황에서 아무 오류도 없다”로 읽으면 안 된다. 예를 들어 수학적 정수에 대한 계산과 고정 폭 기계 정수의 계산은 범위가 다르다. 어떤 모델에 대한 주장이었는지를 이해하는 것까지가 검증 결과를 읽는 일이다.

## Monitor(감시 장치): 규칙의 집행과 규칙의 적절성

행동을 만들어 내는 능력과 그 행동을 허용할지 판단하는 능력을 나누면 통제 구조를 설계할 수 있다. 강의의 한 제안은 AI의 명령과 실제 동작 사이에 monitor를 두는 것이다. Monitor는 센서 정보와 명령을 규칙에 대조하고, 위반 동작을 막는다. 다른 제안은 행동을 먼저 코드로 표현하고 안전 조건을 만족한다는 증명을 검사한 다음 실행하는 것이다. 전자는 실행 중 명령을 제한하는 관점이고, 후자는 실행 전에 행동의 근거를 확인하는 관점이다. [[courses/principles_of_programming/transcripts/2026-09-01|2026-09-01 STT 41:29, 46:05–48:23]]

어느 쪽이든 규칙 자체를 잘 정해야 한다. 금지 구역을 빠뜨린 규칙은 위험한 이동을 허용할 수 있다. 반대로 지나치게 넓은 구역을 금지하면 안전하게 가능한 이동도 막힌다. 강의가 말한 보수적 통제의 대가는 이처럼 허용되는 동작 범위의 감소다. 또한 “모든 명령이 monitor를 거친다”는 조건과 센서·구현에 대한 가정 없이 규칙의 효과를 확대해서는 안 된다.

Simulation(시뮬레이션)은 규칙의 빈틈을 찾는 데 도움을 준다. 여러 상황을 만들어 보고 잘못된 결과가 생기면 규칙이나 모델을 고친다. 그러나 유한한 상황을 통과했다는 사실만으로 모든 가능한 상황의 안전성이 증명되지는 않는다. 9월 1일 42:50의 설명은 이런 반례 탐색의 동기를 제공하며, 강사는 49:16에서 전체 구상을 자신의 생각으로 한정했다. [[courses/principles_of_programming/transcripts/2026-09-01|2026-09-01 STT 42:50, 49:16]]

## Abstraction(추상화): 세부 동작을 의미 있는 단위로 묶기

프로그램을 이해하려고 매번 모든 연산을 펼쳐야 한다면 규모가 커질수록 검토가 어렵다. Abstraction은 세부 계산을 의미 있는 단위로 묶어 “어떤 일을 하는가”를 드러낸다. 좋은 이름과 인터페이스가 있으면 내부 동작을 필요한 순간에만 펼쳐 볼 수 있다. 다만 세부를 숨겼다는 사실 자체가 좋은 구조를 보장하지는 않는다. 무엇을 묶었고 어떤 책임을 분리했는지가 중요하다.

증명이 완성되거나 테스트가 통과한 것과 구조가 이해하기 좋은 것도 별개의 성질이다. 강의는 막힐 때마다 국소적으로 탐색하여 증명을 완성하는 능력과 전체 개념을 정리하여 좋은 구조를 만드는 능력을 구분했다. “줄 수를 줄여라”는 요청은 여러 책임을 한 줄에 압축하는 방식으로도 충족할 수 있다. “여러 곳에 반복된 항 계산을 하나의 함수 인자로 모아라”는 요청은 공통 구조와 바뀌는 부분을 구체적으로 지정한다. 후자는 [[courses/principles_of_programming/units/higher-order-functions|Higher-order function으로 공통 계산 구조를 재사용하는 방법]]으로 구체화된다. [[courses/principles_of_programming/transcripts/2026-09-08|2026-09-08 STT 48:24, 51:07–52:06]]

이 강의의 AI에 관한 평가는 당시 경험에 근거한 관찰이다. 여기서 보존할 원리는 특정 도구의 보편적인 능력 판정이 아니라, 기능적 성공과 설계 품질을 따로 판단하고 열린 품질 요구를 구체적인 구조로 바꾸어야 한다는 점이다.

## Imperative Programming(명령형 프로그래밍)과 Functional Programming(함수형 프로그래밍)

같은 계산도 정보를 어디에 두고 다음 단계로 어떻게 넘기는지에 따라 다르게 표현할 수 있다. Imperative Programming은 memory state(메모리 상태)를 읽고 갱신하는 순서를 쓴다. Functional Programming은 function application(함수 적용)을 연결하고 argument(인자)로 값을 전달한다. 다음 두 표기는 1부터 양의 정수 `n`까지의 합을 표현하는 자료의 예다. 왼쪽 방식에 해당하는 첫 코드는 상태 갱신을 보여 주는 의사코드다. [POP M002 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

```text
sum = 0;
i = n;
while (i > 0) {
  sum = sum + i;
  i = i - 1;
}
```

```scala
def sum(n: Int): Int =
  if (n <= 0) 0
  else n + sum(n - 1)
```

`n=3`의 상태 갱신은 `(sum,i)=(0,3)→(3,2)→(5,1)→(6,0)`이다. 함수형 정의는 `sum(3)=3+sum(2)=3+(2+sum(1))=3+(2+(1+0))=6`으로 읽는다. 같은 코드가 반복되지만, 첫 방식에서는 저장된 `sum,i`가 바뀌고 두 번째에서는 다음 호출의 `n`이 바뀐다. 자료와 강의의 다른 예도 같은 관계를 따른다. `sum(10)=55`, `sum(100)=5050`, `sum(123)=7626`이다.

9월 3일 01:02:42–01:03:34의 설명은 이 값 전달 방식을 합에만 쓰는 요령으로 한정하지 않는다. 함수 적용과 재귀를 연결하면 명시적인 공유 상태 갱신 없이도 계산 가능한 모든 계산을 표현할 수 있다는 일반적 계산 모델의 도입이다. 이 자리에서 형식적인 동등성 증명이 제시된 것은 아니다. 또한 “명시적인 memory 갱신 없이 표현한다”와 “실제 컴퓨터의 저장 공간을 사용하지 않는다”는 서로 다른 주장이다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 01:02:42–01:03:34]]

표현력이 충분하다고 모든 프로그램이 종료하거나 자원을 적게 쓰는 것도 아니다. 위 함수형 합은 결과를 기다리는 덧셈을 남긴다. 그 비용은 [[courses/principles_of_programming/units/recursion|recursion과 call stack]]에서 따로 분석한다. 강의가 두 스타일을 목적에 맞게 섞으라고 한 이유도 여기에 있다. 절차와 자원 사용을 드러내는 표현이 유용할 때도 있고, 계산 관계를 드러내는 표현이 이해하기 쉬울 때도 있다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 13:43]] [[courses/principles_of_programming/transcripts/2026-09-15|2026-09-15 STT 23:35]]

## Module(모듈), code reuse(코드 재사용), 언어 선택

계산을 표현하는 방식과 큰 프로그램을 조직하는 방식은 다른 축이다. 여러 함수와 데이터를 의미 있는 module로 묶으면 내부를 매번 읽지 않고 역할을 중심으로 이해할 수 있다. 강의자료는 조직 방식의 도입으로 Object-Oriented Programming(객체 지향 프로그래밍, OOP)과 Type Class Programming(타입 클래스 프로그래밍)을 비교한다. [POP M002 pp.8–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

| 자료의 비교 관점 | 묶는 대상 | Abstraction과 reuse의 조직 |
|---|---|---|
| Object | data + methods | inheritance(상속)를 통해 함께 다룸 |
| Type Class Instance | type + methods | instantiation(인스턴스화)으로 abstraction, composition(합성)으로 reuse를 구분 |

이는 세부 구현을 배우기 전의 개괄이다. Functional Programming을 쓴다는 말과 Type Class로 module을 구성한다는 말은 같은 분류가 아니다. 강의에서 “Type-Oriented”라고 부른 것은 이 Type Class 관점이다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 17:22]]

DRY는 “Don't repeat yourself”라는 재사용의 동기다. 코드를 복사한 뒤 조금씩 바꾸면 공통 부분의 수정도 여러 곳에 흩어진다. 공통 구조를 generalize(일반화)하고 달라지는 부분을 parameter(매개변수)로 만들면, 같은 구조를 서로 다른 인자로 specialize(특수화)할 수 있다. 합·제곱합·세제곱합에서 항을 만드는 함수만 바꾸는 구성이 그 구체적인 예가 된다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 20:05]]

### Scala·Haskell·Rust로 구분해 보는 계산 모델

강의는 Scala를 두 계산 스타일과 두 조직 방식을 함께 비교하고 Java library와 연결할 수 있는 언어로 소개한다. Scala의 메모리 관리는 Garbage Collection(자동 메모리 회수)과 연결한다. 이 선택 이유가 어느 스타일이나 언어의 무조건적인 우월성을 뜻하지는 않는다.

Haskell은 purely functional(순수 함수형) 모델의 비교 대상으로 등장한다. 9월 3일 15:42–16:38에서 설명한 monadic programming(모나드 방식의 프로그래밍)은 그 모델 안에서 작업을 차례로 기술하는 imperative 느낌의 구성을 가능하게 하는 방법이다. 겉으로 작업 순서를 표현한다는 사실과 계산의 바탕 모델을 구분해야 한다. 그런 표기가 가능하다고 공유 memory의 읽기·덮어쓰기를 중심으로 모델을 바꾸었다는 뜻은 아니다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 15:42–16:38]]

Rust의 학습 동기는 익숙한 imperative 문법을 반복하는 데 있지 않고, ownership types(소유권 타입)를 통해 효율적인 저수준 계산과 memory safety(메모리 안전성)를 함께 다루는 데 있다. 강의는 이중 해제, 해제한 메모리의 사용, 범위 밖 접근을 오류의 동기로 들었다. 이어 28:03에서는 오류 처리를 monadic programming과 비슷한 error monad 아이디어에 연결했다. 여기서는 그 연결까지 이해하면 된다. Ownership의 상세 규칙, monad의 법칙과 실제 오류 처리 API는 후속 학습 내용이며, 이 도입만으로 모든 오류가 type checker에서 제거된다고 결론 내릴 수는 없다. [[courses/principles_of_programming/transcripts/2026-09-03|2026-09-03 STT 25:16–28:03]]

## 핵심 정리

- Specification(명세)이 빠뜨린 요구는 proof checking(증명 검사)만으로 보충되지 않는다.
- Monitor(감시 장치)는 규칙을 집행하므로 규칙의 적절성, 센서와 모델의 가정도 확인해야 한다.
- Abstraction(추상화)의 품질은 줄 수나 테스트 통과와 별개다. 공통 구조와 달라지는 책임을 설명해야 한다.
- Imperative Programming(명령형 프로그래밍)은 상태 갱신으로, Functional Programming(함수형 프로그래밍)은 함수 적용과 값 전달로 계산을 표현한다. 표현력·종료·실제 자원 사용은 서로 다른 판단이다.
- 계산 방식과 module(모듈) 조직은 다른 축이다. Haskell의 imperative 느낌의 구성도 순수 함수형 모델 안에서 설명되며, Rust의 ownership·오류 처리 상세 규칙은 이 도입의 범위를 넘는다.

## 확인·연습문제

### 개념과 계산 확인

#### 확인 Q01 · 코드 생성 뒤에도 남는 판단

코드를 빠르게 생성할 수 있을 때도 사람이 문제 선택과 결과 검토를 각각 해야 하는 이유를 설명하라. 정해진 문제의 성공이 다음에 풀 문제의 가치를 보장하는가?

<details><summary>해설 보기</summary>

문제 선택에서는 목적과 제약, 풀 가치가 있는 문제를 정한다. 결과 검토에서는 specification이 그 목적을 담았는지, 구현과 근거가 조건에 맞는지 읽는다. 이미 정해진 목표의 달성은 그 목표 자체의 적절성이나 다음 목표의 가치를 판정하지 않는다. 원리 이해는 생성량을 늘리는 것 외에 이러한 판단과 구체적인 개선 지시를 가능하게 한다.

**채점·확인:** 문제 선택과 구현 검토를 나누고 생성 속도가 두 판단을 대신하지 못하는 이유를 설명한다.

</details>

#### 확인 Q02 · Specification과 proof checker의 보장

구현 `P`, 조건 `S`, 증명 `π`의 역할을 구분하라. `π`가 검사를 통과하면 테스트·사람의 판단·실제 환경에 관한 검토가 모두 불필요해지는가?

<details><summary>해설 보기</summary>

`S`는 만족해야 할 조건, `P`는 실제 계산, `π`는 `P`가 `S`를 만족한다는 근거다. 증명 생성은 그 근거를 찾고 proof checker는 허용된 규칙에 맞는지 검사한다. 테스트는 선택한 사례의 동작을 확인한다. 검사 통과도 명시한 모델·가정 아래의 성질에 관한 것이므로, 빠진 요구나 모델 밖 현실까지 보장하지 않는다. 예컨대 수학적 정수에 관한 증명은 고정 폭 정수의 범위 문제를 저절로 해결하지 않는다.

**채점·확인:** 생성과 검사의 분리, 테스트의 사례 범위, 명세·모델·가정의 한정을 모두 포함한다.

</details>

#### 확인 Q03 · Monitor와 실행 전 검사

실행 중 monitor와 행동 코드의 실행 전 증명 검사는 무엇을 각각 확인하는가? 금지 구역 규칙이 너무 좁거나 넓은 경우 및 simulation의 한계를 설명하라.

<details><summary>해설 보기</summary>

Monitor는 센서 정보와 명령을 규칙에 대조하여 실행 중 위반 동작을 막는다. 다른 방식은 행동을 코드로 표현하고 안전 조건에 대한 증명을 검사한 뒤 실행한다. 금지 범위가 너무 좁으면 위험한 동작을 허용하고, 너무 넓으면 안전한 동작까지 막을 수 있다. 모든 명령이 감시를 거친다는 조건과 센서·구현의 정확성도 필요하다. Simulation은 규칙의 반례 탐색에 유용하지만 유한한 사례 통과가 모든 상황의 안전 증명은 아니다. 이는 강사가 제안한 구상을 분석한 것이며 완성된 안전 시스템의 검증 결과가 아니다.

**채점·확인:** 검사 시점의 차이와 규칙 자체의 검토 필요성, 보수성의 대가를 제시한다.

</details>

#### 확인 Q04 · 짧은 코드와 좋은 Abstraction

테스트를 통과한 코드를 한 줄로 압축했다. 이것만으로 좋은 abstraction인가? 국소적인 성공과 전체 구조의 품질을 구분하고 더 구체적인 개선 요구를 한 가지 제시하라.

<details><summary>해설 보기</summary>

테스트 통과와 줄 수 감소는 각각 확인한 동작과 표현량에 관한 결과다. 서로 다른 책임을 한 줄에 섞거나 반복 개념을 여러 곳에 남겨 두면 이해·수정·재사용은 나아지지 않는다. 예를 들어 '공통 합산 구조는 한 곳에 두고 달라지는 항 계산을 매개변수로 분리하라'는 요구는 무엇을 묶을지 정한다. 막힐 때마다 국소적으로 탐색하여 성공하는 능력과 전체 구조를 설계하는 능력도 별도로 평가해야 한다.

**채점·확인:** 품질을 줄 수로 대체하지 않고 공통 구조 또는 책임 분리를 명시한다.

</details>

#### 확인 Q05 · 같은 합, 다른 정보 전달

1부터 3까지의 합을 구하는 loop의 상태와 `sum(n)=if(n<=0)0 else n+sum(n-1)`의 전개를 적어라. 함수 적용과 값 전달의 일반적 표현력은 저장 공간의 불필요·항상 종료·효율을 보장하는가?

<details><summary>해설 보기</summary>

Loop는 `(sum,i)=(0,3)→(3,2)→(5,1)→(6,0)`으로 저장 상태를 갱신한다. 재귀식은 `sum(3)=3+(2+(1+0))=6`이며 같은 body에 전달하는 `n`이 3,2,1,0으로 바뀐다. 강의의 일반적 표현력 설명은 명시적 공유 상태 갱신 없이 함수 적용·값 전달·재귀로 계산 가능한 계산을 표현할 수 있다는 뜻이다. 실제 저장 공간이 필요 없거나 작성한 모든 함수가 종료한다는 뜻은 아니다. 이 합도 대기 중인 덧셈을 유지하므로 자원은 별도 분석해야 한다. 표현력의 형식적 동등성 증명이 여기서 제시된 것은 아니다.

**채점·확인:** 두 trace, 변하는 정보, 표현력과 종료·저장 비용의 세 구별을 포함한다.

</details>

#### 확인 Q06 · 계산 방식과 module 조직의 두 축

Functional Programming과 Type Class Programming은 같은 분류인가? 자료의 object/type class 비교와 DRY의 generalize·specialize 관계까지 설명하라.

<details><summary>해설 보기</summary>

Functional/imperative는 계산을 표현하는 방식이고 object/type class는 큰 프로그램을 조직하는 방식이다. 자료는 object를 data+methods, type class instance를 type+methods로 대비한다. OOP의 inheritance가 abstraction과 reuse를 함께 다루는 관점에 비해 type class 설명은 instantiation을 통한 abstraction과 composition을 통한 reuse를 나눈다. 이는 도입 비교다. DRY에서는 공통 구조를 generalize하고 바뀌는 부분을 parameter로 받아 서로 다른 인자로 specialize한다. 단순 복사 후 수정과 달리 공통 수정 지점이 한 곳에 모인다.

**채점·확인:** 두 분류 축, 자료의 조직 비교, 공통화와 인자별 특수화를 빠뜨리지 않는다.

</details>

#### 확인 Q07 · Scala·Haskell·Rust의 학습 동기와 범위

(a) Scala의 선택 이유와 메모리 관리 소개, (b) Haskell의 purely functional 모델과 monadic programming, (c) Rust의 ownership 및 error 처리 연결을 설명하라. 이 도입만으로 구현 능력이나 모든 오류 제거가 확보되는가?

<details><summary>해설 보기</summary>

(a) Scala는 두 계산 스타일과 두 조직 방식을 함께 비교하고 Java library와 연결하는 언어로 소개된다. 메모리 관리는 Garbage Collection과 연결된다.

(b) Haskell은 purely functional 모델의 비교 대상이다. 강의의 monadic programming 설명은 그 모델 안에서 작업을 차례로 기술하여 imperative처럼 느껴지는 구성을 만드는 방법이다. 표면적인 작업 순서가 바탕 모델을 공유 memory 덮어쓰기 중심으로 바꾸거나 실제 저장 공간을 없애는 것은 아니다.

(c) Rust는 ownership types로 효율적인 저수준 계산과 memory safety를 함께 다루려는 동기로 등장한다. 이중 해제·해제 후 사용·범위 밖 접근이 오류의 예다. 9월 3일의 error monad 연결은 monadic programming과 비슷한 아이디어로 오류 처리를 표현한다는 예고다. 소유권 이동·대여, 구체 API, monad 법칙이나 전체 예외 체계는 아직 설명되지 않았다.

**채점·확인:** Haskell 비교 자체를 미학습으로 제외하지 않되, 후속 법칙·API와 Rust 상세 규칙을 이미 배웠다고 확대하지 않는다.

</details>

### 적용 연습

#### 연습 P01 · 검증 통과 뒤의 설계 검토

**새로 만든 강의 기반 일반 연습.** 이 주제에 직접 대응하는 기출 형식 근거는 없다. 본문의 specification·monitor·abstraction 구분만 사용하라.

로봇이 물체를 A에서 B로 옮기는 코드가 '도착 성공' 조건의 증명 검사를 통과했다. 개발자는 충돌 검사를 하지 않았고, 중복된 이동 처리도 한 줄로 압축했다. ① 아직 판단해야 할 요구, ② monitor 또는 실행 전 검사에 추가할 조건과 가정, ③ 코드 품질 개선 요구를 제시하라.

<details><summary>해설 보기</summary>

① 도착 조건만으로 이동 중 충돌 회피를 확인할 수 없다. 실제 목적에 안전한 경로가 포함되는지 specification을 다시 검토해야 한다.

② 충돌을 피해야 한다는 조건을 명시하고 monitor가 명령·센서를 그 조건과 대조하게 하거나, 행동 코드가 그 안전 조건을 만족한다는 증명을 실행 전에 검사할 수 있다. 센서가 상태를 제대로 나타내고 검사를 우회하지 않는다는 가정이 필요하다. 지나치게 넓은 금지는 가능한 안전 이동까지 제한할 수 있다.

③ 줄 수보다 공통 이동 처리와 달라지는 입력을 분리하고 책임이 드러나는 인터페이스를 요구한다. 이 설계 제안이 완성된 현실 안전 증명은 아니며, 어떤 조건을 검증하는지까지 적어야 한다.

**채점·확인:** 도착과 안전을 구별하고 검사 방식 하나의 조건·가정을 명시하며 압축 대신 구조 개선을 설명하면 충족한다.

</details>

### 복습 순서

먼저 Q01–Q04를 보고 '요구·근거·집행·구조'를 한 문장씩 구별한 뒤 P01을 푼다. 다음으로 Q05의 두 trace를 직접 쓰고 Q06–Q07에서 계산 모델과 언어 도입의 범위를 다시 확인한다.

## 출처

- [[courses/principles_of_programming/lectures/2026-09-01-lecture-01|2026-09-01 강의 노트 · 원리·명세·검증]] / [[courses/principles_of_programming/transcripts/2026-09-01|보정 STT · 08:55, 30:05, 36:05, 41:29–49:16, 01:08:59]].
- [[courses/principles_of_programming/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 계산 방식·언어 선택]] / [[courses/principles_of_programming/transcripts/2026-09-03|보정 STT · 13:43, 15:42–20:05, 25:16–28:03, 01:02:42–01:03:34]].
- [[courses/principles_of_programming/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · 추상화와 결과 이해]] / [[courses/principles_of_programming/transcripts/2026-09-08|보정 STT · 48:24, 51:07–54:47]].
- [[courses/principles_of_programming/lectures/2026-09-15-lecture-04|2026-09-15 강의 노트 · 재귀의 자원 비용]] / [[courses/principles_of_programming/transcripts/2026-09-15|보정 STT · 23:35]].
- [Lecture Part 1 · pp.6–9 계산 방식·module·언어 비교](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf).

AI 능력과 안전 구조에 관한 평가는 강사의 당시 관찰·제안이다. 불명확한 발화나 보고된 성능 수치를 확정된 사실로 보충하지 않았다. 공개 보정 STT도 완전한 음성 복원이 아니다. 제공된 과거 평가에는 이 단원의 문제 선택·proof checking·monitor·설계 품질을 직접 묻는 근거가 없어 P01은 일반 연습이다.


---

[[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/expressions-functions|다음: Expression·Value·Function과 Evaluation →]]
