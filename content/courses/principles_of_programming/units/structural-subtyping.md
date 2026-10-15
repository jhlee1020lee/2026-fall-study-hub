---
title: "Structural Subtyping과 함수의 대체 가능성"
description: "읽기 전용 레코드·튜플·함수의 부분형 관계와 중첩 함수의 대체 방향을 확인한다."
course: "principles_of_programming"
unit_id: "structural-subtyping"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["lecture-part2.pdf", "lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/undated-structural-subtyping-6p3wjj22vvvjv0ji"]
---

## 공통 멤버로 표현하는 Structural Subtyping

같은 `greeting`을 서로 다른 구조의 값에 적용하고 싶다고 하자. 프로그래밍의 원리 Part2(NM001) p.3에서 `tom`은 `name`과 `home`, `bob`은 `name`과 `mobile`을 갖는다. 필드 값의 타입은 모두 `String`이다. `greeting`이 읽는 것은 `r.name`뿐이므로 입력에 불필요한 `home`이나 `mobile`까지 요구할 이유는 없다. [Part2 PDF pp.3–4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-004)

~~~text
import reflect.Selectable.reflectiveSelectable
type NameHome = { val name: String; val home: String }
type NameMobile = { val name: String; val mobile: String }
type Name = { val name: String }

def greeting(r: Name) = "Hi " + r.name + ", How are you?"
~~~

`NameHome`을 요구하면 `home`이 없는 `bob`을 받을 근거가 없고, `NameMobile`을 요구하면 `tom` 쪽에 같은 문제가 생긴다. `Name`은 필요한 `name:String`만 요구한다. 따라서 다음 두 관계가 한 코드의 사용을 정당화한다.

~~~text
NameHome <: Name
NameMobile <: Name
~~~

Subtype Polymorphism(부분형 다형성)은 이처럼 한 코드를 여러 입력 타입에 사용하는 방식이다. `tom`·`bob`은 값의 이름, `Name`은 구조의 Type Alias(타입 별칭), `name`은 읽는 멤버다. `type Name=...`가 새 명목 클래스를 만든 것은 아니다. `object` 선언은 여기서 멤버를 가진 한 값에 이름을 주는 역할을 한다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 07:00·16:45]]

`r:Name`을 통해 보장되는 것은 읽을 수 있는 `name:String`이다. `name:Int`만 있는 값은 이름만 같을 뿐 요구 타입을 충족하지 않는다. 제약 없는 타입 변수 `A`도 `name`을 보장하지 않는다. 이것이 [자료형 선수 개념](datatype-prerequisites.md)의 Parametric Polymorphism과 다른 점이다. 원래 값에 `home`이 있더라도 `r:Name`이라는 정적 정보만으로 `r.home`까지 사용할 수 있는 것은 아니다. 자료의 문자열 식을 전개하면 `tom`의 이름에서는 `"Hi Tom, How are you?"`, `bob`의 이름에서는 `"Hi Bob, How are you?"`를 얻는다. 이는 식의 계산이다.

### 허용된 Elimination을 보존하는 관계

`T <: S`는 `T`의 모든 값을 `S`의 값처럼 사용할 수 있다는 관계다. 왼쪽 값을 오른쪽 타입을 요구하는 자리에 공급하는 방향으로 읽는다. 자료는 “사용할 수 있다”를 집합에서의 문자 그대로의 원소 소속과 구분한다. Subtyping을 설명하려고 두 타입의 메모리 표현이나 값 집합이 먼저 같다고 가정할 필요는 없다. [Part2 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-005)

Elimination(제거), 즉 이미 주어진 값의 사용을 보면 이 관계를 구체적으로 확인할 수 있다. `Name`의 소비자는 `.name`을 읽어 문자열을 얻는다. `NameHome`에도 그 멤버가 있으므로 같은 사용을 제공한다. 반대로 임의의 정수를 `Name`처럼 받아 `.name`을 읽게 하는 규칙에는 이 근거가 없다. 특정 호출이 우연히 멤버를 읽지 않았다는 사실보다, 요구 타입이 허용하는 사용을 보존하는지가 중요하다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 20:00·22:40]]

`h:S=>R`가 `S`에서 허용된 연산으로 결과를 만든다면 `T <: S`인 입력도 `S`처럼 사용할 수 있다. 따라서 `h`를 `T=>R`을 요구하는 자리에 넣을 수 있다.

~~~text
T <: S이면 (S=>R) <: (T=>R)
~~~

관계는 타입 사이에 있다. 값 이름 `a`, `b` 자체가 서로의 Subtype이라는 뜻이 아니다. 또한 이 정적 사용 가능성만으로 성능이나 업무상의 행동 계약까지 같아지지는 않는다.

## Structural 관계와 Nominal 관계

Structural Subtyping(구조적 부분형)은 멤버 이름과 타입을 포함한 구조로 관계를 정한다. 같은 구조의 별칭 둘을 비교할 때는 이름의 철자보다 풀어 쓴 요구를 본다. 자료가 사용하는 Duck Typing이라는 별칭도 이 문맥에서 읽는다. 그 이름만으로 타입 검사가 반드시 런타임에 이루어진다는 결론은 나오지 않는다.

Nominal Subtyping(명목적 부분형)은 이름 있는 타입 사이에 명시된 관계를 사용한다. 클래스 `A`와 `B`의 멤버 모양이 같아도 별개의 선언만으로 `B <: A`가 생기지 않는다. `extends` 같은 선언으로 관계를 정하고 그 관계의 허용 조건도 만족해야 한다. 따라서 구조를 줄여 쓴 Alias와 명목 타입을 도입한 클래스는 다르게 판단한다. 자료의 Ad hoc Polymorphism은 그 자료가 Nominal Sub Types에 붙인 명칭이다. [Part2 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-007) [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 43:41·45:36]]

### Reflexivity와 Transitivity

Reflexivity(반사성)는 모든 타입을 자기 타입이 필요한 자리에 쓸 수 있다는 규칙이다. Transitivity(추이성)는 중간 타입을 통해 사용 가능성을 연결한다. [Part2 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-009)

~~~text
T <: T

T <: R    R <: S
----------------
T <: S
~~~

`T`를 `R`처럼 사용할 수 있고 `R`을 `S`처럼 사용할 수 있으면 `T`를 `S`를 요구하는 자리에서도 쓴다. 결론은 `T <: S`다. `S <: T`는 따로 증명해야 한다. 예를 들어 `name,home`을 가진 값은 `name`만 요구하는 곳에 들어가지만, `name`만 있는 값이 `home`까지 제공하지는 않는다. 반사성도 이 역방향을 보충하지 않는다.

## Read-only Record의 세 규칙

여기서는 읽기 전용 `val` 멤버를 비교한다. Record의 Permutation(순열), Width(너비), Depth(깊이)는 각각 다른 질문을 해결한다. [Part2 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011)

| 규칙 | 확인하는 조건 | 허용하는 사용 |
| --- | --- | --- |
| Permutation | 멤버 이름과 타입이 같음 | 나열 순서가 달라도 이름으로 같은 멤버를 읽음 |
| Width | 요구하는 필드가 모두 제공됨 | 추가 필드가 있는 값을 적은 필드의 관점으로 사용 |
| Depth | 같은 읽기 필드에서 `T <: S` | `x:T`에서 읽은 값을 `S`처럼 사용 |

Permutation은 `{val x:Int;val y:String}`을 `{val y:String;val x:Int}`처럼 사용할 수 있게 한다. `x`와 `y`의 이름이나 타입 자체를 바꾸는 규칙은 아니다. 반대 순열도 적용할 수 있지만 임의의 Subtype 관계 전체가 대칭인 것은 아니다.

Width에서는 `NameHome <: Name`이다. 소비자가 `name`만 읽으면 되는 곳에 `home`이 더 있어도 문제가 없다. 역방향은 `home`의 존재를 보장하지 못한다. 필드를 덜 요구한다는 것은 정적 관점의 변화이며 실제 객체에서 필드를 삭제하는 명령이 아니다.

Depth의 전제는 다음과 같다.

~~~text
T <: S
-----------------------------------
{val x:T; ...} <: {val x:S; ...}
~~~

왼쪽의 `.x`는 `T`를 준다. 그 결과를 `S`처럼 쓸 수 있으므로 오른쪽의 소비자도 필요한 사용을 할 수 있다. 같은 이름의 필드라는 사실에 더해 결과 타입의 관계가 필요하다. 강의의 “점 x에서 나오는 값이 다시 S처럼 사용될 수 있으니까 되겠다”는 설명이 이 근거다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 01:01:26]]

### 중첩 레코드의 안쪽과 바깥쪽

p.12의 구조에 설명용 이름 `A,B,C`를 붙여 보자. [Part2 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-012)

~~~text
A = {val x:{val y:Int;val z:String};val w:Int}
B = {val w:Int;val x:{val y:Int;val z:String}}
C = {val w:Int;val x:{val z:String}}
~~~

먼저 바깥 순서를 바꾸는 Permutation으로 `A <: B`다. 다음으로 안쪽에 Width를 적용한다.

~~~text
{val y:Int;val z:String} <: {val z:String}
~~~

이 관계를 바깥 필드 `x`의 Depth로 올려 `B <: C`를 얻는다. `w:Int`는 그대로 두며, Transitivity로 `A <: C`다. `C`를 요구하는 코드는 `r.w`와 `r.x.z`를 읽을 수 있고 `A`는 그 사용을 모두 제공한다. `y`는 바깥 필드가 아니라 `x` 안의 필드이므로 바깥 Width 하나로 없앴다고 설명하면 층위를 잘못 짚는다.

쓰기까지 가능한 `var`에 같은 Depth 방향을 자동으로 옮기면 안 된다. 설명용 반례로 `var x:NameHome`인 저장 위치를 `var x:Name`처럼 허용했다고 하자. 넓어진 관점의 사용자는 `name`만 가진 값을 써 넣을 수 있다. 원래 사용자는 여전히 `x.home`을 읽을 수 있다고 기대하므로 보장이 깨진다. 읽어서 얻는 값의 조건과 써 넣는 값의 조건을 따로 확인해야 한다.

### Table Lookup과 Fixed Offset의 조건

같은 사용을 허용하는 규칙과 그 사용을 구현하는 방법은 별개의 문제다. 날짜 미확인 강의는 필드 이름과 내용을 표처럼 두고 `.name`에서 이름을 찾는 Table Lookup(표 검색) 모형을 제안한다. 이 모형에서는 추가 필드나 순서가 달라도 같은 이름 찾기를 설명할 수 있다. 이름 저장 공간과 검색 작업이 들 수 있다는 설명도 이 모형의 분석이다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 28:13·30:07·32:07]]

Fixed Offset(고정 위치) 모형은 필드를 정해진 칸에서 읽는다고 생각한다. 그런데 “각 타입을 선언 순서대로 저장한다”와 “모든 Subtype의 `name`이 첫 칸이다”를 함께 가정하면 `{val home:String;val name:String}`이 반례가 된다. 이 구조도 Permutation과 Width로 `Name`처럼 쓸 수 있지만 그 가상 배치에서 첫 칸은 `home`이다.

이 반례는 그 단순 배치 가정이 불충분하다는 뜻이다. 다른 표현이나 컴파일 방법까지 배제하여 런타임 검색이 필수라고 증명한 것은 아니다. 강사도 실제 구현을 모른다고 유보하고 코드 생성 횟수에 관한 처음 생각을 다시 검토한다. 따라서 특정 포인터 폭·압축 단위·검색 비용·상속의 성능 우위는 이 논의에서 확인된 구현 사실로 쓰지 않는다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 36:23·37:00]]

## Any와 Nothing의 생성·사용

자료는 `Nothing`을 정상 값이 없는 타입, `Any`를 모든 값을 받아들이는 타입으로 소개한다. Top(최상위)과 Bottom(최하위)은 이 Subtype 관계의 양끝이다. [Part2 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010)

~~~text
Nothing <: T <: Any
~~~

`Nothing`의 정상 값을 만드는 Introduction은 없다. 따라서 “그 모든 값을 `T`처럼 사용할 수 있다”는 전칭 명제에 실제 값을 골라 실패하는 반례도 없다. 값이 없다는 전제에서 공허하게 성립한다. 이미 `Nothing` 값을 받았다고 가정하면 어떤 결과 타입이 필요한 자리에서도 쓸 수 있다는 설명과, 실제로 그런 정상 값을 만들어 공급할 수 있다는 주장은 다르다. 강의의 빈 생성자·빈 case 분석 비유도 불가능한 입력 가정을 설명하는 것이다. 특정 빈 `match` 문법의 컴파일 성공까지 얻지는 않는다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 53:17·57:15]]

~~~text
val a: Int = 3
val b: Any = a
def f(a: Nothing): Int = a
~~~

`f`의 매개변수 `a`는 `Nothing`이고 `Nothing <: Int`이므로 결과의 `Int` 자리에 쓴다. 그러나 정상적인 `Nothing` 인자를 얻은 것은 아니다. 예외를 던지거나 발산하는 `Nothing` 타입 식이 있어도 그 식이 정상 종료하여 넘길 값을 반환한다는 뜻은 아니다.

`Any`는 넓게 받아들이는 대신 특정 구조의 정적 정보를 잃는다. `Int <: Any`이므로 위 대입은 허용되지만, `b:Any`만 보고 정수 전용 연산이나 `.name`을 정당화할 수는 없다. 다른 타입의 값도 허용하기 때문이다. 강의의 “Any에는 Elimination이 없다”는 대비는 여기서는 특정 자료형의 연산을 마음대로 요구할 수 없다는 뜻으로 한정해야 한다. 모든 Scala 공통 연산이 없다는 주장은 아니다. 원문에서 손상된 긍정·부정 표현을 고쳐 인용한 것이 아니라 자료의 타입 규칙으로 설명한 것이다.

## Tuple Subtyping의 같은 Arity

Tuple은 이름 대신 위치로 성분을 읽는다. 여기서 제시된 규칙은 같은 Arity와 같은 위치를 유지하는 Depth다. `T <: S`일 때 다음이 성립한다. 나머지 위치의 타입은 그대로 둔다. [Part2 PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-013)

~~~text
(...,T,...) <: (...,S,...)
~~~

강의는 성분 개수가 같아야 한다는 조건을 두 번 강조한다. `Int <: Any`를 첫째와 셋째 위치에 차례로 적용하면 다음 설명용 관계를 얻는다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 01:04:12·01:04:58]]

~~~text
(Int,String,Int) <: (Any,String,Int) <: (Any,String,Any)
~~~

모든 단계에 세 성분이 있고 가운데는 `String`이다. `(Int,String,Int) <: (Int,String)`이라는 Width는 이 규칙에서 나오지 않는다. `(t._1,t._2)`로 새 Tuple을 만드는 계산과 기존 값의 Subtyping은 구분한다. 또한 `(Int,String)`을 `(String,Int)`처럼 쓰면 첫 성분을 문자열로 읽는 소비자에게 정수를 준다. Record의 이름 기반 Permutation을 Tuple의 위치 교환에 적용할 수는 없다. 더 긴 Tuple도 허용할 수 있겠다는 강의 중 생각은 이 규칙과 별개다.

## Function Subtyping의 입력과 출력

함수를 대체할 때는 사용하는 쪽이 무엇을 공급하고 무엇을 기대하는지 따로 본다. 자료의 정확한 규칙은 다음과 같다. [Part2 PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

~~~text
T <: T'     S <: S'
---------------------------
(T'=>S) <: (T=>S')
~~~

오른쪽 `T=>S'`를 약속받은 사용자는 `T`를 공급하고 결과를 `S'`로 사용한다. 왼쪽 실제 함수는 `T'`만 요구한다. `T <: T'`이므로 공급된 인자를 받아들일 수 있다. 실제 결과 `S`도 `S <: S'`이므로 약속된 결과 자리에서 사용된다.

입력은 관계가 뒤집히는 Contravariance(반공변), 출력은 같은 방향인 Covariance(공변)다. 결과를 만드는 것과 주어진 입력을 사용하는 것이 다르기 때문이다. 강의도 입력의 Elimination과 출력의 Introduction을 대비한다. `A=>B`를 “A를 가정하고 B를 얻는다”는 함의의 모습과 연결하지만, 이 비유 자체가 프로그래밍과 수학 전체의 완전한 동일성 정리는 아니다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 01:06:53·01:11:03·01:12:03]]

입력 방향의 반례를 보자. `Name`만 받는다고 공개한 자리에 `NameHome`을 받아 `home`도 읽는 함수를 넣으면, 사용자는 `name`만 공급할 수 있으므로 실패한다. 반대로 `name`만 읽는 함수는 `name,home`을 함께 주는 사용자를 받을 수 있다.

출력에서도 `XY={val x:Int;val y:Int}`, `X={val x:Int}`이면 `XY <: X`다. `XY`를 반환하는 함수는 `X`만 기대하는 곳에서 쓸 수 있지만, `X`만 반환하는 함수를 `XY` 약속에 넣으면 `.y`를 보장하지 못한다. 두 방향을 같은 방식으로 외우면 이런 반례를 놓친다.

### AB에서 XY를 만드는 함수의 대체

다음은 같은 p.14의 코드다.

~~~text
import reflect.Selectable.reflectiveSelectable
def foo(s: {val a: Int; val b: Int}): {val x: Int; val y: Int} = {
  object tmp {
    val x = s.b
    val y = s.a
  }
  tmp
}
val gee: {val a: Int; val b: Int; val c: Int} => {val x: Int} =
  foo _
~~~

설명용으로 입력 구조를 `AB`, `ABC`, 결과 구조를 `XY`, `X`라 줄여 쓰자. `foo:AB=>XY`는 입력의 `b`를 결과의 `x`로, 입력의 `a`를 결과의 `y`로 넣어 새 객체를 만든다. 기존 필드의 나열 순서를 바꾼 Permutation이 아니다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 01:16:31]]

~~~text
ABC <: AB           XY <: X
--------------------------------
(AB=>XY) <: (ABC=>X)
~~~

일반 규칙에 `T=ABC,T'=AB,S=XY,S'=X`를 넣은 것이다. `gee`의 사용자는 `a,b,c`를 주지만 실제 `foo`는 `a,b`만 읽는다. 결과에는 `x,y`가 있고 사용자는 `x`만 읽는다. 설명용 입력 `a=2,b=9,c=100`에서는 결과가 `x=9,y=2`이며 `gee`를 통한 `.x` 읽기는 9다. `c`를 사용하지 않고 `y`를 요구하지 않는 것이지 데이터를 물리적으로 삭제한 것은 아니다. [[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 NT001 01:17:32·01:18:32]]

역방향 `(ABC=>X) <: (AB=>XY)`는 일반적으로 성립하지 않는다. 실제 함수가 `c`를 필요로 할 수 있고 결과에 `y`가 없을 수 있다. 입력과 출력 중 어느 한쪽의 사용을 보장하지 못해도 대체는 실패한다.

### Higher-order Function에서 방향을 다시 적용하기

Higher-order Function(고차 함수)은 함수 값을 인자나 결과로 다룬다. 아래는 자료의 함수 규칙에서 유도한 설명용 사례다. `F=AB=>XY`, `G=ABC=>X`라 두면 이미 `F <: G`를 얻었다.

함수를 반환하는 바깥 함수에는 출력 Covariance를 적용한다.

~~~text
P <: P    F <: G
-----------------------
(P=>F) <: (P=>G)
~~~

`P`를 공급한 사용자가 `G`를 기대해도 실제로 받은 `F`를 `G`처럼 쓸 수 있다. 즉 `P=>(AB=>XY)`와 `P=>(ABC=>X)`에서 바깥 입력은 그대로다.

함수를 소비하는 바깥 함수에는 입력 Contravariance를 적용한다.

~~~text
F <: G    Int <: Int
-----------------------
(G=>Int) <: (F=>Int)
~~~

`G=>Int`인 소비자는 전달받은 함수에 `ABC`를 주고 결과의 `x`를 읽을 수 있다. `F`인 `foo`도 그 사용을 지원한다. 역방향의 `F=>Int` 소비자는 `AB`만 주거나 결과의 `y`까지 읽을 수 있으므로 임의의 `G`로 대체할 수 없다.

입력 안에 입력이 한 번 더 있으면 방금 얻은 관계에 규칙을 다시 적용한다.

~~~text
(G=>Int) <: (F=>Int)
따라서 ((F=>Int)=>Int) <: ((G=>Int)=>Int)
~~~

두 번의 입력 위치를 지나면서 방향이 두 번 뒤집혔다. 입력과 출력에 동시에 함수 타입이 있어도 전제를 분리한다.

~~~text
(G=>Int) <: (F=>Int)    F <: G
---------------------------------------
((F=>Int)=>F) <: ((G=>Int)=>G)
~~~

오른쪽을 믿는 사용자는 `G=>Int`를 주고 `G`를 기대한다. 왼쪽 실제 함수는 공급된 소비자를 `F=>Int`처럼 사용할 수 있고 자신이 만든 `F`를 `G`로 제공할 수 있다. 중첩된 화살표마다 이 공급·사용을 확인하면 방향을 추측할 필요가 없다.

Top·Bottom도 같은 방식으로 결합한다.

~~~text
P <: Any, Nothing <: R
따라서 (Any=>Nothing) <: (P=>R)

Nothing <: P, R <: Any
따라서 (P=>R) <: (Nothing=>Any)
~~~

이는 타입 관계의 유도다. `Any=>Nothing`인 함수가 모든 입력에서 정상 결과 값을 만든다는 존재 증명도, `Nothing=>Any`에 공급할 정상 입력을 얻었다는 주장도 아니다.

이렇게 함수 타입을 읽기 멤버 안에 넣고 다시 함수의 입력·결과로 사용하는 중첩 추론은 2025 중간 Q1의 부분 첨부에서도 연결된다. 확인되는 것은 구조적 Alias와 함수 타입 선언이며, 원래 질문 지시문 전체는 없다. 별도로 실린 제공 답을 이 유도의 정답으로 채택하지 않고, 클래스 상속·Overriding의 직접 증거로도 사용하지 않는다. [EX:pop_2025_mid_q01_partial L.26-46]

## 확인·연습문제

### 공통 구조와 사용 가능성

#### 확인 Q01 · greeting의 정확한 요구

`tom`은 `name:String,home:String`, `bob`은 `name:String,mobile:String`을 갖는다. `greeting(r)="Hi "+r.name+", How are you?"`에 적절한 공통 입력 타입을 쓰라. `name:Int`인 값이나 임의 `A`도 같은 근거로 받을 수 있는가? `object`와 Type Alias의 역할도 구분하라.

<details><summary>해설 보기</summary>

`type Name={val name:String}`으로 충분하다. `NameHome <: Name`, `NameMobile <: Name`이어서 한 함수가 두 구조의 값을 받는다. `name`이라는 철자만 같고 타입이 `Int`이면 String 요구를 만족하지 않는다. 임의 `A`도 그 멤버를 보장하지 않는다. `Name`은 구조의 별칭, `tom,bob`은 값 이름, `object`는 이 예에서 멤버를 가진 한 값에 이름을 주는 선언이다. 새 명목 클래스를 도입한 것이 아니다. 식을 전개하면 Tom에는 `"Hi Tom, How are you?"`, Bob에는 `"Hi Bob, How are you?"`다. `r:Name`만으로 `r.home`을 읽지는 못한다.

**확인 기준**

- 필드 이름과 `String` 타입 조건을 모두 썼는가?
- 공통 요구를 통해 두 타입의 입력을 쓰는 다형성과 값·별칭·멤버를 구분했는가?

</details>

#### 확인 Q02 · T <: S의 방향

`T <: S`를 허용된 Elimination으로 설명하라. `NameHome`을 `Name`처럼 쓸 수 있는지 확인하고, `S=>R` 함수를 `T=>R` 자리에 쓸 수 있는 방향을 유도하라. 두 타입을 문자 그대로 같은 집합·메모리 표현으로 가정해야 하는가?

<details><summary>해설 보기</summary>

왼쪽 `T`의 값을 오른쪽 `S`를 요구하는 자리에 공급할 수 있다는 관계다. `Name`의 소비자가 허용받은 사용은 `.name`에서 String을 얻는 것이고 `NameHome`이 이를 제공한다. 같은 집합이나 메모리 표현이라는 가정은 필요하지 않다. `S=>R` 함수가 `S`의 허용된 연산을 사용한다면 `T <: S`인 입력에도 그 연산을 쓸 수 있으므로 `(S=>R) <: (T=>R)`이다. 값 이름 자체가 서로의 Subtype이라는 말도 아니며 이 정적 관계만으로 성능·업무 계약 전체가 같아지지 않는다.

**확인 기준**

- 값을 공급하는 방향과 허용 사용을 명시했는가?
- 함수 입력 방향이 뒤집히는 이유를 소비자의 사용으로 설명했는가?

</details>

#### 확인 Q03 · 구현 모형과 규칙

필드 이름을 찾아 읽는 Table Lookup 모형과, 각 타입을 선언 순서대로 저장하고 `.name`을 첫 칸에서 읽는 Fixed Offset 모형을 비교하라. `{val home:String;val name:String}`이 후자의 어떤 가정을 깨는가? 검색이 반드시 필요하다는 결론도 얻는가?

<details><summary>해설 보기</summary>

이름을 찾는 표 모형은 필드 추가·순서 변화에도 `name`을 찾는 사용을 설명하지만 이름 저장과 검색 작업이 들 수 있다. 선언 순서 배치 모형에서는 제시한 구조의 첫 칸이 `home`이다. 이 구조는 Permutation·Width로 `Name`을 충족하는데 첫 칸 읽기는 잘못된 필드를 고르므로 단순 가정이 불충분하다. 이것은 다른 배치나 컴파일 방법을 배제한 증명이 아니다. 따라서 항상 런타임 검색을 한다거나 특정 포인터 폭·비용·코드 생성 횟수를 갖는다는 결론은 없다. 강의의 구현 제안과 유보를 모형으로 읽어야 한다.

**확인 기준**

- 반례가 허용된 Subtype인데 첫 칸 가정에는 맞지 않는 이유를 설명했는가?
- 모형의 결함을 실제 컴파일러의 필수 구현·성능 주장으로 확대하지 않았는가?

</details>

#### 확인 Q04 · Structural과 Nominal

멤버 모양이 같은 두 구조적 Alias와, 별도로 선언한 두 클래스에 대해 같은 Subtype 결론을 자동 적용해도 되는가? Duck Typing이라는 명칭만으로 런타임 검사를 뜻하는가?

<details><summary>해설 보기</summary>

구조적 Alias는 풀어 쓴 멤버 이름·타입을 기준으로 비교한다. 클래스는 타입 이름과 선언한 관계도 기준이므로 모양이 같다는 이유만으로 별개 클래스가 부모·자식이 되지 않는다. `extends` 같은 선언과 그 허용 조건이 필요하다. Duck Typing이라는 별칭만으로 검사가 런타임에만 일어난다는 결론도 없다. 자료의 Ad hoc Polymorphism은 그 자료가 Nominal 관계에 붙인 명칭으로 한정한다.

**확인 기준**

- 별칭과 명목 타입을 구분했는가?
- 명칭에서 검사 시점이나 모든 언어의 분류를 추정하지 않았는가?

</details>

#### 확인 Q05 · 반사성과 추이성

`T <: R`, `R <: S`에서 얻는 결론과 `T <: T`의 근거를 쓰라. 이것만으로 `S <: T`도 얻는가? `NameHome`과 `Name`으로 반례를 설명하라.

<details><summary>해설 보기</summary>

추이성으로 `T <: S`를 얻고 반사성으로 각 타입은 자기 자신의 Subtype이다. 역방향은 주어지지 않는다. `NameHome`의 값은 `name`만 읽는 곳에 쓰지만 `name`만 있는 `Name` 값은 `home`을 요구하는 사용을 제공하지 못한다. 반사성이 부족한 필드를 추가해 주는 규칙은 아니다.

**확인 기준**

- 전제와 결론의 방향을 유지했는가?
- 관계의 대칭성을 가정하지 않고 역방향 실패의 사용을 제시했는가?

</details>

### 읽기 필드와 위치의 규칙

#### 확인 Q06 · Any와 Nothing

`Nothing <: T <: Any`를 생성·사용 관점에서 설명하라. `def f(a:Nothing):Int=a`와 `val b:Any=3`에서 허용되는 것과 얻지 못하는 것은 무엇인가?

<details><summary>해설 보기</summary>

`Nothing`에는 정상 값을 만드는 Introduction이 없으므로 그 모든 값을 `T`처럼 사용하다 실패하는 실제 정상 값 반례도 없다. `Nothing <: Int`이어서 가정한 `a`를 결과 Int 자리에 쓸 수 있으나 호출에 공급할 정상 `Nothing` 값을 얻은 것은 아니다. 예외·발산 식도 정상 값을 반환한다는 뜻은 아니다. `Int <: Any`이므로 3을 Any로 받을 수 있다. 그러나 Any에는 다른 값도 가능하므로 그 정적 정보만으로 정수 전용 연산이나 `.name`을 요구하지 못한다. 모든 공통 연산이 없다는 뜻은 아니며 빈 case 비유도 특정 문법의 컴파일 증명은 아니다.

**확인 기준**

- 정상 값의 부재와 가정한 입력의 사용을 구분했는가?
- Any로 받아들이는 것과 특정 구조 정보를 아는 것을 구분했는가?

</details>

#### 확인 Q07 · 중첩 Record의 세 규칙

읽기 전용 타입 `A={val x:{val y:Int;val z:String};val w:Int}`, `B={val w:Int;val x:{val y:Int;val z:String}}`, `C={val w:Int;val x:{val z:String}}`다. `A <: C`를 유도하고 역방향 실패를 설명하라. 같은 Depth를 `var x`에 자동 적용하면 왜 위험한가?

<details><summary>해설 보기</summary>

`A <: B`는 바깥 필드의 이름·타입을 유지한 Permutation이다. 안쪽 `{val y:Int;val z:String} <: {val z:String}`는 Width다. 이를 바깥 `x`의 Depth로 올려 `B <: C`, 추이성으로 `A <: C`다. C의 소비자는 `w`와 `x.z`를 읽고 A가 모두 제공한다. C만으로는 `x.y`를 보장하지 못해 역방향은 일반적으로 안 된다. 정적 관점을 줄일 뿐 실제 데이터를 지우지 않는다. `var x:NameHome`을 `var x:Name`처럼 쓰게 하면 넓은 관점에서 name만 있는 값을 저장할 수 있어 원래 사용자의 `x.home` 보장이 깨진다. 읽기와 쓰기 조건은 따로 검토한다.

**확인 기준**

- 안쪽 Width와 바깥 Depth의 층위를 구분했는가?
- Permutation·Transitivity, 역방향의 누락 필드, 쓰기 반례를 모두 설명했는가?

</details>

#### 확인 Q08 · Tuple의 같은 Arity

`Int <: Any`일 때 `(Int,String,Int) <: (Any,String,Any)`를 단계별로 보이라. `(Int,String)`로 성분 수를 줄이거나 `(String,Int)`로 위치를 바꿔도 Record 규칙처럼 허용되는가?

<details><summary>해설 보기</summary>

위치별 Depth로 `(Int,String,Int) <: (Any,String,Int) <: (Any,String,Any)`다. 모든 단계에서 세 위치와 가운데 String이 유지된다. 이 자료의 규칙은 같은 Arity를 요구하므로 성분 삭제의 Width는 나오지 않는다. 두 성분의 `(Int,String)`을 `(String,Int)`로 쓰면 첫 성분을 String으로 읽는 사용자에게 Int를 준다. Record는 이름으로 읽으므로 나열 순서를 바꾸지만 Tuple은 위치가 의미를 갖는다. `(t._1,t._2)`로 새 값을 만드는 계산도 기존 값의 Subtyping과 다르다.

**확인 기준**

- 같은 개수·위치 조건과 두 Depth 단계를 썼는가?
- 성분 삭제·위치 교환·새 Tuple 구성과 관계 유도를 구분했는가?

</details>

### 함수와 중첩된 대체 방향

#### 확인 Q09 · 입력과 출력의 반대 방향

`T <: T'`, `S <: S'`일 때 어떤 함수 관계가 성립하는가? 사용자가 공급하는 값과 기대하는 결과로 설명하고, `Name` 대 `NameHome` 입력과 `X={val x:Int}` 대 `XY={val x:Int;val y:Int}` 출력으로 잘못된 방향의 반례를 쓰라.

<details><summary>해설 보기</summary>

`(T'=>S) <: (T=>S')`다. 오른쪽을 믿는 사용자는 T를 공급한다. 실제 함수는 그 값을 받을 수 있는 더 넓은 T'만 요구하고, 실제 출력 S는 약속 S'처럼 쓸 수 있다. 입력은 Contravariance, 출력은 Covariance다. Name만 공급하기로 한 자리에 NameHome의 `home`까지 읽는 함수를 넣으면 입력이 부족하다. 반대로 Name만 읽는 함수는 NameHome을 받을 수 있다. XY를 주는 함수는 X만 기대하는 곳에 쓰지만 X만 주는 함수는 XY를 기대하며 `.y`를 읽는 곳에 쓰지 못한다. 입력의 사용과 결과의 생성을 나누어 따진다.

**확인 기준**

- 함수 관계와 두 전제를 정확히 대응시켰는가?
- 입력·출력 각각의 허용 방향과 실패 사용을 제시했는가?

</details>

#### 확인 Q10 · AB에서 XY를 만드는 함수

`AB={val a:Int;val b:Int}`, `ABC={val a:Int;val b:Int;val c:Int}`, `XY={val x:Int;val y:Int}`, `X={val x:Int}`다. `foo:AB=>XY`는 새 객체에 `x=s.b,y=s.a`를 넣는다. `gee:ABC=>X=foo _`의 근거와 입력 `a=2,b=9,c=100`의 결과를 쓰고 역방향 실패를 설명하라.

<details><summary>해설 보기</summary>

Width로 `ABC <: AB`, `XY <: X`다. 일반 규칙에 `T=ABC,T'=AB,S=XY,S'=X`를 넣어 `(AB=>XY) <: (ABC=>X)`다. foo의 결과는 `x=9,y=2`이고 gee의 공개된 관점에서 읽는 `x`는 9다. c는 필요하지 않고 y는 공개된 결과 요구에 없지만 물리적으로 삭제한 것은 아니다. `a,b`를 읽어 다른 이름의 `x,y`를 새로 구성하므로 단순 Permutation도 아니다. 역방향 함수는 c를 요구할 수 있고 y를 반환하지 않을 수 있어 AB 입력·XY 결과 약속에 맞지 않는다.

**확인 기준**

- 두 Width 전제와 함수 규칙의 대입을 썼는가?
- 결과의 x가 입력 b에서 오는 계산과 역방향의 두 실패를 확인했는가?

</details>

#### 확인 Q11 · 함수를 반환하거나 소비할 때

Q10의 `F=AB=>XY`, `G=ABC=>X`라 두어 `F <: G`다. 다음 네 관계의 방향을 유도하라: (가) `P=>F`와 `P=>G`, (나) `G=>Int`와 `F=>Int`, (다) `(F=>Int)=>Int`와 `(G=>Int)=>Int`, (라) `(F=>Int)=>F`와 `(G=>Int)=>G`. (나)의 역방향이 왜 일반적으로 안 되는가?

<details><summary>해설 보기</summary>

(가) 출력 공변성으로 `(P=>F) <: (P=>G)`다. 같은 P를 주고 G를 기대해도 F를 G처럼 쓴다.

(나) 입력 반공변성으로 `(G=>Int) <: (F=>Int)`다. G 소비자는 ABC를 공급하고 X의 x를 읽을 수 있으며 F도 그 사용을 제공한다. 반대의 F 소비자는 AB만 공급하거나 XY의 y까지 읽을 수 있으므로 임의 G에 안전하지 않다.

(다) 방금 `G=>Int <: F=>Int`를 다시 바깥 입력에 넣어 `((F=>Int)=>Int) <: ((G=>Int)=>Int)`다. 입력을 두 번 지나 방향이 두 번 뒤집힌다.

(라) 입력 전제 `G=>Int <: F=>Int`와 출력 전제 `F <: G`를 함께 사용해 `((F=>Int)=>F) <: ((G=>Int)=>G)`다. 오른쪽 사용자가 주는 G 소비자를 왼쪽은 F 소비자로 쓸 수 있고, 왼쪽이 반환한 F도 G 약속을 충족한다.

**확인 기준**

- 바깥 입력·출력을 매번 분리하여 네 방향을 도출했는가?
- 괄호를 유지하고 소비자의 공급·결과 접근으로 반례를 설명했는가?

</details>

#### 확인 Q12 · Top·Bottom과 함수 관계

임의 타입 `P,R`에 대해 `Any=>Nothing`, `P=>R`, `Nothing=>Any`의 관계를 전제와 함께 쓰라. 첫 함수가 모든 입력에서 정상 값을 반환한다고 결론 내릴 수 있는가?

<details><summary>해설 보기</summary>

`P <: Any`와 `Nothing <: R`로 `(Any=>Nothing) <: (P=>R)`다. 이어 `Nothing <: P`와 `R <: Any`로 `(P=>R) <: (Nothing=>Any)`다. 함수 입력은 역방향, 결과는 정방향으로 적용했다. 이는 정적 타입 관계이며, Any를 받아 정상 Nothing 값을 만든다는 존재·종료 증명이 아니다. 마지막 타입에 공급할 정상 Nothing 입력을 구성한 것도 아니다.

**확인 기준**

- 네 Top·Bottom 전제를 올바른 입력·출력 위치에 썼는가?
- 정적 관계와 정상 실행·값의 존재를 구분했는가?

</details>

### 규칙을 결합하는 연습

#### 연습 P01 · 안쪽 필드와 Tuple의 차이

새로 쓴 강의 기반 일반 연습이다. 이 비교를 직접 묻는 별도 기출 형식 근거는 없다. `R={val item:{val name:String;val home:String};val tag:Int}`, `S={val tag:Any;val item:{val name:String}}`라 두자. `R <: S`를 유도하고 역방향 실패를 보이라. `(Int,String,Int) <: (Any,String)`도 같은 논법으로 얻는다는 주장에는 어떻게 답할 것인가?

<details><summary>해설 보기</summary>

안쪽 record는 home을 요구에서 빼는 Width로 name만 요구하는 구조의 Subtype이다. 이를 item의 Depth에 적용하고 `Int <: Any`를 tag의 Depth에 적용한다. 바깥 나열 순서는 Permutation으로 맞추어 `R <: S`를 얻는다. 역방향은 item.home을 보장하지 못하고 tag:Any를 Int로 쓸 근거도 없다. Tuple 주장은 성분 수가 달라 제시된 같은 Arity 규칙의 전제를 만족하지 않는다. Record의 이름 기반 Width를 위치 기반 Tuple로 옮길 수 없다.

**확인 기준**

- item과 tag 각각의 Depth 전제를 밝혔는가?
- 역방향의 두 부족한 사용과 Tuple 개수 조건을 확인했는가?

</details>

#### 연습 P02 · 읽기 멤버 안의 함수와 바깥 함수

새로 쓴 합성 연습이다. 부분 첨부인 2025 중간 Q1에서 멤버 안의 함수 타입에 규칙을 반복 적용하는 추론만 연결한다 [EX:pop_2025_mid_q01_partial L.26-46]. 원 질문 전체와 별도의 미검증 제공 답은 사용하지 않는다. 선수는 Q07·Q09–Q11이다. Q10의 `F <: G`에 대해 `BF={val run:F}`, `BG={val run:G}`라 두자. `(BG=>F) <: (BF=>G)`를 증명하고 역방향이 일반적으로 실패하는 사용을 제시하라.

<details><summary>해설 보기</summary>

읽기 필드의 Depth로 `BF <: BG`다. 따라서 오른쪽 사용자가 주는 BF를 실제 왼쪽 함수는 BG처럼 받아들인다. 결과도 `F <: G`이므로 약속된 G로 사용할 수 있다. 두 전제로 `(BG=>F) <: (BF=>G)`다.

역방향에서는 실제 `BF=>G` 함수가 입력의 run을 F로 사용하며 AB만 줄 수 있는데, BG가 담은 임의 G는 c까지 요구할 수 있다. 결과도 G만 반환하면 F를 기대한 사용자의 XY 결과, 특히 y를 보장하지 못한다. 바깥 관계를 먼저 외우지 말고, 읽기 멤버·내부 화살표·바깥 화살표마다 조건을 따진다. 이 문제는 별도 새 타입을 결합한 것으로 원 첨부나 제공 CommonTy 답의 전재가 아니다.

**확인 기준**

- 읽기 멤버 Depth 뒤 입력 반공변·출력 공변을 적용했는가?
- 역방향에서 입력의 부족한 c와 출력의 부족한 y를 설명했는가?

</details>

## 출처

[프로그래밍의 원리 Part2 · PDF pp.3–14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf) · 원본 쪽 보기: [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-003) · [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-004) · [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-005) · [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-006) · [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-007) · [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-009) · [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-010) · [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-011) · [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-012) · [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-013) · [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-014)

[프로그래밍의 원리 Part1 · 자료형 선수 참고 pp.68–72, 100](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

[[courses/principles_of_programming/lectures/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 · Structural Subtyping · 강의 정리]]

[[courses/principles_of_programming/transcripts/undated-structural-subtyping-6p3wjj22vvvjv0ji|날짜 미확인 전사 · 07:00·16:45·20:00·28:13·30:07·36:23·45:36·48:24·57:15·01:01:26·01:04:12·01:06:53·01:11:03·01:17:32]]

정확한 타입 규칙과 코드 식은 자료에 근거한다. 전사의 방향·부정·변수 이름이 불명확한 곳과 보이지 않는 실시간 코드·그림·출력은 확정하지 않는다. Table Lookup·Fixed Offset은 논의를 위한 모형이며 실제 구현·비용 측정값이 아니다. 강의 정리는 2차 설명이고 날짜·음성 대조·실제 컴파일 및 실행 결과는 확인되지 않았다.

2025 중간 Q1은 구조적 Alias와 중첩 함수 타입의 부분 첨부만 연결된다 [EX:pop_2025_mid_q01_partial L.26-46]. 원 질문 지시문 전체가 없으며 별도로 제시된 CommonTy는 독립 검증되지 않은 제공 답이다. 이 단원의 해법으로 채택하지 않고 상속·Overriding의 직접 근거로도 사용하지 않는다. 당시 정책이나 현재 출제 가능성을 확정하는 자료는 아니다.


---

[[courses/principles_of_programming/units/datatype-prerequisites|← 이전: 자료로 확인하는 선수 개념: 자료형의 생성·사용과 Polymorphism]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/class-construction|다음: Class와 생성 통제: 명목 타입·불변조건·계약 →]]
