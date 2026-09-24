---
title: "Boolean 조건·분기·반복과 실행 추적"
description: "Boolean·분기·반복을 추적하며 경계값, 누적 최댓값과 delimiter 처리를 복습한다."
course: "computer_programming"
unit_id: "control-flow"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 2 Java Basics 1.pdf", "3 java basics 2.pdf", "Lab02 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-08-lecture-03", "courses/computer_programming/lectures/2026-09-10-lecture-04"]
---

Condition의 값과 실제로 실행되는 문장을 따로 추적한다. Branch·loop의 경계와 누적 상태를 확인해 off-by-one 오류와 생략된 계산을 설명해 보자.

## Boolean expression으로 실행 조건 만들기

[[courses/computer_programming/units/types-expressions|Expression의 값]]을 계산할 수 있으면 그 값으로 실행 경로를 고를 수 있다. Condition(조건)은 `true` 또는 `false`인 boolean expression이다. `if` 안에서만 존재하는 특별한 문장이 아니라 저장하거나 조합할 수 있는 값이다.

| `a` | `b` | `a && b` | `a \|\| b` |
| --- | --- | --- | --- |
| `true` | `true` | `true` | `true` |
| `true` | `false` | `false` | `true` |
| `false` | `true` | `false` | `true` |
| `false` | `false` | `false` | `false` |

`!`는 boolean을 반전한다. 따라서 `(!a) && (!b)`는 `!(a || b)`와, `(!a) || (!b)`는 `!(a && b)`와 동치다. [Computer Programming M006, PDF p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf)의 `(x > 0 && x > 1) || (x < 0 && x < -1)`은 `x > 1 || x < -1`로 단순화된다. `x > 1`이면 이미 `x > 0`이고, `x < -1`이면 이미 `x < 0`이기 때문이다.

자료의 odd(홀수) 검사 `x % 2 == 1`에는 범위 한정이 필요하다. Java에서 `-3 % 2`는 −1이어서 이 검사는 음의 홀수를 놓친다. Signed integer 전체에서는 `x % 2 != 0`을 쓸 수 있다. 이는 [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 55:16의 예에 대한 설명상의 보충이며, 강의자가 처음부터 입력을 음이 아닌 수로 제한했다고 고쳐 쓰는 것은 아니다.

### Short-circuit가 생략하는 계산

Short-circuit evaluation(단락 평가)은 결과를 이미 알면 오른쪽 operand를 평가하지 않는 규칙이다. `&&`는 왼쪽이 `false`일 때, `||`는 왼쪽이 `true`일 때 오른쪽을 건너뛴다.

```java
int denominator = 0;
int num = 100;
if (denominator != 0 && num / denominator == 1) {
    // body
}
```

[M002 PDF p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)의 예에서 왼쪽 조건은 `false`이므로 나눗셈을 시도하지 않는다. 조건의 순서를 바꾸면 0으로 나누는 계산을 먼저 수행하여 보호가 사라진다.

`true || complexCondition`은 오른쪽 조건을 생략하지만 전체가 `true`이므로 `if` body는 실행한다. 반면 `false && complexCondition`은 오른쪽을 생략하고 전체도 `false`라 body를 실행하지 않는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 24:17–27:10에서 강의자가 바로잡은 구별도 이것이다. “조건 계산을 건너뛴다”와 “body를 건너뛴다”는 다른 말이다.

## Branch가 선택하는 경로

M006 p.16의 flowchart(흐름도)는 관련 메뉴나 버튼을 찾고, 클릭한 결과가 성공했는지에 따라 종료 또는 재시도로 갈라지는 자료의 비유다. 그림에서는 조건 지점에서 나가는 화살표를 구별하고, 실패 경로가 다시 앞의 선택으로 돌아오는지 보아야 한다. 이 그림의 모든 세부 절차가 구두로 설명되었다는 뜻은 아니다.

`if`는 소문자 keyword다. `If`나 `IF`로 쓸 수 없다. 연결된 `if–else if–else`는 위에서부터 검사하여 첫 번째 참인 branch(분기) 하나를 선택한다.

```java
int time = 22;
if (time < 10) {
    System.out.println("Good morning.");
} else if (time < 20) {
    System.out.println("Good day.");
} else {
    System.out.println("Good evening.");
}
```

M006 p.21의 `time = 22`는 마지막 branch를 고른다. 이해를 위한 변경으로 `time = 8`을 대입하면 첫 branch만 실행한다. 8이 20보다도 작다는 이유로 둘째 인사까지 출력하지 않는다. 독립적인 여러 `if`와 연결된 branch는 다르다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 05:12의 복습도 조건과 경로를 연결한다.

Ternary operator(삼항 연산자) `condition ? expressionTrue : expressionFalse`는 값 하나를 선택한다. 자료의 `a = 10, b = 20`에서 `a > b ? "a is greater" : "b is greater"`는 둘째 String을 선택한다. 다만 false branch의 실제 범위는 `a <= b`다. `a == b`에도 같은 문구가 선택되므로 문구만으로 조건의 뜻을 판단하면 안 된다. 마찬가지로 `x < 3`의 반대는 `x >= 3`이지 `x > 3`만이 아니다.

### Colon-style switch와 fall-through

`switch`는 하나의 expression 값에 맞는 `case`에서 실행을 시작한다. 현재 자료는 `byte`·`short`·`char`·`int` 및 String 예를 다룬다. 다음은 M006 p.26의 형태다.

```java
char grade = 'B';
switch (grade) {
    case 'A':
        System.out.println("Your score is 4.");
        break;
    case 'B':
        System.out.println("Your score is 3.");
        break;
    default:
        System.out.println("There is no grade " + grade + ".");
}
```

`'B'`에 대응하는 곳에서 시작하고 `break`로 switch를 끝내므로 `Your score is 3.`만 출력한다. P.27처럼 두 `break`를 없애면 B의 출력 뒤 `default`까지 fall-through(아래 구문으로의 계속 실행)하여 `There is no grade B.`도 출력한다. `default`는 match가 없을 때의 진입점일 뿐 아니라 앞 case에서 흘러 내려와 실행될 수도 있다.

`break` 없이도 마지막 문장을 지나 블록 끝에 도달하면 switch는 종료한다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:03:51의 설명을 “break만이 유일한 종료 방법”이라고 확대하면 안 된다. M006 p.28의 `"something"`을 `"x"`·`"y"`와 비교하는 switch와 `equals` 기반 if/else는 모두 `end`를 출력한다. 의도적인 fall-through는 가능하지만 break 누락 때문에 강의자는 if/else를 선호한다고 설명했다. 여기서는 원본 colon-style만 다룬다.

## Loop의 검사·실행·갱신 순서

Loop(반복문)는 같은 body를 상태가 변하는 동안 다시 실행한다. `while`은 body보다 먼저 검사하므로 처음부터 false이면 0회 실행한다. `do-while`은 body 뒤에 검사하므로 최소 1회 실행하며 마지막 semicolon이 필요하다.

[Lab02 M008, PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf)의 다음 두 예는 각각 `i = 0`에서 시작한다.

```java
int i = 0;
while (i < 5) {
    System.out.print(i++ + ",");
}
```

```java
int i = 0;
do {
    System.out.print(i++ + ",");
} while (i < 5);
```

둘 다 `0,1,2,3,4,`를 출력한 뒤 `i = 5`에서 끝난다. 설명용으로 시작값만 5로 바꾸면 while은 아무것도 출력하지 않고, do-while은 `5,`를 한 번 출력하여 `i = 6`이 된 뒤 끝난다.

[[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:07:46 이후에는 처음만 true인 임시 boolean으로 비슷한 동작을 만드는 설명이 있지만 정확한 원래 조건은 불명확하다. 이를 이해하는 **별도 도식**은 다음과 같다.

```text
boolean first = true;
while (first || condition) {
    first = false;
    BODY
}
```

`BODY`와 `condition`은 Java 코드의 실제 identifier가 아닌 자리표시자다. `first`는 충돌하지 않는 새 변수이고 BODY가 이를 수정하지 않는다고 가정한다. 첫 진입은 short-circuit로 condition을 생략하고 이후에는 매번 검사한다. `first = false`를 BODY **앞에** 놓아야 continue가 있어도 다음 검사를 생략하지 않는다. Break는 추가 검사 없이 끝낸다. 이것은 원래 시연을 복원한 코드가 아니다.

### for와 for-each

`for(initialization; condition; update)`는 initialization을 한 번 실행한 뒤 condition → body → update → condition을 반복한다. `for(int i = 0; i < 5; i++)`의 body가 `i`를 출력하면 0, 1, 2, 3, 4를 출력하고, 마지막 갱신에서 5가 되어 끝난다.

```java
String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};
for (String car : cars) {
    System.out.print(car + " ");
}
System.out.println();
```

For-each(원소 순회)는 각 element 값을 왼쪽 variable에 차례로 제공한다. 위 예는 네 이름 뒤에 각각 공백을 붙이고, loop 뒤에서 줄을 바꾼다. 같은 작업을 index-based for로 할 수도 있다. Index가 필요한 변경에는 일반 for가 유용하고, 값 읽기에는 for-each가 counter 관리를 줄인다. 모든 for를 그대로 for-each로 치환할 수 있다는 뜻은 아니다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 05:12–06:06 및 M008 p.11의 비교다.

### break·continue와 body의 범위

```java
for (int i = 0; i < 5; i++) {
    if (i == 3) {
        break;
    }
    System.out.println(i);
}
```

M006 p.37은 출력 전에 3을 검사하므로 `break`일 때 0, 1, 2만 출력한다. 이를 `continue`로 바꾸면 현재 iteration(반복 회차)의 나머지만 건너뛰어 0, 1, 2, 4를 출력한다. Continue는 이 for의 `i++`를 거쳐 다음 condition으로 가므로 3에 머물지 않는다. `if`는 loop가 아니며, break의 대상은 이를 감싼 for다.

단일 statement의 body에서는 braces를 생략할 수 있지만 줄바꿈이 다음 statement까지 포함시켜 주지는 않는다. `while (true) System.out.println("Infinite");`는 조건이 계속 참이고 종료 경로도 없어 계속 출력한다. Header 외에 숨은 종료 조건이 많으면 읽기가 어려워지므로 짧은 코드보다 실행 범위의 명확함이 중요하다.

## Nested loop와 누적 상태의 실행 추적

Nested loop(중첩 반복문)는 바깥 회차마다 안쪽 초기화를 다시 수행한다. M006 p.39의 예는 그 순서를 출력 모양으로 보여 준다.

```java
for (int i = 5; i > 0; i--) {
    for (int j = 0; j < i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
```

`i`가 5, 4, 3, 2, 1일 때마다 `j`가 0에서 다시 시작하여 그만큼의 별을 출력한다. `print`는 줄을 바꾸지 않고, inner loop 밖의 `println`이 한 행을 끝낸다. 결과는 별 5개부터 1개까지의 다섯 줄이며 총 5+4+3+2+1=15개다. 둘째 행에서는 `i = 4`이고 `j = 0,1,2,3`의 네 번 출력 뒤 줄바꿈한다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:20:10

### Running maximum의 초기값

```java
int[] nums = {23, -43, -25, 14, 36};
int max = Integer.MIN_VALUE;
for (int num : nums) {
    if (num > max) {
        max = num;
    }
}
System.out.println("The max number is " + max);
```

M006 p.40의 `max`는 지금까지 읽은 값의 최댓값을 유지한다. 초기값 −2,147,483,648에서 첫 23을 읽어 23으로 바뀌고, −43·−25·14에서는 유지되며 마지막 36에서 갱신된다. 출력은 `The max number is 36`이다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:22:46

초기값을 0으로 잡으면 전부 음수인 입력에서 존재하지도 않는 0을 답으로 남길 수 있다. 반대로 empty array(빈 배열)에서는 위 코드가 한 번도 갱신하지 않아 초기값만 남는다. 이 두 경계 분석은 원본 코드에서 도출한 설명이며, 빈 집합의 최댓값을 이 코드가 정의했다는 뜻은 아니다.

### Fencepost와 마지막 delimiter

M006 p.41은 마지막 원소를 분리하여 trailing comma(끝의 불필요한 쉼표)를 피한다.

```java
char[] chars = {'c', 'o', 'm', 'p', 'u', 't', 'e', 'r'};
for (int i = 0; i < chars.length - 1; i++) {
    System.out.print(chars[i] + ",");
}
System.out.println(chars[chars.length - 1]);
```

Loop는 e까지 각 문자 뒤에 comma를 붙이고, 마지막 r은 comma 없이 출력한다. 결과는 `c,o,m,p,u,t,e,r`와 줄바꿈이다. `'c'`는 char, `","`는 String이므로 둘을 더하면 출력할 String을 만든다. Java에서 `char[]`와 String은 별개의 type이다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 01:25:36

길이 1에서는 loop가 0회이고 마지막 출력만 수행한다. 길이 0에서는 마지막 index 접근이 유효하지 않다. 즉 이 형태는 nonempty array를 전제로 한다. 일반 전체 순회의 `length`와 마지막 원소를 제외하는 `length - 1`은 서로 다른 목적이다.

선택적 기출 적용으로, 2025-1 복기의 날짜 계산 항목도 정수 나눗셈·나머지·조건·누적과 경계 정의를 함께 읽게 한다. 달을 처리하기 전에 “지난 날 수”가 기준일에서 0인지 1인지 정해야 하고, 완료된 달과 현재 달에서 센 부분을 구별해야 한다. 원본은 입력을 2001년으로 제한하면서 윤년 규칙도 요구한다. 2001년은 윤년이 아니므로 그 범위에서 윤년 branch는 실행되지 않는다. 이 불일치를 임의로 넓힌 입력 범위로 고치거나 출제 빈도 주장으로 바꾸지 않는다. 이 항목은 공식 원본·정답이 아닌 복기 자료다. [EX:cp_2025_1_midterm_q09 p.6]

## 핵심 정리

- Short-circuit는 오른쪽 조건을 생략한다. 그 사실만으로 if body까지 생략되는 것은 아니다.
- `if` chain은 첫 참 branch만, colon-style switch는 match부터 break나 블록 끝까지 실행한다.
- Loop는 검사·body·update 순서와 continue/break의 목적지를 따로 읽는다.
- Maximum 초기값, row별 반복수, 마지막 delimiter와 empty 입력은 서로 다른 경계다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · Boolean과 음수 홀수

TT,TF,FT,FF에서 &&·|| 결과를 적고 두 negation 동치를 써라. `(x>0&&x>1)||(x<0&&x<-1)`을 줄이고 x=−3의 `%2==1`과 `%2!=0`을 비교하라.

<details><summary>해설 보기</summary>

AND는 T,F,F,F, OR는 T,T,T,F다. `(!a)&&(!b)`는 `!(a||b)`, `(!a)||(!b)`는 `!(a&&b)`와 같다. 더 강한 비교가 약한 비교를 함의하므로 식은 `x>1||x<-1`이다. −3%2=−1이라 ==1은 false, !=0은 true다. Signed 홀수를 검사하려면 0 아닌 나머지를 봐야 하며 자료의 원래 예가 음수를 제외했다고 고쳐 말하지 않는다.

**확인 기준:** 진리값·동치·함의·signed remainder를 모두 설명한다.

</details>

#### 확인 Q02 · 조건 생략과 body 실행

denominator=0에서 `denominator!=0 && 100/denominator==1`과 역순을 비교하라. `true||complexCondition`과 `false&&complexCondition`의 오른쪽과 if body는 각각 실행되는가?

<details><summary>해설 보기</summary>

원래 순서는 왼쪽 false여서 나눗셈을 생략하고 전체 false다. 역순은 먼저 정수 0 나눗셈을 시도해 실패한다. `true` OR는 오른쪽을 생략하지만 전체 true라 body는 실행한다. `false` AND는 오른쪽도 body도 생략한다. 생략되는 계산·side effect와 최종 논리 결과를 따로 기록해야 한다.

**확인 기준:** 순서의 안전성 및 오른쪽/body 네 판단이 정확하다.

</details>

#### 확인 Q03 · 첫 참 branch와 false 범위

time<10, else if time<20, else인 인사 예에서 time=22와8의 경로는? `a>b?"a is greater":"b is greater"`에서 a==b이면? Flowchart의 실패 화살표도 어떤 뜻인지 설명하라.

<details><summary>해설 보기</summary>

22는 Good evening., 8은 Good morning.만 선택한다. `else if`는 앞 조건이 false인 경로에서만 검사되어 독립 if들과 다르다. Ternary는 같은 값에서도 둘째 문구를 고르지만 그 branch의 수학적 범위는 a<=b다. 마찬가지로 x<3의 false는 x>=3이다. Flowchart에서 실패 화살표가 앞 선택으로 돌아가면 재시도 경로이지 성공 종료가 아니다. Keyword는 소문자 `if`다.

**확인 기준:** 문구보다 조건 범위를 우선하고 첫 참 branch만 선택한다.

</details>

#### 확인 Q04 · Match 이후의 switch

Grade B에서 B case가 score3을 출력하고 다음 default가 no-grade 메시지를 출력한다. B 뒤 break가 있을 때와 없을 때를 비교하라. `default` 진입·블록 종료, `"something"`을 x/y와 비교하는 예도 설명하라.

<details><summary>해설 보기</summary>

`break`가 있으면 `Your score is 3.`만, 없으면 이어 `There is no grade B.`도 출력한다. `default`는 match가 없는 진입점이지만 앞 case에서 fall-through하여 도달할 수도 있다. 마지막 문장을 지나 closing brace에 도달해도 switch는 종료하므로 break만 유일한 종료는 아니다. String이 something이면 x/y가 아니어서 source의 switch와 equals 기반 if/else 모두 end를 출력한다. 이는 제시된 colon-style 예이며 지원 type 전체를 일반화하지 않는다.

**확인 기준:** Default를 항상 ‘match 없음’으로 오해하지 않는다.

</details>

#### 확인 Q05 · 검사 시점과 첫 실행

별도 i=0에서 `while(i<5)`와 `do...while(i<5);`의 body가 `print(i++ + ",")`다. 시작값0과5에서 출력과 최종 i를 비교하라.

<details><summary>해설 보기</summary>

0에서 둘 다 `0,1,2,3,4,`, 최종 i=5다. 5에서 while은 선검사 false로 출력 없이 i=5, do-while은 한 번 실행해 `5,`, 최종 i=6이다. Postfix가 이전값을 출력한 뒤 저장값을 늘린다. `do`–`while`은 후검사여서 최소 한 번 실행하며 끝 semicolon이 필요하다.

**확인 기준:** 네 경우의 출력/최종값과 검사 위치를 구별한다.

</details>

#### 확인 Q06 · `first` flag와 continue

본문의 별도 도식 `while(first||condition)`에서 first=true로 시작한다. BODY가 first를 바꾸지 않을 때 `first=false`를 BODY 뒤에 두면 continue가 왜 문제인가? `break`는?

<details><summary>해설 보기</summary>

첫 진입은 first가 true라 condition을 생략한다. Reset을 BODY 뒤에 두면 continue가 reset을 건너뛰어 first가 계속 true이고 이후 검사도 생략될 수 있다. BODY 전에 false로 만들면 다음 반복부터 condition을 검사한다. `break`는 loop를 끝내 추가 검사하지 않는다. Fresh first variable을 가정한 설명용 도식이며 원래 불명확한 temp 조건을 복구한 것이 아니다.

**확인 기준:** Reset 위치·continue 경로·source 한계를 모두 설명한다.

</details>

#### 확인 Q07 · for와 for-each

`for(int i=0;i<5;i++)` 순서와 출력할 i들을 말하라. `for(String car:cars)`의 colon 양쪽과 출력 후 줄바꿈 위치, index가 필요한 상황을 설명하라.

<details><summary>해설 보기</summary>

초기화 한 번 뒤 검사→body→update→검사이며 출력값은0…4, 마지막 update가5로 만든 뒤 멈춘다. Colon 왼쪽은 element를 받을 type·변수, 오른쪽은 array다. `cars`의 네 이름을 `print(car+" ")`하면 각각 뒤 공백이 있고 loop 밖 println이 한 줄을 끝낸다. 위치에 따라 slot을 바꾸려면 index 기반 for가 유용하고 값만 읽을 때 for-each가 간단하다. 모든 loop를 서로 치환할 수 있다는 뜻은 아니다.

**확인 기준:** Update 시점·colon 구조·출력과 사용 목적을 확인한다.

</details>

#### 확인 Q08 · 중단·생략·body 범위

0≤i<5 순회에서 출력 전에 i==3이면 break 또는 continue한다. 두 출력과 다음 이동을 비교하라. Braces 없는 body와 `while(true) println("Infinite")`도 설명하라.

<details><summary>해설 보기</summary>

`break`는0,1,2만 출력하고 loop 다음으로 간다. `continue`는0,1,2,4를 출력하며 i=3에서 남은 body만 생략하고 for update i++로4가 된 뒤 다시 검사한다. 안의 if는 break 대상 loop가 아니다. Braces를 생략하면 body는 한 statement뿐이며 줄바꿈이 범위를 넓히지 않는다. 계속 true이고 종료 경로가 없는 while은 Infinite를 끝없이 출력한다.

**확인 기준:** Continue 후 update를 빠뜨리지 않고 body 범위를 표시한다.

</details>

#### 확인 Q09 · Triangle의 안쪽 반복

Outer i=5부터 i>0 동안 감소, inner j=0부터 j<i 동안 `print("*")`, inner 뒤 println인 예의 각 행·총 별·둘째 행 j값을 설명하라.

<details><summary>해설 보기</summary>

행별 별은5,4,3,2,1로 총15개다. 둘째 outer에서 i=4, j는0,1,2,3이라 네 번 print한다. Inner 초기화는 outer마다 다시 실행되고 줄바꿈은 inner를 마친 뒤 한 번이라 행이 만들어진다. `print`와 println 위치를 바꾸면 같은 횟수여도 모양이 달라진다.

**확인 기준:** 총합뿐 아니라 reset과 줄바꿈 위치를 설명한다.

</details>

#### 확인 Q10 · Running maximum의 기준

nums={23,−43,−25,14,36}, max=Integer.MIN_VALUE에서 num>max일 때 갱신한다. 각 단계와 0 초기값·empty 입력의 문제를 설명하라.

<details><summary>해설 보기</summary>

초기 −2147483648에서23으로 갱신, −43·−25·14에서23 유지,36에서36으로 바뀐다. 매 단계 max는 방문한 값들의 최댓값이다. 초기0은 모든 원소가 음수이면 array에 없는0을 남긴다. Empty array는 갱신이 없어 sentinel만 남으므로 이 코드가 빈 집합 최댓값을 정의했다고 할 수 없다.

**확인 기준:** 각 갱신과 all-negative·empty의 서로 다른 한계를 설명한다.

</details>

#### 확인 Q11 · 마지막 delimiter

본문의 computer char[]에서 i<length−1 동안 `print(chars[i]+",")`, 끝에 마지막 char를 println한다. 출력과 length1·0, char/String 구별을 설명하라.

<details><summary>해설 보기</summary>

출력은 `c,o,m,p,u,t,e,r`와 줄바꿈이다. `e`까지 comma를 붙이고 마지막 r을 분리해 trailing comma를 피한다. `'c'`는 char, `","`는 String이라 결합 결과는 String이며 char[] 자체는 String이 아니다. 길이1이면 loop0회 뒤 유일한 char 출력, 길이0이면 마지막 index−1 접근이 잘못이다. 이 코드는 nonempty 전제를 갖는다.

**확인 기준:** Delimiter의 목적과 두 경계 입력을 모두 다룬다.

</details>

### 적용 연습

#### 연습 P01 · 경과량과 현재 위치

**새로 작성한 synthetic 기출 응용 연습.** [EX:cp_2025_1_midterm_q09 p.6]에서 입력 범위와 완료한 구간/현재 구간, 0기준 경과량을 구별하는 추론을 옮겼다. 선수는 배열·조건·반복이며 날짜·윤년 구현은 요구하지 않는다. 원문은 2001년 범위와 윤년 요구가 함께 있는 복기본이고 공식 답안은 없다.

서로 연속인 세 구간의 길이는 `{4,6,3}`이다. 구간 index s, 그 안의 0기준 위치 p에서 `elapsed=p; for(i=0;i<s;i++) elapsed+=lengths[i];`로 시작점 이후 경과량을 센다. (s,p)=(0,0),(1,0),(1,5)의 결과와 1기준 전체 위치를 구하라. Bound를 i<=s로 바꾸면 어떤 종류의 오류이며 p의 허용 범위는?

<details><summary>해설 보기</summary>

경과량은0,4,9이며 1기준 전체 위치는1,5,10이다. `s = 1`이면 완료한 첫 구간 길이4만 더하고 현재 구간에서는 p만 센다. `i<=s`는 아직 완료하지 않은 현재 구간 전체까지 더해 같은 위치를 과다 계산한다. `s = 1`,p=0이면4가 아니라10이 되어 경계 오류가 드러난다. 허용 범위는 0≤s<3, 0≤p<lengths[s]다. 1기준을 원할 때 최종 결과에1을 더하는 것과 현재 구간을 통째로 더하는 것은 다르다.

**확인 기준:** 세 결과, 완료/현재 구분, 반례와 입력 범위를 모두 제시한다.

</details>

#### 연습 P02 · 빈 입력도 구분하는 출력 검토

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.** Nonempty char[]를 comma로 연결하려는데 loop가 `i<=chars.length-1`이고 loop 뒤 마지막 원소도 다시 출력한다. 길이1에서 무엇이 잘못되며, 본문 방식의 bound와 empty 입력 처리 위치를 설명하라.

<details><summary>해설 보기</summary>

유일한 문자가 a이면 loop에서 `a,`를 내고 마지막 출력에서 a를 또 내어 `a,a`가 된다. Loop는 `i<chars.length-1`로 마지막 전까지만 처리하고 마지막 출력은 한 번만 한다. Empty 검사는 마지막 index 접근 전에 별도 경로로 처리해야 한다. Bound 수정만으로 length0에서 −1 접근이 사라지지는 않는다.

**확인 기준:** 중복 출력과 empty 접근을 별개로 진단한다.

</details>

### 복습 순서

Q01–Q04는 참/거짓과 실행 문장을 따로 쓰고 Q05–Q08은 loop 이동 경로를 그린다. Q09–Q11의 경계값을 확인한 뒤 P01에서 0기준/1기준을 비교하고 P02의 잘못된 두 bound를 고친다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 보정 녹음문]] — 55:16, 27:10, 24:17, 01:03:51, 01:07:46, 01:20:10, 01:22:46, 01:25:36.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 보정 녹음문]] — 05:12.

### 강의자료와 해당 페이지

- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.69](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-069), [p.70](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-070).
- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-016), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-018), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-021), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-023), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-028), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-031), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-033), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-040), [p.41](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-041).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-012).

9월 8일 01:07:46의 임시 조건은 불명확하다. `first` flag 도식은 설명용이며 당시 코드를 복원하지 않는다. 음수 odd·empty 입력 분석도 코드에서 도출한 보충이다. 현재 switch는 colon-style 범위다.

기출 연결: [EX:cp_2025_1_midterm_q09 p.6]의 입력 범위·경과량·경계 정의를 읽는 추론만 P01로 옮겼다. 원문은 2001년 입력에 윤년 처리도 요구하지만 그 해는 윤년이 아니어서 해당 branch가 실행되지 않는다. 복기본이며 공식 답안은 없고, 원문 전체나 새로운 미리보기 링크를 제공하지 않는다.


---

[[courses/computer_programming/units/arrays|← 이전: Array의 생성·참조와 다차원 데이터]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/methods|다음: Method의 계약·호출·반환과 재사용 →]]
