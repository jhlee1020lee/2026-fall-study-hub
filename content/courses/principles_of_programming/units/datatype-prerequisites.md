---
title: "자료로 확인하는 선수 개념: 자료형의 생성·사용과 Polymorphism"
description: "자료형의 생성·사용, 정의 환경, 재귀 ADT와 타입 매개변수를 복습한다."
course: "principles_of_programming"
unit_id: "datatype-prerequisites"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/undated-structural-subtyping-6p3wjj22vvvjv0ji"]
---

## Introduction과 Elimination으로 읽는 자료형

자료형을 이해할 때는 “어떤 값이 있는가”와 함께 “그 값을 어떻게 만들고 사용하는가”를 묻는다. Introduction(도입)은 값을 만드는 방법이고, Elimination(제거)은 이미 주어진 값을 사용하는 방법이다. 여기서 제거는 메모리에서 값을 지운다는 뜻이 아니다. `Int`의 정수 리터럴은 값을 도입하고, 덧셈이나 비교는 정수 값을 사용한다. 함수 값은 `(x:T)=>e`로 만들고 `f(v)`로 사용한다. 함수 적용에서는 인자가 입력 타입에 맞고 본문이 요구된 결과 타입을 만들어야 한다. 이 단원의 기초는 프로그래밍의 원리 Part1(M002)의 선택한 자료로 보충하는 선수 개념이다. 해당 자료 전체가 녹음으로 확인된 진도라는 뜻은 아니다. [Part1 PDF p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

### Tuple의 위치와 성분 타입

Tuple(튜플)은 여러 성분을 위치에 따라 묶은 값이다. `(1,"a",10)`의 타입은 `(Int,String,Int)`다. 이 식으로 전체 값을 만드는 것이 Introduction이고, Projection(투영)으로 성분을 꺼내는 것이 Elimination이다.

| 식 | 사용하는 위치 | 결과 |
| --- | --- | --- |
| `(1,"a",10)._1` | 첫 번째 | `1` |
| `(1,"a",10)._2` | 두 번째 | `"a"` |
| `(1,"a",10)._3` | 세 번째 | `10` |

따라서 `._2`와 `f(v)`는 각각 이미 주어진 Tuple과 함수를 사용하는 연산이다. Tuple을 만든 `(1,"a",10)`, 함수를 만든 `(x:T)=>e`와 역할이 다르다. 성분의 타입이 모두 같을 필요는 없지만 Arity(성분 수)와 각 위치의 타입을 구분해야 한다. 두 번째 위치가 `String`이라는 정보는 뒤의 Tuple subtyping에서도 유지된다. Record(레코드)의 `r.name`은 이름으로 멤버를 고르므로 위치로 성분을 고르는 Tuple과 다르다. 자료의 “길이 22까지” 표기는 그 자료의 표현 문맥에 관한 설명이며 모든 Scala 버전의 상한으로 일반화하지 않는다. [Part1 PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

## Structural Type과 정의 환경

Structural Type(구조적 타입), 또는 Record Type(레코드 타입)은 필요한 멤버의 이름과 타입을 적는다. `{val a:Int; def b:Int; def f(x:Int):Int}`는 읽을 수 있는 정수 멤버 `a`, 인자 목록 없이 사용하는 정수 메서드 `b`, 정수를 받아 정수를 돌려주는 메서드 `f`를 요구한다. 객체라는 값, 그 값의 정적 타입, 그 타입을 통해 허용되는 멤버 접근을 구분하자.

다음은 Part1 p.70의 코드다. 객체 안의 `val g`와 객체 밖의 `def g`는 다른 Binding(이름 결합)이다. [Part1 PDF p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
import reflect.Selectable.reflectiveSelectable
def bar(x: Int) = x + 1
val foo = new {
  val a = 1 + 2
  def b = a + 1
  def f(x: Int) = b + x
  val g: Int => Int = bar _
}
foo.b
foo.f(3)
val ff: Int => Int = foo.f _
def g(x: {val a: Int; def b: Int;
          def f(x: Int): Int; val g: Int => Int}) =
  x.f(3)
g(foo)
~~~

`foo`를 만들면 `a=3`이다. `foo.b`는 `3+1=4`, `foo.f(3)`은 `4+3=7`이다. 바깥 `g(foo)`도 인자 `x`로 받은 객체에서 `x.f(3)`을 계산하므로 7이다. 이 바깥 함수가 객체의 `g`를 호출한 것은 아니다. `foo.g`에는 `bar`의 함수 값이 들어 있고, `ff`에는 `foo.f`를 함수 값으로 사용하는 자료 표기 `foo.f _`의 결과가 들어 있다. 같은 `Int=>Int` 타입이어도 두 함수의 본문과 정의 환경은 다를 수 있다. Import와 underscore 표기는 공급된 자료의 Scala 문맥을 따른다.

### Type Alias가 바꾸지 않는 것

Type Alias(타입 별칭)는 긴 타입 표현을 다른 이름으로 쓰는 방법이다. 다음 p.71 프로그램은 앞 프로그램과 별개다. 여기의 `f`에는 바깥 `gn`이 추가된다. [Part1 PDF p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
import reflect.Selectable.reflectiveSelectable
type Foo = {val a: Int; def b: Int; def f(x: Int): Int}
val gn = 0
val foo: Foo = new {
  val a = 3
  def b = a + 1
  def f(x: Int) = b + x + gn
}
def g(x: Foo) = {
  val gn = 10
  x.f(3)
}
g(foo)
~~~

`Foo`는 요구 구조의 별칭이지 생성자를 갖는 새 명목 클래스가 아니다. `foo.f`의 자유 이름 `gn`은 정의된 환경의 `gn=0`을 가리킨다. 호출자 `g`의 지역 `gn=10`은 그 결합을 바꾸지 않는다. 따라서 `foo.f(3)`과 `g(foo)`에서 얻는 값은 모두 `(3+1)+3+0=7`이다. 호출자의 같은 철자 이름을 대신 대입하면 Lexical Scope(어휘적 범위)를 잃는다.

### 메서드의 환경과 저장한 함수 값의 환경

p.72에서는 `f(x)=a+x`인 새로운 프로그램을 사용한다. p.70의 `b+x`, p.71의 `b+x+gn`과 합쳐 읽지 않는다. [Part1 PDF p.72](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
def bar(x: Int) = x + 1
val foo = new {
  val a = 2 + 1
  def f(x: Int) = a + x
  val g: Int => Int = bar _
}
val b = foo.f(1)
foo.g(b)
~~~

바깥 환경을 `E1`, 객체 멤버 환경을 `E2`라 하자. `bar`는 `E1`에서 정의된다. 객체 쪽에는 `a=3`, `f(x)=a+x`, 그리고 `bar`의 코드와 원래 환경 `E1`을 묶은 Closure(클로저)가 `g`에 들어간다. `foo.f(1)`은 객체의 `a`와 새 인자 `x=1`을 사용한다.

~~~text
E1:E2:E3[x=1]에서 a+x = 3+1 = 4
따라서 바깥 b = 4
E1:E4[x=4]에서 bar의 x+1 = 4+1 = 5
~~~

두 번째 호출 `foo.g(b)`는 객체 안에 저장되었다는 이유로 `bar`의 정의 환경을 객체 환경으로 바꾸지 않는다. 객체의 메서드가 사용하는 자유 멤버와 저장된 함수 값의 원래 환경을 각각 추적해야 한다. p.72의 `val foo=new ...` 옆에는 `object foo`라는 대응도 있다. 멤버를 가진 한 값을 이름 붙여 선언한다는 연결이며, 모든 singleton·초기화·컴파일 세부가 같다는 주장은 아니다.

## Product와 Sum으로 만드는 재귀 자료

Product(곱)는 여러 성분을 함께 요구한다. Sum(합)은 여러 생성자 대안 중 하나를 구분한다. Algebraic Datatype, ADT(대수적 자료형)는 이 구성을 조합한다. 다음은 자료의 선언 설명 표기다. `of`, `*`, `|`는 이곳에서 Scala 실행식이 아니라 자료형의 구성을 나타낸다. [Part1 PDF p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
Attr = Name of String
     |  Age of Int
     |  DOB of Int * Int * Int
     |  Height of Double
~~~

`DOB(2000,3,10)` 한 경우에는 세 정수가 모두 필요하므로 Product다. 전체 `Attr` 값은 `Name`, `Age`, `DOB`, `Height` 중 한 생성자를 선택하므로 Sum이다. `Age(16)`에 `DOB`의 세 성분까지 들어 있다고 생각하면 서로 다른 대안을 한 Product로 혼동한 것이다.

Recursive ADT(재귀 대수적 자료형)는 생성자의 성분 타입에 자기 타입이 다시 나타난다. [Part1 PDF pp.74–76](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
IList = INil
      |  ICons of Int * IList

BTree = Leaf
      |  Node of Int * BTree * BTree
~~~

`INil()`은 빈 리스트이고 `ICons(hd,tl)`은 정수 하나와 나머지 리스트를 함께 담는다. `ICons(2,ICons(1,INil()))`에는 2 다음에 1이 있고 끝에서 빈 경우를 만난다. `INil`에서 시작하여 생성자를 유한 번 적용하면 유한한 값을 만들 수 있다. 타입이 재귀적이라는 사실이 모든 값이 무한하다는 뜻은 아니다.

트리의 `Leaf()`는 이 정의에서 값이 없는 빈 경우다. `Node(v,l,r)`는 값과 두 하위 트리를 함께 담는다. 빈 경우와 노드 사이가 Sum, 노드 안의 세 성분이 Product, 하위 트리에 `BTree`가 다시 나타나는 것이 Recursion이다. 여기의 `Leaf`를 일상적인 “값은 있고 자식만 없는 잎 노드”와 동일시하면 안 된다.

### Pattern Matching과 길이 계산

Pattern Matching(패턴 매칭)은 어떤 생성자로 값을 만들었는지에 따라 사용하는 Elimination이다. `case C(x,y)`는 `C`로 만든 경우를 골라 그 안의 성분을 사용하게 한다. 전체 결과를 `T`로 쓰려면 가능한 생성자 경우를 처리하고 각 분기 결과를 `T`로 사용할 수 있어야 한다. 다음은 p.76의 리스트 선언과 p.79의 길이 계산이다. [Part1 PDF pp.76, 78–79](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
sealed abstract class IList
case class INil() extends IList
case class ICons(hd: Int, tl: IList) extends IList

def length(xs: IList): Int =
  xs match {
    case INil() => 0
    case ICons(x, tl) => 1 + length(tl)
  }
~~~

빈 경우의 길이는 0이다. `ICons`에서는 현재 원소 하나에 꼬리의 길이를 더한다. 원소 내용 `x`의 크기는 길이에 영향을 주지 않는다.

~~~text
length(ICons(2,ICons(1,INil())))
= 1 + length(ICons(1,INil()))
= 1 + (1 + length(INil()))
= 1 + (1 + 0)
= 2
~~~

구조가 유한하고 각 호출이 더 작은 꼬리로 진행한다는 것이 기저 경우에 도달하는 근거다. 정확한 길이를 `Int`로 센다는 설명에는 구조상의 원소 수가 `0..2147483647` 안에 있고 재귀 호출이 정상 반환한다는 조건도 필요하다. 유한성만으로 정수 표현 범위나 stack·메모리 자원의 충분성이 보장되지는 않는다.

### Option의 부재와 존재를 나누기

`Option[T]`는 `None` 또는 `Some(x)`로 부재와 존재를 나타내는 Sum이다. `Some(3)`은 `Option[Int]`, `Some("abc")`는 `Option[String]` 문맥에서 쓰인다. `None`은 두 문맥 모두에서 부재를 나타낼 수 있지만 정수 0이나 빈 문자열을 숨겨 가진 값은 아니다. [Part1 PDF p.98](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

따라서 `Option[T]` 전체에 `T`의 멤버가 있다고 가정할 수 없다. 먼저 `Some(v)`인 경우에서 `v:T`를 얻고 그 타입이 허용하는 사용을 한다. 다음은 이 차이를 보이는 설명용 예다.

~~~text
o match {
  case None => 0
  case Some(v) => v + 1
}
~~~

여기서는 `o:Option[Int]`를 가정한다. 0은 이 예가 부재에 대해 선택한 결과이며 `None`의 내용물이 아니다. `Some` 분기에서만 `v:Int`를 얻으므로 덧셈을 정당화한다. p.92의 ADT `MyList[A]`는 다시 `MyNil` 또는 `MyCons`다. 그러므로 `Option[MyList[A]]`에서 머리를 사용하려면 바깥 `Some`을 확인한 뒤 안쪽 `MyCons`도 확인해야 한다. 뒤의 클래스형 노드 `MyList[A]`와 이 ADT의 동명 정의는 별개다.

## Parametric Polymorphism과 공통 구조의 차이

Parametric Polymorphism(매개변수 다형성)은 타입을 매개변수로 받아 같은 계산 구조를 여러 타입에 사용하는 방식이다. 다음은 자료의 함수다. [Part1 PDF pp.90–91](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

~~~text
def id[A](x: A): A = x

def applyn[A](f: A => A, n: Int, x: A): A =
  n match {
    case 0 => x
    case _ => f(applyn(f, n - 1, x))
  }
~~~

`id[A]`는 `A`의 구체적인 멤버를 조사하지 않고 받은 값을 돌려준다. 따라서 `id(3)`과 `id("abc")`는 같은 본문을 사용한다. 자료의 `id[T] _`는 타입 인자를 정한 뒤 `T=>T` 함수 값으로 쓰는 표기다. 자료가 설명하는 다형 함수 값 표기의 제한을 모든 Scala 버전의 불가능 정리로 받아들이지는 않는다.

`applyn`은 `A=>A`의 출력을 다시 같은 타입의 입력으로 사용할 수 있다. `n>=0`이고 각 함수 적용과 재귀 호출이 정상 반환한다면 다음처럼 전개한다.

~~~text
applyn(f,0,x) = x
applyn(f,1,x) = f(x)
applyn(f,2,x) = f(f(x))
applyn((x:Int)=>x+1,100,3) = 3+100 = 103
~~~

원래 함수에는 음수를 거르는 검사가 없다. 모든 정수 `n`에서 “정확히 n번 적용하고 종료한다”는 설명으로 확대하면 안 된다. 이 예의 3부터 103까지의 덧셈은 `Int` 범위 안이다.

자료의 `MyOption[A]`, `MyList[A]`, `BTree[A]`도 성분 타입만 바꾸면서 생성 구조를 재사용한다. `MyCons[A](hd:A,tl:MyList[A])`의 머리와 꼬리는 같은 `A`를 공유하고, `Node[A]`의 값과 두 하위 트리도 같은 타입 인자를 공유한다. 이 매개변수화만으로 `A <: B`에서 `MyList[A] <: MyList[B]`가 자동으로 성립한다는 결론은 나오지 않는다. [Part1 PDF p.92](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

임의의 `r:A`에서 `r.name`을 읽으려면 추가 근거가 필요하다. `id`와 달리 `.name`은 특정 이름과 타입의 멤버를 요구하고, 임의의 `A`에는 그런 멤버가 없을 수 있다. 다음 단원의 공통 구조가 이 요구를 표현한다. [Part1 PDF p.100](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

이 구분은 타입에 필요한 연산을 함수 인자로 제공하는 설계로도 이어진다. 2024 중간 Q3-4의 역사적 코드에서 확인되는 연결은 “타입 매개변수만으로 산술 연산을 가정하지 않고, 필요한 연산을 함수로 공급한다”는 추론이다. 예외·결과 자료형을 포함한 그 평가기 전체 구현은 이 선수 개념에 포함하지 않는다. [EX:pop_2024_mid_q03_s04 L.77-81]

## 확인·연습문제

### 자료형의 생성과 사용

#### 확인 Q01 · Introduction과 Elimination

`(1,"a",10)`의 타입과 세 Projection 결과를 쓰고, Tuple 생성·Projection·함수 생성 `(x:T)=>e`·적용 `f(v)`을 Introduction과 Elimination으로 분류하라. Tuple 접근과 Record 접근의 기준도 비교하라.

<details><summary>해설 보기</summary>

Tuple 타입은 `(Int,String,Int)`이며 `._1=1`, `._2="a"`, `._3=10`이다. 전체 Tuple을 묶는 식과 함수 값을 만드는 식은 Introduction이다. Projection은 이미 있는 Tuple을 사용하고, `f(v)`는 이미 있는 함수에 알맞은 입력을 주어 결과를 계산하므로 Elimination이다. 제거는 메모리 삭제가 아니다. Tuple은 위치로, Record의 `r.name`은 이름으로 성분을 선택한다. 성분 수와 위치별 타입은 별개 정보이며 모든 성분의 타입이 같을 필요는 없다.

**확인 기준**

- 네 연산의 분류와 세 Projection의 값·타입을 맞췄는가?
- 위치 접근과 이름 접근, 함수 적용의 입력·결과 타입 조건을 구분했는가?

</details>

### 객체 멤버와 정의 환경

#### 확인 Q02 · p.70의 메서드와 저장한 함수

p.70에서 `bar(x)=x+1`, 객체의 `a=1+2`, `def b=a+1`, `def f(x:Int)=b+x`, `val g:Int=>Int=bar _`다. 바깥 `def g(x:요구구조)=x.f(3)`도 있다. `foo.b`, `foo.f(3)`, 바깥 `g(foo)`를 계산하고 `foo.g`와 `foo.f _`를 비교하라.

<details><summary>해설 보기</summary>

`a=3`이므로 `b=4`, `f(3)=4+3=7`이다. 바깥 `g(foo)`는 받은 객체에서 `f(3)`을 호출하므로 역시 7이며 객체의 동명 `g`를 호출하지 않는다. `foo.g`는 `bar`의 함수 값을 저장하고, `foo.f _`는 자료 표기에서 객체의 `f`를 함수 값으로 사용한다. 후자는 `b+x`를 계산하며 객체 멤버를 사용한다. 둘 다 `Int=>Int`여도 계산과 정의 환경까지 같지는 않다. 객체 값, 그 정적 타입, 타입을 통해 허용된 멤버 사용을 구분한다.

**확인 기준**

- `a=3,b=4,f(3)=7,g(foo)=7`을 도출했는가?
- 객체 `g`와 바깥 `g`, 함수 값을 담은 `val`과 `def`를 구분했는가?

</details>

#### 확인 Q03 · Alias와 호출자의 지역 이름

별개의 p.71 프로그램에서 `type Foo={val a:Int;def b:Int;def f(x:Int):Int}`는 무엇인가? 객체 쪽 `a=3,b=a+1,f(x)=b+x+gn`, 바깥 `gn=0`이다. 호출 함수의 지역 `gn=10`에서 `x.f(3)`을 부르면 결과가 달라지는가?

<details><summary>해설 보기</summary>

`Foo`는 요구 구조의 Type Alias이며 새 명목 클래스나 생성자가 아니다. `f`의 자유 이름 `gn`은 정의된 환경의 0을 가리키고 호출자의 지역 이름은 그 결합을 바꾸지 않는다. `b=4`, `foo.f(3)=4+3+0=7`이고 호출 함수 안의 `x.f(3)`도 7이다. 17이라는 해법은 호출 환경을 정의 환경으로 잘못 사용한 것이다.

**확인 기준**

- 별칭과 객체 생성을 구분했는가?
- 7의 전개와 호출자의 10이 사용되지 않는 이유를 썼는가?

</details>

#### 확인 Q04 · p.72의 두 호출 환경

별개의 p.72 프로그램이다. 바깥 `E1`에 `bar(x)=x+1`, 객체 `E2`에 `a=3`, `f(x)=a+x`, `g=bar _`가 있다. `val b=foo.f(1)` 뒤 `foo.g(b)`의 값을 구하고 두 호출의 환경을 구분하라.

<details><summary>해설 보기</summary>

첫 호출은 객체의 `a=3`과 새 인자 `x=1`을 사용하므로 `b=4`다. 다음은 `g`에 저장된 `bar`의 코드와 원래 환경 `E1`에서 새 인자 `x=4`로 `4+1=5`를 얻는다. 객체에 저장했다는 이유로 함수의 원래 환경을 객체 환경으로 바꾸지 않는다. p.70의 `b+x`, p.71의 `b+x+gn`과 이 `a+x`를 하나의 정의로 합치지 않는다. 자료의 `object foo` 대응은 멤버를 가진 한 값에 이름을 준다는 연결이며 모든 초기화·컴파일 세부의 동일성은 아니다.

**확인 기준**

- `b=4`와 최종 5의 서로 다른 본문을 설명했는가?
- 객체 메서드 환경과 저장한 Closure 환경을 구분했는가?

</details>

### 곱·합·재귀와 다형성

#### 확인 Q05 · ADT의 대안과 성분

`Attr=Name of String | Age of Int | DOB of Int*Int*Int | Height of Double`에서 Sum과 Product를 찾으라. `IList=INil | ICons of Int*IList`와 `BTree=Leaf | Node of Int*BTree*BTree`의 재귀와 기저 경우, Pattern Matching의 역할도 설명하라.

<details><summary>해설 보기</summary>

`Attr` 전체는 생성자 하나를 택하는 Sum, `DOB`의 세 정수는 모두 필요한 Product다. `Age(16)`가 다른 대안의 성분까지 가진 것은 아니다. `INil`은 빈 리스트이고 `ICons`는 머리와 꼬리의 Product이며 꼬리에 자기 타입이 나타난다. 이 정의의 `Leaf`는 값 없는 빈 트리, `Node`는 값과 두 하위 트리다. 빈 경우에서 유한 번 구성하여 유한한 재귀 값을 만들 수 있다. Matching은 주어진 값의 생성자를 골라 성분을 사용하는 Elimination이다. 모든 대안을 처리하고 각 분기 결과를 요구 결과 타입으로 쓸 수 있어야 한다.

**확인 기준**

- 대안 사이의 합과 대안 안의 곱을 구분했는가?
- `Leaf`의 빈 의미, 자기 참조, 분기 결과 타입 조건을 설명했는가?

</details>

#### 확인 Q06 · 길이의 재귀 전개와 조건

`length(INil())=0`, `length(ICons(x,tl))=1+length(tl)`이다. `ICons(2,ICons(1,INil()))`의 길이를 전개하라. 원소를 200과 -10으로 바꾸면 길이가 달라지는가? 정확한 `Int` 길이에 필요한 조건은?

<details><summary>해설 보기</summary>

`1+length(ICons(1,INil()))=1+(1+length(INil()))=1+(1+0)=2`다. 원소 크기를 세지 않으므로 값을 바꿔도 2다. 유한한 구조에서 실제로 더 작은 꼬리로 진행하고 재귀가 정상 반환해야 한다. 구조상의 원소 수는 `0..2147483647` 안에 있어야 정확한 `Int`로 표현된다. 유한성만으로 정수 범위·stack·메모리 충분성이나 임의 재귀 프로그램의 종료를 보장하지 못한다.

**확인 기준**

- 머리 값의 합과 원소 수를 구분했는가?
- 감소하는 구조·기저 경우·정상 반환·정수 범위·자원을 구분했는가?

</details>

#### 확인 Q07 · Option 안에도 남는 대안

`o:Option[Int]`에서 `None=>0; Some(v)=>v+1`로 나누는 이유는? `Option[MyList[A]]`의 `MyList`가 Part1의 `MyNil/MyCons` ADT라면 머리를 사용하기까지 무엇을 확인해야 하는가?

<details><summary>해설 보기</summary>

`None`에는 정수가 없으므로 Option 전체에 정수 연산을 요구할 수 없다. `Some(v)`에서 얻은 `v:Int`에만 `+1`을 적용한다. 0은 이 함수가 부재에 대해 정한 결과이며 `None`의 숨은 값이 아니다. ADT 리스트를 감싼 경우 바깥 `None/Some`을 나눈 뒤 `Some(xs)`의 `xs`도 `MyNil/MyCons`를 나눈다. `MyCons(h,tl)`에서만 머리 `h:A`를 얻는다. 뒤의 클래스형 노드 `MyList[A]`와 동명 정의를 합치면 안 된다.

**확인 기준**

- 바깥 부재와 안쪽 빈 리스트를 별개로 처리했는가?
- `Some`만으로 `MyCons`를 가정하지 않았는가?

</details>

#### 확인 Q08 · 타입 매개변수와 공통 구조

`def id[A](x:A):A=x`가 정수·문자열에 같은 본문을 쓰는 이유와, 제약 없는 `r:A`에서 `r.name`을 읽을 수 없는 이유는? `MyList[A]`·`BTree[A]`의 매개변수화가 보존하는 것과 자동으로 주지 않는 관계도 쓰라.

<details><summary>해설 보기</summary>

`id`는 `A`의 멤버를 조사하지 않고 받은 값을 돌려주므로 `id(3)=3`, `id("abc")="abc"`다. `.name`은 특정 이름·타입의 멤버를 요구하여 임의 `A`에 없는 추가 근거가 필요하다. 매개변수 자료형은 머리·꼬리 또는 값·자식들이 같은 `A`를 공유하는 생성 구조를 여러 성분 타입에 재사용한다. 매개변수화만으로 `A <: B`에서 `MyList[A] <: MyList[B]`가 자동으로 나오지 않는다.

**확인 기준**

- 반환만 하는 연산과 멤버 접근의 요구 차이를 설명했는가?
- 생성 구조 재사용과 자동 Covariance를 구분했는가?

</details>

#### 확인 Q09 · applyn의 전개

`applyn(f,0,x)=x`, 그 외에는 `f(applyn(f,n-1,x))`다. 1회·2회 전개와 `applyn((x:Int)=>x+1,100,3)`을 계산하라. 음수 `n`에도 같은 종료 설명을 적용할 수 있는가?

<details><summary>해설 보기</summary>

1회는 `f(x)`, 2회는 `f(f(x))`다. `A=>A`의 출력을 다시 같은 타입 입력으로 사용한다. `n>=0`이고 각 적용·재귀가 정상 반환하면 3에 1을 100번 더해 103이다. 이 계산의 수들은 `Int` 범위 안이다. 음수 거부 검사가 없으므로 모든 정수에 대해 정확히 `n`번 적용하고 종료한다는 주장은 성립하지 않는다. 음수에서 `n-1`은 이 자연수 기저 경우를 향한 감소 논증이 아니다.

**확인 기준**

- 중간 출력과 다음 입력의 타입을 연결했는가?
- 103과 비음수·정상 반환 조건을 함께 썼는가?

</details>

### 자료 기반 연습

#### 연습 P01 · 두 층의 빈 경우

새로 쓴 자료 기반 일반 연습이며 직접 대응하는 기출 형식 근거는 없다. Part1의 `MyList[A]=MyNil | MyCons of A*MyList[A]`를 사용한다. `Option[MyList[Int]]`인 (가) `None`, (나) `Some(MyNil())`, (다) `Some(MyCons(8,MyNil()))`에서 각각 `"부재"`, `"빈 리스트"`, `"머리 있음"`을 반환하는 경우 분석을 제시하라. (나)에서 머리를 읽으면 왜 잘못되는가?

<details><summary>해설 보기</summary>

설명용 경우 분석은 다음과 같다.

~~~text
입력 match {
  case None => "부재"
  case Some(xs) => xs match {
    case MyNil() => "빈 리스트"
    case MyCons(h,tl) => "머리 있음"
  }
}
~~~

(가)는 리스트 값의 부재, (나)는 리스트 값은 있으나 원소가 없음, (다)는 머리 8과 꼬리가 있는 경우다. `Some`이 있다는 사실로 안쪽의 `MyCons`까지 가정하면 (나)를 처리하지 못한다. 두 합을 순서대로 제거한다.

**확인 기준**

- 세 입력이 각 분기로 가는 과정을 확인했는가?
- 바깥·안쪽의 모든 대안을 처리했는가?

</details>

#### 연습 P02 · 임의 타입의 연산을 공급하기

새로 쓴 합성 연습이다. 2024 중간 Q3-4에서 필요한 연산을 함수로 공급한다는 추론만 연결한다 [EX:pop_2024_mid_q03_s04 L.77-81]. 선수는 함수 적용, `A=>A`와 타입 매개변수이며 평가기·예외·결과 ADT 구현은 범위 밖이다. `def twice[A](step:A=>A,x:A):A`의 본문을 쓰고 문자열에 `"!"`를 붙이는 `step`으로 `"go"`를 처리하라. `x+1`로 직접 쓰면 왜 임의 `A`에 부적절한가?

<details><summary>해설 보기</summary>

본문은 `step(step(x))`다. 안쪽 결과 `A`가 바깥 입력에 맞는다. `step=(s:String)=>s+"!"`이면 `"go" -> "go!" -> "go!!"`다. `x+1`은 `A`에 특정 연산이 있음을 요구하지만 제약 없는 `A`에는 그 근거가 없다. 필요한 연산을 타입이 명시된 함수 인자로 공급하면 본문은 그 함수 적용만 사용한다. 두 적용의 정상 반환을 전제로 한다. 역사적 평가기나 제공 답을 재현한 문제가 아니다.

**확인 기준**

- 두 적용의 중간 타입과 `"go!!"`를 확인했는가?
- 연산을 추측하지 않고 공급하는 설계 이유를 설명했는가?

</details>

## 출처

[프로그래밍의 원리 Part1 · PDF pp.68–74, 76, 78–79, 90–92, 98, 100](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

[[courses/principles_of_programming/lectures/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 · Data Type 선수 개념과 Structural Subtyping · 강의 정리]]

이 단원의 선수 개념은 선택한 Part1 자료에 근거한다. 관련 강의 정리는 2차 설명이며 Part1 pp.63–100 전체의 녹음 진도를 입증하지 않는다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 전사 · 06:03–07:00의 선수 개념 회고]]도 이 범위의 상세 구두 설명을 대신하지 않는다.

자료의 reflectiveSelectable·underscore·다형 함수 값·Tuple 길이 22 표기는 해당 표기 문맥을 따른다. 강의 날짜와 빠진 실제 코드·그림은 확인되지 않았고, 음성 대조나 실제 컴파일·실행 관찰에 근거한 설명은 아니다.

기출 연결은 2024 중간 Q3-4의 연산 함수 공급이라는 추론에 한정한다 [EX:pop_2024_mid_q03_s04 L.77-81]. 2024라는 연도는 2025년 전년도 문제 업로드 공지에 근거한다. Q3 표제의 40점과 소문항 합 35점은 원본 불일치로 남아 있으며 누락 문항을 추정하지 않는다. 당시 점수·제한·일정은 현재 시험 정책이나 출제 예측의 근거가 아니다.


---

[[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/structural-subtyping|다음: Structural Subtyping과 함수의 대체 가능성 →]]
