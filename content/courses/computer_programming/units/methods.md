---
title: "Method의 계약·호출·반환과 재사용"
description: "평균 계산의 재사용, method 계약·signature와 호출·반환 흐름을 복습한다."
course: "computer_programming"
unit_id: "methods"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["3 java basics 2.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-08-lecture-03"]
---

Method declaration을 입력과 결과의 계약으로 읽고 caller부터 반환값 사용까지 추적한다. 같은 계산을 재사용하는 이유를 설명하면서 출력·반환·cast의 역할을 분리해 보자.

## Method로 계산의 책임 나누기

[[courses/computer_programming/units/arrays|Array]]와 [[courses/computer_programming/units/control-flow|Loop]]를 사용해 평균을 구할 수 있어도, 같은 코드를 여러 번 복사하면 수정할 곳도 늘어난다. Function(함수)은 입력을 받아 의미 있는 작업을 수행하는 호출 가능한 block이며, Java에서는 method(메서드)라고 부른다. Modularity(모듈성)는 작은 코드에 분명한 책임을 부여해 관리·검사를 쉽게 하는 것이고, reusability(재사용성)는 그 책임을 다시 호출하는 것이다.

M006 p.43의 그림에서 사과는 function `h`를 통과해 잘린 사과가 된다. 입력, 처리, 출력이라는 세 부분을 나누어 보면, caller가 맡은 입력 준비와 method가 맡은 계산을 구별할 수 있다.

[Computer Programming M006, PDF pp.44–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf)는 세 arrays를 한 declaration에 쓴다.

```java
double[] arr1 = {1.2, 3.4, 2.5, 6.4},
         arr2 = {5.2, 6.7, 8.2, 3.6},
         arr3 = {0.2, 3.4, 4.5, 4.2};
```

앞의 `double[]` type은 comma로 나눈 세 declarators(선언 항목)에 모두 적용된다. 각각 자기 initializer로 만든 별도 array를 가리키며, 마지막 semicolon이 하나의 declaration을 끝낸다. Comma가 세 arrays를 하나의 2D array로 묶는 것은 아니다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:28:34는 이 문법을 설명한 뒤 읽기 좋은 style은 아니라고 평한다. 이는 가독성에 관한 판단이며 문법 오류라는 뜻은 아니다.

### 평균 계산을 한 번 정의하기

원래 반복 코드에서는 array가 바뀔 때마다 `sum = 0`을 다시 하고, 원소를 누적한 뒤 길이로 나눈다. 이를 M006 p.46처럼 하나의 method에 모으면 매 호출에서 새로운 local sum으로 시작한다.

```java
static double average(double[] arr) {
    double sum = 0;
    for (double f : arr) {
        sum += f;
    }
    return sum / arr.length;
}
```

이는 class 내부에 둘 method 정의다. Caller(호출자)가 `average(arr1)`을 부르면 arr1의 reference 값이 parameter(매개변수) `arr`에 전달되고 method는 계산 결과를 반환한다. `System.out.println(average(arr1));`은 반환된 값을 caller가 출력하는 별도 단계다.

| 입력 array | 수학적 합 | 합 ÷ 길이 |
| --- | ---: | ---: |
| `arr1` | 13.5 | 3.375 |
| `arr2` | 23.7 | 5.925 |
| `arr3` | 12.3 | 3.075 |

모두 길이가 4다. 표는 수학적 계산이며 실제 floating-point 표현에는 미세한 오차가 있을 수 있다. Null·empty 입력에 대한 검증은 이 원본 method에 없다. 따라서 제공된 non-null, nonempty arrays에 대한 설명을 모든 입력에서의 안전성 보장으로 확대하지 않는다.

[[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:30:30–01:33:21의 강조는 임의의 문장 묶음보다 `average`·`sum`처럼 작업의 뜻이 드러나는 이름을 쓰는 것이다. 이 시점에 설명을 미룬 `static`의 의미는 [[courses/computer_programming/units/objects-references|Class 소속과 instance 소속]]에서 이어진다.

## Declaration을 입력·결과의 계약으로 읽기

Method declaration(메서드 선언)은 사용자가 어떤 입력과 결과를 기대해야 하는지 보여 준다.

```java
public static int intPlusFloat(int i, float f) {
    return i + (int) f;
}
```

M006 p.49에서 `public`은 접근, `static`은 class 소속, `int`는 return type(반환형), `intPlusFloat`는 이름이다. 괄호 안에는 `int i`와 `float f`라는 parameter type과 이름이 있다. 이름만 보고 “소수 부분까지 보존한 합”이라고 판단할 수는 없다.

Return expression(반환식)은 `f`를 먼저 `int`로 cast한 뒤 정수 덧셈을 한다. 설명용 입력 `i = 2, f = 3.7f`라면 cast된 3에 2를 더해 5를 반환한다. `5.7`을 반환하지 않는다. Cast는 `f`의 선언 type을 바꾸지 않고, 해당 값이 계산에 들어가는 형태를 바꾼다. 이 결과는 [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:34:19의 선언·body 연결을 풀어 쓴 계산이다.

### Parameter와 return의 네 조합

| 원본 method | 입력 | Caller가 받는 값 | 관찰되는 동작 |
| --- | --- | --- | --- |
| `add(int i, int j)` | 두 `int` | `int` 합 | 합을 반환 |
| `printInt(int i)` | 한 `int` | 없음, `void` | 입력값을 출력 |
| `getSpecialValue()` | 없음 | `int` 값 777 | 정해진 값을 반환 |
| `printMyName()` | 없음 | 없음, `void` | 정해진 문자열을 출력 |

마지막 예의 개인 이름 literal은 기능을 이해하는 데 필요하지 않다. 중요한 차이는 **출력과 반환이 서로 다른 전달 경로**라는 점이다. `void`라고 해서 관찰 가능한 행동이 없는 것은 아니다. M006 pp.50–51 및 [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:35:20은 이 네 형태를 나눈다.

`return`은 현재 method 실행을 끝낸다. 값을 반환하며 정상 종료하는 경로에는 선언된 type에 맞는 값이 필요하다. `void` method는 끝에 도달해 종료하거나 `return;`으로 값 없이 먼저 종료할 수 있다. 입문 설명의 “항상 return이 있어야 한다”를 무한 반복·비정상 종료를 포함한 모든 control flow의 완전한 규칙으로 해석하지 않는다.

선택적 기출 보충에서는 declaration 전체와 method signature(메서드 시그니처)를 구별하는 깊이가 요구된다. 현재 다루는 non-generic methods의 signature는 이름과 **순서 있는 parameter types**로 읽는다. `intPlusFloat(int, float)`에서 parameter 이름 `i`·`f`나 호출할 때 넣은 실제 값은 signature가 아니며, return type `int`도 signature에 포함되지 않는다. 그렇다고 return type이 계약에서 중요하지 않은 것은 아니다. 2026-1 복기에는 문항 순서·정확성의 한계가 있고 공식 답안은 없으므로, 이 연결을 강의 중 출제 예고나 전체 시험의 확정 정보로 사용하지 않는다. [EX:cp_2026_1_final_q01a p.1]

## Arguments에서 반환값까지 따라가기

Argument(인수)는 호출할 때 제공하는 값이고 parameter는 method 안에서 그 값을 받는 변수다. M006 p.52의 예는 반환된 값을 저장한 뒤 출력하는 흐름을 보여 준다.

```java
class Main {
    static float interpolate(float x1, float x2, float r1, float r2) {
        return (r2 * x1 + r1 * x2) / (r1 + r2);
    }

    public static void main(String[] args) {
        float intrp = interpolate(0f, 3f, 1.5f, 2.5f);
        System.out.println(intrp);
    }
}
```

Argument를 순서대로 대응시키면 `x1 = 0f`, `x2 = 3f`, `r1 = 1.5f`, `r2 = 2.5f`다. 식은 (2.5×0 + 1.5×3)/(1.5+2.5)=4.5/4=1.125가 된다. 반환된 `float`가 `intrp`에 저장되고 출력된다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:38:59에서 interpolation 수식의 의미·유도는 건너뛰었으므로 이 계산은 **자료 기반 산술 추적**이다. 분모가 0인 경우까지 정상 입력으로 정의한 계약은 아니다.

### Declaration 순서와 호출 순서

M006 p.53에서 `first()`는 아래에 선언된 `second()`를 부르고, `second()`는 `third()`를 부른다.

```java
class Main {
    void first() { second(); }
    void second() { third(); }
    void third() { System.out.println("third"); }
}
```

이 class만 선언했다고 자동으로 출력하지는 않는다. 적절한 객체에서 `first()`가 호출되면 first → second → third 순으로 진행하여 `third`를 출력하고 호출한 곳들로 돌아간다. 같은 class의 method 선언 위치가 아래라는 이유로 호출할 수 없는 것은 아니다. 강의의 “nested” 표현도 이런 호출 관계를 뜻하며, method body 안에 또 다른 method를 선언한다는 Java 문법을 의미하지 않는다.

## 핵심 정리

- 하나의 declaration에 여러 declarators가 있어도 각 array는 별도다.
- Method는 의미 있는 책임을 재사용하게 하며 caller는 반환값을 출력하거나 다른 계산에 쓸 수 있다.
- Return type은 계약에 중요하지만 현재 non-generic signature에는 이름과 순서 있는 parameter types가 들어간다.
- Cast 위치와 실제 호출 관계를 읽어야 하며 선언 위치가 실행 순서는 아니다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 세 arrays와 재사용

`double[] arr1={1.2,3.4,2.5,6.4}, arr2={5.2,6.7,8.2,3.6}, arr3={0.2,3.4,4.5,4.2};`의 type·comma·semicolon과 실제 arrays를 설명하라. 평균 계산을 method로 옮기면 무엇이 좋아지는가?

<details><summary>해설 보기</summary>

앞의 double[]가 세 declarators 모두에 적용되고 comma는 각 이름/initializer를 구분하며 마지막 semicolon이 한 선언을 끝낸다. 각 변수는 자기 별도 array를 가리켜 2D array가 아니다. 이 압축 style을 덜 읽기 좋다고 한 것은 문법 금지가 아니다. Average 책임을 한 method로 묶으면 반복된 body를 한 곳에서 수정·검사하고 여러 입력에 호출할 수 있다. Modularity는 의미 있는 책임 분리, reusability는 그 책임의 재호출이다.

**확인 기준:** 수정된 핵심인 여러 declarators의 의미와 재사용 이유를 모두 설명한다.

</details>

#### 확인 Q02 · 평균 반환과 caller 출력

Q01의 각 array에서 sum=0부터 누적하고 `return sum/arr.length;`한다. 합과 수학적 평균을 구하고, 매 호출 초기화·출력 주체·입력 한계를 설명하라.

<details><summary>해설 보기</summary>

합은13.5,23.7,12.3이고 각각4로 나누면3.375,5.925,3.075다. Local sum은 매 호출 새로0에서 시작하므로 이전 array 합이 섞이지 않는다. Method는 값을 반환하고 caller의 println이 출력하므로 반환값을 다른 계산에도 쓸 수 있다. 실제 floating-point에는 미세 오차가 가능하다. 제공 예는 non-null·nonempty이고 그 밖의 입력을 검사하는 계약은 없다.

**확인 기준:** 세 합/평균·매 호출 reset·반환/출력·입력 전제를 확인한다.

</details>

#### 확인 Q03 · 입력·반환의 네 조합

`add(int,int)`, `printInt(int)`, `getSpecialValue()`, `printMyName()`을 입력·return type·관찰되는 동작으로 분류하라. 선언의 public/static과 return 종료도 설명하라.

<details><summary>해설 보기</summary>

`add`는 두 int를 받아 int 합 반환, printInt는 int를 받아 void로 출력, getSpecialValue는 입력 없이 int777 반환, printMyName은 입력·반환값 없이 정해진 문자열을 출력한다. `public`은 접근, static은 class 소속이다. `return`은 현재 method를 끝내고 값이 있는 반환 경로는 선언 type에 맞아야 한다. `void`는 끝에 도달하거나 return;으로 끝날 수 있으며 출력이 금지되는 것은 아니다. 무한 반복·비정상 종료까지 모든 경로에 ‘항상 값 return’이라고 확대하지 않는다.

**확인 기준:** 네 형태와 출력/반환을 모두 분리한다.

</details>

#### 확인 Q04 · Cast 위치가 바꾸는 계산

`public static int intPlusFloat(int i,float f){return i+(int)f;}`에서 i=2,f=3.7f의 결과를 구하라. 이름·return type·실제 body 중 무엇을 읽어야 하는가?

<details><summary>해설 보기</summary>

`f`를 먼저 int3으로 cast하고 i2와 정수 덧셈하여5를 반환한다. 이름만으로5.7을 기대하면 틀리며 return type int와 cast가 소수 정보를 보존하지 않는 계약을 드러낸다. `f`의 선언 type은 float 그대로이고 해당 expression 값만 변환된다.

**확인 기준:** Cast→합→반환 순서와 f의 type 유지가 맞다.

</details>

#### 확인 Q05 · Argument와 반환값의 경로

`interpolate(0f,3f,1.5f,2.5f)`가 `(r2*x1+r1*x2)/(r1+r2)`를 반환해 intrp에 저장된다. Parameter 대응·계산·저장·출력과 자료 한계를 설명하라.

<details><summary>해설 보기</summary>

순서대로 x1=0,x2=3,r1=1.5,r2=2.5다. 분자는2.5×0+1.5×3=4.5, 분모4여서 float1.125가 intrp에 저장되고 다음 println이 출력한다. Argument는 호출 입력값, parameter는 이를 받는 method의 변수다. 이 산술은 자료 기반이며 수식의 interpolation 유도는 생략되었다. 분모0까지 정상 입력이라는 계약도 없다.

**확인 기준:** 네 대응과4.5/4, 반환/저장/출력을 확인한다.

</details>

#### 확인 Q06 · 선언 순서와 호출 순서

같은 class에 first→second→third 호출이 있고 third만 `println("third")`한다. Class 선언만 했을 때와 적절한 객체에서 first를 불렀을 때를 비교하라. `second`가 아래에 선언되어 있어도 되는가?

<details><summary>해설 보기</summary>

선언만으로는 출력이 없다. `first`를 호출하면 first→second→third로 진행해 third를 한 번 출력하고 caller들로 돌아온다. 같은 class의 아래 선언 method를 부를 수 있으므로 텍스트 위치가 실행 순서가 아니다. 강의의 nested 표현도 호출 관계를 가리키며 method body 안에 method를 선언한다는 문법은 아니다.

**확인 기준:** 실제 호출 유무와 call/return 순서를 설명한다.

</details>

### 적용 연습

#### 연습 P01 · Signature와 계산 계약 비교

**새로 작성한 synthetic 기출 응용 연습.** [EX:cp_2026_1_final_q01a p.1]의 signature 구성 판별을 옮겼다. 선수는 현재 non-generic declaration·parameter·return·cast다. 복기본의 공식 답안은 없으며 overload 선택은 묻지 않는다.

서로 별도 예인 A `int blend(int i,float f){return i+(int)f;}`와 B `double blend(int count,float amount){return count+amount;}`의 signature와 계산 계약을 비교하라. A에 (2,3.7f)를 전달한 결과도 구하라.

<details><summary>해설 보기</summary>

둘의 signature는 `blend(int,float)`로 같다. Parameter 이름과 return type은 signature 구성 요소가 아니지만 계약에서는 중요하다. A는 f를 int로 자른 뒤 더해5를 반환한다. B는 cast 없는 mixed numeric 합을 double로 반환하므로 같은 계산 의미라고 할 수 없고 floating-point 근사도 고려해야 한다. 두 선언은 비교용 독립 예이지 같은 class에 동시에 넣으라는 요구가 아니다. 이름/parameter types가 같다는 사실로 body 결과까지 같다고 결론 내리면 안 된다.

**확인 기준:** 같은 signature·다른 body 계약·A의5를 모두 이유와 함께 제시한다.

</details>

### 복습 순서

Q01–Q02에서 declaration과 평균을 설명한 뒤 Q03의 네 계약을 비교한다. Q04–Q06을 추적하고 P01에서 signature가 같아도 body 의미가 달라질 수 있음을 확인한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 보정 녹음문]] — 01:30:30, 01:28:34, 01:33:21, 01:35:20, 01:34:19, 01:38:59.

### 강의자료와 해당 페이지

- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-043), [p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-044), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-048), [p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-049), [p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-050), [p.51](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-051), [p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-052), [p.53](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-053).

Average의 null·empty 검증 계약은 제공되지 않았다. Interpolation의 수학적 유도는 강의에서 생략되어 여기서는 주어진 식만 추적한다. Static 상세는 9월 8일에 유보되었고 뒤의 객체 단원에서 이어진다.

기출 연결: [EX:cp_2026_1_final_q01a p.1]의 signature 구성 판별을 P01에서 선언·body 비교로 확장한다. 복기본은 순서·정확성의 한계가 있고 공식 답안이 없다. 같은 페이지의 중복 (f), 불완전 queue 문구와 빈 (i)는 복원하지 않는다.


---

[[courses/computer_programming/units/control-flow|← 이전: Boolean 조건·분기·반복과 실행 추적]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/objects-references|다음: Objects·Constructors·Static과 Reference 전달 →]]
