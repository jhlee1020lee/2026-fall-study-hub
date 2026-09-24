---
title: "Array의 생성·참조와 다차원 데이터"
description: "Array 생성·기본값·index·ragged row와 String reference 변경을 확인한다."
course: "computer_programming"
unit_id: "arrays"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["3 java basics 2.pdf", "Lab02 v4.pdf", "Lecture 2 Java Basics 1.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-08-lecture-03", "courses/computer_programming/lectures/2026-09-10-lecture-04"]
---

Array variable, array object, component를 나누어 저장 상태를 그린다. 각 row의 길이를 따라 접근하면 다차원 배열과 String slot 변경도 같은 원리로 설명할 수 있다.

## Array의 선언과 실제 생성

같은 종류의 값을 여러 개 다룰 때 각각 다른 variable 이름을 만들면 저장과 순회가 번거롭다. Array(배열)는 같은 component type의 값들을 index(인덱스)로 선택하게 한다. [[courses/computer_programming/units/types-expressions|Type과 reference]]를 적용하면, array variable과 실제 array object도 구별할 수 있다.

```java
int[] arr = new int[4];
```

`int[]`는 variable의 type, `arr`는 이름, `new int[4]`는 길이가 4인 array를 생성하는 expression이다. 반면 local에서 `int[] arr;`만 선언하면 아직 읽을 수 있는 reference가 할당되지 않았고 array도 생성되지 않았다. Declaration(선언)과 allocation(할당)은 서로 다른 단계다. [Computer Programming M006, PDF pp.3–6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf)

생성된 array의 components는 default value(기본값)로 초기화된다. `int`는 0, `double`은 0.0, `boolean`은 `false`, reference는 `null`이다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 37:38–41:21의 값이 보장되지 않는다는 설명과는 구별해야 할 Java 규칙 보충이다. 이것을 unassigned local도 읽을 수 있다는 뜻으로 옮기면 안 된다.

### Initializer가 정하는 값과 길이

원하는 값을 처음부터 지정하려면 initializer(초기값 목록)를 쓴다.

```java
int[] ages = new int[]{21, 17, 43, 56, 34};
int[] studentAges = {21, 22, 24, 20, 25};
```

두 array의 길이는 각각 initializer의 원소 수인 5다. 둘째는 declaration에서 허용되는 간략한 형태다. 자료의 `new int[3]{14, 13, 12}`는 dimension expression과 initializer를 함께 쓴 **오류 예**다. 이 제한에 대한 강의자의 설계 이유 추측을 확정된 언어 설계 근거로 받아들이지는 않는다.

`int[]`·`double[]`의 components는 primitive 값이고 `String[]`의 components는 String references다. 따라서 array를 연속 저장 공간으로 소개한 설명이 모든 String 문자 내용까지 한 덩어리로 놓인다는 뜻은 아니다.

## Index·length·element assignment

M006 pp.7–10은 네 개의 자동차 이름으로 index를 설명한다.

```java
String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};
System.out.println(cars[0]); // Volvo
cars[0] = "Opel";
System.out.println(cars[0]); // Opel
System.out.println(cars.length); // 4
```

Index는 0부터 시작하므로 길이 4의 마지막 index는 3이다. `cars[0]`에 대입하면 첫 slot의 reference를 바꾼다. 원소를 하나 추가하거나 기존 String의 문자를 고치는 것이 아니므로 길이는 계속 4다. `new int[3]`의 길이는 3이며, array의 `length`에는 괄호가 없다. String의 `length()`와 구별한다.

[Lab02 M008, PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf)의 별도 예는 첫 slot을 `"Hyundai"`로 바꾼다. 따라서 그 예의 출력은 `Volvo`, `Hyundai`, `4`다. 이 값을 theory의 `Opel`과 섞으면 실행 추적이 달라진다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 42:20은 index와 길이의 관계를 설명하며, 9월 10일 녹음의 불명확한 교체 문자열은 Lab02에 인쇄된 값으로 확인한다.

모든 원소를 읽는 다음 loop는 index 0, 1, 2, 3을 방문한다. `i < cars.length`가 중요하다. `i == cars.length`는 이미 범위 밖이다.

```java
for (int i = 0; i < cars.length; i++) {
    System.out.println(cars[i]);
}
```

여기서 `for`는 “0에서 시작해 하나씩 증가하며 범위 안인 동안 읽는다”는 뜻으로 먼저 사용한다. 검사와 갱신의 정확한 순서는 [[courses/computer_programming/units/control-flow|Control flow]]에서 이어진다.

## Array of arrays와 두 단계 indexing

Java의 2D array(이차원 배열)는 각 component가 다시 array를 가리키는 array of arrays다. 따라서 반드시 직사각형일 필요가 없다.

```java
int[][] myNumbers = {{1, 2}, {3, 4, 5}};
System.out.println(myNumbers[1][2]); // 5
myNumbers[0][1] = 0;
```

`myNumbers[1]`은 두 번째 내부 array `{3, 4, 5}`를 고른다. 이어 `[2]`는 그 array의 세 번째 원소 5를 고른다. 마지막 대입은 첫 행의 두 번째 값 2만 0으로 바꾼다. 첫 번째 index는 row array 선택이고, 두 번째 index는 그 안의 component 선택이다. `char[][] ticTacToe`도 바깥 components가 `char[]` references라는 같은 구조다.

Lab02 M008 p.8의 그림에서는 `arr`에서 바깥 array로 가는 화살표를 먼저 따라간 뒤, 세 reference slots에서 각 row array로 가는 화살표를 따라가야 한다. 이 그림의 값은 `{{2,7,9},{3,6,1},{7,4,2}}`이므로 `arr[0][0]`은 2, `arr[1][2]`는 1이다. 화살표는 논리적 reference 관계를 나타내며 실제 memory 주소 간격을 계산하는 도면이 아니다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 48:09의 설명도 이러한 단계별 접근에 해당한다.

### Row마다 다른 길이를 따르는 순회

다음은 M006 p.14의 **별도 예**다. 앞의 indexing 예와 달리 첫 행의 길이가 3이고 둘째 행은 2다.

```java
int[][] myNumbers = {{1, 2, 3}, {4, 5}};
for (int i = 0; i < myNumbers.length; ++i) {
    for (int j = 0; j < myNumbers[i].length; ++j) {
        System.out.println(myNumbers[i][j]);
    }
}
```

바깥 `length`는 row 수 2다. Inner loop(안쪽 반복문)는 현재 고른 `myNumbers[i]`의 길이를 사용한다. 첫 행에서 1, 2, 3을 출력하고 둘째 행에서 4, 5를 출력한다. Inner bound를 2로 고정하면 3을 빠뜨리고, 3으로 고정하면 둘째 행의 범위를 벗어난다. 차원이 늘어나도 각 단계에서 reference를 따라 다음 array를 고른다는 원리는 같다.

## String array의 slot 변경과 immutability

2D String array에서는 두 단계 indexing 뒤에 String reference slot을 얻는다. 이 slot을 바꾸는 일과 String의 문자 내용을 바꾸는 일을 구별하면 array와 immutability가 충돌하지 않는다.

```java
String[][] names = {{"Volvo"}};
String old = names[0][0];
names[0][0] = "Opel";
```

이 코드는 M002 p.48의 String 모델과 array indexing을 연결한 **설명용 재구성**이다. 마지막 줄 뒤 `names[0][0]`은 `"Opel"`을 가리키지만 `old`는 여전히 `"Volvo"`를 가리킨다. Array slot에 새 reference를 저장했을 뿐 Volvo의 문자 내용을 수정하지 않았다.

[[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 52:15–52:47에는 이 주제의 질의응답이 남아 있지만, 정확한 질문과 “String itself to the memory address”라는 답변 전체의 뜻은 불확실하다. 위 코드를 당시 질문의 복원으로 제시하지 않는다. 강의에서 뒤로 미룬 object·memory 관계는 [[courses/computer_programming/units/objects-references|Objects와 reference 전달]]에서 더 자세히 연결된다.

## 핵심 정리

- 선언만으로 array가 생기지 않는다. 생성된 components의 기본값과 local reference의 대입 여부는 별개다.
- 길이가 n이면 유효 index는 0…n−1이다. Slot 대입은 길이를 늘리지 않는다.
- 2D array는 row references를 가진 array이며 안쪽 bound는 현재 row의 length다.
- String slot을 바꾸어도 이전 String을 가리키는 다른 reference는 유지된다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 선언·생성·initializer

Local `int[] a;`, `int[] b=new int[4];`, `int[] c={21,17,43,56,34};`를 구별하고 `new int[3]{14,13,12}`의 문제를 설명하라. 다른 component types의 기본값도 적어라.

<details><summary>해설 보기</summary>

a는 reference 선언만이고 읽기 전 대입이 필요하다. b는 길이4 array를 생성해 네 int가 0으로 초기화된다. c는 initializer 다섯 값으로 길이5 array를 만든다. Dimension expression과 initializer를 함께 쓴 마지막 표현은 허용되지 않아 `new int[]{14,13,12}`처럼 쓸 수 있다. 새 double·boolean·reference components는 각각 0.0·false·null이다. String[]는 문자 내용이 아니라 references를 담으며 local a의 상태와 component 기본값은 다르다.

**확인 기준:** 세 선언의 실제 생성 여부·길이·값과 오류 수정 근거를 설명한다.

</details>

#### 확인 Q02 · Slot 변경과 길이

`{"Volvo","BMW","Ford","Mazda"}`에서 첫 slot을 theory에서는 Opel, Lab02에서는 Hyundai로 바꾼다. 각 전후 첫 값, 길이, 마지막 index와 전체 순회 bound를 설명하라.

<details><summary>해설 보기</summary>

Theory는 Volvo→Opel, Lab02는 Volvo→Hyundai다. 두 경우 길이4·마지막 index3이며 `i=0`부터 `i<cars.length`가 네 slot을 읽는다. `cars.length`에 괄호를 붙이지 않고 String의 `length()`와 구별한다. 기존 slot의 reference만 바뀌므로 원소 추가도, 이전 String 수정도 아니다. `i<=cars.length`는 index4를 접근하려 해 범위를 벗어난다.

**확인 기준:** 두 자료 값을 섞지 않고 length4/index3을 구별한다.

</details>

#### 확인 Q03 · 두 단계 indexing

A=`{{1,2},{3,4,5}}`에서 A[1][2]를 읽고 A[0][1]=0을 적용하라. 별개 Lab02 그림 B=`{{2,7,9},{3,6,1},{7,4,2}}`의 B[0][0], B[1][2]는? 두 index가 고르는 대상을 설명하라.

<details><summary>해설 보기</summary>

A[1]은 `{3,4,5}` row를 골라 그 [2]가 5다. 대입 뒤 A는 `{{1,0},{3,4,5}}`다. B의 두 읽기는 2와1이다. 바깥 array의 component는 row array reference이고 안쪽 index는 선택된 row의 값을 고른다. `char[][]`에서도 바깥은 char[] references이며 모든 row가 같은 길이라는 보장은 없다. 화살표를 물리 주소 간격으로 계산하지 않는다.

**확인 기준:** 세 읽기와 수정 위치, row reference 구조를 정확히 제시한다.

</details>

#### 확인 Q04 · Row별 길이와 방문 순서

`{{1,2,3},{4,5}}`를 outer index i와 inner index j로 순회한다. 두 loop의 bound, 출력 순서, 안쪽 bound를 2 또는3으로 고정할 때의 문제를 설명하라.

<details><summary>해설 보기</summary>

Outer는 `i<myNumbers.length`로 두 rows, inner는 `j<myNumbers[i].length`로 현재 row를 따른다. 각 row에서 j=0으로 다시 시작해 1,2,3 다음4,5를 방문한다. 고정2는 첫 row의3을 놓치고 고정3은 둘째 row index2를 잘못 읽는다. 따라서 직사각형이라는 가정 없이 row를 선택한 뒤 길이를 구해야 한다.

**확인 기준:** 누락과 범위 밖 접근을 서로 다른 오류로 설명한다.

</details>

#### 확인 Q05 · String slot과 이전 reference

`String[][] names={{"Volvo"}}; String old=names[0][0]; names[0][0]="Opel";` 뒤 두 읽기는? Immutability와 연결하고 이 예의 출처 한계도 말하라.

<details><summary>해설 보기</summary>

names[0][0]은 Opel, old는 Volvo다. 두 단계 indexing으로 선택한 slot에 새 reference가 저장되었고 기존 Volvo의 문자는 바뀌지 않았다. 따라서 immutability와 양립한다. 이 코드는 본문의 설명용 재구성이며 52:15–52:47의 불명확한 원래 질문을 복원한 것이 아니다.

**확인 기준:** Slot/reference/object 내용을 구별하고 불확실성을 지우지 않는다.

</details>

### 적용 연습

#### 연습 P01 · 변경된 slot만 추적하기

**새로 작성한 강의 기반 일반 연습.** 직접 대응 기출 유형 근거는 없다.
```java
String[][] labels = {{"red", "blue"}, {"green"}};
String old = labels[0][1];
labels[0][1] = labels[1][0];
labels[1][0] = "gold";
```
최종 각 row와 old, 바깥/안쪽 길이를 적고 고정 inner bound 2의 문제를 찾아라.

<details><summary>해설 보기</summary>

최종 rows는 `{"red","green"}`, `{"gold"}`, old는 blue다. 첫 대입은 green의 reference를 첫 row 둘째 slot에 복사한다. 다음 대입은 둘째 row 첫 slot만 gold로 바꾸므로 앞서 저장한 green은 유지된다. 바깥길이2, row길이2·1은 그대로다. 고정 bound2는 둘째 row index1을 접근하므로 잘못이며 해당 row의 length를 사용해야 한다. 어떤 String의 문자도 바꾸지 않았다.

**확인 기준:** 순차 대입의 대상·길이 불변·범위 오류를 모두 확인한다.

</details>

### 복습 순서

Q01–Q02에서 생성과 길이를 확인하고 Q03–Q04에서는 화살표와 방문 순서를 그린다. Q05와 P01을 풀 때 바뀐 slot에만 표시를 하라.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 보정 녹음문]] — 37:38, 41:21, 42:20, 48:09, 52:15, 52:47.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 보정 녹음문]] — 01:35–03:25.

### 강의자료와 해당 페이지

- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-003), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-006), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-010), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-014).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-008).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048).

Theory의 첫 원소 교체는 Opel, Lab02는 Hyundai다. 9월 10일 불명확한 단어는 PDF로 확인한 값과 구별한다. 9월 8일 52:15–52:47의 정확한 질문·모호한 답은 여전히 불확실하며 String slot 예는 설명용 재구성이다.


---

[[courses/computer_programming/units/types-expressions|← 이전: Variables·Types·Operators와 String]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/control-flow|다음: Boolean 조건·분기·반복과 실행 추적 →]]
