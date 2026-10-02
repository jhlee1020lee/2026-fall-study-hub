---
title: "Encapsulation과 접근·상태 설계"
description: "접근 수준, 상태 일관성, null 검사와 getter/setter의 효과를 복습한다."
course: "computer_programming"
unit_id: "encapsulation"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["4 oop.pdf", "5 encapsulation.pdf", "Lab03 v2.pdf", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

허용할 접근과 상태 변경을 함께 설계하는 이유를 정리한다. 판매·문자열 검증·접근 기록을 추적하며 정상 결과와 실패 뒤 상태를 구분해 보자.

## Encapsulation: 상태 변경을 객체의 책임으로 묶기

객체를 사용하려고 그 내부의 모든 field(필드)와 method(메서드)를 알아야 한다면, 구현이 조금만 바뀌어도 사용하는 코드가 함께 흔들린다. Encapsulation(캡슐화)은 내부 상태와 동작을 묶고, 외부에는 필요한 interaction을 제공하는 설계다. 자동차를 운전할 때 조향 장치와 가속 장치의 사용법은 필요하지만 엔진의 모든 부품을 알 필요는 없다는 비유가 여기에 해당한다. Abstraction(추상화)은 사용자가 알아야 할 복잡성을 줄이고, defensive programming(방어적 프로그래밍)은 예상하지 않은 상태 변경을 제한한다. 내부를 숨긴다는 말은 source의 존재를 비밀로 한다는 뜻보다 **허용하는 접근 경로를 정한다**는 뜻이다. [Computer Programming M012 PDF pp.4–7]

2026-09-15 강의의 로봇 팔·머리·몸통 분업 비유도 같은 이유를 설명한다. 각 부분을 만드는 사람은 다른 부분의 전체 구현 대신 합의된 기능과 결과에 의존할 수 있다. 이는 협업에서 interface가 필요한 이유이며 검증을 생략하라는 뜻은 아니다. 여기서 interface는 일반적인 사용 경계이고, 아직 Java의 `interface` 선언을 뜻하지 않는다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:08:56–01:09:54]]의 불명확한 비율 표현은 정확한 백분율로 바꾸지 않는다. 이 설명의 기존 맥락은 [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트 · Encapsulation]]에서도 이어 볼 수 있다.

M011 p.59의 capsule 그림은 variables와 methods를 한 class로 묶는다. M012 p.3은 복잡한 기계 내부와 간단한 조작 panel을 대비한다. 두 그림을 함께 읽으면 단순히 코드를 한 상자에 넣는 것과, 사용하는 쪽에 필요한 조작만 제공하는 것의 차이가 보인다. 수리하는 사람에게 필요한 내부 정보와 정상 기능을 사용하는 사람에게 필요한 정보는 다르다.

### 판매 한 번에 함께 바뀌는 두 값

`FruitStore`는 `balance = 10000`, `stock = 30`에서 시작한다. 개당 가격이 `2000`인 과일 세 개를 팔면 다음 두 변화가 함께 일어나야 한다.

\[
\text{stock}'=30-3=27,\qquad
\text{balance}'=10000+2000\times3=16000.
\]

외부 코드가 두 field를 직접 수정하면 판매 규칙을 알아야 하고, 재고만 줄이는 실수를 할 수 있다. M012 p.5는 다음처럼 두 대입을 한 행동으로 묶는다. 이는 판매 예제의 method이며 완전한 상거래 시스템은 아니다.

```java
void sell(int num) {
    balance += 2000 * num;
    stock -= num;
}
```

이제 caller(호출자)는 `sell(3)`을 요청하면 된다. 다만 method를 추가해도 field가 그대로 노출되어 있다면 caller가 그 경로를 우회할 수 있다. `AppleStore`는 두 field를 `private`로 두고 `getBalance()`, `getStock()`으로 읽으며 `sell()`로 변경하도록 만든다. 값을 알 수 있다는 것과 원하는 값을 대입할 수 있다는 것은 다르다. Getter(조회 메서드)는 이 구별을 가능하게 한다. [M012 PDF pp.11–12]

이 예제의 methods에는 `public`이 없다. 실제 접근 수준은 같은 package에서 사용할 수 있는 package-private이다. 강의도 모든 코드가 같은 package에 있다고 전제한다. 편의상 공개된 기능이라고 부른 표현을 실제 `public` 선언으로 기억하면 안 된다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:16:32–01:18:17]]

## Access control: 사용할 수 있는 경로 정하기

Access modifier(접근 제어자)는 특정 위치에서 member를 사용할 수 있는지 정한다. M012 p.10의 `private int weight = 80;`을 별개의 외부 class에서 직접 읽으려 하면 private access 오류가 난다. 값이 없어서가 아니라 그 접근이 허용되지 않아서다.

| 표기 | 이 범위에서의 의미 | 구별할 점 |
|---|---|---|
| `private` | 선언한 class 내부의 접근 | 외부가 field 이름을 안다고 직접 접근할 수 있지는 않다. |
| modifier 생략 | 같은 package에서 접근 | `default`라는 접근 keyword를 적는 것이 아니다. |
| `protected` | 같은 package와 subclass의 상속 문맥에서 접근 | 다른 package에서는 임의의 부모 객체를 통한 접근까지 허용하지 않는다. |
| `public` | 외부에도 공개하는 member | 그 member를 담은 class 자체의 접근 가능성도 필요하다. |

이는 member 접근을 이해하는 출발점이다. 네 수준을 모든 top-level class 선언에 그대로 적용할 수는 없다. Package의 이름 공간과 top-level class 접근은 [Packages](packages.md)에서, 다른 package의 subclass에 관한 제한은 [Inheritance](inheritance.md)에서 구체화한다. [M012 PDF pp.9–10]

### 실패를 반환하면서 상태는 보존하기

접근을 제한해도 허용된 method가 잘못된 상태를 만들 수 있다. 재고 `30`에서 무조건 `50`개를 판매하면 재고가 음수가 된다. M012 pp.13–16은 `private` helper인 `inStock(int num)`을 두고 `shortage = num - stock`이 양수이면 `false`, 아니면 `true`를 돌려준다. 판매는 이 검사에 성공했을 때만 두 field를 변경한다.

```java
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

`sell(50)`에서는 `50 - 30 = 20`이므로 실패한다. 반환값은 `false`이고 상태는 `balance = 10000`, `stock = 30` 그대로다. 자료의 caller는 이 결과를 받아 `Not enough apples in stock`을 출력한다. 실패 메시지를 출력하는 역할과 판매 method의 반환 역할을 구분해야 한다. 반환 type이 `void`에서 `boolean`으로 바뀐 이유도 요청이 성공했는지 caller가 알아야 하기 때문이다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:20:14–01:22:07]]

이 helper가 완전한 validation(유효성 검사)은 아니다. **원본 코드로부터 계산한 경계 사례**로, 초기 상태에서 `sell(-1)`은 `shortage = -31`이어서 검사를 통과한다. 잔액은 `8000`, 재고는 `31`이 된다. 음수 주문을 거부하는 조건이 원본에 없기 때문이다. 이는 새로 설명한 코드 추론이며 강의자가 이 사례를 말했다는 주장은 아니다. Encapsulation은 검사를 둘 책임을 모아 주지만 올바른 검사 내용을 자동으로 만들어 주지는 않는다.

## Getter와 setter: 조회·검증·추적을 나누기

Getter와 setter(설정 메서드)는 Java의 특수 문법이 아니라 일반 method의 이름과 역할에 관한 관례다. M012 p.18의 `getAge()`는 `age`를 반환하고, `setAge(int age)`는 `this.age = age`로 현재 객체의 field에 parameter(매개변수)를 대입한다. 모든 private field에 두 method를 모두 제공할 필요는 없다. Getter만 공개하면 해당 경로는 read-only, setter만 공개하면 write-only로 설계할 수 있다. 이것이 class 내부에서도 field를 바꿀 수 없다는 뜻은 아니다. 앞의 `sell()`도 자기 class의 private fields를 직접 갱신한다.

Setter는 대입 전 validation을, getter와 setter는 호출 기록을 수행할 수도 있다. 2026-09-15 01:24:58–01:25:52의 나이 예는 부적절한 입력을 거부할 수 있다는 동기다. 음수나 지나치게 큰 수를 언급했다는 이유로 특정 나이 범위가 공식 predicate(판정 조건)로 정해진 것은 아니다. [[courses/computer_programming/transcripts/2026-09-15|해당 날짜 STT · 선택적 접근과 validation]]

### `null`과 빈 문자열을 구분하는 검사 순서

M012 p.21의 `Person.setName`은 `name == null || name.equals("")`를 검사한다. `null`은 reference(참조)가 객체를 가리키지 않는 상태이고, `""`는 빈 내용의 String이다. 첫 조건은 reference 상태를, 둘째는 문자열 내용을 확인한다. `||`의 short-circuit evaluation(단락 평가) 때문에 첫 조건이 참이면 둘째 조건은 실행되지 않는다. 따라서 `null`에 `equals()`를 호출하지 않는다. 순서를 거꾸로 하면 나중의 null 검사로 앞선 호출 실패를 막을 수 없다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:26:50–01:28:49]]

강의의 주소 0이라는 설명은 개념적 단순화다. 이 설명에서 필요한 것은 “호출할 객체가 없다”는 의미이며 Java가 물리 주소 0을 보장한다는 주장이 아니다.

Lab04의 `Book`은 같은 원리를 제목에 적용한다. 다음은 [NM003 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-009)의 일반 설명 예제이며, NM002 v2 p.8에도 같은 코드가 있다. 이 Lab04 부분은 새 녹음이나 배정된 강의 날짜가 없는 **자료 기반 보충**이다.

```java
class Book {
    private String title;

    public void setTitle(String title) {
        if (title == null || title.equals("")) {
            System.out.println("Title cannot be null or empty");
        } else {
            this.title = title;
        }
    }

    public String getTitle() {
        return title;
    }
}
```

새 객체의 `title`에는 명시적 초기값이 없으므로 `null`이 들어 있다. 다음은 이 코드의 상태 변화를 설명하기 위해 구성한 trace다.

| 순서 | 입력 또는 동작 | 이후 `title` | 이유 |
|---|---|---|---|
| 생성 직후 | `getTitle()` | `null` | 아직 제목을 저장하지 않았다. |
| 첫 설정 | `setTitle("Java")` | `"Java"` | 두 거부 조건이 모두 거짓이다. |
| 실패한 설정 | `setTitle("")` | `"Java"` | 오류 branch에는 field 대입이 없다. |
| 다시 실패 | `setTitle(null)` | `"Java"` | short-circuit 후 거부하며 이전 값은 남는다. |
| 공백 설정 | `setTitle(" ")` | `" "` | 공백 한 글자는 빈 문자열과 다르다. |

공백을 자동으로 제거하거나 거부한다고 해석하면 이 predicate보다 강한 규칙을 발명하게 된다. `getTitle()` 자체는 이 예에서 상태를 바꾸지 않는다. 그러나 getter라는 이름만으로 모든 getter가 부작용이 없다고 단정할 수도 없다.

### 조회 기록도 상태 변화다

M012 pp.22–23의 원본 class 이름은 `ChangableVar`다. `setValue()`는 값을 대입할 때마다 `countOfChange`를 증가시키고 change 번호를 출력한다. `getValue()`는 `readHistory`를 증가시킨 뒤 값을 반환한다. 따라서 getter를 부르는 행위도 기록 상태를 바꾼다.

의도된 trace는 첫 조회 값 `0`/history `1`, `setValue(52)` 뒤 change `#1`, `setValue(53)` 뒤 change `#2`, 둘째 조회 값 `53`/history `2`다. 같은 값을 두 번 설정해도 setter에 이전 값과 비교하는 조건이 없으므로 두 번 센다. Counter가 뜻하는 것은 실제 값이 달라진 횟수가 아니라 **그 method가 호출된 횟수**다.

다만 p.23에서 호출하는 `getReadHistory()` 정의는 p.22에 없다. 따라서 이 trace는 자료가 의도한 설명이고 두 페이지를 그대로 합친 완전한 실행 프로그램은 아니다. 2026-09-15 01:29:46 강의도 logging/debugging의 동기를 설명하고 긴 trace의 상세 순회는 생략했다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT · 접근 기록]]

## 공통 상태의 재사용과 서로 다른 행동

Encapsulation이 사용 경계를 정한다면, inheritance(상속)는 class 사이에서 특성을 재사용하고 확장하는 관계이고, polymorphism(다형성)은 공통 행동을 구체적인 class마다 다르게 제공하는 개념이다. M011 pp.58–61과 M014 p.4는 각각 abstraction, code reuse, 행동 다양화라는 동기를 연결한다.

M011 p.60의 그림은 `Organisms` 아래 `Animals`와 `Plants`, 그 아래 각각 `Duck`·`Cat`과 `Tree`·`Grass`를 둔다. 더 구체적인 class가 공통 특성을 이어받는 구조를 읽는다. 강의의 `Cat`에 tail을 추가하는 비유도 이 확장을 설명하지만, 불확실한 생물학 표현이나 method 이름을 검증된 사실로 복원하지는 않는다.

예를 들어 동물의 특성을 바탕으로 `Cat` class에 새 특성을 추가하는 일과, 그 class로 여러 cat objects를 만드는 일은 다르다. 개·고양이·오리의 `animalSound()`는 공통 요청을 받지만 각 class에 맞는 소리를 제공한다. 이는 같은 class의 두 객체가 단지 서로 다른 속도 값을 가진다는 설명보다 구현의 차이에 초점을 둔다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:03:16–01:04:10]]

[[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 강의 노트 · OOP 복습]]과 [[courses/computer_programming/transcripts/2026-09-17|같은 날짜 STT 00:55–01:51]]도 이 세 특징을 소개한다. 당시의 개념 소개와 새 자료의 상세 문법은 구분한다. [Inheritance](inheritance.md)의 재사용·접근·생성 규칙과 [Object contracts and interfaces](object-contracts-interfaces.md)의 호출 선택은 이 기초를 확장하는 자료 기반 학습이다.

## 핵심 정리

- Encapsulation은 읽기 허용과 임의 변경 허용을 구별하며, abstraction과 data protection을 함께 지원한다.
- 성공한 판매는 관련 상태를 함께 바꾸고 실패는 상태를 보존해야 한다. `private`만으로 입력 검사가 완성되지는 않는다.
- Modifier 생략은 package-private이다. Getter/setter는 일반 method라서 검증·기록을 수행할 수 있다.
- `null` 검사를 먼저 둔 `||`와 정확한 문자열 조건을 따라 추적한다. 빈 문자열과 공백 문자열은 다르다.
- Inheritance는 class의 재사용 관계이고 polymorphism은 공통 요청의 구현 차이다.

## 확인·연습문제

### 접근과 상태

#### 확인 Q01 · 설계 경계

자동차 조작부와 로봇 분업 비유에서 abstraction과 defensive programming의 역할을 나누어 설명하라. Getter가 값을 알려 주면 encapsulation이 사라지는가?

<details><summary>해설 보기</summary>

조작부는 사용하는 데 필요한 기능만 드러내 내부 복잡성을 줄인다. 로봇의 각 담당자도 다른 부분 전체 대신 합의된 동작에 의존한다. Defensive programming은 허용된 경로로만 상태를 바꾸게 한다. Getter로 읽는 것과 임의 대입은 다르므로 encapsulation은 남는다. 구현을 비밀로 하거나 협업 검증을 생략한다는 뜻은 아니다.

**확인 기준:** 복잡성 축소, 변경 경로 통제, 읽기/쓰기 권한 구별을 모두 설명한다.

</details>

#### 확인 Q02 · Class 관계와 객체

`Cat`에 공통 동물 특성을 재사용하고 tail을 추가하는 일, cat 객체 둘을 만드는 일, `animalSound()`를 동물별로 다르게 제공하는 일을 구별하라.

<details><summary>해설 보기</summary>

첫째는 parent 특성의 재사용·확장인 inheritance다. 둘째는 같은 class로 별도 objects를 만드는 일이다. 셋째는 공통 행동을 구체 class마다 다르게 구현하는 polymorphism의 소개다. 같은 class의 두 객체가 서로 다른 speed 값을 가진다는 사실만으로 세 번째 설명을 대신할 수 없다. 당시 녹음은 이 동기를 소개한 것이며 상세 dispatch 문법은 별도 자료 학습이다.

**확인 기준:** Class 확장, 객체 생성, 구현 다양화의 세 층을 구별한다.

</details>

#### 확인 Q03 · 함께 바뀌는 상태

초기 `balance=10000`, `stock=30`, 가격 2000에서 세 개를 판매하면 무엇이 남는가? `sell()` 추가만으로 외부의 잘못된 변경을 막을 수 있는가?

<details><summary>해설 보기</summary>

`stock=30-3=27`, `balance=10000+2000*3=16000`이다. 두 변경을 `sell()`에 모아야 caller가 한쪽 변경을 빠뜨리지 않는다. Field가 계속 노출되면 method를 우회할 수 있으므로 private 상태와 허용된 methods를 함께 설계한다. Getter는 조회 경로만 제공한다. 원본 `sell`·getters에는 `public`이 없어서 같은 package에서의 호출을 전제한다.

**확인 기준:** 두 수치, 우회 가능성, 원본 package-private를 확인한다.

</details>

#### 확인 Q04 · 접근 수준

`private`, modifier 생략, `protected`, `public`의 접근 범위를 설명하라. 별도 class가 `private int weight=80`을 읽지 못하는 이유와 `default`를 적어야 하는지도 답하라.

<details><summary>해설 보기</summary>

`private`는 선언 class 내부 접근, 생략은 같은 package 접근, `protected`는 같은 package 및 subclass의 상속 문맥, `public`은 외부 접근을 허용한다. `weight`의 값은 존재하지만 직접 읽을 권한이 없다. Package-private를 위해 `default`를 쓰지 않는다. 다른 package의 subclass가 임의의 부모 receiver까지 자유롭게 쓸 수는 없고, public member라도 담고 있는 class가 접근 가능해야 한다. 네 modifier를 top-level class에도 그대로 적용하지 않는다.

**확인 기준:** 값 존재와 접근 허용을 분리하고 protected의 한정을 남긴다.

</details>

#### 확인 Q05 · 실패와 음수 경계

원본 `inStock`은 `num-stock>0`이면 실패한다. 각기 초기 `(balance,stock)=(10000,30)`에서 `sell(50)`과 `sell(-1)`의 반환·상태를 계산하고 boolean 결과의 역할을 설명하라.

<details><summary>해설 보기</summary>

`50-30=20`이므로 첫 호출은 `false`, 상태 `(10000,30)`을 유지한다. Caller가 실패 메시지를 출력하며 helper가 메시지 책임까지 맡는 것은 아니다. `-1-30=-31`은 검사를 통과하므로 둘째는 `true`, 잔액 `10000-2000=8000`, 재고 `30-(-1)=31`이다. `boolean`은 성공 여부를 전달하려고 `void` 대신 사용한다. Helper를 private로 두어 검사 구현을 감추더라도 음수 거부 조건은 별도로 필요하다. 음수 trace는 코드 추론이다.

**확인 기준:** 실패 시 두 상태 보존과 음수 통과의 계산을 모두 확인한다.

</details>

### 검증과 기록

#### 확인 Q06 · 선택적 접근과 short-circuit

Getter/setter는 특수 문법인가? `this.age=age`의 양쪽을 구별하고, `name==null || name.equals("")`의 순서를 바꾸면 왜 위험한지 설명하라.

<details><summary>해설 보기</summary>

둘은 일반 method의 관례다. `this.age`는 현재 객체 field, 오른쪽 `age`는 parameter다. Getter만 또는 setter만 공개해 외부 읽기/쓰기 경로를 선택할 수 있고 내부 method는 자기 private field를 직접 사용할 수 있다. `null`이면 왼쪽이 참이어서 오른쪽 호출을 생략한다. 역순은 객체 없는 reference에 먼저 `equals()`를 호출하므로 나중 검사가 보호하지 못한다. Null은 빈 문자열도 보장된 물리 주소 0도 아니다. 나이 예는 검증 동기이지 공식 허용 구간은 아니다.

**확인 기준:** 관례·parameter 구별·선택적 공개·평가 순서 네 항목을 확인한다.

</details>

#### 확인 Q07 · 기록의 부작용

`ChangableVar`에서 첫 조회, `setValue(52)`, `setValue(53)`, 둘째 조회의 값과 counters를 추적하라. 같은 값을 두 번 설정할 때와 자료의 실행 가능성도 설명하라.

<details><summary>해설 보기</summary>

첫 읽기는 값 0/history 1, 두 설정은 change #1과 #2, 둘째 읽기는 값 53/history 2다. Getter도 `readHistory`를 바꾸므로 부작용이 있다. Setter는 값 비교 없이 호출마다 증가하므로 같은 값 두 번도 두 번 센다. 이는 실제 값 변경 횟수와 다르다. P.23에서 쓰는 `getReadHistory()`가 p.22에 정의되어 있지 않으므로 의도된 trace이지 완성 코드의 실행 입증은 아니다. 녹음도 긴 trace는 생략했다.

**확인 기준:** 값·읽기 수·설정 호출 수를 분리하고 누락 method를 지적한다.

</details>

#### 확인 Q08 · Book의 거부 경로

새 `Book`의 제목을 조회한 뒤 `setTitle("Java")`, `setTitle("")`, `setTitle(null)`, `setTitle(" ")`를 차례로 호출한다. 각 단계의 값과 거부 조건을 설명하라.

<details><summary>해설 보기</summary>

처음은 field 기본값 `null`이다. 이후 `"Java"`, `"Java"`, `"Java"`, `" "`가 된다. 빈 문자열과 null은 오류 branch에 들어가 대입하지 않아 이전 값이 남는다. Null은 short-circuit로 안전하게 거부된다. 공백은 `equals("")`가 아니므로 허용된다. 이 getter는 값을 바꾸지 않으며, trim이나 공백 거부를 추가한 코드로 해석하지 않는다. Lab04의 자료 복습이며 새 녹음의 사례는 아니다.

**확인 기준:** 초기값과 실패 뒤 보존, 공백 통과를 모두 맞힌다.

</details>

### 적용 연습

#### 연습 P01 · 접근 가능한 변경인가

새로 만든 강의 기반 일반 연습이다. 후보의 package·subclass 접근 문제는 Inheritance에서 다루며, 이 상태 보존 연습의 직접 기출 형식 근거로 사용하지 않는다. 선수 개념은 Q03–Q05다. 같은 package의 별도 `Cashier`가 원본 `AppleStore`의 `stock`에 직접 대입하거나 `sell(50)`을 호출하려 한다. 어느 경로가 허용되는지, 허용된 호출이 실패하면 무엇이 남는지 설명하라.

<details><summary>해설 보기</summary>

직접 field 대입은 `private`라 금지된다. Modifier 없는 `sell(50)`은 같은 package라 호출 가능하지만 stock 30에서는 `false`이고 balance 10000, stock 30이 유지된다. 접근 가능성은 요청의 성공 여부와 별개다. 원본의 다른 package subclass 표 전체를 해결했다는 뜻은 아니다.

**확인 기준:** 접근 판정과 상태 판정을 따로 쓰고 두 field를 확인한다.

</details>

#### 연습 P02 · 이름 검증과 접근 기록

새로 만든 강의·자료 기반 일반 연습이다. 해당 검증·기록 조합의 직접적인 기출 형식 근거는 없다. 동료가 “getter는 항상 상태를 보존하고, null/empty 검사면 공백도 거부된다”고 주장한다. Q06–Q08의 서로 다른 두 예로 각각 반박하고, 확인할 관찰값을 제시하라.

<details><summary>해설 보기</summary>

`ChangableVar.getValue()` 뒤에는 watched value가 같아도 `readHistory`가 1 늘어 첫 주장이 깨진다. `Book.setTitle(" ")`은 빈 문자열 비교가 거짓이라 공백을 저장해 둘째 주장이 깨진다. 같은 getter 이름이나 안전해 보이는 조건만으로 동작을 일반화하지 말고 실제로 바뀌는 field와 predicate를 확인한다.

**확인 기준:** 두 반례마다 관찰값과 코드상의 이유를 연결한다.

</details>

### 짧은 복습 계획

Q03·Q05·Q08을 표 없이 다시 추적하고 Q04로 접근 가능성을 설명한다. 다음 날 Q07과 P02를 풀어 이름만 보고 부작용을 추측하지 않는지 확인한다.

## 출처

9월 15일의 접근·검증 설명과 9월 17일의 OOP 소개를 연결한다. Lab04의 Book 확장은 녹음 없는 자료 복습이다. 불명확한 비율·생물학 표현은 확정하지 않으며, `ChangableVar`의 누락 method와 AppleStore의 음수 주문 한계를 남긴다.

### 날짜별 노트와 녹취

- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · 강의 노트]]

- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · 강의 노트]]

- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 · 보정 녹취 · 01:03:16–01:04:10; 01:08:56–01:09:54; 01:16:32–01:18:17; 01:20:14–01:22:07; 01:24:58–01:29:46]]

- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 · 보정 녹취 · 00:55–01:51]]

### 자료와 해당 페이지

- [4 oop · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.58](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-058), [p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-059), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-061)

- [5 encapsulation · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-007), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-015), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-018), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-023)

- [Lab03 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-004)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-008)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-004), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-009)

이 단원과 직접 대응하는 기출 형식 근거가 없어 P 문제는 강의·자료 기반 일반 연습으로 제시한다.
