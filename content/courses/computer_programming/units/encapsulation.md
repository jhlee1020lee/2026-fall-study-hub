---
title: "Encapsulation과 접근·상태 설계"
description: "상태 일관성, 접근 범위, 실패 처리와 getter·setter의 검증·추적을 복습한다."
course: "computer_programming"
unit_id: "encapsulation"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["4 oop.pdf", "5 encapsulation.pdf", "Lab03 v2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

상태를 읽을 권한과 바꿀 권한을 분리하고 method가 지킬 관계를 설명한다. Access modifier·validation·logging을 함께 검토하면 private만으로 해결되지 않는 오류를 찾을 수 있다.

## Encapsulation이 허용된 interaction을 만든다

[[courses/computer_programming/units/objects-references|Objects와 references]]로 상태를 묶었다면 다음 문제는 누가 어떤 경로로 그 상태를 바꿀 수 있는가다. Encapsulation(캡슐화)은 필요한 interaction(상호작용)을 제공하면서 내부 복잡성과 허용하지 않을 접근을 감추는 설계다. 자동차 사용자는 steering wheel과 accelerator로 조작할 수 있지만 engine 내부 전체를 이해할 필요는 없다.

Abstraction(추상화)은 사용에 필요한 interface(사용 접점)로 복잡성을 줄이는 목적이고, defensive programming(방어적 프로그래밍)은 예상하지 못한 상태 변경을 제한하는 목적이다. 여기서 interface는 우선 객체의 사용 약속을 뜻하며, 이후 배울 Java의 `interface` 선언 문법 전체를 전제하지 않는다. 사람에게 source의 존재를 비밀로 하는 것이 아니라 프로그램에서 허용할 경로를 설계하는 것이다. [Computer Programming M012, PDF pp.2–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf)

[[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:08:56 이후의 robot arm·head·chest 분업 비유도 이 목적에 맞는다. 각 부분을 맡은 사람은 다른 부분의 모든 구현을 읽기보다 합의한 기능에 의존해 연결할 수 있다. 이는 검증 없이 남의 코드를 믿으라는 뜻은 아니다. 어떤 입력을 받고 어떤 결과·상태를 보장하는지 합의해야 협력이 가능하다.

### Inheritance·polymorphism이 다루는 다른 관계

OOP의 소개에서는 abstraction을 Encapsulation, code reuse(코드 재사용)를 Inheritance(상속), 행동의 다양화를 Polymorphism(다형성)에 연결한다. M011 pp.58–61의 Organisms → Animals·Plants → Duck·Cat·Tree·Grass는 **class 사이의 계층**을 설명한다. Child class는 parent class의 특성을 이어받아 코드를 재사용하고 자기 특성을 추가할 수 있다. Cat class를 정의하고 그 class에서 여러 cat objects를 만드는 관계와 다르다.

Polymorphism의 소개 예는 공통 행동 `animalSound`를 개·고양이·오리가 서로 다른 소리로 구현한다는 것이다. Caller가 공통 약속으로 요청해도 구체적 class의 행동은 다를 수 있다. 같은 Car class의 두 instances가 speed=100과 speed=90을 갖는 단순 상태 차이를 이런 구현 차이와 혼동하지 않는다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:04:10 및 [M011 PDF pp.58–61](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf)

이 단계에서 필요한 것은 동기의 구별이다. 구체적인 inheritance 문법, override, method dispatch는 이후 학습이며 현재 예제의 전제로 몰래 끼워 넣지 않는다.

## 관련 상태를 하나의 판매 동작으로 바꾸기

FruitStore의 balance가 10000, stock이 30이고 과일 가격이 2000이라고 하자. 세 개를 팔면 두 값이 함께 바뀌어야 한다.

| 상태 | Balance | Stock |
| --- | ---: | ---: |
| 판매 전 | 10000 | 30 |
| 변화 | +2000×3 = +6000 | −3 |
| 판매 후 | 16000 | 27 |

외부 코드가 stock만 3 줄이고 balance를 그대로 두면 판매 규칙이 깨진다. M012 pp.4–6은 두 변경을 `sell(int num)`에 모아, caller가 내부 계산을 반복하지 않게 한다. 그러나 method만 만들고 fields를 계속 노출하면 외부의 직접 대입은 여전히 가능하다.

다음 AppleStore 예에서는 balance와 stock을 `private`로 두고, `getBalance()`·`getStock()`으로 읽고 `sell`로 변경한다. Getter(읽기 메서드)가 값을 알려 주어도 외부의 임의 대입까지 허용하지는 않는다. “읽을 수 있다”와 “원하는 값으로 쓸 수 있다”는 다른 권한이다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:16:32 및 M012 pp.11–12

원본의 이 methods에는 `public`이 붙어 있지 않아 package-private다. 예제의 같은 package 안에서 호출된다는 전제와 강의 중 편의상 public이라고 부른 표현을 구별한다. 이 예는 관련 상태를 일관되게 변경하는 책임을 설명하며 실제 상거래의 모든 검증·동시성 문제를 해결한 시스템은 아니다.

## Access modifier로 접근 경로 제한하기

Access modifier(접근 제어자)는 member에 허용된 접근 범위를 나타낸다. M012 pp.9–10의 현재 소개를 다음처럼 읽을 수 있다.

| Member의 표기 | 입문 범위에서의 의미 |
| --- | --- |
| `private` | 선언 class 내부의 접근을 중심으로 허용 |
| Modifier 생략 | 같은 package에서 접근하는 package-private |
| `protected` | 같은 package 및 상속 관계에 따른 접근 |
| `public` | 외부 class에 접근을 허용하는 공개 member |

Package(패키지)는 여기서는 classes의 묶음이라는 전제만 사용한다. 생략된 modifier를 설명하는 default access라는 말 때문에 실제 선언에 `default`를 적는 것은 아니다. `protected`도 다른 package의 아무 receiver에나 무제한 접근한다는 뜻이 아니다. 각 class 선언 형태에서 네 표기를 똑같이 쓸 수 있다는 일반화 역시 피해야 한다.

M012 p.10의 `private int weight = 80;`을 별도 class의 코드에서 직접 읽으면 private access diagnostic이 난다. 이는 값이 80이라는 사실의 비밀 여부보다 해당 접근 경로가 허용되지 않았기 때문이다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:14:06의 소개 이후, Packages의 상세는 p.23 이후 전환에서 유보되었다. 여기의 표가 그 상세 규칙을 대신하지는 않는다.

## Private helper와 실패 시 상태 보존

판매 method에 접근 경로를 모으면 입력 검사를 한 곳에 둘 수 있다. 재고보다 많은 수량을 그냥 빼면 stock이 음수가 되므로, M012 p.14는 다음 helper를 사용한다. 아래 두 method는 AppleStore class 내부의 조각이다.

```java
private boolean inStock(int num) {
    int shortage = num - stock;
    if (shortage > 0) {
        return false;
    } else {
        return true;
    }
}

boolean sell(int num) {
    if (inStock(num)) {
        balance += 2000 * num;
        stock -= num;
        return true;
    } else {
        return false;
    }
}
```

Private helper(내부 보조 메서드)는 검사 방법을 숨기고, caller에게는 판매 요청과 성공 여부만 제공한다. `sell`의 return type이 기존 void에서 boolean으로 바뀐 것은 caller가 실패를 알아야 하기 때문이다.

초기 balance=10000, stock=30에서 `sell(50)`이면 shortage=20이다. Helper가 false를 반환하여 두 대입을 모두 건너뛰므로 **결과는 false이고 상태도 10000/30으로 유지**된다. Caller는 `Not enough apples in stock`을 출력한다. 실패한 뒤 false만 반환하고 stock을 이미 줄였다면 이 계약을 지킨 것이 아니다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:21:14 및 M012 pp.15–16

반대로 이 인쇄 코드는 음수 수량을 거부하지 않는다. 같은 초기 상태에서 `sell(-1)`을 추적하면 shortage=−31이라 통과하고 balance=8000, stock=31이 된다. 이 값은 **원본 코드에서 도출한 경계 분석**이며 강의에서 그 숫자를 말했다는 뜻은 아니다. Encapsulation은 검사를 둘 장소를 제공하지만, 그 안의 검사가 자동으로 완전해지지는 않는다.

## Getter·setter의 선택과 validation

Getter와 setter(쓰기 메서드)는 Java의 특수 문법이 아니라 일반 methods의 이름·설계 관례다.

```java
private int age;

public int getAge() {
    return age;
}

public void setAge(int age) {
    this.age = age;
}
```

M012 p.18의 조각에서 getter는 값을 반환하고 setter는 parameter를 field에 대입한다. Getter만 공개하면 이 접점은 read-only(읽기 전용), setter만 공개하면 write-only(쓰기 전용)가 된다. 모든 private field에 둘 다 필요하지 않다. Class 내부까지 반드시 getter/setter만 써야 한다거나 setter가 언제나 void여야 한다는 규칙도 아니다.

Setter에는 validation(유효성 검사)을 둘 수 있다. 음수나 지나치게 큰 나이를 거절한다는 논의는 동기이며, 강의가 정확한 허용 나이 범위를 정한 것은 아니다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:24:58

### Null 검사를 먼저 하는 이유

M012 p.21의 이름 setter는 [[courses/computer_programming/units/control-flow|Short-circuit]]를 상태 보호에 사용한다.

```java
public void setName(String name) {
    if (name == null || name.equals("")) {
        System.out.println("Name cannot be null or empty");
    } else {
        this.name = name;
    }
}
```

`name == null`은 reference가 없음을 검사하고, `name.equals("")`는 존재하는 String의 내용이 비었는지 검사한다. Null이면 왼쪽이 true라 오른쪽 method 호출을 건너뛴다. 순서를 바꾸어 null receiver에 equals부터 호출하면 뒤의 검사로 보호할 수 없다. Non-null이고 빈 문자열도 아닌 경우만 저장한다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:28:49의 보충이다. Null을 특정 물리 주소 0으로 보장하는 설명은 필요하지 않다.

## Access tracing으로 사용 경로 관찰하기

접근을 methods에 모으면 읽기와 쓰기를 기록할 수도 있다. M012 p.22의 원래 class 이름은 `ChangableVar`다. `setValue`는 valueToBeWatched에 대입하고 countOfChange를 1 늘린 뒤 change 번호를 출력한다. `getValue`는 readHistory를 1 늘리고 저장값을 반환한다. 따라서 getter도 관찰 가능한 side effect(부수 효과)를 가질 수 있다.

P.23의 자료에 제시된 의도된 흐름은 다음과 같다.

| 순서 | 동작 | 추적 결과 |
| --- | --- | --- |
| 1 | 첫 `getValue()` | 기본값 0, readHistory=1 |
| 2 | `setValue(52)` | value=52, change #1 |
| 3 | `setValue(53)` | value=53, change #2 |
| 4 | 두 번째 `getValue()` | 값 53, readHistory=2 |

같은 값을 다시 넣어도 setter에는 이전 값과의 비교가 없으므로 count가 증가한다. 즉 “실제로 다른 값으로 바뀐 횟수”보다 **setter 호출 횟수**를 센다.

다만 p.23에서 호출하는 `getReadHistory()`의 정의가 p.22에 없다. 위 표는 그 history를 읽을 수 있다는 자료의 의도에 따른 설명이지, 두 페이지의 코드가 그대로 완전하게 실행된 결과라는 주장이 아니다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 01:29:46에서도 debugging·logging의 동기는 설명하지만 긴 예제의 상세 추적은 건너뛴다. 이 자료 기반 분석은 누락된 method 구현을 임의로 채우지 않고, 내부 상태를 관찰하는 접점의 설계 효과를 보여 준다.

## 핵심 정리

- Encapsulation은 사용할 접점과 허용된 변경 경로를 설계한다. 읽기 공개와 임의 쓰기 허용은 다르다.
- 판매는 balance와 stock을 함께 바꾸고 실패하면 둘 다 유지해야 한다.
- Modifier 생략은 package-private이며 public도 default keyword도 아니다.
- Setter에 검사를 모을 수 있지만 검사 내용의 완전성은 별도로 확인한다.
- Getter도 counter를 바꿀 수 있어 이름만으로 side effect가 없다고 단정하지 않는다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 값을 읽게 해도 남는 보호

Getter가 값을 알려 주는데 private field의 encapsulation이 남는 이유는? Abstraction·defensive programming과 robot 분업 비유의 약속을 설명하라.

<details><summary>해설 보기</summary>

읽기 허용과 외부의 임의 쓰기 허용은 다르다. 필요한 method 접점만 제공하면 내부 구현을 몰라도 쓰게 하면서 허용하지 않은 변경 경로를 제한할 수 있다. Abstraction은 사용 복잡성을 줄이고 defensive programming은 잘못된 상태 변경을 막는 목적이다. Robot 부분 담당자도 입력·결과·상태 약속으로 연결하며 검증 없이 믿으라는 뜻은 아니다. 여기의 interface는 사용 접점으로 Java interface 문법 전체를 전제하지 않는다.

**확인 기준:** Source 비밀과 접근 경로 제한을 혼동하지 않는다.

</details>

#### 확인 Q02 · 계층·instance·행동 차이

Organisms→Animals→Cat의 관계와 Cat objects 여러 개의 관계는 같은가? 공통 animalSound가 class마다 다른 소리를 내는 것과 같은 Car class의 speed 차이는?

<details><summary>해설 보기</summary>

첫째는 parent·child classes의 상속 관계로 특성·코드를 재사용하고 child 특성을 더한다. 여러 Cat objects는 한 class의 instances라 다른 축이다. 공통 animalSound를 구체적 class별로 다르게 구현하는 것은 polymorphism의 소개이고, 같은 Car method가 서로 다른 speed fields를 읽는 것은 instance 상태 차이다. 이 구별은 동기 소개이며 dispatch·override 세부 코드를 요구하지 않는다.

**확인 기준:** Class 관계·생성 관계·구현 차이·상태 차이를 분리한다.

</details>

#### 확인 Q03 · 한 판매의 두 상태

`balance = 10000`,stock30,가격2000에서3개 판매 후 값은? 외부가 stock만 바꾸는 문제와 sell method만 추가했을 때 남는 문제, getter의 권한을 설명하라.

<details><summary>해설 보기</summary>

`balance = 10000 + 6000 = 16000`,stock=30−3=27이다. `stock`만 줄이면 수입과 재고의 관계가 깨진다. `sell`이 두 변경을 묶어도 fields가 노출되면 외부가 우회하므로 private 접근 설계가 필요하다. Getters는 읽기만 제공해 임의 쓰기를 허용하지 않는다. Source의 sell/getters에는 public이 없어서 같은 package 호출을 가정한다.

**확인 기준:** 두 계산·우회 가능성·읽기/쓰기 권한을 설명한다.

</details>

#### 확인 Q04 · 접근 표기의 실제 의미

`private`·modifier 생략·protected·public의 현재 소개 범위를 적어라. 생략 자리에 default를 쓰는가? 별도 class가 private weight80을 읽을 때는?

<details><summary>해설 보기</summary>

`private`는 선언 class 내부 접근 중심, 생략은 같은 package의 package-private, protected는 같은 package와 상속에 따른 접근, public은 외부 접근 허용이다. `default` keyword를 넣는 것이 아니며 modifier 없다고 public이 되지 않는다. 별도 class의 직접 weight 접근은 private diagnostic을 낸다. 이 표를 모든 class 선언 형태나 cross-package의 아무 receiver에도 적용하는 완전 규칙으로 확대하지 않는다.

**확인 기준:** 네 수준과 생략 의미, 입문 표의 한정을 설명한다.

</details>

#### 확인 Q05 · 성공·실패·음수 주문

각각 독립 초기 balance10000,stock30이다. `inStock`은 `num-stock>0`이면 false, 아니면 true다. `sell`은 true일 때만 balance+=2000*num,stock-=num 후 true, 아니면 false를 반환한다. `sell(3)`, `sell(50)`, `sell(-1)`을 추적하고 helper와 boolean의 목적을 설명하라.

<details><summary>해설 보기</summary>

3은 shortage−27로 통과해 true,16000/27이다. 50은 shortage20으로 실패해 false,10000/30 유지다. −1은 shortage−31로 통과해 true,8000/31이 된다. `private` helper는 검사 세부를 내부에 모으고 boolean은 caller가 실패를 알게 한다. 실패 결과뿐 아니라 두 상태 불변을 확인해야 하며 현재 helper는 음수 검증이 빠져 완전 validation이 아니다.

**확인 기준:** 세 shortage·return·상태 및 실패 시 불변을 확인한다.

</details>

#### 확인 Q06 · 선택적인 getter·setter

`getAge`는 field를 반환하고 setAge(int age)는 this.age=age를 수행한다. 모든 private field에 둘 다 필요한가? 나이 범위와 setter의 return type을 자료에서 어디까지 정할 수 있는가?

<details><summary>해설 보기</summary>

둘은 일반 methods의 이름 관례다. Getter만 공개하면 그 접점은 read-only, setter만이면 write-only로 구성할 수 있어 항상 둘 다 필요하지 않다. Setter에 validation을 둘 수 있지만 정확한 허용 나이 범위는 제시되지 않았다. Source setAge의 void는 예 선택이지 모든 setter의 필수 규칙이 아니며 class 내부에서 언제나 accessor만 써야 하는 것도 아니다.

**확인 기준:** 관례/문법과 선택적 권한, 미정 age 범위를 구별한다.

</details>

#### 확인 Q07 · `null` guard의 순서

`name==null || name.equals("")`이면 메시지만 출력하고 아니면 field에 저장한다. `null`,빈문자열,Code의 경로와 condition을 반대로 쓸 때의 문제를 설명하라.

<details><summary>해설 보기</summary>

`null`은 왼쪽 true로 equals를 생략하고 저장하지 않는다. 빈 String은 왼쪽 false, equals true라 역시 저장하지 않는다. Code는 둘 다 false여서 저장한다. `equals`를 먼저 두면 null receiver 호출이 먼저 실패하여 뒤 guard가 보호하지 못한다. `null` 여부와 String 내용은 다른 검사이며 null을 물리 주소0으로 설명할 필요는 없다.

**확인 기준:** 세 경로·이전 field 보존·short-circuit 순서를 설명한다.

</details>

#### 확인 Q08 · 읽기·쓰기 counter

ChangableVar는 getValue마다 readHistory++, setValue마다 값을 대입하고 countOfChange++한다. Default0에서 get, set52, set53, get 후 상태는? 같은53을 한 번 더 set하면? 자료의 실행 한계도 설명하라.

<details><summary>해설 보기</summary>

첫 get은0/history1, set52는값52/change1, set53은값53/change2, 둘째 get은53/history2다. 다시53을 set해도 비교가 없어 change3이 된다. Getter도 side effect가 있고 change counter는 값이 달라진 횟수보다 호출 횟수다. P23이 부르는 getReadHistory의 정의가 p22에 없어 이 trace는 의도된 자료 분석이며 두 페이지가 완전 실행된 결과라는 뜻은 아니다.

**확인 기준:** 두 counters와 재대입의 count, 누락 method 한계를 모두 적는다.

</details>

### 적용 연습

#### 연습 P01 · 검사 추가 후 연속 요청

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.** 본문 판매 예를 바꾸어 num<=0 또는 num>stock이면 false와 상태 유지, 그 외에는 가격2000으로 판매한다고 정했다. 초기 balance10000,stock3에서 sell(0),sell(2),sell(2)를 순서대로 요청한다. 매 return·상태와 변경 전 검사해야 할 이유를 설명하라.

<details><summary>해설 보기</summary>

첫0은 새 positivity 조건에 걸려 false,10000/3 유지다. 다음2는 통과하여 true,14000/1이다. 마지막2는 현재 stock1보다 커 false,14000/1 유지다. 각 호출은 갱신된 상태를 기준으로 검사한다. 검사를 쓰기 뒤에 하면 실패한 요청도 이미 stock·balance를 바꿀 수 있어 실패 불변 계약을 깬다. 새 positivity 검사는 연습의 명시적 변경이지 원래 source가 이미 구현한 조건이 아니다.

**확인 기준:** 순차 상태·새 조건의 출처·실패 불변을 모두 확인한다.

</details>

### 복습 순서

Q01–Q04로 설계 목적과 접근을 설명한다. Q05의 성공·실패·음수 상태를 계산하고 Q06–Q08에서 validation과 counter를 추적한 뒤 P01의 각 호출을 확인한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 보정 녹음문]] — 01:08:56, 01:04:10, 01:16:32, 01:14:06, 01:21:14, 01:24:58, 01:29:46.
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 보정 녹음문]] — 00:55–01:51.

### 강의자료와 해당 페이지

- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-061).
- [5 encapsulation.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-003), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-012), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-014), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-018), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-023).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-004).

상속·다형성은 동기 소개이며 구체적인 override·dispatch나 cross-package protected receiver 규칙의 완전한 설명은 이후 범위다. AppleStore의 modifier 없는 methods는 같은 package 전제다. ChangableVar의 getReadHistory 구현은 자료에 없어 의도된 trace만 분석하며 상세 설명은 강의에서 생략되었다.


---

[[courses/computer_programming/units/objects-references|← 이전: Objects·Constructors·Static과 Reference 전달]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/lab-applications|다음: 입력 검증·Board 판정·객체 상호작용 실습 →]]
