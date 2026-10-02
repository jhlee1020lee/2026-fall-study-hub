---
title: "Inheritance·형 변환·재정의와 생성 순서"
description: "상속 설계와 overload·override·hiding·cast·초기화·접근 규칙을 복습한다."
course: "computer_programming"
unit_id: "inheritance"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["6 inheritance 1.pdf"]
private_source_assets: []
source_lectures: []
---

재사용 관계가 부모의 동작과 자식의 의미를 함께 보존하는지 확인한다. 호출·field·cast·생성 순서를 각각의 규칙으로 추적해 보자.

## Inheritance와 composition: 재사용할 관계 선택하기

비슷한 class(클래스)를 매번 복사하면 공통 기능을 고칠 때 여러 복사본을 함께 고쳐야 한다. Inheritance(상속)는 기존 class를 바탕으로 더 구체적인 class를 정의하여 공통 기능을 재사용하고 차이를 추가하는 방법이다. Parent, superclass, base class는 부모 쪽을, child, subclass, derived class는 자식 쪽을 가리킨다. 여기의 상세 규칙은 **RM001 Inheritance 1에 근거한 자료 기반 학습**이다. 새 녹음이나 특정 날짜의 실제 진도를 뜻하지 않으며, [Encapsulation](encapsulation.md)과 [Packages](packages.md)의 접근 경계를 전제로 한다.

RM001 pp.4–5는 `Lecture`의 `hasTA = true`, `hasExams = true`, `hasAssignments = false`를 여러 class에 반복한 코드에서 출발한다. `CSLecture extends Lecture`는 `isHard = true`를 추가하고, `CPLecture extends CSLecture`는 `isExciting = true`를 추가한다. 공통 정의를 모으는 효과가 보인다. 다만 자식의 `hasAssignments = true` 재선언은 부모 field의 값을 일괄 변경하는 것이 아니라 같은 이름의 별도 field를 선언하는 hiding이다. 이 가상 class의 이름과 boolean 값은 이번 학기의 과제·시험·난이도에 관한 사실이 아니다.

[RM001 PDF pp.7–9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-009)의 그림은 확장의 세 선택을 비교한다. `A` 자체를 `A′`로 대체하면 기존에 `A`를 쓰던 연결이 깨질 수 있다. 복사해 별도 `A′`를 만들면 비슷하지만 다른 두 구현을 관리해야 한다. 마지막 그림은 기존 `A`와 사용자 연결을 남기고 `A′`에서 `A`로 향하는 점선 상속 관계를 더한다. 이것이 점진적 확장의 동기다. 유지보수·일관성·개발 효율·신뢰성은 재사용으로 추구하는 이점이며 상속 선언만으로 자동 보장되는 성과는 아니다.

### “Is-a”와 “has-a”를 동작까지 확인하기

`CarOwner`는 `Person`의 한 종류이므로 is-a 관계를 표현할 수 있다. 자동차를 소유한다는 has-a 관계는 `Car`를 field로 보관하는 composition(합성)으로 표현한다. `CarOwner extends Car`가 필요한 것은 아니다. [RM001 PDF pp.17–18]

수학적 포함 관계만으로도 부족하다. RM001 p.19의 `Circle extends Ellipse`는 두 축을 같은 radius로 초기화하지만 `Ellipse`의 `stretchX()`와 `stretchY()`를 물려받는다. **설명용 계산**으로 축이 `(2, 2)`인 원에서 X축만 2배 늘리면 `(4, 2)`가 되어 더 이상 원의 조건을 만족하지 않는다. 부모의 연산을 허용하면서 자식의 의미를 유지할 수 있는지를 확인해야 한다. 공통 field가 많다는 이유만으로 상속을 선택하면 이 문제가 숨는다.

## `extends`와 하나의 직접 superclass

`class Child extends Parent`는 부모의 접근 가능한 members를 이어받는 관계를 선언한다. RM001 p.15의 `Parent`는 `int var = 123;`과 `Parent`를 출력하는 `func()`를 갖고, `Child`는 빈 body로 이를 확장한다. 같은 package의 이 예에서는 `parent.func()`와 `child.func()`가 모두 `Parent`를 출력하며 두 객체의 `var` 조회는 각각 `123`이다. 자식에게 새 코드를 쓰지 않았다고 사용할 행동이 전혀 없는 것은 아니다. 반대로 private member를 자식이 직접 사용할 수 있다는 뜻도 아니다.

| 계층 형태 | 의미 | 직접 부모 수 |
|---|---|---|
| Single: `A → B` | B가 A를 확장 | B는 하나 |
| Multilevel: `A → B → C` | B가 자식이면서 C의 부모 | 각 class는 하나 |
| Hierarchical: A 아래 B·C·D | 한 부모에 여러 자식 | 각 자식은 하나 |

여러 단계나 여러 자식이 있는 것과 한 class가 여러 직접 부모를 갖는 것은 다르다. 일반 class는 명시적 superclass가 없으면 `Object`로 연결되며, `Object` 자체는 superclass가 없는 root다. `toString()`은 문자열 표현을, `getClass()`는 실제 class를 나타내는 `Class` 객체를 제공한다. `equals()`와 `hashCode()`는 다음 단원에서 구체화한다. RM001 p.21의 목록 전체가 재정의 가능한 것은 아니다. 예를 들어 `getClass()`는 override할 수 없다. `wait`, `notify`, `finalize`, `clone` 등의 상세 사용은 여기의 학습 범위가 아니다.

RM001 pp.26–28의 `class C extends A, B`는 Java에서 허용되지 않는 반례다. 그 예에서 `D.f()`는 `var`를 `1`, `A.f()`는 `2`, `B.f()`는 `3`으로 바꾼다. 두 부모의 `f()` 중 무엇을 쓰는지 충돌하는 상황을 설명하지만 `C` 선언 자체가 불법이므로 결과를 `2` 또는 `3`인 실제 실행 출력으로 고를 수 없다. 여러 interface를 구현하는 경우는 여러 class를 직접 상속하는 경우와 구별한다. 또한 자료의 분류 그림은 `Object` 아래 `Character`, 그 아래 `Digit`와 `Letter`, 다시 `Letter` 아래 `Vowel`과 `Consonant`를 둔다. 이 계층은 개념 비유이지 Java 표준 library의 실제 계층 목록이 아니다.

## Overloading과 overriding: 같은 이름에서 다른 질문하기

Overloading(오버로딩)은 같은 이름에 다른 parameter 목록을 제공하는 것이고, overriding(재정의)은 상속한 instance method를 자식의 구현으로 바꾸는 것이다. RM001 p.16의 `Point.move(int dx, int dy)`와 `Point3d.move(int dx, int dy, int dz)`는 인자 수가 다르다. 세 좌표를 옮기는 method를 추가했을 뿐 두 인자 method를 같은 signature로 대체하지 않는다.

### `SlowPoint`의 제한된 이동

RM001 p.31의 `SlowPoint`는 부모와 같은 두 인자 `move(int,int)`를 정의한다. 자식은 이동량을 제한하고, 좌표를 실제로 더하는 일은 `super.move()`에 맡긴다. 다음은 해당 일반 예제의 자식 부분이다.

```java
class SlowPoint extends Point {
    int xLimit = 10, yLimit = 10;
    void move(int dx, int dy) {
        super.move(limit(dx, xLimit), limit(dy, yLimit));
    }
    static int limit(int d, int limit) {
        return d > limit ? limit : d < -limit ? -limit : d;
    }
}
```

`limit(20,10)`은 `10`, `limit(-12,10)`은 `-10`이다. 따라서 원점에서 `move(20,-12)`를 요청하는 **설명용 trace**는 `(10,-10)`으로 끝난다. 경계값 `10`, `-10`은 이미 허용 범위라 그대로다. 이 계산은 원본 식으로부터 도출한 것이며 별도 강의 발화나 실행 기록은 아니다.

`@Override`는 “상위 method를 재정의하려 한다”는 의도를 compiler에 알려 잘못된 signature를 발견하도록 돕는다. Annotation이 객체를 만들거나 method를 호출하는 것은 아니다. RM001 p.33의 서로 다른 `Parent`와 `Child` 객체에 `printName()`을 호출하면 각각 `Parent`, `Child`가 출력된다. 이름이 같다는 조건만으로 모든 반환 type·접근 규칙까지 충족한 것은 아니므로 선언 전체를 읽어야 한다.

호출을 읽을 때는 **먼저 어떤 signature가 선택되는가**, **그 signature가 override되어 어느 body가 실행되는가**를 분리한다. 2026-1 기말 복기 9번은 수치 인자의 `int`/`double` 차이와 이 두 판단을 결합한다. 먼저 reference의 선언 type에서 사용할 수 있는 overload와 인자 type을 확인하고, 선택된 instance method의 override를 실제 객체에서 찾는다. Field 조회는 이 두 번째 단계로 보내지 않는다. 이는 복기 문제의 요구하는 추론을 옮긴 것이며 원문 전체나 답안을 재현한 것은 아니다. [EX:cp_2026_1_final_q09 p.6]

## Field·static hiding과 dynamic dispatch

Hiding(숨김)과 dynamic dispatch(동적 호출 선택)를 하나의 규칙으로 외우면 cast 예제를 잘못 읽게 된다. RM001 pp.34–39는 둘을 구분한다.

| 접근 대상 | 선택 기준 | 실제 객체가 자식이면 항상 자식 쪽인가? |
|---|---|---|
| Field | 접근 식의 compile-time type | 아니다. |
| `static` method | type에 따라 이름 해석 | 아니다. |
| Override된 instance method | 선택된 signature에 대해 실제 receiver 객체 | 자식 override가 실행된다. |

`Super s = new Sub();`에서 `s.greeting()`이 static이면 `Super` 쪽의 `Goodnight`가 선택된다. 같은 `s`로 부르는 instance method `name()`은 `Sub`의 override를 사용한다. 한 reference에서 호출한다고 두 선택 규칙이 같아지지 않는다. Static method를 class 이름으로 읽으면 이 소속 차이를 드러내기 쉽다. [RM001 PDF p.35]

Field의 경우 `Point.x`가 `int 2`, `Test.x`가 `double 4.7`이면 `Test` 내부의 `x`, `super.x`, `((Point)this).x`는 각각 `4.7`, `2`, `2`다. Cast는 객체를 바꾸거나 child field를 지우지 않고 접근 식의 type을 바꾼다. 반면 `T1 → T2 → T3`에서 각 instance `s()`가 String `"1"`, `"2"`, `"3"`을 반환하면 `T3` 객체 안의 `s()`, `((T2)this).s()`, `((T1)this).s()`는 모두 `"3"`을 반환한다. **부모 type으로 cast해도 override가 취소되지 않는다.**

RM001 p.36의 “Hiding Variables” 예에는 `Child`의 `extends Parent`가 빠져 있다. 그 페이지 그대로는 독립된 두 class의 `123`과 `456` 조회이며 상속 hiding의 실행 증거는 아니다. 올바른 상속 field 관계는 p.38의 `Test extends Point` 예에서 확인한다.

## Upcast와 downcast: 객체는 유지하고 보는 type 바꾸기

Upcast(상향 형 변환)는 자식 객체를 부모 type의 reference로 다루는 것이다. `Parent p = new Child();`는 이를 자동으로 수행하고, `(Parent)`를 명시해도 새로운 객체를 만들지 않는다. 보이는 members는 선언 type에 제한되지만 override된 instance 동작은 실제 `Child`에 따른다. [RM001 PDF pp.40–42]

Downcast(하향 형 변환)는 더 구체적인 type으로 객체를 사용하려는 명시적 cast다. 실제 객체가 목표 type 또는 그 subclass여야 한다. RM001 p.44의 `Parent` reference는 실제 `Sister`를 가리키므로 `print()`는 `Sister`를 출력하고 `Sister` cast는 맞지만 `Brother` cast는 객체의 실제 type과 맞지 않아 `ClassCastException`의 대상이다. 다만 원본은 두 local variable에 모두 `sister`라는 이름을 쓰므로 한 block 그대로는 중복 선언 오류도 있다. 이 별도 오류와 런타임 cast 검사를 혼동하지 않는다.

`instanceof`는 객체가 해당 type으로 다루어질 수 있는지 확인한다. [RM001 PDF pp.22–23]

| 실제 객체 | `instanceof Parent` | `instanceof Child` |
|---|---|---|
| `new Parent()` | `true` | `false` |
| `new Child()` | `true` | `true` |
| `null` | `false` | `false` |

같은 class인 경우도 참이므로 “엄격한 자손인가”만 검사하는 것은 아니다. `MyClass`의 객체는 `MyClass`와 `Object` 검사에 모두 참이며, 자료의 `String`과 `Integer` reference도 `Object`다. `Integer integer = 3`은 wrapper reference를 만드는 예이지 primitive 값 `3` 자체에 `instanceof`를 적용하는 예가 아니다. 또 runtime 검사가 있다는 말이 compiler의 type 검사가 전혀 없다는 뜻은 아니다. Compiler도 cast가 type상 가능한지 검사한다.

## `super`: 부모 구현과 초기화에 연결하기

`this`는 현재 객체를 가리킨다. `super`는 그 객체의 부모 쪽 선언이나 구현을 선택하는 문맥이다. 별도의 부모 객체를 새로 생성하거나 private 접근 제한을 해제하는 keyword가 아니다.

RM001 p.45에서 부모 `var = 123`, 자식 `var = 456`이면 `child.var`는 `456`, 자식의 `getParentVar()`가 반환하는 `super.var`는 `123`이다. p.46의 `Child.printName()`은 `Child`만 출력하고, 별도 `printParentName()`이 `super.printName()`을 호출한다. 따라서 두 method를 차례로 호출했을 때 `Child`, `Parent`가 나온다. Override body에 원래부터 부모 호출이 있는 것처럼 둘을 합치면 안 된다.

앞의 `T3` 예에서도 `s()`는 `"3"`, `super.s()`는 바로 부모 `T2`의 `"2"`, `((T2)this).s()`는 다시 `"3"`이다. 일반 호출의 dispatch와 명시적인 부모 구현 호출은 다르다. `super.super.Print()`는 지원되지 않는다. RM001 p.53처럼 `Child.Print()`가 `super.Print()`를, `Parent.Print()`가 다시 `super.Print()`를 호출하면 `Grand` 다음 `Child`가 출력된다. 이는 부모가 연결한 경로이며, 조부모에게서 이어받은 모든 member를 사용할 수 없다는 뜻은 아니다. 원문의 `Print` 대소문자도 유지해야 한다.

`this`와 `super`를 비교하는 2025-1 중간 복기 5번에 적용할 때도 keyword 정의만 나열하기보다 **현재 객체의 식**, **부모 field/body 선택**, **constructor 연결**을 나누어 설명하면 된다. [EX:cp_2025_1_midterm_q05 p.3]

### Constructor chain의 순서와 `color` 충돌

자식 객체를 생성하면 부모 부분의 초기화를 거친다. RM001 p.48의 예는 부모 constructor의 `Parent` 출력 뒤 자식의 `Child` 출력을 보여 준다. p.49의 `Geometry`는 인자를 받는 constructor와 `dimension = 3`을 설정하는 no-argument constructor를 모두 제공한다. 그 예의 빈 `Point()`는 implicit `super()`로 접근 가능한 무인자 부모 constructor를 호출한다. 부모에 그런 constructor가 항상 존재하는 것은 아니다. `this(...)`는 같은 class의 다른 constructor로, `super(...)`는 부모 초기화로 연결한다.

RM001 p.50의 코드는 부모 `Point()`가 `x = 1; y = 1;`을 설정하고, 자식 `ColoredPoint`에 `int color = 0;`을 둔다. 호출은 `Object` constructor까지 올라간 뒤 돌아오며 부모 초기화 뒤 자식 field initializer가 적용된다. 따라서 **p.50 코드의 최종 상태는 `(x,y,color) = (1,1,0)`**이다. [p.51 순서 설명](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051)은 `color = 0xFF00FF`라고 다르게 인쇄한다. 순서 설명은 유지하되 p.50의 `0`이 자동으로 `0xFF00FF`가 된다고 해석하지 않는다.

2026-1 기말 복기 1-(c)의 constructor 판단도 이 자료 범위에서 읽는다. 명시적 `this(...)`/`super(...)`의 유무와 접근 가능한 부모 무인자 constructor의 존재를 따로 확인해야 한다. 이 비교는 최신 Java의 모든 constructor 문법에 관한 주장이 아니다. [EX:cp_2026_1_final_q01c p.1]

## 상속해도 유지되는 접근 경계

`Shape`의 protected `height`, `width`를 `Rectangle.getArea()`가 곱하는 예는 공유 상태를 부모에 두되 모든 외부 코드에 공개하지 않는 방법이다. Override는 상위 method의 접근 범위를 줄일 수 없다. `public`은 계속 `public`, `protected`는 `protected` 또는 `public`이어야 한다. Package 접근 method도 실제 상속되는 문맥에서 같거나 더 넓은 접근으로 재정의한다. [RM001 PDF pp.55–56]

`Point.move()`가 좌표를 더하고 `useCount`, `totalUseCount`를 증가시키며, `PointBack.moveBack()`이 좌표를 빼고 두 counter를 증가시키는 예에서는 소속을 따져야 한다. `useCount`는 각 객체의 호출 수이고 `static protected totalUseCount`는 여러 객체가 공유하는 누적 수다. 한 객체의 count와 전체 count를 같은 값으로 가정하면 안 된다. [RM001 PDF p.57]

다른 package의 예에서 `ComplexAlgebra.C`의 `real`, `add`, `multiply`는 protected이고 `imag`, `angle`, `radius`는 package 접근이다. `RealAlgebra.R extends C`는 `super(value, 0)`으로 초기화하고 상속 문맥에서 `real`을 사용해 실수부를 표현하지만 package 접근 members를 직접 쓸 수 없다. `multiply`의 `...`는 구현 생략이다. Cross-package protected는 subclass의 상속 문맥에 한정되며 임의의 부모 receiver를 통해 무조건 접근하는 권한이 아니다. [RM001 PDF pp.59–60]

이것은 두 package와 subclass를 그린 2025-1 중간 복기 4번의 접근 분석에도 필요하다. 선언 위치, 접근하는 코드의 package, subclass 관계, 접근에 쓰는 receiver type을 차례로 확인한다. “자식이면 protected는 어디서나 가능”이라는 표 한 칸으로 끝내지 않는다. 해당 문항은 역사적 복기본이며 공식 원본·정답 확인을 뜻하지 않는다. [EX:cp_2025_1_midterm_q04 p.2]

### Private 상태는 부모 method를 통해 바뀔 수 있다

자식이 부모의 private field를 직접 이름으로 사용할 수 없다고 부모가 관리하는 상태가 사라지는 것은 아니다. RM001 p.61의 `Point.move()`는 자기 private static `totalMoves`를 증가시킬 수 있다. `Point3d`가 `super.move(dx,dy)`를 호출하면 그 부모 코드가 합법적으로 counter를 바꾸지만, 자식 코드의 직접 `totalMoves++`는 접근 오류다. p.63의 private `x`, `y`도 부모 `move()`가 갱신하고 자식은 자기 private `z`를 갱신한다.

`Parent`와 `Child`가 각각 private `makeMoney()`를 정의해 `100`과 `0`을 반환하는 p.64 예는 두 독립된 private method다. 같은 이름이어도 override 관계가 아니다. 부모의 접근 가능한 동작을 재사용하는 일과 private 내부에 직접 접근하는 일은 구별된다.

## `final`: 확장·재정의·재대입의 서로 다른 제한

`final`은 붙는 대상에 따라 뜻이 달라진다. [RM001 PDF pp.65–68]

| 대상 | 금지하는 변화 | 여전히 가능한 것 |
|---|---|---|
| `final class ColoredPoint` | 이 class를 다시 `extends`하기 | 그 class의 객체를 사용하기 |
| `final` instance method | 자식에서 override하기 | 상속받아 호출하기 |
| `static final` method | 같은 signature로 숨기기 | 허용된 방식으로 호출하기 |
| 초기화된 `final` variable | 다른 값을 재대입하기 | reference라면 별도로 mutable한 객체 상태를 다루기 |

자료의 `static final Point origin = new Point(0, 0);`은 공유 reference를 고정한다. `p.origin = new Point(-1,-2)`는 새 reference를 대입하므로 오류다. 그러나 reference가 고정되었다고 가리키는 `Point`의 변경 가능한 `x`, `y`, `useCount`까지 모두 immutable(불변)이 되는 것은 아니다. 객체 동일성의 고정, 객체 상태의 변경, class 확장 금지를 구별하면 `final`을 만능 보호 장치로 오해하지 않을 수 있다.

## 핵심 정리

- Is-a는 부모 연산을 지원하면서 자식의 의미를 유지해야 한다. Has-a는 field로 객체를 포함하는 composition에 대응한다.
- Overload signature 선택과 instance override 선택은 별도 단계다. Field와 static method는 식의 type으로 읽는다.
- Cast는 객체를 바꾸지 않는다. `super`의 부모 body 선택은 부모 type으로 cast한 일반 호출과 다르다.
- 부모 초기화·자식 초기화를 차례로 확인하며, 접근 가능한 부모 constructor가 있다는 조건을 빠뜨리지 않는다.
- 상속에도 private·package·protected 경계가 남고 override는 접근을 좁힐 수 없다. `final` reference는 객체 전체의 불변성을 뜻하지 않는다.

## 확인·연습문제

### 관계와 호출 선택

#### 확인 Q01 · 재사용과 불변 조건

(a) A 수정·복사·상속의 장단점과 parent/child 용어를 비교하라. (b) `CarOwner`의 is-a/has-a를 나누어라. (c) `Lecture`의 field 재선언과 `Circle`의 한 축 늘리기가 왜 주의할 사례인지 설명하라.

<details><summary>해설 보기</summary>

(a) A를 대체하면 기존 사용 관계가 깨질 수 있고 복사하면 유사한 구현을 여럿 관리한다. A를 유지하고 subclass로 확장하면 공통 기능을 모으면서 점진적으로 추가할 수 있으나 안전성이 자동 보장되지는 않는다. Parent/superclass/base와 child/subclass/derived는 관계의 양쪽이다. 

(b) `CarOwner`는 Person is-a, Car has-a이므로 Person 상속과 Car field를 구별한다. 

(c) Lecture의 공통 fields를 CSLecture/CPLecture가 재사용하되 `hasAssignments=true` 재선언은 별도 field hiding이다. 가상 값은 학기 정책이 아니다. Circle의 축 `(2,2)`에 X만 2배를 적용하면 `(4,2)`가 되어 원의 조건을 잃는다.

**확인 기준:** 세 확장 전략, 두 관계, field hiding, 축 계산을 모두 확인한다.

</details>

#### 확인 Q02 · 직접 superclass와 계층

빈 `Child extends Parent`가 같은 package의 `var=123`, `func()`를 사용할 수 있는가? Single·multilevel·hierarchical, `Object`, 잘못된 `extends A,B`를 비교하라.

<details><summary>해설 보기</summary>

접근 가능한 부모 members를 이어받으므로 두 객체의 var는 각 123, func는 모두 Parent를 출력한다. Single은 A→B, multilevel은 A→B→C, hierarchical은 A 아래 여러 자식으로 각 class의 직접 부모는 하나다. 일반 class는 Object 계층에 연결되며 Object 자체는 부모가 없다. `toString()`은 표현, `getClass()`는 실제 class의 Class 객체를 주지만 getClass는 override할 수 없다. 다이아몬드의 D/A/B가 f에서 1/2/3을 쓰더라도 C의 `extends A,B` 자체가 불법이라 실제 출력 2 또는 3을 고를 수 없다. 여러 interface 구현은 별개다. Character 분류 그림은 표준 library 계층이 아니다.

**확인 기준:** 상속된 접근·직접 부모 수·불법 선언·Object 한정을 확인한다.

</details>

#### 확인 Q03 · Overload와 제한된 이동

`Point3d.move(int,int,int)`와 `SlowPoint.move(int,int)`를 구별하라. 원점에서 SlowPoint에 `(20,-12)`를 요청하고 경계 ±10도 검사하라. `@Override`의 역할은?

<details><summary>해설 보기</summary>

세 인자 method는 부모 두 인자 signature와 다른 overload다. SlowPoint의 같은 두 인자 instance method는 override이며 각 이동량을 [-10,10]으로 제한해 `super.move`에 전달한다. 20→10, -12→-10이므로 좌표는 `(10,-10)`이다. 10과 -10은 그대로다. `@Override`는 의도를 compiler가 검사해 잘못된 signature를 찾도록 돕고 호출이나 생성 자체는 하지 않는다. 자료의 별도 Parent/Child printName은 Parent 다음 Child를 출력한다. 같은 이름만으로 반환 type·접근 규칙까지 충족하지 않는다.

**확인 기준:** Signature 구별, 양쪽 제한, 부모 갱신, annotation 역할을 확인한다.

</details>

#### 확인 Q04 · Field·static·instance 선택

`Super s=new Sub()`의 static `greeting()`과 override된 `name()`은 어느 쪽인가? Test의 `x=4.7`, Point의 `x=2`와 T3의 parent casts도 추적하라.

<details><summary>해설 보기</summary>

`static`은 선언 type Super의 Goodnight이고 instance name은 실제 Sub의 override다. Test 내부의 `x`, `super.x`, `((Point)this).x`는 `4.7,2,2`다. Field는 식의 type으로 고르며 cast가 객체나 자식 field를 제거하지 않는다. 반면 T1/T2/T3의 s가 각 문자열 1/2/3을 반환할 때 T3에서 일반 호출과 T2/T1 cast 뒤 호출은 모두 `"3"`이다. Instance override는 cast로 취소되지 않는다. RM001 p.36은 Child에 extends가 빠져 독립 class 예이므로 그 페이지를 상속 실행 증거로 쓰지 않는다.

**확인 기준:** 세 선택 규칙과 field/instance cast 차이를 이유로 설명한다.

</details>

### Cast와 초기화

#### 확인 Q05 · Cast와 실제 객체

`Parent p=new Sister()`에서 Parent/Sister 검사와 Brother cast를 판단하라. Parent/Child의 네 `instanceof` 조합, null, wrapper와 compile/runtime 검사도 설명하라.

<details><summary>해설 보기</summary>

Parent·Sister 검사는 참이고 Brother cast는 실제 Sister를 Brother로 바꾸지 못해 실행 시 ClassCastException 대상이다. 원본 p.44에는 중복 local 이름 sister 오류도 있어 그대로 실행된 결과로 말하지 않는다. new Parent는 Parent 참/Child 거짓, new Child는 양쪽 참이며 같은 type도 참이다. Null은 모두 거짓이다. Upcast는 자동 가능하고 객체를 새로 만들지 않으며 보이는 members만 제한한다. Downcast는 목표 type 또는 그 subclass인 실제 객체가 필요하다. Compiler도 type상 가능성을 확인한다. MyClass/String/Integer 객체는 Object이며 `Integer integer=3`은 wrapper reference이지 primitive에 instanceof를 적용한 것이 아니다.

**확인 기준:** 실제 type·null·동일 type·compile 오류와 runtime 실패를 구별한다.

</details>

#### 확인 Q06 · super와 부모 body

부모 var 123/자식 var 456, 별도 `printName`/`printParentName`, T3의 `s()`/`super.s()`/parent cast를 비교하라. `super.super.Print()` 대신 자료는 어떻게 연결하는가?

<details><summary>해설 보기</summary>

Child의 var는 456, `getParentVar()`의 super.var는 123이다. Child.printName은 Child만, 별도 printParentName의 super 호출은 Parent를 출력한다. T3의 세 호출은 `"3","2","3"`으로 일반 dispatch와 부모 body 선택이 다르다. `this`는 현재 객체이고 super는 그 객체의 부모 쪽 문맥이지 새 부모 객체나 private 접근 열쇠가 아니다. `super.super.Print()`는 지원되지 않는다. Child.Print→Parent.Print→Grandparent.Print의 명시 경로로 Grand 다음 Child가 나오며, 조부모에게서 상속한 모든 member가 금지된다는 뜻은 아니다.

**확인 기준:** Field/body/현재 객체와 직접 부모 경로를 구별한다.

</details>

#### 확인 Q07 · 초기화 순서와 충돌

Geometry의 빈 Point constructor가 가능한 조건과 `this(...)`/`super(...)` 차이는? Parent/Child 출력 순서 및 p.50의 ColoredPoint 최종 상태를 p.51과 비교하라.

<details><summary>해설 보기</summary>

Geometry에는 dimension을 3으로 설정하는 접근 가능한 무인자 constructor가 있어서 빈 Point()의 implicit super()가 가능하다. 모든 부모에 자동으로 그런 constructor가 있는 것은 아니다. this(...)는 같은 class의 다른 constructor, super(...)는 부모 초기화로 연결한다. 자료의 출력은 Parent 뒤 Child다. p.50에서는 Object까지 호출 후 돌아와 부모가 x=y=1, 자식 initializer가 color=0을 설정하므로 `(1,1,0)`이다. p.51의 0xFF00FF는 다른 값의 원문 충돌로 남기며 초기화 순서가 0을 변환했다고 설명하지 않는다.

**확인 기준:** 부모 constructor 존재·접근 조건, 순서, 최종 세 값과 충돌을 확인한다.

</details>

### 접근 경계

#### 확인 Q08 · 접근·counter·override

(a) Shape/Rectangle의 protected 상태와 override 접근 규칙을 설명하라. (b) 공통 count=0에서 PointBack 객체 A가 두 번, B가 한 번 이동했을 때 각 count는? (c) 다른 package의 C/R에서 접근 가능한 members와 초기화를 구별하라.

<details><summary>해설 보기</summary>

(a) Rectangle은 상속 문맥에서 height*width를 계산한다. `public` override는 public, protected는 protected/public이며 package method도 실제 상속될 때 같거나 넓게 한다. 

(b) 각 useCount는 A=2, B=1, static totalUseCount=3이다. Move는 좌표를 더하고 moveBack은 빼지만 모두 counters를 증가시킨다. 

(c) 다른 package R은 C의 protected real/add/multiply를 상속 문맥에서 사용하고 package 접근 imag/angle/radius는 직접 못 쓴다. R의 super(value,0)은 부모 부분 초기화다. `protected`는 임의 부모 receiver에 대한 무제한 허용이 아니며 multiply의 ...는 구현 생략이다.

**확인 기준:** 객체별/공유 count, 접근 비축소, protected/package 구별을 확인한다.

</details>

#### 확인 Q09 · 부모의 private 상태

Point3d는 부모의 private x/y나 totalMoves를 직접 못 쓰는데 왜 `super.move`로 바꿀 수 있는가? 같은 이름의 두 private `makeMoney()`는 override인가?

<details><summary>해설 보기</summary>

접근 가능한 부모 method body는 자기 private 상태를 사용할 권한이 있다. 자식은 그 동작을 호출해 x/y와 부모 counter 갱신을 맡기고 자신의 private z만 직접 갱신한다. 자식의 직접 totalMoves++는 접근 오류다. `private` 제한이 부모 상태의 존재나 정상 동작을 없애는 것은 아니다. Parent의 100과 Child의 0을 반환하는 private makeMoney는 서로 독립된 methods라 dynamic override가 아니다.

**확인 기준:** 합법적인 동작 호출과 금지된 직접 접근, private 비재정의를 확인한다.

</details>

#### 확인 Q10 · final의 대상

`final` class, instance method, static method, 초기화된 reference variable이 각각 금지하는 일을 적어라. `static final Point origin`에서 재대입과 객체 상태 변경은 같은가?

<details><summary>해설 보기</summary>

`final` class는 추가 extends를, final instance method는 override를, static final method는 같은 signature hiding을 막는다. Method를 물려받아 호출하는 것 자체는 금지하지 않는다. 초기화된 final variable은 재대입할 수 없어 origin을 새 Point로 바꾸는 것은 오류다. 그러나 기존 객체의 별도 mutable x/y/useCount 변경까지 reference의 final이 막지는 않는다. `static`은 공유 소속, final은 reference 재대입 제한으로 각각 읽는다.

**확인 기준:** 상속·override·hiding·재대입·상태 변경을 따로 판단한다.

</details>

### 적용 연습

#### 연습 P01 · Signature 다음에 body

새로 만든 기출 연결 연습이다. [EX:cp_2026_1_final_q09 p.6]의 overload→override 추론과 [EX:cp_2025_1_midterm_q05 p.3]의 부모 구현 구별을 옮겼다. 선수는 Q03–Q06이며 모두 현재 단원 범위다. 같은 package에서 `Base.f(int)`는 `"I"`, `Base.f(double)`은 `"D"`를 반환하고 `Sub`는 double 버전만 override해 `"S"`를 반환한다. Sub의 `parentValue()`는 `super.f(2.0)`을 반환한다. `Base b=new Sub()`에 대해 `b.f(2)`, `b.f(2.0)`, `((Base)b).f(2.0)`, `((Sub)b).parentValue()`를 순서와 이유로 답하라.

<details><summary>해설 보기</summary>

결과는 `I,S,S,D`다. `int` 인자는 int signature를 골라 상속된 Base body를 쓴다. `double` 인자는 double signature를 고른 뒤 실제 Sub override를 쓴다. Base cast는 객체를 바꾸지 않아 셋째도 S다. 실제 Sub이므로 마지막 downcast는 맞으며 parentValue의 명시적 super 호출만 Base의 double body로 가서 D다. 원문 프로그램의 수치만 바꾼 것이 아니라 override 대상과 부모 호출을 결합해 판단을 분리했다.

**확인 기준:** 네 값에 signature 선택과 body 선택 근거를 각각 쓴다.

</details>

#### 연습 P02 · 이동한 subclass의 조건

새로 만든 기출 연결 연습이다. [EX:cp_2025_1_midterm_q04 p.2]의 package·상속 접근 판단과 [EX:cp_2026_1_final_q01c p.1]의 constructor 전제를 함께 적용한다. 선수는 Q07–Q09, 자료의 Java 문맥이다. `public` `Base`에는 public `Base(int n)`만 있고 protected field `value`, package-access method `helper()`, private field `hidden`이 있다. 다른 package의 `Sub extends Base`에서 빈 constructor, `this.value` 접근, `helper()` 호출, `hidden` 직접 접근을 각각 판단하라. Constructor를 연결할 최소 방향도 설명하라.

<details><summary>해설 보기</summary>

빈 constructor가 요구하는 접근 가능한 Base()가 없어서 실패한다. Sub constructor가 적절한 int를 `super(n)`으로 넘기는 방향이 필요하며 새 Base()를 원래 존재한 것으로 가정할 수 없다. Sub 내부의 this.value는 상속 문맥의 protected 접근이라 가능하다. helper는 다른 package에 공개되지 않고 hidden도 직접 접근 불가다. 생성 오류를 고쳐도 접근 오류가 함께 사라지지는 않는다. 임의 Base receiver의 protected 접근까지 허용했다고 일반화하지 않는다.

**확인 기준:** Constructor와 세 member 판단을 분리하고 package 이동의 영향을 설명한다.

</details>

### 짧은 복습 계획

Q04·Q06에서 cast와 super의 결과를 나란히 적고 P01을 푼다. 다음 날 Q07·Q08 및 P02로 생성 가능성과 접근 가능성을 따로 검사한다.

## 출처

Inheritance 1의 자료 기반 복습이며 새 녹음이나 강의 날짜를 뜻하지 않는다. p.36의 extends 누락, p.44의 중복 local 이름, pp.50–51의 color 값 충돌을 유지한다. Protected의 receiver 제한과 제공된 constructor 문맥 안에서 읽으며, Object의 동시성·정리 API 상세는 범위 밖이다.

### 자료와 해당 페이지

- [6 inheritance 1 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-005), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-009), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-017), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-028), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-036), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-041), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-042), [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-044), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-045), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-053), [p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-055), [p.56](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-056), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-057), [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-061), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-062), [p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-063), [p.64](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-064), [p.65](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-065), [p.66](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-066), [p.67](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-067), [p.68](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-068)

### 기출 연결의 범위

역사적 복기본이며 공식 원본·정답 확인이나 이번 학기 출제 예고가 아니다. 제공된 공식 답안은 없고 새 연습의 해설은 위 추론으로 확인한다. 기말 복기의 순서·정확성 한계와 누락 문항은 그대로 남긴다.

- [EX:cp_2026_1_final_q09 p.6] · [[exam_questions/cp_2026_1_final_q09|공개된 문항 미리보기]]

- [EX:cp_2025_1_midterm_q05 p.3]

- [EX:cp_2026_1_final_q01c p.1]

- [EX:cp_2025_1_midterm_q04 p.2]
