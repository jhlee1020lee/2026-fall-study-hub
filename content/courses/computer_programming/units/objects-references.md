---
title: "Objects·Constructors·Static과 Reference 전달"
description: "OOP 책임, 초기화·static 공유와 reference 전달·GC를 상태 추적으로 복습한다."
course: "computer_programming"
unit_id: "objects-references"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 1 Introduction.pdf", "Lecture 2 Java Basics 1.pdf", "4 oop.pdf", "Lab03 v2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-01-lecture-01", "courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

각 대입이 variable의 reference를 바꾸는지, 공유 object의 field를 바꾸는지 표시한다. Class·constructor·static·method 호출을 그 저장 모델에 연결하면 caller에 남는 결과를 설명할 수 있다.

## Object로 상태와 행동의 책임 묶기

[[courses/computer_programming/units/methods|Method]]는 작업을 묶는다. Object-oriented programming(OOP, 객체지향 프로그래밍)은 여기서 더 나아가 software를 **상태와 행동을 가진 objects의 상호작용**으로 바라본다. Object(객체)는 물리적인 자동차뿐 아니라 개념적인 bank account나 software entity인 Linked List도 나타낼 수 있다. Linked List의 구현까지 지금 필요하다는 뜻은 아니다. M011 p.3의 사람·집·자동차 모델은 사람에서 집으로 `lives in`, 자동차로 `drives`라는 관계를 연결한다. 객체의 목록뿐 아니라 객체 사이의 관계도 프로그램의 모델에 포함된다는 뜻이다.

[Computer Programming M011, PDF pp.3–6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf)의 coffee 예를 생각해 보자. Procedural(절차적) 설명은 원두 준비, 분쇄, 물 준비, 끓이기, 원두 넣기, 섞기를 순서대로 나열한다. OOP 설명은 grind·boil·mix 기능을 Coffee Machine이라는 객체의 책임으로 모으고, 사용자가 재료를 넣어 기능을 사용하게 한다. 기능 목록 자체가 조리 순서는 아니다. 객체는 어떤 기능을 제공하는지 정하고, caller가 필요한 순서로 요청한다.

[[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 03:38의 핵심도 OOP가 새로운 종류의 계산을 가능하게 한다기보다 큰 프로그램을 이해·확장·관리하기 좋은 구조를 만든다는 것이다. Java와 C++은 이 원리를 배우는 도구로 소개되지만, 여기서 C++ 구현을 추가하지는 않는다.

### Class와 instance, reference variable

Class(클래스)는 object의 blueprint(설계도)다. Instance(인스턴스)는 그 class로 만든 object이며 instantiate는 생성 행위다. Attributes(속성)는 appearance나 state를 나타내고 methods는 행동을 정의한다. 둘을 members(멤버)라고 한다.

```java
class Car {
    int width = 10;
    String color = "red";
}
```

Method body에서 `Car car = new Car();`를 실행하면 `Car`라는 type의 reference variable `car`와 새 Car object가 구별된다. `new Car()`가 object를 만들며, `car`는 그것을 가리키는 값을 저장한다. `car.width`를 읽으면 10이고 `car.width = 5;` 뒤에는 5다. Fuel·speed·color처럼 물리적 부품이 아닌 상태도 attribute가 될 수 있다.

`Car car = new Car(), newCar = new Car();`는 두 objects를 만든다. `newCar.color = "blue";` 뒤에도 `car.color`는 red다. 같은 class를 사용한다고 instance fields까지 공유하는 것은 아니다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 13:45 및 M011 pp.7–14의 구별이다. 2025-1 복기의 정의 항목을 읽을 때도 class를 설명하는 문장과 실제 instance·reference를 식별하는 문장을 함께 만들면 관계가 분명해진다. 이는 공식 답안 없는 복기 자료의 선택적 연결이다. [EX:cp_2025_1_midterm_q01 p.1]

명시적으로 초기화하지 않은 fields에는 기본값이 있다. `boolean`은 false, `int`는 0, `float`은 0.0, String reference는 null이다. `char`의 기본값은 `'\u0000'`이며, 자료의 빈 것처럼 보이는 표기를 유효한 빈 char literal로 읽으면 안 된다. 이 규칙은 읽기 전에 대입해야 하는 local variable과 다르다.

## Receiver가 결정하는 instance method의 상태

M011 p.15의 호출은 type 이름과 variable 이름의 차이를 드러낸다.

```java
class Car {
    void printHello() {
        System.out.println("Hello World!");
    }
}
```

이 별도 예제의 객체를 `Car car = new Car();`로 만든 뒤 `car.printHello();`를 부른다. Dot 앞의 `car`가 receiver(호출 대상)를 정하고, method 이름과 괄호가 행동을 고른다. `printHello`는 non-static instance method이므로 type 이름 `Car`를 receiver 대신 쓰면 안 된다. `void`여도 `Hello World!`를 출력한다.

M011 p.16의 `getSpeed()`는 `return speed;`다. `myCar.speed = 100`, `yourCar.speed = 90`이면 각각의 호출 결과는 100과 90이다. 같은 method 정의가 다른 receiver의 상태를 읽는다.

반면 9월 19일 확보된 [Lab03 M014, PDF pp.6–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf)의 자료 기반 예는 `speed = 10`이고 body가 `return 10 * speed;`다. 따라서 field를 읽으면 10, method를 부르면 100이다. `getSpeed`라는 이름만으로 단순 getter라고 가정하거나 두 자료의 body를 합치면 안 된다.

## Constructor와 this가 정하는 초기 상태

Constructor(생성자)는 object 생성 과정의 특별한 초기화 구성이다. Class와 이름이 같으며 return type을 쓰지 않는다. `void`도 붙이지 않는다. M011 p.20의 `Car()`는 생성할 때 `A car is created.`를 출력한다. Parameter를 받으면 서로 다른 초기화 경로를 만들 수 있다.

```java
public class Car {
    int weight;
    String color = "unknown";

    Car(int w) { weight = w; }
    Car(int w, String c) {
        weight = w;
        color = c;
    }

    void printInfo() {
        System.out.println(weight + " kg, " + color);
    }
}
```

M011 p.22에서 `new Car(1500, "red").printInfo();`는 `1500 kg, red`, `new Car(2000).printInfo();`는 `2000 kg, unknown`을 출력한다. 둘째 constructor 경로는 color initializer를 그대로 둔다. 이 class에 선언된 것은 두 parameter 형태이며 무인자 constructor는 없다. 초기화를 모아 두면 object 생성 후 관련 fields를 따로 설정하다 빠뜨리는 일을 줄인다.

Lab03 p.8의 자료 보충은 carNumber와 model을 1234·Sonata로 초기화하고 `Car initialized.` 메시지를 보인다. 다만 선언의 `myCar`와 출력문의 `mayCar.model`이 불일치하므로, 자료에 적힌 의도된 `1234 Sonata` 출력과 인쇄 코드 그대로의 유효성은 구별한다.

### Shadowing이 있을 때의 this

`this`는 현재 object를 가리킨다. Parameter가 field와 이름이 같아 field를 가리는 shadowing(이름 가림)이 있으면 명시적인 구별이 필요하다.

```java
class Car {
    int speed = 30;

    void cantChangeSpeed(int speed) {
        speed = speed;
    }

    void changeSpeed(int speed) {
        this.speed = speed;
    }
}
```

M011 p.26의 첫 method는 parameter를 자기 자신에게 대입한다. 둘째는 receiver의 field를 parameter 값으로 바꾼다. 하지만 `this`가 없다고 언제나 local을 뜻하는 것은 아니다. P.24의 `changeColor()`에는 local color가 없으므로 `this.color = "red";` 다음 `color = "blue";`는 같은 field를 차례로 바꾼다. 출력은 red, blue이며 최종 field도 blue다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 24:11의 둘째 대입은 local만 바꾼다는 설명은 인쇄 코드와 충돌하여 이처럼 명시적으로 바로잡는다.

M011 p.25의 다음 class 내부 method 조각은 `this`의 다른 용도다.

```java
int speed = 100;
String speedAndUnit() {
    return speed + " km/h";
}
void printSpeedAndUnit() {
    System.out.println(this.speedAndUnit());
}
```

`car.printSpeedAndUnit()`는 `100 km/h`를 출력한다. 여기서는 `this.speedAndUnit()`의 this를 생략해도 같은 receiver다. `printSpeedAndUnit`의 대소문자도 identifier의 일부다.

Lab03 p.9는 **자료 기반 constructor 연결**을 추가한다. `Car()`의 `this(55, "blue")`가 두 parameter constructor를 부르므로 field initializer가 처음 100/red여도 이 생성 경로의 최종 상태는 55/blue다. `this.printSpeed()`는 method 호출, `this(...)`는 constructor 연결이다. Constructor를 일반 method처럼 임의 재호출하는 것은 아니며, 연결이 가능하므로 생성마다 constructor body 하나만 실행된다는 식의 일반화도 하지 않는다. 상세 연결은 9월 15일에는 유보되었다.

## static member의 공유 상태와 receiver 제한

Static member(정적 멤버)는 개별 object보다 class와 연결된다. `Car.num`과 `Car.printNum()`은 먼저 instance를 만들지 않고 사용할 수 있다. M011 pp.27–30의 각 자동차 상태와 전체 개수의 대비를 코드로 읽으면 다음과 같다.

```java
class Car {
    static int num;
    static int totalMile;
    int mile;

    Car() { num++; }

    void setMile(int mile) {
        this.mile = mile;
        totalMile += mile;
    }
}
```

Class의 두 int fields는 0에서 시작한다. 세 objects를 만들고 각 object에 `setMile(20)`, `setMile(30)`, `setMile(40)`을 한 번씩 호출하면 `num = 3`, `totalMile = 90`이다. 각 `mile`은 별개지만 `totalMile`은 공유된다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 33:33

이름이 자동으로 의미를 보장하지는 않는다. Setter를 다시 호출하면 이 코드가 새 입력을 또 더하므로 totalMile이 현재 instance mile들의 합과 달라질 수 있다. Num도 생성 횟수를 셀 뿐 살아 있는 object 수를 자동 추적하지 않는다.

Lab03 p.10의 static owner 예는 공유 String field를 두 constructors가 연속 대입하고, 한 instance를 통한 대입을 다른 instance에서 읽은 뒤 class 이름으로 다시 바꾼다. 개인 이름 literal을 첫째·둘째·셋째·넷째 값으로 바꾸어 설명하면, 두 번 생성 후에는 둘째 값, 첫 관찰 출력은 셋째 값, 마지막 출력은 넷째 값이다. 같은 field를 갱신하는 구조가 핵심이다.

### Static context에는 암묵적인 instance가 없다

```java
class Car {
    float fuel;
    static float totalFuel() {
        return fuel; // invalid unqualified instance access
    }
}
```

M011 p.32와 M014 p.11의 이 **오류 예**는 어느 Car의 fuel인지 정하지 못한다. Static method에는 특정 object인 `this`가 없기 때문이다. `new Car()`를 다른 곳에 한 번 추가해도 method 정의의 문제는 해결되지 않는다. `non-static variable fuel cannot be referenced from a static context`는 compile diagnostic이지 실행 중 출력이 아니다.

금지되는 것은 receiver 없는 직접 접근이다. Static code도 명시적인 object reference로 instance field나 method에 접근할 수 있으며, instance method에서 static member를 쓰는 것도 가능하다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 36:24 주변의 반대로 말한 static/non-static 문장을 올바른 규칙으로 채택하지 않는다.

## Reference 대입과 객체의 identity

Reference assignment(참조 대입)는 object를 복제하지 않는다.

```java
String str1 = new String("hey");
String str2 = new String("hey");
String str3 = str1;
```

M011 p.35에서 `str1 == str2`는 false, `str1 == str3`은 true다. 첫 둘은 별도 objects이고 마지막 대입은 str1의 reference 값을 복사한다. 같은 내용과 같은 객체는 서로 다른 관계다.

```java
Car myCar = new Car();
Car car1 = myCar;
Car car2 = myCar;
Car car3 = car1;
```

이 예에는 `new`가 한 번뿐이므로 네 variables가 한 object를 가리킨다. 한 reference를 통해 field를 바꾸면 다른 references로 읽어도 같은 변경이 보인다. 반대로 Lab03 p.12의 처음 두 `new Car()`는 다른 objects라 비교가 false이며 `car2 = car1` 뒤에는 true다. [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT]] 08:32의 “We don't get false”라는 부정 표현은 자료의 false/true 결과와 충돌한다. 그 발화를 확정된 identity 규칙으로 바꾸지 않는다.

## Argument는 reference까지 값으로 복사된다

Java의 argument passing(인수 전달)은 **항상 값 복사**다. Primitive이면 primitive 값을, reference이면 reference 값을 parameter에 복사한다. Caller variable과 callee(피호출자)의 parameter는 별개 저장 대상이다.

### Primitive parameter의 local swap

M011 pp.37–39의 `swap(int a, int b)` 안에서는 다음을 수행한다.

```java
int temp = a;
a = b;
b = temp;
```

Caller의 초기 a=2, b=3을 받으면 callee는 local a=3, b=2, temp=2가 되지만 caller는 2,3을 유지한다. Parameter 이름이 같아도 caller 저장 공간을 가리키는 별명은 아니다. Lab03 p.13의 `changeNumber(int number)`도 parameter를 100으로 대입하지만 caller number=10은 그대로여서 10을 출력한다.

원자료의 별도 심화 예 M011 pp.49–50에는 마지막 줄이 `a = temp`로 인쇄되어 있다. 그대로 실행을 추적하면 local a도 다시 2가 되고 b는 3이어서 p.50 그림의 3/2와 다르다. 이 오타를 몰래 고쳐 인용하지 않는다. 두 버전 모두 caller x=2, y=3을 바꾸지 못한다는 결론은 같다.

### Copied reference를 통한 공유 field 변경

`IntHolder`가 constructor로 초기화한 `int value` field를 갖는다고 하자. Caller가 value=2와 value=3인 두 holders를 전달하면 callee의 `a`·`b`는 같은 objects를 가리키는 reference 복사본이다. M011 p.41의 변경 대상은 parameter 자체가 아니라 fields다.

```java
int temp = a.value;
a.value = b.value;
b.value = temp;
```

이제 caller도 공유 objects의 values를 3,2로 읽는다. M014 p.14의 자료 예에서도 `car1`이 speed=50인 Car를 가리킨 채 `changeSpeed(car1)`를 호출하면, 전달되는 것은 정수 50이나 object 전체가 아니라 **car1에 저장된 reference 값**이다. Callee의 `car.speed = 100`은 공유 object를 바꾸므로 caller의 `car1.speed`도 100이다. 반면 callee의 `car`에 다른 reference를 대입하는 것은 caller `car1`을 재대입하지 않는다.

강의와 slides는 이 효과를 call-by-reference라고도 부른다. 정확한 Java 규칙은 reference 값까지 call-by-value(값 전달)라는 것이며, M011 p.42에도 이 관점의 단서가 있다. 객체 전체 복사 비용 없이 같은 객체에 접근할 수 있다는 설명과 caller variable 자체를 바꿀 수 있다는 주장은 구별해야 한다.

### String swap과 Wrapper field swap

M011 pp.52–53의 String swap은 `temp = a; a = b; b = temp;`로 **callee의 reference variables**만 바꾼다. Caller s1=`"Hi"`, s2=`"all"`은 그대로다. 그림에서는 caller에서 시작한 연결과 callee a·b의 저장값을 따로 보아야 한다. Reference가 교차하는 모습을 보았다고 caller까지 교환되었다고 판단하면 안 된다.

반면 수업의 `Wrapper`는 String field `s`를 가진 별도 class다. Caller → Wrapper object → String이라는 두 단계가 생긴다. Pp.55–56의 다음 method-body 조각은 공유된 Wrapper의 fields를 바꾼다.

```java
String temp = a.s;
a.s = b.s;
b.s = temp;
```

결과적으로 caller가 읽는 `s1.s`와 `s2.s`는 all, Hi가 된다. String 문자 내용을 고친 것도, caller의 Wrapper reference 자체를 바꾼 것도 아니다. 그림에서는 Wrapper field에서 String으로 이어지는 한 단계가 추가된 점에 주목하면 된다.

원본 p.51의 마지막 줄 `a = temp`는 local swap조차 완성하지 않으며, p.54의 `a.s = temp`도 의도한 field swap과 다르다. 여기서는 정확한 pp.52–53·55–56의 대입 순서를 사용하고, 원본 Wrapper class 전체를 실행 가능한 완성 프로그램으로 바꾸지 않는다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 54:55–55:51 주변의 plain String swap이 결국 성공한다는 발화 역시 caller 교환 성공으로 채택하지 않는다. 이 심화 설명을 9월 17일에 다시 모두 했다고 볼 근거도 없다.

## Object lifetime과 garbage collection

Primitive variable의 저장값은 바로 2 같은 값이지만 reference variable에서는 저장된 reference를 따라 object에 도달한다. M011 pp.46–48의 symbol table(심벌 테이블)은 이름과 저장 위치를 연결하는 도식이다. 이를 특정 JVM에서 표가 어디에 놓이는지나 실제 물리 주소값을 보장하는 설명으로 확대하지 않는다.

`new`는 필요한 object memory를 할당하며, garbage collector(GC, 가비지 컬렉터)는 더 이상 사용되지 않는 objects의 memory를 회수한다. 9월 15일 설명의 swap 안에서 만든 `new IntHolder(4)`가 반환 후 다른 곳에서 참조되지 않는 경우는 회수 가능한 상태가 되는 예다. Method가 반환하는 즉시 반드시 회수된다는 뜻은 아니다. [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT]] 12:50도 자동 memory 관리를 설명한다.

2025-1 복기의 GC 항목에 연결할 때도 생성·도달 가능성·수거 가능 상태·실제 수거 시점을 나누어 설명해야 한다. 복기본은 즉시 회수나 정확한 시점을 보장하지 않고 공식 답안도 없다. [EX:cp_2025_1_midterm_q03 p.2]

C의 명시적 allocation/free와 대비되는 핵심은 관리 책임이다. 자동 관리가 `new` 같은 생성 표현도 쓰지 않는다는 뜻은 아니며, 특정 언어가 항상 몇 배 빠르다는 일반 법칙도 아니다. 게임의 health=0, simulation 종료, object가 GC 대상이 되는 일은 각각 application 상태·실행 흐름·memory lifetime의 다른 사건이다. 이런 상태를 누가 바꿀 수 있게 할지는 [[courses/computer_programming/units/encapsulation|Encapsulation과 접근 제어]]에서 다룬다.

## 핵심 정리

- Class는 정의, instance는 생성된 object, reference variable은 그것을 가리키는 값의 저장소다.
- Instance method는 receiver가 필요하다. `this`의 생략 효과는 shadowing 유무에 달린다.
- Static field는 공유되지만 counter·합계의 의미는 실제 갱신 코드가 결정한다.
- Java는 reference도 값으로 복사한다. Parameter 재대입과 shared field 변경을 구별한다.
- GC 대상이 될 수 있다는 것과 실제 수거 시점은 다르다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · Capabilities와 절차

Coffee Machine의 grind·boil·mix와 사용자의 커피 절차는 같은 목록인가? OOP의 objects·interaction을 물리적 물체에만 한정할 수 있는가?

<details><summary>해설 보기</summary>

Capabilities는 객체가 제공하는 기능이고 사용 절차는 caller가 재료와 요청을 어떤 순서로 준비·실행하는지다. OOP는 그 책임을 상태·행동을 가진 objects와 상호작용으로 나눈다. Car뿐 아니라 bank account 같은 개념적 대상, Linked List 같은 software entity도 모델일 수 있다. 사람→집의 lives in, 사람→차의 drives처럼 관계도 중요하다. 새 계산 능력을 주기보다 큰 프로그램의 이해·확장·관리를 돕는 구조이며 Linked List 구현까지 현재 선수는 아니다.

**확인 기준:** 기능 목록/호출 순서·state/behavior·entity/관계를 구별한다.

</details>

#### 확인 Q02 · Class·instance·기본값

Car에 width=10,color="red"가 있다. `Car car=new Car(), newCar=new Car(); car.width=5; newCar.color="blue";` 뒤 각각의 상태와 object 수는? 초기화하지 않은 fields와 local의 차이도 설명하라.

<details><summary>해설 보기</summary>

Objects는2개다. Car는 class/type, car·newCar는 reference variables이며 각각 새 instance를 가리킨다. `car`의 상태는 5/red, `newCar`는 10/blue다. Attributes와 methods를 members라 하고 같은 정의를 사용해도 instance fields는 별도다. 미초기화 field는 boolean false,int0,float0.0,String null,char `'\u0000'`의 defaults를 받지만 local은 읽기 전 대입이 필요하다. 빈 char literal로 기본값을 쓰면 안 된다.

**확인 기준:** 2개 객체·두 상태·reference와 field defaults를 포함한다.

</details>

#### 확인 Q03 · Receiver와 method body

`Car car=new Car(); car.printHello();`에서 `Car`와 `car`의 역할은? Non-static `void printHello`는 `Hello World!`를 출력한다. 각 receiver의 `speed`가 100과 90일 때 `return speed`인 method의 결과를 구하고, `speed = 10`에서 `return 10*speed`인 Lab03 method와 구별하라.

<details><summary>해설 보기</summary>

Car는 type이고 car가 receiver 객체를 가리킨다. Instance method를 `Car.printHello()`로 대신 부를 수 없으며 void여도 Hello World!를 출력한다. `return speed`에서는 receiver speed100/90에 따라100/90을 반환한다. Lab03 별도 body는 field10을 읽어100을 반환하므로 field 출력10과 method 결과100이 다르다. 이름 getSpeed만으로 body를 추정하지 않는다.

**확인 기준:** 대소문자와 receiver 구별, 두 source bodies의 차이를 설명한다.

</details>

#### 확인 Q04 · Constructor의 초기 상태

`color` initializer는 unknown이고 `Car(int w)`는 weight만, `Car(int w,String c)`는 두 fields를 설정한다. `new Car(1500,"red")`, `new Car(2000)`의 상태·printInfo 결과, no-arg 여부를 설명하라. Lab03 myCar/mayCar 문제는?

<details><summary>해설 보기</summary>

각각1500/red와2000/unknown, printInfo는 `1500 kg, red`, `2000 kg, unknown`이다. 두 번째 경로는 color initializer를 유지한다. 선언된 두 parameter 형태에 no-arg는 없으며 constructor는 class와 이름이 같고 void를 포함한 return type이 없다. 생성 때 초기화 책임을 모은다. Lab03은 myCar 선언 뒤 mayCar.model을 써 literal 코드 유효성과 의도된1234 Sonata 출력을 구별해야 한다.

**확인 기준:** 두 경로·initializer 유지·return type 없음·원문 typo를 구별한다.

</details>

#### 확인 Q05 · Shadowing이 있는 경우와 없는 경우

Field speed=30에서 parameter speed=80을 받아 `speed=speed`와 `this.speed=speed`를 각각 독립 실행하면? Local color가 없는 method의 `this.color="red"; color="blue";`는?

<details><summary>해설 보기</summary>

첫 대입은 parameter 자신만 대입해 field30 유지, 둘째는 receiver field를80으로 바꾼다. `color`를 가리는 local이 없으면 두 color 표기는 같은 field여서 red 다음blue가 되고 최종blue다. ‘`this` 없으면 무조건 local’이라는 설명은 틀리다. 이 color 결론은 잘못된 강의 발화를 조용히 정상 발화로 바꾸지 않고 printed code를 읽어 정정한 것이다.

**확인 기준:** 각 대입의 저장 대상을 parameter/field로 표시한다.

</details>

#### 확인 Q06 · Method의 this와 constructor 연결

`speed = 100`에서 speedAndUnit이 `speed+" km/h"`를 반환하고 printSpeedAndUnit이 `println(this.speedAndUnit())`한다. 호출과 출력을 적어라. 별도 Lab03 Car()가 `this(55,"blue")`로 fields를 설정하면 초기100/red는 어떻게 되는가?

<details><summary>해설 보기</summary>

`car.printSpeedAndUnit()`는 `100 km/h`를 출력하며 이 context에서는 this를 생략해도 같은 receiver다. Lab03 chain의 최종 상태는55/blue다. `this.printSpeed()` 같은 method 호출과 `this(...)` constructor 연결은 다르다. Constructor를 보통 method처럼 임의 재호출하는 뜻도, 생성당 body가 무조건 하나라는 뜻도 아니다. 상세 연결은 후취득 자료 보충이며 당시 deferred 설명 전체를 복원하지 않는다.

**확인 기준:** 정확한 printSpeedAndUnit 철자·출력·두 this 용도를 구별한다.

</details>

#### 확인 Q07 · 공유 counter와 실제 합계

Static num,totalMile은0이고 constructor는 num++, setMile(v)는 `this.mile=v; totalMile+=v;`다. 세 objects에20,30,40을 한 번씩 설정한 뒤 첫 object에20을 다시 설정하면? Static owner에 생성/대입으로 첫째→둘째→셋째→넷째 값을 넣는 경우도 설명하라.

<details><summary>해설 보기</summary>

처음 num3,totalMile90이고 mile은20,30,40이다. 반복 설정 후 num3,totalMile110이며 현재 mile합은 여전히90이다. Counter는 생성 횟수이지 생존 object 수가 아니며 totalMile도 코드가 입력을 누적할 뿐이다. `owner`는 하나의 shared field라 두 생성 후 둘째 값, 한 instance를 통한 셋째 대입을 다른 instance로 읽으면 셋째, class를 통한 마지막 대입 후 넷째다. Personal literals는 필요하지 않다.

**확인 기준:** 3/90→3/110과 instance합90, owner의 공유를 설명한다.

</details>

#### 확인 Q08 · Static context의 receiver

`float fuel; static float totalFuel(){return fuel;}`의 오류는 무엇인가? 다른 곳에 new Car() 하나를 만들면 고쳐지는가? Static과 instance 사이의 허용된 접근을 설명하라.

<details><summary>해설 보기</summary>

`fuel`은 존재하지만 어느 Car의 fuel인지 정할 암묵적 receiver가 static method에 없다. 따라서 compile diagnostic이며 정상 runtime 출력이 아니다. 외부에서 new를 한 번 실행한다고 그 정의에 receiver가 생기지 않는다. Static code도 명시적 object reference를 통해 instance member에 접근할 수 있고 instance method는 static member를 사용할 수 있다.

**확인 기준:** ‘객체 존재’가 아닌 ‘receiver 지정’ 문제임을 설명한다.

</details>

#### 확인 Q09 · Reference 수와 object 수

별개의 new String("hey")인 str1,str2와 str3=str1의 == 결과는? `Car myCar=new Car(); car1=myCar; car2=myCar; car3=car1;`의 object 수와 한 field 변경의 관찰 결과도 설명하라.

<details><summary>해설 보기</summary>

`str1 == str2`는 false, str1==str3은 true다. Reference 대입은 값을 복사하며 object 복제가 아니다. Car 예는 new 한 번으로 object1개를 네 variables가 가리켜 한 field 변경을 모두 읽는다. 별도 Car 둘의 비교는 false지만 car2=car1 뒤 true다. 9월17일 ‘don't get false’ 발화는 이 결과와 충돌하며 확정 규칙으로 채택하지 않는다.

**확인 기준:** new 수·alias·identity와 내용 비교를 구별한다.

</details>

#### 확인 Q10 · Primitive swap의 두 저장소

Caller x2,y3을 parameters a,b로 복사한 뒤 temp=a; a=b; b=temp;를 실행한다. Caller와 locals는? 마지막 줄이 원문 일부처럼 a=temp이면 diagram의3/2와 맞는가? `changeNumber`가 10의 parameter를100으로 바꾸면?

<details><summary>해설 보기</summary>

정상 local swap은 temp2,a3,b2지만 caller x2,y3은 그대로다. 마지막 줄이 a=temp이면 local도a2,b3이 되어 diagram3/2와 충돌한다. 두 버전 모두 caller 저장소를 대입하지 않기 때문이다. `changeNumber`도 parameter100일 뿐 caller10은 유지되어10을 출력한다. 같은 이름이 caller 변수의 alias를 만들지 않는다.

**확인 기준:** 올바른/인쇄 오류 local trace와 caller 불변을 모두 적는다.

</details>

#### 확인 Q11 · 복사된 reference와 field 변경

`Car car1`은 `speed`가 50인 `Car` 객체를 가리킨다. `changeSpeed(car1)`을 호출하면 parameter `Car car`를 통해 `car.speed=100`을 실행한다. 무엇이 복사되고 caller가 무엇을 읽는가? Local car를 다른 객체로 바꾸는 경우와 IntHolder value2/3의 field swap도 비교하라.

<details><summary>해설 보기</summary>

복사되는 것은 reference 값이지 정수50이나 Car 전체가 아니다. Caller와 parameter가 같은 객체를 가리켜 field 대입 후 car1.speed도100이다. Local car 재대입은 caller car1을 바꾸지 않는다. Holders의 temp=a.value; a.value=b.value; b.value=temp;는 공유 fields를3/2로 바꿔 caller에도 보인다. Java는 reference도 by value로 전달하며 source의 call-by-reference 표현을 caller variable 자체 교환으로 읽으면 안 된다.

**확인 기준:** 복사값·field mutation·parameter rebinding의 세 구별이 필수다.

</details>

#### 확인 Q12 · String swap의 변경 대상

Caller s1="Hi",s2="all"을 a,b로 전달해 temp=a; a=b; b=temp;한다. Callee와 caller references 및 String 내용은 어떻게 되는가?

<details><summary>해설 보기</summary>

Callee a는all,b는Hi로 바뀌지만 caller s1은Hi,s2는all이다. Parameter reference 복사본만 재대입했고 caller 저장소와 String 문자에는 쓰지 않았다. 그림의 local 화살표 교차만 보고 caller 교환 성공으로 판정하면 안 된다. 원본 p51의 a=temp 마지막 줄은 local swap조차 완성하지 않는다.

**확인 기준:** Caller/callee 네 references와 문자 불변을 확인한다.

</details>

#### 확인 Q13 · Wrapper의 한 단계 더 깊은 slot

Wrapper에는 String field s가 있고 두 객체의 s가 Hi/all이다. `temp = a.s`; a.s=b.s; b.s=temp를 실행하면 caller는? 마지막 줄이 p54처럼 a.s=temp이면?

<details><summary>해설 보기</summary>

올바른 field swap은 공유 Wrapper.s를 all/Hi로 바꾸어 caller도 그 값을 읽는다. Caller의 Wrapper references나 String 문자를 바꾸지 않고 caller→Wrapper→String 중 두 번째 연결을 바꾼 것이다. 잘못된 마지막 a.s=temp는 첫 field를Hi로 되돌리고 둘째는all이라 원래대로 남는다. Pp55–56의 올바른 순서와 p54 인쇄 코드를 구별하며 원본 전체를 완성 실행 프로그램으로 간주하지 않는다.

**확인 기준:** Reference 두 단계·두 trace·변경되지 않는 대상을 설명한다.

</details>

#### 확인 Q14 · 수거 가능성과 실제 시점

Method 안의 new IntHolder(4)가 return 후 어디에서도 참조되지 않는다. GC가 즉시 실행되었는가? Primitive/reference 저장 모델과 health0·simulation 종료도 구별하라.

<details><summary>해설 보기</summary>

회수 가능한 상태가 될 수 있을 뿐 즉시 회수를 보장하지 않는다. Primitive 저장소에는 값, reference 저장소에는 객체로 이어지는 reference가 있고 symbol-table 그림은 논리 모델이지 물리 주소 보장이 아니다. Java 자동 관리는 unused object memory 회수 책임을 맡지만 new 생성 표현을 없애지 않는다. Health0은 application 상태, simulation 종료는 control flow이며 object 도달 가능성과 별개다. C의 explicit free와 대비가 보편적 성능 배수를 증명하지도 않는다.

**확인 기준:** 도달 가능성·eligibility·실제 수거·application 상태를 분리한다.

</details>

### 적용 연습

#### 연습 P01 · 새 생성과 남은 reference

**새로 작성한 synthetic 기출 응용 연습.** [EX:cp_2025_1_midterm_q01 p.1]의 class/instance 관계와 [EX:cp_2025_1_midterm_q03 p.2]의 GC 조건을 생성·alias·재대입 추적으로 옮겼다. 선수는 본문의 new·reference·GC이며 공식 답안 없는 복기 자료다.
```java
Car a = new Car();
Car b = a;
a = new Car();
b = null;
```
다른 references는 없다고 하자. 각 줄 뒤 object 수와 마지막의 도달 가능성은? 마지막 줄 직후 실제 수거 개수를 확정할 수 있는가?

<details><summary>해설 보기</summary>

생성 누계는1,1,2,2다. 첫 object는 둘째 줄에서 a·b가 공유한다. 셋째 줄은 a만 새 object를 가리키게 해서 첫 object는 b를 통해 남는다. 넷째 줄 뒤 첫 object로의 경로가 없어 회수 대상이 될 수 있고 둘째는 a로 도달한다. 생성 총수와 현재 도달 수는2와1로 다르며 실제 수거가 즉시 일어났는지나 그 수는 코드만으로 확정할 수 없다.

**확인 기준:** 각 줄 생성수와 셋째/넷째 줄의 차이, 실제 GC 한정을 제시한다.

</details>

#### 연습 P02 · Field 변경 뒤 local 재대입

**새로 작성한 강의 기반 일반 연습.** 이 조합의 직접 기출 유형 근거는 없다. `Car`의 instance field `speed`는 0으로 시작한다. `static void helper(Car car)`의 body는 `car.speed=40; car=new Car(); car.speed=90;`다. Caller의 `Car a`는 `a.speed=10`인 객체를 가리킨다. `helper(a)` 호출 뒤 `a.speed`는 얼마인가? Static helper가 이 field들을 만질 수 있는 이유는?

<details><summary>해설 보기</summary>

Caller a는40을 읽는다. 첫 대입은 공유 원래 object를 바꾼다. `new` 이후 local car는 별도 object를 가리키고90은 거기에 저장되어 a를 재대입하지 않는다. Static helper도 명시적인 car receiver를 사용하므로 receiver 없는 fuel 접근과 다르다. 이 추적이 두 objects의 수거 시점을 정하지는 않는다.

**확인 기준:** 40/90의 소속 object와 explicit receiver를 구별한다.

</details>

### 복습 순서

Q01–Q04로 정의와 생성 경로를 설명하고 Q05–Q08은 receiver와 공유 상태를 추적한다. Q09–Q13에서 caller/parameter/object를 세 칸으로 나누어 그린 뒤 Q14와 P01–P02로 도달 가능성을 확인한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|2026-09-01 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 보정 녹음문]] — 01:15:24.
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 보정 녹음문]] — 03:38, 13:45, 33:33, 36:24, 54:55–55:51 (plain `String` swap 성공 발화; caller references는 바뀌지 않음), 57:33 (공유 `Wrapper.s` field 변경).
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 보정 녹음문]] — 08:32, 12:50.

### 강의자료와 해당 페이지

- [Lecture 1 Introduction.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/1.intro.pdf) — [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-012).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048).
- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-003), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-007), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-016), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-020), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-022), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-026), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-030), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-032), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-036), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-039), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-042), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-044), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-053), [p.54](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-054), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-056).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-015).

9월 15일 강의와 9월 17일 복습을 구별한다. Lab03은 9월 19일 확보한 자료 보충이며 17:39 이후 없는 녹음을 복원하지 않는다. Color/static/identity 관련 잘못된 발화와 swap 코드·그림의 불일치는 아래 문항에서도 구별한다. Constructor 예의 myCar/mayCar, 잘못된 마지막 swap 대입은 조용히 수정한 원문으로 제시하지 않는다.

기출 연결은 class·object 관계 [EX:cp_2025_1_midterm_q01 p.1]와 GC 조건 [EX:cp_2025_1_midterm_q03 p.2]다. 기존 [[exam_questions/cp_2025_1_midterm_q01|Class와 Object 문항 미리보기]], [[exam_questions/cp_2025_1_midterm_q03|GC 문항 미리보기]]를 참고할 수 있다. 둘 다 공식 답안 없는 복기 자료이며 수거 시점이나 출제 확률을 보장하지 않는다.


---

[[courses/computer_programming/units/methods|← 이전: Method의 계약·호출·반환과 재사용]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/encapsulation|다음: Encapsulation과 접근·상태 설계 →]]
