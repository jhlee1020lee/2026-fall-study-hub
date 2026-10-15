---
title: "Data Type 선수 개념과 Structural Subtyping · 강의 정리 · 날짜 미확인"
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

### Introduction·Elimination과 Tuple의 생성·사용

Introduction(도입)은 어떤 타입의 값을 만드는 방법이고, Elimination(제거)은 이미 주어진 값을 사용하는 방법이다. 여기서 ‘제거’는 값을 메모리에서 지운다는 뜻이 아니다. `Int`의 정수 리터럴은 값을 도입하고, 덧셈·뺄셈·비교는 정수 값을 사용한다. Function Type(함수 타입)에서는 `(x:T)=>e`가 함수 값을 만들고 `f(v)`가 그 함수에 인자를 공급한다. 인자 `v`가 입력 타입에 맞고 함수 본문이 요구된 결과 타입을 만든다는 조건 아래 함수 적용을 설명할 수 있다. 이 생성·사용 구분은 Part1 자료에 근거한 선수 개념이다. [Part1 PDF p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-068)

Tuple(튜플)은 여러 성분을 위치에 따라 묶은 값이다. 자료의 `(1,"a",10)`은 `(Int,String,Int)`인 세 성분의 튜플로 읽는다. 전체를 만드는 식이 Introduction이고, `._1`·`._2`·`._3`로 성분을 꺼내는 Projection(투영)이 Elimination이다. 세 투영값은 `(1,"a",10)._1=1`, `(1,"a",10)._2="a"`, `(1,"a",10)._3=10`이다. 따라서 `._2`는 두 번째 성분 `"a"`를 사용하게 해 주는 식이다. `f(v)`도 이미 존재하는 함수 값을 사용한다는 점에서 같은 구분의 Elimination이다. [Part1 PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-069)

튜플은 모든 성분이 같은 타입일 필요가 없다. 대신 Arity(성분 수)와 각 위치의 타입이 함께 타입을 정한다. `(Int,String,Int)`에서 두 번째 위치는 `String`이고 세 번째 위치는 `Int`이다. Record(레코드)의 `r.name`처럼 이름으로 멤버를 고르는 것과 튜플의 위치 접근을 구분해야 한다. 자료의 “Only up to length 22”는 그 자료의 튜플 표현 문맥에 관한 한정이다.

### Structural Type과 Type Alias: 멤버와 정의 환경

Structural Type(구조적 타입), 또는 Record Type(레코드 타입)은 필요한 멤버의 이름과 타입을 적는다. `{val a:Int; def b:Int; def f(x:Int):Int}`는 읽을 수 있는 정수 `a`, 인자 없는 정수 메서드 `b`, 정수를 받아 정수를 돌려주는 메서드 `f`를 요구한다. 값 자체, 그 값에 붙는 정적 타입, 그 타입이 허용하는 멤버 사용은 서로 구분한다.

아래는 Part1 PDF p.70의 자료 코드다. `val g`는 객체 안에 저장한 함수 값이고, 맨 아래의 `def g`는 객체를 인자로 받는 별개의 바깥 함수다. [Part1 PDF p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-070)

~~~
import reflect.Selectable.reflectiveSelectable
def bar (x: Int) = x+1
val foo = new {
  val a = 1+2
  def b = a + 1
  def f(x: Int) = b + x
  val g : Int => Int = bar _
}
foo.b
foo.f(3)
val ff : Int=>Int = foo.f _
def g(x: {val a: Int; def b: Int;
          def f(x:Int): Int; val g: Int => Int}) =
  x.f(3)
g(foo)
~~~

식에 따른 계산은 `a=3`, `foo.b=3+1=4`, `foo.f(3)=4+3=7`이다. 바깥 `g(foo)`도 인자 `x`에 `foo`를 받아 `x.f(3)`을 계산하므로 7이다. `foo.f _`는 이 자료에서 메서드를 함수 값으로 사용하는 표기다. `ff`는 그 함수 값을 가리키며, `foo.g`는 `bar _`를 저장한 다른 멤버다. 두 함수가 모두 `Int=>Int`이어도 그 코드와 정의 환경이 같다는 뜻은 아니다.

Type Alias(타입 별칭)는 긴 구조를 다른 이름으로 적는 방법이다. 다음은 별도의 p.71 자료 코드이며, 앞 페이지의 선언에 이어 붙이는 코드가 아니다. [Part1 PDF p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071)

~~~
import reflect.Selectable.reflectiveSelectable
type Foo = {val a: Int; def b: Int; def f(x:Int):Int}

val gn = 0
val foo : Foo = new {
  val a = 3
  def b = a + 1
  def f(x: Int) = b + x + gn
}
foo.f(3)
def g(x: Foo) = {
  val gn = 10
  x.f(3)
}
g(foo)
~~~

`type Foo = ...`는 기존 구조의 별칭이다. 생성자를 가진 새 Nominal Type(명목 타입)을 선언한 것이 아니다. `foo.f`의 자유 이름 `gn`은 그 메서드가 정의된 환경의 `gn=0`을 가리킨다. 호출하는 `g` 안에 같은 철자의 지역 이름 `gn=10`이 있어도 `foo.f`의 정의 환경을 바꾸지 않는다. 따라서 `foo.f(3)`과 `g(foo)`에서 계산하는 값은 모두 `(3+1)+3+0=7`이다. 호출자의 지역 변수를 함수 본문의 자유 변수에 대신 끼워 넣으면 이 Lexical Scope(어휘적 범위)를 잃는다.

p.72는 `f(x)=a+x`를 사용하는 또 다른 자료 코드다. 이 페이지에서 `val foo=new ...` 옆에는 `object foo`라는 대응 표기도 있다. 멤버를 가진 한 값을 만들고 이름을 준다는 연결을 보여 준다. [Part1 PDF p.72](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-072)

~~~
def bar (x: Int) = x+1
val foo = new {
  val a = 2 + 1
  def f(x: Int) = a + x
  val g : Int => Int = bar _
}
val b = foo.f(1)
foo.g(b)
~~~

자료의 환경 표기를 따라 바깥 환경을 `E1`, 객체 멤버 환경을 `E2`라 하자. `bar`의 코드는 `E1`에서 정의되고, `E2`에는 `a=3`, `f(x)=a+x`, `g=(bar의 코드,E1)`이 들어간다. `foo.f(1)`을 적용할 때는 객체의 `a`와 새 인자 `x=1`을 사용하므로 `E1:E2:E3[x=1]`에서 `a+x=3+1=4`이다. 이 값이 바깥 `b`에 저장된다. 이어 `foo.g(b)`는 객체에 저장된 `bar`의 Closure(클로저)를 적용한다. 그 함수는 `E1`과 새 인자 환경 `E4[x=4]`를 사용하여 `x+1=4+1=5`를 준다. 메서드의 자유 멤버를 찾는 환경과 객체 안에 저장된 함수 값의 원래 정의 환경은 이처럼 다를 수 있다. p.70의 `b+x`, p.71의 `b+x+gn`, p.72의 `a+x`는 각각 구분해서 계산해야 한다.

### Algebraic Datatype: Product·Sum·Recursion과 Pattern Matching

Product(곱)는 여러 성분을 함께 요구하고, Sum(합)은 여러 생성자 대안 중 하나를 고른다. Algebraic Datatype, ADT(대수적 자료형)는 이 두 구성을 조합한다. 다음은 Part1 PDF p.73의 자료 선언 표기다. `of`와 `*`는 이 페이지의 자료형 설명 표기이며 Scala 실행문으로 읽지 않는다. [Part1 PDF p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-073)

~~~
Attr = Name of String
     |  Age of Int
     |  DOB of Int * Int * Int
     |  Height of Double
~~~

전체 `Attr`는 `Name`·`Age`·`DOB`·`Height` 중 하나로 만들어지는 Sum이다. 그중 `DOB` 한 경우는 세 `Int`를 모두 함께 갖는 Product다. 예컨대 `DOB(2000,3,10)`을 만들려면 세 성분이 필요하지만, `Age(16)`을 만들 때 `DOB`의 세 성분까지 함께 제공할 필요는 없다. 서로 다른 대안의 필드를 모두 한 값이 가진다고 보는 것이 Sum을 Product로 오해하는 경우다.

Recursive ADT(재귀 대수적 자료형)는 생성자의 성분 타입에 그 자료형 자신이 나타난다. p.74의 자료 선언은 다음과 같다. [Part1 PDF p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-074)

~~~
IList = INil
      |  ICons of Int * IList
~~~

`INil()`은 빈 리스트를 만들고, `ICons(hd,tl)`은 정수 머리 `hd`와 나머지 리스트 `tl`을 함께 넣어 새 리스트를 만든다. 따라서 `ICons(2,ICons(1,INil()))`은 머리 2, 다음 머리 1, 마지막 빈 경우로 이어지는 두 원소 리스트다. ‘재귀’는 이 타입 정의에 자기 타입이 다시 나타난다는 뜻이다. 모든 값이 무한히 크다는 뜻은 아니다. `INil`이라는 기저 경우에서 시작해 유한 번 생성자를 적용하면 유한한 값을 만든다.

p.76의 `BTree = Leaf | Node of Int * BTree * BTree`도 같은 방식으로 읽는다. `Leaf()`는 이 예의 빈 트리이고, `Node(v,l,r)`는 정수 값과 왼쪽·오른쪽 트리를 모두 가진다. `Leaf`와 `Node` 사이가 Sum, `Node` 내부의 값·두 하위 트리 사이가 Product, 두 하위 트리의 타입이 다시 `BTree`라는 점이 Recursion이다. 이는 자료에 근거한 생성 구조 설명이다. [Part1 PDF p.76](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076)

Pattern Matching(패턴 매칭)은 ADT를 어느 생성자로 만들었는지에 따라 나누어 사용하는 Elimination이다. `C(a,b)`로 만들었다면 `case C(x,y) => ...`에서 그 안의 성분을 `x`와 `y`로 사용한다. 전체 식의 결과를 `T`로 설명하려면 가능한 생성자 경우를 처리하고 각 분기의 결과도 `T`로 사용할 수 있어야 한다. [Part1 PDF p.78](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-078)

다음 `IList` 선언은 p.76, `length` 본문은 p.79의 자료 코드다. 생성자 대안과 각 case가 직접 대응한다. [Part1 PDF p.76](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076) [Part1 PDF p.79](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-079)

~~~
sealed abstract class IList
case class INil() extends IList
case class ICons(hd: Int, tl: IList) extends IList

def length(xs: IList) : Int =
  xs match {
    case INil() => 0
    case ICons(x, tl) => 1 + length(tl)
  }
~~~

`INil`이면 셀 수가 0이고, `ICons`이면 현재 셀 하나에 꼬리의 길이를 더한다. `x`의 정수 내용은 길이에 영향을 주지 않는다. 설명용 전개는 다음과 같다.

~~~
length(ICons(2,ICons(1,INil())))
= 1 + length(ICons(1,INil()))
= 1 + (1 + length(INil()))
= 1 + (1 + 0)
= 2
~~~

이 종료 설명에는 구조가 유한하고 각 재귀 호출이 더 작은 꼬리로 진행한다는 조건이 있다. 자기 호출이 있다는 사실만으로 임의의 재귀 프로그램의 종료까지 결론 낼 수는 없다.

Option[T](옵션 타입)는 `T` 값의 부재와 존재를 구별하는 Sum이다. 자료는 Introduction으로 `None`과 `Some(x)`, Elimination으로 Pattern Matching 등을 제시한다. `Some(3)`은 `Option[Int]`로, `Some("abc")`는 `Option[String]`으로 사용할 수 있다. `None`은 두 타입 문맥에서 모두 빈 경우를 나타낸다. `None`이 정수 0이나 빈 문자열을 숨겨 가지고 있다는 뜻은 아니다. [Part1 PDF p.98](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-098)

`Option[T]` 전체에 `T`의 멤버를 곧바로 요구할 수 없는 이유는 `None` 대안에 `T` 값이 없기 때문이다. 먼저 `None`인지 `Some(v)`인지 나누고, `Some`에서 꺼낸 `v:T`에 대해 그 타입이 허용하는 사용을 한다. 설명용 식으로 `o:Option[Int]`의 두 경우를 다루면 다음처럼 적을 수 있다.

~~~
o match {
  case None => 0
  case Some(v) => v + 1
}
~~~

여기서 0은 부재일 때 이 예가 선택한 결과일 뿐 `None`의 내용물이 아니다. `Some` 분기에서는 `v:Int`를 얻었으므로 정수 덧셈을 정당화한다. `Option[MyList[A]]`에서도 먼저 `Some(xs)`에서 `xs:MyList[A]`를 얻어야 한다. 더구나 p.92의 ADT `MyList[A]` 자체도 `MyNil`·`MyCons`의 Sum이므로, 머리 성분을 쓰려면 `MyCons`인지 다시 구분해야 한다. 바깥 `Option`을 벗기는 일과 안쪽 리스트 생성자를 구분하는 일은 서로 다른 단계다. [Part1 PDF p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092)

### Parametric Polymorphism과 타입 매개변수의 한계

Parametric Polymorphism(매개변수 다형성)은 타입을 매개변수로 받아 같은 계산 구조를 여러 타입에 사용하는 방식이다. 다음은 자료의 `id`와 `applyn` 코드다. [Part1 PDF p.90](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-090) [Part1 PDF p.91](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-091)

~~~
def id[A](x: A) : A = x

def applyn[A](f: A => A, n: Int, x: A): A =
  n match {
    case 0 => x
    case _ => f(applyn(f, n - 1, x))
  }

applyn((x:Int)=>x+1,100,3)
~~~

`id[A]`는 `A`의 구체 구조를 조사하지 않고 받은 값을 그대로 돌려준다. `id(3)`에서는 `Int`, `id("abc")`에서는 `String`을 성분 타입으로 사용한다. 자료 표기에서 `id[T] _`는 타입 매개변수를 `T`로 정한 `T=>T` 함수 값이다. 타입을 매개변수로 받는 선언과, 특정 입력·출력 타입을 가진 함수 값을 구분해야 한다.

`applyn`은 `A=>A` 함수를 받아 같은 타입의 결과를 다음 적용에 다시 사용할 수 있게 한다. `n=0`이면 `x`이고, 양의 `n`에서는 먼저 `n-1`번의 결과를 얻은 뒤 `f`를 한 번 더 적용한다. `n>=0`이고 `f`의 각 적용이 결과를 준다는 조건에서 다음 설명용 전개가 성립한다.

~~~
applyn(f,0,x) = x
applyn(f,1,x) = f(x)
applyn(f,2,x) = f(f(x))
applyn((x:Int)=>x+1,100,3) = 3+100 = 103
~~~

자료 코드는 음수 입력을 막는 검사를 따로 두지 않았다. 따라서 ‘100번 반복’의 유도 조건을 버리고 모든 정수 `n`에 대해 같은 종료 설명을 적용해서는 안 된다.

p.92의 `MyOption[A]`·`MyList[A]`·`BTree[A]`도 타입 매개변수에 따라 성분 타입을 바꾸면서 생성 구조를 재사용한다. `MyCons[A](hd:A,tl:MyList[A])`에서는 머리와 꼬리가 같은 `A`를 공유하고, `Node[A](value:A,left:BTree[A],right:BTree[A])`에서도 두 하위 트리는 같은 매개변수의 트리다. `MyList[Int]`와 `MyList[String]`은 다른 성분 타입을 갖지만 빈 경우와 cons 경우라는 계산 구조는 공통이다. `MyOption[A]`도 `MyNone[A]()` 또는 `MySome[A](some:A)`라는 대안을 가지므로, 존재하는 경우의 내용 타입만 `A`에 따라 달라진다. [Part1 PDF p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092)

아무 제약 없는 `A`에서 보장되는 것과 특정 멤버를 요구하는 것은 다르다. `id[A]`는 `A`를 그대로 반환하면 되지만, 임의의 `r:A`에서 `r.name`을 읽으려면 모든 `A`에 그 이름과 알맞은 타입의 멤버가 있어야 한다. `A=Int`만 생각해도 그 요구는 타입 변수 자체에서 나오지 않는다. ‘알려지지 않은 자료형에 대해 프로그램한다’는 Parametric Polymorphism과, 공통 구조를 명시하여 그 구조만 사용하는 Subtype Polymorphism(부분형 다형성)을 이 지점에서 구분한다. [Part1 PDF p.100](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-100)

### Value·Type·Member를 구분하는 greeting의 공통 요구

Part2 자료의 `object tom`은 `name`과 `home`, `object bob`은 `name`과 `mobile` 멤버를 가지며, 각 필드의 값 타입은 `String`이다. `tom`·`bob`은 멤버를 가진 값의 이름이고, `NameHome`·`NameMobile`은 그 구조를 적는 타입 별칭이다. `name`은 그 값에서 선택하여 읽는 멤버다. 서로 다른 레코드 타입이라도 `name:String`을 읽는 연산은 공통으로 제공할 수 있다. [Part2 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-003) [STT 07:00] [STT 09:21]

다음은 Part2 PDF p.4의 공통 요구를 나타내는 자료 코드다. [Part2 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-004)

~~~
import reflect.Selectable.reflectiveSelectable
type NameHome = { val name: String; val home: String }
type NameMobile = { val name: String; val mobile: String}
type Name = { val name: String }

def greeting(r: Name) = "Hi " + r.name + ", How are you?"
greeting(tom)
greeting(bob)
~~~

`greeting` 본문은 `home`도 `mobile`도 사용하지 않는다. 요구를 `NameHome`으로 정하면 `home`이 없는 `bob`을 받아들일 근거가 없어지고, `NameMobile`로 정하면 `tom` 쪽에 같은 문제가 생긴다. `Name`은 필요한 `name:String`만 요구하므로 다음 두 관계로 두 값을 모두 받아들인다.

~~~
NameHome <: Name
NameMobile <: Name
~~~

이것이 하나의 코드를 서로 다른 입력 타입에 사용하는 Subtype Polymorphism이다. `type Name=...`는 구조의 별칭이고, `object tom`은 여기서 특정 값을 이름 붙여 선언하는 표기다. Part1 p.72의 `new`·`object` 대응은 이 값 생성의 연결을 설명하지만, singleton이나 초기화·컴파일의 모든 세부가 언제나 같다는 뜻까지 주지는 않는다. [Part2 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-004) [Part1 PDF p.72](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-072) [STT 08:21] [STT 16:45]

Member Checking(멤버 검사)에서는 이름과 타입을 함께 본다. `r:Name`이면 `r.name:String`을 얻지만, 그 정적 타입만으로 `r.home`이나 `r.mobile`까지 사용할 수는 없다. 원래 값에 추가 멤버가 있어도 공개된 타입이 그 멤버를 보장하지 않을 수 있다. 반대로 `{val name:Int}`는 이름만 일치할 뿐 `name:String`이라는 요구를 충족하지 않는다. 임의의 `A`를 받는다는 표기만으로도 이 요구는 생기지 않는다. `greeting`의 자료 식에 `r.name`을 대입하면 `tom`에서는 `"Hi Tom, How are you?"`, `bob`에서는 `"Hi Bob, How are you?"`라는 문자열 계산을 설명할 수 있다. 이는 자료 식의 전개이며 불명확한 실시간 출력의 복원이 아니다.

### Subtype은 허용된 Elimination의 보존이다

`T <: S`는 `T`의 모든 값을 `S`의 값처럼 사용할 수 있다는 관계다. 왼쪽의 값을 오른쪽 타입을 요구하는 자리에 공급하는 방향으로 읽는다. 자료는 “can be used as”를, 집합의 부분집합에서 말하는 문자 그대로의 원소 소속과 구분한다. 두 타입의 표현이나 메모리 배치가 같다고 먼저 가정하는 정의가 아니다. [Part2 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-005)

Elimination 관점에서 `S`가 허용하는 사용을 확인하면 관계를 구체적으로 이해할 수 있다. `Name`의 소비자는 `.name`을 통해 `String`을 읽는다. `NameHome` 값에도 그 읽기 멤버가 있으므로 그 사용을 지원한다. 반대로 `Int`를 `Name`처럼 받아 놓고 `.name`을 요구하는 데에는 같은 근거가 없다. 특정 한 호출이 우연히 해당 멤버를 쓰지 않는 것과, 그 타입이 허용하는 사용을 일반적으로 보존하는 것도 구분해야 한다. [STT 20:00] [STT 22:40] [STT 24:28]

Type Checking(타입 검사)에서 식 `t`가 `T` 타입이고 `T <: S`이면, `S`가 요구되는 자리에서 `t`를 사용할 수 있다고 설명한다. 이때 관계는 타입 `T`와 `S` 사이에 있다. `a`·`b` 같은 값 이름끼리 Subtype 관계를 적는 것이 아니다. `t:S`로 보아도 된다는 사실은 `t`가 `S`만을 위해 새로 만들어졌다거나 내부 데이터가 삭제되었다는 뜻도 아니다.

`h:S=>R`가 `S`의 허용된 연산만으로 결과 `R`을 만든다고 하자. `T <: S`이면 `T`를 받아도 그 입력을 `S`처럼 사용할 수 있으므로 `h`는 `T=>R`을 요구하는 자리에서도 쓰인다. 따라서 다음 관계를 얻는다. 이는 뒤에서 유도할 함수 입력의 반대 방향을 이미 포함한다. [Part2 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-005)

~~~
T <: S
따라서 (S=>R) <: (T=>R)
~~~

이 사용 가능성은 정적 타입이 허용하는 연산에 관한 근거다. 객체의 물리적 표현, 성능, 업무상의 의미나 별도 계약까지 자동으로 같아진다는 보장은 아니다.

### Structural·Nominal Subtyping의 판정 근거

Structural Subtyping(구조적 부분형)은 필요한 멤버 이름과 타입으로 관계를 정한다. `NameHome`의 구조를 풀어 보면 `Name`이 요구하는 `name:String`이 있고, 나열 순서는 그 요구의 본질이 아니다. 같은 구조를 가리키는 별칭을 두 개 적었다면 별칭 이름의 철자보다 풀어 쓴 구조가 판정의 근거다. 자료는 이를 Duck Typing이라고도 부른다. 여기서의 초점은 필요한 사용을 제공하는 구조인지이며, 이 별칭만으로 검사가 반드시 런타임에 이루어진다고 결론 내릴 수는 없다. [Part2 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-007) [STT 39:55] [STT 40:53]

Nominal Subtyping(명목적 부분형)은 이름을 가진 타입 사이에 명시한 관계를 사용한다. 별개의 클래스 `A`와 `B`를 선언하여 멤버 모양이 같아졌다는 사실만으로 `B <: A`가 생기지는 않는다. `B`가 `A`를 상속한다고 `extends` 등으로 명시하는 관계가 필요하다. 선언했다고 임의의 불일치가 모두 허용된다는 뜻은 아니며, 허용 조건과 부모 타입을 요구하는 사용도 만족해야 한다. [STT 43:41] [STT 45:36]

따라서 `type Name={val name:String}`처럼 기존 구조를 줄여 쓰는 것과 `class`로 명목 타입을 정의하는 것은 다르다. 구조적 별칭 둘은 구조로 비교하고, 명목 클래스 둘은 타입 이름과 선언된 관계를 함께 확인한다. 자료가 Nominal Sub Types에 붙인 Ad hoc Polymorphism이라는 명칭은 이 대비의 용어로 읽는다. [Part2 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-007)

### Reflexivity·Transitivity와 관계의 방향

Reflexivity(반사성)는 모든 타입 `T`에 대해 `T <: T`라는 규칙이다. 같은 타입을 요구하는 자리에 그 타입의 값을 쓰는 데에 추가 변환 관계가 필요하지 않다. Transitivity(추이성)는 중간 타입을 통해 사용 가능성을 연결한다. [Part2 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-009) [STT 48:24]

~~~
T <: T

T <: R    R <: S
----------------
T <: S
~~~

`T`의 값을 `R`처럼 사용할 수 있고, `R`에 허용된 사용이 `S`의 요구도 충족한다면, `T`의 값을 `S`를 요구하는 자리에서 사용할 수 있다. 이 결론은 `T <: S`이며 `S <: T`가 아니다. 예컨대 `{val name:String;val home:String} <: {val name:String}`이라고 해서 `name`만 있는 값에서 `home`까지 읽을 수는 없다. 반사성도 자기 타입과의 관계만 주므로 이 역방향을 보충하지 않는다. 중첩 레코드에서는 순서를 바꾼 중간 타입, 안쪽 요구를 줄인 타입을 각각 정당화한 다음 추이성으로 연결한다.

### Read-only Record의 Permutation·Width·Depth

이 절의 레코드 멤버는 읽기 전용 `val`이다. Permutation(순열)은 같은 이름·같은 타입의 멤버를 다른 순서로 나열해도 그 요구를 충족한다는 규칙이다. `{val x:Int;val y:String}`와 `{val y:String;val x:Int}`는 같은 읽기 멤버를 제공한다. 순서를 교환하는 것은 `x`와 `y`의 이름이나 타입을 서로 바꾸는 것이 아니다. 반대 순열도 적용할 수 있지만, 그 사실이 임의의 Subtype 관계 전체의 대칭성을 뜻하지는 않는다. [Part2 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011) [STT 01:00:01]

Width(너비)는 필드가 더 많은 쪽을 일부 필드만 요구하는 자리에 쓸 수 있다는 규칙이다.

~~~
{val name:String; val home:String} <: {val name:String}
~~~

오른쪽의 소비자는 `name`만 읽으면 되고 왼쪽 값은 그 사용을 제공한다. `home`이 추가된 것은 문제가 없지만, 반대로 `name`만 있는 값은 `home`을 요구하는 모든 사용을 지원하지 못한다. Width는 실제 객체에서 필드를 삭제하라는 명령이 아니라 정적으로 요구하는 멤버를 줄이는 관계다. [Part2 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011)

Depth(깊이)는 같은 읽기 필드의 타입에 있는 Subtype 관계를 바깥 레코드로 올린다.

~~~
T <: S
-----------------------------------
{val x:T; ...} <: {val x:S; ...}
~~~

왼쪽 값에서 `.x`를 읽으면 `T`를 얻고, `T <: S`에 의해 그 결과를 `S`처럼 쓸 수 있다. 따라서 오른쪽 소비자가 `x:S`에서 허용된 연산을 해도 된다. 이름이 같다는 조건만으로는 충분하지 않으며, 필드 결과 타입의 관계가 필요하다. [STT 01:01:26]

자료의 중첩 예를 다음과 같이 축약하자. `A`·`B`·`C`는 유도를 위한 설명용 이름이다. [Part2 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-012)

~~~
A = {val x:{val y:Int;val z:String};val w:Int}
B = {val w:Int;val x:{val y:Int;val z:String}}
C = {val w:Int;val x:{val z:String}}
~~~

먼저 바깥 필드 순서만 바꾸는 Permutation으로 `A <: B`를 얻는다. 그다음 안쪽 레코드에 Width를 적용한다.

~~~
{val y:Int;val z:String} <: {val z:String}
~~~

이 안쪽 관계를 `x`의 Depth로 올리면 `B <: C`다. `w:Int`는 반사성으로 그대로 두고, `x`가 제공하는 값만 더 작은 요구 구조로 노출한다. 추이성으로 `A <: C`를 얻는다. `C`의 소비자가 `r.w`를 읽으면 정수를 얻고, `r.x.z`를 읽으면 문자열을 얻는다. `A`의 값은 이 두 사용을 모두 지원한다. `y`는 `x` 안쪽의 필드이므로 바깥 Width 한 번으로 없앴다고 설명하면 적용 층위를 잘못 짚는다.

쓰기 가능한 `var`에는 같은 Depth 방향을 자동 적용할 수 없다. 설명용 반례로 `NameHome <: Name`을 생각하자. `var x:NameHome`인 저장 위치를 `var x:Name`으로 허용하면, 넓어진 쪽의 사용자가 `name`만 있는 값을 `x`에 써 넣을 수 있다. 원래 쪽은 여전히 `x.home`을 읽을 수 있다고 기대하므로 보장이 깨진다. 읽기에서는 더 구체적인 값을 넓은 타입으로 보아도 되지만, 쓰기까지 허용하면 들어올 값의 조건도 검토해야 한다. 이는 자료의 읽기 필드 규칙을 가변 필드로 확대하지 않기 위한 설명용 반례다.

### Table Lookup·Fixed Offset은 구현 가설이다

구조적으로 같은 사용이 가능하다는 규칙과 그 사용을 실제 코드로 구현하는 방법은 별개의 질문이다. STT는 하나의 `greeting` 코드를 서로 다른 구조에 어떻게 적용할지 묻고, 필드 이름과 내용을 표처럼 두는 모형을 제안한다. `r.name`에서 표를 검색하여 `name`에 대응하는 값을 찾는다고 생각하면, 추가 필드 수나 나열 순서가 달라도 같은 이름 찾기 연산을 설명할 수 있다. 그 모형에서는 이름 저장 공간과 검색 작업이 필요할 수 있다. [STT 28:13] [STT 30:07] [STT 32:07]

다른 모형은 타입별 저장 순서가 고정되어 있을 때 `.name`을 정해진 칸 읽기로 바꾸는 것이다. 이때 ‘각 레코드를 선언된 순서대로 저장하고, 모든 `Name`의 Subtype에서도 `name`이 첫 칸에 있다’는 가정을 추가하면 문제가 생긴다. 설명용 구조 `{val home:String;val name:String}`도 Permutation과 Width에 따라 `Name`의 Subtype인데, 그 가상의 저장 규칙에서는 첫 칸이 `home`이기 때문이다. 첫 칸만 읽으면 요구한 `name`을 얻는다는 논증이 성립하지 않는다. [Part2 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011) [STT 32:54] [STT 34:31]

이는 그 단순한 배치 가정의 반례다. 다른 표현이나 컴파일 방법을 모두 배제한 것이 아니므로 런타임 검색이 필수라고 증명한 것도 아니다. 강사는 실제 구현을 잘 모르겠다고 유보하고, 코드 생성 횟수에 대한 처음 생각도 뒤에서 다시 검토한다. 포인터 폭, 필드 압축 수치, 항상 발생하는 비용, 상속의 성능 우위는 이 설명에서 확인된 구현 사실로 쓰지 않는다. [STT 36:23] [STT 37:00] [STT 38:55]

### Tuple Subtyping의 같은 Arity와 위치 조건

Tuple Subtyping(튜플 부분형)에서 제시된 규칙은 같은 Arity를 유지하면서 같은 위치의 성분 타입에 Depth를 적용하는 것이다. [Part2 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-013)

~~~
T <: S
-----------------------------
(...,T,...) <: (...,S,...)
~~~

STT는 우선 성분 개수가 같은 튜플을 다룬다는 조건을 두 번 강조한다. 나머지 위치의 타입은 그대로 두고 한 위치를 넓힐 수 있으며, 여러 위치에 적용하려면 각 위치의 관계를 확인하고 단계를 연결한다. 튜플 성분은 이름 대신 위치로 선택하므로 어느 성분이 `._1`이고 `._2`인지 유지해야 한다. [STT 01:04:12] [STT 01:04:58]

설명용 유도로 `Int <: Any`를 두 번째가 아닌 첫째·셋째 위치에 차례로 적용하면 다음 관계를 얻는다.

~~~
(Int,String,Int) <: (Any,String,Int) <: (Any,String,Any)
~~~

두 단계 모두 세 성분이며 가운데 `String` 위치는 바뀌지 않는다. 반면 `(Int,String,Int) <: (Int,String)`은 이 규칙에서 나오지 않는다. 마지막 성분을 버리고 싶다면 새 튜플 `(t._1,t._2)`를 구성하는 별도 계산을 설명할 수는 있지만, 그것을 여기서 제시한 Subtype 규칙이라고 부를 근거는 없다. 또한 `(Int,String)`을 단순히 순서를 바꾸어 `(String,Int)`로 취급하면 첫 위치를 문자열로 쓰는 소비자에게 정수를 주게 된다. 레코드의 이름 기반 Permutation과 튜플의 성분 재배열은 같은 일이 아니다. 더 긴 튜플도 허용할 수 있겠다는 강의 중 생각은 제시된 같은-Arity 규칙과 구분한다.

### Function Subtyping: 입력 Contravariance와 출력 Covariance

Function Subtyping(함수 부분형)은 입력과 출력을 같은 방향으로 바꾸는 규칙이 아니다. 자료의 전제와 결론은 다음과 같다. [Part2 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

~~~
T <: T'     S <: S'
---------------------------
(T'=>S) <: (T=>S')
~~~

오른쪽 `T=>S'`를 보고 함수를 쓰는 사람은 `T`를 인자로 공급하고, 받은 결과를 `S'`로 사용한다. 대체하여 넣는 왼쪽 실제 함수는 `T'`를 요구한다. `T <: T'`이므로 사용자가 공급한 `T`는 그 입력 요구를 충족한다. 실제 함수가 `S`를 반환하면 `S <: S'`에 의해 사용자는 그 결과를 약속된 `S'`로 쓸 수 있다. 입력과 결과의 두 사용을 모두 보존하므로 전체 함수의 대체가 성립한다. [STT 01:06:53] [STT 01:08:47]

입력 쪽은 `T <: T'`에 대해 함수 관계에서 `T'`가 왼쪽에 오는 Contravariance(반공변)다. 출력 쪽은 `S <: S'`와 같은 방향인 Covariance(공변)다. 한쪽씩 분리하면 다음처럼 유도한다.

~~~
T <: T'
---------------------------
(T'=>S) <: (T=>S)

S <: S'
---------------------------
(T=>S) <: (T=>S')

Transitivity:
(T'=>S) <: (T=>S) <: (T=>S')
~~~

입력 반공변의 설명용 반례로 `NameHome <: Name`을 사용하자. `NameHome`을 받아 `r.home`까지 읽는 함수는 `Name`만 받는다고 약속한 자리에 일반적으로 넣을 수 없다. 그 약속을 믿은 사용자는 `name`만 있는 값을 줄 수 있고, 그때 실제 함수에 필요한 `home`이 없다. 반대로 `name`만 읽는 `Name` 입력 함수는 `NameHome` 값을 공급하는 사용자를 받아들일 수 있다. 사용자가 추가 정보를 주어도 함수는 자신이 요구한 부분만 사용한다.

출력 공변도 반례로 확인할 수 있다. `XY={val x:Int;val y:Int}`, `X={val x:Int}`라 하면 `XY <: X`다. `XY`를 돌려주는 함수는 `X` 결과만 기대하는 자리에서 사용해도 `.x`를 제공한다. 반대로 `X`만 반환하는 함수를 `XY` 결과를 약속하는 자리에 넣으면 사용자가 `.y`를 읽을 때 그 요구를 보장하지 못한다. 입력에서 ‘더 많이 요구하는 함수’와 출력에서 ‘더 적게 제공하는 함수’가 왜 위험한지 각각 확인해야 한다.

강의는 입력을 주어진 값의 Elimination, 출력을 결과를 만드는 Introduction이라는 관점에서 비교한다. 함수 `A=>B`의 본문은 `A`를 사용할 수 있다는 가정 아래 `B`를 만든다. 이를 ‘`A`를 가정하여 `B`를 얻는다’는 함의의 모습과 연결할 수 있지만, 이 비교만으로 프로그래밍과 수학 전체가 완전히 동일하다는 일반 정리가 성립하는 것은 아니다. [STT 01:11:03] [STT 01:12:03]

### Any·Nothing: Top·Bottom의 생성과 사용 한계

자료는 `Nothing`을 값이 없는 타입, `Any`를 모든 값을 받아들이는 타입으로 소개한다. 모든 타입 `T`에 대해 다음 관계를 둔다. 이때 Top(최상위)·Bottom(최하위)은 Subtype 관계의 양끝을 가리킨다. [Part2 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010)

~~~
Nothing <: T <: Any
~~~

`Nothing`에는 정상적인 값을 만드는 Introduction이 없다. 따라서 ‘`Nothing`의 모든 값은 `T`처럼 사용할 수 있다’는 명제에 실제 값을 골라 실패를 보이는 반례도 없다. 값이 없다는 전제에서 이 전칭 명제는 Vacuous Truth(공허하게 참)로 성립한다. `Nothing` 값을 이미 받았다고 가정한다면 어떤 결과 타입을 요구하는 자리에서도 그 값을 사용할 수 있다는 Elimination 관점도 같은 경계를 표현한다. 불가능한 가정을 다루는 것과 정상 값을 만들어 공급할 수 있다는 것은 다르다. [STT 53:17] [STT 57:15]

아래는 p.10의 자료 코드다. [Part2 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010)

~~~
val a : Int = 3
val b : Any = a
def f(a: Nothing) : Int = a
~~~

`f` 본문의 매개변수 `a`는 `Nothing`이고 `Nothing <: Int`이므로 `Int`가 요구되는 결과 자리에 쓸 수 있다. 이 타입 관계는 정상적으로 구성된 `Nothing` 인자를 확보해 주지 않는다. 예외를 던지거나 발산하는 `Nothing` 타입 식을 생각하더라도, 그 식이 정상 종료하여 `f`에 전달할 값을 반환한다는 뜻이 아니다. 빈 ADT의 생성자 경우가 0개라는 강의의 case 분석 비유도 이런 불가능한 입력 가정의 설명으로 읽는다. 특정 빈 `match` 구문의 문법이나 컴파일 성공까지 이 비유에서 얻지는 못한다.

`Any` 쪽은 여러 타입의 값을 받아들이는 대신 특정 구조에 관한 정보가 약해진다. 자료의 첫 `a`는 `Int`이고 `Int <: Any`이므로 `b:Any`에 공급할 수 있다. 하지만 `b`의 정적 타입 `Any`만 보고 정수 전용 계산을 하거나 `.name`을 읽을 근거는 없다. `Any`에는 정수 이외 값도 들어올 수 있기 때문이다. 실제로 그 식에 3을 넣었다는 계산 설명과, `Any`를 받는 임의의 코드가 사용할 수 있는 정적 정보는 구분한다. [STT 55:17] [STT 58:07] [STT 59:05]

강의의 ‘`Any`에는 Elimination이 없다’는 표현은 이 대비에서 정수나 레코드 같은 특정 자료형의 연산을 마음대로 요구할 수 없다는 뜻으로 한정한다. 모든 Scala 공통 연산이 존재하지 않는다는 주장으로 확대하지 않는다. `Nothing`을 값 없음, `Any`를 넓은 수용 범위로 이해하면 `Any <: Int`나 `Int <: Nothing`을 같은 논리로 역추론할 수 없는 이유도 분명하다.

Function Subtyping과 결합한 설명용 유도로, 임의의 타입 `P`·`R`에 대해 다음 관계를 얻는다.

~~~
P <: Any, Nothing <: R
따라서 (Any=>Nothing) <: (P=>R)

Nothing <: P, R <: Any
따라서 (P=>R) <: (Nothing=>Any)
~~~

첫 관계는 입력을 더 넓게 받고 결과를 더 좁게 제공하는 방향, 두 번째는 그 반대쪽 경계 타입을 요구하는 방향이다. 이것들은 타입 규칙의 유도이지 `Any=>Nothing` 함수가 모든 입력에서 정상 종료하여 결과 값을 만들어 낼 수 있다는 존재 증명이 아니다. 또 `Nothing=>Any`를 사용할 정상적인 `Nothing` 입력이 생겼다는 뜻도 아니다. [Part2 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010) [Part2 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

### AB=>XY를 ABC=>X로 사용하는 함수 값

다음은 Part2 PDF p.14의 자료 코드다. `foo`는 입력 필드를 읽어 이름이 다른 결과 필드를 가진 새 객체를 만든다. [Part2 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

~~~
import reflect.Selectable.reflectiveSelectable
def foo(s: {val a: Int; val b: Int}) : {val x: Int; val y: Int} = {
  object tmp {
    val x = s.b
    val y = s.a
  }
  tmp
}
val gee: {val a: Int; val b: Int; val c: Int} => {val x: Int} =
  foo _
~~~

타입의 구조를 설명하기 위한 축약을 다음과 같이 두자.

~~~
AB  = {val a:Int;val b:Int}
ABC = {val a:Int;val b:Int;val c:Int}
XY  = {val x:Int;val y:Int}
X   = {val x:Int}
~~~

`foo:AB=>XY`는 `s.b`를 새 객체의 `x`로, `s.a`를 `y`로 설정한다. 입력 `a`·`b`의 나열 순서만 바꾸는 Permutation이 아니다. 필드의 이름이 `x`·`y`인 새로운 결과 레코드를 구성하는 계산이다. 강의에서도 처음 순서 변경처럼 말하다가 바로 이 새 값 생성 설명으로 고친다. [STT 01:16:31]

`gee:ABC=>X` 자리에 `foo _`를 쓰는 근거는 두 Width 관계에서 출발한다.

~~~
ABC <: AB
XY <: X
~~~

일반 함수 규칙의 `T=ABC`, `T'=AB`, `S=XY`, `S'=X`를 대입하면 다음 결론이 나온다.

~~~
(AB=>XY) <: (ABC=>X)
~~~

`gee`의 사용자는 `a`·`b`·`c`를 제공한다. 실제 함수 `foo`는 그중 `a`·`b`만 필요하므로 입력을 사용할 수 있다. 결과에는 `x`·`y`가 모두 있고, 사용자는 `X`라는 약속에 따라 `x`만 읽으면 된다. 사용자가 읽는 `x`의 값은 원래 입력의 `b`다. 설명용으로 `a=2,b=9,c=100`인 값을 공급하면 `foo`의 결과는 `x=9,y=2`이고, `gee`를 통해 허용된 `.x` 읽기는 9를 얻는다. 이는 코드 식의 계산이며 실제 시연 출력을 채운 것이 아니다. [STT 01:17:32] [STT 01:18:32]

`c`를 사용하지 않아도 되는 것과 `foo`가 `c`까지 처리한다는 것은 다르다. 또한 `gee`의 결과 타입에서 `y`가 요구되지 않는다고 해서 결과 객체에서 `y`를 물리적으로 삭제한 것은 아니다.

역방향 `(ABC=>X) <: (AB=>XY)`는 일반적으로 성립하지 않는다. 설명용 반례로 `c`를 읽어 `x`로 반환하는 함수를 생각하면, `AB`만 줄 수 있다고 약속한 사용자는 필요한 `c`를 공급하지 않을 수 있다. 결과 측에서도 `X`만 주는 함수에는 `y`가 없을 수 있다. 입력 문제와 결과 문제 중 하나만 발생해도 대체가 정당하지 않다. 따라서 ‘필드가 많으니 함수도 같은 방향’이라는 암기 대신, 사용자가 무엇을 주고 무엇을 읽는지를 양쪽에서 확인해야 한다.

### Higher-order Function에서 반복되는 방향 유도

Higher-order Function(고차 함수)은 함수 값을 인자나 결과로 다룬다. Function Subtyping 규칙은 이 경우에도 입력·결과 전체 타입에 적용한다. 다음은 앞의 자료 규칙에서 유도한 설명용 사례이며 새로운 구두 발화나 시연 코드가 아니다. [Part2 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

~~~
F = AB=>XY
G = ABC=>X
F <: G
~~~

먼저 함수 값을 반환하는 경우를 보자. `makeF:P=>F`가 있다면 `P` 입력을 받아 만든 `F`를 `G`처럼 사용할 수 있다. 입력 타입 `P`는 반사성으로 같게 두고, 결과에 `F <: G`를 적용한다.

~~~
P <: P    F <: G
-----------------------
(P=>F) <: (P=>G)
~~~

따라서 `makeF`는 `P=>G`를 요구하는 자리에 사용될 수 있다. 실제로 나온 함수에 사용자가 `ABC`를 주면, 안쪽 실제 함수는 `AB`만 읽어 `XY`를 만들고 사용자는 `X`만 쓰므로 앞의 설명이 그대로 성립한다. `=>`가 중첩되면 괄호를 써서 `P=>(AB=>XY)`와 `P=>(ABC=>X)` 중 어느 입력·출력을 비교하는지 표시한다.

이제 함수 값을 받는 경우에는 바깥 입력의 방향이 뒤집힌다. `consumeG:G=>Int`는 `G`라는 약속으로 함수 값을 사용한다. `F <: G`이므로 사용자가 `F`를 주어도 그 값을 `G`처럼 쓸 수 있다.

~~~
F <: G    Int <: Int
---------------------------
(G=>Int) <: (F=>Int)
~~~

예를 들어 `consumeG`는 받은 함수에 `ABC`를 공급하고 결과의 `x`를 읽는 사용을 할 수 있다. `F`인 `foo`를 주어도 입력의 `a`·`b`를 사용하고 `x`를 제공하므로 이 요구를 지원한다. 반대로 `F=>Int`인 소비자는 `AB`만 공급하거나 반환값의 `y`까지 읽을 수 있다. 그 소비자에게 임의의 `G`를 주면 그 함수가 `c`를 필요로 하거나 `y`를 돌려주지 않을 수 있다. 따라서 소비자 타입의 역방향을 자동으로 허용할 수 없다.

함수 입력 안에 함수 입력이 한 번 더 중첩되면 규칙을 두 번 적용한다. 위에서 얻은 `(G=>Int) <: (F=>Int)`를 새 입력 관계로 삼으면 다음이 성립한다.

~~~
(F=>Int)=>Int <: (G=>Int)=>Int
~~~

바깥 함수의 실제 입력은 `F=>Int`이고, 공개된 사용자가 주는 것은 그 Subtype인 `G=>Int`다. 결과 `Int`는 그대로다. 두 번의 입력 위치를 지나면서 방향이 두 번 뒤집힌다. 이는 `F`와 `G`의 내부 구조를 다시 추측한 결과가 아니라, 이미 증명한 함수 타입 관계를 또 하나의 타입 관계로 사용한 유도다.

입력과 결과에 함수 타입이 동시에 있는 경우도 전제를 분리하면 된다.

~~~
G=>Int <: F=>Int     F <: G
-----------------------------------------
((F=>Int)=>F) <: ((G=>Int)=>G)
~~~

오른쪽 약속을 믿는 사용자는 `G=>Int`인 소비자를 주고 `G`인 결과를 기대한다. 왼쪽 실제 함수는 그 소비자를 `F=>Int`처럼 사용할 수 있고, 자신이 반환한 `F`는 `G`처럼 쓰인다. 각 화살표의 입력과 결과를 구분하여 관계를 적용하는 것이 중첩된 타입에서도 같은 대체 가능성을 유지하는 근거다.

## 회상·연습문제

### 회상

#### 회상 Q01 Introduction·Elimination과 위치별 타입

Introduction과 Elimination의 차이를 설명하라. t=(1,"a",10), f=(x:Int)=>x+1이라 할 때 다음을 각각 분류하고, 사용 식의 값과 타입을 구하라: t를 만드는 식, t._2, f를 만드는 식, f(t._3). Tuple의 Arity와 위치별 타입은 무엇이며, 레코드의 .name 접근과 무엇이 다른가?

<details><summary>정답</summary>

Introduction은 값을 만드는 방법이고 Elimination은 이미 있는 값을 사용하는 방법이다. 메모리에서 값을 지운다는 구분이 아니다.

(1,"a",10)은 Tuple의 Introduction이며 타입은 (Int,String,Int), Arity는 3이다. t._2는 두 번째 성분을 꺼내는 Projection이므로 Elimination이고 값은 "a", 타입은 String이다. 세 위치의 타입은 차례로 Int, String, Int이므로 서로 같을 필요가 없다.

(x:Int)=>x+1은 Int=>Int 함수 값의 Introduction이다. f(t._3)에서는 먼저 Tuple Elimination으로 t._3=10:Int를 얻고, 함수 Elimination인 적용으로 f(10)=10+1=11:Int를 얻는다. 함수의 입력 타입 Int와 인자의 타입이 맞는다.

Tuple은 위치로 고르고 레코드는 멤버 이름으로 고른다. ._2를 .name처럼 이름에 무관한 위치 교환으로 이해해서는 안 된다. 확인할 점은 생성 두 가지와 사용 두 가지를 구분하고, t._2와 f(t._3)의 타입까지 쓰는 것이다.

</details>

#### 회상 Q02 Structural Type·Alias와 정의 환경

Structural Type과 type alias가 무엇을 정하는지 설명하라. 아래 세 경우는 서로 독립된 자료 예다. 각 계산을 전개하고 메서드의 멤버 환경과 저장된 함수 값의 정의 환경을 구분하라.

1. Part1 p.70: bar(x)=x+1, foo.a=1+2, foo.b=a+1, foo.f(x)=b+x, foo.g=bar _이다. foo.b, foo.f(3), 바깥 g(foo)를 구하라. 바깥 g(x)는 x.f(3)을 계산한다. ff=foo.f _와 foo.g, 바깥 g는 같은 binding인가?
2. p.71: type Foo={val a:Int;def b:Int;def f(x:Int):Int}, 바깥 gn=0, foo.a=3, foo.b=a+1, foo.f(x)=b+x+gn이다. g(x:Foo)의 지역 gn=10에서 x.f(3)을 호출하면 무엇이 되는가?
3. p.72: 바깥 E1에서 bar(x)=x+1을 정의하고 객체 E2에 a=2+1, f(x)=a+x, g=bar _를 둔다. b=foo.f(1) 뒤 foo.g(b)의 값을 환경과 함께 추적하라.

<details><summary>정답</summary>

Structural Type은 필요한 멤버 이름과 타입을 정한다. 예를 들어 Foo는 읽기 정수 a, 정수 결과의 인자 없는 메서드 b, Int를 받아 Int를 주는 f를 요구한다. type Foo=...는 이 구조의 별칭이며 생성자를 가진 새 Nominal Type을 만드는 선언은 아니다.

1. p.70에서 a=3, foo.b=3+1=4, foo.f(3)=4+3=7이다. 바깥 g(foo)도 x에 foo를 주어 x.f(3)을 호출하므로 7이다. ff는 객체의 f 메서드를 함수 값으로 사용하는 표기이고, foo.g는 bar의 함수 값을 저장한 멤버다. 바깥 g는 객체를 받는 다른 함수다. ff와 foo.g가 모두 Int=>Int이어도 코드와 환경까지 같지는 않다.
2. p.71의 f는 정의 환경의 gn=0을 사용한다. 따라서 b+x+gn=(3+1)+3+0=7이다. 호출자 g의 지역 gn=10은 f의 자유 이름 gn의 binding을 바꾸지 않는다. Lexical Scope에 따라 foo.f(3)과 g(foo)는 모두 7이다.
3. p.72의 E2에는 a=3과 f의 코드, 그리고 g=(bar의 코드,E1)이 있다. foo.f(1)은 E1:E2:E3[x=1]에서 a+x=3+1=4를 계산하여 바깥 b=4를 만든다. foo.g(b)는 저장된 Closure를 적용하므로 E1:E4[x=4]에서 x+1=4+1=5를 얻는다. f는 객체의 a를 쓰고, g에 저장한 함수는 bar의 원래 환경을 쓴다.

확인할 점은 p.70의 b+x, p.71의 b+x+gn, p.72의 a+x를 합치지 않는 것이다. 결과 숫자만 맞추고 호출자의 지역 변수를 정의 환경에 끼워 넣는 설명은 충분하지 않다.

</details>

#### 회상 Q03 Product·Sum·Recursion과 두 단계 case 분석

자료의 Attr=Name of String | Age of Int | DOB of Int * Int * Int | Height of Double, IList=INil | ICons of Int * IList, BTree=Leaf | Node of Int * BTree * BTree에서 Product·Sum·Recursion이 어디에 있는지 설명하라. of와 *는 자료형 설명 표기다.

length(INil())=0, length(ICons(x,tl))=1+length(tl)로 length(ICons(2,ICons(1,INil())))를 전개하고 종료 설명의 조건을 쓰라. Option[T]의 생성과 사용을 설명하고, Option[MyList[A]]에서 머리 성분을 쓰려면 어떤 case들을 구분해야 하는지 쓰라.

<details><summary>정답</summary>

Attr의 Name·Age·DOB·Height 중 하나를 선택하는 부분이 Sum이고, DOB 한 경우가 세 Int를 함께 담는 부분이 Product다. Age 값을 만들 때 다른 생성자의 필드까지 함께 넣을 필요는 없다.

IList의 INil과 ICons가 Sum, ICons의 Int 머리와 IList 꼬리가 Product다. 꼬리 타입에 IList 자신이 나타나므로 Recursive ADT다. BTree에서도 Leaf와 Node가 Sum이고, Node의 정수 값·왼쪽 트리·오른쪽 트리가 Product다. 두 하위 트리의 타입이 BTree이므로 재귀적이다. 기저 생성자에서 유한 번 구성한 값은 유한하다.

~~~
length(ICons(2,ICons(1,INil())))
= 1 + length(ICons(1,INil()))
= 1 + (1 + length(INil()))
= 1 + (1 + 0)
= 2
~~~

머리 값 2와 1의 크기는 길이 계산에 영향을 주지 않는다. 유한한 구조에서 매번 더 작은 꼬리로 진행한다는 것이 종료 근거다. 자기 호출이 있다는 이유만으로 임의의 재귀 프로그램도 종료한다고 할 수는 없다.

Option[T]는 None 또는 Some(v)로 도입하며, Pattern Matching으로 두 대안을 나누어 사용한다. Some(3)은 Option[Int], Some("abc")는 Option[String]으로 쓸 수 있다. None은 두 문맥 모두의 부재 경우이며 숨겨 둔 0이나 빈 문자열이 아니다.

Option[MyList[A]]에서는 먼저 None과 Some(xs)를 구분한다. None에는 리스트가 없고, Some에서만 xs:MyList[A]를 얻는다. 이어 MyNil()과 MyCons(hd,tl)을 구분해야 한다. MyNil에는 머리가 없고, MyCons에서만 hd:A와 tl:MyList[A]를 얻는다. 바깥 Some을 한 번 벗겼다는 사실만으로 안쪽 리스트가 비어 있지 않다고 결론 낼 수 없다. 각 case의 결과를 하나의 타입으로 쓰려면 모든 가능한 경우를 처리하고 각 분기가 그 결과 타입을 충족해야 한다.

</details>

#### 회상 Q04 타입 매개변수와 공통 구조의 차이

def id[A](x:A):A=x가 id(3)과 id("abc")에 공통으로 쓰이는 이유를 설명하라. id[T] _와 타입 매개변수 선언은 어떻게 다른가? MyOption[A]·MyList[A]·BTree[A]에서 A를 바꾸면 무엇이 바뀌고 무엇이 공통으로 남는가?

applyn[A](f:A=>A,n:Int,x:A)는 n=0에서 x, 그 밖에는 f(applyn(f,n-1,x))이다. applyn(f,2,x)를 전개하고 자료의 applyn((x:Int)=>x+1,100,3)의 값과 전개 조건을 쓰라. 마지막으로 아무 제약 없는 A의 .name을 읽는 greeting을 id와 같은 논리로 정당화할 수 있는지, Subtype Polymorphism과 비교하라.

<details><summary>정답</summary>

id는 A의 내부 구조나 특정 멤버를 사용하지 않고 받은 x를 그대로 반환한다. id(3)은 A=Int에서 3을, id("abc")는 A=String에서 "abc"를 반환한다. 타입 매개변수 선언은 여러 A에 사용할 계산을 정의하고, id[T] _는 T를 정한 뒤의 T=>T 함수 값이라는 자료 표기다.

MyOption[A]는 부재·존재, MyList[A]는 빈 리스트·머리와 꼬리, BTree[A]는 빈 트리·값과 두 하위 트리라는 생성 구조를 재사용한다. A를 바꾸면 저장하는 내용의 타입이 달라진다. MyCons[A]의 머리:A와 꼬리:MyList[A], Node[A]의 값:A와 두 BTree[A]는 같은 매개변수를 공유한다.

~~~
applyn(f,2,x)
= f(applyn(f,1,x))
= f(f(applyn(f,0,x)))
= f(f(x))
~~~

각 단계가 같은 타입 A를 주어야 다음 f의 입력으로 쓸 수 있으므로 f:A=>A가 필요하다. 자료의 정수 계산은 3에 1을 100번 더하여 103이다. 이 전개는 n>=0이고 필요한 각 f 적용이 정상적으로 결과를 준다는 조건을 둔다. 음수 n에서는 이 감소가 0이라는 기저 경우로 향한다는 근거가 없다.

Parametric Polymorphism은 알려지지 않은 A에 특정 멤버를 요구하지 않는 계산을 쓴다. 아무 제약 없는 A가 name:String을 제공한다는 보장은 없으므로 .name은 정당화되지 않는다. 반면 Subtype Polymorphism에서는 {val name:String}이라는 공통 구조를 요구하고 그 구조의 Subtype들을 받는다. 단순히 여러 타입에서 사용된다는 말만으로 두 근거를 동일시해서는 안 된다.

</details>

#### 회상 Q05 greeting의 Value·Type·Member와 공통 요구

tom은 name:String과 home:String을, bob은 name:String과 mobile:String을 가진다. greeting의 본문은 "Hi "+r.name+", How are you?"이다. 두 값을 받기에 필요한 구조적 입력 타입과 두 Subtype 관계를 쓰라. NameHome만 받거나 아무 제약 없는 A를 받으면 왜 같은 해법이 되지 않는가?

type Name={val name:String}, object tom, tom.name이 각각 무엇을 나타내는지 구분하라. name:Int만 있는 값의 전달과, r:Name에서 r.home 사용도 판정하라. 이것이 어떤 Polymorphism인지 설명하라.

<details><summary>정답</summary>

공통 요구는 Name={val name:String}이다. NameHome={val name:String;val home:String}, NameMobile={val name:String;val mobile:String}이라 하면 NameHome <: Name과 NameMobile <: Name이다. 함수는 String인 name만 읽으므로 추가 home이나 mobile은 그 사용을 방해하지 않는다.

NameHome을 요구하면 home이 없는 bob의 전달을 정당화할 수 없다. 아무 제약 없는 A를 쓰면 A에 name:String이 있다는 근거가 없다. 반면 name:Int만 있는 값은 이름은 같지만 결과 타입 String이라는 요구가 맞지 않아 이 근거로 전달할 수 없다.

type Name은 필요한 구조의 alias이고 새 명목 클래스가 아니다. object tom은 멤버를 가진 특정 값에 이름을 주는 선언이며, tom.name은 그 값의 멤버를 읽는 식이다. new로 값을 만드는 자료 예와 개념적으로 연결되지만 모든 초기화·컴파일 세부가 같다는 결론은 필요하지 않다.

r:Name에서 보장되는 읽기는 name:String이다. 원래 값에 home이 있더라도 이 정적 타입만으로 r.home을 허용할 수는 없다. 하나의 greeting 코드를 서로 다른 입력 타입에 사용하는 근거는 Subtype Polymorphism이다. 확인할 점은 값 이름, 타입 별칭, 멤버 이름을 구분하고 멤버의 존재와 타입을 함께 확인하는 것이다.

</details>

#### 회상 Q06 Elimination을 보존하는 대체 사용

T <: S의 방향을 “어느 값을 어느 타입을 요구하는 자리에 쓰는가”로 설명하라. NameHome <: Name을 .name의 Elimination으로 확인하고, 이를 두 타입의 문자 그대로의 집합 동일성이나 메모리 표현 동일성으로 정의할 필요가 있는지 답하라. 한 소비자가 우연히 멤버를 읽지 않는 경우만으로 관계를 증명할 수 있는가?

h:S=>R가 S의 허용된 연산만 사용한다고 하자. T <: S에서 h를 T=>R 자리에도 쓸 수 있는 이유와 함수 타입 관계를 유도하라.

<details><summary>정답</summary>

T <: S는 왼쪽 T의 모든 값을 오른쪽 S의 값처럼 사용할 수 있다는 방향이다. Name의 소비자는 .name으로 String을 읽을 수 있어야 한다. NameHome에도 그 이름과 타입의 읽기 멤버가 있으므로 이 Elimination을 지원한다. Int를 같은 자리에 허용하면 .name:String을 얻을 근거가 없다.

여기서 필요한 것은 S가 허용하는 사용의 보존이다. 두 타입이 같은 원소 집합이거나 같은 메모리 배치를 가진다고 먼저 가정할 필요는 없다. 특히 한 호출이 우연히 .name을 사용하지 않는다는 사실은 Name이 허용하는 다른 사용까지 지원한다는 증거가 아니다. 타입이 허용하는 사용을 일반적으로 검토해야 한다.

T=>R라는 약속의 사용자는 T를 공급한다. h는 S를 요구하지만 T <: S이므로 그 입력을 S처럼 사용할 수 있다. h가 만든 R은 약속된 결과와 같다. 따라서 (S=>R) <: (T=>R)이다. 입력 타입의 관계와 함수 전체의 관계는 반대 방향이다. 이 논증은 정적 타입의 허용 연산에 관한 것이며 성능이나 별도 업무 계약까지 자동으로 보장하지 않는다.

</details>

#### 회상 Q07 Table Lookup과 Fixed Offset 가설의 비교

강의가 제안한 두 모형, 즉 필드 이름·내용을 표에 두고 r.name을 찾는 Table Lookup과 정해진 칸을 읽는 Fixed Offset을 비교하라. 이름 저장과 검색은 첫 모형에서 어떤 역할을 하는가?

“각 타입의 선언 순서대로 저장하며 모든 Name Subtype의 name은 첫 칸에 있다”는 단순 가정을 {val home:String;val name:String}으로 검토하라. 어떤 가정이 깨지며, 이 반례만으로 실제 컴파일러의 런타임 검색 필수성·코드 생성 횟수·상속의 성능 우위를 결론 낼 수 있는가?

<details><summary>정답</summary>

Table Lookup 모형은 필드 이름과 내용을 대응시켜 저장하고 name이라는 이름을 찾아 값을 반환한다. 필드 수나 나열 순서가 달라도 같은 이름 찾기 연산으로 필요한 멤버를 읽는 설명이 된다. 이 모형에서는 이름을 저장할 공간과 검색 작업이 필요할 수 있다. 이것은 모형 안의 역할 설명이다. [STT 30:07] [STT 32:07]

Fixed Offset 모형은 필드 위치를 정해 두고 .name을 해당 칸 읽기로 바꾼다. 그런데 선언 순서대로 저장한다는 가정 아래 {val home:String;val name:String}의 첫 칸은 home이다. 이 타입도 Permutation과 Width에 따라 Name={val name:String}을 충족하므로, 모든 허용 입력에서 첫 칸이 name이라는 가정은 성립하지 않는다. 첫 칸 읽기로는 요구한 name을 보장하지 못한다.

깨진 것은 그 단순한 저장·위치 가정이다. 다른 표현이나 컴파일 방법을 모두 배제한 것이 아니므로 런타임 검색이 필수라는 증명은 아니다. 실제 코드 생성 횟수, 포인터 폭, 필드 압축 수치, 항상 드는 비용이나 상속의 성능 우위도 이 비교만으로 확정할 수 없다. 강사는 구현을 잘 모르겠다고 유보하고 코드 생성에 대한 생각도 다시 검토한다. [STT 36:23] [STT 37:00]

확인할 점은 언어 수준의 Subtyping 규칙과 구현 가설을 분리하고, 반례가 부정하는 가정을 정확히 한정하는 것이다.

</details>

#### 회상 Q08 Structural·Nominal 관계의 판정 근거

type R={val name:String;val home:String}, type S={val home:String;val name:String}이라는 두 구조적 alias를 비교하라. 반면 같은 멤버를 가진 서로 독립된 명목 클래스 A와 B 사이에서도 모양만으로 B <: A를 얻을 수 있는가? 각각 관계를 정하는 근거를 설명하라.

자료의 Duck Typing이라는 명칭만으로 타입 검사가 반드시 런타임에 일어난다고 결론 낼 수 있는가? 명시적 관계를 선언하기만 하면 멤버 요구의 불일치도 모두 허용되는가?

<details><summary>정답</summary>

R과 S는 alias를 풀어 멤버 이름과 타입으로 비교한다. 두 구조는 같은 name:String과 home:String을 제공하고 순서만 다르므로 Permutation에 따라 R <: S와 S <: R를 얻는다. alias 이름의 철자가 새 명목 타입을 만들지는 않는다.

별개 명목 클래스 A와 B는 타입 이름과 명시된 관계도 판정 근거다. 같은 멤버를 가진다는 사실만으로 B <: A가 자동 생성되지 않는다. extends 같은 선언된 관계와 해당 언어의 허용 조건을 확인해야 한다. 관계를 선언했다는 이유만으로 부모가 요구하는 사용과 모순되는 임의의 구조까지 허용되는 것도 아니다.

Structural Subtyping의 초점은 요구 구조를 제공하는지이며, 자료의 Duck Typing이라는 별칭은 검사의 시점을 증명하지 않는다. 자료가 Nominal Sub Types에 붙인 Ad hoc Polymorphism도 이 자료의 용어 대비로 읽는다. 확인할 점은 alias의 구조 비교와 명목 클래스의 선언 관계를 구분하고, 별칭만으로 런타임 동작이나 언어 전체의 용어 분류를 추론하지 않는 것이다.

</details>

#### 회상 Q09 Reflexivity·Transitivity와 역방향

Reflexivity와 Transitivity를 전제·결론으로 쓰라. T <: R과 R <: S에서 얻는 결론의 사용 방향을 설명하라.

T={val name:String;val home:String;val mobile:String}, R={val name:String;val home:String}, S={val name:String}이라고 하자. T <: R, R <: S를 알고 있을 때 T <: S를 도출하라. Reflexivity나 Transitivity가 S <: T도 주는지, 허용된 멤버 사용으로 확인하라.

<details><summary>정답</summary>

Reflexivity는 임의의 타입 X에 대해 X <: X이다. Transitivity는 T <: R와 R <: S를 전제로 T <: S를 준다. 왼쪽 T의 값을 오른쪽 S를 요구하는 자리에 쓸 수 있다는 방향을 유지한다.

주어진 레코드는 T의 값을 R처럼 사용할 수 있고 그 R의 값을 S처럼 사용할 수 있으므로 추이성으로 T <: S다. S 소비자가 name:String을 읽는 사용을 T가 지원한다. 같은 타입을 그대로 쓰는 단계가 필요하면 T <: T, R <: R, S <: S의 반사성을 쓸 수 있다.

이 규칙들은 S <: T를 주지 않는다. S에는 name만 있는 값이 허용되지만 T 소비자는 home과 mobile까지 읽을 수 있어야 한다. 그런 S 값을 공급하면 그 요구를 충족하지 못할 수 있다. 반사성은 자기 타입과의 관계일 뿐 부족한 필드를 추가하지 않으며, 추이성도 주어진 방향의 사슬만 연결한다.

</details>

#### 회상 Q10 Nothing·Any의 생성과 사용

Nothing <: T <: Any를 Introduction·Elimination 관점에서 설명하라. Nothing 쪽 명제가 Vacuous Truth가 되는 이유를 쓰고, def f(a:Nothing):Int=a의 결과 타입이 허용된다는 사실과 정상적인 호출 가능성을 구분하라. 예외나 발산하는 Nothing 타입 식이 이 차이를 없애는가?

val a:Int=3; val b:Any=a에서 허용되는 타입 관계는 무엇인가? b:Any만으로 정수 전용 계산이나 .name을 요구할 수 있는지, 그리고 “Any에는 모든 공통 연산도 없다”까지 결론 낼 수 있는지 답하라.

<details><summary>정답</summary>

Nothing은 정상적인 값이 없는 Bottom이고 Any는 모든 타입의 값을 받아들이는 Top이다. 모든 타입 T에 대해 Nothing <: T와 T <: Any가 주어진다.

Nothing에는 정상 값을 만드는 Introduction이 없다. 따라서 “Nothing의 모든 값을 T처럼 사용할 수 있다”는 전칭 명제에 실패하는 실제 값을 고를 수도 없다. 이것이 값 부재에 근거한 Vacuous Truth다. 가정상 Nothing 값이 주어지면 어떤 T의 결과 자리에도 쓸 수 있다는 Elimination을 설명할 수 있지만, 정상적인 인자를 만들어 공급할 수 있다는 뜻은 아니다.

f의 본문 a는 Nothing이고 Nothing <: Int이므로 Int가 필요한 반환 자리에 허용된다. 이 타입 관계로 실제 Nothing 인자가 생기지는 않는다. 예외를 던지거나 발산하는 식도 정상 종료하여 인자를 반환하는 것은 아니므로 정상 호출을 보장하지 않는다. 빈 ADT의 경우 수가 0이라는 비유 역시 특정 빈 match 구문의 컴파일 성공을 증명하지 않는다.

a에서 b로의 사용은 Int <: Any라는 타입 관계로 정당화한다. a와 b라는 값 이름 사이의 Subtype 관계가 아니다. b의 실제 대입값이 3이라는 계산 사실과, Any만 받는 코드가 사용할 수 있는 정적 정보는 다르다. Any에는 정수 이외의 값도 올 수 있으므로 정수 전용 연산이나 name:String을 보장할 수 없다. 강의의 Elimination 부재라는 대비는 이런 특정 타입 연산을 임의로 요구할 수 없다는 뜻으로 한정하며 모든 Scala 공통 연산이 없다는 주장까지 주지는 않는다.

</details>

#### 회상 Q11 중첩 레코드의 규칙 적용 층위

모든 필드는 읽기 전용 val이다. 다음 타입에서 A <: C를 중간 타입 B를 거쳐 도출하라.

~~~
A = {val x:{val y:Int;val z:String};val w:Int}
B = {val w:Int;val x:{val y:Int;val z:String}}
C = {val w:Int;val x:{val z:String}}
~~~

Permutation·Width·Depth·Transitivity가 각각 어디에 쓰이는가? C 소비자의 r.w와 r.x.z를 확인하고, 안쪽 y를 바깥 Width 한 번으로 없앴다고 할 수 있는지 답하라. 이 Depth를 var에도 그대로 적용하면 왜 위험한지 NameHome <: Name을 이용하여 반례를 설명하라.

<details><summary>정답</summary>

A <: B는 바깥 멤버의 순서만 바꾸는 Permutation이다. 이름 x와 w에 붙은 타입은 그대로다. 안쪽에서는 Width로 다음을 얻는다.

~~~
{val y:Int;val z:String} <: {val z:String}
~~~

이를 x의 읽기 결과 타입에 대한 Depth로 올리면 B <: C다. w:Int는 반사성으로 그대로 유지한다. 두 관계를 Transitivity로 연결하여 A <: C를 얻는다.

C 소비자가 r.w를 읽으면 Int를, r.x.z를 읽으면 String을 얻어야 한다. A의 값도 두 사용을 모두 제공한다. y는 바깥 필드가 아니라 x가 반환하는 안쪽 레코드의 필드이므로 바깥 Width 한 번이라는 설명은 층위를 잘못 짚는다. 이 관계는 정적 요구를 줄일 뿐 객체에서 y를 물리적으로 지우지 않는다.

쓰기 가능한 경우에는 입력되는 값도 확인해야 한다. var x:NameHome인 저장 위치를 같은 방향으로 var x:Name처럼 보게 허용했다고 가정하자. 넓어진 쪽은 name만 있는 값을 x에 쓸 수 있다. 그러나 원래 쪽은 x.home을 읽을 수 있다고 기대한다. 새 값에는 home이 없어 그 보장이 깨진다. 따라서 읽기 val의 Depth를 var에 자동 확대할 수 없다.

확인할 점은 안쪽 Width와 바깥 Depth를 분리하고, 순서 변경을 필드 이름 변경과 혼동하지 않는 것이다.

</details>

#### 회상 Q12 Tuple의 같은 Arity와 위치별 Depth

Int <: Any를 사용하여 (Int,String,Int) <: (Any,String,Any)를 위치별 단계로 유도하라. 각 단계의 Arity와 그대로인 위치를 쓰라.

같은 규칙으로 (Int,String,Int) <: (Int,String) 또는 (Int,String) <: (String,Int)를 얻을 수 있는가? 레코드 Width·Permutation과 비교하고, t의 첫 두 성분만 필요해서 (t._1,t._2)를 구성하는 일은 어떤 종류의 연산인지 설명하라.

<details><summary>정답</summary>

주어진 규칙은 같은 Arity에서 같은 위치의 타입을 넓히는 Depth다.

~~~
(Int,String,Int)
<: (Any,String,Int)     // 첫째 위치에 Int <: Any
<: (Any,String,Any)     // 셋째 위치에 Int <: Any
~~~

두 단계 모두 Arity는 3이다. 둘째 위치 String은 유지되고, 각 단계에서 바꾸지 않은 다른 위치도 그대로다. Transitivity로 처음 타입과 마지막 타입의 관계를 얻는다.

이 규칙은 세 성분을 두 성분으로 줄이는 Tuple Width를 주지 않는다. (Int,String)을 (String,Int)로 바꾸는 Tuple Permutation도 주지 않는다. 첫 위치를 String으로 사용할 소비자에게 원래 첫 위치 Int를 주면 그 기대가 맞지 않는다. 이름으로 고르는 레코드의 순서 변경과 위치로 고르는 Tuple의 재배열은 다르다.

(t._1,t._2)는 기존 Tuple의 두 성분을 Projection으로 꺼내 새 Tuple을 도입하는 별도의 계산이다. 이를 긴 Tuple 자체가 짧은 Tuple의 Subtype이라는 주장으로 바꾸어서는 안 된다. 확인할 점은 여기서 제공된 규칙의 같은 Arity·같은 위치 조건을 지키는 것이다.

</details>

#### 회상 Q13 함수 입력·출력의 대체 가능성

T <: T', S <: S'일 때 (T'=>S) <: (T=>S')를 사용자의 공급·소비 관점에서 유도하라. 입력만 바꾸는 단계와 출력만 바꾸는 단계로도 쓰고 Contravariance·Covariance를 구분하라.

NameHome <: Name과 XY={val x:Int;val y:Int} <: X={val x:Int}를 이용하여 입력을 잘못된 방향으로 바꾸었을 때와 출력을 잘못된 방향으로 바꾸었을 때의 반례를 각각 제시하라. 함수의 입력 Elimination·출력 Introduction과 함의의 비교는 무엇을 설명하는가?

<details><summary>정답</summary>

오른쪽 T=>S'를 믿는 사용자는 T를 공급하고 결과를 S'로 사용한다. 실제 함수는 T'를 요구하지만 T <: T'이므로 그 인자를 받아들일 수 있다. 실제 반환값 S도 S <: S'에 따라 약속된 결과로 사용할 수 있다. 이 두 조건을 함께 만족하므로 대체가 성립한다.

~~~
(T'=>S) <: (T=>S)       // T <: T', 입력 Contravariance
(T=>S)  <: (T=>S')      // S <: S', 출력 Covariance
(T'=>S) <: (T=>S')      // Transitivity
~~~

입력 쪽은 타입 관계가 뒤집히는 Contravariance, 출력 쪽은 같은 방향인 Covariance다. 실제 함수는 공개된 입력보다 더 강한 요구를 해서는 안 되고, 공개된 결과보다 부족한 결과를 주어서는 안 된다.

입력의 반례: NameHome을 받아 .home을 읽는 함수를 Name만 받는다고 약속한 자리에 넣으면, 사용자가 name만 있는 값을 공급할 수 있다. 그러면 필요한 home이 없다. 반대로 name만 읽는 함수에는 NameHome 값을 주어도 그 요구를 충족한다.

출력의 반례: X만 반환하는 함수를 XY를 준다고 약속한 자리에 넣으면, 사용자가 결과의 .y를 읽을 때 보장할 수 없다. XY를 주는 함수는 X만 요구하는 자리에서 .x를 제공할 수 있다.

함수 본문은 입력으로 주어진 값을 Elimination으로 사용하고 결과 값을 Introduction으로 만든다. A를 가정하여 B를 얻는다는 함의의 모습과 이 역할을 비교할 수 있다. 이 비교만으로 프로그래밍과 수학 전체의 완전한 동일성까지 증명한 것은 아니다. 확인할 점은 규칙의 방향 암기와 별도로 사용자가 주는 값과 읽는 결과를 양쪽 모두 설명하는 것이다.

</details>

#### 회상 Q14 foo·gee의 입력과 새 결과 레코드

AB={val a:Int;val b:Int}, ABC={val a:Int;val b:Int;val c:Int}, XY={val x:Int;val y:Int}, X={val x:Int}라 하자. 자료의 foo:AB=>XY는 새 객체를 만들며 x=s.b, y=s.a를 설정한다. gee:ABC=>X 자리에 foo _를 넣는 두 전제와 함수 규칙의 대입을 쓰라.

a=2,b=9,c=100을 공급했을 때 실제 결과와 gee 사용자가 읽을 수 있는 x를 구하라. 이 계산이 Permutation인지, c와 y가 각각 어떻게 취급되는지 설명하라. 역방향 (ABC=>X) <: (AB=>XY)가 일반적으로 성립하지 않는 이유를 입력·출력에서 각각 제시하라.

<details><summary>정답</summary>

입력에서는 Width로 ABC <: AB, 출력에서도 Width로 XY <: X를 얻는다. 함수 규칙에 T=ABC, T'=AB, S=XY, S'=X를 대입하면 다음과 같다.

~~~
(AB=>XY) <: (ABC=>X)
~~~

gee 사용자는 a,b,c를 공급한다. 실제 foo는 그중 a,b만 읽으면 되므로 입력 요구를 충족한다. 결과에 x,y를 모두 만들므로 X만 기대한 사용자는 x를 읽을 수 있다.

주어진 입력에서 x=s.b=9, y=s.a=2인 새 객체를 만든다. gee를 통해 약속된 결과 타입은 X이므로 .x는 9를 주지만 그 타입만으로 .y 사용을 정당화할 수 없다. 입력의 a,b를 읽어 이름 x,y인 새 필드를 구성한 것이므로 기존 필드 순서만 바꾸는 Permutation은 아니다. c를 사용하지 않아도 되는 것이지 c를 처리했다는 뜻은 아니다. y도 정적 결과 요구에서 빠졌을 뿐 실제 객체에서 물리적으로 삭제한 것이 아니다.

역방향의 입력 문제는 ABC=>X 함수가 c를 읽을 수 있다는 것이다. AB=>XY를 믿는 사용자는 c 없는 AB를 줄 수 있어 그 요구를 충족하지 못한다. 출력 문제는 X만 만드는 함수에 y가 없을 수 있다는 것이다. XY를 기대한 사용자는 y까지 읽을 수 있어야 한다. 어느 한 문제만 있어도 역방향을 일반적으로 허용할 수 없다.

</details>

### 통합 연습

#### 연습 P01 Option·MyList의 case 분석과 Closure

다음은 일반 통합 연습이다. 선수 개념은 Lexical Scope, Closure, 함수 적용, 기초 Pattern Matching이다. 본문의 MyList[A]는 MyNil[A]() 또는 MyCons[A](hd:A,tl:MyList[A])로 만들어진다. applyn은 Q04의 정의를 사용한다.

headTwice[A](o:Option[MyList[A]],step:A=>A):Option[A]를 작성하라. None과 Some(MyNil())이면 None을, Some(MyCons(hd,tl))이면 머리에 step을 정확히 두 번 적용한 값을 Some에 담아 반환해야 한다. 꼬리는 처리하지 않는다. 바깥 Option과 안쪽 MyList의 case 분석을 나누어 작성하라.

이후 다음 세 입력의 결과를 단계별로 구하라. Scala 자료의 표기 문맥에서 식을 정적으로 전개하는 문제다.

~~~
val offset = 1
val step: Int=>Int = (x:Int)=>x+offset

def run(o:Option[MyList[Int]]):Option[Int] = {
  val offset = 100
  headTwice[Int](o,step)
}
~~~

입력은 None, Some(MyNil[Int]()), Some(MyCons[Int](5,MyCons[Int](8,MyNil[Int]())))이다. run의 offset이 step에 영향을 주는가? 함수가 임의의 A에 대해 정당한 이유와 필요한 종료 조건을 설명하고, step의 자리에 (x:A)=>x.name을 아무 제약 없이 넣을 수 있는지도 답하라.

<details><summary>정답</summary>

바깥 값의 부재와 빈 리스트는 서로 다른 생성 경로이지만, 명세가 두 경우 모두 None을 반환하도록 정했다. 두 Sum을 차례로 제거하면 다음과 같다.

~~~
def headTwice[A](
  o: Option[MyList[A]],
  step: A=>A
): Option[A] =
  o match {
    case None => None
    case Some(xs) =>
      xs match {
        case MyNil() => None
        case MyCons(hd,tl) =>
          Some(applyn[A](step,2,hd))
      }
  }
~~~

None 분기에는 리스트가 없다. Some(xs)에서만 xs:MyList[A]를 얻으며, MyNil에는 머리가 없다. MyCons에서 얻은 hd:A에 step:A=>A를 적용하므로 각 결과를 다음 입력으로 다시 쓸 수 있다. Some으로 담으면 Option[A]이고, None도 Option[A] 문맥에서 허용되므로 모든 분기가 결과 타입을 충족한다.

입력별 전개는 다음과 같다.

1. run(None): 바깥 None case에서 즉시 None이다. step을 적용하지 않는다.
2. run(Some(MyNil[Int]())): Some에서 리스트를 꺼낸 뒤 MyNil case로 들어가 None이다. Some이 있다는 이유만으로 머리가 있는 것은 아니다.
3. 비어 있지 않은 입력: 머리 hd=5와 꼬리를 얻는다. 꼬리의 8은 명세상 사용하지 않는다.

~~~
applyn[Int](step,2,5)
= step(applyn[Int](step,1,5))
= step(step(applyn[Int](step,0,5)))
= step(step(5))
= step(6)
= 7
~~~

따라서 세 번째 결과는 Some(7)이다. step은 바깥 offset=1을 가진 정의 환경의 Closure다. run의 지역 offset=100은 호출 환경에 생긴 별개 binding이므로 step의 자유 이름을 바꾸지 않는다.

headTwice는 A의 구체 멤버를 조사하지 않고 생성자를 나누고 전달받은 함수를 적용한다. 따라서 타입 매개변수를 가진 같은 계산 구조를 쓸 수 있다. (x:A)=>x.name은 임의의 A가 name을 제공하지 않으므로 별도 구조적 조건 없이 정당화되지 않는다. 또한 이 문제의 step 자리에는 입력·출력이 같은 A인 함수가 필요하다.

applyn은 여기서 n=2이고 2→1→0으로 진행한다. 두 step 적용이 정상 결과를 준다는 조건 아래 계산이 끝난다. headTwice 자체는 꼬리를 순회하지 않는다. 전체 길이를 세는 재귀나 꼬리의 모든 원소를 처리했다고 설명하면 명세와 다르다. 확인할 점은 두 단계 case 분석, 각 분기의 Option[A], 두 번의 함수 적용, 정의 환경의 offset을 모두 보이는 것이다.

</details>

#### 연습 P02 중첩 레코드·함수 멤버·Tuple의 합성

다음은 읽기 전용 val에 대한 일반 통합 연습이며 아래 이름들은 설명용 타입 축약이다.

~~~
A = {val payload:{val name:String;val home:String};val tag:Int}
B = {val payload:{val name:String}}
C = {val text:String;val size:Int}
D = {val text:String}
F = B=>C
G = A=>D

Full = {val build:F;val stamp:Int}
View = {val build:G}
~~~

render:F는 입력 r에서 새 결과 객체의 text를 "Hello "+r.payload.name으로, size를 1로 설정한다. v:Full의 build는 render이고 stamp는 7이다.

1. A <: B를 적용 층위별로 증명하고 C <: D와 함께 F <: G를 유도하라.
2. Full <: View와 (Full,Int) <: (View,Any)를 도출하라. 각 단계에서 Width·Depth·함수 규칙·Tuple 규칙이 어디에 쓰이는지 표시하라.
3. consumer가 v를 View로 받아, payload의 name="Mina", home="home-data", tag=4인 A 값을 build에 공급한다. 실제 결과와 consumer가 그 정적 타입으로 읽을 수 있는 필드를 구하라. 이것이 필드 이름의 단순 Permutation인지도 설명하라.
4. Tuple의 둘째 성분 삭제나 두 성분 교환도 위 유도에 포함되는가? 또 Full·View의 build를 모두 var로 바꾸어 같은 Depth를 자동 허용하면 어떤 쓰기 문제가 생기는가?

<details><summary>정답</summary>

1. 안쪽 레코드에서 Width를 먼저 쓴다.

~~~
{val name:String;val home:String} <: {val name:String}
~~~

이 관계를 payload의 읽기 결과 타입에 대한 Depth로 올린다.

~~~
A
<: {val payload:{val name:String};val tag:Int}
<: B
~~~

마지막 단계는 바깥 tag를 요구하지 않는 Width다. Transitivity로 A <: B를 얻는다. C <: D도 결과의 size를 요구하지 않는 Width다. 실제 render는 B를 요구하고 C를 제공한다. 공개된 G의 사용자가 주는 A는 B로 쓸 수 있고, 실제 C는 D로 쓸 수 있으므로 입력 Contravariance와 출력 Covariance로 F=(B=>C) <: G=(A=>D)다.

2. F <: G를 build의 읽기 결과 타입에 올린 뒤 stamp 요구를 줄인다.

~~~
Full
<: {val build:G;val stamp:Int}     // build에 Depth
<: View                          // 바깥 Width
~~~

이 두 단계를 추이성으로 연결한다. 이제 Tuple은 같은 Arity 2를 유지한다.

~~~
(Full,Int) <: (View,Int) <: (View,Any)
~~~

첫째 단계는 첫 위치의 Full <: View, 둘째 단계는 둘째 위치의 Int <: Any를 사용한 위치별 Depth다. 각 단계에서 다른 위치는 반사성으로 유지한다.

3. View 소비자는 v.build:G를 얻는다. 공급한 A에는 render가 필요한 payload.name:String이 있다. render는 text="Hello Mina", size=1인 새 C 객체를 만든다. 그러나 G의 공개된 결과는 D이므로 소비자가 그 타입으로 읽을 수 있는 필드는 text:String이다. 따라서 .text는 "Hello Mina"이고 .size는 D만으로 정당화되지 않는다. 입력 tag와 payload.home은 이 계산에서 사용하지 않는다. 실제 결과의 size가 물리적으로 삭제된 것은 아니다.

입력의 payload를 읽어 다른 이름 text와 size를 가진 결과를 구성했으므로 새 값의 Introduction이다. 기존 레코드의 같은 멤버 나열 순서만 바꾸는 Permutation이 아니다.

4. Tuple 유도는 성분 수와 위치를 유지한다. 둘째 성분을 없애려면 새 값을 구성하는 별도 계산이 필요하고, 성분을 교환하는 것도 여기의 Subtype 규칙이 아니다.

가변 build에 같은 Depth를 적용한다고 가정하면 View 쪽 사용자는 임의의 G를 써 넣을 수 있다. 예를 들어 다음 G는 허용된다.

~~~
A 입력 s를 받아 text=s.payload.home만 가진 D 객체를 반환하는 함수
~~~

이 함수는 home을 필요로 하며 size를 제공하지 않는다. 원래 Full 쪽은 build:F라고 믿고 home 없는 B를 공급하거나 결과의 size를 읽을 수 있으므로 쓰기 뒤 그 보장이 깨진다. 따라서 이 읽기 val 유도를 var로 자동 확대해서는 안 된다.

확인할 점은 안쪽 레코드의 Width, 바깥 payload의 Depth, 함수 입력·출력의 방향, build의 Depth, Tuple의 위치를 각각 분리하는 것이다.

</details>

#### 연습 P03 고차 함수의 방향과 Top·Bottom 경계

다음은 본문의 Higher-order Function 유도를 결합하는 일반 통합 연습이다. AB={val a:Int;val b:Int}, ABC={val a:Int;val b:Int;val c:Int}, XY={val x:Int;val y:Int}, X={val x:Int}이고, F=AB=>XY, G=ABC=>X라 하자. 먼저 F <: G의 전제를 확인하라.

1. 함수 값을 반환하는 생산자 Int=>F와 Int=>G의 관계, 함수 값을 받는 소비자 G=>Int와 F=>Int의 관계를 각각 유도하라.
2. 이미 얻은 소비자 관계를 다시 함수의 입력에 적용하여 ((F=>Int)=>Int)와 ((G=>Int)=>Int)를 비교하라. 이어 ((F=>Int)=>F) <: ((G=>Int)=>G)를 입력·결과의 두 전제로 증명하라.
3. 역방향 (F=>Int) <: (G=>Int)를 자동 허용할 수 없는 이유를 보여라. AB만 공급하고 결과의 y를 읽는 소비자와, c를 읽어 x만 반환하는 G를 사용하여 구체적으로 설명하라.
4. 임의의 타입 P·R에 대해 (Any=>Nothing) <: (P=>R) <: (Nothing=>Any)를 함수 규칙으로 유도하라. 이 관계가 정상 종료하는 Any=>Nothing 함수나 정상적인 Nothing 입력의 존재를 보장하는지도 설명하라.

<details><summary>정답</summary>

기초 관계는 Width에 의한 ABC <: AB와 XY <: X다. 함수 규칙은 입력을 반대로, 결과를 같은 방향으로 비교하므로 F=(AB=>XY) <: G=(ABC=>X)다.

1. 생산자의 바깥 입력 Int는 반사성으로 유지하고 반환하는 함수 값에 F <: G를 적용한다.

~~~
(Int=>F) <: (Int=>G)
~~~

사용자는 같은 Int를 주고 나온 F를 G처럼 사용한다. 반면 소비자는 함수 값을 입력으로 받으므로 방향이 뒤집힌다.

~~~
F <: G, Int <: Int
따라서 (G=>Int) <: (F=>Int)
~~~

G를 사용하도록 작성한 소비자에게 F를 주어도 F를 G처럼 사용할 수 있다. 예를 들어 ABC를 공급하고 결과의 x만 읽는 사용은 F도 지원한다.

2. K=G=>Int, L=F=>Int로 두면 방금 K <: L을 얻었다. 바깥 함수가 이 소비자를 입력으로 받으므로 다시 Contravariance를 적용한다.

~~~
(L=>Int) <: (K=>Int)
즉 ((F=>Int)=>Int) <: ((G=>Int)=>Int)
~~~

두 입력 위치를 지나며 방향이 두 번 뒤집힌다. 괄호를 유지해야 어느 함수의 입력인지 혼동하지 않는다.

입력과 결과를 동시에 바꾸는 관계는 다음 두 전제를 쓴다.

~~~
(G=>Int) <: (F=>Int)    // 바깥 함수의 입력 관계
F <: G                 // 바깥 함수의 결과 관계
따라서 ((F=>Int)=>F) <: ((G=>Int)=>G)
~~~

오른쪽 약속의 사용자는 G=>Int 소비자를 공급한다. 왼쪽 실제 함수는 이를 F=>Int처럼 사용할 수 있다. 왼쪽이 반환한 F 역시 사용자가 기대한 G로 쓸 수 있다. 입력과 출력 양쪽 모두 사용을 보존한다.

3. k:F=>Int가 받은 h에 a=1,b=2만 있는 AB 값을 주고 h의 결과 .y를 읽는다고 하자. 모든 F는 그 입력을 받고 XY를 제공하므로 이 사용은 허용된다. 이제 g:G가 s.c를 읽어 x=s.c만 가진 객체를 만든다고 하자. G로서는 올바른 입력 ABC와 결과 X의 요구를 만족한다.

k에게 임의의 G도 줄 수 있다고 허용하면, k는 g에 c 없는 AB를 공급한다. 입력 요구가 충족되지 않는다. c가 있는 값을 공급하는 별도 경우를 생각하더라도 g의 결과에는 y가 없으므로 k의 결과 사용도 보장되지 않는다. 이는 실제로 그런 잘못된 호출을 실행하라는 뜻이 아니라 공개된 타입의 사용을 비교하는 반례다. 따라서 F <: G에서 소비자의 역방향을 자동으로 얻을 수 없다.

4. 함수 규칙의 전제를 각각 대입한다.

~~~
P <: Any, Nothing <: R
따라서 (Any=>Nothing) <: (P=>R)

Nothing <: P, R <: Any
따라서 (P=>R) <: (Nothing=>Any)
~~~

두 관계를 연결하여 요구한 사슬을 얻는다. 첫 관계는 실제 함수의 입력을 더 넓게 받고 결과를 더 좁게 제공하는 방향이다. 둘째 관계는 공급되는 Nothing을 P처럼 사용할 수 있고 R 결과를 Any로 사용할 수 있다는 방향이다.

이것은 타입 관계의 유도다. Any=>Nothing 타입이 모든 입력에서 정상 종료하여 Nothing 값을 만들어 낼 수 있다는 존재 증명이 아니다. Nothing에는 정상 값이 없고, 예외나 발산도 정상 결과를 반환하지 않는다. Nothing=>Any라는 약속을 적었다고 정상적인 Nothing 입력이 생기는 것도 아니다. 확인할 점은 각 화살표의 입력·결과를 따로 비교하고 타입의 대체 허용과 정상 값의 존재를 구분하는 것이다.

</details>

## 출처

### Sources

[[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|Structural Types and Subtyping · 보정 STT · 날짜 미확인]]

[Part1 자료 저장소](https://github.com/snu-sf-class/pp202602) · [Part2 PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf)

| 출처 | 위치 | 연결 내용 |
|---|---|---|
| M002 · Part1 | [p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-068), [p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-069) | Introduction·Elimination, Tuple의 생성·투영 |
| M002 · Part1 | [p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-070), [p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071), [p.72](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-072) | Structural Type·alias, 세 독립 코드와 정의 환경 |
| M002 · Part1 | [p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-073), [p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-074), [p.76](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076), [p.77](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-077), [p.78](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-078), [p.79](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-079) | Product·Sum·Recursion, 생성자와 기초 case 분석 |
| M002 · Part1 | [p.90](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-090), [p.91](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-091), [p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092), [p.98](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-098), [p.100](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-100) | Parametric Polymorphism, applyn, MyList와 Option |
| NM001 · Part2 | [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-007) | greeting, 사용 가능성, Structural·Nominal 판정 |
| NM001 · Part2 | [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014) | 일반 규칙, Top·Bottom, 읽기 레코드·Tuple·함수 |
| NT001 · 보정 STT | [STT 07:00]–[STT 18:07]; [STT 20:00]–[STT 27:14]; [STT 28:13]–[STT 38:55]; [STT 39:55]–[STT 48:24]; [STT 49:17]–[STT 59:05]; [STT 01:00:01]–[STT 01:12:03]; [STT 01:16:31]–[STT 01:18:32] | 공통 구조, Elimination, 구현 가설과 유보, Subtyping의 기술 논지 |
| pop_2025_mid_q01_partial · 2025년 중간 1번 | issues/13.md L.26–46 | 구조적 멤버 안에 함수 타입이 중첩된 부분 자료: Q11·Q13·Q14·P02·P03의 개념 연결 |
| pop_2025_mid_q01_partial · 별도 제공 답안 | issues/13.md L.12–16 | P02·P03에서 규칙을 중첩하는 풀이 구조와의 간접 비교 |

M002의 네 선수 목표는 자료 기반 설명이다. NT001의 Functional Programming 회고는 Part1 pp.63–100 전체의 상세 구두 진도나 수업 날짜를 입증하지 않는다. 고급 Pattern Matching·guard, 트리 탐색·BST 및 List library 전체는 이 범위에 포함되지 않는다. Tuple 길이 22, reflectiveSelectable·underscore, 다형 함수 값의 제한은 자료의 표기·버전 문맥에 한정된다. 계산은 자료 식의 정적 전개이며 컴파일·실행 결과의 확인은 아니다.

NM001에서는 pp.3–7, 9–14를 사용한다. pp.15–29의 다른 단원과 p.30 이후의 상세 내용은 이 노트의 진도에 추가하지 않으며, p.30 이후는 미래·참고 범위다. 읽기 val의 Depth, 같은 Arity·위치의 Tuple 규칙이라는 조건을 유지한다. Higher-order Function 관계와 Top·Bottom을 결합한 관계는 주어진 규칙의 설명용 유도다.

현재 두 강의의 수업 날짜는 모두 미확인이다. NT001은 원음 미검증 텍스트이며 완전한 축어 전사나 누락 감사가 아니다. 제공된 첫 05:06부터 마지막 01:18:32까지의 텍스트 밖 발화와 중간 공백의 상태는 확인되지 않았다. 시연의 정확한 코드 입력·출력, 화면·판서·도식, 실제 import와 타입 주석의 세부도 확인되지 않았다.

NT001의 불확실성에는 07:49–15:54의 시연 토큰·출력·주석 관찰, 19:04–24:28의 Introduction/Elimination·긍정/부정·지시어 혼선, 42:42의 명목 타입 방향 혼선, 48:24의 추이성 기호, 49:17–59:05의 ‘타입의 n을’·RGB/MDC·빈 match·생성/사용 설명, 01:00:01–01:04:58의 Width 방향·중첩 레코드 지시어·숫자 인덱스, 01:05:57–01:18:32의 prime·부정·함수 이름·결과 접근 표현이 포함된다. 정확한 정의·식은 해당 PDF에, 새 계산과 중첩 유도는 표시된 설명용 전제에 근거한다. 이들을 불명확한 발화 자체가 확인된 것으로 읽어서는 안 된다. Any에 관한 특정 연산 정보의 부재와 모든 공통 연산의 부재, Nothing의 타입 허용과 정상 값의 존재도 구분한다. 함수와 함의의 비교만으로 프로그래밍과 수학 전체의 동일성이 성립하지는 않는다.

28:13–38:55의 Table Lookup·Fixed Offset과 후속 비용 논의는 강사의 제안 모형·추측과 유보를 포함한다. 실제 컴파일러의 layout·전문화·포인터 폭·검색 필수성·정량 비용·코드 생성 횟수·상속의 성능 우위는 확인되지 않았다.

2025년 중간 1번 자료는 issues/13.md L.26–46의 구조·함수 타입 일부이며 전체 원래 발문은 없다. L.12–16은 별도로 제공된 답안으로 독립 검증된 전체 풀이가 아니다. 연결은 구조적 멤버와 함수의 입력·출력 관계를 나누어 적용하는 개념·풀이 구조에 한정한다. Q와 P는 본문 및 명시된 선수 개념에서 푸는 일반·합성 연습이며 역사 문항과의 직접 대응이나 전체 문제의 재구성을 뜻하지 않는다.
