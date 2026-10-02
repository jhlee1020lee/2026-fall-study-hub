---
title: "동적 Binding·Object 계약·Interface와 Abstract Class"
description: "Binding, Object 계약, List·Comparable와 interface/abstract class 설계를 복습한다."
course: "computer_programming"
unit_id: "object-contracts-interfaces"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["7 inheritance 2.pdf", "6 inheritance 1.pdf"]
private_source_assets: []
source_lectures: []
---

같은 호출이 어느 구현을 선택하는지와 객체의 표현·동등성·순서 계약을 구별한다. Interface와 abstract class가 공통 동작과 상태를 어떻게 나누는지 회상해 보자.

## Binding: 호출할 수 있는 method와 실행할 body 구분하기

같은 type(자료형)의 reference(참조)로 서로 다른 객체를 다루려면, 호출의 약속은 공통으로 유지하면서 실제 행동은 객체에 맞게 선택할 수 있어야 한다. Binding(바인딩)은 method 호출을 어떤 동작에 연결하는지 설명한다. [Inheritance](inheritance.md)에서 익힌 선언 type과 실제 객체의 구별이 출발점이다. 이 단원의 상세 내용은 NM001 Inheritance 2와 필요한 RM001 내용에 근거한 **자료 기반 학습**이며 새 녹음이나 특정 날짜의 수업 진도를 뜻하지 않는다.

NM001 pp.4–7은 다음 두 reference 배치를 유지한 채 method 선언만 바꾸어 비교한다.

```java
Parent parent = new Parent();
Parent child = new Child();
```

| `print()`의 선언 | `parent.print()` | `child.print()` | 이유 |
|---|---|---|---|
| 두 class의 `static` method | `Parent.print()` | `Parent.print()` | 두 식의 선언 type이 모두 `Parent`다. |
| 부모 instance method와 자식 override | `Parent.print()` | `Child.print()` | 두 실제 receiver의 class가 다르다. |

Compiler는 reference의 선언 type과 사용할 수 있는 signature를 안다. Runtime에는 선택된 instance signature에 대해 실제 객체의 override를 선택한다. NM001 p.3의 “compilation 중 type을 모른다”는 문구는 선언 type까지 모른다는 뜻으로 받아들일 수 없어 이렇게 한정한다. `private` method는 자식의 override 대상이 아니며 `final` method도 override할 수 없다. 이 구별에서 JVM 내부 최적화나 호출 비용을 추론하지 않는다.

2026-1 기말 복기 2번처럼 field·static·instance 호출이 함께 나오면 먼저 각 표현을 분류한다. Field와 static 선택은 선언 type, override된 instance 호출은 실제 receiver를 따라 추적하며, 부모 type cast가 나타나도 instance override는 유지된다. 이 세 경로를 구분하는 설명이 단순히 출력만 적는 것보다 중요하다. 복기본은 역사적 보조 자료이며 전체 문제나 제공 답안을 여기 옮기지 않는다. [EX:cp_2026_1_final_q02 p.2]

### `Shape[]`로 서로 다른 도형에 같은 요청 보내기

NM001 pp.8–9의 `Shape.randShape()`는 `(int)(Math.random() * 2)`에 따라 `Circle` 또는 `Square`를 반환한다. 반환 type은 `Shape`지만 실제 객체는 구체적인 도형이다. 자료의 두 loop는 서로 다른 일을 한다.

```java
Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();
```

배열 생성은 처음에 네 reference slot을 만들며, 각 slot은 `null`이다. 도형 네 개를 이미 생성한 것은 아니다. 첫 loop가 slot마다 도형 객체의 reference를 넣고, 둘째 loop가 공통 `draw()`를 요청한다. 실제 `Circle`이면 `Circle.draw()`, `Square`이면 `Square.draw()`가 실행된다. Slot을 채우지 않은 채 호출하면 받을 객체가 없다는 경계도 배열 초기값과 연결해 이해할 수 있다.

자료의 `Circle`, `Square`, `Circle`, `Circle` 네 줄은 가능한 출력 예다. 같은 배열 길이라는 이유로 난수 결과도 항상 그 순서가 되지는 않는다. 이 예는 서로 다른 구체 type을 공통 type으로 순회하는 이유를 보여 주지만, Lab04에 동일한 상속 구조를 구현해야 한다는 요구는 아니다.

## `toString()`: 객체를 바꾸지 않고 표현을 제공하기

객체를 출력할 때마다 field를 개별적으로 연결하면 같은 표현 규칙이 여러 곳에 반복된다. `Object`의 `public String toString()`을 재정의하면 객체의 문자열 표현을 한곳에 모을 수 있다. 반환 type이 `String`이라는 점에서, 직접 인쇄하고 반환하지 않는 `void` method와도 다르다. [NM001 PDF pp.12–16]

```java
class MyClass {
    @Override
    public String toString() {
        return "MyClass";
    }
}
```

이 자료 예에서 `"String = " + myClass`는 `String = MyClass`라는 표현을 만든다. NM001 p.14는 이를 String으로 cast한다고 표현하지만, 객체의 실제 class가 `String`으로 변하거나 reference cast를 하는 것이 아니다. **객체를 설명하는 String을 얻어 연결하는 것**이다.

자료의 String 예에서는 직접 출력과 `toString()` 결과가 같은 내용을 나타내고, File 예도 두 방식에서 같은 경로 표현을 보여 준다. 이것은 경로의 표현 예이지 파일을 여는 동작은 아니다. 별도의 `Student` 예는 `fName`, `lName`, `id`를 `String.format("%s %s (%d)", ...)`로 표현한다. 개인 이름이나 식별값을 외울 이유는 없다. 중요한 것은 여러 출력 지점이 같은 format을 사용하게 하는 책임 분리다.

## `equals()`: identity와 내용 동등성을 구별하기

Reference의 `==`는 같은 객체를 가리키는지, 즉 identity(동일성)를 검사한다. `Object.equals()`의 기본 동작도 이 구별에 해당하지만, class는 의미 있는 field를 기준으로 내용 동등성을 정의할 수 있다. NM001 p.18의 별도 `new String("abc")` 두 개는 `==`가 `false`, `equals()`가 `true`다. String이 이미 내용 비교를 제공하기 때문이다. 이것을 물리 주소를 직접 노출하는 연산으로 이해할 필요는 없다.

Primitive 값 자체에는 instance `equals()` method가 없다. 따라서 p.17의 primitive에 대해서도 `==`와 `equals()`가 같다는 문장은 정확하지 않다. Primitive 값의 비교와 wrapper 객체의 method 호출을 구분해야 한다.

### `Shoes`의 검사 순서와 두 종류의 null 경계

NM001 pp.19–21의 `Shoes`는 `company`, `model`, `size`로 동등성을 정의한다. 검사는 다음 순서다.

1. `this == o`이면 같은 객체이므로 즉시 `true`다.
2. 그 외에는 `o instanceof Shoes`인지 검사한다.
3. 맞으면 `Shoes`로 cast하고 `company.equals(...)`, `model.equals(...)`, `size == ...`가 모두 참인지 확인한다.
4. `Shoes`가 아니면 `false`다.

예제의 `Nice`, `AirMax`, `265`라는 값이 같은 별도 두 객체를 `s1`, `s2`라 하고 `s3 = s1`로 두면 다음과 같다.

| 비교 | 결과 | 이유 |
|---|---|---|
| `s1 == s2` | `false` | 따로 생성한 두 객체다. |
| `s1.equals(s2)` | `true` | 선택한 세 field가 모두 같다. |
| `s1 == s3` | `true` | 같은 객체의 reference를 대입했다. |
| `s1.equals(s3)` | `true` | 첫 identity 검사에서 끝난다. |

인자 `o`가 `null`이면 `instanceof`가 거짓이어서 `false`로 끝난다. 그러나 이것이 내부 field까지 null-safe라는 뜻은 아니다. 서로 다른 `Shoes`를 비교할 때 receiver의 `company`나 `model`이 `null`이면 그 field에 직접 `equals()`를 부르는 경로가 실패할 수 있다. 이는 코드에서 읽은 한계이며 완전한 범용 equality 구현이라고 포장하지 않는다. [NM001 PDF p.20]

## Collection의 동등성과 `hashCode()` 계약

동등성을 정의하면 collection(컬렉션)에서도 그 의미를 사용할 수 있다. NM001 p.23의 `frequency` 예는 `result = 0`부터 시작한다. 찾는 값 `o`가 `null`이면 각 원소에 대해 `e == null`인 횟수를 세고, 아니라면 `o.equals(e)`가 참인 횟수를 센다. Null receiver에 method를 호출하지 않기 위해 경로를 나눈 것이다. 내용이 같은 별도 `Shoes`도 위 `equals()`를 만족하면 같은 값의 출현으로 집계할 수 있다.

여기의 `Collection<?>`는 특정 원소 type을 고정하지 않은 collection을 다루는 표기다. 전체 generic type 체계를 다룬 것은 아니다. 이름도 구별해야 한다. `Collection`은 interface이고 이런 static utility를 제공하는 class 이름은 `Collections`다. NM001 p.22의 축약된 설명을 두 이름이 같은 것으로 읽지 않는다.

`hashCode()`는 객체에 대응하는 `int`를 제공하며 다음 방향의 계약이 필요하다.

\[
a.equals(b)=\text{true}\quad\Longrightarrow\quad
a.hashCode()=b.hashCode().
\]

역방향은 보장되지 않는다. 같은 hash 값에 서로 다른 객체가 대응할 수 있으므로 hash가 같다는 사실만으로 `equals()`가 참인 것은 아니다. `equals()`를 재정의할 때 이 계약을 맞추지 않으면 hash 기반 사용이 어긋날 수 있다. 자료의 `hashcode()` 표제와 달리 실제 식별자는 대문자 C를 가진 `hashCode()`다. 앞의 `Shoes` 페이지에는 그 구현이 없으므로 equality 예제를 완전한 hash 기반 사용 예제로 확장하지 않는다. [NM001 PDF p.24]

2026-1 기말 복기 1-(d)의 연결 지점도 이 **함의의 방향**이다. 한 실행에서 원하는 결과가 나왔는지가 아니라 내용상 같은 두 객체에 대해 계약이 유지되는지를 설명해야 한다. Collection의 내부 hash 알고리즘을 새로 가정할 필요는 없다. [EX:cp_2026_1_final_q01d p.1]

## `interface`: 구현이 지켜야 할 호출 약속

Interface(인터페이스)는 구현 class가 제공할 동작을 signature로 정하는 type 계약이다. Body 없는 abstract method(추상 메서드)는 입력과 반환 type을 선언하며, 이를 `implements`하는 구체 class는 필요한 구현을 제공해야 한다. 한 class가 직접 확장하는 class는 하나이지만 여러 interfaces를 구현할 수 있다. [NM001 PDF pp.26–32]

```java
interface MyInterface {
    void printNum(int i);
}

class MyClass implements MyInterface {
    public void printNum(int i) {
        System.out.println(i);
    }
}
```

위 선언 부분은 NM001 p.30의 예다. 하지만 그 아래에는 선언하지 않은 `myClass.func(123)` 호출이 있다. 그 호출을 그대로 성공 실행의 증거로 삼을 수 없다. 의도된 연결은 계약의 `printNum(int)`과 그 public 구현이며, `func` 누락을 몰래 새 method로 채우지 않는다.

Interface fields는 명시하지 않아도 `public static final`이며 초기값이 필요하다. `RamenCooker`의 `numSteps = 5`, `amountWater = 500`, `boilTime = 3`은 객체마다 setter로 바꿀 instance 상태가 아니라 공유 상수다. `void boilWater()`와 `boolean noodleFirst()`는 구현이 제공할 행동이다. [NM001 PDF pp.28–29]

`PizzaStore`는 `Pizza bakePizza()`와 `void deliver()`를 약속한다. `PizzaHut`와 `MrPizza` 구현은 cheese 또는 pepperoni를 추가하는 내부 단계, 배달 위치나 담당자를 찾는 단계를 다르게 구성한다. Caller는 이 세부 단계보다 반환 type과 호출 약속에 의존한다. 다만 NM001 p.31의 `bakePizza()`에는 필요한 `Pizza` 반환이 없고 helper 정의도 생략되어 있으므로 **불완전한 설계 sketch**다. 완성된 실행 코드로 재현하지 않는다.

2025-1 중간 복기 2번의 interface 설명 요구에는 “공통 계약을 정한다”와 “그 계약을 구체 class가 구현한다”를 함께 연결하면 된다. 단순히 “body가 없다”만 외우면 뒤의 `default`/`static` 사례를 설명하지 못한다. [EX:cp_2025_1_midterm_q02 p.1]

### `List<Integer>`의 공통 연산과 구현 교체

NM001 pp.33–35의 `List<E>`는 순서 있는 원소들을 다루는 공통 interface이고 `E`는 원소 type이다. `ArrayList`와 `LinkedList`는 이를 구현하는 예다. 자료의 다음 연산 순서는 interface를 통해 객체를 사용하는 의미를 보여 준다.

```java
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
```

세 번의 `add` 후 순서는 `[10,20,30]`이다. Zero-based index `2`의 `get` 결과는 `30`이며 목록은 그대로다. 여기서 `remove(1)`은 `int` index `1`인 원소 `20`을 제거하므로 `[10,30]`이 되고 `size()`는 `2`다. `Integer`는 primitive `int` 자체가 아니라 wrapper type이며 이 예는 숫자를 넣을 때의 boxing을 이용한다.

생성 부분을 `new LinkedList<>()`로 바꾸어도 이 공통 연산 열을 사용할 수 있다. 그렇다고 속도나 내부 저장 방식까지 같다는 뜻은 아니다. 자료의 `MyFavoriteList`, `MyOwnList`는 실제로 List 계약을 구현한 사용자 class가 있다는 가정의 이름이지 제공된 구현은 아니다. `set()`도 공통 연산으로 소개되지만 위 trace에서는 호출하지 않는다. Generic type 규칙과 collection 구현 내부는 후속 범위로 남는다.

## `Comparable<T>`: 어떤 속성으로 순서를 정할 것인가

동등성뿐 아니라 순서가 필요한 객체는 `Comparable<T>`의 `int compareTo(T obj)`를 구현할 수 있다. 결과의 **부호**가 핵심이다. 양수면 receiver가 더 큰 쪽, 음수면 인자가 더 큰 쪽, `0`이면 선택한 ordering(순서 관계)에서 동등한 위치다. 반드시 `1`, `-1`만 반환해야 하는 것은 아니다. [NM001 PDF pp.36–39]

`Seagull`에는 `flyingHeight`와 `numFriend`가 있지만 비교는 높이만 사용한다. `(10,1)`인 객체와 `(3,100)`인 객체를 비교하면 높이 `10 > 3`이어서 `1`이다. 친구 수는 결과를 바꾸지 않는다. 높이가 같으면 서로 다른 객체라도 `0`이므로 비교 결과의 “같음”을 모든 field의 equality나 identity로 확대할 수 없다. 이 예는 `equals()` override를 제공하지 않는다.

`equals()`는 Object에서 이어지는 동작이지만 모든 객체 종류에 유용한 전체 순서가 자연스럽게 있는 것은 아니다. 그러므로 비교 기준을 정할 때 `Comparable`을 선택적으로 구현한다. 이 구별이 NM001 p.46에서 두 계약을 나누는 이유다.

### String의 lexicographic comparison

Lexicographic comparison(사전식 비교)은 처음 다른 문자에서 순서를 정한다. NM001 pp.40–41의 제공된 구현 발췌는 두 길이의 최소값까지 같은 위치의 문자를 비교한다. 처음 다른 `c1`, `c2`를 만나면 `c1 - c2`, 그 범위가 모두 같으면 `len1 - len2`를 반환한다. 길이부터 비교하거나 모든 문자 코드의 합을 비교하는 알고리즘이 아니다.

| 자료의 비교 | 결정되는 지점 | 결과 |
|---|---|---|
| `"aaaaaa".compareTo("bbbbbb")` | 첫 `a - b` | `-1` |
| 반대 방향 | 첫 `b - a` | `1` |
| `"aaaaaa"`와 자기 자신 | 차이 없음, 길이 같음 | `0` |
| `"bbbbbb".compareTo("bccccc")` | 첫 `b` 다음의 `b - c` | `-1` |
| `"bbbbbb".compareTo("BBBBBB")` | 첫 `b - B` | `32` |

마지막 결과는 양수가 반드시 `1`이 아님을 직접 보여 준다. 한 문자열이 다른 문자열의 공통 prefix(접두사) 전체라면 길이 차이가 결정한다. 예를 들어 설명용으로 `"ab"`와 `"abc"`를 비교하면 공통 부분 이후 `2 - 3 = -1`이다. [NM001 PDF p.42]

자료의 ASCII 표현은 이런 영문 코드값 예에 관한 설명이다. 모든 문화권의 사전 정렬 규칙을 뜻하지 않는다. 또한 `char[] value`는 공급된 구현 발췌의 표현이며 모든 Java 버전의 실제 String 내부 저장 방식에 관한 현재성 주장이 아니다.

### 정렬 기준과 출력 표현은 다른 책임이다

NM001 pp.44–45의 또 다른 `Student` class는 `gpa` 차이의 부호를 `1`/`-1`/`0`으로 반환한다. 자료의 가상 수치 `3.3`, `4.2`, `3.1`을 목록에 추가한 뒤 `Collections.sort(sList)`를 부르면 `[3.1,3.3,4.2]` 순서가 된다. `add()`가 원소를 넣고 `sort()`는 이미 들어 있는 원소의 순서를 바꾼다. “sort로 저장한다”는 p.43의 문구를 원소 추가 동작으로 해석하지 않는다.

이 class의 `toString()`은 `Double.toString(gpa)`를 반환해 표시를 편하게 한다. **순서를 정하는 것은 `compareTo()`, 화면에 보일 표현을 정하는 것은 `toString()`**이다. 앞의 이름/id를 표현한 `Student`와는 별도 class 정의다. 이는 실제 학생 성적 자료가 아닌 instructor의 수치 예다.

주어진 subtraction 방식은 모든 `double`의 완전한 순서를 보장하는 예도 아니다. 코드 추론상 차이가 `NaN`이면 `diff > 0`, `diff < 0`가 모두 거짓이 되어 `0`을 반환할 수 있다. 이 경계는 source의 유한 값 예와 일반적인 수치 순서를 구별하기 위한 설명이다.

## Body를 제공하는 interface와 공통 상태를 가진 abstract class

### `default` body와 package default access

NM001 p.47은 Java 8부터 interface의 `default`/`static` methods에 body를 둘 수 있다고 설명한다. 따라서 앞쪽의 “interface method에는 body가 없다”는 문구는 기본 abstract-method 형태에 한정해야 한다. 자료의 예는 다음과 같다.

```java
interface RamenCooker {
    void boilWater();
    default void clean() {
        System.out.println("Rinsing with water");
    }
}
```

`boilWater()`는 구현이 필요하지만 `clean()`은 공통 body를 제공한다. Static method의 body는 interface 자체에 연결된 동작이라는 차이가 있다. 여기의 `default`는 실제 keyword로 구현을 제공하며, 접근 modifier를 생략해 같은 package에 공개하는 default access와는 별개다. 이후 Java 버전의 interface 기능 전체를 이 예로 확장하지 않는다.

### Abstract class의 상태·초기화·추상 행동

Abstract class(추상 클래스)는 공통 instance 상태와 구현을 두고 일부 동작을 abstract로 남길 수 있다. Abstract method를 선언한 class는 abstract여야 하고 그 abstract class를 직접 `new`로 만들 수 없다. 반대로 abstract class가 반드시 abstract method와 concrete method를 하나씩 가져야 하는 것은 아니다. [NM001 PDF pp.49–55]

자료의 `Person`에는 `description`, `name`, private `age`와 공통 `printName()`, `ageOneYear()`가 있다. `work()`와 `play()`는 자식이 구현한다. `Student`는 `Study hard`/`Drink hard`, `BusinessMan`은 `Meeting all day`/`Go to the movies`라는 서로 다른 행동 문자열을 제공한다. 공통 `ageOneYear()`는 예시 나이 `25 → 26`, `34 → 35`를 만들도록 의도되어 있다. 이는 가상 class 행동을 구분하기 위한 예이며 개인의 생활에 관한 사실이 아니다.

하지만 자식 constructors가 호출하는 `super(description,name,age)`에 대응하는 constructor가 p.50의 `Person`에는 없다. 따라서 이 페이지들은 그대로 합쳐 실행 가능한 완성 코드가 아니다. 의도된 상태 초기화와 출력 관계를 읽되 누락된 constructor를 원래부터 있었다고 채우지 않는다.

| 설계상 필요 | 자료가 제시하는 선택 | 이유 |
|---|---|---|
| 관련 없는 여러 종류에 같은 연산을 요구 | Interface | 공통 호출 계약을 제공한다. |
| 이미 다른 superclass가 있는 class에 계약 추가 | Interface | 여러 interfaces를 구현할 수 있다. |
| 관련 class의 instance fields·구현 공유 | Abstract class | 공통 상태와 동작을 둘 수 있다. |
| 공통 초기화 constructor·protected helper | Abstract class | 상태 관리 책임을 공유할 수 있다. |

NM001 p.56의 optional 구조는 `AbstractList<E> implements List<E>` 위에 `ArrayList<E> extends AbstractList<E>`를 놓는다. Interface는 계약을, abstract class는 공유 구현의 층을 제공한다. `ArrayList`가 더 이상 List 관계를 갖지 않는다는 뜻은 아니며 관계는 `AbstractList`를 통해 이어진다. 이 구조를 이해하는 데 collection 내부의 모든 method 구현까지 새로 가정할 필요는 없다.

## 핵심 정리

- Compiler는 선언 type과 signature를 검사하고, override된 instance body는 실제 receiver로 선택한다.
- `toString()`은 표현, `equals()`는 동등성, `compareTo()`는 선택한 순서를 담당한다. 세 결과의 뜻은 다르다.
- `equals()`가 참이면 같은 `hashCode()`가 필요하지만 그 역은 보장되지 않는다.
- Interface는 공통 호출 계약을, abstract class는 공유 instance 상태·초기화·구현을 제공할 수 있다.
- Null 인자와 null field, 가능한 난수 출력과 고정 출력, 자료 sketch와 완성 코드를 구별한다.

## 확인·연습문제

### Binding과 Object 계약

#### 확인 Q01 · Binding의 두 단계

`Parent parent=new Parent(); Parent child=new Child();`에서 print가 static일 때와 Child가 instance print를 override할 때를 비교하라. Compiler가 모르는 것은 선언 type인가?

<details><summary>해설 보기</summary>

`static`이면 둘 다 Parent.print, instance override이면 Parent.print 다음 Child.print다. 선언 type은 둘 다 Parent로 compiler가 알고 호출 가능한 signature를 검사한다. Runtime 선택에서 실제 receiver의 override가 달라진다. 자료 p.3의 'type을 모른다'를 선언 type 무지로 일반화하지 않는다. `private` method는 override 관계가 아니며 final method는 override할 수 없다. 이 언어 구별로 JVM 최적화나 물리 호출 비용까지 결정하지 않는다.

**확인 기준:** 두 출력 열과 compile/runtime 역할을 모두 설명한다.

</details>

#### 확인 Q02 · 배열 slot과 도형

`new Shape[4]` 직후, randShape로 채운 뒤, draw loop의 세 상태를 구별하라. 자료의 Circle/Square/Circle/Circle 순서는 항상 같은가?

<details><summary>해설 보기</summary>

처음에는 null reference slot 넷만 있어 실제 도형은 없다. 첫 loop가 `(int)(Math.random()*2)`의 선택에 따른 Circle/Square reference를 넣는다. 둘째 loop는 공통 Shape의 draw를 호출하지만 실제 객체에 따라 Circle.draw 또는 Square.draw가 실행된다. 채우기 전에 호출하면 받을 객체가 없다. 네 줄은 가능한 sample이며 배열 길이가 난수 순서를 고정하지 않는다. 이 예가 Lab04에 같은 상속 구조를 강제하지도 않는다.

**확인 기준:** 배열 생성과 객체 생성, 두 loop의 책임을 구별한다.

</details>

#### 확인 Q03 · 문자열 표현

MyClass.toString이 `"MyClass"`를 반환할 때 `"String = "+myClass`는 무엇인가? String/File 예와 Student format 예가 보여 주는 공통 역할도 설명하라.

<details><summary>해설 보기</summary>

`String = MyClass`라는 표현을 만든다. `public String toString()`은 String을 반환하며 객체의 실제 class를 String으로 cast하는 것이 아니다. Void print와도 다르다. String/File의 직접 출력과 toString 표현이 같다는 예는 표현 재사용을 보여 줄 뿐 파일을 열지 않는다. Student의 `%s %s (%d)` 형식은 이름·id를 한곳에서 형식화해 여러 출력 지점의 중복을 줄인다. 특정 개인명이나 경로를 외울 필요는 없다.

**확인 기준:** 반환·표현·객체 type 유지·format 재사용을 확인한다.

</details>

#### 확인 Q04 · Identity·내용·null

(a) 동일 fields의 별도 Shoes s1/s2와 `s3=s1`의 네 비교 및 검사 순서를 설명하라. (b) Null 인자와 null field는 어떻게 다른가? (c) 두 `new String("abc")` 및 primitive `equals`와 비교하라.

<details><summary>해설 보기</summary>

(a) `s1==s2`, `s1.equals(s2)`, `s1==s3`, `s1.equals(s3)`는 false,true,true,true다. Shoes는 identity 즉시 참→instanceof Shoes→cast→company/model의 equals와 size의 == 모두 검사→다른 type은 거짓 순서다. 

(b) Null 인자는 instanceof가 거짓이지만 별도 객체 비교에서 receiver의 company/model이 null이면 내부 equals 호출은 실패할 수 있다. 

(c) 두 new String("abc")도 별도 identity라 ==는 거짓, 내용 equals는 참이다. Object의 기본 equals는 identity이며 내용 비교는 override가 제공한다. Primitive 값에는 instance equals가 없고 wrapper와 구별한다.

**확인 기준:** 네 비교뿐 아니라 검사 순서와 두 null 경계를 설명한다.

</details>

#### 확인 Q05 · 출현 횟수와 hash 계약

원소가 `[null, s1, s2, null]`이고 s1/s2의 Shoes fields가 같고 non-null이라면 null과 s1의 frequency는 각각? Collection/Collections와 equals/hashCode 방향도 설명하라.

<details><summary>해설 보기</summary>

Null은 e==null인 둘을 세어 2, s1은 s1.equals(e)가 참인 s1/s2를 세어 2다. Null search receiver에는 equals를 부를 수 없어 branch를 나눈다. Collection은 interface, Collections는 이런 static utility class이며 `Collection<?>`는 여기서 특정 element type을 고정하지 않는 표기다. Equals 참이면 hashCode의 int 결과가 같아야 한다. 같은 hash라도 충돌 가능성 때문에 equals 참을 보장하지 않는다. Shoes 자료에는 hashCode 구현이 없어 완성된 hash 사용 예가 아니다. 식별자는 `hashCode()`다.

**확인 기준:** 2/2의 이유, null branch, 단방향 함의와 source 한계를 확인한다.

</details>

### Interface와 순서

#### 확인 Q06 · Interface의 계약과 sketch

RamenCooker 상수·추상 methods와 MyInterface/PizzaStore 구현이 지켜야 할 것을 설명하라. 자료가 완성 프로그램이 아닌 지점은?

<details><summary>해설 보기</summary>

Interface는 입력·반환 signature의 공통 계약이다. 구체 class는 필요한 abstract methods를 제공하고 하나의 class를 extends하면서 여러 interfaces를 implements할 수 있다. Fields는 초기값을 가진 public static final이라 numSteps=5, amountWater=500, boilTime=3은 객체별 설정 상태가 아니다. `boilWater()`/noodleFirst는 행동 계약이다. MyInterface의 printNum(int)는 public 구현과 연결되지만 p.30의 func(123)은 선언되어 있지 않다. PizzaStore는 bakePizza가 Pizza를 반환하고 deliver가 void인 형태를 유지해야 한다. 내부 조리·배달 단계는 달라도 되지만 자료 body의 반환문·helpers 누락 때문에 실행 완성본은 아니다. Body 금지는 기본 abstract-method 형태에만 한정한다.

**확인 기준:** 계약·상수·복수 interface·누락 호출/반환을 모두 확인한다.

</details>

#### 확인 Q07 · List 연산 추적

`List<Integer>`에 10,20,30을 add하고 get(2), remove(1), size()를 수행한다. 각 결과와 LinkedList로 교체할 때 유지되는 것·보장되지 않는 것은?

<details><summary>해설 보기</summary>

목록은 [10,20,30], get(2)는 30이며 목록 그대로다. `int` 인자 remove(1)은 index 1의 20을 제거해 [10,30], size는 2다. List<E>는 순서 있는 원소의 공통 계약이고 E는 원소 type이다. Integer는 wrapper이며 숫자 추가에 boxing이 쓰인다. LinkedList도 이 연산 계약을 제공하지만 성능·저장 방식이 같다는 뜻은 아니다. MyFavoriteList/MyOwnList는 실제 List 구현이 있어야 하는 가정 이름이다. `set()`은 갱신 연산으로 소개되었지만 이 trace에서 호출하지 않았다.

**확인 기준:** Index와 값, 조회와 변경, 계약과 구현을 구별한다.

</details>

#### 확인 Q08 · Comparable의 비교 기준

Seagull의 `(height,friends)=(10,1)`과 `(3,100)`을 비교하라. 같은 높이의 별도 두 객체는? compareTo 결과 0과 equals의 관계도 설명하라.

<details><summary>해설 보기</summary>

원본은 flyingHeight만 보므로 첫 비교는 1이다. Friends의 대소는 관계없다. 같은 높이는 0이지만 동일 객체나 모든 field의 equality를 뜻하지 않는다. `compareTo()`의 양수/음수/0은 선택한 순서에서 receiver가 큼/작음/동순위라는 뜻이며 반드시 ±1만 반환하지 않는다. `equals()`는 Object의 동작으로 모든 객체에 있지만 유용한 전체 순서는 모든 종류에 자연스럽지 않아 Comparable<T>를 선택한다. 이 Seagull은 equals override를 제공하지 않는다.

**확인 기준:** 선택 속성·부호·0의 한정·equals와의 구별을 확인한다.

</details>

#### 확인 Q09 · String 순서의 결정 위치

제공 알고리즘에서 `aaaaaa/bbbbbb`, 그 역, 자기 자신, `bbbbbb/bccccc`, `bbbbbb/BBBBBB`, `ab/abc`를 비교하라. 길이부터 정렬하는가?

<details><summary>해설 보기</summary>

결과는 -1,1,0,-1,32,-1이다. 최소 길이까지 같은 위치를 비교해 처음 다른 문자 코드의 차이를 반환한다. `bbbbbb`/`bccccc`는 둘째 b-c=-1, 소문자/대문자는 첫 b-B=32다. `ab`/`abc`는 공통 prefix가 모두 같아 길이 2-3=-1로 결정된다. 길이 우선이나 전체 코드 합 비교가 아니다. 양수 32도 유효하다. 이는 공급된 char[] 구현 발췌와 영문 코드값 예이며 현행 모든 JDK 저장 방식이나 문화권 사전 순서를 뜻하지 않는다.

**확인 기준:** 처음 다른 위치와 prefix 경계, 32의 의미를 설명한다.

</details>

#### 확인 Q10 · 정렬과 표시

가상 GPA 3.3,4.2,3.1의 Student 목록에서 add·sort·compareTo·toString의 책임을 구분하라. 원본의 차이 기반 compareTo는 NaN에도 완전한가?

<details><summary>해설 보기</summary>

`add()`는 삽입하고 Collections.sort는 compareTo의 GPA 순서를 이용해 [3.1,3.3,4.2]로 재배치한다. `toString()`은 Double.toString(gpa)로 표시만 맡는다. Sort가 원소를 추가하거나 toString이 정렬 기준을 정하지 않는다. 이 Student는 앞의 이름/id 예와 별도 정의다. `diff`가 NaN이면 >0과 <0이 모두 거짓이어서 0을 반환할 수 있으므로 일반 유한 수치 예를 모든 double의 완전한 순서로 확대하지 않는다.

**확인 기준:** 네 책임과 NaN의 두 거짓 비교를 확인한다.

</details>

### 공통 구현과 상태

#### 확인 Q11 · Interface body와 default

`boilWater()`는 body가 없지만 `default clean()`은 있다. 구현 class의 의무와 static body의 소속, package-default와의 차이를 설명하라.

<details><summary>해설 보기</summary>

`boilWater()`의 abstract 계약은 구체 구현이 제공해야 한다. `default clean()`은 공통 body로 Rinsing with water를 출력한다. `static` body는 interface 자체에 연결된다. 자료는 Java 8부터 default/static body를 허용하므로 앞의 'body가 없다'는 기본형의 요약으로만 읽는다. 여기서는 실제 default keyword로 body를 제공하며 modifier 생략의 package access와 다른 의미다. 이후 버전의 모든 기능·충돌 규칙을 배웠다는 뜻은 아니다.

**확인 기준:** Abstract 의무·default 공통 body·static 소속·접근 용어 차이를 확인한다.

</details>

#### 확인 Q12 · 공통 상태와 abstract class

(a) Person과 두 자식의 공통·개별 책임 및 의도된 나이·행동을 설명하라. (b) Constructor 누락과 abstract class의 생성·method 조건은? (c) Interface와 abstract class의 선택 기준 및 AbstractList→ArrayList의 List 관계는?

<details><summary>해설 보기</summary>

(a) Person은 description/name/private age와 printName/ageOneYear를 공유하고 자식은 work/play를 구현한다. 초기화가 갖춰졌다는 의도에서 25→26,34→35이고 Student는 Study hard/Drink hard, BusinessMan은 Meeting all day/Go to the movies다. 

(b) 그러나 super(description,name,age)에 맞는 Person constructor가 없어 그대로의 실행 증거는 아니다. Abstract method가 있으면 class도 abstract여야 하고 직접 new할 수 없지만 abstract/concrete method를 꼭 하나씩 가져야 하지는 않는다. 

(c) 관련 class의 상태·constructor·protected helpers 공유에는 abstract class, 관련 없는 종류의 공통 연산이나 기존 superclass에 추가할 계약에는 interface가 맞다. AbstractList implements List, ArrayList extends AbstractList이므로 List 관계가 이어진다.

**확인 기준:** 의도된 동작과 누락 constructor를 분리하고 설계 기준과 계약 연결을 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 같은 객체의 세 선택

새로 만든 기출 연결 연습이다. [EX:cp_2026_1_final_q02 p.2]에서 field/static/instance를 따로 분류하는 요구를 가져왔다. 선수는 Inheritance의 hiding·cast와 Q01이다. 부모 `Meter`에 field `value=4`, static `kind()`→`"base"`, instance `read()`→부모 value가 있고, `FastMeter`는 별도 `value=9`, static kind→`"fast"`, read override→`super.value+value`를 둔다. `Meter a=new FastMeter(); Meter b=a;`에서 `a.value=6` 후 b.value, b.kind(), b.read()와 FastMeter field의 값은?

<details><summary>해설 보기</summary>

`6,"base",15,9`다. A와 b는 같은 객체의 aliases이며 a.value 대입은 선언 type Meter의 field를 6으로 바꾼다. B도 그 field를 읽고 static kind는 Meter를 고른다. Read만 실제 FastMeter override를 실행해 부모 6+자식 9=15다. 대입은 자식 field를 바꾸지 않는다. Alias와 상태 변경을 함께 추적하므로 원문 상수 치환만 한 문제가 아니다.

**확인 기준:** 동일 객체·서로 다른 fields·static type·instance override 네 근거를 적는다.

</details>

#### 연습 P02 · Hash 관찰과 보장

새로 만든 기출 연결 연습이다. [EX:cp_2026_1_final_q01d p.1]의 equals→hashCode 함의 판단을 두 관찰의 비교로 옮겼다. 선수는 Q04–Q05이며 hash 내부 알고리즘은 필요 없다. 실험 A는 equals가 참인 두 객체의 hash가 12와 15였다. 실험 B는 hash가 둘 다 12였으나 equals는 거짓이었다. 어느 것이 계약 위반이며 단 한 번 일치한 관찰로 구현 전체를 보증할 수 있는가?

<details><summary>해설 보기</summary>

A는 같은 객체 값에 같은 hash가 필요하다는 방향을 위반한다. B는 서로 다른 값의 hash 충돌이 허용되어 그 사실만으로 위반이 아니다. 한 번 맞은 결과는 모든 equals-true 쌍에 대한 계약을 증명하지 못한다. 어떤 hash 함수나 실제 집합 출력도 추가로 가정할 필요가 없다.

**확인 기준:** 필요조건의 방향과 관찰/일반 보장을 구별한다.

</details>

#### 연습 P03 · 공통 동작과 공통 상태

새로 만든 기출 연결 연습이다. [EX:cp_2025_1_midterm_q02 p.1]의 interface 개념 설명을 설계 선택으로 확장했다. 선수는 Q06·Q11·Q12로 모두 현재 범위다. 서로 관련 없는 두 class는 이미 각기 다른 부모를 extends하지만 같은 출력 동작을 제공해야 한다. 별도의 관련 class 가족은 공통 instance 상태와 초기화도 공유해야 한다. 두 필요에 어떤 수단을 제안하고, 'interface에는 body가 전혀 없다'는 설명을 어떻게 고칠 것인가?

<details><summary>해설 보기</summary>

첫 경우에는 공통 interface 계약을 implements하게 하여 기존 class 상속과 병행한다. 둘째는 abstract class에 상태·constructor·공통 구현을 모으고 필요한 행동을 abstract로 남기는 설계가 적합하다. Interface의 기본 abstract methods에는 body가 없지만 자료가 설명하는 default/static methods에는 body가 있다. 공통 signature만으로 자료의 누락 constructor나 return이 완성되지는 않는다.

**확인 기준:** 각 선택을 필요와 연결하고 body 없는 기본형의 한정을 명시한다.

</details>

### 짧은 복습 계획

Q04·Q05로 identity·equality·hash의 함의를 먼저 확인하고 Q08–Q10의 순서와 표현을 비교한다. 다음 날 P01을 trace하고 P03에서 설계 이유를 문장으로 설명한다.

## 출처

Inheritance 2와 필요한 Inheritance 1의 자료 기반 복습이다. `printNum`/`func` 불일치, Pizza 반환·helper 누락, Person constructor 누락은 완성 코드로 바꾸지 않는다. Shoes의 null field·hashCode 한계, String 구현 버전과 가상 GPA/NaN 한정을 유지한다. Interface의 default/static body를 포함하되 generic·collection 내부 전체를 다룬 것은 아니다.

### 자료와 해당 페이지

- [7 inheritance 2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-009), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-024), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-053), [p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-054), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056)

- [6 inheritance 1 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-034), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-039), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-047)

### 기출 연결의 범위

역사적 복기본이며 공식 원본·정답 확인이나 이번 학기 출제 예고가 아니다. 제공된 공식 답안은 없고 새 연습의 해설은 위 추론으로 확인한다. 기말 복기의 순서·정확성 한계와 누락 문항은 그대로 남긴다.

- [EX:cp_2026_1_final_q02 p.2] · [[exam_questions/cp_2026_1_final_q02|공개된 문항 미리보기]]

- [EX:cp_2026_1_final_q01d p.1]

- [EX:cp_2025_1_midterm_q02 p.1]
