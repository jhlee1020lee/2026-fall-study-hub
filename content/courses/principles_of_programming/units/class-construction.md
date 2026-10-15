---
title: "Class와 생성 통제: 명목 타입·불변조건·계약"
description: "생성 함수와 클래스의 소속 기준, 범위 검사, 불변조건과 행동 계약을 비교한다."
course: "principles_of_programming"
unit_id: "class-construction"
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

## Class와 Factory의 생성 절차

같은 멤버를 가진 객체를 여러 입력으로 만들려면 생성 절차를 묶어 쓸 수 있다. Factory(생성 함수)는 입력을 받아 객체를 구성해 반환하는 함수다. Class(클래스)는 여기에 타입 이름과 그 타입의 값을 구성하는 절차를 함께 제공한다. 두 방식의 코드가 비슷하더라도 결과 타입에 속하는 기준은 다르다. [Structural·Nominal 관계](structural-subtyping.md)가 이 차이를 판단하는 기준이다.

프로그래밍의 원리 Part2(NM001) p.16의 `gee_type`은 이름·나이·문자열 메서드를 요구하는 Structural Type(구조적 타입)의 Alias(별칭)다. 다음 코드는 그 구조의 값을 만드는 자료 예다. [Part2 PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-016)

~~~text
import reflect.Selectable.reflectiveSelectable

type gee_type = {
  val name: String
  val age: Int
  def getPP(): String
}

def gee_fun(_name: String, _age: Int): gee_type = {
  if (!(_age >= 0 && _age < 200))
    throw new Exception("Out of range")
  object tmp {
    val name: String = _name
    val age: Int = _age
    def getPP(): String = name + " of age " + age.toString()
  }
  tmp
}

val gee: gee_type = gee_fun("David Jones",25)
gee.getPP()
~~~

`_name`은 `String`, `_age`는 `Int` 입력이다. 먼저 나이 범위를 검사하고, 정상 경로에서 `name=_name`, `age=_age`인 객체를 만든다. 마지막 `tmp`가 반환값이다. `getPP()`는 인자가 없는 메서드 호출이며 `age.toString()`은 정수를 문자열 연결에 사용한다. 자료 식의 전개는 다음과 같다.

~~~text
"David Jones" + " of age " + "25"
= "David Jones of age 25"
~~~

입력이 다른 경우에도 같은 생성 코드를 쓴다. Alias를 선언하는 것 자체가 객체를 만드는 것은 아니며, 실제 생성은 함수 본문이 한다. 날짜 미확인 강의도 이런 구조적 생성 함수에서 출발해 클래스의 차이를 설명한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 03:06·05:36]]

### 같은 검사와 멤버를 Class에 두기

p.17은 같은 검사와 멤버를 클래스 본문에 둔다. [Part2 PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-017)

~~~text
class foo_type(_name: String, _age: Int) {
  if (!(_age >= 0 && _age < 200))
    throw new Exception("Out of range")
  val name: String = _name
  val age: Int = _age
  def getPP(): String = name + " of age " + age.toString()
}

val foo: foo_type = new foo_type("David Jones",25)
foo.getPP()
~~~

`new foo_type(...)`는 Constructor(생성자)에 입력을 공급한다. 검사 후 정상적으로 생성된 값은 `foo_type`인 객체다. `foo.name`, `foo.age`는 멤버를 읽고 `foo.getPP()`는 메서드를 호출한다. 자료 p.17의 별도 use 줄에는 `foo.getPP`처럼 괄호가 생략되어 있지만, 정의와 실제 호출 예는 `getPP()`다. 이 차이를 버전과 무관한 자동 적용 규칙으로 일반화하지 않는다.

`gee_fun`과 `new foo_type` 모두 나이 검사를 거쳐 같은 멤버를 만들지만, `gee_type`은 요구 구조를 가진 값 전체를 받아들이는 Alias이고 `foo_type`은 클래스 선언이 도입한 Nominal Type(명목 타입)이다. 클래스는 “어떤 구조인가”에 더해 “어떤 이름의 클래스와 선언된 생성·상속 관계에 속하는가”를 판단 기준으로 둔다. 강의의 “이 타입의 이름을 주는 거예요”는 이 차이를 짚는다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 08:32]]

## 구조적 사용과 명목적 소속의 방향

`foo_type`의 객체는 `name:String`, `age:Int`, `getPP():String`을 제공한다. 따라서 그 구조만 요구하는 `gee_type` 관점으로 사용할 수 있다. [Part2 PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-018)

~~~text
foo_type <: gee_type

val v1: gee_type = foo
val v2: foo_type = gee  // type error
~~~

p.18에서 보아야 할 것은 두 관계의 비대칭이다. `foo_type <: gee_type`은 인정되지만, 반대 `gee_type <: foo_type`에는 취소 표시가 있고 두 번째 대입에는 type error가 붙는다. 구조만 같다는 사실은 그 클래스의 명목적 소속을 만들지 못한다. `gee_fun`이 비슷한 검사까지 한다는 사실도 이 소속을 대신하지 않는다.

더 작은 구조를 요구하는 함수도 가능하다. 같은 페이지의 함수는 `name:String`만 읽으므로 클래스 값 `foo`를 받을 수 있다.

~~~text
def greeting(r: {val name: String}) =
  "Hi " + r.name + ", How are you?"

greeting(foo)
~~~

이 함수에는 객체가 어느 Factory나 클래스에서 왔는지보다 필요한 읽기 멤버가 있는지가 중요하다. 반면 특정 클래스의 생성 경로와 계약에 의존해야 하는 함수는 명목 타입을 요구할 이유가 있다. 이 비교의 `gee_type`은 p.16의 구조적 Alias다. 뒤의 상속 예제 p.28에 같은 철자의 클래스가 나오더라도 별개의 정의다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 25:16·26:22]]

## Invariant를 지키는 생성 경로

Invariant(불변조건)는 추상화의 값에 대해 유지하려는 성질이다. 이 예의 나이 조건은 `0 <= age < 200`이다. `age:Int`라는 타입 선언은 값이 정수라는 정보이고, 그 정수가 이 범위에 든다는 것은 추가 조건이다.

검사는 다음 식이 참일 때 예외 경로로 간다.

~~~text
!(_age >= 0 && _age < 200)
~~~

두 부등식을 모두 만족해야 정상 생성으로 진행한다. 설명용 경계값을 직접 대입하면 다음과 같다.

| `_age` | `_age >= 0` | `_age < 200` | 자료 코드의 경로 |
| --- | --- | --- | --- |
| `-1` | 거짓 | 참 | 예외 |
| `0` | 참 | 참 | 정상 생성 |
| `199` | 참 | 참 | 정상 생성 |
| `200` | 참 | 거짓 | 예외 |

`gee_fun`과 클래스 생성자는 모두 이 검사를 한다. 그러므로 두 절차가 정상 반환한 객체는 검사 조건을 통과했다. 그러나 이것이 모든 `gee_type` 값의 나이가 그 범위에 있다는 뜻은 아니다. 다른 코드가 그 Factory를 거치지 않고 같은 구조를 만들 수 있기 때문이다.

예를 들어 `age=-1`인 읽기 멤버와 나머지 요구 멤버를 갖춘 구조적 값을 생각하자. 이 설명용 반례는 `age:Int`에는 맞지만 범위에는 어긋난다. 구조적 Alias에는 “반드시 `gee_fun`을 호출해서 만들 것”이라는 조건이 없다. 자료 p.19의 “구조적 타입에서는 성질을 가정할 수 없다”는 대비도 보충해서 읽어야 한다. 선언된 필드 타입까지 무의미하다는 뜻이 아니라, 구조만으로 추가적인 업무상 성질을 가정할 수 없다는 뜻이다. [Part2 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-019)

클래스는 이름으로 소속과 허용된 생성 경로를 관리하여 더 강한 성질을 유지할 기반을 준다. 다만 클래스 이름 자체가 임의의 Invariant를 증명하는 것은 아니다. 검사식이 올바르고, 허용된 생성 경로가 이를 지키며, 이후의 변경이나 상속이 조건을 깨뜨리지 않아야 한다. 여기서 나이 조건을 적용하는 대상도 `null`이 아닌 정상 생성 객체다. 구조적 타입에 대한 대입이 허용된다는 사실만으로 `null` 역참조가 안전해지지는 않는다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 20:31·22:26]]

## Behavioural Contract와 상속의 책임

Behavioural Contract(행동 계약)는 사용하는 코드가 객체의 동작에 대해 무엇을 가정할 수 있는지 정한다. 부모 타입 자리에 자식을 공급할 수 있다는 정적 관계와, 부모 사용자가 믿는 의미적 약속을 지킨다는 사실은 구분해야 한다. 강의는 상속받는 쪽이 유지해야 할 성질을 깨면 사용자가 이해한 추상화도 깨진다고 설명한다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 18:36·19:34]]

나이가 범위 안이라는 조건을 약속했다면 자식도 그 조건을 존중해야 한다. `getPP()`가 이름과 나이를 일정한 형식으로 표현한다고 약속했다면 반환 타입이 여전히 `String`이라는 이유만으로 의미를 임의로 바꾸어도 되는 것은 아니다. 예컨대 사용자가 `"이름 of age 나이"` 형식을 계약의 일부로 믿고 있었다면 전혀 다른 형식은 그 사용을 깨뜨릴 수 있다. 반대로 계약이 표시 형식의 변경을 허용했다면 그 범위의 변경은 허용된다. 두 계약은 같은 `()=>String` 모양만으로 구분되지 않는다.

따라서 `extends`라는 문법만으로 나이·출력 의미를 포함한 모든 행동 약속이 자동 검사되지는 않는다. 부모를 정의할 때 유지할 성질과 바꾸어도 되는 부분을 분명히 해야 한다. 강의가 제안하는 생성 뒤 성질 확인 절차는 이런 동기를 설명하는 생각이며, 구체적인 검사용 API나 완성된 구현이 주어진 것은 아니다. 생성자 통제와 이후의 계약 유지가 함께 필요하다는 것이 핵심이다. [[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 NT002 23:21·24:17]]

## 확인·연습문제

### 생성 절차와 타입의 소속

#### 확인 Q01 · Factory의 입력부터 결과까지

Part2 p.16의 `gee_type={val name:String;val age:Int;def getPP():String}`와 `gee_fun(_name:String,_age:Int)`를 생각하자. 함수는 `!(_age>=0 && _age<200)`이면 예외, 아니면 `name=_name,age=_age,getPP()=name+" of age "+age.toString()`인 객체를 반환한다. `gee_fun("David Jones",25)`의 경로·멤버·문자열을 설명하고 Alias 자체가 객체를 만드는지 답하라.

<details><summary>해설 보기</summary>

25는 `0<=25<200`이어서 정상 경로다. 함수가 구성한 객체는 `name="David Jones",age=25`이며 `getPP()`는 `"David Jones"+" of age "+"25"="David Jones of age 25"`다. `age.toString()`은 정수를 문자열 연결에 쓴다. 마지막 객체가 함수 결과로 반환된다. Alias는 요구 구조를 이름 붙이고, 실제 생성은 입력을 받아 검사·구성하는 함수 본문이 한다. `getPP()`는 빈 인자 목록의 메서드 호출이다.

**확인 기준**

- 검사·구성·반환의 순서와 정확한 문자열을 도출했는가?
- Alias와 실행되는 Factory 본문, 멤버 읽기와 메서드 호출을 구분했는가?

</details>

#### 확인 Q02 · 같은 구성 코드와 다른 타입

p.17의 `class foo_type(_name:String,_age:Int)`가 Q01과 같은 검사·멤버를 가진다고 하자. `new foo_type("David Jones",25)`와 Factory 결과 타입의 뜻을 비교하라. 자료 p.17의 use 줄 `foo.getPP`와 정의·호출 `getPP()`의 차이에서 무엇을 일반화하면 안 되는가?

<details><summary>해설 보기</summary>

두 절차는 정상 입력에 name·age·getPP를 갖는 값을 만든다. 그러나 `gee_type`은 요구 구조의 별칭이고 `foo_type`은 클래스 선언이 도입한 명목 타입이다. 클래스는 타입 이름과 생성 절차를 함께 주며 그 소속은 선언한 생성·상속 관계로 판단한다. `new`는 그 생성자에 입력을 공급하고 `foo.name,foo.age`는 멤버를 읽는다. 자료의 정의와 호출 예는 `getPP()`인데 별도 use 줄에는 괄호가 빠져 있다. 이 표기 차이를 모든 Scala 버전의 자동 적용 규칙으로 확대하지 않는다.

**확인 기준**

- 코드의 유사성과 타입 소속 기준의 차이를 설명했는가?
- 이름의 철자·괄호를 유지하고 자료의 표기 차이를 구분했는가?

</details>

#### 확인 Q03 · p.18의 한 방향만 허용되는 대입

Q01의 구조적 `gee_type`과 p.17의 클래스 `foo_type`을 사용한다. `foo`는 정상 생성 클래스 객체, `gee`는 Factory가 만든 구조적 객체다. `val v1:gee_type=foo`, `val v2:foo_type=gee`와 `greeting(r:{val name:String})`에 foo를 주는 경우를 각각 판단하라.

<details><summary>해설 보기</summary>

`foo_type <: gee_type`이므로 v1은 필요한 name:String·age:Int·getPP():String을 모두 제공한다. greeting도 name:String만 읽으므로 foo를 받을 수 있다. 반대로 v2에는 foo_type의 명목적 소속이 필요하며 구조가 같고 같은 검사를 했다는 사실만으로 그 소속이 생기지 않는다. p.18은 `gee_type <: foo_type`를 취소 표시하고 v2를 type error로 둔다. 이 `gee_type`은 p.16의 Alias이며 p.28 상속 예제의 동명 클래스와 별개다. 멤버 사용은 null이 아닌 정상 객체라는 전제도 필요하다.

**확인 기준**

- 허용 방향과 취소된 역방향을 구분했는가?
- 구조적 사용 가능성과 특정 클래스의 소속을 혼동하지 않았는가?

</details>

### 불변조건과 계약

#### 확인 Q04 · 검사한 생성 경로와 타입 전체

나이 조건 `0<=age<200`에서 -1·0·199·200을 각각 판정하라. gee_fun이 검사하더라도 모든 gee_type 값이 조건을 만족한다고 볼 수 없는 이유와, 클래스 이름만으로 임의 Invariant가 증명되지 않는 이유를 설명하라.

<details><summary>해설 보기</summary>

-1은 아래 경계, 200은 위 경계 밖이어서 예외 경로다. 0과 199는 두 부등식을 모두 만족해 정상 생성된다. gee_type은 age:Int 구조만 요구하므로 다른 코드가 Factory를 거치지 않고 age=-1과 나머지 요구 멤버를 가진 구조적 값을 만들 수 있다. 정수 타입에는 맞아도 범위에는 어긋난다. 따라서 검사한 두 생성 절차가 정상 반환한 객체와 그 구조적 타입 전체를 구분한다. 클래스는 소속·생성 경로 통제의 기반을 주지만 실제 검사, 허용된 생성 경로와 상속·변경, null이 아닌 정상 객체 조건을 확인해야 한다. 필드 타입 보장은 여전히 의미가 있다.

**확인 기준**

- 네 경계값을 예외·정상 경로와 연결했는가?
- 검사 우회 구조의 반례와 클래스의 추가 검토 조건을 설명했는가?

</details>

#### 확인 Q05 · 정적 대체와 행동 약속

부모 계약이 (가) `getPP()`는 반드시 `"이름 of age 나이"` 형식, (나) 반환은 String이면 되고 표시 형식은 변경 가능, 두 경우라고 하자. 자식이 String 반환 타입을 유지하면서 다른 형식을 쓰면 각각 어떻게 판단하는가? `extends`만으로 판정이 끝나는가?

<details><summary>해설 보기</summary>

(가)에서는 사용자가 그 형식을 약속으로 의존하므로 자식이 다른 형식으로 바꾸면 계약을 깬다. (나)는 그 변경을 허용하므로 표시 형식 변경만으로 위반이라 할 수 없다. 나이 범위도 계약에 포함했다면 하위 타입이 존중해야 한다. 정적 타입 관계가 필요한 멤버 사용을 허용해도 임의 의미 조건 전체를 자동 증명하지 않는다. 바꿀 수 있는 부분과 유지할 불변조건·메서드 의미를 명시하고 실제 동작을 따로 검토해야 한다. 생성 뒤 성질 확인이라는 강의의 생각을 구체적인 검사용 API나 실제 성공 구현이 주어진 것으로 읽지 않는다.

**확인 기준**

- 두 계약의 다른 판정을 같은 반환 타입과 구분했는가?
- 정적 관계·허용 변경·의미적 계약을 각각 설명했는가?

</details>

### 생성과 계약을 검토하는 연습

#### 연습 P01 · 검사했다는 주장 검토

새로 쓴 강의 기반 일반 연습이다. Factory·명목 소속·불변조건을 직접 묻는 관련 기출 형식 근거는 없다. 어떤 개발자가 ‘gee_fun으로 만든 모든 결과가 범위 검사를 통과하므로 gee_type 매개변수의 age도 항상 0 이상 200 미만이다’라고 주장한다. 그 논증의 잘못된 단계와 반례를 제시하고, 주장할 수 있는 더 좁은 문장과 클래스 사용 시 확인할 조건을 쓰라.

<details><summary>해설 보기</summary>

‘그 Factory가 정상 반환한 결과’에서 ‘같은 구조의 모든 값’으로 대상을 넓힌 단계가 잘못이다. 예컨대 name:String, age=-1:Int, 요구한 getPP():String을 가진 객체는 Factory를 거치지 않아도 구조적 요구를 충족한다. 반례가 나이 범위에는 어긋나므로 전체 주장도 틀리다. 더 좁은 문장은 ‘주어진 검사식을 통과해 gee_fun 또는 제시된 생성자가 정상 반환한 객체의 age는 범위 안이다’다. 클래스에서는 검사식의 정확성과 허용된 생성·상속·변경이 성질을 유지하는지, 사용 대상이 null 아닌 정상 객체인지 확인한다. 필드 타입과 업무상 범위를 별개로 취급한다.

**확인 기준**

- 모든 Factory 결과와 모든 구조적 값 사이의 양화 대상 차이를 찾았는가?
- 반례의 구조는 맞추면서 범위만 깨고, 좁힌 문장에 정상 반환 조건을 넣었는가?

</details>

#### 연습 P02 · 사용자가 믿을 계약

새로 쓴 강의 기반 일반 연습이다. 행동 계약을 직접 묻는 관련 기출 근거는 없다. 사용자 코드는 getPP 결과를 `" of age "`로 나누어 이름과 나이를 읽는다. 자식은 같은 String 반환 타입으로 `"나이: 25, 이름: David Jones"`를 반환하려 한다. 계약이 명시되지 않은 상태에서 타입만으로 변경의 안전성을 판단할 수 있는가? 사용자·부모 작성자가 확인할 사항을 제시하라.

<details><summary>해설 보기</summary>

String이라는 타입은 사용자의 분리 규칙을 보장하지 않는다. 새 형식에는 정확한 구분 문자열이 없으므로 기존 파싱 사용은 깨질 수 있다. 먼저 부모가 표시 형식을 고정 약속으로 주었는지, 사용자가 허용 범위 밖의 구현 세부에 의존했는지 확인해야 한다. 고정 계약이면 자식은 그 형식을 유지해야 한다. 형식 변경이 허용된 계약이면 사용자가 그 고정 파싱을 안전한 사용으로 주장할 수 없다. 나이 범위 같은 다른 약속도 따로 유지해야 한다. 명목 관계가 있다는 것만으로 의미의 대체 가능성을 확정하지 않는다.

**확인 기준**

- String 타입과 구체 문자열 계약을 구분했는가?
- 계약의 유무·허용 변경에 따라 책임을 나누고 임의의 위반 판정을 피했는가?

</details>

## 출처

[프로그래밍의 원리 Part2 · PDF pp.16–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf) · 원본 쪽 보기: [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-016) · [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-017) · [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-018) · [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part2/page-019)

[프로그래밍의 원리 Part1 · 구조적 타입·별칭 선수 참고 pp.70–72](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part1.pdf)

[[courses/principles_of_programming/lectures/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 · Class·재귀 자료·Inheritance와 Overriding · 강의 정리]]

[[courses/principles_of_programming/transcripts/undated-classes-inheritance-jk9b2ob0objzgyvy|날짜 미확인 전사 · 03:06·05:36·08:32·18:36·20:31·23:21·25:16]]

전사의 대입·범위 부정·출력 표현과 실시간 시연이 불명확한 곳은 자료의 정확한 코드 분석과 구분한다. 강의 정리는 2차 설명이며 날짜·음성 대조·실제 컴파일 및 실행 결과는 확인되지 않았다. 나이 검사·정적 소속만으로 임의의 Invariant·행동 계약·null 안전성을 증명하지 않는다.

검토한 기출에는 Factory와 Class의 소속, 생성 범위 검사, 행동 계약을 직접 다루는 문항이 없다. 2025 부분 Q1의 class 외곽이나 2024 문제의 예외 클래스만으로 이 단원의 기출 형식 근거를 만들지 않는다.


---

[[courses/principles_of_programming/units/structural-subtyping|← 이전: Structural Subtyping과 함수의 대체 가능성]] · [[courses/principles_of_programming/units/index|단원 목차]] · [[courses/principles_of_programming/units/recursive-classes|다음: 재귀 클래스, Option과 Companion Object →]]
