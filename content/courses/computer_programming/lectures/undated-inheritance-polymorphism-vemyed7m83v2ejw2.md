---
title: "Object 계약·Polymorphism과 Generics 도입 · 강의 정리 · 날짜 미확인"
course: "computer_programming"
lang: "ko"
term: "2026_Fall"
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
source_assets: ["6 inheritance 1.pdf", "7 inheritance 2.pdf", "8 polymorphism.pdf", "Lab 6 Polymorphism.pdf", "Lecture 2 Java Basics 1.pdf"]
source_basis: "privacy_reviewed_corrected_text_and_official_materials"
---

## 강의 내용과 설명

### Reference type과 상속 관계

**Reference(참조)** 변수는 객체 자체가 아니라 객체를 가리키는 값을 보관한다. 같은 객체를 가리키는 두 변수를 alias라고 한다. **Declared type(선언 타입)** 은 소스에 적힌 변수의 타입이고, **runtime class(실제 클래스)** 는 그 변수가 가리키는 객체를 만든 클래스다. 예를 들어 Parent child = new Child();에서 변수 child의 선언 타입은 Parent, 실제 객체의 클래스는 Child다. 대입은 Child 객체를 Parent 객체로 새로 만드는 과정이 아니다.

선택 선수자료인 RM001의 **Inheritance(상속)** 를 적용하면 Child extends Parent는 Child가 Parent의 하위 타입이라는 관계를 만든다. 클래스는 하나의 직접 superclass를 가지며, 별도 superclass를 쓰지 않은 일반 클래스도 Object로 이어진다. 상속은 부모의 모든 것을 자식 코드에서 직접 읽을 수 있다는 뜻은 아니다. public은 외부 공개, private은 해당 클래스 내부, modifier를 생략한 package access는 같은 package에서의 접근이다. protected는 같은 package와 상속 관계에서 접근을 허용하되 접근 맥락의 제한을 따른다. 부모의 private 상태는 부모가 제공하는 메서드를 통해 사용한다. Encapsulation(캡슐화)은 이런 공개 계약과 내부 상태·구현의 경계를 정하는 일이다. [RM001, PDF pp.12-23, 55-64][RM001]

메서드 선언의 parameter는 입력을 받는 변수이고, argument는 호출 때 전달하는 식이다. return은 값을 호출한 곳에 돌려주며, println은 출력한다. 따라서 String을 반환하는 메서드와 void로 출력만 하는 메서드는 서로 다른 책임을 가진다. 배열의 index는 0부터 length - 1까지이고, for loop는 초기화 후 조건 검사, 본문, 갱신, 다음 조건 검사 순서로 진행한다. 이 기초가 뒤의 객체 배열 순회와 overload 계산에 사용된다.

### Static binding과 dynamic binding의 서로 다른 선택 기준

**Binding(바인딩)** 은 메서드 호출을 어떤 동작에 연결하는지 설명한다. 자료 보충인 NM001의 다음 두 Parent/Child 정의는 서로 비교하는 독립된 예다. 먼저 static 메서드를 둔 경우다.

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

두 변수의 선언 타입이 모두 Parent이므로 출력은 Parent.print(), Parent.print()다. Child의 static print는 부모의 static print를 **hide(숨김)** 한다. 실제 객체가 Child라는 이유로 Child.print를 고르지 않는다. static은 클래스에 속하므로 Parent.print()처럼 클래스 이름으로 쓰면 이 의미가 더 분명하다. [NM001, PDF pp.4-5][NM001]

이번에는 static을 없애고 Child가 instance method를 override한다.

~~~text
class Parent {
    void print() {
        System.out.println("Parent.print()");
    }
}
class Child extends Parent {
    @Override
    void print() {
        System.out.println("Child.print()");
    }
}

Parent parent = new Parent();
Parent child = new Child();
parent.print();
child.print();
~~~

이때 출력은 Parent.print(), Child.print()다. Compiler(컴파일러)는 Parent 타입에서 print() 호출이 가능한지 검사하고, 실행 중에는 receiver, 즉 호출을 받는 실제 객체에 맞는 override body를 선택한다. 같은 Parent 선언으로도 두 객체의 동작이 달라지는 **Dynamic dispatch(동적 디스패치)** 다. private 메서드는 상속된 override 대상이 아니며 final 메서드도 override할 수 없다. 이들은 실제 객체의 하위 구현을 고르는 사례와 구별한다. [NM001, PDF pp.3, 6-7][NM001]

NM001 p.3의 “Types of variables are unknown during the compilation.”은 선언 타입을 컴파일러가 모른다는 규칙으로 받아들이면 틀린다. 선언 타입은 알고 있으며 실행 중 달라질 수 있는 실제 receiver와 구현을 구분해야 한다. NT001 00:48은 static/dynamic binding을 회고하지만 위의 정확한 두 출력 비교는 인쇄 자료 보충이다. [NT001, STT 00:48][NT001]

| 호출 종류 | 컴파일 때 확인하는 기준 | 실행할 body를 고르는 기준 |
| --- | --- | --- |
| `static` method hiding | 참조 표현식의 선언 타입 | 그 선언 타입에서 선택한 `static` 메서드 |
| Instance method overriding | 선언 타입에서 해당 호출이 가능한지 | 실제 receiver 객체의 override body |

[NM001, PDF pp.3-7][NM001]

### Shape 배열에서 같은 draw 호출이 달라지는 이유

자료 보충인 Shape 예에서는 Shape가 void draw()를 제공하고 Circle과 Square가 각각 자신의 draw를 재정의한다. Shape.randShape()의 반환 타입은 Shape지만 실제 반환 객체는 Circle 또는 Square다.

~~~text
class Shape {
    void draw() { }

    public static Shape randShape() {
        switch ((int)(Math.random() * 2)) {
            default:
            case 0: return new Circle();
            case 1: return new Square();
        }
    }
}
class Circle extends Shape {
    void draw() { System.out.println("Circle.draw()"); }
}
class Square extends Shape {
    void draw() { System.out.println("Square.draw()"); }
}

Shape[] shapes = new Shape[4];
for (int i = 0; i < shapes.length; i++) {
    shapes[i] = Shape.randShape();
}
for (int i = 0; i < shapes.length; i++) {
    shapes[i].draw();
}
~~~

new Shape[4]는 Shape reference slot 네 개를 만든다. 도형 객체 네 개를 생성한 것이 아니며, 처음 각 원소 값은 null이다. 첫 loop가 index 0, 1, 2, 3의 slot에 반환된 도형 참조를 저장한다. 두 번째 loop의 shapes[i]는 선언상 Shape이지만 Circle 객체이면 Circle.draw(), Square 객체이면 Square.draw()가 선택된다. 첫 loop 없이 null 원소에 draw()를 호출하면 receiver가 없어 NullPointerException이 발생한다는 것은 이 코드의 호출 조건에 대한 설명이다.

Math.random()의 값은 0 이상 1 미만이므로 2를 곱한 뒤 int로 변환하면 이 예에서는 0 또는 1이 된다. 자료의 네 출력 Circle.draw(), Square.draw(), Circle.draw(), Circle.draw()는 가능한 순서 하나다. 매번 그 순서라는 뜻이 아니다. 배열의 공통 원소 타입과 각 원소의 실제 클래스를 구별하면 여러 종류의 도형을 동일한 loop로 다룰 수 있다. [NM001, PDF pp.8-9][NM001]

### Object.toString: 객체의 문자열 표현

Object의 **public String toString()** 은 객체를 설명하는 문자열 표현을 제공한다. 상속 관계가 Object로 이어지므로 직접 선언하지 않은 클래스도 기본 메서드를 가지며, 필요한 클래스는 자신의 정보에 맞게 override한다. NT001은 호출자가 매번 필드를 조합하지 않아도 자연스러운 문자열 표현을 얻는다는 동기를 설명한다. [NT001, STT 00:48, 01:48][NT001]

자료 보충인 MyClass의 toString이 "MyClass"를 반환하면 다음 연결의 결과는 String = MyClass다.

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

NM001 p.14는 이를 “casts the object to the String class”라고 표현하지만 reference cast로 객체가 String 인스턴스가 된다는 뜻은 아니다. 문자열 연결에서 문자열 표현을 얻어 사용한 것이다. 원래 객체의 클래스는 여전히 MyClass다. toString은 String을 반환하고 println이 그 결과를 출력한다. toString 자체가 출력만 하고 void를 반환하는 메서드여서는 해당 계약을 구현하지 못한다. [NM001, PDF pp.12-14][NM001]

NM001 p.13의 String 예는 cp와 cp.toString()이 같은 내용을 나타내며, File 예도 객체 표현과 file.toString()이 같은 경로 문자열을 출력한다. 이는 파일 내용 읽기를 보여 주는 예가 아니다. Student 예는 fName, lName, id를 한곳에서 다음 형식으로 표현한다.

~~~text
@Override
public String toString() {
    return String.format("%s %s (%d)", fName, lName, id);
}
~~~

%s는 문자열 자리, %d는 정수 자리다. 매번 fName + " " + lName + " (" + id + ")"를 호출자가 조합하는 대신 객체에 표현 책임을 둔다. 여기의 Student는 뒤에서 GPA를 비교할 Student와 별개의 자료 예다. 문자열 표현이 같다는 사실만으로 두 객체가 equals로 같다는 결론은 나오지 않는다. [NM001, PDF pp.13, 15-16][NM001]

### equals: identity와 내용 동등성, type과 null 검사

**Identity(동일성)** 는 두 참조가 같은 객체를 가리키는지의 문제다. 참조의 ==는 identity를 비교하고, Object.equals의 기본 의미도 이 동일성이다. **Content equality(내용 동등성)** 를 원하면 어떤 필드가 의미상 같은 값을 만드는지 정하여 equals를 재정의한다. 실제 물리 주소를 프로그램이 드러내 비교한다는 설명으로 확대할 필요는 없다. NT001 01:48이 말하는 내용 비교의 동기가 여기에 해당한다. [NT001, STT 01:48][NT001]

자료의 new String("abc")를 두 번 호출하면 별도 두 객체이므로 s1 == s2는 false지만 s1.equals(s2)는 true다. String은 이미 문자 내용을 비교하는 equals를 제공하기 때문이다. 과거 기초 설명인 T007 15:58, 16:54도 같은 구별을 다루며, M002의 "Apple" 예도 identity false, 내용 비교 true다. Primitive int 값 자체에는 instance equals 메서드가 없다. NM001 p.17의 primitive에도 ==와 equals가 같다는 문구는 wrapper 객체와 primitive를 혼동한 부정확한 설명이다. [NM001, PDF pp.17-18][NM001]; [M002, PDF p.61][M002]

자료 보충인 Shoes는 company, model, size 세 필드로 내용 동등성을 정한다. 다음은 자료의 equals 본문이다.

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

첫 검사는 같은 객체라면 바로 true를 돌려준다. 그다음 instanceof로 o가 Shoes로 취급할 수 있는 객체인지 검사한 뒤 cast한다. String인 company와 model은 내용 equals로 비교하고, primitive int인 size는 ==로 비교한다. 세 조건을 &&로 묶었으므로 하나라도 다르면 false다. 타입 확인 없이 먼저 (Shoes)o를 수행하면 다른 종류의 객체에 대한 비교가 cast 실패로 이어질 수 있다.

~~~text
Shoes s1 = new Shoes("Nice", "AirMax", 265);
Shoes s2 = new Shoes("Nice", "AirMax", 265);
Shoes s3 = s1;

s1 == s2       // false
s1.equals(s2)  // true
s1 == s3       // true
s1.equals(s3)  // true
~~~

s1과 s2는 별도 객체지만 세 값이 같고, s3는 s1의 alias다. s1.equals(null)은 null instanceof Shoes가 false여서 false다. 그러나 s1.company 자체가 null이면 this.company.equals(...)의 receiver가 null이므로 안전하지 않다. Null인 비교 인자를 거부하는 것과 내부 필드의 null을 안전하게 다루는 것은 서로 다른 조건이다. 자료의 생성자는 null을 금지하거나 변환하지 않으므로 이 코드를 모든 입력에 안전한 완성 구현으로 볼 수 없다. [NM001, PDF pp.19-21][NM001]

equals는 non-null 객체에서 reflexivity(자기 자신과 같음), symmetry(양방향 결과 일치), transitivity(연쇄적인 동등성), 비교에 쓰이는 정보가 변하지 않을 때의 consistency(일관성)를 지켜야 하며, non-null 객체의 equals(null)은 false여야 한다. 예를 들어 a와 b가 같은 신발이라고 판정하면서 b와 a는 다르다고 판정하면 collection의 조회 결과가 비교 방향에 따라 달라진다. 내용 동등성은 단순히 true가 나오는 코드를 쓰는 일이 아니라 일관된 관계를 설계하는 일이다.

별도 자료 보충인 NM004의 Point2D는 o instanceof Point2D를 확인하고 x, y를 각각 ==로 비교한다. 유한 좌표 (2.0, 3.0)를 가진 별도 두 객체는 이 equals에서 true이고 참조 ==는 false다. 한 좌표가 다르면 false, null 인자도 false다. toString은 "(2.0,3.0)" 같은 표현을 만들지만 equality를 결정하지 않는다. 이 예에는 hashCode가 없고, 직접 double ==를 모든 수치 동등성의 정의로 일반화할 수 없다. 특히 NaN 좌표는 자기 자신과도 ==가 false이므로 제시된 Point2D.equals가 reflexivity까지 만족하는 범용 수치 구현은 아니다. [NM004, PDF p.33][NM004]

### Collection의 동등성 검사와 equals/hashCode 계약

**Collection** 은 원소 집합을 다루는 interface이고 **Collections** 는 collection을 다루는 static utility 메서드들의 클래스다. NM001 p.22의 설명에서 이 둘을 구별해야 한다. p.23의 frequency는 result를 0으로 시작하여 찾는 값 o와 같은 원소 수를 센다. 자료의 핵심 분기는 다음과 같다.

~~~text
if (o == null) {
    for (Object e : c) {
        if (e == null) result++;
    }
} else {
    for (Object e : c) {
        if (o.equals(e)) result++;
    }
}
~~~

o가 null이면 o.equals를 호출할 수 없으므로 각 원소가 null인지 직접 센다. o가 non-null이면 o.equals(e)를 호출한다. 예를 들어 c가 앞의 s1, s2, null을 순서대로 담았고 찾는 o가 s1이면 Shoes의 내용 equals에 따라 두 신발을 세어 2가 된다. o가 null이면 결과는 1이다. Collection<?>의 ?는 특정 원소 타입 이름을 여기서 고정하지 않는 표기라는 정도로 읽으면 된다. 어떤 객체든 아무 연산에 넣어도 안전하다는 뜻은 아니다. [NM001, PDF pp.22-23][NM001]

**Hash code** 는 hashCode()가 반환하는 int 값이다. Java 철자는 hashCode이며 자료의 hashcode와 대소문자가 다르다. a.equals(b)가 true이면 a.hashCode()와 b.hashCode()도 같아야 한다. 역은 성립하지 않는다. 서로 다른 두 객체에 같은 int가 나오는 collision(충돌)이 가능하므로 hash 값이 같다고 equals가 true인 것은 아니다. 비교에 필요한 상태가 변하지 않는 동안 같은 객체의 hash 값도 일관되어야 한다.

별도 Shoes 객체 s1과 s2를 equals로 같게 정의하면서 서로 다른 hash 값을 주면 hash 기반 저장·검색에서 같은 값이라는 계약과 분류 기준이 어긋난다. 따라서 equals를 내용 비교로 바꾸면 같은 내용에 같은 hash 값을 주도록 hashCode 계약도 맞춰야 한다. 자료의 Shoes와 Point2D는 hashCode 구현을 보여 주지 않으므로 이 계약 전체가 완성된 예는 아니다. 새 hash 함수나 충돌 처리 알고리즘을 원본 예에 덧붙일 필요는 없다. Object의 모든 메서드를 반드시 다시 구현해야 하거나 어느 library와도 자동 호환된다는 뜻도 아니다. [NM001, PDF p.24][NM001]

### Interface가 정하는 입력·반환 계약

**Interface(인터페이스)** 는 호출자에게 어떤 동작을 제공하는지 약속하는 타입이다. **Abstract method(추상 메서드)** 는 body 없이 이름, parameter 타입, 반환 타입을 선언한다. 구체 클래스는 implements로 계약을 받아들이며, 남아 있는 abstract 동작을 실제 구현으로 만족시켜야 한다. 이미 상속한 적절한 구현이 있으면 그것을 사용할 수도 있고, abstract 클래스는 일부 구현 의무를 다음 하위 클래스에 남길 수도 있다. 하나의 클래스는 superclass 하나를 extends하면서 interface 여러 개를 implements할 수 있다. Interface 자체를 구현 없이 직접 생성하는 대신 계약을 구현한 concrete class의 객체를 사용한다. 공개된 호출 계약을 통해 내부 구현을 몰라도 사용하게 한다는 점에서 encapsulation과 연결된다. [NT001, STT 02:48, 03:33, 04:25][NT001]

자료 보충인 RamenCooker는 다음 값과 동작을 선언한다.

~~~text
interface RamenCooker {
    int numSteps = 5;
    int amountWater = 500;
    int boilTime = 3;
    void boilWater();
    boolean noodleFirst();
}
~~~

interface field는 생략해도 public static final이다. 따라서 5, 500, 3은 객체마다 바꾸는 instance 상태가 아니라 초기화된 상수다. 값을 주지 않거나 이 성격과 충돌하는 modifier를 붙이면 안 된다. boilWater()는 반환값이 없는 행동이고 noodleFirst()는 boolean 결과를 제공해야 한다. 선언만으로 실제 조리 절차가 정해지지는 않는다. [NM001, PDF pp.26-29][NM001]

MyInterface의 void printNum(int i)를 MyClass가 구현할 때 public void printNum(int i)로 접근을 유지하며 인자를 출력한다. 다만 p.30 하단에는 myClass.func(123);가 인쇄되어 있다. 위에서 제공한 메서드는 printNum이지 func가 아니므로 이 호출과 주석의 123은 그대로 성공 출력의 근거가 되지 않는다. 별도 학습용 수정 호출 myClass.printNum(123);라면 제공된 구현이 123을 출력한다는 의미다. 원자료의 호출 이름과 이 수정은 구별한다. [NM001, PDF p.30][NM001]

PizzaStore의 계약은 Pizza bakePizza()와 void deliver()다. PizzaHut는 addCheese와 findDeliveryLocation을, MrPizza는 addPepperoni와 findDeliveryMan을 사용하도록 sketch되어 있다. 서로 다른 내부 전략이어도 호출자는 같은 이름과 입력·반환 타입을 기대한다. 특히 bakePizza는 Pizza를 반환해야 한다. 자료의 두 body에는 반환문이 없고 helper 정의도 없으므로 완성 프로그램이 아닌 설계 sketch다. 공통 계약은 구현 전략을 감추되 필요한 결과까지 생략해도 된다는 허가가 아니다. [NM001, PDF pp.31-32][NM001]

### `List<E>`: 같은 계약으로 구현을 바꾸기

**`List<E>`** 는 순서가 있는 원소들을 다루는 interface이며 E는 원소의 타입 자리다. ArrayList와 LinkedList는 그 구현 예다. 자료 보충의 다음 호출을 순서대로 추적한다.

~~~text
List<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
list.get(2);
list.remove(1);
list.size();
~~~

add 세 번 뒤 원소 순서는 [10, 20, 30]이다. index는 0부터 시작하므로 get(2)는 30을 반환하고 목록을 바꾸지 않는다. remove(1)은 이 호출에서 int index 1의 원소 20을 제거하고 반환한다. 목록은 [10, 30]이 되고 size()는 2다. 숫자 값 1을 가진 원소를 찾아 제거하라는 호출과 혼동하면 안 된다. set은 지정 위치의 원소를 바꾸는 별도 연산이며 위 trace에서는 호출되지 않았다.

Integer는 primitive int가 아닌 wrapper 클래스다. list.add(10)은 이 예에서 int 값이 Integer로 boxing되어 들어가는 표면적인 사용이다. get의 원소 타입도 Integer라는 계약을 유지한다. 숫자를 썼다는 이유로 `List<Integer>`가 `List<int>`가 되거나 모든 사용에서 자동으로 primitive로 바뀌는 것은 아니다.

생성 부분을 new LinkedList<>()로 바꾸어도 이 연산들을 지원하는 같은 List 계약을 사용하므로 위의 의미를 유지할 수 있다. MyFavoriteList와 MyOwnList는 실제로 List를 구현한 사용자 클래스가 있다고 가정한 placeholder다. 이름만 적으면 구현이 저절로 생기지 않는다. 공통 API를 쓴다는 사실은 내부 저장 방식이나 성능이 같다는 뜻도 아니다. [NM001, PDF pp.33-35][NM001]

### `Comparable<T>`와 compareTo의 부호

**`Comparable<T>`** 는 객체에 순서를 부여할 때 선택하는 interface다. int compareTo(T obj)의 반환값이 양수면 receiver가 뒤쪽 또는 더 큰 쪽, 음수면 인자가 더 큰 쪽, 0이면 선택한 ordering에서 같은 위치다. 계약은 부호에 있으므로 반드시 1, -1만 반환해야 하는 것은 아니다. Object.equals로 동일성을 물을 수 있는 것과 모든 객체 종류에 자연스러운 순서가 있는 것은 다르다. NT001은 이 차이로 equals와 Comparable을 구별한다. Comparable을 구현해도 다른 superclass를 상속하거나 다른 interface를 함께 구현할 수 있다. [NT001, STT 05:25, 06:23, 07:23][NT001]

자료 보충인 Seagull은 flyingHeight와 numFriend를 보관하지만 compareTo는 높이만 비교한다.

~~~text
public int compareTo(Seagull seagull) {
    if (this.flyingHeight > seagull.flyingHeight) {
        return 1;
    } else if (this.flyingHeight == seagull.flyingHeight) {
        return 0;
    } else {
        return -1;
    }
}
~~~

높이와 친구 수가 각각 (10, 1), (3, 100)인 두 객체에서 첫째의 compareTo(둘째)는 10 > 3이므로 1이다. 친구 수 1 < 100은 이 ordering에 사용되지 않는다. 역방향은 -1이다. 높이가 같은 다른 두 객체는 친구 수가 달라도 0이다. 그러므로 p.37의 same은 모든 필드나 reference identity가 같다는 뜻으로 읽으면 안 된다. 이 Seagull은 equals override를 제공하지 않으므로 별도 두 객체가 compareTo에서는 0, 기본 equals에서는 false일 수 있다.

정렬·순서 기반 사용을 설계할 때는 어떤 속성의 같음을 ordering의 0으로 볼지와 equals의 의미가 일관되는지 살펴야 한다. 단지 Comparable이라는 이름만 붙이면 모든 collection의 모든 요구를 만족한다는 보장은 없다. [NM001, PDF pp.36-39, 46][NM001]

### String.compareTo의 사전식 계산

자료 보충의 **Lexicographic comparison(사전식 비교)** 는 앞에서부터 같은 위치의 문자를 비교한다. NM001의 구현 발췌는 두 길이 중 작은 값을 lim으로 정하고, k = 0부터 k < lim인 동안 비교한다. 처음 다른 c1, c2를 만나면 c1 - c2를 반환한다. lim까지 모두 같으면 len1 - len2를 반환한다. 먼저 문자열 전체 길이를 비교하거나 문자 코드의 총합을 비교하는 방식이 아니다. [NM001, PDF pp.40-41][NM001]

~~~text
"aaaaaa".compareTo("bbbbbb")  // 'a' - 'b' = -1
"bbbbbb".compareTo("aaaaaa")  // 'b' - 'a' = 1
"aaaaaa".compareTo("aaaaaa")  // 끝까지 같고 길이 차이 0
"bbbbbb".compareTo("bccccc")  // 첫 b는 같고 다음 b - c = -1
"bbbbbb".compareTo("BBBBBB")  // 첫 b - B = 98 - 66 = 32
~~~

마지막 결과 32가 양수라는 사실만으로도 순서를 알 수 있다. 1만 찾아 검사하는 코드는 compareTo 계약을 잘못 사용한 것이다. 공통 접두사 예를 더하면 "ab"와 "abc"는 앞 두 문자가 모두 같아서 길이 차이 2 - 3 = -1이 된다. "ab"가 먼저 온다. 이 접두사 예는 인쇄된 알고리즘을 설명하는 학습용 적용이다.

자료의 ASCII 언급은 위 영문 문자 계산에 맞지만 문화권별 사전 정렬 전체를 뜻하지 않는다. char[] value는 공급된 구현 발췌의 표현이며 모든 Java 버전이 같은 방식으로 String을 저장한다는 주장도 아니다. [NM001, PDF pp.41-42][NM001]

### Student 정렬에서 compareTo와 toString의 다른 책임

자료 보충의 또 다른 Student는 이름·ID 대신 double gpa만 보관하고 `Comparable<Student>`를 구현한다. 핵심 메서드는 다음과 같다.

~~~text
public int compareTo(Student anotherStudent) {
    double diff = gpa - anotherStudent.gpa;
    return diff > 0 ? 1 : diff < 0 ? -1 : 0;
}

@Override
public String toString() {
    return Double.toString(gpa);
}
~~~

보통의 유한 입력 3.3, 4.2, 3.1에 대해 3.3은 4.2보다 작고 3.1보다 크다. 세 Student를 add한 직후 목록의 GPA 순서는 [3.3, 4.2, 3.1]이고, Collections.sort(sList)는 compareTo의 오름차순에 맞추어 [3.1, 3.3, 4.2]로 재배치한다. add가 저장하고 sort가 기존 원소의 순서를 바꾼다. NM001 p.43의 sort로 “stored”한다는 표현을 원소 추가로 해석하면 안 된다.

toString은 각 Student를 GPA 문자열로 보여 주므로 println(sList)의 표현을 읽기 쉽게 만든다. 정렬 기준은 compareTo이며 toString의 글자 순서가 아니다. 예를 들어 toString의 표시 문구만 바꾸어도 compareTo가 같으면 이 예의 GPA 순서 기준은 유지된다. 이 수치는 가상 객체 예이지 학생 성적 통계가 아니다.

위 subtraction 구현을 NaN까지 포함한 모든 double의 완전한 순서로 일반화할 수는 없다. diff가 NaN이면 diff > 0과 diff < 0이 모두 false여서 0을 반환할 수 있다. 따라서 유한한 예시 값의 trace와 전체 수치 영역을 위한 비교 설계는 구별해야 한다. [NM001, PDF pp.43-45][NM001]

### Interface의 default/static body와 package access

Interface가 계약이라는 사실은 body를 절대로 가질 수 없다는 뜻이 아니다. NM001 p.47은 Java 8부터 default와 static 메서드에 body를 둘 수 있다고 명시한다. 자료 예의 boilWater는 body 없는 abstract 동작이고 clean은 다음 공통 구현이다.

~~~text
interface RamenCooker {
    void boilWater();

    default void clean() {
        System.out.println("Rinsing with water");
    }
}
~~~

구현 객체는 이 default 동작을 사용할 수 있고 필요하면 재정의할 수 있다. static 메서드의 body는 interface 자체와 연결된 동작이며 interface 이름을 통한 호출로 구별한다. 따라서 구체 클래스가 모든 메서드의 body를 매번 새로 작성해야 하는 것은 아니다.

여기의 **default method** 와 modifier를 생략한 **package access** 는 다르다. 앞의 default 키워드는 interface에 구현 body를 제공하는 기능이다. 뒤의 package access는 접근 범위다. NM001 pp.26-27, 54 및 NT001 08:22, 14:45의 body가 없다는 일반화는 기본 abstract-method 형태에 한정해야 하며 p.47의 예외를 지우면 안 된다. [NM001, PDF pp.26-27, 47, 54][NM001]; [NT001, STT 08:22, 14:45][NT001]

### Abstract class: 공통 상태와 구현, 남겨 둔 행동

**Abstract class(추상 클래스)** 는 공통 instance 상태와 구현을 공유하면서 일부 행동을 abstract method로 남길 수 있는 클래스다. abstract method를 선언한 클래스는 abstract여야 하며 직접 new로 인스턴스를 만들 수 없다. 반대로 abstract 클래스가 반드시 abstract method와 concrete method를 하나씩 모두 가져야 하는 것은 아니다. NT001 08:22에는 직접 생성이 가능한 것처럼 보이는 미확정 문장이 있으나, 생성 불가라는 기술 조건은 NM001 p.49에 명시되어 있다. Abstract class도 class이며 concrete class와 구별되는 것이다. [NM001, PDF p.49][NM001]; [NT001, STT 08:22, 11:03][NT001]

Person 자료 예에는 String description, String name, private int age가 있다. printName은 description과 name을 출력하고 ageOneYear는 age를 1 증가시킨 뒤 나이를 출력한다. work와 play는 다음처럼 body 없이 남긴다.

~~~text
abstract void work();
abstract void play();
~~~

공통 이름 출력과 나이 증가를 각 subclass에서 복사할 이유는 없다. 반면 어떤 Person인지 모르는 상태에서 work나 play에 임의의 기본 행동을 넣으면 그 행동이 맞지 않는 subclass까지 상속받을 수 있다. Abstract로 남기면 concrete subclass가 의미 있는 행동을 제공하도록 요구한다. description과 name은 modifier 생략에 따른 package 접근이고 age는 private다. Person의 메서드가 age를 관리하는 것과 자식이 age를 직접 읽는 것은 다르다. 자료 주석의 “non-field field”는 Java field 종류를 정의하는 정상 용어가 아니다. [NM001, PDF p.50][NM001]; [NT001, STT 09:13, 10:13, 13:48][NT001]

Student는 work에서 Study hard, play에서 Drink hard를 출력하고 BusinessMan은 work에서 Meeting all day, play에서 Go to the movies를 출력한다. 이는 가상 클래스의 행동 설정이다. 자료의 Person 변수 goodStudent와 busyMan은 실제 Student, BusinessMan을 각각 가리킨다. 올바른 초기화가 갖추어졌다는 의도 아래 p.53의 호출 결과를 순서대로 읽으면 다음과 같다.

~~~text
goodStudent.printName()   -> Good Student
busyMan.printName()       -> Busy Man
goodStudent.ageOneYear()  -> Student is now 26 years old.
busyMan.ageOneYear()      -> Man is now 35 years old.
goodStudent.work()        -> Study hard
busyMan.work()            -> Meeting all day
goodStudent.play()        -> Drink hard
busyMan.play()            -> Go to the movies
~~~

나이는 25에서 26, 34에서 35로 바뀐다. 그러나 pp.51-52의 subclass constructor가 호출하는 super(description, name, age)에 대응하는 세 인자 Person constructor는 p.50에 없다. 따라서 위 결과는 자료가 의도한 초기화와 행동의 trace이지 인쇄된 전체 코드를 그대로 실행한 결과가 아니다. 누락 constructor를 원래 있던 코드처럼 채워서는 안 된다. [NM001, PDF pp.50-53][NM001]

서로 관련 없는 종류에도 같은 연산을 요구하거나 이미 다른 superclass를 가진 클래스에 계약을 더할 때는 interface가 유용하다. 관련 클래스들이 instance field, 공통 초기화 constructor, protected helper, 메서드 구현을 공유할 때는 abstract class가 유용하다. Interface는 다른 interface를 extends할 수 있고, abstract class는 클래스를 extends하면서 interface를 implements할 수 있다. [NM001, PDF pp.54-55][NM001]; [NT001, STT 15:42, 16:41][NT001]

`List<E>` → `AbstractList<E>` → `ArrayList<E>` 구조도 역할을 나눈다. List가 공통 계약을 제공하고 AbstractList가 List를 implements하며 공통 구현을 제공한다. ArrayList는 AbstractList를 extends하여 구체 구현이 된다. ArrayList가 List와 관계없어진 것이 아니라 중간층을 통해 그 계약을 이어받는다. E는 모든 층에서 이어지는 이름 붙인 type parameter다. NM001 p.56은 Optional로 표시하지만 NT001 16:41, 17:36, 18:29, 19:24에서 이 구조의 의미를 설명한다. 실제 collection 알고리즘 전체가 제공된 것은 아니다. [NM001, PDF p.56][NM001]; [NT001, STT 16:41, 17:36, 18:29, 19:24][NT001]

기록된 답변의 설계 논점은 work와 play를 구현한 다음 abstract 제한을 없애면 보통 Person 클래스로도 만들 수 있다는 것이다. 그렇게 하면 Person 직접 생성과 부모의 기본 행동 상속이 가능해진다. Abstract로 남기는 선택은 의도하지 않은 직접 생성과 임의의 기본 동작을 막으며 설계상의 빈칸을 드러낸다. NT001 19:24 이후에 응답은 있지만 별도 학생 질문 본문은 없으므로 그 질문을 만들어 붙일 수는 없다. [NT001, STT 20:24, 21:11, 22:06, 23:03][NT001]

### Method signature와 반환형만 다른 선언

**Polymorphism(다형성)** 은 같은 이름의 행동을 서로 다른 방식으로 제공하는 관점이다. 자료의 makeNoise 그림은 같은 요청에 동물마다 다른 소리를 내는 동기를 보여 준다. printInt, printFloat, printString처럼 같은 출력 역할을 타입마다 다른 이름으로 만들면 호출자가 이름도 각각 기억해야 한다. 다만 의미가 비슷하다고 곧바로 overriding은 아니다. Animal.move()와 Fish.swim()은 이동이라는 의미가 관련되어도 이름이 다르다. 자료의 Animal a = new Fish();에서 a.move()는 상속된 move를 호출하고 ((Fish)a).swim()은 Fish에 추가된 별도 동작에 접근한다. [NM004, PDF pp.4-6][NM004]; [NT001, STT 23:58, 24:54, 25:54, 26:53][NT001]

이 예제 범위에서 Java **Method signature(메서드 시그니처)** 는 이름과 순서 있는 parameter type 목록으로 구분한다. parameter 변수 이름과 return type은 구별 기준이 아니다. 두 int parameter의 이름을 x, y에서 a, b로 바꾸어도 같은 signature다.

~~~text
int add(int a, int b)
int add(int a, int b, int c)
float add(float a, float b)
~~~

이 세 선언은 입력 개수 또는 타입이 달라 함께 둘 수 있다. 반면 int add(int a, int b)와 double add(int a, int b)는 반환형만 달라 공존할 수 없다. 호출 식 add(1, 2)의 이름과 입력만으로 서로를 구별할 수 없기 때문이다. 결과를 double 변수에 넣는다고 두 번째 선언을 선택하는 규칙이 생기지 않는다.

NM004 p.7은 일반적인 signature 표기에 반환형도 적지만 p.8과 NT001 27:51은 Java에서 반환형을 제외한다고 명시한다. **Overloading(오버로딩)** 은 같은 이름의 서로 다른 signatures를 제공하는 것이고, **Overriding(재정의)** 은 상속된 instance method와 같은 signature에 클래스별 구현을 제공하는 것이다. [NM004, PDF pp.7-9][NM004]; [NT001, STT 27:51, 28:51, 29:34, 30:30][NT001]

### 입력 타입별 같은 작업과 abs_add의 재사용

첫 overload 활용은 같은 작업을 다른 입력 타입으로 제공하는 것이다. NM004의 Point는 float x, y를 가지며 다음 두 메서드가 각각 좌표에 변위를 더한다.

~~~text
void move(int dx, int dy) {
    x += dx;
    y += dy;
}
void move(float dx, float dy) {
    x += dx;
    y += dy;
}
~~~

초기 좌표 (0.0, 0.0)에서 move(3, 0)은 int 두 개를 받는 선언을 골라 (3.0, 0.0)으로 이동한다. 이어 move(0.0f, 4.0f)는 float 두 개를 받는 선언을 골라 (3.0, 4.0)이 된다. 숫자 정밀도에 맞는 입력을 받으면서 이동이라는 의미를 유지한다. NM005 p.4에도 int/float 입력을 받는 두 move overload와 좌표를 표시하는 toString 예가 있다. 자료 보충의 타입·동작 비교이지 해당 lab의 실제 시연 기록은 아니다. [NM004, PDF pp.11-12][NM004]; [NM005, PDF p.4][NM005]

둘째 활용은 입력 모양이 달라도 밀접한 작업을 같은 이름에 묶는 것이다. Scalar 두 개의 abs_add는 두 절댓값의 합을 반환하고, 배열의 abs_add는 모든 원소의 절댓값 합을 반환한다.

~~~text
static double abs_add(double a, double b) {
    return Math.abs(a) + Math.abs(b);
}
static double abs_add(double[] arr) {
    double sum = 0;
    for (int index = 0; index < arr.length; ++index) {
        sum = abs_add(sum, arr[index]);
    }
    return sum;
}
~~~

배열 overload에서 sum은 0으로 시작한다. 보통의 유한 값에 대해 이미 누적한 sum이 음수가 아니므로 |sum| + |다음 원소|는 이전 절댓값 합에 다음 절댓값을 더한다. 학습용 적용으로 [-2.0, 3.0, -4.0]이면 sum은 0 → 2 → 5 → 9다. 인쇄된 1.0부터 10.0까지의 배열은 1 + 2 + … + 10 = 55이므로 반환값은 55.0이다.

Scalar 구현을 배열 구현이 호출하면 핵심 동작의 변경이 그 호출을 사용하는 배열 경로에도 반영된다. 이는 overload 사이의 호출에 의한 재사용이며 extends에 의한 상속이 아니다. NT001 34:41은 유지보수상의 이점과 함께 호출 비용을 언급하지만, 이 코드만으로 항상 느리다거나 실제 시간이 증가했다고 판단할 수 없다. 예시가 NaN, infinity, overflow까지 포함한 완전한 수치 계약을 제공하는 것도 아니다. [NM004, PDF p.13][NM004]; [NT001, STT 31:21, 32:15, 33:13, 34:10, 34:41][NT001]

### indexOf overload의 검색 시작 위치

추가 parameter는 기존 동작에 정보를 더할 수 있다. NM004의 DNA 예는 다음 문자열에서 "CGC"를 검색한다.

~~~text
String dna =
    "TACGAAGTTACTCGCTGTCAGATCGTAAGCGACGCGATCGTAATGTGAAT";
int first = dna.indexOf("CGC");
int second = dna.indexOf("CGC", first + "CGC".length());
System.out.println(first + ", " + second);
~~~

첫 indexOf는 처음 일치하는 부분의 시작 위치를 반환한다. zero-based index 12, 13, 14의 문자가 C, G, C이므로 first는 12다. 두 번째 호출은 first + 3, 즉 15부터 찾는다. index 32, 33, 34에서 다음 C, G, C가 있으므로 second는 32이고 출력 표현은 12, 32다. 두 번째 parameter는 “두 번째 일치를 달라”는 횟수가 아니라 검색을 시작하는 index다. 12를 그대로 주면 첫 일치가 여전히 범위에 있어 다시 12를 얻는다.

이 코드는 첫 일치 뒤 substring 길이만큼 건너뛰는 방식이다. 겹치는 모든 일치를 열거하거나 미발견(-1) 처리를 완성한 예는 아니다. NT001 35:41의 CCT와 36:41의 offset 없는 듯한 설명은 인쇄 코드의 CGC, + length와 다르며, 여기의 정확한 검색식은 자료에 근거한다. NM005 p.5는 indexof라고 인쇄하지만 Java 메서드 철자는 indexOf다. 서로 다른 출처의 표기를 조용히 하나로 고쳐 인용하지 않는다. [NM004, PDF p.14][NM004]; [NM005, PDF p.5][NM005]; [NT001, STT 35:41, 36:41, 37:41][NT001]

### 기본값 overload와 공통 body에 대한 위임

Parameter를 생략한 호출에 기본 동작을 제공할 수도 있다. NM004의 power 예는 다음과 같다.

~~~text
static double power(double input, int n) {
    if (n <= 0) return 1;
    return input * power(input, n - 1);
}
static double power(double input) {
    return power(input, 2);
}
~~~

power(2)는 한 parameter overload를 고른 뒤 power(2, 2)에 위임한다. 이는 2 × power(2, 1), 다시 2 × 2 × power(2, 0)이 되고 base case에서 1을 반환하여 4.0이다. power(2, 10)은 열 번 곱해 1024.0이다. 반환 타입이 double이므로 base case의 정수 1도 반환 시 double 값으로 사용된다.

n <= 0 조건은 음수에도 적용된다. 따라서 power(2, -1)은 1.0이지 수학적 역수 0.5가 아니다. 자료의 함수를 모든 정수 지수의 거듭제곱으로 일반화하면 안 된다. 한 parameter 메서드가 계산을 복제하지 않고 기본 지수 2를 전달하므로 핵심 구현을 한곳에서 관리할 수 있다. [NM004, PDF p.15][NM004]; [NT001, STT 38:38, 39:33][NT001]

debug 예도 같은 설계 원칙을 보여 준다. 기본 debug()는 "var 1 : "와 var1을 출력한다. debug(String s)의 첫 대안은 그 field 출력식을 다시 쓰고, 둘째 대안은 추가 문구를 출력한 뒤 기본 debug()를 호출한다.

~~~text
void debug() {
    System.out.println("var 1 : " + this.var1);
}

// 대안 A
void debug(String s) {
    System.out.println(s + "var 1 : " + this.var1);
}

// 대안 B
void debug(String s) {
    System.out.print("Output : " + s);
    debug();
}
~~~

A와 B는 둘 중 하나를 고르는 대안이다. 같은 클래스에 동시에 넣으면 같은 debug(String) signature가 중복된다. var1 = 0, s = "state: "라는 학습용 입력에서 A는 state: var 1 : 0, B는 Output : state: var 1 : 0을 출력한다. B에는 접두어가 더 있으므로 두 출력이 완전히 같은 것은 아니다. B의 장점은 기본 field 출력이 바뀌어도 위임한 쪽에서 그 변경을 함께 사용한다는 점이다. “한 overload가 주요 작업을 하고 나머지는 위임한다”는 것은 설계 원칙이며 모든 overload에 강제되는 문법 규칙은 아니다. [NM004, PDF p.16][NM004]; [NT001, STT 40:30, 41:23][NT001]

### Constructor overload: 문법적 구별과 좌표 의미

**Constructor(생성자)** 는 객체 초기화를 담당하는 특별한 선언이며 현재 클래스 이름을 사용하고 반환형을 적지 않는다. 서로 다른 parameter 목록으로 여러 초기화 경로를 제공할 수 있다. NM004 p.17의 Point()는 x = y = 0, Point(int, int)와 Point(float, float)는 입력을 Cartesian coordinates(직교좌표) x, y로 저장한다. 그런데 Point(double radius, double theta)는 polar coordinates(극좌표)로 해석한다.

~~~text
Point(double radius, double theta) {
    this.x = radius * Math.cos(theta);
    this.y = radius * Math.sin(theta);
}
~~~

반지름 radius와 각 theta로부터 x = radius cos(theta), y = radius sin(theta)를 계산한다. 수학적으로 radius = 2, theta = 0이면 x = 2 × 1 = 2, y = 2 × 0 = 0이다. 이 식의 각은 Math.cos/sin이 요구하는 radian 의미로 해석한다.

Point(2.0f, 0.0f)는 직교좌표 입력인데 Point(2.0, 0.0)는 극좌표 입력이 된다. Type 차이로 overload를 구별할 수 있다는 문법적 사실과, 호출자가 의미를 쉽게 예상할 수 있다는 API 설계 기준은 별개다. float에서 double로 정밀도만 바꾼다고 생각했는데 좌표계까지 바뀌면 오해하기 쉽다. NT001은 문자열이나 indicator 같은 명시적 구별을 더하는 설계를 제안하지만 새로운 필수 constructor 선언을 제공한 것은 아니다.

원자료에는 import Math;도 인쇄되어 있다. 이는 유효한 Math package 사용을 입증하지 못하는 잘못된 import 표기이며, Point가 그 package에 속한다는 뜻도 아니다. 위 식을 설명하는 것과 인쇄된 전체 코드가 그대로 완성 프로그램이라고 인증하는 것은 다르다. NT001의 “radians and theta”와 인쇄된 radius, theta도 구별한다. [NM004, PDF p.17][NM004]; [NT001, STT 41:23, 42:21, 43:12, 44:12][NT001]

### this(...)와 super(...): 초기화 위임과 순서

NM004 p.18은 좌표 대입을 수행하는 공통 constructor를 float 두 개를 받는 형태로 두고 다른 constructor가 그 경로에 위임한다. 다음은 자료의 constructor 관계를 보여 주는 발췌다.

~~~text
Point(float x, float y) {
    this.x = x;
    this.y = y;
}
Point(int x, int y) {
    this((float) x, (float) y);
}
Point() {
    this(0, 0);
}
~~~

무인자 생성 경로는 Point() → Point(int, int) → Point(float, float)다. this(0, 0)의 0은 int literal이므로 가운데 경로가 먼저 선택되고, 명시적 float cast를 거쳐 공통 좌표 대입에 도달한다. 위임받은 constructor가 끝난 뒤 호출한 constructor의 나머지 부분으로 돌아온다. 이는 새 객체 세 개를 만드는 과정이 아니라 한 객체의 초기화 경로다.

NT001 46:08의 0.0을 쓰겠다는 제안은 그대로 float literal이 아니다. 0.0은 double이고, 0.0f가 float다. p.18의 float/int constructor 목록에서 this(0.0, 0.0)는 자동 narrowing으로 float constructor를 선택하지 못한다. 앞 p.17의 double 극좌표 constructor가 이 목록에도 있다고 임의로 합치면 안 된다. 별도 학습용 호출 this(0.0f, 0.0f)는 float overload를 직접 고르는 예지만 이것이 원래 발화였다고 바꾸어 적을 수는 없다. [NM004, PDF p.18][NM004]; [M002, PDF pp.40-42][M002]; [NT001, STT 45:08, 46:08][NT001]

이 수업의 이전 Java 기준에서 명시적 this(...) 또는 super(...) constructor 호출은 constructor body의 첫 동작에 둔다. 먼저 위임된 초기화를 마친 다음 그 결과를 사용하는 순서를 확보하려는 것이다. NM004 p.19와 NT001 48:59, 49:57은 Java 25에서는 제한된 사전 작업을 허용한다고 별도로 언급한다. 따라서 첫 동작 규칙을 모든 버전에 대한 예외 없는 주장으로 만들지 않는다. 여기서는 그 새로운 문법의 상세를 추가하지 않는다. [NM004, PDF p.19][NM004]; [NT001, STT 47:08, 47:59, 48:59, 49:57][NT001]

this(...)는 같은 클래스의 다른 constructor로 위임하고 super(...)는 부모 constructor로 위임한다. 선택 선수자료 RM001의 Parent constructor가 Parent를 출력하고 Child constructor가 super() 후 Child를 출력하면 new Child()의 출력 순서는 Parent, Child다. 부모 초기화를 거쳐 자식 초기화로 돌아오기 때문이다. 명시적 위임이 없으면 부모의 무인자 constructor로 연결되는 경우도 있지만, 호출 가능한 부모 무인자 constructor가 있어야 한다. 부모 constructor를 동적으로 override하여 고르는 것은 아니다. [RM001, PDF pp.48-50][RM001]

### Ambiguous overloading과 most-specific 선택

Overload 선언들의 signature가 다르다고 모든 호출이 유일하게 결정되는 것은 아니다. ColoredPoint extends Point이면 ColoredPoint 값을 Point parameter에도 전달할 수 있다. NM004 pp.20-21에는 다음 두 후보가 있다.

~~~text
static void test(ColoredPoint p, Point q) {
    System.out.println("(ColoredPoint, Point)");
}
static void test(Point p, ColoredPoint q) {
    System.out.println("(Point, ColoredPoint)");
}
~~~

ColoredPoint cp = new ColoredPoint(); 뒤 Test.test(cp, cp)를 부르면 양쪽 모두 적용 가능하다. 첫 후보는 첫 자리에서 더 구체적이고, 둘째 후보는 둘째 자리에서 더 구체적이다. 한 후보의 전체 parameter 목록이 다른 후보보다 더 구체적이라고 결정되지 않으므로 compile-time ambiguity(모호성)다. 원자료에도 reference to test is ambiguous라는 오류가 있다. [NM004, PDF pp.20-21][NM004]

Pp.22-23은 둘째 선언을 test(ColoredPoint, ColoredPoint)로 바꾼다. 이제 첫 자리에서는 두 후보가 같고 둘째 자리에서 새 후보가 Point보다 구체적이다. 같은 test(cp, cp)에는 새 후보가 선택되어 (ColoredPoint, ColoredPoint)를 출력한다. 이것은 선언 순서가 빠른 메서드나 위에서 먼저 발견한 메서드를 실행하는 규칙이 아니다. NT001 52:44의 먼저 matches한다는 구두 표현은 이 **Most-specific(가장 구체적인)** 타입 관계를 설명하는 축약으로 한정해야 한다. [NM004, PDF pp.22-23][NM004]; [NT001, STT 50:55, 51:49, 52:44][NT001]

### Instance overriding, 반환형과 constructor의 차이

Overriding은 상속된 instance method의 호출 약속을 유지하면서 subclass의 동작을 바꾸거나 확장한다. NM004의 Employee는 public double getSalary()에서 180을 반환하고 Manager는 같은 signature에서 250을 반환한다. Employee 객체의 결과는 180.0, Manager 객체의 결과는 250.0이다. @Override는 compiler가 재정의 의도와 선언의 관계를 확인하도록 하는 annotation이다. annotation이 별도의 overload를 만드는 것은 아니다. 메서드 이름을 잘못 쓰거나 parameter 목록을 달리하여 override하지 못하면 이를 발견하는 데 도움이 된다. [NM004, PDF pp.25-26][NM004]; [NT001, STT 53:49, 54:47][NT001]

Laidoff의 첫 대안은 double getSalary()로 0을 반환한다. 둘째 대안은 int getSalary()다. 부모의 반환형 double을 int로 바꾼 둘째 선언은 반환형별 overload가 아니라 호환되지 않는 override이므로 compile-time error다. 정수 값 0을 double 메서드에서 반환할 수 있다는 것과 메서드 선언의 반환 타입 자체를 int로 바꿀 수 있다는 것은 다르다. 원자료 p.28의 diagnostic도 return type int is not compatible with double이라고 명시한다.

자료와 NT001의 반환형이 같아야 한다는 일반화는 여기의 primitive int/double 사례에 맞추어 읽는다. 이 예만으로 모든 reference return도 반드시 글자 그대로 같은 타입이어야 한다고 확대하면 안 된다. P.27의 두 Laidoff 정의는 서로 비교하는 대안이고, pp.26, 28 출력식에는 잘못된 닫는 quotation mark도 있다. 이 인쇄 오류까지 포함한 전체를 그대로 성공 실행 코드로 제시하지 않는다. NM005 p.6의 public string toString()도 Java에서는 String이어야 하는 원자료 철자 오류다. [NM004, PDF pp.27-28][NM004]; [NM005, PDF p.6][NM005]; [NT001, STT 55:45, 56:45][NT001]

Constructor는 상속되는 instance method가 아니므로 override하지 않는다. Manager는 자기 초기화를 Manager()에 선언한다. Manager 안에 반환형 없는 Employee()를 넣어 부모 constructor를 재정의할 수 없다. 부모 초기화가 필요하면 super(...)로 연결한다. Constructor overload는 같은 클래스의 초기화 경로 선택이고, constructor chaining은 초기화 순서이며, instance overriding은 이미 존재하는 receiver에 대한 동작 선택이다. [NM004, PDF p.32][NM004]; [NT001, STT 01:02:14][NT001]

### instanceof와 getClass 분기를 overriding과 비교하기

자료의 HumanResources.getSalary(Employee e)는 static helper 안에서 e instanceof Executive이면 960, e instanceof Manager이면 250, 그 외에는 180을 반환한다. 이 방식은 객체별 override를 호출하는 대신 helper가 타입을 알아보고 값을 고르는 것이다. 수치는 단위 없는 예시이며 실제 임금 정보가 아니다. [NM004, PDF p.29][NM004]; [NT001, STT 57:38, 58:34][NT001]

**instanceof** 는 실제 객체가 해당 타입 또는 하위 타입에 해당하는지를 검사한다. 따라서 subclass 관계에 따라 검사 순서가 중요할 수 있다. 예를 들어 Executive가 Manager의 하위 타입인 계층이라면 Manager를 먼저 검사할 때 Executive도 그 branch에 들어갈 수 있다. 이는 검사 순서의 영향을 설명하는 학습용 가정이며 원자료가 그 상속 관계를 새로 명시했다는 뜻은 아니다.

다른 자료 예는 e.getClass().getName()을 switch하여 "personnelpkg.Executive", "personnelpkg.Manager"라는 정확한 클래스 이름 문자열에 맞춘다. getClass는 객체의 실제 클래스를 나타내며 superclass 이름을 알아내는 메서드가 아니다. 새로운 Manager subtype의 객체는 instanceof Manager를 만족할 수 있지만 실제 클래스 이름은 그 subtype 이름이므로 Manager 문자열과 일치하지 않을 수 있다. getClass를 사용하려면 receiver가 non-null이어야 한다는 호출 조건도 있다. [NM004, PDF p.30][NM004]; [NT001, STT 01:00:18][NT001]

CEO, Cleaner, Researcher처럼 종류가 늘고 급여·근무시간·장소를 다루는 helper가 여러 개이면 각 분기 목록을 함께 갱신해야 한다. 누락된 타입은 기본 branch로 잘못 처리될 수 있다. Overriding은 각 클래스가 자신의 동작을 책임지고 caller는 같은 메서드를 호출하도록 하는 대안이다. 원본 p.31의 마지막 else에는 반환문의 구두점 오류도 있으므로 그대로의 완성 코드로 인증하지 않는다. 이런 유지보수 비교가 instanceof나 getClass의 모든 사용을 금지한다는 규칙은 아니다. 이름 문자열을 검사하는 예도 실제로 Executive와 Manager를 생성하므로 클래스 의존성이 사라졌다고 할 수 없다. [NM004, PDF pp.29-31][NM004]; [NT001, STT 59:24, 01:01:17][NT001]

### Field hiding과 RealPoint의 네 출력

**Field hiding(필드 숨김)** 은 부모의 field를 없애고 하나의 field로 재정의하는 것이 아니다. NM004 p.34의 Point.static int x = 2와 Test.static double x = 4.7은 별도 선언이다. Test의 instance method 안에서 x, super.x, ((Point)this).x를 읽으면 차례로 4.7, 2, 2다. 이 cast는 같은 객체를 Point 타입의 식으로 보아 부모 field를 선택하게 한다. Field 선택을 instance overriding처럼 해석하면 안 된다. [NM004, PDF p.34][NM004]; [NT001, STT 01:03:10, 01:04:09][NT001]

이제 자료 보충인 RealPoint 예를 전체 메커니즘으로 읽는다. Point와 RealPoint의 관련 선언은 다음과 같다.

~~~text
class Point {
    int x = 0, y = 0;
    int color;
    int getX() { return x; }
    int getY() { return y; }
    void move(int dx, int dy) { x += dx; y += dy; }

    static void show(int x, int y) {
        System.out.println("(" + x + ", " + y + ")");
    }
    static void show(float x, float y) {
        System.out.println("(" + x + ", " + y + ")");
    }
}

class RealPoint extends Point {
    float x = 0.0f, y = 0.0f;

    void move(int dx, int dy) {
        move((float)dx, (float)dy);
    }
    void move(float dx, float dy) {
        x += dx;
        y += dy;
    }
    int getX() { return (int)Math.floor(x); }
    int getY() { return (int)Math.floor(y); }
}
~~~

RealPoint의 float x, y는 Point의 int x, y와 별개다. move(int, int)는 같은 signature의 부모 instance method를 override한다. move(float, float)는 다른 signature인 overload다. getX/getY도 부모 메서드를 override하며 자식 float 좌표에 Math.floor를 적용하고 int로 돌려준다. floor는 내림이므로 음수에서는 단순 소수부 제거와도 다르다. 예컨대 floor(-1.2)는 -2다. [NM004, PDF pp.35-36][NM004]

~~~text
RealPoint rp = new RealPoint();
Point p = rp;

rp.move(1.71828f, 4.14159f);
p.move(1, -1);

Point.show(p.x, p.y);
Point.show(rp.x, rp.y);
Point.show(p.getX(), p.getY());
Point.show(rp.getX(), rp.getY());
~~~

rp와 p는 객체 하나를 가리킨다. 첫 호출은 rp의 선언 타입 RealPoint에서 float 두 개의 signature를 선택하여 자식의 float fields를 바꾼다. 둘째 호출은 p의 선언 타입 Point에서 move(int, int)를 고른다. 그러나 이 메서드는 instance method이므로 실제 RealPoint의 override에 들어가며, 그 body가 1과 -1을 float로 바꾸어 float overload에 위임한다. 따라서 두 이동 모두 자식의 좌표를 바꾸고 부모 int 좌표는 (0, 0)으로 남는다.

자식 좌표는 float 연산으로 x에 1.71828f와 1.0f, y에 4.14159f와 -1.0f를 더한 값이다. 자료가 제시하는 소수 표현은 (2.7182798, 3.14159)다. 십진수로 이상적으로 계산한 2.71828과 표현이 조금 다른 이유는 float가 이 값들을 유한한 이진 정밀도로 저장하기 때문이다.

첫 show의 p.x, p.y는 Point의 int fields이므로 show(int, int)를 골라 (0, 0)을 출력한다. 둘째의 rp.x, rp.y는 RealPoint의 float fields이므로 show(float, float)를 골라 (2.7182798, 3.14159)를 출력한다. 셋째와 넷째는 모두 실제 RealPoint의 getter override를 실행하고 반환 타입은 int다. 각각 바닥값 2, 3을 얻어 show(int, int)에 전달하므로 나머지 두 출력은 모두 (2, 3)이다.

같은 객체인데 p.x는 0, p.getX()는 2인 이유는 field 접근이 선언 타입을 따르고 instance method는 실제 receiver의 override를 따르기 때문이다. NT001은 두 move가 바꾸는 대상까지 설명하지만 01:09:54에서 네 show의 상세 풀이를 생략한다. 위의 완전한 네 출력 추적은 NM004 pp.35-37에 근거한 자료 보충이다. 구두의 double 표현과 달리 인쇄 코드의 타입은 float다. [NM004, PDF pp.35-37][NM004]; [NT001, STT 01:05:06, 01:06:05, 01:07:02, 01:07:58, 01:08:57, 01:09:54][NT001]

### Compile-time overload 선택 후 runtime receiver dispatch

수업 용어의 **Static/syntactic polymorphism** 은 compile time에 호출 형태를 선택하는 경우이며, **Dynamic/pure polymorphism** 은 실행 중 실제 receiver에 따라 override 구현을 선택하는 경우다. “static polymorphism”이란 말이 모든 관련 메서드 선언에 static 키워드가 붙는다는 뜻은 아니다. Instance method도 overload되면 signature 선택은 컴파일 때 이루어진다. [NM004, PDF p.39][NM004]; [NT001, STT 01:11:50, 01:12:45][NT001]

Polynomial 자료의 네 후보는 times(Polynomial), times(int), times(float), times(Polynomial, int)다. 다음 세 호출에서 선택되는 목록은 차례로 (int), (float), (Polynomial, int)다.

~~~text
poly.times(9);
poly.times(85.2f);
poly.times(new Polynomial("2.95 * x + 22"), 3);
~~~

P.41 그림은 선언에서 signature를 추출하여 method table에 연결하고 각 호출의 인자 타입을 해당 목록과 대응시킨다. 이 설명은 overload의 선택이 컴파일 때 정해진다는 뜻이다. 모든 overloaded body가 생성 코드에서 삭제된다는 뜻은 아니다. Polynomial constructor의 문자열 해석이나 실제 곱셈 body가 제공되지 않았으므로 다항식 계산 결과를 만들 수는 없다. [NM004, PDF pp.40-41][NM004]; [NT001, STT 01:13:39, 01:14:31, 01:15:28, 01:16:18][NT001]

Employee e = new Manager(); e.getSalary();에서는 먼저 Employee 타입이 허용하는 getSalary() 호출인지 검사한다. 그다음 실제 Manager 객체의 override body를 실행한다. Pp.42-43 그림은 실제 객체의 현재 클래스에서 구현을 찾고 없으면 직접 superclass를 따라 Object까지 올라가는 관계, 선택된 method data에서 code location을 참조하는 관계, 실제 code를 실행하는 관계를 보여 준다. “getSalary라는 클래스”를 찾는 것이 아니라 메서드 구현을 선택하는 것이다. Method Area, RT constant pool, Heap Memory 상자의 배치와 화살표는 개념도다. 모든 JVM의 물리 저장 배치, 매 호출의 선형 검색, 항상 더 큰 호출 비용을 확정하지 않는다. Compiler가 선언 타입을 모르거나 아무 검사도 할 수 없다는 뜻도 아니다. [NM004, PDF pp.42-43][NM004]; [NT001, STT 01:17:13, 01:18:07][NT001]

두 선택을 한 번에 구별하는 다음 **학습용 Java 예**는 위 규칙들을 결합한 예이며 원자료의 별도 Animal/Dog 소스를 복원한 것이 아니다. inspect의 두 static overload body와 Dog의 instance override body를 모두 읽어야 결과를 알 수 있다.

~~~text
class Animal {
    static String kind() {
        return "Animal.kind";
    }
    String sound() {
        return "Animal.sound";
    }
}
class Dog extends Animal {
    static String kind() {
        return "Dog.kind";
    }
    @Override
    String sound() {
        return "Dog.sound";
    }
}
class DispatchExample {
    static void inspect(Animal a) {
        System.out.println("inspect(Animal): " + a.sound());
    }
    static void inspect(Dog d) {
        System.out.println("inspect(Dog): " + d.sound());
    }

    public static void main(String[] args) {
        Animal a = new Dog();
        Dog d = new Dog();

        inspect(a);
        inspect(d);
        inspect((Animal)d);
        System.out.println(a.kind());
        System.out.println(d.kind());
        System.out.println(((Animal)d).kind());
        System.out.println(((Animal)d).sound());
    }
}
~~~

inspect(a)는 인자 식 a의 선언 타입이 Animal이므로 inspect(Animal)을 선택한다. 그 body 안의 a.sound()는 실제 Dog receiver에 동적으로 dispatch되어 Dog.sound를 반환한다. 따라서 첫 줄은 inspect(Animal): Dog.sound다. inspect(d)는 inspect(Dog)를 선택하고 역시 Dog.sound를 호출하므로 둘째 줄은 inspect(Dog): Dog.sound다. inspect((Animal)d)는 cast 식의 타입이 Animal이므로 셋째 줄은 inspect(Animal): Dog.sound다. 인자의 실제 객체가 Dog라고 첫 overload가 나중에 inspect(Dog)로 바뀌지는 않는다.

그다음 세 kind 호출은 static hiding이다. a.kind()는 Animal.kind, d.kind()는 Dog.kind, ((Animal)d).kind()는 Animal.kind다. static을 객체 변수로 쓴 형태의 의미를 비교한 것이며 클래스 이름으로 호출하면 선택 기준이 더 잘 보인다. 마지막 ((Animal)d).sound()는 cast 후에도 같은 Dog 객체의 instance method를 호출하므로 Dog.sound다. 예상되는 일곱 출력은 다음과 같다.

~~~text
inspect(Animal): Dog.sound
inspect(Dog): Dog.sound
inspect(Animal): Dog.sound
Animal.kind
Dog.kind
Animal.kind
Dog.sound
~~~

Cast가 식의 타입을 바꾸면 overload나 static/field 선택에 영향을 줄 수 있지만 객체를 다른 클래스로 바꾸거나 부모 instance body로 강제로 되돌리지는 않는다. 선택 선수자료 RM001의 T3 객체도 ((T2)this).s(), ((T1)this).s()가 모두 T3의 "3"을 반환한다. 부모의 특정 body를 부르는 super.s()와는 다른 동작이다. [RM001, PDF pp.37-39, 46-47][RM001]

### 내장 operator의 operand 타입과 평가 방식

Java는 같은 기호에 대해 operand 타입별로 정해진 동작을 제공하지만 사용자가 자기 클래스에 임의의 operator overload를 정의할 수는 없다. 숫자 10 + 20은 30, 1.5 + 2.0은 3.5다. String이 포함된 "10" + "20"은 "1020"이고 "sum = " + 30은 "sum = 30"이다. [NM004, PDF pp.44-45][NM004]; [NT001, STT 01:19:07][NT001]

물리 PDF p.44의 삽입 그림에는 다음 String 예도 있다.

~~~text
String s = "Dog" + " barks.";
s += "Too Loud!";
~~~

첫 값은 "Dog barks."이고 두 번째 대입 후 값은 "Dog barks.Too Loud!"다. 첫 문자열 끝이나 두 번째 문자열 앞에 추가 공백이 없으므로 마침표 바로 뒤에 Too가 붙는다. +=는 연결 결과를 다시 s에 대입한다. 불변 String 객체 자체를 제자리에서 수정하는 것이 아니다.

같은 그림의 원문 float f = 0.5 % 0.3;은 타입 오류를 포함한다. 접미사 없는 0.5와 0.3은 double literal이므로 % 결과도 double이고 float 변수에 그대로 대입할 수 없다. 자료와 별도인 학습용 수정 예 double f = 0.5 % 0.3;은 결과 변수 타입을 맞춘 것이다. 부동소수점 operand에도 remainder 연산을 사용한다는 의미는 살리되 이진 표현 때문에 결과가 정확한 십진수 0.2라고 보장하지 않는다. 이는 원래 선언을 조용히 고쳐 인용한 것이 아니다. [NM004, PDF p.44][NM004]; [M002, PDF pp.40-42][M002]

정수 &와 |는 각 비트에 적용된다. 작은 양의 정수 예에서 6은 110, 3은 011이다. AND하면 010, 즉 2이고 OR하면 111, 즉 7이다. Boolean true & false는 false, true | false는 true다. 다만 boolean의 single &와 |는 양쪽 operand를 모두 평가한다. &&는 왼쪽 false에서 오른쪽을 생략하고, ||는 왼쪽 true에서 오른쪽을 생략하는 short-circuit evaluation(단락 평가)이다. [NM004, PDF p.46][NM004]

역사적 기초 설명(T007, STT 24:17)과 자료 M002의 다음 guard는 그 차이를 보여 준다.

~~~text
int denominator = 0;
int num = 100;
if (denominator != 0 && num / denominator == 1) {
    // 조건이 참일 때만 수행할 부분
}
~~~

왼쪽 denominator != 0이 false라서 오른쪽 정수 나눗셈을 평가하지 않는다. &&를 &로 바꾸면 오른쪽도 평가하여 0으로 나누는 문제가 생긴다. 결과의 논리값만 비슷하다고 평가 과정까지 같은 것은 아니다. ||도 왼쪽 true이면 오른쪽의 side effect나 오류 가능성이 있는 식을 평가하지 않는다. NT001 01:20:06의 불명확한 operator 발음을 새 토큰으로 복원하는 대신, 여기서는 명확한 인쇄 기호와 과거 기초 설명에 근거해 구별한다. [M002, PDF pp.66-70][M002]; [NT001, STT 01:20:06][NT001]

### Upcast와 downcast: 객체, 접근 가능한 메서드와 실패 시점

**Cast(형 변환)** 는 여기서 참조를 어떤 타입의 식으로 사용할지 지정한다. Cast는 객체의 실제 클래스를 바꾸지 않으며 원래 변수의 선언 타입도 다시 쓰지 않는다. NM004의 계층 Animal → Mammal → Dog → Beagle에서 Dog dog = new Beagle();의 객체는 Beagle이다. (Mammal)dog와 (Animal)dog는 상위 타입으로 보는 upcast이고, (Beagle)dog는 실제 객체가 Beagle이므로 가능한 downcast다. 모두 같은 객체를 가리킨다. [NM004, PDF p.47][NM004]; [NT001, STT 01:22:07][NT001]

**Upcasting(상향 형 변환)** 은 구체 구현을 상위 계약으로 다루게 한다. Employee e = (Employee)(new Executive());와 Employee e = new Executive();는 명시적·암시적 upcast의 비교다. Animal a = new Beagle();도 구체 종류를 몰라도 Animal 계약으로 사용하는 방식이다. 제시된 상속 관계에서 상위 타입 참조에 하위 객체를 넣는 것은 그 객체를 잘라 내거나 부모 객체로 복사하는 연산이 아니다. [NM004, PDF p.48][NM004]; [NT001, STT 01:23:05][NT001]

**Downcasting(하향 형 변환)** 은 실행 중 실제 객체가 목표 타입 또는 그 하위 타입인지 확인해야 한다. 아래 두 경우는 실패 이유와 시점이 다르다. 이 Life/Animal은 앞 학습용 DispatchExample의 Animal과 독립된 자료 예다.

~~~text
class Life {
    public void breed() { }
}
class Animal extends Life {
    public void move() { }
}

// 경우 A
Life mylife = new Life();
((Animal)mylife).move();
~~~

관련 타입 사이이므로 cast 표현을 쓸 수는 있지만, 실제 객체는 Life이지 Animal이 아니다. 실행 시 cast에서 ClassCastException이 발생하며 move까지 도달하지 못한다. 하위 클래스에 어떤 메서드가 있다는 이유로 부모 객체에 그 기능이 생기지 않는다. [NM004, PDF p.49][NM004]

~~~text
// 경우 B
Life mylife = new Animal();
mylife.move();           // compile-time error인 호출
((Animal)mylife).move(); // 앞의 잘못된 호출을 제외하고 보면 가능한 호출
~~~

경우 B의 실제 객체는 Animal이다. 그러나 mylife의 선언 타입 Life에는 move가 없으므로 첫 호출은 compile time에 허용되지 않는다. 런타임까지 기다렸다가 객체를 보고 이 호출을 허용하는 방식이 아니다. 잘못된 첫 줄을 제외하고 둘째 줄을 보면 Animal cast가 실제 객체와 맞고 move에 접근할 수 있다. 두 줄을 그대로 한 프로그램에 두고 둘째 줄만 실제 실행됐다고 설명해서는 안 된다. [NM004, PDF p.50][NM004]; [NT001, STT 01:23:53, 01:24:50][NT001]

안전 조건을 드러내는 학습용 형태는 다음과 같다.

~~~text
if (mylife instanceof Animal) {
    Animal animal = (Animal)mylife;
    animal.move();
}
~~~

이 검사에서 null은 false이므로 body에 들어가지 않는다. 참고로 null reference 자체를 Animal로 cast하는 것은 null을 얻지만 그 뒤 move를 호출할 receiver는 없으므로 NullPointerException이다. 이 역시 객체의 클래스 불일치로 생기는 ClassCastException과 구별된다. 상위 타입으로 cast해도 instance override는 유지되며, 접근 범위 같은 컴파일 조건까지 cast가 없애 주지는 않는다. [RM001, PDF pp.37, 39-43][RM001]

### Generics: 타입 자리를 남겨 두는 동기

**Generics(제네릭)** 는 메서드·클래스·interface에 **Type variable(타입 변수)** 를 두어 여러 타입에 공통 구조를 적용하는 방식이다. 자료는 이를 **Parametric polymorphism(매개변수 다형성)** 이라고 부른다. 구체 타입마다 거의 같은 구조를 반복하기보다 타입의 자리를 남겨 두고 사용 시 그 자리에 타입을 지정하려는 동기다. [NM004, PDF p.52][NM004]; [NT001, STT 01:25:47][NT001]

앞의 `List<E>`에서 E는 이름 붙인 type parameter다. `List<Integer>`는 그 자리를 Integer로 정한 사용이고 `List<String>`은 String으로 정한 사용이다. `AbstractList<E>` implements `List<E>`에서 같은 E를 유지하는 것은 공통 구현과 interface 계약이 같은 원소 타입을 연결한다는 뜻이다. E를 임의로 Object로 바꾸거나 primitive로 자동 unboxing하는 표기로 읽으면 안 된다. 또한 어떤 클래스 A가 B의 하위 타입이라는 이유만으로 `List<A>`를 `List<B>`로 자동 취급할 수 있다는 뜻도 아니다. 이런 변환 규칙은 이 짧은 도입에서 제공하지 않는다.

**Wildcard(와일드카드)** 의 표기는 ?이며 이름 붙인 E와 구별한다. Collection<?>는 어떤 특정 원소 타입인지 여기서 이름 붙이지 않은 collection을 표현한다는 정도로 읽는다. 아무 타입의 값이나 그 안에 넣거나 아무 연산을 할 수 있다는 뜻은 아니다. NT001 16:41의 E를 wildcard라고 한 표현과 01:26:45의 물음표에 대한 넓은 표현을 정확한 타입 규칙으로 채택하지 않는다. 이 구별은 자료 측 표기와 의미에 근거한 한정이다. [NM001, PDF p.56][NM001]; [NM004, PDF p.66][NM004]

NT001 01:25:47의 arbitrary type “during runtime”이라는 표현은 NM004 p.59의 compile-time 타입 검사 설명과 충돌한다. 실행 중 임의 타입으로 자유롭게 바뀐다는 규칙으로 받아들일 수 없다. 반대로 자료 p.59와 NM005 p.8의 모든 runtime type error가 사라진다는 주장도 과도하다. 타입 계약에 맞지 않는 일부 사용을 컴파일 때 발견한다는 이점과 모든 실행 오류가 없다는 보장은 다르다.

NT001 01:26:45는 generics 상세를 다음 시간에 다루겠다고 남긴다. 따라서 현재 설명은 타입 placeholder와 E/? 구별, 재사용 동기까지다. Generic class·method·constructor의 상세 구현, static member의 타입 변수 제한, bounds와 wildcard 연산, Producer-Consumer와 Scheduler 구현은 이 강의 기록에 포함시키지 않는다. 전체 자료에 후속 코드가 있다는 사실로 이 강의에서 모두 설명했다고 볼 수 없다. [NM004, PDF pp.52, 59][NM004]; [NM005, PDF p.8][NM005]; [NT001, STT 01:25:47, 01:26:45][NT001]

[NM001]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf
[NM004]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf
[NM005]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf
[M002]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf
[RM001]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf
[NT001]: https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2

## 회상·연습문제

### 일반 회상 문제

#### 회상 Q01 Static hiding과 instance overriding

다음은 서로 독립된 두 정의다. 각 정의에서 호출 네 개의 출력과 선택 근거를 순서대로 쓰라. Compiler가 아는 declared type과 실제 receiver를 구별하고, private/final 메서드도 같은 방식으로 override할 수 있는지 설명하라.

~~~text
// 정의 S
class Parent { static void print() { System.out.println("P-static"); } }
class Child extends Parent {
    static void print() { System.out.println("C-static"); }
}
Parent p = new Parent();
Parent c = new Child();
Child d = new Child();
p.print(); c.print(); d.print(); ((Parent)d).print();

// 정의 I: 위 클래스들과 별도로 사용
class Parent { void print() { System.out.println("P-instance"); } }
class Child extends Parent {
    @Override void print() { System.out.println("C-instance"); }
}
Parent p = new Parent();
Parent c = new Child();
Child d = new Child();
p.print(); c.print(); d.print(); ((Parent)d).print();
~~~

[NM001, PDF pp.3-7][NM001]; [NT001, STT 00:48][NT001]

<details><summary>정답</summary>

정의 S의 출력은 P-static, P-static, C-static, P-static이다. Static method는 class에 속하고 Child의 선언은 Parent의 선언을 hide한다. p와 c는 Parent, d는 Child, cast 식은 Parent 타입이므로 그 타입에서 선택한다. 실제 객체가 Child여도 static 호출이 그 객체의 구현으로 dispatch되지 않는다.

정의 I의 출력은 P-instance, C-instance, C-instance, C-instance이다. 호출 가능한 print() signature는 선언 타입으로 검사하고, 그 signature의 body는 실제 receiver를 따른다. p만 Parent 객체이고 나머지는 Child 객체다. Cast는 d의 객체를 바꾸지 않으므로 마지막도 Child의 override다.

Compiler는 p/c/d의 선언 타입을 안다. NM001 p.3의 선언 타입을 컴파일 때 모른다는 문장은 이 규칙이 아니다. 실행 중 달라질 수 있는 receiver의 class와 선언 타입을 혼동하면 안 된다. Private method는 상속된 override 대상이 아니며 final method도 override할 수 없다. 확인할 점은 static hiding과 instance overriding을 같은 선택 규칙으로 설명하지 않는 것이다.

</details>

#### 회상 Q02 객체 배열의 slot, null과 draw

Shape의 instance draw()를 Circle과 Square가 각각 override하여 "Circle", "Square"를 출력한다고 하자.

~~~text
Shape[] shapes = new Shape[3];
shapes[0] = new Square();
shapes[2] = new Circle();
for (int i = 0; i < shapes.length; i++) {
    if (shapes[i] != null) shapes[i].draw();
}
~~~

배열 생성 직후와 두 대입 후의 slot 값을 구별하고 출력 순서를 쓰라. Null 검사를 없애면 어느 index에서 왜 멈추는가? 각 slot을 randShape()로 채우되 (int)(Math.random()*2)가 0이면 Circle, 1이면 Square를 반환한다면, 가능한 두 선택과 출력 순서를 미리 고정할 수 없는 이유도 설명하라.

[NM001, PDF pp.8-9][NM001]

<details><summary>정답</summary>

배열 생성 직후는 [null, null, null]이다. 배열 객체와 reference slot 세 개를 만들었으며 도형 객체 세 개를 자동 생성한 것은 아니다. 두 대입 후는 [Square 객체의 참조, null, Circle 객체의 참조]다.

Loop는 index 0, 1, 2를 방문한다. 0에서는 실제 Square의 draw, 1에서는 검사 후 생략, 2에서는 실제 Circle의 draw를 호출하므로 출력은 Square 다음 Circle이다. 원소 식의 공통 타입은 Shape지만 구현 선택은 각 non-null 객체를 따른다.

검사를 없애면 Square를 출력한 뒤 index 1에서 NullPointerException이 발생한다. Null에는 instance method를 받을 객체가 없으므로 index 2에 도달하지 못한다.

Math.random()의 범위 0 이상 1 미만을 2배하면 0 이상 2 미만이고, 이 비음수 값을 int로 바꾸면 0 또는 1이다. 모든 slot을 채웠다면 각 출력은 Circle 또는 Square지만 특정 순서를 보장하지 않는다. 자료의 네 줄은 sample 하나다. 확인할 점은 배열의 원소 타입, slot의 값, 실제 도형의 class를 세 가지로 구분하는 것이다.

</details>

#### 회상 Q03 toString의 반환값과 객체의 표현

다음 Badge는 가상의 표시용 값만 사용한다.

~~~text
class Badge {
    String group, role;
    int number;
    Badge(String group, String role, int number) {
        this.group = group; this.role = role; this.number = number;
    }
    @Override public String toString() {
        return String.format("%s/%s:%d", group, role, number);
    }
}
Object a = new Badge("A", "reader", 6);
Object b = new Badge("A", "reader", 6);
System.out.println("badge=" + a);
System.out.println(a.toString());
~~~

두 출력, toString의 정확한 반환 계약, 표현 책임을 객체에 두는 이점을 설명하라. a가 String 객체로 cast된 것인지, 두 표현이 같으면 a.equals(b)도 true인지 판단하라. toString을 void 메서드로 바꾸어 내부에서 출력만 해도 되는가? File 객체의 문자열 표현을 출력하는 것과 파일 내용을 읽는 것도 구별하라.

[NM001, PDF pp.12-18][NM001]; [NT001, STT 00:48, 01:48][NT001]

<details><summary>정답</summary>

출력은 badge=A/reader:6, 다음 줄 A/reader:6이다. %s, %s, %d에 group, role, number가 차례로 들어간다. Object 타입 참조를 사용해도 실제 Badge의 override가 문자열 표현을 제공한다.

계약은 public String toString()이다. 호출자가 매번 세 필드를 조합하지 않아도 한곳에 정한 표현을 재사용한다. String을 반환하는 일과 println이 출력하는 일은 다르다. void toString()은 Object의 String 반환 계약과 호환되지 않아 대체할 수 없다.

a의 실제 객체는 계속 Badge다. 문자열 연결이 표현을 얻는 것이며 객체를 String 인스턴스로 바꾸는 reference cast가 아니다. NM001 p.14의 casts라는 표현은 이 점에서 부정확하다.

Badge에는 equals override가 없고 a와 b는 서로 다른 객체다. 따라서 표현이 같아도 기본 equals는 false다. 같은 문자열 표현은 내용 동등성의 정의가 아니다. File의 toString도 경로의 표현을 얻는 일이며 파일을 열어 내용을 읽었다는 뜻은 아니다. 확인할 점은 반환·출력·객체 타입·동등성을 구분하는 것이다.

</details>

#### 회상 Q04 equals의 identity·type·field·null 경계

Shoes는 String company/model과 int size를 저장하며 다음 equals를 사용한다. 각 선언은 해당 필드를 그대로 초기화하는 생성자가 있다고 가정한다.

~~~text
public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Shoes) {
        Shoes s = (Shoes)o;
        return company.equals(s.company)
            && model.equals(s.model) && size == s.size;
    }
    return false;
}
Shoes a = new Shoes("Co", "M", 240);
Shoes b = new Shoes("Co", "M", 240);
Shoes c = a;
Shoes n = new Shoes(null, "M", 240);
~~~

a==b, a.equals(b), a==c, a.equals(c), a.equals(null), a.equals("Co")를 구하고 검사 순서를 설명하라. n.equals(n)과 n.equals(b)의 차이, type 검사 전에 cast하면 생길 문제도 설명하라. 별도 new String("xy") 두 개의 ==/equals와 primitive int의 equals 가능 여부를 비교하라.

또한 Point2D.equals가 instanceof Point2D 확인 후 x==다른.x && y==다른.y로 비교할 때, 별개 객체 (-2.0,3.0) 두 개와 (-2.0,4.0), null을 비교하라. NaN 좌표가 있으면 reflexivity가 깨질 수 있는가? 이 구현에서 toString과 hashCode가 각각 동등성에 어떤 보장을 주는지도 쓰라.

[NM001, PDF pp.17-21][NM001]; [NM004, PDF p.33][NM004]; [M002, PDF p.61][M002]; [T007, STT 15:58, 16:54][T007]

<details><summary>정답</summary>

여섯 결과는 false, true, true, true, false, false다. a와 b는 별개 객체지만 세 필드가 같고, c는 a의 alias다. this==o를 먼저 검사한 뒤 instanceof를 통과한 경우에만 Shoes로 cast하고 두 String 내용과 int 값을 비교한다. Null과 다른 타입은 instanceof를 통과하지 않는다. 다른 종류의 non-null 객체를 검사 없이 Shoes로 cast하면 ClassCastException이 생길 수 있다.

n.equals(n)은 identity 검사에서 true로 끝난다. n.equals(b)는 identity가 false이고 type 검사를 통과한 뒤 company가 null인 상태로 company.equals를 호출하므로 NullPointerException이 생긴다. Null 인자를 거부하는 것과 null field를 안전하게 처리하는 것은 다르다. 이 예는 company/model이 non-null이라는 조건에서 해석해야 한다.

별도 new String 두 개는 ==가 false, String.equals가 true다. 참조의 ==는 identity를, String.equals는 이미 정의된 문자 내용을 비교한다. Primitive int 값 자체에는 instance equals가 없다. NM001 p.17의 primitive 관련 문장은 이 점에서 부정확하며 wrapper의 equals와 구별한다.

두 유한 좌표가 모두 같으면 Point2D.equals는 true지만 별개 객체의 ==는 false다. y가 4.0이면 false, null도 instanceof 때문에 false다. NaN==NaN은 false이므로 예를 들어 x가 NaN인 Point2D는 제시된 equals에서 자신과 비교해도 false가 될 수 있다. 이 구현을 모든 수치에 적합한 동등성 관계로 일반화할 수 없다.

toString은 표현만 제공한다. Point2D와 Shoes 모두 여기에는 hashCode 구현이 제시되지 않아 equals/hashCode 계약 전체가 완성된 예가 아니다. 확인할 점은 identity, 내용 비교, type guard, null 인자, null field를 각각 추적하는 것이다.

</details>

#### 회상 Q05 frequency와 equals/hashCode 계약

Non-null fields를 가진 Shoes a와 b가 별개 객체이지만 내용 equals는 true, Shoes z는 다른 값이라고 하자. Collection c의 순서는 [a, null, b, a, z, null]이다. NM001 p.23처럼 찾는 o가 null이면 e==null, 아니면 o.equals(e)를 세는 frequency(c,o)의 값을 o=a와 o=null에서 각각 구하라.

Collection과 Collections를 구별하고 null 분기가 필요한 이유를 설명하라. a.equals(b)는 true인데 hashCode가 각각 12, 19라면 어떤 계약을 어기는가? 다른 객체의 hashCode가 둘 다 12이면 반드시 equals도 true인가? Equals의 reflexivity·symmetry·transitivity·consistency와 null 조건, hash 값의 상태 유지 조건까지 설명하라. 이 계약을 지키기 위해 Object의 모든 메서드를 재작성해야 하는지도 판단하라.

[NM001, PDF pp.22-24][NM001]; [NT001, STT 00:48, 01:48][NT001]

<details><summary>정답</summary>

o=a이면 a, b, a를 세어 3이다. Null 원소에는 a.equals(null)이 false이고 z도 다르다. o=null이면 null slot 두 개를 세어 2다. Null receiver로 o.equals(e)를 호출할 수 없으므로 분기를 나눈다.

Collection은 interface, Collections는 이러한 static utility를 제공하는 class다. NM001 p.22가 이 역할을 섞어 설명하는 부분을 구별해야 한다. `Collection<?>` 표기의 ?가 모든 연산을 임의 타입에 허용한다는 뜻은 아니다.

a.equals(b)가 true이면 a.hashCode()==b.hashCode()여야 한다. 12와 19는 이를 어긴다. Hash 기반 사용이 내용 동등성과 다른 분류를 하게 될 수 있으므로 equals를 내용 비교로 바꿀 때 해당 hashCode 계약도 맞춰야 한다. 반대로 동일 hash는 collision일 수 있어 equals true를 함의하지 않는다. 실제 철자는 hashCode이며 자료의 hashcode와 구별한다.

Non-null 객체의 equals는 자신과 같아야 하고(reflexivity), a와 b의 비교 방향이 바뀌어도 같아야 하며(symmetry), a=b와 b=c이면 a=c여야 한다(transitivity). 비교에 쓰는 정보가 변하지 않으면 같은 비교의 결과도 유지되어야 한다(consistency). Non-null 객체의 equals(null)은 false다. Equals 비교에 쓰는 정보가 변하지 않는 동안 같은 객체의 hash 값도 일관되어야 한다.

자료의 Shoes에는 hashCode 구현이 빠져 있으므로 완전한 hash 기반 사용 예라고 할 수 없다. 모든 Object method를 다시 구현해야 한다거나 모든 collection 요구를 자동 충족한다는 뜻은 아니다. 확인할 점은 equals true에서 같은 hash로 가는 한 방향의 필수 조건과 그 역을 구분하는 것이다.

</details>

#### 회상 Q06 Interface의 abstract 동작과 상수

다음 interface에서 field와 각 메서드의 의미를 설명하라. Concrete class Cooker가 상속받은 구현도 없다고 할 때, 어떤 접근 수준과 반환 계약을 가진 동작을 제공해야 하는가?

~~~text
interface Boiler {
    int WATER = 600;
    void boil();
    boolean noodleFirst();
}
~~~

WATER를 구현 객체마다 다른 값으로 바꾸거나 초기값을 생략할 수 있는지, 한 class가 다른 class를 extends하면서 Boiler와 또 다른 interface를 implements할 수 있는지도 판단하라. Abstract class와 이미 상속받은 구현이 있는 경우의 의무도 구별하라.

NM001 p.30은 printNum을 선언하고 func를 호출하며, p.31의 Pizza 반환 메서드 sketch에는 return이 없다. 이 둘을 그대로 성공 출력의 근거로 삼을 수 있는가? Interface를 통해 호출하는 사람이 내부 구현을 몰라도 되는 이유도 설명하라.

[NM001, PDF pp.26-32, 47][NM001]; [NT001, STT 02:48, 03:33, 04:25][NT001]

<details><summary>정답</summary>

Boiler는 동작의 이름·입력·반환 형태를 제공하는 type 계약이다. boil()은 반환값이 없는 행동, noodleFirst()는 boolean을 반환하는 행동이다. Body 없는 선언은 abstract method다. Cooker가 concrete이고 적절한 inherited implementation도 없다면 public void boil()과 public boolean noodleFirst()를 실제 body로 제공해야 한다. Interface의 public 호출 계약을 더 좁은 접근 수준으로 구현할 수 없다.

WATER는 생략해도 public static final인 상수다. 초기값 600이 필요하고, 구현 객체마다 재대입하여 바꿀 instance field가 아니다. 별도 instance 상태가 필요하다면 그것은 구현 class의 다른 field다.

한 class는 superclass 하나를 extends하면서 여러 interfaces를 implements할 수 있다. 적절한 구현을 상속했다면 각 body를 다시 직접 쓸 의무는 없다. Abstract class는 미구현 abstract 동작을 남길 수 있지만 그것을 최종 concrete class가 만족해야 한다. 또한 default/static body가 가능한 interface까지 모든 메서드에 body가 없다고 일반화하면 안 된다.

NM001 p.30의 func 호출은 제시된 printNum 구현과 이름이 달라 성공 근거가 아니다. 별도의 수정 호출 printNum(123)은 그 구현과 맞는다. p.31의 bakePizza는 Pizza 반환 계약인데 return과 helper 정의가 생략되어 완성 코드가 아니다. 이 원본 결함과 의도된 설계 관계를 구별한다.

호출자는 Boiler의 공개 signature에 의존하고 구현은 실제 조리 절차를 감출 수 있다. Encapsulation과 공통 호출 계약의 이점이며 필요한 결과를 생략해도 된다는 뜻은 아니다. 확인할 점은 계약, 상수, concrete 구현 의무와 abstract/default의 예외를 함께 설명하는 것이다.

</details>

#### 회상 Q07 List의 index 연산과 구현 교체

다음 호출을 순서대로 추적하여 get의 반환값, remove의 반환값, 최종 목록과 size를 쓰라.

~~~text
List<Integer> values = new ArrayList<>();
values.add(5); values.add(15); values.add(25);
Integer last = values.get(2);
Integer removed = values.remove(1);
int size = values.size();
~~~

Get이 목록을 바꾸는지, remove(1)이 값 1을 찾아 지우는지 구별하라. 생성식만 new LinkedList<>()로 바꾸었을 때 유지되는 의미와 보장되지 않는 성질은 무엇인가? Integer/E의 뜻, boxing의 역할, MyOwnList라는 이름만 쓰는 것으로 구현이 생기는지, 목록의 set 연산과 이 trace의 관계도 설명하라.

[NM001, PDF pp.33-35][NM001]

<details><summary>정답</summary>

세 add 뒤 목록은 [5, 15, 25]다. Zero-based index 2의 get은 Integer 값 25를 반환하고 목록을 바꾸지 않는다. remove(1)은 이 호출에서 int index 1의 원소 15를 반환하며 제거한다. 최종 목록은 [5, 25], size는 2다. 값 1인 원소를 검색하는 요청과 다르다.

List는 순서 있는 원소에 대한 interface 계약이다. 이 연산을 지원하는 LinkedList로 구현을 바꾸어도 같은 호출 열의 의미와 결과를 유지한다. 내부 저장 방식과 속도까지 같다는 보장은 없다. MyOwnList는 실제로 필요한 계약을 구현한 class가 있다고 가정한 이름이며 이름만으로 구현이 생기지 않는다.

E는 원소 타입의 자리이고 `List<Integer>`에서는 Integer로 정한다. Integer는 primitive int가 아닌 wrapper다. add에 쓴 int 값은 이 사용에서 boxing되며 get의 선언상 원소 타입은 Integer다. 모든 사용이 자동으로 primitive가 된다는 뜻은 아니다. Set은 지정 위치의 원소를 바꾸는 별도 연산이지만 이 호출 열에는 없으므로 최종 상태에 추가 변화를 만들지 않는다. 확인할 점은 index, 반환값, 상태 변경, interface와 구현을 나누는 것이다.

</details>

#### 회상 Q08 Comparable의 부호와 선택한 속성

Seagull은 int flyingHeight/numFriend를 갖고, `Comparable<Seagull>`의 compareTo가 높이가 더 크면 1, 같으면 0, 작으면 -1을 반환한다. Equals는 override하지 않았다. a=(6,90), b=(9,2), c=(6,1)은 별개의 non-null 객체다.

a.compareTo(b), b.compareTo(a), a.compareTo(c), a==c, a.equals(c)를 구하라. 친구 수가 순서를 바꾸는지, compareTo의 양수는 반드시 1이어야 하는지, 0이 모든 필드나 identity의 같음을 뜻하는지 설명하라. Comparable과 Object.equals의 역할 차이 및 Comparable을 구현하면서 다른 상속/implements 관계를 가질 수 있는지도 쓰라.

[NM001, PDF pp.36-39, 46][NM001]; [NT001, STT 05:25, 06:23, 07:23][NT001]

<details><summary>정답</summary>

결과는 -1, 1, 0, false, false다. 첫 비교는 6<9, 역방향은 9>6, a와 c는 같은 높이다. 친구 수는 제시된 compareTo가 읽지 않으므로 순서에 영향이 없다. a와 c는 별개 객체이고 equals를 재정의하지 않았으므로 기본 identity 비교는 false다.

이 구현은 1/-1을 사용하지만 Comparable의 반환 계약은 양수·음수·0의 부호다. 양수는 receiver가 더 큰 쪽, 음수는 인자가 더 큰 쪽, 0은 선택한 ordering에서 같은 위치를 뜻한다. 0을 모든 필드의 동등성이나 같은 객체라는 의미로 바꾸면 안 된다. Equals와 ordering을 함께 사용하는 설계에서는 이 관계를 점검해야 한다.

Equals는 Object의 기본 계약을 물려받지만 모든 객체 종류에 자연스러운 순서가 있는 것은 아니다. 필요한 class가 Comparable을 구현하여 순서를 정한다. 다른 superclass를 extends하거나 다른 interfaces를 함께 implements하는 것도 가능하다. 제시된 비교가 필요한 List 정렬에 쓰일 수 있다는 것이 모든 collection의 모든 요구를 충족한다는 보장은 아니다. 확인할 점은 비교 기준과 반환 부호를 실제 코드에서 찾는 것이다.

</details>

#### 회상 Q09 String의 첫 차이와 공통 접두사

NM001의 compareTo 발췌 규칙은 최소 길이까지 앞에서 비교하고, 첫 다른 문자에서는 c1-c2, 끝까지 같으면 len1-len2를 반환한다. 영문 문자 코드 'a'=97, 'b'=98, 'c'=99, 'd'=100, 'D'=68, 'e'=101을 사용하여 다음 값을 각각 계산하라.

~~~text
"bc".compareTo("be")
"ax".compareTo("b")
"cat".compareTo("cater")
"dog".compareTo("Dog")
"bc".compareTo("bc")
~~~

계산에 사용한 위치와 부호의 뜻을 설명하라. 전체 길이부터 비교하거나 compareTo 결과가 1일 때만 더 크다고 판단하면 왜 틀리는가? 이 발췌가 모든 Java 버전의 String 저장 구조나 문화권 사전 정렬을 보장하는지도 구별하라.

[NM001, PDF pp.40-42][NM001]

<details><summary>정답</summary>

첫 값은 첫 b가 같고 index 1의 c-e=99-101=-2다. 둘째는 index 0의 a-b=97-98=-1이므로 뒤의 x나 전체 길이는 결정에 쓰지 않는다. 셋째는 공통 접두사 cat의 세 문자가 모두 같아 3-5=-2다. 넷째는 첫 d-D=100-68=32다. 마지막은 모든 문자가 같고 길이 차이도 0이다.

음수이면 receiver가 먼저, 양수이면 뒤에 오며 0이면 이 문자열 비교에서 같다. 결과 32도 양수이므로 ==1만 검사하면 더 큰 경우를 놓친다. 길이는 최소 길이까지 첫 차이가 없을 때만 사용된다.

이는 공급된 코드 발췌의 정적 계산이다. 발췌에 char[]가 있다고 모든 Java 버전의 내부 저장이 같다는 뜻이 아니고, 위 코드 단위의 영문 비교를 문화권별 collation 전체와 같다고 할 수도 없다. 확인할 점은 비교를 멈춘 첫 위치 또는 공통 접두사 이후의 길이 차이를 명시하는 것이다.

</details>

#### 회상 Q10 정렬 기준과 출력 표현의 분리

다음 Student는 이름/ID 표현 예와 독립된 가상 수치 예다.

~~~text
class Student implements Comparable<Student> {
    double gpa;
    Student(double gpa) { this.gpa = gpa; }
    public int compareTo(Student s) {
        double diff = gpa - s.gpa;
        return diff > 0 ? 1 : diff < 0 ? -1 : 0;
    }
    @Override public String toString() { return Double.toString(gpa); }
}
List<Student> xs = new ArrayList<>();
xs.add(new Student(2.5));
xs.add(new Student(4.0));
xs.add(new Student(3.75));
Collections.sort(xs);
System.out.println(xs);
~~~

Add 직후와 sort 뒤의 순서, 최종 출력 및 관련 비교 부호를 구하라. ToString만 "score=" 접두어를 붙이도록 바꾸면 정렬 기준도 바뀌는가? Sort가 원소를 추가하는지도 설명하라. gpa가 NaN인 객체를 추가하면 위 비교를 완전한 수치 순서로 사용할 수 있는지 조건을 검토하라.

[NM001, PDF pp.43-45][NM001]

<details><summary>정답</summary>

Add 직후는 [2.5, 4.0, 3.75] 순서다. 2.5-4.0은 음수, 4.0-3.75는 양수, 2.5-3.75는 음수이므로 이 유한 값들의 오름차순은 [2.5, 3.75, 4.0]이다. Println의 표현도 [2.5, 3.75, 4.0]이다.

Add는 원소를 넣고 sort는 이미 있는 원소의 순서를 바꾼다. 정렬 기준은 compareTo다. ToString만 바꾸면 [score=2.5, score=3.75, score=4.0]처럼 보이지만 GPA 순서의 기준은 그대로다. 자료 p.43의 stored라는 표현을 sort가 저장/추가를 수행한다는 뜻으로 읽으면 안 된다.

Diff가 NaN이면 >0과 <0이 모두 false여서 위 구현은 0을 반환한다. 따라서 NaN을 포함한 모든 double의 완전한 ordering이라는 보장은 없다. 이 문제의 정렬 trace는 보통의 유한 입력에 한정한다. 확인할 점은 저장·정렬·표현을 서로 다른 책임으로 설명하고 NaN 경계를 남기는 것이다.

</details>

#### 회상 Q11 Default/static body와 package access

Java 8 이상이며 interface body를 허용하는 다음 독립된 예를 읽으라.

~~~text
interface Reader {
    void read();
    default void clean() { System.out.println("clean"); }
    static String kind() { return "reader-api"; }
}
class TextReader implements Reader {
    public void read() { System.out.println("read"); }
}
TextReader r = new TextReader();
r.read();
r.clean();
System.out.println(Reader.kind());
~~~

세 출력과 abstract/default/static 메서드의 역할을 쓰라. TextReader가 clean의 body를 새로 작성해야 하는가? Interface의 static method를 r.kind()로 호출할 수 있는가? 여기의 default와 class method에서 access modifier를 생략한 package access의 차이를 설명하고, interface에는 body가 절대 없다는 진술을 판정하라.

[NM001, PDF pp.26-27, 47, 54][NM001]; [NT001, STT 08:22, 14:45][NT001]

<details><summary>정답</summary>

출력은 read, clean, reader-api 순서다. Read는 interface에 body가 없는 abstract 동작이고 TextReader가 public 구현을 제공한다. Clean은 default body를 물려받아 사용하므로 이 concrete class가 반드시 새로 작성할 필요는 없으며 필요하면 override할 수 있다. Kind는 interface 자체의 static 동작이므로 Reader.kind()로 부른다. 이 static method는 구현 class의 instance member로 상속되는 것이 아니므로 r.kind()는 제시된 선언에서 허용되지 않는다.

Default method의 default는 interface에 공통 body를 제공하는 키워드다. Class에서 접근 modifier를 생략하는 package access는 같은 package에서의 접근 범위를 뜻하며 이 기능과 다르다. Clean의 접근이 package 전용이라는 뜻도 아니다.

NM001 p.47이 Java 8 default/static body를 명시하므로 pp.26-27, 54 및 NT001의 body가 없다는 넓은 문장은 기본 abstract-method 형태에 한정해야 한다. 확인할 점은 body 존재와 접근 범위를 하나의 default 의미로 합치지 않는 것이다.

</details>

#### 회상 Q12 Abstract class의 상태·공통 구현·추상 동작

다음은 공통 초기화를 명시한 별도의 학습용 예다. 같은 package의 클래스라고 하자.

~~~text
abstract class Person {
    String description, name;
    private int age;
    Person(String description, String name, int age) {
        this.description = description; this.name = name; this.age = age;
    }
    public void printName() { System.out.println(description + " " + name); }
    public void ageOneYear() { age++; System.out.println(age); }
    abstract void work();
    abstract void play();
}
class Learner extends Person {
    Learner() { super("sample", "L", 20); }
    public void work() { System.out.println("read"); }
    public void play() { System.out.println("walk"); }
}
Person p = new Learner();
p.printName(); p.ageOneYear(); p.work(); p.play();
~~~

출력과 공유된 부분/하위 구현 부분을 나누어 설명하라. Person을 직접 new할 수 있는가? Learner가 age를 직접 읽는 것과 ageOneYear를 호출하는 것은 같은가? Work/play에 부모의 임의 body를 넣고 abstract를 없애는 설계와 비교하라. Abstract class가 반드시 abstract/concrete method를 각각 하나씩 가져야 하는지도 판단하라.

서로 관련 없는 클래스에 공통 연산을 더하는 경우와 공통 상태·constructor·protected helper를 재사용하는 경우에는 interface/abstract class 중 무엇이 적절한가? `AbstractList<E>` implements `List<E>`, `ArrayList<E>` extends `AbstractList<E>`의 관계와 E도 설명하라. 원자료 Person에 빠진 constructor가 있다는 사실과 위 별도 예를 구별하라.

[NM001, PDF pp.49-56][NM001]; [NT001, STT 10:13, 13:48, 16:41, 17:36, 18:29, 20:24, 22:06][NT001]

<details><summary>정답</summary>

출력은 sample L, 21, read, walk 순서다. Name/description/age와 printName/ageOneYear는 부모가 공통으로 관리하고 work/play는 Learner가 의미를 정한다. Person 참조에서 같은 호출을 사용해 실제 Learner의 구현을 실행한다.

Person은 abstract여서 직접 인스턴스를 만들 수 없다. Abstract method가 있는 class는 abstract여야 하지만 abstract class가 반드시 두 종류의 method를 하나씩 가져야 하는 것은 아니다. Description/name은 modifier가 생략된 package 접근이고 age는 private다. Learner가 age를 직접 읽는 것은 허용되지 않지만 부모의 public ageOneYear는 부모 내부에서 age를 다루므로 호출할 수 있다.

부모가 work/play의 concrete body를 주고 class의 abstract를 없애면 Person 직접 생성과 그 기본 동작의 상속이 가능하다. Abstract로 남기면 그런 임의 동작을 피하고 concrete subclass가 남은 계약을 만족하도록 요구한다. 이는 단순히 할 수 있는 기능을 늘리기보다 초기화·직접 생성·동작의 책임을 명시하는 설계다.

서로 다른 종류가 같은 연산을 지원하거나 이미 다른 superclass를 가진 class에 계약을 더하려면 interface가 적절하다. 관련 class가 instance fields, 공통 초기화 constructor, 구현과 protected helper를 공유하려면 abstract class가 적절하다.

`List<E>`는 계약, `AbstractList<E>`는 그 계약을 implements하는 공통 구현층, `ArrayList<E>`는 그 층을 extends하는 concrete 구현이다. ArrayList가 List 계약에서 벗어난 것이 아니다. E는 같은 원소 타입을 연결하는 이름 붙인 type parameter이며 ? wildcard가 아니다.

NM001 p.50에는 pp.51-52의 super(description,name,age)에 대응하는 constructor가 없다. 이 문제는 초기화를 명시한 별도 예이므로 원자료 누락을 원래 존재했던 코드로 복원한 것이 아니다. 확인할 점은 공유 상태의 접근 조건, abstract 의무, 초기화와 계약의 연결을 함께 설명하는 것이다.

</details>

#### 회상 Q13 Method signature와 반환형

아래 선언 후보를 같은 class에 둘 때 signature가 겹치는 쌍을 찾고, 겹치지 않는 overload를 묶으라. 변수 이름이나 반환형만 바꾼 경우를 구별하라.

~~~text
int total(int a, int b)
double total(int x, int y)
int total(int a, int b, int c)
float total(float a, float b)
void total(String text)
~~~

Double 변수에 total(2,3)을 대입하면 반환형으로 첫 두 선언을 구별할 수 있는가? 같은 작업을 printInt/printFloat/printString처럼 다른 이름으로만 제공하는 설계와 overload의 동기를 비교하라. Animal.move()와 Fish.swim()의 행동이 비슷하다는 이유로 overriding이라고 부를 수 있는지도 판단하라.

[NM004, PDF pp.4-9][NM004]; [NM005, PDF p.4][NM005]; [NT001, STT 25:54, 26:53, 27:51, 28:51][NT001]

<details><summary>정답</summary>

첫 두 선언은 모두 total(int,int)여서 충돌한다. Parameter 이름 a/b와 x/y 및 반환형 int/double은 이 범위의 Java signature를 구별하지 않는다. 둘 중 하나만 둔 뒤 total(int,int,int), total(float,float), total(String)을 함께 둘 수 있다. 이들은 개수 또는 순서 있는 parameter type 목록이 다르다.

결과를 double 변수에 넣는다고 반환형별 overload가 생기지 않는다. 첫 두 선언이 함께 있으면 class 선언 자체가 잘못된 것이며 대입 문맥으로 해결하지 못한다. NM004 p.7의 일반 표기와 달리 p.8은 Java에서 반환형을 제외함을 명시한다.

Overload는 같은 의미의 이름을 유지하며 서로 다른 입력 형태를 제공해 호출자가 관련 작업을 알아보기 쉽게 한다. 서로 다른 이름만 쓰면 같은 역할의 이름을 따로 기억해야 한다. 그러나 의미가 비슷한 것만으로 override는 아니다. Move와 swim은 이름이 달라 같은 signature가 아니며 Fish에 추가된 swim이 Animal.move를 재정의하지 않는다. 확인할 점은 동작의 의미와 Java가 구별하는 signature 조건을 따로 적용하는 것이다.

</details>

#### 회상 Q14 Type별 이동과 abs_add의 누적

Point는 초기 float 좌표가 (0.0f,0.0f)이고 move(int,int), move(float,float)가 각각 x/y에 입력을 더한다. move(-2,1), move(0.5f,2.0f)를 차례로 호출할 때 선택 signature와 각 단계 좌표를 쓰라.

다음 두 overload에서 abs_add(-4.0,1.0), abs_add(new double[]{-4.0,1.0,-2.0}), 빈 배열의 반환값을 계산하고 배열의 각 sum을 적으라. 입력은 non-null 배열과 작은 유한 값으로 제한한다.

~~~text
static double abs_add(double a, double b) {
    return Math.abs(a) + Math.abs(b);
}
static double abs_add(double[] xs) {
    double sum = 0;
    for (int i = 0; i < xs.length; i++) sum = abs_add(sum, xs[i]);
    return sum;
}
~~~

이것이 같은/밀접한 작업을 한 이름에 묶는 이유, scalar body에 위임하는 유지보수 이점과 상속의 차이를 설명하라. 위임이 반드시 더 느리다는 주장도 판단하라.

[NM004, PDF pp.11-13][NM004]; [NM005, PDF pp.4-5][NM005]; [NT001, STT 31:21, 33:13, 34:41][NT001]

<details><summary>정답</summary>

첫 호출의 두 int는 move(int,int)를 골라 (-2.0,1.0)이 된다. 둘째는 f 접미사가 있는 두 float여서 move(float,float)를 골라 (-1.5,3.0)이 된다. 서로 다른 입력 타입을 받아도 좌표 이동이라는 의미가 유지된다.

Scalar 반환은 |-4|+|1|=5.0이다. 배열 sum은 0→4→5→7이므로 7.0이다. 빈 배열은 loop를 한 번도 돌지 않아 0.0을 반환한다. |a+b|와 |a|+|b|는 다르며 여기서는 후자다. 작은 유한 값에서 sum이 음수가 아니므로 다음 단계는 이전 합에 다음 원소의 절댓값을 더한다.

배열과 scalar의 입력 모양은 다르지만 절댓값 합이라는 밀접한 의미를 공유한다. 배열이 scalar 동작을 호출하면 핵심 동작의 변경을 같은 경로에서 재사용한다. Extends로 물려받는 상속이 아니라 overload 사이의 호출에 의한 재사용이다. 계약을 바꾸면 배열 의미에도 영향이 있으므로 변경도 함께 검토해야 한다.

NT001 34:41의 호출 비용 일반화는 측정 근거가 없으므로 유지보수상의 이유와 구분한다. 확인할 점은 각 인자 타입, 각 누적값, 재사용 관계를 제시하는 것이다.

</details>

#### 회상 Q15 indexOf의 검색 시작점과 겹침

Index는 0부터 시작하고 indexOf가 일치를 찾지 못하면 -1을 반환한다고 하자.

~~~text
String dna = "ACGCATCGCG";
String pattern = "CGC";
int first = dna.indexOf(pattern);
int second = dna.indexOf(pattern, first + pattern.length());
int again = dna.indexOf(pattern, first);
~~~

세 결과와 두 번째 검색 시작 위치를 문자 index로 확인하라. 두 번째 parameter가 일치 횟수인지도 설명하라. 별도 문자열 "CGCGC"에서 첫 일치 뒤 pattern.length()만큼 건너뛰는 방식이 겹치는 다음 일치까지 찾는가? First+1부터 찾는 경우와 비교하라. 패턴이 처음부터 없을 때 first+length를 무조건 다음 검색으로 쓰면 안 되는 이유도 설명하라.

[NM004, PDF p.14][NM004]; [NM005, PDF p.5][NM005]; [NT001, STT 35:41, 36:41, 37:41][NT001]

<details><summary>정답</summary>

dna의 문자는 A0 C1 G2 C3 A4 T5 C6 G7 C8 G9다. first는 1, pattern 길이는 3이므로 다음 시작점은 4다. 그 뒤 C6 G7 C8에서 일치하여 second=6이다. again은 1에서 검색하므로 같은 첫 일치를 다시 찾아 1이다. 추가 parameter는 검색 시작 index이며 몇 번째 일치를 요구하는 번호가 아니다.

별도 문자열 CGCGC에는 index 0과 2에서 겹치는 CGC가 있다. first=0에서 3부터 찾으면 다음 일치 2를 이미 지나쳐 -1이다. 1부터 찾으면 2를 얻는다. 따라서 +length 방식은 첫 일치 전체 뒤의 검색이지 겹치는 모든 일치의 열거가 아니다.

first=-1이면 첫 일치가 없으므로 first+length가 첫 결과 뒤의 위치라는 해석 자체가 성립하지 않는다. 미발견 여부를 먼저 확인해야 한다. 이 짧은 trace는 모든 검색을 완성하는 구현이 아니다.

원자료의 정확한 메서드명은 indexOf다. NM005 p.5의 indexof, NT001 35:41의 CCT 및 36:41의 offset 없는 듯한 설명은 인쇄 코드와 구별한다. 확인할 점은 실제 문자 index, 시작점과 겹침/미발견 조건을 명시하는 것이다.

</details>

#### 회상 Q16 기본값 wrapper와 공통 body 위임

다음 power와 서로 대안인 두 debug(String) body를 읽으라.

~~~text
static double power(double x, int n) {
    if (n <= 0) return 1;
    return x * power(x, n - 1);
}
static double power(double x) { return power(x, 2); }

// MyClass 내부, var1은 7
void debug() { System.out.println("var 1 : " + var1); }
// 대안 A
void debug(String s) { System.out.println(s + "var 1 : " + var1); }
// 대안 B
void debug(String s) { System.out.print("Output : " + s); debug(); }
~~~

power(3), power(3,3), power(3,-2)의 호출 경로와 반환값을 구하라. 음의 지수를 수학적 역수로 처리하는가? s="log: "일 때 두 debug 대안의 정확한 출력과, 기본 debug의 field 표시를 바꿀 때 수정 범위를 비교하라. A와 B를 동시에 둘 수 있는가? 한 body에 위임하는 원칙이 강제 문법 규칙인지, 속도 향상을 보장하는지도 설명하라.

[NM004, PDF pp.15-16][NM004]; [NT001, STT 38:38, 39:33, 40:30, 41:23][NT001]

<details><summary>정답</summary>

power(3)은 power(3,2)로 위임하고 3×power(3,1)→3×3×power(3,0)→3×3×1이어서 9.0이다. power(3,3)은 3×3×3×1=27.0이다. power(3,-2)는 n<=0을 즉시 만족하여 1.0이다. 1/9을 계산하는 일반적인 음의 지수 함수가 아니다.

A의 출력은 log: var 1 : 7이다. B의 print는 줄바꿈 없이 Output : log: 를 출력하고 debug()의 println이 이어지므로 한 줄 Output : log: var 1 : 7이다. 접두어가 달라 두 대안의 출력이 완전히 같지는 않다.

기본 debug의 field 표시를 바꾸면 A의 복사된 field 출력도 함께 수정해야 한다. B는 그 부분을 호출하므로 기본 body의 변경을 재사용한다. A/B는 둘 중 하나를 선택하는 대안이며 동시에 선언하면 debug(String) signature가 중복된다.

한 overload가 주요 작업을 하고 나머지가 위임한다는 것은 관련 동작의 중복을 줄이는 설계 원칙이다. 모든 overload에 강제되는 문법 규칙도, 호출 속도가 반드시 빨라지거나 느려진다는 보장도 아니다. 확인할 점은 기본값 전달과 계산/출력 문자열을 실제 body에 따라 구하는 것이다.

</details>

#### 회상 Q17 Constructor overload와 좌표 의미

Point의 다음 초기화 경로를 가정한다. 무인자는 (0,0), int/int와 float/float는 받은 x,y를 직교좌표로 저장하고, double/double은 radius,theta를 받아 x=radius*cos(theta), y=radius*sin(theta)로 저장한다. 각은 radian이다.

~~~text
Point()
Point(int x, int y)
Point(float x, float y)
Point(double radius, double theta)
~~~

new Point(), new Point(3,1), new Point(3.0f,1.0f), new Point(3.0,1.0)가 선택하는 경로와 저장되는 좌표를 쓰라. 극좌표 (radius=3,theta=0)도 수식으로 계산하라. Float 입력을 double로 바꾼 것이 단순 정밀도 변경인지, signature가 합법이면 좋은 API라고 할 수 있는지 설명하라. 명시적 indicator 제안과 원자료 import Math;의 의미도 구별하라.

[NM004, PDF p.17][NM004]; [M002, PDF pp.40-42][M002]; [NT001, STT 42:21, 43:12, 44:12][NT001]

<details><summary>정답</summary>

무인자 경로는 (0,0), int/int 경로는 (3,1), float/float 경로도 (3,1)을 저장한다. 마지막의 3.0과 1.0은 double literal이므로 double/double 경로를 선택하여 (3 cos(1), 3 sin(1))을 저장한다. 이는 입력 그대로의 (3,1)과 다른 의미다. 극좌표 (3,0)은 수학적으로 cos(0)=1, sin(0)=0이어서 (3,0)이다.

Parameter 목록이 달라 overload 구별은 가능하지만 float에서 double로 바뀔 때 좌표계 의미까지 바뀌면 호출자가 수치 정밀도 변경으로 오해하기 쉽다. 문법적 가능성과 예상하기 쉬운 API라는 설계 기준은 다르다. NT001의 indicator 제안은 좌표계를 명확히 표시하자는 동기이지 새로운 필수 constructor 구현을 제공한 것은 아니다.

원자료의 import Math;는 유효한 Math package나 Point의 소속을 입증하지 못하는 잘못된 import 표기다. 위 수식을 설명하는 것과 원자료 전체가 그대로 완성 코드라고 하는 것은 다르다. 또한 NT001의 radians and theta라는 표현을 인쇄 identifier radius/theta로 조용히 고쳐 인용하지 않는다. 확인할 점은 constructor의 class 이름·무반환형, 입력 타입과 수치의 의미를 구분하는 것이다.

</details>

#### 회상 Q18 this와 super의 초기화 경로

다음은 JDK 11 기준의 독립된 초기화 예다. 먼저 A에서 new Point()를 수행할 때 위임 순서·최종 좌표·출력 순서와 생성 객체 수를 구하라.

~~~text
// A
class Point {
    float x, y;
    Point(float x, float y) {
        this.x = x; this.y = y; System.out.println("F");
    }
    Point(int x, int y) {
        this((float)x, (float)y); System.out.println("I");
    }
    Point() { this(0, 0); System.out.println("Z"); }
}
// B: A와 별도
class Parent { Parent() { System.out.println("parent"); } }
class Child extends Parent {
    Child() { super(); System.out.println("child"); }
}
~~~

A의 this(0,0)을 this(0.0,0.0) 또는 this(0.0f,0.0f)로 각각 바꾸면 어떻게 다른가? B의 new Child() 출력, this(...)/super(...)의 차이, 명시적 호출을 생략할 때 부모 constructor에 필요한 조건도 설명하라. JDK 11에서 위임 호출 앞에 출력문을 넣어도 되는가? Java 25의 언급까지 포함해 버전 범위를 구별하고, 이 선택이 dynamic dispatch인지 판단하라.

[NM004, PDF pp.18-19][NM004]; [RM001, PDF pp.48-51][RM001]; [M002, PDF pp.40-42][M002]; [NT001, STT 45:08, 46:08, 48:59, 49:57][NT001]

<details><summary>정답</summary>

A의 위임은 Point()→Point(int,int)→Point(float,float)다. Int literal 0 두 개가 int 경로를 고르고 그 body의 명시적 cast가 float 경로로 전달한다. 공통 대입 후 돌아오므로 출력은 F, I, Z이며 최종 (0.0,0.0)이다. 한 객체의 초기화에 여러 constructor가 관여한 것이지 객체 세 개를 만든 것이 아니다.

0.0은 double이다. A에는 double/double constructor가 없고 double을 float/int로 자동 narrowing하지 않으므로 this(0.0,0.0)는 해당 목록에 맞지 않는다. 0.0f는 float이므로 그 대안은 float 경로를 직접 거쳐 F, Z가 된다. NM004 p.17의 극좌표 constructor를 별도 p.18 예에 임의로 합치면 안 된다. NT001 46:08의 0.0 제안을 원래 0.0f였던 발화로 바꾸지 않는다.

B의 출력은 parent 다음 child다. This(...)는 같은 class의 다른 constructor, super(...)는 부모 constructor로 위임한다. 명시적 this/super가 없을 때의 암시적 super()에는 호출 가능한 부모 무인자 constructor가 필요하다. 부모에 인자 constructor만 있거나 무인자 constructor가 접근 불가능하면 자동으로 해결되지 않는다.

JDK 11에서는 명시적 constructor 위임 호출을 body의 첫 문장에 두어야 하므로 그 앞에 출력문을 넣는 것은 허용되지 않는다. 위임된 초기화가 끝난 뒤 나머지 body로 돌아온다. NM004 p.19와 NT001은 Java 25의 제한된 사전 작업을 따로 언급하므로 이 규칙을 모든 버전의 절대 명제로 확대하지 않는다. 새 버전의 상세 문법은 이 문제에서 요구하지 않는다.

Constructor는 상속되어 override되는 instance method가 아니다. 이 경로는 초기화 위임이고 실제 receiver의 override body를 고르는 dynamic dispatch와 다르다. 확인할 점은 인자 타입에 따른 경로 선택과 반환 후 실행 순서를 분리하는 것이다.

</details>

#### 회상 Q19 적용 가능한 overload와 most-specific

ColoredPoint extends Point이며 다음 static overload들은 이름을 출력한다.

~~~text
static void test(ColoredPoint p, Point q) { System.out.println("CP,P"); }
static void test(Point p, ColoredPoint q) { System.out.println("P,CP"); }
ColoredPoint c = new ColoredPoint();
Point p = c;
~~~

각 호출을 독립적으로 분석하라: test(c,p), test(p,c), test(c,c), test(null,null). 적용 가능한 후보와 유일한 most-specific 존재 여부를 쓰라. 다음에는 둘째 선언을 test(ColoredPoint,ColoredPoint)로 교체한다. 이때 test(c,c)와 test(c,p)는 무엇을 고르는가? 선언 순서를 바꾸면 모호성이 사라지는가?

[NM004, PDF pp.20-23][NM004]; [NT001, STT 50:55, 51:49, 52:44][NT001]

<details><summary>정답</summary>

처음 test(c,p)는 선언 타입 (ColoredPoint,Point)에 맞는 첫 후보만 적용 가능해 CP,P다. 두 번째 후보의 둘째 parameter에 Point 식 p를 cast 없이 넘길 수 없다. test(p,c)는 반대로 둘째 후보만 적용 가능해 P,CP다. p가 실제 ColoredPoint를 가리켜도 overload 선택의 인자 식 타입은 Point다.

test(c,c)는 두 후보 모두 적용 가능하지만 첫 후보는 첫 자리에서, 둘째 후보는 둘째 자리에서 더 구체적이다. 전체 parameter 목록에서 하나가 다른 하나보다 더 구체적이지 않아 compile-time ambiguity다. Null은 두 reference type 모두에 적용 가능하므로 test(null,null)도 같은 우열 문제로 모호하다.

둘째 선언을 (ColoredPoint,ColoredPoint)로 교체하면 test(c,c)는 그 후보가 두 자리 전체에서 더 구체적이므로 CP,CP를 고른다. test(c,p)는 둘째 인자의 선언 타입이 Point여서 여전히 (ColoredPoint,Point)를 고른다.

선언 순서는 기준이 아니다. NT001 52:44의 먼저 matches한다는 설명을 먼저 발견한 method를 고른다는 알고리즘으로 받아들이면 안 된다. 확인할 점은 signature가 다름, 호출에 적용 가능함, 유일한 most-specific이 있음이라는 서로 다른 조건을 구분하는 것이다.

</details>

#### 회상 Q20 Instance override와 반환형·annotation·constructor

Employee의 public double getSalary()는 120을 반환하고 Manager의 같은 instance signature는 210을 반환한다. Employee e=new Manager(); e.getSalary()의 값과 선택 과정을 설명하라. 다음 제안들은 각각 독립적으로 판단하라.

1. Subclass가 public double getSalary(){return 0;}를 선언한다.
2. Subclass가 public int getSalary(){return 0;}를 선언한다.
3. @Override를 붙였지만 메서드를 getSalaries()로 쓴다.
4. Manager 안에 반환형 없는 Employee(){...}를 써서 부모 constructor를 override하려 한다.

Primitive 반환값 0을 double method에서 반환하는 일과 반환형 선언을 int로 바꾸는 일을 구별하라. @Override가 하는 검사, 부모 초기화 방법, reference 반환형에 관한 일반화의 한계도 설명하라. NM005 p.6의 public string toString() 표기를 Java 규칙으로 채택할 수 있는가?

[NM004, PDF pp.25-28, 32][NM004]; [NM005, PDF p.6][NM005]; [RM001, PDF pp.32, 48][RM001]; [NT001, STT 54:47, 55:45, 56:45, 01:02:14][NT001]

<details><summary>정답</summary>

e의 선언 타입 Employee에서 getSalary() 호출 가능성을 검사하고 실제 Manager의 override를 실행하므로 반환값은 210.0이다. 부모 구현을 그대로 사용한 Employee 객체라면 120.0이다.

1은 호환되는 double 반환 override이며 int literal 0을 반환 시 double 값으로 사용할 수 있다. 2는 같은 이름·parameter 목록에 호환되지 않는 primitive 반환형을 선언한 것이어서 compile-time error다. 반환형만 다른 overload가 아니다. 3은 부모의 getSalary()와 이름이 다르므로 재정의가 아니며 @Override가 그 의도 불일치를 발견한다. Annotation 자체가 overload를 만들거나 dispatch 규칙을 바꾸지는 않는다.

4는 constructor override가 아니다. Constructor는 상속되지 않고 현재 class의 이름을 사용한다. Manager의 초기화는 Manager(...)에 쓰고 부모 초기화는 super(...)로 연결한다. Instance method overriding과 constructor chaining은 다른 일이다.

자료의 반환형이 같아야 한다는 넓은 설명은 이 primitive int/double 사례에 한정해야 하며 모든 reference return도 글자 그대로 같은 타입만 가능하다는 결론은 나오지 않는다. NM005의 소문자 string도 Java의 String과 다른 잘못된 표기다. 확인할 점은 signature 조건 외에 반환형 호환성과 instance method라는 조건을 유지하는 것이다.

</details>

#### 회상 Q21 instanceof와 정확한 class-name 분기

이 문제에서는 Executive extends Manager extends Employee, TeamLead extends Manager라는 계층을 명시한다. Helper A는 아래 순서로 검사한다.

~~~text
if (e instanceof Executive) return 900;
else if (e instanceof Manager) return 300;
else return 100;
~~~

Helper B는 non-null e의 getClass().getName()이 "sample.Executive"이면 900, "sample.Manager"이면 300, 그 밖에는 100을 반환한다. 실제 package 이름은 sample이다.

TeamLead 객체와 Executive 객체에 대한 A/B 결과, A에서 Manager 검사를 먼저 옮긴 경우의 결과를 구하라. GetClass가 superclass 이름을 반환하는가? Null 입력의 instanceof 분기와 getClass 호출도 비교하라. 새로운 Employee subtype을 추가할 때 중앙 분기들의 유지보수 위험과 instance overriding 대안을 설명하라. 이 비교로 instanceof/getClass의 모든 사용을 금지할 수 있는가?

[NM004, PDF pp.29-31][NM004]; [NT001, STT 57:38, 59:24, 01:00:18, 01:01:17][NT001]

<details><summary>정답</summary>

A는 TeamLead를 Manager의 subtype으로 판정하여 300, Executive는 첫 분기에서 900을 반환한다. B는 TeamLead의 정확한 이름 sample.TeamLead가 두 문자열과 다르므로 100, Executive에는 900이다. 실제 class 이름 검사와 subtype 포함 검사는 같은 규칙이 아니다.

A에서 Manager를 먼저 검사하면 Executive도 Manager이므로 300을 반환하여 더 구체적인 Executive 분기에 도달하지 않는다. 이 관계는 문제에 명시한 계층의 결과이며 원자료가 그 계층을 새로 명시했다는 뜻이 아니다. GetClass는 객체의 실제 class를 나타내며 superclass를 찾는 동작이 아니다.

Null instanceof는 false이므로 A는 두 검사 뒤 100을 반환한다. B의 e.getClass()는 null receiver 때문에 NullPointerException이다. Instance method 호출도 receiver가 필요하므로 overriding 설계에서 null 처리는 별도로 정해야 한다.

중앙 helper가 급여·시간·장소별로 존재하면 새 type마다 여러 목록과 값을 갱신해야 하고 빠뜨리면 default branch가 잘못 적용된다. Instance overriding은 각 class가 자기 동작을 두고 caller가 Employee 계약의 같은 method를 부르게 하는 대안이다. 모든 type 검사가 잘못됐다는 일반 금지 규칙은 아니다. NT001의 superclass 표현이나 class 의존성이 모두 사라진다는 설명도 그대로 채택하지 않는다. 확인할 점은 subtype 판정, 정확한 class, 검사 순서와 null을 나누는 것이다.

</details>

#### 회상 Q22 Field hiding·overload·override의 네 출력

다음 정의의 모든 body를 읽고 네 show의 signature와 출력, 바뀐 field들을 계산하라. Float 값은 이 예의 0.25/0.5 단위에서 정확히 표현된다.

~~~text
class Point {
    int x = 0, y = 0;
    int getX() { return x; }
    int getY() { return y; }
    void move(int dx, int dy) { x += dx; y += dy; }
    static void show(int x, int y) { System.out.println("("+x+", "+y+")"); }
    static void show(float x, float y) { System.out.println("("+x+", "+y+")"); }
}
class RealPoint extends Point {
    float x = 0.0f, y = 0.0f;
    @Override void move(int dx, int dy) { move((float)dx, (float)dy); }
    void move(float dx, float dy) { x += dx; y += dy; }
    @Override int getX() { return (int)Math.floor(x); }
    @Override int getY() { return (int)Math.floor(y); }
}
RealPoint r = new RealPoint();
Point p = r;
r.move(-1.5f, 2.25f);
p.move(1, -3);
Point.show(p.x, p.y);
Point.show(r.x, r.y);
Point.show(p.getX(), p.getY());
Point.show(r.getX(), r.getY());
~~~

같은 객체의 p.x와 p.getX()가 다른 이유와 floor(-0.5)의 값을 설명하라. 별개의 static field 예로 Base에 static int x=3, Sub에 static double x=4.5가 선언되어 있고 Sub extends Base라면, Sub의 instance method에서 x, super.x, ((Base)this).x는 각각 무엇인가? Field hiding이 부모 field를 없애는가?

[NM004, PDF pp.34-37][NM004]; [RM001, PDF pp.37-39][RM001]; [NT001, STT 01:06:05, 01:07:58, 01:09:54][NT001]

<details><summary>정답</summary>

r과 p는 객체 하나를 가리킨다. 첫 이동은 RealPoint에서 move(float,float)를 골라 자식 fields를 (-1.5,2.25)로 만든다. 둘째는 p의 Point 타입에서 move(int,int)를 선택하지만 instance dispatch로 RealPoint의 override에 들어간다. 그 body가 float overload에 위임하여 자식 fields는 (-0.5,-0.75)가 된다. 부모 Point의 int fields는 (0,0)으로 남는다.

첫 show는 p.x/p.y의 int 타입으로 show(int,int)를 선택하여 (0, 0)이다. 둘째는 r.x/r.y의 float 타입으로 show(float,float)를 선택하여 (-0.5, -0.75)다. 셋째와 넷째 getter는 모두 실제 RealPoint의 override를 실행한다. Floor(-0.5)=-1, floor(-0.75)=-1이고 반환 타입은 int이므로 둘 다 show(int,int)에서 (-1, -1)이다.

p.x는 Point에 선언된 field를 읽지만 p.getX()는 실제 receiver의 override에서 RealPoint.x를 읽는다. Field는 선언 타입으로, overload는 인자 식 타입으로, override body는 실제 receiver로 선택한다. 단순 int cast의 0 방향 절단과 Math.floor의 내림을 혼동하면 안 된다.

별도 static 예의 결과는 4.5, 3, 3이다. Sub.x와 Base.x는 각각 존재한다. Super나 Base 타입의 cast 식으로 부모 선언을 선택할 뿐 부모 field가 지워지거나 하나의 field가 override되는 것이 아니다.

NM004의 소수 예와 달리 여기서는 정확히 표현되는 수를 골랐고 NT001의 double이라는 표현과 달리 선언은 float다. 확인할 점은 네 호출 각각의 expression type·선택 signature·실행 body·field 대상을 연결하는 것이다.

</details>

#### 회상 Q23 Compile-time 선택 뒤 runtime body

다음은 모든 body가 명시된 별도 학습용 예다. 네 println의 출력과, inspect 안에서 다시 이루어지는 sound/kind의 선택을 각각 설명하라.

~~~text
class Animal {
    static String kind() { return "A"; }
    String sound() { return "quiet"; }
}
class Dog extends Animal {
    static String kind() { return "D"; }
    @Override String sound() { return "woof"; }
}
class Probe {
    static String inspect(Animal x) { return "via-A:" + x.sound() + ":" + x.kind(); }
    static String inspect(Dog x) { return "via-D:" + x.sound() + ":" + x.kind(); }
}
Animal a = new Dog();
Dog d = new Dog();
System.out.println(Probe.inspect(a));
System.out.println(Probe.inspect(d));
System.out.println(Probe.inspect((Animal)d));
System.out.println(((Animal)d).sound());
~~~

별도로 Polynomial이 times(Polynomial), times(int), times(float), times(Polynomial,int)를 제공한다고 할 때 poly.times(4), poly.times(7.5f), poly.times(other,2)의 선택 목록을 쓰라. Body와 다항식 parser가 없을 때 계산 결과도 정할 수 있는가? Employee e=new Manager(); e.getSalary()의 선언 검사→실제 구현→code 실행 과정을 NM004 도식과 연결하라. Overloaded body가 bytecode에서 모두 사라진다는 주장, compiler가 선언 타입을 모른다는 주장, 매 호출 선형 검색/더 느린 실행을 도식이 보장한다는 주장도 판정하라.

[NM004, PDF pp.39-43][NM004]; [RM001, PDF pp.37-39, 46-47][RM001]; [NT001, STT 01:11:50, 01:15:28, 01:16:18, 01:17:13, 01:18:07][NT001]

<details><summary>정답</summary>

네 출력은 다음과 같다.

~~~text
via-A:woof:A
via-D:woof:D
via-A:woof:A
woof
~~~

첫 inspect는 인자 a의 선언 타입 Animal로 inspect(Animal)을 선택한다. 그 body에서 sound()는 실제 Dog receiver의 override이므로 woof다. kind는 static이고 body의 x가 Animal 타입이므로 A다. 둘째는 Dog 식 d로 inspect(Dog)를 고르며 sound는 woof, static kind는 D다. 셋째는 cast 식이 Animal이므로 첫 overload를 골라 via-A:woof:A다. Overload를 고른 뒤 실제 Dog라는 이유로 다른 overload로 바뀌지 않는다. 마지막 cast도 객체를 바꾸지 않아 Dog.sound를 호출한다. 상위 타입 cast는 super.sound()처럼 부모 body를 직접 지정하는 것과 다르다.

Polynomial 세 선택은 times(int), times(float), times(Polynomial,int)다. 인자 개수와 타입으로 compile time에 선택하며 static polymorphism이라는 용어가 해당 선언에 반드시 static 키워드가 있다는 뜻은 아니다. Body와 parser가 없으므로 실제 다항식 계산값은 만들 수 없다.

Employee 호출은 먼저 선언 타입에서 signature와 호출 가능성을 검사하고 실제 Manager의 해당 instance 구현을 실행한다. NM004 도식은 현재 class에서 구현을 찾고 없으면 직접 superclass를 따라 Object까지 찾는 관계, method data의 code location을 참조하고 code를 실행하는 관계를 설명한다.

이 개념도는 overload body의 삭제를 뜻하지 않는다. Compiler는 선언 타입을 알고 있으며 signature 외에도 필요한 정적 검사를 한다. 그림의 메모리 상자나 탐색 화살표로 모든 JVM의 실제 배치·매 호출 선형 검색·항상 더 큰 비용을 확정할 수도 없다. NT001의 그런 넓은 표현은 도식이 뒷받침하는 선택 관계와 구별한다. 확인할 점은 호출의 각 단계에서 사용하는 타입 정보를 분리하는 것이다.

</details>

#### 회상 Q24 내장 operator의 타입과 평가 과정

다음 값과 문자열의 결과를 계산하라. 정수 11은 1011, 6은 0110이다.

~~~text
11 & 6
11 | 6
true & false
true | false
7 + 8
"7" + 8
String s = "Cat" + " sits.";
String old = s;
s += "Again!";
~~~

s와 old의 내용, +=가 원래 String 객체를 제자리에서 수정하는지 설명하라. 아래 두 식은 각각 독립적으로 분석한다. 논리 결과뿐 아니라 오른쪽 평가와 오류 여부도 구별하라.

~~~text
int den = 0;
boolean a = den != 0 && 12 / den == 2;
boolean b = den != 0 & 12 / den == 2;
~~~

true || 오른쪽식과 true | 오른쪽식도 평가 방식이 같은가? NM004 p.44의 원문 float f = 0.5 % 0.3;이 그대로 허용되는지 literal/result 타입으로 설명하고, 변수 타입만 맞춘 별도 수정 예와 소수 결과의 한계를 쓰라. 사용자가 자기 class의 +를 정의할 수 있는지도 판단하라.

[NM004, PDF pp.44-46][NM004]; [M002, PDF pp.40-42, 48, 66-70][M002]; [T007, STT 24:17, 25:11][T007]; [NT001, STT 01:19:07, 01:20:06][NT001]

<details><summary>정답</summary>

1011 AND 0110=0010이므로 2, OR는 1111이므로 15다. Boolean true & false는 false, true | false는 true다. 숫자 7+8은 15, String을 포함한 연결은 "78"이다. 같은 기호도 operand 타입에 따라 Java가 정한 의미를 사용한다.

첫 s는 "Cat sits."이고 += 뒤는 "Cat sits.Again!"이다. 추가 공백이 없으므로 마침표 뒤에 바로 Again이 붙는다. old는 계속 "Cat sits."다. 불변 String 자체를 수정한 것이 아니라 연결 결과를 s에 다시 대입한다.

&&의 왼쪽 den!=0이 false여서 오른쪽을 생략하므로 a=false다. &는 boolean이어도 양쪽을 평가해 12/0에서 ArithmeticException이 생기므로 b의 정상적인 값이 만들어지지 않는다. true || 오른쪽식은 오른쪽을 생략하지만 true | 오른쪽식은 평가한다. Side effect나 오류가 있는 식에서는 결과의 논리값만으로 두 방식이 같다고 할 수 없다.

원문의 0.5와 0.3은 double literal이고 % 결과도 double이다. Float 변수에 그대로 넣는 것은 자동 narrowing이 아니므로 허용되지 않는다. 별도의 수정 예 double f = 0.5 % 0.3;은 변수 타입을 맞춘 것이지 원본 선언을 정확한 코드로 인용한 것이 아니다. 부동소수점 remainder라는 의미를 보존하되 결과가 정확한 십진수 0.2라고 보장하지 않는다.

Java는 이런 내장 의미를 제공하지만 사용자가 임의로 자기 class의 operator overload를 정의하지는 못한다. 확인할 점은 비트 연산·boolean 결합·단락 평가와 literal 타입을 구분하는 것이다.

</details>

#### 회상 Q25 Cast의 호환성·호출 가능성·실패 시점

Life에는 breed()만, Animal extends Life에는 move()가 있고 Mammal→Dog→Beagle은 Animal 아래로 이어진다고 하자. Dog와 Beagle에 추가 override는 없다고 가정한다.

~~~text
Dog dog = new Beagle();
Mammal m = dog;
Animal a = (Animal)dog;
Beagle b = (Beagle)dog;
Life x = new Animal();
Life y = new Life();
Life z = null;
~~~

Dog/m/a/b가 가리키는 객체와 각 변환 방향을 설명하라. 다음 호출은 서로 독립적이다. Compile-time 허용 여부와, 허용된다면 정상 호출/실행 중 cast 실패/null receiver 실패를 구분하라.

~~~text
x.move();
((Animal)x).move();
((Animal)y).move();
((Animal)z).move();
~~~

Instanceof guard를 쓰면 y/z에서 무엇이 달라지는가? Cast가 객체·변수 선언·접근 제한·instance override를 바꾸는지 설명하고 upcast를 쓰는 목적도 쓰라.

[NM004, PDF pp.47-50][NM004]; [RM001, PDF pp.37, 39-43][RM001]; [NT001, STT 01:22:07, 01:23:05, 01:23:53, 01:24:50][NT001]

<details><summary>정답</summary>

dog/m/a/b는 모두 처음 만든 같은 Beagle 객체를 가리킨다. Dog에서 Mammal/Animal로 보는 것은 upcast이며 m의 대입은 암시적이다. Beagle로 보는 downcast는 실제 객체가 Beagle이므로 호환된다. Cast는 새 객체를 만들거나 원래 dog 변수의 선언을 다시 쓰지 않는다.

x.move()는 선언 타입 Life에 move가 없어 compile-time error다. ((Animal)x).move()는 cast가 실제 Animal 객체와 맞아 정상적으로 Animal의 move를 호출할 수 있다. ((Animal)y)는 관련 type 사이의 표현이라 쓸 수는 있지만 실제 Life 객체가 Animal이 아니므로 runtime에 ClassCastException이고 move까지 가지 않는다. Null을 Animal로 cast하면 null을 얻으므로 cast 자체의 class 불일치가 아니다. 그 뒤 z의 move 호출에서 NullPointerException이다.

if (value instanceof Animal) 안에서만 Animal로 cast하여 move를 부르면 y는 Animal이 아니고 z는 null이어서 둘 다 body를 생략한다. x는 검사 후 호출 가능하다. 이 guard는 실제 객체 호환성과 null을 확인하는 것이며 접근 제한을 없애 주지는 않는다.

Upcast는 구체 종류를 몰라도 상위 계약으로 공통 코드를 쓰게 한다. Cast가 객체의 실제 class를 바꾸지 않으므로 instance override가 있으면 상위 타입 cast 뒤에도 실제 receiver의 구현을 따른다. NT001의 변수 type이 바뀐다는 표현은 cast 식의 타입과 변수 선언을 구별하여 읽어야 한다. 확인할 점은 정적 호출 가능성, 실제 객체 호환성, non-null receiver라는 별개 조건이다.

</details>

#### 회상 Q26 Generics 도입의 E와 물음표

구체 타입마다 비슷한 List 구조를 반복하는 대신 원소 타입 자리를 남긴다는 관점에서 Generics/parametric polymorphism의 동기를 설명하라. 다음 선언 관계에서 E가 무엇을 연결하는지 말하고, `List<Integer>`와 `List<String>`의 원소 타입을 각각 쓰라.

~~~text
abstract class AbstractList<E> implements List<E> { /* 공통 구현의 자리 */ }
~~~

E는 ?와 같은 wildcard인가? E를 항상 Object 또는 primitive로 바꾸어 읽어도 되는가? Integer가 Number의 subtype이라는 이유만으로 `List<Integer>`를 `List<Number>`로 자동 취급할 수 있는가? `Collection<?>` 표기가 임의 타입의 값을 아무 연산으로 넣을 자유를 뜻하는지도 판단하라.

NT001의 arbitrary type during runtime과 자료의 모든 runtime type error가 사라진다는 설명을 각각 어떻게 한정해야 하는가? 이 짧은 도입에서 상세 generic 구현·bounds·Producer-Consumer까지 배웠다고 결론낼 수 있는가?

[NM001, PDF p.56][NM001]; [NM004, PDF pp.52, 59, 66][NM004]; [NM005, PDF p.8][NM005]; [NT001, STT 16:41, 01:25:47, 01:26:45][NT001]

<details><summary>정답</summary>

Generics는 method/class/interface에 type variable을 두어 공통 구조를 여러 타입에 적용하는 방식이다. 같은 구조를 타입별로 반복하는 부담을 줄이려는 동기이며 자료는 parametric polymorphism이라고 부른다. E는 이름 붙인 type parameter이고 위 관계는 공통 구현층과 List 계약의 원소 타입을 같은 E로 유지한다. `List<Integer>`에서는 Integer, `List<String>`에서는 String이다.

E와 ?는 다르다. ?는 어떤 특정 원소 타입인지 여기서 이름 붙이지 않는 wildcard 표기다. E를 임의로 Object로 치환하거나 항상 primitive로 unboxing하여 읽을 수 없다. Integer는 wrapper이며 type parameter를 보존해야 한다. Integer의 subtype 관계가 `List<Integer>`를 `List<Number>`로 자동 바꾸는 규칙을 주지 않는다. `Collection<?>`도 아무 타입이나 넣고 모든 연산을 안전하게 할 수 있다는 뜻은 아니다. 이 문제는 그런 상세 변환·연산 규칙을 구현하도록 요구하지 않는다.

NT001의 during runtime 표현을 실행 중 임의 타입으로 자유롭게 바뀐다는 규칙으로 받아들이면 안 된다. NM004 p.59의 compile-time 타입 검사 이점과 구별한다. 반대로 NM004 p.59와 NM005 p.8의 모든 runtime type error가 사라진다는 일반화도 과도하다. 일부 부적합한 사용을 컴파일 때 발견한다는 이점과 모든 실행 오류의 부재는 다르다.

NT001은 상세를 다음 시간으로 미룬다. 여기의 범위는 placeholder 동기와 E/? 구별이다. 후속 generic class/method/constructor, bounds와 wildcard 연산, Producer-Consumer 구현으로 확대할 수 없다. 확인할 점은 표기의 타입 연결을 보존하고 이 도입을 완전한 구현 교육으로 바꾸지 않는 것이다.

</details>

### 통합 연습

#### 연습 P01 목록의 내용 동등성·표현·문자열 순서

다음은 가상의 품목을 표현하는 독립된 통합 연습이다. code는 항상 non-null이고 아래 객체의 비교 정보는 바뀌지 않는다. Java의 List/ArrayList/Collections를 사용한다. HashCode 구현은 의도적으로 제시하지 않았다.

~~~text
class Item implements Comparable<Item> {
    final String code;
    final int stock;
    Item(String code, int stock) { this.code = code; this.stock = stock; }
    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Item)) return false;
        return code.equals(((Item)o).code);
    }
    @Override public String toString() { return code + "#" + stock; }
    public int compareTo(Item other) { return code.compareTo(other.code); }
}
Item a = new Item("ba", 4);
Item b = new Item("b", 6);
Item c = new Item("aa", 9);
Item d = new Item("ba", 1);
List<Item> items = new ArrayList<>();
items.add(a); items.add(b); items.add(c); items.add(d); items.add(null);
int count = Collections.frequency(items, new Item("ba", 0));
int missing = Collections.frequency(items, null);
Item firstRemoved = items.remove(4);
Item secondRemoved = items.remove(3);
Item observed = items.get(1);
Collections.sort(items);
System.out.println(items);
~~~

1. Count/missing와 두 remove/get 반환값, 각 제거 뒤 상태와 최종 size를 구하라.
2. Sort의 비교 기준을 code의 첫 차이/접두사로 확인하고 최종 출력까지 계산하라. ToString의 stock이 순서를 바꾸는가?
3. A==d, a.equals(d), a.compareTo(d), a/d의 문자열 표현을 비교하라. 같은 문자열 표현·동등성·동순위·identity 중 무엇을 각각 검사하는가?
4. Non-null code 조건이 없으면 어떤 equals 경로가 위험한가? Null을 남긴 채 이 compareTo로 정렬해도 안전하다고 할 수 있는가?
5. Hash 기반 사용까지 계약을 맞추려면 a/d의 hash 값에 어떤 조건이 필요한가? 같은 hash가 다른 code의 동등성까지 뜻하는지, 나중에 표현만 바꿀 때 equality/order도 바뀌는지 설명하라. 새 hash 함수 구현은 요구하지 않는다.

[NM001, PDF pp.12-24, 33-46][NM001]; [NT001, STT 01:48, 05:25][NT001]

<details><summary>정답</summary>

처음 목록은 [a,b,c,d,null]이다. 찾는 Item("ba",0)의 equals는 stock을 읽지 않으므로 a와 d를 세어 count=2다. Null 검색은 null slot 하나를 세어 missing=1이다. 이 두 경로는 null receiver로 equals를 부르지 않도록 분리된다.

remove(4)는 index 4의 null을 반환하고 [a,b,c,d]를 남긴다. remove(3)는 그다음 index 3의 d를 반환하고 [a,b,c]를 남긴다. get(1)은 b를 반환하며 목록을 바꾸지 않는다. 최종 size는 3이고 sort는 새 객체를 추가하지 않는다.

문자열 aa는 a와 b의 첫 문자 차이 때문에 b와 ba보다 앞선다. 문자열 b와 ba는 첫 b가 같고 짧은 문자열 전체가 공통 접두사이므로 길이 차이 1-2=-1에 따라 b가 앞선다. 따라서 정렬 순서는 c,b,a다. 최종 출력은 다음과 같다.

~~~text
[aa#9, b#6, ba#4]
~~~

CompareTo가 code만 읽으므로 stock의 크기는 순서를 바꾸지 않는다. ToString은 그 순서의 각 객체를 표시할 뿐이다.

a와 d는 별개 객체이므로 a==d는 false다. code가 같아 a.equals(d)는 true이고, 같은 code 문자열의 compareTo는 0이다. 문자열 표현은 ba#4와 ba#1로 서로 다르다. 이 설계의 equality와 ordering 기준은 code이며 표시된 모든 정보가 같아야 한다는 정의가 아니다. 표현, 내용 동등성, 순서의 0, reference identity를 분리해야 한다.

code가 null인 별도 Item과 비교하면 identity guard를 통과한 뒤 code.equals(...)의 null receiver가 위험하다. Null 비교 인자 자체는 instanceof에서 거부되지만 내부 null field 문제는 별개다. CompareTo도 other/code가 non-null이라는 전제로 읽었으므로 null을 남긴 목록을 이 구현으로 안전하게 정렬할 수 있다는 보장은 없다. 실제 정렬 구현의 비교 순서를 추측해 예외 발생 시점을 단정하지 않는다.

a와 d는 equals로 같으므로 같은 hashCode를 가져야 한다. 다른 code의 객체가 우연히 같은 hash를 가질 수 있어 그 역은 성립하지 않는다. 비교 정보가 변하지 않을 때 equals와 hash의 일관성도 유지되어야 한다. 현재 제시된 class에는 hashCode가 없으므로 hash 기반 계약 전체를 완성했다고 할 수 없다. ToString만 바꾸면 equals/compareTo의 code 기준은 그대로다.

확인할 점은 null 분기, zero-based 제거 위치, 동등성과 표시의 다른 필드, 접두사 비교, equal→같은 hash라는 방향을 모두 사용한 답인지다.

</details>

#### 연습 P02 좌표 초기화·이동·공통 계산에 대한 위임

아래는 좌표 이동을 기록하는 독립된 통합 연습이다. JDK 11 기준이며 모든 수는 작고 유한하다. Main 안의 사용 부분과 같은 class의 static 계산 helper 문맥을 가정한다.

~~~text
class Vec {
    float x, y;
    Vec(float x, float y) {
        this.x = x; this.y = y; System.out.println("F");
    }
    Vec(int x, int y) {
        this((float)x, (float)y); System.out.println("I");
    }
    Vec() { this(0, 0); System.out.println("Z"); }
    void move(int dx, int dy) { move((float)dx, (float)dy); }
    void move(float dx, float dy) { x += dx; y += dy; }
    public String toString() { return "(" + x + "," + y + ")"; }
    void debug() { System.out.println("point=" + this); }
    void debug(String message) { System.out.print(message); debug(); }
}
static double abs_add(double a, double b) { return Math.abs(a) + Math.abs(b); }
static double abs_add(double[] xs) {
    double sum = 0;
    for (int i = 0; i < xs.length; i++) sum = abs_add(sum, xs[i]);
    return sum;
}
static double power(double x, int n) {
    if (n <= 0) return 1;
    return x * power(x, n - 1);
}
static double power(double x) { return power(x, 2); }

Vec v = new Vec();
v.move(-2, 1);
v.move(0.5f, -0.5f);
v.debug("end: ");
double pathCost = abs_add(new double[]{-2.0, 1.0, 0.5, -0.5});
double finalCost = abs_add(v.x, v.y);
double squareX = power(v.x);
double negativeExponent = power(v.x, -1);
~~~

1. Constructor 경로와 모든 출력, 각 move 후 좌표를 순서대로 쓰라. Move(int,int)가 하는 일은 상속 또는 constructor 호출인가?
2. PathCost의 각 sum과 최종값, finalCost, squareX의 위임·재귀 계산, negativeExponent를 구하라. PathCost와 finalCost가 달라도 모순이 아닌 이유를 설명하라.
3. Debug의 공통 표시를 바꿀 때 위임의 이점과 속도 보장의 유무를 설명하라.
4. Vec()에서 this(0.0,0.0)로 바꾸면 어떤 문제가 있는가? 별도의 double/double constructor를 극좌표로 추가하면 float/double 차이를 정밀도 차이로만 볼 수 있는가? This 경로와 superclass 초기화·instance overriding도 구별하라.

[NM004, PDF pp.11-19][NM004]; [M002, PDF pp.40-42][M002]; [RM001, PDF pp.48-51][RM001]; [NT001, STT 33:13, 34:41, 39:33, 41:23, 44:12, 46:08][NT001]

<details><summary>정답</summary>

new Vec()의 위임은 무인자→int/int→float/float다. 공통 constructor의 대입이 끝난 뒤 돌아오므로 F, I, Z가 차례로 출력된다. 같은 객체 한 개의 초기화다. 초기 좌표는 (0.0,0.0)이다.

move(-2,1)은 int/int overload를 골라 float로 변환하여 float/float body에 위임하고 (-2.0,1.0)을 만든다. 둘째 호출은 float/float를 직접 골라 (-1.5,0.5)가 된다. Debug(String)은 print 후 debug()에 위임하고 toString은 표현을 반환하므로 다음 출력 한 줄은 end: point=(-1.5,0.5)다. 전체 출력은 다음과 같다.

~~~text
F
I
Z
end: point=(-1.5,0.5)
~~~

move의 위임은 서로 다른 signature를 가진 instance overload 사이의 일반 호출이다. Extends 상속이나 this(...) constructor 위임이 아니다.

PathCost의 sum은 0→2→3→3.5→4이므로 4.0이다. FinalCost는 |-1.5|+|0.5|=2.0이다. 전자는 각 이동량 성분의 절댓값을 누적하고 후자는 최종 좌표의 절댓값을 더한다. 반대 방향 이동이 최종 좌표에서 일부 상쇄되므로 두 값이 달라도 모순이 아니다.

power(v.x)는 power(-1.5,2)로 위임한다. -1.5×power(-1.5,1)→(-1.5)×(-1.5)×power(-1.5,0)=2.25다. negativeExponent는 n=-1이 base case n<=0을 만족하여 1.0이다. 이 body를 수학적 역수 계산으로 해석할 수 없다.

Debug의 field 표시를 기본 debug() 한곳에서 바꾸면 String overload가 이를 재사용한다. Overload를 독립 복사본으로 유지하는 부담을 줄이지만 속도 향상이나 손해는 이 코드로 보장할 수 없다.

0.0은 double이므로 제시된 float/int constructor에 자동 narrowing하여 전달되지 않는다. 0.0f라면 float 경로를 직접 선택한다. 별도의 double/double 극좌표 constructor를 추가하면 같은 숫자 쌍도 타입에 따라 좌표계 의미까지 달라질 수 있으므로 정밀도 차이만은 아니다. This(...)는 같은 class 초기화에 대한 위임, super(...)는 부모 초기화이고 둘 다 constructor의 dynamic override가 아니다. JDK 11에서는 명시적 constructor 위임이 첫 문장이어야 하며 NM004가 별도 언급한 Java 25 예외의 상세를 여기서 추가하지 않는다.

확인할 점은 constructor·일반 overload 위임을 구별하고, 이동 후 상태와 두 종류 합·재귀 base case를 각각 계산하는 것이다.

</details>

#### 연습 P03 Interface·abstract 상태와 두 단계 dispatch

다음은 소리를 표현하는 가상 장치의 독립된 통합 연습이다. 모든 클래스는 같은 package에 있다.

~~~text
interface SoundSource {
    String sound();
    default String caption() { return "[" + sound() + "]"; }
    static String api() { return "sound"; }
}
abstract class Device implements SoundSource {
    protected String tag;
    Device(String tag) { this.tag = tag; }
    static String kind() { return "Device"; }
}
class Alarm extends Device {
    Alarm(String tag) { super(tag); }
    public String sound() { return "alarm-" + tag; }
    static String kind() { return "Alarm"; }
}
class Silent extends Device {
    Silent(String tag) { super(tag); }
    public String sound() { return "silent-" + tag; }
}
class Reporter {
    static String report(Device x) {
        return "D:" + x.caption() + ":" + x.kind();
    }
    static String report(Alarm x) {
        return "A:" + x.caption() + ":" + x.kind();
    }
}
Device d = new Alarm("r");
Alarm a = new Alarm("s");
System.out.println(Reporter.report(d));
System.out.println(Reporter.report(a));
System.out.println(Reporter.report((Device)a));
System.out.println(SoundSource.api());
System.out.println(d.kind());
System.out.println(d.caption());
System.out.println(((Alarm)d).sound());
~~~

1. 일곱 출력을 순서대로 쓰고 각 report signature, 그 body의 static kind, default caption 안의 instance sound 선택을 구별하라.
2. Device가 직접 sound body를 쓰지 않아도 되는 이유, Alarm의 public 구현과 부모 constructor 호출의 역할을 설명하라. 이 구조에서 interface/abstract class가 담당하는 책임은 무엇인가?
3. 다음 세 경우를 서로 독립적으로 분석하라: new Device("x"), Device other=new Silent("q"); 뒤 ((Alarm)other).sound(), Device n=null; 뒤 Reporter.report((Alarm)n). 마지막 경우는 선택 signature와 실행 중 실패를 모두 설명하라. Non-null이며 Alarm인 경우에만 sound를 호출하는 instanceof guard도 쓰라.
4. 상위 타입 cast로 Alarm의 sound 대신 Device의 body를 강제할 수 있는가? Report의 반환형만 바꾼 같은 parameter 목록을 추가할 수 있는지도 판단하라.

[NM001, PDF pp.26-32, 47, 49-56][NM001]; [NM004, PDF pp.8-9, 25, 32, 39-43, 47-50][NM004]; [RM001, PDF pp.37-39, 46-48][RM001]; [NT001, STT 10:13, 01:11:50, 01:24:50][NT001]

<details><summary>정답</summary>

일곱 출력은 다음과 같다.

~~~text
D:[alarm-r]:Device
A:[alarm-s]:Alarm
D:[alarm-s]:Device
sound
Device
[alarm-r]
alarm-r
~~~

첫 report는 인자 식 d가 Device라 report(Device)를 고른다. 그 body의 x도 Device이므로 static kind는 Device다. caption은 interface의 default body를 사용하지만 그 안의 sound는 실제 Alarm의 public instance 구현을 호출하여 alarm-r을 얻는다.

둘째는 Alarm 식 a로 report(Alarm)을 골라 prefix A와 static Alarm.kind를 사용하고 caption은 alarm-s를 감싼다. 셋째는 cast 식 Device로 report(Device)를 골라 prefix D와 Device.kind를 쓰지만 실제 Alarm의 sound는 유지되어 alarm-s다. SoundSource.api는 interface static 호출이다. d.kind()는 선언 타입 Device에 따라 Device이고 d.caption()은 실제 Alarm의 sound를 사용한다. 마지막 downcast는 실제 객체가 Alarm이어서 맞으며 alarm-r을 얻는다.

Device는 abstract여서 SoundSource의 남은 abstract sound 의무를 다음 concrete class에 남길 수 있다. Alarm과 Silent는 public String sound()로 계약을 만족한다. Interface는 sound/caption의 공통 계약과 default 동작을, Device는 tag 상태와 공통 constructor 초기화를 제공한다. Super(tag)는 같은 객체의 부모 부분을 초기화하는 것이며 constructor overriding이 아니다.

new Device("x")는 abstract class를 직접 만들려 하므로 compile-time error다. other는 선언상 Device여서 Alarm cast를 쓸 수 있지만 실제 객체가 Silent이므로 실행 중 cast에서 ClassCastException이다. n을 Alarm로 cast한 결과는 null이다. report의 signature는 cast 식의 타입으로 report(Alarm)을 선택하지만 body의 x.caption()에서 null receiver로 NullPointerException이 생긴다. Signature 선택의 성공은 receiver의 안전성 보장이 아니다.

조건을 드러내는 guard는 다음과 같다.

~~~text
if (other instanceof Alarm) {
    Alarm alarm = (Alarm)other;
    alarm.sound();
}
~~~

other가 Silent이거나 null이면 body를 생략한다. 실제 Alarm이면 같은 객체를 확인하고 사용한다. 상위 cast는 객체를 바꾸지 않으며 instance sound를 부모 body로 되돌리지 않는다. 이 Device에는 sound의 concrete body도 없다. 같은 report(Device) 또는 report(Alarm)에 반환형만 달리한 선언을 더할 수 없다. Java signature가 같기 때문이다.

확인할 점은 interface default body 안에서도 instance 호출은 실제 receiver를 따르며, overload/static 선택·abstract 구현 의무·초기화·cast 실패는 각각 별개의 조건이라는 것이다.

</details>

## 출처

- [NT001](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2), 강의 기록: STT 00:48, 10:13, 27:51, 01:11:50, 01:25:47, 01:26:45.
- [NM001: Inheritance 2](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf), PDF pp.3-56. 관련 원본 쪽: [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-023), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-047), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056).
- [NM004: Polymorphism](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf), PDF pp.4-50, 52; pp.59, 66은 도입의 오해 방지 한정. 관련 원본 쪽: [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-041), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-044).
- [NM005: Polymorphism 실습 자료](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf), 물리 36쪽 중 recap pp.4-6: [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-004). P.8은 runtime-error 일반화의 한정에만 사용한다.
- [RM001: Inheritance 1](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf), 선택 선수자료 PDF pp.12-23, 32, 34-51, 55-67.
- [M002: Java Basics 1](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf), 선수자료 PDF pp.40-42, 48, 61, 66-70.
- [T007: 과거 기초 설명](https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/2026-09-08), 2026-09-08 기록의 STT 15:58, 16:54, 24:17, 25:11.

NT001의 수업 날짜는 확인되지 않았다. 95개 발화의 00:03부터 01:27:32까지의 표시는 각 시작 시각이며, 종료 시각이나 녹음 길이를 확정하지 않는다. 업로드·제목·시간표·상대적 주차로 날짜를 정하지 않는다. 음성·공백 구간·화자 신원·별도 학생 질문·칠판·live code는 미확인이고 불명확한 표현이 남아 있다. 코드와 수치 계산은 의미 추적이며 실제 실행·시간 측정 결과가 아니다.

NM001의 상세 예는 자료 보충이고 RM001·M002·T007은 선수·과거 자료이며, 이를 모두 NT001에서 새로 설명한 내용으로 보지 않는다. NM005의 Lab 1/Lab 6 표기로 세션이나 날짜를 확정하지 않는다. Generics는 타입 변수의 동기와 표기 도입까지만 다루며, 상세 Generics·Producer–Consumer와 실습 전체 구현은 범위 밖이다. 원자료의 오류와 올바른 적용 조건은 해당 설명에서 구별한다.

두 비공식 복기는 현재 담당 교수 Jaemin Yoo(유재민)와 별개이며, 2025년 봄학기 중간의 김상한과 2026년 봄학기 기말의 유영재라는 교수명 및 연도·시험 구분은 파일명에만 근거한다. 교수 신원·학기·시험 종류의 독립 확인과 검증된 공식 정답은 없다. 복기의 문제 순서·표현은 부정확할 수 있다. 29개 검토 가능 항목과 별개로 기말 1-(i), PDF p.1은 본문이 없어 제외하며, 중복 (f)·불완전 문구와 중간 10번의 수치 불일치는 임의 보완하지 않는다. 연결은 명시된 개념·풀이 구조에 한정하며 현재 수업의 출제 방식·범위·빈도를 뜻하지 않는다. 모든 Q/P는 일반·통합 강의 연습이다. 쪽수는 표지를 포함해 1부터 센 물리 PDF 쪽수다.

[M002]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf
[NM001]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf
[NM004]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf
[NM005]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf
[NT001]: https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2
[RM001]: https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf
[T007]: https://jhlee1020lee.github.io/2026-fall-study-hub/courses/computer_programming/transcripts/2026-09-08
