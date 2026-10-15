---
title: "Inheritance·Overriding과 간접 동작 변화"
description: "부모 생성자 결합과 동적 메서드 선택을 계산하고 재정의의 계약을 점검한다."
course: "principles_of_programming"
unit_id: "inheritance-overriding"
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

## Inheritance와 부모 생성자 인자

Inheritance(상속)는 부모의 멤버와 구현을 이용하면서 자식 타입의 멤버를 더하는 방법이다. 부모 타입이 요구하는 사용에 자식을 공급하는 명목 관계도 함께 다룬다. 이를 계산하려면 [생성자와 멤버의 구분](class-construction.md)을 유지하고 부모·자식 생성자의 이름 결합을 따로 추적해야 한다.

프로그래밍의 원리 Part2(NM001) p.28은 다음 프로그램을 사용한다. 여기의 `foo_type`, `gee_type`은 앞의 이름·나이 예제와 별개의 클래스다. 특히 `gee_type`은 p.16의 구조적 Alias가 아니다. [Part2 PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-028)

~~~text
class foo_type(x: Int, y: Int) {
  val a: Int = x
  def b: Int = a + y
  def f(z: Int): Int = b + y + z
}

class gee_type(x: Int) extends foo_type(x+1,x+2) {
  val c: Int = f(x) + b
}

(new gee_type(30)).c
~~~

`extends foo_type(x+1,x+2)`는 `gee_type <: foo_type`을 선언하면서 부모 부분을 초기화할 인자도 지정한다. 자식 입력을 같은 값으로 그대로 넘길 필요는 없다. 자식 생성자의 `x`, 부모 생성자의 `x,y`, 메서드의 `z`는 각각 다른 Binding(이름 결합)이다. 강의도 부모 생성자를 부르되 인자가 일대일로 같은 값일 필요는 없다고 설명한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:03:09]]

이 단원에서 계산하는 것은 이 자료 코드가 정상 생성한 객체의 결과와 `def b`·`def f`의 동작이다. 부모의 `a`가 설정된 뒤 자식 본문의 `c`를 초기화하는 이 정의를 따르며, 임의의 생성자 도중 가상 호출이나 재정의된 `val` 초기화 규칙 전체로 확대하지 않는다.

### new gee_type(30)의 결합과 계산

먼저 자식 생성자의 `x=30`이다. 따라서 부모에게 주는 첫 인자는 `30+1=31`, 둘째는 `30+2=32`다. 부모 안의 결합은 `x=31,y=32`가 되고 `val a=x`는 31을 저장한다.

자식 본문의 `f(x)`에 나타나는 `x`는 여전히 자식의 30이다. 이 인자를 메서드의 `z`에 공급하며, 상속한 본문의 `y`는 부모에게 전달된 32를 사용한다.

~~~text
부모 생성자 인자 = (31,32)
a = 31
b = a+y = 31+32 = 63
f(30) = b+y+30 = 63+32+30 = 125
c = f(30)+b = 125+63 = 188
~~~

부모의 `a`를 30으로 놓으면 첫 인자 변환을 빠뜨린다. 반대로 자식 본문의 `f(x)`에 부모의 31을 넣으면 다른 Binding을 가져온 것이다. `a,c`는 `val` 멤버이고 `b,f`는 `def` 메서드다. `b`는 사용할 때 본문을 계산하며, 숫자가 일정하더라도 생성 때 저장한 `val b`와 같다고 보면 안 된다. 단순 생성자 매개변수 `x,y`를 모두 공개 `val` 필드라고 읽어서도 안 된다.

이 예에서는 `a,b,f`를 재정의하지 않고 `c`만 추가한다. 부모의 생성과 구현을 이용해 위 결과를 얻는다는 사실과, 어떤 하위 클래스도 부모의 모든 행동 계약을 반드시 지킨다는 주장은 별개다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:04:04]]

## Parent View와 구현 Reuse

같은 페이지에는 다음 함수가 있다.

~~~text
def test(f: foo_type) = f.a + f.b

test(new foo_type(10,20))
test(new gee_type(30))
~~~

`test`의 매개변수 이름 `f`는 전달된 객체를 가리킨다. 클래스의 메서드 이름 `f`와 철자만 같다. 이 본문은 객체의 `a`와 `b`를 사용할 뿐 메서드 `f(z)`를 호출하지 않는다.

| 공급한 객체 | `a` | `b` | `test`의 계산 |
| --- | --- | --- | --- |
| `new foo_type(10,20)` | 10 | `10+20=30` | `10+30=40` |
| `new gee_type(30)` | 31 | `31+32=63` | `31+63=94` |

자식에는 `c=188`도 있지만 `test`는 그 멤버를 요구하지 않는다. `gee_type <: foo_type`이므로 부모 관점에서 허용된 `a,b` 사용에 자식을 공급할 수 있다. 자식의 `c`가 부모 타입의 인터페이스에 추가되었다는 뜻은 아니다.

Parent View(부모 관점)의 Abstraction(추상화)은 구체 객체의 더 많은 정보를 모두 요구하지 않고 현재 사용에 필요한 부모의 관점으로 이해하는 일이다. Reuse(재사용)는 자식이 부모 생성 절차와 `a,b,f` 구현을 복사 없이 이용한다는 점이다. 두 효과는 함께 나타날 수 있지만 구현을 재사용했다는 이유만으로 좋은 추상화가 자동으로 생기지는 않는다. 사용자가 의존한 계약이 유지되는지도 확인해야 한다. 강의도 이 효과와 한계를 함께 논의하며 일부 동작만 바꾸고 나머지 구현을 쓰려는 동기를 설명한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:06:30·01:07:26·01:08:16]]

## Overriding과 상속된 메서드의 의존

Overriding(재정의)은 상속한 메서드의 구현을 자식에서 바꾸는 것이다. p.29는 p.28의 선언에 이어 붙이는 코드가 아니라 다른 프로그램이다. 여기서 부모 `b`는 0, `f(z)`는 `b*z`다. 같은 입력 30을 쓰더라도 이전 덧셈 프로그램과 결과가 다르다. [Part2 PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-029)

~~~text
class foo_type(x: Int, y: Int) {
  val a: Int = x
  def b: Int = 0
  def f(z: Int): Int = b * z
}

class gee_type(x: Int) extends foo_type(x+1,x+2) {
  override def b = 10
  // or, override def b = super.b + 10
  val c: Int = f(x) + b
}

(new gee_type(30)).c
~~~

자식이 직접 재정의한 것은 `b`뿐이다. `a`와 `f`의 본문은 바꾸지 않았다. 그러나 상속된 `f` 안의 `b`도 현재 객체에 대한 메서드 사용이다. 실제 수신 객체가 자식이면 재정의한 `b=10`을 선택한다. Dynamic Dispatch(동적 메서드 선택)의 이 효과 때문에 `f`를 직접 덮어쓰지 않아도 계산 결과가 달라진다. 부모에서 적힌 본문이 0이라는 이유로 `f`의 `b`를 상수 0으로 치환하면 안 된다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:13:52]]

### c=310이 되는 전개

`new gee_type(30)`의 부모 인자는 여전히 31,32이고 `a=31`이다. 이 프로그램의 `f`는 부모의 `y`를 사용하지 않고 `b*z`만 계산한다.

~~~text
현재 객체의 b = 10
f(30) = 10*30 = 300
c = f(30)+b = 300+10 = 310
~~~

p.28의 188과 p.29의 310 차이는 산술 착오가 아니다.

| 프로그램 | 부모 `b` | 상속된 `f(z)` | 자식의 변경 | `gee_type(30).c` |
| --- | --- | --- | --- | --- |
| p.28 | `a+y` | `b+y+z` | `c` 추가 | 188 |
| p.29 | `0` | `b*z` | `b=10` 재정의, `c` 추가 | 310 |

`b`와 `f`가 `def`라는 조건을 유지하여 계산한 결과다. 다른 초기화 방식이나 가변 상태가 있는 프로그램에 이 숫자를 그대로 적용할 수는 없다.

### 부모 타입으로 받아도 유지되는 동적 선택

p.29의 `test`는 앞의 덧셈 함수와 다르다.

~~~text
def test(v: foo_type) =
  println(v.f(42))

test(new foo_type(1,2))
test(new gee_type(0))
~~~

첫 객체는 부모 구현을 사용한다. `b=0`이므로 `f(42)=0*42=0`이며 `println`에 전달할 값은 0이다.

둘째 객체의 자식 생성자 입력은 0이다. 부모에게는 1,2가 전달되고 `a=1`이 된다. 그러나 `test`가 메서드 `f`에 주는 인자는 생성자 입력 0이 아니라 42다. 실제 객체의 `b=10`을 선택하므로 `f(42)=10*42=420`을 `println`에 전달한다. 이 객체 자체의 `c`는 `f(0)+b=0+10=10`이지만 `test`는 `c`를 읽지 않는다.

`v`의 정적 타입이 `foo_type`이라는 사실은 어떤 멤버를 사용할 수 있는지를 정한다. 실제 자식 객체의 재정의가 사라지거나 부모 구현의 상수로 되돌아간다는 뜻이 아니다. 위 숫자들은 인쇄된 코드의 전개이며 실제 컴파일러 실행 결과를 관찰한 기록은 아니다.

### super.b가 지정하는 구현

주석의 대안은 `override def b=10` 대신 다음 본문을 쓰는 것이다.

~~~text
override def b = super.b + 10
~~~

`super.b`는 이 예에서 부모의 `b` 구현을 명시적으로 사용한다. 부모 본문이 0이므로 자식의 결과는 `0+10=10`이다. 따라서 같은 자료의 `f(30)=300`, `c=310`, `test(new gee_type(0))`에서 전달하는 값 420도 그대로다. 부모 본문이 달라져도 언제나 상수 10과 같은 효과라는 규칙은 아니다. `super.b`를 현재 자식의 `b`를 처음부터 다시 부르는 재귀 호출로 해석하지 않는 것이 중요하다.

## 현재 구현과 Behavioural Contract

부모의 현재 `b` 본문이 0이라는 관찰과 “모든 하위 타입의 `b`도 언제나 0이다”라는 계약은 다르다. 사용자가 후자를 믿고 있었다면 자식의 재정의는 그 약속을 깨뜨린다. 반대로 부모 계약이 `b`의 변경을 허용하고 `f`는 현재 객체의 `b`에 의존한다고 정했다면, 위 변화는 허용된 확장점이다. 강의가 어떤 변경을 허용하는지 주석으로 밝혀야 한다고 설명하는 이유다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:11:58]]

재정의할 메서드만 검토하면 간접 영향을 놓칠 수 있다. 이 예에서는 `b`의 변경이 그것을 부르는 `f`, 그리고 `f`와 `b`를 사용하는 `c`의 계산에 영향을 준다. 그렇다고 프로그램의 모든 관련 동작이 반드시 바뀐다는 정리는 아니다. 실제 의존과 부모가 허용한 계약을 확인해야 한다.

같은 이름에 다른 인자 타입의 호출 형태를 추가하는 Overloading(오버로딩)은 같은 메서드의 구현을 바꾸는 이 Overriding과 구분한다. 후속 p.30의 상세 overloading 예나 subclass ADT·enum·variance·fold·iterator는 이 단원의 완료된 강의 범위로 추가하지 않는다. 강의의 구현 비용·재사용 동기에 관한 유보와 추측도 특정 compiler의 구현이나 성능을 검증한 사실로 바꾸지 않는다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 01:14:42·01:15:40]]

## 확인·연습문제

### 상속과 부모 관점

#### 확인 Q01 · p.28의 세 이름 결합

별개의 p.28 프로그램이다. 부모 `foo_type(x:Int,y:Int)`는 `val a=x;def b:Int=a+y;def f(z:Int):Int=b+y+z`, 자식 `gee_type(x:Int) extends foo_type(x+1,x+2)`는 `val c:Int=f(x)+b`다. `new gee_type(30)`의 부모 인자·a·b·f(30)·c를 순서대로 구하라.

<details><summary>해설 보기</summary>

자식 x=30에서 부모 인자는 (31,32)다. 부모 안의 x=31,y=32이므로 a=31, b=31+32=63이다. 자식의 f(x)는 자식 x=30을 메서드 인자 z로 보내므로 f(30)=63+32+30=125, c=125+63=188이다. extends는 gee_type <: foo_type의 명목 관계와 부모 부분 초기화의 인자를 함께 지정한다. 자식 x, 부모 x,y, 메서드 z는 서로 다른 결합이다. p.16의 구조적 gee_type Alias와 이 클래스 이름을 합치지 않는다.

**확인 기준**

- (31,32),31,63,125,188을 식으로 검산했는가?
- 부모 a에 자식 30을 그대로 넣거나 f의 인자에 부모 31을 쓰지 않았는가?

</details>

#### 확인 Q02 · val·def·생성자 매개변수

Q01에서 `a,c`, `b,f`, 생성자 `x,y`를 같은 종류의 저장 필드로 취급해도 되는가? 계산의 초기화·재정의 조건과, 이 예가 보장하지 않는 일반 규칙을 설명하라.

<details><summary>해설 보기</summary>

a와 c는 val 멤버로 초기화한 값을 둔다. b와 f는 def이므로 사용할 때 본문을 계산한다. 현재 값이 일정하다는 이유로 b를 생성 시 저장한 val로 바꾸어 읽으면 안 된다. val 없는 생성자 매개변수 x,y를 모두 외부 공개 val 필드라고 볼 근거도 없다. Q01은 부모 a가 설정된 뒤 자식 본문의 c를 초기화하며 a,b,f를 재정의하지 않는 주어진 정의로 계산한다. 이 결과를 임의 생성자 도중의 가상 호출, 재정의 val의 eager 초기화, 가변 상태가 있는 프로그램 전체에 확대하지 않는다. 이후 호출 분석도 정상 생성이 완료된 객체와 제시된 def 메서드를 전제로 한다.

**확인 기준**

- 저장한 값·호출 시 계산·입력 이름 결합을 구분했는가?
- 특정 예의 초기화 순서를 임의 초기화 문제의 보장으로 바꾸지 않았는가?

</details>

#### 확인 Q03 · test의 두 호출과 Reuse

Q01의 p.28 정의에서 `def test(f:foo_type)=f.a+f.b`다. `test(new foo_type(10,20))`와 `test(new gee_type(30))`를 계산하라. 매개변수 f가 메서드 f(z)를 호출하는가? 부모 관점의 Abstraction과 구현 Reuse도 비교하라.

<details><summary>해설 보기</summary>

부모 객체는 a=10,b=10+20=30이므로 test=40이다. 자식 객체는 a=31,b=63이므로 test=94다. test의 f는 객체를 가리키는 매개변수이며 본문은 그 객체의 a,b만 사용한다. 이름이 같은 메서드 f(z)를 호출하지 않는다. gee_type <: foo_type이어서 부모가 허용한 사용에 자식을 공급한다. 실제 c=188이 있어도 부모 인터페이스에 c가 새로 추가되는 것은 아니다. Abstraction은 부모 관점으로 필요한 성질만 사용하는 것이고, Reuse는 자식이 부모 생성·구현을 복사 없이 이용하는 것이다. 구현 재사용만으로 좋은 추상화나 모든 행동 계약의 유지는 증명되지 않는다.

**확인 기준**

- 40·94를 a,b로 계산하고 메서드 f와 매개변수 f를 구분했는가?
- 부모의 사용 관점·추가 c·구현 재사용·계약을 구분했는가?

</details>

### 재정의와 간접 의존

#### 확인 Q04 · p.29의 새 b와 f

p.29는 새 프로그램이다. 부모 `val a=x;def b:Int=0;def f(z:Int):Int=b*z`, 자식은 `extends foo_type(x+1,x+2)`, `override def b=10`, `val c:Int=f(x)+b`다. 정상 생성된 `gee_type(30)`의 f(30),c를 계산하라. `test(v:foo_type)=println(v.f(42))`에 부모 객체 (1,2)와 자식 객체 (0)을 주면 어떤 수를 println에 전달하는가? 자식 (0)의 c도 구하라.

<details><summary>해설 보기</summary>

자식의 실제 b는 10이므로 f(30)=10*30=300, c=300+10=310이다. f를 직접 재정의하지 않았어도 그 안의 b가 현재 객체의 재정의 메서드를 선택한다. 부모 객체는 b=0이므로 f(42)=0이다. 자식 (0)은 부모 인자 (1,2),a=1이지만 test의 메서드 인자는 생성자 입력 0과 다른 42여서 f(42)=420이다. 그 객체 자신의 c는 f(0)+10=10이다. 따라서 두 println 인자는 0,420이다. 정적 타입 foo_type이 실제 자식의 재정의를 지우지 않는다. p.28의 덧셈 본문으로 얻은 188과 이 310은 다른 프로그램의 계산이다.

**확인 기준**

- 300·310·0·420·10을 각각 올바른 수신 객체와 인자로 전개했는가?
- 부모 본문 위치의 b를 상수 0으로 고정하지 않고 def의 동적 선택을 설명했는가?

</details>

#### 확인 Q05 · super.b의 구현 선택

Q04의 자식 정의를 `override def b=super.b+10`으로 대신하면 b·f(30)·c와 `test(new gee_type(0))`의 수는 무엇인가? 왜 자식 b를 다시 부르는 재귀 호출이 아니며, 언제나 상수 10과 같다고는 할 수 없는가?

<details><summary>해설 보기</summary>

이 부모의 b 본문은 0이다. super.b로 그 구현을 명시해 사용하므로 자식 b=0+10=10, f(30)=300,c=310, test의 println 인자는 420으로 같다. super.b를 현재 자식 b를 처음부터 다시 호출하는 것으로 읽지 않는다. 부모 본문이 다른 수를 주면 더한 결과도 달라질 수 있으므로 언제나 `override def b=10`과 같은 규칙은 아니다. 여기의 비교는 정상 생성 객체에서 제시된 def b·def f의 메서드 동작에 한정한다.

**확인 기준**

- 부모 0에 10을 더하는 경로와 나머지 계산을 연결했는가?
- 구현의 명시 선택과 동적 재호출을 구분했는가?

</details>

#### 확인 Q06 · 현재 본문과 영구 계약

‘부모의 b는 현재 0이다’와 ‘모든 하위 타입의 b는 반드시 0이다’는 같은가? 자식에서 b만 바꿀 때 검토할 의존과 허용 변경은 무엇인가? 다른 인자 타입의 f를 추가하는 것과도 구분하라.

<details><summary>해설 보기</summary>

현재 본문은 구현 관찰이고 두 번째 문장은 모든 하위 타입에 부과한 계약이다. 계약이 b=0을 고정했다면 b=10인 재정의는 이를 깨지만, b 변경을 허용하고 f가 현재 b를 쓰도록 정했다면 허용된 확장일 수 있다. 이 예의 의존은 b -> f -> c이며 c는 b도 직접 사용한다. 재정의한 메서드만 볼 것이 아니라 호출자와 사용자 약속을 확인한다. 모든 관련 동작이 반드시 변한다는 정리는 아니다. 같은 메서드 구현을 바꾸는 Overriding과 다른 인자 타입의 호출 형태를 추가하는 Overloading은 구분한다. 후속 p.30의 상세 예를 현재 완료된 강의로 추가하지 않는다.

**확인 기준**

- 구현 사실과 계약을 구분하여 두 조건의 다른 판정을 설명했는가?
- 간접 의존을 추적하면서 정적 상속 문법만으로 의미 안전성을 단정하지 않았는가?

</details>

### 상속 계산과 계약 연습

#### 연습 P01 · 인자 변환을 기호로 검산하기

새로 쓴 강의 기반 일반 연습이다. 부모 생성자 변환을 직접 다룬 관련 기출 형식 근거는 없다. Q01의 p.28 정의에서 자식 입력을 k라 하되 `0<=k<=100`으로 제한한다. 정상 생성 후 부모 인자·a·b·f(k)·c와 `test(new gee_type(k))`를 k의 식으로 도출하라. k=30으로 원래 수와 비교하고 각 x의 결합을 설명하라.

<details><summary>해설 보기</summary>

부모 인자는 (k+1,k+2), a=k+1이다. b=(k+1)+(k+2)=2k+3, f(k)=b+(k+2)+k=4k+5, c=(4k+5)+(2k+3)=6k+8이다. test는 a+b=(k+1)+(2k+3)=3k+4다. k=30에서 a=31,b=63,f(30)=125,c=188,test=94로 맞는다. 자식 x=k가 f의 인자이고 부모 내부의 y=k+2는 상속 본문이 사용한다. 주어진 작은 입력 범위의 모든 중간 계산은 Int 범위 안이다. def를 그대로 둔 정상 생성 객체의 식이며 임의 val 초기화·가변 상태로 옮기지 않는다.

**확인 기준**

- 각 단계의 결합과 `4k+5,6k+8,3k+4`를 재전개했는가?
- k=30에서 188·94가 함께 맞고 적용 범위도 지켰는가?

</details>

#### 연습 P02 · 상수 재정의와 super의 차이

새로 쓴 강의 기반 일반 연습이다. 동적 선택·super·행동 계약을 직접 묻는 관련 기출 근거는 없다. Q04와 별개의 변형에서 부모의 `def b:Int=2`, `def f(z:Int):Int=b*z`다. 다른 모든 생성 관계는 같고 자식의 `c=f(x)+b`를 유지한다. (가) `override def b=10`, (나) `override def b=super.b+10`을 각각 쓰면 x=30의 b,f(30),c 및 정상 생성 후 f(42)는 무엇인가? 부모 계약이 b=2를 고정한 경우와 b 변경을 허용한 경우도 비교하라.

<details><summary>해설 보기</summary>

(가)는 b=10, f(30)=300,c=310,f(42)=420이다. (나)는 부모 구현을 사용해 b=2+10=12이므로 f(30)=360,c=372,f(42)=504다. 상속된 f는 두 경우 모두 현재 객체의 b를 선택한다. 부모 인자는 (31,32),a=31로 같지만 이 f는 y를 사용하지 않아 위 곱셈에 y를 넣지 않는다. 두 재정의가 원래 자료에서 같았던 것은 부모 b=0이었기 때문이다. b=2 고정이 계약이면 둘 다 위반이다. 변경을 허용한 계약이라면 이 차이만으로 위반이라 할 수 없지만 f가 현재 b에 의존한다는 약속도 존중해야 한다. 계산은 이 정상 생성·def-only 예에 한정한다.

**확인 기준**

- 두 구현에서 10과 12를 먼저 구하고 310·372·420·504를 독립 계산했는가?
- 상속된 본문과 동적으로 선택된 메서드, 구현 변화와 계약 조건을 구분했는가?

</details>

## 출처

[프로그래밍의 원리 Part2 · PDF pp.28–29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf) · 원본 쪽 보기: [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-028) · [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-029)

[프로그래밍의 원리 Part1 · Abstraction·Reuse 선수 참고 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

[[courses/principles_of_programming/lectures/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 · Class·재귀 자료·Inheritance와 Overriding · 강의 정리]]

[[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 전사 · 01:03:09·01:04:04·01:06:30·01:07:26·01:11:58·01:13:52·01:14:42·01:15:40]]

수치는 p.28과 p.29의 서로 다른 인쇄 코드를 전개한 값이다. 불명확한 발화의 숫자·지시어·부정·출력이나 실제 시연을 복원한 것이 아니다. 강의 정리는 2차 설명이고 날짜·음성 대조·실제 컴파일 및 실행 결과는 확인되지 않았다. 분석은 정상 생성과 제시된 def 메서드에 한정하며 임의의 val 초기화나 가상 호출 규칙을 보장하지 않는다.

직접 대응하는 부모 생성자 변환·동적 재정의·super 기출 후보는 없다. 2025 부분 Q1의 외곽 class는 구조적 Alias를 묶는 선언으로, extends·override의 근거가 아니다. Part2 p.30 이후 상세 Overloading·subclass ADT·enum·variance·fold·iterator는 현재 완료된 강의 범위에 추가하지 않는다.


---

[[courses/principles_of_programming/units/recursive-classes|← 이전: 재귀 클래스, Option과 Companion Object]] · [[courses/principles_of_programming/units/index|단원 목차]]
