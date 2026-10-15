---
title: "Class·재귀 자료·Inheritance와 Overriding · 강의 정리 · 날짜 미확인"
course: "principles_of_programming"
lang: "ko"
term: "2026_Fall"
course_confidence: "materials_and_transcript_matched"
date: null
lecture_date: null
date_confidence: "unknown"
source_kind: "lecture_note"
note_layout: "content_first_v1"
reader_layout: "content_first"
review_status: "approved"
draft: false
cssclasses: ["plain-document"]
source_mode: "text_only_practical"
audio_verified: false
verbatim_complete: false
source_assets: ["lecture-part1.pdf", "lecture-part2.pdf"]
source_basis: "privacy_reviewed_corrected_text_and_official_materials"
---

## 강의 내용과 설명

### Class와 Factory: 같은 멤버를 만드는 두 생성 절차

Class(클래스)는 타입 이름과 그 타입의 값을 구성하는 절차를 함께 제공한다. 이를 이해하려면 먼저 Structural Type(구조적 타입)을 반환하는 Factory(생성 함수)를 살펴볼 수 있다. 아래는 Part 2 PDF p.16의 코드다. [Part 2, PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-016)

```text
import reflect.Selectable.reflectiveSelectable

type gee_type = {val name:String; val age: Int; def getPP(): String}

def gee_fun(_name: String, _age: Int) : gee_type = {
  if (!(_age >= 0 && _age < 200))
    throw new Exception("Out of range")
  object tmp {
    val name : String = _name
    val age : Int = _age
    def getPP() : String = name + " of age " + age.toString()
  }
  tmp
}

val gee : gee_type = gee_fun("David Jones",25)
gee.getPP()
```

`gee_type`은 `name:String`, `age:Int`, `getPP():String`을 요구하는 구조의 Type Alias(타입 별칭)다. 별칭을 선언하는 것 자체가 값을 생성하지는 않는다. `gee_fun`은 이름과 나이를 받아 검사하고, 정상 경로에서는 그 구조를 갖춘 객체 `tmp`를 구성하여 반환한다. 이처럼 입력에 따라 값을 구성하는 함수를 Factory라고 이해할 수 있다. `_name`과 `_age`는 인자 이름이며 객체 멤버 `name`과 `age`에 각각 들어간다. `getPP()`는 인자가 없는 메서드 호출이고, `age.toString()`은 정수를 문자열로 바꾸어 문자열 연결에 사용한다. 강의도 구조적 값을 만드는 함수에서 출발해 클래스의 차이를 설명한다. [STT 03:06] [STT 05:36]

Part 2 PDF p.17은 같은 검사와 멤버를 클래스 본문에 둔다. 다음은 해당 자료 코드다. [Part 2, PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-017)

```text
class foo_type(_name: String, _age: Int) {
  if (!(_age >= 0 && _age < 200))
    throw new Exception("Out of range")
  val name : String = _name
  val age : Int = _age
  def getPP() : String = name + " of age " + age.toString()
}

val foo : foo_type = new foo_type("David Jones",25)
foo.getPP()
```

`new foo_type("David Jones",25)`는 생성 절차에 두 인자를 공급한다. 검사를 통과하면 `foo_type`의 객체가 만들어진다. `foo.name`과 `foo.age`로 멤버를 읽고, `foo.getPP()`로 메서드를 호출한다. 자료의 문자열 식을 손으로 전개하면 `"David Jones" + " of age " + "25"`이므로 결과 문자열은 `David Jones of age 25`다. 인쇄된 코드의 계산이다.

두 본문이 비슷하더라도 결과 타입의 소속 기준은 다르다. `gee_type`은 요구한 멤버 구조를 갖춘 값을 받아들이는 별칭이다. `foo_type`은 클래스 선언이 정한 Nominal Type(명목 타입)이다. 클래스 정의는 타입 이름을 도입하고, 인자를 받아 그 타입의 값을 구성하는 절차도 제공한다. 생성된 객체라는 값, 그 값의 타입, 타입의 이름, 생성자를 호출하는 식을 구분해야 한다. 강의의 “이 타입의 이름을 주는 거예요”라는 설명도 이 차이를 짚는다. [STT 08:32]

### Structural 사용과 Nominal 소속의 방향

Subtype(하위 타입) 관계 `S <: T`는 `T`가 요구하는 사용에 `S`의 값을 공급할 수 있는 방향을 표시한다. 여기서는 `foo_type`의 객체가 `gee_type`이 요구하는 세 멤버를 모두 제공한다. 따라서 자료는 `foo_type <: gee_type`을 인정한다. 반대의 `gee_type <: foo_type` 관계에는 취소 표시가 있다. 두 방향을 모두 허용하는 그림으로 읽으면 안 된다. [Part 2, PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-018) [STT 25:16]

자료의 다음 두 대입은 이 비대칭을 보여 준다.

```text
val v1 : gee_type = foo
val v2 : foo_type = gee  // type error
```

첫 줄은 클래스 객체 `foo`를 그 객체가 제공하는 구조의 관점으로 사용한다. 둘째 줄은 구조적 타입의 값 `gee`를 특정 클래스의 값이라고 요구한다. 구조가 같다는 정보만으로 그 클래스의 생성·상속 관계에 속한다는 근거가 생기지는 않는다. `gee_fun`이 검사도 하고 같은 문자열 메서드도 만든다는 사실은 이 명목적 소속을 대신하지 못한다.

같은 페이지의 자료 코드는 더 작은 구조만 요구할 수도 있음을 보여 준다.

```text
def greeting(r:{val name:String}) =
  "Hi " + r.name + ", How are you?"

greeting(foo)
```

`greeting`에 필요한 것은 `name:String`이라는 멤버다. 이 요구를 충족하는 클래스 객체도 받을 수 있으며, 다른 방식으로 만든 값도 그 구조를 제공하면 받을 수 있다. 이 함수의 매개변수 타입을 특정 클래스 이름으로 바꾸면 요구가 달라진다. 공통 멤버만 필요한 코드와 특정 명목 타입의 계약까지 필요로 하는 코드는 서로 다른 타입을 선택할 이유가 있다. 멤버를 실제로 읽을 때 참조가 정상 객체라는 전제도 필요하다. 구조적 사용 가능성이 `null`의 역참조를 안전하게 만드는 것은 아니다.

### Age Invariant: 검사 경로와 타입 전체의 보장

Invariant(불변조건)는 추상화의 값에 대해 유지하려는 성질이다. 나이 예제에서는 정상적으로 생성된 객체에 대해 `0 <= age < 200`을 유지하려 한다. `age:Int`라는 선언과 이 범위 조건은 서로 다른 정보다. 전자는 필드의 타입이며, 후자는 그 정수에 추가한 조건이다. [Part 2, PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-019)

자료의 검사는 `!(_age >= 0 && _age < 200)`일 때 예외를 던진다. 따라서 두 부등식을 모두 만족해야 정상 생성 경로로 간다. 설명용 경계값을 대입하면 다음과 같다.

- `_age=0`: `0>=0`과 `0<200`이 모두 참이므로 범위 안이다.
- `_age=199`: `199>=0`과 `199<200`이 모두 참이므로 범위 안이다.
- `_age=-1`: 첫 조건이 거짓이므로 전체의 부정은 참이다. 예외 경로로 간다.
- `_age=200`: 둘째 조건이 거짓이므로 역시 예외 경로로 간다.

이 판정은 인쇄된 부등식에 대한 설명용 전개다. `gee_fun`과 `new foo_type` 모두 동일한 검사를 하므로 이 두 절차가 정상 반환한 값은 검사 조건을 통과했다. 그러나 모든 `gee_type` 값이 `gee_fun`을 거쳤다는 뜻은 아니다. 다른 코드가 `name:String`, `age:Int`, `getPP():String`의 구조만 맞추어 값을 구성할 수도 있다. 구조 선언에는 그 값이 반드시 이 Factory를 호출해야 한다는 조건이 없다.

이 점을 드러내는 설명용 반례는 `age=-1`인 정수 멤버와 나머지 요구 멤버를 갖춘 구조적 값이다. 그 값은 나이 범위에는 어긋나지만 `age:Int`라는 요구에는 어긋나지 않는다. 이는 타입 선언이 요구하는 것과 추가 범위 조건의 차이를 보여 주는 논리적 예다. 자료 p.19의 구조적 타입에서는 성질을 가정할 수 없다는 대비도 필드의 선언된 타입까지 무효라는 뜻으로 받아들이면 안 된다. 구조만으로 추가적인 업무 조건이 성립한다고 가정할 수 없다는 뜻이다.

클래스는 명목적 소속과 생성 경로를 관리하여 이런 추가 조건을 유지할 기반을 준다. 그렇지만 클래스 이름만으로 임의의 Invariant가 증명되지는 않는다. 검사 자체가 올바르고, 허용된 생성 경로가 조건을 지키며, 변경과 상속이 그 조건을 깨뜨리지 않아야 한다. `null`과 정상 생성 객체도 구분해야 한다. 강의의 Introduction 통제와 성질 유지 논의는 이러한 조건 아래에서 이해해야 한다. Subtype 관계 자체를 곧바로 집합의 부분집합이나 의미적 조건의 증명과 동일시할 수는 없다. [STT 20:31] [STT 22:26]

### Inheritance와 Behavioural Contract

부모 타입을 요구하는 위치에 자식 객체를 넣을 수 있다는 정적 관계와, 부모의 사용자가 믿는 행동 약속을 지킨다는 사실은 구분해야 한다. Behavioural Contract(행동 계약)는 객체를 사용하는 코드가 무엇을 가정할 수 있는지 정한다. 나이가 일정 범위라는 Invariant나 `getPP()`의 문자열 의미가 추상화의 약속이라면 자식도 그 약속을 존중해야 한다. 강의는 상속받는 쪽이 유지해야 할 성질을 깨뜨리면 추상화가 무너진다고 설명한다. [STT 18:36] [STT 19:34]

예를 들어 사용자가 `getPP()`를 “이름, 공백을 포함한 of age, 나이의 문자열”이라고 약속받았다고 하자. 자식이 그 의미를 전혀 다르게 바꾸면 반환 타입이 여전히 `String`이어도 사용자가 의존한 의미는 깨질 수 있다. 반대로 계약이 문자열 형식의 변경을 허용했다면 그 범위 안의 변경은 허용된다. 이 두 경우는 메서드의 타입만 보아서는 구분되지 않는다.

따라서 `extends`로 명목 관계를 선언한 사실이 모든 의미적 약속을 자동 검사한다는 결론은 나오지 않는다. 부모를 정의할 때는 유지할 성질과 자식이 바꾸어도 되는 부분을 분명히 해야 한다. 강의는 생성 이후 성질을 다시 확인하는 절차를 둘 수도 있다는 생각을 제시하지만, 구체적인 검사 API나 완성된 구현을 제공하지는 않는다. 여기서 배울 것은 특정 검사용 함수의 사용법이 아니라 생성·상속·변경 전체에서 계약을 유지해야 하는 이유다. [STT 23:21] [STT 24:17]

### Recursive ADT를 읽는 기초: Product, Sum, Pattern Matching

Introduction(도입)은 타입의 값을 만드는 방법이고, Elimination(제거)은 이미 주어진 값을 사용하는 방법이다. 객체를 만들고 멤버를 읽는 구분도 이 관점으로 볼 수 있다. 함수는 `(x:T)=>e`로 만들고 `f(v)`로 사용한다. Tuple(튜플)은 여러 성분을 함께 구성하며 위치로 성분을 꺼낸다. Record(레코드)는 이름으로 멤버를 사용한다. Type Alias는 이런 타입 표현에 별칭을 주는 것으로, 별칭을 만드는 것과 생성 절차를 정의하는 것은 구분한다. 이 절의 자료형 기초는 Part 1의 자료에 근거한 선수 설명이다. 해당 페이지 전체의 구두 강의를 복원한 범위가 아니다. [Part 1, PDF p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-068) [Part 1, PDF p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071)

Product(곱)는 여러 성분을 **함께** 요구한다. Sum(합)은 여러 대안 **중 하나**를 생성자 이름으로 구분한다. Part 1의 `Attr` 예에서 `DOB of Int * Int * Int`는 세 정수를 함께 담는 곱이다. `Name`, `Age`, `DOB`, `Height` 중 하나의 생성자로 값을 만드는 전체 선택은 합이다. 여기서 `*`와 `|`는 자료형의 구성을 설명하는 표기이며 정수 곱셈이나 조건식의 논리 연산으로 읽지 않는다. [Part 1, PDF p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-073)

Recursive ADT(재귀 대수적 자료형)는 구성 성분에 자기 타입이 다시 나타나는 자료형이다. 다음은 Part 1 PDF p.74의 정의 표기다.

```text
IList = INil
|  ICons of Int * IList
```

`INil`은 빈 리스트라는 기저 경우다. `ICons`는 정수 하나와 나머지 `IList`를 함께 담는다. 전체는 빈 경우와 비어 있지 않은 경우의 합이고, `ICons` 안은 정수와 꼬리의 곱이다. `ICons(2,ICons(1,INil()))`에서는 첫 원소가 2, 다음이 1이며 마지막 `INil()`에서 끝난다. 타입 이름이 다시 등장한다는 것과 실제 값에 포인터 순환이 있다는 것은 같은 주장이 아니다. 이 식은 유한하게 중첩한 두 원소 값이다. [Part 1, PDF p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-074)

Pattern Matching(패턴 매칭)은 어떤 생성자로 만들어졌는지를 나누어 사용하는 Elimination이다. 다음은 자료 p.79의 함수다. 필요한 빈 경우와 재귀 경우를 읽는 데 사용한다. [Part 1, PDF p.78](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-078) [Part 1, PDF p.79](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-079)

```text
def length(xs: IList) : Int =
  xs match {
    case INil() => 0
    case ICons(x, tl) => 1 + length(tl)
  }
```

두 원소 값에 대한 설명용 계산은 다음과 같다.

```text
length(ICons(2,ICons(1,INil())))
= 1 + length(ICons(1,INil()))
= 1 + (1 + length(INil()))
= 1 + (1 + 0)
= 2
```

각 단계에서 꼬리 `tl`은 현재 리스트보다 노드가 하나 적다. 유한한 리스트에 대해 이 크기가 감소하고 기저 경우에서 멈춘다는 것이 이 계산의 종료 근거다. 재귀 타입이나 재귀 함수라는 이름만으로 임의의 계산이 반드시 종료하는 것은 아니다.

설명용으로 `Int`를 사용해 정확한 길이·노드 수를 세는 계산은 구조상의 개수가 `0` 이상 `2^31−1` 이하이고 각 재귀 호출이 정상적으로 값을 반환한다는 전제로 다룬다. 유한성만으로 수치 범위나 실행 자원의 충분성이 보장되지는 않는다. 트리의 노드 수는 왼쪽·오른쪽 위치마다 세는 구조상의 개수로 정한다.

`Option[T]`는 값이 없는 `None`과 값 `x:T`가 들어 있는 `Some(x)`를 구분한다. `Some(3)`은 `Option[Int]`, `Some("abc")`는 `Option[String]`의 예이며, `None`은 두 문맥 모두에서 부재를 나타낼 수 있다. 따라서 `Option[T]` 자체에 `T`의 멤버가 있다고 가정하면 안 된다. `Some`인 경우 내부의 `T` 값을 얻은 뒤 그 멤버를 사용한다. [Part 1, PDF p.98](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-098)

`MyList[A]`의 `A`는 값 매개변수가 아니라 타입 매개변수다. `A=Int`와 `A=String`에서는 같은 재귀 구조에 다른 성분 타입을 사용한다. 이것이 Parametric Polymorphism(매개변수 다형성)의 관점이다. 임의의 `A`에 `name` 같은 특정 필드가 있다고 가정하는 것과는 다르다. 뒤에서 부모 타입의 자리에 자식 객체를 넣는 Subtype Polymorphism과도 구분한다. [Part 1, PDF p.90](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-090) [Part 1, PDF p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092)

### Recursive Class: MyList 노드와 YourList의 빈 경우

Part 2 PDF p.20은 클래스 이름을 필드 타입 안에 다시 써서 재귀 구조를 표현한다. 아래는 자료 코드다. [Part 2, PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-020)

```text
class MyList[A](v: A, nxt: Option[MyList[A]]) {
  val value : A = v
  val next : Option[MyList[A]] = nxt
}

type YourList[A] = Option[MyList[A]]

val t : YourList[Int] =
  Some(new MyList(3,Some(new MyList(4,None))))
val s : YourList[Int] = None
```

`MyList[A]` 하나는 값이 있는 **노드**다. `value:A`와 `next:Option[MyList[A]]`를 함께 갖는 곱이며, `next`의 `Option`은 다음 노드가 없는 `None`과 있는 `Some`의 합이다. 이름 `MyList`를 정의하면서 그 이름을 안쪽 타입에 다시 사용할 수 있다는 것이 자기 참조다. 이 예의 단순 필드 나열과 이름을 설명하는 데서 모든 구조적 타입 체계가 재귀를 표현할 수 없다는 불가능성 정리를 끌어낼 수는 없다. [STT 28:17] [STT 30:16]

정수 노드를 설명용 기호 `INode`로 적으면 그 구성은 `Int * Option[INode]`라고 볼 수 있다. 이는 `MyList[Int]`의 값·다음 노드 구조를 나타내는 설명용 수식이며, 별도 Scala 선언이나 후속 자료에 있는 동명의 `INode` 함수 구현을 뜻하지 않는다. 이 노드가 없는 전체 리스트까지 나타내려면 바깥에 다시 `Option`이 필요하다. 그래서 자료가 `YourList[A]=Option[MyList[A]]`라는 별칭을 둔다.

`t`를 바깥에서 안쪽으로 읽으면 네 단계가 구분된다. 바깥 `Some`은 첫 노드가 있다는 뜻이다. 그 노드의 `value`는 3이다. 그 노드의 `next`가 `Some`이므로 다음 노드가 있고 그 값은 4다. 둘째 노드의 `next=None`에서 끝난다. 노드 수는 2다. `s=None`은 첫 노드부터 없는 빈 리스트로 노드 수가 0이다.

노드의 끝을 나타내는 안쪽 `None`과 전체 리스트가 비었다는 바깥 `None`은 같은 부재 생성자를 서로 다른 위치에 사용한 것이다. `MyList[A]` 자체를 빈 리스트와 동일시하거나, `value`와 `next`라는 두 필드를 `value.next`라는 한 접근 경로로 합치면 이 구조를 잘못 읽게 된다. `None`은 유한한 값을 구성할 기저 경우를 주며, 유한한 값의 다음 부분을 따라가는 처리에 종료 근거를 마련한다. 이것이 모든 가능한 재귀 값과 처리 함수의 종료 보장은 아니다. [STT 30:16] [STT 32:02]

### Null과 Option: 멤버 접근에 필요한 근거

`next`에서 `Option`을 빼고 다음 노드를 반드시 `MyList[A]`로 받는다고 가정하자. 정상 노드를 하나 만들려면 다음 노드를 주고, 그 노드를 만들려면 또 다음 노드를 주어야 한다. 별도 기저 표현이 없으면 이 방식만으로 유한 리스트의 끝을 지정할 수 없다. 강의는 `null`을 끝 표시로 사용하는 경우와 `Option`으로 빈 경우를 명시하는 경우를 비교한다. [STT 34:56] [STT 35:53]

`null`은 실제 노드의 필드 정보를 제공하지 않는다. `null`인 참조에서 노드 멤버를 읽으려 하면 정상 값을 얻지 못하고 예외가 발생할 수 있다. 그러므로 `null` 기반 표현에서는 멤버를 사용하기 전에 현재 참조가 실제 노드인지 확인해야 한다. 첫 노드가 `null`이 아니라는 사실은 그 노드의 `next`도 `null`이 아니라는 뜻이 아니다. 다음 참조를 따라갈 때마다 그 위치에서 다시 필요한 검사를 해야 한다. [STT 38:34]

반면 `s:Option[MyList[A]]`에서 `s`는 노드가 아니라 부재 또는 노드를 담은 값이다. 다음은 자료의 Option과 Pattern Matching을 결합한 **설명용 예제**다.

```text
def firstValue[A](s: Option[MyList[A]]): Option[A] =
  s match {
    case None => None
    case Some(node) => Some(node.value)
  }
```

빈 경우에는 `node.value`를 읽을 노드가 없다. `Some(node)`인 경우에 내부의 `node:MyList[A]`를 얻고 그 노드의 `value`를 읽는다. 따라서 전체 `Option`에 바로 `.value`를 요구하는 대신 경우를 나누어야 한다. 또한 `node.next`는 다시 `Option[MyList[A]]`이므로 다음 원소를 읽으려면 그 값의 경우도 다시 나눈다. 현재 노드의 존재와 다음 노드의 존재는 서로 다른 정보다. [STT 43:16]

이 설명용 함수는 `Some` 안에 정상 노드가 들어 있다는 전제를 둔다. `Option`이라고 해서 잘못된 내부 값, 별도로 허용된 `null`, 부적절한 강제 추출까지 모두 방지하는 것은 아니다. 명시적인 빈 경우가 필요한 분기를 타입에 드러내 준다는 점이 핵심이다.

Part 2 p.21은 자료의 언어 모델에서 `null`을 클래스·구조적 타입의 특수 원소로 설명하고 Scala에서 그 사용을 권장하지 않는다고 적는다. 이를 모든 Scala 설정과 모든 타입의 영구 규칙으로 확대하지 않는다. Java에 `Option`이나 합을 표현할 수단이 전혀 없다는 주장도 이 예로 증명되지 않는다. `null` 역참조 위험이 있다는 사실만으로 언어 전체의 Type Safety를 부정할 수 없으며, 자료의 “Efficient” 표현을 일반적인 성능 우열이나 측정값으로 받아들여서도 안 된다. [Part 2, PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-021)

### Argument Members: Parameter와 Val Member

Constructor Parameter(생성자 매개변수)는 생성할 때 받은 입력이고, Member(멤버)는 만들어진 객체를 통해 사용하는 구성 요소다. Part 2 p.22의 긴 `MyList`에서는 `v`와 `nxt`를 받고, 별도의 `val value=v`, `val next=nxt`로 읽기 멤버를 정의한다. 다음은 자료가 그 정의를 줄여 쓴 두 형태다. 같은 클래스 정의를 대체하는 표현들이다. [Part 2, PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-022)

```text
class MyList[A](val value:A, val next:Option[MyList[A]]) {
}
```

```text
class MyList[A](val value:A, val next:Option[MyList[A]])
```

`val value:A`는 인자를 받으면서 그 이름의 읽기 멤버도 선언한다. `val next`도 마찬가지다. 클래스 본문에 추가할 내용이 없으면 자료의 마지막 형태처럼 빈 중괄호를 생략한다. 긴 정의와 짧은 정의 모두 값 하나와 선택적인 다음 노드라는 정보를 같은 타입으로 담는다. 클래스 본문에 다른 멤버를 추가하는 것도 가능하다. [STT 44:52]

이 축약에서 실제로 제시된 것은 `val`이다. 생성자의 괄호 안에 이름이 등장한다는 이유만으로 모든 매개변수가 외부에서 읽을 수 있는 공개 필드라고 해석해서는 안 된다. 뒤의 상속 예제에서 단순 `x:Int`는 이 `val value:A`와 구분해야 한다. 받은 값을 멤버에 저장한다는 설명 역시 `next`가 가리키는 재귀 구조 전체를 Deep Copy한다는 뜻은 아니다.

### Companion Object와 Apply: 노드 생성과 Some 감싸기

Part 2 p.23은 클래스 옆에 같은 이름의 `object MyList`를 두고 `apply`를 정의한다. 다음은 해당 자료 코드다. [Part 2, PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-023)

```text
class MyList[A](val value:A, val next:Option[MyList[A]])

object MyList {
  def apply[A](v: A, nxt: Option[MyList[A]]) =
    new MyList(v,nxt)
}

type YourList[A] = Option[MyList[A]]

object YourList {
  def apply[A](v: A, nxt: Option[MyList[A]]) =
    Some(new MyList(v,nxt))
}

val t0 = None
val t1 = Some(new MyList(3,Some(MyList(4,None))))
val t2 = YourList(3,(YourList(4,None)))
```

타입 자리의 `MyList[A]`는 클래스의 타입 이름이고, 값 자리에서 `apply`를 호출하는 `MyList`는 객체다. 동명이라는 사실만으로 `object MyList` 자체가 리스트 노드 인스턴스가 되는 것은 아니다. 클래스와 같은 이름의 객체를 Companion Object(동반 객체)라고 부르며, 클래스와 관련된 생성 함수 등을 여기에 둘 수 있다. 여기서 타입의 이름, 객체라는 값, 객체의 메서드 `apply`, `new`로 생성된 노드라는 값을 구분한다. `YourList`는 타입 자리에서는 별칭이고 값 자리에서는 별도로 선언한 객체라는 점도 같다. [STT 47:29] [STT 50:27]

자료의 `MyList(4,None)`은 `MyList.apply(4,None)`라는 호출 표기로 읽고, 그 본문에 따라 `new MyList(4,None)`이라는 노드를 만든다. 반면 `YourList(4,None)`은 `YourList.apply(4,None)`를 호출하고 `Some(new MyList(4,None))`을 만든다. 뒤의 결과에는 바깥 `Some`이 하나 더 있다. 그래서 이를 모두 “new만 생략했다”라고 설명하면 반환 구조의 차이를 놓친다. 어떤 `apply`가 무엇을 만드는지는 실제 본문을 읽어야 한다. 이 예의 `apply`는 생성자를 실제로 사용하며, 모든 `apply`가 새 객체를 만들거나 특정 결과를 반환하는 것은 아니다. [STT 51:20]

`t1`과 `t2`의 관계는 설명용으로 다음과 같이 전개할 수 있다.

```text
t1의 구성식
Some(new MyList(3,Some(MyList(4,None))))
→ Some(new MyList(3,Some(new MyList(4,None))))

t2의 구성식
YourList(3,YourList(4,None))
→ YourList(3,Some(new MyList(4,None)))
→ Some(new MyList(3,Some(new MyList(4,None))))
```

두 식 모두 값 3 다음에 4가 있고 둘째 노드의 `next=None`인 같은 두 원소 **구조**를 나타낸다. 이는 별도로 생성한 객체들의 참조 동일성이나 클래스의 자동 구조적 동등성까지 주장하는 말이 아니다. `t0=None`은 첫 노드가 없는 빈 리스트다. 따라서 `t0`를 `t1`·`t2`와 같은 두 원소 값이라고 묶으면 안 된다. 이 설명은 자료에 직접 적힌 수동 `object/apply`에 근거하며 다른 Scala 버전이나 Case Class의 자동 생성 규칙을 가정하지 않는다.

### Binary Tree: Internal Node의 세 성분과 빈 트리

Binary Tree(이진트리)의 노드에는 값, 왼쪽 자식, 오른쪽 자식이 함께 필요하다. Part 2 p.24는 그 구조를 다음과 같이 제시한다. 이때 곱의 세 성분 중 자식 성분에는 `Option`이 들어 있다. [Part 2, PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-024)

```text
MyTree[A] =
  (value: A) *
  (left: Option[MyTree[A]]) *
  (right: Option[MyTree[A]])
```

이는 Product인 노드 안에 빈 경우와 있는 경우의 Sum을 두고, 그 있는 경우가 다시 같은 노드 타입을 참조하는 구조다. Part 1의 자료형 표기 `BTree = Leaf | Node of Int * BTree * BTree`도 빈 경우와 값·두 하위 트리를 담는 경우를 구분한다. 이 ADT의 `Leaf`는 값을 담지 않는 빈 경우다. 일상적으로 “자식 없는 노드”라고 부르는 값 있는 잎 노드와 같은 뜻이라고 가정하면 안 된다. Option 기반 표현에서는 `None`이 빈 경우에 대응하고 `Some(node)`가 값과 두 자식 성분을 가진 경우에 대응한다. 이는 자료를 연결한 선수 설명이다. [Part 1, PDF p.76](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076)

다음은 Part 2 p.25의 자료 코드다. [Part 2, PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-025)

```text
class MyTree[A](v: A,
                lt: Option[MyTree[A]],
                rt: Option[MyTree[A]]) {
  val value = v
  val left = lt
  val right = rt
}

type YourTree[A] = Option[MyTree[A]]

val t0 : YourTree[Int] = None
val t1 : YourTree[Int] = Some(new MyTree(3,None,None))
val t2 : YourTree[Int] =
  Some(new MyTree(3,Some(new MyTree(4,None,None)),None))
```

`MyTree[A]`는 노드 하나이며 `YourTree[A]`는 전체가 비어 있을 수도 있는 트리다. `t0`에는 노드가 없다. `t1`에는 값 3의 노드 하나가 있고 그 왼쪽과 오른쪽이 모두 비어 있다. `t2`는 루트 값이 3이고, 왼쪽에 값 4의 노드가 있으며 오른쪽은 비어 있다. 값 4의 노드도 두 자식이 모두 비어 있다. 이 경우 트리 노드는 모두 2개다. 리스트 예제와 같은 `t0,t1,t2` 철자를 쓰지만 여기서는 별도의 트리 값들이다. 특히 트리의 `t1`과 `t2`는 서로 다른 구조다.

각 자식의 `Option`은 그 방향에 노드가 없는 경우를 나타낸다. 바깥 `Option`은 루트조차 없는 전체 빈 트리를 나타낸다. 바깥을 없애면 `MyTree[A]`만으로는 정상적인 빈 전체 트리를 나타내지 못하고, 자식의 `Option`을 없애면 정상 노드만을 계속 요구하여 끝내는 표현이 별도로 필요해진다. 강의가 기저 경우의 필요성을 강조하는 이유다. [STT 54:25] [STT 58:33]

Part 2 p.26은 같은 정보를 `val` 매개변수와 `YourTree.apply`로 줄여 쓴다. 다음은 긴 정의를 대체하는 자료 코드다. [Part 2, PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-026)

```text
class MyTree[A](val value : A,
                val left : Option[MyTree[A]],
                val right : Option[MyTree[A]])

type YourTree[A] = Option[MyTree[A]]

object YourTree {
  def apply[A](v:A, lt:Option[MyTree[A]], rt:Option[MyTree[A]]) =
    Some(new MyTree(v,lt,rt))
}

val t0: YourTree[Int] = None
val t1: YourTree[Int] = YourTree(3,None,None)
val t2: YourTree[Int] = YourTree(3,YourTree(4,None,None),None)
```

안쪽 `YourTree(4,None,None)`을 전개하면 `Some(new MyTree(4,None,None))`이다. 이 값을 왼쪽 인자에 넣고 바깥 호출을 전개하면 `Some(new MyTree(3,Some(new MyTree(4,None,None)),None))`이다. 따라서 짧은 `t2`는 긴 `t2`와 같은 루트·왼쪽·오른쪽 구조를 만든다. 빈 트리 `t0`, 한 노드 `t1`, 두 노드 `t2`의 구분은 축약 후에도 보존된다.

자기 참조와 곱에 `Option`의 합을 더하여 이런 ADT 형태를 표현할 수 있다는 것이 이 예의 내용이다. 단일 클래스의 필드를 나열하는 문법과 선택 대안을 직접 나열하는 ADT 표기가 다르다고 해서 클래스·상속으로 합을 인코딩할 수 없다는 결론은 나오지 않는다. 또한 기저 경우는 유한 트리를 만들 수 있게 하지만, 임의의 재귀 연산에 대한 종료 증명은 여전히 별도다. 이 표현만으로 범주론적 Duality의 정식 조건이나 모든 자료형의 표현 가능성을 증명한 것도 아니다. [STT 01:00:20]

### Inheritance: 부모 인자 전달과 추가 멤버의 계산

Part 2 p.28의 `foo_type`과 `gee_type`은 앞의 이름·나이 예제와 별개의 정의다. 여기의 `gee_type`은 구조적 별칭이 아니라 `foo_type`을 상속하는 클래스다. 같은 철자만 보고 두 예제를 합치면 명목 관계와 계산을 모두 잘못 읽게 된다. 아래는 p.28의 자료 코드다. [Part 2, PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-028)

```text
class foo_type(x: Int, y: Int) {
  val a : Int = x
  def b : Int = a + y
  def f(z: Int) : Int = b + y + z
}

class gee_type(x: Int) extends foo_type(x+1,x+2) {
  val c : Int = f(x) + b
}

(new gee_type(30)).c
```

`extends foo_type(x+1,x+2)`는 `gee_type <: foo_type`이라는 명목 관계를 선언하면서 부모 부분의 초기화에 줄 인자도 지정한다. 자식 생성자의 `x`를 부모의 `x`에 같은 값으로 그대로 넘길 필요는 없다. 자식의 입력, 부모 생성자의 입력, 메서드 호출의 입력은 각기 다른 Binding(이름 결합)이다. 강의도 부모 생성자를 호출하되 인자가 일대일로 같은 값일 필요는 없다고 설명한다. [STT 01:03:09]

`new gee_type(30)`에 대한 설명용 손계산은 다음 순서다.

1. 자식 생성자의 `x=30`이다. 부모의 첫 인자는 `30+1=31`, 둘째 인자는 `30+2=32`다.
2. 부모 생성자의 결합은 `x=31,y=32`가 된다. `val a=x`이므로 `a=31`이다.
3. 상속된 `b`를 사용하면 `a+y=31+32=63`을 계산한다.
4. 자식의 `c`를 초기화할 때 쓰는 `f(x)`에서 인자는 자식의 `x=30`이다. 따라서 부모에서 정의한 `f`의 인자 `z=30`이 된다.
5. `f(30)=b+y+30=63+32+30=125`다.
6. `c=f(30)+b=125+63=188`이다.

여기서 부모의 `a`가 30이라고 놓으면 부모에게 전달한 첫 인자의 변환을 빠뜨린다. 또 `f(x)`에서 `x`를 부모의 31로 바꾸면 자식 본문에 있는 결합을 잘못 읽은 것이다. 부모 메서드의 `y`는 부모에 전달된 32이며, 자식의 `x`와 별개다.

`a`와 `c`는 `val` 멤버이고, `b`와 `f`는 `def` 메서드다. `b`는 인자 목록 없이 사용할 때 본문을 계산하며, `f`는 `z`를 받아 계산한다. 위 수치가 일정한 이 예에서도 `b`를 생성 시 한 번 저장한 `val` 초기값과 동일시하면 안 된다. 단순 생성자 매개변수 `x,y`를 자동으로 공개 `val` 필드라고 읽어서도 안 된다. 이 예는 `a,b,f`를 재정의하지 않고 `c`만 추가한다. 부모 생성자를 사용했다는 사실만으로 임의의 하위 클래스가 모든 행동 계약을 유지한다는 증명이 되지는 않는다. [STT 01:04:04]

### Parent View의 Abstraction과 구현 Reuse

같은 p.28에는 다음 자료 코드가 있다.

```text
def test(f: foo_type) = f.a + f.b

test(new foo_type(10,20))
test(new gee_type(30))
```

이 함수의 매개변수 이름 `f`는 전달된 **객체**를 뜻한다. 클래스 안의 메서드 이름 `f`와 철자만 같다. 이 `test`는 객체의 `a`와 `b`를 사용할 뿐 메서드 `f(z)`를 호출하지 않는다. [Part 2, PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-028)

첫 호출은 부모 객체를 만든다. 입력이 `x=10,y=20`이므로 `a=10`, `b=10+20=30`이고, `test`의 결과는 `10+30=40`이다. 둘째 호출의 자식 객체는 앞서 전개한 대로 `a=31,b=63`이므로 `test`는 `31+63=94`를 계산한다. 자식의 `c=188`은 이 합에 들어가지 않는다.

`gee_type <: foo_type`이므로 자식 객체를 부모 타입의 매개변수에 공급할 수 있다. 이 Parent View(부모 관점)의 Abstraction(추상화)은 구체 객체가 더 많은 멤버를 갖더라도 현재 사용에 필요한 부모의 관점으로 이해하는 것이다. `test`는 `c`를 요구하지 않는다. 자식에 `c`가 추가되었다고 부모 타입의 인터페이스에도 `c`가 추가된 것은 아니다. [STT 01:06:30]

Reuse(재사용)는 자식이 부모의 생성 절차와 `a,b,f` 구현을 이용한다는 점이다. 자식 클래스마다 같은 코드를 복사해 다시 쓰는 대신 이미 정의한 부모 구현을 물려받는다. 추상화는 사용자가 의존할 관점을 정하는 일이고, 재사용은 구현을 다시 이용하는 일이다. 두 효과가 함께 나타날 수 있지만, 구현을 재사용했다는 이유만으로 좋은 추상화가 자동으로 생기지는 않는다. 사용자가 의존하는 계약이 유지되는지도 살펴야 한다. 강의의 재사용 논의는 이 동기와 한계를 함께 다룬다. 일부 동작만 바꾸면서 나머지 구현을 사용하려는 요구가 Overriding으로 이어진다. [STT 01:07:26] [STT 01:08:16]

### Dynamic Overriding: B를 바꾸면 상속된 F의 결과도 달라진다

Overriding(재정의)은 상속한 메서드의 구현을 자식에서 바꾸는 것이다. Part 2 p.29는 p.28과 **다른** 프로그램을 제시한다. 부모의 `a=x`는 같지만, `b`는 0을 주고 `f(z)`는 `b*z`를 계산한다. 아래는 p.29의 자료 코드다. [Part 2, PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-029)

```text
class foo_type(x: Int, y: Int) {
  val a : Int = x
  def b : Int = 0
  def f(z: Int) : Int = b * z
}

class gee_type(x: Int) extends foo_type(x+1,x+2) {
  override def b = 10
  // or, override def b = super.b + 10
  val c : Int = f(x) + b
}

(new gee_type(30)).c

def test(v: foo_type) =
  println(v.f(42))

test(new foo_type(1,2))
test(new gee_type(0))
```

자식은 `b`만 재정의한다. `f`의 본문은 상속된 그대로다. 그러나 그 본문에서 사용하는 `b`는 실제로 메서드 호출이므로 현재 수신 객체의 재정의한 구현을 선택한다. 이를 Dynamic Dispatch(동적 메서드 선택)의 관점으로 읽는다. 상속된 `f`를 자식 객체에서 부르면 그 안에서도 같은 자식 객체의 `b`를 사용한다. 부모에 쓰인 `b`의 초기 본문이 0이라는 이유만으로 `f` 안의 `b`가 상수 0으로 고정되는 것이 아니다. 강의의 “F는 오버라이드 안 했어요 … B만 오버라이드 했어요”라는 질문이 바로 이 간접 효과를 겨냥한다. [STT 01:13:52]

`new gee_type(30)`의 `c`를 손으로 전개하면 다음과 같다.

1. 부모 생성자 인자는 여전히 31과 32다. 따라서 `a=31`이다.
2. 이 객체에서 `b`를 사용하면 자식의 `override def b=10`을 선택한다.
3. `c`의 `f(x)`는 `f(30)`이다. 상속된 본문 `b*z`에서 `b=10,z=30`이므로 `f(30)=10*30=300`이다.
4. `c=f(30)+b=300+10=310`이다.

p.28의 188과 다른 것은 같은 입력 30을 잘못 계산해서가 아니다. p.28은 `b=a+y,f(z)=b+y+z`이고 p.29는 `b=0,f(z)=b*z`인 별개 정의이기 때문이다.

p.29의 `test`도 p.28의 덧셈 함수와 다르다. 여기서는 `v.f(42)`를 계산하여 출력하도록 쓰였다. 부모 객체 `new foo_type(1,2)`는 `b=0`이므로 `f(42)=0*42=0`이다. 따라서 자료 코드상 `println`에 전달되는 값은 0이다.

자식 객체 `new gee_type(0)`에서는 자식 입력이 0이므로 부모 생성자 인자는 1과 2다. 하지만 `test`가 호출하는 메서드의 인자는 0이 아니라 **42**다. 이 객체의 `b=10`을 사용하므로 `v.f(42)=10*42=420`이고, `println`에 전달되는 값은 420이다. 매개변수 `v`의 정적 타입이 `foo_type`이어도 실제 수신 객체의 `b` 선택은 사라지지 않는다. 이 수치는 코드에 따른 계산이다.

주석의 대안 `override def b=super.b+10`은 부모 구현을 명시적으로 사용한다. 이 예에서는 부모의 `b`가 0이므로 `0+10=10`을 얻어 같은 수치를 준다. 다른 부모 본문에서도 항상 같은 효과가 난다는 규칙은 아니다.

계약에 따라 이 변화의 의미도 달라진다. 부모의 현재 구현 `b=0`을 “모든 하위 타입도 항상 0을 반환한다”라는 약속으로 사용했다면 자식의 변경은 그 가정을 깨뜨린다. 반면 계약이 `b`의 재정의를 허용하고 `f`가 현재 객체의 `b`를 사용한다고 정했다면 이 간접 변화는 허용된 확장이다. 재정의한 메서드뿐 아니라 그것을 호출하는 상속 메서드까지 검토해야 하는 이유다. [STT 01:11:58]

여기서 분석한 대상은 `def b`와 `def f`의 메서드 선택이다. 이를 `val` 필드의 즉시 초기화나 생성자 도중 가상 호출의 모든 규칙으로 확대하지 않는다. 메서드의 인자 타입을 바꾸어 다른 호출 형태를 추가하는 Overloading(오버로딩)과도 구분한다. 후속 p.30의 `f(String)` 상세 예제를 현재 구두 강의 범위에 포함할 근거는 없다. 또한 강의의 구현 비용에 관한 추측은 특정 Compiler의 구현 방식이나 성능 수치의 검증이 아니다. 이 예에서 확인하는 것은 `b`에 의존하는 `f`의 계산 변화이지, 프로그램의 모든 관련 동작이 반드시 바뀐다는 정리가 아니다. [STT 01:14:42] [STT 01:15:40]

## 회상·연습문제

### Class의 생성과 행동 계약

#### 회상 Q01 Factory와 Class의 입력·검사·결과

Part 2 pp.16–17의 `gee_fun`과 `new foo_type`을 비교하라.

1. 두 생성 절차의 입력 타입, 정상 생성 전에 검사하는 조건, 범위를 벗어났을 때의 경로를 적어라.
2. 정상 반환한 값의 세 멤버와 각 타입을 적고, `name`을 읽는 것과 `getPP()`를 호출하는 것을 구분하라. `age.toString()`의 역할도 설명하라.
3. 두 절차가 같은 멤버를 만들더라도 `gee_type`과 `foo_type`의 소속 기준이 다른 이유를 설명하라. `type` 별칭 선언 자체가 객체를 생성하는지도 답하라.

<details><summary>정답</summary>

두 절차 모두 `_name:String`과 `_age:Int`를 받는다. `_age >= 0 && _age < 200`을 만족해야 정상 생성한다. 그 조건의 부정이 참이면 `Exception("Out of range")`를 던지므로 정상 객체를 반환하는 경로와 구별해야 한다.

`gee_fun`은 검사 뒤 `object tmp`를 구성하여 반환한다. 클래스는 검사와 멤버 정의를 클래스 본문에 두고 `new foo_type(...)`으로 생성 절차를 호출한다. 두 정상 결과는 다음 멤버를 제공한다.

| 멤버 | 타입·사용 |
|---|---|
| `name` | `String`인 읽기 멤버, `v.name`으로 읽음 |
| `age` | `Int`인 읽기 멤버, `v.age`로 읽음 |
| `getPP` | `def getPP():String`, `v.getPP()`로 호출 |

`getPP()`의 본문은 `name + " of age " + age.toString()`이다. `age.toString()`은 정수를 문자열로 바꾸어 문자열 연결에 사용한다. 예를 들어 자료의 이름과 나이를 대입한 손계산은 `David Jones of age 25`다.

`gee_type`은 필요한 구조를 적은 Type Alias다. 그 구조를 충족하는 다른 값도 받아들이며, 별칭 선언만으로 객체가 생기지는 않는다. `foo_type`은 클래스 선언이 도입한 Nominal Type으로, 그 클래스와 허용된 상속 관계에 대한 소속이 필요하다. 생성 본문의 유사성이 타입 소속 기준까지 같게 만들지는 않는다. [STT 08:32]

확인할 점: 입력과 객체 멤버, 구조적 별칭과 명목 타입, 예외 경로와 정상 결과를 각각 구분해야 한다.

</details>

#### 회상 Q02 구조적 사용과 명목 소속의 방향

여기서 `gee_type`은 Part 2 p.16의 구조적 별칭이고, `foo:foo_type`은 p.17의 정상 객체, `gee:gee_type`은 `gee_fun`의 정상 결과다. 참조는 `null`이 아니라고 하자.

다음 각 사용이 p.18에서 허용되는지와 그 근거를 설명하라.

~~~text
val v1: gee_type = foo
val v2: foo_type = gee
greeting(foo)
greeting(gee)
~~~

`greeting(r:{val name:String})`은 `r.name`만 읽는다. 또한 별도로 만든 값이 `name:String`, `age:Int`, `getPP():String`을 모두 갖추었다면 그것만으로 `foo_type`의 값이 되는지 답하라. 두 Subtype 방향을 명시하라.

<details><summary>정답</summary>

`v1` 대입은 허용된다. `foo_type` 객체는 `gee_type`이 요구하는 세 멤버를 제공하므로 `foo_type <: gee_type` 방향의 구조적 사용이 가능하다.

`v2` 대입은 자료에서 `type error`다. `gee`가 같은 멤버를 갖추고 같은 검사까지 거쳤어도 그 사실만으로 `foo_type`이라는 명목 타입에 속하지는 않는다. 따라서 `gee_type <: foo_type`은 이 예에서 성립하지 않는다. p.18의 역방향 관계는 취소된 관계다.

`greeting(foo)`와 `greeting(gee)`는 모두 필요한 `name:String`을 제공하므로 허용된다. `greeting`의 요구는 특정 클래스의 소속이나 나이 범위가 아니라 해당 필드를 읽을 수 있는 구조다. 별도의 값도 이 구조를 제공하면 같은 함수에 전달할 수 있다. 그러나 그 값이 세 멤버를 모두 제공해도 별개의 명목 소속까지 자동으로 얻지는 않는다. [STT 25:16]

확인할 점: 구조적 요구를 충족하는 방향을 명목적 소속의 역방향으로 뒤집지 않아야 한다. 이 `gee_type`은 p.28의 동명 상속 클래스와 별개다.

</details>

#### 회상 Q03 검사된 결과와 타입 전체의 Invariant

Part 2 pp.16–19의 `0 <= age < 200`을 대상으로 답하라.

1. `_age=-1, 0, 199, 200`을 두 부등식에 대입하여 `gee_fun`과 `new foo_type`의 정상 생성 여부를 판정하라.
2. “`gee_fun`이 검사하므로 모든 `gee_type` 값의 `age`도 이 범위다”라는 주장에 구조적 반례를 제시하라. 실행 코드 대신 멤버와 값을 명시해도 된다.
3. 클래스 이름이 있다는 사실만으로 이 Invariant가 증명되는지 설명하고, 정상 객체 전체에 그 성질을 유지하려면 무엇을 확인해야 하는지 적어라.

<details><summary>정답</summary>

검사는 `!(_age >= 0 && _age < 200)`일 때 예외 경로로 간다.

| `_age` | `_age >= 0` | `_age < 200` | 결과 경로 |
|---|---|---|---|
| `-1` | 거짓 | 참 | 예외 |
| `0` | 참 | 참 | 정상 생성 |
| `199` | 참 | 참 | 정상 생성 |
| `200` | 참 | 거짓 | 예외 |

두 절차는 같은 검사를 하므로 표의 판정이 같다. 이는 인쇄된 조건을 대입한 결과다.

반례로 `name="A"`, `age=-1`, `getPP():String`을 갖춘 구조적 값을 생각할 수 있다. 메서드가 `name + " of age " + age.toString()`을 반환하도록 정하면 요구한 세 멤버의 타입은 모두 맞는다. `gee_fun`을 호출하지 않고 구성한 이 값의 `age`는 범위 밖이다. 따라서 “검사된 생성 함수의 정상 결과”에서 성립하는 성질을 “그 구조적 타입의 모든 값”으로 확대할 수 없다. `age:Int`라는 정적 정보와 추가 범위 조건을 구분해야 한다.

클래스는 명목 소속과 생성 경로를 관리할 수단을 준다. 그러나 클래스 이름은 임의의 Invariant의 증명이 아니다. 실제 검사와 모든 허용된 생성 경로가 올바른지, 허용된 변경·상속이 조건을 유지하는지 확인해야 한다. `null`까지 정상 생성 객체로 간주해서도 안 된다. [STT 20:31]

확인할 점: 구조적 타입이 필드 타입조차 보장하지 않는다는 결론은 틀리다. 보장되지 않는 것은 여기서 구조 선언에 추가되지 않은 나이 범위다.

</details>

#### 회상 Q04 상속 선언과 허용할 행동 변경

부모가 정상 객체의 `0 <= age < 200`을 약속한다고 하자. `getPP():String`의 계약은 다음 두 경우를 별도로 생각한다.

- 계약 A: 결과는 정확히 `name + " of age " + age.toString()`이다.
- 계약 B: 결과가 이름과 나이를 올바르게 나타내면 문자열 형식은 변경할 수 있다.

자식이 `extends`로 부모의 Subtype이 되었다. 자식이 나이를 범위 밖으로 만들거나, 유효한 이름·나이를 다른 문자열 형식으로 표현할 때 정적 타입 관계와 Behavioural Contract를 어떻게 따로 판단해야 하는가? 부모 설명에 명시해야 할 내용도 적어라. “상속 후 자동 검증 API가 이미 제공되었다”라고 가정해도 되는지도 답하라.

<details><summary>정답</summary>

`extends`는 허용된 명목적 Subtype 관계를 선언한다. 부모 타입을 요구하는 곳에 자식 객체를 공급할 정적 근거와, 부모 사용자가 의존하는 모든 의미적 약속의 증명은 별개다. 반환 타입이 `String`이라는 정보만으로 문자열의 의미나 나이 범위를 증명할 수 없다.

자식의 정상 객체가 나이 범위를 벗어나면 두 계약 모두의 Invariant를 위반한다. 문자열이 다른 형식이어도 이름과 나이를 올바르게 표현한다면 계약 B에서는 허용될 수 있다. 그러나 계약 A가 요구한 정확한 문자열과 다르면 계약 A는 위반한다. 허용 여부는 “자식이니까 자유롭게 변경 가능하다”가 아니라 부모가 약속한 변경 범위에 따라 결정한다.

부모는 정상 객체의 조건, 유지할 Invariant, 메서드의 의미, 재정의로 바꿀 수 있는 부분과 유지해야 할 부분을 명시해야 한다. 자식의 생성·변경·재정의를 검토할 때 그 조건을 다시 확인한다. [STT 18:36] [STT 23:21]

강의의 생성 후 검사 제안은 계약 유지의 동기다. 특정 자동 검증 API나 완성된 구현이 제공되었다는 근거는 없으므로 그 존재를 풀이의 전제로 둘 수 없다.

확인할 점: 정적 관계가 성립하는지와 약속한 행동이 유지되는지를 각각 답하고, 문자열 형식의 변경 허용 여부도 계약별로 구분해야 한다.

</details>

### 재귀 클래스와 Option

#### 회상 Q05 재귀 리스트의 Product·Sum·빈 경우

Part 2 p.20의 `MyList[A]`는 `value:A`와 `next:Option[MyList[A]]`를 가진다. `YourList[A]=Option[MyList[A]]`이다.

~~~text
val empty: YourList[Int] = None
val pair: YourList[Int] =
  Some(new MyList(3,Some(new MyList(4,None))))
~~~

1. 정의의 자기 참조, 노드 안의 Product, `Option`의 Sum이 각각 어디에 있는지 설명하라. `A`는 값 인자인가 타입 인자인가?
2. 두 값의 바깥 `Option`, 각 노드의 `value`·`next`, 노드 수와 종료점을 추적하라. `MyList[A]` 자체가 전체 빈 리스트를 나타내는지도 답하라.
3. `None` 기저 경우가 있다는 이유만으로 모든 재귀 처리가 종료한다고 말할 수 있는가? 유한한 `pair`를 끝까지 처리하는 데 필요한 진행 조건을 적어라.

<details><summary>정답</summary>

`next`의 타입에 정의 중인 `MyList[A]`가 다시 나타나는 것이 자기 참조다. 한 노드는 `A`의 값과 `Option[MyList[A]]`의 값을 함께 담는 Product다. `Option`은 `None` 또는 `Some(node)` 중 하나라는 Sum이다. `A`는 타입 매개변수이므로 `Int`나 `String`을 넣어 같은 노드 구조의 성분 타입을 정한다. 실제 원소 3과 4는 생성자의 값 인자다.

`empty=None`은 첫 노드가 없으므로 노드 수가 0이다. `pair`는 다음처럼 읽는다.

| 위치 | 값·의미 |
|---|---|
| 전체 값 | `Some`이므로 첫 노드 존재 |
| 첫 노드 | `value=3`, `next=Some(둘째 노드)` |
| 둘째 노드 | `value=4`, `next=None` |
| 노드 수·끝 | 2개, 둘째 노드의 `next`에서 종료 |

`MyList[A]`는 값이 있는 노드다. 노드가 전혀 없는 전체 리스트도 나타내기 위해 바깥 `Option`으로 감싼 `YourList[A]`가 필요하다. 전체의 `None`과 노드 안 `next=None`은 부재가 나타나는 위치가 다르다. [STT 30:16] [STT 32:02]

기저 경우는 유한 구조를 만들 수 있게 한다. 처리 함수가 유한한 현재 리스트보다 작은 `next` 부분을 처리하고 `None`에서 멈춘다는 조건이 있어야 종료를 설명할 수 있다. 현재 값을 그대로 다시 처리하는 재귀처럼 진행하지 않는 정의는 `None`의 존재만으로 종료하지 않는다.

확인할 점: 두 필드는 `value`와 `next`이며 `value.next`라는 하나의 경로가 아니다. 재귀 타입 선언과 실제 값의 순환·무한 실행도 동일시하지 않는다.

</details>

#### 회상 Q06 현재 노드와 다음 노드의 존재 근거

정상 노드만 `Some` 안에 들어 있고 추가적인 `null`은 없다고 하자. `s:Option[MyList[A]]`에서 둘째 원소가 있으면 `Some(둘째 값)`, 없으면 `None`을 얻고 싶다.

1. `s.value`를 바로 읽을 수 없는 이유를 설명하고, `None/Some`을 두 번 구분하는 정확한 절차 또는 짧은 코드를 적어라. 빈 리스트·한 노드·두 노드의 결과도 설명하라.
2. 별도의 `null` 기반 표현에서 `next`가 다음 노드 또는 `null`이라고 하자. `p`가 `null`이 아니라는 검사 한 번으로 `p.next.value`까지 안전해지는가? 필요한 검사 위치를 답하라.
3. 이 비교가 “`Option`은 모든 오류를 방지한다” 또는 “Java에는 Sum을 표현할 방법이 없다”는 결론을 주는지도 설명하라.

<details><summary>정답</summary>

`s`는 노드 자체가 아니라 노드가 없을 수도 있는 `Option`이다. `Some`에서 내부 노드를 얻은 뒤에 그 노드의 멤버를 사용할 수 있다. 첫 노드의 `next`도 다시 `Option`이므로 둘째 노드의 존재를 따로 확인한다. 설명용 절차는 다음과 같다.

~~~text
s match {
  case None => None
  case Some(first) =>
    first.next match {
      case None => None
      case Some(second) => Some(second.value)
    }
}
~~~

빈 리스트는 첫 `None`에서, 한 노드 리스트는 첫 노드의 `next=None`에서 `None`을 얻는다. 두 노드가 있으면 둘째 노드에서 `second.value`를 읽어 `Some`으로 감싼다. p.20의 3,4 리스트라면 결과는 `Some(4)`다. [STT 43:16]

`null` 기반 표현에서는 먼저 `p`가 실제 노드인지 확인해야 `p.next`를 읽을 수 있다. 그 뒤 읽은 다음 참조도 `null`이 아닌지 확인해야 그 참조의 `value`를 읽을 수 있다. 현재 노드의 존재는 다음 노드의 존재를 보장하지 않으므로 첫 검사만으로는 부족하다. [STT 38:34]

`Option`은 부재·존재 분기를 타입에 드러낸다. 그러나 잘못된 내부 값, 별도로 허용된 `null`, 부적절한 강제 추출 등 모든 오류를 자동으로 제거한다는 뜻은 아니다. 이 예는 Java 전체의 Sum 표현 가능성을 판정하는 근거도 아니다.

확인할 점: `Option`을 검사한 결과와 그 안의 노드를 혼동하지 않고, 각 멤버 접근에 필요한 존재 근거를 제시해야 한다.

</details>

#### 회상 Q07 Argument Members를 긴 정의로 전개하기

Part 2 p.22의 축약 정의를 같은 두 정보를 제공하는 긴 정의로 풀어 써라. 긴 정의에서는 생성자 입력을 `v`와 `nxt`로 명명하라.

~~~text
class MyList[A](val value:A, val next:Option[MyList[A]])
~~~

입력 Parameter와 객체의 `val` Member가 어떻게 대응하는지 설명하라. 빈 본문의 중괄호를 생략하는 조건, 단순 `x:Int` Parameter를 자동 공개 필드로 간주할 수 있는지, `next` 저장이 전체 꼬리의 Deep Copy를 뜻하는지도 답하라.

<details><summary>정답</summary>

긴 정의는 다음과 같다.

~~~text
class MyList[A](v:A, nxt:Option[MyList[A]]) {
  val value:A = v
  val next:Option[MyList[A]] = nxt
}
~~~

`v`와 `nxt`는 생성할 때 받는 입력이다. `value`와 `next`는 생성된 객체를 통해 읽는 멤버다. 축약형의 `val value`와 `val next`는 인자 전달과 같은 이름의 읽기 멤버 선언을 함께 표현한다. 두 형태 모두 성분 타입 `A`의 값 하나와 선택적인 다음 노드를 담는다. [STT 44:52]

본문에 별도 내용이 없으면 자료처럼 빈 `{}`를 생략할 수 있다. 다른 멤버를 추가한다면 본문을 사용하여 정의할 수 있다. 이 `val` 예로부터 모든 단순 Parameter가 자동 공개 멤버라는 결론은 나오지 않는다. 특히 상속 예의 `x:Int`와 `val a:Int`를 구분해야 한다.

`next`에는 받은 `Option[MyList[A]]` 값을 둔다. 그 설명은 꼬리가 가리키는 모든 노드를 새로 복제한다는 뜻이 아니다. 긴 정의나 축약 정의 어디에도 그런 재귀 복제 절차는 없다.

확인할 점: 멤버 이름과 타입이 보존되는지 확인하고, 단순 Parameter·읽기 멤버·전체 재귀 구조 복제를 서로 다른 주장으로 다루어야 한다.

</details>

#### 회상 Q08 타입 이름·Companion Object·Apply 전개

Part 2 p.23의 실제 `apply` 본문을 사용하라. `MyList.apply(v,nxt)`는 `new MyList(v,nxt)`를, `YourList.apply(v,nxt)`는 `Some(new MyList(v,nxt))`를 반환한다.

1. 타입 자리의 `MyList[A]`와 값 자리의 `MyList`, `new MyList(...)`로 만든 노드를 구분하고 Companion Object의 의미를 설명하라.
2. `MyList(4,None)`과 `YourList(4,None)`을 `apply` 호출과 최종 생성식으로 각각 전개하라.
3. 다음 세 값의 구조와 노드 수를 비교하고, 같은 구조라는 결론이 참조 동일성까지 뜻하는지 답하라.

~~~text
t0 = None
t1 = Some(new MyList(3,Some(MyList(4,None))))
t2 = YourList(3,YourList(4,None))
~~~

모든 `apply`를 “`new`만 생략한 것”으로 설명할 수 있는지도 답하라.

<details><summary>정답</summary>

타입 자리의 `MyList[A]`는 클래스 타입이다. 호출 식에서 `MyList`는 `apply` 메서드를 가진 동명 `object`라는 값이다. 클래스와 같은 이름으로 둔 객체가 Companion Object이며, 관련 생성 함수를 함께 둘 수 있다. 그 객체 자체가 곧 리스트 노드인 것은 아니다. `new MyList(...)`로 구성한 값이 노드다.

두 호출은 실제 본문에 따라 다르게 전개된다.

~~~text
MyList(4,None)
→ MyList.apply(4,None)
→ new MyList(4,None)

YourList(4,None)
→ YourList.apply(4,None)
→ Some(new MyList(4,None))
~~~

따라서 앞은 `MyList[Int]` 노드, 뒤는 바깥 `Some`으로 감싼 `YourList[Int]` 구조다. [STT 51:20]

`t1`은 안쪽 `MyList(4,None)`을 전개하고, `t2`는 안쪽 `YourList`부터 전개한다.

~~~text
t1 → Some(new MyList(3,Some(new MyList(4,None))))

t2 → YourList(3,Some(new MyList(4,None)))
   → Some(new MyList(3,Some(new MyList(4,None))))
~~~

`t1`과 `t2`는 3 다음에 4가 있고 끝이 `None`인 두 노드 구조다. `t0=None`은 노드가 0개인 빈 리스트로 둘과 다르다. 같은 구조를 나타낸다는 말만으로 별도 생성 객체들의 참조 동일성이나 자동 구조적 동등성을 주장할 수는 없다.

`apply`의 반환 내용은 본문에 달려 있다. 여기서도 `YourList.apply`는 `new` 호출뿐 아니라 `Some` 포장까지 한다. 따라서 모든 `apply`의 의미를 `new` 생략으로 일반화할 수 없다.

확인할 점: 타입·객체·메서드·생성된 노드 네 대상을 구분하고, `Some`의 각 층을 생략하지 않아야 한다.

</details>

#### 회상 Q09 이진트리의 세 성분과 긴·축약 생성식

Part 2 pp.24–26에서 `MyTree[A]`는 `value:A`, `left:Option[MyTree[A]]`, `right:Option[MyTree[A]]`를 가진다. `YourTree[A]=Option[MyTree[A]]`이며 `YourTree.apply(v,lt,rt)=Some(new MyTree(v,lt,rt))`이다.

다음 값들을 긴 생성식으로 전개하고 각 루트·왼쪽·오른쪽과 전체 노드 수를 적어라.

~~~text
t0: YourTree[Int] = None
t1: YourTree[Int] = YourTree(3,None,None)
t2: YourTree[Int] = YourTree(3,YourTree(4,None,None),None)
~~~

노드의 Product, 자식과 전체 트리의 Sum을 설명하고, Part 1 p.76의 `Leaf`가 값 있는 잎 노드와 같은 의미인지도 답하라. 기저 경우와 재귀 처리의 종료 조건을 구분하라.

<details><summary>정답</summary>

세 값의 긴 생성식은 다음과 같다.

~~~text
t0 = None
t1 = Some(new MyTree(3,None,None))
t2 = Some(new MyTree(3,Some(new MyTree(4,None,None)),None))
~~~

| 값 | 루트·왼쪽·오른쪽 | 노드 수 |
|---|---|---|
| `t0` | 루트 자체가 없음 | 0 |
| `t1` | 루트 3, 왼쪽·오른쪽 모두 `None` | 1 |
| `t2` | 루트 3, 왼쪽은 값 4의 노드, 오른쪽은 `None`; 값 4의 두 자식도 `None` | 2 |

`t2`는 안쪽 호출을 `Some(new MyTree(4,None,None))`으로 전개하고 그 값을 바깥 호출의 왼쪽 인자로 넣으면 얻어진다. 축약은 자식의 위치나 `Some`의 층을 바꾸지 않는다.

한 노드는 값·왼쪽·오른쪽을 함께 갖는 세 성분의 Product다. 각 자식의 `Option`은 그 방향의 빈 경우와 노드가 있는 경우의 Sum이다. 바깥 `YourTree`의 `Option`은 루트 자체가 없는 전체 빈 트리도 표현한다. 정상 노드 타입 `MyTree[A]`만으로 전체 빈 경우를 대신할 수는 없다. [STT 54:25] [STT 58:33]

Part 1의 `BTree = Leaf | Node of Int * BTree * BTree`에서 `Leaf`는 값을 담지 않는 빈 경우다. Option 표현의 `None`에 대응한다. `Some(new MyTree(3,None,None))`처럼 값은 있고 두 자식만 없는 노드와 구분해야 한다.

`None`은 유한 구조의 기저 표현을 준다. 연산의 종료를 설명하려면 유한한 트리에서 현재보다 작은 자식 부분으로 진행하고 빈 경우에서 멈추는 조건이 별도로 필요하다.

확인할 점: 빈 트리·값 있는 한 노드·두 노드 트리를 구분하고, 좌우 자식을 바꾸지 않아야 한다.

</details>

### 상속과 동적 메서드 선택

#### 회상 Q10 부모 생성자와 자식 본문의 Binding

Part 2 p.28의 독립된 예를 사용하라. 부모 `foo_type(x:Int,y:Int)`는 `val a=x`, `def b:Int=a+y`, `def f(z:Int):Int=b+y+z`를 정의한다. 자식 `gee_type(x:Int) extends foo_type(x+1,x+2)`는 `val c:Int=f(x)+b`를 추가한다.

`new gee_type(30)`에서 다음을 순서대로 추적하라.

1. `extends`가 선언하는 명목 관계와 부모에게 전달할 두 인자.
2. 자식 `x`, 부모 `x,y`, `f`의 `z` 각각의 결합.
3. `a`, `b`, `f(30)`, `c`의 계산.
4. 단순 Parameter, `val` Member, `def` Method의 차이. 이 예에서 부모의 어떤 멤버가 재정의되었는지도 답하라.

<details><summary>정답</summary>

`extends`는 `gee_type <: foo_type`의 명목 관계를 선언한다. 자식 입력 `x=30`에서 부모 호출 인자는 `x+1=31`과 `x+2=32`다. 자식과 부모의 동명 Parameter를 같은 결합으로 보지 않는다.

| 위치 | 결합·계산 |
|---|---|
| 자식 생성자 | `x=30` |
| 부모 생성자 | `x=31`, `y=32` |
| 부모의 `a` | `a=31` |
| `b` 사용 | `a+y=31+32=63` |
| 자식의 `f(x)` 호출 | 자식의 `x=30`을 전달하므로 `z=30` |
| `f(30)` | `b+y+z=63+32+30=125` |
| `c` 초기화 | `f(30)+b=125+63=188` |

`x,y,z`는 각 생성자나 호출이 받은 입력 이름이다. 이들이 모두 외부 공개 필드라는 뜻은 아니다. `a,c`는 `val` 멤버이고 `b,f`는 `def` 메서드다. 이 예에서 매번 같은 수치를 얻더라도 `b`를 생성 시 저장된 `val` 초기값으로 해석하지 않는다. [STT 01:03:09] [STT 01:04:04]

자식은 `a,b,f`를 재정의하지 않고 `c`만 추가한다. 부모의 입력 변환과 자식의 추가 초기화는 서로 구분된다. 여기의 `gee_type`은 앞의 name·age 구조적 별칭과 별개이며, p.29의 다른 `b,f` 본문도 끌어오지 않는다.

확인할 점: `a=30` 또는 `f(x)`의 인자 31로 계산하면 Binding을 혼동한 것이다. 이 수치 전개는 인쇄된 코드의 손계산이다.

</details>

#### 회상 Q11 부모 관점 Abstraction과 구현 Reuse

Q10과 같은 p.28 정의에서 `test`는 다음과 같다.

~~~text
def test(f:foo_type) = f.a + f.b
~~~

`test(new foo_type(10,20))`와 `test(new gee_type(30))`의 값을 각각 전개하라. 이 함수의 매개변수 `f`와 클래스의 메서드 `f(z)`를 구분하라. 자식의 `c`가 계산에 들어가는지, 부모 타입의 관점에서 `c`를 읽을 수 있는지도 설명하라. 마지막으로 이 예의 Abstraction과 Reuse가 각각 무엇이며, 구현 재사용만으로 좋은 행동 계약이 보장되는지 답하라.

<details><summary>정답</summary>

부모 객체 `new foo_type(10,20)`에서는 `a=10`, `b=a+y=10+20=30`이다. 따라서 첫 호출은 `10+30=40`을 계산한다.

자식 객체 `new gee_type(30)`는 부모 인자로 31과 32를 전달하므로 `a=31`, `b=31+32=63`이다. 둘째 호출은 `31+63=94`를 계산한다. `c=188`은 이 합에 포함되지 않는다.

`test` 안의 `f`는 전달된 객체를 가리키는 매개변수 이름이다. `f.a`와 `f.b`는 그 객체의 멤버 사용이며, 메서드 `f(z)`를 호출한 식이 아니다. `gee_type <: foo_type`이므로 `a,b`를 사용하는 부모 관점에 자식 객체를 공급할 수 있다. 그러나 부모 타입에 `c`가 선언된 것은 아니므로 그 관점만으로 `c`를 요구할 근거는 없다.

Abstraction은 더 많은 멤버가 있는 구체 객체를 현재 필요한 부모의 관점으로 이해하는 것이다. Reuse는 자식이 부모의 생성 절차와 `a,b,f` 구현을 복사하지 않고 이용하는 것이다. 둘은 연결되지만 같은 목적은 아니다. 구현을 재사용했어도 부모 사용자가 의존하는 계약이 유지되는지 별도로 판단해야 한다. [STT 01:06:30] [STT 01:07:26]

확인할 점: 두 결과의 차이는 부모에게 전달한 인자의 차이에서 나오며, 자식 `c`를 자동으로 더하는 데서 나오지 않는다.

</details>

#### 회상 Q12 B의 Overriding이 F·C·부모 관점에 주는 영향

이번에는 Part 2 p.29의 별개 정의다. 부모는 `val a=x`, `def b:Int=0`, `def f(z:Int):Int=b*z`를 갖는다. 자식은 `extends foo_type(x+1,x+2)` 후 `override def b=10`과 `val c:Int=f(x)+b`를 둔다. `test(v:foo_type)`는 `println(v.f(42))`를 실행하는 정의다.

1. `(new gee_type(30)).c`를 부모 인자부터 전개하라.
2. `test(new foo_type(1,2))`와 `test(new gee_type(0))`에서 `println`에 전달할 값을 계산하라. 자식 생성자의 0과 메서드 인자 42를 구분하라.
3. `f`를 재정의하지 않았는데 결과가 바뀌는 이유를 설명하라. 대안 `override def b=super.b+10`은 이 예에서 어떤 값인가?
4. 이 변경이 계약 위반인 경우와 허용되는 경우를 구분하라. 분석을 임의의 `val` 초기화 규칙이나 후속 Overloading 예로 확대해도 되는지도 답하라.

<details><summary>정답</summary>

`new gee_type(30)`는 부모 인자로 31과 32를 전달하므로 `a=31`이다. 이 수신 객체에서 `b`는 자식의 재정의한 메서드를 선택하여 10이다. 자식 본문의 `f(x)`는 `f(30)`이므로 `10*30=300`이다. 따라서 `c=300+10=310`이다.

부모 객체 `new foo_type(1,2)`에는 `b=0`이므로 `v.f(42)=0*42=0`이다. 첫 `println`에 전달할 값은 0이다. `new gee_type(0)`는 부모 인자 1과 2를 사용하지만, `test`가 `f`에 넘기는 값은 42다. 실제 객체의 `b=10`을 선택하므로 `v.f(42)=10*42=420`이다.

`f`의 본문은 상속된 그대로지만 본문 안의 `b`는 현재 수신 객체의 메서드를 사용한다. 부모 타입의 매개변수로 받았다고 이 Dynamic Dispatch가 없어지지 않는다. 따라서 `f`의 코드를 직접 바꾸지 않아도 그 의존 대상인 `b`가 바뀌면 결과가 바뀐다. [STT 01:13:52]

`super.b+10`은 부모 구현을 명시적으로 사용한다. 이 예의 부모 `b`는 0이므로 `0+10=10`으로 같은 수치를 준다. 부모 본문이 다를 때도 항상 `10`과 같다는 일반 규칙은 아니다.

부모 계약이 모든 하위 객체의 `b=0`을 약속했다면 변경은 그 약속을 깨뜨린다. 반대로 `b`의 재정의를 허용하고 `f`가 현재 객체의 `b`를 사용한다고 정했다면 의도한 변경일 수 있다. 직접 재정의한 메서드뿐 아니라 그 메서드에 의존하는 상속 메서드도 검토해야 한다. [STT 01:11:58]

이 분석은 `def b`와 `def f`의 선택에 한정한다. 임의의 `val` 초기화나 생성자 도중의 가상 호출 전체를 설명하지 않는다. 같은 메서드 구현의 재정의와 다른 인자 타입의 호출 형태를 더하는 Overloading도 구분하며, 후속 페이지의 상세 학습으로 확장하지 않는다.

확인할 점: p.28의 덧셈 정의로 계산하지 않아야 한다. 310·0·420은 주어진 코드의 손계산이다.

</details>

### 생성·재귀 구조·동적 선택의 통합 연습

#### 연습 P01 같은 구조를 받는 API와 검사된 객체를 받는 API

다음은 생성 통제와 계약을 비교하기 위해 새로 정한 예다. 선수 지식은 Structural Type, Type Alias, `val` Member, `new`, `extends`, 문자열 연결이다.

`type Profile = {val name:String;val age:Int;def label():String}`이라는 구조적 별칭이 있다. 별개의 클래스 `Person(_name:String,_age:Int)`은 `0 <= _age < 200`을 검사하고 실패하면 예외를 던진다. 정상 객체는 `val name=_name`, `val age=_age`를 갖고 `label()`은 `name + " of age " + age.toString()`을 반환한다. 다음 값과 API 요구를 사용하라. 참조는 `null`이 아니고 생성 후 멤버 변경은 없다고 하자.

- `good:Person = new Person("Mina",20)`.
- `other:Profile`은 `Person`이나 그 자식에서 만들지 않은 구조적 값이다. `name="Mina"`, `age=-1`이며 `label()`은 같은 연결식으로 문자열을 만든다.
- API G는 `name:String`만 읽어 인사말을 만든다.
- API D는 이름·나이를 읽고 `label()`을 호출한다. API D의 사용자는 나이 범위와 `label()`의 정확한 `" of age "` 형식까지 믿고 싶어 한다.

1. G가 받을 최소 구조를 적고 두 값을 각각 받을 수 있는 이유를 설명하라. 두 값이 `Profile` 관점에서도 사용 가능한지 답하라.
2. D의 입력을 단지 `Profile`로 정했을 때 사용자의 두 추가 가정이 보장되는가? `other`의 `label()`을 전개하여 반례를 설명하라.
3. D의 입력을 `Person`으로 정하면 `other`가 자동으로 들어오는가? D의 두 가정을 유지하기 위해 클래스와 허용된 하위 타입의 계약에 명시할 내용을 제안하라.
4. 자식이 유효한 `name`·`age`는 유지하면서 `label()`을 `name + ":" + age.toString()`으로 바꾸는 경우를 판단하라. D가 정확한 형식 요구를 철회하고 “이름과 나이를 올바르게 나타내면 형식 변경 가능”으로 계약을 바꾸면 결론이 어떻게 달라지는가?

<details><summary>정답</summary>

G의 최소 구조는 `{val name:String}`이다. G는 `age`나 `label`을 사용하지 않으므로 그 멤버나 명목 소속을 요구할 이유가 없다. `good`과 `other`는 모두 `name:String`을 제공하므로 받을 수 있다. 두 값은 `Profile`이 요구하는 세 멤버도 제공하므로 그 구조적 관점으로 사용할 수 있다.

`Profile`은 `age:Int`와 `label():String`만 요구한다. 정수의 추가 범위나 문자열의 정확한 의미를 선언한 것은 아니다. `other.label()`을 손으로 전개하면 다음과 같다.

~~~text
"Mina" + " of age " + (-1).toString()
= "Mina of age -1"
~~~

이 값은 구조를 충족하면서 범위를 위반한다. 더구나 같은 구조에서 `label():String`이 임의의 다른 문자열을 돌려주도록 정의해도 메서드의 반환 타입 자체는 맞을 수 있다. 따라서 구조만으로 D의 두 가정을 모두 얻을 수 없다.

`Person`을 요구하면 `other`는 같은 구조라는 이유만으로 명목 소속을 얻지 않는다. `good`은 실제 정상 생성 절차를 통과했다. 다만 `Person`이라는 이름만 적으면 모든 행동이 자동으로 증명되는 것은 아니다. 이 문제의 조건에서는 다음을 계약으로 명시하고 허용된 모든 생성·상속 경로에서 유지해야 한다.

- 정상 객체의 `age`는 `0 <= age < 200`이며 생성 실패는 정상 결과와 구분한다.
- `name`·`age`를 설정하는 허용 경로는 그 조건을 지킨다.
- D의 현재 계약 아래에서는 `label()`의 결과가 정확히 `name + " of age " + age.toString()`이다.
- 허용한 자식의 재정의도 이 의미와 Invariant를 유지한다. 멤버 변경을 허용하는 다른 설계라면 변경 뒤에도 같은 조건을 유지해야 한다.

이를 바탕으로 D는 정상 `Person` 객체의 계약에 의존할 수 있다. 상속 선언만으로 임의의 의미적 약속이 검사되었다고 가정하지 않는다.

콜론 형식으로 바꾼 자식은 여전히 `String`을 반환하고 나이 범위도 유지한다. 그러나 D가 요구한 정확한 문자열 형식은 위반한다. 형식 변경을 허용하는 계약으로 바꾸었다면 이름과 나이를 올바르게 포함한 `"Mina:20"` 같은 결과는 허용될 수 있다. 이때 D의 사용자도 더 이상 고정된 `" of age "` 형식에 의존해서는 안 된다. 나이 범위의 약속은 형식 요구를 철회해도 유지된다.

확인할 점: G의 구조적 사용 가능성, D의 명목 소속 요구, 값의 범위, 메서드의 의미를 별도로 판단해야 한다. 문자열 반환 타입과 행동 계약을 같은 것으로 취급하면 반례를 설명할 수 없다.

</details>

#### 연습 P02 리스트와 비대칭 트리의 안전한 노드 수 계산

`MyList/YourList`와 `MyTree/YourTree`는 본문의 `val` 멤버 및 `apply` 정의를 그대로 사용한다. 모든 입력은 유한하게 구성된 정상 노드이고 `Some` 안에 `null`은 없다. 이 문제에서 노드 수는 구조상의 각 위치를 세며 `0` 이상 `2147483647` 이하이고, 각 재귀 호출은 정상적으로 값을 반환한다고 가정한다. 선수 지식은 Part 1 자료에 근거한 Product·Sum, Pattern Matching, 타입 매개변수, `length`의 빈 경우·작은 꼬리 처리다.

~~~text
val xs: YourList[String] =
  YourList("r",YourList("s",YourList("t",None)))
val tr: YourTree[String] =
  YourTree("r",None,YourTree("s",YourTree("t",None,None),None))
~~~

1. `tr`을 `Some/new`를 모두 드러낸 긴 생성식으로 바꾸고 루트·좌우 자식 위치를 적어라. 두 입력이 원소 이름과 노드 수가 같다고 같은 구조인지도 설명하라.
2. `countList[A](xs:YourList[A]):Int`와 `countTree[A](tr:YourTree[A]):Int`를 작성하라. 둘 다 전체 빈 값은 0이고 존재하는 노드 하나당 1을 센다. `None/Some`을 구분하고 노드 멤버는 `Some`에서 얻은 뒤 사용하라. 원소 `A`에 대한 추가 연산은 필요하지 않다.
3. 두 주어진 입력과 전체 빈 입력에 대한 계산을 전개하라. 두 함수의 종료 근거를 설명하라.
4. 트리의 `Some(n)` 분기를 `1+countTree(n.left)`로만 쓰는 오류를 생각하라. 이 입력에서 얻는 오답을 구하고, 왜 오른쪽 재귀 결과까지 필요한지 Product 관점에서 설명하라.

<details><summary>정답</summary>

`tr`의 긴 생성식은 다음과 같다.

~~~text
Some(new MyTree("r",None,
  Some(new MyTree("s",
    Some(new MyTree("t",None,None)),None))))
~~~

루트 `"r"`의 왼쪽은 없고 오른쪽은 `"s"` 노드다. `"s"`의 왼쪽은 `"t"` 노드이고 오른쪽은 없다. `"t"`의 두 자식은 없다. `xs`는 `"r"→"s"→"t"`의 다음 노드 하나씩을 가진 리스트다. 두 자료는 원소 이름과 노드 수가 같아도 리스트의 `next`와 트리의 `left/right`라는 구성 성분이 다르므로 같은 구조라고 할 수 없다.

새로 작성한 노드 수 함수는 다음과 같다. 정확한 계수 계약은 문제에서 정한 `0≤노드 수≤2147483647`인 입력에 적용한다.

~~~text
def countList[A](xs:YourList[A]):Int =
  xs match {
    case None => 0
    case Some(n) => 1 + countList(n.next)
  }

def countTree[A](tr:YourTree[A]):Int =
  tr match {
    case None => 0
    case Some(n) =>
      1 + countTree(n.left) + countTree(n.right)
  }
~~~

첫 함수는 노드 하나와 나머지 `next`를 세고, 둘째 함수는 노드 하나와 두 자식을 센다. 각 부분구조의 개수와 중간 합도 전체 개수 이하이므로 명시한 범위에서는 `Int` 덧셈이 정확한 계수 범위를 넘지 않는다. 유한한 입력이라는 사실만으로 이 수치 상한이 성립하지는 않는다. 두 함수 모두 `Some(n)`에서 정상 노드 `n`을 얻은 뒤 멤버를 사용한다. 타입 매개변수 `A`는 값의 타입을 정할 뿐이며 노드 수를 세는 데 특정 필드나 산술 기능을 요구하지 않는다.

리스트의 계산은 각 단계에서 한 노드씩 제거한 꼬리로 진행한다.

~~~text
countList(xs) = 1 + (1 + (1 + 0)) = 3
countList(None) = 0
~~~

트리에서는 `"t"` 부분부터 다음처럼 계산한다. 아래의 이름은 각 노드가 루트인 `Some` 부분 트리를 가리킨다.

~~~text
countTree("t" 부분) = 1 + 0 + 0 = 1
countTree("s" 부분) = 1 + 1 + 0 = 2
countTree(tr) = 1 + 0 + 2 = 3
countTree(None) = 0
~~~

입력이 유한하고 각 재귀 호출이 현재보다 작은 꼬리 또는 자식 부분으로 진행하므로 결국 `None`에 도달한다. 이는 수치 범위와 각 재귀 호출의 정상 반환을 전제로 한 함수식의 전개다. 재귀 선언 자체나 `Option`이라는 이름만으로 모든 함수가 종료한다는 논증은 아니다.

잘못된 트리 분기는 루트의 왼쪽 `None`만 처리하여 `1+0=1`을 준다. 실제 오른쪽 부분의 두 노드를 누락한다. 노드가 값·왼쪽·오른쪽을 함께 담는 Product이므로 전체 노드 수에는 양쪽 자식의 결과가 모두 필요하다. 빈 자식 하나가 있다고 현재 노드나 다른 자식이 없어지는 것은 아니다.

확인할 점: 바깥 빈 값과 값 있는 잎 노드를 구별하고, 루트의 1과 두 자식의 재귀 결과를 모두 포함해야 한다. 이 문제의 두 함수는 원소의 내용이나 `null` 역참조에 기대지 않는다.

</details>

#### 연습 P03 Super 호출과 간접 의존을 함께 추적하기

다음은 생성자 Binding, `super.b`, 상속된 메서드의 Dynamic Dispatch를 함께 살피기 위해 새로 정의한 독립 프로그램이다. 본문의 p.28·29 정의를 같은 프로그램으로 합쳐 읽지 말고 아래 본문을 기준으로 계산하라. 선수 지식은 `val/def`, `extends`, `override`, 부모 관점 사용이다.

~~~text
class Base(x:Int,y:Int) {
  val a:Int = x
  def b:Int = a + y
  def f(z:Int):Int = b * z
}
class Shift(k:Int) extends Base(k+1,k+2) {
  override def b:Int = super.b + 10
  def report(z:Int):Int = f(z) + a
}
def inspect(v:Base,z:Int):Int = v.f(z) + v.b
~~~

객체 생성이 끝난 뒤 `p=new Base(3,4)`, `s=new Shift(2)`를 사용한다.

1. `s`의 부모 인자, `a`, `super.b`, 재정의한 `b`를 계산하라. `super.b`와 상속된 `f` 안의 `b`가 각각 어떤 구현을 선택하는지 구분하라.
2. `p.f(5)`, `inspect(p,5)`, `s.f(5)`, `s.report(5)`, `inspect(s,5)`를 전개하라. `inspect`의 매개변수 타입이 `Base`인데도 결과가 달라지는 이유를 설명하라.
3. `Shift`에서 `override def b` 한 줄만 제거하면 `a`·`f(5)`·`report(5)`·`inspect(s,5)` 중 무엇이 어떻게 달라지는가? 의존 경로와 함께 답하라.
4. 부모 계약이 “항상 `b=a+y`”인 경우와 “`b` 재정의 허용, `f(z)`는 현재 객체의 `b*z`”인 경우에 이 자식을 각각 평가하라. Abstraction과 Reuse의 관점도 구분하라.

<details><summary>정답</summary>

`Shift`의 입력 `k=2`에서 부모 인자는 `k+1=3`과 `k+2=4`다. 부모의 결합은 `x=3,y=4`이므로 `a=3`이다. 자식의 `super.b`는 부모 구현 `a+y`를 명시적으로 사용하여 `3+4=7`을 얻는다. 따라서 자식의 `b=7+10=17`이다.

반면 상속된 `f` 본문의 일반적인 `b` 사용은 현재 수신 객체의 메서드를 선택한다. `s`에서 `f`를 호출하면 그 객체의 재정의한 `b=17`을 사용한다. `super.b`가 부모 본문을 선택하는 것과 일반적인 `b`의 동적 선택을 혼동하지 않는다.

| 식 | 전개 | 값 |
|---|---|---|
| `p.f(5)` | `(3+4)*5` | 35 |
| `inspect(p,5)` | `35+(3+4)` | 42 |
| `s.f(5)` | `17*5` | 85 |
| `s.report(5)` | `85+3` | 88 |
| `inspect(s,5)` | `85+17` | 102 |

`inspect`는 부모 타입에 허용된 `f`와 `b`만 사용하므로 자식을 받을 수 있다. 정적 타입이 `Base`여도 실제 객체가 `Shift`이면 `f` 내부와 `v.b`에서 자식의 재정의를 선택한다. `report`는 자식에 추가된 메서드로 `inspect`가 요구하거나 호출하는 멤버는 아니다.

재정의 한 줄을 제거하면 부모의 `b=3+4=7`을 그대로 상속한다. 부모 생성자 인자와 `a=3`은 변하지 않는다. 그러나 다음 의존 경로의 값은 달라진다.

~~~text
b: 17 → 7
b → f(5): 85 → 35
b → f(5) → report(5): 88 → 38
b → f(5), b → inspect(s,5): 102 → 42
~~~

`f`·`report`·`inspect`의 본문은 그대로인데 그 안에서 사용하는 `b`의 선택이 달라져 결과가 달라진다. `a`는 바뀐 `b`에 의존하지 않으므로 값 3을 유지한다.

부모가 모든 하위 객체에 `b=a+y`를 약속했다면 `b=17`인 이 자식은 `a+y=7`과 달라 계약을 위반한다. 두 번째 계약은 `b`의 재정의를 허용하고 `f`의 계산을 현재 `b`로 정의하므로 이 변경은 그 조건 아래 허용된다. `f`가 부모 구현의 7을 영원히 사용할 것이라고 가정하는 사용자는 두 번째 계약을 잘못 읽은 것이다.

Abstraction에서는 `inspect`가 의존하는 부모의 관점과 허용된 행동을 정한다. Reuse에서는 자식이 부모 생성 절차·`a`·`f`를 이용하고 `super.b`로 부모 계산도 활용한다. 재사용한 코드 양과 행동 계약의 올바름은 따로 판단해야 한다.

확인할 점: 부모 인자, `super`를 통한 명시적 선택, 일반 메서드의 동적 선택을 분리해야 한다. 여기서는 생성 완료 뒤의 `def` 호출을 계산하므로 별도의 `val` 재정의 초기화 규칙을 가정할 필요가 없다.

</details>

## 출처

### Sources

[[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|Class·Inheritance 보정 STT · 날짜 미확인]]

[Part 2 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf) · [Part 1 공식 자료 저장소](https://github.com/snu-sf-class/pp202602). 아래 쪽수는 PDF의 물리적 페이지다.

| 출처 | 위치 | 연결 내용 |
|---|---|---|
| M002 · Part 1 | [p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-068) · [p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-069) · [p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-070) · [p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071) | Introduction·Elimination, Tuple·Record와 Type Alias의 자료 기반 선수 개념 |
| M002 · Part 1 | [p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-073) · [p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-074) · [p.76](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076) · [p.78](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-078) · [p.79](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-079) | Product·Sum·재귀 ADT, 빈 경우·노드, Pattern Matching과 length의 진행 |
| M002 · Part 1 | [p.90](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-090) · [p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092) · [p.98](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-098) | 타입 매개변수와 Option의 생성·제거 |
| NM001 · Part 2 / NT002 | [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-016) · [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-017) · [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-018) · [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-019) / [STT 03:06], [STT 08:32], [STT 18:36], [STT 20:31], [STT 23:21], [STT 25:16] | Q01–Q04·P01의 생성, 구조적 사용, 명목 소속, Invariant·계약 |
| NM001 · Part 2 / NT002 | [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-020) · [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-021) · [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-022) · [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-023) / [STT 30:16], [STT 32:02], [STT 38:34], [STT 43:16], [STT 44:52], [STT 51:20] | Q05–Q08·P02의 재귀 리스트, null·Option, val 멤버, Companion Object·apply |
| NM001 · Part 2 / NT002 | [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-024) · [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-025) · [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-026) / [STT 54:25], [STT 58:33], [STT 01:00:20] | Q09·P02의 Option 기반 트리와 긴·축약 생성식 |
| NM001 · Part 2 / NT002 | [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-028) / [STT 01:03:09], [STT 01:04:04], [STT 01:06:30], [STT 01:07:26] | Q10–Q11·P03의 부모 인자, Binding, Parent View·Reuse |
| NM001 · Part 2 / NT002 | [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-029) / [STT 01:11:58], [STT 01:13:52] | Q12·P03의 def 기반 Dynamic Dispatch, super와 간접 의존·계약 |

두 현재 강의의 날짜는 모두 미확인이다. Part 1 자료형은 자료 기반 선수 설명이며 pp.63–100 전체의 구두 강의를 뜻하지 않는다. Part 2 p.30 이후의 상세 내용은 후속·참고 범위다.

보정 STT는 원음 미검증이며 완전한 축어록이나 음성 누락 검증 자료가 아니다. 첫 표시는 01:46, 마지막 구간의 시작은 01:15:40이다. 끝 시각·구간 사이의 침묵·누락은 확인되지 않았다. 미완성·불명확한 발화의 한정은 그대로 적용된다. 제공되지 않은 말·live 코드·화면·판서·그림은 확인할 수 없다. 수치는 자료 코드나 명시한 설명용 예의 손계산이며 실제 컴파일·실행 결과가 아니다.

Part 2 p.18의 역방향 Subtype 관계는 취소되어 있다. p.16의 구조적 별칭 gee_type과 p.28의 동명 클래스, pp.28·29의 서로 다른 b·f·test 정의는 구별한다. p.17은 getPP()를 정의·호출하지만 use 줄에는 getPP라고 적혀 있다. 본문은 정의에 따른 getPP()를 사용하며, 이 표기 차이에서 Scala 버전별 자동 적용 규칙을 일반화하지 않는다.

계약·null·재귀 종료·def/val에 관한 설명은 본문의 생성·변경·정상 노드·유한성·진행 조건에 한정한다. 강의의 언어 표현력·안전성·구현 비용에 관한 포괄적 발언이나 미제공 수학 도식을 일반 정리로 확장하지 않는다.

| 역사 자료 | 정확한 파일·행 | 연결의 성격과 한계 |
|---|---|---|
| 2024 중간 Q1-1 · pop_2024_mid_q01 | repository/Assignment/pp-midterm-1/src/main/scala/Main.scala L.46–68 | Q05·P02의 빈 경우, 작은 꼬리, 부분 결과 결합과 풀이 구조 연결. 클래스 생성·명목 소속의 직접 문항 대응은 아님 |
| 2024 중간 Q1-2 · pop_2024_mid_q01 | repository/Assignment/pp-midterm-1/src/main/scala/Main.scala L.70–92 | Q09·P02의 빈 트리와 두 하위 트리 분석에 풀이 구조 연결. 구체적인 fold 구현은 요구하거나 옮기지 않음 |
| 2025 중간 Q1 부분 발췌 · pop_2025_mid_q01_partial | issues/13.md L.26–46 | Q02·P01에서 멤버의 이름·타입을 요구하는 구조를 읽는 개념만 연결. 전체 문제 지시문이 없으며 class라는 외곽 표기만으로 명목 상속·override 문항으로 볼 수 없음 |

2024 중간의 연도는 2025년 게시물의 “작년도” 업로드 안내(issues/03.md L.5–9)에 근거한다. list/tree의 풀이 구조 연결에는 재귀 ADT·Pattern Matching·타입 매개변수가 선수 지식이다. 이 모음에서 직접 대응하는 상속 문항은 확인되지 않았으며 모든 기출에 없다는 뜻은 아니다. 2025 발췌는 완전한 문제·시험지가 아니고 별도 제공 답은 독립 검증되지 않았다. 2024 기말 자료도 Q3–Q4에 한정된다. 코드 기출의 위치는 원래 파일·행 기준이며 PDF 쪽수는 없다.
