---
title: "동적 Binding·Object 계약·Interface와 Abstract Class"
description: "Object의 동등성·순서 계약과 interface·abstract class의 역할을 코드와 설계로 확인한다."
course: "computer_programming"
unit_id: "object-contracts-interfaces"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["7 inheritance 2.pdf", "6 inheritance 1.pdf", "8 polymorphism.pdf", "Lab 6 Polymorphism.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/2026-09-10-lecture-04", "courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

## Binding과 Object의 공통 계약

### Declared type과 receiver가 정하는 서로 다른 선택

같은 종류의 연산을 여러 객체에 적용하려면 호출자가 아는 약속과 객체가 제공하는 구현을 분리해야 한다. Reference(참조) 변수는 객체를 가리키는 값을 보관한다. `Parent child = new Child();`에서 declared type(선언 타입)은 `Parent`, 실제 객체의 class는 `Child`다. 대입은 객체를 새 `Parent`로 복사하지 않는다. 선수자료인 Inheritance 1의 `Child extends Parent` 관계를 사용하되, 상속이 부모의 private 상태까지 자식 코드에서 직접 읽게 한다는 뜻은 아니다. [computer_programming:RM001, PDF pp.20-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

Binding(바인딩)은 method 호출을 어떤 동작에 연결하는지 설명한다. NM001의 다음 두 정의는 독립된 비교 예다. 먼저 static method(정적 메서드)를 둔다.

~~~text
class Parent {
    static void print() {
        System.out.println("Parent.print()");
    }
}
class Child extends Parent {
    static void print() {
        System.out.println("Child.print()");
    }
}

Parent parent = new Parent();
Parent child = new Child();
parent.print();
child.print();
~~~

두 표현식의 declared type이 모두 `Parent`이므로 결과는 차례로 `Parent.print()`, `Parent.print()`다. `Child.print`는 부모의 static method를 hide한다. 실제 객체가 `Child`라고 해서 그쪽 static body를 고르지 않는다. `Parent.print()`처럼 class 이름으로 호출하면 class 소속이라는 의미가 더 분명하다. [computer_programming:NM001, PDF pp.4-5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

이번에는 두 method에서 `static`을 제거하고, 자식의 같은 `void print()` 선언에 `@Override`를 붙인다. `parent.print()`는 `Parent.print()`, `child.print()`는 `Child.print()`를 출력하는 body에 연결된다. Compiler(컴파일러)는 `Parent`에서 `print()` 호출이 가능한지 검사한다. 그 계약 안에서 실제 receiver(호출을 받는 객체)의 override body를 고르는 것이 dynamic dispatch(동적 디스패치)다. `private` method는 상속되어 override되는 대상이 아니고 `final` method도 override할 수 없다. Static hiding과 instance overriding은 이 기준부터 다르다. [computer_programming:NM001, PDF pp.3-7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

NM001 p.3은 “Types of variables are unknown during the compilation.”이라고 쓰지만, 이를 compiler가 declared type을 모른다는 뜻으로 받아들이면 틀린다. 실제 receiver의 class에 따라 구현이 달라질 수 있다는 의미로 한정해야 한다. 날짜 미확인 녹취 NT001 00:48도 binding을 회고한다. 위 두 출력의 정확한 비교는 NM001의 자료 예다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 00:48]]

### Shape 배열: 공통 호출과 개별 구현

`Shape`가 `draw()`를 제공하고 `Circle`, `Square`가 이를 override하면 호출자는 개별 종류를 검사하지 않고 도형을 그리도록 요청할 수 있다. 자료의 `Shape.randShape()`는 `(int)(Math.random() * 2)`가 0이면 `new Circle()`, 1이면 `new Square()`를 반환한다. 반환 type은 `Shape`지만 실제 객체는 두 subtype 중 하나다. [computer_programming:NM001, PDF pp.8-9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

~~~text
Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();
~~~

첫 줄은 reference slot 네 개를 만들며 처음 값은 모두 `null`이다. 도형 네 개를 이미 만든 것이 아니다. 첫 loop가 index 0부터 3까지 실제 도형의 reference를 저장한다. 두 번째 loop는 같은 `shapes[i].draw()`를 반복하지만 실제 객체가 `Circle`이면 `Circle.draw()`, `Square`이면 `Square.draw()` body를 사용한다.

자료의 `Circle.draw(), Square.draw(), Circle.draw(), Circle.draw()`는 가능한 네 줄의 한 예다. 난수 순서를 고정한 약속이 아니다. 첫 loop를 생략하고 `null` slot에 instance method를 호출하면 receiver가 없어 `NullPointerException`이 발생한다. 공통 원소 type, 실제 객체, slot을 채우는 단계는 각각 구별해야 한다.

### toString: 출력 형식의 책임을 객체에 두기

Object의 `public String toString()`은 객체를 설명하는 문자열 표현을 반환한다. 호출자가 출력할 때마다 fields를 따로 조합하면 형식을 바꿀 곳이 여러 군데 생긴다. 객체에 표현 책임을 두면 같은 객체를 사용하는 여러 호출자가 그 표현을 공유할 수 있다. NT001 날짜 미확인 00:48, 01:48의 설명도 이 동기에 해당한다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 00:48,01:48]]

NM001의 `MyClass`는 다음처럼 표현을 정한다.

~~~text
class MyClass {
    @Override
    public String toString() {
        return "MyClass";
    }
}
MyClass myClass = new MyClass();
System.out.println("String = " + myClass);
~~~

연결 결과는 `String = MyClass`다. 원래 객체의 class가 `String`으로 바뀌는 것은 아니다. P.14의 “casts the object to the String class”는 reference cast라는 정확한 설명이 아니며, 여기서는 문자열 표현을 얻어 연결한다. `toString`의 String 반환과 `println`의 출력도 다르다. `void`로 출력만 하는 method는 이 반환 계약을 대신하지 못한다. [computer_programming:NM001, PDF pp.12-14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

P.13의 String 예에서는 객체 표현과 `cp.toString()`의 내용이 같고, File 예에서도 객체 표현과 `file.toString()`은 같은 경로 표현이다. 파일 내용을 읽었다는 예가 아니다. 별도 Student 예는 이름 fields와 `id`를 `String.format("%s %s (%d)", fName, lName, id)`로 표현한다. `%s` 두 자리와 `%d` 한 자리를 한곳에서 관리하므로 호출자는 매번 이름과 괄호를 직접 연결하지 않아도 된다. 이 Student는 뒤의 GPA 비교용 Student와 별개 정의다. 문자열 표현이 같다는 것만으로 `equals`도 같다고 결론낼 수는 없다. [computer_programming:NM001, PDF pp.13-16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### equals: identity와 content equality

Reference의 `==`는 identity(동일성), 즉 같은 객체를 가리키는지를 비교한다. Object의 기본 `equals`도 이 의미다. 내용상 같은 값으로 다루려면 class가 의미 있는 fields를 정해 content equality(내용 동등성)를 구현해야 한다. NT001 날짜 미확인 01:48은 reference 대신 내용을 비교하려는 목적을 강조한다. 물리 주소의 수치를 직접 드러내 비교한다는 뜻으로 넓히지 않는다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:48]]

`new String("abc")`를 두 번 사용하면 별개 두 객체이므로 reference `==`는 false지만 String의 `equals`는 true다. String이 문자 내용 비교를 이미 제공하기 때문이다. Primitive 값 자체에는 instance `equals`가 없다. NM001 p.17의 primitive에서도 두 방식이 같다는 문구는 primitive와 wrapper를 혼동하지 않도록 바로잡아 읽어야 한다. [computer_programming:NM001, PDF pp.17-18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

자료의 Shoes는 `String company, model`과 `int size`를 보관한다. 해당 `equals` body는 다음과 같다.

~~~text
public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Shoes) {
        Shoes shoes = (Shoes) o;
        return this.company.equals(shoes.company)
            && this.model.equals(shoes.model)
            && this.size == shoes.size;
    }
    return false;
}
~~~

같은 객체라면 즉시 true다. 그 외에는 `instanceof Shoes`로 type을 확인한 뒤 cast하여 String 두 개는 내용으로, primitive `size`는 값으로 비교한다. `&&`이므로 세 조건이 모두 true여야 한다. Type 검사 전에 무조건 cast하면 다른 class의 객체를 비교할 때 실패할 수 있다. [computer_programming:NM001, PDF pp.19-20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

~~~text
Shoes s1 = new Shoes("Nice", "AirMax", 265);
Shoes s2 = new Shoes("Nice", "AirMax", 265);
Shoes s3 = s1;
~~~

| 비교 | 결과 | 이유 |
| --- | --- | --- |
| `s1 == s2` | false | 별개 객체 |
| `s1.equals(s2)` | true | 세 fields가 같은 내용 |
| `s1 == s3` | true | 같은 객체의 alias |
| `s1.equals(s3)` | true | 첫 identity 검사에서 참 |

[computer_programming:NM001, PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

`s1.equals(null)`은 `null instanceof Shoes`가 false여서 false다. 그러나 `s1.company`가 null이면 다른 객체와 비교하는 경로의 `this.company.equals(...)`가 안전하지 않다. Null인 인자와 null인 내부 field는 다른 경계다. 자기 자신 비교는 첫 줄에서 끝날 수 있으므로 같은 코드라도 어떤 경로를 거치는지 봐야 한다.

동등성은 non-null 객체에서 자기 자신과 같아야 하고(reflexivity), 비교 방향을 바꿔도 결과가 같아야 하며(symmetry), a=b와 b=c이면 a=c여야 한다(transitivity). 비교 정보가 바뀌지 않으면 결과도 일관되어야 하고, non-null receiver의 `equals(null)`은 false여야 한다. 이는 내용을 비교한다는 설명을 일관된 관계로 적용하기 위한 조건이다.

별도 자료 Point2D는 `instanceof Point2D` 뒤 두 double 좌표를 각각 `==`로 비교한다. 유한 좌표 (2.0, 3.0)가 같은 별개 객체는 이 `equals`에서 true, reference `==`에서는 false다. 좌표가 하나 다르거나 인자가 null이면 false다. 다만 NaN 좌표는 자기 자신과도 `==`가 false이므로 이 구현을 모든 double 값에 대한 동등성으로 일반화할 수 없다. `toString`이 만드는 `(2.0,3.0)` 표현도 비교 기준과는 별개다. [computer_programming:NM004, PDF p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

### Collection에서 동등성을 쓰는 방식과 hashCode

`Collection`은 interface이고 `Collections`는 collection을 다루는 static utility class다. NM001 p.22의 두 이름은 구별해서 읽는다. 다음은 p.23의 frequency가 찾는 값 `o`의 출현 횟수를 세는 전체 구조다.

~~~text
public static int frequency(Collection<?> c, Object o) {
    int result = 0;
    if (o == null) {
        for (Object e : c)
            if (e == null)
                result++;
    } else {
        for (Object e : c)
            if (o.equals(e))
                result++;
    }
    return result;
}
~~~

Null인 `o`에는 `equals`를 호출할 수 없어 `e == null`을 직접 센다. Non-null이면 `o.equals(e)`의 의미를 사용한다. 앞 Shoes들의 non-null fields를 유지하고 collection에 `s1, s2, null`이 있다고 가정하면, `s1`을 찾을 때 2, null을 찾을 때 1이다. 서로 다른 신발 객체도 내용 동등성이 true이면 같은 값의 출현이다. `Collection<?>`는 원소 type을 여기서 특정 이름으로 고정하지 않는 표기 정도로 읽으며, 아무 값이나 안전하게 추가할 수 있다는 뜻은 아니다. [computer_programming:NM001, PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

`hashCode()`는 int를 반환한다. 실제 철자는 대문자 C를 쓴 `hashCode`이며 자료의 `hashcode`와 구별한다. `a.equals(b)`가 true이면 두 객체의 hash code는 같아야 한다. 반대 방향은 성립하지 않는다. 같은 hash code를 갖는 서로 다른 값의 collision(충돌)이 가능하다. 비교 정보가 바뀌지 않는 동안 hash 값의 일관성도 필요하다.

내용상 같은 객체들을 서로 다른 hash로 분류하면 hash 기반 저장·검색이 의존하는 계약과 어긋난다. 따라서 내용 `equals`를 정의할 때 `hashCode`도 그 기준과 맞춰야 한다. Shoes와 Point2D 자료는 hashCode 구현을 보여 주지 않으므로 전체 hash 계약을 완성한 구현으로 볼 수 없다. 모든 Object method를 다시 구현해야 한다는 뜻도 아니다. [computer_programming:NM001, PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

이 구별을 적용할 때는 “한 번의 조회에서 true가 나왔다”와 “동등한 값을 항상 같은 기준으로 찾도록 계약이 맞는다”를 분리해야 한다. 비공식 복기 문항과의 연결도 이 보장 여부를 설명하는 사고 과정에 한정된다. HashSet의 내부 알고리즘이나 복기 원문 구현을 여기서 새로 완성할 필요는 없다. [EX:cp_2026_1_final_q01d p.1] [EX:cp_2026_1_final_q03 p.3]

### Interface: 구현을 몰라도 사용할 수 있는 계약

Interface(인터페이스)는 어떤 연산을 제공하는지 정하는 type 계약이다. Abstract method(추상 메서드)는 body 없이 method 이름, parameter types, return type을 선언한다. 구체 class는 `implements`로 계약을 받아들이고 남아 있는 abstract methods를 만족해야 한다. 이미 상속한 적절한 구현을 사용할 수도 있으며, abstract class는 일부 의무를 다음 subclass에 남길 수 있다.

Class는 하나의 superclass를 `extends`하면서 여러 interfaces를 `implements`할 수 있다. Interface는 다른 interfaces를 확장할 수 있다. 호출자가 공개 계약만 알고 내부 구현을 몰라도 쓸 수 있다는 점에서 encapsulation과 연결된다. NT001 날짜 미확인 02:48-04:25의 설명이 이 동기다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 02:48,03:33,04:25]]

자료의 RamenCooker 선언은 상수와 연산을 함께 보여 준다.

~~~text
interface RamenCooker {
    int numSteps = 5;
    int amountWater = 500;
    int boilTime = 3;
    public void boilWater();
    public boolean noodleFirst();
}
~~~

Interface fields는 modifier를 생략해도 `public static final`이다. 값 5, 500, 3은 객체마다 바꾸는 instance 상태가 아니라 초기화된 상수다. 초기값을 생략하거나 이 성격과 충돌하는 modifier를 붙일 수 없다. `boilWater`는 반환값 없는 행동을, `noodleFirst`는 boolean 결과를 요구하지만 선언만으로 조리 방식까지 정하지 않는다. [computer_programming:NM001, PDF pp.26-29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

`MyInterface`의 `void printNum(int i);`를 구현하는 class는 `public void printNum(int i)`를 제공한다. P.30에는 아래쪽 호출이 `myClass.func(123);`로 인쇄되어 있어 선언된 method와 맞지 않는다. 의도된 연결을 확인하는 학습용 수정 호출 `myClass.printNum(123);`라면 123을 출력한다. 이 수정과 인쇄 원문은 구별한다. [computer_programming:NM001, PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

PizzaStore의 약속은 `Pizza bakePizza()`와 `void deliver()`다. PizzaHut는 cheese 추가와 배달 위치 찾기, MrPizza는 pepperoni 추가와 배달원 찾기로 내부 전략을 달리한다. 호출자는 공통 signature와 반환 계약을 사용한다. 특히 `bakePizza`는 Pizza를 반환해야 한다. 원자료에는 반환문과 helper 정의가 빠져 있어 설계 sketch이지 완성 프로그램이 아니다. [computer_programming:NM001, PDF pp.31-32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Interface를 설명할 때는 “구현이 다르다”에서 멈추지 말고, 호출자가 어떤 입력을 주며 어떤 반환값과 동작을 기대하는지까지 연결해야 한다. 비공식 복기본의 interface 개념 문항과 연결되는 요구도 이 부분이다. [EX:cp_2025_1_midterm_q02 p.1]

### List: 연산 계약을 유지하면서 구현 바꾸기

`List<E>`는 순서 있는 원소들을 다루는 interface다. E는 원소 type의 자리이며 ArrayList, LinkedList는 구현 예다. 다음은 NM001의 연산 순서다.

~~~text
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
~~~

세 `add` 뒤 목록은 [10, 20, 30]이다. Index는 0부터 시작하므로 `get(2)`는 30을 반환하고 목록을 바꾸지 않는다. `remove(1)`은 이 호출에서 int index 1의 원소 20을 제거한다. 목록은 [10, 30], `size()`는 2다. 값 1을 찾아 제거하는 호출과 혼동하지 않는다. `set`은 특정 위치의 원소를 갱신하는 별도 연산이며 이 trace에서는 호출되지 않았다.

Integer는 primitive int가 아닌 wrapper class다. 이 예의 `add(10)`은 boxing을 통해 Integer 원소를 사용한다. `List<Integer>`가 `List<int>`라는 뜻은 아니다. 생성 부분을 `new LinkedList<>()`로 바꾸어도 같은 연산을 지원하는 List 계약을 통해 이 연산 열의 의미를 유지할 수 있다. 내부 저장 방식과 속도까지 같다는 뜻은 아니다. 자료의 MyFavoriteList, MyOwnList는 List를 실제로 구현한 사용자 class가 있다는 가정의 이름이며 해당 class bodies는 제공되지 않았다. [computer_programming:NM001, PDF pp.33-35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### Comparable: 선택한 속성으로 순서 정하기

동등성은 모든 객체에 기본 의미가 있지만 유용한 순서가 모든 종류에 자연스럽게 있는 것은 아니다. `Comparable<T>`는 순서가 필요한 class가 선택하는 interface다. `int compareTo(T obj)`의 반환 부호가 순서를 나타낸다. 양수면 receiver가 더 큰 쪽, 음수면 인자가 더 큰 쪽, 0이면 선택한 ordering에서 같은 위치다. 반환값은 반드시 1 또는 -1일 필요가 없다. NT001 날짜 미확인 05:25-07:23은 Object의 equals와 선택적인 순서 계약을 비교한다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 05:25,06:23,07:23]]

NM001의 `Seagull implements Comparable<Seagull>`은 `flyingHeight`, `numFriend`를 보관하지만 비교에는 높이만 쓴다.

~~~text
public int compareTo(Seagull seagull) {
    if (this.flyingHeight > seagull.flyingHeight)
        return 1;
    else if (this.flyingHeight == seagull.flyingHeight)
        return 0;
    else
        return -1;
}
~~~

높이/친구 수가 (10, 1)과 (3, 100)이면 첫 객체의 `compareTo`는 1이다. 친구 수는 이 순서에 영향을 주지 않는다. 같은 높이의 별개 객체들은 0을 얻을 수 있지만 identity나 모든 fields, equals까지 같다는 뜻은 아니다. 이 예에는 equals override도 없다. Comparable을 구현해도 다른 superclass 상속이나 다른 interface 구현을 함께 할 수 있지만, 모든 collection의 요구를 자동으로 충족한다는 보장으로 넓히지는 않는다. [computer_programming:NM001, PDF pp.36-39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [computer_programming:NM001, PDF p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

### String의 lexicographic comparison

Lexicographic comparison(사전식 비교)은 처음 다른 문자에서 순서를 결정한다. 자료의 String 구현 발췌는 두 길이의 최소값 `lim`까지 같은 index의 문자를 비교하고 첫 차이 `c1 - c2`를 반환한다. 공통 범위가 모두 같으면 `len1 - len2`를 반환한다. 전체 문자 코드의 합이나 길이부터 비교하는 방식이 아니다. [computer_programming:NM001, PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

| 비교 | 결정 위치 | 반환값 |
| --- | --- | --- |
| `"aaaaaa".compareTo("bbbbbb")` | 첫 a와 b | -1 |
| `"bbbbbb".compareTo("aaaaaa")` | 첫 b와 a | 1 |
| `"aaaaaa".compareTo("aaaaaa")` | 차이 없음, 길이도 같음 | 0 |
| `"bbbbbb".compareTo("bccccc")` | 두 번째 b와 c | -1 |
| `"bbbbbb".compareTo("BBBBBB")` | 첫 b와 B | 32 |

[computer_programming:NM001, PDF p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

마지막 결과가 32여도 양수라는 점이 순서를 나타낸다. 한 문자열이 다른 문자열의 전체 prefix이면 처음 다른 문자가 없으므로 짧은 쪽이 길이 차이로 먼저 온다. 예를 들어 학습용 `"ab"`와 `"abcd"`는 공통 두 글자가 같아 2-4=-2다. 자료의 ASCII 언급은 이런 영문 코드 예의 비교에 맞으며 문화권별 사전 정렬 전체가 아니다. `char[] value`도 공급된 구현 발췌의 표현으로 읽으며 모든 Java 버전의 String 저장 형태라고 단정하지 않는다.

### GPA 정렬: 비교 기준과 표시 형식 분리하기

NM001의 또 다른 Student는 GPA를 보관하고 Comparable을 구현한다. 앞의 이름/id Student와 독립된 정의다.

~~~text
class Student implements Comparable<Student> {
    double gpa;
    Student(double gpa) { this.gpa = gpa; }

    public int compareTo(Student anotherStudent) {
        double diff = gpa - anotherStudent.gpa;
        return diff > 0 ? 1 : diff < 0 ? -1 : 0;
    }

    @Override
    public String toString() {
        return Double.toString(gpa);
    }
}
~~~

목록에 3.3, 4.2, 3.1을 차례로 넣으면 처음 순서는 [3.3, 4.2, 3.1]이다. `Collections.sort(sList)`는 compareTo가 정한 순서에 따라 [3.1, 3.3, 4.2]로 재배치한다. `add`는 저장할 원소를 추가하고 sort는 이미 있는 원소들의 순서를 바꾼다. `toString`은 각 GPA를 읽을 수 있는 문자열로 표시할 뿐 순서를 결정하지 않는다. [computer_programming:NM001, PDF pp.43-45](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

이 subtraction 방식은 주어진 유한 값에 맞춰 읽어야 한다. Diff가 NaN이면 `diff > 0`과 `diff < 0`이 모두 false여서 0을 돌려줄 수 있다. 따라서 모든 double 값을 완전하게 정렬하는 범용 구현으로 일반화할 수 없다. 이 한정은 자료 코드의 조건을 분석한 설명이다.

### Interface의 default/static body

Interface를 body 없는 abstract methods로 처음 소개해도 그것이 모든 method의 절대 규칙은 아니다. NM001 p.47은 Java 8부터 default/static methods에 body를 허용한다고 명시한다.

~~~text
interface RamenCooker {
    void boilWater();
    default void clean() {
        System.out.println("Rinsing with water");
    }
}
~~~

`boilWater`는 여전히 구현해야 할 abstract 동작이고 `clean`은 구현 class가 사용할 공통 instance body다. Static method는 interface 자체에 속한 동작이며 receiver별 override를 고르는 instance 호출과 다르다. 여기의 `default`는 body를 제공하는 keyword다. Access modifier를 생략하여 같은 package에만 접근을 허용하는 package access와 다른 용법이다. [computer_programming:NM001, PDF p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

앞선 자료 pp.26-27, 54와 NT001 날짜 미확인 08:22, 14:45의 “body가 없다”는 일반화에는 이 예외가 필요하다. 녹취의 표현을 고친 인용으로 만들지 않고, 같은 자료 p.47의 명시된 조건을 적용한다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 08:22,14:45]]

### Abstract class: 공통 상태와 의미 있는 빈칸

Abstract class(추상 클래스)는 공통 instance 상태와 구현을 공유하면서 일부 동작을 abstract로 남길 수 있다. Abstract method를 선언하면 class도 abstract여야 하며 직접 `new Person()`처럼 생성할 수 없다. 반대로 abstract class가 반드시 abstract method와 concrete method를 각각 하나씩 가져야 한다는 뜻은 아니다. [computer_programming:NM001, PDF p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Person 자료에는 package access인 `description`, `name`, private인 `age`가 있다. `printName`과 `ageOneYear`는 공통 구현이고 `work`, `play`는 다음처럼 남긴다.

~~~text
abstract void work();
abstract void play();
~~~

NT001 날짜 미확인 10:13의 이유는 어떤 Person인지 모르는 상황에서 임의의 work/play body를 만들지 않으려는 것이다. Student와 BusinessMan은 공통 fields와 동작을 재사용하면서 자기 행동을 정한다. Private age는 자식이 직접 접근하는 대신 Person의 공통 method가 다룬다. `description`, `name`도 modifier가 없으므로 public이 아니다. [computer_programming:NM001, PDF pp.50-52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 09:13,10:13,13:48]]

| 종류 | work | play | ageOneYear의 의도된 변화 |
| --- | --- | --- | --- |
| Student | `Study hard` | `Drink hard` | 25 → 26 |
| BusinessMan | `Meeting all day` | `Go to the movies` | 34 → 35 |

이것은 자료의 가상 class 행동과 상태 예다. Pp.51-52는 `super(description, name, age)`를 호출하지만 p.50에는 그 세 인자 Person constructor가 없다. 따라서 표는 필요한 초기화가 갖춰졌다는 의도 아래의 trace이며, 페이지 전체가 그대로 완성 프로그램이라는 뜻은 아니다. `non-field field`라는 원본 주석도 새로운 Java field 종류를 정의하지 않는다. [computer_programming:NM001, PDF pp.50-53](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

Work/play에 concrete 기본 body를 넣고 abstract 제한을 없애면 일반 class 설계도 가능하다. 그 경우 자식은 기본 행동을 그대로 물려받을 수 있다. Abstract로 남기면 직접 생성하지 못하게 하고 구체 class가 해당 동작을 제공하도록 설계의 빈칸을 드러낸다. NT001 20:24-23:03의 답변은 이 선택 이유를 설명한다. 기록에 없는 질문자의 원래 문장을 재구성할 필요는 없다. Abstract class도 class이며 concrete class와 구별될 뿐이다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 20:24,21:11,22:06,23:03]]

서로 관련 없는 종류들이 같은 연산을 지원하거나 이미 다른 superclass를 가진 class에 계약을 더할 때는 interface가 유용하다. 관련 class들이 instance fields, 공통 초기화 constructor, protected helper와 구현을 공유할 때는 abstract class가 유용하다. [computer_programming:NM001, PDF pp.54-55](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf)

자료의 선택적 List 예는 계약과 공통 구현을 층으로 나누는 이유를 보여 준다.

~~~text
public abstract class AbstractList<E> implements List<E> { ... }
public class ArrayList<E> extends AbstractList<E> { ... }
~~~

위 코드는 관계를 보여 주는 skeleton이며 collection 알고리즘을 채운 구현이 아니다. List는 연산 계약, AbstractList는 여러 구현이 공유할 부분, ArrayList는 구체 구현을 담당한다. ArrayList가 AbstractList를 상속한다고 List 관계가 사라지지 않는다. `implements List<E>` 관계가 상속을 통해 이어진다. NT001 날짜 미확인 16:41-19:24는 중복 구현을 줄이는 이 연결을 설명한다. E는 이름 붙인 type parameter이며 `?` wildcard와 구별한다. 그 짧은 generic 동기는 method-overloading의 마지막에서 이어진다. [computer_programming:NM001, PDF p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 16:41,17:36,18:29,19:24]]

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Declared type과 receiver

`Parent parent = new Parent(); Parent child = new Child();`에서 두 `print()`가 각각 자기 class 이름을 출력한다. (a) 둘 다 `static`일 때와 instance method를 Child가 override할 때의 두 출력을 비교하라. (b) compiler가 알고 있는 type은 무엇인가? `private`, `final`은 같은 override 대상인가?

<details><summary>해설 보기</summary>

`static`인 두 호출은 `Parent.print()`, `Parent.print()`다. 호출 expression의 declared type이 둘 다 Parent라서 Child의 static hiding body로 dispatch하지 않는다. Instance 대안에서는 첫 receiver가 Parent, 둘째가 Child여서 `Parent.print()`, `Child.print()`다.

Compiler는 두 변수의 declared type Parent를 알고 그 계약에 `print()`가 있는지 검사한다. 이후 instance signature의 override body만 실제 receiver에 따라 달라진다. 대입이 Child 객체를 Parent 객체로 복사하지 않는다. `private` method는 상속된 override 대상이 아니고 `final` method는 override할 수 없다.

**확인 기준:** 두 경우의 네 결과, declared type에 의한 검사, receiver에 의한 instance 구현 선택을 각각 설명해야 한다.

</details>

#### 확인 Q02 · Shape 배열의 두 단계

`Shape[] shapes = new Shape[4];` 뒤 첫 loop가 각 slot에 `randShape()`의 Circle 또는 Square를 저장하고 둘째 loop가 `draw()`를 호출한다. 배열 생성 직후와 첫 loop 후의 차이, 네 출력의 결정 방법, 첫 loop를 생략한 경우를 설명하라. 자료의 Circle/Square/Circle/Circle 순서는 고정인가?

<details><summary>해설 보기</summary>

생성 직후에는 null reference slot 네 개만 있다. 첫 loop가 index 0–3에 실제 Circle/Square 객체의 reference를 넣는다. 두 번째 loop는 공통 Shape 계약으로 호출하지만 각 실제 객체의 override를 선택한다. 예를 들어 저장된 종류가 Circle/Square/Circle/Circle이면 그 순서로 각 `draw()` 메시지가 나온다. 난수 선택이므로 자료의 한 sample을 항상 같은 순서로 보장할 수 없다.

첫 loop를 생략하면 첫 `shapes[0].draw()`의 receiver가 null이어서 `NullPointerException`이다. 배열의 길이 4와 생성된 도형의 수를 혼동하면 안 된다.

**확인 기준:** slot·객체·호출을 구분하고 sample의 불확정성과 null 실패를 모두 적는다.

</details>

#### 확인 Q03 · 표현을 반환하는 toString

`MyClass.toString()`이 `"MyClass"`를 반환할 때 `"String = " + myClass`의 값과 객체 type을 설명하라. Student의 `String.format("%s %s (%d)", fName, lName, id)`는 어떤 책임을 모으는가? 출력만 하는 `void` method, File의 표현, 동등성과도 구별하라.

<details><summary>해설 보기</summary>

연결된 값은 `String = MyClass`다. `public String toString()`이 제공한 표현을 이용한 것이며 원래 MyClass 객체를 String instance로 cast하거나 class를 바꾼 것이 아니다. 반환된 String은 호출자가 다시 사용하거나 출력할 수 있다. `void` method가 직접 출력만 하는 것은 String 반환 계약을 충족하지 못한다.

Student는 두 이름 field의 `%s`와 정수 id의 `%d`를 한 형식에 모아 각 호출자가 연결식을 복사하는 일을 줄인다. File의 `toString()`은 경로의 표현이지 파일 내용 읽기가 아니다. 표현이 같은 두 객체가 반드시 `equals`로 같아지는 것도 아니다.

**확인 기준:** 정확한 결과와 반환/출력/cast의 차이, format의 세 자리, 표현과 동등성의 독립성을 확인한다.

</details>

#### 확인 Q04 · Shoes의 identity·내용·null

Shoes의 `equals(Object o)`는 `this == o`면 true, 그 외에는 `o instanceof Shoes` 뒤 company·model의 `equals`와 size의 `==`를 AND한다. 같은 non-null fields를 가진 별개 s1,s2와 `s3 = s1`에 대해 네 비교 `s1 == s2`, `s1.equals(s2)`, `s1 == s3`, `s1.equals(s3)`를 설명하라. 다른 type, null 인자, null company와 String·primitive의 경우도 구분하라.

<details><summary>해설 보기</summary>

결과는 false, true, true, true다. s1과 s2는 별개 객체지만 세 field의 내용이 같고, s3는 s1의 alias여서 identity 검사부터 true다. 다른 type과 null 인자는 `instanceof Shoes`를 통과하지 않아 false다. Type 검사 뒤 cast해야 다른 종류를 Shoes처럼 사용하는 실패를 피한다.

반면 s1.company가 null이고 다른 Shoes와 비교하면 `this.company.equals(...)`의 receiver가 없어 실패할 수 있다. 자기 비교는 첫 줄에서 true로 끝날 수 있으므로 null 인자와 null field를 합치지 않는다. 두 `new String("abc")`도 별개 identity라 `==`는 false지만 String의 내용 `equals`는 true다. Primitive 자체에는 instance `equals`가 없으며 size는 값 `==`로 비교한다.

Non-null 객체의 동등성은 reflexivity, symmetry, transitivity, 비교 정보가 안 바뀔 때 consistency를 지켜야 하고 `equals(null)`은 false여야 한다.

**확인 기준:** 네 결과마다 이유를 쓰고 null의 두 경로, type guard, 동등성 조건을 빠뜨리지 않는다.

</details>

#### 확인 Q05 · Point2D의 유한 좌표와 NaN

Point2D의 `equals`가 type 검사 뒤 `x == other.x && y == other.y`만 검사하며 identity shortcut은 없다고 하자. 별개 (2.0,3.0) 두 객체, 한 좌표가 다른 객체, null을 비교하고, x가 NaN인 객체의 자기 비교가 드러내는 한계를 설명하라. `toString()`과 hash 계약은 완성되었는가?

<details><summary>해설 보기</summary>

같은 유한 두 좌표는 각각 `==`가 true라 내용 `equals`는 true지만 별개 reference의 `==`는 false다. 좌표 하나가 다르면 AND가 false이고, null은 type 검사에서 false다. x가 NaN이면 `x == x`조차 false이므로 이 body의 자기 `equals`도 false다. 모든 double에 대해 reflexivity를 만족하는 구현으로 일반화할 수 없는 이유다.

`(2.0,3.0)`이라는 `toString()` 표현은 표시 책임이며 동등성 판정과 별개다. 제시된 Point2D는 `hashCode`를 보여 주지 않아 내용 동등성에 맞는 hash 계약까지 완성했다고 볼 수 없다.

**확인 기준:** finite 전제와 NaN의 자기 비교를 직접 추적한다. 보이지 않는 hashCode를 가정하지 않는다.

</details>

#### 확인 Q06 · frequency와 hash의 보장

Collection에 Q04의 s1,s2,null이 이 순서로 있다. `frequency(c,o)`가 o가 null이면 `e == null`, 아니면 `o.equals(e)`를 센다고 할 때 s1과 null의 횟수를 구하라. `Collection`/`Collections`, `equals` true와 같은 hashCode의 함의 방향, 한 번 성공한 조회가 주는 보장도 설명하라.

<details><summary>해설 보기</summary>

대상 s1은 첫 원소와 identity로, 둘째와 세 field 내용으로 같고 null과는 다르므로 2다. 대상 null은 null 원소 하나만 `e == null`로 세어 1이다. `null` 대상에 `o.equals(e)`를 부르면 receiver가 없기 때문에 branch가 필요하다. `Collection`은 interface, `Collections`는 이런 static utility를 제공하는 class다.

`a.equals(b)`가 true이면 `a.hashCode() == b.hashCode()`여야 한다. 같은 hash여도 collision 때문에 `equals` true는 따라오지 않는다. 비교 정보가 그대로일 때의 일관성도 필요하다. 내용 `equals`만 보여 준 Shoes/Point2D를 완전한 hash 호환 구현으로 가정할 수 없다. 조회가 한 번 성공한 사실은 모든 동등한 값에 대한 계약의 보장이 아니다. 또한 순회하는 `Collection<?>`가 임의 type의 삽입을 허용한다는 뜻도 아니다.

**확인 기준:** 2와 1의 모든 원소를 추적하고 함의의 역을 부정한다. 관측과 계약을 구별한다.

</details>

#### 확인 Q07 · Interface가 요구하는 것

RamenCooker의 상수 5,500,3과 `void boilWater()`, `boolean noodleFirst()`를 설명하라. 구체 class는 모든 body를 반드시 새로 직접 써야 하는가? MyInterface의 `printNum(int)`와 인쇄 호출 `func(123)`, PizzaStore의 `Pizza bakePizza()`/`void deliver()` sketch에 각각 어떤 한계가 있는가?

<details><summary>해설 보기</summary>

Interface는 caller가 아는 입력·반환·행동 계약이다. 세 fields는 생략해도 `public static final`이며 초기화된 상수여서 객체별 변경 상태가 아니다. 초기화가 필요하며 충돌하는 modifier를 붙일 수 없다. `boilWater`는 반환값 없는 행동, `noodleFirst`는 boolean 결과를 요구하되 조리 전략은 구현이 정한다. 한 class는 superclass 하나를 extends하면서 여러 interfaces를 implements할 수 있고 interface는 다른 interfaces를 extends할 수 있다.

구체 class는 남은 abstract 의무를 충족해야 하지만 적절한 상속 구현을 재사용할 수 있다. `abstract` class는 일부를 다음 subclass에 남길 수 있다. `default`/static body 예외도 Q12와 구별한다. `printNum(int)` 구현은 public이어야 한다. 인쇄된 `func(123)`는 그 method와 일치하지 않는다. 따로 명시한 수정 호출 `printNum(123)`이라면 123을 출력한다.

PizzaStore의 두 구현은 내부 준비법을 달리해도 `bakePizza()`가 Pizza를 반환하고 `deliver()`는 void인 공통 계약을 지켜야 한다. PizzaHut은 치즈 추가·배달 위치 찾기, MrPizza는 페퍼로니 추가·배달원 찾기를 sketch한다. 원본에는 반환문과 helpers가 빠져 있어 완성 프로그램이 아니다. 공개 계약을 통해 구현 세부를 숨길 수 있다는 점이 encapsulation과 연결된다.

**확인 기준:** 상수 modifiers, 구현 의무의 조건, 두 원본 결함을 모두 설명한다.

</details>

#### 확인 Q08 · List의 index trace

`List<Integer> list = new ArrayList<>();`에 10,20,30을 차례로 add하고 `get(2)`, `remove(1)`, `size()`를 호출한다. 각 결과와 목록 상태, `set`의 역할, Integer와 int, 구현을 LinkedList로 바꾸는 의미를 설명하라.

<details><summary>해설 보기</summary>

세 add 후 [10,20,30]이다. Zero-based `get(2)`는 30을 반환하고 목록은 유지한다. 여기서 `remove(1)`은 int index 1의 값 20을 제거하므로 [10,30], size는 2다. 값 1을 찾는 삭제가 아니다. `set`은 위치의 값을 갱신하는 별도 연산으로 이 순서에서는 호출되지 않았다.

Integer는 wrapper reference type이며 숫자 add에는 boxing이 적용된다. `List<int>`로 표기를 바꿀 수 없다. 같은 지원 연산에 대해 생성 부분을 LinkedList로 바꾸어도 caller는 List 계약을 쓸 수 있다. 내부 저장이나 성능이 같다는 뜻은 아니다. MyFavoriteList/MyOwnList는 실제 List 구현이 있다는 가정이며 제공된 class body가 아니다.

**확인 기준:** get·remove·size의 결과와 상태를 각각 쓰며 boxing과 계약/구현 구별을 확인한다.

</details>

#### 확인 Q09 · Ordering의 부호와 equality

높이만 비교하는 Seagull의 (height,friends)가 a=(10,1), b=(3,100), c=(10,99)다. `a.compareTo(b)`, `b.compareTo(a)`, `a.compareTo(c)`의 결과를 설명하라. 0은 identity/equals를 뜻하는가? 모든 객체가 Comparable인가?

<details><summary>해설 보기</summary>

자료 body는 높이가 크면 1, 같으면 0, 작으면 -1이므로 결과는 1,-1,0이다. 친구 수는 이 기준에서 읽지 않는다. 일반 `compareTo` 계약은 양수·음수·0의 의미를 요구하며 반드시 ±1만 반환해야 하는 것은 아니다.

0은 선택한 높이 ordering의 동순위일 뿐이다. a,c는 별개 identity이고 이 class는 equals override를 제시하지 않았으므로 모든 fields나 equals까지 같다고 할 수 없다. `equals`는 Object에서 기본 의미를 얻지만 순서는 유용한 class가 Comparable로 선택하는 계약이다. Comparable을 implements해도 다른 superclass나 interfaces 관계는 가능하며 모든 collection에 자동 적합하다는 보장도 아니다.

**확인 기준:** 세 부호의 방향과 선택 속성, 0과 equals의 차이, 순서의 선택성을 적는다.

</details>

#### 확인 Q10 · String의 첫 차이와 prefix

공급된 String 비교 발췌는 첫 다른 문자에서 코드 차이, 공통 범위가 같으면 길이 차이를 반환한다. 다음 여섯 결과를 결정 위치와 함께 구하라: `aaaaaa` 대 `bbbbbb`, 역방향, `aaaaaa` 대 자기 자신, `bbbbbb` 대 `bccccc`, `bbbbbb` 대 `BBBBBB`, `ab` 대 `abcd`.

<details><summary>해설 보기</summary>

차례로 -1,1,0,-1,32,-2다. 첫 둘은 첫 a와 b의 차이와 그 역이다. 셋째는 모든 문자와 길이가 같다. 넷째는 첫 b가 같아 두 번째 b-c에서 -1로 결정한다. 다섯째는 첫 b-B=32로 즉시 결정한다. 마지막은 공통 두 문자 뒤 한쪽이 끝나 2-4=-2다.

따라서 길이를 먼저 비교하거나 전체 코드 합을 비교하지 않는다. 32처럼 크기가 1이 아닌 값도 양수라는 부호가 순서를 뜻한다. 이 영문 코드 비교를 문화권별 사전 정렬 전체나 모든 Java 버전의 String 내부 저장 형태로 확대하지 않는다.

**확인 기준:** 여섯 숫자와 최초 결정 위치를 모두 적는다. Prefix에서는 문자 차이가 없음을 밝힌다.

</details>

#### 확인 Q11 · GPA의 저장·정렬·표현

Student.compareTo가 `diff = gpa - other.gpa; return diff > 0 ? 1 : diff < 0 ? -1 : 0;`, toString이 `Double.toString(gpa)`다. 3.3,4.2,3.1을 add한 뒤 sort하면 무엇이 바뀌는가? 두 method의 역할과 diff가 NaN인 경계도 설명하라.

<details><summary>해설 보기</summary>

`add` 직후 [3.3,4.2,3.1]이며 주어진 유한 값의 compareTo 부호를 따라 sort하면 [3.1,3.3,4.2]다. `add`는 저장 원소를 늘리고 sort는 이미 저장된 원소의 순서를 바꾼다. `compareTo`가 순서를 정하고 toString은 각 GPA를 읽을 수 있게 나타낼 뿐이다. 표시만 고쳐 정렬 기준이 달라지지 않는다. 이 Student는 이름/id 표현 예와 독립된 정의다.

`diff`가 NaN이면 >0과 <0이 모두 false라 마지막 0을 반환한다. 이를 모든 double에 대해 올바른 동순위 판정이라고 보장할 수 없다. 그래서 결과는 이 유한 값의 전제 아래 읽는다.

**확인 기준:** 초기·최종 순서, 두 method와 add/sort의 분담, NaN의 두 false를 확인한다.

</details>

#### 확인 Q12 · default body와 package access

`interface RamenCooker { void boilWater(); default void clean() { System.out.println("Rinsing with water"); } }`에서 구현 의무와 공통 body를 나누어 설명하라. Interface static body와 access modifier를 생략한 경우의 default도 같은 뜻인가?

<details><summary>해설 보기</summary>

`boilWater`는 abstract 의무라 구체 구현에서 충족해야 한다. `clean`은 사용할 수 있는 공통 instance body로 `Rinsing with water`를 출력한다. 자료는 Java 8부터 interface의 default/static bodies를 허용한다고 명시하므로 “interface에는 body가 전혀 없다”는 보편 규칙은 성립하지 않는다.

`static` body는 interface 자체에 속하며 receiver별 instance override 선택과 다르다. `default` keyword의 body 제공은 access modifier 생략으로 얻는 package access와 다른 용법이다. 이 구별만으로 모든 이후 버전의 interface 문법이나 충돌 해결을 다룬 것은 아니다.

**확인 기준:** abstract/default/static을 구별하고 package access와 혼동하지 않는다.

</details>

#### 확인 Q13 · Person의 공통 상태와 빈 동작

Person에 package-access description/name, private age, 공통 printName/ageOneYear와 abstract work/play가 있다. (a) work/play에 기본 body를 두는 대안과 비교하라. (b) 초기화가 갖춰졌다고 가정하여 Student 25, BusinessMan 34의 나이와 work/play를 추적하라. (c) 원본의 `super(description,name,age)` 호출이 보여 주는 누락은 무엇인가?

<details><summary>해설 보기</summary>

`abstract`로 남기면 Person을 직접 생성할 수 없고 구체 subclass가 남은 동작을 정해야 한다. 임의의 work/play를 부모가 정하지 않아 설계의 빈칸이 드러난다. Concrete body를 제공하고 abstract 제한을 없애면 보통 class가 되고 자식이 기본 동작을 그대로 상속할 수 있다. `abstract` class가 반드시 abstract/concrete method를 각각 하나 이상 가져야 하는 것은 아니다.

필요한 초기화를 전제하면 공통 ageOneYear로 25→26,34→35다. Student의 work/play는 `Study hard`/`Drink hard`, BusinessMan은 `Meeting all day`/`Go to the movies`다. `printName`과 나이 변경은 부모 구현을 재사용한다. `private` age는 자식이 직접 읽는 대신 부모 method가 다루며 description/name도 public이 아니다.

그러나 Person 페이지에는 세 인자 constructor가 없고 자식 페이지들은 그것을 호출한다. 따라서 위는 의도된 상태 trace이며 인쇄 전체의 성공 실행 결과로 주장할 수 없다. `non-field field` 주석도 새로운 Java field 종류가 아니다.

**확인 기준:** 설계 대안·접근 수준·두 나이와 네 행동·누락된 constructor를 모두 설명한다.

</details>

#### 확인 Q14 · 계약·공통 구현·구체 구현

서로 관련 없는 객체들이 같은 연산을 지원해야 하는 경우와 관련 class들이 상태·초기화·helper를 공유하는 경우에 무엇을 선택하는가? `AbstractList<E> implements List<E>`와 `ArrayList<E> extends AbstractList<E>`에서 세 층의 역할과 List 관계가 유지되는 이유를 설명하라.

<details><summary>해설 보기</summary>

전자는 interface로 공통 연산 계약을 주는 경우다. 이미 superclass가 있는 class에 다른 계약을 더할 때도 유용하다. 후자는 abstract class에 instance fields, 공통 constructor 초기화, protected helpers와 공통 구현을 모으는 경우다.

List는 연산 계약, AbstractList는 그 계약의 공통 구현 일부, ArrayList는 구체 구현이다. ArrayList가 AbstractList를 상속하면 그 superclass의 List 구현 관계가 이어지므로 List를 버린 것이 아니다. 여러 구현이 공통 부분을 다시 쓰지 않게 하는 구조다. 제시된 것은 skeleton이지 실제 collection 알고리즘 전체가 아니다. `E`는 동일 type 자리를 잇는 이름 있는 parameter이며 `?` wildcard와 같지 않다.

**확인 기준:** 둘의 선택 이유와 세 층·전달되는 관계를 설명하고 generic 상세를 가정하지 않는다.

</details>

### 연습

#### 연습 P01 · 동등성 검사 기록의 감사

새로 작성한 synthetic practice다. Identity와 content equality, hashCode 계약이 선수 조건이다. [EX:cp_2026_1_final_q01d p.1], [EX:cp_2026_1_final_q03 p.3]의 ‘관측과 계약에 의한 보장 구별’만 연결한다(3-(a), 구현 보완은 제외).

가상 검사 기록 A는 `a.equals(b)=true`, hash 17/23이고 B는 `a.equals(c)=false`, hash 17/17이다. 담당자는 B를 결함, A를 ‘조회 한 번이 성공했으니 괜찮음’으로 판정했다. 각 판정의 오류와 아직 확인하지 않은 조건을 설명하라. 새 hash 구현은 작성하지 않는다.

<details><summary>해설 보기</summary>

A는 equal→same hash라는 필수 함의를 위반한다. 한 조회가 우연히 성공해도 17≠23이라는 계약 위반이 사라지지 않는다. B는 unequal인데 같은 hash인 collision이므로 그 사실만으로 결함이 아니다. Same hash→equal이라는 역을 잘못 쓴 판정이다.

이 두 기록만으로 equals의 reflexivity/symmetry/transitivity와 비교 정보가 그대로일 때의 consistency, hash의 일관성 전체를 확인한 것은 아니다. 어느 실행의 contains 결과나 모든 library 호환성도 정할 수 없다.

**확인 기준:** A의 필수 위반, B의 허용 가능 collision, 단일 관측의 한계와 미확인 조건을 적는다.

</details>

#### 연습 P02 · 계약과 공유 상태를 나누는 설계

새로 작성한 lecture-based general practice다. 색인의 interface 정의 문항은 있으나 이 설계 과제와 직접 대응하는 출제 형식 근거는 없다.

이미 다른 superclass를 가진 외부 장치와, 공통 name·counter·초기화·helper를 공유하는 내부 장치들이 모두 `String report()`를 제공해야 한다. 최소 설계의 역할을 interface/abstract class/concrete class로 배정하라. 공통 동작에 default body를 둘 수 있다는 것만으로 interface가 instance counter를 보관할 수 있는가? 공통 report 문자열이 같으면 두 장치가 equals로 같은가?

<details><summary>해설 보기</summary>

공통 report 입력·String 반환 계약은 interface에 둔다. 외부 장치는 자기 superclass를 유지하며 그 interface를 implements할 수 있다. 관련 내부 장치는 interface를 implements하는 abstract class에서 name/counter·공통 초기화·helpers를 재사용하고, concrete subclasses가 남은 의미 있는 동작을 충족한다. AbstractList→ArrayList와 같은 역할 분담이다.

`default` body는 공통 instance 동작을 제공할 수 있지만 interface fields가 `public static final`인 점을 바꾸지 않는다. 객체마다 변하는 counter는 공유 abstract class의 instance 상태로 둘 이유가 있다. 같은 문자열 표현만으로 identity나 equals가 정해지지 않으므로 별도 동등성 기준이 필요하다. 완전한 장치 구현은 요구되지 않는다.

**확인 기준:** 외부 class의 상속 유지, 내부 공유 상태, interface field 제한과 표시/동등성 분리를 확인한다.

</details>

## 출처

### 강의 노트와 전사

- [[courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2|날짜 미확인 · Object 계약·polymorphism·generic 도입]]
- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · 배열·순회 선수 내용]]
- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · 객체·constructor·static·reference 선수 내용]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · 객체·초기화·reference 복습]]

날짜가 있는 노트는 해당 선수 내용을 다시 찾기 위한 링크다. Inheritance·dispatch의 상세를 그 날짜에 모두 다뤘다는 뜻은 아니다.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 전사]] — 00:48, 01:48, 02:48, 03:33, 04:25, 05:25, 06:23, 07:23, 08:22, 09:13, 10:13, 13:48, 14:45, 16:41, 17:36, 18:29, 19:24, 20:24, 21:11, 22:06, 23:03.

### 자료와 원본 쪽

쪽수는 물리 PDF 기준이다. 각 쪽 링크에서 원본 페이지를 함께 볼 수 있다.

- [6 inheritance 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [20쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-020), [21쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-021), [22쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-022), [23쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-023).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [3쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-003), [4쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [5쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [6쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [7쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007), [8쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-008), [9쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-009), [12쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-012), [13쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-013), [14쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-014), [15쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-015), [16쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-016), [17쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-017), [18쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-018), [19쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-019), [20쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-020), [21쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-021), [22쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-022), [23쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-023), [24쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-024), [26쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-026), [27쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-027), [28쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-028), [29쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-029), [30쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-030), [31쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-031), [32쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-032), [33쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-033), [34쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-034), [35쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-035), [36쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-036), [37쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-037), [38쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-038), [39쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-039), [40쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-040), [41쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-041), [42쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-042), [43쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-043), [44쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-044), [45쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-045), [46쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-046), [47쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-047), [49쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-049), [50쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-050), [51쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-051), [52쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-052), [53쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-053), [54쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-054), [55쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [56쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056).
- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [33쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-033).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [1쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [4쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-004), [6쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-006), [19쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).

### 범위와 불확실성

NT001은 날짜 미확인 전사다. 95개 발화에 남은 124개 문자 그대로의 불확실성 표시와 76개 추가 한계를 유지하며, 불명확한 말·부정·누락을 자료 문장으로 복원하지 않는다. 인쇄 예제는 자료 근거이며 모두 새로 말한 예제라는 뜻이 아니다. 아래 시간은 전사에서 찾을 위치이며 별도 시간 앵커를 뜻하지 않는다.

NM005는 물리 PDF 36쪽이다. 등록명은 Lab 6이지만 표지는 Lab 1이고, TODO와 19쪽의 제공되지 않은 ZIP이 남아 있다. 여기서는 개념 자료로만 사용하며 완성된 채점 대상 구현이나 해당 실습의 출석·제출 규칙을 가져오지 않는다.

NM001 3쪽의 ‘컴파일 때 변수 type을 모른다’는 일반화, 14쪽의 String cast 표현, 17쪽의 primitive equals 표현은 그대로의 Java 규칙으로 채택하지 않는다. 22쪽의 Collection/Collections, 30쪽의 func/printNum, Pizza의 누락된 반환문, Person의 빠진 constructor와 주석을 구별한다. 앞쪽의 interface body 금지는 47쪽의 Java 8 default/static 예외로 한정한다. Shoes·Point2D에는 호환 hashCode가 제시되지 않았고, NaN은 좌표 equality와 GPA 비교의 일반화를 막는다. String 발췌는 제시된 구현과 문자 예의 범위이며 전체 버전·locale 규칙을 확정하지 않는다. NT001 16:41의 E/wildcard 표현과 abstract class의 직접 생성·성능에 관한 불확실한 진술도 자료와 구별한다. List/Comparable의 전체 알고리즘·모든 계약 및 상세 generics는 이 범위를 넘는다.

### 비공식 복기와의 제한된 연결

복기 자료는 비공식이며 검증된 공식 정답은 제공되지 않았다. 파일명에만 연결된 2025년 봄 중간 김상한, 2026년 봄 기말 유영재는 현재 유재민(Jaemin Yoo) 교수와 다르다. 연결은 아래 개념·풀이 구조에 한정하며 현재 수업의 출제 형식·범위·빈도·확률을 뜻하지 않는다. 신규 문항은 일반 또는 합성 연습이다.

- [EX:cp_2025_1_midterm_q02 p.1] — Interface의 입력·반환·행동 계약을 설명하는 개념 연결이다. Class와 method 기초를 전제로 하며 anonymous class·lambda 구현은 가져오지 않는다.
- [EX:cp_2026_1_final_q01d p.1] — Equal이면 같은 hashCode가 필요하다는 한 방향 함의를 연결한다. Identity/content와 Object 계약이 선수 내용이며 hash 구현은 요구하지 않는다.
- [EX:cp_2026_1_final_q03 p.3] — 3-(a)의 단일 관측과 계약에 의한 보장 구별만 연결한다. Equality·override가 선수 내용이며 3-(b)의 구현 보완과 HashSet 내부는 제외한다.

Shape 배열, toString 형식, List index, Seagull/String/GPA 계산, Person·List 계층에는 직접 대응하는 색인 문항이 없다. P02는 이 자료에서 만든 일반 설계 연습이다.
