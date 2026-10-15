---
title: "메서드 시그니처와 오버로딩 설계"
description: "Signature·overload 선택과 constructor 위임을 추적하고 generic의 재사용 동기를 구별한다."
course: "computer_programming"
unit_id: "method-overloading"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["8 polymorphism.pdf", "Lab 6 Polymorphism.pdf", "6 inheritance 1.pdf", "Lecture 2 Java Basics 1.pdf", "7 inheritance 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2", "courses/computer_programming/lectures/2026-09-01-lecture-01", "courses/computer_programming/lectures/2026-09-10-lecture-04", "courses/computer_programming/lectures/2026-09-15-lecture-05", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

## Method signature와 overload의 선택

### 같은 행동을 여러 입력 형태에 제공하기

숫자를 출력하는 기능마다 `printInt`, `printFloat`, `printString`이라는 별도 이름을 붙이면 사용자는 같은 목적의 동작을 여러 이름으로 기억해야 한다. Polymorphism(다형성)은 하나의 이름이나 계약을 통해 여러 형태의 행동을 제공하는 관점이다. 그중 overloading(오버로딩)은 같은 이름에 서로 다른 parameter 목록을 허용한다. 의미가 비슷하다는 것만으로 Java의 동일한 method가 되는 것은 아니다. 예를 들어 `Animal.move()`와 `Fish.swim()`은 모두 이동을 표현하더라도 이름이 다르므로 서로 overriding 관계가 아니다. [computer_programming:NM004, PDF pp.4-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

이 단원의 non-generic method에서 signature(시그니처)를 비교할 때는 **method 이름과 순서 있는 parameter type 목록**을 본다. Parameter의 변수 이름과 return type은 이 구별에 들어가지 않는다.

| 선언 형태 | 구별되는 부분 |
|---|---|
| `int add(int a, int b)` | `add(int, int)` |
| `int add(int x, int y, int z)` | `add(int, int, int)` |
| `float add(float a, float b)` | `add(float, float)` |
| `double add(int x, int y)` | 첫 행과 같은 `add(int, int)` |

앞의 세 형태는 parameter의 개수나 type이 달라 함께 제공할 수 있다. 마지막 형태를 첫 행과 함께 선언하는 것은 반환형만으로 overload를 나누려는 것이어서 허용되지 않는다. 호출자가 `add(1, 2)`라고 쓰는 입력 형태가 같기 때문이다. Parameter 이름을 `a, b`에서 `x, y`로 바꾸어도 새 signature가 생기지 않는다. 자료 p.7의 일반적인 signature 표기는 반환형도 함께 보여 주지만, Java에 대한 p.8과 날짜 미확인 녹취 27:51은 반환형을 제외한다고 설명한다. 이 두 문맥을 구분해야 한다. [computer_programming:NM004, PDF pp.7-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 27:51]]

Overloading은 **다른 signature를 추가**하는 일이고, overriding은 **상속된 instance method의 같은 signature에 다른 구현을 제공**하는 일이다. 반환형만 바꾼 선언을 overloading이라고 부르면 이 구분도 무너진다. 비공식 타 교수 기출 복원본의 signature 관련 항목은 이 구별을 다시 따져 보는 보조 연결이다. 현재 수업의 출제 범위를 뜻하지 않는다. [EX:cp_2026_1_final_q01a p.1]

### Type별 이동과 배열의 절댓값 합

같은 작업을 다른 type의 입력에 제공하는 간단한 예가 `Point.move`다. 다음 발췌의 좌표 fields는 `float`이고, 두 method는 입력 type만 다르게 받는다. [computer_programming:NM004, PDF pp.11-12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

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

원점에서 `move(3, 0)`을 부르면 두 `int` 인자에 맞는 overload를 통해 좌표가 `(3.0, 0.0)`이 된다. 이어 `move(0.0f, 4.0f)`를 부르면 두 `float` 인자에 맞는 overload가 선택되어 `(3.0, 4.0)`에 도달한다. 접미사 `f`는 설명용 장식이 아니라 literal의 type을 구별하는 부분이다. [computer_programming:NM004, PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

입력 모양이 달라도 밀접한 계산이면 같은 이름이 유용하다. 자료의 `abs_add(double a, double b)`는 두 값의 절댓값 합을 반환한다. 배열을 받는 `abs_add(double[] arr)`는 그 scalar overload를 반복해서 호출한다. 다음은 두 핵심 body를 함께 읽기 위한 발췌다. [computer_programming:NM004, PDF p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

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

보통의 유한 입력에서 누적값 `sum`은 음수가 아니다. 그러므로 다음 단계의 `abs_add(sum, arr[index])`는 이미 모은 합에 다음 원소의 절댓값을 더한다. 자료의 `1.0`부터 `10.0`까지 배열은 `1 + 2 + … + 10 = 55.0`이 된다. 같은 원리를 확인하기 위해 새로 고른 작은 배열 `{-2.0, 3.0, -4.0}`을 손으로 추적하면 다음과 같다.

| 처리한 원소 | 계산 | 새 `sum` |
|---|---|---:|
| 없음 | 초기값 | 0.0 |
| -2.0 | `abs_add(0.0, -2.0)` | 2.0 |
| 3.0 | `abs_add(2.0, 3.0)` | 5.0 |
| -4.0 | `abs_add(5.0, -4.0)` | 9.0 |

이 재사용은 `extends`로 구현을 상속받는 일이 아니다. 한 overload의 body가 다른 overload를 **호출하여** 공통 계산을 이용하는 것이다. 핵심 계산을 한곳에서 관리하면 그에 의존하는 배열 계산도 같은 변경을 따르기 쉽다. 반대로 scalar method의 의미를 바꾸면 배열 method의 의미도 다시 확인해야 한다. 날짜 미확인 녹취 34:41의 호출 비용 언급을 모든 호출의 성능 결론으로 일반화할 수는 없다. 여기서 확인되는 이점은 구현의 중복과 변경 부담을 줄이는 설계다. 이 예는 NaN, infinity, overflow까지 규정한 일반 수치 library의 계약은 아니다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 34:41]]

### 추가 parameter로 검색의 시작 위치 지정하기

기본 기능은 유지하면서 선택 정보를 더 받는 overload도 있다. 자료의 DNA 문자열과 `String.indexOf`가 그 예다. 두 번째 parameter는 “몇 번째 일치”라는 순번이 아니라 **검색을 시작할 index**다. [computer_programming:NM004, PDF p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
String dna = new String("TACGAAGTTACTCGCTGTCAGATCGTAAGCGACGCGATCGTAATGTGAAT");
int first = dna.indexOf("CGC");
int second = dna.indexOf("CGC", first + "CGC".length());
~~~

Index는 0부터 센다. 첫 `CGC`가 시작하는 위치는 12이고 길이는 3이다. 따라서 두 번째 호출은 `12 + 3 = 15`부터 검색하여 다음 일치의 시작 위치 32를 얻는다. 12를 그대로 넘기면 첫 일치가 여전히 검색 구간에 있으므로 같은 12를 다시 찾는다. 이름을 `indexOfSecond`로 늘리는 대신 같은 검색 method에 시작 위치라는 추가 정보를 준 셈이다.

이 코드는 첫 일치가 있다는 전제에서 두 번째 검색을 보여 준다. 첫 결과가 `-1`인 경우의 처리를 포함하지 않으며, 앞 일치의 길이만큼 건너뛰므로 겹치는 모든 일치를 열거하는 일반 알고리즘도 아니다. 날짜 미확인 녹취 35:41의 검색어는 `CCT`로 들리는 불확실성이 있고 36:41의 설명에는 이 offset이 빠진 듯한 부분이 있다. 위의 `CGC`와 `+ length()`는 인쇄 코드의 근거이며, 발화를 복원한 인용문이 아니다. NM005 p.5의 `indexof` 표기도 정확한 Java identifier `indexOf`와 구분해야 한다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 35:41]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 36:41]] [computer_programming:NM005, PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

### 기본값 wrapper와 공통 body에 대한 위임

Overload는 parameter를 생략한 호출에 기본값을 제공할 수도 있다. 자료의 `power`에서는 지수를 받는 method가 계산을 맡고, 지수가 없는 method가 기본 지수 2를 전달한다. [computer_programming:NM004, PDF p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
static double power(double input, int n) {
    if (n <= 0)
        return 1;
    return input * power(input, n - 1);
}

static double power(double input) {
    return power(input, 2);
}
~~~

`power(2)`는 먼저 `power(2, 2)`로 연결된다. 계산은 `2 × power(2, 1)`, 다시 `2 × 2 × power(2, 0)`이며 마지막 호출이 1을 반환하므로 결과는 `4.0`이다. `power(2, 10)`은 2를 열 번 곱하여 `1024.0`을 얻는다. 반환형이 `double`이므로 base case의 정수 literal `1`도 반환할 때 그 type으로 변환된다.

조건이 `n == 0`이 아니라 `n <= 0`이라는 점도 계산의 일부다. 인쇄된 코드에 `n = -1`을 주면 바로 `1.0`을 반환한다. 음의 지수에 대해 역수를 계산하는 일반적인 수학적 거듭제곱 함수로 읽으면 안 된다. 여기서 배우는 것은 기본값 wrapper와 재귀 body의 관계이며, 모든 입력의 수학적 계약이나 자원 한계까지 보장한 구현은 아니다.

같은 위임 원리는 `debug`에도 적용된다. 자료의 기본 `debug()`는 `var1`을 출력한다. 추가 메시지를 받는 `debug(String s)`의 첫 제안은 그 field 출력식을 복사한다. 둘째 제안은 추가 부분만 출력한 뒤 기본 method를 부른다. 다음 두 body는 **서로 선택할 대안**이다. 같은 class에 같은 signature로 둘 다 선언하는 예가 아니다. [computer_programming:NM004, PDF p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
// Alternative A: copy the field-output expression
void debug(String s) {
    System.out.println(s + "var 1 : " + this.var1);
}

// Alternative B: delegate the common field output
void debug(String s) {
    System.out.print("Output : " + s);
    debug();
}
~~~

`var1 = 0`, `s = "state: "`라면 첫 대안은 `state: var 1 : 0`을 출력한다. 둘째는 기본 `debug()`가 `var 1 : 0`을 출력하므로 전체 줄이 `Output : state: var 1 : 0`이 된다. 둘째에만 `"Output : "`가 있으므로 두 body의 문자열까지 같다고 할 수는 없다. 다만 기본 field 출력의 형식을 바꿀 때 위임한 대안은 그 변경을 자동으로 따르는 구조다. 날짜 미확인 녹취 41:23은 이를 문법상 강제가 아니라 설계 원칙으로 설명한다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 41:23]]

### Constructor overload와 초기화 의미의 일관성

Constructor도 parameter 목록이 다르면 여러 초기화 경로를 제공할 수 있다. NM004 p.17의 `Point`는 `double x, y`를 가지며 다음 네 경로를 비교한다. 앞서 `move`를 설명한 `float` fields의 예제와는 별개 class 예제다. [computer_programming:NM004, PDF p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

| Constructor | 입력의 의미 | 저장하는 좌표 |
|---|---|---|
| `Point()` | 원점 | `x = y = 0` |
| `Point(int x, int y)` | Cartesian coordinates(직교좌표) | 받은 `x, y` |
| `Point(float x, float y)` | Cartesian coordinates | 받은 `x, y` |
| `Point(double radius, double theta)` | Polar coordinates(극좌표) | `radius * Math.cos(theta)`, `radius * Math.sin(theta)` |

마지막 경로에서 수학적으로 `radius = 2`, `theta = 0`이면 `x = 2 cos 0 = 2`, `y = 2 sin 0 = 0`이다. 핵심은 constructor가 단순 대입 외에 표현을 변환할 수도 있다는 점이다.

그러나 구별할 수 있는 signature가 곧 이해하기 좋은 API를 뜻하지는 않는다. `new Point(2.0f, 0.0f)`는 두 값을 Cartesian coordinates로, `new Point(2.0, 0.0)`는 radius와 theta로 해석한다. Type의 정밀도를 바꾸었을 뿐이라고 생각한 호출자가 좌표계까지 바뀐다는 사실을 놓치기 쉽다. 날짜 미확인 녹취 44:12는 이 혼란을 지적하고 좌표계 indicator처럼 의미를 명시하는 구별을 제안한다. 그 제안은 새로운 필수 constructor의 정확한 구현을 제공한 것은 아니다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 44:12]]

자료의 `import Math;`는 유효한 import의 근거로 삼을 수 없다. 여기서 필요한 것은 인쇄된 constructor 목록과 변환식의 의미다. 그 한 줄을 조용히 고쳐 페이지 전체를 완전한 실행 프로그램으로 제시하지 않는다. 구두의 radius·radians 관련 불명확한 표현 역시 인쇄 identifier와 수식으로 대체한 발화처럼 인용하지 않는다.

### this와 super로 초기화 경로 연결하기

여러 constructor가 같은 대입을 반복한다면 한 constructor로 모을 수 있다. NM004 p.18은 다음과 같이 `Point(float, float)`에 공통 초기화를 맡긴다. 여기에서도 fields는 `double`이지만 constructor 목록은 앞 페이지와 다르다. 특히 앞 페이지의 두 `double` parameter constructor를 이 예에 합쳐 넣으면 안 된다. [computer_programming:NM004, PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
Point(float x, float y) {
    this.x = x;
    this.y = y;
}

Point(int x, int y) {
    this((float)x, (float)y);
}

Point() {
    this(0, 0);
}
~~~

`new Point()`의 위임 경로를 parameter type과 함께 추적하면 다음과 같다.

| 단계 | 선택 이유 | 다음 동작 |
|---|---|---|
| `Point()` | 인자 없음 | `this(0, 0)` |
| `Point(int, int)` | `0` 두 개는 `int` literal | 두 값을 `float`로 cast하여 위임 |
| `Point(float, float)` | 명시적으로 변환한 두 `float` | fields에 대입 |

이는 객체 세 개를 만드는 과정이 아니다. **객체 하나의 초기화**에서 여러 constructor body를 거쳐 공통 대입을 수행한다. 안쪽의 위임받은 초기화를 마친 뒤 바깥 constructor로 돌아온다.

날짜 미확인 녹취에서는 `0.0`을 쓰자는 설명도 나온다. 그러나 접미사 없는 `0.0`은 `double`이므로 이 페이지의 `int`/`float` constructor에 그대로 전달할 수 없다. 별도의 학습용 표현 `this(0.0f, 0.0f)`라면 두 `float`를 직접 전달한다. 이것은 type을 분명히 하기 위해 새로 쓴 비교이며 원래 발화를 `0.0f`라고 고친 인용이 아니다. [computer_programming:NM004, PDF pp.18-19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 46:08]]

`this(...)`는 같은 class의 다른 constructor에, `super(...)`는 직접 superclass의 constructor에 초기화를 맡긴다. Constructor는 상속받아 override하는 instance method가 아니다. Subclass의 constructor는 자기 class 이름을 쓰며, 필요한 부모 초기화를 `super(...)`로 연결한다. 명시적 부모 호출이 없을 때의 `super()`도 접근 가능한 부모의 무인자 constructor가 있어야 성립한다.  [computer_programming:RM001, PDF pp.49-51](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf)

아래 constructor 문제 Q06·P02는 JDK 11을 가정한다. 그 조건에서 명시적 `this(...)` 또는 `super(...)`를 constructor의 첫 동작으로 두어 위임받은 초기화를 먼저 수행한다는 규칙을 배운다. NM004 p.19와 날짜 미확인 녹취 48:59–49:57은 Java 25에서 제한된 사전 작업을 허용한다는 별도 언급도 한다. 제공된 언급을 모든 버전의 절대 규칙으로 지우거나, 그 언급만으로 해당 버전의 상세 허용 문법을 확정해서는 안 된다. [computer_programming:NM004, PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 48:59]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 49:57]]

비공식 타 교수 복원본의 `this`/`super` 항목은 같은 객체의 초기화 위임과 부모 초기화를 구별한다는 풀이 구조로만 연결된다. Constructor가 상속된 method라는 뜻으로 읽지 않는 것이 중요하다. [EX:cp_2025_1_midterm_q05 p.3]

### 적용 가능한 overload가 여러 개일 때

상속 관계 때문에 한 인자가 여러 parameter type에 들어갈 수 있다. `ColoredPoint extends Point`이면 `ColoredPoint`는 `Point` parameter에도 전달할 수 있다. 이 유연성 때문에 signature가 다른 두 선언이 있어도 어떤 호출에는 답이 하나로 정해지지 않을 수 있다. [computer_programming:NM004, PDF pp.20-21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

~~~text
static void test(ColoredPoint p, Point q) {
    System.out.println("(ColoredPoint, Point)");
}

static void test(Point p, ColoredPoint q) {
    System.out.println("(Point, ColoredPoint)");
}
~~~

`ColoredPoint cp`에 대해 `test(cp, cp)`를 생각하자.

| 후보 | 첫 번째 인자 | 두 번째 인자 |
|---|---|---|
| `test(ColoredPoint, Point)` | 정확히 `ColoredPoint` | `Point`로 볼 수 있음 |
| `test(Point, ColoredPoint)` | `Point`로 볼 수 있음 | 정확히 `ColoredPoint` |

둘 다 적용 가능하다. 첫 후보가 첫 자리에서 더 구체적이고 둘째 후보가 둘째 자리에서 더 구체적이므로, 전체 parameter 목록에서 어느 하나가 다른 하나보다 더 구체적이지 않다. 이것이 ambiguous 호출이다. 먼저 선언된 method를 고르거나 실행 중 객체를 더 자세히 살펴보는 방식으로 해결하지 않는다.

자료 pp.22–23은 둘째 선언을 `test(ColoredPoint, ColoredPoint)`로 **교체**한다. 그러면 그 후보는 첫 자리에서 첫 후보와 같고 둘째 자리에서는 더 구체적이다. 같은 `test(cp, cp)`에 대해 이 most-specific 후보가 선택되어 `(ColoredPoint, ColoredPoint)`를 출력한다. 날짜 미확인 녹취 52:44의 먼저 맞는다는 표현은 선언 순서가 아니라 이 type 관계를 설명하는 축약으로 읽어야 한다. [computer_programming:NM004, PDF pp.22-23](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 52:44]]

`null`도 reference parameter들 사이의 선택을 생각하게 한다. `null`은 여러 reference type에 전달할 수 있지만, 서로 무관한 두 parameter type 사이에 항상 우열이 생기는 것은 아니다. 반대로 cast로 인자 expression의 type을 명시하면 적용 가능한 후보가 달라질 수 있다. 이때 cast는 `null` 객체의 실제 class를 바꾸는 일이 아니다. 비공식 타 교수 복원본은 이런 적용 가능성과 most-specific 판단을 함께 요구하는 보조 사례다. 전체 원문이나 개별 선택지의 답을 옮기지 않아도, “적용 가능 후보를 모은 뒤 type 관계로 하나가 결정되는가”라는 절차를 이 단원에 연결할 수 있다. [EX:cp_2026_1_final_q08 p.5]

### Generic이 필요한 이유: 반복되는 구조에 type 이름 붙이기

Overloading은 `move(int, int)`와 `move(float, float)`처럼 입력 형태를 구별할 때 유용하다. 그러나 원소 type만 바꾸어 같은 list 구조와 연산을 계속 복사해야 한다면 overload를 하나씩 추가하는 것만으로는 공통 구조를 잘 표현하지 못한다. Generic(제네릭)은 이런 반복에서 method·class·interface에 type variable을 두어 여러 type에 적용하는 방식이다. 자료는 이를 parametric polymorphism이라고 부른다. 같은 구조의 재사용이 그 도입 동기다. 앞서 배운 [Object 계약과 interface의 List 기반](object-contracts-interfaces.md)에서 `List<E>`라는 계약과 그 일부 공통 구현을 제공하는 `AbstractList<E>`를 보았다. 같은 `E`는 그 구조 안에서 같은 원소 type의 자리를 연결하는 **이름 있는 type parameter**다. [computer_programming:NM001, PDF pp.55-56](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) [computer_programming:NM004, PDF p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) [computer_programming:NM004, PDF p.59](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf)

`List<Integer>`와 `List<String>`은 같은 list 계약을 각각 다른 원소 type에 사용하는 예다. `Integer`와 `String`은 구체적인 type arguments이고 `E`는 선언에서 이름 붙인 자리다. 이 자리에는 여기의 예처럼 reference type을 쓰므로 primitive `int`를 그대로 넣은 `List<int>`로 바꾸지 않는다. 어떤 원소가 허용되는지를 type 단계에서 드러내면 단순히 `Object`에 여러 값을 담고 사용할 때마다 기대하는 type으로 cast하는 부담을 줄일 수 있다. 이는 프로그램의 모든 오류를 없앤다는 보장은 아니다. NM005 pp.7–8은 자료에 있는 설명이며 해당 부분의 모든 예가 새로 구두 설명되었다는 뜻은 아니다. [computer_programming:NM005, PDF pp.7-8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf)

`?`는 이와 다른 wildcard(와일드카드), 즉 이름을 붙이지 않은 미지의 type을 나타낸다. `List<?>`를 `List<E>`와 같은 “아무 type이나 넣어도 되는 상자”로 읽으면 안 된다. 미지의 원소 type을 호출자가 임의로 정해 새 값을 넣을 수 있다는 보장이 없고, 이름 있는 `E`처럼 여러 위치의 동일한 type 관계를 표현한 것도 아니다. [computer_programming:NM004, PDF p.66](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) 앞의 `Collection<?>`를 순회하며 `Object`와 비교한 예는 관찰과 비교를 보여 줄 뿐 임의 삽입을 정당화하지 않는다. 또한 이 동기만으로 `List<Subtype>`을 `List<Supertype>`으로 자유롭게 바꿀 수 있다는 결론도 나오지 않는다.

날짜 미확인 녹취 16:41은 `E`를 wildcard라고 부른다. 01:25:47의 `[[unclear: can take arbitrary type during runtime]]`은 type placeholder가 임의의 type을 취하는 시점에 관한 불명확한 표현이다. 이는 자료의 compile-time typing 설명과 구별한다. 이름 있는 parameter `E`와 `?`를 구별하고, 자료의 type parameter 설명에 따라 type 검사에서 드러낼 수 있는 관계를 배운다. 발화를 그런 문장으로 수정한 인용은 아니다. 여기서 다루는 것은 재사용의 동기와 표기의 첫 구분까지다. 상세 generic class·method·constructor 구현, bounds와 ProducerConsumer는 이후의 자료 기반 주제이며 이 설명으로 완료되지 않는다. [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 16:41]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:25:47]] [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 / date unconfirmed · 01:26:45]]

**개념 확인.** (a) 원소 type만 다른 list 구현을 반복하는 문제에 왜 overload 목록보다 type parameter가 도움이 되는가? (b) `List<E>`의 `E`, `List<Integer>`의 `Integer`, `List<?>`의 `?`는 각각 무엇인가? (c) 이 설명만으로 임의 삽입과 `List<Subtype>`에서 `List<Supertype>`으로의 변환을 보장할 수 있는가?

**풀이.** (a) 공통 연산과 저장 구조를 유지하면서 변하는 type에 이름을 붙여 여러 위치의 관계를 재사용할 수 있기 때문이다. 입력 형태마다 별도 method를 추가하는 overload와 해결하는 반복의 수준이 다르다. (b) `E`는 선언에서 관계를 잇는 이름 있는 parameter, `Integer`는 그 자리에 넣는 구체적인 reference type argument, `?`는 이름 없는 미지의 type이다. (c) 미지의 type을 마음대로 정할 수 없고 parameterized type 사이의 상속 관계도 따로 확인해야 한다. 따라서 두 보장은 이 동기에서 따라오지 않으며, 상세한 허용 연산과 generic 관계는 뒤의 학습이 필요하다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Signature와 의미상 같은 행동

선언 `int add(int a,int b)`, `double add(int x,int y)`, `int add(int x,int y,int z)`, `float add(float a,float b)` 중 공존할 수 없는 쌍과 이유를 설명하라. Parameter 이름 변경은 새 overload인가? `Fish.swim()`과 `Animal.move()`는 overriding 관계인가?

<details><summary>해설 보기</summary>

앞 두 선언은 둘 다 `add(int,int)`여서 반환형만으로 공존할 수 없다. 세 int와 두 float 형태는 개수 또는 type 목록이 달라 별도 overload다. 이 non-generic 범위에서 signature는 이름과 순서 있는 parameter types로 비교하며 변수 이름과 반환형은 구별 기준이 아니다. Caller가 `add(1,2)`로 주는 이름·입력이 같으므로 반환 결과에 기대어 둘을 나눌 수 없다.

Overloading은 다른 signature를 추가하고 overriding은 상속된 같은 instance signature의 구현을 바꾼다. `swim`과 `move`는 이름이 달라 비슷한 의미만으로 override가 아니다. 같은 목적의 이름을 공유하면 여러 `printInt`류 이름을 외울 부담을 줄일 수 있지만 문법적 식별 조건과 설계 동기는 별개다.

**확인 기준:** 같은 signature 쌍, 다른 두 형태, parameter 이름·return type 제외, swim/move를 모두 판별한다.

</details>

#### 확인 Q02 · Point 이동과 abs_add 재사용

`float` fields가 0인 Point에서 `move(int,int)`와 `move(float,float)`가 각각 dx,dy를 더한다. `move(3,0)`와 `move(0.0f,4.0f)`를 추적하라. 또한 scalar `abs_add(a,b)=|a|+|b|`를 배열 body가 sum=0부터 `sum=abs_add(sum,arr[i])`로 호출한다. 1.0–10.0과 {-2.0,3.0,-4.0}의 계산 및 재사용의 의미를 설명하라.

<details><summary>해설 보기</summary>

첫 호출은 int/int overload라 (3.0,0.0), 둘째는 `f` 접미사의 float/float overload라 (3.0,4.0)이다. 같은 좌표 이동을 input type별로 제공한다.

배열 계산은 보통의 유한 입력과 표현 범위 안에서 누적 sum이 음수가 아니므로 `|sum|+|next|=sum+|next|`다. 1부터10은 10×11/2=55.0이다. 작은 배열은 0.0→2.0→5.0→9.0으로 추적한다. Scalar와 배열은 input shape가 달라도 밀접한 계산이다. 배열 body가 scalar body를 호출하여 핵심 계산을 재사용하는 것이지 extends 상속이 아니다. Scalar 의미를 바꾸면 배열 의미도 다시 확인해야 한다. 중복 유지 부담을 줄이는 이점이 있으며 매 호출이 반드시 비싸다는 측정 결론은 없다. NaN·infinity·overflow의 전체 수치 계약은 제공되지 않았다.

**확인 기준:** 선택 type 두 개, 좌표 두 단계, 55와 2/5/9 및 호출에 의한 재사용을 확인한다.

</details>

#### 확인 Q03 · indexOf의 추가 정보

자료 DNA에서 `CGC`의 첫 시작 index는 12, 길이는 3, 그 뒤 다음 시작은 32다. `indexOf("CGC", first + "CGC".length())`는 어느 위치부터 검색하는가? 시작값을 first로 바꾸면? 왜 ‘두 번째 일치 번호’를 주는 것이 아니며, 미발견·겹침에는 어떤 한계가 있는가?

<details><summary>해설 보기</summary>

시작 index는 12+3=15이며 그 이후 첫 일치가 32다. 시작값 12를 다시 주면 첫 CGC가 아직 범위에 있어 12를 재발견한다. 두 번째 parameter는 zero-based 검색 시작 위치이지 2번째를 지정하는 순번이 아니다. 같은 검색 이름에 추가 정보를 보태는 overload의 예다.

이는 첫 검색이 성공한 전제이며 first=-1의 처리 조건은 없다. 전체 길이만큼 건너뛰므로 이전 일치 안에서 시작하는 겹침을 모두 열거하는 방식도 아니다.

**확인 기준:** 15→32와 재검색12의 이유를 설명하며 미발견과 겹침 한계를 둘 다 적는다.

</details>

#### 확인 Q04 · 기본값을 주는 wrapper와 debug 대안

`power(input,n)`은 n<=0이면 1, 아니면 input×power(input,n-1)이고 `power(input)`은 n=2로 위임한다. `power(2)`, `power(2,10)`, `power(2,-1)`을 구하라. 기본 debug()가 `var 1 : 0`을 출력할 때 `debug(s)`의 복사 대안은 `s+"var 1 : "+var1`, 위임 대안은 `print("Output : "+s); debug();`다. s=`"state: "`의 출력과 설계 차이를 설명하라.

<details><summary>해설 보기</summary>

`power(2)`는 `power(2,2)`→2×power(2,1)→2×2×power(2,0)이라 4.0이다. `power(2,10)`은 2 열 개의 곱으로 1024.0, `power(2,-1)`은 첫 n<=0에서 1.0이다. 반환형이 double이므로 base case의 1도 그 type으로 반환한다. 음수 지수의 역수 함수가 아니다.

복사 대안은 `state: var 1 : 0`, 위임 대안은 `Output : state: var 1 : 0`이다. Prefix가 달라 완전히 같은 문자열은 아니다. 위임 대안은 기본 debug의 field 출력 형식을 고칠 때 그 변경을 따른다. 두 debug(String) body는 같은 signature의 선택 대안이므로 둘 다 동시에 선언하지 않는다. 핵심 body로 일을 모으는 것은 이 예의 유지보수 원칙이지 모든 overload의 문법상 강제가 아니다.

**확인 기준:** 세 수치 결과, negative base case, 두 정확한 출력과 위임의 변경 전파를 확인한다.

</details>

#### 확인 Q05 · 가능한 overload와 예측 가능한 API

서로 독립된 p.17 Point 예의 fields는 double이다. Point()는 원점, Point(int,int)/Point(float,float)는 Cartesian, Point(double radius,double theta)는 polar 변환이다. 네 경로와 radius=2,theta=0을 설명하고 `new Point(2.0f,0.0f)`와 `new Point(2.0,0.0)`의 의미 차이가 왜 위험한지 논하라.

<details><summary>해설 보기</summary>

무인자는 (0,0), int/int와 float/float는 주어진 x,y를 저장한다. `double`/`double`은 x=r cos(theta), y=r sin(theta)라 수학적으로 r=2,theta=0이면 (2,0)이다. 두 호출은 이 값에서는 같은 좌표가 될 수 있어도 전자는 직교좌표, 후자는 극좌표라는 서로 다른 해석이다.

정밀도만 바꾼다고 생각한 caller가 입력 의미까지 바꿀 수 있어 혼란스럽다. 서로 다른 signature로 구별 가능하다는 것과 좋은 API인지는 별개다. 좌표계 indicator처럼 의도를 명시하는 구별은 제안이지만 새 필수 constructor 구현은 제공되지 않았다. 원본 `import Math;`도 유효한 전체 프로그램의 근거가 아니며 이 예를 다음 쪽의 다른 constructor 목록과 합치지 않는다.

**확인 기준:** 네 초기화 경로·변환식·의미 변경을 설명하고 두 Point 정의를 섞지 않는다.

</details>

#### 확인 Q06 · this와 super의 한 객체 초기화

별도 p.18 예는 Point(float,float)가 fields를 대입하고, Point(int,int)가 `this((float)x,(float)y)`, Point()가 `this(0,0)`을 사용한다. 한 객체의 경로를 추적하라. 0/0.0/0.0f는 같은 선택인가? `this(...)`와 `super(...)`, 암시적 super()의 조건, constructor 첫 동작 규칙의 version 범위를 설명하라.

<details><summary>해설 보기</summary>

`Point()`→`Point(int,int)`→`Point(float,float)`다. 두 0은 int라 중간 경로를 고르고, 그 body가 float로 cast한 뒤 공통 대입에 위임한다. 안쪽 초기화가 끝난 뒤 바깥으로 돌아오며 객체 세 개가 생기지 않는다. `this(0.0f,0.0f)`는 float 경로에 직접 맞지만 접미사 없는 `this(0.0,0.0)`은 double이라 이 int/float 목록에 그대로 맞지 않는다. 앞 p.17의 double constructor를 가져와 해결하면 다른 예를 섞는 것이다.

`this(...)`는 같은 class의 다른 constructor, `super(...)`는 직접 superclass의 constructor로 초기화를 잇는다. 암시적 super()도 접근 가능한 부모의 무인자 constructor가 있어야 한다. Constructor는 상속·override하지 않는다. 여기서는 JDK 11 문맥을 가정하여 명시적 this/super 첫 동작 규칙을 적용한다. 자료 p.19는 Java 25의 제한된 선행 작업도 별도로 언급하므로 모든 버전의 절대 규칙이나 상세 허용 구문으로 확대하지 않는다.

**확인 기준:** 각 argument type·단일 객체·접근 가능성·version 한정을 설명한다.

</details>

#### 확인 Q07 · 두 자리의 most-specific 판단

ColoredPoint extends Point다. `test(ColoredPoint,Point)`와 `test(Point,ColoredPoint)`에 ColoredPoint cp를 두 번 전달하면 왜 모호한가? 둘째 선언을 `test(ColoredPoint,ColoredPoint)`로 교체하면? 선언 순서나 runtime receiver로 해결할 수 있는가?

<details><summary>해설 보기</summary>

처음에는 cp가 Point에도 들어가 두 후보 모두 적용 가능하다. 첫 후보는 첫 자리에서 더 구체적이고 둘째는 둘째 자리에서 더 구체적이므로 전체 목록에서 유일한 most-specific 후보가 없다. 이것은 overload 선택 단계의 ambiguous 호출이다.

교체 후 (ColoredPoint,ColoredPoint)는 첫 후보와 첫 자리가 같고 둘째 자리가 더 구체적이어서 선택된다. 그 body는 `(ColoredPoint, ColoredPoint)`를 출력한다. 다른 signature가 있다는 것만으로 모든 호출이 유일해지는 것은 아니다. 선언 순서대로 먼저 고르거나 runtime에 overload 선택을 미루는 방법이 아니다. `null`/cast도 먼저 적용 가능 후보와 expression type을 따져야 한다.

**확인 기준:** 교체 전후 각 자리의 type 관계로 판정하고 선언 순서 규칙을 사용하지 않는다.

</details>

### 연습

#### 연습 P01 · 두 자리 후보와 cast

새로 작성한 synthetic practice다. [EX:cp_2026_1_final_q08 p.5]에서 reference overload의 적용 가능성·null·cast 판단만 옮긴다. Shape의 서로 다른 subclasses Circle/Square, overload와 upcast가 선수 조건이다.

후보는 `choose(Shape,Shape)`, `choose(Circle,Shape)`, `choose(Shape,Square)`다. Circle c와 Square s는 non-null이다. (a) choose(c,s), (b) choose((Shape)c,s), (c) choose(null,null)의 선택을 설명하라. (d) `choose(Circle,Square)`를 추가하면 a,c에 무엇이 달라지는가? Body는 값을 읽지 않고 선택된 signature를 표시한다고 가정한다.

<details><summary>해설 보기</summary>

(a)는 세 후보가 적용 가능하지만 Circle/Shape와 Shape/Square가 서로 다른 자리에서 더 구체적이라 모호하다. Shape/Shape보다 둘이 구체적이라는 사실만으로 두 후보 사이 우열은 생기지 않는다.

(b)는 첫 expression의 type이 Shape라 Circle/Shape가 제외된다. 남은 Shape/Square가 Shape/Shape보다 둘째 자리에서 구체적이므로 선택된다. 실제 c 객체는 그대로다. (c)의 null 둘은 모든 reference 목록에 적용되지만 같은 교차 우열이 남아 모호하다.

(d)의 Circle/Square는 두 교차 후보 각각보다 한 자리에서 같고 다른 자리에서 더 구체적이다. 따라서 a,c 모두 새 후보를 선택한다. `null` 자체가 실제 Circle이나 Square 객체로 변한 것은 아니며, 여기서는 body가 역참조하지 않는다는 조건도 중요하다.

**확인 기준:** 각 호출의 후보 포함/제외와 두 자리 우열을 설명한다. Cast·null을 객체 변환으로 읽지 않는다.

</details>

#### 연습 P02 · 초기화 위임의 회귀 점검

새로 작성한 lecture-based general practice다. 색인의 this/super 개념 문항만으로 이 변경 점검의 직접 출제 형식을 확인할 수는 없다. JDK 11 초기화 문맥을 가정한다.

p.18과 같은 int→float constructor 위임에서 공통 float body에 가상 검사를 한 번 추가하려 한다. 기본 경로가 `this(0,0)`인 경우와 이를 `this(0.0f,0.0f)`로 바꾼 경우의 경로 및 검사 횟수를 비교하라. `this(0.0,0.0)`로 바꾸면 왜 안 되는가? 공통 body 재사용과 부모의 접근 가능한 constructor 조건도 연결하라.

<details><summary>해설 보기</summary>

첫 경로는 무인자→int/int→float/float, 둘째는 무인자→float/float다. 각 경우 한 객체의 공통 float body에 한 번 도달하므로 검사도 한 번이다. 여러 constructor를 거친다고 객체나 검사가 자동으로 여러 개가 되지 않는다. 공통 대입/검사를 한곳에 두면 두 경로가 같은 변경을 따른다.

접미사 없는 0.0은 double이고 이 목록에는 double/double constructor가 없어 그대로 int/float로 전달할 수 없다. 기본값만 바꾼 것처럼 보여도 literal type을 확인해야 한다. `this(...)`는 같은 class의 위임이므로 superclass 초기화를 대체하거나 접근 권한을 없애지 않는다. 실제 초기화 경로에서 필요한 접근 가능한 부모 constructor가 있어야 하며 암시적 super()도 예외가 아니다. 가상 검사 위치는 이 JDK 11 문맥의 위임 뒤에 두는 것으로 읽는다.

**확인 기준:** 두 경로·검사1회·double literal·부모 접근 조건을 빠뜨리지 않는다.

</details>

### Generic 도입 보충

#### 확인 Q08 · Generic의 재사용 동기

(a) 원소 type만 다른 list 구현을 계속 복사할 때 overload 추가와 type parameter는 어떤 반복을 해결하는가? (b) `List<E>`, `List<Integer>`, `List<String>`, `List<?>`에서 E·Integer/String·?를 구별하라. (c) Object 저장 후 cast와 비교한 이점 및 임의 삽입·상속 변환·모든 오류 제거에 대한 한계를 설명하라.

<details><summary>해설 보기</summary>

Overload는 서로 다른 입력 형태의 관련 동작을 같은 이름으로 제공한다. Generic은 반복되는 같은 구조에서 바뀌는 type에 이름을 붙여 여러 위치의 관계를 함께 재사용한다. List 계약→AbstractList의 공통 구현→ArrayList라는 기반 위에서 원소 type마다 구조를 복사하는 부담을 줄이는 동기다.

E는 선언의 이름 있는 type parameter이고 Integer와 String은 구체 reference type arguments다. Integer는 primitive int가 아니므로 `List<int>`로 바꾸지 않는다. ?는 이름 없는 미지 type이며 E처럼 다른 위치의 같은 type을 이름으로 연결한 표기가 아니다.

원소 type을 드러내면 Object로 저장하고 매번 기대 type으로 cast하는 부담을 줄일 수 있다. 하지만 caller가 List<?>의 미지 type을 임의로 골라 값을 넣을 수 있다는 보장은 없고 `List<Subtype>`→`List<Supertype>`의 자유로운 변환도 여기서 따라오지 않는다. 모든 프로그램 오류를 없애지도 않는다. 이 답은 재사용 동기와 표기 구별까지이며 상세 generic class/method/constructor·bounds와 ProducerConsumer는 후속 자료 주제로 남는다.

**확인 기준:** 재사용·E/argument/?·세 가지 비보장을 모두 설명한다. 상세 generic 구현을 덧붙이지 않는다.

</details>

## 출처

### 강의 노트와 전사

- [[courses/computer_programming/lectures/undated-inheritance-polymorphism-vemyed7m83v2ejw2|날짜 미확인 · Object 계약·polymorphism·generic 도입]]
- [[courses/computer_programming/lectures/2026-09-01-lecture-01|2026-09-01 · literal type·변환의 기초]]
- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · 배열·순회 선수 내용]]
- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · 객체·constructor·static·reference 선수 내용]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · 객체·초기화·reference 복습]]

날짜가 있는 노트는 해당 선수 내용을 다시 찾기 위한 링크다. Inheritance·dispatch의 상세를 그 날짜에 모두 다뤘다는 뜻은 아니다.

- [[courses/computer_programming/transcripts/undated-inheritance-polymorphism-vemyed7m83v2ejw2|NT001 · 날짜 미확인 전사]] — 26:53, 27:51, 33:13, 34:41, 35:41, 36:41, 41:23, 44:12, 46:08, 48:59, 49:57, 50:55, 52:44, 16:41, 01:25:47, 01:26:45.

### 자료와 원본 쪽

쪽수는 물리 PDF 기준이다. 각 쪽 링크에서 원본 페이지를 함께 볼 수 있다.

- [8 polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf) — [4쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-004), [5쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-005), [6쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-006), [7쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-007), [8쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-008), [11쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-011), [12쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-012), [13쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-013), [14쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-014), [15쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-015), [16쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-016), [17쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-017), [18쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-018), [19쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-019), [20쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-020), [21쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-021), [22쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-022), [23쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-023), [52쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-052), [59쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-059), [66쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/8.polymorphism/page-066).
- [Lab 6 Polymorphism.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf) — [1쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-001), [3쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-003), [5쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-005), [7쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-007), [8쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-008), [19쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab.6.polymorphism/page-019).
- [6 inheritance 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf) — [49쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-049), [50쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-050), [51쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/6.inheritance.1/page-051).
- [7 inheritance 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf) — [55쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-055), [56쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/7.inheritance.2/page-056).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [40쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-040), [41쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-041), [42쪽](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042).

### 범위와 불확실성

NT001은 날짜 미확인 전사다. 95개 발화에 남은 124개 문자 그대로의 불확실성 표시와 76개 추가 한계를 유지하며, 불명확한 말·부정·누락을 자료 문장으로 복원하지 않는다. 인쇄 예제는 자료 근거이며 모두 새로 말한 예제라는 뜻이 아니다. 아래 시간은 전사에서 찾을 위치이며 별도 시간 앵커를 뜻하지 않는다.

NM005는 물리 PDF 36쪽이다. 등록명은 Lab 6이지만 표지는 Lab 1이고, TODO와 19쪽의 제공되지 않은 ZIP이 남아 있다. 여기서는 개념 자료로만 사용하며 완성된 채점 대상 구현이나 해당 실습의 출석·제출 규칙을 가져오지 않는다.

NM004 7쪽의 signature 표기에 return type이 보이더라도 이 범위의 overload 구별에 return type을 넣지 않는다. NT001의 CCT·offset·radius/radians·0.0 등 불확실한 말은 CGC, +length, 인쇄 식별자와 별개다. 17쪽의 Cartesian/polar Point와 18쪽의 this 위임 Point는 다른 예다. 원본 import Math;도 완성 코드로 간주하지 않는다. 함수 호출 비용·재귀 한계의 측정 근거는 없다.

Q06·P02는 여기서 한정한 JDK 11 초기화 문맥을 가정하며, NM004 19쪽의 첫 동작 규칙과 별도 Java 25 언급을 구별한다. 이후 버전의 상세 사양을 확인했다는 뜻은 아니다. Generic 보충은 재사용 동기, 이름 있는 E와 ? 및 비보장만 다룬다. 상세 generic class/method/constructor·bounds와 ProducerConsumer는 후속 자료 주제로 남는다.

### 비공식 복기와의 제한된 연결

복기 자료는 비공식이며 검증된 공식 정답은 제공되지 않았다. 파일명에만 연결된 2025년 봄 중간 김상한, 2026년 봄 기말 유영재는 현재 유재민(Jaemin Yoo) 교수와 다르다. 연결은 아래 개념·풀이 구조에 한정하며 현재 수업의 출제 형식·범위·빈도·확률을 뜻하지 않는다. 신규 문항은 일반 또는 합성 연습이다.

- [EX:cp_2026_1_final_q01a p.1] — Non-generic method의 이름·순서 있는 parameter types를 비교한다. Parameter 이름·return type과 구별하며 상세 generic signature 규칙은 제외한다.
- [EX:cp_2025_1_midterm_q05 p.3] — Object·상속을 전제로 this(...)와 super(...)의 개념만 연결한다. 원문 문항 전체를 constructor 연습으로 분류하지 않는다.
- [EX:cp_2026_1_final_q08 p.5] — Reference overload의 적용 가능성과 유일한 most-specific 선택을 null·cast로 나누는 구조를 P01에 연결한다. 상속·reference type·Q07이 선수 내용이며 원래 선택지별 답은 제시하지 않는다. [[exam_questions/cp_2026_1_final_q08|기존 문항 미리보기]]

Point 이동·abs_add·DNA 검색·power/debug·극좌표 설계·완전한 constructor 위임 추적에는 직접 대응하는 색인 문항이 없다. P02는 일반 변경 점검이며 generic 구현·bounds 문항은 보충 범위를 넘는다.
