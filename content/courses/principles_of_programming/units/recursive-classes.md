---
title: "재귀 클래스, Option과 Companion Object"
description: "Option으로 빈 경우를 표현하고 리스트·트리 생성식과 재귀 계산을 추적한다."
course: "principles_of_programming"
unit_id: "recursive-classes"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["lecture-part2.pdf", "lecture-part1.pdf"]
private_source_assets: []
source_lectures: ["courses/principles_of_programming/lectures/undated-classes-inheritance-jk9b2ob0objzgyvy"]
---

## Recursive Class의 노드와 빈 리스트

리스트의 길이가 달라질 때마다 별도의 필드 구조를 선언할 수는 없다. [Product와 Sum](datatype-prerequisites.md)을 이용하면 한 노드의 정보와 나머지 구조를 나누어 표현할 수 있다. Recursive Class(재귀 클래스)는 필드의 타입 안에서 지금 정의하는 클래스 이름을 다시 사용한다. 프로그래밍의 원리 Part2(NM001) p.20의 예는 값 하나와 선택적인 다음 노드를 함께 둔다. [Part2 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-020)

~~~text
class MyList[A](v: A, nxt: Option[MyList[A]]) {
  val value: A = v
  val next: Option[MyList[A]] = nxt
}

type YourList[A] = Option[MyList[A]]

val t: YourList[Int] =
  Some(new MyList(3,Some(new MyList(4,None))))
val s: YourList[Int] = None
~~~

`A`는 타입 매개변수다. `MyList[Int]`와 `MyList[String]`은 같은 노드 구조에 다른 성분 타입을 넣는다. 여기의 `MyList[A]`는 값이 있는 노드이며, 앞서 Part1에서 본 `MyNil/MyCons` ADT와는 별개의 동명 정의다.

노드는 `value:A`와 `next:Option[MyList[A]]`를 함께 가지므로 Product다. `next`는 `None` 또는 `Some(다음 노드)`라는 Sum이고, 그 안에 같은 `MyList[A]`가 다시 나타나므로 재귀적이다. `MyList[A]` 노드 자체에는 “첫 노드도 없음”이라는 경우가 없다. 그래서 전체 빈 리스트까지 나타내려면 `YourList[A]=Option[MyList[A]]`로 한 번 더 감싼다.

### 두 원소와 두 위치의 None

자료의 `t`를 바깥에서 안쪽으로 읽으면 다음과 같다.

| 위치 | 값 | 의미 |
| --- | --- | --- |
| 전체 리스트 | `Some(...)` | 첫 노드가 있음 |
| 첫 노드 | `value=3` | 첫 원소는 3 |
| 첫 노드의 `next` | `Some(...)` | 둘째 노드가 있음 |
| 둘째 노드 | `value=4` | 둘째 원소는 4 |
| 둘째 노드의 `next` | `None` | 뒤 노드가 없음 |

따라서 `t`에는 노드가 2개다. 반면 `s=None`은 첫 노드부터 없는 빈 리스트로 노드가 0개다. 바깥 `None`과 마지막 `next=None`은 같은 부재 생성자를 다른 위치에 쓴 것이다. `value`와 `next`는 서로 다른 멤버이며 `value.next`라는 한 접근 경로가 아니다. 강의가 “None으로 하면 베이스 케이스가 생기잖아요”고 하는 이유도 노드가 없는 경우에서 유한한 구성을 시작할 수 있기 때문이다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 30:16·32:02]]

타입 이름이 다시 등장하는 것과 실제 값에 포인터 순환이 있는 것은 다르다. 위 식은 유한하게 중첩한 값이다. 재귀 타입 선언만으로 모든 값과 처리 함수의 종료가 보장되는 것도 아니다. 유한한 값을 따라 더 작은 `next`로 진행하고 기저 경우를 처리한다는 조건이 별도로 필요하다. 이 예는 클래스 이름을 통한 자기 참조를 보여 주며, 모든 Structural Type 체계에서 재귀가 불가능하다는 정리를 주지는 않는다.

## Option으로 드러내는 멤버 접근의 조건

만약 `next`의 `Option`을 없애고 반드시 `MyList[A]`인 다음 노드를 받게 한다면, 정상 노드를 만들 때마다 또 다른 노드가 필요하다. 이 방식만으로는 유한 리스트의 끝을 표시할 수 없으므로 별도 기저 표현이 필요하다. 강의는 `null`로 끝을 표시하는 관례와 `Option`으로 부재를 명시하는 방식을 비교한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 34:56·35:53]]

`null`은 실제 노드의 필드 정보를 제공하지 않는다. 그 참조를 통해 노드의 멤버를 읽으면 정상 값을 얻지 못하고 예외가 발생할 수 있다. 따라서 현재 참조가 노드인지 확인한 뒤 사용해야 한다. 첫 노드가 `null`이 아니더라도 `next`는 끝 표시일 수 있으므로 이후의 각 역참조에도 필요한 검사를 반복한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 38:34·40:16]]

`s:Option[MyList[A]]`에서는 이 분기 필요성이 타입에 드러난다. 전체 `s`는 노드 자체가 아니므로 곧바로 `s.value`를 요구하지 않는다. 다음은 자료의 Option과 Pattern Matching을 결합한 설명용 예다.

~~~text
def firstValue[A](s: Option[MyList[A]]): Option[A] =
  s match {
    case None => None
    case Some(node) => Some(node.value)
  }
~~~

`None`에서는 읽을 노드가 없다. `Some(node)`에서는 내부의 `node:MyList[A]`를 얻으므로 그 `value`를 사용한다. 그러나 `node.next`는 다시 `Option[MyList[A]]`다. 둘째 원소를 읽으려면 그 값이 `Some`인지도 확인해야 한다. 현재 노드의 존재와 다음 노드의 존재는 다른 정보다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 43:16]]

이 예는 `Some` 안에 정상 노드가 있다는 전제를 둔다. `Option`만으로 잘못된 내부 값·강제 추출·별도로 허용된 `null`까지 모두 막지는 않는다. p.21의 `null` 설명은 공급된 언어 모델의 설명이다. 이를 모든 Scala 설정의 영구 규칙으로 확대하거나, Java에는 Option·Sum을 표현할 수단이 전혀 없다고 결론 내리면 안 된다. `null` 역참조 위험만으로 언어의 모든 Type Safety를 부정할 수도 없고, 자료의 효율성 표현이 일반적인 성능 측정값인 것도 아니다. [Part2 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-021)

## Argument Members와 생성자 입력

[Class의 생성 경로](class-construction.md)에서 받은 입력과 생성 후 읽는 멤버를 구분했다. 긴 `MyList`는 Constructor Parameter(생성자 매개변수) `v,nxt`를 받고 `val value=v`, `val next=nxt`로 멤버를 따로 정의한다. p.22의 Argument Members(인자 멤버)는 이 두 역할을 합친 표기다. [Part2 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-022)

~~~text
class MyList[A](val value: A, val next: Option[MyList[A]]) {
}
~~~

이것은 앞의 긴 클래스 정의를 대체하는 형태다. `val value:A`는 입력을 받으면서 같은 이름의 읽기 멤버도 선언한다. `val next`도 같다. 본문에 추가할 내용이 없으면 다음처럼 빈 중괄호도 생략한다.

~~~text
class MyList[A](val value: A, val next: Option[MyList[A]])
~~~

두 형태 모두 값과 선택적인 다음 노드라는 정보를 같은 타입으로 저장한다. 클래스 본문에 추가 멤버를 정의할 수도 있다. 여기서 직접 확인하는 축약은 `val`이다. 단순히 생성자 괄호 안에 이름이 있다고 모든 매개변수가 외부에서 읽는 공개 필드가 되는 것은 아니다. 뒤 상속 예제의 `x:Int`와 이 `val value:A`를 구분해야 한다. `next`에 받은 값을 저장하는 것은 그 값이 가리키는 재귀 구조 전체를 Deep Copy한다는 뜻도 아니다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 44:52·45:39]]

## Companion Object의 apply가 만드는 값

생성식이 길면 관련 생성 함수를 객체에 모아 편리한 호출 표기를 만들 수 있다. p.23은 클래스와 같은 이름의 `object MyList`에 `apply`를 둔다. 이런 객체를 Companion Object(동반 객체)라고 한다. [Part2 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-023)

~~~text
class MyList[A](val value: A, val next: Option[MyList[A]])

object MyList {
  def apply[A](v: A, nxt: Option[MyList[A]]) =
    new MyList(v,nxt)
}

type YourList[A] = Option[MyList[A]]

object YourList {
  def apply[A](v: A, nxt: Option[MyList[A]]) =
    Some(new MyList(v,nxt))
}
~~~

타입 자리의 `MyList[A]`는 클래스 타입 이름이고, 값 자리에서 `apply`를 사용하는 `MyList`는 객체다. 같은 이름이라는 이유만으로 Companion Object 자체가 리스트 노드 인스턴스가 되는 것은 아니다. `YourList[A]`라는 타입 Alias와 값 자리의 `object YourList`도 구분한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 47:29·50:27]]

`MyList(4,None)`은 이 예에서 `MyList.apply(4,None)`를 호출하고 본문에 따라 `new MyList(4,None)`을 만든다. 반면 `YourList(4,None)`은 `Some(new MyList(4,None))`을 만든다. 하나는 노드이고 다른 하나는 그 노드를 담은 Option이다. “new만 생략했다”는 설명으로는 이 차이를 나타낼 수 없다. 어떤 값을 만드는지는 실제 `apply` 본문으로 결정된다. 이 예의 `apply`는 여전히 생성자를 실행한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 51:20]]

### t0와 t1·t2의 다른 구조

자료의 세 식은 다음과 같다. 가장 바깥의 `None`을 먼저 구분하자.

~~~text
val t0 = None
val t1 = Some(new MyList(3,Some(MyList(4,None))))
val t2 = YourList(3,(YourList(4,None)))
~~~

`t0`는 노드가 없는 빈 리스트다. `t1`과 `t2`만 3 다음에 4가 오는 두 원소 구조다. 각 `apply` 본문을 대입하면 이 관계가 드러난다.

~~~text
t1:
Some(new MyList(3,Some(MyList(4,None))))
→ Some(new MyList(3,Some(new MyList(4,None))))

t2:
YourList(3,YourList(4,None))
→ YourList(3,Some(new MyList(4,None)))
→ Some(new MyList(3,Some(new MyList(4,None))))
~~~

두 식이 같은 노드 구조를 나타낸다는 설명은 별도로 생성한 객체의 참조 동일성이나 자동 구조적 동등성까지 주장하는 것이 아니다. `t0`를 이 두 원소 값과 묶어 같다고 해서는 안 된다. 또한 모든 `apply`가 새 객체를 만들거나 같은 방식으로 Option을 감싼다는 규칙도 없다. 수동으로 정의한 이 Companion Object의 본문을 읽어 얻은 결과다.

## Binary Tree의 세 성분과 빈 가지

Binary Tree(이진트리)의 노드는 값과 왼쪽·오른쪽 자식을 함께 갖는다. p.24는 다음 구성으로 표현한다. 곱의 각 자식 성분 안에 다시 Option의 합이 있다. [Part2 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-024)

~~~text
MyTree[A] =
  (value: A) *
  (left: Option[MyTree[A]]) *
  (right: Option[MyTree[A]])
~~~

이 구조는 Part1의 `BTree=Leaf | Node of Int * BTree * BTree`와 연결된다. 그 ADT의 `Leaf`는 빈 경우이고 `Node`는 값과 두 하위 트리를 담는다. Option 기반 표현에서는 `None`이 빈 경우, `Some(node)`가 값 있는 노드에 대응한다. 이 연결은 자료형 기초를 이용한 설명이며, 실제 강의 중 보이지 않는 그림의 배치를 재구성한 것은 아니다.

p.25의 긴 정의는 입력과 멤버를 따로 둔다. [Part2 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-025)

~~~text
class MyTree[A](v: A,
                lt: Option[MyTree[A]],
                rt: Option[MyTree[A]]) {
  val value = v
  val left = lt
  val right = rt
}
type YourTree[A] = Option[MyTree[A]]

val t0: YourTree[Int] = None
val t1: YourTree[Int] = Some(new MyTree(3,None,None))
val t2: YourTree[Int] =
  Some(new MyTree(3,Some(new MyTree(4,None,None)),None))
~~~

여기의 `t0,t1,t2`는 앞의 리스트와 별개의 트리 값이다. `t0`는 빈 트리다. `t1`은 값 3이고 두 자식이 없는 한 노드다. `t2`는 루트 3의 왼쪽에 값 4가 있고 오른쪽은 비어 있다. 값 4의 두 자식도 없다. 따라서 트리의 `t1`과 `t2`는 서로 다른 구조다.

각 자식의 Option은 그 방향의 빈 가지를 나타내고, 바깥 `YourTree`의 Option은 루트조차 없는 전체 빈 트리를 나타낸다. 노드를 표현하는 Product만으로는 이런 부재 대안이 드러나지 않는다. 강의가 기저 경우를 강조하는 이유다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 54:25·58:33]]

### 긴 생성식과 짧은 생성식의 대응

p.26에서는 Argument Members와 `YourTree.apply`로 같은 정보를 줄여 쓴다. 다음은 긴 정의를 대체한다. [Part2 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-026)

~~~text
class MyTree[A](val value: A,
                val left: Option[MyTree[A]],
                val right: Option[MyTree[A]])

type YourTree[A] = Option[MyTree[A]]

object YourTree {
  def apply[A](v: A, lt: Option[MyTree[A]], rt: Option[MyTree[A]]) =
    Some(new MyTree(v,lt,rt))
}

val t0: YourTree[Int] = None
val t1: YourTree[Int] = YourTree(3,None,None)
val t2: YourTree[Int] = YourTree(3,YourTree(4,None,None),None)
~~~

안쪽 `YourTree(4,None,None)`은 `Some(new MyTree(4,None,None))`이다. 이 값을 바깥의 왼쪽 인자로 넣고 `apply`를 전개하면 다음과 같다.

~~~text
Some(new MyTree(3,Some(new MyTree(4,None,None)),None))
~~~

짧아졌어도 빈 트리, 한 노드, 왼쪽 자식이 있는 두 노드의 구분은 유지된다. 노드 필드의 곱·자기 참조와 Option의 합을 조합한 것이다. 한 클래스의 필드 나열이 선택 대안을 직접 나열하지 않는다고 해서 클래스·상속으로 Sum을 인코딩할 수 없다는 결론은 나오지 않는다. 그 후속 표현과 enum 등은 여기의 필수 범위를 넘어선다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:00:20]]

### 구조를 따라 진행하는 재귀 계산

리스트에서는 빈 경우를 처리하고 다음 노드로 진행한다. 트리에서는 빈 가지를 처리하고 왼쪽·오른쪽을 각각 처리한다. 설명용으로 구조상의 노드 수를 세면 빈 경우는 0, 노드 경우는 “1 + 왼쪽 수 + 오른쪽 수”다. 위 `t2`에서는 값 4인 노드의 수가 `1+0+0=1`, 루트에서 `1+1+0=2`다.

이 계산은 유한하고 비순환적인 구조에서 실제 하위 구조로 진행하며 각 재귀 호출이 정상 반환한다는 조건 아래 설명한다. 정확한 `Int` 개수라면 구조상의 수가 `0..2147483647` 안에 있어야 한다. 같은 하위 노드를 여러 위치에서 공유하면 이 설명은 위치별로 세며, 서로 다른 객체의 수를 중복 없이 세는 알고리즘과 다르다. 유한한 구조라도 범위 초과나 자원 부족을 자동으로 피하지는 못한다.

빈 경우와 재귀 성분을 처리한 결과를 다시 결합한다는 사고는 역사적 리스트·트리 fold 문항과 연결된다. 여기서는 그 풀이 구조만 연결하며 fold 구현 전체, enum·variance 문법, 당시 시험 제한을 현재 단원에 추가하지 않는다. [EX:pop_2024_mid_q01_s01 L.46-57] [EX:pop_2024_mid_q01_s02 L.70-78]

## 확인·연습문제

### 노드와 빈 경우의 구분

#### 확인 Q01 · MyList와 YourList의 역할

`class MyList[A](v:A,nxt:Option[MyList[A]])`는 `value=v,next=nxt`를 둔다. `YourList[A]=Option[MyList[A]]`다. `None`과 `Some(new MyList(3,Some(new MyList(4,None))))`을 비교하고 곱·합·자기 참조·기저 경우를 찾으라.

<details><summary>해설 보기</summary>

None은 첫 노드조차 없는 전체 빈 리스트다. 다른 값의 바깥 Some은 첫 노드의 존재, 그 노드의 value는 3, next의 Some은 둘째 노드의 존재, 둘째 value는 4, 둘째 next=None은 끝을 뜻한다. 노드는 value와 next를 함께 갖는 Product이며 next는 None/Some의 Sum이고 그 안에 MyList[A]가 다시 나와 재귀적이다. 값 있는 MyList 노드와 빈 경우까지 포함한 YourList는 다르다. Part1의 MyNil/MyCons ADT와도 동명 별개 선언이다. None을 기저로 유한하게 구성할 수 있다는 사실이 모든 값의 비순환성이나 모든 처리 함수의 종료를 증명하지는 않는다.

**확인 기준**

- 바깥 None과 마지막 next=None의 서로 다른 위치·의미를 설명했는가?
- value와 next를 두 멤버로 구분하고 노드 수 0·2를 구조에서 확인했는가?

</details>

#### 확인 Q02 · 현재 노드와 다음 노드

`s:Option[MyList[A]]`에서 왜 바로 `s.value`를 읽지 않는가? `Some(node)`를 확인한 뒤 둘째 노드의 값을 읽으려면 무엇을 더 확인하는가? null로 끝을 표시하는 표현과 비교하라.

<details><summary>해설 보기</summary>

Option에는 노드가 없는 None이 있으므로 먼저 None/Some을 나눈다. Some(node)에서 정상 node:MyList[A]를 얻으면 value와 next를 읽지만, next도 Option이므로 다시 None/Some을 나누어야 둘째 노드의 value를 읽을 수 있다. 현재 노드가 있다는 사실과 다음 노드가 있다는 사실은 다르다. null 기저 표현에서는 첫 참조와 이후 각 next가 실제 노드인지 확인한 뒤 역참조해야 한다. 처음 한 번의 검사로 모든 다음 접근이 정당화되지는 않는다. Option은 분기 필요성을 타입에 드러내지만 잘못된 내부 값·강제 추출·별도의 null 허용까지 모두 막는 보장은 아니다. 이를 모든 Java·Scala 설정의 규칙이나 성능 우열로 확대하지 않는다.

**확인 기준**

- 두 번의 존재 조건과 null의 매 역참조 전제를 구분했는가?
- Option을 모든 오류를 막는 장치라고 단정하지 않았는가?

</details>

#### 확인 Q03 · 인자와 멤버, 저장과 복제

긴 선언 `class MyList[A](v:A,nxt:Option[MyList[A]]){val value:A=v;val next:Option[MyList[A]]=nxt}`를 Argument Members로 줄여 쓰라. 어떤 정보가 유지되는가? val 없는 생성자 이름도 전부 공개 필드인가? next 저장이 Deep Copy인가?

<details><summary>해설 보기</summary>

축약은 다음과 같다.

~~~text
class MyList[A](val value:A, val next:Option[MyList[A]])
~~~

입력 두 값을 같은 타입의 읽기 멤버 value와 next로 둔다는 정보는 유지된다. 긴 형태는 매개변수 v,nxt와 멤버를 별도 이름으로 두고, 짧은 형태는 val이 두 역할을 함께 선언한다. 본문이 비어 있어 중괄호를 생략한 것이며 필요하면 추가 멤버를 둘 수 있다. 단순 생성자 매개변수 이름이 있다는 이유로 모두 외부에서 읽는 공개 val 필드가 되지는 않는다. next에 받은 값을 저장한다는 것은 그 값이 가리키는 전체 재귀 구조를 깊게 복제한다는 뜻도 아니다.

**확인 기준**

- 두 필드의 정확한 타입과 val 표기를 유지했는가?
- 공개 멤버·생성자 입력·전체 구조 복제를 구분했는가?

</details>

### Companion과 생성식 전개

#### 확인 Q04 · MyList.apply와 YourList.apply

동명 object MyList의 apply는 `new MyList(v,nxt)`를, object YourList의 apply는 `Some(new MyList(v,nxt))`를 반환한다. `MyList(4,None)`과 `YourList(4,None)`을 풀어 쓰고, 타입 이름·object 값·노드를 구분하라.

<details><summary>해설 보기</summary>

`MyList(4,None)`은 `MyList.apply(4,None)`를 거쳐 노드 `new MyList(4,None)`을 만든다. `YourList(4,None)`은 `YourList.apply(4,None)`를 거쳐 `Some(new MyList(4,None))`이라는 Option을 만든다. 타입 자리 MyList[A]는 클래스 타입이며 값 자리 MyList는 apply를 가진 Companion Object다. 그 object 자체가 노드 인스턴스는 아니다. YourList 타입 Alias와 동명 object도 역할이 다르다. 따라서 ‘new만 생략’이라는 설명으로는 반환 구조 차이를 놓친다. 이 apply 본문은 실제로 생성자를 실행하지만 모든 apply가 새 객체를 만들거나 Option을 감싼다는 규칙은 아니다.

**확인 기준**

- 노드와 Some으로 감싼 노드의 타입·구조 차이를 설명했는가?
- 같은 이름의 타입·값·apply 본문을 구분했는가?

</details>

#### 확인 Q05 · 빈 t0와 두 원소 t1·t2

앞의 apply 정의에서 `t0=None`, `t1=Some(new MyList(3,Some(MyList(4,None))))`, `t2=YourList(3,YourList(4,None))`다. 세 값을 모두 같다고 할 수 있는가? t1,t2를 apply 본문으로 끝까지 전개하라.

<details><summary>해설 보기</summary>

t0는 빈 리스트이며 노드가 없다. t1은 안쪽 `MyList(4,None)`을 `new MyList(4,None)`로 바꾸어 `Some(new MyList(3,Some(new MyList(4,None))))`이다. t2는 안쪽부터 `YourList(4,None)=Some(new MyList(4,None))`, 이어 바깥 YourList를 전개하여 같은 모양의 식을 얻는다. 따라서 t1과 t2만 3 다음 4가 오는 두 노드 구조다. t0를 그 구조와 동일시하면 안 된다. 별도로 생성한 t1,t2의 같은 구조 설명은 참조 동일성이나 자동 구조적 동등성까지 주장하는 것이 아니다.

**확인 기준**

- t0=0개, t1·t2=2개를 구분했는가?
- 안쪽·바깥 apply를 모두 전개하고 구조와 객체 동일성을 구분했는가?

</details>

#### 확인 Q06 · 이진트리의 긴 식과 짧은 식

노드는 `value:A,left:Option[MyTree[A]],right:Option[MyTree[A]]`를 갖고 `YourTree[A]=Option[MyTree[A]]`다. `YourTree.apply(v,lt,rt)=Some(new MyTree(v,lt,rt))`일 때 `t0=None`, `t1=YourTree(3,None,None)`, `t2=YourTree(3,YourTree(4,None,None),None)`을 비교하고 t2의 긴 식을 쓰라.

<details><summary>해설 보기</summary>

t0는 루트가 없는 빈 트리다. t1은 값 3의 노드 하나이고 두 자식이 없다. t2는 루트 3의 왼쪽에 값 4의 노드가 있고 오른쪽은 비어 있다. t2를 전개하면 `Some(new MyTree(3,Some(new MyTree(4,None,None)),None))`이다. 한 노드의 세 성분은 Product, 각 자식 Option은 그 방향의 빈 가지/존재의 Sum이며 바깥 Option은 전체 빈 트리를 표현한다. Part1의 빈 Leaf와 값·두 자식의 Node라는 구분과 연결된다. 긴 생성자 입력 뒤 val로 저장하는 선언과 세 val 인자 멤버 선언도 같은 필드 정보를 유지한다. 이 노드 필드 나열이 직접 Sum 대안을 적지 않는다고 클래스·상속으로 Sum을 표현할 수 없다는 결론은 아니다.

**확인 기준**

- t0·t1·t2의 다른 구조와 좌우 위치를 정확히 구분했는가?
- 긴 식·세 val 필드·곱과 두 층의 부재 표현을 연결했는가?

</details>

#### 확인 Q07 · 구조상의 수와 진행 조건

트리의 구조상 노드 수를 빈 경우 0, 노드 경우 `1+왼쪽 수+오른쪽 수`로 셀 때 Q06 t2를 전개하라. 한 자식을 두 위치에서 공유한다면 무엇을 세는가? 정확한 Int 개수에 필요한 조건은?

<details><summary>해설 보기</summary>

값 4 노드에서 `1+0+0=1`, 루트 3에서 `1+1+0=2`다. 재귀는 실제 더 작은 하위 구조를 따라가야 한다. 유한·비순환 구조이며 호출이 정상 반환하고 구조상의 개수가 `0..2147483647` 안에 있다는 조건으로 정확한 Int 수를 설명한다. 공유 노드를 좌우 두 위치에서 따라가면 위치마다 다시 세므로 서로 다른 객체 수를 중복 없이 세는 알고리즘과 다르다. 타입에 자기 이름이 있다는 사실만으로 진행·자원·정수 범위를 보장하지 않는다.

**확인 기준**

- 빈 경우부터 아래에서 위로 수를 결합했는가?
- 위치 수와 서로 다른 객체 수, 유한성과 정수·자원 조건을 구분했는가?

</details>

### 경우 분석과 재귀 구조 연습

#### 연습 P01 · 둘째 원소의 존재를 표현하기

새로 쓴 강의 기반 일반 연습이다. Option 멤버 접근 자체를 직접 묻는 기출 형식 근거는 없다. 본문의 MyList 클래스에 대해 `secondValue[A](s:Option[MyList[A]]):Option[A]`를 None/Some 경우 분석만으로 작성하라. 빈 리스트·한 노드·3 다음 4인 두 노드에서 결과를 설명하라. Some 안에는 정상 노드가 있다고 가정한다.

<details><summary>해설 보기</summary>

필요한 두 존재 조건을 차례로 나눈다.

~~~text
def secondValue[A](s: Option[MyList[A]]): Option[A] =
  s match {
    case None => None
    case Some(first) => first.next match {
      case None => None
      case Some(second) => Some(second.value)
    }
  }
~~~

빈 리스트는 바깥 None에서 끝나고, 한 노드는 first.next=None에서 끝나므로 둘 다 None이다. 두 노드 예에서는 first.value=3, first.next=Some(second), second.value=4여서 Some(4)다. 두 분기를 합치고 곧바로 next의 value를 읽으면 한 노드 입력을 안전하게 처리하지 못한다. Option[A] 결과는 값이 없는 경우도 표현하여 임의 A의 가짜 기본값을 만들 필요가 없다.

**확인 기준**

- 세 입력의 분기 경로와 None·Some(4)를 검산했는가?
- first가 있다는 사실과 second가 있다는 사실을 구분했는가?

</details>

#### 연습 P02 · 빈 리스트와 꼬리 결과 결합

새로 쓴 합성 연습이다. 2024 중간 Q1-1에서 빈 경우와 꼬리의 계산 결과를 결합하는 구조만 연결한다 [EX:pop_2024_mid_q01_s01 L.46-57]. 선수는 Product/Sum·Option과 유한한 꼬리로의 진행이다. 역사적 enum·variance·fold/concat 구현은 요구하지 않는다. 본문의 Option 기반 리스트에서 길이를 빈 경우 0, 노드 경우 `1+꼬리 길이`로 설명하고 두 노드 3,4의 전개를 쓰라. 노드 값이 아닌 꼬리를 재귀 처리하는 이유와 정확한 Int 조건도 쓰라.

<details><summary>해설 보기</summary>

전체 None은 0이다. Some(node)이면 현재 위치 1과 node.next의 길이를 더한다. 두 노드 식에서는 `1+(1+0)=2`다. node.value는 임의 A의 데이터이며 다음 리스트 구조가 아니다. 구조상 더 작은 next를 처리하기 때문에 끝의 None으로 진행하는 논거가 생긴다. 유한·비순환이며 각 호출이 정상 반환하고 위치 수가 `0..2147483647` 안이어야 정확한 Int 길이다. 유한성만으로 stack·메모리 충분성은 나오지 않는다. 이는 역사적 자료형의 전체 fold를 구현한 답이 아니라 현재 표현으로 재귀 구조를 설명한 해법이다.

**확인 기준**

- 바깥 None과 마지막 next=None을 기저 결과에 연결했는가?
- 재귀 대상·현재 1의 결합·범위·정상 반환 조건을 모두 설명했는가?

</details>

#### 연습 P03 · 공유된 자식과 두 재귀 결과

새로 쓴 합성 연습이다. 2024 중간 Q1-2의 빈 가지와 두 하위 결과 결합만 연결한다 [EX:pop_2024_mid_q01_s02 L.70-78]. 선수는 세 노드 필드·Option·유한 비순환 하위 구조다. 전체 fold·탐색 구현과 당시 enum 문법은 범위 밖이다. 정상 노드 `leaf=new MyTree(7,None,None)`와 `root=new MyTree(3,Some(leaf),Some(leaf))`가 있다. `Some(root)`의 위치별 노드 수와 서로 다른 노드 객체 수를 비교하고, 오른쪽을 None으로 바꾸면 각각 무엇이 달라지는지 설명하라.

<details><summary>해설 보기</summary>

leaf의 위치별 수는 `1+0+0=1`이다. root는 좌우를 각각 처리하여 `1+1+1=3`이다. 실제 만들어 둔 노드 객체는 leaf와 root 두 개이므로 서로 다른 객체 수는 2다. 오른쪽만 None으로 구성한 새 root를 비교하면 위치별 수는 `1+1+0=2`, 그 트리에서 도달하는 서로 다른 노드 객체도 root와 leaf 두 개다. 같은 자식을 두 필드에서 쓰는 것이 깊은 복제는 아니다. 위치별 재귀 결합과 객체 중복 제거는 다른 문제다. 계산은 비순환 공유 구조에서 정상 반환하며 이 예의 수가 Int 범위 안이라는 조건에 따른다.

**확인 기준**

- 두 하위 결과를 별도로 결합하여 3과 2를 구분했는가?
- 공유·새 root 구성·깊은 복제·객체 수를 혼동하지 않았는가?

</details>

## 출처

[프로그래밍의 원리 Part2 · PDF pp.20–26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf) · 원본 쪽 보기: [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-020) · [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-021) · [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-022) · [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-023) · [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-024) · [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-025) · [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-026)

[프로그래밍의 원리 Part1 · Product·Sum·ADT·Option 선수 참고 pp.73–74, 76, 79, 92, 98](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

[[courses/principles_of_programming/lectures/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 · Class·재귀 자료·Inheritance와 Overriding · 강의 정리]]

[[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 전사 · 30:16·32:02·38:34·43:16·44:52·51:20·54:25·58:33]]

자료의 MyList·MyTree 정의로 생성식을 분석한다. 전사의 불명확한 숫자·기호·value.next 표현·명명 변경과 보이지 않는 트리 그림은 복원하지 않는다. 강의 정리는 2차 설명이며 날짜·음성 대조·실제 컴파일 및 실행 결과는 확인되지 않았다. p.21의 null·효율성 표현은 자료의 언어 모형이며 Java·Scala 전체의 안전성·성능에 관한 일반 명제는 아니다.

2024 중간 Q1-1은 빈 경우·꼬리 결과 결합 [EX:pop_2024_mid_q01_s01 L.46-57], Q1-2는 빈 가지·좌우 결과 결합 [EX:pop_2024_mid_q01_s02 L.70-78]의 풀이 구조만 연결한다. 2024 연도는 2025년 전년도 문제 공지에 근거한다. 역사적 enum·variance·전체 fold·concat·탐색 구현과 당시 제한은 현재 강의 범위·정책으로 옮기지 않는다. Companion·apply·null을 직접 묻는 기출 근거는 없다.


---

[[courses/principles_of_programming/units/class-construction|← 이전: Class와 생성 통제: 명목 타입·불변조건·계약]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/inheritance-overriding|다음: Inheritance·Overriding과 간접 동작 변화 →]]
