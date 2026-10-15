---
title: "오버라이딩·디스패치와 형변환"
description: "Declared type에 따른 선택과 receiver의 override를 분리하여 field·operator·cast를 추적한다."
course: "computer_programming"
unit_id: "polymorphic-dispatch"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["8 polymorphism.pdf", "Lecture 2 Java Basics 1.pdf", "Lab 6 Polymorphism.pdf", "7 inheritance 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/2026-09-01-lecture-01", "courses/computer_programming/lectures/2026-09-08-lecture-03", "courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

## Overriding과 receiver에 따른 dispatch

### 같은 instance method 계약에 다른 구현 제공하기

[Method overloading](method-overloading.md)은 입력의 개수와 type으로 서로 다른 signature를 구별했다. Overriding(재정의)은 다른 문제를 해결한다. 상위 type으로 같은 동작을 요청하면서도 실제 객체의 종류에 맞는 구현을 실행하려는 것이다. NM004의 `Employee`와 `Manager`는 같은 `getSalary()` 계약에 서로 다른 body를 제공한다. [computer_programming:NM004, PDF pp.25-26](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
class Employee {
    public double getSalary() { return 180; }
}

class Manager extends Employee {
    @Override
    public double getSalary() { return 250; }
}
~~~

`new Employee()`의 호출값은 `180.0`, `new Manager()`의 호출값은 `250.0`이다. 둘 다 `double` 반환형을 가지므로 body의 정수 literal은 반환 시 그 type으로 변환된다. `@Override`는 상속된 method를 실제로 재정의하는지 확인하도록 의도를 표시한다. Annotation이 새로운 signature를 만들거나 parameter가 다른 method를 자동으로 override로 바꾸는 것은 아니다.

반환형과 반환하는 값의 type도 구별해야 한다. 자료의 첫 `Laidoff` 대안은 `public double getSalary() { return 0; }`이다. `0`을 반환하는 표현은 `double` 반환형에 맞게 변환될 수 있다. 둘째 대안인 `public int getSalary() { return 0; }`는 method 선언 자체의 반환형을 바꾼다. 이름과 빈 parameter 목록은 같으므로 별도 overload가 아니며 부모의 `double` 반환과 호환되지 않는 overriding이다. 자료 p.28의 diagnostic도 `int`가 `double`과 호환되지 않는다고 설명한다. P.27의 “return type must also be the same”은 이 primitive 반환형 비교에 맞추어 읽는다. Reference 반환형의 모든 호환 규칙까지 “언제나 완전히 같은 type만 가능하다”라고 일반화하지 않는다. [computer_programming:NM004, PDF pp.27-28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 55:45]]

P.27의 같은 이름 `Laidoff` 두 선언은 비교할 대안이다. Pp.26·28의 출력문에는 잘못된 닫는 quotation mark도 있다. 위의 class 핵심만 읽는 것과 그 페이지 전체가 수정 없이 실행되는 프로그램이라고 주장하는 것은 다르다. 날짜 미확인 녹취 55:45–56:45의 끊긴 오류 설명을 완성된 인용문으로 고치지도 않는다.

Constructor는 이 overriding 대상이 아니다. `Manager` 안의 초기화는 `Manager()`처럼 자기 class 이름으로 선언하고, 부모 초기화가 필요하면 `super(...)`로 연결한다. `Manager` 안에 반환형 없는 `Employee()`를 선언하여 부모 constructor를 override할 수는 없다. Constructor는 상속되는 instance method가 아니기 때문이다. [computer_programming:NM004, PDF p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

NM005 p.6의 Object method 연습도 같은 구별로 읽을 수 있다. 그 페이지의 소문자 `string` 표기를 그대로 Java의 `String` type 이름으로 채택하지 않는다. `toString()`이 반환할 type을 올바르게 설명하는 것과 원래 인쇄를 조용히 고친 인용은 별개다. 구체적인 Object 계약은 [Object 계약과 interface 단원](object-contracts-interfaces.md)의 조건을 함께 따른다. [computer_programming:NM005, PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### Type 검사 분기와 객체에 맡기는 동작

Overriding 없이도 외부 helper가 객체의 종류를 검사하여 값을 고를 수 있다. 자료의 `HumanResources.getSalary(Employee e)`는 `static` method이며 다음 분기를 사용한다. 수치 960, 250, 180에는 자료에서 확정한 화폐 단위가 없다. [computer_programming:NM004, PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
if (e instanceof Executive) {
    return 960;
} else if (e instanceof Manager) {
    return 250;
} else {
    return 180;
}
~~~

이 helper는 `e.getSalary()`의 override를 호출해서 값을 얻는 것이 아니다. 각 type을 직접 검사하고 자기 body에 적힌 상수를 고른다. `instanceof Manager`는 Manager 객체뿐 아니라 그 subtype 객체에도 참일 수 있다. 따라서 검사하는 type들 사이에 상속 관계가 있으면 branch의 순서도 중요하다. 보다 넓은 type을 먼저 처리하면 뒤의 구체적인 경우에 도달하지 못할 수 있다. 이 설명만으로 자료가 명시하지 않은 Executive와 Manager 사이의 정확한 상속 관계를 새로 정하지는 않는다.

다른 버전은 `e.getClass().getName()`을 읽고 `"personnelpkg.Executive"`, `"personnelpkg.Manager"`와 비교한다. 여기서 얻는 것은 **실제 class의 정확한 이름**이다. Superclass의 이름을 얻는 동작이 아니며, Manager의 새 subtype은 `instanceof Manager`를 만족해도 이름 문자열이 `"personnelpkg.Manager"`와 같지는 않을 수 있다. 두 검사는 서로 다른 판별 조건이다. `null instanceof Manager`는 false인 반면, `null` reference에 대한 `getClass()` instance 호출은 할 수 없다. [computer_programming:NM004, PDF p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:00:18]]

CEO, Cleaner, Researcher처럼 처리할 종류가 늘어날 때 외부 분기 목록을 계속 갱신해야 한다. 같은 분기가 여러 helper에 흩어져 있으면 한곳을 빼먹어 새 객체를 기본 branch의 값으로 처리할 위험도 있다. Overriding은 해당 동작을 각 class의 책임으로 두고 호출자는 공통 method를 부르게 하는 대안이다. 날짜 미확인 녹취의 이 설명은 유지보수 책임에 관한 것이다. `instanceof`와 `getClass()`의 모든 사용이 나쁘다거나 class 의존성이 모두 사라진다는 주장이 아니다. 자료의 helper 사용부도 구체 class를 직접 생성한다. P.31의 잘못된 `else { return 180 };` 구두점을 성공 코드처럼 그대로 쓰지 않는다. [computer_programming:NM004, PDF p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:01:17]]

### RealPoint: fields, overload, override를 따로 추적하기

같은 이름이 있다고 모든 선택이 runtime dispatch인 것은 아니다. 먼저 field hiding(필드 숨김)을 보자. 자료 p.34의 `Point`에는 `static int x = 2`, subclass `Test`에는 `static double x = 4.7`이 있다. `Test`의 instance method 안에서 `x`, `super.x`, `((Point)this).x`를 읽은 결과는 각각 `4.7`, `2`, `2`다. 두 fields는 별도 선언으로 존재하며, cast가 객체를 다른 객체로 바꾸는 것은 아니다. 같은 이름의 field 선택과 instance method의 overriding을 분리해야 한다. [computer_programming:NM004, PDF p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

RealPoint 예제는 세 가지 선택을 한꺼번에 보여 준다. 부모 `Point`는 정수 좌표 fields와 기본 이동 method, 두 `show` overload를 제공한다. [computer_programming:NM004, PDF p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

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
~~~

Subclass는 같은 이름의 별도 `float` fields를 선언하고 이동과 조회를 바꾼다. [computer_programming:NM004, PDF p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
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

`move(int, int)`는 부모와 signature가 같으므로 override다. `move(float, float)`는 parameter 목록이 달라 overload다. `getX()`, `getY()`는 실제 좌표의 floor(바닥값)를 정수로 돌려주는 override다. 예를 들어 수학적으로 `floor(-1.2) = -2`이므로 음수에서 단순한 정수 cast의 0 방향 절삭과 구별된다.

다음 호출에서 객체는 하나다. `p = rp`는 새 Point를 만들지 않고 같은 RealPoint를 상위 type reference로 보관한다. [computer_programming:NM004, PDF p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

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

처음에는 부모의 `int x, y`와 자식의 `float x, y`가 모두 0이다. 첫 이동은 다음과 같이 나뉜다.

1. `rp`의 선언 type과 두 `float` 인자로 `move(float, float)`를 선택한다.
2. 그 body의 `x, y`는 RealPoint fields이므로 자식 좌표만 바뀐다.
3. 두 번째 호출 `p.move(1, -1)`은 선언 type Point에서 허용되는 `move(int, int)`를 선택한다.
4. 실제 receiver가 RealPoint이므로 그 signature의 RealPoint override를 실행한다.
5. 그 body가 다시 `float` overload에 위임하여 자식 좌표에 `1.0f, -1.0f`를 더한다.

부모의 정수 fields를 증가시키는 `Point.move` body는 이 경로에서 실행되지 않는다. 따라서 그 fields는 `0, 0`으로 남는다. 자식 좌표의 최종 표시는 자료대로 `2.7182798, 3.14159`다. 이 `float` 표시는 이상적인 십진 덧셈 `2.71828`과 동일한 표기를 보장하지 않는다. 표의 수치는 원자료에 있는 값이며 새 실행 측정 결과가 아니다.

| 출력 호출 | 먼저 결정되는 type/field | 실행 또는 값 | 자료의 출력 |
|---|---|---|---|
| `Point.show(p.x, p.y)` | Point의 `int` fields | `show(int, int)`에 0, 0 | `(0, 0)` |
| `Point.show(rp.x, rp.y)` | RealPoint의 `float` fields | `show(float, float)`에 자식 좌표 | `(2.7182798, 3.14159)` |
| `Point.show(p.getX(), p.getY())` | 반환형이 `int`인 호출 | RealPoint getter의 floor 결과 | `(2, 3)` |
| `Point.show(rp.getX(), rp.getY())` | 반환형이 `int`인 호출 | 같은 RealPoint getter | `(2, 3)` |

같은 객체에 대해 `p.x = 0`이고 `p.getX() = 2`일 수 있는 이유가 드러난다. 앞은 reference의 선언 type으로 선택한 부모 field를 읽고, 뒤는 실제 receiver의 method body가 자식 field를 읽는다. `show`가 어떤 overload인지는 그 **인자 expression의 type**으로 정해진다. Getter가 실제로 2라는 값을 반환해서 정수 overload를 고르는 것이 아니라, 선언된 반환형이 `int`이기 때문에 그 overload를 고른다.

날짜 미확인 녹취 01:03:10–01:09:54는 메커니즘을 설명하되 네 `show`의 상세 풀이를 생략한다. 위의 완전한 trace는 NM004 pp.35–37을 읽은 자료 기반 보충이다. 01:07:58의 `double` 발화를 인쇄된 `float`로 바꾼 인용문으로 만들지 않는다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:03:10]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:07:58]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:09:54]]

비공식 타 교수 복원본의 상위 reference·static method·field·override 연결은 바로 이 분리 절차를 요구한다. Cast로 보는 type이 달라져도 같은 receiver의 override가 사라지는 것은 아니라는 점을 먼저 확인하면 된다. 원문의 전체 코드나 출력 답을 옮기지 않는다. [EX:cp_2026_1_final_q02 p.2]

### Compile-time 선택 뒤에 runtime 구현 선택하기

수업 자료는 compile time에 해결하는 overloading을 static/syntactic polymorphism, 실행 중 receiver에 따라 해결하는 overriding을 dynamic/pure polymorphism이라고 부른다. 여기서 “static”이라는 분류어와 `static` method modifier는 구분해야 한다. Instance method도 어느 overload signature를 호출하는지는 compile time에 결정할 수 있다. [computer_programming:NM004, PDF pp.39-40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

Polynomial 예제의 세 호출은 다음 입력 목록을 가진다.

| 호출의 인자 형태 | 선택할 parameter 목록 |
|---|---|
| `poly.times(9)` | `int` |
| `poly.times(85.2f)` | `float` |
| `poly.times(new Polynomial(...), 3)` | `Polynomial, int` |

P.41의 전체 그림에서는 네 `times` 선언의 signatures가 method table의 항목에 대응하고, 세 호출이 자신의 인자 목록에 맞는 항목으로 연결되는 것을 보아야 한다. `times(Polynomial)`도 별도 후보로 보이지만 두 인자 호출은 `times(Polynomial, int)`에 대응한다. 이는 overload의 선택을 설명하는 그림이지 선택되지 않은 method bodies가 binary에서 모두 삭제된다는 뜻이 아니다. Polynomial의 body나 문자열을 해석하는 constructor는 제공되지 않았으므로 이 표에서 실제 다항식 계산 결과를 만들어 낼 수는 없다. [computer_programming:NM004, PDF pp.40-41](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

`Employee e = new Manager(); e.getSalary();`에서는 서로 다른 두 질문을 차례로 푼다. 먼저 선언 type Employee가 `getSalary()` 호출을 허용하는지 검사한다. 그다음 그 signature의 instance method를 실제 Manager receiver에서 실행한다. Compiler가 변수의 선언 type을 모르는 것이 아니다. 선언 type으로 할 수 있는 검사와 실제 객체에 따라 달라지는 구현의 선택이 다르다.

Pp.42–43의 그림은 이 두 번째 선택을 세 단계로 나타낸다. 현재 class의 method에서 시작하여 필요하면 직접 superclass를 따라 Object까지 찾고, 선택된 method data에서 code location을 참조한 뒤, 해당 method code를 실행한다. 그림의 Method Area, RT constant pool, Heap Memory 상자와 화살표는 이 흐름을 설명하는 schematic(개념도)로 읽는다. 모든 JVM의 실제 저장 배치를 확정하거나, 매 호출이 반드시 계층을 선형 검색한다거나, runtime dispatch가 언제나 더 느리다는 성능 결론으로 옮기지 않는다. 날짜 미확인 녹취 01:15:28–01:18:07의 compiler·binary 삭제·검색 비용 관련 불명확한 설명도 이 경계를 넘는 근거로 쓰지 않는다. [computer_programming:NM004, PDF pp.42-43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:15:28]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:18:07]]

비공식 타 교수 복원본의 수치 인자 overload와 override가 결합된 항목 역시 두 단계를 섞으면 풀기 어렵다. 먼저 호출 위치에서 보이는 method 목록과 인자 type으로 signature를 고르고, 그 signature가 instance method이면 receiver의 override를 찾는다. 실행 중 다른 overload를 처음부터 다시 고르는 절차가 아니다. [EX:cp_2026_1_final_q09 p.6]

### Operand type에 따라 달라지는 operator의 의미

같은 표기를 여러 의미로 쓰는 관점은 operator에서도 볼 수 있다. 자료는 이를 operator overloading으로 소개하지만 Java가 사용자가 임의의 operator overload를 정의하는 기능을 제공한다는 뜻은 아니다. 여기서는 언어가 이미 정한 operand type별 의미를 읽는다. [computer_programming:NM004, PDF pp.44-46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| 식 | 의미 | 결과 |
|---|---|---|
| `10 + 20` | 정수 addition | `30` |
| `1.5 + 2.0` | 부동소수점 addition | `3.5` |
| `"10" + "20"` | String concatenation | `"1020"` |
| `"sum = " + 30` | String과 값의 연결 | `"sum = 30"` |

P.44의 삽입 그림에는 `String s = "Dog" + " barks.";`와 `s += "Too Loud!";`가 있다. 첫 문장 뒤의 값은 `"Dog barks."`이고, 둘째 뒤에는 `"Dog barks.Too Loud!"`가 된다. 첫 문자열 끝과 추가 문자열 앞에 공백이 없으므로 `.`와 `Too` 사이에도 새 공백이 생기지 않는다. `+=`는 연결한 결과를 다시 `s`에 대입한다. 불변 String 객체 내부를 고친다는 뜻이 아니라 변수의 reference가 연결 결과를 가리키도록 바뀌는 것이다. [computer_programming:NM004, PDF p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

같은 그림의 `float f = 0.5 % 0.3;`는 원문 그대로 유효한 대입 예가 아니다. M002의 literal·conversion 규칙을 적용하면 `0.5`와 `0.3`은 접미사 없는 `double` literal이므로 `%` 결과도 `double`이다. 그것을 명시적 변환 없이 `float` 변수에 대입할 수 없다. 별도로 작성한 학습용 수선 `double f = 0.5 % 0.3;`는 변수 type을 맞춘다. 이는 원문의 quotation이나 실제 실행 기록이 아니다. 또한 소수의 이진 표현 때문에 결과를 정확한 십진수 0.2로 보장하지 않는다. 날짜 미확인 녹취 01:19:07의 부동소수점 `%` 언급과 이 인쇄 예의 type 분석은 구별된다. [computer_programming:M002, PDF pp.40-42](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:19:07]]

정수의 `&`와 `|`는 각 bit에 적용된다. 자료의 `6`과 `3`은 비교할 낮은 세 bit가 `110`, `011`이다. 두 bit가 모두 1인 위치만 남기면 `010 = 2`, 하나라도 1인 위치를 남기면 `111 = 7`이다. [computer_programming:NM004, PDF p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
  110          110
& 011        | 011
-----        -----
  010          111
~~~

Boolean operands에서는 `true & false`가 false이고 `true | false`가 true다. Boolean의 전체 값에 적용하는 logical 연산과 정수의 자리별 bitwise 연산을 구분한다. 더 나아가 boolean `&`/`|`는 양쪽 operands를 평가하지만 `&&`/`||`는 short-circuit할 수 있다. `&&`는 왼쪽 false일 때, `||`는 왼쪽 true일 때 오른쪽을 생략한다. 최종 진리값이 같은 경우라도 평가 과정까지 같지는 않다.

예를 들어 정수 `denominator = 0`, `numerator = 100`인 상황에서 `denominator != 0 && numerator / denominator > 2`는 왼쪽이 false여서 나눗셈을 평가하지 않는다. `&&`를 `&`로 바꾸면 오른쪽도 평가하므로 0으로 나누는 문제가 생긴다. 이는 앞서 배운 short-circuit 원리를 현재 operator 구별에 연결한 예다. 2026-09-08 녹취 24:17의 설명은 이 앞선 수업의 근거이며, 날짜 미확인 NT001의 새 발화로 합치지 않는다. NT001 01:20:06의 불명확한 operator 발음만으로 정확한 token을 복원하지도 않는다. [computer_programming:M002, PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) [[courses/computer_programming/transcripts/2026-09-08|T007 · 2026-09-08 · 24:17]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:20:06]]

### Cast가 바꾸는 관점과 실제 객체의 경계

자료의 계층은 `Animal → Mammal → Dog → Beagle`이다. 다음 예에서 새로 만든 객체는 처음부터 Beagle 하나다. [computer_programming:NM004, PDF p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
Dog dog = new Beagle();
Mammal mammal = (Mammal)dog;
Animal animal = (Animal)dog;
Beagle beagle = (Beagle)dog;
~~~

Mammal이나 Animal로 보는 upcast(상향 형변환)는 같은 객체를 더 넓은 계약으로 사용한다. Beagle로 보는 downcast(하향 형변환)도 여기서는 실제 객체와 맞는다. Cast가 객체를 새 class로 변환하거나 원래 변수 선언의 type을 바꾸는 것은 아니다. 그 reference를 **해당 expression에서 어떤 type으로 사용할지** 지정한다. 날짜 미확인 녹취 01:22:07의 variable type 변경이라는 표현도 이 구별과 함께 읽는다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:22:07]]

Upcast는 암시적으로도 가능하다. `Employee e = (Employee)(new Executive());`와 `Employee e = new Executive();`는 자료가 비교하는 명시적·암시적 upcast다. 구체적인 subclass 구현을 모두 몰라도 Employee 계약을 사용하는 코드를 쓸 수 있다. 상위 type으로 cast했다고 receiver의 instance override가 정지하는 것은 아니다. 반면 field와 static method의 선택에서는 앞에서 살핀 선언 type의 구별이 계속 중요하다. Cast가 접근 권한까지 우회하는 기능도 아니다. [computer_programming:NM004, PDF p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

Downcast는 실제 객체가 목표 type에 맞는지 따로 확인해야 한다. 자료의 다음 두 상황은 실패하는 단계부터 다르다. [computer_programming:NM004, PDF pp.49-50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| 선언과 사용 | 문제 또는 허용 이유 |
|---|---|
| `Life mylife = new Life();` 뒤 `((Animal)mylife).move()` | 관련 type 사이 cast 표현은 가능해도 실제 객체가 Animal이 아니므로 `ClassCastException`의 대상 |
| `Life mylife = new Animal();` 뒤 `mylife.move()` | Life 계약에 `move`가 없어 compile-time에 허용되지 않는 호출 |
| 실제 Animal을 담은 두 번째 reference의 `((Animal)mylife).move()` | Animal expression의 method에 접근하며 실제 객체도 목표 type에 맞음 |

이 표에서 허용되지 않는 `mylife.move()` 줄과 허용되는 cast 줄은 비교할 대안이다. 오류가 있는 줄까지 같은 프로그램에 두고 그 뒤가 정상 실행된다고 읽지 않는다. “상위 type이라서 안 보이는 method”와 “실제 객체가 목표 subtype이 아닌 cast”를 모두 runtime 오류로 합치면 안 된다. NT001 01:23:53의 불분명한 오류명을 새로 복원하지 않아도 이 두 단계는 인쇄 자료로 구별할 수 있다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:23:53]]

`null`에는 별도의 경계가 있다. `(Animal)null`이라는 reference cast 자체는 `null`을 그대로 나타낸다. 이를 곧바로 instance method의 receiver로 쓰면 객체가 없어 호출할 수 없는 것이며, 실제 Life 객체를 Animal로 잘못 본 경우의 `ClassCastException`과 다르다. `mylife instanceof Animal`은 `null`에서 false이므로, 필요한 subtype 기능에 접근하기 전에 객체의 호환성을 검사하는 데 사용할 수 있다. 이 검사는 모든 설계를 분기로 바꾸라는 뜻이 아니다. 공통 계약이면 override로 호출하고, 정말 subtype의 확장 기능이 필요한 지점에서 declared type과 실제 객체를 함께 확인한다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Override의 반환 계약

Employee의 `public double getSalary()`는 180, Manager의 같은 선언은 250을 반환한다. 두 결과와 `@Override`의 역할을 설명하라. 별도 Laidoff 대안 `double getSalary(){return 0;}`와 `int getSalary(){return 0;}`는 왜 다른가? Manager 안의 반환형 없는 `Employee()`는 constructor override인가?

<details><summary>해설 보기</summary>

호출값은 180.0,250.0이다. 정수 return expression을 선언된 double로 반환하는 변환과 method 선언의 반환형은 구별한다. `double` 대안은 0을 double로 반환할 수 있지만 int 대안은 이름·빈 parameter가 같아 새 overload가 아니며 부모 double 반환과 호환되지 않는 override다. `@Override`는 실제 상속 method를 재정의하는지 확인할 의도를 표시하며 다른 parameter의 method를 override로 바꾸지 않는다. 이 primitive 비교를 모든 reference 반환형이 반드시 동일해야 한다는 규칙으로 일반화하지 않는다.

Constructor는 상속·override 대상이 아니다. Manager는 Manager()를 선언하고 필요한 부모 초기화를 super(...)로 연결한다. Manager 안의 Employee() 선언은 부모 constructor override가 아니다. NM005의 소문자 string은 정확한 type String과 구별한다. 원본의 잘못된 quotation mark나 중복된 대안 class를 고치지 않은 전체 프로그램의 성공으로 주장하지 않는다.

**확인 기준:** 두 결과, expression/declaration 차이, incompatible return, annotation·constructor를 모두 구별한다.

</details>

#### 확인 Q02 · Type 분기의 판정과 책임

`static` helper는 Executive에 960, Manager에 250, 그 밖에 180을 준다. 다른 helper는 `getClass().getName()`의 정확한 이름을 비교한다. 새로운 Manager subtype에서는 두 검사가 같은가? 관련 type의 branch 순서, null, 새 class 추가의 유지보수와 overriding 대안을 설명하라.

<details><summary>해설 보기</summary>

`instanceof Manager`는 Manager의 subtype에도 true지만 exact class-name은 새 구체 class 이름이므로 Manager 문자열과 다를 수 있다. 이는 superclass 이름을 얻는 검사가 아니다. 관련된 type들에서는 넓은 branch가 먼저면 구체 branch를 가릴 수 있지만, 원본에 없는 Executive/Manager 사이 관계를 새로 정하면 안 된다.

`null`은 instanceof 검사들을 false로 만들므로 제시된 분기만 따르면 default 180에 도달한다. 이것이 의미상 유효한 직원이라는 뜻은 아니다. `null`에 getClass()를 호출하는 대안은 receiver가 없어 실패한다. 960/250/180에는 확정된 화폐 단위가 없다.

Helper는 자체 type 분기와 상수로 값을 고르며 `e.getSalary()` override를 호출하는 구조가 아니다. 종류가 늘면 여러 helper 목록의 누락으로 잘못된 기본값이 생길 수 있다. 동작을 각 class의 override에 두고 공통 계약으로 호출하면 그 중앙 갱신 부담을 줄인다. 모든 instanceof/getClass 사용이 잘못되거나 class 의존성이 사라진다는 뜻은 아니다.

**확인 기준:** subtype/exact-name·branch 순서·null·유지보수의 네 차이를 근거로 설명한다.

</details>

#### 확인 Q03 · Field hiding은 별도 선언

`Point`의 `static int x=2`와 `Test extends Point`의 `static double x=4.7`이 있다. Test의 instance method에서 x, super.x, ((Point)this).x를 읽으면? Cast가 객체를 바꾸거나 부모 field를 제거하는가? `floor(-1.2)`와 정수 cast도 구별하라.

<details><summary>해설 보기</summary>

결과는 4.7,2,2다. 단순 x는 Test 선언을, super.x는 부모 선언을, Point로 보는 expression의 x도 Point 선언을 선택한다. 두 fields는 별도 선언으로 남고 객체가 Point로 새로 변하지 않는다. Field hiding을 receiver에 따른 instance override로 처리하면 안 된다.

수학적 floor(-1.2)는 -2지만 단순 `(int)-1.2`는 0 쪽으로 절삭해 -1이다. 따라서 RealPoint getter의 floor 후 int 반환을 단순 cast로 바꾸어 읽으면 음수에서 의미가 달라진다.

**확인 기준:** 세 field 값과 선택 근거, 음수 floor/cast의 두 값을 확인한다.

</details>

#### 확인 Q04 · RealPoint의 네 출력 전체

Point에는 초기 0인 int x,y와 move(int,int)가 있고, RealPoint에는 별도 float x,y, int move의 override→float move 위임, floor를 int로 반환하는 getters가 있다. `RealPoint rp=new RealPoint(); Point p=rp; rp.move(1.71828f,4.14159f); p.move(1,-1);` 뒤 `show(p.x,p.y)`, `show(rp.x,rp.y)`, `show(p.getX(),p.getY())`, `show(rp.getX(),rp.getY())`를 trace하라. Show는 int/int와 float/float static overload다.

<details><summary>해설 보기</summary>

객체는 RealPoint 하나이며 p와 rp는 alias다. 첫 호출의 float 인자는 RealPoint의 float overload를 골라 자식 fields를 바꾼다. 둘째는 Point에서 보이는 int signature를 선택하지만 실제 receiver의 RealPoint override를 실행한다. 그 body가 float overload에 위임하므로 역시 자식 fields만 바뀌고 Point.move body는 실행되지 않는다.

부모 int fields는 0,0이며 자식 float 값의 자료 표시는 2.7182798,3.14159다. 네 호출은 차례로:

1. p의 int fields→show(int,int)→`(0, 0)`.
2. rp의 float fields→show(float,float)→`(2.7182798, 3.14159)`.
3. 실제 RealPoint getters의 floor→int 2,3→show(int,int)→`(2, 3)`.
4. 같은 getter override와 반환 type→`(2, 3)`.

따라서 p.x와 p.getX()가 0과2로 다를 수 있다. Getter의 반환값이 우연히 정수여서 overload를 고르는 것이 아니라 선언 반환형이 int여서 고른다. 소수 표시는 원자료의 float 표현이지 이상적인 십진수 표기나 새 실행 측정의 보장이 아니다.

**확인 기준:** 두 이동의 signature/body/변경 field를 따로 추적하고 네 출력·각 show type을 모두 제시한다.

</details>

#### 확인 Q05 · Overload 선택 후 instance dispatch

Polynomial의 후보는 times(int), times(float), times(Polynomial), times(Polynomial,int)다. `times(9)`, `times(85.2f)`, `times(new Polynomial(...),3)`의 signature를 고르라. Employee e=new Manager(); e.getSalary()의 두 선택 단계와 그림의 method→code 연결은 무엇인가? 이 그림만으로 결과 다항식·binary body 삭제·항상 느린 dispatch를 알 수 있는가?

<details><summary>해설 보기</summary>

인자 type/개수로 차례로 times(int), times(float), times(Polynomial,int)를 선택한다. 두 인자 호출을 한 인자 Polynomial overload와 혼동하지 않는다. 수업의 static/syntactic polymorphism은 이런 compile-time 선택을 뜻하며 method가 반드시 static modifier라는 뜻은 아니다.

Employee 선언에서 getSalary()가 허용되는 signature인지 먼저 검사하고, 같은 signature의 instance body는 실제 Manager receiver의 override를 고른다. Runtime에 다른 overload 전체를 다시 선택하지 않는다. 도식은 현재 class에서 시작해 필요하면 superclass들을 Object 방향으로 확인하고, 선택된 method data에서 code location을 찾아 code를 실행하는 흐름이다.

Polynomial bodies/문자열 constructor 해석은 없어 실제 계산 결과는 정할 수 없다. 도식은 모든 JVM의 저장 배치, 매번 선형 검색, 모든 overloaded bodies의 binary 삭제나 보편적 비용을 증명하지 않는다.

**확인 기준:** 세 signature, 두 단계, code 연결을 설명하고 제공되지 않은 결과·구현·성능을 추정하지 않는다.

</details>

#### 확인 Q06 · Operator의 값과 평가 과정

(a) 10+20, 1.5+2.0, `"10"+"20"`, `"sum = "+30`을 비교하라. (b) `String s="Dog"+" barks."; s+="Too Loud!";`의 값과 String의 변경 여부는? (c) `float f=0.5 % 0.3;`의 type 문제는? (d) 6&3,6|3,true&false,true|false와 &&/||의 평가 차이, denominator=0인 guard를 설명하라.

<details><summary>해설 보기</summary>

수치 addition은 30과3.5, String 연결은 `"1020"`, `"sum = 30"`이다. Java가 정한 operand별 의미이며 사용자가 임의 operator overload를 정의하는 기능은 아니다.

첫 s는 `"Dog barks."`, += 후 `"Dog barks.Too Loud!"`다. 추가 공백이 없으며 연결 결과를 변수에 다시 대입하는 것이지 불변 String 내부를 바꾸지 않는다. 접미사 없는 0.5와0.3은 double이므로 %도 double이며 그대로 float에 대입할 수 없다. 별도 학습용 수선은 `double f=0.5 % 0.3;`로 type을 맞춘다. 이진 표현 때문에 정확한 십진수0.2를 보장하지 않는다.

110과011을 bitwise AND하면010=2, OR하면111=7이다. `boolean` true&false는 false, true|false는 true다. `boolean` &/|는 두 operands를 평가하지만 &&는 왼쪽 false에서, ||는 왼쪽 true에서 오른쪽을 생략할 수 있다. 정수 denominator=0,numerator=100일 때 `denominator != 0 && numerator / denominator > 2`는 왼쪽 false라 나누지 않는다. &로 바꾸면 오른쪽 정수 나눗셈을 평가하여 0 나눗셈 문제가 생긴다. 이 guard의 역사적 근거는 T007 2026-09-08 24:17이며 NT001 새 발화와 합치지 않는다.

**확인 기준:** 네 plus·두 s·double→float·네 AND/OR 결과·생략 조건과 guard를 모두 설명한다.

</details>

#### 확인 Q07 · Cast의 관점과 실패 단계

Animal→Mammal→Dog→Beagle에서 `Dog dog=new Beagle()`를 Mammal/Animal/Beagle로 cast하면 무엇이 유지되는가? Life에 move가 없고 Animal extends Life에만 move가 있을 때 다음 대안들을 구별하라: (a) 실제 Animal을 담은 Life의 move 호출, (b) 같은 reference의 Animal cast 후 move, (c) 실제 Life의 Animal cast, (d) null cast와 instance 호출. `instanceof`와 접근 권한·override의 관계도 설명하라.

<details><summary>해설 보기</summary>

실제 객체는 Beagle 하나로 유지된다. Mammal/Animal은 더 넓은 계약으로 보는 upcast이며 암시적으로도 가능하다. Beagle downcast는 실제 객체와 맞는다. Cast는 expression의 사용 type을 지정할 뿐 원래 변수 선언이나 객체 class를 바꾸지 않는다.

(a)는 Life 계약에 move가 없어 compile-time 호출 가능성에서 실패한다. (b)는 Animal expression에서 move가 보이고 실제 객체도 Animal이라 맞는다. (c)는 관련 type 간 cast 표현은 가능해도 실제 Life가 Animal이 아니므로 `ClassCastException`이다. 각각 독립 대안으로 판단하며 오류 줄 뒤가 정상 진행한다고 읽지 않는다. (d)는 `(Animal)null` 자체가 null인 채로 허용되지만 이어 instance method를 부르면 receiver가 없어 `NullPointerException`이다.

`x instanceof Animal`은 null에서 false이고 실제 객체의 호환성을 검사해 subtype 기능을 쓸 때 도울 수 있다. Cast로 접근 권한을 우회하지 못하며 상위 type cast도 실제 receiver의 instance override를 멈추지 않는다. 공통 계약이면 override 호출을, 정말 확장 기능이 필요하면 적절한 type 확인을 사용한다.

**확인 기준:** 동일 객체·expression type·compile-time/잘못된 cast/null 호출의 세 실패를 분리한다.

</details>

### 연습

#### 연습 P01 · 같은 객체의 서로 다른 상태 경로

새로 작성한 synthetic practice다. [EX:cp_2026_1_final_q02 p.2]의 field/static/instance 분리와 [EX:cp_2026_1_final_q09 p.6]의 overload→override 순서만 연결한다. binding, method signature, field hiding과 alias가 선수 조건이다. 다음 class들은 같은 package, 호출 줄들은 적절한 method 안에 있다고 하자.

~~~text
class Device {
    int state = 3;
    static String kind() { return "device"; }
    void step(int n) { state += n; }
    void step(float n) { state += 10; }
    String report() { return "" + state; }
}
class Sensor extends Device {
    int state = 20;
    static String kind() { return "sensor"; }
    @Override void step(int n) { state += 2 * n; }
    @Override String report() { return state + "/" + super.state; }
}
Sensor s = new Sensor();
Device d = s;
d.step(1);
d.step(1.0f);
~~~

`d.state`, `s.state`, `d.report()`, `((Device)s).report()`, `d.kind()`, `s.kind()`의 값을 근거와 함께 구하라. 어떤 step body가 어느 field를 바꿨는지 먼저 적는다.

<details><summary>해설 보기</summary>

s와 d는 Sensor 객체 하나를 가리킨다. `d.step(1)`은 Device에서 int signature를 선택한 뒤 Sensor override로 들어가 Sensor.state를 20+2×1=22로 만든다. `d.step(1.0f)`는 float signature를 고른다. Sensor가 이 signature를 override하지 않아 Device의 body를 사용하며 그 body의 state는 Device field이므로 3+10=13이다.

따라서 d.state=13, s.state=22다. 두 report 호출은 같은 Sensor override로 dispatch하여 `"22/13"`을 반환한다. Device cast는 receiver를 바꾸지 않는다. `static` kind는 expression type으로 골라 d.kind()=`"device"`, s.kind()=`"sensor"`다. 같은 객체라고 모든 field 접근이나 static body 선택이 같아지지 않는다.

**확인 기준:** 두 step의 signature/body/field, 여섯 결과, cast 후 dispatch 유지까지 각각 확인한다.

</details>

#### 연습 P02 · Subtype 기능이 필요한 경계

새로 작성한 lecture-based general practice다. 색인에는 이 null·확장 기능 분류와 직접 대응하는 문항 근거가 없다. Life에는 breed만 있고 Animal extends Life에는 move가 추가되어 있다. 각 대안은 독립적이다.

x가 (a) new Animal(), (b) new Life(), (c) null을 담은 Life reference일 때 `x.move()`와 `((Animal)x).move()`를 각각 분류하라. `if (x instanceof Animal) { ((Animal)x).move(); }`는 어떤 경우 body에 들어가는가? 이 guard를 모든 공통 method 호출에 넣어야 하는가?

<details><summary>해설 보기</summary>

세 경우 모두 x의 declared type은 Life이므로 `x.move()`는 호출 가능성 검사에서 허용되지 않는다. 실제 값이 Animal인 a도 예외가 아니다. Cast 뒤 호출은 a에서는 실제 객체와 맞아 move에 접근하고, b에서는 실제 Life가 Animal이 아니므로 `ClassCastException`, c에서는 cast 자체가 null을 유지한 뒤 호출이 `NullPointerException`이다.

`instanceof` guard는 a에서만 true다. b와 c는 false여서 cast/호출 body에 들어가지 않는다. 이처럼 정말 Animal의 확장 기능이 필요할 때 호환성 검사는 유용하다. 이미 공통 계약에 선언된 동작은 그 계약으로 호출하고 실제 receiver의 override를 사용하면 되므로 모든 공통 method를 type 분기로 바꿀 이유는 없다.

**확인 기준:** 직접 호출의 공통 실패와 cast 뒤 세 결과, guard의 세 판정, 설계 사용 범위를 확인한다.

</details>

## 출처

### 강의 노트와 전사

- [[courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2|날짜 미확인 · Object 계약·polymorphism·generic 도입]]
- [[courses/computer_programming/lectures/2026-09-01-lecture-01|2026-09-01 · literal type·변환의 기초]]
- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · operator·short-circuit]]
- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · 객체·constructor·static·reference 선수 내용]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · 객체·초기화·reference 복습]]

날짜가 있는 노트는 해당 선수 내용을 다시 찾기 위한 링크다. Inheritance·dispatch의 상세를 그 날짜에 모두 다뤘다는 뜻은 아니다.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 전사]] — 54:47, 55:45, 56:45, 57:38, 59:24, 01:00:18, 01:01:17, 01:03:10, 01:06:05, 01:07:58, 01:09:54, 01:11:50, 01:15:28, 01:18:07, 01:19:07, 01:20:06, 01:22:07, 01:23:53, 01:24:50.
- [[courses/computer_programming/transcripts/2026-09-08|T007 · 2026-09-08 전사 / transcript]] — 24:17.

### 자료와 원본 쪽

쪽수는 물리 PDF 기준이다. 각 쪽 링크에서 원본 페이지를 함께 볼 수 있다.

- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [25쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-025), [26쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-026), [27쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-027), [28쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-028), [29쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-029), [30쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-030), [31쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-031), [32쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-032), [34쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-034), [35쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-035), [36쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-036), [37쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-037), [39쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-039), [40쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-040), [41쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-041), [42쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-042), [43쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-043), [44쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-044), [45쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-045), [46쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-046), [47쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-047), [48쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-048), [49쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-049), [50쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-050).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [1쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [6쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-006), [19쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [40쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-040), [41쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-041), [42쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042), [69쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-069).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [4쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-004), [5쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-005), [6쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-006), [7쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-007).

### 범위와 불확실성

NT001은 날짜 미확인 전사다. 95개 발화에 남은 124개 문자 그대로의 불확실성 표시와 76개 추가 한계를 유지하며, 불명확한 말·부정·누락을 자료 문장으로 복원하지 않는다. 인쇄 예제는 자료 근거이며 모두 새로 말한 예제라는 뜻이 아니다. 아래 시간은 전사에서 찾을 위치이며 별도 시간 앵커를 뜻하지 않는다.

NM005는 물리 PDF 36쪽이다. 등록명은 Lab 6이지만 표지는 Lab 1이고, TODO와 19쪽의 제공되지 않은 ZIP이 남아 있다. 여기서는 개념 자료로만 사용하며 완성된 채점 대상 구현이나 해당 실습의 출석·제출 규칙을 가져오지 않는다.

NM004의 잘못된 닫는 quotation mark, Laidoff 대안 class 중복, 31쪽 구두점과 NM005의 lowercase string은 유효한 완성 코드로 받아들이지 않는다. Primitive int/double 반환형 예를 모든 reference 반환형의 동일성 규칙으로 넓히지 않는다. 960/250/180의 통화 단위, Executive/Manager 사이의 미제시 관계, getClass가 superclass 이름을 돌려준다는 발화는 확정하지 않는다. RealPoint의 네 출력은 자료 보충이며 인쇄 float를 불확실한 double 발화로 바꾸지 않는다. 도식은 method data와 code의 연결을 설명할 뿐 실제 JVM 전체 배치·binary 삭제·매번 선형 검색·보편 비용을 보장하지 않는다. Polynomial body와 문자열 constructor 의미도 제공되지 않았다.

Short-circuit 예는 M002 물리 PDF 69쪽에 있으며, 2026-09-08 T007 24:17의 근거는 날짜 미확인 NT001과 별도다. NM004 44쪽의 float f=0.5 % 0.3은 double literal 때문에 그대로 대입할 수 없다. 불명확한 operator 소리·오류명·downcast 빈도는 복원하거나 통계로 일반화하지 않는다.

### 비공식 복기와의 제한된 연결

복기 자료는 비공식이며 검증된 공식 정답은 제공되지 않았다. 파일명에만 연결된 2025년 봄 중간 김상한, 2026년 봄 기말 유영재는 현재 유재민(Jaemin Yoo) 교수와 다르다. 연결은 아래 개념·풀이 구조에 한정하며 현재 수업의 출제 형식·범위·빈도·확률을 뜻하지 않는다. 신규 문항은 일반 또는 합성 연습이다.

- [EX:cp_2026_1_final_q02 p.2] — Field/static의 declared-type 선택과 instance override를 분리하는 구조를 P01에 연결한다. binding·method signature·field hiding이 선수 내용이다. [[exam_questions/cp_2026_1_final_q02|기존 문항 미리보기]]
- [EX:cp_2026_1_final_q09 p.6] — 먼저 overload signature, 다음 실제 receiver의 override라는 두 단계를 P01에 연결한다. Overload·override가 선수 내용이며 RealPoint의 자료 계산을 원문 수치로 대체하지 않는다. [[exam_questions/cp_2026_1_final_q09|기존 문항 미리보기]]

HR 분기 유지보수, RealPoint의 네 출력, Polynomial 도식, 정확한 operator 예와 Life cast의 전체 분류에는 직접 대응하는 색인 문항이 없다. P02는 일반 연습이다.
