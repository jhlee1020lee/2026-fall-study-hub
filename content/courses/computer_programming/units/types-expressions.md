---
title: "Variables·Types·Operators와 String"
description: "Type 변환, 연산 순서, String과 한 줄 입력을 계산·추적으로 확인한다."
course: "computer_programming"
unit_id: "types-expressions"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 2 Java Basics 1.pdf", "3 java basics 2.pdf", "4 oop.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-01-lecture-01", "courses/computer_programming/lectures/2026-09-08-lecture-03"]
---

각 expression의 type·결과값·최종 variable 상태를 따로 기록한다. String의 내용과 reference를 구별하면 연산·입력 코드의 흔한 오해를 잡을 수 있다.

## Variable과 type이 정하는 저장·계산의 의미

[[courses/computer_programming/units/java-runtime|Java 실행 환경]]에서 source를 실행하는 방법을 보았다면, 이제 각 문장이 어떤 값을 읽고 바꾸는지 구별해야 한다. Variable(변수)은 type(자료형)에 맞는 값을 다루는 이름 있는 저장 대상이다. Declaration(선언)은 이름과 type을 정하고, initialization(초기화)은 처음 값을 넣으며, assignment(대입)는 값을 저장한다.

```java
int x;        // declaration
x = 10;       // assignment before the first read
x = 15;       // later assignment
int sum = 0;  // declaration with initialization
```

이는 [Computer Programming M002, PDF pp.27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)의 구분을 풀어 쓴 예다. Identifier(식별자)는 case-sensitive하므로 `myVar`와 `myvar`는 다르다. 문자·숫자·underscore·dollar sign으로 이름을 구성하되 숫자로 시작하지 않으며, `age`·`sum`·`totalVolume`처럼 역할이 보이는 이름이 읽기 쉽다. 소문자로 시작하는 것은 관례다. `String`은 keyword가 아니라 class 이름이며, 수업의 JDK 11에서 단독 `_`를 유효한 변수명으로 사용하면 안 된다.

Local variable(지역 변수)은 읽기 전에 값이 할당되어야 한다. `int x;`만으로 읽을 수 있는 값이 생기지는 않는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 12:10의 초기값이 JVM에 의해 불확실하게 정해진다는 표현은 이 규칙과 구별해야 한다. 여기서는 정확성을 위해 **local의 definite assignment와 field·array component의 default initialization은 다르다**고 보충한다.

### Primitive type과 reference type

Primitive type(기본형)은 `boolean`, `char`, `byte`, `short`, `int`, `long`, `float`, `double`의 여덟 가지다. `boolean`은 `true` 또는 `false`이고, `char`는 `'A'`처럼 single quotes로 쓰는 문자 값이다. 정수형의 크기는 다음과 같다.

| Type | Bits | Signed 범위 |
| --- | ---: | --- |
| `byte` | 8 | −128 … 127 |
| `short` | 16 | −32,768 … 32,767 |
| `int` | 32 | −2,147,483,648 … 2,147,483,647 |
| `long` | 64 | −2⁶³ … 2⁶³−1 |

N-bit signed 정수는 −2⁽ᴺ⁻¹⁾부터 2⁽ᴺ⁻¹⁾−1까지 2ᴺ개의 값을 나타낸다. `byte`에서 −128 … 127은 256개다. 최댓값도 128이라고 쓰면 257개가 되어 맞지 않는다.

Floating-point(부동소수점)인 `float`은 32 bits, `double`은 64 bits이며, 자료는 각각 약 6–7자리와 15자리 정밀도를 비교한다. 이는 소수점 아래 자리 수의 고정 보장이 아니라 대략적인 **유효숫자**다. M002 p.33의 표현은 이 의미로 바로잡아 읽어야 한다. M002 p.31과 M011 p.46의 그림이 floating-point를 Integral Value 아래에 연결한 것도 올바른 분류가 아니다. 일반 계산에는 `double`을 쓰는 이유가 정밀도에 있고, 많은 데이터를 다룰 때는 memory 비용도 고려한다. [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 STT]] 01:01:31의 설명도 이 선택과 연결된다.

Reference type(참조형)의 variable은 객체 전체가 아니라 객체를 가리키는 reference 값을 저장한다. 따라서 긴 `String`의 문자 내용 크기와 reference variable의 크기는 다른 문제다. Reference를 반드시 물리적 주소라고 생각하거나 모든 객체 크기가 같다고 생각하면 안 된다. Binary encoding과 endian의 상세는 이 범위에서 전개하지 않는다.

## Conversion과 literal의 type

Widening conversion(확대 변환)은 자료의 `byte → short → int → long → float → double` 방향으로 소개된다. Narrowing conversion(축소 변환)은 반대 방향에서 정보가 줄어들 수 있어 cast(형 변환)를 명시한다.

```java
double testDouble = 1.0;
float testFloat = (float) testDouble;
```

`(float)`는 이 expression의 값을 변환하며 `testDouble`의 선언 type 자체를 바꾸지 않는다. [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 STT]] 01:08:40과 M002 pp.38–42는 대입하려는 값이 어떤 type인지 먼저 읽도록 한다.

| 대입 | 판정과 이유 |
| --- | --- |
| `float f = 3.72;` | `3.72`는 기본적으로 `double`이므로 그대로 narrowing할 수 없다. |
| `double d = 3.72f;` | `f` suffix로 `float` literal이 되며 `double`로 widening한다. |
| `int i = 1000L;` | 크기가 작아도 `1000L`의 type은 `long`이므로 그대로 대입할 수 없다. |
| `long l = 1000;` | `int` literal을 `long`으로 widening한다. |

자료의 `13243`과 `13243L`도 같은 구별이다. Widening이 자동이라는 말은 언제나 숫자 정보가 완벽하게 보존된다는 뜻은 아니다. 큰 정수를 floating-point로 바꾸면 정밀도 한계로 반올림될 수 있다. 이 사슬을 `char`와 `boolean`까지 포괄하는 모든 conversion 규칙으로 확대하지 않는다.

## Operator의 결과값과 변수의 다음 상태

`x + 10`에서 `x`와 `10`은 operand(피연산자), `+`는 operator(연산자)다. Arithmetic operator(산술 연산자) `+`, `-`, `*`, `/`, `%`는 합·차·곱·나눗셈·나머지를 계산하고 `++`·`--`는 값을 1씩 바꾼다. Unary(단항)와 arithmetic은 배타적인 분류가 아니므로 `++`는 둘 다에 해당한다.

| Expression | 결과 | 계산 이유 |
| --- | --- | --- |
| `5 / 2` | `int` 값 `2` | 정수 나눗셈은 소수 부분을 버린다. |
| `5 % 2` | `int` 값 `1` | 몫이 아니라 나머지다. |
| `15 / 3.0` | `double` 값 `5.0` | 혼합 type의 계산에서 operand가 변환된다. |
| `2 << 3` | `int` 값 `16` | 이 예의 이진 `10`을 세 자리 옮기면 `10000`이다. |
| `0b1 & 0b0` | `0` | 대응 bit에 AND를 적용한다. |
| `true && false` | `false` | Boolean 조건을 결합한다. |

정수의 `5 / 0`은 오류다. 이 결론을 floating-point division까지 같은 규칙으로 일반화하지 않는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 04:33–09:18의 연산 소개는 바로 뒤 혼합 type 예와 함께 읽어야 한다. 모든 operator가 입력 type을 그대로 유지하는 것은 아니다. Bitwise operator(비트 연산자) `&`·`|`·`^`는 각각 AND·OR·XOR이고, shift는 bit 위치를 바꾸는 연산이다.

### Prefix·postfix와 compound assignment

다음은 M002 pp.57–58의 독립적인 두 초기 상태다.

```java
int x1 = 1, y1 = 1;
int prefixResult = x1 + ++y1;  // 3; y1 is now 2

int x2 = 1, y2 = 1;
int postfixResult = x2 + y2++; // 2; y2 is now 2
```

Prefix(전위) `++y1`은 바꾼 값 2를 expression에 제공한다. Postfix(후위) `y2++`는 이전 값 1을 제공하면서 저장된 값도 2로 갱신한다. 따라서 expression의 결과와 최종 variable 상태를 따로 기록해야 한다.

Compound assignment(복합 대입)는 왼쪽 variable을 읽어 계산한 결과를 그곳에 다시 저장한다. `x = 10; x += 5;` 뒤에는 15다. 같은 `int` 예에서 `x -= 3`, `x *= 3`, `x /= 3`, `x %= 3`는 각각 해당 산술 결과를 저장하고, `x &= 3`·`x |= 3`·`x ^= 3`·`x >>= 3`·`x <<= 3`도 같은 갱신 구조다. 특히 `x <<= 3`의 왼쪽 operand는 `x`이지 `3`이 아니다. 이를 모든 type에서의 단순 문자열 치환 규칙으로 받아들이지는 않는다. 두 operand를 사용하는 compound assignment를 unary라고 부른 발화도 실제 문법과 구별한다.

`x = 1, y = 2, z = 3`인 상태에서 `x = y = z`는 `x = (y = z)`로 묶인다. 안쪽 assignment가 `y`에 3을 저장하고 값 3을 내므로 `x`도 3이 된다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 29:09–30:09의 가독성 지적처럼, 이 동작을 이해하는 것과 압축식을 습관적으로 사용하는 것은 별개다.

### Precedence·associativity·evaluation order

Precedence(우선순위)는 expression의 묶임, associativity(결합 방향)는 같은 순위에서의 묶임을 정한다. Operand evaluation order(피연산자 평가 순서)는 실제 계산의 진행 순서다.

```java
int x = 5;
int y = 10;
int z = ++x + y * 3;
```

식은 `(++x) + (y * 3)`이다. Java는 왼쪽 operand부터 평가하므로 `++x`가 `x`를 6으로 바꾸고 6을 낸다. 오른쪽 곱은 `y` 자체를 바꾸지 않고 30을 낸다. 따라서 `z = 36`, 최종 `x = 6`, `y = 10`이다. “곱셈의 우선순위가 높다”를 “오른쪽 곱을 왼쪽 operand보다 반드시 먼저 실행한다”로 바꾸면 안 된다.

자료의 표에서 Java에 해당하는 묶음은 높은 쪽부터 접근·괄호, unary·cast·prefix, `* / %`, `+ -`, shifts, relational, equality, bitwise AND, XOR, OR, logical AND, logical OR, `?:`, assignment 순이다. Relational `< <= > >=`와 equality `== !=`도 다른 단계다. M002 p.74의 `sizeof`, pointer 의미의 `*`·`&`, comma operator는 C/C++ 항목이므로 Java 규칙으로 가져오지 않는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 32:03–33:02에서 increment 순위에 확신이 없었던 발화와 표의 실제 prefix 표기를 구분하며, 강의는 표 전체의 암기를 요구하지 않았으며, 복잡한 식에는 괄호로 의도를 드러내면 된다.

## String의 내용과 reference를 따로 읽기

`String`은 reference type이며 `length()`, `toUpperCase()`, `toLowerCase()`, `concat()` 같은 methods를 제공한다. M002 pp.43–45의 네 글자 예를 개인 이름 대신 `"Java"`로 바꾼 설명용 예에서 `length()`는 4, 대문자 변환 결과는 `"JAVA"`, 소문자 변환 결과는 `"java"`다. `"Java".concat("Code")`와 `"Java" + "Code"`는 모두 `"JavaCode"`다. 원자료와 마찬가지로 공백은 자동으로 추가되지 않는다.

`+`는 왼쪽부터 묶인 앞선 결과에 따라 계산이 달라진다.

```java
System.out.println(1 + "2");                       // 12
System.out.println("The answer is: " + 2 + 3 + "!"); // The answer is: 23!
System.out.println(2 + 3 + " is the answer!");       // 5 is the answer!
```

둘째 줄은 String 뒤에 2와 3을 차례로 붙이고, 셋째 줄은 정수 합 5를 먼저 만든다. 실제 literal의 colon도 출력에 포함된다. 이것을 primitive numeric widening이라고 부르면 안 되며, `println`이 String만 받는다고 생각해도 안 된다.

### Immutability와 equality

String의 immutability(불변성)는 객체의 문자 내용을 바꿀 수 없다는 뜻이다. Variable의 reference 재대입은 가능하다.

```java
String appleOne = "Apple";
String appleTwo = "Apple";
appleTwo = "Pear";
```

마지막 줄 뒤에도 `appleOne`은 `"Apple"`을 가리킨다. 기존 Apple의 문자가 Pear로 변한 것이 아니라 `appleTwo`의 reference가 달라졌다. [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 STT]] 01:15:24의 설명과 [M002 PDF pp.47–48](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)은 이 구별에 쓰인다. String Pool은 이 공유 관계를 설명하는 모델이며 특정 JVM의 물리 배치를 보장하지 않는다.

`new String("Apple")`를 두 번 호출한 별도 객체들은 내용이 같아도 `==`가 `false`다. `String.equals()`는 내용을 비교하므로 `true`다. 반면 같은 literal `"Apple"`을 가리키는 두 변수는 pooled object를 공유하여 두 비교가 모두 `true`다. 이때도 `==`는 내용 검사가 아니라 identity(동일 객체 여부) 검사다.

Primitive 비교의 `== != > < >= <=`는 boolean을 만들며 `=`는 대입이다. `=>`·`=<`·`<>`로 바꾸어 쓰지 않는다. Non-null String `a`의 내용이 `b`와 다른지 확인하려면 `!a.equals(b)`로 boolean 결과를 뒤집는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 19:41–21:36의 설명이다. Null 가능성이 있으면 [[courses/computer_programming/units/control-flow|Short-circuit 조건]]으로 receiver를 먼저 보호해야 한다. 모든 class의 `equals`가 String처럼 내용을 비교한다는 일반화는 하지 않는다.

## Scanner의 입력·반환·저장·출력

`Scanner` 예제는 String을 외부 입력과 연결한다. 다음은 M002 pp.21–22의 코드이며, `import`는 파일 앞에, 나머지 문장들은 method body에 놓는다.

```java
import java.util.*;
```

```java
Scanner scanner = new Scanner(System.in);
System.out.println("Enter username");
String userName = scanner.nextLine();
System.out.println("Username is: " + userName);
```

`scanner.nextLine()`은 한 줄 입력과 Enter를 기다린 뒤 그 줄을 String으로 반환한다. Assignment가 반환값을 `userName`에 저장하고, 다음 문장이 그 값을 출력한다. 입력·반환·저장·출력은 서로 다른 단계다. 공백을 포함한 한 줄을 요구한다면 공백 뒤 내용을 임의로 버려서는 안 된다. [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 STT]] 54:38의 입력 설명도 이 흐름에 해당한다. 여기서 사용하는 `import`와 Scanner만으로 뒤에 유보된 Packages 전체를 배운 것은 아니다.

## 핵심 정리

- Local variable은 읽기 전 대입이 필요하며 field·array component의 기본값과 다르다.
- Literal의 type과 cast 위치를 먼저 읽는다. Widening이 항상 정확한 숫자 보존을 뜻하지 않는다.
- Precedence는 묶임, evaluation order는 진행 순서다. `++`의 결과와 저장값은 따로 적는다.
- String 재대입은 문자 변경이 아니다. `==`와 `equals()`는 서로 다른 질문에 답한다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 선언·대입·이름

Method 안의 `int x;`와 `int x=10;`, 이후 `x=15;`를 구별하라. `myVar`/`myvar`, `String`, `_`와 field 기본값도 설명하라.

<details><summary>해설 보기</summary>

첫째는 선언만이어서 읽기 전 대입이 필요하고, 둘째는 선언과 초기화, 셋째는 기존 변수의 대입이다. `myVar`와 `myvar`는 서로 다른 identifier다. `String`은 class 이름이지 keyword가 아니며 수업의 JDK 11에서 단독 `_`는 유효한 identifier가 아니다. 의미 있는 소문자 시작 이름은 읽기 관례다. Field·새 array component의 기본값 규칙을 unassigned local에 적용하면 안 된다.

**확인 기준:** 선언/초기화/재대입 및 identifier 오류와 관례를 구별한다.

</details>

#### 확인 Q02 · Primitive 범위와 reference

8개 primitive를 분류하고 정수형 bits를 적어라. `byte`의 양 끝이 −128과 128일 수 없는 이유, `float`/`double` 정밀도와 긴 String reference의 의미를 설명하라.

<details><summary>해설 보기</summary>

`boolean`은 참·거짓, `char`는 문자, `byte/short/int/long`은 8/16/32/64-bit signed integers, `float/double`은 32/64-bit floating-point다. N-bit signed 범위는 −2^(N−1)부터 2^(N−1)−1이다. `byte`는 256상태라 −128…127이며 양쪽 128까지면 257개가 된다. `float` 약 6–7자리, double 약 15자리는 유효숫자이며 소수점 이하 보장 자리가 아니다. `double`은 정밀도와 더 큰 memory 비용을 함께 고려한다. String reference는 문자 내용 전체가 아니라 객체를 가리키는 값이다. Floating-point를 integral 아래 둔 자료 그림은 올바른 분류가 아니다.

**확인 기준:** 8종·bits·256개 계산·유효숫자·reference 저장을 모두 포함한다.

</details>

#### 확인 Q03 · Literal type과 cast

`float f=3.72;`, `double d=3.72f;`, `int i=1000L;`, `long l=1000;`를 각각 판정하라. `(float)testDouble`은 선언 type을 바꾸며 모든 widening은 정확한가?

<details><summary>해설 보기</summary>

첫째·셋째는 각각 double→float, long→int narrowing이라 그대로는 불가능하다. 둘째·넷째는 float→double, int→long widening이다. 값이 작아 보여도 literal type이 결정한다. Cast는 expression 값을 변환하며 `testDouble`의 선언 type은 double로 남는다. 자동 widening이어도 큰 정수→floating-point는 정밀도 한계로 반올림될 수 있다. 이 입문 사슬은 char·boolean까지의 완전한 변환표가 아니다.

**확인 기준:** 네 판정, cast 대상, widening의 한정을 적는다.

</details>

#### 확인 Q04 · 몫·나머지·혼합 연산

`5/2`, `5%2`, `15/3.0`, `2<<3`, `0b1&0b0`, `true&&false`의 결과와 type 또는 종류를 설명하라. `x+10`의 operand와 operator, `++` 분류도 적어라.

<details><summary>해설 보기</summary>

차례로 int 2, int 1, double 5.0, int 16, int 0, boolean false다. 정수 몫은 소수 부분을 버리고 `%`는 나머지다. 3.0이 mixed 계산을 double로 만들며 binary `10`의 왼쪽 3자리 이동은 `10000`이다. Bitwise AND와 boolean AND는 대상이 다르다. `x`·10이 operands, `+`가 operator이고 `++`는 unary이면서 arithmetic이다. 정수의 0 나눗셈은 오류지만 floating-point까지 같은 결론으로 확대하지 않는다.

**확인 기준:** 숫자뿐 아니라 몫/나머지와 bit/boolean 차이를 설명한다.

</details>

#### 확인 Q05 · 증가 결과와 저장 상태

각각 독립 초기값 `x=1,y=1`에서 `x + ++y`와 `x + y++`를 계산하고 최종 x,y를 적어라.

<details><summary>해설 보기</summary>

Prefix는 y를 2로 바꾼 값을 사용해 3, postfix는 이전 1을 사용해 2를 낸다. 두 경우 모두 x=1,y=2다. Postfix도 y를 바꾸므로 expression 결과가 2라고 y가 1로 남는 것은 아니다.

**확인 기준:** 각 결과와 최종 상태를 분리한다.

</details>

#### 확인 Q06 · 복합·연속 대입

`int x=10; x+=5; x<<=3;`의 중간값을 구하라. 독립적으로 x=1,y=2,z=3에서 `x=y=z`를 묶어 설명하고 복합 대입 표의 연산들을 분류하라.

<details><summary>해설 보기</summary>

x는 10→15→120이다. `x<<=3`은 이 int 예에서 x를 왼쪽 operand로 3자리 이동시켜 저장하며 `3<<x`가 아니다. `x=y=z`는 `x=(y=z)`여서 y와 x가 모두 3, z도 3이다. `+= -= *= /= %=`는 산술 결과, `&= |= ^=`는 bitwise 결과, `>>= <<=`는 shift 결과를 왼쪽 변수에 저장한다. 두 operands를 쓰는 이 문법을 unary로 분류하거나 모든 type에서 단순 문자열 치환과 같다고 일반화하지 않는다.

**확인 기준:** 120의 왼쪽 operand, 오른쪽 결합, 각 갱신 대상이 정확하다.

</details>

#### 확인 Q07 · 묶임과 평가 순서

x=5,y=10에서 `int z=++x+y*3;`를 괄호로 표시하고 평가 순서와 최종값을 설명하라. 표의 `sizeof`·pointer `*`·comma를 Java 규칙으로 사용해도 되는가?

<details><summary>해설 보기</summary>

`(++x)+(y*3)`로 묶인다. 왼쪽 ++x가 먼저 x=6과 값 6을 만들고 오른쪽 곱은 30을 만들지만 y를 바꾸지 않는다. z=36,x=6,y=10이다. Precedence는 묶임, associativity는 같은 순위의 묶임 방향, evaluation order는 진행 순서다. Relational과 equality, bitwise AND/XOR/OR, logical AND/OR도 별도 단계다. C/C++ 항목을 Java로 가져오지 않고 괄호로 의도를 드러낸다.

**확인 기준:** 곱셈 우선순위를 오른쪽 우선 평가로 혼동하지 않는다.

</details>

#### 확인 Q08 · String 연산과 출력

`"Java"`의 length·대/소문자 결과, `concat("Code")`를 적어라. `1+"2"`, `"The answer is: "+2+3+"!"`, `2+3+" is the answer!"`도 계산하라.

<details><summary>해설 보기</summary>

각각 4, `JAVA`, `java`, `JavaCode`이며 공백은 자동 삽입되지 않는다. 세 식은 String `12`, `The answer is: 23!`, `5 is the answer!`다. `+`는 왼쪽부터 묶여 String이 된 뒤에는 2와 3을 따로 붙이고, 마지막 식은 먼저 정수 합 5를 낸다. Colon은 literal 일부다. String 변환은 primitive widening과 다르고 println은 숫자도 출력할 수 있다.

**확인 기준:** 공백·colon·숫자 합과 문자열 연결을 정확히 구별한다.

</details>

#### 확인 Q09 · Immutability와 재대입

`String a="Apple", b="Apple"; b="Pear";` 뒤 a,b가 가리키는 내용을 설명하라. `b` 대입이 immutability를 깨는가?

<details><summary>해설 보기</summary>

a는 Apple, b는 Pear를 가리킨다. 마지막 대입은 b에 저장된 reference를 바꿀 뿐 기존 Apple의 문자를 수정하지 않는다. 같은 객체를 가리키던 a도 그대로 남는다. Pool의 공유 그림은 이런 관계를 설명하지만 물리 memory 배치를 보장하지 않는다.

**확인 기준:** 변경된 저장 위치를 b의 reference로 지정한다.

</details>

#### 확인 Q10 · Identity와 내용 비교

별개의 `new String("Apple")` 두 개와 같은 literal을 쓰는 두 변수를 각각 `==`·`equals()`로 비교하라. Non-null a의 내용 불일치와 올바른 primitive 비교 기호도 적어라.

<details><summary>해설 보기</summary>

별개 objects는 `==` false, `equals()` true다. 같은 pooled literal을 공유하면 둘 다 true지만 ==가 내용 검사로 바뀐 것은 아니다. Non-null a에서는 `!a.equals(b)`로 내용의 다름을 검사한다. `== != > < >= <=`가 비교이며 `=`는 대입이다. `=> =< <>`는 대체 기호가 아니다. `null` receiver는 먼저 보호해야 하며 모든 class의 equals가 String과 같은 의미를 갖지는 않는다.

**확인 기준:** 두 상황의 네 결과와 이유, non-null 전제를 포함한다.

</details>

#### 확인 Q11 · 입력에서 반환·저장·출력까지

Scanner가 `Computer Programming` 한 줄을 읽어 `String userName=scanner.nextLine();`로 저장하고 `println("Username is: "+userName)`을 실행한다. 각 단계와 출력을 설명하라.

<details><summary>해설 보기</summary>

`import java.util.*;`로 이름을 사용할 준비를 하고 method 안에서 `new Scanner(System.in)`으로 입력 객체를 만든다. nextLine은 한 줄과 Enter를 기다려 공백을 포함한 String을 반환한다. 대입이 userName에 저장하고 println이 `Username is: Computer Programming`과 줄바꿈을 출력한다. 입력·반환·대입 자체를 출력으로 혼동하면 안 되며 이 예가 Packages 전체나 모든 입력 오류를 다루지는 않는다.

**확인 기준:** 공백 보존 및 네 단계의 책임을 설명한다.

</details>

#### 확인 Q12 · 같은 단계의 결합 방향

`10-3-2`와 x=1,y=2,z=3에서 `x=y=z`의 묶임을 비교하라. 괄호를 쓰는 목적은 무엇인가?

<details><summary>해설 보기</summary>

뺄셈은 `(10-3)-2`여서 5이고 `10-(3-2)`의 9와 다르다. 대입은 `x=(y=z)`로 오른쪽 결합하여 x=y=z=3이다. Associativity는 같은 순위의 묶임을 정하며 operand 평가 순서 자체의 이름은 아니다. 괄호는 원하는 묶임을 명시해 읽기 실수를 줄인다.

**확인 기준:** 5와9의 차이와 대입의 오른쪽 결합을 설명한다.

</details>

### 적용 연습

#### 연습 P01 · 출력은 같아도 상태는 같은가

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.**
```java
int n = 2;
String a = "n=" + n++ + (n * 2);
String b = "n=" + (n + n * 2);
```
a,b와 최종 n을 구하고, 처음 식에서 괄호로 둘러싼 부분이 무엇을 바꾸는지 설명하라.

<details><summary>해설 보기</summary>

a를 만들 때 postfix가 옛 값 2를 붙이고 n을 3으로 바꾼다. `(n*2)`는 6이므로 a는 `n=26`이다. 다음 식의 괄호 안은 3+3×2=9여서 b는 `n=9`, 최종 n=3이다. 첫 식의 괄호는 곱을 숫자로 계산하지만 앞 String과 이미 결합한 2까지 합치지는 않는다. 두 번째는 합 전체를 계산한 뒤 String으로 연결한다.

**확인 기준:** n의 변화 시점과 각 +의 String/숫자 동작을 표시한다.

</details>

#### 연습 P02 · 서로 다른 두 수정 제안

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.** `float f=3.72;`와 별개로 `String a=new String("Code"), b=new String("Code");`가 있다. ‘값이 작으니 첫 줄은 맞고, a==b가 false면 글자도 다르다’라는 두 주장을 각각 고쳐라.

<details><summary>해설 보기</summary>

첫 주장은 literal type을 무시한다. `3.72`는 double이므로 float로 넣으려면 예컨대 `3.72f`를 사용하거나 해당 값에 명시적 cast를 한다. 두 번째는 identity와 내용을 혼동한다. 별도 new라 ==는 false지만 a.equals(b)는 true다. Cast는 숫자 expression의 변환이며 equals는 String 내용을 검사하므로 서로 바꿔 쓸 해결책이 아니다.

**확인 기준:** 각 오류의 원인을 type과 identity로 분리한다.

</details>

### 복습 순서

Q01–Q04로 type과 변환을 확인하고 Q05–Q08은 중간값 표를 만든다. Q09–Q12를 설명한 뒤 P01–P02를 풀고 틀린 계산 단계만 다시 추적한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|2026-09-01 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 보정 녹음문]] — 57:48, 01:01:31 (`float`/`double` 정밀도·memory 선택), 01:03:31 (정수 범위), 01:08:40, 01:15:24, 54:38.
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 보정 녹음문]] — 12:10, 04:33, 09:18, 14:06 (compound assignment의 operand 순서), 29:09–30:09 (`x = y = z`의 가독성), 32:03, 33:02, 19:41, 21:36.

### 강의자료와 해당 페이지

- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-021), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-027), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-033), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-039), [p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-042), [p.45](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-045), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-048), [p.57](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-057), [p.60](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-060), [p.61](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-061), [p.62](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-062), [p.64](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-064), [p.71](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-071), [p.73](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-073), [p.74](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-074).
- [3 java basics 2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/3.java.basics.2/page-018).
- [4 oop.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf) — [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-046), [p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-047), [p.48](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/4.oop/page-048).

정수 범위·유효숫자·local 초기화 설명은 자료의 부정확한 표현을 구별해 읽는다. C/C++ 항목이 섞인 precedence 표를 Java 전체 규칙으로 옮기지 않는다. String Pool 그림은 논리적 공유 설명이며 물리 배치 보장이 아니다. Import·Scanner 예는 Packages 전체 학습을 뜻하지 않는다.


---

[[courses/computer_programming/units/java-runtime|← 이전: Programming의 목적과 Java 실행·개발 환경]] · [[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/arrays|다음: Array의 생성·참조와 다차원 데이터 →]]
